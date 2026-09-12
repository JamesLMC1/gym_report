from django.shortcuts import render, get_object_or_404, redirect
from .models import Set
from .forms import SetForm


def index(request):
    latest_set_list = Set.objects.all()[:5]
    return render(request, "gym/index.html", {"sets": latest_set_list})


def all(request):
    all_sets = Set.objects.all()
    return render(request, "gym/all.html", {"sets": all_sets})


def detail(request, set_id):
    set_obj = get_object_or_404(Set, pk=set_id)
    return render(request, "gym/detail.html", {"set": set_obj})


def by_exercise(request, exercise_name):
    sets = Set.objects.filter(nombre_ejercicio__icontains=exercise_name)
    return render(request, "gym/by_exercise.html", {"sets": sets, "exercise_name": exercise_name})


def create(request):
    if request.method == 'POST':
        form = SetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gym:all')
    else:
        form = SetForm()
    return render(request, "gym/create.html", {"form": form})
