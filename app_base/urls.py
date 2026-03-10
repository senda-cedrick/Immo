from django.urls import path
from . import views
from immo_travel.views import home_views

urlpatterns = [
    path('', home_views.HomeView.as_view(), name='home'), # Cette route captera le http://127.0.0.1:8000/
    # Page d'affichage 
    path('agence/', views.agences, name='agences'),
    path('agences/', views.garanties, name='garanties'),
    path('appartements/', views.appartements, name='appartements'),
    path('locataires/', views.locataires, name='locataires'),
    path('personnels/', views.personnels, name='personnels'),
    path('proprietaires/', views.proprietaires, name='proprietaires'),
    
    # --- / -----

]

