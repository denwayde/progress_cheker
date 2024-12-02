from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder

def notifications_btns() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    buttons = [
        InlineKeyboardButton(text="Редлайн для пользователей", callback_data="users_notification_redline"),
        InlineKeyboardButton(text="Мои напоминания", callback_data="admin_notifacion"),
    ]
   
    kb.add(*buttons)
    kb.adjust(1)
    kb.row(InlineKeyboardButton(text="❌ Отмена", callback_data="otmena"), InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main_menu"))
    return kb.as_markup(resize_keyboard=True)