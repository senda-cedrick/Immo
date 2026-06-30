from django.db import models
from django.utils import timezone


class Agence(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    numero_impot = models.CharField(max_length=50, blank=True)
    numero_fisc = models.CharField(max_length=50, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom

class Personnel(models.Model):
    SEXE_CHOIX = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('ND', 'Non défini'),
    )
    user = models.OneToOneField('app_users.User', on_delete=models.CASCADE, related_name='personnel')
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, related_name='personnel')
    sexe = models.CharField(max_length=2, choices=SEXE_CHOIX)
    telephone = models.CharField(max_length=20)
    
    # Optionnel : si on veut lier un agent à des propriétés
    # charge_immo = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.noms

class Proprietaire(models.Model):
    user = models.OneToOneField('app_users.User', on_delete=models.CASCADE, related_name='proprietaire_profile')
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, related_name='proprietaires')
    telephone = models.CharField(max_length=20)
    adresse = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.noms

class Client(models.Model):
    """Remplace Locataire pour plus de généricité"""
    user = models.OneToOneField('app_users.User', on_delete=models.CASCADE, related_name='client_profile')
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, related_name='clients')
    telephone = models.CharField(max_length=20)
    adresse = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.noms

class TypePropriete(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom

class TypeLogement(models.Model):
    """Type spécifique de logement (pour plus de granularité)"""
    nom = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom

class Propriete(models.Model):
    STATUT_CHOIX = (
        ('DISPONIBLE', 'Disponible'),
        ('LOUE', 'Loué'),
        ('VENDU', 'Vendu'),
        ('EN_MAINTENANCE', 'En maintenance'),
    )
    
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, related_name='proprietes')
    proprietaire = models.ForeignKey(Proprietaire, on_delete=models.CASCADE, related_name='proprietes')
    type_propriete = models.ForeignKey(TypePropriete, on_delete=models.PROTECT)
    
    # Caractéristiques
    adresse = models.TextField()
    ville = models.CharField(max_length=50)
    superficie = models.DecimalField(max_digits=10, decimal_places=2)
    nb_pieces = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    
    # Gestion
    statut = models.CharField(max_length=20, choices=STATUT_CHOIX, default='DISPONIBLE')
    agent = models.ForeignKey('Personnel', on_delete=models.SET_NULL, null=True, blank=True, related_name='proprietes_gerees')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type_propriete.nom} - {self.ville}"

class Logement(models.Model):
    """Sous-élément d'une propriété (appartement spécifique dans un immeuble)"""
    STATUT_CHOIX = (
        ('DISPONIBLE', 'Disponible'),
        ('LOUE', 'Loué'),
        ('VENDU', 'Vendu'),
        ('EN_MAINTENANCE', 'En maintenance'),
    )

    propriete = models.ForeignKey(Propriete, on_delete=models.CASCADE, related_name='logements')
    identifiant = models.CharField(max_length=50)  # ex: "A-203", "B-01"
    surface = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    etage = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)

    # Type spécifique de logement (pour plus de granularité)
    type_logement = models.ForeignKey(TypeLogement, on_delete=models.SET_NULL, null=True, blank=True)

    # Statut individuel pour chaque logement
    statut = models.CharField(max_length=20, choices=STATUT_CHOIX, default='DISPONIBLE')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.propriete} - {self.identifiant}"

class Contrat(models.Model):
    """NOUVEAU : Contrat central (location/vente)"""
    TYPE_CHOIX = (
        ('LOCATION', 'Location'),
        ('VENTE', 'Vente'),
        ('BAIL_COMMERCIAL', 'Bail commercial'),
    )

    reference = models.CharField(max_length=50, unique=True)

    @classmethod
    def generate_reference(cls, contrat_type, year=None):
        """
        Génère une référence unique pour un contrat selon le format TYPE-ANNEE-NUMERO
        Exemple: LOC-2024-001, VENT-2024-001, etc.
        """
        if year is None:
            year = timezone.now().year

        # Trouver le dernier numéro pour ce type et cette année
        last_contrat = Contrat.objects.filter(
            reference__startswith=f"{contrat_type[:3]}-{year}-"
        ).order_by('-reference').first()

        if last_contrat:
            # Extraire le numéro et incrémenter
            last_num = int(last_contrat.reference.split('-')[-1])
            new_num = last_num + 1
        else:
            new_num = 1

        # Formater avec zéros initiaux (3 chiffres)
        return f"{contrat_type[:3]}-{year}-{new_num:03d}"
    type = models.CharField(max_length=20, choices=TYPE_CHOIX)
    
    propriete = models.ForeignKey(Propriete, on_delete=models.CASCADE, related_name='contrats', null=True, blank=True)
    logement = models.ForeignKey(Logement, on_delete=models.CASCADE, related_name='contrats', null=True, blank=True)
    proprietaire = models.ForeignKey('Proprietaire', on_delete=models.CASCADE, related_name='contrats')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contrats')
    agent = models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True, blank=True, related_name='contrats_geres')
    
    # Dates
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)  # null pour vente
    
    # Financier
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    conditions = models.TextField()
    
    # Statut
    STATUT_CHOIX = (
        ('BROUILLON', 'Brouillon'),
        ('ACTIF', 'Actif'),
        ('TERMINE', 'Terminé'),
        ('RESILIE', 'Résilié'),
    )
    statut = models.CharField(max_length=20, choices=STATUT_CHOIX, default='BROUILLON')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reference} - {self.type}"

    def save(self, *args, **kwargs):
        """
        Remplit automatiquement le propriétaire si ce n'est pas déjà défini.
        Le propriétaire est déterminé à partir de la propriété ou du logement lié.
        """
        if not self.proprietaire:
            if self.propriete:
                self.proprietaire = self.propriete.proprietaire
            elif self.logement:
                self.proprietaire = self.logement.propriete.proprietaire
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='un_seul_bien_par_contrat',
                check=(
                    models.Q(propriete__isnull=False, logement__isnull=True) |
                    models.Q(propriete__isnull=True, logement__isnull=False)
                )
            )
        ]

class Maintenance(models.Model):
    """NOUVEAU : Suivi des maintenances"""
    propriete = models.ForeignKey(Propriete, on_delete=models.CASCADE, related_name='maintenances')
    logement = models.ForeignKey(Logement, on_delete=models.CASCADE, null=True, blank=True, related_name='maintenances')
    
    description = models.TextField()
    prestataire = models.CharField(max_length=100)
    cout = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Maintenance {self.propriete} - {self.date}"

class Garantie(models.Model):
    STATUT_CHOIX = (
        ('EN_ATTENTE', 'En attente'),
        ('VERSEE', 'Versée'),
        ('PARTIELLEMENT_UTILISEE', 'Partiellement utilisée'),
        ('UTILISEE', 'Utilisée'),
        ('REMBOURSEE', 'Remboursée'),
    )
    TYPE_GARANTIE_CHOIX = (
        ('UNIQUE', 'Versement unique'),
        ('MENSUELLE', 'Planification mensuelle'),
        ('AUTRE', 'Autre'),
    )

    contrat = models.OneToOneField(Contrat, on_delete=models.CASCADE, related_name='garantie')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_garantie = models.CharField(max_length=20, choices=TYPE_GARANTIE_CHOIX, default='UNIQUE')
    statut = models.CharField(max_length=30, choices=STATUT_CHOIX, default='EN_ATTENTE')
    date_constitution = models.DateField(help_text="Date de versement ou de début de la garantie")
    notes = models.TextField(blank=True, help_text="Conditions spécifiques ou notes sur la garantie")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Garantie de {self.montant} pour le contrat {self.contrat.reference}"
