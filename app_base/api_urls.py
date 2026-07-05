from django.urls import path
from . import views

urlpatterns = [
    # API pour Proprietaire (JWT)
    path('proprietaire/dashboard/', views.ProprietaireDashboardAPI.as_view(), name='api_proprietaire_dashboard'),
    path('proprietaire/proprietes/', views.ProprietaireProprietesAPI.as_view(), name='api_proprietaire_proprietes'),
    path('proprietaire/contrats/', views.ProprietaireContratsAPI.as_view(), name='api_proprietaire_contrats'),
    path('proprietaire/contrats/<int:contrat_id>/', views.ProprietaireContratDetailAPI.as_view(), name='api_proprietaire_contrat_detail'),
    path('proprietaire/paiements/', views.ProprietairePaiementsAPI.as_view(), name='api_proprietaire_paiements'),
    path('proprietaire/paiements/<int:paiement_id>/', views.ProprietairePaiementDetailAPI.as_view(), name='api_proprietaire_paiement_detail'),

    # API pour Client (JWT)
    path('client/dashboard/', views.ClientDashboardAPI.as_view(), name='api_client_dashboard'),
    path('client/contrats/', views.ClientContratsAPI.as_view(), name='api_client_contrats'),
    path('client/contrats/<int:contrat_id>/', views.ClientContratDetailAPI.as_view(), name='api_client_contrat_detail'),

    # API pour JS (utilitaires)
    path('get_logements/', views.get_logements_for_propriete, name='api_get_logements'),
    path('generate-contrat-reference/', views.generate_contrat_reference, name='api_generate_contrat_reference'),
]
