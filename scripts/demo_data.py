"""
Script de génération de données de démonstration pour le projet Immo.
Usage:
    python scripts/demo_data.py

Ce script crée des données factices pour toutes les applications :
    - app_base : Agence, Personnel, Proprietaire, Appartement, Propriete, Locataire, Logement, Garantie
    - app_users : Profile, User, LogUser
    - app_paiements : Paiement, Impayes
    - app_caisse : Caisse
"""

import os
import sys
import django

# Configuration de Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'immo_travel.settings')
django.setup()

from django.db import transaction
from django.utils import timezone
from datetime import date, timedelta
from random import randint, choice, uniform
from decimal import Decimal

from app_base.models import (
    Agence, Personnel, Proprietaire, Appartement,
    Propriete, TypePropriete, Locataire, Logement, Garantie
)
from app_users.models import Profile, User, LogUser
from app_paiements.models import Paiement, Impayes
from app_caisse.models import Caisse


def clean_data():
    """Supprime toutes les données existantes dans l'ordre inverse des dépendances."""
    print("🗑️  Nettoyage des données existantes...")
    Caisse.objects.all().delete()
    Impayes.objects.all().delete()
    Paiement.objects.all().delete()
    Garantie.objects.all().delete()
    Logement.objects.all().delete()
    Propriete.objects.all().delete()
    Appartement.objects.all().delete()
    Locataire.objects.all().delete()
    Personnel.objects.all().delete()
    Agence.objects.all().delete()
    Proprietaire.objects.all().delete()
    LogUser.objects.all().delete()
    User.objects.all().delete()
    Profile.objects.all().delete()
    print("✅ Nettoyage terminé.\n")


@transaction.atomic
def create_demo_data():
    """Crée les données de démonstration."""
    print("🚀 Création des données de démonstration...\n")

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
        {'username': 'admin',     'noms': 'Admin Système',      'email': 'admin@immo.local',   'profile': profiles[0], 'is_staff': True},
        {'username': 'manager1',  'noms': 'Jean Dupont',        'email': 'j.dupont@immo.local', 'profile': profiles[1], 'is_staff': True},
        {'username': 'agent1',    'noms': 'Marie Kabange',      'email': 'm.kabange@immo.local', 'profile': profiles[2]},
        {'username': 'proprio1',  'noms': 'Paul Mukendi',       'email': 'p.mukendi@immo.local', 'profile': profiles[3]},
        {'username': 'compta1',   'noms': 'Alice Tshibangu',    'email': 'a.tshibangu@immo.local', 'profile': profiles[4]},
        {'username': 'super1',    'noms': 'Georges Lumbala',    'email': 'g.lumbala@immo.local', 'profile': profiles[5]},
    ]
    users = []
    for udata in users_data:
        defaults = {
            'noms': udata['noms'],
            'email': udata['email'],
            'profile': udata['profile'],
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
        {'nom': 'Agence Centre-Ville',  'numero_impot': 'A123456', 'numero_fisc': 'F123456', 'effectif': 15, 'revenu': 45000000, 'email': 'centre@immo.cd', 'active': True},
        {'nom': 'Agence Gombe',         'numero_impot': 'A789012', 'numero_fisc': 'F789012', 'effectif': 10, 'revenu': 32000000, 'email': 'gombe@immo.cd', 'active': True},
        {'nom': 'Agence Limete',        'numero_impot': 'A345678', 'numero_fisc': 'F345678', 'effectif': 8,  'revenu': 18000000, 'email': 'limete@immo.cd', 'active': True},
    ]
    agences = [Agence.objects.create(**a) for a in agences_data]
    print(f"✅ {len(agences)} agences créées.")

    # ──────────────────────────────────────────────
    # 4. PERSONNEL (app_base)
    # ──────────────────────────────────────────────
    personnel_data = [
        {'noms': 'Kabasele Tshimanga', 'sexe': 'M', 'role': 'Directeur',       'status': 'Actif',  'agence': agences[0], 'email': 'kabasele@immo.cd'},
        {'noms': 'Mbuyi Kalenga',      'sexe': 'M', 'role': 'Agent Commercial', 'status': 'Actif',  'agence': agences[0], 'email': 'mbuyi@immo.cd'},
        {'noms': 'Ngalula Mwamba',     'sexe': 'F', 'role': 'Secrétaire',       'status': 'Actif',  'agence': agences[1], 'email': 'ngalula@immo.cd'},
        {'noms': 'Ilunga Kayembe',     'sexe': 'M', 'role': 'Agent Immobilier', 'status': 'Actif',  'agence': agences[1], 'email': 'ilunga@immo.cd'},
        {'noms': 'Tshibola Ntumba',    'sexe': 'F', 'role': 'Comptable',        'status': 'Actif',  'agence': agences[2], 'email': 'tshibola@immo.cd'},
        {'noms': 'Mwepu Kazadi',       'sexe': 'M', 'role': 'Agent de Terrain', 'status': 'Actif',  'agence': agences[2], 'email': 'mwepu@immo.cd'},
    ]
    for pdata in personnel_data:
        Personnel.objects.create(**pdata)
    print(f"✅ {len(personnel_data)} personnels créés.")

    # ──────────────────────────────────────────────
    # 5. PROPRIETAIRES (app_base)
    # ──────────────────────────────────────────────
    proprietaires_data = [
        {'noms': 'M. Tshisekedi Félix',       'bienconfie': 3,  'bienlocatif': 5,  'catalogue': 'Résidentiel', 'email': 'tshisekedi@mail.com'},
        {'noms': 'Mme Bemba Gertrude',        'bienconfie': 2,  'bienlocatif': 3,  'catalogue': 'Commercial',  'email': 'bemba@mail.com'},
        {'noms': 'M. Katumbi Moïse',          'bienconfie': 4,  'bienlocatif': 7,  'catalogue': 'Mixte',       'email': 'katumbi@mail.com'},
        {'noms': 'Mme Masangu Sylvie',        'bienconfie': 1,  'bienlocatif': 2,  'catalogue': 'Résidentiel', 'email': 'masangu@mail.com'},
        {'noms': 'M. Mbiye Charles',          'bienconfie': 2,  'bienlocatif': 4,  'catalogue': 'Commercial',  'email': 'mbiye@mail.com'},
    ]
    for pr in proprietaires_data:
        Proprietaire.objects.create(**pr)
    print(f"✅ {len(proprietaires_data)} propriétaires créés.")

    # ──────────────────────────────────────────────
    # 6. APPARTEMENTS (app_base)
    # ──────────────────────────────────────────────
    appartements_data = [
        {'identifiant': 'APT-001', 'prix': '450',   'status': 'Libre'},
        {'identifiant': 'APT-002', 'prix': '350',   'status': 'Occupé'},
        {'identifiant': 'APT-003', 'prix': '500',   'status': 'Libre'},
        {'identifiant': 'APT-004', 'prix': '300',   'status': 'Occupé'},
        {'identifiant': 'APT-005', 'prix': '600',   'status': 'En rénovation'},
        {'identifiant': 'APT-006', 'prix': '420',   'status': 'Libre'},
        {'identifiant': 'APT-007', 'prix': '380',   'status': 'Occupé'},
        {'identifiant': 'APT-008', 'prix': '550',   'status': 'Réservé'},
    ]
    for a in appartements_data:
        Appartement.objects.create(**a)
    print(f"✅ {len(appartements_data)} appartements créés.")

    # ──────────────────────────────────────────────
    # 7. PROPRIETES (app_base)
    # ──────────────────────────────────────────────
    proprietes_data = [
        {'type_propriete': TypePropriete.objects.get_or_create(nom='Immeuble')[0], 'ville': 'Kinshasa/Gombe',      'agent': 'Mbuyi Kalenga',    'gestion': True,  'appartement': Appartement.objects.get(identifiant='APT-001')},
        {'type_propriete': TypePropriete.objects.get_or_create(nom='Villa')[0],    'ville': 'Kinshasa/Ngaliema',    'agent': 'Ilunga Kayembe',   'gestion': True,  'appartement': Appartement.objects.get(identifiant='APT-002')},
        {'type_propriete': TypePropriete.objects.get_or_create(nom='Immeuble')[0], 'ville': 'Kinshasa/Limete',      'agent': 'Mwepu Kazadi',     'gestion': True,  'appartement': Appartement.objects.get(identifiant='APT-003')},
        {'type_propriete': TypePropriete.objects.get_or_create(nom='Studio')[0],   'ville': 'Kinshasa/Kalamu',      'agent': 'Mbuyi Kalenga',    'gestion': False, 'appartement': Appartement.objects.get(identifiant='APT-004')},
        {'type_propriete': TypePropriete.objects.get_or_create(nom='Duplex')[0],   'ville': 'Kinshasa/Gombe',       'agent': 'Ilunga Kayembe',   'gestion': True,  'appartement': Appartement.objects.get(identifiant='APT-005')},
    ]
    for p in proprietes_data:
        Propriete.objects.create(**p)
    print(f"✅ {len(proprietes_data)} propriétés créées.")

    # ──────────────────────────────────────────────
    # 8. LOCATAIRES (app_base)
    # ──────────────────────────────────────────────
    locataires_data = [
        {'noms': 'Kakudji Pierre',          'telephone': '+243811000001', 'contrat': 'BAIL-001', 'loye': 450, 'regularite': 'Régulier', 'email': 'kakudji@mail.com'},
        {'noms': 'Mukendi Albert',          'telephone': '+243811000002', 'contrat': 'BAIL-002', 'loye': 350, 'regularite': 'Régulier', 'email': 'mukendi@mail.com'},
        {'noms': 'Tshitenge Joséphine',     'telephone': '+243811000003', 'contrat': 'BAIL-003', 'loye': 500, 'regularite': 'Irégulier', 'email': 'tshitenge@mail.com'},
        {'noms': 'Kabongo Raphaël',         'telephone': '+243811000004', 'contrat': 'BAIL-004', 'loye': 300, 'regularite': 'Régulier', 'email': 'kabongo@mail.com'},
        {'noms': 'Mwabila Esther',          'telephone': '+243811000005', 'contrat': 'BAIL-005', 'loye': 420, 'regularite': 'Nouveau', 'email': 'mwabila@mail.com'},
        {'noms': 'Kazadi Michel',           'telephone': '+243811000006', 'contrat': 'BAIL-006', 'loye': 380, 'regularite': 'Régulier', 'email': 'kazadi@mail.com'},
    ]
    for l in locataires_data:
        Locataire.objects.create(**l)
    print(f"✅ {len(locataires_data)} locataires créés.")

    # ──────────────────────────────────────────────
    # 9. LOGEMENTS (app_base)
    # ──────────────────────────────────────────────
    logements_data = [
        {'identifiant': Appartement.objects.get(identifiant='APT-001'), 'status': 'Occupé',        'proprietaire': Proprietaire.objects.get(noms='M. Tshisekedi Félix'),       'agent': Propriete.objects.get(type_propriete__nom='Immeuble', ville='Kinshasa/Gombe')},
        {'identifiant': Appartement.objects.get(identifiant='APT-002'), 'status': 'Occupé',        'proprietaire': Proprietaire.objects.get(noms='Mme Bemba Gertrude'),        'agent': Propriete.objects.get(type_propriete__nom='Villa', ville='Kinshasa/Ngaliema')},
        {'identifiant': Appartement.objects.get(identifiant='APT-003'), 'status': 'Libre',         'proprietaire': Proprietaire.objects.get(noms='M. Tshisekedi Félix'),       'agent': Propriete.objects.get(type_propriete__nom='Immeuble', ville='Kinshasa/Limete')},
        {'identifiant': Appartement.objects.get(identifiant='APT-004'), 'status': 'Occupé',        'proprietaire': Proprietaire.objects.get(noms='M. Katumbi Moïse'),          'agent': Propriete.objects.get(type_propriete__nom='Studio', ville='Kinshasa/Kalamu')},
        {'identifiant': Appartement.objects.get(identifiant='APT-005'), 'status': 'En rénovation', 'proprietaire': Proprietaire.objects.get(noms='Mme Masangu Sylvie'),        'agent': Propriete.objects.get(type_propriete__nom='Duplex', ville='Kinshasa/Gombe')},
    ]
    for lg in logements_data:
        Logement.objects.create(**lg)
    print(f"✅ {len(logements_data)} logements créés.")

    # ──────────────────────────────────────────────
    # 10. GARANTIES (app_base)
    # ──────────────────────────────────────────────
    garanties_data = [
        {'locataire': Locataire.objects.get(noms='Kakudji Pierre'), 'montant': 450,  'planification': 'Mensuelle',  'date_apparition': date.today() - timedelta(days=30)},
        {'locataire': Locataire.objects.get(noms='Mukendi Albert'), 'montant': 350,  'planification': 'Trimestrielle', 'date_apparition': date.today() - timedelta(days=15)},
        {'locataire': Locataire.objects.get(noms='Kabongo Raphaël'), 'montant': 300,  'planification': 'Mensuelle',  'date_apparition': date.today() - timedelta(days=45)},
        {'locataire': Locataire.objects.get(noms='Kazadi Michel'), 'montant': 380,  'planification': 'Semestrielle', 'date_apparition': date.today() - timedelta(days=90)},
    ]
    for g in garanties_data:
        Garantie.objects.create(**g)
    print(f"✅ {len(garanties_data)} garanties créées.")

    # ──────────────────────────────────────────────
    # 11. PAIEMENTS (app_paiements)
    # ──────────────────────────────────────────────
    paiements_data = [
        {'locataires': Locataire.objects.get(noms='Kakudji Pierre'), 'montant': 450, 'date_paie': date.today() - timedelta(days=5),  'date_normal': date.today() - timedelta(days=10), 'type_paie': 'Espèces'},
        {'locataires': Locataire.objects.get(noms='Mukendi Albert'), 'montant': 350, 'date_paie': date.today() - timedelta(days=2),  'date_normal': date.today() - timedelta(days=5),  'type_paie': 'Virement'},
        {'locataires': Locataire.objects.get(noms='Kakudji Pierre'), 'montant': 450, 'date_paie': date.today() - timedelta(days=35), 'date_normal': date.today() - timedelta(days=40), 'type_paie': 'Mobile Money'},
        {'locataires': Locataire.objects.get(noms='Kabongo Raphaël'), 'montant': 300, 'date_paie': date.today() - timedelta(days=1),  'date_normal': date.today() - timedelta(days=5),  'type_paie': 'Espèces'},
        {'locataires': Locataire.objects.get(noms='Kazadi Michel'), 'montant': 380, 'date_paie': date.today() - timedelta(days=3),  'date_normal': date.today() - timedelta(days=7),  'type_paie': 'Virement'},
    ]
    for p in paiements_data:
        Paiement.objects.create(**p)
    print(f"✅ {len(paiements_data)} paiements créés.")

    # ──────────────────────────────────────────────
    # 12. IMPAYES (app_paiements)
    # ──────────────────────────────────────────────
    impayes_data = [
        {'locataires': Locataire.objects.get(noms='Tshitenge Joséphine'), 'impaye': 500,  'situation': 'En retard', 'date_sortie': date.today() + timedelta(days=15), 'detail': 'Loyer mois en cours'},
        {'locataires': Locataire.objects.get(noms='Kakudji Pierre'), 'impaye': 150,  'situation': 'Partiel',   'date_sortie': date.today() + timedelta(days=30), 'detail': 'Reste sur charge'},
        {'locataires': Locataire.objects.get(noms='Mwabila Esther'), 'impaye': 420,  'situation': 'En retard', 'date_sortie': date.today() + timedelta(days=7),  'detail': 'Premier mois non payé'},
    ]
    for i in impayes_data:
        Impayes.objects.create(**i)
    print(f"✅ {len(impayes_data)} impayés créés.")

    # ──────────────────────────────────────────────
    # 13. CAISSE (app_caisse)
    # ──────────────────────────────────────────────
    caisse_data = [
        {'id_caisse': 1, 'type_caisse': 'Entrée', 'status_caisse': 'Validé',   'cout': 450, 'paiement': Paiement.objects.get(locataires__noms='Kakudji Pierre', montant=450, type_paie='Espèces'), 'details': 'Loyer APT-001 payé par Pierre Kakudji'},
        {'id_caisse': 2, 'type_caisse': 'Entrée', 'status_caisse': 'Validé',   'cout': 350, 'paiement': Paiement.objects.get(locataires__noms='Mukendi Albert'), 'details': 'Loyer APT-002 payé par Albert Mukendi'},
        {'id_caisse': 3, 'type_caisse': 'Entrée', 'status_caisse': 'En attente', 'cout': 450, 'paiement': Paiement.objects.get(locataires__noms='Kakudji Pierre', montant=450, type_paie='Mobile Money'), 'details': 'Loyer mois précédent APT-001'},
        {'id_caisse': 4, 'type_caisse': 'Entrée', 'status_caisse': 'Validé',   'cout': 300, 'paiement': Paiement.objects.get(locataires__noms='Kabongo Raphaël'), 'details': 'Loyer APT-004 payé par Raphaël Kabongo'},
        {'id_caisse': 5, 'type_caisse': 'Sortie', 'status_caisse': 'Validé',   'cout': 80,  'paiement': Paiement.objects.get(locataires__noms='Kakudji Pierre', montant=450, type_paie='Espèces'), 'details': 'Commission agence sur loyer Kakudji'},
    ]
    for c in caisse_data:
        Caisse.objects.create(**c)
    print(f"✅ {len(caisse_data)} entrées de caisse créées.")

    # ──────────────────────────────────────────────
    # 14. LOGS (app_users)
    # ──────────────────────────────────────────────
    LogUser.objects.create(
        user=User.objects.get(username='admin'),
        action='Génération automatique des données de démonstration'
    )
    print("✅ Journal système créé.")

    # ──────────────────────────────────────────────
    print("\n🎉 Données de démonstration créées avec succès !")
    print(f"   - {Profile.objects.count()} profils")
    print(f"   - {User.objects.count()} utilisateurs")
    print(f"   - {Agence.objects.count()} agences")
    print(f"   - {Personnel.objects.count()} personnels")
    print(f"   - {Proprietaire.objects.count()} propriétaires")
    print(f"   - {Appartement.objects.count()} appartements")
    print(f"   - {Propriete.objects.count()} propriétés")
    print(f"   - {Locataire.objects.count()} locataires")
    print(f"   - {Logement.objects.count()} logements")
    print(f"   - {Garantie.objects.count()} garanties")
    print(f"   - {Paiement.objects.count()} paiements")
    print(f"   - {Impayes.objects.count()} impayés")
    print(f"   - {Caisse.objects.count()} entrées de caisse")


if __name__ == '__main__':
    clean_data()
    create_demo_data()