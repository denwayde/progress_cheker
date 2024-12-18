from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
def get_users_settings() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.button(text="Да")
    # kb.button(text="Нет")
    buttons = [
        InlineKeyboardButton(text="Список пользователей", callback_data="list_users"),
        InlineKeyboardButton(text="Добавить пользователей", callback_data="add_users"),
        InlineKeyboardButton(text="Изменить пользователя", callback_data="edit_user"),
        InlineKeyboardButton(text="Удалить пользователя", callback_data="delete_user"),
        InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")
    ]
    kb.add(*buttons)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)