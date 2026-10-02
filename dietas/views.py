from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render

from config import api_service
from .forms import ComidaForm
from .models import Comida

CAMPOS = ('nombre', 'tipo', 'calorias', 'proteinas_g', 'carbos_g', 'grasas_g', 'receta')


def _body(form):
    return {campo: form.cleaned_data.get(campo) for campo in CAMPOS}


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
    latest = Comida.objects.all()[:5]
    return render(request, 'dietas/index.html', {'latest': latest})


@login_required
def all(request):
    comidas = Comida.objects.all()
    return render(request, 'dietas/all.html', {'comidas': comidas})


@login_required
def detail(request, comida_id):
    try:
        comida = Comida.objects.get(pk=comida_id)
    except Comida.DoesNotExist:
        raise Http404('La comida no existe')
    return render(request, 'dietas/detail.html', {'comida': comida})


@login_required
def catalogo(request):
    items = api_service.get_comidas()
    if items:
        for item in items:
            sincronizar_comida(item)
        messages.success(request, f'Catálogo sincronizado: {len(items)} comidas del microservicio.')
    else:
        messages.error(request, 'No se pudo cargar el catálogo de comidas.')
    comidas = Comida.objects.all()
    return render(request, 'dietas/catalogo_comidas.html', {'comidas': comidas})


@login_required
def create(request):
    if request.method == 'POST':
        form = ComidaForm(request.POST)
        if form.is_valid():
            creado, error = api_service.crear_comida(_body(form))
            if error:
                messages.error(request, error)
            elif not creado:
                messages.error(request, 'El microservicio no devolvió la comida creada.')
            else:
                sincronizar_comida(creado)
                messages.success(request, 'Comida creada y sincronizada.')
                return redirect('dietas:index')
    else:
        form = ComidaForm()
    return render(request, 'dietas/form.html', {'form': form, 'titulo': 'Registrar Comida'})


@login_required
def edit(request, comida_id):
    try:
        comida = Comida.objects.get(pk=comida_id)
    except Comida.DoesNotExist:
        raise Http404('La comida no existe')

    if request.method == 'POST':
        form = ComidaForm(request.POST, instance=comida)
        if form.is_valid():
            actualizado, error = api_service.actualizar_comida(comida_id, _body(form))
            if error:
                messages.error(request, error)
            else:
                if actualizado:
                    sincronizar_comida(actualizado)
                else:
                    form.save()
                messages.success(request, 'Comida actualizada en el microservicio.')
                return redirect('dietas:detail', comida_id=comida.id)
    else:
        form = ComidaForm(instance=comida)
    return render(request, 'dietas/form.html', {'form': form, 'titulo': 'Editar Comida'})


@login_required
def delete(request, comida_id):
    try:
        comida = Comida.objects.get(pk=comida_id)
    except Comida.DoesNotExist:
        raise Http404('La comida no existe')

    if request.method == 'POST':
        _, error = api_service.eliminar_comida(comida_id)
        if error:
            messages.error(request, error)
        else:
            comida.delete()
            messages.success(request, 'Comida eliminada del microservicio.')
            return redirect('dietas:index')
    return render(request, 'dietas/delete.html', {'comida': comida})
