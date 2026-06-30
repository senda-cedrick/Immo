from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaiementListView.as_view(), name='paiements'),
    path('ajouter/', views.PaiementCreateView.as_view(), name='ajouter_paiement'),
    path('<int:pk>/', views.PaiementDetailView.as_view(), name='paiement_detail'),
    path('<int:pk>/modifier/', views.PaiementUpdateView.as_view(), name='modifier_paiement'),
    path('<int:pk>/supprimer/', views.PaiementDeleteView.as_view(), name='supprimer_paiement'),
]