from django.shortcuts import render
from django.views.generic import View

from app_base.models import Agence, Proprietaire, Propriete, Personnel, Client, Logement, Garantie, Contrat
from app_caisse.models import Caisse
from app_paiements.models import Paiement
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Sum


class HomeView(View):

    @method_decorator(login_required)
    def get(self, request):
        ctx = {
            "link":"home",
            # KPIs
            "nblocataires" : Client.objects.count(),
            "nbclients" : Client.objects.count(),
            "nbproprietaires" : Proprietaire.objects.count(),
            "nbpropriete" : Propriete.objects.count(),
            "nbagence" : Agence.objects.count(),
            "nbpaiements" : Paiement.objects.count(),
            "nbcaisse" : Caisse.objects.count(),
            "nbcontrats" : Contrat.objects.count(),
            "nbgaranties" : Garantie.objects.count(),
            "nbpersonnel" : Personnel.objects.count(),
            "nbappartements" : Logement.objects.count(),
            "nblogements" : Logement.objects.count(),
            # Derniers paiements pour le tableau
            "derniers_paiements" : Paiement.objects.select_related('client__user').order_by('-date_paie')[:5],
        }
        return render(request, "home.html", ctx)