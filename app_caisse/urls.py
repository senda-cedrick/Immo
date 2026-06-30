from django.urls import path
from . import views

urlpatterns = [
    # Routes pour Caisse
    path('caisses/', views.CaisseListView.as_view(), name='caisses'),
    path('caisses/ajouter/', views.CaisseCreateView.as_view(), name='ajouter_caisse'),
    path('caisses/<int:pk>/modifier/', views.CaisseUpdateView.as_view(), name='modifier_caisse'),
    path('caisses/<int:pk>/supprimer/', views.CaisseDeleteView.as_view(), name='supprimer_caisse'),
]