from django.db import models
from app_base.models import Locataire


# Create your models here.
class Paiement(models.Model):
    id_paie =  models.IntegerField(primary_key=True)
    locataires = models.ForeignKey(Locataire, on_delete=models.CASCADE)
    Montant = models.IntegerField()
    date_paie = models.DateField()
    date_normal= models.DateField()
    type_paie= models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
            managed = False
            db_table = 'paiement'

    def _str_(self):
        return self.id_paie
class Impayes(models.Model):
    id_impaye =  models.IntegerField(primary_key=True)
    locataires = models.ForeignKey(Locataire, on_delete=models.CASCADE)
    impaye = models.IntegerField()
    situation = models.CharField(max_length=50)
    date_sortie= models.DateField()
    detail= models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
            managed = False
            db_table = 'impaye'

    def _str_(self):
        return self.id_impaye
