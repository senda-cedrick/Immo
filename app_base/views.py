from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    AgenceForm, PersonnelForm, ProprietaireForm, ClientForm,
    TypeProprieteForm, TypeLogementForm, ProprieteForm, LogementForm,
    ContratForm, GarantieForm, MaintenanceForm
)
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    Agence, Personnel, Proprietaire, Client,
    TypePropriete, TypeLogement, Propriete, Logement, Contrat, Garantie, Maintenance
)
from django.http import JsonResponse
from app_paiements.models import Paiement
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import ProprietaireProprieteSerializer, ProprietaireContratSerializer

# Supprimé car ces vues n'existaient pas
# def garanties(request): ...
# def locataires(request): ...
# def proprietaires(request): ...

@login_required
def dashboard(request):
    # Logique pour récupérer les statistiques du dashboard
    user = request.user
    if user.is_authenticated and user.profile and user.profile.name == 'Proprietaire':
        proprietes_ids = Propriete.objects.filter(proprietaire__user=user).values_list('id', flat=True)
        nb_prop = proprietes_ids.count()
        nb_log = Logement.objects.filter(propriete_id__in=proprietes_ids).count()

        # Calculer le nombre d'agences qui gèrent les propriétés du propriétaire
        nb_agences = Propriete.objects.filter(
            id__in=proprietes_ids
        ).values('agence').distinct().count()

        # Calculer le nombre de clients qui louent les logements du propriétaire
        contrats_ids = Contrat.objects.filter(
            Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids)
        ).values_list('id', flat=True)
        clients_ids = Contrat.objects.filter(id__in=contrats_ids).values('client').distinct()
        nb_clients = clients_ids.count()

        nb_contrat_actif = Contrat.objects.filter(
            Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids),
            statut='ACTIF'
        ).count()
        nb_contrat_non_sign = Contrat.objects.filter(
            Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids),
            statut='BROUILLON'
        ).count()

        # Calculer le revenu mensuel estimé
        from django.db.models import Sum
        revenu_mensuel = Contrat.objects.filter(
            Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids),
            statut='ACTIF'
        ).aggregate(total=Sum('montant'))['total'] or 0

        # Calculer le taux d'occupation
        taux_occupation = 0
        if nb_log > 0:
            logements_occupes = Contrat.objects.filter(
                Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids),
                statut='ACTIF'
            ).values('logement').distinct().count()
            taux_occupation = round((logements_occupes / nb_log) * 100)

        # Calculer le nombre de paiements en retard
        paiements_retard = Paiement.objects.filter(
            contrat_id__in=contrats_ids,
            statut='EN_RETARD'
        ).count()

        # Calculer le nombre de contrats expirant dans les 30 jours
        from django.utils import timezone
        from datetime import timedelta
        contrats_expirant = Contrat.objects.filter(
            Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids),
            statut='ACTIF',
            date_fin__gte=timezone.now(),
            date_fin__lte=timezone.now() + timedelta(days=30)
        ).count()

        # Calculer le nombre de garanties
        from app_base.models import Garantie
        nb_garanties = Garantie.objects.filter(contrat_id__in=contrats_ids).count()

        # Calculer le nombre d'entrées de caisse
        from app_caisse.models import Caisse
        nb_caisses = Caisse.objects.filter(paiement_id__in=contrats_ids).count()

        nb_paiements = Paiement.objects.filter(contrat_id__in=contrats_ids).count()
        derniers_paiements = Paiement.objects.filter(contrat_id__in=contrats_ids).select_related(
            'client__user', 'contrat'
        ).order_by('-date_paiement')[:5]

        # Utiliser le template dédié pour les propriétaires
        stats = {
            'nbagence': nb_agences,
            'nbpropriete': nb_prop,
            'nbclients': nb_clients,
            'nblogements': nb_log,
            'nbcontrats': nb_contrat_actif + nb_contrat_non_sign,
            'nbcontrats_actifs': nb_contrat_actif,
            'nbcontrats_brouillons': nb_contrat_non_sign,
            'nbpaiements': nb_paiements,
            'revenu_mensuel': revenu_mensuel,
            'taux_occupation': taux_occupation,
            'paiements_retard': paiements_retard,
            'contrats_expirant': contrats_expirant,
            'nbgaranties': nb_garanties,
            'nbcaisses': nb_caisses,
            'visites_planifiees': 0,  # À implémenter plus tard
            'derniers_paiements': derniers_paiements,
        }
        return render(request, 'home_proprietaire.html', stats)

    # Logique pour les clients
    elif user.is_authenticated and user.profile and user.profile.name == 'Client':
        # Récupérer les données spécifiques au client
        client_obj = Client.objects.get(user=user)

        # Importer timezone et timedelta pour les calculs de dates
        from django.utils import timezone
        from datetime import timedelta

        # Statistiques pour le client
        contrats_actifs = Contrat.objects.filter(client=client_obj, statut='ACTIF')
        nb_contrats_actifs = contrats_actifs.count()

        # Calculer le nombre de paiements en retard
        paiements_retard = Paiement.objects.filter(
            client=client_obj,
            statut='EN_RETARD'
        ).count()

        # Calculer le montant total dû
        from django.db.models import Sum
        montant_du = Paiement.objects.filter(
            client=client_obj,
            statut__in=['EN_ATTENTE', 'EN_RETARD']
        ).aggregate(total=Sum('montant'))['total'] or 0

        # Calculer le nombre de paiements à venir (non payés, non en retard)
        paiements_a_venir = Paiement.objects.filter(
            client=client_obj,
            statut='EN_ATTENTE',
            date_echeance__gte=timezone.now()
        ).count()

        # Récupérer les paiements proches (prochains 30 jours)
        paiements_prochains = Paiement.objects.filter(
            client=client_obj,
            date_echeance__gte=timezone.now(),
            date_echeance__lte=timezone.now() + timedelta(days=30)
        ).select_related('contrat').order_by('date_echeance')

        # Calculer le nombre de contrats proches de l'expiration
        contrats_proches_expiration = Contrat.objects.filter(
            client=client_obj,
            statut='ACTIF',
            date_fin__gte=timezone.now(),
            date_fin__lte=timezone.now() + timedelta(days=30)
        ).count()

        # Calculer le montant total des paiements en retard
        montant_retard = Paiement.objects.filter(
            client=client_obj,
            statut='EN_RETARD'
        ).aggregate(total=Sum('montant'))['total'] or 0

        # Préparer les données pour le template
        client_stats = {
            'nb_contrats_actifs': nb_contrats_actifs,
            'paiements_retard': paiements_retard,
            'montant_du': montant_du,
            'paiements_a_venir': paiements_a_venir,
            'contrats_actifs': contrats_actifs,
            'paiements_prochains': paiements_prochains,
            'contrats_proches_expiration': contrats_proches_expiration,
            'montant_retard': montant_retard,
        }
        return render(request, 'home_client.html', client_stats)

    from app_caisse.models import Caisse
    from app_base.models import Garantie
    stats = {
        'nbagence': Agence.objects.filter(active=True).count(),
        'nbpropriete': Propriete.objects.count(),
        'nbclients': Client.objects.count(),
        'nbproprietaires': Proprietaire.objects.count(),
        'nbpersonnel': Personnel.objects.count(),
        'nbcontrats': Contrat.objects.count(),
        'nbpaiements': Paiement.objects.count(),
        'nbcaisse': Caisse.objects.count(),
        'nbgaranties': Garantie.objects.count(),
        'nblogements': Logement.objects.count(),
        'derniers_paiements': Paiement.objects.select_related('client__user').order_by('-date_paiement')[:5]
    }
    return render(request, 'home.html', stats)

# --- Vues pour Agence ---

class AgenceListView(LoginRequiredMixin, ListView):
    model = Agence
    template_name = 'agences.html'
    context_object_name = 'agences'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().annotate(
            effectif=Count('personnel', distinct=True),
            revenu=Sum(
                'proprietes__contrats__montant',
                filter=Q(proprietes__contrats__statut='ACTIF'),
                default=0
            )
        )
        user = self.request.user
        if user.is_authenticated and getattr(user, 'profile', None) and user.profile.name == 'Proprietaire':
            ids = Propriete.objects.filter(proprietaire__user=user).values_list('agence', flat=True).distinct()
            qs = qs.filter(id__in=ids)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(nom__icontains=query)
        return qs


class AgenceDetailView(LoginRequiredMixin, DetailView):
    model = Agence
    template_name = 'agence_detail.html'
    context_object_name = 'agence'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agence = context['agence']
        agence.effectif = agence.personnel.count()
        proprietes_ids = agence.proprietes.values_list('id', flat=True)
        revenu = Contrat.objects.filter(
            propriete_id__in=proprietes_ids,
            statut='ACTIF'
        ).aggregate(total=Sum('montant'))['total'] or 0
        agence.revenu = revenu

        context['personnels'] = agence.personnel.select_related('user').all()
        context['proprietes'] = agence.proprietes.select_related('type_propriete').all()
        context['contrats'] = Contrat.objects.filter(
            propriete__agence=agence
        ).select_related('client', 'propriete').order_by('-date_debut')[:10]
        context['total_personnel'] = agence.effectif
        context['total_proprietes'] = agence.proprietes.count()
        context['total_contrats_actifs'] = agence.proprietes.filter(contrats__statut='ACTIF').count()
        return context

class AgenceCreateView(LoginRequiredMixin, CreateView):
    model = Agence
    form_class = AgenceForm
    template_name = 'agence_form.html'
    success_url = reverse_lazy('agences')

class AgenceUpdateView(LoginRequiredMixin, UpdateView):
    model = Agence
    form_class = AgenceForm
    template_name = 'agence_form.html'
    success_url = reverse_lazy('agences')

class AgenceDeleteView(LoginRequiredMixin, DeleteView):
    model = Agence
    template_name = 'agence_confirm_delete.html'
    success_url = reverse_lazy('agences')
    success_message = "Agence supprimée avec succès."


# --- Vues pour Personnel ---

class PersonnelListView(LoginRequiredMixin, ListView):
    model = Personnel
    template_name = 'personnels.html'
    context_object_name = 'personnels'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('agence', 'user')
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(user__noms__icontains=query) |
                Q(agence__nom__icontains=query) |
                Q(telephone__icontains=query)
            )
        return qs

class PersonnelDetailView(LoginRequiredMixin, DetailView):
    model = Personnel
    template_name = 'personnel_detail.html'
    context_object_name = 'personnel'

class PersonnelCreateView(LoginRequiredMixin, CreateView):
    model = Personnel
    form_class = PersonnelForm
    template_name = 'personnel_form.html'
    success_url = reverse_lazy('personnels')

class PersonnelUpdateView(LoginRequiredMixin, UpdateView):
    model = Personnel
    form_class = PersonnelForm
    template_name = 'personnel_form.html'
    success_url = reverse_lazy('personnels')

class PersonnelDeleteView(LoginRequiredMixin, DeleteView):
    model = Personnel
    template_name = 'personnel_confirm_delete.html'
    success_url = reverse_lazy('personnels')
    success_message = "Personnel supprimé avec succès."


# --- Vues pour Proprietaire ---

class ProprietaireListView(LoginRequiredMixin, ListView):
    model = Proprietaire
    template_name = 'proprietaire_list.html'
    context_object_name = 'proprietaires'
    paginate_by = 10

class ProprietaireDetailView(LoginRequiredMixin, DetailView):
    model = Proprietaire
    template_name = 'proprietaire_detail.html'
    context_object_name = 'proprietaire'

    def get_queryset(self):
        return super().get_queryset().select_related('user', 'agence')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proprietaire = self.get_object()

        # Récupérer les propriétés et calculer les statistiques
        proprietes_list = Propriete.objects.filter(proprietaire=proprietaire).select_related('type_propriete')
        context['proprietes'] = proprietes_list
        context['total_proprietes'] = proprietes_list.count()
        context['total_contrats'] = Contrat.objects.filter(propriete__proprietaire=proprietaire).count()

        return context

class ProprietaireCreateView(LoginRequiredMixin, CreateView):
    model = Proprietaire
    form_class = ProprietaireForm
    template_name = 'proprietaire_form.html'
    success_url = reverse_lazy('proprietaires')

class ProprietaireUpdateView(LoginRequiredMixin, UpdateView):
    model = Proprietaire
    form_class = ProprietaireForm
    template_name = 'proprietaire_form.html'
    success_url = reverse_lazy('proprietaires')

class ProprietaireDeleteView(LoginRequiredMixin, DeleteView):
    model = Proprietaire
    template_name = 'proprietaire_confirm_delete.html'
    success_url = reverse_lazy('proprietaires')


# --- Vues pour Client ---

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients.html'
    context_object_name = 'clients'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and getattr(user, 'profile', None) and user.profile.name == 'Proprietaire':
            proprietes_ids = Propriete.objects.filter(proprietaire__user=user).values_list('id', flat=True)
            contrats_ids = Contrat.objects.filter(
                Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids)
            ).values_list('client', flat=True).distinct()
            qs = qs.filter(id__in=contrats_ids)
        return qs

class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'client_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.get_object()

        # Calculer les statistiques
        context['total_contrats'] = Contrat.objects.filter(client=client).count()
        context['total_paiements'] = Paiement.objects.filter(client=client).count()
        context['contrats_actifs'] = Contrat.objects.filter(client=client, statut='ACTIF').count()

        # Calculer le montant dû (paiements en retard ou non payés)
        paiements_en_retard = Paiement.objects.filter(
            client=client,
            statut__in=['EN_ATTENTE', 'EN_RETARD']
        )
        context['montant_du'] = paiements_en_retard.aggregate(
            total=Sum('montant')
        )['total'] or 0

        # Récupérer les contrats et paiements du client
        context['contrats'] = Contrat.objects.filter(client=client).select_related(
            'propriete', 'logement', 'agent__user'
        ).order_by('-date_debut')[:10]

        context['paiements'] = Paiement.objects.filter(client=client).select_related(
            'contrat'
        ).order_by('-date_paiement')[:10]

        return context

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client_form.html'
    success_url = reverse_lazy('clients')

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client_form.html'
    success_url = reverse_lazy('clients')

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'client_confirm_delete.html'
    success_url = reverse_lazy('clients')


# --- Vues pour TypePropriete ---

class TypeProprieteListView(LoginRequiredMixin, ListView):
    model = TypePropriete
    template_name = 'type_proprietes.html'
    context_object_name = 'type_proprietes'
    paginate_by = 10

    def get_queryset(self):
        # Optimisation des requêtes avec prefetch_related
        return super().get_queryset().prefetch_related('propriete_set__logements')

class TypeProprieteDetailView(LoginRequiredMixin, DetailView):
    model = TypePropriete
    template_name = 'type_propriete_detail.html'
    context_object_name = 'type_propriete'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('propriete_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_propriete = self.get_object()
        context['proprietes'] = type_propriete.propriete_set.select_related('type_propriete', 'agence').all()  # type: ignore
        context['total_proprietes'] = context['proprietes'].count()
        return context

class TypeProprieteCreateView(LoginRequiredMixin, CreateView):
    model = TypePropriete
    form_class = TypeProprieteForm
    template_name = 'type_propriete_form.html'
    success_url = reverse_lazy('type_proprietes')

class TypeProprieteUpdateView(LoginRequiredMixin, UpdateView):
    model = TypePropriete
    form_class = TypeProprieteForm
    template_name = 'type_propriete_form.html'
    success_url = reverse_lazy('type_proprietes')

class TypeProprieteDeleteView(LoginRequiredMixin, DeleteView):
    model = TypePropriete
    template_name = 'type_propriete_confirm_delete.html'
    success_url = reverse_lazy('type_proprietes')

# --- Vues pour TypeLogement ---

class TypeLogementListView(LoginRequiredMixin, ListView):
    model = TypeLogement
    template_name = 'type_logements.html'
    context_object_name = 'type_logements'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().prefetch_related('logement_set')

class TypeLogementDetailView(LoginRequiredMixin, DetailView):
    model = TypeLogement
    template_name = 'type_logement_detail.html'
    context_object_name = 'type_logement'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('logement_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_logement = self.get_object()
        context['logements'] = type_logement.logement_set.select_related('propriete__type_propriete', 'propriete__agence').all()  # type: ignore
        context['total_logements'] = context['logements'].count()
        return context

class TypeLogementCreateView(LoginRequiredMixin, CreateView):
    model = TypeLogement
    form_class = TypeLogementForm
    template_name = 'type_logement_form.html'
    success_url = reverse_lazy('type_logements')

class TypeLogementUpdateView(LoginRequiredMixin, UpdateView):
    model = TypeLogement
    form_class = TypeLogementForm
    template_name = 'type_logement_form.html'
    success_url = reverse_lazy('type_logements')

class TypeLogementDeleteView(LoginRequiredMixin, DeleteView):
    model = TypeLogement
    template_name = 'type_logement_confirm_delete.html'
    success_url = reverse_lazy('type_logements')



# --- Vues pour Propriete ---

class ProprieteListView(LoginRequiredMixin, ListView):
    model = Propriete
    template_name = 'proprietes.html'
    context_object_name = 'proprietes'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('agence', 'proprietaire__user', 'type_propriete', 'agent__user')
        user = self.request.user
        if user.is_authenticated and getattr(user, 'profile', None) and user.profile.name == 'Proprietaire':
            qs = qs.filter(proprietaire__user=user)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(adresse__icontains=query) |
                Q(ville__icontains=query) |
                Q(proprietaire__user__noms__icontains=query) |
                Q(type_propriete__nom__icontains=query)
            )
        return qs

class ProprieteDetailView(LoginRequiredMixin, DetailView):
    model = Propriete
    template_name = 'propriete_detail.html'
    context_object_name = 'propriete'

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related('type_propriete', 'agent__user', 'agence', 'proprietaire__user')
            .prefetch_related('logements', 'contrats__client__user', 'contrats__agent__user')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        propriete = self.get_object()
        context['logements'] = propriete.logements.all()  # type: ignore
        context['contrats'] = propriete.contrats.all()  # type: ignore
        return context

class ProprieteCreateView(LoginRequiredMixin, CreateView):
    model = Propriete
    form_class = ProprieteForm
    template_name = 'propriete_form.html'
    success_url = reverse_lazy('proprietes')

class ProprieteUpdateView(LoginRequiredMixin, UpdateView):
    model = Propriete
    form_class = ProprieteForm
    template_name = 'propriete_form.html'
    success_url = reverse_lazy('proprietes')

class ProprieteDeleteView(LoginRequiredMixin, DeleteView):
    model = Propriete
    template_name = 'propriete_confirm_delete.html'
    success_url = reverse_lazy('proprietes')


# --- Vues pour Logement ---

class LogementListView(LoginRequiredMixin, ListView):
    model = Logement
    template_name = 'logements.html'
    context_object_name = 'logements'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('propriete__type_propriete', 'propriete__agence', 'propriete__proprietaire__user')
        user = self.request.user
        if user.is_authenticated and getattr(user, 'profile', None) and user.profile.name == 'Proprietaire':
            proprietes_ids = Propriete.objects.filter(proprietaire__user=user).values_list('id', flat=True)
            qs = qs.filter(propriete_id__in=proprietes_ids)
        return qs

class LogementDetailView(LoginRequiredMixin, DetailView):
    model = Logement
    template_name = 'logement_detail.html'
    context_object_name = 'logement'

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related('propriete__type_propriete', 'propriete__agence', 'propriete__proprietaire__user')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logement = self.get_object()
        context['contrats'] = logement.propriete.contrats.select_related('client__user', 'agent__user').all()  # type: ignore
        return context

class LogementCreateView(LoginRequiredMixin, CreateView):
    model = Logement
    form_class = LogementForm
    template_name = 'logement_form.html'
    success_url = reverse_lazy('logements')

class LogementUpdateView(LoginRequiredMixin, UpdateView):
    model = Logement
    form_class = LogementForm
    template_name = 'logement_form.html'
    success_url = reverse_lazy('logements')

class LogementDeleteView(LoginRequiredMixin, DeleteView):
    model = Logement
    template_name = 'logement_confirm_delete.html'
    success_url = reverse_lazy('logements')


# --- Vues pour Contrat ---

class ContratListView(LoginRequiredMixin, ListView):
    model = Contrat
    template_name = 'contrat_list.html'
    context_object_name = 'contrats'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related(
            'client__user', 'agent__user',
            'propriete__type_propriete', 'logement__propriete__type_propriete'
        )
        user = self.request.user
        if user.is_authenticated and getattr(user, 'profile', None):
            if user.profile.name == 'Proprietaire':
                proprietes_ids = Propriete.objects.filter(proprietaire__user=user).values_list('id', flat=True)
                qs = qs.filter(
                    Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids)
                )
            elif user.profile.name == 'Client':
                # Les clients ne voient que leurs propres contrats
                qs = qs.filter(client__user=user)
        return qs

class ContratDetailView(LoginRequiredMixin, DetailView):
    model = Contrat
    template_name = 'contrat_detail.html'
    context_object_name = 'contrat'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'client__user', 'agent__user', 
            'propriete__type_propriete', 'logement__propriete__type_propriete'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contrat = self.get_object()
        context['paiements'] = Paiement.objects.filter(contrat=contrat).order_by('-date_echeance')
        return context

class ContratCreateView(LoginRequiredMixin, CreateView):
    model = Contrat
    form_class = ContratForm
    template_name = 'contrat_form.html'
    success_url = reverse_lazy('contrats')

class ContratUpdateView(LoginRequiredMixin, UpdateView):
    model = Contrat
    form_class = ContratForm
    template_name = 'contrat_form.html'
    success_url = reverse_lazy('contrats')

class ContratDeleteView(LoginRequiredMixin, DeleteView):
    model = Contrat
    template_name = 'contrat_confirm_delete.html'
    success_url = reverse_lazy('contrats')


# --- Vues pour Garantie ---

class GarantieListView(LoginRequiredMixin, ListView):
    model = Garantie
    template_name = 'garantie_list.html'
    context_object_name = 'garanties'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('contrat__client__user')
        user = self.request.user
        if user.is_authenticated and getattr(user, 'profile', None) and user.profile.name == 'Proprietaire':
            proprietes_ids = Propriete.objects.filter(proprietaire__user=user).values_list('id', flat=True)
            contrats_ids = Contrat.objects.filter(
                Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids)
            ).values_list('id', flat=True)
            qs = qs.filter(contrat_id__in=contrats_ids)
        return qs

class GarantieCreateView(LoginRequiredMixin, CreateView):
    model = Garantie
    form_class = GarantieForm
    template_name = 'garantie_form.html'
    success_url = reverse_lazy('garanties')

class GarantieUpdateView(LoginRequiredMixin, UpdateView):
    model = Garantie
    form_class = GarantieForm
    template_name = 'garantie_form.html'
    success_url = reverse_lazy('garanties')

class GarantieDetailView(LoginRequiredMixin, DetailView):
    model = Garantie
    template_name = 'garantie_detail.html' # Vous devrez créer ce template
    context_object_name = 'garantie'

    def get_queryset(self):
        return super().get_queryset().select_related('contrat__client__user')

class GarantieDeleteView(LoginRequiredMixin, DeleteView):
    model = Garantie
    template_name = 'garantie_confirm_delete.html' # Vous devrez créer ce template
    success_url = reverse_lazy('garanties')
    success_message = "Garantie supprimée avec succès."


# --- Vues pour Maintenance ---

class MaintenanceListView(LoginRequiredMixin, ListView):
    model = Maintenance
    template_name = 'maintenance_list.html'
    context_object_name = 'maintenances'
    paginate_by = 10

class MaintenanceCreateView(LoginRequiredMixin, CreateView):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'maintenance_form.html'
    success_url = reverse_lazy('maintenances')

class MaintenanceDetailView(LoginRequiredMixin, DetailView):
    model = Maintenance
    template_name = 'maintenance_detail.html' # Vous devrez créer ce template
    context_object_name = 'maintenance'

class MaintenanceUpdateView(LoginRequiredMixin, UpdateView):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'maintenance_form.html'
    success_url = reverse_lazy('maintenances')

class MaintenanceDeleteView(LoginRequiredMixin, DeleteView):
    model = Maintenance
    template_name = 'maintenance_confirm_delete.html' # Vous devrez créer ce template
    success_url = reverse_lazy('maintenances')
    success_message = "Maintenance supprimée avec succès."

# --- Vues API pour le Javascript ---

@login_required
def get_logements_for_propriete(request):
    """
    API endpoint pour récupérer les logements d'une propriété.
    Utilisé par le formulaire de contrat pour le dropdown dépendant.
    """
    propriete_id = request.GET.get('propriete_id')
    if not propriete_id:
        return JsonResponse({'logements': []})

    logements = Logement.objects.filter(propriete_id=propriete_id).values('id', 'identifiant')
    return JsonResponse({'logements': list(logements)})

@login_required
def generate_contrat_reference(request):
    """
    API endpoint pour générer une référence de contrat automatique.
    Utilisé par le formulaire de contrat pour générer des références uniques.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

    try:
        data = json.loads(request.body)
        contrat_type = data.get('type')

        if not contrat_type:
            return JsonResponse({'error': 'Type de contrat requis'}, status=400)

        # Générer la référence en utilisant la méthode du modèle
        reference = Contrat.generate_reference(contrat_type)

        return JsonResponse({'reference': reference})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# --- API pour Proprietaire ---

class ProprietaireDashboardAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not (user.profile and user.profile.name == 'Proprietaire'):
            return Response({'error': 'Accès refusé'}, status=403)

        proprietes_ids = Propriete.objects.filter(proprietaire__user=user).values_list('id', flat=True)
        nb_prop = proprietes_ids.count()
        nb_log = Logement.objects.filter(propriete_id__in=proprietes_ids).count()
        nb_agences = Propriete.objects.filter(id__in=proprietes_ids).values('agence').distinct().count()

        contrats_ids = Contrat.objects.filter(
            Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids)
        ).values_list('id', flat=True)
        clients_ids = Contrat.objects.filter(id__in=contrats_ids).values('client').distinct()
        nb_clients = clients_ids.count()

        nb_contrat_actif = Contrat.objects.filter(
            Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids),
            statut='ACTIF'
        ).count()
        nb_contrat_non_sign = Contrat.objects.filter(
            Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids),
            statut='BROUILLON'
        ).count()

        revenu_mensuel = Contrat.objects.filter(
            Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids),
            statut='ACTIF'
        ).aggregate(total=Sum('montant'))['total'] or 0

        taux_occupation = 0
        if nb_log > 0:
            logements_occupes = Contrat.objects.filter(
                Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids),
                statut='ACTIF'
            ).values('logement').distinct().count()
            taux_occupation = round((logements_occupes / nb_log) * 100)

        paiements_retard = Paiement.objects.filter(
            contrat_id__in=contrats_ids,
            statut='EN_RETARD'
        ).count()

        contrats_expirant = Contrat.objects.filter(
            Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids),
            statut='ACTIF',
            date_fin__gte=timezone.now(),
            date_fin__lte=timezone.now() + timedelta(days=30)
        ).count()

        nb_paiements = Paiement.objects.filter(contrat_id__in=contrats_ids).count()

        data = {
            'nb_proprietes': nb_prop,
            'nb_logements': nb_log,
            'nb_agences': nb_agences,
            'nb_clients': nb_clients,
            'nb_contrats_actifs': nb_contrat_actif,
            'nb_contrats_non_signes': nb_contrat_non_sign,
            'revenu_mensuel': revenu_mensuel,
            'taux_occupation': taux_occupation,
            'nb_paiements_retard': paiements_retard,
            'nb_contrats_expirant_30j': contrats_expirant,
            'nb_paiements_total': nb_paiements,
        }
        return Response(data)


class ProprietaireProprietesAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not (user.profile and user.profile.name == 'Proprietaire'):
            return Response({'error': 'Accès refusé'}, status=403)

        proprietes = Propriete.objects.filter(proprietaire__user=user).select_related('type_propriete', 'agence')
        serializer = ProprietaireProprieteSerializer(proprietes, many=True)
        return Response(serializer.data)


class ProprietaireContratsAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not (user.profile and user.profile.name == 'Proprietaire'):
            return Response({'error': 'Accès refusé'}, status=403)

        proprietes_ids = Propriete.objects.filter(proprietaire__user=user).values_list('id', flat=True)
        contrats = Contrat.objects.filter(
            Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids)
        ).select_related('client__user', 'propriete', 'logement', 'agent__user')
        serializer = ProprietaireContratSerializer(contrats, many=True)
        return Response(serializer.data)
