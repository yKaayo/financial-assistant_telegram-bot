import logging

from sqlalchemy.orm import Session

from app.database.repositories import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = UserRepository(session)

    def get_or_create(self, telegram_user_id: int, username: str | None, first_name: str | None):
        user = self.repository.get_by_telegram_user_id(telegram_user_id)
        if user is None:
            user = self.repository.create(telegram_user_id=telegram_user_id, username=username, first_name=first_name)
            logger.info("User created telegram_user_id=%s", telegram_user_id)
        elif user.username != username or user.first_name != first_name:
            user.username = username
            user.first_name = first_name
            self.session.add(user)
        self.session.commit()
        return user
