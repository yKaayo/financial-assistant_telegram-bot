from sqlalchemy import BigInteger, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base, TimestampMixin


class ConversationState(Base, TimestampMixin):
    __tablename__ = "conversation_states"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    state_data: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
