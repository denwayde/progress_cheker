from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_places() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.button(text="Да")
    # kb.button(text="Нет")
    buttons = [
        InlineKeyboardButton(text="Партер", callback_data="place_parter"),
        InlineKeyboardButton(text="Балкон (Центр)", callback_data="place_balkonCenter"),
        InlineKeyboardButton(text="Балкон (Правое крыло)", callback_data="place_balkonRight"),
        InlineKeyboardButton(text="Балкон (Левое крыло)", callback_data="place_balkonLeft")
    ]
    kb.add(*buttons)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
