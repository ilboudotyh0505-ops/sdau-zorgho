"""
Tests pour la transformation de coordonnées
"""

from django.test import TestCase
from django.contrib.gis.geos import Point
from rest_framework.test import APIClient
from rest_framework import status


class CoordinateTransformTestCase(TestCase):
    """Tests pour la transformation de systèmes de coordonnées"""
    
    def setUp(self):
        self.client = APIClient()
        # Vous devrez créer un utilisateur de test authentifié
    
    def test_transform_wgs84_to_utm(self):
        """Test transformation WGS84 vers UTM"""
        data = {
            'longitude': -0.6167,
            'latitude': 12.2500,
            'srid_source': 4326,
            'srid_cible': 32630
        }
        
        response = self.client.post('/api/coordinates/transform/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('coordonnees_cible', response.data)
    
    def test_transform_invalid_srid(self):
        """Test avec SRID invalide"""
        data = {
            'longitude': -0.6167,
            'latitude': 12.2500,
            'srid_source': 9999,  # SRID invalide
            'srid_cible': 4326
        }
        
        response = self.client.post('/api/coordinates/transform/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_systemes(self):
        """Test récupération liste des systèmes"""
        response = self.client.get('/api/coordinates/systemes/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('systemes', response.data)
        self.assertGreater(len(response.data['systemes']), 0)
    
    def test_batch_transform(self):
        """Test transformation par lot"""
        data = {
            'points': [
                {'longitude': -0.6167, 'latitude': 12.2500},
                {'longitude': -0.6200, 'latitude': 12.2600}
            ],
            'srid_source': 4326,
            'srid_cible': 32630
        }
        
        response = self.client.post('/api/coordinates/batch_transform/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], 2)
