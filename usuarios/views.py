from django.http import Http404
from django.shortcuts import render, redirect
from .models import Usuario
from .forms import UsuarioForm


def index(request):
    latest = Usuario.objects.all()[:5]
    return render(request, "usuarios/index.html", {"latest": latest})


def detail(request, usuario_id):
    try:
        usuario = Usuario.objects.get(pk=usuario_id)
    except Usuario.DoesNotExist:
        raise Http404("El usuario no existe")
    return render(request, "usuarios/detail.html", {"usuario": usuario})


def create(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("usuarios:index")
    else:
        form = UsuarioForm()
    return render(request, "usuarios/form.html", {"form": form, "titulo": "Registrar Usuario"})


def edit(request, usuario_id):
    try:
        usuario = Usuario.objects.get(pk=usuario_id)
    except Usuario.DoesNotExist:
        raise Http404("El usuario no existe")

    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect("usuarios:detail", usuario_id=usuario.id)
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, "usuarios/form.html", {"form": form, "titulo": "Editar Usuario"})


def delete(request, usuario_id):
    try:
        usuario = Usuario.objects.get(pk=usuario_id)
    except Usuario.DoesNotExist:
        raise Http404("El usuario no existe")

    if request.method == "POST":
        usuario.delete()
        return redirect("usuarios:index")
    return render(request, "usuarios/delete.html", {"usuario": usuario})
