from app.bot.messages.templates import main_menu_text
from app.graph.state import BotState


def menu_node(state: BotState) -> BotState:
    return {
        **state,
        "action": "menu",
        "step": "idle",
        "data": {},
        "response_kind": "menu",
        "response_text": main_menu_text(),
    }
