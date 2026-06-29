from django.urls import path
from . import views

urlpatterns = [
    # Agences
    path('agences/', views.AgenceListView.as_view(), name='agences'),
    path('agences/ajouter/', views.AgenceCreateView.as_view(), name='ajouter_agence'),
    path('agences/<int:pk>/', views.AgenceDetailView.as_view(), name='agence_detail'),
    path('agences/<int:pk>/modifier/', views.AgenceUpdateView.as_view(), name='modifier_agence'),
    path('agences/<int:pk>/supprimer/', views.AgenceDeleteView.as_view(), name='supprimer_agence'),

    # Personnel
    path('personnels/', views.PersonnelListView.as_view(), name='personnels'),
    path('personnels/ajouter/', views.PersonnelCreateView.as_view(), name='ajouter_personnel'),
    path('personnels/<int:pk>/', views.PersonnelDetailView.as_view(), name='personnel_detail'),
    path('personnels/<int:pk>/modifier/', views.PersonnelUpdateView.as_view(), name='modifier_personnel'),
    path('personnels/<int:pk>/supprimer/', views.PersonnelDeleteView.as_view(), name='supprimer_personnel'),

    # Proprietaires
    path('proprietaires/', views.ProprietaireListView.as_view(), name='proprietaires'),
    path('proprietaires/ajouter/', views.ProprietaireCreateView.as_view(), name='ajouter_proprietaire'),
    path('proprietaires/<int:pk>/', views.ProprietaireDetailView.as_view(), name='proprietaire_detail'),
    path('proprietaires/<int:pk>/modifier/', views.ProprietaireUpdateView.as_view(), name='modifier_proprietaire'),
    path('proprietaires/<int:pk>/supprimer/', views.ProprietaireDeleteView.as_view(), name='supprimer_proprietaire'),

    # Clients
    path('clients/', views.ClientListView.as_view(), name='clients'),
    path('clients/ajouter/', views.ClientCreateView.as_view(), name='ajouter_client'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/modifier/', views.ClientUpdateView.as_view(), name='modifier_client'),
    path('clients/<int:pk>/supprimer/', views.ClientDeleteView.as_view(), name='supprimer_client'),

    # Proprietes & Logements
    path('proprietes/', views.ProprieteListView.as_view(), name='proprietes'),
    path('proprietes/ajouter/', views.ProprieteCreateView.as_view(), name='ajouter_propriete'),
    path('proprietes/<int:pk>/', views.ProprieteDetailView.as_view(), name='propriete_detail'),
    path('proprietes/<int:pk>/modifier/', views.ProprieteUpdateView.as_view(), name='modifier_propriete'),
    path('proprietes/<int:pk>/supprimer/', views.ProprieteDeleteView.as_view(), name='supprimer_propriete'),
    
    path('logements/', views.LogementListView.as_view(), name='logements'),
    path('logements/ajouter/', views.LogementCreateView.as_view(), name='ajouter_logement'),
    path('logements/<int:pk>/', views.LogementDetailView.as_view(), name='logement_detail'),
    path('logements/<int:pk>/modifier/', views.LogementUpdateView.as_view(), name='modifier_logement'),
    path('logements/<int:pk>/supprimer/', views.LogementDeleteView.as_view(), name='supprimer_logement'),

    # Types de Propriété
    path('type_proprietes/', views.TypeProprieteListView.as_view(), name='type_proprietes'),
    path('type_proprietes/ajouter/', views.TypeProprieteCreateView.as_view(), name='ajouter_type_propriete'),
    path('type_proprietes/<int:pk>/', views.TypeProprieteDetailView.as_view(), name='type_propriete_detail'),
    path('type_proprietes/<int:pk>/modifier/', views.TypeProprieteUpdateView.as_view(), name='modifier_type_propriete'),
    path('type_proprietes/<int:pk>/supprimer/', views.TypeProprieteDeleteView.as_view(), name='supprimer_type_propriete'),

    # Types de Logement
    path('type_logements/', views.TypeLogementListView.as_view(), name='type_logements'),
    path('type_logements/ajouter/', views.TypeLogementCreateView.as_view(), name='type_logement_create'),
    path('type_logements/<int:pk>/', views.TypeLogementDetailView.as_view(), name='type_logement_detail'),
    path('type_logements/<int:pk>/modifier/', views.TypeLogementUpdateView.as_view(), name='type_logement_update'),
    path('type_logements/<int:pk>/supprimer/', views.TypeLogementDeleteView.as_view(), name='type_logement_delete'),

    # Contrats
    path('contrats/', views.ContratListView.as_view(), name='contrats'),
    path('contrats/ajouter/', views.ContratCreateView.as_view(), name='ajouter_contrat'),
    path('contrats/<int:pk>/', views.ContratDetailView.as_view(), name='contrat_detail'),
    path('contrats/<int:pk>/modifier/', views.ContratUpdateView.as_view(), name='modifier_contrat'),
    path('contrats/<int:pk>/supprimer/', views.ContratDeleteView.as_view(), name='supprimer_contrat'),

    # Garanties
    path('garanties/', views.GarantieListView.as_view(), name='garanties'),
    path('garanties/ajouter/', views.GarantieCreateView.as_view(), name='ajouter_garantie'),
    path('garanties/<int:pk>/', views.GarantieDetailView.as_view(), name='garantie_detail'),
    path('garanties/<int:pk>/modifier/', views.GarantieUpdateView.as_view(), name='modifier_garantie'),
    path('garanties/<int:pk>/supprimer/', views.GarantieDeleteView.as_view(), name='supprimer_garantie'),

    # Maintenances
    path('maintenances/', views.MaintenanceListView.as_view(), name='maintenances'),
    path('maintenances/ajouter/', views.MaintenanceCreateView.as_view(), name='ajouter_maintenance'),
    path('maintenances/<int:pk>/', views.MaintenanceDetailView.as_view(), name='maintenance_detail'),
    path('maintenances/<int:pk>/modifier/', views.MaintenanceUpdateView.as_view(), name='modifier_maintenance'),
    path('maintenances/<int:pk>/supprimer/', views.MaintenanceDeleteView.as_view(), name='supprimer_maintenance'),

    # API pour JS
    path('api/get_logements/', views.get_logements_for_propriete, name='api_get_logements'),
    path('api/generate-contrat-reference/', views.generate_contrat_reference, name='api_generate_contrat_reference'),
]
