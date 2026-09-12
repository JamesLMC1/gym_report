from django.shortcuts import render, get_object_or_404, redirect
from .models import Workout
from .forms import WorkoutForm


def index(request):
    latest = Workout.objects.all()[:5]
    return render(request, "workouts/index.html", {"workouts": latest})


def detail(request, workout_id):
    w = get_object_or_404(Workout, pk=workout_id)
    return render(request, "workouts/detail.html", {"workout": w})


def create(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('workouts:index')
    else:
        form = WorkoutForm()
    return render(request, "workouts/create.html", {"form": form})
