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
import base64

from rest_framework.permissions import IsAuthenticated
from app_users.utils import create_profile
from django.contrib.auth import login,authenticate,logout
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import MultiPartParser, FormParser

from app_users.models import LogUser, Profile, User
from app_users.serializers import UserSerializer


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
    listuser= User.objects.order_by('-date_joined')
    profiles = Profile.objects.all()
    ctrep =[]

    if request.method == "POST":
        rech = request.POST['rech']
        p = Paginator(listuser.filter(noms__contains=rech) | listuser.filter(profile__name__contains=rech) , 10)
        page = request.GET.get('page') 
        pages =p.get_page(page)
    else:
        p = Paginator(listuser, 20)
        page = request.GET.get('page') 
        pages =p.get_page(page)       
    
    user = User.objects.get(pk=request.user.id)
    LogUser(user=user,action="Affichage de la liste des utilisateurs")

    ctx = {
        'users' : listuser,
        'pages' : pages,
        'profiles':profiles,
        'compte' : len(listuser),
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
        if user.profile.id == 1 :
            agent.append(user)
        if user.profile.id == 2 :
            propietaire.append(user)
        if user.profile.id == 3 :
            locataire.append(user)
        if user.profile.id == 4 :
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

# ---Page ---
def addusers(request):
    return render(request, 'app_user/ajouter_user.html')
#--- page/----

@login_required
def adduser(request,):

    if request.method == 'POST':
        photo = request.FILES.get("image_url")
        password  = request.POST.get("password")
        username = request.POST.get("username")
        noms = request.POST.get("noms")
        id_profile = request.POST.get("profile")
        profile = Profile.objects.get(pk=id_profile)

        rs_username = User.objects.filter(username=username)
        try:
            if len(rs_username)>0:
                messages.warning(request,"Ce nom utilisateur existe déjà")
                return redirect('/user/users') 
            else:
                user = User(
                    #email = email,
                    username = username.upper(),
                    noms = noms.upper(),
                    profile = profile,
                    photo_url = photo,
                    is_active = True
                )   
            user.set_password(password)
            user.save()
        except:
            pass

        owner = User.objects.get(pk=request.user.id)
        LogUser(user=owner,action=f"Ajout d'un utilisateur {user.noms} ")
        return HttpResponseRedirect('/user/users/')

    return render(request,'app_user/ajouter_user.html',{'profiles':profile})

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

def update_user(request, myid):
    user  = User.objects.get(id = myid)
    id_profile = request.POST.get("profile")
    #email = request.POST.get("email")
    username = request.POST.get("username")
    noms = request.POST.get("noms")
    profile = Profile.objects.get(pk=id_profile)
    
    user.profile = profile
    #user.email = email
    user.usename = username
    user.noms = noms
    user.save()
    
    return HttpResponseRedirect('/user/users/')

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

def generer_user_motdepasse(request,myid): 
    user  = User.objects.get(id = myid)
    user.set_password("oye@2026") 
    user.save()

    return HttpResponseRedirect('/user/')

def page_modifpassword(request):
    
    return render(request,'app_user/modifierMotPasse.html')
 
def active_user(request, myid):
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

def update_profile_user(request, myid):
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
