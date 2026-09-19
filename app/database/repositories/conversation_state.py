from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import ConversationState


class ConversationStateRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, telegram_user_id: int) -> ConversationState | None:
        stmt = select(ConversationState).where(ConversationState.telegram_user_id == telegram_user_id)
        return self.session.scalar(stmt)

    def upsert(self, telegram_user_id: int, state_data: dict) -> ConversationState:
        state = self.get(telegram_user_id)
        if state is None:
            state = ConversationState(telegram_user_id=telegram_user_id, state_data=state_data)
        else:
            state.state_data = state_data
        self.session.add(state)
        self.session.flush()
        return state
