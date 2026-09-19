from typing import Literal, TypedDict


class BotState(TypedDict, total=False):
    user_id: int
    chat_id: int
    action: str
    step: str
    data: dict
    message_id: int | None
    error: str | None
    event_type: Literal["callback", "message"]
    event_value: str
    response_text: str
    response_kind: str
    response_data: dict
