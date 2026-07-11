from django import forms
from .models import (
    Agence, Personnel, TypePropriete, TypeLogement, Propriete, Logement, Client, Proprietaire,
    Contrat, Garantie, Maintenance, ProprieteImage
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
        fields = ['user', 'telephone', 'adresse']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+243...'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['user', 'agence', 'telephone', 'adresse']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'agence': forms.Select(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+243...'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TypeProprieteForm(forms.ModelForm):
    class Meta:
        model = TypePropriete
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Maison'}),
        }

class TypeLogementForm(forms.ModelForm):
    class Meta:
        model = TypeLogement
        fields = ['nom', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Studio'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description du type de logement'}),
        }

class ProprieteForm(forms.ModelForm):
    class Meta:
        model = Propriete
        fields = ['agence', 'proprietaire', 'type_propriete', 'adresse', 'ville', 'superficie', 'nb_pieces', 'description', 'statut', 'agent', 'main_image']
        widgets = {
            'type_propriete': forms.Select(attrs={'class': 'form-control'}),
            'ville': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Kinshasa/Gombe'}),
            'agent': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description de la propriété'}),
            'surface': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 250'}),
            'main_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
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
        widgets = {
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: LOC-2024-001'}),
            'type': forms.Select(attrs={'class': 'form-control', 'id': 'id_type'}),
            'propriete': forms.Select(attrs={'class': 'form-control'}),
            'logement': forms.Select(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'agent': forms.Select(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
        }

class GarantieForm(forms.ModelForm):
    class Meta:
        model = Garantie
        fields = ['contrat', 'montant', 'type_garantie', 'statut', 'date_constitution', 'notes']
        widgets = {
            'contrat': forms.Select(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'type_garantie': forms.Select(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'date_constitution': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Conditions spécifiques ou notes...'}),
        }

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = '__all__'
        widgets = {
            'propriete': forms.Select(attrs={'class': 'form-control'}),
            'logement': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'prestataire': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Entreprise XYZ'}),
            'cout': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
