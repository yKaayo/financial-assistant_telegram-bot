from sqlalchemy.orm import Session

from app.database.repositories import ConversationStateRepository


class ConversationService:
    def __init__(self, session: Session) -> None:
        self.repository = ConversationStateRepository(session)
        self.session = session

    def load_state(self, telegram_user_id: int) -> dict:
        row = self.repository.get(telegram_user_id)
        return row.state_data if row else {}

    def save_state(self, telegram_user_id: int, state: dict) -> None:
        self.repository.upsert(telegram_user_id=telegram_user_id, state_data=state)
        self.session.commit()

    def clear_state(self, telegram_user_id: int) -> None:
        self.save_state(telegram_user_id=telegram_user_id, state={})
