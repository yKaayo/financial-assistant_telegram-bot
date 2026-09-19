from app.bot.messages.templates import deleted_text
from app.graph.state import BotState
from app.services.task_service import TaskNotFoundError, TaskService


def delete_node(state: BotState, task_service: TaskService) -> BotState:
    callback = state.get("event_value", "")
    step = state.get("step", "")
    data = dict(state.get("data", {}))

    if callback == "action_delete" and step in {"", "idle"}:
        tasks, _ = task_service.list_tasks(state["user_id"], page=1)
        return {**state, "action": "delete", "step": "waiting_task", "data": {}, "response_kind": "select_delete_task", "response_text": "Selecione a tarefa para excluir:", "response_data": {"tasks": tasks}}

    if step == "waiting_task" and callback.startswith("delete_task_"):
        task_id = int(callback.rsplit("_", maxsplit=1)[-1])
        try:
            task_service.get_task_or_raise(state["user_id"], task_id)
        except TaskNotFoundError:
            return {**state, "response_kind": "error", "response_text": "Tarefa não encontrada."}
        data["task_id"] = task_id
        return {**state, "step": "waiting_confirm", "data": data, "response_kind": "confirm_delete", "response_text": "⚠️ Deseja realmente excluir esta tarefa?"}

    if step == "waiting_confirm" and callback == "delete_confirm_yes":
        try:
            task_service.delete_task(state["user_id"], data["task_id"])
            return {**state, "action": "menu", "step": "idle", "data": {}, "response_kind": "deleted", "response_text": deleted_text()}
        except TaskNotFoundError:
            return {**state, "response_kind": "error", "response_text": "Tarefa não encontrada."}

    if step == "waiting_confirm" and callback == "delete_confirm_no":
        return {**state, "action": "menu", "step": "idle", "data": {}, "response_kind": "canceled", "response_text": "Exclusão cancelada."}

    return {**state, "response_kind": "info", "response_text": "Use os botões para excluir uma tarefa."}
