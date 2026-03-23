# Structure du projet SDAU Zorgho

```
sdau_zorgho/
│
├── 📁 sdau_zorgho/                    # Configuration Django
│   ├── __init__.py
│   ├── settings.py                    # ⚙️ Configuration principale
│   ├── urls.py                        # 🔗 Routes principales
│   ├── wsgi.py                        # 🌐 Déploiement WSGI
│   └── asgi.py                        # 🌐 Déploiement ASGI
│
├── 📁 sdau/                           # Application principale
│   ├── __init__.py
│   ├── apps.py                        # Configuration app
│   ├── models.py                      # 🗄️ Modèles (Secteur, ZoneSdau, Utilisateur)
│   ├── serializers.py                 # 📤 Serializers API REST
│   ├── views.py                       # 🎯 Vues API
│   ├── views_frontend.py              # 🎨 Vues frontend
│   ├── urls_frontend.py               # 🔗 Routes frontend
│   ├── admin.py                       # 👨‍💼 Interface admin Django
│   └── tests.py                       # 🧪 Tests unitaires
│
├── 📁 templates/                      # Templates HTML
│   ├── base.html                      # 📄 Template de base
│   └── 📁 sdau/
│       ├── login.html                 # 🔐 Page de connexion
│       ├── register.html              # ✍️ Page d'inscription
│       └── carte.html                 # 🗺️ Page carte interactive
│
├── 📁 static/                         # Fichiers statiques (CSS, JS, images)
│   └── (vide - sera créé automatiquement)
│
├── 📁 staticfiles/                    # Fichiers statiques collectés
│   └── (généré par collectstatic)
│
├── 📁 media/                          # Fichiers uploadés
│   └── (vide)
│
├── 📁 venv/                           # Environnement virtuel Python
│   └── (créé lors de l'installation)
│
├── 📄 manage.py                       # 🔧 Utilitaire Django
├── 📄 requirements.txt                # 📦 Dépendances Python
├── 📄 .env.example                    # 🔐 Variables d'environnement (exemple)
├── 📄 .env                            # 🔐 Variables d'environnement (à créer)
├── 📄 .gitignore                      # 🚫 Fichiers ignorés par Git
│
├── 📄 README.md                       # 📚 Documentation principale
├── 📄 INSTALLATION.md                 # 📘 Guide d'installation
├── 📄 API_DOCUMENTATION.md            # 📖 Documentation API
│
├── 📄 start.bat                       # ▶️ Script démarrage Windows
├── 📄 start.sh                        # ▶️ Script démarrage Linux/Mac
├── 📄 check_environment.py            # ✅ Vérification environnement
└── 📄 commands.txt                    # 📝 Commandes utiles

```

## 📊 Architecture de l'application

### Backend (Django/GeoDjango)
```
┌─────────────────────────────────────────┐
│         Django REST Framework           │
├─────────────────────────────────────────┤
│  API Endpoints                          │
│  • /api/auth/                           │
│  • /api/zones/                          │
│  • /api/secteurs/                       │
│  • /api/utilisateurs/                   │
└─────────────────────────────────────────┘
           ↕
┌─────────────────────────────────────────┐
│         GeoDjango Models                │
│  • Secteur                              │
│  • ZoneSdau                             │
│  • Utilisateur                          │
│  • UtilisateurZone                      │
└─────────────────────────────────────────┘
           ↕
┌─────────────────────────────────────────┐
│    PostgreSQL + PostGIS                 │
│    Base: SDAU_ZORGHOV2                  │
└─────────────────────────────────────────┘
```

### Frontend (HTML/CSS/JS + Leaflet)
```
┌─────────────────────────────────────────┐
│         Interface Utilisateur           │
├─────────────────────────────────────────┤
│  Pages                                  │
│  • Login/Register (auth-page)           │
│  • Carte Interactive (carte-page)       │
├─────────────────────────────────────────┤
│  Composants                             │
│  • Sidebar (tableau de bord)            │
│  • Leaflet Map (visualisation)          │
│  • Filtres et recherche                 │
│  • Statistiques                         │
└─────────────────────────────────────────┘
           ↕
┌─────────────────────────────────────────┐
│         Leaflet.js                      │
│  • Couches GeoJSON                      │
│  • Fonds de carte (OSM, Satellite)      │
│  • Interactions (zoom, popup)           │
└─────────────────────────────────────────┘
```

## 🔄 Flux de données

### 1. Authentification
```
Utilisateur → Login Form → POST /api/auth/login/
                                    ↓
                            Vérification credentials
                                    ↓
                            Création session Django
                                    ↓
                          Redirection vers /carte/
```

### 2. Chargement de la carte
```
Page /carte/ → GET /api/zones/geojson/
                     ↓
              PostgreSQL/PostGIS query
                     ↓
              Serialization (GeoJSON)
                     ↓
              Response → Leaflet.js
                     ↓
              Affichage sur carte
```

### 3. Filtrage
```
Utilisateur → Sélection filtres → Paramètres URL
                                        ↓
                          GET /api/zones/geojson/?type=Habitat
                                        ↓
                              Query filtrée PostgreSQL
                                        ↓
                              GeoJSON filtré → Carte
```

## 🎯 Fonctionnalités principales

### ✅ Authentification et sécurité
- [x] Inscription/Connexion/Déconnexion
- [x] Sessions Django avec cookies sécurisés
- [x] Déconnexion automatique après 2 minutes d'inactivité
- [x] Protection CSRF
- [x] Validation des mots de passe

### ✅ Visualisation cartographique
- [x] Carte Leaflet interactive
- [x] 3 fonds de carte (OSM, Satellite, CartoDB)
- [x] Affichage des zones SDAU avec couleurs normalisées
- [x] Affichage des secteurs avec contours
- [x] Info-bulles au survol
- [x] Popups détaillées au clic
- [x] Nord géographique
- [x] Échelle cartographique
- [x] Contrôle de zoom

### ✅ Recherche et filtrage
- [x] Recherche textuelle dans les zones
- [x] Filtrage par secteur (Secteur 1-6)
- [x] Filtrage par type de zone (8 types)
- [x] Filtrage par statut d'aménagement (9 statuts)
- [x] Combinaison de filtres multiples
- [x] Réinitialisation des filtres

### ✅ Interaction utilisateur
- [x] Tableau de bord repliable
- [x] Contrôle de transparence des zones
- [x] Statistiques en temps réel
- [x] Légende dynamique
- [x] Zoom automatique sur zones filtrées

### ✅ Statistiques
- [x] Nombre total de zones
- [x] Superficie totale (ha)
- [x] Répartition par type de zone
- [x] Répartition par statut d'aménagement
- [x] Répartition par secteur

### ✅ API REST
- [x] Endpoints RESTful complets
- [x] Authentification par session
- [x] Pagination automatique
- [x] Filtrage via query params
- [x] Export GeoJSON
- [x] Documentation API complète

## 📈 Évolutions futures possibles

### Phase 2 (court terme)
- [ ] Export PDF des zones filtrées
- [ ] Impression de la carte
- [ ] Mesure de distances et surfaces
- [ ] Géolocalisation de l'utilisateur
- [ ] Mode sombre

### Phase 3 (moyen terme)
- [ ] Gestion des droits utilisateurs avancée
- [ ] Historique des modifications
- [ ] Commentaires sur les zones
- [ ] Notifications par email
- [ ] Tableau de bord statistiques avancé

### Phase 4 (long terme)
- [ ] API mobile (React Native / Flutter)
- [ ] Édition des géométries en ligne
- [ ] Import/Export Shapefile
- [ ] Intégration avec d'autres systèmes SIG
- [ ] Rapports automatiques générés

## 🛠️ Technologies utilisées

| Catégorie | Technologie | Version | Rôle |
|-----------|-------------|---------|------|
| **Backend** | Django | 4.2.7 | Framework web |
| | GeoDjango | (intégré) | Extension géospatiale |
| | Django REST Framework | 3.14.0 | API REST |
| **Base de données** | PostgreSQL | 13+ | SGBD |
| | PostGIS | 3.0+ | Extension spatiale |
| **Frontend** | HTML5 | - | Structure |
| | CSS3 | - | Styles |
| | JavaScript ES6 | - | Interactions |
| | Bootstrap | 5.3.2 | Framework CSS |
| | Leaflet.js | 1.9.4 | Cartographie |
| **Python** | Python | 3.11 | Langage |
| | GDAL | 3.7.3 | Géotraitement |
| | Shapely | 2.0.2 | Géométries |
| | psycopg2 | 2.9.9 | Connecteur PostgreSQL |

## 📞 Informations projet

**Projet** : Application WebMapping SDAU Zorgho  
structure: DGUHVT - Direction Générale de l'Urbanisme, de l'Habitat, de la Viabilisation et de la Topographie  
**Localisation** : Zorgho, Province du Ganzourgou, Région d'oubri, Burkina Faso  
**Développeur** : Étudiant en Géomatique - Université Virtuelle  
**Contact** : ilboudotyh0505@gmail.com  
**Année** : 2026


---

**Fait avec ❤️ pour l'aménagement urbain du Burkina Faso** 🇧🇫
