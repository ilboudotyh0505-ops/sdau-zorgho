#!/bin/bash
# Script de démarrage pour SDAU Zorgho (Linux/Mac)

echo "================================"
echo "SDAU Zorgho - Démarrage"
echo "================================"
echo ""

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
    echo ""
fi

# Activer l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source venv/bin/activate
echo ""

# Vérifier si les dépendances sont installées
echo "Vérification des dépendances..."
pip install -q -r requirements.txt
echo ""

# Vérifier la connexion à la base de données
echo "Vérification de la connexion à la base de données..."
python manage.py check
if [ $? -ne 0 ]; then
    echo ""
    echo "ERREUR: Impossible de se connecter à la base de données"
    echo "Vérifiez votre fichier .env et PostgreSQL"
    exit 1
fi
echo ""

# Collecter les fichiers statiques
echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear
echo ""

# Démarrer le serveur
echo "================================"
echo "Démarrage du serveur Django..."
echo "URL: http://127.0.0.1:8000"
echo "Appuyez sur Ctrl+C pour arrêter"
echo "================================"
echo ""
python manage.py runserver
