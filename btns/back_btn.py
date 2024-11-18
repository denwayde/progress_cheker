#InlineKeyboardButton(text="Назад", callback_data="back_to_users_menu"))
from aiogram.types import InlineKeyboardButton

def back_btn(where_call):
    return InlineKeyboardButton(text="Назад", callback_data = where_call))

# def points_for_edit(start_call, back_btn) -> InlineKeyboardMarkup:#editusername_
#     kb = InlineKeyboardBuilder()
#     usernames = select_data("SELECT name FROM points")
#     buttons = [InlineKeyboardButton(text=x[0], callback_data=f"{start_call}{x[0]}") for x in usernames]
#     kb.add(*buttons, back_btn)
#     kb.adjust(2)
#     return kb.as_markup(resize_keyboard=True)