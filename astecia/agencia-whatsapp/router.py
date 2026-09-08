"""
AGENCIA — Router de Agentes
Sasha @ Programadora Senior

Detecta a qué agente va dirigido el mensaje de Juan Camilo
y lo procesa con Claude API usando el system prompt correcto.

Uso:
  @jarvis  → Gerente de Programación
  @jade    → Inteligencia y Capacitaciones
  @ego     → Auditor Supremo
  @sasha   → Programadora Senior
  @brook   → Frontend y Dashboards
  @erik    → Diseño
  @cinthya → Automatización

Sin @mención → Jarvis responde por defecto
"""

import os
import re
import anthropic
from agents.prompts import AGENT_PROMPTS
from history import get_history, save_message

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Modelo por agente (clasificación de Jade)
AGENT_MODELS = {
    "jarvis":  "claude-opus-4-5",
    "ego":     "claude-opus-4-5",
    "sasha":   "claude-opus-4-5",
    "jade":    "claude-sonnet-4-5",
    "brook":   "claude-sonnet-4-5",
    "erik":    "claude-sonnet-4-5",
    "cinthya": "claude-sonnet-4-5",
}

AGENT_NAMES = list(AGENT_MODELS.keys())

# Límite de tokens de respuesta por WhatsApp (1600 chars aprox)
MAX_TOKENS = 1024


def detect_agent(message: str) -> tuple[str, str]:
    """
    Detecta si el mensaje tiene @mención a un agente.
    Devuelve (agente, mensaje_limpio).
    Si no hay mención → Jarvis por defecto.
    """
    pattern = r"^@(\w+)\s*(.*)"
    match = re.match(pattern, message, re.DOTALL | re.IGNORECASE)
    if match:
        mention = match.group(1).lower()
        clean_msg = match.group(2).strip()
        if mention in AGENT_NAMES:
            return mention, clean_msg
    return "jarvis", message


async def route_message(message: str, media_url: str | None = None) -> str:
    """
    Enruta el mensaje al agente correcto y devuelve la respuesta.
    """
    agent, clean_message = detect_agent(message)

    # Agregar nota de media si existe
    if media_url:
        clean_message += f"\n[Juan Camilo adjuntó un archivo: {media_url}]"

    # Recuperar historial de conversación del agente
    history = get_history(agent)

    # Agregar mensaje del usuario al historial
    history.append({"role": "user", "content": clean_message})

    try:
        response = client.messages.create(
            model=AGENT_MODELS[agent],
            max_tokens=MAX_TOKENS,
            system=AGENT_PROMPTS[agent],
            messages=history,
        )
        reply = response.content[0].text

        # Guardar en historial
        save_message(agent, "user", clean_message)
        save_message(agent, "assistant", reply)

        # Prefijo de identificación del agente
        agent_prefix = {
            "jarvis":  "🤖 *Jarvis*",
            "jade":    "🌿 *Jade*",
            "ego":     "👁️ *Ego*",
            "sasha":   "🔐 *Sasha*",
            "brook":   "🖥️ *Brook*",
            "erik":    "🎨 *Erik*",
            "cinthya": "⚙️ *Cinthya*",
        }
        return f"{agent_prefix[agent]}\n\n{reply}"

    except Exception as e:
        return f"❌ Error en el agente {agent.capitalize()}: {str(e)}"
