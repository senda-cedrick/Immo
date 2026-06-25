from django import forms
from .models import Profile, User
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm

class ProfileForm(forms.ModelForm):
    """
    Formulaire pour la création et la mise à jour des profils.
    """
    name = forms.CharField(label="Nom du profil", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Manager, Agent, ...'}))
    class Meta:
        model = Profile
        fields = ['name']

class UserCreationForm(BaseUserCreationForm):
    """
    Formulaire pour la création d'utilisateurs.
    """
    photo_url = forms.ImageField(label="Photo", required=False)
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('username', 'noms', 'email', 'profile', 'photo_url')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class UserChangeForm(BaseUserChangeForm):
    """
    Formulaire pour la modification d'utilisateurs.
    """
    photo_url = forms.ImageField(label="Photo", required=False, widget=forms.ClearableFileInput)
    password = None # On ne gère pas le mot de passe ici
    class Meta:
        model = User
        fields = ('username', 'noms', 'email', 'profile', 'photo_url', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'