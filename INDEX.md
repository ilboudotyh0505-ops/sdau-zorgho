# 📚 Index de la documentation - SDAU Zorgho

Bienvenue dans le projet **Application WebMapping SDAU Zorgho** ! Ce document vous guide vers toutes les ressources disponibles.

---

## 🎯 Par où commencer ?

### 👉 **Nouveau sur le projet ?**
1. Lire **[QUICKSTART.md](QUICKSTART.md)** (5 minutes) - Démarrage ultra-rapide
2. Suivre **[INSTALLATION.md](INSTALLATION.md)** (15-30 min) - Installation complète pas à pas
3. Explorer la **[carte interactive](http://127.0.0.1:8000/carte/)** après installation

### 👉 **Développeur expérimenté ?**
1. Consulter **[STRUCTURE.md](STRUCTURE.md)** - Architecture du projet
2. Lire **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Endpoints API REST
3. Vérifier **[requirements.txt](requirements.txt)** - Dépendances

### 👉 **Prêt pour la production ?**
1. Lire **[DEPLOYMENT.md](DEPLOYMENT.md)** - Déploiement sur serveur
2. Configurer la sécurité selon les recommandations
3. Mettre en place les sauvegardes automatiques

---

## 📖 Documentation disponible

### 🚀 Guides de démarrage

| Fichier | Description | Durée | Public |
|---------|-------------|-------|---------|
| **[QUICKSTART.md](QUICKSTART.md)** | Guide de démarrage rapide en 5 étapes | 5 min | Débutants |
| **[INSTALLATION.md](INSTALLATION.md)** | Installation détaillée pas à pas | 30 min | Tous |
| **[README.md](README.md)** | Documentation générale du projet | 10 min | Tous |

### 🏗️ Documentation technique

| Fichier | Description | Public |
|---------|-------------|---------|
| **[STRUCTURE.md](STRUCTURE.md)** | Architecture et organisation du code | Développeurs |
| **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** | Documentation complète de l'API REST | Développeurs |
| **[requirements.txt](requirements.txt)** | Liste des dépendances Python | Développeurs |

### 🚀 Déploiement et production

| Fichier | Description | Public |
|---------|-------------|---------|
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Guide de déploiement en production | DevOps/Admin |
| **[.env.example](.env.example)** | Exemple de configuration environnement | Tous |

### 🔧 Fichiers de configuration

| Fichier | Description | Rôle |
|---------|-------------|------|
| **[manage.py](manage.py)** | Utilitaire de gestion Django | Commandes Django |
| **[requirements.txt](requirements.txt)** | Dépendances Python | Installation |
| **[.env.example](.env.example)** | Variables d'environnement | Configuration |
| **[.gitignore](.gitignore)** | Fichiers ignorés par Git | Versioning |

### 🛠️ Scripts utilitaires

| Fichier | Description | Plateforme |
|---------|-------------|------------|
| **[start.bat](start.bat)** | Script de démarrage automatique | Windows |
| **[start.sh](start.sh)** | Script de démarrage automatique | Linux/Mac |
| **[check_environment.py](check_environment.py)** | Vérification de l'environnement | Tous |
| **[commands.txt](commands.txt)** | Commandes utiles | Référence |

---

## 📁 Structure des répertoires

```
sdau_zorgho/
│
├── 📚 DOCUMENTATION (vous êtes ici)
│   ├── README.md                   # Documentation principale
│   ├── QUICKSTART.md               # Démarrage rapide
│   ├── INSTALLATION.md             # Installation détaillée
│   ├── API_DOCUMENTATION.md        # Documentation API
│   ├── STRUCTURE.md                # Architecture projet
│   ├── DEPLOYMENT.md               # Guide déploiement
│   └── INDEX.md                    # Ce fichier
│
├── ⚙️ CONFIGURATION
│   ├── sdau_zorgho/settings.py     # Configuration Django
│   ├── sdau_zorgho/urls.py         # Routes principales
│   ├── .env.example                # Exemple configuration
│   └── requirements.txt            # Dépendances
│
├── 💻 CODE SOURCE
│   ├── sdau/models.py              # Modèles de données
│   ├── sdau/views.py               # Vues API
│   ├── sdau/serializers.py         # Serializers
│   └── sdau/admin.py               # Interface admin
│
├── 🎨 FRONTEND
│   └── templates/                  # Templates HTML
│       ├── base.html               # Template de base
│       └── sdau/
│           ├── login.html          # Page connexion
│           ├── register.html       # Page inscription
│           └── carte.html          # Carte interactive
│
└── 🔧 UTILITAIRES
    ├── manage.py                   # Commandes Django
    ├── start.bat                   # Démarrage Windows
    ├── start.sh                    # Démarrage Linux/Mac
    └── check_environment.py        # Vérification
```

---

## 🎓 Parcours d'apprentissage recommandé

### Niveau 1 : Débutant (1-2 heures)
1. ✅ Lire **QUICKSTART.md**
2. ✅ Installer selon **INSTALLATION.md**
3. ✅ Créer un compte et se connecter
4. ✅ Explorer la carte interactive
5. ✅ Tester les filtres et la recherche

### Niveau 2 : Intermédiaire (3-5 heures)
1. ✅ Lire **STRUCTURE.md** pour comprendre l'architecture
2. ✅ Consulter **API_DOCUMENTATION.md**
3. ✅ Tester les endpoints API avec Postman ou cURL
4. ✅ Modifier des couleurs ou styles dans les templates
5. ✅ Ajouter un nouveau filtre

### Niveau 3 : Avancé (1-2 jours)
1. ✅ Lire **DEPLOYMENT.md**
2. ✅ Configurer un serveur de test
3. ✅ Déployer avec Gunicorn + Nginx
4. ✅ Configurer SSL avec Let's Encrypt
5. ✅ Mettre en place les sauvegardes automatiques

---

## 🔗 Liens rapides

### Pages web (après installation)
- 🏠 **Page d'accueil** : http://127.0.0.1:8000/
- 🔐 **Connexion** : http://127.0.0.1:8000/login/
- ✍️ **Inscription** : http://127.0.0.1:8000/register/
- 🗺️ **Carte** : http://127.0.0.1:8000/carte/
- 👨‍💼 **Admin Django** : http://127.0.0.1:8000/admin/

### API REST
- 📊 **Zones GeoJSON** : http://127.0.0.1:8000/api/zones/geojson/
- 📈 **Statistiques** : http://127.0.0.1:8000/api/zones/statistiques/
- 🗂️ **Secteurs** : http://127.0.0.1:8000/api/secteurs/
- 👤 **Utilisateur** : http://127.0.0.1:8000/api/utilisateurs/me/

### Ressources externes
- 📖 **Django** : https://docs.djangoproject.com/
- 🗺️ **Leaflet** : https://leafletjs.com/
- 🌍 **PostGIS** : https://postgis.net/
- 🐘 **PostgreSQL** : https://www.postgresql.org/

---

## ❓ Questions fréquentes

### Quel fichier lire en premier ?
➡️ **QUICKSTART.md** pour un aperçu rapide, puis **INSTALLATION.md** pour l'installation complète.

### Comment tester l'API ?
➡️ Lire **API_DOCUMENTATION.md**, puis utiliser Postman ou cURL avec les exemples fournis.

### Comment déployer en production ?
➡️ Suivre **DEPLOYMENT.md** qui couvre Gunicorn, Nginx, SSL et Docker.

### Où trouver les commandes Django ?
➡️ Consulter **commands.txt** pour une liste rapide des commandes utiles.

### Comment modifier les couleurs de la carte ?
➡️ Éditer la méthode `get_couleur_cartographie()` dans **sdau/models.py**

---

## 📞 Support et contact

**Développeur** :
- 👨‍🎓 Étudiant en Géomatique
- 🏫 Université Virtuelle
- 📧 Email : ilboudotyh0505@gmail.com

**Institution** :
- 🏛️ DGUHVT - Direction Générale de l'Urbanisme, de l'Habitat, de la Viabilisation et de la Topographie
- 🌍 Burkina Faso
- 📍 Zorgho, Province du Ganzourgou, Région du Centre-Est

---

## ✅ Checklist complète

### Installation
- [ ] Lire QUICKSTART.md
- [ ] Lire INSTALLATION.md
- [ ] Installer les prérequis (Python, PostgreSQL, GDAL)
- [ ] Extraire le projet
- [ ] Configurer .env
- [ ] Lancer check_environment.py
- [ ] Démarrer le serveur
- [ ] Créer un compte
- [ ] Se connecter
- [ ] Explorer la carte

### Développement
- [ ] Lire STRUCTURE.md
- [ ] Lire API_DOCUMENTATION.md
- [ ] Comprendre les modèles Django
- [ ] Tester les endpoints API
- [ ] Modifier un template
- [ ] Lancer les tests unitaires

### Production
- [ ] Lire DEPLOYMENT.md
- [ ] Configurer la sécurité
- [ ] Déployer sur serveur
- [ ] Configurer SSL
- [ ] Mettre en place les sauvegardes
- [ ] Monitorer les logs

---

## 📊 Métriques du projet

| Métrique | Valeur |
|----------|--------|
| **Lignes de code Python** | ~1500 |
| **Lignes de code HTML/JS** | ~1200 |
| **Nombre de fichiers** | ~30 |
| **Modèles Django** | 4 |
| **Endpoints API** | 15+ |
| **Pages frontend** | 3 |
| **Documentation** | 7 fichiers |

---

## 🎉 Félicitations !

Vous avez maintenant accès à toute la documentation nécessaire pour :
- ✅ Installer l'application
- ✅ Développer de nouvelles fonctionnalités
- ✅ Déployer en production
- ✅ Maintenir et dépanner

**Bon développement !** 💻🗺️

---

**Fait avec ❤️ pour l'aménagement urbain du Burkina Faso** 🇧🇫

