from rest_framework import serializers
from .models import Paiement


class PaiementSerializer(serializers.ModelSerializer):
    contrat_info = serializers.CharField(source='contrat.__str__', read_only=True)
    client_noms = serializers.CharField(source='contrat.client.user.noms', read_only=True)

    class Meta:
        model = Paiement
        fields = ['id', 'contrat', 'contrat_info', 'client_noms',
                  'montant', 'date_paiement', 'date_echeance',
                  'mode_paiement', 'reference', 'statut',
                  'penalites', 'date_regularisation', 'situation', 'detail',
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']