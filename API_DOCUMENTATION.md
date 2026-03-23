# Documentation API - SDAU Zorgho

Documentation complète de l'API REST pour l'application WebMapping SDAU Zorgho.

**Base URL** : `http://127.0.0.1:8000/api/`

---

## 🔐 Authentification

### POST /api/auth/login/
Connexion d'un utilisateur.

**Request Body** :
```json
{
  "email": "user@example.com",
  "password": "motdepasse123"
}
```

**Response (200 OK)** :
```json
{
  "message": "Connexion réussie",
  "user": {
    "id_user": 1,
    "username": "jdoe",
    "email": "user@example.com",
    "nom": "Doe",
    "prenom": "John",
    "role": "gestionnaire",
    "is_active": true,
    "date_joined": "2024-01-15T10:30:00Z"
  }
}
```

**Response (401 Unauthorized)** :
```json
{
  "error": "Email ou mot de passe incorrect"
}
```

---

### POST /api/auth/logout/
Déconnexion de l'utilisateur courant.

**Response (200 OK)** :
```json
{
  "message": "Déconnexion réussie"
}
```

---

### POST /api/auth/register/
Inscription d'un nouvel utilisateur.

**Request Body** :
```json
{
  "username": "jdoe",
  "email": "john.doe@example.com",
  "nom": "Doe",
  "prenom": "John",
  "role": "consultation",
  "password": "motdepasse123",
  "password_confirm": "motdepasse123"
}
```

**Response (201 Created)** :
```json
{
  "message": "Compte créé avec succès"
}
```

---

### GET /api/auth/check/
Vérifier si l'utilisateur est authentifié.

**Response (200 OK)** :
```json
{
  "authenticated": true,
  "user": {
    "id_user": 1,
    "username": "jdoe",
    "email": "user@example.com",
    "nom": "Doe",
    "prenom": "John",
    "role": "gestionnaire"
  }
}
```

---

## 🗺️ Zones SDAU

### GET /api/zones/
Liste toutes les zones SDAU (format simplifié, sans géométrie).

**Query Parameters** :
- `type_zone` : Filtrer par type (ex: `Habitat`, `Activités`)
- `statut_amenagement` : Filtrer par statut (ex: `À créer`, `À viabiliser`)
- `id_secteur` : Filtrer par ID de secteur
- `id_secteur__nom_secteur` : Filtrer par nom de secteur
- `search` : Recherche textuelle dans zone_sdau, type_zone, statut_amenagement

**Example** :
```
GET /api/zones/?type_zone=Habitat&search=urbaniser
```

**Response (200 OK)** :
```json
{
  "count": 150,
  "next": "http://127.0.0.1:8000/api/zones/?page=2",
  "previous": null,
  "results": [
    {
      "id_zone": 1,
      "zone_sdau": "Zone à urbaniser en priorité",
      "aire_ha": "15.50",
      "type_zone": "Habitat",
      "statut_amenagement": "À créer",
      "nom_secteur": "Secteur 1"
    },
    ...
  ]
}
```

---

### GET /api/zones/{id}/
Détail d'une zone SDAU avec géométrie GeoJSON.

**Response (200 OK)** :
```json
{
  "type": "Feature",
  "id": 1,
  "geometry": {
    "type": "MultiPolygon",
    "coordinates": [
      [
        [
          [-0.6234, 12.2456],
          [-0.6234, 12.2567],
          [-0.6123, 12.2567],
          [-0.6123, 12.2456],
          [-0.6234, 12.2456]
        ]
      ]
    ]
  },
  "properties": {
    "id_zone": 1,
    "zone_sdau": "Zone à urbaniser en priorité",
    "aire_ha": "15.50",
    "type_zone": "Habitat",
    "statut_amenagement": "À créer",
    "id_secteur": 1,
    "nom_secteur": "Secteur 1",
    "couleur": "#FFE4B5"
  }
}
```

---

### GET /api/zones/geojson/
Toutes les zones au format GeoJSON (pour affichage sur carte).

**Query Parameters** : Mêmes filtres que `/api/zones/`

**Response (200 OK)** :
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": 1,
      "geometry": {...},
      "properties": {
        "id_zone": 1,
        "zone_sdau": "Zone à urbaniser en priorité",
        "aire_ha": "15.50",
        "type_zone": "Habitat",
        "statut_amenagement": "À créer",
        "nom_secteur": "Secteur 1",
        "couleur": "#FFE4B5"
      }
    },
    ...
  ]
}
```

---

### GET /api/zones/statistiques/
Statistiques globales du SDAU.

**Response (200 OK)** :
```json
{
  "total_zones": 150,
  "superficie_totale": "1250.75",
  "zones_par_type": {
    "Habitat": 45,
    "Activités": 30,
    "Équipements": 25,
    "Naturelle": 20,
    "Espaces verts": 15,
    "Agricole/pastoralisme": 10,
    "Touristique": 3,
    "Réserve foncière": 2
  },
  "zones_par_statut": {
    "À créer": 60,
    "À viabiliser": 40,
    "À aménager": 25,
    "À réhabiliter": 10,
    "À restructurer": 8,
    "À requalifier": 4,
    "À restaurer": 2,
    "À conserver": 1
  },
  "zones_par_secteur": {
    "Secteur 1": 30,
    "Secteur 2": 28,
    "Secteur 3": 25,
    "Secteur 4": 22,
    "Secteur 5": 25,
    "Secteur 6": 20
  }
}
```

---

### GET /api/zones/choix/
Options disponibles pour les filtres.

**Response (200 OK)** :
```json
{
  "types_zone": [
    "Habitat",
    "Activités",
    "Équipements",
    "Naturelle",
    "Espaces verts",
    "Agricole/pastoralisme",
    "Touristique",
    "Réserve foncière"
  ],
  "statuts_amenagement": [
    "À créer",
    "À viabiliser",
    "À aménager",
    "À réhabiliter",
    "À restructurer",
    "À requalifier",
    "À restaurer",
    "À conserver",
    "À protéger"
  ],
  "secteurs": [
    "Secteur 1",
    "Secteur 2",
    "Secteur 3",
    "Secteur 4",
    "Secteur 5",
    "Secteur 6"
  ]
}
```

---

## 🏘️ Secteurs

### GET /api/secteurs/
Liste tous les secteurs avec géométrie GeoJSON.

**Response (200 OK)** :
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": 1,
      "geometry": {
        "type": "MultiPolygon",
        "coordinates": [...]
      },
      "properties": {
        "id_secteur": 1,
        "nom_secteur": "Secteur 1",
        "superficie_ha": 450.25
      }
    },
    ...
  ]
}
```

---

### GET /api/secteurs/{id}/
Détail d'un secteur.

**Response (200 OK)** :
```json
{
  "type": "Feature",
  "id": 1,
  "geometry": {...},
  "properties": {
    "id_secteur": 1,
    "nom_secteur": "Secteur 1",
    "superficie_ha": 450.25
  }
}
```

---

## 👤 Utilisateurs

### GET /api/utilisateurs/me/
Informations de l'utilisateur connecté.

**Response (200 OK)** :
```json
{
  "id_user": 1,
  "username": "jdoe",
  "email": "john.doe@example.com",
  "nom": "Doe",
  "prenom": "John",
  "role": "gestionnaire",
  "is_active": true,
  "date_joined": "2024-01-15T10:30:00Z"
}
```

---

### GET /api/utilisateurs/
Liste tous les utilisateurs (admin uniquement).

**Response (200 OK)** :
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id_user": 1,
      "username": "jdoe",
      "email": "john.doe@example.com",
      "nom": "Doe",
      "prenom": "John",
      "role": "gestionnaire",
      "is_active": true,
      "date_joined": "2024-01-15T10:30:00Z"
    },
    ...
  ]
}
```

---

## 🎨 Couleurs cartographiques

Les couleurs suivent les normes de cartographie urbaine :

| Type de zone | Couleur (HEX) | Aperçu |
|--------------|---------------|--------|
| Habitat | `#FFE4B5` | 🟡 Jaune pâle |
| Activités | `#FFA07A` | 🟠 Saumon |
| Équipements | `#87CEEB` | 🔵 Bleu ciel |
| Naturelle | `#90EE90` | 🟢 Vert clair |
| Espaces verts | `#228B22` | 🌳 Vert forêt |
| Agricole/pastoralisme | `#F0E68C` | 🟤 Kaki |
| Touristique | `#DDA0DD` | 🟣 Prune |
| Réserve foncière | `#D3D3D3` | ⚪ Gris clair |

---

## 🔒 Codes de statut HTTP

- **200 OK** : Requête réussie
- **201 Created** : Ressource créée avec succès
- **400 Bad Request** : Données invalides
- **401 Unauthorized** : Non authentifié
- **403 Forbidden** : Accès refusé
- **404 Not Found** : Ressource non trouvée
- **500 Internal Server Error** : Erreur serveur

---

## 📝 Exemples avec cURL

### Connexion
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass123"}' \
  -c cookies.txt
```

### Récupérer les zones (avec filtres)
```bash
curl http://127.0.0.1:8000/api/zones/geojson/?type_zone=Habitat \
  -b cookies.txt
```

### Statistiques
```bash
curl http://127.0.0.1:8000/api/zones/statistiques/ \
  -b cookies.txt
```

### Déconnexion
```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -b cookies.txt
```

---

## 🛠️ Exemples avec JavaScript (Fetch API)

### Connexion
```javascript
const response = await fetch('/api/auth/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken')
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'pass123'
  })
});

const data = await response.json();
console.log(data);
```

### Charger les zones
```javascript
const response = await fetch('/api/zones/geojson/?type_zone=Habitat');
const geojson = await response.json();

// Ajouter à Leaflet
L.geoJSON(geojson).addTo(map);
```

### Appliquer des filtres
```javascript
const params = new URLSearchParams({
  type_zone: 'Habitat',
  statut_amenagement: 'À créer',
  id_secteur__nom_secteur: 'Secteur 1'
});

const response = await fetch(`/api/zones/geojson/?${params}`);
const filteredData = await response.json();
```

---

**Documentation générée pour SDAU Zorgho - DGUHVT Burkina Faso** 🇧🇫
