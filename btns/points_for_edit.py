from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db_func import select_data

def points_for_edit(start_call) -> InlineKeyboardMarkup:#editusername_
    kb = InlineKeyboardBuilder()
    usernames = select_data("SELECT name FROM points")
    buttons = [InlineKeyboardButton(text=x[0], callback_data=f"{start_call}{x[0]}") for x in usernames]
    kb.add(*buttons)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)