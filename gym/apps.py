from django.apps import AppConfig


class GymConfig(AppConfig):
    # Tipo de campo para la clave primaria automática (id)
    # BigAutoField crea enteros grandes (BigInt), ideal para tablas que crecerán mucho
    default_auto_field = 'django.db.models.BigAutoField'

    # Nombre interno de la app que Django usa para identificarla
    # Debe coincidir con el nombre de la carpeta
    name = 'gym'
