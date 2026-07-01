from django.db import models
from app_base.models import Client, Contrat, Personnel


# Create your models here.
class Paiement(models.Model):
    TYPE_CHOICES = (
        ('LOYER', 'Loyer'),
        ('CAUTION', 'Caution'),
        ('FRAIS_AGENCE', "Frais d'agence"),
        ('AUTRE', 'Autre'),
    )
    STATUT_CHOICES = (
        ('PAYE', 'Payé'),
        ('EN_ATTENTE', 'En attente'),
        ('EN_RETARD', 'En retard'),
        ('ANNULE', 'Annulé'),
    )

    contrat = models.ForeignKey(Contrat, on_delete=models.CASCADE, related_name='paiements')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    agent = models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True, blank=True, related_name='paiements')
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    date_paiement = models.DateField(null=True, blank=True, help_text="La date à laquelle le paiement a été effectué.")
    date_echeance = models.DateField(help_text="La date à laquelle le paiement est attendu.")
    type_paiement = models.CharField(max_length=20, choices=TYPE_CHOICES, default='LOYER')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        # Affiche des informations plus utiles dans l'admin
        return f"Paiement de {self.montant} pour {self.contrat.reference} ({self.get_statut_display()})"

    def est_en_retard(self):
        from django.utils import timezone
        # Un paiement est en retard si :
        # 1. Son statut est 'EN_ATTENTE'
        # 2. Sa date d'échéance est strictement inférieure à aujourd'hui
        # (les paiements dus aujourd'hui ne sont pas encore en retard)
        if self.statut == 'EN_ATTENTE' and self.date_echeance < timezone.now().date():
            return True
        return False

# Le modèle Impayes est supprimé au profit d'un champ 'statut' dans Paiement.
