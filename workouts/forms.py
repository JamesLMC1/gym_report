from django import forms
from .models import Rutina


class RutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = ['nombre', 'descripcion', 'nivel', 'duracion_dias']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'nivel': forms.Select(attrs={'class': 'form-input'}),
            'duracion_dias': forms.NumberInput(attrs={'class': 'form-input'}),
        }
