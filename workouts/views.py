from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render

from config import api_service
from gym.models import Ejercicio
from .forms import RutinaForm
from .models import Rutina, RutinaEjercicio

CAMPOS = ('nombre', 'descripcion', 'nivel', 'duracion_dias')


def _body(form):
    return {campo: form.cleaned_data.get(campo) for campo in CAMPOS}


def sincronizar_ejercicio(item):
    if not item or not item.get('id'):
        return None
    obj, _ = Ejercicio.objects.update_or_create(
        id=item['id'],
        defaults={
            'nombre': item.get('nombre') or '',
            'grupo_muscular': item.get('grupo_muscular') or '',
            'descripcion': item.get('descripcion') or '',
            'dificultad': item.get('dificultad') or '',
            'imagen_url': item.get('imagen_url') or '',
            'created_at': item.get('created_at'),
        },
    )
    return obj


def sincronizar_rutina(item):
    if not item or not item.get('id'):
        return None
    obj, _ = Rutina.objects.update_or_create(
        id=item['id'],
        defaults={
            'nombre': item.get('nombre') or '',
            'descripcion': item.get('descripcion') or '',
            'nivel': item.get('nivel') or '',
            'duracion_dias': item.get('duracion_dias'),
            'created_at': item.get('created_at'),
        },
    )
    return obj


def sincronizar_detalle(item):
    """Sincroniza una rutina con sus ejercicios (GET /rutinas/{id})."""
    rutina = sincronizar_rutina(item)
    if not rutina:
        return None
    for re in item.get('ejercicios') or []:
        ejercicio = sincronizar_ejercicio(re.get('ejercicios'))
        if not ejercicio or not re.get('id'):
            continue
        RutinaEjercicio.objects.update_or_create(
            id=re['id'],
            defaults={
                'rutina': rutina,
                'ejercicio': ejercicio,
                'series': re.get('series'),
                'repeticiones': re.get('repeticiones') or '',
                'descanso_segundos': re.get('descanso_segundos'),
            },
        )
    return rutina


@login_required
def index(request):
    latest = Rutina.objects.all()[:5]
    return render(request, 'workouts/index.html', {'latest': latest})


@login_required
def all(request):
    rutinas = Rutina.objects.all()
    return render(request, 'workouts/all.html', {'rutinas': rutinas})


@login_required
def detail(request, rutina_id):
    try:
        rutina = Rutina.objects.get(pk=rutina_id)
    except Rutina.DoesNotExist:
        raise Http404('La rutina no existe')

    detalle = api_service.get_rutina(rutina_id)
    if detalle:
        sincronizar_detalle(detalle)
        rutina.refresh_from_db()

    items = rutina.items.select_related('ejercicio')
    return render(request, 'workouts/detail.html', {'rutina': rutina, 'items': items})


@login_required
def catalogo(request):
    items = api_service.get_rutinas()
    if items:
        for item in items:
            sincronizar_rutina(item)
        messages.success(request, f'Catálogo sincronizado: {len(items)} rutinas desde {api_service.etiqueta_conexion()}.')
    else:
        messages.error(request, 'No se pudo cargar el catálogo de rutinas.')
    rutinas = Rutina.objects.all()
    return render(request, 'workouts/catalogo_rutinas.html', {'rutinas': rutinas})


@login_required
def create(request):
    if request.method == 'POST':
        form = RutinaForm(request.POST)
        if form.is_valid():
            creado, error = api_service.crear_rutina(_body(form))
            if error:
                messages.error(request, error)
            elif not creado:
                messages.error(request, 'El microservicio no devolvió la rutina creada.')
            else:
                sincronizar_rutina(creado)
                messages.success(request, f'Rutina creada y sincronizada en {api_service.etiqueta_conexion()}.')
                return redirect('workouts:index')
    else:
        form = RutinaForm()
    return render(request, 'workouts/form.html', {'form': form, 'titulo': 'Registrar Rutina'})


@login_required
def edit(request, rutina_id):
    try:
        rutina = Rutina.objects.get(pk=rutina_id)
    except Rutina.DoesNotExist:
        raise Http404('La rutina no existe')

    if request.method == 'POST':
        form = RutinaForm(request.POST, instance=rutina)
        if form.is_valid():
            actualizado, error = api_service.actualizar_rutina(rutina_id, _body(form))
            if error:
                messages.error(request, error)
            else:
                if actualizado:
                    sincronizar_rutina(actualizado)
                else:
                    form.save()
                messages.success(request, f'Rutina actualizada en {api_service.etiqueta_conexion()}.')
                return redirect('workouts:detail', rutina_id=rutina.id)
    else:
        form = RutinaForm(instance=rutina)
    return render(request, 'workouts/form.html', {'form': form, 'titulo': 'Editar Rutina'})


@login_required
def delete(request, rutina_id):
    try:
        rutina = Rutina.objects.get(pk=rutina_id)
    except Rutina.DoesNotExist:
        raise Http404('La rutina no existe')

    if request.method == 'POST':
        _, error = api_service.eliminar_rutina(rutina_id)
        if error:
            messages.error(request, error)
        else:
            rutina.delete()
            messages.success(request, f'Rutina eliminada de {api_service.etiqueta_conexion()}.')
            return redirect('workouts:index')
    return render(request, 'workouts/delete.html', {'rutina': rutina})
