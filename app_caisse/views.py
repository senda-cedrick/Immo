from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Sum, Q
from .models import Caisse
from .forms import CaisseForm
from app_base.models import Propriete, Contrat
from app_paiements.models import Paiement

# Create your views here.

class CaisseListView(LoginRequiredMixin, ListView):
    model = Caisse
    template_name = 'caisse_list.html'
    context_object_name = 'caisses'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and getattr(user, 'profile', None) and user.profile.name == 'Proprietaire':
            proprietes_ids = Propriete.objects.filter(proprietaire__user=user).values_list('id', flat=True)
            contrats_ids = Contrat.objects.filter(
                Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids)
            ).values_list('id', flat=True)
            paiements_ids = Paiement.objects.filter(contrat_id__in=contrats_ids).values_list('id', flat=True)
            queryset = queryset.filter(paiement_id__in=paiements_ids)
        # Filtrer par type si spécifié
        type_filter = self.request.GET.get('type')
        if type_filter:
            queryset = queryset.filter(type_caisse=type_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated and getattr(user, 'profile', None) and user.profile.name == 'Proprietaire':
            proprietes_ids = Propriete.objects.filter(proprietaire__user=user).values_list('id', flat=True)
            contrats_ids = Contrat.objects.filter(
                Q(propriete_id__in=proprietes_ids) | Q(logement__propriete_id__in=proprietes_ids)
            ).values_list('id', flat=True)
            paiements_ids = Paiement.objects.filter(contrat_id__in=contrats_ids).values_list('id', flat=True)
            # Calculer les totaux par type pour le propriétaire
            context['total_entrees'] = Caisse.objects.filter(
                paiement_id__in=paiements_ids,
                type_caisse='ENTREE'
            ).count()
            context['total_sorties'] = Caisse.objects.filter(
                paiement_id__in=paiements_ids,
                type_caisse='SORTIE'
            ).count()
            context['solde'] = self.calculer_solde(paiements_ids)
        else:
            # Calculer les totaux par type pour tous
            context['total_entrees'] = Caisse.objects.filter(type_caisse='ENTREE').count()
            context['total_sorties'] = Caisse.objects.filter(type_caisse='SORTIE').count()
            context['solde'] = self.calculer_solde()
        return context

    def calculer_solde(self, paiements_ids=None):
        """Calculer le solde actuel (entrées - sorties)"""
        if paiements_ids:
            entree_total = Caisse.objects.filter(
                paiement_id__in=paiements_ids,
                type_caisse='ENTREE'
            ).aggregate(total=Sum('cout'))['total'] or 0
            sortie_total = Caisse.objects.filter(
                paiement_id__in=paiements_ids,
                type_caisse='SORTIE'
            ).aggregate(total=Sum('cout'))['total'] or 0
        else:
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