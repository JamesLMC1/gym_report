from django.urls import path
from . import views

app_name = "profesores_involucrados"

urlpatterns = [
    path("", views.index, name="index"),
]
