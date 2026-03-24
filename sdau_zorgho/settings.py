"""
Configuration Django pour SDAU Zorgho
Application WebMapping - DGUHVT Burkina Faso
"""
# ⚠️ IMPORTANT : Cette ligne doit être AVANT INSTALLED_APPS
AUTH_USER_MODEL = 'sdau.Utilisateur'


# Chemin vers les données PROJ (pour pyproj et GeoDjango)

from pathlib import Path
import os
from decouple import config

# Répertoires de base
BASE_DIR = Path(__file__).resolve().parent.parent
#GDAL_LIBRARY_PATH = r"C:\Users\lenovo\Documents\DGUHVT\donnee stage\sdau_zorgho\venv\Lib\site-packages\osgeo\gdal.dll"
#GEOS_LIBRARY_PATH = r"C:\Users\lenovo\Documents\DGUHVT\donnee stage\sdau_zorgho\venv\Lib\site-packages\osgeo\geos_c.dll"
import os

os.environ['GDAL_LIBRARY_PATH'] = '/usr/lib/libgdal.so'
os.environ['GEOS_LIBRARY_PATH'] = '/usr/lib/libgeos_c.so'
# Sécurité
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
# Forcer l'utilisation de PROJ depuis l'environnement virtuel
#PROJ_LIB = os.path.join(os.path.dirname(__file__), '..', 'venv', 'Lib', 'site-packages', 'osgeo', 'data', 'proj')
#os.environ['PROJ_LIB'] = PROJ_LIB



# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',  # GeoDjango
    
    # Extensions tierces
    'rest_framework',
    'rest_framework_gis',
    'corsheaders',
    'django_filters',
    
    # Applications locales
    'sdau',
  # Votre application
    'sdau_zorgho',   
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sdau_zorgho.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sdau_zorgho.wsgi.application'

# Base de données PostGIS
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config('DB_NAME', default='SDAU_ZORGHOV2'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='12345'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            'options': '-c search_path=public,django'}
    }
}
# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# AUTHENTIFICATION
# ============================================
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
# Internationalisation
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Ouagadougou'
USE_I18N = True
USE_TZ = True

# Fichiers statiques
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuration REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
}

# Configuration CORS
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:8000,http://127.0.0.1:8000'
).split(',')
CORS_ALLOW_CREDENTIALS = True

# Sessions - Déconnexion automatique après 2 minutes
SESSION_COOKIE_AGE = config('SESSION_COOKIE_AGE', default=120, cast=int)  # 2 minutes
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG  # True en production avec HTTPS
SESSION_COOKIE_SAMESITE = 'Lax'

# Type de clé primaire par défaut
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration spécifique SDAU Zorgho
ZORGHO_CENTER = {
    'lat': config('ZORGHO_LAT', default=12.2500, cast=float),
    'lon': config('ZORGHO_LON', default=-0.6167, cast=float),
    'zoom': config('ZORGHO_ZOOM', default=13, cast=int),
}

