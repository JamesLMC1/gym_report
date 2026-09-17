from django import forms
from .models import Set


class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ['nombre_ejercicio', 'peso', 'repeticiones', 'tiempo_descanso']
        widgets = {
            'nombre_ejercicio': forms.TextInput(attrs={'class': 'form-input'}),
            'peso': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'repeticiones': forms.NumberInput(attrs={'class': 'form-input'}),
            'tiempo_descanso': forms.NumberInput(attrs={'class': 'form-input'}),
        }
