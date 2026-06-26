from django.db import models
from app_base.models import Client


# Create your models here.
class Paiement(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    date_paie = models.DateField()
    date_normal= models.DateField()
    type_paie= models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        # Affiche des informations plus utiles dans l'admin
        return f"Paiement de {self.client.user.noms} - {self.montant}"
    
class Impayes(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    impaye = models.DecimalField(max_digits=12, decimal_places=2)
    situation = models.CharField(max_length=50)
    date_sortie= models.DateField()
    detail= models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    def __str__(self):
        # Affiche des informations plus utiles dans l'admin
        return f"Impayé de {self.client.user.noms} - {self.impaye}"
