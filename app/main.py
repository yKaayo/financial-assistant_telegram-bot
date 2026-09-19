import logging

from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters

from app.bot.handlers import callback_handler, message_handler, start_handler
from app.config.logging import setup_logging
from app.config.settings import settings
from app.database.database import SessionLocal, engine
from app.database.models import Base

logger = logging.getLogger(__name__)


def init_database() -> None:
    Base.metadata.create_all(bind=engine)


def build_app() -> Application:
    application = Application.builder().token(settings.telegram_bot_token).build()
    application.bot_data["db_session_factory"] = SessionLocal
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    return application


def main() -> None:
    setup_logging(settings.log_level)
    logger.info("Starting bot")
    init_database()
    app = build_app()
    app.run_polling()


if __name__ == "__main__":
    main()
