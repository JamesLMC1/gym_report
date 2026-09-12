from django.urls import path
from . import views

app_name = "gym"

urlpatterns = [
    path("", views.index, name="index"),
    path("all/", views.all, name="all"),
    path("<int:set_id>/", views.detail, name="detail"),
    path("exercise/<str:exercise_name>/", views.by_exercise, name="by_exercise"),
]
