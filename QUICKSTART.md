# 🚀 Guide de démarrage rapide - SDAU Zorgho

**Temps estimé** : 15-30 minutes  
**Niveau** : Débutant à Intermédiaire

---

## ⚡ Démarrage rapide (5 étapes)

### 1️⃣ Vérifier les prérequis (5 min)

✅ **Python 3.11+** installé
```bash
python --version
# Doit afficher : Python 3.11.x ou supérieur
```

✅ **PostgreSQL avec PostGIS** installé et démarré
```bash
psql --version
# Doit afficher : psql (PostgreSQL) 13.x ou supérieur
```

✅ **GDAL** installé
```bash
# Windows : Vérifier que OSGeo4W est installé
# Linux : sudo apt-get install gdal-bin

gdalinfo --version
```

---

### 2️⃣ Extraire le projet (1 min)

```bash
# Windows
# Extraire sdau_zorgho.zip avec l'explorateur de fichiers

# Linux/Mac
unzip sdau_zorgho.zip
cd sdau_zorgho
```

---

### 3️⃣ Configurer la base de données (5 min)

```bash
# Se connecter à PostgreSQL
psql -U postgres

# Dans psql :
\c SDAU_ZORGHOV2
SELECT PostGIS_version();  -- Vérifier PostGIS
\dt                         -- Vérifier les tables
\q                          -- Quitter
```
venv/bin/activate
✅ Vous devez voir les tables : `secteur` et `zone_sdau`

---

### 4️⃣ Configurer l'environnement (10 min)

```bash
# 1. Créer l'environnement virtuel
python -m venv venv

# 2. Activer l'environnement
# Windows :
venv\Scripts\activate
# Linux/Mac :
source 

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Copier et configurer .env
# Windows :
copy .env.example .env
# Linux/Mac :
cp .env.example .env

# 5. Éditer .env avec vos informations
# Ouvrir .env et modifier :
#   DB_PASSWORD=votre_mot_de_passe_postgres
```

---

### 5️⃣ Lancer l'application (2 min)

```bash
# Vérifier l'environnement
python check_environment.py

# Si tout est OK, lancer le serveur :
python manage.py runserver
```

🎉 **Ouvrir dans le navigateur** : http://127.0.0.1:8000

---

## 🎯 Première utilisation

### Créer un compte
1. Cliquer sur **"Créer un compte"**
2. Remplir le formulaire :
   - Nom : Votre nom
   - Prénom : Votre prénom
   - Username : votre_username
   - Email : votre_email@example.com
   - Rôle : Consultation (ou Gestionnaire)
   - Mot de passe : min. 8 caractères
3. Cliquer sur **"Créer le compte"**

### Se connecter
1. Entrer votre **email** et **mot de passe**
2. Cliquer sur **"Se connecter"**
3. Vous êtes redirigé vers la carte ! 🗺️

### Explorer la carte
1. **Visualiser** : Toutes les zones du SDAU de Zorgho s'affichent
2. **Zoomer** : Molette de la souris ou boutons +/-
3. **Info** : Survoler une zone pour voir l'info-bulle
4. **Détails** : Cliquer sur une zone pour voir la popup détaillée

### Utiliser les filtres
1. **Ouvrir** le panneau latéral (icône ☰ en haut à gauche)
2. **Rechercher** : Taper un nom de zone
3. **Filtrer** :
   - Par secteur : Secteur 1, 2, 3...
   - Par type : Habitat, Activités, Équipements...
   - Par statut : À créer, À viabiliser...
4. **Appliquer** : Cliquer sur "Appliquer les filtres"
5. **Réinitialiser** : Cliquer sur "Réinitialiser"

### Voir les statistiques
Dans le panneau latéral :
- 📊 **Nombre total de zones**
- 📐 **Superficie totale** (en hectares)
- 🎨 **Légende** des couleurs

---

## 🛠️ Commandes utiles

### Démarrage automatique
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

### Vérification
```bash
# Vérifier l'environnement
python check_environment.py

# Vérifier Django
python manage.py check

# Lancer les tests
python manage.py test
```

### Administration
```bash
# Créer un superutilisateur
python manage.py createsuperuser

# Accéder à l'admin
# http://127.0.0.1:8000/admin/
```

### Collecte des fichiers statiques
```bash
python manage.py collectstatic
```

---

## ❓ Questions fréquentes

### ❌ Erreur : "GDAL not found"
**Solution** :
- Windows : Installer OSGeo4W → https://trac.osgeo.org/osgeo4w/
- Linux : `sudo apt-get install gdal-bin libgdal-dev`

### ❌ Erreur : "could not connect to server"
**Solution** :
1. Vérifier que PostgreSQL est démarré
2. Vérifier les credentials dans `.env`
3. Tester : `psql -U postgres`

### ❌ Les zones ne s'affichent pas
**Solution** :
1. Ouvrir la console du navigateur (F12)
2. Vérifier les erreurs
3. Tester l'API : http://127.0.0.1:8000/api/zones/geojson/

### ❌ Déconnexion automatique trop rapide
**Solution** :
Modifier dans `.env` :
```
SESSION_COOKIE_AGE=300  # 5 minutes au lieu de 2
```

---

## 📚 Documentation complète

Pour aller plus loin :

1. **INSTALLATION.md** : Guide d'installation détaillé pas à pas
2. **README.md** : Documentation générale du projet
3. **API_DOCUMENTATION.md** : Documentation complète de l'API REST
4. **STRUCTURE.md** : Architecture et structure du projet

---

## 🎓 Ressources d'apprentissage

### Django
- Documentation officielle : https://docs.djangoproject.com/
- GeoDjango : https://docs.djangoproject.com/en/4.2/ref/contrib/gis/

### Leaflet
- Documentation : https://leafletjs.com/reference.html
- Tutoriels : https://leafletjs.com/examples.html

### PostGIS
- Documentation : https://postgis.net/documentation/
- Tutoriels : https://postgis.net/workshops/

---

## 📞 Support

**Développeur** : Étudiant en Géomatique  
**Email** : ilboudotyh0505@gmail.com  
**Institution** : DGUVT - Burkina Faso

---

## ✅ Checklist de démarrage

Cochez au fur et à mesure :

- [ ] Python 3.11+ installé
- [ ] PostgreSQL + PostGIS installés
- [ ] GDAL installé
- [ ] Projet extrait
- [ ] Base de données vérifiée
- [ ] Environnement virtuel créé
- [ ] Dépendances installées
- [ ] Fichier .env configuré
- [ ] `check_environment.py` réussi
- [ ] Serveur lancé
- [ ] Compte créé
- [ ] Connexion réussie
- [ ] Carte affichée
- [ ] Filtres testés
- [ ] 🎉 Application fonctionnelle !

---

**Bon développement !** 💻🗺️

**Fait avec ❤️ pour l'aménagement urbain du Burkina Faso** 🇧🇫
