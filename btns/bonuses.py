from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
#from aiogram.utils.keyboard import ReplyKeyboardBuilder
# from btns.admin_replybtn import admin_replybtns

def bonuses_btns() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text="Бонус строки", callback_data="row_bonus"),
        InlineKeyboardButton(text="Бонус столбца", callback_data="column_bonus"),
        InlineKeyboardButton(text="Бонус минимумов", callback_data="minimums_bonus"),
    ]
    kb.add(*buttons)
    kb.adjust(1)
    kb.row(InlineKeyboardButton(text="❌ Отмена", callback_data="otmena"))
    return kb.as_markup(resize_keyboard=True)