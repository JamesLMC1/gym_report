from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Set


def index(request):
    # Últimos 5 sets registrados
    latest_set_list = Set.objects.all()[:5]

    if not latest_set_list:
        return HttpResponse("No hay registros de ejercicios aún.")

    lines = []
    for i, s in enumerate(latest_set_list, start=1):
        lines.append(
            f"{i}. {s.nombre_ejercicio} — Peso: {s.peso}kg — "
            f"Reps: {s.repeticiones} — Descanso: {s.tiempo_descanso}s"
        )

    return HttpResponse("\n".join(lines))


def all(request):
    # Lista todos los sets registrados
    all_sets = Set.objects.all()

    if not all_sets:
        return HttpResponse("No hay registros de ejercicios aún.")

    lines = []
    for i, s in enumerate(all_sets, start=1):
        lines.append(
            f"{i}. {s.nombre_ejercicio} — Peso: {s.peso}kg — "
            f"Reps: {s.repeticiones} — Descanso: {s.tiempo_descanso}s"
        )

    return HttpResponse("\n".join(lines))


def detail(request, set_id):
    # Detalle completo de un set por su ID
    set_obj = get_object_or_404(Set, pk=set_id)

    output = (
        f"Ejercicio: {set_obj.nombre_ejercicio}\n"
        f"Peso: {set_obj.peso}kg\n"
        f"Repeticiones: {set_obj.repeticiones}\n"
        f"Descanso: {set_obj.tiempo_descanso} segundos"
    )
    return HttpResponse(output)


def by_exercise(request, exercise_name):
    # Busca todos los sets que contengan el nombre del ejercicio
    sets = Set.objects.filter(nombre_ejercicio__icontains=exercise_name)

    if not sets:
        return HttpResponse(f"No se encontraron sets para '{exercise_name}'.")

    lines = []
    for i, s in enumerate(sets, start=1):
        lines.append(
            f"{i}. Peso: {s.peso}kg — "
            f"Reps: {s.repeticiones} — Descanso: {s.tiempo_descanso}s"
        )

    output = f"Sets de '{exercise_name}':\n\n" + "\n".join(lines)
    return HttpResponse(output)
