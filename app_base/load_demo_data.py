from django.core.management.base import BaseCommand
from django.utils import timezone
from app_base.models import Agence, Locataire
from app_users.models import User, Profile

class Command(BaseCommand):
    help = 'Charge les données de démonstration pour le projet Immo'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Début du chargement des données de démonstration...'))

        # --- Création des profils et utilisateurs ---
        self.stdout.write('Création des profils et utilisateurs...')
        
        # Crée les profils s'ils n'existent pas
        manager_profile, _ = Profile.objects.get_or_create(name='Manager')
        agent_profile, _ = Profile.objects.get_or_create(name='Agent')

        # Crée un super-utilisateur
        if not User.objects.filter(username='superadmin').exists():
            User.objects.create_superuser('superadmin', 'admin@example.com', 'admin123')

        # Crée un utilisateur Manager
        if not User.objects.filter(username='manager1').exists():
            User.objects.create_user(
                username='manager1', email='manager@example.com', password='demo123',
                noms='Chef Agence', profile=manager_profile, is_staff=True
            )

        # --- Création des données pour app_base ---
        self.stdout.write('Création des agences et locataires...')

        # Crée une agence
        agence, created = Agence.objects.get_or_create(
            nom='Agence Principale',
            defaults={
                'numero_impot': 'IMPOT-001',
                'numero_fisc': 'FISC-001',
                'email': 'contact@agence-principale.com',
                'effectif': 10,
                'revenu': 50000
            }
        )

        # Crée un locataire
        Locataire.objects.get_or_create(
            noms='Jean Dupont',
            defaults={
                'telephone': '0123456789',
                'email': 'jean.dupont@locataire.com',
                'contrat': 'Contrat-A1',
                'loye': 750,
                'regularite': 'Bon payeur'
            }
        )

        self.stdout.write(self.style.SUCCESS('✅ Données de démonstration chargées avec succès !'))