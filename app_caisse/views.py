from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import Caisse
from .forms import CaisseForm

# Create your views here.

class CaisseListView(LoginRequiredMixin, ListView):
    model = Caisse
    template_name = 'caisse_list.html'
    context_object_name = 'caisses'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrer par type si spécifié
        type_filter = self.request.GET.get('type')
        if type_filter:
            queryset = queryset.filter(type_caisse=type_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculer les totaux par type
        context['total_entrees'] = Caisse.objects.filter(type_caisse='ENTREE').count()
        context['total_sorties'] = Caisse.objects.filter(type_caisse='SORTIE').count()
        context['solde'] = self.calculer_solde()
        return context

    def calculer_solde(self):
        """Calculer le solde actuel (entrées - sorties)"""
        entree_total = Caisse.objects.filter(type_caisse='ENTREE').aggregate(
            total=Sum('cout')
        )['total'] or 0
        sortie_total = Caisse.objects.filter(type_caisse='SORTIE').aggregate(
            total=Sum('cout')
        )['total'] or 0
        return entree_total - sortie_total

class CaisseCreateView(LoginRequiredMixin, CreateView):
    model = Caisse
    form_class = CaisseForm
    template_name = 'caisse_form.html'
    success_url = reverse_lazy('caisses')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nouvelle entrée de caisse'
        return context

class CaisseUpdateView(LoginRequiredMixin, UpdateView):
    model = Caisse
    form_class = CaisseForm
    template_name = 'caisse_form.html'
    success_url = reverse_lazy('caisses')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modifier entrée de caisse'
        return context

class CaisseDeleteView(LoginRequiredMixin, DeleteView):
    model = Caisse
    template_name = 'caisse_confirm_delete.html'
    success_url = reverse_lazy('caisses')
    success_message = "Entrée de caisse supprimée avec succès."