from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.core.exceptions import ValidationError


def validate_file_extension(value):    
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError("Extension non supportée")

class Profile(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    email = models.CharField(max_length=255, unique=True,null=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    noms = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, blank=True, null=True)
    finger_print = models.TextField(null=True, blank=True)
    photo_url = models.ImageField(upload_to='photos/', blank=True, null=True)

    REQUIRED_FIELDS = []

class LogUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_synchronize = models.BooleanField(default=False)

    def __str__(self):
        name = self.user.username or ""
        return name