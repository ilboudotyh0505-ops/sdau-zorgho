@echo off
REM Script de démarrage pour SDAU Zorgho (Windows)

echo ================================
echo SDAU Zorgho - Demarrage
echo ================================
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv\Scripts\activate.bat" (
    echo Creation de l'environnement virtuel...
    python -m venv venv
    echo.
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat
echo.

REM Vérifier si les dépendances sont installées
echo Verification des dependances...
pip install -q -r requirements.txt
echo.

REM Vérifier la connexion à la base de données
echo Verification de la connexion a la base de donnees...
python manage.py check
if %errorlevel% neq 0 (
    echo.
    echo ERREUR: Impossible de se connecter a la base de donnees
    echo Verifiez votre fichier .env et PostgreSQL
    pause
    exit /b 1
)
echo.

REM Collecter les fichiers statiques
echo Collecte des fichiers statiques...
python manage.py collectstatic --noinput --clear
echo.

REM Démarrer le serveur
echo ================================
echo Demarrage du serveur Django...
echo URL: http://127.0.0.1:8000
echo Appuyez sur Ctrl+C pour arreter
echo ================================
echo.
python manage.py runserver

pause
