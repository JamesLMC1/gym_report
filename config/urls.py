from django.contrib import admin
from django.urls import path, include

from config.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('accounts.urls')),
    path('gym/', include('gym.urls')),
    path('workouts/', include('workouts.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('dietas/', include('dietas.urls')),
    path('chat/', include('chat.urls')),
]
