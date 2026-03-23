# Application WebMapping SDAU Zorgho

Application de géolocalisation des zones du Schéma Directeur d'Aménagement et d'Urbanisme (SDAU) de la ville de Zorgho, Province du Ganzourgou, Région du Centre-Est, Burkina Faso.

## 🏛️ Institution

**Direction Générale de l'Urbanisme, de l'Habitat, de la Viabilisation et de la Topographie (DGUHVT)**
Ministère de l'Urbanisme et de l'Habitat - Burkina Faso

## 🎓 Développeur

Étudiant en Géomatique - Université Virtuelle
Email: ilboudotyh0505@gmail.com

## 🚀 Technologies utilisées

- **Backend**: Django 4.2.7 avec GeoDjango
- **Base de données**: PostgreSQL avec extension PostGIS
- **Frontend**: HTML5, CSS3, JavaScript ES6
- **Cartographie**: Leaflet.js
- **Python**: 3.11

## 📋 Prérequis

- Python 3.11+
- PostgreSQL 13+ avec PostGIS
- GDAL/GEOS (librairies géospatiales)
- Visual Studio Code (recommandé)

## 🔧 Installation

### 1. Cloner le projet

```bash
cd sdau_zorgho
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Installer GDAL (important pour GeoDjango)

**Windows:**
1. Télécharger OSGeo4W: https://trac.osgeo.org/osgeo4w/
2. Installer GDAL, GEOS et PROJ
3. Ajouter au PATH: `C:\OSGeo4W\bin`

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install gdal-bin libgdal-dev python3-gdal
sudo apt-get install binutils libproj-dev
```

### 4. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

### 5. Configurer PostgreSQL/PostGIS

```sql
-- Se connecter à PostgreSQL
psql -U postgres

-- Créer l'extension PostGIS (si pas déjà fait)
CREATE EXTENSION postgis;

-- Vérifier la connexion à la base SDAU_ZORGHOV2
\c SDAU_ZORGHOV2
SELECT PostGIS_version();
```

### 6. Configurer les variables d'environnement

Copier `.env.example` vers `.env` et remplir les informations:

```bash
cp .env.example .env
```

Éditer `.env`:
```
DB_NAME=SDAU_ZORGHOV2
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
SECRET_KEY=votre_clé_secrète_django
```

### 7. Appliquer les migrations

```bash
# Vérifier que Django peut se connecter à la base
python manage.py inspectdb

# Les tables existent déjà, pas besoin de créer de migrations
# Créer un superutilisateur
python manage.py createsuperuser
```

## 🎯 Lancement de l'application

```bash
# Démarrer le serveur de développement
python manage.py runserver

# L'application sera accessible sur:
# http://127.0.0.1:8000/
```

## 📱 Utilisation

### Connexion
1. Accéder à http://127.0.0.1:8000/login/
2. Se connecter avec vos identifiants
3. Vous serez redirigé vers la carte interactive

### Fonctionnalités disponibles

#### Visualisation
- **Carte interactive** avec fonds de carte multiples (OpenStreetMap, Satellite, CartoDB)
- **Légende dynamique** par type de zone
- **Nord géographique** visible
- **Échelle** cartographique

#### Recherche et filtres
- Recherche textuelle dans les noms de zones
- Filtrage par **secteur** (Secteur 1 à 6)
- Filtrage par **type de zone** (Habitat, Activités, Équipements, etc.)
- Filtrage par **statut d'aménagement** (À créer, À viabiliser, etc.)

#### Interaction
- **Zoom/Dézoom** avec molette ou boutons
- **Info-bulles** au survol des zones
- **Popups** détaillées au clic
- **Contrôle de transparence** des zones
- **Tableau de bord** repliable

#### Statistiques
- Nombre total de zones
- Superficie totale en hectares
- Statistiques par type et statut

### Sécurité
- **Déconnexion automatique** après 2 minutes d'inactivité
- Authentification requise pour accéder à la carte
- Sessions sécurisées

## 📊 Structure de la base de données

### Table `secteur`
- `id_secteur` (PK) : Identifiant unique
- `nom_secteur` : Nom du secteur (Secteur 1 à 6)
- `geom` : Géométrie MultiPolygon (SRID 4326)

### Table `zone_sdau`
- `id_zone` (PK) : Identifiant unique
- `zone_sdau` : Type de zone SDAU (25 valeurs possibles)
- `aire_ha` : Superficie en hectares
- `type_zone` : Catégorie (Habitat, Activités, etc.)
- `statut_amenagement` : Statut (À créer, À viabiliser, etc.)
- `id_secteur` (FK) : Référence au secteur
- `geom` : Géométrie MultiPolygon (SRID 4326)

### Table `utilisateur`
- `id_user` (PK) : Identifiant unique
- `nom`, `prenom` : Identité
- `email` : Email unique
- `role` : admin, gestionnaire, consultation

### Table `utilisateur_zone`
- Table de liaison Many-to-Many
- `id_user` (FK), `id_zone` (FK)

## 🎨 Charte graphique

- **Couleur primaire**: #2C5F8D (Bleu institutionnel)
- **Couleur secondaire**: #6CA6CD (Bleu clair)
- **Couleur accent**: #FFA500 (Orange)
- **Fond blanc**: Pages d'authentification
- **Fond bleu-blanc**: Page de carte

### Couleurs cartographiques (normes urbaines)
- **Habitat**: #FFE4B5 (Jaune pâle)
- **Activités**: #FFA07A (Saumon)
- **Équipements**: #87CEEB (Bleu ciel)
- **Naturelle**: #90EE90 (Vert clair)
- **Espaces verts**: #228B22 (Vert forêt)
- **Agricole/pastoralisme**: #F0E68C (Kaki)
- **Touristique**: #DDA0DD (Prune)
- **Réserve foncière**: #D3D3D3 (Gris clair)

## 🔌 API REST

### Endpoints disponibles

#### Authentification
- `POST /api/auth/login/` - Connexion
- `POST /api/auth/logout/` - Déconnexion
- `POST /api/auth/register/` - Inscription
- `GET /api/auth/check/` - Vérifier l'authentification

#### Zones SDAU
- `GET /api/zones/` - Liste des zones (avec filtres)
- `GET /api/zones/{id}/` - Détail d'une zone
- `GET /api/zones/geojson/` - Export GeoJSON
- `GET /api/zones/statistiques/` - Statistiques globales
- `GET /api/zones/choix/` - Options de filtres

#### Secteurs
- `GET /api/secteurs/` - Liste des secteurs
- `GET /api/secteurs/{id}/` - Détail d'un secteur

#### Utilisateurs
- `GET /api/utilisateurs/me/` - Utilisateur connecté
- `GET /api/utilisateurs/` - Liste des utilisateurs
- `POST /api/utilisateurs/` - Créer un utilisateur

## 🐛 Dépannage

### Erreur GDAL
```python
# Dans settings.py, vérifier les chemins:
if os.name == 'nt':  # Windows
    GDAL_LIBRARY_PATH = r'C:\OSGeo4W\bin\gdal304.dll'
    GEOS_LIBRARY_PATH = r'C:\OSGeo4W\bin\geos_c.dll'
```

### Erreur de connexion PostgreSQL
```bash
# Vérifier que PostgreSQL est démarré
# Vérifier les credentials dans .env
# Tester la connexion:
psql -U postgres -d SDAU_ZORGHOV2
```

### Erreur PostGIS
```sql
-- Activer l'extension dans la base
CREATE EXTENSION IF NOT EXISTS postgis;
```

## 📞 Support

Pour toute question ou assistance:
- Email: ilboudotyh0505@gmail.com
- Institution: DGUHVT - Burkina Faso

## 📄 Licence

Projet développé dans le cadre d'un stage académique pour la DGUHVT.
© 2024 - Université Virtuelle en Géomatique

---

**Fait avec ❤️ pour l'aménagement urbain du Burkina Faso** 🇧🇫
