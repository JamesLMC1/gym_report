from django.contrib import admin
from .models import Set

# ==============================================================================
# CONFIGURACIÓN DEL PANEL DE ADMINISTRACIÓN PARA EL MODELO SET
# ==============================================================================
# Registra el modelo Set en el panel de administración de Django.
# Esto permite crear, editar y eliminar sets desde http://localhost:8000/admin/
#
# Sin personalización adicional, el admin muestra:
# - Lista de todos los sets con sus campos
# - Formulario para crear nuevos sets
# - Opciones de búsqueda y filtrado básicas
# ==============================================================================
admin.site.register(Set)
