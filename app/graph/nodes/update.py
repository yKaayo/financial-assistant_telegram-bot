from app.bot.messages.templates import updated_text
from app.graph.state import BotState
from app.services.task_service import TaskNotFoundError, TaskService, TaskValidationError


def update_node(state: BotState, task_service: TaskService) -> BotState:
    callback = state.get("event_value", "")
    text = state.get("event_value", "") if state.get("event_type") == "message" else ""
    step = state.get("step", "")
    data = dict(state.get("data", {}))

    if callback == "action_edit" and step in {"", "idle"}:
        tasks, _ = task_service.list_tasks(state["user_id"], page=1)
        return {**state, "action": "edit", "step": "waiting_task", "data": {}, "response_kind": "select_edit_task", "response_text": "Selecione a tarefa para editar:", "response_data": {"tasks": tasks}}

    if step == "waiting_task" and callback.startswith("edit_task_"):
        task_id = int(callback.rsplit("_", maxsplit=1)[-1])
        try:
            task_service.get_task_or_raise(state["user_id"], task_id)
        except TaskNotFoundError:
            return {**state, "response_kind": "error", "response_text": "Tarefa não encontrada."}
        return {**state, "step": "waiting_field", "data": {"task_id": task_id}, "response_kind": "select_field", "response_text": "Qual campo você deseja alterar?"}

    if step == "waiting_field" and callback.startswith("edit_field_"):
        field = callback.replace("edit_field_", "", 1)
        data["field"] = field
        if field == "status":
            return {**state, "step": "waiting_status_value", "data": data, "response_kind": "ask_status", "response_text": "Escolha o novo status:"}
        label = "título" if field == "title" else "descrição"
        return {**state, "step": "waiting_text_value", "data": data, "response_kind": "ask_text_value", "response_text": f"Informe o novo {label}:"}

    if step == "waiting_status_value" and callback.startswith("status_"):
        try:
            task_service.update_task(state["user_id"], data["task_id"], status=callback.replace("status_", "", 1))
            return {**state, "action": "menu", "step": "idle", "data": {}, "response_kind": "updated", "response_text": updated_text()}
        except (TaskNotFoundError, TaskValidationError):
            return {**state, "response_kind": "error", "response_text": "Não foi possível atualizar a tarefa."}

    if step == "waiting_text_value" and text:
        try:
            task_service.update_task(state["user_id"], data["task_id"], **{data["field"]: text})
            return {**state, "action": "menu", "step": "idle", "data": {}, "response_kind": "updated", "response_text": updated_text()}
        except (TaskNotFoundError, TaskValidationError):
            return {**state, "response_kind": "error", "response_text": "Não foi possível atualizar a tarefa."}

    return {**state, "response_kind": "info", "response_text": "Use os botões para editar uma tarefa."}
