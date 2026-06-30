from rest_framework import serializers
from .models import (
    Agence, Personnel, Proprietaire, Client,
    TypePropriete, TypeLogement, Propriete, Logement, Contrat, Garantie, Maintenance
)


class AgenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agence
        fields = '__all__'


class PersonnelSerializer(serializers.ModelSerializer):
    user_noms = serializers.CharField(source='user.noms', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    profile_name = serializers.CharField(source='user.profile.name', read_only=True)

    class Meta:
        model = Personnel
        fields = ['id', 'user', 'user_noms', 'user_username', 'profile_name', 'agence', 'telephone', 'adresse', 'poste']


class ProprietaireSerializer(serializers.ModelSerializer):
    user_noms = serializers.CharField(source='user.noms', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    agence_nom = serializers.CharField(source='agence.nom', read_only=True)

    class Meta:
        model = Proprietaire
        fields = ['id', 'user', 'user_noms', 'user_username', 'user_email', 'agence', 'agence_nom', 'telephone', 'adresse']


class ClientSerializer(serializers.ModelSerializer):
    user_noms = serializers.CharField(source='user.noms', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'user', 'user_noms', 'user_username', 'agence', 'telephone', 'adresse', 'profession']


class TypeProprieteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypePropriete
        fields = '__all__'


class TypeLogementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeLogement
        fields = '__all__'


class ProprieteSerializer(serializers.ModelSerializer):
    proprietaire_noms = serializers.CharField(source='proprietaire.user.noms', read_only=True)
    agence_nom = serializers.CharField(source='agence.nom', read_only=True)
    type_propriete_nom = serializers.CharField(source='type_propriete.nom', read_only=True)
    agent_noms = serializers.CharField(source='agent.user.noms', read_only=True, default=None)

    class Meta:
        model = Propriete
        fields = [
            'id', 'agence', 'agence_nom', 'proprietaire', 'proprietaire_noms',
            'type_propriete', 'type_propriete_nom', 'adresse', 'ville',
            'superficie', 'nb_pieces', 'description', 'statut', 'agent', 'agent_noms',
            'date_creation'
        ]


class LogementSerializer(serializers.ModelSerializer):
    propriete_adresse = serializers.CharField(source='propriete.adresse', read_only=True)
    type_logement_nom = serializers.CharField(source='type_logement.nom', read_only=True)

    class Meta:
        model = Logement
        fields = [
            'id', 'propriete', 'propriete_adresse', 'identifiant',
            'type_logement', 'type_logement_nom', 'etage', 'surface',
            'description', 'statut', 'loyer_mensuel', 'charges_mensuelles'
        ]


class ContratSerializer(serializers.ModelSerializer):
    proprietaire_noms = serializers.CharField(source='proprietaire.user.noms', read_only=True)
    client_noms = serializers.CharField(source='client.user.noms', read_only=True)
    agent_noms = serializers.CharField(source='agent.user.noms', read_only=True)
    propriete_adresse = serializers.CharField(source='propriete.adresse', read_only=True, default=None)
    logement_identifiant = serializers.CharField(source='logement.identifiant', read_only=True, default=None)

    class Meta:
        model = Contrat
        fields = [
            'id', 'reference', 'type_contrat', 'proprietaire', 'proprietaire_noms',
            'client', 'client_noms', 'propriete', 'propriete_adresse',
            'logement', 'logement_identifiant', 'agent', 'agent_noms',
            'date_debut', 'date_fin', 'montant', 'statut', 'date_signature',
            'notes', 'date_creation'
        ]


class GarantieSerializer(serializers.ModelSerializer):
    contrat_reference = serializers.CharField(source='contrat.reference', read_only=True)

    class Meta:
        model = Garantie
        fields = [
            'id', 'contrat', 'contrat_reference', 'type_garantie',
            'montant', 'date_debut', 'date_fin', 'description'
        ]


class MaintenanceSerializer(serializers.ModelSerializer):
    logement_identifiant = serializers.CharField(source='logement.identifiant', read_only=True)
    propriete_adresse = serializers.CharField(source='logement.propriete.adresse', read_only=True)

    class Meta:
        model = Maintenance
        fields = [
            'id', 'logement', 'logement_identifiant', 'propriete_adresse',
            'description', 'date_debut', 'date_fin', 'cout', 'statut'
        ]


# Serializers spécifiques pour les propriétaires

class ProprietaireProprieteSerializer(serializers.ModelSerializer):
    type_propriete_nom = serializers.CharField(source='type_propriete.nom', read_only=True)
    agence_nom = serializers.CharField(source='agence.nom', read_only=True)
    nb_logements = serializers.SerializerMethodField()
    nb_contrats_actifs = serializers.SerializerMethodField()
    taux_occupation = serializers.SerializerMethodField()

    class Meta:
        model = Propriete
        fields = [
            'id', 'agence_nom', 'type_propriete_nom', 'adresse', 'ville',
            'superficie', 'nb_pieces', 'statut', 'nb_logements',
            'nb_contrats_actifs', 'taux_occupation'
        ]

    def get_nb_logements(self, obj):
        return obj.logements.count()

    def get_nb_contrats_actifs(self, obj):
        return Contrat.objects.filter(
            Q(propriete=obj) | Q(logement__propriete=obj),
            statut='ACTIF'
        ).count()

    def get_taux_occupation(self, obj):
        nb_log = obj.logements.count()
        if nb_log == 0:
            return 0
        nb_occupes = Contrat.objects.filter(
            Q(propriete=obj) | Q(logement__propriete=obj),
            statut='ACTIF'
        ).values('logement').distinct().count()
        return round((nb_occupes / nb_log) * 100)


class ProprietaireContratSerializer(serializers.ModelSerializer):
    client_noms = serializers.CharField(source='client.user.noms', read_only=True)
    propriete_adresse = serializers.CharField(source='propriete.adresse', read_only=True, default=None)
    logement_identifiant = serializers.CharField(source='logement.identifiant', read_only=True, default=None)
    paiements_count = serializers.SerializerMethodField()
    dernier_paiement_date = serializers.SerializerMethodField()

    class Meta:
        model = Contrat
        fields = [
            'id', 'reference', 'type_contrat', 'client_noms',
            'propriete_adresse', 'logement_identifiant', 'date_debut',
            'date_fin', 'montant', 'statut', 'paiements_count', 'dernier_paiement_date'
        ]

    def get_paiements_count(self, obj):
        return obj.paiements.count()

    def get_dernier_paiement_date(self, obj):
        dernier = obj.paiements.order_by('-date_paiement').first()
        return dernier.date_paiement if dernier else None


class ProprietaireDashboardSerializer(serializers.Serializer):
    nb_proprietes = serializers.IntegerField()
    nb_logements = serializers.IntegerField()
    nb_agences = serializers.IntegerField()
    nb_clients = serializers.IntegerField()
    nb_contrats_actifs = serializers.IntegerField()
    nb_contrats_non_signes = serializers.IntegerField()
    revenu_mensuel = serializers.DecimalField(max_digits=15, decimal_places=2)
    taux_occupation = serializers.FloatField()
    nb_paiements_retard = serializers.IntegerField()
    nb_contrats_expirant_30j = serializers.IntegerField()
    nb_paiements_total = serializers.IntegerField()