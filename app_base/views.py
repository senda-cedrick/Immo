from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib import messages
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
def ajouter_agence(request):
    # Étape 1 : On vérifie si l'utilisateur a cliqué sur le bouton "Ajouter" (Requête POST)
    if request.method == 'POST':
        
        # Étape 2 : On remplit le formulaire Django avec les données du dictionnaire request.POST
        # Django va chercher request.POST['nom'], request.POST['numero_impot'], etc.
        form = AgenceForm(request.POST)
        
        # Étape 3 : Validation automatique des données
        # Django vérifie si l'email est correct, si l'effectif est bien un nombre, etc.
        if form.is_valid():
            
            # Étape 4 : Enregistrement dans PostgreSQL
            # La méthode .save() crée une ligne dans votre table PostgreSQL et valide la transaction
            form.save()
            
            # (Optionnel) Ajouter un message de succès pour l'utilisateur
            messages.success(request, "L'agence a été ajoutée avec succès !")
            
            # Étape 5 : Redirection vers la page de liste des agences
            return redirect('agences') 
        
        else:
            # Si le formulaire n'est pas valide, Django y attache des erreurs automatiquement
            messages.error(request, "Une erreur est survenue. Veuillez vérifier les champs.")
            
    else:
        # Si la requête est un GET (l'utilisateur arrive juste sur la page), on affiche un formulaire vide
        form = AgenceForm()
        
    # Étape 6 : On renvoie le template avec le formulaire (qu'il soit vide ou qu'il contienne des erreurs)
    return render(request, 'app_base/agence.html', {'form': form})

        # ________En_