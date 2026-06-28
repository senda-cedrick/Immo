from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    AgenceForm, PersonnelForm, ProprietaireForm, ClientForm,
    TypeProprieteForm, ProprieteForm, LogementForm,
    ContratForm, GarantieForm, MaintenanceForm
)
from django.db.models import Sum, Count, Q
from django.utils import timezone
from .models import (
    Agence, Personnel, Proprietaire, Client,
    TypePropriete, Propriete, Logement, Contrat, Garantie, Maintenance
)
from app_paiements.models import Paiement

# Supprimé car ces vues n'existaient pas
# def garanties(request): ...
# def locataires(request): ...
# def proprietaires(request): ...

@login_required
def dashboard(request):
    # Logique pour récupérer les statistiques du dashboard
    stats = {
        'nbagence': Agence.objects.filter(active=True).count(),
        'nbpropriete': Propriete.objects.count(),
        'nbclients': Client.objects.count(),
        'nbproprietaires': Proprietaire.objects.count(),
        'nbpersonnel': Personnel.objects.count(),
        'nbappartements': Logement.objects.count(),
        'nbcontrats': Contrat.objects.count(),
        'nbpaiements': Paiement.objects.count(),
        'nbcaisse': 0,  # À implémenter
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

class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'client_detail.html'

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client_form.html'
    success_url = reverse_lazy('clients')

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'app_base/client_form.html'
    success_url = reverse_lazy('clients')

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'app_base/client_confirm_delete.html'
    success_url = reverse_lazy('clients')


# --- Vues pour TypePropriete ---

class TypeProprieteListView(LoginRequiredMixin, ListView):
    model = TypePropriete
    template_name = 'type_proprietes.html'
    context_object_name = 'type_proprietes'
    paginate_by = 10

class TypeProprieteDetailView(LoginRequiredMixin, DetailView):
    model = TypePropriete
    template_name = 'type_propriete_detail.html'
    context_object_name = 'type_propriete'

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


# --- Vues pour Propriete ---

class ProprieteListView(LoginRequiredMixin, ListView):
    model = Propriete
    template_name = 'proprietes.html'
    context_object_name = 'proprietes'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('agence', 'proprietaire__user', 'type_propriete', 'agent__user')
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
    template_name = 'app_base/propriete_detail.html' # Assurez-vous que ce template existe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        propriete = context['propriete']
        context['logements'] = propriete.logements.all()
        context['contrats'] = propriete.contrats.select_related('client__user', 'agent__user').all()
        return context

class ProprieteCreateView(LoginRequiredMixin, CreateView):
    model = Propriete
    form_class = ProprieteForm
    template_name = 'app_base/propriete_form.html'
    success_url = reverse_lazy('proprietes')

class ProprieteUpdateView(LoginRequiredMixin, UpdateView):
    model = Propriete
    form_class = ProprieteForm
    template_name = 'app_base/propriete_form.html'
    success_url = reverse_lazy('proprietes')

class ProprieteDeleteView(LoginRequiredMixin, DeleteView):
    model = Propriete
    template_name = 'app_base/propriete_confirm_delete.html'
    success_url = reverse_lazy('proprietes')


# --- Vues pour Logement ---

class LogementListView(LoginRequiredMixin, ListView):
    model = Logement
    template_name = 'logements.html'
    context_object_name = 'logements'
    paginate_by = 10

class LogementDetailView(LoginRequiredMixin, DetailView):
    model = Logement
    template_name = 'app_base/logement_detail.html'

class LogementCreateView(LoginRequiredMixin, CreateView):
    model = Logement
    form_class = LogementForm
    template_name = 'app_base/logement_form.html'
    success_url = reverse_lazy('logements')

class LogementUpdateView(LoginRequiredMixin, UpdateView):
    model = Logement
    form_class = LogementForm
    template_name = 'app_base/logement_form.html'
    success_url = reverse_lazy('logements')

class LogementDeleteView(LoginRequiredMixin, DeleteView):
    model = Logement
    template_name = 'app_base/logement_confirm_delete.html'
    success_url = reverse_lazy('logements')


# --- Vues pour Contrat ---

class ContratListView(LoginRequiredMixin, ListView):
    model = Contrat
    template_name = 'contrat_list.html'
    context_object_name = 'contrats'
    paginate_by = 10

class ContratDetailView(LoginRequiredMixin, DetailView):
    model = Contrat
    template_name = 'contrat_detail.html'
    context_object_name = 'contrat'

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
    template_name = 'app_base/garantie_list.html'
    context_object_name = 'garanties'
    paginate_by = 10

class GarantieCreateView(LoginRequiredMixin, CreateView):
    model = Garantie
    form_class = GarantieForm
    template_name = 'app_base/garantie_form.html'
    success_url = reverse_lazy('garanties')

class GarantieUpdateView(LoginRequiredMixin, UpdateView):
    model = Garantie
    form_class = GarantieForm
    template_name = 'app_base/garantie_form.html'
    success_url = reverse_lazy('garanties')


# --- Vues pour Maintenance ---

class MaintenanceListView(LoginRequiredMixin, ListView):
    model = Maintenance
    template_name = 'app_base/maintenance_list.html'
    context_object_name = 'maintenances'
    paginate_by = 10

class MaintenanceCreateView(LoginRequiredMixin, CreateView):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'app_base/maintenance_form.html'
    success_url = reverse_lazy('maintenances')