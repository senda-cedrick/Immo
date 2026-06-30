#!/usr/bin/env python
"""
Script pour vérifier si les contrats ont des propriétaires.
"""

import os
import sys
import django

# Configurer Django
sys.path.append('/Users/tresorkabis/dev/Immo')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'immo_travel.settings')
django.setup()

from app_base.models import Contrat

def check_contrats():
    """Vérifie si tous les contrats ont des propriétaires."""
    contrats = Contrat.objects.all()
    print(f"Nombre de contrats: {contrats.count()}")

    for contrat in contrats:
        try:
            proprietaire_nom = contrat.proprietaire.user.noms if contrat.proprietaire else "AUCUN"
            print(f"{contrat.reference}: proprietaire={proprietaire_nom}")
        except Exception as e:
            print(f"{contrat.reference}: ERREUR - {e}")

if __name__ == "__main__":
    check_contrats()