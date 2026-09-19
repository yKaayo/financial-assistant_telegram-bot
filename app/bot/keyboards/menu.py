from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.database.models import Task


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Criar", callback_data="action_create")],
        [InlineKeyboardButton("📋 Listar", callback_data="action_list")],
        [InlineKeyboardButton("✏️ Editar", callback_data="action_edit")],
        [InlineKeyboardButton("🗑️ Excluir", callback_data="action_delete")],
    ])


def cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancelar", callback_data="cancel")]])


def back_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar ao menu", callback_data="nav_menu")]])


def status_keyboard(prefix: str = "status") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Pendente", callback_data=f"{prefix}_pending")],
        [InlineKeyboardButton("Em andamento", callback_data=f"{prefix}_in_progress")],
        [InlineKeyboardButton("Concluída", callback_data=f"{prefix}_completed")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="cancel")],
    ])


def edit_field_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Título", callback_data="edit_field_title")],
        [InlineKeyboardButton("Descrição", callback_data="edit_field_description")],
        [InlineKeyboardButton("Status", callback_data="edit_field_status")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="cancel")],
    ])


def task_selection_keyboard(tasks: list[Task], mode: str) -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(f"#{task.id} {task.title}", callback_data=f"{mode}_task_{task.id}")] for task in tasks]
    rows.append([InlineKeyboardButton("❌ Cancelar", callback_data="cancel")])
    return InlineKeyboardMarkup(rows)


def delete_confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Sim", callback_data="delete_confirm_yes")],
        [InlineKeyboardButton("❌ Não", callback_data="delete_confirm_no")],
    ])


def pagination_keyboard(page: int, total_pages: int) -> InlineKeyboardMarkup:
    row = []
    if page > 1:
        row.append(InlineKeyboardButton("⬅️ Anterior", callback_data="list_prev"))
    if page < total_pages:
        row.append(InlineKeyboardButton("Próxima ➡️", callback_data="list_next"))
    return InlineKeyboardMarkup([row, [InlineKeyboardButton("🔙 Voltar ao menu", callback_data="nav_menu")]] if row else [[InlineKeyboardButton("🔙 Voltar ao menu", callback_data="nav_menu")]])
