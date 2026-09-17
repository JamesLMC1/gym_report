from django.http import Http404
from django.shortcuts import render, redirect
from .models import Workout
from .forms import WorkoutForm


def index(request):
    from gym.models import Set
    if not Set.objects.exists():
        from usuarios.models import Usuario
        if not Usuario.objects.exists():
            return render(request, "workouts/bloqueado.html", {"mensaje": "Primero debes registrar un usuario"})
        return render(request, "workouts/bloqueado.html", {"mensaje": "Primero debes registrar al menos un ejercicio en Gym"})

    latest = Workout.objects.all()[:5]
    return render(request, "workouts/index.html", {"latest": latest})


def detail(request, workout_id):
    try:
        workout = Workout.objects.get(pk=workout_id)
    except Workout.DoesNotExist:
        raise Http404("El entrenamiento no existe")
    return render(request, "workouts/detail.html", {"workout": workout})


def create(request):
    from gym.models import Set
    if not Set.objects.exists():
        from usuarios.models import Usuario
        if not Usuario.objects.exists():
            return render(request, "workouts/bloqueado.html", {"mensaje": "Primero debes registrar un usuario"})
        return render(request, "workouts/bloqueado.html", {"mensaje": "Primero debes registrar al menos un ejercicio en Gym"})

    if request.method == "POST":
        form = WorkoutForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("workouts:index")
    else:
        form = WorkoutForm()
    return render(request, "workouts/form.html", {"form": form, "titulo": "Registrar Entrenamiento"})


def edit(request, workout_id):
    try:
        workout = Workout.objects.get(pk=workout_id)
    except Workout.DoesNotExist:
        raise Http404("El entrenamiento no existe")

    if request.method == "POST":
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return redirect("workouts:detail", workout_id=workout.id)
    else:
        form = WorkoutForm(instance=workout)
    return render(request, "workouts/form.html", {"form": form, "titulo": "Editar Entrenamiento"})


def delete(request, workout_id):
    try:
        workout = Workout.objects.get(pk=workout_id)
    except Workout.DoesNotExist:
        raise Http404("El entrenamiento no existe")

    if request.method == "POST":
        workout.delete()
        return redirect("workouts:index")
    return render(request, "workouts/delete.html", {"workout": workout})
