from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def user_btns() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.button(text="Да")
    # kb.button(text="Нет")
    buttons = [
        InlineKeyboardButton(text="Отправить отчет", callback_data="send_report"),
        InlineKeyboardButton(text="Редактировать отчет", callback_data="edit_report"),
        InlineKeyboardButton(text="Мой рейтинг", callback_data="my_rating"),
        InlineKeyboardButton(text="Минимумы", callback_data="mins"),
    ]
    kb.add(*buttons)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)