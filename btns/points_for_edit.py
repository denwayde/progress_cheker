from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db_func import select_data

def points_for_edit(start_call, text_btn, back_btn, data=None, zakrit = None) -> InlineKeyboardMarkup:#editusername_
    kb = InlineKeyboardBuilder()
    usernames = select_data("SELECT name FROM points")
    buttons = [InlineKeyboardButton(text=x[0], callback_data=f"{start_call}{x[0]}") for x in usernames]
    kb.add(*buttons)
    kb.adjust(2)
    if data != None:
        kb.row(InlineKeyboardButton(text=text_btn, callback_data=back_btn), InlineKeyboardButton(text="♻ Изменить", callback_data=f'changecheckedpoint_{data}'))
    else:
        kb.row(InlineKeyboardButton(text=text_btn, callback_data=back_btn))

    if zakrit != None:
        kb.row(InlineKeyboardButton(text="✖ Закрыть", callback_data=f'otmena')) 
    return kb.as_markup(resize_keyboard=True)