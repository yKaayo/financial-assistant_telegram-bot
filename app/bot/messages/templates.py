STATUS_LABELS = {
    "pending": "Pendente",
    "in_progress": "Em andamento",
    "completed": "Concluída",
}


def main_menu_text() -> str:
    return "🤖 Menu Principal\n\nEscolha uma opção:" 


def created_text(title: str) -> str:
    return f"✅ Tarefa criada com sucesso: {title}"


def updated_text() -> str:
    return "✅ Tarefa atualizada com sucesso."


def deleted_text() -> str:
    return "✅ Tarefa excluída com sucesso."


def canceled_text() -> str:
    return "Operação cancelada."


def friendly_error_text() -> str:
    return "❌ Não consegui concluir essa operação.\n\nTente novamente ou volte ao menu."
