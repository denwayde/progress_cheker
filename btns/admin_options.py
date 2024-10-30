from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_btns() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.button(text="Да")
    # kb.button(text="Нет")
    buttons = [
        InlineKeyboardButton(text="Прогресс пользователей", callback_data="users_progress"),
        InlineKeyboardButton(text="Excel отчет", callback_data="excel_report"),
        InlineKeyboardButton(text="Пункты", callback_data="points"),
        InlineKeyboardButton(text="Пользователи", callback_data="users"),
        InlineKeyboardButton(text="Время сдачи", callback_data="red_line"),
        InlineKeyboardButton(text="Оповещение", callback_data="notification")

    ]
    kb.add(*buttons)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)