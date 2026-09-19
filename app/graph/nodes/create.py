from app.bot.messages.templates import created_text
from app.graph.state import BotState
from app.services.task_service import TaskService, TaskValidationError


def create_node(state: BotState, task_service: TaskService) -> BotState:
    callback = state.get("event_value", "")
    text = state.get("event_value", "") if state.get("event_type") == "message" else ""
    step = state.get("step", "")
    data = dict(state.get("data", {}))

    if callback == "action_create" and step in {"", "idle"}:
        return {**state, "action": "create", "step": "waiting_title", "data": {}, "response_kind": "ask_title", "response_text": "Digite o título da tarefa:"}

    if step == "waiting_title" and text:
        data["title"] = text
        return {**state, "action": "create", "step": "waiting_description", "data": data, "response_kind": "ask_description", "response_text": "Agora informe a descrição:"}

    if step == "waiting_description" and text:
        data["description"] = text
        return {**state, "action": "create", "step": "waiting_status", "data": data, "response_kind": "ask_status", "response_text": "Escolha o status:"}

    if step == "waiting_status" and callback.startswith("status_"):
        status = callback.replace("status_", "", 1)
        data["status"] = status
        try:
            task = task_service.create_task(
                user_id=state["user_id"],
                title=data["title"],
                description=data["description"],
                status=data["status"],
            )
            return {**state, "action": "menu", "step": "idle", "data": {}, "response_kind": "created", "response_text": created_text(task.title)}
        except TaskValidationError:
            return {**state, "response_kind": "error", "response_text": "Dados inválidos. Tente novamente."}

    expected = "Use os botões ou envie o texto solicitado para continuar a criação."
    return {**state, "response_kind": "info", "response_text": expected}
