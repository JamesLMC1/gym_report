from django.urls import path
from . import views

app_name = "workouts"

urlpatterns = [
    path("", views.index, name="index"),
    path("crear/", views.create, name="create"),
    path("<int:workout_id>/", views.detail, name="detail"),
    path("<int:workout_id>/editar/", views.edit, name="edit"),
    path("<int:workout_id>/eliminar/", views.delete, name="delete"),
]
