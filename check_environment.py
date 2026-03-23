"""
Script de vérification de l'environnement SDAU Zorgho
Exécuter avant de lancer l'application
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Vérifier la version de Python"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("  ⚠️  Attention : Python 3.11+ recommandé")
        return False
    return True

def check_module(module_name, package_name=None):
    """Vérifier si un module Python est installé"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"✓ {package_name} installé")
        return True
    except ImportError:
        print(f"✗ {package_name} NON installé - pip install {package_name}")
        return False

def check_gdal():
    """Vérifier GDAL/GEOS"""
    try:
        from osgeo import gdal, ogr, osr
        print(f"✓ GDAL {gdal.__version__} installé")
        return True
    except ImportError:
        print("✗ GDAL NON installé")
        print("  → Windows: Installer OSGeo4W depuis https://trac.osgeo.org/osgeo4w/")
        print("  → Linux: sudo apt-get install gdal-bin libgdal-dev python3-gdal")
        return False

def check_postgres_connection():
    """Vérifier la connexion PostgreSQL"""
    try:
        import psycopg2
        from decouple import config
        
        conn = psycopg2.connect(
            dbname=config('DB_NAME', default='SDAU_ZORGHOV2'),
            user=config('DB_USER', default='postgres'),
            password=config('DB_PASSWORD', default=''),
            host=config('DB_HOST', default='localhost'),
            port=config('DB_PORT', default='5432')
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✓ PostgreSQL connecté")
        
        # Vérifier PostGIS
        cursor.execute("SELECT PostGIS_version();")
        postgis_version = cursor.fetchone()[0]
        print(f"✓ PostGIS {postgis_version} activé")
        
        # Vérifier les tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['secteur', 'zone_sdau']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"  ⚠️  Tables manquantes : {', '.join(missing_tables)}")
        else:
            print(f"✓ Tables principales présentes : secteur, zone_sdau")
            
            # Compter les enregistrements
            cursor.execute("SELECT COUNT(*) FROM secteur;")
            secteur_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM zone_sdau;")
            zone_count = cursor.fetchone()[0]
            
            print(f"  • {secteur_count} secteurs")
            print(f"  • {zone_count} zones SDAU")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Erreur de connexion PostgreSQL : {e}")
        print("  → Vérifier le fichier .env")
        print("  → Vérifier que PostgreSQL est démarré")
        return False

def check_env_file():
    """Vérifier la présence du fichier .env"""
    env_path = Path('.env')
    if env_path.exists():
        print("✓ Fichier .env présent")
        return True
    else:
        print("✗ Fichier .env MANQUANT")
        print("  → Copier .env.example vers .env")
        print("  → Configurer les variables dans .env")
        return False

def check_directories():
    """Vérifier les répertoires nécessaires"""
    required_dirs = ['templates', 'static', 'sdau', 'sdau_zorgho']
    all_present = True
    
    for dirname in required_dirs:
        dir_path = Path(dirname)
        if dir_path.exists():
            print(f"✓ Répertoire {dirname}/ présent")
        else:
            print(f"✗ Répertoire {dirname}/ MANQUANT")
            all_present = False
    
    return all_present

def main():
    print("=" * 60)
    print("VÉRIFICATION DE L'ENVIRONNEMENT - SDAU ZORGHO")
    print("=" * 60)
    print()
    
    checks = []
    
    # Vérifications
    print("1. Version de Python")
    checks.append(check_python_version())
    print()
    
    print("2. Structure des fichiers")
    checks.append(check_env_file())
    checks.append(check_directories())
    print()
    
    print("3. Modules Python essentiels")
    checks.append(check_module('django', 'Django'))
    checks.append(check_module('rest_framework', 'djangorestframework'))
    checks.append(check_module('corsheaders', 'django-cors-headers'))
    checks.append(check_module('decouple', 'python-decouple'))
    print()
    
    print("4. Modules géospatiaux")
    checks.append(check_gdal())
    checks.append(check_module('shapely', 'Shapely'))
    print()
    
    print("5. Base de données PostgreSQL")
    checks.append(check_module('psycopg2', 'psycopg2-binary'))
    if checks[-1]:  # Si psycopg2 est installé
        checks.append(check_postgres_connection())
    print()
    
    # Résumé
    print("=" * 60)
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"✅ SUCCÈS : Tous les tests passés ({passed}/{total})")
        print()
        print("Vous pouvez maintenant lancer l'application :")
        print("  • Windows : start.bat")
        print("  • Linux/Mac : ./start.sh")
        print("  • Manuel : python manage.py runserver")
    else:
        print(f"⚠️  ATTENTION : {total - passed} test(s) échoué(s) sur {total}")
        print()
        print("Veuillez corriger les problèmes ci-dessus avant de continuer.")
        print("Consultez le fichier INSTALLATION.md pour plus de détails.")
    
    print("=" * 60)
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
