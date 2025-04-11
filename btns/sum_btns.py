from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def sum_btns() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
 
    buttons = [
        InlineKeyboardButton(text="🙂 150руб 🙂", callback_data="150_rub"),
        InlineKeyboardButton(text="😎 300руб 😎", callback_data="300_rub"),
        InlineKeyboardButton(text="🦄 Ввести сумму", callback_data="vvesti_rub"),
    ]
   
    kb.add(*buttons)
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text="❌ Закрыть", callback_data="otmena"),)
    return kb.as_markup(resize_keyboard=True)