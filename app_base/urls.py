from django.urls import path
from . import views
from immo_travel.views import home_views


urlpatterns = [
    path('', home_views.HomeView.as_view(), name='home'),
    
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

    # Pages statiques
    path('garanties/', views.garanties, name='garanties'),
    path('appartements/', views.appartements, name='appartements'),
    path('locataires/', views.locataires, name='locataires'),
    path('proprietaires/', views.proprietaires, name='proprietaires'),
]