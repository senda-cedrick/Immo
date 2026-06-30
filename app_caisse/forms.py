from django import forms
from .models import Caisse

class CaisseForm(forms.ModelForm):
    class Meta:
        model = Caisse
        fields = ['type_caisse', 'status_caisse', 'cout', 'paiement', 'details']
        widgets = {
            'type_caisse': forms.Select(attrs={'class': 'form-control'}),
            'status_caisse': forms.Select(attrs={'class': 'form-control'}),
            'cout': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'paiement': forms.Select(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }