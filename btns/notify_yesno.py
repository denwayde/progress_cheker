from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



def should_notify() -> InlineKeyboardMarkup:#editusername_
    kb = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text="Да", callback_data="notifyme"), InlineKeyboardButton(text="Нет", callback_data="dontnotifyme")]
    kb.add(*buttons)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)