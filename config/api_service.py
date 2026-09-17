import urllib.request
import json

API_BASE = "https://microserviciogym.onrender.com"


def get_ejercicios():
    try:
        r = urllib.request.urlopen(f"{API_BASE}/ejercicios", timeout=10)
        return json.loads(r.read())
    except Exception:
        return []


def get_ejercicio(ejercicio_id):
    try:
        r = urllib.request.urlopen(f"{API_BASE}/ejercicios/{ejercicio_id}", timeout=10)
        return json.loads(r.read())
    except Exception:
        return None


def get_rutinas():
    try:
        r = urllib.request.urlopen(f"{API_BASE}/rutinas", timeout=10)
        return json.loads(r.read())
    except Exception:
        return []


def get_rutina(rutina_id):
    try:
        r = urllib.request.urlopen(f"{API_BASE}/rutinas/{rutina_id}", timeout=10)
        return json.loads(r.read())
    except Exception:
        return None


def get_comidas():
    try:
        r = urllib.request.urlopen(f"{API_BASE}/comidas", timeout=10)
        return json.loads(r.read())
    except Exception:
        return []


def get_comida(comida_id):
    try:
        r = urllib.request.urlopen(f"{API_BASE}/comidas/{comida_id}", timeout=10)
        return json.loads(r.read())
    except Exception:
        return None
