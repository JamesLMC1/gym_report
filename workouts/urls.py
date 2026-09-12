from django.urls import path
from . import views

app_name = "workouts"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:workout_id>/", views.detail, name="detail"),
]
