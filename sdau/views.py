"""
Vues API pour SDAU Zorgho - VERSION CORRIGÉE
Support filtrage multi-secteurs avec relation Many-to-Many
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging

from .models import Secteur, ZoneSdau, Utilisateur
from .serializers import (
    SecteurSerializer,
    ZoneSdauSerializer,
    ZoneSdauListSerializer,
    UtilisateurSerializer,
    UtilisateurCreateSerializer,
    StatistiquesSerializer,
    CoordinateTransformSerializer,  # ✅ NOUVEAU
    SystemeCoordonneeSerializer      # ✅ NOUVEAU
)

logger = logging.getLogger(__name__)


class SecteurViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Secteur.objects.all()
    serializer_class = SecteurSerializer
    permission_classes = [IsAuthenticated]


class ZoneSdauViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ZoneSdau.objects.prefetch_related('secteurs').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields = {
        'type_zone': ['exact'],
        'statut_amenagement': ['exact'],
    }

    search_fields = ['zone_sdau', 'type_zone', 'statut_amenagement']

    def get_queryset(self):
        queryset = super().get_queryset()
        secteurs = self.request.query_params.getlist('secteur')
        if secteurs:
            secteurs_ids = secteurs
            queryset = queryset.filter(
                secteurs__id_secteur__in=secteurs_ids
            ).distinct()
           
        nom_secteur = self.request.query_params.get('nom_secteur')
        if nom_secteur:
            queryset = queryset.filter(
                secteurs__nom_secteur__icontains=nom_secteur
            ).distinct()
        return queryset

    def get_serializer_class(self):
        if self.action == 'list' and self.request.query_params.get('format') != 'geojson':
            return ZoneSdauListSerializer
        return ZoneSdauSerializer

    @action(detail=False, methods=['get'])
    def geojson(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = ZoneSdauSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        zones = self.filter_queryset(self.get_queryset())
        zones_par_secteur = {}
        for secteur in Secteur.objects.all():
            count = secteur.zones.filter(
                id_zone__in=zones.values_list('id_zone', flat=True)
            ).count()
            zones_par_secteur[secteur.nom_secteur] = count

        stats = {
            'total_zones': zones.count(),
            'superficie_totale': zones.aggregate(
                total=Sum('aire_ha')
            )['total'] or 0,
            'zones_par_type': dict(
                zones.values('type_zone')
                .annotate(count=Count('id_zone'))
                .values_list('type_zone', 'count')
            ),
            'zones_par_statut': dict(
                zones.values('statut_amenagement')
                .annotate(count=Count('id_zone'))
                .values_list('statut_amenagement', 'count')
            ),
            'zones_par_secteur': zones_par_secteur,
        }

        serializer = StatistiquesSerializer(stats)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def choix(self, request):
        secteurs_data = [
            {'id': s.id_secteur, 'nom': s.nom_secteur} 
            for s in Secteur.objects.all()
        ]
        return Response({
            'types_zone': [choice[0] for choice in ZoneSdau.TYPE_ZONE_CHOICES],
            'statuts_amenagement': [choice[0] for choice in ZoneSdau.STATUT_AMENAGEMENT_CHOICES],
            'secteurs': secteurs_data,
        })
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def point_info(self, request):
        try:
            from django.contrib.gis.geos import Point

            # Récupération et validation des coordonnées
            try:
                longitude = float(request.data.get('longitude'))
                latitude = float(request.data.get('latitude'))
            except (TypeError, ValueError):
                return Response(
                    {'error': 'Coordonnées invalides. Veuillez entrer des nombres valides.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not (-180 <= longitude <= 180):
                return Response(
                    {'error': 'Longitude doit être entre -180 et 180 degrés.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not (-90 <= latitude <= 90):
                return Response(
                    {'error': 'Latitude doit être entre -90 et 90 degrés.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Limites Burkina Faso
            BF_LON_MIN, BF_LON_MAX = -5.5, 2.5
            BF_LAT_MIN, BF_LAT_MAX = 9.5, 15.1

            if not (BF_LON_MIN <= longitude <= BF_LON_MAX and BF_LAT_MIN <= latitude <= BF_LAT_MAX):
                return Response({
                    'success': True,
                    'zone_trouvee': False,
                    'message': 'Les coordonnées sont en dehors du Burkina Faso',
                    'coordonnees': {'longitude': longitude, 'latitude': latitude},
                    'suggestion': 'Vérifiez que vous utilisez le bon système de coordonnées (WGS84)'
                }, status=status.HTTP_200_OK)

            point = Point(longitude, latitude, srid=4326)
            zones = ZoneSdau.objects.filter(geom__contains=point).prefetch_related('secteurs')

            if zones.exists():
                zone = zones.first()
                return Response({
                    'success': True,
                    'zone_trouvee': True,
                    'zone': {
                        'zone_sdau': zone.zone_sdau,
                        'type_zone': zone.type_zone,
                        'statut_amenagement': zone.statut_amenagement,
                        'aire_ha': float(zone.aire_ha),
                        'secteurs': [s.nom_secteur for s in zone.secteurs.all()],
                        'couleur': zone.get_couleur_cartographie()
                    },
                    'coordonnees': {'longitude': longitude, 'latitude': latitude, 'srid': 4326}
                })
            else:
                from django.contrib.gis.db.models.functions import Distance

                zone_proche = ZoneSdau.objects.annotate(distance=Distance('geom', point)).order_by('distance').first()
                distance_m = zone_proche.distance.m if zone_proche else None

                return Response({
                    'success': True,
                    'zone_trouvee': False,
                    'message': 'Aucune zone trouvée pour ces coordonnées',
                    'coordonnees': {'longitude': longitude, 'latitude': latitude},
                    'zone_proche': {
                        'nom': zone_proche.zone_sdau if zone_proche else None,
                        'distance_metres': round(distance_m, 2) if distance_m else None
                    } if zone_proche else None
                })

        except Exception as e:
            logger.error(f"Erreur lors de la recherche de point: {str(e)}")
            return Response({'error': f'Erreur serveur: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CoordinateTransformViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def transform(self, request):
        serializer = CoordinateTransformSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            from django.contrib.gis.geos import Point

            data = serializer.validated_data
            point_source = Point(data['longitude'], data['latitude'], srid=data['srid_source'])
            point_source.transform(data['srid_cible'])

            coords_transformees = {'x': point_source.x, 'y': point_source.y, 'srid': data['srid_cible']}
            if data['srid_cible'] == 4326:
                coords_transformees['longitude'] = point_source.x
                coords_transformees['latitude'] = point_source.y
            else:
                coords_transformees['est'] = point_source.x
                coords_transformees['nord'] = point_source.y

            return Response({
                'success': True,
                'coordonnees_source': {'x': data['longitude'], 'y': data['latitude'], 'srid': data['srid_source']},
                'coordonnees_cible': coords_transformees,
                'systeme_source': self._get_nom_systeme(data['srid_source']),
                'systeme_cible': self._get_nom_systeme(data['srid_cible'])
            })
        except Exception as e:
            logger.error(f"Erreur transformation coordonnées: {str(e)}")
            return Response({'error': f'Erreur lors de la transformation: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def systemes(self, request):
        systemes = [
            {'srid': 4326, 'nom': 'WGS84', 'description': 'Système GPS mondial (latitude/longitude)',
             'unite': 'degrés décimaux', 'zone_application': 'Monde entier', 'exemple': 'Longitude: -0.6167, Latitude: 12.2500'},
            {'srid': 32630, 'nom': 'UTM Zone 30N', 'description': 'Universal Transverse Mercator Zone 30 Nord',
             'unite': 'mètres', 'zone_application': 'Burkina Faso (partie Ouest)', 'exemple': 'Est: 750000, Nord: 1350000'},
            {'srid': 32631, 'nom': 'UTM Zone 31N', 'description': 'Universal Transverse Mercator Zone 31 Nord',
             'unite': 'mètres', 'zone_application': 'Burkina Faso (partie Est)', 'exemple': 'Est: 250000, Nord: 1350000'},
            {'srid': 2043, 'nom': 'Adindan UTM Zone 30N', 'description': 'Système géodésique Adindan (datum local)',
             'unite': 'mètres', 'zone_application': 'Afrique de l\'Ouest', 'exemple': 'Est: 750000, Nord: 1350000'},
            {'srid': 3857, 'nom': 'Web Mercator', 'description': 'Projection Mercator pour cartographie web',
             'unite': 'mètres', 'zone_application': 'Cartographie web (Google Maps, OpenStreetMap)', 'exemple': 'X: -68700, Y: 1371000'}
        ]
        return Response({
            'systemes': systemes,
            'systeme_actuel': 4326,
            'recommandation': 'Utilisez UTM Zone 30N (32630) pour des mesures précises au Burkina Faso Ouest'
        })

    @action(detail=False, methods=['post'])
    def batch_transform(self, request):
        from django.contrib.gis.geos import Point
        points = request.data.get('points', [])
        srid_source = request.data.get('srid_source')
        srid_cible = request.data.get('srid_cible')

        if not points or not srid_source or not srid_cible:
            return Response({'error': 'Paramètres requis : points, srid_source, srid_cible'},
                            status=status.HTTP_400_BAD_REQUEST)
        if len(points) > 1000:
            return Response({'error': 'Maximum 1000 points par requête'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            resultats = []
            for idx, point_data in enumerate(points):
                lon = point_data.get('longitude')
                lat = point_data.get('latitude')
                if lon is None or lat is None:
                    resultats.append({'index': idx, 'error': 'Coordonnées manquantes'})
                    continue
                point = Point(lon, lat, srid=srid_source)
                point.transform(srid_cible)
                result = {'index': idx, 'source': {'longitude': lon, 'latitude': lat}, 'cible': {'x': point.x, 'y': point.y}}
                if srid_cible == 4326:
                    result['cible']['longitude'] = point.x
                    result['cible']['latitude'] = point.y
                else:
                    result['cible']['est'] = point.x
                    result['cible']['nord'] = point.y
                resultats.append(result)

            return Response({'success': True, 'total': len(points),
                             'transformes': len([r for r in resultats if 'error' not in r]),
                             'resultats': resultats})
        except Exception as e:
            logger.error(f"Erreur transformation batch: {str(e)}")
            return Response({'error': f'Erreur: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _get_nom_systeme(self, srid):
        noms = {4326: 'WGS84 (GPS)', 32630: 'UTM Zone 30N', 32631: 'UTM Zone 31N', 2043: 'Adindan UTM Zone 30N', 3857: 'Web Mercator'}
        return noms.get(srid, f'SRID {srid}')


class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UtilisateurCreateSerializer
        return UtilisateurSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UtilisateurSerializer(request.user)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Email et mot de passe requis'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Utilisateur.objects.get(email=email)
            if user.check_password(password):
                if user.is_active:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    serializer = UtilisateurSerializer(user)
                    return Response({'message': 'Connexion réussie', 'user': serializer.data})
                return Response({'error': 'Compte désactivé'}, status=status.HTTP_403_FORBIDDEN)
            return Response({'error': 'Email ou mot de passe incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
        except Utilisateur.DoesNotExist:
            return Response({'error': 'Email ou mot de passe incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({'error': 'Erreur serveur lors de la connexion'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return Response({'message': 'Déconnexion réussie'})

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UtilisateurCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Compte créé avec succès'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def check(self, request):
        if request.user.is_authenticated:
            serializer = UtilisateurSerializer(request.user)
            return Response({'authenticated': True, 'user': serializer.data})
        return Response({'authenticated': False})
