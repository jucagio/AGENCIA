from telegram import Update
from telegram.ext import ContextTypes

from src.agents.registry import get_agent
from src.config.settings import settings
from src.services.claude_service import stream_agent_response, session_service
from src.services.rate_limiter import RateLimiter
from src.utils.logger import logger
from src.utils.mention_parser import parse_message

_rate_limiter = RateLimiter(
    max_messages=settings.RATE_LIMIT_MESSAGES,
    window_seconds=settings.RATE_LIMIT_WINDOW_SECONDS,
)

_HELP_TEXT = (
    "Menciona a un agente para comenzar:\n\n"
    "🤖 @jarvis — Gerente de Programación\n"
    "🔮 @jade — Inteligencia & Capacitaciones\n"
    "💻 @sasha — Programadora & Seguridad\n"
    "🌊 @brook — Frontend & BD\n"
    "🎨 @erik — Diseño\n"
    "⚙️ @cinthya — Automatización\n"
    "👁 @ego — Auditor Supremo\n\n"
    "Tip: agrega *Ultrathink* para análisis más profundo."
)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    text = (update.message.text or "").strip()

    # Solo Juan Camilo puede usar el bot
    if user_id not in settings.ALLOWED_USER_IDS:
        await update.message.reply_text("Acceso no autorizado.")
        return

    # Rate limiting
    if not _rate_limiter.allow(user_id):
        await update.message.reply_text(
            "Demasiados mensajes en poco tiempo. Espera un momento."
        )
        return

    # Comandos de control
    if text.startswith("/"):
        await _handle_command(update, text)
        return

    # Parsear @mention
    parsed = parse_message(text)

    if not parsed.agent_name:
        await update.message.reply_text(_HELP_TEXT, parse_mode="Markdown")
        return

    agent = get_agent(parsed.agent_name)
    if agent is None:
        await update.message.reply_text(
            f"Agente '@{parsed.agent_name}' no encontrado. {_HELP_TEXT}",
            parse_mode="Markdown",
        )
        return

    if not parsed.content:
        await update.message.reply_text(
            f"Escribe un mensaje después de @{agent.name}. Ej: `@{agent.name} hola`",
            parse_mode="Markdown",
        )
        return

    logger.info(
        "dispatch_agent",
        user_id=user_id,
        agent=agent.name,
        ultrathink=parsed.has_ultrathink,
        content_len=len(parsed.content),
    )

    placeholder = await update.message.reply_text(
        f"_{agent.display_name} está pensando..._",
        parse_mode="Markdown",
    )

    try:
        await stream_agent_response(
            user_id=user_id,
            agent_name=parsed.agent_name,
            user_content=parsed.content,
            placeholder=placeholder,
            ultrathink=parsed.has_ultrathink,
        )
    except Exception as exc:
        logger.error("stream_failed", agent=parsed.agent_name, error=str(exc))
        await placeholder.edit_text(
            "Error al procesar la solicitud. Intenta de nuevo."
        )


async def _handle_command(update: Update, text: str) -> None:
    """Comandos de control del bot."""
    parts = text.split()
    cmd = parts[0].lower()

    if cmd == "/start" or cmd == "/help":
        await update.message.reply_text(_HELP_TEXT, parse_mode="Markdown")

    elif cmd == "/reset":
        user_id = update.effective_user.id
        if len(parts) > 1:
            # /reset @jarvis — limpia solo ese agente
            agent_name = parts[1].lstrip("@").lower()
            session_service.clear(user_id, agent_name)
            await update.message.reply_text(f"Contexto de @{agent_name} borrado.")
        else:
            # /reset — limpia todos los agentes
            session_service.clear_all(user_id)
            await update.message.reply_text("Contexto de todos los agentes borrado.")

    elif cmd == "/agents":
        await update.message.reply_text(_HELP_TEXT, parse_mode="Markdown")
