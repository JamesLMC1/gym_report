from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import RegistroForm


class RegistroView(FormView):
    """Registra un nuevo usuario y lo deja autenticado tras el registro."""
    template_name = "registro/register.html"
    form_class = RegistroForm
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        """Evita que un usuario ya autenticado vuelva a registrarse."""
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Guarda el usuario, inicia sesión y muestra mensaje de bienvenida."""
        user = form.save()
        login(self.request, user)
        messages.success(
            self.request,
            f"¡Cuenta creada! Bienvenido, {user.get_short_name() or user.username}.",
        )
        return super().form_valid(form)
