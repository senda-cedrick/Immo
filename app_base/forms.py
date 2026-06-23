from django import forms
from .models import Agence

class AgenceForm(forms.ModelForm):
    class Meta:
        model = Agence
        fields = ['nom', 'numero_impot', 'numero_fisc', 'effectif', 'revenu', 'email']