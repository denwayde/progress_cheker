from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def user_main() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.button(text="Да")
    # kb.button(text="Нет")
    buttons = [
        InlineKeyboardButton(text="Мой рейтинг", callback_data="user_rating"),
        InlineKeyboardButton(text="Минимумы", callback_data="mins"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="otmena"),

    ]
    kb.add(*buttons)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)