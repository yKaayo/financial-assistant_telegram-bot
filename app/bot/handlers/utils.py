from telegram import InlineKeyboardMarkup, Update

from app.bot.keyboards.menu import (
    back_menu_keyboard,
    cancel_keyboard,
    delete_confirmation_keyboard,
    edit_field_keyboard,
    main_menu_keyboard,
    pagination_keyboard,
    status_keyboard,
    task_selection_keyboard,
)


def resolve_keyboard(state: dict) -> InlineKeyboardMarkup:
    kind = state.get("response_kind")
    if kind in {"menu", "created", "updated", "deleted", "canceled", "error"}:
        return main_menu_keyboard() if kind != "error" else back_menu_keyboard()
    if kind in {"ask_title", "ask_description", "ask_text_value"}:
        return cancel_keyboard()
    if kind == "ask_status":
        return status_keyboard()
    if kind == "list":
        data = state.get("response_data", {})
        return pagination_keyboard(data.get("page", 1), data.get("total_pages", 1))
    if kind == "select_field":
        return edit_field_keyboard()
    if kind == "confirm_delete":
        return delete_confirmation_keyboard()
    if kind == "select_edit_task":
        return task_selection_keyboard(state.get("response_data", {}).get("tasks", []), "edit")
    if kind == "select_delete_task":
        return task_selection_keyboard(state.get("response_data", {}).get("tasks", []), "delete")
    return back_menu_keyboard()


async def send_graph_response(update: Update, state: dict) -> None:
    keyboard = resolve_keyboard(state)
    text = state.get("response_text", "")
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(text, reply_markup=keyboard)
    elif update.message:
        await update.message.reply_text(text, reply_markup=keyboard)
