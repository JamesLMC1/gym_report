from django import forms
from .models import Workout


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['fecha', 'duracion', 'notas']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
