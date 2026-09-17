from django.http import Http404
from django.shortcuts import render, redirect
from .models import Set
from .forms import SetForm
from config.api_service import get_ejercicios, get_ejercicio, get_rutinas, get_rutina


def index(request):
    from usuarios.models import Usuario
    if not Usuario.objects.exists():
        return render(request, "gym/bloqueado.html", {"mensaje": "Primero debes registrar un usuario"})

    latest_set_list = Set.objects.all()[:5]
    return render(request, "gym/index.html", {"latest_set_list": latest_set_list})


def all(request):
    from usuarios.models import Usuario
    if not Usuario.objects.exists():
        return render(request, "gym/bloqueado.html", {"mensaje": "Primero debes registrar un usuario"})

    all_sets = Set.objects.all()
    return render(request, "gym/all.html", {"all_sets": all_sets})


def detail(request, set_id):
    try:
        set_obj = Set.objects.get(pk=set_id)
    except Set.DoesNotExist:
        raise Http404("El set no existe")
    return render(request, "gym/detail.html", {"set_obj": set_obj})


def by_exercise(request, exercise_name):
    sets = Set.objects.filter(nombre_ejercicio__icontains=exercise_name)
    return render(request, "gym/by_exercise.html", {"sets": sets, "exercise_name": exercise_name})


def crear_desde_catalogo(request):
    from usuarios.models import Usuario
    if not Usuario.objects.exists():
        return render(request, "gym/bloqueado.html", {"mensaje": "Primero debes registrar un usuario"})

    ejercicios = get_ejercicios()
    return render(request, "gym/catalogo_ejercicios.html", {"ejercicios": ejercicios})


def crear_set_desde_ejercicio(request, ejercicio_id):
    from usuarios.models import Usuario
    if not Usuario.objects.exists():
        return render(request, "gym/bloqueado.html", {"mensaje": "Primero debes registrar un usuario"})

    ejercicio = get_ejercicio(ejercicio_id)
    if not ejercicio:
        raise Http404("Ejercicio no encontrado en el catálogo")

    if request.method == "POST":
        form = SetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("gym:index")
    else:
        form = SetForm(initial={"nombre_ejercicio": ejercicio["nombre"]})
    return render(request, "gym/form.html", {
        "form": form,
        "titulo": f"Registrar Set: {ejercicio['nombre']}",
        "ejercicio": ejercicio,
    })


def create(request):
    from usuarios.models import Usuario
    if not Usuario.objects.exists():
        return render(request, "gym/bloqueado.html", {"mensaje": "Primero debes registrar un usuario"})

    if request.method == "POST":
        form = SetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("gym:index")
    else:
        form = SetForm()
    return render(request, "gym/form.html", {"form": form, "titulo": "Registrar Set"})


def edit(request, set_id):
    try:
        set_obj = Set.objects.get(pk=set_id)
    except Set.DoesNotExist:
        raise Http404("El set no existe")

    if request.method == "POST":
        form = SetForm(request.POST, instance=set_obj)
        if form.is_valid():
            form.save()
            return redirect("gym:detail", set_id=set_obj.id)
    else:
        form = SetForm(instance=set_obj)
    return render(request, "gym/form.html", {"form": form, "titulo": "Editar Set"})


def delete(request, set_id):
    try:
        set_obj = Set.objects.get(pk=set_id)
    except Set.DoesNotExist:
        raise Http404("El set no existe")

    if request.method == "POST":
        set_obj.delete()
        return redirect("gym:index")
    return render(request, "gym/delete.html", {"set_obj": set_obj})


def rutinas(request):
    from usuarios.models import Usuario
    if not Usuario.objects.exists():
        return render(request, "gym/bloqueado.html", {"mensaje": "Primero debes registrar un usuario"})

    rutinas = get_rutinas()
    return render(request, "gym/rutinas.html", {"rutinas": rutinas})


def rutina_detail(request, rutina_id):
    from usuarios.models import Usuario
    if not Usuario.objects.exists():
        return render(request, "gym/bloqueado.html", {"mensaje": "Primero debes registrar un usuario"})

    rutina = get_rutina(rutina_id)
    if not rutina:
        raise Http404("Rutina no encontrada")
    return render(request, "gym/rutina_detail.html", {"rutina": rutina})
