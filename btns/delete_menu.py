from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder




def delete_options() -> InlineKeyboardMarkup:#editusername_
    kb = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text="Да", callback_data='delete_allprogress'),
        InlineKeyboardButton(text="Нет", callback_data='otmena')
               ]
    kb.add(*buttons)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

