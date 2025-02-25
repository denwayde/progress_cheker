from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
#from aiogram.utils.keyboard import ReplyKeyboardBuilder
# from btns.admin_replybtn import admin_replybtns

def admin_btns() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
 
    buttons = [
        InlineKeyboardButton(text="📈 Прогресс пользователей", callback_data="users_progress"),
        InlineKeyboardButton(text="📑 Excel отчет", callback_data="excel_report"),
        InlineKeyboardButton(text="⏺ Пункты", callback_data="points"),
        InlineKeyboardButton(text="✨ Бонусы", callback_data="bonuses"),
        InlineKeyboardButton(text="🙍🏻‍♀️🙍🏻‍♂️ Пользователи", callback_data="users"),
        InlineKeyboardButton(text="🔊 Оповещения", callback_data="admin_notifications"),
        InlineKeyboardButton(text="📧 Сообщение пользователям", callback_data="msg_to_users"),
        InlineKeyboardButton(text="💣 Очистить прогресс", callback_data="deleteprogress_menu"),
    ]
   
    kb.add(*buttons)
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text="❌ Отмена", callback_data="otmena"))
    return kb.as_markup(resize_keyboard=True)