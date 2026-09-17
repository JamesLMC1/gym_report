from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path("", views.index, name="index"),
    path("crear/", views.create, name="create"),
    path("<int:usuario_id>/", views.detail, name="detail"),
    path("<int:usuario_id>/editar/", views.edit, name="edit"),
    path("<int:usuario_id>/eliminar/", views.delete, name="delete"),
]
