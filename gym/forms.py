from django import forms
from .models import Set


class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ['nombre_ejercicio', 'peso', 'repeticiones', 'tiempo_descanso']
