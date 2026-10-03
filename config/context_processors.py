from config import api_service


def microservicios(request):
    """Expone la lista de microservicios configurados a todas las plantillas."""
    return {"microservicios": api_service.microservicios()}
