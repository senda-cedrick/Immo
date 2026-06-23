from django.contrib import admin
from app_users.models import User
from django.contrib import admin
from app_base.models import Locataire
from app_users.models import LogUser, Profile, User

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','noms','email','profile','is_active')

class LogAdmin(admin.ModelAdmin):
    list_display = ('id','user','action','created_at')

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
