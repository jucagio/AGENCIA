from telegram.ext import Application, MessageHandler, filters

from src.config.settings import settings
from src.handlers.error_handler import handle_error
from src.handlers.message_handler import handle_message
from src.utils.logger import logger, setup_logging


def main() -> None:
    setup_logging(settings.LOG_LEVEL)
    logger.info("starting_bot", environment=settings.ENVIRONMENT)

    app = (
        Application.builder()
        .token(settings.TELEGRAM_TOKEN)
        .build()
    )

    # Manejar todos los mensajes de texto (con y sin @mention, con y sin comando)
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(handle_error)

    logger.info("bot_polling")
    app.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()
