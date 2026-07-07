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
    ProprieteImage,
    LogementImage,
)


class ProprieteImageInline(admin.TabularInline):
    model = ProprieteImage
    extra = 1
    readonly_fields = ('uploaded_at',)


class LogementImageInline(admin.TabularInline):
    model = LogementImage
    extra = 1
    readonly_fields = ('uploaded_at',)


@admin.register(ProprieteImage)
class ProprieteImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'propriete', 'caption', 'is_primary', 'uploaded_at')
    list_filter = ('is_primary',)
    search_fields = ('propriete__adresse', 'caption')

    def save_model(self, request, obj, form, change):
        # If this image is set as primary, unset others for the same propriete
        super().save_model(request, obj, form, change)
        if obj.is_primary:
            # unset others
            obj.propriete.images.exclude(id=obj.id).update(is_primary=False)
            # update main_image on Propriete
            obj.propriete.main_image = obj.image
            obj.propriete.save()
        else:
            # If no primary exists for the propriete, optionally set this as main if none
            if not obj.propriete.main_image:
                # set the first available image as main
                primary = obj.propriete.images.filter(is_primary=True).first() or obj
                obj.propriete.main_image = primary.image
                obj.propriete.save()

    def delete_model(self, request, obj):
        prop = obj.propriete
        was_primary = obj.is_primary
        super().delete_model(request, obj)
        if was_primary:
            # choose another primary if exists
            new = prop.images.order_by('-uploaded_at').first()
            if new:
                new.is_primary = True
                new.save()
                prop.main_image = new.image
            else:
                prop.main_image = None
            prop.save()


@admin.register(LogementImage)
class LogementImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'logement', 'caption', 'is_primary', 'uploaded_at')
    list_filter = ('is_primary',)
    search_fields = ('logement__identifiant', 'caption')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.is_primary:
            obj.logement.images.exclude(id=obj.id).update(is_primary=False)
            obj.logement.main_image = obj.image
            obj.logement.save()
        else:
            if not obj.logement.main_image:
                primary = obj.logement.images.filter(is_primary=True).first() or obj
                obj.logement.main_image = primary.image
                obj.logement.save()

    def delete_model(self, request, obj):
        log = obj.logement
        was_primary = obj.is_primary
        super().delete_model(request, obj)
        if was_primary:
            new = log.images.order_by('-uploaded_at').first()
            if new:
                new.is_primary = True
                new.save()
                log.main_image = new.image
            else:
                log.main_image = None
            log.save()


@admin.register(Propriete)
class ProprieteAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_propriete', 'ville', 'statut', 'proprietaire')
    inlines = [ProprieteImageInline]


@admin.register(Logement)
class LogementAdmin(admin.ModelAdmin):
    list_display = ('id', 'identifiant', 'propriete', 'statut')
    inlines = [LogementImageInline]


admin.site.register(Agence)
admin.site.register(Personnel)
admin.site.register(Proprietaire)
admin.site.register(Client)
admin.site.register(Contrat)
admin.site.register(Garantie)
admin.site.register(TypePropriete)
admin.site.register(Maintenance)