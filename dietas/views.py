from django.shortcuts import render
from django.http import Http404
from config.api_service import get_comidas, get_comida


def index(request):
    from usuarios.models import Usuario
    if not Usuario.objects.exists():
        return render(request, "dietas/bloqueado.html", {"mensaje": "Primero debes registrar un usuario"})

    comidas = get_comidas()
    return render(request, "dietas/index.html", {"comidas": comidas})


def detail(request, comida_id):
    from usuarios.models import Usuario
    if not Usuario.objects.exists():
        return render(request, "dietas/bloqueado.html", {"mensaje": "Primero debes registrar un usuario"})

    comida = get_comida(comida_id)
    if not comida:
        raise Http404("Comida no encontrada")
    return render(request, "dietas/detail.html", {"comida": comida})
