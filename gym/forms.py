from django import forms
from .models import Ejercicio


class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ['nombre', 'grupo_muscular', 'descripcion', 'dificultad', 'imagen_url']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input'}),
            'grupo_muscular': forms.TextInput(attrs={'class': 'form-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'dificultad': forms.Select(attrs={'class': 'form-input'}),
            'imagen_url': forms.TextInput(attrs={'class': 'form-input'}),
        }
