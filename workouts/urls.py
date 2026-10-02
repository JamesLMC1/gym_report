from django.urls import path
from . import views

app_name = "workouts"

urlpatterns = [
    path("", views.index, name="index"),
    path("all/", views.all, name="all"),
    path("crear/", views.create, name="create"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("<uuid:rutina_id>/", views.detail, name="detail"),
    path("<uuid:rutina_id>/editar/", views.edit, name="edit"),
    path("<uuid:rutina_id>/eliminar/", views.delete, name="delete"),
]
