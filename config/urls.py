from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('accounts.urls')),
    path('registro/', include('registro.urls')),
    path('gym/', include('gym.urls')),
    path('workouts/', include('workouts.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('dietas/', include('dietas.urls')),
    path('chat/', include('chat.urls')),
    path('profesores/', include('profesores_involucrados.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
