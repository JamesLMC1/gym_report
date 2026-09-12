from django.urls import path
from . import views

app_name = "workouts"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:workout_id>/", views.detail, name="detail"),
    path("<int:workout_id>/update/", views.update, name="update"),
    path("<int:workout_id>/delete/", views.delete, name="delete"),
]
