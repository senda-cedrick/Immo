from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.core.exceptions import ValidationError
import os



def validate_file_extension(value):    
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError("Extension non supportée")

class Profile(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    # email, username et password sont déjà dans AbstractUser.
    # On peut surcharger l'email pour le rendre unique et obligatoire.
    email = models.EmailField(unique=True, null=False, blank=False)
    noms = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    finger_print = models.TextField(null=True, blank=True)
    photo_url = models.ImageField(upload_to='photos/', blank=True, null=True, validators=[validate_file_extension])

    # L'email est maintenant requis pour la création d'un utilisateur.
    REQUIRED_FIELDS = ['noms']
    EMAIL_FIELD = 'email'

    @property
    def is_manager(self):
        """Vérifie si l'utilisateur a le profil 'Manager'."""
        return self.profile and self.profile.name == 'Manager'

    @property
    def is_agent(self):
        """Vérifie si l'utilisateur a le profil 'Agent'."""
        return self.profile and self.profile.name == 'Agent'

    @property
    def is_proprietaire(self):
        """Vérifie si l'utilisateur a le profil 'Proprietaire'."""
        return self.profile and self.profile.name == 'Proprietaire'


class LogUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_synchronize = models.BooleanField(default=False)

    def __str__(self):
        name = self.user.username or ""
        return name
