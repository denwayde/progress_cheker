from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def points_main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.button(text="Да")
    # kb.button(text="Нет")
    buttons = [
        InlineKeyboardButton(text="Список пунктов прогресса", callback_data="list_progresspoints"),
        InlineKeyboardButton(text="Добавить пункт прогресса", callback_data="add_progress_points"),
        InlineKeyboardButton(text="Изменить пункт прогресса", callback_data="edit_progress_points"),
        InlineKeyboardButton(text="Удалить пункт прогресса", callback_data="delete_progress_points"),
        InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main_menu"),
    ]
    kb.add(*buttons)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)