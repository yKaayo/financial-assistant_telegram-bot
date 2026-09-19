from telegram import Update
from telegram.ext import ContextTypes

from app.bot.handlers.utils import send_graph_response
from app.services import GraphService


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user is None or update.effective_chat is None or update.message is None:
        return
    session = context.application.bot_data["db_session_factory"]()
    try:
        graph_service = GraphService(session)
        state = graph_service.process_event(
            telegram_user_id=update.effective_user.id,
            chat_id=update.effective_chat.id,
            event_type="message",
            event_value=update.message.text or "",
        )
        await send_graph_response(update, state)
    finally:
        session.close()
