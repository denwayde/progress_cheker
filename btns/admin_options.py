from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
#from aiogram.utils.keyboard import ReplyKeyboardBuilder
# from btns.admin_replybtn import admin_replybtns

def admin_btns() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.button(text="Да")
    # kb.button(text="Нет")
    buttons = [
        InlineKeyboardButton(text="Прогресс пользователей", callback_data="users_progress"),
        InlineKeyboardButton(text="Excel отчет", callback_data="excel_report"),
        InlineKeyboardButton(text="Пункты", callback_data="points"),
        InlineKeyboardButton(text="Пользователи", callback_data="users"),
        InlineKeyboardButton(text="Оповещения", callback_data="admin_notifications"),#InlineKeyboardButton(text="Время сдачи", callback_data="red_line"),
        InlineKeyboardButton(text="Отчистить прогресс", callback_data="deleteprogress_menu"),
    ]
    # buttons = [
    #     KeyboardButton(text="Прогресс пользователей", callback_data="users_progress"),
    #     KeyboardButton(text="Excel отчет", callback_data="excel_report"),
    #     KeyboardButton(text="Пункты", callback_data="points"),
    #     KeyboardButton(text="Пользователи", callback_data="users"),
    #     KeyboardButton(text="Время сдачи", callback_data="red_line"),
    #     KeyboardButton(text="Оповещения", callback_data="notification")#NUJNO DELAT MENU ADMINA INLAIN OSTALNIE KNOPKI REPLY

    # ]
    kb.add(*buttons)
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text="❌ Отмена", callback_data="otmena"))
    return kb.as_markup(resize_keyboard=True)