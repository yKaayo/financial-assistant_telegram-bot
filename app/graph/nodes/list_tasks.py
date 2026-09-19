from app.bot.messages.templates import STATUS_LABELS
from app.graph.state import BotState
from app.services.task_service import TaskService


def list_node(state: BotState, task_service: TaskService) -> BotState:
    callback = state.get("event_value", "")
    page = state.get("data", {}).get("page", 1)
    if callback == "list_next":
        page += 1
    if callback == "list_prev":
        page = max(1, page - 1)

    tasks, total = task_service.list_tasks(user_id=state["user_id"], page=page)
    total_pages = max(1, (total + 4) // 5)
    if page > total_pages:
        page = total_pages
        tasks, total = task_service.list_tasks(user_id=state["user_id"], page=page)

    if not tasks:
        text = "📋 Você ainda não possui tarefas."
    else:
        lines = ["📋 Suas tarefas\n"]
        for task in tasks:
            lines.append(f"{task.id}. {task.title}\n   Status: {STATUS_LABELS.get(task.status, task.status)}")
        text = "\n\n".join(lines)

    return {
        **state,
        "action": "list",
        "step": "showing",
        "data": {"page": page},
        "response_kind": "list",
        "response_text": text,
        "response_data": {"page": page, "total_pages": total_pages},
    }
