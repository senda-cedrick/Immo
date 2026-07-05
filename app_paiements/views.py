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

        # Filtrer par statut si le paramètre est présent dans l'URL
        statut_filter = self.request.GET.get('statut')
        if statut_filter:
            # Gérer les statuts multiples séparés par des virgules
            statuts = [s.strip() for s in statut_filter.split(',')]
            qs = qs.filter(statut__in=statuts)

        # Filtrer par état de retard si les paramètres sont présents
        non_retard = self.request.GET.get('non_retard')
        en_retard_param = self.request.GET.get('en_retard')

        if non_retard:
            # Filtrer les paiements EN_ATTENTE qui ne sont pas en retard
            qs = qs.filter(statut='EN_ATTENTE')
            qs = [p for p in qs if not p.est_en_retard()]
            # Convertir la liste en queryset (solution temporaire)
            if qs:
                ids = [p.id for p in qs]
                qs = super().get_queryset().filter(id__in=ids).select_related('contrat__client__user', 'agent__user')
            else:
                qs = super().get_queryset().none()

        elif en_retard_param:
            # Filtrer les paiements qui sont en retard (EN_RETARD ou EN_ATTENTE en retard)
            qs = list(qs)
            qs = [p for p in qs if p.statut == 'EN_RETARD' or p.est_en_retard()]
            # Convertir la liste en queryset
            if qs:
                ids = [p.id for p in qs]
                qs = super().get_queryset().filter(id__in=ids).select_related('contrat__client__user', 'agent__user')
            else:
                qs = super().get_queryset().none()

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
                try:
                    client_obj = Client.objects.get(user=user)
                    qs = qs.filter(client=client_obj)
                except Client.DoesNotExist:
                    # Si le client n'existe pas, retourner un queryset vide
                    qs = qs.none()
        else:
            # Si l'utilisateur n'a pas de profil, retourner un queryset vide
            qs = qs.none()
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