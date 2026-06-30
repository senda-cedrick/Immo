#!/usr/bin/env python
"""
Script pour mettre à jour les contrats existants avec le champ proprietaire.
"""

import os
import sys
import django

# Configurer Django
sys.path.append('/Users/tresorkabis/dev/Immo')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'immo_travel.settings')
django.setup()

from app_base.models import Contrat

def update_contrats():
    """Met à jour les contrats existants avec le propriétaire."""
    contrats = Contrat.objects.filter(proprietaire__isnull=True)
    updated = 0

    print(f"Trouvé {contrats.count()} contrats sans propriétaire")

    for contrat in contrats:
        try:
            if contrat.propriete:
                contrat.proprietaire = contrat.propriete.proprietaire
                print(f"Mise à jour de {contrat.reference} via propriété")
            elif contrat.logement:
                contrat.proprietaire = contrat.logement.propriete.proprietaire
                print(f"Mise à jour de {contrat.reference} via logement")
            else:
                print(f"Impossible de déterminer le propriétaire pour {contrat.reference}")
                continue

            contrat.save()
            updated += 1

        except Exception as e:
            print(f"Erreur lors de la mise à jour de {contrat.reference}: {e}")

    print(f"\nRésultat: {updated}/{contrats.count()} contrats mis à jour")

if __name__ == "__main__":
    update_contrats()