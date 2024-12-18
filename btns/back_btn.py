#InlineKeyboardButton(text="Назад", callback_data="back_to_users_menu"))
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def back_btn_element(where_call):
    # kb = InlineKeyboardBuilder()
    return InlineKeyboardButton(text="Назад", callback_data = where_call)



def back_btn(data) -> InlineKeyboardMarkup:#editusername_
    kb = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text="⬅ Назад", callback_data=data)]
    kb.add(*buttons)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)