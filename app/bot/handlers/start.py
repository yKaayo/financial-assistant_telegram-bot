import logging

from telegram import Update
from telegram.ext import ContextTypes

from app.services import GraphService, UserService

logger = logging.getLogger(__name__)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user is None or update.effective_chat is None or update.message is None:
        return

    session = context.application.bot_data["db_session_factory"]()
    try:
        user_service = UserService(session)
        graph_service = GraphService(session)
        user = update.effective_user
        user_service.get_or_create(user.id, user.username, user.first_name)
        state = graph_service.process_event(user.id, update.effective_chat.id, "callback", "start")
        from app.bot.handlers.utils import send_graph_response

        await send_graph_response(update, state)
        logger.info("Start handled telegram_user_id=%s", user.id)
    finally:
        session.close()
