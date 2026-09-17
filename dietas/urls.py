from django.urls import path
from . import views

app_name = "dietas"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:comida_id>/", views.detail, name="detail"),
]
