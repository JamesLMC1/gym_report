import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from config import api_service
from .forms import EjercicioForm
from .models import Ejercicio

CAMPOS = ('nombre', 'grupo_muscular', 'descripcion', 'dificultad', 'imagen_url')


def _body(form):
    return {campo: form.cleaned_data.get(campo) for campo in CAMPOS}


def _crear_local(datos):
    """Crea el ejercicio solo en la BD local (microservicio no disponible)."""
    return Ejercicio.objects.create(id=uuid.uuid4(), created_at=timezone.now(), **datos)


def _actualizar_local(ejercicio, datos):
    for campo, valor in datos.items():
        setattr(ejercicio, campo, valor)
    ejercicio.save()
    return ejercicio


def sincronizar_ejercicio(item):
    """Inserta/actualiza en la BD local un ejercicio del microservicio."""
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


@login_required
def index(request):
    latest = Ejercicio.objects.all()[:5]
    return render(request, 'gym/index.html', {'latest': latest})


@login_required
def all(request):
    ejercicios = Ejercicio.objects.all()
    return render(request, 'gym/all.html', {'ejercicios': ejercicios})


@login_required
def detail(request, ejercicio_id):
    try:
        ejercicio = Ejercicio.objects.get(pk=ejercicio_id)
    except Ejercicio.DoesNotExist:
        raise Http404('El ejercicio no existe')
    return render(request, 'gym/detail.html', {'ejercicio': ejercicio})


@login_required
def catalogo(request):
    """Muestra el catálogo en vivo del microservicio (sin guardar nada)."""
    items = api_service.get_ejercicios()
    if items:
        guardados = {str(pk) for pk in Ejercicio.objects.values_list('id', flat=True)}
        for item in items:
            item['guardado'] = str(item.get('id')) in guardados
        messages.success(
            request,
            f'Catálogo cargado: {len(items)} ejercicios desde {api_service.etiqueta_conexion()}. '
            f'Usa "Guardar" para añadirlos a tu lista.',
        )
    else:
        messages.error(request, 'No se pudo cargar el catálogo de ejercicios desde el microservicio.')
    return render(request, 'gym/catalogo_ejercicios.html', {'ejercicios': items or []})


@login_required
@require_POST
def guardar(request, ejercicio_id):
    """Guarda en la BD local un ejercicio traído del catálogo."""
    item = api_service.get_ejercicio(ejercicio_id)
    if not item:
        messages.error(request, 'No se pudo obtener el ejercicio del microservicio para guardarlo.')
    else:
        sincronizar_ejercicio(item)
        messages.success(request, f'Ejercicio guardado en tu lista desde {api_service.etiqueta_conexion()}.')
    return redirect('gym:catalogo')


@login_required
def create(request):
    if request.method == 'POST':
        form = EjercicioForm(request.POST)
        if form.is_valid():
            datos = _body(form)
            creado, error = api_service.crear_ejercicio(datos)
            if creado:
                sincronizar_ejercicio(creado)
                messages.success(request, f'Ejercicio creado en {api_service.etiqueta_conexion()}.')
            else:
                _crear_local(datos)
                messages.warning(request, 'El microservicio no está disponible: ejercicio guardado solo en la base local.')
            return redirect('gym:index')
    else:
        form = EjercicioForm()
    return render(request, 'gym/form.html', {'form': form, 'titulo': 'Registrar Ejercicio'})


@login_required
def edit(request, ejercicio_id):
    try:
        ejercicio = Ejercicio.objects.get(pk=ejercicio_id)
    except Ejercicio.DoesNotExist:
        raise Http404('El ejercicio no existe')

    if request.method == 'POST':
        form = EjercicioForm(request.POST, instance=ejercicio)
        if form.is_valid():
            datos = _body(form)
            actualizado, error = api_service.actualizar_ejercicio(ejercicio_id, datos)
            if actualizado:
                sincronizar_ejercicio(actualizado)
                messages.success(request, f'Ejercicio actualizado en {api_service.etiqueta_conexion()}.')
            else:
                _actualizar_local(ejercicio, datos)
                messages.warning(request, 'El microservicio no está disponible: cambios guardados solo en la base local.')
            return redirect('gym:detail', ejercicio_id=ejercicio.id)
    else:
        form = EjercicioForm(instance=ejercicio)
    return render(request, 'gym/form.html', {'form': form, 'titulo': 'Editar Ejercicio'})


@login_required
def delete(request, ejercicio_id):
    try:
        ejercicio = Ejercicio.objects.get(pk=ejercicio_id)
    except Ejercicio.DoesNotExist:
        raise Http404('El ejercicio no existe')

    if request.method == 'POST':
        _, error = api_service.eliminar_ejercicio(ejercicio_id)
        ejercicio.delete()
        if error:
            messages.warning(request, 'El microservicio no está disponible: ejercicio eliminado solo en la base local.')
        else:
            messages.success(request, f'Ejercicio eliminado de {api_service.etiqueta_conexion()}.')
        return redirect('gym:index')
    return render(request, 'gym/delete.html', {'ejercicio': ejercicio})
