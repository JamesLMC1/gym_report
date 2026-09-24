from django.shortcuts import render, redirect
from django.http import Http404
from config.api_service import get_comidas, get_comida
from .models import Receta
from .forms import RecetaForm


def index(request):
    from usuarios.models import Usuario
    if not Usuario.objects.exists():
        return render(request, "dietas/bloqueado.html", {"mensaje": "Primero debes registrar un usuario"})

    comidas = get_comidas()
    recetas = Receta.objects.all()
    return render(request, "dietas/index.html", {"comidas": comidas, "recetas": recetas})


def detail(request, comida_id):
    from usuarios.models import Usuario
    if not Usuario.objects.exists():
        return render(request, "dietas/bloqueado.html", {"mensaje": "Primero debes registrar un usuario"})

    comida = get_comida(comida_id)
    if not comida:
        raise Http404("Comida no encontrada")
    return render(request, "dietas/detail.html", {"comida": comida})


def receta_detail(request, receta_id):
    from usuarios.models import Usuario
    if not Usuario.objects.exists():
        return render(request, "dietas/bloqueado.html", {"mensaje": "Primero debes registrar un usuario"})

    try:
        receta = Receta.objects.get(pk=receta_id)
    except Receta.DoesNotExist:
        raise Http404("Receta no encontrada")
    return render(request, "dietas/receta_detail.html", {"receta": receta})


def receta_create(request):
    from usuarios.models import Usuario
    if not Usuario.objects.exists():
        return render(request, "dietas/bloqueado.html", {"mensaje": "Primero debes registrar un usuario"})

    if request.method == "POST":
        form = RecetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dietas:index")
    else:
        form = RecetaForm()
    return render(request, "dietas/form.html", {"form": form, "titulo": "Crear Receta"})


def receta_edit(request, receta_id):
    from usuarios.models import Usuario
    if not Usuario.objects.exists():
        return render(request, "dietas/bloqueado.html", {"mensaje": "Primero debes registrar un usuario"})

    try:
        receta = Receta.objects.get(pk=receta_id)
    except Receta.DoesNotExist:
        raise Http404("Receta no encontrada")

    if request.method == "POST":
        form = RecetaForm(request.POST, instance=receta)
        if form.is_valid():
            form.save()
            return redirect("dietas:receta_detail", receta_id=receta.id)
    else:
        form = RecetaForm(instance=receta)
    return render(request, "dietas/form.html", {"form": form, "titulo": "Editar Receta"})


def receta_delete(request, receta_id):
    from usuarios.models import Usuario
    if not Usuario.objects.exists():
        return render(request, "dietas/bloqueado.html", {"mensaje": "Primero debes registrar un usuario"})

    try:
        receta = Receta.objects.get(pk=receta_id)
    except Receta.DoesNotExist:
        raise Http404("Receta no encontrada")

    if request.method == "POST":
        receta.delete()
        return redirect("dietas:index")
    return render(request, "dietas/delete.html", {"receta": receta})
