from django.db import models


def flow_status(request):
    from usuarios.models import Usuario
    from gym.models import Set

    tiene_usuarios = Usuario.objects.exists()
    tiene_ejercicios = Set.objects.exists()

    return {
        "tiene_usuarios": tiene_usuarios,
        "tiene_ejercicios": tiene_ejercicios,
    }
