from django import forms
from .models import (
    Agence, Personnel, TypePropriete, Propriete, Logement, Client, Proprietaire,
    Contrat, Garantie, Maintenance
)

class AgenceForm(forms.ModelForm):
    class Meta:
        model = Agence
        fields = ['nom', 'adresse', 'telephone', 'email', 'numero_impot', 'numero_fisc', 'active']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Agence Centre-Ville'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+243...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ex: contact@agence.cd'}),
            'numero_impot': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: A123456'}),
            'numero_fisc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: F123456'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = ['user', 'agence', 'sexe', 'telephone']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'agence': forms.Select(attrs={'class': 'form-control'}),
            'sexe': forms.Select(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+243...'}),
        }

class ProprietaireForm(forms.ModelForm):
    class Meta:
        model = Proprietaire
        fields = ['user', 'agence', 'telephone', 'adresse']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['user', 'agence', 'telephone', 'adresse']

class TypeProprieteForm(forms.ModelForm):
    class Meta:
        model = TypePropriete
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Maison'}),
        }

class ProprieteForm(forms.ModelForm):
    class Meta:
        model = Propriete
        fields = ['agence', 'proprietaire', 'type_propriete', 'adresse', 'ville', 'superficie', 'nb_pieces', 'description', 'statut', 'agent']
        widgets = {
            'type_propriete': forms.Select(attrs={'class': 'form-control'}),
            'ville': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Kinshasa/Gombe'}),
            'agent': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description de la propriété'}),
            'surface': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 250'}),
        }

class LogementForm(forms.ModelForm):
    class Meta:
        model = Logement
        fields = ['propriete', 'identifiant', 'surface', 'etage', 'description']
        widgets = {
            'propriete': forms.Select(attrs={'class': 'form-control'}),
            'identifiant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: APT-001'}),
            'surface': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 120'}),
            'etage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 3'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ContratForm(forms.ModelForm):
    class Meta:
        model = Contrat
        fields = '__all__'

class GarantieForm(forms.ModelForm):
    class Meta:
        model = Garantie
        fields = '__all__'
        widgets = {
            'date_apparition': forms.DateInput(attrs={'type': 'date'})
        }

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = '__all__'
