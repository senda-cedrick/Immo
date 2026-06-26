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
    TypePropriete, Propriete, Logement, Contrat, Garantie
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
                u.set_password('demo123')
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
        types_propriete_data = ['Immeuble', 'Villa', 'Appartement', 'Studio']
        types_propriete = [TypePropriete.objects.get_or_create(nom=nom)[0] for nom in types_propriete_data]
        print(f"✅ {len(types_propriete)} types de propriété créés.")

        # ──────────────────────────────────────────────
        # 8. PROPRIETES (app_base)
        # ──────────────────────────────────────────────
        proprio_obj = Proprietaire.objects.first()
        agent_obj = Personnel.objects.filter(user__profile__name='Agent').first()
        proprietes_data = [
            {'agence': agences[0], 'proprietaire': proprio_obj, 'type_propriete': types_propriete[0], 'adresse': '100 Av. de la Liberté', 'ville': 'Kinshasa/Gombe', 'superficie': 1200, 'statut': 'LOUE', 'agent': agent_obj},
            {'agence': agences[1], 'proprietaire': proprio_obj, 'type_propriete': types_propriete[1], 'adresse': '200 Av. de la Paix', 'ville': 'Kinshasa/Ngaliema', 'superficie': 800, 'statut': 'DISPONIBLE'},
        ]
        proprietes = [Propriete.objects.get_or_create(adresse=p['adresse'], defaults=p)[0] for p in proprietes_data]
        print(f"✅ {len(proprietes_data)} propriétés créées.")

        # ──────────────────────────────────────────────
        # 9. LOGEMENTS (app_base)
        # ──────────────────────────────────────────────
        logements_data = [
            {'propriete': proprietes[0], 'identifiant': 'A-101', 'surface': 80, 'etage': 1},
            {'propriete': proprietes[0], 'identifiant': 'A-102', 'surface': 85, 'etage': 1},
            {'propriete': proprietes[0], 'identifiant': 'B-201', 'surface': 120, 'etage': 2},
        ]
        for lg in logements_data:
            Logement.objects.get_or_create(propriete=lg['propriete'], identifiant=lg['identifiant'], defaults=lg)
        print(f"✅ {len(logements_data)} logements créés.")

        # ──────────────────────────────────────────────
        # 10. CONTRATS (app_base)
        # ──────────────────────────────────────────────
        client1 = Client.objects.get(user__username='client1')
        contrats_data = [
            {
                'reference': 'LOC-2024-001', 'type': 'LOCATION', 'propriete': proprietes[0],
                'client': client1, 'proprietaire': proprio_obj, 'agent': agent_obj,
                'date_debut': date.today() - timedelta(days=100), 'montant': Decimal('450.00'),
                'conditions': 'Loyer mensuel, payable avant le 5 de chaque mois.', 'statut': 'ACTIF'
            }
        ]
        contrats = [Contrat.objects.get_or_create(reference=c['reference'], defaults=c)[0] for c in contrats_data]
        print(f"✅ {len(contrats)} contrats créés.")

        # ──────────────────────────────────────────────
        # 11. PAIEMENTS (app_paiements)
        # ──────────────────────────────────────────────
        contrat_actif = contrats[0]
        client_actif = contrat_actif.client
        paiements_data = [
            {'client': client_actif, 'montant': 450, 'date_paie': date.today() - timedelta(days=65), 'date_normal': date.today() - timedelta(days=70), 'type_paie': 'CASH'},
            {'client': client_actif, 'montant': 450, 'date_paie': date.today() - timedelta(days=35), 'date_normal': date.today() - timedelta(days=40), 'type_paie': 'VIREMENT'},
            {'client': client_actif, 'montant': 450, 'date_paie': date.today() - timedelta(days=5), 'date_normal': date.today() - timedelta(days=10), 'type_paie': 'MOBILE_MONEY'},
        ]
        for p in paiements_data:
            # The 'defaults' will contain all keys from p, including 'client'
            Paiement.objects.get_or_create(
                client=p['client'],
                date_paie=p['date_paie'],
                montant=p['montant'],
                defaults=p
            )
        print(f"✅ {len(paiements_data)} paiements créés.")

        # ──────────────────────────────────────────────
        # 12. CAISSE (app_caisse)
        # ──────────────────────────────────────────────
        first_payment = Paiement.objects.order_by('date_paie').first()
        first_montant = first_payment.montant if first_payment else Decimal('0.00')
        caisse_data = [
            {
                'type_caisse': 'ENTREE',
                'status_caisse': 'VALIDATED',
                'cout': first_montant,
                'paiement': first_payment,
                'details': 'Loyer de Kakudji Pierre'
            },
            {
                'type_caisse': 'SORTIE',
                'status_caisse': 'VALIDATED',
                'cout': Decimal('50.00'),
                'paiement': None,
                'details': 'Frais de nettoyage'
            },
        ]
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
        print(f"   - {Paiement.objects.count()} paiements")
        print(f"   - {Caisse.objects.count()} entrées de caisse")


if __name__ == '__main__':
    clean_data()
    create_demo_data()