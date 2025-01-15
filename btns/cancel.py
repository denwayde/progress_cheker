from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def back_btn_element(where_call):
    # kb = InlineKeyboardBuilder()
    return InlineKeyboardButton(text="Назад", callback_data = where_call)



def back_btn(data) -> InlineKeyboardMarkup:#editusername_
    kb = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text="Назад", callback_data=data)]
    kb.add(*buttons, back_btn)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def otmena_btn() -> InlineKeyboardMarkup:#editusername_
    kb = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text="❌ Отмена", callback_data="otmena")]
    kb.add(*buttons)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def zakrit_btn() -> InlineKeyboardMarkup:#editusername_
    kb = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text="✖ Закрыть", callback_data="otmena")]
    kb.add(*buttons)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)