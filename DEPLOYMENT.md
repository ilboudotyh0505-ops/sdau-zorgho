# 🚀 Guide de déploiement en production - SDAU Zorgho

Ce guide vous aide à déployer l'application SDAU Zorgho en production.

---

## ⚠️ Avant de déployer

### Checklist de sécurité

- [ ] **SECRET_KEY** : Générer une nouvelle clé secrète unique
- [ ] **DEBUG** : Passer à `False`
- [ ] **ALLOWED_HOSTS** : Configurer avec votre domaine
- [ ] **BASE DE DONNÉES** : Utiliser des credentials sécurisés
- [ ] **HTTPS** : Activer SSL/TLS
- [ ] **CORS** : Restreindre les origines autorisées
- [ ] **Fichiers sensibles** : Vérifier que `.env` n'est pas committé

---

## 🔐 Configuration de production

### 1. Générer une SECRET_KEY sécurisée

```python
# Dans un shell Python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copier la clé générée dans `.env` :
```
SECRET_KEY=nouvelle-cle-secrete-tres-longue-et-aleatoire
```

### 2. Modifier settings.py pour la production

```python
# Dans sdau_zorgho/settings.py

DEBUG = False  # ⚠️ IMPORTANT : Passer à False

ALLOWED_HOSTS = ['votre-domaine.com', 'www.votre-domaine.com', 'ip-serveur']

# Sécurité renforcée
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CORS restreint
CORS_ALLOWED_ORIGINS = [
    'https://votre-domaine.com',
    'https://www.votre-domaine.com',
]
```

### 3. Configurer la base de données production

```ini
# Dans .env
DB_NAME=SDAU_ZORGHOV2_PROD
DB_USER=sdau_user
DB_PASSWORD=mot_de_passe_tres_securise
DB_HOST=localhost  # ou IP serveur DB
DB_PORT=5432
```

### 4. Fichiers statiques

```python
# Dans settings.py
STATIC_ROOT = '/var/www/sdau_zorgho/static/'
MEDIA_ROOT = '/var/www/sdau_zorgho/media/'
```

```bash
# Collecter les fichiers statiques
python manage.py collectstatic --noinput
```

---

## 🖥️ Déploiement sur serveur Linux (Ubuntu)

### Étape 1 : Installer les dépendances système

```bash
# Mettre à jour le système
sudo apt-get update
sudo apt-get upgrade

# Installer Python et outils
sudo apt-get install python3.11 python3.11-venv python3-pip

# Installer PostgreSQL et PostGIS
sudo apt-get install postgresql postgresql-contrib postgis

# Installer GDAL
sudo apt-get install gdal-bin libgdal-dev python3-gdal

# Installer Nginx
sudo apt-get install nginx

# Installer Gunicorn (serveur WSGI)
pip install gunicorn
```

### Étape 2 : Configurer PostgreSQL

```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Créer l'utilisateur et la base
CREATE USER sdau_user WITH PASSWORD 'mot_de_passe_securise';
CREATE DATABASE SDAU_ZORGHOV2_PROD OWNER sdau_user;
\c SDAU_ZORGHOV2_PROD
CREATE EXTENSION postgis;
GRANT ALL PRIVILEGES ON DATABASE SDAU_ZORGHOV2_PROD TO sdau_user;
\q

# Restaurer les données (si backup disponible)
pg_restore -U sdau_user -d SDAU_ZORGHOV2_PROD backup.dump
```

### Étape 3 : Déployer l'application

```bash
# Créer un utilisateur système
sudo useradd -m -s /bin/bash sdau

# Créer les répertoires
sudo mkdir -p /var/www/sdau_zorgho
sudo chown sdau:sdau /var/www/sdau_zorgho

# Se connecter en tant que sdau
sudo su - sdau
cd /var/www/sdau_zorgho

# Cloner/copier le projet
# (Utiliser Git, SCP, ou autre méthode)
git clone https://votre-repo.git .
# OU
scp -r local/sdau_zorgho/* sdau@server:/var/www/sdau_zorgho/

# Créer l'environnement virtuel
python3.11 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
pip install gunicorn

# Configurer .env
cp .env.example .env
nano .env  # Éditer avec les valeurs de production

# Vérifier
python manage.py check --deploy

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Créer un superutilisateur
python manage.py createsuperuser
```

### Étape 4 : Configurer Gunicorn

Créer `/etc/systemd/system/sdau.service` :

```ini
[Unit]
Description=SDAU Zorgho Gunicorn daemon
After=network.target

[Service]
User=sdau
Group=sdau
WorkingDirectory=/var/www/sdau_zorgho
Environment="PATH=/var/www/sdau_zorgho/venv/bin"
ExecStart=/var/www/sdau_zorgho/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/sdau_zorgho/sdau.sock \
          sdau_zorgho.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Activer et démarrer le service
sudo systemctl daemon-reload
sudo systemctl start sdau
sudo systemctl enable sdau
sudo systemctl status sdau
```

### Étape 5 : Configurer Nginx

Créer `/etc/nginx/sites-available/sdau` :

```nginx
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;

    # Redirection HTTPS (à configurer après certificat SSL)
    # return 301 https://$server_name$request_uri;

    client_max_body_size 20M;

    location /static/ {
        alias /var/www/sdau_zorgho/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/sdau_zorgho/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/sdau_zorgho/sdau.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

```bash
# Activer le site
sudo ln -s /etc/nginx/sites-available/sdau /etc/nginx/sites-enabled/
sudo nginx -t  # Tester la configuration
sudo systemctl restart nginx
```

### Étape 6 : Configurer SSL avec Let's Encrypt

```bash
# Installer Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtenir un certificat
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com

# Renouvellement automatique (déjà configuré par défaut)
sudo certbot renew --dry-run
```

---

## 🐳 Déploiement avec Docker (Optionnel)

### Créer Dockerfile

```dockerfile
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Installer dépendances système
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Répertoire de travail
WORKDIR /app

# Copier requirements et installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copier le projet
COPY . .

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "sdau_zorgho.wsgi:application"]
```

### Créer docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgis/postgis:13-3.1
    environment:
      POSTGRES_DB: SDAU_ZORGHOV2
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    command: gunicorn sdau_zorgho.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - .env

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### Lancer avec Docker

```bash
# Construire et démarrer
docker-compose up -d --build

# Vérifier les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

---

## 📊 Monitoring et maintenance

### Logs

```bash
# Logs Gunicorn
sudo journalctl -u sdau -f

# Logs Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Sauvegarde base de données

```bash
# Backup
pg_dump -U sdau_user SDAU_ZORGHOV2_PROD > backup_$(date +%Y%m%d).sql

# Backup avec compression
pg_dump -U sdau_user -Fc SDAU_ZORGHOV2_PROD > backup_$(date +%Y%m%d).dump

# Restauration
psql -U sdau_user SDAU_ZORGHOV2_PROD < backup.sql
# OU
pg_restore -U sdau_user -d SDAU_ZORGHOV2_PROD backup.dump
```

### Script de sauvegarde automatique

Créer `/usr/local/bin/backup_sdau.sh` :

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/sdau"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup base de données
pg_dump -U sdau_user -Fc SDAU_ZORGHOV2_PROD > $BACKUP_DIR/db_$DATE.dump

# Backup fichiers media
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/sdau_zorgho/media/

# Garder seulement les 7 derniers backups
find $BACKUP_DIR -name "*.dump" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

Ajouter au crontab (tous les jours à 2h du matin) :

```bash
sudo crontab -e
# Ajouter :
0 2 * * * /usr/local/bin/backup_sdau.sh
```

---

## 🔍 Vérifications post-déploiement

- [ ] Application accessible via le domaine
- [ ] HTTPS actif (cadenas vert)
- [ ] Connexion/Déconnexion fonctionnent
- [ ] Carte s'affiche correctement
- [ ] Filtres fonctionnent
- [ ] API répond correctement
- [ ] Fichiers statiques chargés
- [ ] Logs sans erreurs critiques
- [ ] Sauvegarde automatique configurée

---

## 📞 Support production

**En cas de problème en production** :

1. Vérifier les logs : `sudo journalctl -u sdau -n 100`
2. Vérifier Nginx : `sudo nginx -t`
3. Redémarrer les services :
   ```bash
   sudo systemctl restart sdau
   sudo systemctl restart nginx
   ```

---

**Bon déploiement !** 🚀

**Fait avec ❤️ pour l'aménagement urbain du Burkina Faso** 🇧🇫
