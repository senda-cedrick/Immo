#!/usr/bin/env python
"""
Script pour afficher les profils existants dans la base de données.
"""

import os
import sys
import django

# Ajouter le chemin du projet au path Python
sys.path.append('/Users/tresorkabis/dev/Immo')

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'immo_travel.settings')
django.setup()

from app_users.models import Profile

def display_profiles():
    """Affiche tous les profils existants dans la base de données."""
    print("\n" + "="*50)
    print("LISTE DES PROFILS EXISTANTS".center(50))
    print("="*50 + "\n")

    profiles = Profile.objects.all()

    if not profiles:
        print("Aucun profil trouvé dans la base de données.")
        return

    # Afficher l'en-tête du tableau
    print(f"{'ID':<5} {'NOM DU PROFIL':<30}")
    print("-" * 35)

    # Afficher chaque profil
    for profile in profiles:
        print(f"{profile.id:<5} {profile.name:<30}")

    print("\n" + "="*50)
    print(f"Total: {profiles.count()} profil(s)")
    print("="*50 + "\n")

    # Afficher des informations supplémentaires
    print("INFORMATIONS SUPPLÉMENTAIRES:")
    print("• Ces profils sont utilisés pour catégoriser les utilisateurs")
    print("• Chaque utilisateur peut avoir un seul profil")
    print("• Les profils sont gérés via l'interface d'administration")
    print("• URL d'accès: /user/profiles/ (nécessite une authentification)\n")

if __name__ == "__main__":
    display_profiles()