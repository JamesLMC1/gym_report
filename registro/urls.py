from django.urls import path

from .views import RegistroView

app_name = "registro"

urlpatterns = [
    path("", RegistroView.as_view(), name="register"),
]
