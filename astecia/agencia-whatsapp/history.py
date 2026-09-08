"""
AGENCIA — Historial de Conversación
Sasha @ Programadora Senior

Mantiene el historial de conversación por agente en memoria.
Máximo 20 mensajes por agente (10 turnos) para no saturar el contexto.
"""

from collections import defaultdict

# Historial en memoria: { agente: [{"role": ..., "content": ...}] }
_history: dict[str, list[dict]] = defaultdict(list)

MAX_MESSAGES_PER_AGENT = 20  # 10 turnos (user + assistant)


def get_history(agent: str) -> list[dict]:
    """Devuelve una copia del historial del agente."""
    return list(_history[agent])


def save_message(agent: str, role: str, content: str) -> None:
    """Guarda un mensaje en el historial del agente."""
    _history[agent].append({"role": role, "content": content})

    # Mantener solo los últimos MAX_MESSAGES_PER_AGENT mensajes
    if len(_history[agent]) > MAX_MESSAGES_PER_AGENT:
        _history[agent] = _history[agent][-MAX_MESSAGES_PER_AGENT:]


def clear_history(agent: str) -> None:
    """Limpia el historial de un agente específico."""
    _history[agent] = []


def clear_all_history() -> None:
    """Limpia el historial de todos los agentes."""
    _history.clear()
