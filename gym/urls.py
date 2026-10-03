from django.urls import path
from . import views

app_name = "gym"

urlpatterns = [
    path("", views.index, name="index"),
    path("all/", views.all, name="all"),
    path("crear/", views.create, name="create"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("<uuid:ejercicio_id>/guardar/", views.guardar, name="guardar"),
    path("<uuid:ejercicio_id>/", views.detail, name="detail"),
    path("<uuid:ejercicio_id>/editar/", views.edit, name="edit"),
    path("<uuid:ejercicio_id>/eliminar/", views.delete, name="delete"),
]
