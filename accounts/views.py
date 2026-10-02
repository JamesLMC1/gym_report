from django.contrib.auth.views import LoginView, LogoutView

from .forms import LoginForm


class LoginUsuarioView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class LogoutUsuarioView(LogoutView):
    next_page = "accounts:login"
