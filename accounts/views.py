from django.contrib.auth.views import LoginView, LogoutView

from .forms import LoginForm


class LoginUsuarioView(LoginView):
    """Vista de inicio de sesión; redirige al home si ya está autenticado."""
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class LogoutUsuarioView(LogoutView):
    """Cierra la sesión del usuario y redirige al login."""
    next_page = "accounts:login"
