from django.urls import path
from . import views
from immo_travel.views import home_views
from immo_travel.views.agence_views import AgenceCreateView, AgenceListView,AgenceDetailView, ListAgence


urlpatterns = [
    path('', home_views.HomeView.as_view(), name='home'), # Cette route captera le http://127.0.0.1:8000/
    # Page show 
    path('agence/', views.agences, name='agences'),
    path('lagence/',  ListAgence, name='lagences'),
    path("agences/", AgenceListView.as_view(), name="agences"),
    path('garanties/', views.garanties, name='garanties'),
    path('appartements/', views.appartements, name='appartements'),
    path('locataires/', views.locataires, name='locataires'),
    path('personnels/', views.personnels, name='personnels'),
    path('proprietaires/', views.proprietaires, name='proprietaires'),
    
    # --- / -----

]

