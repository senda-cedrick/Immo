from django.urls import path
    
from app_users.views import LoginPageView, active_user, adduser, edit_profile_user, edituser, listeusers, logout_user, logusers, page_modifpassword, print_users, rechercher_user, update_profile_user, update_user, update_user_motdepasse,generer_user_motdepasse
urlpatterns = [
    path('users/', listeusers, name='users'),
    path('logusers/',  logusers, name='logusers'),
    path('adduser/', adduser, name='adduser'),
    path('edituser/<int:myid>/', edituser, name="edituser"),
    path('edit_profile_user/<int:myid>/',edit_profile_user, name="edit_profile_user"),
    path('update_profile_user/<int:myid>/', update_profile_user, name="update_profile_user"),
    path('update_user/<int:myid>/', update_user, name="update_user"),
    path('active_user/<int:myid>/', active_user, name="active_user"),
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('recherche/', rechercher_user, name='recherche'),
    path('print-users/', print_users, name="print_users"),
    path('update_user_motdepasse/',update_user_motdepasse, name='update_user_motdepasse'),
    path('generer_user_motdepasse/<int:myid>', generer_user_motdepasse, name='generer_user_motdepasse'),    
    path('page_modifpassword/', page_modifpassword, name='page_modifpassword'),

   
]