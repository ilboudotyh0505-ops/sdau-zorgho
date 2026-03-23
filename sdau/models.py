"""
Modèles GeoDjango pour SDAU Zorgho - VERSION CORRIGÉE
Relation Many-to-Many entre Secteur et ZoneSdau
"""

from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models as django_models


class Secteur(models.Model):
    """
    Secteurs administratifs de la ville de Zorgho
    Table existante : secteur
    """
    id_secteur = models.AutoField(primary_key=True)
    nom_secteur = models.CharField(max_length=100, verbose_name="Nom du secteur")
    geom = models.MultiPolygonField(srid=4326, verbose_name="Géométrie")

    class Meta:
        db_table = "secteur"
        managed = False   # 🔥 TRÈS IMPORTANT
        verbose_name = "Secteur"
        verbose_name_plural = "Secteurs"
        ordering = ['nom_secteur']

    def __str__(self):
        return self.nom_secteur
    def get_centroide(self, srid=None):
        """
        Retourne le centroïde du secteur
        
        Args:
            srid (int, optional): SRID pour la transformation
        
        Returns:
            dict: Coordonnées du centroïde
        """
        centroide = self.geom.centroid
        
        if srid and srid != 4326:
            centroide.transform(srid)
            return {'x': centroide.x, 'y': centroide.y, 'srid': srid}
        
        return {
            'longitude': centroide.x,
            'latitude': centroide.y,
            'srid': 4326
        }

class ZoneSdau(models.Model):
    """
    Zones du SDAU de Zorgho
    Table existante : zone_sdau
    """

    ZONE_SDAU_CHOICES = [
        ('Zone à urbaniser en priorité', 'Zone à urbaniser en priorité'),
        ('Zone de recasement', 'Zone de recasement'),
        ("Zone d'activité diverse à créer", "Zone d'activité diverse à créer"),
        ('Zone résidentielle de densification à viabiliser', 'Zone résidentielle de densification à viabiliser'),
        ('Zone de végétation naturelle à restaurer', 'Zone de végétation naturelle à restaurer'),
        ("Zone d'habitat planifier à créer", "Zone d'habitat planifier à créer"),
        ('Zone de requalification urbaine', 'Zone de requalification urbaine'),
        ("zone d'habitat planifieée à viabiliser et à densif", "zone d'habitat planifieée à viabiliser et à densif"),
        ("Zone d'extension de l'habitat", "Zone d'extension de l'habitat"),
        ('Zone de promotion touristique à créer', 'Zone de promotion touristique à créer'),
        ('Zone inondable non aedificandi', 'Zone inondable non aedificandi'),
        ("Zone d'affleurement granitique", "Zone d'affleurement granitique"),
        ('Zone de formation professionnelle', 'Zone de formation professionnelle'),
        ("Zone d'activité admistrative et commerciale à crée", "Zone d'activité admistrative et commerciale à crée"),
        ('Parc urbain à créer', 'Parc urbain à créer'),
        ('Zone de réserve foncière à créer', 'Zone de réserve foncière à créer'),
        ('Zone résidentielle à structurer et viabiliser', 'Zone résidentielle à structurer et viabiliser'),
        ('Zone industrielle à créer', 'Zone industrielle à créer'),
        ('zone de restructuration urbaine', 'zone de restructuration urbaine'),
        ('Zone administrative à réhabiliter', 'Zone administrative à réhabiliter'),
        ('Zone bleue de barrage et cours d\'eau', 'Zone bleue de barrage et cours d\'eau'),
        ('Zone de rénovation du bâti', 'Zone de rénovation du bâti'),
        ('Zone agropastorale familiale à conserver', 'Zone agropastorale familiale à conserver'),
        ('Zone commerciale à aménager', 'Zone commerciale à aménager'),
        ("Zone d'habitat rural à conserver", "Zone d'habitat rural à conserver"),
    ]

    TYPE_ZONE_CHOICES = [
        ('Habitat', 'Habitat'),
        ('Activités', 'Activités'),
        ('Équipements', 'Équipements'),
        ('Naturelle', 'Naturelle'),
        ('Espaces verts', 'Espaces verts'),
        ('Agricole/pastoralisme', 'Agricole/pastoralisme'),
        ('Touristique', 'Touristique'),
        ('Réserve foncière', 'Réserve foncière'),
    ]

    STATUT_AMENAGEMENT_CHOICES = [
        ('À créer', 'À créer'),
        ('À viabiliser', 'À viabiliser'),
        ('À aménager', 'À aménager'),
        ('À réhabiliter', 'À réhabiliter'),
        ('À restructurer', 'À restructurer'),
        ('À requalifier', 'À requalifier'),
        ('À restaurer', 'À restaurer'),
        ('À conserver', 'À conserver'),
        ('À protéger', 'À protéger'),
    ]

    # Dictionnaire de couleurs cartographiques par zone SDAU
    COULEURS_CARTOGRAPHIQUES = {
        # Zones d'habitat - Teintes jaunes/oranges
        'Zone à urbaniser en priorité': '#FFD700',  # Or
        'Zone de recasement': '#FFA500',  # Orange
        "Zone d'habitat planifier à créer": '#FFB347',  # Orange pastel
        'Zone résidentielle de densification à viabiliser': '#FFCC99',  # Pêche clair
        "zone d'habitat planifieée à viabiliser et à densif": '#FFE4B5',  # Moccasin
        "Zone d'extension de l'habitat": '#FFDAB9',  # PeachPuff
        'Zone de requalification urbaine': '#F4A460',  # SandyBrown
        'Zone résidentielle à structurer et viabiliser': '#DEB887',  # BurlyWood
        'zone de restructuration urbaine': '#D2691E',  # Chocolat
        'Zone de rénovation du bâti': '#CD853F',  # Peru
        "Zone d'habitat rural à conserver": '#FFE5CC',  # Beige clair
        
        # Zones d'activités - Teintes violettes/mauves
        "Zone d'activité diverse à créer": '#9370DB',  # Violet moyen
        "Zone d'activité admistrative et commerciale à crée": '#8B7AB8',  # Mauve
        'Zone industrielle à créer': '#7B68AA',  # Violet foncé
        'Zone commerciale à aménager': '#BA55D3',  # Orchidée moyenne
        
        # Équipements et services - Teintes roses/rouges
        'Zone de formation professionnelle': '#FF69B4',  # Rose vif
        'Zone administrative à réhabiliter': '#FF1493',  # Rose profond
        
        # Espaces verts et naturels - Teintes vertes
        'Zone de végétation naturelle à restaurer': '#228B22',  # Vert forêt
        'Parc urbain à créer': '#90EE90',  # Vert clair
        'Zone de réserve foncière à créer': '#98FB98',  # Vert pâle
        
        # Zones naturelles/géologiques - Teintes grises/brunes
        "Zone d'affleurement granitique": '#A9A9A9',  # Gris foncé
        'Zone inondable non aedificandi': '#4682B4',  # Bleu acier
        
        # Zones bleues - Eau
        'Zone bleue de barrage et cours d\'eau': '#1E90FF',  # Bleu Dodger
        
        # Agriculture et pastoralisme - Teintes vert olive/jaune
        'Zone agropastorale familiale à conserver': '#6B8E23',  # Olive terne
        
        # Tourisme - Teintes turquoise/cyan
        'Zone de promotion touristique à créer': '#40E0D0',  # Turquoise
    }

    id_zone = models.AutoField(primary_key=True)
    zone_sdau = models.CharField(max_length=200, choices=ZONE_SDAU_CHOICES)
    aire_ha = models.DecimalField(max_digits=10, decimal_places=2)
    type_zone = models.CharField(max_length=100, choices=TYPE_ZONE_CHOICES)
    statut_amenagement = models.CharField(max_length=100, choices=STATUT_AMENAGEMENT_CHOICES)

    secteurs = models.ManyToManyField(
        Secteur,
        through='SecteurZone',
        related_name='zones'
    )

    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        db_table = "zone_sdau"
        managed = False   # 🔥 TRÈS IMPORTANT
        ordering = ['zone_sdau']

    def __str__(self):
        secteurs_list = ", ".join([s.nom_secteur for s in self.secteurs.all()])
        return f"{self.zone_sdau} - Secteur(s): {secteurs_list}"

    def get_couleur_cartographie(self):
        """
        Retourne la couleur cartographique en format hexadécimal
        selon le type de zone SDAU
        """
        return self.COULEURS_CARTOGRAPHIQUES.get(self.zone_sdau, '#CCCCCC')  # Gris par défaut
    def transformer_geometrie(self, srid_cible):
        """
        Transforme la géométrie de la zone vers un autre système de coordonnées
        
        Args:
            srid_cible (int): SRID du système cible (ex: 32630 pour UTM Zone 30N)
        
        Returns:
            MultiPolygon: Géométrie transformée
        """
        from django.contrib.gis.geos import MultiPolygon
        
        # Cloner la géométrie pour ne pas modifier l'original
        geom_transformee = self.geom.clone()
        
        # Transformer vers le système cible
        geom_transformee.transform(srid_cible)
        
        return geom_transformee
    
    def get_centroide(self, srid=None):
        """
        Retourne le centroïde de la zone
        
        Args:
            srid (int, optional): SRID pour la transformation. 
                                  Si None, utilise le SRID original (4326)
        
        Returns:
            dict: {'longitude': float, 'latitude': float} ou {'x': float, 'y': float}
        """
        centroide = self.geom.centroid
        
        if srid and srid != 4326:
            centroide.transform(srid)
            return {'x': centroide.x, 'y': centroide.y, 'srid': srid}
        
        return {
            'longitude': centroide.x,
            'latitude': centroide.y,
            'srid': 4326
        }
    
    def get_bbox(self, srid=None):
        """
        Retourne la bounding box de la zone
        
        Args:
            srid (int, optional): SRID pour la transformation
        
        Returns:
            dict: {'min_x', 'min_y', 'max_x', 'max_y', 'srid'}
        """
        geom = self.geom
        
        if srid and srid != 4326:
            geom = self.geom.clone()
            geom.transform(srid)
        
        extent = geom.extent  # (min_x, min_y, max_x, max_y)
        
        return {
            'min_x': extent[0],
            'min_y': extent[1],
            'max_x': extent[2],
            'max_y': extent[3],
            'srid': srid or 4326
        }


class SecteurZone(models.Model):
    id_secteur = models.ForeignKey(
        Secteur,
        on_delete=models.CASCADE,
        db_column='id_secteur'
    )
    id_zone = models.ForeignKey(
        ZoneSdau,
        on_delete=models.CASCADE,
        db_column='id_zone'
    )

    class Meta:
        db_table = 'secteur_zone'
        unique_together = ('id_secteur', 'id_zone')
    

    def __str__(self):
        return f"{self.id_secteur} - {self.id_zone}"

class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('gestionnaire', 'Gestionnaire'),
        ('consultation', 'Consultation'),
    ]

    id_user = models.IntegerField(unique=True, null=True, blank=True, editable=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='consultation')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nom', 'prenom']

    class Meta:
        db_table = 'utilisateur'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new or self.id_user != self.id:
            Utilisateur.objects.filter(pk=self.pk).update(id_user=self.id)
            self.id_user = self.id

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"


class UtilisateurZone(models.Model):
    id_user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, db_column='id_user')
    id_zone = models.ForeignKey(ZoneSdau, on_delete=models.CASCADE, db_column='id_zone')

    class Meta:
        db_table = 'utilisateur_zone'
        unique_together = ['id_user', 'id_zone']

    def __str__(self):
        return f"{self.id_user.get_full_name()} - {self.id_zone.zone_sdau}"
