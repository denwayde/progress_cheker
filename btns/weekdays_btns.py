from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


def weekdays(sohranit=None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.button(text="Да")
    # kb.button(text="Нет")
    buttons = []#InlineKeyboardButton(text="Отчет", callback_data="user_report")
    for x in days_of_week:
        buttons.append(InlineKeyboardButton(text=x, callback_data=f"dayofweek_{x}"))
    kb.add(*buttons)
    kb.adjust(2)
    if sohranit != None:    
        kb.row(sohranit)  
    
    return kb.as_markup(resize_keyboard=True)

def hours(sohranit=None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.button(text="Да")
    # kb.button(text="Нет")
    buttons = []#InlineKeyboardButton(text="Отчет", callback_data="user_report")
    for x in range(1,25):
        buttons.append(InlineKeyboardButton(text=str(x), callback_data=f"hour_{x}"))
    kb.add(*buttons)
    kb.adjust(2)
    if sohranit != None:    
        kb.row(sohranit)
    
    return kb.as_markup(resize_keyboard=True)

def mins() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.button(text="Да")
    # kb.button(text="Нет")
    buttons = []#InlineKeyboardButton(text="Отчет", callback_data="user_report")
    for x in range(0,60, 5):
        if x == 0:
            buttons.append(InlineKeyboardButton(text=f"{x}0", callback_data=f"minute_{x}0"))
        else:
            buttons.append(InlineKeyboardButton(text=str(x), callback_data=f"minute_{x}"))
    kb.add(*buttons)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

