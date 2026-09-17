from django import forms
from .models import Workout


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['fecha', 'duracion', 'notas']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'duracion': forms.NumberInput(attrs={'class': 'form-input'}),
            'notas': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }
