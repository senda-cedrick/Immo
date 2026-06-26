"""
Script de migration des données de l'ancienne modélisation vers la nouvelle.
À exécuter après makemigrations et migrate.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'immo_travel.settings')
django.setup()

from app_base.models import (
    Agence as OldAgence, Personnel as OldPersonnel,
    Proprietaire as OldProprietaire, Appartement,
    TypePropriete as OldTypePropriete, Propriete as OldPropriete,
    Locataire as OldLocataire, Logement as OldLogement,
    Garantie as OldGarantie
)
from app_paiements.models import Paiement as OldPaiement, Impayes as OldImpayes
from app_caisse.models import Caisse as OldCaisse

from app_users.models import Profile, User
from app_base.models import (
    Agence, Personnel, Proprietaire, Client,
    TypePropriete, Propriete, Logement,
    Contrat, Maintenance, Garantie
)
from app_paiements.models import Paiement
from app_caisse.models import Caisse


def migrate_agences():
    """Migre les agences anciennes vers nouvelles"""
    print("Migration des agences...")
    count = 0
    for old in OldAgence.objects.all():
        new, created = Agence.objects.get_or_create(
            nom=old.nom,
            defaults={
                'adresse': '',
                'telephone': '',
                'email': old.email,
                'numero_impot': old.numero_impot or '',
                'numero_fisc': old.numero_fisc or '',
                'active': old.active,
            }
        )
        if created:
            count += 1
    print(f"  → {count} agences créées")


def migrate_type_proprietes():
    """Migre les types de propriété"""
    print("Migration des types de propriété...")
    count = 0
    for old in OldTypePropriete.objects.all():
        new, created = TypePropriete.objects.get_or_create(
            nom=old.nom,
            defaults={'description': ''}
        )
        if created:
            count += 1
    print(f"  → {count} types créés")


def migrate_proprietaires():
    """Migre les propriétaires"""
    print("Migration des propriétaires...")
    count = 0
    for old in OldProprietaire.objects.all():
        # Créer un User fictif ou lier à un User existant si possible
        user, _ = User.objects.get_or_create(
            email=old.email,
            defaults={'noms': old.noms, 'username': old.email}
        )
        
        # Créer le profil Proprietaire si absent
        profile, _ = Profile.objects.get_or_create(name='Proprietaire')
        user.profile = profile
        user.save()
        
        # Créer le profil Proprietaire
        prop, created = Proprietaire.objects.get_or_create(
            user=user,
            defaults={
                'telephone': '',
                'adresse': '',
            }
        )
        if created:
            count += 1
    print(f"  → {count} propriétaires créés")


def migrate_locataires_to_clients():
    """Migre les locataires vers clients"""
    print("Migration des locataires vers clients...")
    count = 0
    for old in OldLocataire.objects.all():
        user, _ = User.objects.get_or_create(
            email=old.email,
            defaults={'noms': old.noms, 'username': old.email}
        )
        
        profile, _ = Profile.objects.get_or_create(name='Client')
        user.profile = profile
        user.save()
        
        # Récupérer l'agence depuis un contrat existant ou utiliser la première
        agence = Agence.objects.first()
        
        client, created = Client.objects.get_or_create(
            user=user,
            defaults={
                'agence': agence,
                'telephone': old.telephone or '',
                'adresse': '',
            }
        )
        if created:
            count += 1
    print(f"  → {count} clients créés")


def migrate_proprietes():
    """Migre les propriétés"""
    print("Migration des propriétés...")
    count = 0
    for old in OldPropriete.objects.all():
        # Trouver le propriétaire (premier disponible)
        proprietaire = Proprietaire.objects.first()
        if not proprietaire:
            print("  ⚠ Aucun propriétaire disponible, skip")
            continue
            
        new, created = Propriete.objects.get_or_create(
            type_propriete__nom=old.type_propriete.nom if old.type_propriete else 'Maison',
            adresse=old.description or '',
            defaults={
                'proprietaire': proprietaire,
                'ville': old.ville or '',
                'superficie': old.surface or 0,
                'nb_pieces': None,
                'description': old.description or '',
                'statut': 'DISPONIBLE',
            }
        )
        if created:
            count += 1
    print(f"  → {count} propriétés créées")


def migrate_appartements_to_logements():
    """Migre les appartements vers logements"""
    print("Migration des appartements vers logements...")
    count = 0
    for old in Appartement.objects.all():
        # Trouver une propriété associée
        propriete = Propriete.objects.first()
        if not propriete:
            continue
            
        log, created = Logement.objects.get_or_create(
            propriete=propriete,
            identifiant=old.identifiant,
            defaults={
                'surface': old.surface,
                'etage': old.etage,
                'description': old.description or '',
            }
        )
        if created:
            count += 1
    print(f"  → {count} logements créés")


def migrate_contrats():
    """Crée des contrats fictifs pour les paiements existants"""
    print("Création des contrats de liaison...")
    count = 0
    for old in OldPaiement.objects.select_related('locataires').all():
        try:
            client = Client.objects.get(user__email=old.locataires.email)
            propriete = Propriete.objects.first()
            proprietaire = Proprietaire.objects.first()
            
            if not propriete or not proprietaire or not client:
                continue
            
            ref = f"CONT-{old.id:06d}"
            contrat, created = Contrat.objects.get_or_create(
                reference=ref,
                defaults={
                    'type': 'LOCATION',
                    'statut': 'ACTIF',
                    'propriete': propriete,
                    'client': client,
                    'proprietaire': proprietaire,
                    'date_debut': old.date_paie,
                    'date_fin': None,
                    'montant': old.montant or 0,
                    'conditions': 'Contrat migré automatiquement',
                }
            )
            if created:
                count += 1
        except Exception as e:
            print(f"  ⚠ Erreur sur paiement {old.id}: {e}")
    print(f"  → {count} contrats créés")


def migrate_paiements():
    """Migre les paiements anciens vers nouveaux"""
    print("Migration des paiements...")
    count = 0
    for old in OldPaiement.objects.all():
        try:
            # Trouver le contrat correspondant
            contrat = Contrat.objects.filter(reference=f"CONT-{old.id:06d}").first()
            if not contrat:
                continue
                
            new, created = Paiement.objects.get_or_create(
                contrat=contrat,
                montant=old.montant or 0,
                date_paiement=old.date_paie,
                defaults={
                    'date_echeance': old.date_normal or old.date_paie,
                    'mode_paiement': 'CASH',
                    'reference': '',
                    'statut': 'PAYE',
                }
            )
            if created:
                count += 1
        except Exception as e:
            print(f"  ⚠ Erreur sur paiement {old.id}: {e}")
    print(f"  → {count} paiements créés")




def run_migration():
    """Exécute toutes les migrations"""
    print("=" * 50)
    print("DÉBUT DE LA MIGRATION")
    print("=" * 50)
    
    migrate_agences()
    migrate_type_proprietes()
    migrate_proprietaires()
    migrate_locataires_to_clients()
    migrate_proprietes()
    migrate_appartements_to_logements()
    migrate_contrats()
    migrate_paiements()
    
    print("=" * 50)
    print("MIGRATION TERMINÉE")
    print("=" * 50)


if __name__ == '__main__':
    run_migration()