from langgraph.graph import START, StateGraph

from app.bot.messages.templates import canceled_text, friendly_error_text
from app.graph.nodes.create import create_node
from app.graph.nodes.delete import delete_node
from app.graph.nodes.list_tasks import list_node
from app.graph.nodes.menu import menu_node
from app.graph.nodes.update import update_node
from app.graph.state import BotState
from app.services.task_service import TaskService


class BotGraph:
    def __init__(self, task_service: TaskService) -> None:
        self.task_service = task_service
        graph = StateGraph(BotState)
        graph.add_node("menu", menu_node)
        graph.add_node("create", lambda state: create_node(state, self.task_service))
        graph.add_node("list", lambda state: list_node(state, self.task_service))
        graph.add_node("update", lambda state: update_node(state, self.task_service))
        graph.add_node("delete", lambda state: delete_node(state, self.task_service))
        graph.add_node("cancel", self.cancel_node)
        graph.add_node("unknown", self.unknown_node)
        graph.add_conditional_edges(START, self.route)
        self.graph = graph.compile()

    @staticmethod
    def route(state: BotState) -> str:
        callback = state.get("event_value", "") if state.get("event_type") == "callback" else ""
        action = state.get("action", "")

        if callback in {"cancel"}:
            return "cancel"
        if callback in {"nav_menu", "start"}:
            return "menu"
        if callback.startswith("action_create") or action == "create":
            return "create"
        if callback.startswith("action_list") or callback in {"list_next", "list_prev"} or action == "list":
            return "list"
        if callback.startswith("action_edit") or callback.startswith("edit_") or action == "edit":
            return "update"
        if callback.startswith("action_delete") or callback.startswith("delete_") or action == "delete":
            return "delete"
        if state.get("event_type") == "message" and action in {"create", "edit"}:
            return "create" if action == "create" else "update"
        return "unknown"

    @staticmethod
    def cancel_node(state: BotState) -> BotState:
        return {**state, "action": "menu", "step": "idle", "data": {}, "response_kind": "canceled", "response_text": canceled_text()}

    @staticmethod
    def unknown_node(state: BotState) -> BotState:
        return {**state, "response_kind": "error", "response_text": friendly_error_text()}

    def run(self, state: BotState) -> BotState:
        return self.graph.invoke(state)
