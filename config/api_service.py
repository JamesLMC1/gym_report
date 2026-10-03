import json
import logging
import threading
import time
import urllib.error
import urllib.request
from decimal import Decimal

from config.env import get_env

logger = logging.getLogger(__name__)

DEFAULT_PRIMARY = "https://microserviciogym.onrender.com"
TIMEOUT = float(get_env("MICROSERVICE_TIMEOUT", "15") or 15)
COOLDOWN = float(get_env("MICROSERVICE_COOLDOWN", "30") or 30)

# Circuit breaker simple: {base_url: timestamp_hasta_el_que_se_omite}
_failed_until = {}

# Última conexión por hilo (para saber qué microservicio respondió)
_local = threading.local()


def _label(base):
    """Etiqueta legible del microservicio según su URL."""
    host = base.replace("https://", "").replace("http://", "").strip("/")
    if "micro-python" in host:
        return "Python (FastAPI)"
    if "micro-java" in host:
        return "Java (Spring Boot)"
    if "micro-go" in host:
        return "Go"
    if "microserviciogym" in host:
        return "Node (Express)"
    return host


def microservicios():
    """Lista de microservicios configurados (primario + respaldos)."""
    return [
        {"url": base, "label": _label(base), "primario": index == 0}
        for index, base in enumerate(_bases())
    ]


def ultima_conexion():
    """Info del último microservicio contactado en este hilo."""
    return {
        "url": getattr(_local, "url", None),
        "label": getattr(_local, "label", None),
        "ok": getattr(_local, "ok", False),
    }


def etiqueta_conexion():
    """Etiqueta del microservicio que respondió, o 'microservicio' si falló."""
    return getattr(_local, "label", None) or "microservicio"


def _bases():
    """Bases en orden de preferencia: primaria + respaldos (otro lenguaje)."""
    primary = (get_env("MICROSERVICE_PRIMARY_URL", DEFAULT_PRIMARY) or DEFAULT_PRIMARY).strip()
    fallbacks_raw = get_env("MICROSERVICE_FALLBACK_URLS", "") or ""
    fallbacks = [u.strip() for u in fallbacks_raw.split(",") if u.strip()]

    bases = []
    for base in [primary, *fallbacks]:
        base = base.rstrip("/")
        if base and base not in bases:
            bases.append(base)
    return bases


def _default(o):
    if isinstance(o, Decimal):
        return float(o)
    return str(o)


def _do_request(base, method, path, payload):
    req = urllib.request.Request(f"{base}{path}", data=payload, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        raw = r.read()
        return json.loads(raw) if raw else None


def _request(method, path, data=None):
    """Llama al microservicio primario y, si falla, a los de respaldo.

    Devuelve (data, error). Aplica un circuit breaker para no golpear
    repetidamente una base caída durante COOLDOWN segundos.
    """
    payload = None
    if data is not None:
        payload = json.dumps(data, default=_default).encode("utf-8")

    bases = _bases()
    if not bases:
        return None, "No hay microservicios configurados."

    now = time.monotonic()
    candidatas = [b for b in bases if _failed_until.get(b, 0) <= now] or bases
    last_error = "Ningún microservicio respondió."

    _local.url = None
    _local.label = None
    _local.ok = False

    for base in candidatas:
        try:
            result = _do_request(base, method, path, payload)
            _failed_until.pop(base, None)
            _local.url = base
            _local.label = _label(base)
            _local.ok = True
            logger.info("Microservicio %s respondió %s %s.", base, method, path)
            return result, None
        except urllib.error.HTTPError as e:
            detalle = e.read().decode("utf-8", errors="replace")
            last_error = f"Error del microservicio ({e.code}): {detalle}"
            if e.code >= 500:
                _failed_until[base] = time.monotonic() + COOLDOWN
            logger.warning("Falló %s %s %s: %s", base, method, path, last_error)
        except Exception as e:
            last_error = f"No se pudo conectar con el microservicio: {e}"
            _failed_until[base] = time.monotonic() + COOLDOWN
            logger.warning("Falló %s %s %s: %s", base, method, path, last_error)

    return None, last_error


# ------------------------- Lectura (GET) -------------------------
def get_ejercicios():
    data, _ = _request("GET", "/ejercicios")
    return data or []


def get_ejercicio(ejercicio_id):
    data, _ = _request("GET", f"/ejercicios/{ejercicio_id}")
    return data


def get_rutinas():
    data, _ = _request("GET", "/rutinas")
    return data or []


def get_rutina(rutina_id):
    data, _ = _request("GET", f"/rutinas/{rutina_id}")
    return data


def get_comidas():
    data, _ = _request("GET", "/comidas")
    return data or []


def get_comida(comida_id):
    data, _ = _request("GET", f"/comidas/{comida_id}")
    return data


# ------------------------- Escritura (POST/PUT/DELETE) -------------------------
def crear_ejercicio(data):
    return _request("POST", "/ejercicios", data)


def actualizar_ejercicio(ejercicio_id, data):
    return _request("PUT", f"/ejercicios/{ejercicio_id}", data)


def eliminar_ejercicio(ejercicio_id):
    return _request("DELETE", f"/ejercicios/{ejercicio_id}")


def crear_rutina(data):
    return _request("POST", "/rutinas", data)


def actualizar_rutina(rutina_id, data):
    return _request("PUT", f"/rutinas/{rutina_id}", data)


def eliminar_rutina(rutina_id):
    return _request("DELETE", f"/rutinas/{rutina_id}")


def crear_comida(data):
    return _request("POST", "/comidas", data)


def actualizar_comida(comida_id, data):
    return _request("PUT", f"/comidas/{comida_id}", data)


def eliminar_comida(comida_id):
    return _request("DELETE", f"/comidas/{comida_id}")
