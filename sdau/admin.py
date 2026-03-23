"""
Configuration de l'administration Django pour SDAU Zorgho
"""

from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Secteur, ZoneSdau, Utilisateur, UtilisateurZone, SecteurZone


# ============================================
# Admin Utilisateur (personnalisé)
# ============================================
@admin.register(Utilisateur)
class UtilisateurAdmin(BaseUserAdmin):
    """
    Administration des utilisateurs personnalisés
    """
    
    list_display = ['get_full_name', 'email', 'nom', 'prenom', 'role', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['email', 'nom', 'prenom', 'username']
    ordering = ['nom', 'prenom']
    
    fieldsets = (
        ('Informations de connexion', {
            'fields': ('username', 'email', 'password')
        }),
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'role')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Création d\'utilisateur', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'nom', 'prenom', 'password1', 'password2', 'role'),
        }),
    )
    
    readonly_fields = ['last_login', 'date_joined']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Nom complet'


# ============================================
# Admin Secteur (avec carte)
# ============================================
@admin.register(Secteur)
class SecteurAdmin(gis_admin.GISModelAdmin):
    """
    Administration des secteurs avec carte interactive
    """
    
    list_display = ['id_secteur', 'nom_secteur']
    search_fields = ['nom_secteur']
    ordering = ['nom_secteur']
    
    default_lon = -0.6167
    default_lat = 12.2500
    default_zoom = 12
    
    gis_widget_kwargs = {
        'attrs': {
            'default_lon': default_lon,
            'default_lat': default_lat,
            'default_zoom': default_zoom,
        },
    }
    
    


# ============================================
# Admin ZoneSdau (avec carte)
# ============================================
@admin.register(ZoneSdau)
class ZoneSdauAdmin(gis_admin.GISModelAdmin):
    """
    Administration des zones SDAU avec carte interactive
    """
    
    list_display = ['id_zone', 'zone_sdau', 'type_zone', 'statut_amenagement', 'aire_ha', 'get_secteurs_display']
    list_filter = ['type_zone', 'statut_amenagement']
    search_fields = ['zone_sdau', 'type_zone', 'statut_amenagement']
    ordering = ['zone_sdau']
    list_per_page = 50
    
    default_lon = -0.6167
    default_lat = 12.2500
    default_zoom = 13
    
    gis_widget_kwargs = {
        'attrs': {
            'default_lon': default_lon,
            'default_lat': default_lat,
            'default_zoom': default_zoom,
        },
    }
    
    readonly_fields = ['aire_ha']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('zone_sdau', 'type_zone', 'statut_amenagement')
        }),
        ('Données géographiques', {
            'fields': ('aire_ha', 'geom')
        }),
    )
    
    def get_secteurs_display(self, obj):
        """Affiche la liste des secteurs dans l'admin"""
        return ", ".join([s.nom_secteur for s in obj.secteurs.all()])
    
    get_secteurs_display.short_description = "Secteurs"


@admin.register(SecteurZone)
class SecteurZoneAdmin(admin.ModelAdmin):
    """
    Administration de la table de jonction Secteur-Zone
    """
    list_display = ['id', 'id_secteur', 'id_zone']
    list_filter = ['id_secteur']
    search_fields = [
        'id_secteur__nom_secteur',
        'id_zone__zone_sdau'
    ]
    raw_id_fields = ['id_secteur', 'id_zone']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('id_secteur', 'id_zone')


# ============================================
# Admin UtilisateurZone (liaison)
# ============================================
@admin.register(UtilisateurZone)
class UtilisateurZoneAdmin(admin.ModelAdmin):
    """
    Administration des assignations utilisateur-zone
    """
    
    list_display = ['id', 'id_user', 'id_zone']
    list_filter = ['id_user__role']
    search_fields = [
        'id_user__nom', 
        'id_user__prenom', 
        'id_user__email',
        'id_zone__zone_sdau'
    ]
    
    autocomplete_fields = ['id_user', 'id_zone']
    
    fieldsets = (
        ('Assignation', {
            'fields': ('id_user', 'id_zone')
        }),
    )


# ============================================
# Configuration globale de l'admin
# ============================================
ZoneSdauAdmin.search_fields = ['zone_sdau', 'type_zone']
UtilisateurAdmin.search_fields = ['email', 'nom', 'prenom', 'username']

admin.site.site_header = "Administration SDAU Zorgho"
admin.site.site_title = "SDAU Zorgho"
admin.site.index_title = "Tableau de bord - Gestion du Schéma Directeur"
