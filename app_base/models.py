from django.db import models

# Create your models here.
class Agence(models.Model):
    # id = models.BigAutoField(primary_key=True) est ajouté automatiquement
    nom = models.CharField(max_length=50)
    numero_impot = models.CharField(max_length=50)
    numero_fisc = models.CharField(max_length=50)
    effectif = models.IntegerField(default=0)
    revenu=models.IntegerField(default=0)
    email = models.EmailField(max_length=100)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.nom} ({self.effectif})"
    
class Personnel(models.Model):
    SEXE_CHOISES = (
        ('M','Masculin'),
        ('F','Feminin'),
        ('ND','Non défini'),
    )
    # id = models.BigAutoField(primary_key=True) est ajouté automatiquement
    noms = models.CharField(max_length=50)
    sexe = models.CharField(max_length=2, choices=SEXE_CHOISES)
    role = models.CharField(max_length=50)
    status = models.CharField(max_length=40, blank=True, null=True)
    agence=models.ForeignKey(Agence, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return self.noms 

class Proprietaire(models.Model):
   
    # id = models.BigAutoField(primary_key=True) est ajouté automatiquement
    noms = models.CharField(max_length=50)
    bienconfie = models.IntegerField(blank=True, null=True)
    bienlocatif = models.IntegerField(blank=True, null=True)
    catalogue =  models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        

    def __str__(self):
        return self.noms 

class Appartement(models.Model):
       
    # id = models.BigAutoField(primary_key=True) est ajouté automatiquement
    identifiant = models.CharField(max_length=50)
    prix =  models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status =  models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.identifiant 
class Propriete(models.Model):
       
    # id = models.BigAutoField(primary_key=True) est ajouté automatiquement
    type_propiete = models.CharField(max_length=50)
    ville =  models.CharField(max_length=50)
    Agent =  models.CharField(max_length=50)
    gestion = models.BooleanField(default=True)
    appartements = models.ForeignKey(Appartement, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.Agent 
class Locataire(models.Model):
    # id = models.BigAutoField(primary_key=True) est ajouté automatiquement
    noms = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)
    contrat = models.CharField(max_length=50)
    loye = models.IntegerField(default=0)
    regularite=models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.noms} ({self.email})"
class Logement(models.Model):
    # id = models.BigAutoField(primary_key=True) est ajouté automatiquement
    identifiant = models.ForeignKey(Appartement, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    proprietaire = models.ForeignKey(Proprietaire, on_delete=models.CASCADE)
    agent= models.ForeignKey(Propriete, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.identifiant)
class Garantie(models.Model):
    # id = models.BigAutoField(primary_key=True) est ajouté automatiquement
    locataires = models.ForeignKey(Locataire, on_delete=models.CASCADE)
    montant= models.IntegerField()
    planification = models.CharField(max_length=50)
    date_appartition= models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Garantie pour {self.locataires.noms}"
