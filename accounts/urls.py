from django.urls import path

from .views import LoginUsuarioView, LogoutUsuarioView

app_name = "accounts"

urlpatterns = [
    path("login/", LoginUsuarioView.as_view(), name="login"),
    path("logout/", LogoutUsuarioView.as_view(), name="logout"),
]
