import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from config import api_service
from gym.models import Ejercicio
from .forms import RutinaForm
from .models import Rutina, RutinaEjercicio

CAMPOS = ('nombre', 'descripcion', 'nivel', 'duracion_dias')


def _body(form):
    return {campo: form.cleaned_data.get(campo) for campo in CAMPOS}


def _crear_local(datos):
    """Crea la rutina solo en la BD local (microservicio no disponible)."""
    return Rutina.objects.create(id=uuid.uuid4(), created_at=timezone.now(), **datos)


def _actualizar_local(rutina, datos):
    for campo, valor in datos.items():
        setattr(rutina, campo, valor)
    rutina.save()
    return rutina


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
    """Página principal: muestra las últimas 5 rutinas registradas."""
    latest = Rutina.objects.all()[:5]
    return render(request, 'workouts/index.html', {'latest': latest})


@login_required
def all(request):
    """Lista todas las rutinas guardadas en la base de datos local."""
    rutinas = Rutina.objects.all()
    return render(request, 'workouts/all.html', {'rutinas': rutinas})


@login_required
def detail(request, rutina_id):
    """Muestra una rutina con sus ejercicios; lanza 404 si no existe."""
    try:
        rutina = Rutina.objects.get(pk=rutina_id)
    except Rutina.DoesNotExist:
        raise Http404('La rutina no existe')

    items = rutina.items.select_related('ejercicio')
    return render(request, 'workouts/detail.html', {'rutina': rutina, 'items': items})


@login_required
def catalogo(request):
    """Muestra el catálogo en vivo del microservicio (sin guardar nada)."""
    items = api_service.get_rutinas()
    if items:
        guardados = {str(pk) for pk in Rutina.objects.values_list('id', flat=True)}
        for item in items:
            item['guardado'] = str(item.get('id')) in guardados
        messages.success(
            request,
            f'Catálogo cargado: {len(items)} rutinas desde {api_service.etiqueta_conexion()}. '
            f'Usa "Guardar" para añadirlas a tu lista.',
        )
    else:
        messages.error(request, 'No se pudo cargar el catálogo de rutinas desde el microservicio.')
    return render(request, 'workouts/catalogo_rutinas.html', {'rutinas': items or []})


@login_required
@require_POST
def guardar(request, rutina_id):
    """Guarda en la BD local una rutina (con sus ejercicios) traída del catálogo."""
    detalle = api_service.get_rutina(rutina_id)
    if not detalle:
        messages.error(request, 'No se pudo obtener la rutina del microservicio para guardarla.')
    else:
        sincronizar_detalle(detalle)
        messages.success(request, f'Rutina guardada en tu lista desde {api_service.etiqueta_conexion()}.')
    return redirect('workouts:catalogo')


@login_required
def create(request):
    """Registra una rutina: la crea en el microservicio y/o en la BD local."""
    if request.method == 'POST':
        form = RutinaForm(request.POST)
        if form.is_valid():
            datos = _body(form)
            creado, error = api_service.crear_rutina(datos)
            if creado:
                sincronizar_rutina(creado)
                messages.success(request, f'Rutina creada en {api_service.etiqueta_conexion()}.')
            else:
                _crear_local(datos)
                messages.warning(request, 'El microservicio no está disponible: rutina guardada solo en la base local.')
            return redirect('workouts:index')
    else:
        form = RutinaForm()
    return render(request, 'workouts/form.html', {'form': form, 'titulo': 'Registrar Rutina'})


@login_required
def edit(request, rutina_id):
    """Edita una rutina existente en el microservicio y/o en la BD local."""
    try:
        rutina = Rutina.objects.get(pk=rutina_id)
    except Rutina.DoesNotExist:
        raise Http404('La rutina no existe')

    if request.method == 'POST':
        form = RutinaForm(request.POST, instance=rutina)
        if form.is_valid():
            datos = _body(form)
            actualizado, error = api_service.actualizar_rutina(rutina_id, datos)
            if actualizado:
                sincronizar_rutina(actualizado)
                messages.success(request, f'Rutina actualizada en {api_service.etiqueta_conexion()}.')
            else:
                _actualizar_local(rutina, datos)
                messages.warning(request, 'El microservicio no está disponible: cambios guardados solo en la base local.')
            return redirect('workouts:detail', rutina_id=rutina.id)
    else:
        form = RutinaForm(instance=rutina)
    return render(request, 'workouts/form.html', {'form': form, 'titulo': 'Editar Rutina'})


@login_required
def delete(request, rutina_id):
    """Confirma y elimina una rutina del microservicio y de la BD local."""
    try:
        rutina = Rutina.objects.get(pk=rutina_id)
    except Rutina.DoesNotExist:
        raise Http404('La rutina no existe')

    if request.method == 'POST':
        _, error = api_service.eliminar_rutina(rutina_id)
        rutina.delete()
        if error:
            messages.warning(request, 'El microservicio no está disponible: rutina eliminada solo en la base local.')
        else:
            messages.success(request, f'Rutina eliminada de {api_service.etiqueta_conexion()}.')
        return redirect('workouts:index')
    return render(request, 'workouts/delete.html', {'rutina': rutina})
