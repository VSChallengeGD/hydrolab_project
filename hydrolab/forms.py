from django import forms
from .models import Calculation

class CalculationForm(forms.ModelForm):
     class Meta:
        model = Calculation
        fields = ['well_name', 'depth', 'flow_rate', 'density', 'tau0', 'k_cons', 'n_index']
        widgets = {
            'well_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Скважина №5'}),
            'depth': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.1'}),
            'flow_rate': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.1'}), 
            'density': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.1'}), 
            'tau0': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}), 
            'k_cons': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'n_index': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '1'}),
        }