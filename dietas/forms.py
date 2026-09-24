from django import forms
from .models import Receta


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['nombre', 'tipo', 'calorias', 'proteinas_g', 'carbos_g', 'grasas_g', 'receta']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input'}),
            'tipo': forms.Select(attrs={'class': 'form-input'}),
            'calorias': forms.NumberInput(attrs={'class': 'form-input'}),
            'proteinas_g': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'carbos_g': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'grasas_g': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'receta': forms.Textarea(attrs={'class': 'form-input', 'rows': 6}),
        }
