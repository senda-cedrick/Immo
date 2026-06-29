"""
Script de génération de données de démonstration pour le projet Immo.
Usage:
    python manage.py shell < scripts/demo_data.py

Ce script crée des données factices pour toutes les applications :
    - app_base : Agence, Personnel, Proprietaire, Client, Propriete, Logement, Contrat, etc.
    - app_users : Profile, User, LogUser
    - app_paiements : Paiement
    - app_caisse : Caisse
"""

import os
import sys
import django
from datetime import date, timedelta
from random import randint, choice
from decimal import Decimal
import uuid

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'immo_travel.settings')
django.setup()

from django.db import transaction
from django.utils import timezone
from datetime import date, timedelta
from random import randint, choice, uniform
from decimal import Decimal
from django.contrib.auth import get_user_model

from app_users.models import Profile, LogUser
from app_base.models import (
    Agence, Personnel, Proprietaire, Client,
    TypePropriete, TypeLogement, Propriete, Logement, Contrat, Garantie
)
from app_paiements.models import Paiement
from app_caisse.models import Caisse

User = get_user_model()


def clean_data():
    """Supprime toutes les données existantes dans l'ordre inverse des dépendances."""
    print("🗑️  Nettoyage des données existantes...")
    Caisse.objects.all().delete()
    Paiement.objects.all().delete()
    Garantie.objects.all().delete()
    Contrat.objects.all().delete()
    Logement.objects.all().delete()
    Propriete.objects.all().delete()
    TypePropriete.objects.all().delete()
    Client.objects.all().delete()
    Proprietaire.objects.all().delete()
    Personnel.objects.all().delete()
    Agence.objects.all().delete()
    LogUser.objects.all().delete()
    User.objects.all().delete()
    Profile.objects.all().delete()
    print("✅ Nettoyage terminé.\n")


def create_demo_data():
    """Crée les données de démonstration."""
    print("🚀 Création des données de démonstration...\n")
    
    # Utiliser une transaction pour assurer l'atomicité
    with transaction.atomic():

        # ──────────────────────────────────────────────
        # 1. PROFILES (app_users)
        # ──────────────────────────────────────────────
        profiles_data = [
            {'name': 'Administrateur'},
            {'name': 'Manager'},
            {'name': 'Agent'},
            {'name': 'Proprietaire'},
            {'name': 'Comptable'},
            {'name': 'Superviseur'},
            {'name': 'Client'},
        ]
        profiles = []
        for pdata in profiles_data:
            p, _ = Profile.objects.get_or_create(name=pdata['name'])
            profiles.append(p)
        print(f"✅ {len(profiles)} profils créés.")

        # ──────────────────────────────────────────────
        # 2. USERS (app_users)
        # ──────────────────────────────────────────────
        users_data = [
            {'username': 'admin',     'noms': 'Admin Système',      'email': 'admin@immo.local',   'profile_name': 'Administrateur', 'is_staff': True},
            {'username': 'manager1',  'noms': 'Jean Dupont',        'email': 'j.dupont@immo.local', 'profile_name': 'Manager', 'is_staff': True},
            {'username': 'agent1',    'noms': 'Marie Kabange',      'email': 'm.kabange@immo.local', 'profile_name': 'Agent'},
            {'username': 'proprio1',  'noms': 'Paul Mukendi',       'email': 'p.mukendi@immo.local', 'profile_name': 'Proprietaire'},
            {'username': 'compta1',   'noms': 'Alice Tshibangu',    'email': 'a.tshibangu@immo.local', 'profile_name': 'Comptable'},
            {'username': 'super1',    'noms': 'Georges Lumbala',    'email': 'g.lumbala@immo.local', 'profile_name': 'Superviseur'},
            {'username': 'client1',   'noms': 'Kakudji Pierre',     'email': 'kakudji@mail.com',     'profile_name': 'Client'},
            {'username': 'client2',   'noms': 'Mukendi Albert',     'email': 'mukendi@mail.com',     'profile_name': 'Client'},
        ]
        users = []
        for udata in users_data:
            defaults = {
                'noms': udata['noms'],
                'email': udata['email'],
                'profile': Profile.objects.get(name=udata['profile_name']),
            }
            if 'is_staff' in udata:
                defaults['is_staff'] = udata['is_staff']
            u, created = User.objects.get_or_create(
                username=udata['username'],
                defaults=defaults,
            )
            if created:
                u.set_password('demo')
                u.save()
            users.append(u)
        # Créer un superuser si pas déjà fait
        if not User.objects.filter(is_superuser=True).exists():
            su = User.objects.create_superuser(
                username='superadmin',
                email='superadmin@immo.local',
                password='admin123',
                noms='Super Administrateur'
            )
            users.insert(0, su)
            print(f"✅ Superuser 'superadmin' créé (mot de passe: admin123)")
        print(f"✅ {len(users)} utilisateurs créés.")

        # ──────────────────────────────────────────────
        # 3. AGENCES (app_base)
        # ──────────────────────────────────────────────
        agences_data = [
            {'nom': 'Agence Centre-Ville', 'adresse': '123 Av. du Centre, Kinshasa', 'telephone': '+243810000001', 'email': 'centre@immo.cd', 'active': True},
            {'nom': 'Agence Gombe', 'adresse': '456 Bd. du 30 Juin, Gombe', 'telephone': '+243810000002', 'email': 'gombe@immo.cd', 'active': True},
        ]
        agences = [Agence.objects.get_or_create(nom=a['nom'], defaults=a)[0] for a in agences_data]
        print(f"✅ {len(agences)} agences créées.")

        # ──────────────────────────────────────────────
        # 4. PERSONNEL (app_base)
        # ──────────────────────────────────────────────
        personnel_data = [
            {'user': User.objects.get(username='manager1'), 'agence': agences[0], 'sexe': 'M', 'telephone': '+243820000001'},
            {'user': User.objects.get(username='agent1'), 'agence': agences[0], 'sexe': 'F', 'telephone': '+243820000002'},
        ]
        for pdata in personnel_data:
            Personnel.objects.get_or_create(user=pdata['user'], defaults=pdata)
        print(f"✅ {len(personnel_data)} personnels créés.")

        # ──────────────────────────────────────────────
        # 5. PROPRIETAIRES (app_base)
        # ──────────────────────────────────────────────
        proprietaires_data = [
            {'user': User.objects.get(username='proprio1'), 'agence': agences[0], 'telephone': '+243990000001', 'adresse': '10 Av. des propriétaires'},
        ]
        for pr in proprietaires_data:
            Proprietaire.objects.get_or_create(user=pr['user'], defaults=pr)
        print(f"✅ {len(proprietaires_data)} propriétaires créés.")

        # ──────────────────────────────────────────────
        # 6. CLIENTS (app_base)
        # ──────────────────────────────────────────────
        clients_data = [
            {'user': User.objects.get(username='client1'), 'agence': agences[0], 'telephone': '+243811000001', 'adresse': '25 Av. des clients'},
            {'user': User.objects.get(username='client2'), 'agence': agences[1], 'telephone': '+243811000002', 'adresse': '30 Av. des palmiers'},
        ]
        for cl in clients_data:
            Client.objects.get_or_create(user=cl['user'], defaults=cl)
        print(f"✅ {len(clients_data)} clients créés.")

        # ──────────────────────────────────────────────
        # 7. TYPES DE PROPRIETE (app_base)
        # ──────────────────────────────────────────────
        types_propriete_data = [
            {'nom': 'Immeuble', 'description': 'Bâtiment multi-étages avec plusieurs appartements ou bureaux, souvent situé en zone urbaine.'},
            {'nom': 'Villa', 'description': 'Maison individuelle de standing avec jardin, généralement située en zone résidentielle.'},
            {'nom': 'Appartement', 'description': 'Unité résidentielle faisant partie d\'un bâtiment plus grand, idéale pour la location urbaine.'},
            {'nom': 'Studio', 'description': 'Petit espace compact avec une seule pièce principale servant de salon, chambre et cuisine.'},
        ]
        types_propriete = []
        for type_data in types_propriete_data:
            type_obj, created = TypePropriete.objects.get_or_create(
                nom=type_data['nom'],
                defaults={'description': type_data['description']}
            )
            types_propriete.append(type_obj)
        print(f"✅ {len(types_propriete)} types de propriété créés avec descriptions.")

        # ──────────────────────────────────────────────
        # 7.1. TYPES DE LOGEMENT (app_base) - Granularité supplémentaire
        # ──────────────────────────────────────────────
        types_logement_data = [
            {'nom': 'Studio', 'description': 'Petit logement avec une seule pièce principale combinant salon, chambre et cuisine.'},
            {'nom': 'Appartement standard', 'description': 'Logement classique avec salon séparé, chambre(s) et cuisine.'},
            {'nom': 'Duplex', 'description': 'Logement sur deux niveaux avec escalier intérieur, souvent plus spacieux.'},
            {'nom': 'Penthouse', 'description': 'Logement de luxe situé au dernier étage avec terrasse et vue panoramique.'},
            {'nom': 'Maison individuelle', 'description': 'Logement indépendant avec accès direct à l\'extérieur et souvent un jardin.'},
            {'nom': 'Loft', 'description': 'Grand espace ouvert avec hauts plafonds, souvent dans un bâtiment industriel reconverti.'},
        ]
        types_logement = []
        for type_data in types_logement_data:
            type_obj, created = TypeLogement.objects.get_or_create(
                nom=type_data['nom'],
                defaults={'description': type_data['description']}
            )
            types_logement.append(type_obj)
        print(f"✅ {len(types_logement)} types de logement créés pour plus de granularité.")

        # ──────────────────────────────────────────────
        # 8. PROPRIETES (app_base) - Données diversifiées
        # ──────────────────────────────────────────────
        proprio_obj = Proprietaire.objects.first()
        agent_obj = Personnel.objects.filter(user__profile__name='Agent').first()
        proprietes_data = [
            {'agence': agences[0], 'proprietaire': proprio_obj, 'type_propriete': types_propriete[0], 'adresse': '100 Av. de la Liberté', 'ville': 'Kinshasa/Gombe', 'superficie': 1200, 'nb_pieces': 15, 'statut': 'LOUE', 'agent': agent_obj},
            {'agence': agences[1], 'proprietaire': proprio_obj, 'type_propriete': types_propriete[1], 'adresse': '200 Av. de la Paix', 'ville': 'Kinshasa/Ngaliema', 'superficie': 800, 'nb_pieces': 8, 'statut': 'DISPONIBLE'},
            {'agence': agences[0], 'proprietaire': proprio_obj, 'type_propriete': types_propriete[2], 'adresse': '300 Bd Lumumba', 'ville': 'Kinshasa/Lingwala', 'superficie': 600, 'nb_pieces': 6, 'statut': 'LOUE', 'agent': agent_obj},
            {'agence': agences[1], 'proprietaire': proprio_obj, 'type_propriete': types_propriete[3], 'adresse': '400 Rue Commerce', 'ville': 'Kinshasa/Kintambo', 'superficie': 400, 'nb_pieces': 4, 'statut': 'DISPONIBLE'},
            {'agence': agences[0], 'proprietaire': proprio_obj, 'type_propriete': types_propriete[0], 'adresse': '500 Av des Martyrs', 'ville': 'Kinshasa/Bandundu', 'superficie': 900, 'nb_pieces': 10, 'statut': 'MAINTENANCE', 'agent': agent_obj},
        ]
        proprietes = [Propriete.objects.get_or_create(adresse=p['adresse'], defaults=p)[0] for p in proprietes_data]
        print(f"✅ {len(proprietes_data)} propriétés créées.")

        # ──────────────────────────────────────────────
        # 9. LOGEMENTS (app_base) - Données diversifiées
        # ──────────────────────────────────────────────
        logements_data = [
            # Logements pour la propriété 1 (100 Av. de la Liberté - Immeuble)
            {'propriete': proprietes[0], 'identifiant': 'A-101', 'surface': 80, 'etage': 1, 'description': 'Studio avec balcon'},
            {'propriete': proprietes[0], 'identifiant': 'A-102', 'surface': 85, 'etage': 1, 'description': 'Appartement 2 pièces'},
            {'propriete': proprietes[0], 'identifiant': 'B-201', 'surface': 120, 'etage': 2, 'description': 'Grand appartement 3 pièces'},
            {'propriete': proprietes[0], 'identifiant': 'B-202', 'surface': 95, 'etage': 2, 'description': 'Appartement avec vue'},
            {'propriete': proprietes[0], 'identifiant': 'C-301', 'surface': 110, 'etage': 3, 'description': 'Penthouse luxueux'},

            # Logements pour la propriété 2 (200 Av. de la Paix - Villa)
            {'propriete': proprietes[1], 'identifiant': 'V-001', 'surface': 200, 'etage': 1, 'description': 'Maison complète avec jardin'},
            {'propriete': proprietes[1], 'identifiant': 'V-002', 'surface': 150, 'etage': 1, 'description': 'Appartement indépendant'},

            # Logements pour la propriété 3 (300 Bd Lumumba - Appartement)
            {'propriete': proprietes[2], 'identifiant': 'APT-101', 'surface': 60, 'etage': 1, 'description': 'Studio économique'},
            {'propriete': proprietes[2], 'identifiant': 'APT-102', 'surface': 65, 'etage': 1, 'description': 'Studio avec kitchenette'},
            {'propriete': proprietes[2], 'identifiant': 'APT-201', 'surface': 75, 'etage': 2, 'description': 'Appartement 1 pièce'},

            # Logements pour la propriété 4 (400 Rue Commerce - Studio)
            {'propriete': proprietes[3], 'identifiant': 'ST-101', 'surface': 35, 'etage': 1, 'description': 'Studio compact'},
            {'propriete': proprietes[3], 'identifiant': 'ST-102', 'surface': 40, 'etage': 1, 'description': 'Studio avec mezzanine'},
        ]
        for lg in logements_data:
            Logement.objects.get_or_create(propriete=lg['propriete'], identifiant=lg['identifiant'], defaults=lg)
        print(f"✅ {len(logements_data)} logements créés.")

        # ──────────────────────────────────────────────
        # 9.0.5. TYPES DE LOGEMENTS - Granularité supplémentaire
        # ──────────────────────────────────────────────
        # Associer des types spécifiques à chaque logement pour démontrer la granularité
        Logement.objects.filter(identifiant='A-101').update(type_logement=types_logement[0])  # Studio
        Logement.objects.filter(identifiant='A-102').update(type_logement=types_logement[1])  # Appartement standard
        Logement.objects.filter(identifiant='B-201').update(type_logement=types_logement[1])  # Appartement standard
        Logement.objects.filter(identifiant='B-202').update(type_logement=types_logement[2])  # Duplex
        Logement.objects.filter(identifiant='C-301').update(type_logement=types_logement[3])  # Penthouse

        Logement.objects.filter(identifiant='V-001').update(type_logement=types_logement[4])  # Maison individuelle
        Logement.objects.filter(identifiant='V-002').update(type_logement=types_logement[1])  # Appartement standard

        Logement.objects.filter(identifiant='APT-101').update(type_logement=types_logement[0])  # Studio
        Logement.objects.filter(identifiant='APT-102').update(type_logement=types_logement[0])  # Studio
        Logement.objects.filter(identifiant='APT-201').update(type_logement=types_logement[1])  # Appartement standard

        Logement.objects.filter(identifiant='ST-101').update(type_logement=types_logement[0])  # Studio
        Logement.objects.filter(identifiant='ST-102').update(type_logement=types_logement[5])  # Loft

        print("✅ Types de logements attribués (démonstration de la granularité)")

        # ──────────────────────────────────────────────
        # 9.1. STATUTS DES LOGEMENTS - Démonstration de la diversité
        # ──────────────────────────────────────────────
        # Mettre à jour les statuts pour montrer que différents logements
        # dans une même propriété peuvent avoir des statuts différents
        Logement.objects.filter(identifiant='A-101').update(statut='LOUE')  # Loué (contrat actif)
        Logement.objects.filter(identifiant='A-102').update(statut='DISPONIBLE')  # Disponible
        Logement.objects.filter(identifiant='B-201').update(statut='LOUE')  # Loué
        Logement.objects.filter(identifiant='B-202').update(statut='DISPONIBLE')  # Disponible
        Logement.objects.filter(identifiant='C-301').update(statut='DISPONIBLE')  # Disponible

        Logement.objects.filter(identifiant='V-001').update(statut='LOUE')  # Loué
        Logement.objects.filter(identifiant='V-002').update(statut='DISPONIBLE')  # Disponible

        Logement.objects.filter(identifiant='APT-101').update(statut='LOUE')  # Loué (contrat actif)
        Logement.objects.filter(identifiant='APT-102').update(statut='DISPONIBLE')  # Disponible
        Logement.objects.filter(identifiant='APT-201').update(statut='DISPONIBLE')  # Disponible

        Logement.objects.filter(identifiant='ST-101').update(statut='DISPONIBLE')  # Disponible
        Logement.objects.filter(identifiant='ST-102').update(statut='DISPONIBLE')  # Disponible

        print("✅ Statuts des logements mis à jour (démonstration de la diversité)")

        # ──────────────────────────────────────────────
        # 10. CONTRATS (app_base) - Cohérence avec les propriétés louées
        # ──────────────────────────────────────────────
        client1 = Client.objects.get(user__username='client1')
        client2 = Client.objects.get(user__username='client2')
        logement1 = Logement.objects.get(identifiant='A-101')  # Propriété 1 (LOUE)
        logement3 = Logement.objects.get(identifiant='APT-101')  # Propriété 3 (LOUE)

        # Créer un troisième client pour les contrats supplémentaires
        client3 = Client.objects.get(user__username='client1')  # Réutiliser client1 pour B-201
        client4 = Client.objects.get(user__username='client2')  # Réutiliser client2 pour V-001

        # Récupérer les logements marqués comme LOUE
        logement_b201 = Logement.objects.get(identifiant='B-201')  # Loué sans contrat
        logement_v001 = Logement.objects.get(identifiant='V-001')  # Loué sans contrat

        contrats_data = [
            {
                'reference': 'LOC-2024-001', 'type': 'LOCATION',
                'logement': logement1, 'propriete': None, # Lié au logement, pas à la propriété entière
                'client': client1, 'agent': agent_obj,
                'date_debut': date.today() - timedelta(days=100), 'montant': Decimal('450.00'),
                'conditions': 'Loyer mensuel, payable avant le 5 de chaque mois.', 'statut': 'ACTIF'
            },
            {
                'reference': 'LOC-2024-002', 'type': 'LOCATION',
                'logement': logement3, 'propriete': None, # Propriété 3 (300 Bd Lumumba) - LOUE
                'client': client2, 'agent': agent_obj,
                'date_debut': date.today() - timedelta(days=80), 'montant': Decimal('350.00'),
                'conditions': 'Loyer mensuel, caution incluse.', 'statut': 'ACTIF'
            },
            {
                'reference': 'LOC-2024-003', 'type': 'LOCATION',
                'logement': logement_b201, 'propriete': None, # B-201 - LOUE
                'client': client3, 'agent': agent_obj,
                'date_debut': date.today() - timedelta(days=90), 'montant': Decimal('550.00'),
                'conditions': 'Loyer mensuel, appartement premium.', 'statut': 'ACTIF'
            },
            {
                'reference': 'LOC-2024-004', 'type': 'LOCATION',
                'logement': logement_v001, 'propriete': None, # V-001 - LOUE
                'client': client4, 'agent': agent_obj,
                'date_debut': date.today() - timedelta(days=70), 'montant': Decimal('600.00'),
                'conditions': 'Loyer mensuel, maison avec jardin.', 'statut': 'ACTIF'
            }
        ]
        contrats = [Contrat.objects.get_or_create(reference=c['reference'], defaults=c)[0] for c in contrats_data]
        print(f"✅ {len(contrats)} contrats créés.")

        # ──────────────────────────────────────────────
        # 10.5. GARANTIES (app_base) - Associées aux contrats
        # ──────────────────────────────────────────────
        garanties_data = [
            {
                'contrat': contrats[0],
                'montant': Decimal('900.00'),
                'type_garantie': 'UNIQUE',
                'statut': 'VERSEE',
                'date_constitution': date.today() - timedelta(days=95),
                'notes': 'Caution de 2 mois de loyer pour le contrat LOC-2024-001'
            },
            {
                'contrat': contrats[1],
                'montant': Decimal('700.00'),
                'type_garantie': 'UNIQUE',
                'statut': 'VERSEE',
                'date_constitution': date.today() - timedelta(days=75),
                'notes': 'Caution de 2 mois de loyer pour le contrat LOC-2024-002'
            },
            {
                'contrat': contrats[2],
                'montant': Decimal('1100.00'),
                'type_garantie': 'UNIQUE',
                'statut': 'EN_ATTENTE',
                'date_constitution': date.today() - timedelta(days=85),
                'notes': 'Caution en attente de validation pour le contrat LOC-2024-003'
            },
            {
                'contrat': contrats[3],
                'montant': Decimal('1200.00'),
                'type_garantie': 'UNIQUE',
                'statut': 'VERSEE',
                'date_constitution': date.today() - timedelta(days=65),
                'notes': 'Caution de 2 mois de loyer pour le contrat LOC-2024-004'
            }
        ]
        garanties = [Garantie.objects.create(**g) for g in garanties_data]
        print(f"✅ {len(garanties)} garanties créées.")

        # ──────────────────────────────────────────────
        # 11. PAIEMENTS (app_paiements)
        # ──────────────────────────────────────────────
        contrat_actif = contrats[0]
        client_actif = contrat_actif.client
        # Création de 3 paiements pour le contrat actif
        paiements_data = [
            {
                'contrat': contrat_actif, 'client': client_actif, 'montant': 450,
                'date_paiement': date.today() - timedelta(days=65), 'date_echeance': date.today() - timedelta(days=70),
                'type_paiement': 'LOYER', 'statut': 'PAYE'
            },
            {
                'contrat': contrat_actif, 'client': client_actif, 'montant': 450,
                'date_paiement': date.today() - timedelta(days=35), 'date_echeance': date.today() - timedelta(days=40),
                'type_paiement': 'LOYER', 'statut': 'PAYE'
            },
            {
                'contrat': contrat_actif, 'client': client_actif, 'montant': 450,
                'date_paiement': None, 'date_echeance': date.today() - timedelta(days=10),
                'type_paiement': 'LOYER', 'statut': 'EN_RETARD'
            },
        ]
        for p in paiements_data:
            Paiement.objects.create(**p)
        print(f"✅ {len(paiements_data)} paiements créés.")

        # ──────────────────────────────────────────────
        # 12. CAISSE (app_caisse) - Données enrichies
        # ──────────────────────────────────────────────
        paiements = list(Paiement.objects.filter(date_paiement__isnull=False).order_by('date_paiement'))

        # Créer des données de caisse variées pour démontrer toutes les fonctionnalités
        caisse_data = []

        # Entrées de caisse liées à des paiements (loyers perçus)
        for i, paiement in enumerate(paiements[:3]):  # 3 premières entrées liées à des paiements
            caisse_data.append({
                'type_caisse': 'ENTREE',
                'status_caisse': 'VALIDATED',
                'cout': paiement.montant,
                'paiement': paiement,
                'details': f'Loyer perçu - Contrat {paiement.contrat.reference}'
            })

        # Autres entrées de caisse (revenus divers)
        caisse_data.extend([
            {
                'type_caisse': 'ENTREE',
                'status_caisse': 'VALIDATED',
                'cout': Decimal('200.00'),
                'paiement': None,
                'details': 'Frais de dossier - Nouveau client'
            },
            {
                'type_caisse': 'ENTREE',
                'status_caisse': 'PENDING',
                'cout': Decimal('150.00'),
                'paiement': None,
                'details': 'Caution - Appartement A-102 (en attente de validation)'
            },
            {
                'type_caisse': 'ENTREE',
                'status_caisse': 'VALIDATED',
                'cout': Decimal('75.00'),
                'paiement': None,
                'details': 'Frais de visite - Propriété 200 Av. de la Paix'
            },
        ])

        # Sorties de caisse (dépenses)
        caisse_data.extend([
            {
                'type_caisse': 'SORTIE',
                'status_caisse': 'VALIDATED',
                'cout': Decimal('120.00'),
                'paiement': None,
                'details': 'Remboursement caution - Client précédent'
            },
            {
                'type_caisse': 'SORTIE',
                'status_caisse': 'VALIDATED',
                'cout': Decimal('85.00'),
                'paiement': None,
                'details': 'Frais de réparation - Robinet fuite A-101'
            },
            {
                'type_caisse': 'SORTIE',
                'status_caisse': 'REJECTED',
                'cout': Decimal('300.00'),
                'paiement': None,
                'details': 'Achat matériel - Refusé (budget dépassé)'
            },
            {
                'type_caisse': 'SORTIE',
                'status_caisse': 'PENDING',
                'cout': Decimal('60.00'),
                'paiement': None,
                'details': 'Frais de ménage - En attente d\'approbation'
            },
        ])

        # Créer toutes les entrées de caisse
        for c in caisse_data:
            Caisse.objects.create(**c)

        print(f"✅ {len(caisse_data)} entrées de caisse créées.")

        # ──────────────────────────────────────────────
        # 13. LOGS (app_users)
        # ──────────────────────────────────────────────
        LogUser.objects.create(
            user=User.objects.get(username='admin'),
            action='CREATE'
        )
        print("✅ Journal système créé.")

        # ──────────────────────────────────────────────
        print("\n🎉 Données de démonstration créées avec succès !")
        print(f"   - {Profile.objects.count()} profils")
        print(f"   - {User.objects.count()} utilisateurs")
        print(f"   - {Agence.objects.count()} agences")
        print(f"   - {Personnel.objects.count()} membres du personnel")
        print(f"   - {Proprietaire.objects.count()} propriétaires")
        print(f"   - {Client.objects.count()} clients")
        print(f"   - {Propriete.objects.count()} propriétés")
        print(f"   - {Logement.objects.count()} logements")
        print(f"   - {Contrat.objects.count()} contrats")
        print(f"   - {Garantie.objects.count()} garanties")
        print(f"   - {Paiement.objects.count()} paiements")
        print(f"   - {Caisse.objects.count()} entrées de caisse")


if __name__ == '__main__':
    clean_data()
    create_demo_data()