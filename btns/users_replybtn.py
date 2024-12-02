
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def user_replybtns() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder() 
    buttons = [
        KeyboardButton(text="Отчет"),
        KeyboardButton(text="Остальное"),
    ]
    kb.add(*buttons)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)#