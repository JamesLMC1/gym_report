from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "autofocus": True,
            "autocomplete": "username",
            "placeholder": "Tu usuario",
        }),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "autocomplete": "current-password",
            "placeholder": "Tu contraseña",
        }),
    )
