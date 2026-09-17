from django.urls import path
from . import views

app_name = "gym"

urlpatterns = [
    path("", views.index, name="index"),
    path("all/", views.all, name="all"),
    path("crear/", views.create, name="create"),
    path("catalogo/", views.crear_desde_catalogo, name="catalogo"),
    path("catalogo/<str:ejercicio_id>/", views.crear_set_desde_ejercicio, name="crear_desde_ejercicio"),
    path("rutinas/", views.rutinas, name="rutinas"),
    path("rutinas/<str:rutina_id>/", views.rutina_detail, name="rutina_detail"),
    path("<int:set_id>/", views.detail, name="detail"),
    path("<int:set_id>/editar/", views.edit, name="edit"),
    path("<int:set_id>/eliminar/", views.delete, name="delete"),
    path("exercise/<str:exercise_name>/", views.by_exercise, name="by_exercise"),
]
