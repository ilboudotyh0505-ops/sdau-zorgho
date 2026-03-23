"""
Tests pour l'application SDAU Zorgho
"""

from django.test import TestCase
from django.contrib.gis.geos import MultiPolygon, Polygon
from .models import Secteur, ZoneSdau, Utilisateur


class SecteurModelTest(TestCase):
    def setUp(self):
        # Créer un secteur de test
        poly = Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0)))
        self.secteur = Secteur.objects.create(
            nom_secteur="Secteur Test",
            geom=MultiPolygon(poly)
        )
    
    def test_secteur_creation(self):
        self.assertEqual(self.secteur.nom_secteur, "Secteur Test")
        self.assertIsNotNone(self.secteur.geom)
    
    def test_secteur_str(self):
        self.assertEqual(str(self.secteur), "Secteur Test")


class ZoneSdauModelTest(TestCase):
    def setUp(self):
        # Créer un secteur
        poly = Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0)))
        self.secteur = Secteur.objects.create(
            nom_secteur="Secteur 1",
            geom=MultiPolygon(poly)
        )
        
        # Créer une zone
        self.zone = ZoneSdau.objects.create(
            zone_sdau="Zone à urbaniser en priorité",
            aire_ha=10.5,
            type_zone="Habitat",
            statut_amenagement="À créer",
            id_secteur=self.secteur,
            geom=MultiPolygon(poly)
        )
    
    def test_zone_creation(self):
        self.assertEqual(self.zone.zone_sdau, "Zone à urbaniser en priorité")
        self.assertEqual(self.zone.type_zone, "Habitat")
    
    def test_zone_couleur(self):
        couleur = self.zone.get_couleur_cartographie()
        self.assertEqual(couleur, '#FFE4B5')  # Couleur pour Habitat


class UtilisateurModelTest(TestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create_user(
            username='testuser',
            email='test@example.com',
            nom='Doe',
            prenom='John',
            password='testpass123'
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.get_full_name(), 'John Doe')
    
    def test_user_authentication(self):
        self.assertTrue(self.user.check_password('testpass123'))
