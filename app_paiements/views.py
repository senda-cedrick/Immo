from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Paiement
# from .forms import PaiementForm # Assurez-vous d'avoir un PaiementForm

class PaiementListView(LoginRequiredMixin, ListView):
    model = Paiement
    template_name = 'paiement_list.html'
    context_object_name = 'paiements'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().select_related('contrat__client__user', 'agent__user')

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