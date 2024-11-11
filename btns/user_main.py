from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def user_main() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.button(text="Да")
    # kb.button(text="Нет")
    buttons = [
        InlineKeyboardButton(text="Отчет", callback_data="user_report"),
        InlineKeyboardButton(text="Мой рейтинг", callback_data="user_rating"),
        InlineKeyboardButton(text="Минимумы", callback_data="mins"),

    ]
    kb.add(*buttons)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)