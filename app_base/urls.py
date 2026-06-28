from django.urls import path
from . import views

urlpatterns = [
    # Redirections pour compatibilité (anciens noms)
    path('logements/', views.LogementListView.as_view(), name='appartements'),
    path('logement/<int:pk>/', views.LogementDetailView.as_view(), name='appartement_detail'),
    path('logement/add/', views.LogementCreateView.as_view(), name='ajouter_appartement'),
    path('logement/<int:pk>/edit/', views.LogementUpdateView.as_view(), name='modifier_appartement'),
    path('logement/<int:pk>/delete/', views.LogementDeleteView.as_view(), name='supprimer_appartement'),
    path('locataires/', views.ClientListView.as_view(), name='locataires'),
    path('locataire/<int:pk>/', views.ClientDetailView.as_view(), name='locataire'),
    
    # Agences
    path('agences/', views.AgenceListView.as_view(), name='agences'),
    path('agence/<int:pk>/', views.AgenceDetailView.as_view(), name='agence_detail'),
    path('agence/add/', views.AgenceCreateView.as_view(), name='ajouter_agence'),
    path('agence/<int:pk>/edit/', views.AgenceUpdateView.as_view(), name='modifier_agence'),
    path('agence/<int:pk>/delete/', views.AgenceDeleteView.as_view(), name='supprimer_agence'),

    # Personnel
    path('personnels/', views.PersonnelListView.as_view(), name='personnels'),
    path('personnel/<int:pk>/', views.PersonnelDetailView.as_view(), name='personnel_detail'),
    path('personnel/add/', views.PersonnelCreateView.as_view(), name='ajouter_personnel'),
    path('personnel/<int:pk>/edit/', views.PersonnelUpdateView.as_view(), name='modifier_personnel'),
    path('personnel/<int:pk>/delete/', views.PersonnelDeleteView.as_view(), name='supprimer_personnel'),

    # Types de propriété
    path('type-proprietes/', views.TypeProprieteListView.as_view(), name='type_proprietes'),
    path('type-propriete/<int:pk>/', views.TypeProprieteDetailView.as_view(), name='type_propriete_detail'),
    path('type-propriete/add/', views.TypeProprieteCreateView.as_view(), name='ajouter_type_propriete'),
    path('type-propriete/<int:pk>/edit/', views.TypeProprieteUpdateView.as_view(), name='modifier_type_propriete'),
    path('type-propriete/<int:pk>/delete/', views.TypeProprieteDeleteView.as_view(), name='supprimer_type_propriete'),

    # Propriétés
    path('proprietes/', views.ProprieteListView.as_view(), name='proprietes'),
    path('propriete/<int:pk>/', views.ProprieteDetailView.as_view(), name='propriete_detail'),
    path('propriete/add/', views.ProprieteCreateView.as_view(), name='ajouter_propriete'),
    path('propriete/<int:pk>/edit/', views.ProprieteUpdateView.as_view(), name='modifier_propriete'),
    path('propriete/<int:pk>/delete/', views.ProprieteDeleteView.as_view(), name='supprimer_propriete'),

    # Clients (anciennement Locataires)
    path('clients/', views.ClientListView.as_view(), name='clients'),
    path('client/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('client/add/', views.ClientCreateView.as_view(), name='ajouter_client'),
    path('client/<int:pk>/edit/', views.ClientUpdateView.as_view(), name='modifier_client'),
    path('client/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='supprimer_client'),

    # Proprietaires
    path('proprietaires/', views.ProprietaireListView.as_view(), name='proprietaires'),
    path('proprietaire/<int:pk>/', views.ProprietaireDetailView.as_view(), name='proprietaire_detail'),
    path('proprietaire/add/', views.ProprietaireCreateView.as_view(), name='ajouter_proprietaire'),
    path('proprietaire/<int:pk>/edit/', views.ProprietaireUpdateView.as_view(), name='modifier_proprietaire'),
    path('proprietaire/<int:pk>/delete/', views.ProprietaireDeleteView.as_view(), name='supprimer_proprietaire'),

    # Contrats
    path('contrats/', views.ContratListView.as_view(), name='contrats'),
    path('contrat/<int:pk>/', views.ContratDetailView.as_view(), name='contrat_detail'),
    path('contrat/add/', views.ContratCreateView.as_view(), name='ajouter_contrat'),
    path('contrat/<int:pk>/edit/', views.ContratUpdateView.as_view(), name='modifier_contrat'),
    path('contrat/<int:pk>/delete/', views.ContratDeleteView.as_view(), name='supprimer_contrat'),

    # Garanties
    path('garanties/', views.GarantieListView.as_view(), name='garanties'),
    path('garantie/add/', views.GarantieCreateView.as_view(), name='ajouter_garantie'),
    path('garantie/<int:pk>/edit/', views.GarantieUpdateView.as_view(), name='modifier_garantie'),

    # Logements (nouveau nommage cohérent)
    path('logements/', views.LogementListView.as_view(), name='logements'),
    path('logement/<int:pk>/', views.LogementDetailView.as_view(), name='logement_detail'),

]
