"""
Configuration des URLs pour SDAU Zorgho
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from sdau.views import (
    AuthViewSet,
    CoordinateTransformViewSet,
    SecteurViewSet,
    UtilisateurViewSet,
    ZoneSdauViewSet,
)

# Router pour l'API REST
router = DefaultRouter()
router.register(r'secteurs', SecteurViewSet, basename='secteur')
router.register(r'zones', ZoneSdauViewSet, basename='zone')
router.register(r'utilisateurs', UtilisateurViewSet, basename='utilisateur')
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'coordinates', CoordinateTransformViewSet, basename='coordinates')  # ✅ NOUVEAU

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('sdau.urls_frontend')),  # URLs frontend
    path('administration/', admin.site.urls),
]

