from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, PreCheckoutQuery, ContentType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from states import SetConfigsToBot
import os
from re import fullmatch
from dotenv import load_dotenv


load_dotenv()  # Загрузка переменных из файла .env

router = Router()  # [1]

from handlers.for_start import start_func
@router.message(Command("start"), StateFilter(None))  # [2]
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    await start_func(message, state, 'Здравствуйте, Вас приветсвует бот, который поможет Вам забронировать место в зале. Давайте приступим.\nНапишите пожалуйста боту ФИО', SetConfigsToBot.set_name, bot)


from handlers.for_get_name import name_proccessor
@router.message(SetConfigsToBot.set_name)
async def sss_name(message: Message, state: FSMContext, bot: Bot):
    await name_proccessor(message, state, bot, f"Приятно познакомиться, {message.text}. Выберите пожалуйста область зала", SetConfigsToBot.set_place)



@router.callback_query(F.data.startswith('place_'), SetConfigsToBot.set_place)
async def place_handler(call: CallbackQuery, state: FSMContext, bot: Bot):#vot tut ty konechno tupanul b..
    message_data = call.data.split('_')
    if message_data[1] == 'parter':
        await set_row_handler(call, state, "Партер", bot, SetConfigsToBot.set_row)
    elif message_data[1] == 'balkonCenter':
        await set_row_handler(call, state, "Балкон (Центр)", bot, SetConfigsToBot.set_row)
    elif message_data[1] == 'balkonRight':
        await set_row_handler(call, state, "Балкон (Правое крыло)", bot, SetConfigsToBot.set_row)
    elif message_data[1] == 'balkonLeft':
        await set_row_handler(call, state, "Балкон (Левое крыло)", bot, SetConfigsToBot.set_row)


from handlers.for_set_row import row_handler
@router.callback_query(F.data.startswith('row_'), SetConfigsToBot.set_row)
async def sss_row_handler(call: CallbackQuery, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    await row_handler(call, state, bot, f"Вы выбрали:\nОбласть зала - {user_data['place']}\nРяд - №{call.data.split('_')[1]}.\nВыберите пожалуйста место в ряду", SetConfigsToBot.set_num)


from handlers.finish_handle import succeed_changing
@router.callback_query(F.data.startswith('num_'), SetConfigsToBot.set_num)
async def nnn(call:CallbackQuery, state: FSMContext, bot: Bot):
    is_code = await state.get_data()
    if hasattr(is_code, 'code'):
        await succeed_changing(call, state, bot)
    else:
        await num_handler(call, state, bot, "Напишите пожалуйста сумму пожертвования", SetConfigsToBot.set_rub)


@router.message(F.text.isdigit()==False, SetConfigsToBot.set_rub)
async def rub_handler1(message: Message, state: FSMContext, bot: Bot):
    await message.answer('Похоже что Вы написали не число. Попробуйте ввести сумму пожертвования снова')
    await state.set_state(SetConfigsToBot.set_rub)

