from django.shortcuts import render

# Create your views here.

def home(request):
    
    return render(request, 'index.html')

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

