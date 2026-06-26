from django.db import models


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
    propriete = models.ForeignKey(Propriete, on_delete=models.CASCADE, related_name='logements')
    identifiant = models.CharField(max_length=50)  # ex: "A-203", "B-01"
    surface = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    etage = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    
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
    type = models.CharField(max_length=20, choices=TYPE_CHOIX)
    
    propriete = models.ForeignKey(Propriete, on_delete=models.CASCADE, related_name='contrats')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contrats')
    proprietaire = models.ForeignKey(Proprietaire, on_delete=models.CASCADE, related_name='contrats')
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
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='garanties')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    planification = models.CharField(max_length=50)
    date_apparition = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Garantie pour {self.client}"
