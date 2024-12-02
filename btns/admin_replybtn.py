#from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
#from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def admin_replybtns() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    # kb.button(text="Да")
    # kb.button(text="Нет")
    # buttons = [
    #     InlineKeyboardButton(text="Прогресс пользователей", callback_data="users_progress"),
    #     InlineKeyboardButton(text="Excel отчет", callback_data="excel_report"),
    #     InlineKeyboardButton(text="Пункты", callback_data="points"),
    #     InlineKeyboardButton(text="Пользователи", callback_data="users"),
    #     InlineKeyboardButton(text="Оповещения", callback_data="admin_notifications")#InlineKeyboardButton(text="Время сдачи", callback_data="red_line"),

    # ]
    buttons = [
        KeyboardButton(text="Мой отчет"),
        KeyboardButton(text="Администрация"),
    ]
    kb.add(*buttons)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)#