#!/bin/bash
# Script pour charger les données de démonstration du projet Immo
# Usage : ./load_demo_data.sh
#
# Étapes :
#   1. Active / crée l'environnement virtuel
#   2. Supprime et recrée la base de données PostgreSQL (immo_db)
#   3. Supprime TOUS les fichiers de migration (sauf __init__.py)
#   4. Recrée les migrations pour chaque application
#   5. Exécute les migrations
#   6. Génère les données de démonstration

set -e  # Arrêter le script en cas d'erreur

echo "========================================="
echo "  Chargement des données de démonstration"
echo "  Projet Immo"
echo "========================================="
echo ""

# ─── 1. Environnement virtuel ───────────────────
if [ -d ".venv" ]; then
    echo "🔧 Activation de l'environnement virtuel..."
    source .venv/bin/activate
else
    echo "⚠️  Aucun environnement virtuel trouvé (.venv)."
    echo "   Création d'un environnement virtuel..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "   Installation des dépendances..."
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi
fi

# Vérifier si Django est accessible
if ! python -c "import django" 2>/dev/null; then
    echo "❌ Django n'est pas installé. Installation en cours..."
    pip install -r requirements.txt
fi

# ─── 2. Suppression et recréation de la base de données PostgreSQL ──
echo ""
echo "🗄️  Connexion à PostgreSQL..."

# Charger les variables depuis un fichier .env s'il existe, sinon utiliser des valeurs par défaut
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

DB_NAME=${DB_NAME:-immo_db}
DB_USER=${DB_USER:-postgres}
DB_PASS=${DB_PASS:-postgres}
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
# Vérifier que PostgreSQL est accessible
if command -v psql &> /dev/null; then
    echo "   ️ Suppression de la base de données '$DB_NAME'..."
    # Terminer toutes les connexions actives
    PGPASSWORD="$DB_PASS" psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d postgres -t -c "
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = '$DB_NAME'
          AND pid <> pg_backend_pid();
    " 2>/dev/null || echo "   ⚠️  Aucune connexion active à terminer."
    
    # Supprimer la base
    PGPASSWORD="$DB_PASS" psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;" 2>/dev/null || {
        echo "   ⚠️  Impossible de supprimer la base (peut-être n'existe-t-elle pas)."
    }
    
    # Créer la base
    echo "   ✅ Création de la base de données '$DB_NAME'..."
    PGPASSWORD="$DB_PASS" psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d postgres -c "CREATE DATABASE $DB_NAME;" 2>/dev/null || {
        echo "   ❌ Échec de la création de la base de données."
        echo "   Vérifiez que PostgreSQL est en cours d'exécution."
        echo "   Commande pour démarrer PostgreSQL : brew services start postgresql"
        exit 1
    }
    echo "✅ Base de données '$DB_NAME' recréée avec succès."
else
    echo "⚠️  psql non trouvé. Assurez-vous que PostgreSQL est installé."
    exit 1
fi

# ─── 3. Suppression de TOUS les fichiers de migration ───
echo ""
echo "🗑️  Suppression des anciens fichiers de migration..."
APPS=("app_base" "app_users" "app_paiements" "app_caisse" "app_report")
for APP in "${APPS[@]}"; do
    MIGRATIONS_DIR="$APP/migrations"
    if [ -d "$MIGRATIONS_DIR" ]; then
        echo "   → $APP"
        find "$MIGRATIONS_DIR" -type f -name "*.py" ! -name "__init__.py" -delete
        find "$MIGRATIONS_DIR" -type f -name "*.pyc" -delete
    fi
done
echo "✅ Anciens fichiers de migration supprimés."

# ─── 4. Recréation des migrations ────────────────
echo ""
echo "🔄 Recréation des migrations..."
python manage.py makemigrations app_base app_users app_paiements app_caisse app_report

# ─── 5. Application des migrations ───────────────
echo ""
echo "🚀 Application des migrations..."
python manage.py migrate

# ─── 6. Génération des données de démonstration ──
echo ""
echo "📦 Génération des données de démonstration..."
python scripts/reset_demo.py

echo ""
echo "========================================="
echo "  ✅ Données chargées avec succès !"
echo "========================================="
echo ""
echo "   Utilisateurs créés (mot de passe par défaut : demo) :"
echo "   - Superadmin   : superadmin / admin123"
echo "   - Manager      : manager1"
echo "   - Agent        : agent1"
echo "   - Propriétaire : proprio1"
echo "   - Client       : client1"
echo ""
echo "   Connexion : http://127.0.0.1:8000/user/login/"
