from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Profesor


@login_required
def index(request):
    """Lista todos los docentes involucrados con su foto."""
    return render(request, 'profesores_involucrados/index.html', {'profesores': Profesor.objects.all()})
