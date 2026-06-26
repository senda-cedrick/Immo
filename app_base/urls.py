from django.urls import path
from . import views
from immo_travel.views import home_views


urlpatterns = [
    path('', home_views.HomeView.as_view(), name='home'), # Cette route captera le http://127.0.0.1:8000/
    
    # Page show __
    path('agences/', views.AgenceListView.as_view(), name='agences'),
    path('agence/<int:pk>/', views.AgenceDetailView.as_view(), name='agence_detail'),
    path('garanties/', views.garanties, name='garanties'),
    path('appartements/', views.appartements, name='appartements'),
    path('locataires/', views.locataires, name='locataires'),
    path('personnels/', views.personnels, name='personnels'),
    path('proprietaires/', views.proprietaires, name='proprietaires'),
    
    # --- / -----
    
    #Page Forms_create___
    path('agence/add/', views.AgenceCreateView.as_view(), name='ajouter_agence'),
    path('agence/<int:pk>/edit/', views.AgenceUpdateView.as_view(), name='modifier_agence'),
    path('agence/<int:pk>/delete/', views.AgenceDeleteView.as_view(), name='supprimer_agence'),
    # path('appartement/add', views.appartement, name='appartement'),
    # path('garantie/add', views.garantie, name='garantie'),
    # path('locataire/add', views.locataire, name='locataire'),
    # path('personnel/add', views.personnel, name='personnel'),
    # path('proprietaire/add', views.proprietaire, name='proprietaire'),

]
