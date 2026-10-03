from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    """Página de inicio; solo accesible para usuarios autenticados."""
    template_name = "home.html"
