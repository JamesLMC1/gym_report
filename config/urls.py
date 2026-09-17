from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gym/', include('gym.urls')),
    path('workouts/', include('workouts.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('dietas/', include('dietas.urls')),
]
