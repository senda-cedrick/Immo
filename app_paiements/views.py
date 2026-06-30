from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import Paiement
# from .forms import PaiementForm # Assurez-vous d'avoir un PaiementForm

class PaiementListView(LoginRequiredMixin, ListView):
    model = Paiement
    template_name = 'paiement_list.html'
    context_object_name = 'paiements'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('contrat__client__user', 'agent__user')
        user = self.request.user
        if user.is_authenticated and getattr(user, 'profile', None):
            if user.profile.name == 'Proprietaire':
                from app_base.models import Propriete, Contrat
                proprietes_ids = Propriete.objects.filter(proprietaire__user=user).values_list('id', flat=True)
                contrats_ids = Contrat.objects.filter(
                    Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids)
                ).values_list('id', flat=True)
                qs = qs.filter(contrat_id__in=contrats_ids)
            elif user.profile.name == 'Client':
                # Les clients ne voient que leurs propres paiements
                from app_base.models import Client
                client_obj = Client.objects.get(user=user)
                qs = qs.filter(client=client_obj)
        return qs

class PaiementCreateView(LoginRequiredMixin, CreateView):
    model = Paiement
    # form_class = PaiementForm
    fields = ['contrat', 'client', 'agent', 'montant', 'type_paiement', 'date_paiement', 'date_echeance', 'statut', 'notes']
    template_name = 'paiement_form.html'
    success_url = reverse_lazy('paiements')

class PaiementDetailView(LoginRequiredMixin, DetailView):
    model = Paiement
    template_name = 'paiement_detail.html'
    context_object_name = 'paiement'

class PaiementUpdateView(LoginRequiredMixin, UpdateView):
    model = Paiement
    # form_class = PaiementForm
    fields = ['contrat', 'client', 'agent', 'montant', 'type_paiement', 'date_paiement', 'date_echeance', 'statut', 'notes']
    template_name = 'paiement_form.html'
    success_url = reverse_lazy('paiements')

class PaiementDeleteView(LoginRequiredMixin, DeleteView):
    model = Paiement
    template_name = 'paiement_confirm_delete.html'
    success_url = reverse_lazy('paiements')