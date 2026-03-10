from django.db import models
from app_paiements.models import Paiement

# Create your models here.
class Caisse(models.Model):
    id_caisse =  models.IntegerField(primary_key=True)
    type_caisse = models.CharField(max_length=50, default="Entree")
    status_caisse = models.CharField(max_length=50)
    cout= models.IntegerField()
    paiement = models.ForeignKey(Paiement, on_delete=models.CASCADE)
    details= models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 

    def _str_(self):
        return self.id_caisse  