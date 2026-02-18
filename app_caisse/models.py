from django.db import models
from app_base.models import Locataire
# Create your models here.
class Caisse(models.Model):
    id_caisse =  models.IntegerField(primary_key=True)
    type_caisse = models.ForeignKey(Locataire, on_delete=models.CASCADE)
    status_caisse = models.CharField(max_length=50)
    cout= models.IntegerField()
    paiement = models.CharField(max_length=50)
    details= models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
            managed = False
            db_table = 'caisse'

    def _str_(self):
        return self.id_caisse  