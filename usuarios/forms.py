from django import forms
from .models import Usuario


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'edad', 'peso', 'estatura']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input'}),
            'edad': forms.NumberInput(attrs={'class': 'form-input'}),
            'peso': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'estatura': forms.NumberInput(attrs={'class': 'form-input'}),
        }
