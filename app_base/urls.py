from django.urls import path
from . import views
from immo_travel.views import home_views
from immo_travel.views.agence_views import AgenceCreateView, AgenceListView,AgenceDetailView, ListAgence


urlpatterns = [
    path('', home_views.HomeView.as_view(), name='home'), # Cette route captera le http://127.0.0.1:8000/
<<<<<<< HEAD
    # Page show 
    path('agence/', views.agences, name='agences'),
    path('lagence/',  ListAgence, name='lagences'),
    path("agences/", AgenceListView.as_view(), name="agences"),
=======
    
    # Page show __
    path('agences/', views.agences, name='agences'),
>>>>>>> 7360511890d14c35120a9860bc29f4f40ab58ac0
    path('garanties/', views.garanties, name='garanties'),
    path('appartements/', views.appartements, name='appartements'),
    path('locataires/', views.locataires, name='locataires'),
    path('personnels/', views.personnels, name='personnels'),
    path('proprietaires/', views.proprietaires, name='proprietaires'),
    
    # --- / -----
    
    #Page Forms_create___
    path('agence/add', views.agence, name='agence'),
    path('appartement/add', views.appartement, name='appartement'),
    path('garantie/add', views.garantie, name='garantie'),
    path('locataire/add', views.locataire, name='locataire'),
    path('personnel/add', views.personnel, name='personnel'),
    path('proprietaire/add', views.proprietaire, name='proprietaire'),

]

