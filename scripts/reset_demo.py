#!/usr/bin/env python3
"""
Script unique pour réinitialiser et peupler la base de données avec des données de démonstration.
Ce script combine les fonctionnalités de clean_data(), create_demo_data() et populate_demo_images()
avec des options supplémentaires pour le contrôle du processus.

Usage:
    python scripts/reset_demo.py [--limit N] [--query QUERY] [--wipe-media]

Options:
    --limit N       Limite le nombre de propriétés/logements à traiter pour les images
    --query QUERY   Mot-clé de recherche pour Unsplash (ex: apartment, kitchen, house)
    --wipe-media    Supprime les médias existants avant de télécharger de nouvelles images

Exemples:
    python scripts/reset_demo.py
    python scripts/reset_demo.py --limit 5 --query "luxury apartment"
    python scripts/reset_demo.py --wipe-media --limit 10
"""

import os
import sys
import argparse
import urllib.request
import ssl
import certifi
import re
import urllib.parse
import random
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone
from datetime import date, timedelta
from random import randint, choice, uniform
from decimal import Decimal
from pathlib import Path

# Ajouter le répertoire racine du projet au chemin Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Préparer l'environnement Django
PROJECT_SETTINGS = os.environ.get('DJANGO_SETTINGS_MODULE', 'immo_travel.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', PROJECT_SETTINGS)

import django
django.setup()

from django.contrib.auth import get_user_model
from app_users.models import Profile, LogUser
from app_base.models import (
    Agence, Personnel, Proprietaire, Client,
    TypePropriete, TypeLogement, Propriete, Logement, Contrat, Garantie, ProprieteImage, LogementImage
)
from app_paiements.models import Paiement
from app_caisse.models import Caisse

User = get_user_model()

def clean_data():
    """Supprime toutes les données existantes dans l'ordre inverse des dépendances."""
    print("🗑️  Nettoyage des données existantes...")
    # Ordre important pour éviter les violations de contraintes
    Caisse.objects.all().delete()
    Paiement.objects.all().delete()
    Garantie.objects.all().delete()
    Contrat.objects.all().delete()
    LogementImage.objects.all().delete()
    ProprieteImage.objects.all().delete()
    Logement.objects.all().delete()
    Propriete.objects.all().delete()
    TypePropriete.objects.all().delete()
    TypeLogement.objects.all().delete()
    Client.objects.all().delete()
    Proprietaire.objects.all().delete()
    Personnel.objects.all().delete()
    Agence.objects.all().delete()
    LogUser.objects.all().delete()
    User.objects.all().delete()
    Profile.objects.all().delete()
    print("✅ Nettoyage terminé.\n")

def create_demo_data():
    """Crée les données de démonstration complètes."""
    print("🚀 Création des données de démonstration...\n")

    with transaction.atomic():
        # 1. PROFILES
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

        # 2. USERS
        users_data = [
            {'username': 'admin',     'noms': 'Admin Système',      'email': 'admin@immo.local',   'profile_name': 'Administrateur', 'is_staff': True},
            {'username': 'manager1',  'noms': 'Jean Dupont',        'email': 'j.dupont@immo.local', 'profile_name': 'Manager', 'is_staff': True},
            {'username': 'agent1',    'noms': 'Marie Kabange',      'email': 'm.kabange@immo.local', 'profile_name': 'Agent'},
            {'username': 'agent2',    'noms': 'Lucie Mbuyi',        'email': 'l.mbuyi@immo.local',   'profile_name': 'Agent'},
            {'username': 'proprio1',  'noms': 'Paul Mukendi',       'email': 'p.mukendi@immo.local', 'profile_name': 'Proprietaire'},
            {'username': 'proprio2',  'noms': 'Jeanine Kalala',     'email': 'j.kalala@immo.local',  'profile_name': 'Proprietaire'},
            {'username': 'compta1',   'noms': 'Alice Tshibangu',    'email': 'a.tshibangu@immo.local', 'profile_name': 'Comptable'},
            {'username': 'super1',    'noms': 'Georges Lumbala',    'email': 'g.lumbala@immo.local', 'profile_name': 'Superviseur'},
            {'username': 'client1',   'noms': 'Kakudji Pierre',     'email': 'kakudji@mail.com',     'profile_name': 'Client'},
            {'username': 'client2',   'noms': 'Mukendi Albert',     'email': 'mukendi@mail.com',     'profile_name': 'Client'},
            {'username': 'client3',   'noms': 'Ndaye Marie',        'email': 'ndaye.marie@mail.com', 'profile_name': 'Client'},
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

        # 3. AGENCES
        agences_data = [
            {'nom': 'Agence Centre-Ville', 'adresse': '123 Av. du Centre, Kinshasa', 'telephone': '+243810000001', 'email': 'centre@immo.cd', 'active': True},
            {'nom': 'Agence Gombe', 'adresse': '456 Bd. du 30 Juin, Gombe', 'telephone': '+243810000002', 'email': 'gombe@immo.cd', 'active': True},
        ]
        agences = [Agence.objects.get_or_create(nom=a['nom'], defaults=a)[0] for a in agences_data]
        print(f"✅ {len(agences)} agences créées.")

        # 4. PERSONNEL
        personnel_data = [
            {'user': User.objects.get(username='manager1'), 'agence': agences[0], 'sexe': 'M', 'telephone': '+243820000001'},
            {'user': User.objects.get(username='agent1'), 'agence': agences[0], 'sexe': 'F', 'telephone': '+243820000002'},
            {'user': User.objects.get(username='agent2'), 'agence': agences[1], 'sexe': 'F', 'telephone': '+243820000003'},
        ]
        for pdata in personnel_data:
            Personnel.objects.get_or_create(user=pdata['user'], defaults=pdata)
        print(f"✅ {len(personnel_data)} personnels créés.")

        # 5. PROPRIETAIRES
        proprietaires_data = [
            {'user': User.objects.get(username='proprio1'), 'telephone': '+243990000001', 'adresse': '10 Av. des propriétaires'},
            {'user': User.objects.get(username='proprio2'), 'telephone': '+243990000002', 'adresse': '25 Blvd. du 30 Juin'},
        ]
        for pr in proprietaires_data:
            Proprietaire.objects.get_or_create(user=pr['user'], defaults=pr)
        print(f"✅ {len(proprietaires_data)} propriétaires créés.")

        # 6. CLIENTS
        clients_data = [
            {'user': User.objects.get(username='client1'), 'agence': agences[0], 'telephone': '+243811000001', 'adresse': '25 Av. des clients'},
            {'user': User.objects.get(username='client2'), 'agence': agences[1], 'telephone': '+243811000002', 'adresse': '30 Av. des palmiers'},
            {'user': User.objects.get(username='client3'), 'agence': agences[0], 'telephone': '+243811000003', 'adresse': '18 Rue Mont Ngaliema'},
        ]
        for cl in clients_data:
            Client.objects.get_or_create(user=cl['user'], defaults=cl)
        print(f"✅ {len(clients_data)} clients créés.")

        # 7. TYPES DE PROPRIETE
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
        print(f"✅ {len(types_propriete)} types de propriété créés.")

        # 7.1. TYPES DE LOGEMENT
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
        print(f"✅ {len(types_logement)} types de logement créés.")

        # 8. PROPRIETES
        proprio1 = Proprietaire.objects.get(user__username='proprio1')
        proprio2 = Proprietaire.objects.get(user__username='proprio2')
        agent1 = Personnel.objects.get(user__username='agent1')
        agent2 = Personnel.objects.get(user__username='agent2')

        proprietes_data = [
            {'agence': agences[0], 'proprietaire': proprio1, 'type_propriete': types_propriete[0], 'adresse': '100 Av. de la Liberté', 'ville': 'Kinshasa/Gombe', 'superficie': 1200, 'nb_pieces': 15, 'statut': 'LOUE', 'agent': agent1},
            {'agence': agences[1], 'proprietaire': proprio1, 'type_propriete': types_propriete[1], 'adresse': '200 Av. de la Paix', 'ville': 'Kinshasa/Ngaliema', 'superficie': 800, 'nb_pieces': 8, 'statut': 'DISPONIBLE'},
            {'agence': agences[0], 'proprietaire': proprio1, 'type_propriete': types_propriete[2], 'adresse': '300 Bd Lumumba', 'ville': 'Kinshasa/Lingwala', 'superficie': 600, 'nb_pieces': 6, 'statut': 'LOUE', 'agent': agent1},
            {'agence': agences[1], 'proprietaire': proprio2, 'type_propriete': types_propriete[3], 'adresse': '400 Rue Commerce', 'ville': 'Kinshasa/Kintambo', 'superficie': 400, 'nb_pieces': 4, 'statut': 'DISPONIBLE'},
            {'agence': agences[0], 'proprietaire': proprio2, 'type_propriete': types_propriete[0], 'adresse': '500 Av des Martyrs', 'ville': 'Kinshasa/Bandundu', 'superficie': 900, 'nb_pieces': 10, 'statut': 'MAINTENANCE', 'agent': agent2},
            {'agence': agences[1], 'proprietaire': proprio2, 'type_propriete': types_propriete[1], 'adresse': '600 Ave. Ngongo', 'ville': 'Kinshasa/Lemba', 'superficie': 750, 'nb_pieces': 9, 'statut': 'LOUE', 'agent': agent2},
        ]
        proprietes = [Propriete.objects.get_or_create(adresse=p['adresse'], defaults=p)[0] for p in proprietes_data]
        print(f"✅ {len(proprietes_data)} propriétés créées.")

        # 9. LOGEMENTS
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

        # Attribuer les types de logements
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

        # Mettre à jour les statuts
        Logement.objects.filter(identifiant='A-101').update(statut='LOUE')
        Logement.objects.filter(identifiant='A-102').update(statut='DISPONIBLE')
        Logement.objects.filter(identifiant='B-201').update(statut='LOUE')
        Logement.objects.filter(identifiant='B-202').update(statut='DISPONIBLE')
        Logement.objects.filter(identifiant='C-301').update(statut='DISPONIBLE')

        Logement.objects.filter(identifiant='V-001').update(statut='LOUE')
        Logement.objects.filter(identifiant='V-002').update(statut='DISPONIBLE')

        Logement.objects.filter(identifiant='APT-101').update(statut='LOUE')
        Logement.objects.filter(identifiant='APT-102').update(statut='DISPONIBLE')
        Logement.objects.filter(identifiant='APT-201').update(statut='DISPONIBLE')

        Logement.objects.filter(identifiant='ST-101').update(statut='DISPONIBLE')
        Logement.objects.filter(identifiant='ST-102').update(statut='DISPONIBLE')

        print(f"✅ {len(logements_data)} logements créés avec types et statuts.")

        # 10. CONTRATS
        client1 = Client.objects.get(user__username='client1')
        client2 = Client.objects.get(user__username='client2')
        client3 = Client.objects.get(user__username='client3')

        logement_a101 = Logement.objects.get(identifiant='A-101')   # Propriété 1 (proprio1)
        logement_apt101 = Logement.objects.get(identifiant='APT-101')  # Propriété 3 (proprio1)
        logement_b201 = Logement.objects.get(identifiant='B-201')   # Propriété 1 (proprio1)
        logement_v001 = Logement.objects.get(identifiant='V-001')   # Propriété 2 (proprio2)
        logement_st101 = Logement.objects.get(identifiant='ST-101') # Propriété 4 (proprio2)

        contrats_data = [
            {
                'reference': 'LOC-2024-001', 'type': 'LOCATION',
                'logement': logement_a101, 'propriete': None,
                'proprietaire': logement_a101.propriete.proprietaire,
                'client': client1, 'agent': agent1,
                'date_debut': date.today() - timedelta(days=100), 'montant': Decimal('450.00'),
                'conditions': 'Loyer mensuel, payable avant le 5 de chaque mois.', 'statut': 'ACTIF'
            },
            {
                'reference': 'LOC-2024-002', 'type': 'LOCATION',
                'logement': logement_apt101, 'propriete': None,
                'proprietaire': logement_apt101.propriete.proprietaire,
                'client': client2, 'agent': agent1,
                'date_debut': date.today() - timedelta(days=80), 'montant': Decimal('350.00'),
                'conditions': 'Loyer mensuel, caution incluse.', 'statut': 'ACTIF'
            },
            {
                'reference': 'LOC-2024-003', 'type': 'LOCATION',
                'logement': logement_b201, 'propriete': None,
                'proprietaire': logement_b201.propriete.proprietaire,
                'client': client3, 'agent': agent2,
                'date_debut': date.today() - timedelta(days=90), 'montant': Decimal('550.00'),
                'conditions': 'Loyer mensuel, appartement premium.', 'statut': 'ACTIF'
            },
            {
                'reference': 'LOC-2024-004', 'type': 'LOCATION',
                'logement': logement_st101, 'propriete': None,
                'proprietaire': logement_st101.propriete.proprietaire,
                'client': client1, 'agent': agent2,
                'date_debut': date.today() - timedelta(days=70), 'montant': Decimal('600.00'),
                'conditions': 'Loyer mensuel, studio meublé.', 'statut': 'ACTIF'
            }
        ]
        contrats = [Contrat.objects.get_or_create(reference=c['reference'], defaults=c)[0] for c in contrats_data]
        print(f"✅ {len(contrats)} contrats créés.")

        # 11. GARANTIES
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

        # 12. PAIEMENTS
        contrat1 = contrats[0]  # proprio1
        contrat2 = contrats[1]  # proprio1
        contrat3 = contrats[2]  # proprio1
        contrat4 = contrats[3]  # proprio2

        paiements_data = [
            # Contrat 1 (proprio1, client1) - 3 paiements
            {'contrat': contrat1, 'client': contrat1.client, 'montant': 450,
             'date_paiement': date.today() - timedelta(days=65), 'date_echeance': date.today() - timedelta(days=70),
             'type_paiement': 'LOYER', 'statut': 'PAYE'},
            {'contrat': contrat1, 'client': contrat1.client, 'montant': 450,
             'date_paiement': date.today() - timedelta(days=35), 'date_echeance': date.today() - timedelta(days=40),
             'type_paiement': 'LOYER', 'statut': 'PAYE'},
            {'contrat': contrat1, 'client': contrat1.client, 'montant': 450,
             'date_paiement': None, 'date_echeance': date.today() - timedelta(days=10),
             'type_paiement': 'LOYER', 'statut': 'EN_RETARD'},
            # Contrat 2 (proprio1, client2) - 2 paiements
            {'contrat': contrat2, 'client': contrat2.client, 'montant': 350,
             'date_paiement': date.today() - timedelta(days=50), 'date_echeance': date.today() - timedelta(days=55),
             'type_paiement': 'LOYER', 'statut': 'PAYE'},
            {'contrat': contrat2, 'client': contrat2.client, 'montant': 350,
             'date_paiement': None, 'date_echeance': date.today() - timedelta(days=5),
             'type_paiement': 'LOYER', 'statut': 'EN_RETARD'},
            # Contrat 3 (proprio1, client3) - 2 paiements
            {'contrat': contrat3, 'client': contrat3.client, 'montant': 550,
             'date_paiement': date.today() - timedelta(days=40), 'date_echeance': date.today() - timedelta(days=45),
             'type_paiement': 'LOYER', 'statut': 'PAYE'},
            {'contrat': contrat3, 'client': contrat3.client, 'montant': 550,
             'date_paiement': None, 'date_echeance': date.today() - timedelta(days=15),
             'type_paiement': 'LOYER', 'statut': 'EN_RETARD'},
            # Contrat 4 (proprio2, client1) - 2 paiements
            {'contrat': contrat4, 'client': contrat4.client, 'montant': 600,
             'date_paiement': date.today() - timedelta(days=60), 'date_echeance': date.today() - timedelta(days=65),
             'type_paiement': 'LOYER', 'statut': 'PAYE'},
            {'contrat': contrat4, 'client': contrat4.client, 'montant': 600,
             'date_paiement': None, 'date_echeance': date.today() - timedelta(days=20),
             'type_paiement': 'LOYER', 'statut': 'EN_ATTENTE'},
        ]
        for p in paiements_data:
            Paiement.objects.create(**p)
        print(f"✅ {len(paiements_data)} paiements créés.")

        # 13. CAISSE
        all_paiements = list(Paiement.objects.filter(date_paiement__isnull=False).order_by('date_paiement'))

        caisse_data = []
        # Entrées de caisse liées à des paiements (loyers perçus)
        for i, paiement in enumerate(all_paiements[:4]):  # 4 premières entrées liées à des paiements
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

        # 14. LOGS
        LogUser.objects.create(
            user=User.objects.get(username='admin'),
            action='CREATE'
        )
        print("✅ Journal système créé.")

        # Résumé
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

def download_image(url):
    """Télécharge une image depuis une URL."""
    try:
        ctx = ssl.create_default_context(cafile=certifi.where())
        with urllib.request.urlopen(url, context=ctx, timeout=30) as r:
            data = r.read()
            return data
    except Exception as e:
        print(f"Erreur téléchargement {url}: {e}")
        return None

def save_image_to_field(instance, field_name, data, filename):
    """Enregistre bytes dans le champ ImageField d'une instance et sauvegarde."""
    if not data:
        return None
    content = ContentFile(data)
    getattr(instance, field_name).save(filename, content, save=True)
    return getattr(instance, field_name).name

def get_unsplash_images_from_search(query, max_results=50):
    """Récupère les URLs d'images depuis la page de résultats Unsplash."""
    if not query:
        query = 'logement'
    page_url = f"https://unsplash.com/fr/s/photos/{urllib.parse.quote(query)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36'
    }
    try:
        req = urllib.request.Request(page_url, headers=headers)
        ctx = ssl.create_default_context(cafile=certifi.where())
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            html = r.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Impossible de récupérer la page Unsplash {page_url}: {e}")
        return []

    # Extraire les URLs d'images
    matches = re.findall(r'https://images\.unsplash\.com/[^\s"\'<>]+', html)
    cleaned = []
    for m in matches:
        m = m.split('"')[0].split("'", 1)[0]
        if '?ixlib' in m:
            pass
        if m not in cleaned:
            cleaned.append(m)
        if len(cleaned) >= max_results:
            break
    print(f"Trouvé {len(cleaned)} images Unsplash pour '{query}'")
    return cleaned

def wipe_media():
    """Supprime les médias existants pour les propriétés et logements."""
    print("🧹 Suppression des médias existants...")
    # Supprimer les images principales
    Propriete.objects.update(main_image='')
    Logement.objects.update(main_image='')

    # Supprimer les images associées
    ProprieteImage.objects.all().delete()
    LogementImage.objects.all().delete()
    print("✅ Médias existants supprimés.")

def get_local_images():
    """Récupère les images locales depuis les dossiers photos/, media/logements/ et media/proprietes/."""
    project_root = Path(__file__).resolve().parent.parent
    search_dirs = [
        project_root / 'photos',
        project_root / 'media' / 'logements',
        project_root / 'media' / 'proprietes',
    ]
    extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    images = []
    for d in search_dirs:
        if d.exists():
            for f in d.iterdir():
                if f.is_file() and f.suffix.lower() in extensions:
                    images.append(str(f))
    print(f"📁 {len(images)} images locales trouvées dans {[str(d) for d in search_dirs if d.exists()]}")
    return images


def populate_images(limit=None, query=None, local_only=False):
    """Télécharge et attache des images depuis Unsplash ou utilise les images locales."""
    props = list(Propriete.objects.all())
    logs = list(Logement.objects.all())

    if limit:
        props = props[:limit]
        logs = logs[:limit]

    now = timezone.now()
    local_images = get_local_images()
    print(f"Traitement de {len(props)} propriétés et {len(logs)} logements (limit={limit}, query={query}, local_only={local_only})")

    # Essayer Unsplash si pas en mode local_only
    candidates = []
    if not local_only:
        candidates = get_unsplash_images_from_search(query or 'logement', max_results=200)

    if not candidates:
        print("ℹ️  Utilisation des images locales en fallback.")

    # --- Propriétés ---
    for idx, p in enumerate(props, start=1):
        if p.main_image:
            print(f"[SKIP] Propriété {p.id} ({p.adresse}) a déjà une image principale")
            continue

        data = None
        src = None

        # Essayer Unsplash
        if candidates:
            src = candidates[(p.id - 1) % len(candidates)]
            print(f"[UNSPLASH] Propriété {p.id} ({p.adresse}) <- {src[:50]}...")
            data = download_image(src)

        # Fallback vers image locale
        if not data and local_images:
            local_path = local_images[(p.id - 1) % len(local_images)]
            src = os.path.basename(local_path)
            print(f"[LOCAL] Propriété {p.id} ({p.adresse}) <- {src}")
            try:
                with open(local_path, 'rb') as f:
                    data = f.read()
            except Exception as e:
                print(f"[ERREUR] Lecture image locale {local_path}: {e}")
                continue

        if not data:
            print(f"[ERREUR] Aucune image disponible pour propriété {p.id}")
            continue

        month_path = now.strftime('%Y/%m')
        ext = os.path.splitext(src or 'propriete.jpg')[1] or '.jpg'
        filename = f"proprietes/{month_path}/propriete_{p.id}{ext}"
        try:
            saved_name = save_image_to_field(p, 'main_image', data, filename)
            if saved_name:
                caption = f"Photo de la propriété (source: {'Unsplash' if 'unsplash' in (src or '') else 'locale'})"
                ProprieteImage.objects.create(propriete=p, image=saved_name, caption=caption, is_primary=True)
                print(f"[OK] Propriété {p.id} ({p.adresse}) image enregistrée -> {saved_name}")
        except Exception as e:
            print(f"[ERREUR] Sauvegarde image pour propriété {p.id}: {e}")

    # --- Logements ---
    for idx, l in enumerate(logs, start=1):
        if l.main_image:
            print(f"[SKIP] Logement {l.id} ({l.identifiant}) a déjà une image principale")
            continue

        data = None
        src = None

        # Essayer Unsplash
        if candidates:
            src = candidates[(l.id - 1) % len(candidates)]
            print(f"[UNSPLASH] Logement {l.id} ({l.identifiant}) <- {src[:50]}...")
            data = download_image(src)

        # Fallback vers image locale
        if not data and local_images:
            local_path = local_images[(l.id - 1) % len(local_images)]
            src = os.path.basename(local_path)
            print(f"[LOCAL] Logement {l.id} ({l.identifiant}) <- {src}")
            try:
                with open(local_path, 'rb') as f:
                    data = f.read()
            except Exception as e:
                print(f"[ERREUR] Lecture image locale {local_path}: {e}")
                continue

        if not data:
            print(f"[ERREUR] Aucune image disponible pour logement {l.id}")
            continue

        month_path = now.strftime('%Y/%m')
        ext = os.path.splitext(src or 'logement.jpg')[1] or '.jpg'
        filename = f"logements/{month_path}/logement_{l.id}{ext}"
        try:
            saved_name = save_image_to_field(l, 'main_image', data, filename)
            if saved_name:
                caption = f"Photo du logement (source: {'Unsplash' if 'unsplash' in (src or '') else 'locale'})"
                LogementImage.objects.create(logement=l, image=saved_name, caption=caption, is_primary=True)
                print(f"[OK] Logement {l.id} ({l.identifiant}) image enregistrée -> {saved_name}")
        except Exception as e:
            print(f"[ERREUR] Sauvegarde image pour logement {l.id}: {e}")

def main():
    """Fonction principale."""
    parser = argparse.ArgumentParser(description='Script de réinitialisation et peuplement de données de démonstration')
    parser.add_argument('--limit', type=int, default=None, help='Limite le nombre de propriétés/logements à traiter pour les images')
    parser.add_argument('--query', type=str, default=None, help='Mot-clé de recherche pour Unsplash (ex: apartment, kitchen, house)')
    parser.add_argument('--wipe-media', action='store_true', help='Supprime les médias existants avant de télécharger de nouvelles images')
    parser.add_argument('--skip-data', action='store_true', help='Ne pas recréer les données, seulement gérer les images')
    parser.add_argument('--local-only', action='store_true', help='Utiliser uniquement les images locales (pas de téléchargement Unsplash)')
    args = parser.parse_args()

    print("🔄 Script de réinitialisation des données de démonstration")
    print(f"Options: limit={args.limit}, query={args.query}, wipe_media={args.wipe_media}, skip_data={args.skip_data}, local_only={args.local_only}")

    if not args.skip_data:
        # Nettoyer et recréer les données
        clean_data()
        create_demo_data()
    else:
        print("📋 Conservation des données existantes (option --skip-data activée)")

    if args.wipe_media:
        wipe_media()

    # Peupler les images
    populate_images(limit=args.limit, query=args.query, local_only=args.local_only)

    print("\n✅ Script terminé avec succès !")

if __name__ == '__main__':
    main()