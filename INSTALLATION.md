# Guide d'installation pas à pas - SDAU Zorgho

Ce guide vous accompagne étape par étape pour installer et démarrer l'application WebMapping SDAU Zorgho.

## 📋 Checklist des prérequis

Avant de commencer, assurez-vous d'avoir :

- [ ] Windows 10/11, Linux ou macOS
- [ ] Python 3.11+ installé
- [ ] PostgreSQL 13+ installé avec extension PostGIS
- [ ] Visual Studio Code (recommandé)
- [ ] Connexion internet pour télécharger les dépendances

---

## 🔧 Étape 1 : Installation de PostgreSQL et PostGIS

### Windows

1. **Télécharger PostgreSQL** :
   - Aller sur https://www.postgresql.org/download/windows/
   - Télécharger la version 13 ou supérieure
   - Lancer l'installateur

2. **Lors de l'installation** :
   - Définir le mot de passe pour l'utilisateur `postgres` (notez-le !)
   - Port : laisser 5432
   - Cocher "PostGIS" dans les composants additionnels

3. **Vérifier l'installation** :
   ```cmd
   psql --version
   ```

### Linux (Ubuntu/Debian)

```bash
# Installer PostgreSQL et PostGIS
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib postgis

# Démarrer PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Se connecter
sudo -u postgres psql
```

---

## 🗺️ Étape 2 : Installation de GDAL et GEOS

### Windows

1. **Télécharger OSGeo4W** :
   - Aller sur https://trac.osgeo.org/osgeo4w/
   - Télécharger OSGeo4W Network Installer (64-bit)

2. **Installer** :
   - Choisir "Express Desktop Install"
   - Installer GDAL, GEOS, PROJ

3. **Ajouter au PATH** :
   - Panneau de configuration → Système → Variables d'environnement
   - Ajouter `C:\OSGeo4W64\bin` au PATH

4. **Vérifier** :
   ```cmd
   gdalinfo --version
   ```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get install gdal-bin libgdal-dev
sudo apt-get install python3-gdal
sudo apt-get install binutils libproj-dev

# Vérifier
gdalinfo --version
```

---

## 🐍 Étape 3 : Créer la base de données

1. **Se connecter à PostgreSQL** :
   ```bash
   # Windows
   psql -U postgres

   # Linux
   sudo -u postgres psql
   ```

2. **Créer la base (si elle n'existe pas déjà)** :
   ```sql
   -- Vérifier si la base existe
   \l

   -- Si SDAU_ZORGHOV2 n'existe pas, la créer :
   CREATE DATABASE "SDAU_ZORGHOV2";

   -- Se connecter à la base
   \c SDAU_ZORGHOV2

   -- Activer PostGIS
   CREATE EXTENSION IF NOT EXISTS postgis;

   -- Vérifier PostGIS
   SELECT PostGIS_version();

   -- Quitter
   \q
   ```

3. **Vérifier les tables existantes** :
   ```sql
   \c SDAU_ZORGHOV2
   \dt

   -- Vous devriez voir :
   -- secteur
   -- zone_sdau
   -- utilisateur (si déjà créée)
   -- utilisateur_zone (si déjà créée)
   ```

---

## 📦 Étape 4 : Configuration du projet Django

1. **Extraire le projet** :
   - Placer le dossier `sdau_zorgho` dans un emplacement accessible
   - Par exemple : `C:\Users\VotreNom\Documents\sdau_zorgho`

2. **Ouvrir dans Visual Studio Code** :
   ```bash
   cd C:\Users\VotreNom\Documents\sdau_zorgho
   code .
   ```

3. **Créer l'environnement virtuel** :
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Installer les dépendances** :
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

   ⚠️ **Si erreur avec GDAL** :
   - Windows : Télécharger wheel depuis https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal
   - Installer avec : `pip install GDAL-3.x.x-cp311-cp311-win_amd64.whl`

---

## ⚙️ Étape 5 : Configuration des variables d'environnement

1. **Copier le fichier d'exemple** :
   ```bash
   # Windows
   copy .env.example .env

   # Linux/Mac
   cp .env.example .env
   ```

2. **Éditer le fichier `.env`** :
   ```ini
   DB_NAME=SDAU_ZORGHOV2
   DB_USER=postgres
   DB_PASSWORD=votre_mot_de_passe_postgres
   DB_HOST=localhost
   DB_PORT=5432

   SECRET_KEY=changez-cette-cle-secrete-en-production
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   SESSION_COOKIE_AGE=120  # 2 minutes

   ZORGHO_LAT=12.2500
   ZORGHO_LON=-0.6167
   ZORGHO_ZOOM=13
   ```

3. **Vérifier les chemins GDAL (Windows seulement)** :
   
   Éditer `sdau_zorgho/settings.py` si nécessaire :
   ```python
   if os.name == 'nt':  # Windows
       GDAL_LIBRARY_PATH = r"C:\Users\lenovo\Documents\DGUHVT\donnee stage\sdau_zorgho\venv\Lib\site-packages\osgeo\gdal.dll"
       GEOS_LIBRARY_PATH = r"C:\Users\lenovo\Documents\DGUHVT\donnee stage\sdau_zorgho\venv\Lib\site-packages\osgeo\geos_c.dll"
   ```

---

## 🚀 Étape 6 : Tester l'application

1. **Vérifier la connexion à la base** :
   ```bash
   python manage.py check
   ```
   
   ✅ Si succès : "System check identified no issues"

2. **Créer un superutilisateur** :
   ```bash
   python manage.py createsuperuser
   ```
   
   Remplir :
   - Username : admin
   - Email : votre_email@example.com
   - Password : (votre mot de passe)

3. **Collecter les fichiers statiques** :
   ```bash
   python manage.py collectstatic
   ```

4. **Démarrer le serveur** :
   ```bash
   python manage.py runserver
   ```

5. **Tester dans le navigateur** :
   - Ouvrir http://127.0.0.1:8000/
   - Vous devriez être redirigé vers `/login/`
   - Créer un compte ou se connecter

---

## 🎯 Étape 7 : Utilisation de l'application

### Première connexion

1. **Créer un compte** :
   - Cliquer sur "Créer un compte"
   - Remplir le formulaire
   - Se connecter avec les identifiants créés

2. **Accéder à la carte** :
   - Après connexion, vous êtes redirigé vers `/carte/`
   - La carte de Zorgho s'affiche avec toutes les zones du SDAU

### Fonctionnalités

#### Visualisation
- ✅ Carte interactive avec zoom/pan
- ✅ Plusieurs fonds de carte (OSM, Satellite, CartoDB)
- ✅ Légende dynamique par type de zone
- ✅ Nord géographique

#### Recherche et filtres
- ✅ Recherche textuelle
- ✅ Filtrage par secteur
- ✅ Filtrage par type de zone
- ✅ Filtrage par statut d'aménagement

#### Interaction
- ✅ Info-bulles au survol
- ✅ Popups détaillées au clic
- ✅ Contrôle de transparence
- ✅ Tableau de bord repliable

#### Sécurité
- ✅ Déconnexion automatique après 2 minutes d'inactivité

---

## 🐛 Résolution de problèmes

### Erreur : "GDAL not found"

**Solution Windows** :
1. Vérifier que OSGeo4W est installé
2. Ajouter `C:\OSGeo4W64\bin` au PATH
3. Redémarrer le terminal

**Solution Linux** :
```bash
sudo apt-get install gdal-bin libgdal-dev python3-gdal
```

### Erreur : "could not connect to server"

**Solution** :
1. Vérifier que PostgreSQL est démarré :
   ```bash
   # Windows
   services.msc → PostgreSQL
   
   # Linux
   sudo systemctl status postgresql
   ```

2. Vérifier les credentials dans `.env`

3. Tester la connexion :
   ```bash
   psql -U postgres -d SDAU_ZORGHOV2
   ```

### Erreur : "PostGIS not installed"

**Solution** :
```sql
-- Se connecter à la base
\c SDAU_ZORGHOV2

-- Activer PostGIS
CREATE EXTENSION postgis;

-- Vérifier
SELECT PostGIS_version();
```

### Erreur : "table does not exist"

**Solution** :
Vérifier que les tables `secteur` et `zone_sdau` existent et sont remplies :
```sql
\c SDAU_ZORGHOV2
\dt

SELECT COUNT(*) FROM secteur;
SELECT COUNT(*) FROM zone_sdau;
```

### Les zones ne s'affichent pas sur la carte

**Solution** :
1. Ouvrir la console du navigateur (F12)
2. Vérifier les erreurs JavaScript
3. Vérifier que l'API retourne des données :
   - http://127.0.0.1:8000/api/zones/geojson/

---

## 📞 Support et contact

**Développeur** :
- Email : ilboudotyh0505@gmail.com
- Étudiant en Géomatique - Université Virtuelle

**Institution** :
- DGUHVT - Direction Générale de l'Urbanisme, de l'Habitat, de la Viabilisation et de la Topographie
- Burkina Faso

---

## ✅ Checklist de vérification finale

Avant de déployer en production :

- [ ] PostgreSQL et PostGIS installés et fonctionnels
- [ ] Base de données `SDAU_ZORGHOV2` créée avec les tables
- [ ] GDAL/GEOS installés et dans le PATH
- [ ] Environnement virtuel Python créé et activé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Fichier `.env` configuré avec les bons credentials
- [ ] `python manage.py check` retourne "no issues"
- [ ] Superutilisateur créé
- [ ] Fichiers statiques collectés
- [ ] Serveur démarre sans erreur
- [ ] Page de connexion accessible
- [ ] Carte s'affiche avec les zones SDAU
- [ ] Filtres fonctionnent
- [ ] Déconnexion automatique après 2 minutes

---

**Fait avec ❤️ pour l'aménagement urbain du Burkina Faso** 🇧🇫
