from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Workout


def index(request):
    # Lista los últimos 5 entrenamientos
    latest = Workout.objects.all()[:5]

    if not latest:
        return HttpResponse("No hay entrenamientos registrados aún.")

    lines = []
    for i, w in enumerate(latest, start=1):
        lines.append(f"{i}. {w.fecha} — {w.duracion} min — {w.notas or 'Sin notas'}")

    return HttpResponse("\n".join(lines))


def detail(request, workout_id):
    # Detalle de un entrenamiento por su ID
    w = get_object_or_404(Workout, pk=workout_id)

    output = (
        f"Fecha: {w.fecha}\n"
        f"Duración: {w.duracion} minutos\n"
        f"Notas: {w.notas or 'Sin notas'}"
    )
    return HttpResponse(output)
