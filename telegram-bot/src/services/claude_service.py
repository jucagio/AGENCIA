import anthropic
from telegram import Message as TelegramMessage

from src.agents.registry import get_agent, load_system_prompt
from src.config.settings import settings
from src.services.session_service import SessionService
from src.utils.logger import logger

_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

# Singleton de sesiones compartido en toda la app
session_service = SessionService(max_messages=settings.MAX_HISTORY_MESSAGES)

EDIT_EVERY_N_CHARS = 100  # editar el mensaje placeholder cada N chars acumulados


async def stream_agent_response(
    user_id: int,
    agent_name: str,
    user_content: str,
    placeholder: TelegramMessage,
    ultrathink: bool = False,
) -> str:
    """
    Llama a Claude API con streaming y edita el placeholder de Telegram en tiempo real.
    Retorna el texto completo de la respuesta.
    """
    agent = get_agent(agent_name)
    if agent is None:
        raise ValueError(f"Agente '{agent_name}' no existe en el registro")

    system_prompt = load_system_prompt(agent_name)
    history = session_service.get_history(user_id, agent_name)

    # Agregar el mensaje del usuario al historial y construir messages para la API
    session_service.add_message(user_id, agent_name, "user", user_content)
    messages = history + [{"role": "user", "content": user_content}]

    accumulated = ""
    last_edit_at = 0

    # Construir kwargs para la API; extended thinking si ultrathink activo
    api_kwargs: dict = dict(
        model=agent.model,
        max_tokens=16384 if ultrathink else 4096,
        system=system_prompt,
        messages=messages,
    )
    if ultrathink:
        api_kwargs["thinking"] = {"type": "enabled", "budget_tokens": 10000}

    try:
        with _client.messages.stream(**api_kwargs) as stream:
            for chunk in stream.text_stream:
                accumulated += chunk
                if len(accumulated) - last_edit_at >= EDIT_EVERY_N_CHARS:
                    await _safe_edit(
                        placeholder,
                        f"_{agent.display_name} esta escribiendo..._\n\n{accumulated}",
                    )
                    last_edit_at = len(accumulated)

    except anthropic.APIError as exc:
        logger.error("anthropic_api_error", agent=agent_name, error=str(exc))
        raise

    final_text = f"*{agent.display_name}* {agent.emoji}\n\n{accumulated}"
    await _safe_edit(placeholder, final_text)

    session_service.add_message(user_id, agent_name, "assistant", accumulated)
    logger.info("response_complete", agent=agent_name, chars=len(accumulated))

    return accumulated


async def _safe_edit(message: TelegramMessage, text: str) -> None:
    """Edita el mensaje de Telegram; ignora errores de flood control o sin cambios."""
    from src.utils.telegram_helpers import MAX_MESSAGE_LEN

    display = text[:MAX_MESSAGE_LEN]
    try:
        await message.edit_text(display, parse_mode="Markdown")
    except Exception:
        try:
            # Fallback: sin Markdown por si hay caracteres especiales sin escapar
            await message.edit_text(display)
        except Exception:
            pass  # Ignorar (flood control, mensaje no cambio, etc.)
