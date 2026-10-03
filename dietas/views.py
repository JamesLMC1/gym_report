import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from config import api_service
from .forms import ComidaForm
from .models import Comida

CAMPOS = ('nombre', 'tipo', 'calorias', 'proteinas_g', 'carbos_g', 'grasas_g', 'receta')


def _body(form):
    return {campo: form.cleaned_data.get(campo) for campo in CAMPOS}


def _crear_local(datos):
    """Crea la comida solo en la BD local (microservicio no disponible)."""
    return Comida.objects.create(id=uuid.uuid4(), created_at=timezone.now(), **datos)


def _actualizar_local(comida, datos):
    for campo, valor in datos.items():
        setattr(comida, campo, valor)
    comida.save()
    return comida


def sincronizar_comida(item):
    if not item or not item.get('id'):
        return None
    obj, _ = Comida.objects.update_or_create(
        id=item['id'],
        defaults={
            'nombre': item.get('nombre') or '',
            'tipo': item.get('tipo') or '',
            'calorias': item.get('calorias'),
            'proteinas_g': item.get('proteinas_g'),
            'carbos_g': item.get('carbos_g'),
            'grasas_g': item.get('grasas_g'),
            'receta': item.get('receta') or '',
            'created_at': item.get('created_at'),
        },
    )
    return obj


@login_required
def index(request):
    """Página principal: muestra las últimas 5 comidas registradas."""
    latest = Comida.objects.all()[:5]
    return render(request, 'dietas/index.html', {'latest': latest})


@login_required
def all(request):
    """Lista todas las comidas guardadas en la base de datos local."""
    comidas = Comida.objects.all()
    return render(request, 'dietas/all.html', {'comidas': comidas})


@login_required
def detail(request, comida_id):
    """Muestra el detalle de una comida; lanza 404 si no existe."""
    try:
        comida = Comida.objects.get(pk=comida_id)
    except Comida.DoesNotExist:
        raise Http404('La comida no existe')
    return render(request, 'dietas/detail.html', {'comida': comida})


@login_required
def catalogo(request):
    """Muestra el catálogo en vivo del microservicio (sin guardar nada)."""
    items = api_service.get_comidas()
    if items:
        guardados = {str(pk) for pk in Comida.objects.values_list('id', flat=True)}
        for item in items:
            item['guardado'] = str(item.get('id')) in guardados
        messages.success(
            request,
            f'Catálogo cargado: {len(items)} comidas desde {api_service.etiqueta_conexion()}. '
            f'Usa "Guardar" para añadirlas a tu lista.',
        )
    else:
        messages.error(request, 'No se pudo cargar el catálogo de comidas desde el microservicio.')
    return render(request, 'dietas/catalogo_comidas.html', {'comidas': items or []})


@login_required
@require_POST
def guardar(request, comida_id):
    """Guarda en la BD local una comida traída del catálogo."""
    item = api_service.get_comida(comida_id)
    if not item:
        messages.error(request, 'No se pudo obtener la comida del microservicio para guardarla.')
    else:
        sincronizar_comida(item)
        messages.success(request, f'Comida guardada en tu lista desde {api_service.etiqueta_conexion()}.')
    return redirect('dietas:catalogo')


@login_required
def create(request):
    """Registra una comida: la crea en el microservicio y/o en la BD local."""
    if request.method == 'POST':
        form = ComidaForm(request.POST)
        if form.is_valid():
            datos = _body(form)
            creado, error = api_service.crear_comida(datos)
            if creado:
                sincronizar_comida(creado)
                messages.success(request, f'Comida creada en {api_service.etiqueta_conexion()}.')
            else:
                _crear_local(datos)
                messages.warning(request, 'El microservicio no está disponible: comida guardada solo en la base local.')
            return redirect('dietas:index')
    else:
        form = ComidaForm()
    return render(request, 'dietas/form.html', {'form': form, 'titulo': 'Registrar Comida'})


@login_required
def edit(request, comida_id):
    """Edita una comida existente en el microservicio y/o en la BD local."""
    try:
        comida = Comida.objects.get(pk=comida_id)
    except Comida.DoesNotExist:
        raise Http404('La comida no existe')

    if request.method == 'POST':
        form = ComidaForm(request.POST, instance=comida)
        if form.is_valid():
            datos = _body(form)
            actualizado, error = api_service.actualizar_comida(comida_id, datos)
            if actualizado:
                sincronizar_comida(actualizado)
                messages.success(request, f'Comida actualizada en {api_service.etiqueta_conexion()}.')
            else:
                _actualizar_local(comida, datos)
                messages.warning(request, 'El microservicio no está disponible: cambios guardados solo en la base local.')
            return redirect('dietas:detail', comida_id=comida.id)
    else:
        form = ComidaForm(instance=comida)
    return render(request, 'dietas/form.html', {'form': form, 'titulo': 'Editar Comida'})


@login_required
def delete(request, comida_id):
    """Confirma y elimina una comida del microservicio y de la BD local."""
    try:
        comida = Comida.objects.get(pk=comida_id)
    except Comida.DoesNotExist:
        raise Http404('La comida no existe')

    if request.method == 'POST':
        _, error = api_service.eliminar_comida(comida_id)
        comida.delete()
        if error:
            messages.warning(request, 'El microservicio no está disponible: comida eliminada solo en la base local.')
        else:
            messages.success(request, f'Comida eliminada de {api_service.etiqueta_conexion()}.')
        return redirect('dietas:index')
    return render(request, 'dietas/delete.html', {'comida': comida})
