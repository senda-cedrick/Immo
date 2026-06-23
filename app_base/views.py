from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import AgenceForm
# Create your views here.

class HomeView(TemplateView):
    template_name = 'index.html'
    
        #__Page Form create__
def home(request):
    
    return render(request, 'home.html')

def agences(request):
    
    return render(request, 'agences.html')

def garanties(request):
    return render(request, 'garanties.html')

def appartements(request):
    return render(request, 'appartements.html')

def locataires(request):
    return render(request, 'locataires.html')

def personnels(request):
    return render(request, 'personnels.html')

def proprietaires(request):
    return render(request, 'proprietaires.html')
        # _________________
        
        
        #__Page Form create__
def agence(request):
    
    return render(request,'agence.html')
        #   __________
def appartement(request):
    return render(request, 'appartement.html')
        #   ___________
def garantie(request):
    return render(request, 'garantie.html')
        #   ____________
def locataire(request):
    return render(request, 'locataire.html')
        #   ____________
def personnel(request):
    return render(request, 'personnel.html')
        #   ____________
def proprietaire(request):
    return render(request, 'proprietaire.html')

        # ________En_