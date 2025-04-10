from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


def weekdays(remove_day = '', nazad = None, sohranit=None, otmena = None, dontrmnd = None) -> InlineKeyboardMarkup:
    days_of_week1 = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    try:
        days_of_week1.remove(remove_day)
    except ValueError:
        pass
    kb = InlineKeyboardBuilder()
    # kb.button(text="Да")
    # kb.button(text="Нет")
    buttons = []#InlineKeyboardButton(text="Отчет", callback_data="user_report")
    for x in days_of_week1:
        buttons.append(InlineKeyboardButton(text=x, callback_data=f"dayofweek_{x}"))
    kb.add(*buttons)
    kb.adjust(2)
    if dontrmnd == None:
        kb.row(InlineKeyboardButton(text='❄ Не присылать оповещений', callback_data="dontremindme"))
    if sohranit != None and nazad == None:    
        kb.row(sohranit)  
    elif nazad != None and sohranit == None:
        kb.row(nazad)
    elif nazad != None and sohranit != None:
        kb.row(nazad)
        kb.row(sohranit)
    if otmena!=None:
        kb.row(otmena)
    
    return kb.as_markup(resize_keyboard=True)

def hours(nazad = None, sohranit=None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.button(text="Да")
    # kb.button(text="Нет")
    buttons = []#InlineKeyboardButton(text="Отчет", callback_data="user_report")
    for x in range(1,24):
        buttons.append(InlineKeyboardButton(text=str(x), callback_data=f"hour_{x}"))
    kb.add(*buttons)
    kb.adjust(3)
    if sohranit != None and nazad == None:    
        kb.row(sohranit)  
    elif nazad != None and sohranit == None:
        kb.row(nazad)
    elif nazad != None and sohranit != None:
        kb.row(nazad, sohranit)
    return kb.as_markup(resize_keyboard=True)

def mins(nazad = None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.button(text="Да")
    # kb.button(text="Нет")
    buttons = []#InlineKeyboardButton(text="Отчет", callback_data="user_report")
    for x in range(0,60, 5):
        if x == 0 or x==5:
            buttons.append(InlineKeyboardButton(text=f"0{x}", callback_data=f"minute_0{x}"))
        else:
            buttons.append(InlineKeyboardButton(text=str(x), callback_data=f"minute_{x}"))
    kb.add(*buttons)
    kb.adjust(3)
    if nazad != None:
        kb.row(nazad)
    return kb.as_markup(resize_keyboard=True)



def back_btn(btn_name, data) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=btn_name, callback_data=data)]
    kb.add(*buttons)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
    

