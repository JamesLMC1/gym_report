import json
import urllib.error
import urllib.request
from pathlib import Path

from django.contrib import messages
from django.shortcuts import redirect, render

from config.env import get_env
from .models import ChatMessage

PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "asistente_gym.md"
HISTORY_LIMIT = 20

DEFAULT_SYSTEM_PROMPT = (
    "Eres un asistente de gimnasio. Respondes solo preguntas sobre "
    "entrenamiento, ejercicios, rutinas y nutrición básica, en español y de forma corta."
)


def _system_prompt():
    try:
        return PROMPT_PATH.read_text(encoding="utf-8")
    except OSError:
        return DEFAULT_SYSTEM_PROMPT


def _session_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def _call_deepseek(question, history, session_id):
    api_key = get_env("OPENCODE_API_KEY")
    if not api_key:
        return None, "Falta la variable OPENCODE_API_KEY en el archivo .env"

    model = get_env("OPENCODE_MODEL", "deepseek-v4-flash")
    base_url = get_env("OPENCODE_BASE_URL", "https://opencode.ai/zen/v1").rstrip("/")

    msgs = [{"role": "system", "content": _system_prompt()}]
    msgs.extend({"role": m.role, "content": m.content} for m in history)
    msgs.append({"role": "user", "content": question})

    payload = json.dumps({"model": model, "messages": msgs}).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "GymChat/1.0",
            "x-opencode-session": session_id,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
        return data["choices"][0]["message"]["content"], None
    except urllib.error.HTTPError as e:
        detalle = e.read().decode("utf-8", errors="replace")
        return None, f"Error de la API ({e.code}): {detalle}"
    except Exception as e:
        return None, f"No se pudo conectar con el modelo: {e}"


def index(request):
    if request.method == "POST":
        pregunta = request.POST.get("pregunta", "").strip()
        if not pregunta:
            messages.error(request, "Escribe una pregunta antes de enviarla.")
            return redirect("chat:index")

        qs = ChatMessage.objects.all()
        historial = list(qs[max(0, qs.count() - HISTORY_LIMIT):])
        respuesta, error = _call_deepseek(pregunta, historial, _session_id(request))

        if error:
            messages.error(request, error)
        else:
            ChatMessage.objects.create(role="user", content=pregunta)
            ChatMessage.objects.create(role="assistant", content=respuesta)

        return redirect("chat:index")

    mensajes = ChatMessage.objects.all()
    return render(request, "chat/index.html", {"mensajes": mensajes})


def limpiar(request):
    if request.method == "POST":
        ChatMessage.objects.all().delete()
    return redirect("chat:index")
