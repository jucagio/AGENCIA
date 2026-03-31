import html
import traceback

from telegram import Update
from telegram.ext import ContextTypes

from src.utils.logger import logger


async def handle_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log de errores no capturados en los handlers."""
    logger.error(
        "unhandled_exception",
        error=str(context.error),
        traceback=traceback.format_exc(),
    )
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "Ocurrió un error inesperado. Intenta de nuevo en un momento."
        )
