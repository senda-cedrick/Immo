from django import forms
from .models import Agence, Personnel, TypePropriete

class AgenceForm(forms.ModelForm):
    class Meta:
        model = Agence
        fields = ['nom', 'numero_impot', 'numero_fisc', 'effectif', 'revenu', 'email', 'active']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Agence Centre-Ville'}),
            'numero_impot': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: A123456'}),
            'numero_fisc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: F123456'}),
            'effectif': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 15'}),
            'revenu': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 45000000'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ex: contact@agence.cd'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = ['noms', 'sexe', 'role', 'status', 'agence', 'email']
        widgets = {
            'noms': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Jean Dupont'}),
            'sexe': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Comptable'}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Actif'}),
            'agence': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ex: j.dupont@immo.cd'}),
        }

class TypeProprieteForm(forms.ModelForm):
    class Meta:
        model = TypePropriete
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Maison'}),
        }