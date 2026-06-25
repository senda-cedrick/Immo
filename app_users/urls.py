from django.urls import path

from app_users.views import (LoginPageView, active_user, listeusers, logout_user, logusers, page_modifpassword, print_users, rechercher_user, update_user_motdepasse,generer_user_motdepasse, ProfileListView, ProfileCreateView, ProfileUpdateView, ProfileDeleteView, UserCreateView, UserUpdateView, UserDeleteView)
urlpatterns = [
    path('users/', listeusers, name='users'),
    path('users/add/', UserCreateView.as_view(), name='user_add'),
    path('users/edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),

    path('logusers/',  logusers, name='logusers'),

    path('active_user/<int:myid>/', active_user, name="active_user"),
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('recherche/', rechercher_user, name='recherche'),
    path('print-users/', print_users, name="print_users"),
    path('update_user_motdepasse/',update_user_motdepasse, name='update_user_motdepasse'),
    path('generer_user_motdepasse/<int:myid>', generer_user_motdepasse, name='generer_user_motdepasse'),    
    path('page_modifpassword/', page_modifpassword, name='page_modifpassword'),

    # URLs pour la gestion des profils
    path('profiles/', ProfileListView.as_view(), name='profile_list'),
    path('profiles/add/', ProfileCreateView.as_view(), name='profile_add'),
    path('profiles/edit/<int:pk>/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('profiles/delete/<int:pk>/', ProfileDeleteView.as_view(), name='profile_delete'),
   
]