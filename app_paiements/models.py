from django.db import models
from app_base.models import Locataire


# Create your models here.
class Paiement(models.Model):
    locataires = models.ForeignKey(Locataire, on_delete=models.CASCADE)
    montant = models.IntegerField()
    date_paie = models.DateField()
    date_normal= models.DateField()
    type_paie= models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        # Affiche des informations plus utiles dans l'admin
        return f"Paiement de {self.locataires.noms} - {self.montant}"
    
class Impayes(models.Model):
    locataires = models.ForeignKey(Locataire, on_delete=models.CASCADE)
    impaye = models.IntegerField()
    situation = models.CharField(max_length=50)
    date_sortie= models.DateField()
    detail= models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    def __str__(self):
        # Affiche des informations plus utiles dans l'admin
        return f"Impayé de {self.locataires.noms} - {self.impaye}"
