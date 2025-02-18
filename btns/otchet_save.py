from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db_func import select_data

def otchet_save(data) -> InlineKeyboardMarkup:#editusername_
    kb = InlineKeyboardBuilder()
    
    buttons = [
        InlineKeyboardButton(text='⬅ К списку пунктов', callback_data="user_report"),
        InlineKeyboardButton(text="♻ Изменить значение", callback_data=f'changecheckedpoint_{data}'),
        InlineKeyboardButton(text=' Сохранить и отправить отчет', callback_data="otmena")
        ]
    kb.add(*buttons)
    kb.adjust(1)
    # if data != None:
    #     kb.row(InlineKeyboardButton(text=text_btn, callback_data=back_btn), InlineKeyboardButton(text="♻ Изменить", callback_data=f'changecheckedpoint_{data}'))
    # else:
    #     kb.row(InlineKeyboardButton(text=text_btn, callback_data=back_btn))

    # if zakrit != None:
        # kb.row(InlineKeyboardButton(text="✖ Закрыть", callback_data=f'otmena')) 
    return kb.as_markup(resize_keyboard=True)