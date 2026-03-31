"""
Configuration Django pour SDAU Zorgho
Application WebMapping - DGUHVT Burkina Faso
"""

import os
from pathlib import Path

import dj_database_url
from decouple import config
from django.core.exceptions import ImproperlyConfigured

# Configuration GDAL/GEOS selon l'environnement
if os.name == "nt":  # Windows local
    gdal_path = config("GDAL_LIBRARY_PATH", default= r"C:\Users\lenovo\Documents\DGUHVT\donnee stage\sdau_zorgho\venv\Lib\site-packages\osgeo\gdal.dll")
    geos_path = config("GEOS_LIBRARY_PATH", default= r"C:\Users\lenovo\Documents\DGUHVT\donnee stage\sdau_zorgho\venv\Lib\site-packages\osgeo\geos_c.dll")

    if gdal_path:
        GDAL_LIBRARY_PATH = gdal_path
    if geos_path:
        GEOS_LIBRARY_PATH = geos_path

    # ✅ AJOUT ICI (TRÈS IMPORTANT)
    os.environ['PROJ_LIB'] = r"C:\Users\lenovo\Documents\DGUHVT\donnee stage\sdau_zorgho\venv\Lib\site-packages\osgeo\data\proj"
    os.environ['GDAL_DATA'] = r"C:\Users\lenovo\Documents\DGUHVT\donnee stage\sdau_zorgho\venv\Lib\site-packages\osgeo\data\gdal"

else:  # Linux / Render / Docker
    GDAL_LIBRARY_PATH = config(
        "GDAL_LIBRARY_PATH",
        default="/usr/lib/x86_64-linux-gnu/libgdal.so"
    )
    GEOS_LIBRARY_PATH = config(
        "GEOS_LIBRARY_PATH",
        default="/usr/lib/x86_64-linux-gnu/libgeos_c.so"
    )

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------------------------------
# UTILITAIRES
# -----------------------------------------------------------------------------
def env_list(name, default=""):
    return [x.strip() for x in config(name, default=default).split(",") if x.strip()]


# -----------------------------------------------------------------------------
# CONFIGURATION GÉNÉRALE
# -----------------------------------------------------------------------------
AUTH_USER_MODEL = "sdau.Utilisateur"

ENV = config("ENV", default="local")  # local | production
DEBUG = config("DEBUG", default=(ENV == "local"), cast=bool)

SECRET_KEY = config("SECRET_KEY", default="")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-local-dev-only"
    else:
        raise ImproperlyConfigured("SECRET_KEY manquante en production")


# -----------------------------------------------------------------------------
# CONFIGURATION GDAL / GEOS
# -----------------------------------------------------------------------------
if os.name == "nt":  # Windows local
    osgeo_base = BASE_DIR / "venv" / "Lib" / "site-packages" / "osgeo"

    GDAL_LIBRARY_PATH = config(
        "GDAL_LIBRARY_PATH",
        default=str(osgeo_base / "gdal.dll")
    )
    GEOS_LIBRARY_PATH = config(
        "GEOS_LIBRARY_PATH",
        default=str(osgeo_base / "geos_c.dll")
    )

    os.environ.setdefault("PROJ_LIB", str(osgeo_base / "data" / "proj"))
    os.environ.setdefault("GDAL_DATA", str(osgeo_base / "data" / "gdal"))

else:  # Linux / Render / Docker
    GDAL_LIBRARY_PATH = config(
        "GDAL_LIBRARY_PATH",
        default="/usr/lib/x86_64-linux-gnu/libgdal.so"
    )
    GEOS_LIBRARY_PATH = config(
        "GEOS_LIBRARY_PATH",
        default="/usr/lib/x86_64-linux-gnu/libgeos_c.so"
    )


# -----------------------------------------------------------------------------
# HÔTES / CSRF / CORS
# -----------------------------------------------------------------------------
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "127.0.0.1,localhost")

render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if render_host and render_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(render_host)

CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS",
    "http://127.0.0.1:8000,http://localhost:8000,https://sdau-zorgho-1.onrender.com"
)

CORS_ALLOWED_ORIGINS = env_list(
    "CORS_ALLOWED_ORIGINS",
    "http://127.0.0.1:8000,http://localhost:8000"
)
CORS_ALLOW_CREDENTIALS = True


# -----------------------------------------------------------------------------
# SÉCURITÉ
# -----------------------------------------------------------------------------
# IMPORTANT :
# On le met aussi en local pour éviter le blocage OSM "Referer is required"
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

SESSION_COOKIE_AGE = config("SESSION_COOKIE_AGE", default=600, cast=int)
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

CSRF_COOKIE_SAMESITE = "Lax"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/carte/"
LOGOUT_REDIRECT_URL = "/login/"

if DEBUG:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
else:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_CONTENT_TYPE_NOSNIFF = True


# -----------------------------------------------------------------------------
# APPLICATIONS
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "rest_framework",
    "rest_framework_gis",
    "corsheaders",
    "django_filters",
    "sdau",
    "sdau_zorgho",
]


# -----------------------------------------------------------------------------
# MIDDLEWARE
# -----------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# -----------------------------------------------------------------------------
# URLS / TEMPLATES / WSGI
# -----------------------------------------------------------------------------
ROOT_URLCONF = "sdau_zorgho.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "sdau_zorgho.wsgi.application"


# -----------------------------------------------------------------------------
# BASE DE DONNÉES
# -----------------------------------------------------------------------------
#if ENV == "local":
    #DATABASES = {
        #"default": {
            #"ENGINE": "django.contrib.gis.db.backends.postgis",
            #"NAME": config("DB_NAME", default="SDAU_ZORGHOV2"),
            #"USER": config("DB_USER", default="postgres"),
            #"PASSWORD": config("DB_PASSWORD", default="12345"),
            #"HOST": config("DB_HOST", default="localhost"),
            #"PORT": config("DB_PORT", default="5432"),
            #"OPTIONS": {
               # "options": "-c search_path=public,django"
            #},
       # }
   # }
#else:
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from decouple import config

# Récupération de la variable d’environnement
SECRET_KEY = config("SECRET_KEY", default="")

if not SECRET_KEY:
    raise ImproperlyConfigured("SECRET_KEY manquante en production")

DATABASE_URL = config("DATABASE_URL", default="")

if not DATABASE_URL:
    raise ImproperlyConfigured("DATABASE_URL manquante en production")

# Configuration de la base
DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        ssl_require=True,
    )
}

# Forcer PostGIS
DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"

# Options supplémentaires (sécurité SSL)
DATABASES["default"].setdefault("OPTIONS", {})
DATABASES["default"]["OPTIONS"]["sslmode"] = "require"
    #DATABASES["default"]["OPTIONS"]["options"] = "-c search_path=public,django"


# -----------------------------------------------------------------------------
# AUTHENTIFICATION
# -----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]


# -----------------------------------------------------------------------------
# INTERNATIONALISATION
# -----------------------------------------------------------------------------
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Africa/Ouagadougou"
USE_I18N = True
USE_TZ = True


# -----------------------------------------------------------------------------
# FICHIERS STATIQUES / MEDIA
# -----------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# -----------------------------------------------------------------------------
# DRF
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
}


# -----------------------------------------------------------------------------
# DIVERS
# -----------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ZORGHO_CENTER = {
    "lat": config("ZORGHO_LAT", default=12.2500, cast=float),
    "lon": config("ZORGHO_LON", default=-0.6167, cast=float),
    "zoom": config("ZORGHO_ZOOM", default=13, cast=int),
}
