from django.db import models
from app_paiements.models import Paiement

# Create your models here.
class Caisse(models.Model):
    id_caisse = models.AutoField(primary_key=True)
    type_caisse = models.CharField(max_length=50, default="Entree")
    status_caisse = models.CharField(max_length=50)
    cout = models.DecimalField(max_digits=12, decimal_places=2)
    paiement = models.ForeignKey(Paiement, on_delete=models.CASCADE, null=True, blank=True)
    details= models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 

    def __str__(self):
        return f"Caisse #{self.id_caisse} - {self.type_caisse} ({self.cout})"
