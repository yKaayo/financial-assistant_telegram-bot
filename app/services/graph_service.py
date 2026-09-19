import logging

from sqlalchemy.orm import Session

from app.graph.graph import BotGraph
from app.graph.state import BotState
from app.services.conversation_service import ConversationService
from app.services.task_service import TaskService

logger = logging.getLogger(__name__)


class GraphService:
    def __init__(self, session: Session) -> None:
        self.conversation = ConversationService(session)
        self.task_service = TaskService(session)
        self.graph = BotGraph(self.task_service)

    def process_event(self, telegram_user_id: int, chat_id: int, event_type: str, event_value: str) -> BotState:
        previous = self.conversation.load_state(telegram_user_id)
        state: BotState = {
            **previous,
            "user_id": telegram_user_id,
            "chat_id": chat_id,
            "event_type": event_type,  # type: ignore[assignment]
            "event_value": event_value,
        }
        try:
            result = self.graph.run(state)
        except Exception:
            logger.exception("Unexpected graph error telegram_user_id=%s", telegram_user_id)
            result = {
                **state,
                "action": "menu",
                "step": "idle",
                "data": {},
                "response_kind": "error",
                "response_text": "❌ Não consegui concluir essa operação.\n\nTente novamente ou volte ao menu.",
            }
        self.conversation.save_state(telegram_user_id, {
            "action": result.get("action", "menu"),
            "step": result.get("step", "idle"),
            "data": result.get("data", {}),
        })
        return result
