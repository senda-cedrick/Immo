from django.shortcuts import render
from django.views.generic import View

from app_base.models import Agence,Proprietaire,Propriete,Personnel,Appartement,Locataire,Logement,Garantie
from app_caisse.models import Caisse
from app_paiements.models import Paiement
from app_users.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(View):

    @method_decorator(login_required)
    def get(self, request):
        user = None
        if request.user.id:
            user = User.objects.get(pk=request.user.id)
        ctx = {
            "link":"home",
            "nblocataires" : Locataire.objects.count(),
            "nbproprietaires" : Proprietaire.objects.count(),
            "nbpropriete" : Propriete.objects.count(),
            "nbagence" : Agence.objects.count(),
            "nbpaiements" : Paiement.objects.count(),
            "nbcaisse" : Caisse.objects.count(),
            "nbgaranties" : Garantie.objects.count(),
            
            "user" : user
        }
        return render(request, "index.html", ctx)
    