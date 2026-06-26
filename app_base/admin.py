from django.contrib import admin

# Register your models here.
from .models import (
    Agence,
    Personnel,
    Proprietaire,
    Client,
    TypePropriete,
    Propriete,
    Logement,
    Contrat,
    Maintenance,
    Garantie,
)

admin.site.register(Agence)
admin.site.register(Personnel)
admin.site.register(Proprietaire)
admin.site.register(Client)
admin.site.register(Propriete)
admin.site.register(Logement)
admin.site.register(Contrat)
admin.site.register(Garantie)
admin.site.register(TypePropriete)
admin.site.register(Maintenance)