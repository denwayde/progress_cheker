from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
#from aiogram.utils.keyboard import ReplyKeyboardBuilder
# from btns.admin_replybtn import admin_replybtns

def msg_frequency() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
 
    buttons = [
        InlineKeyboardButton(text="Ежедневно", callback_data="send_msg_repeatly"),
        InlineKeyboardButton(text="Один раз", callback_data="send_msg_ones"),
    ]
   
    kb.add(*buttons)
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text="❌ Отмена", callback_data="otmena"), InlineKeyboardButton(text="⬅ Назад", callback_data="msg_to_users"),)
    return kb.as_markup(resize_keyboard=True)

def msg_usrbtns() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
 
    buttons = [
        InlineKeyboardButton(text="Отправить сообщение", callback_data="send_msg"),
        InlineKeyboardButton(text="Изменить сообщение", callback_data="changemsg"),
        InlineKeyboardButton(text="Удалить сообщение", callback_data="deletemsg"),
    ]
    kb.add(*buttons)
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text="❌ Отмена", callback_data="otmena"))
    return kb.as_markup(resize_keyboard=True)


from db_func import select_data_dict
def theme_explorer(action):
    kb = InlineKeyboardBuilder()
    msg_themes = select_data_dict("SELECT msg_theme FROM admin_messages WHERE msg_date IS NULL OR msg_date >= DATE('now')")
    buttons = [ InlineKeyboardButton(text=x['msg_theme'], callback_data=f"{action}_{x['msg_theme']}") for x in msg_themes ]
    kb.add(*buttons)
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text="❌ Отмена", callback_data="otmena"), InlineKeyboardButton(text="⬅ Назад", callback_data="msg_to_users"),)
    return kb.as_markup(resize_keyboard=True)