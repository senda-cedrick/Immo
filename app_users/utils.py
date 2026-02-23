import base64
import binascii
from datetime import datetime
import threading
import requests
import pathlib
import json
from app_users.models import LogUser, Profile, User
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.apps import apps

def create_profile():
        profiles = ["agent","locataire", "Propietaire","Manager",]
        e_profiles = Profile.objects.all()
        for p in profiles:
            t_profile = Profile.objects.filter(name=p).first()
            if t_profile is None:
                profile = Profile()
                profile.name = p
                profile.save()
def create_user_profile(user):
        Profile = apps.get_model('app_users', 'Profile') # Charge le modèle sans import direct
        Profile.objects.create(user=user)
class Client:

    ip:str = None
    username:str = None
    password:str = None
    user:str = None
    access:str = None
    refresh:str = None
    header_type: str = "Bearer"
    cred_path: pathlib.Path = pathlib.Path("creds.json")

    def go(self, ip=None, username=None, password=None):
        if ip == None:
            try:
                data = readIP()
            except FileNotFoundError:
                data = None
            ip = data
        self.ip = ip
        self.username = username
        self.password = password

        if self.cred_path.exists():
            try:
                data = json.loads(self.cred_path.read_text())
            except Exception:
                data = None
            if data is None:
                self.clear_tokens()
                self.perform_auth()
            else:
                self.access = data.get('access')
                self.refresh = data.get('refresh')
                self.user = data.get('user')

                token_verified = self.verify_token()
                if not token_verified:
                    refreshed = self.perform_refresh()

                    if not refreshed:
                        self.clear_tokens()
                        self.perform_auth()
                if self.user != self.username:
                    self.clear_tokens()
                    self.perform_auth()
        else:
            self.perform_auth()
    
    def get_headers(self, header_type=None):
        _type = header_type or self.header_type
        token = self.access

        if not token:
            return {}
        return {'Authorization': f"{_type} {token}"}
    
    def perform_auth(self):
        endpoint = f"{self.ip}/api/token/"
        status_code = 400
        try:
            r = requests.post(endpoint, json={'username':self.username, 'password':self.password})       
            status_code = r.status_code         
        except Exception:
            Exception(f"Connection refused")
        
        if status_code == 200:
            self.write_creds(r.json())   
    
    def write_creds(self, data:dict):
        if self.cred_path is not None:
            self.access = data.get('access')
            self.refresh = data.get('refresh')
            self.user = data.get('user')
            if self.access and self.refresh and self.user:
                self.cred_path.write_text(json.dumps(data))
    
    def verify_token(self):
        data = {
            "token": f"{self.access}"
        }
        endpoint = f"{self.ip}/api/token/verify/"
        status_code = 400
        try:
            r = requests.post(endpoint, json=data)   
            status_code = r.status_code           
        except requests.exceptions.ConnectionError:
            Exception(f"Connection refused")
        
        return status_code == 200
    
    def clear_tokens(self):
        self.access = None
        self.refresh = None
        self.user = None
        if self.cred_path.exists():
            self.cred_path.unlink()
    
    def perform_refresh(self):
        headers = self.get_headers()
        data = {
            "refresh": f"{self.refresh}"
        }
        endpoint = f"{self.ip}/api/token/refresh/"
        status_code = 400
        try: 
            r = requests.post(endpoint, json=data, headers=headers)
            status_code = r.status_code
        except Exception:
            Exception("Connexion refusée")
        if status_code != 200:
            self.clear_tokens()
            return False
        refresh_data = r.json()
        if not 'access' in refresh_data:
            self.clear_tokens()
            return False
        stored_data = {
            'access': refresh_data.get('access'),
            'refresh': self.refresh
        }
        self.write_creds(stored_data)
        return True

    def get_data(self, endpoint=None):
        headers = self.get_headers()
        endpoint = f"{self.ip}/{endpoint}"
        status_code = 400
        try:
            r = requests.get(endpoint, headers=headers)
            status_code = r.status_code
        except Exception:
            Exception("Requete incomplete")
        
        data = None
        if status_code == 200: 
            data = r.json()
        return data
    
    def post_data(self, data, endpoint=None):
        _type = self.header_type
        token = self.access
        headers = {
            "Authorization": f"{_type} {token}",
            "Content-Type":"application/json",
            "Accept":"application/json"
        }
        endpoint = f"{self.ip}/{endpoint}"
        status_code = 400
        try:
            r = requests.post(endpoint,json=data,headers=headers)
            status_code = r.status_code
        except Exception:
            Exception("Requete incomplete")
        
        data = None
        if status_code != 400: 
            data = r.json()
        
        return data
    
    def post_data_form(self, data, endpoint=None):
        _type = self.header_type
        token = self.access
        headers = {
            "Authorization": f"{_type} {token}",
            "Content-Type":"application/json",
            "Accept":"application/json"
        }
        endpoint = f"{self.ip}/{endpoint}"
        
        status_code = 400
        try:
            r = requests.post(endpoint,data=data,headers=headers)
            status_code = r.status_code
        except Exception:
            Exception("Requete incomplete")
        
        data = None
        if status_code != 400: 
            data = r.json()
        
        return data
    
    def get_user(self):
        return self.get_data("api/user/")
    # app_users/utils.py

def pdf_decorator(pdfname="pdf_decorator.pdf"):
    """Décorateur temporaire pour éviter l'erreur d'import"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator
    
    
