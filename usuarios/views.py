from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Usuario
from .forms import UsuarioForm


@login_required
def index(request):
    """Página principal: muestra los últimos 5 usuarios registrados."""
    latest = Usuario.objects.all()[:5]
    return render(request, "usuarios/index.html", {"latest": latest})


@login_required
def detail(request, usuario_id):
    """Muestra el detalle de un usuario; lanza 404 si no existe."""
    try:
        usuario = Usuario.objects.get(pk=usuario_id)
    except Usuario.DoesNotExist:
        raise Http404("El usuario no existe")
    return render(request, "usuarios/detail.html", {"usuario": usuario})


@login_required
def create(request):
    """Registra un nuevo usuario desde el formulario."""
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("usuarios:index")
    else:
        form = UsuarioForm()
    return render(request, "usuarios/form.html", {"form": form, "titulo": "Registrar Usuario"})


@login_required
def edit(request, usuario_id):
    """Edita los datos de un usuario existente."""
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


@login_required
def delete(request, usuario_id):
    """Confirma y elimina un usuario."""
    try:
        usuario = Usuario.objects.get(pk=usuario_id)
    except Usuario.DoesNotExist:
        raise Http404("El usuario no existe")

    if request.method == "POST":
        usuario.delete()
        return redirect("usuarios:index")
    return render(request, "usuarios/delete.html", {"usuario": usuario})
