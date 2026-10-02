from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nombre",
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Tu nombre",
            "autocomplete": "given-name",
        }),
    )
    last_name = forms.CharField(
        label="Apellido",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Tu apellido",
            "autocomplete": "family-name",
        }),
    )
    email = forms.EmailField(
        label="Correo",
        widget=forms.EmailInput(attrs={
            "class": "form-input",
            "placeholder": "tucorreo@ejemplo.com",
            "autocomplete": "email",
        }),
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Usuario"
        self.fields["username"].help_text = ""
        self.fields["username"].widget.attrs.update({
            "class": "form-input",
            "placeholder": "Elige un usuario",
            "autocomplete": "username",
        })
        self.fields["password1"].label = "Contraseña"
        self.fields["password1"].widget.attrs.update({
            "class": "form-input",
            "placeholder": "Crea una contraseña",
            "autocomplete": "new-password",
        })
        self.fields["password2"].label = "Confirmar contraseña"
        self.fields["password2"].widget.attrs.update({
            "class": "form-input",
            "placeholder": "Repite la contraseña",
            "autocomplete": "new-password",
        })

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo.")
        return email
