"""
Serializers pour l'API REST SDAU Zorgho - VERSION CORRIGÉE
Support de la relation Many-to-Many Secteur-Zone
"""

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Secteur, Utilisateur, ZoneSdau

# ==========================================================
# SECTEURS
# ==========================================================

class SecteurSerializer(GeoFeatureModelSerializer):
    """Serializer pour les secteurs avec géométrie GeoJSON"""

    nb_zones = serializers.SerializerMethodField()

    class Meta:
        model = Secteur
        geo_field = 'geom'
        fields = [
            'id_secteur',
            'nom_secteur',
            'nb_zones'
        ]

    def get_nb_zones(self, obj):
        return obj.zones.count()


# ==========================================================
# ZONES SDAU (GeoJSON)
# ==========================================================

class ZoneSdauSerializer(GeoFeatureModelSerializer):
    """
    Serializer pour les zones SDAU avec géométrie GeoJSON
    Support des secteurs multiples
    """
    secteurs = serializers.SerializerMethodField()
    noms_secteurs = serializers.SerializerMethodField()
    couleur = serializers.SerializerMethodField()
    type_zone = serializers.CharField(source='get_type_zone_display')

    class Meta:
        model = ZoneSdau
        geo_field = 'geom'
        fields = [
            'id_zone',
            'zone_sdau',
            'aire_ha',
            'type_zone',
            'statut_amenagement',
            'secteurs',
            'noms_secteurs',
            'couleur'
        ]
    
    def get_secteurs(self, obj):
        """Retourne la liste des ID de secteurs"""
        return [
            {'id_secteur': s.id_secteur, 'nom_secteur': s.nom_secteur}
            for s in obj.secteurs.all()
        ]  # → Résultat dans le GeoJSON : "secteurs": [{"id": 1, "nom_secteur": "Secteur 1"}]

    def get_noms_secteurs(self, obj):
        """Retourne la liste des noms de secteurs"""
        return list(obj.secteurs.values_list('nom_secteur', flat=True))
    
    def get_couleur(self, obj):
        """Retourne la couleur cartographique de la zone"""
        return obj.get_couleur_cartographie()


# ==========================================================
# ZONES SDAU (Liste simplifiée)
# ==========================================================

class ZoneSdauListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour les listes (sans géométrie)"""

    noms_secteurs = serializers.SerializerMethodField()
    type_zone = serializers.CharField(source='get_type_zone_display')  # ✅ Affichage propre
    class Meta:
        model = ZoneSdau
        fields = [
            'id_zone',
            'zone_sdau',
            'aire_ha',
            'type_zone',
            'statut_amenagement',
            'noms_secteurs'
        ]
    
    def get_noms_secteurs(self, obj):
        """Retourne les noms des secteurs séparés par virgule"""
        return ", ".join(obj.secteurs.values_list('nom_secteur', flat=True))


# ==========================================================
# UTILISATEURS
# ==========================================================

class UtilisateurSerializer(serializers.ModelSerializer):
    """Serializer pour les utilisateurs"""
    
    class Meta:
        model = Utilisateur
        fields = [
            'id_user',
            'username',
            'email',
            'nom',
            'prenom',
            'role',
            'is_active',
            'date_joined'
        ]
        read_only_fields = ['id_user', 'date_joined']


class UtilisateurCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création d'utilisateurs"""
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = Utilisateur
        fields = [
            'username',
            'email',
            'nom',
            'prenom',
            'role',
            'password',
            'password_confirm'
        ]
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Les mots de passe ne correspondent pas.'
            })
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = Utilisateur(**validated_data)
        user.set_password(password)
        user.role = 'consultation'
        user.save()
        return user


# ==========================================================
# STATISTIQUES
# ==========================================================

class StatistiquesSerializer(serializers.Serializer):
    total_zones = serializers.IntegerField()
    superficie_totale = serializers.DecimalField(max_digits=12, decimal_places=2)
    zones_par_type = serializers.DictField()
    zones_par_statut = serializers.DictField()
    zones_par_secteur = serializers.DictField()


# ==========================================================
# TRANSFORMATION DE COORDONNÉES
# ==========================================================

class CoordinateTransformSerializer(serializers.Serializer):

    longitude = serializers.FloatField(required=True)
    latitude = serializers.FloatField(required=True)
    srid_source = serializers.IntegerField(required=True)
    srid_cible = serializers.IntegerField(required=True)

    SYSTEMES_VALIDES = [4326, 32630, 32631, 2043, 3857]

    def validate_srid_source(self, value):
        if value not in self.SYSTEMES_VALIDES:
            raise serializers.ValidationError(
                f"SRID source invalide. Systèmes supportés : {self.SYSTEMES_VALIDES}"
            )
        return value

    def validate_srid_cible(self, value):
        if value not in self.SYSTEMES_VALIDES:
            raise serializers.ValidationError(
                f"SRID cible invalide. Systèmes supportés : {self.SYSTEMES_VALIDES}"
            )
        return value

    def validate(self, data):
        srid = data['srid_source']
        lon = data['longitude']
        lat = data['latitude']

        if srid == 4326:
            if not (-180 <= lon <= 180):
                raise serializers.ValidationError({'longitude': 'Longitude invalide'})
            if not (-90 <= lat <= 90):
                raise serializers.ValidationError({'latitude': 'Latitude invalide'})

        elif srid in [32630, 32631]:
            if not (0 <= lon <= 1000000):
                raise serializers.ValidationError({'longitude': 'Coordonnée Est UTM invalide'})
            if not (0 <= lat <= 10000000):
                raise serializers.ValidationError({'latitude': 'Coordonnée Nord UTM invalide'})

        return data


# ==========================================================
# SYSTÈMES DE COORDONNÉES
# ==========================================================

class SystemeCoordonneeSerializer(serializers.Serializer):
    srid = serializers.IntegerField()
    nom = serializers.CharField()
    description = serializers.CharField()
    unite = serializers.CharField()
    zone_application = serializers.CharField()
