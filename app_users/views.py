from django.shortcuts import render
from datetime import datetime
from importlib.metadata import files
from app_users.utils import pdf_decorator
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
import base64
import secrets
import string

from rest_framework.permissions import IsAuthenticated
from app_users.utils import create_profile, Client
from django.contrib.auth import login,authenticate,logout
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from rest_framework.parsers import MultiPartParser, FormParser

from app_users.models import LogUser, Profile, User
from app_users.serializers import UserSerializer
from .forms import ProfileForm, UserCreationForm, UserChangeForm


class RegisterViewset(ModelViewSet):
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)
    queryset = User.objects.all()

class ApiTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

class ApiToken(TokenObtainPairView):
    serializer_class = ApiTokenSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        user = self.user
        data['user'] = user.username

        if user.profile is None or user.profile.id == 4:
            if user.is_superuser:
                data['refresh'] = str(refresh)
                data['access'] = str(refresh.access_token)
                LogUser(user=user,action="Connexion distante du Manager ou Admin").save()
                return data
            else:
                data['refresh'] = str(refresh)
                data['access'] = str(refresh.access_token)
                LogUser(user=user,action="Connexion distante du Manager").save()
                return data
        elif user.profile.id == 2 or user.profile.id == 3 :
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            LogUser(user=user,action="Connexion distante").save()
            return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@login_required
def listeusers(request):
    """
    Affiche la liste des utilisateurs, avec pagination et possibilité de recherche.
    La recherche s'effectue via un paramètre GET 'q'.
    """
    users_list = User.objects.select_related('profile').order_by('-date_joined')
    profiles = Profile.objects.all()
    search_query = request.GET.get('q', '')

    if search_query:
        users_list = users_list.filter(
            Q(noms__icontains=search_query) | 
            Q(username__icontains=search_query) | 
            Q(profile__name__icontains=search_query)
        )

    paginator = Paginator(users_list, 15)  # 15 utilisateurs par page
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)

    # Créer une chaîne de caractères lisible pour le nombre d'utilisateurs
    nombre_utilisateurs = paginator.count
    if nombre_utilisateurs == 1:
        compte_str = "1 utilisateur"
    else:
        compte_str = f"{nombre_utilisateurs} utilisateurs"

    # Ajouter une classe CSS pour la couleur du statut
    for user in pages:
        if user.is_active:
            user.statut_class = 'badge badge-success'
        else:
            user.statut_class = 'badge badge-danger'

    LogUser.objects.create(user=request.user, action="Affichage de la liste des utilisateurs")

    ctx = {
        'pages': pages,
        'profiles': profiles,
        'compte_str': compte_str,
        "lutilisateur" : 'active'
    }
    return render(request,'app_user/users.html',ctx)

@pdf_decorator(pdfname="Utilisateurs.pdf")
def print_users(request):
    users = User.objects.filter(is_active=True)
    profiles = Profile.objects.all()

    user = User.objects.get(pk=request.user.id)
    LogUser(user=user,action="Impression de la liste des utilisateurs")

    agent = []
    propietaire = []
    locataire = []
    managers = []
    data_profiles = []
    
    for user in users:
        if user.is_agent:
            agent.append(user)
        if user.is_proprietaire:
            propietaire.append(user)
        if user.profile.id == 3 :
            locataire.append(user)
        if user.is_manager:
            managers.append(user)
    
    data_profiles.append(agent)
    data_profiles.append(propietaire)
    data_profiles.append(locataire)
    data_profiles.append(managers)

    ctx = {
        "agents" : agent,
        "propietaires" : propietaire,
        "locataires" : locataire,
        "managers" : managers,
        "date" : datetime.today()
    }    
    return render(request, "app_report/print_users.html", ctx)

@login_required
def logusers(request):
    logusers= LogUser.objects.order_by('-id')
   
    if request.method == "POST":
        rech = request.POST['rech']

        p = Paginator(logusers.filter(user__noms__contains=rech) , 10)
        page = request.GET.get('page') 
        pages =p.get_page(page)

    else:
        p = Paginator(logusers, 10)
        page = request.GET.get('page') 
        pages =p.get_page(page)

    ctx = {
        'compte' : len(logusers),
        'pages' : pages,
        "lloguser" : 'active'
    }

    return render(request,'app_user/logusers.html',ctx)

def edituser(request, myid):

    sel_user = User.objects.get(id = myid)
    liste_user = User.objects.all()

    p = Paginator(User.objects.all(), 5)
    page = request.GET.get('page')
    pages =p.get_page(page)
    profiles = Profile.objects.all()

    ctx = {
        'sel_user': sel_user,
        'users': liste_user,
        'pages' : pages,
        'nombre' : len(liste_user),
        'profiles': profiles
    }
    return render(request,'app_user/users.html',ctx)

@login_required
def update_user_motdepasse(request):
    user  = User.objects.get(id = request.user.id)
    passew = request.POST.get("pass")
    cpass = request.POST.get("cpass")

    if   passew == cpass: 
        user.set_password(passew) 
        user.save()
       
    else:
        messages.warning(request,"mot de passe incompatible")
        return redirect('/user/page_modifpassword')
        

        
    return HttpResponseRedirect('/user/login/')

@login_required
def generer_user_motdepasse(request,myid): 
    """Génère un mot de passe aléatoire sécurisé pour un utilisateur."""
    user  = User.objects.get(id = myid)
    # Générer un mot de passe aléatoire de 12 caractères
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    new_password = ''.join(secrets.choice(alphabet) for _ in range(12))
    user.set_password(new_password) 
    user.save()
    
    LogUser.objects.create(user=request.user, action=f"Réinitialisation du mot de passe de {user.noms}")
    messages.success(request, f"Mot de passe réinitialisé avec succès pour {user.noms}")
    return redirect('/user/users/')

def page_modifpassword(request):
    
    return render(request,'app_user/modifierMotPasse.html')
 
@login_required
def active_user(request, myid):
       """Active ou désactive un utilisateur. Réservé aux superusers."""
       if not request.user.is_superuser and not request.user.is_manager:
           messages.warning(request, "Seuls les administrateurs peuvent activer/désactiver des utilisateurs")
           return redirect('/user/users/')
       user  = User.objects.get(id = myid)   
       if user.is_active == False:    
          user.is_active = True
          user.save()
       else :
          user.is_active = False
          user.save()

       return HttpResponseRedirect('/user/users/')

class LoginPageView(View):
    template_name = 'app_user/login.html'
    #form_class = forms.LoginForm

    def get(self, request):
        message = ''
        return render(request, self.template_name, context={'message': message})
        
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            username=username,
            password=password,
        )
        if user is not None:
            login(request, user)
            return redirect('/')
        message = 'Identifiants invalides.'
        return render(request, self.template_name, context={'message': message})

def logout_user(request):
    logout(request)
    return redirect('login')

def edit_profile_user(request, myid):

    sel_user= User.objects.get(id = myid)
    liste_user = User.objects.all()

    p = Paginator(User.objects.all(), 10)
    page = request.GET.get('page')
    pages =p.get_page(page)
    profiles = Profile.objects.all()

    ctx = {
        'sel_user_profile': sel_user,
        'users': liste_user,
        'pages' : pages,
        'nombre' : len(liste_user),
        'profiles': profiles
    }
    return render(request,'app_user/users.html',ctx)

@login_required
def update_profile_user(request, myid):
    """Met à jour le profil d'un utilisateur."""
    if not request.user.is_superuser and not request.user.is_manager:
        messages.warning(request, "Vous n'avez pas la permission de modifier ce profil")
        return redirect('/user/users/')
    user  = User.objects.get(id = myid)
    id_profile = request.POST.get("profile")
    profile = Profile.objects.get(pk=id_profile)
    user.profile = profile
    user.save()
    
    return HttpResponseRedirect('/user/users/')

def rechercher_user(request):

    if request.method == "POST":
        rech = request.POST['rech']

        users = User.objects.filter(noms__contains=rech)
        

        return render(request,'app_user/users.html',{'rech':rech,
        'users_rech' : users})

    else:
        return render(request,'app_user/users.html')

class UserAPIViewset(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        id_user = self.request.user.id
        user = User.objects.get(pk=id_user)

        try:
            profile = user.profile.id
        except Profile.DoesNotExist:
            profile = None
        
        querySet = None
        if profile == 2 or profile == 3 or user.is_superuser:    
            querySet = User.objects.filter(id=user.id)

        return querySet


def login_remote(request):
    create_profile()

    if request.method == 'POST':
        
        ip = request.POST.get("ip")
        password = request.POST.get("password")
        username = request.POST.get("username")

        client = Client()
        client.go(ip,username,password)

        user_data = client.get_user()
        
        if type(user_data) == list and len(user_data)>0:
            userd = user_data[0]

            user = User(
                id = userd.get('id'),
                email = userd.get('email'),
                username = userd.get('username'),
                noms = userd.get('noms'),
                profile_id = userd.get('profile'),
                finger_print = userd.get('finger_print'),
                photo_url = userd.get('photo_url'),
                is_active = True
            )   
            user.set_password(password)
            if not User.objects.filter(username=username).exists():
                user.save()
            user = authenticate(
                username=username,
                password=password,
            )
                                       
            login(request, user)
            LogUser(user=user,action="Première connexion et récupération des données sur pc").save()
                
            return redirect('/')
        
    return HttpResponseRedirect('/')


# Create your views here.

class ManagerRequiredMixin(UserPassesTestMixin):
    """
    Mixin pour restreindre l'accès aux managers et super-utilisateurs.
    """
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff or (self.request.user.profile and self.request.user.profile.name == 'Manager')

    def handle_no_permission(self):
        messages.error(self.request, "Accès refusé. Vous n'avez pas les permissions nécessaires.")
        return redirect('home')


# --- Vues pour la gestion des profils (CRUD) ---

class UserCreateView(LoginRequiredMixin, ManagerRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'app_user/user_form.html'
    success_url = reverse_lazy('users')
    extra_context = {'action': 'Ajouter'}

    def form_valid(self, form):
        messages.success(self.request, "L'utilisateur a été créé avec succès.")
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, ManagerRequiredMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'app_user/user_form.html'
    success_url = reverse_lazy('users')
    extra_context = {'action': 'Modifier'}

    def form_valid(self, form):
        messages.success(self.request, "L'utilisateur a été mis à jour avec succès.")
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin, ManagerRequiredMixin, DeleteView):
    model = User
    template_name = 'app_user/user_confirm_delete.html'
    success_url = reverse_lazy('users')
    success_message = "L'utilisateur a été supprimé avec succès."

class ProfileListView(LoginRequiredMixin, ManagerRequiredMixin, ListView):
    model = Profile
    template_name = 'app_user/profile_list.html'
    context_object_name = 'profiles'
    paginate_by = 10

class ProfileCreateView(LoginRequiredMixin, ManagerRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'app_user/profile_form.html'
    success_url = reverse_lazy('profile_list')
    extra_context = {'action': 'Ajouter'}

class ProfileUpdateView(LoginRequiredMixin, ManagerRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'app_user/profile_form.html'
    success_url = reverse_lazy('profile_list')
    extra_context = {'action': 'Modifier'}

class ProfileDeleteView(LoginRequiredMixin, ManagerRequiredMixin, DeleteView):
    model = Profile
    template_name = 'app_user/profile_confirm_delete.html'
    success_url = reverse_lazy('profile_list')
