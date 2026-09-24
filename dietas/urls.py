from django.urls import path
from . import views

app_name = "dietas"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:comida_id>/", views.detail, name="detail"),
    path("receta/crear/", views.receta_create, name="receta_create"),
    path("receta/<int:receta_id>/", views.receta_detail, name="receta_detail"),
    path("receta/<int:receta_id>/editar/", views.receta_edit, name="receta_edit"),
    path("receta/<int:receta_id>/eliminar/", views.receta_delete, name="receta_delete"),
]
