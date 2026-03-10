from django.contrib import admin

# Register your models here.
from .models import Agence, Personnel, Locataire, Propriete

admin.site.register(Agence)
admin.site.register(Personnel)
admin.site.register(Locataire)
admin.site.register(Propriete)