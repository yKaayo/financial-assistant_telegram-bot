from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_telegram_user_id(self, telegram_user_id: int) -> User | None:
        stmt = select(User).where(User.telegram_user_id == telegram_user_id)
        return self.session.scalar(stmt)

    def create(self, telegram_user_id: int, username: str | None, first_name: str | None) -> User:
        user = User(telegram_user_id=telegram_user_id, username=username, first_name=first_name)
        self.session.add(user)
        self.session.flush()
        return user
