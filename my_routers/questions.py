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
    await start_func(message, state, 'Здравствуйте. Введите пожалуйста пароль, выданный администратором', SetConfigsToBot.set_name, bot)


# from handlers.for_get_name import name_proccessor
# @router.message(SetConfigsToBot.set_name)
# async def sss_name(message: Message, state: FSMContext, bot: Bot):
#     await name_proccessor(message, state, bot, f"Приятно познакомиться, {message.text}. Выберите пожалуйста область зала", SetConfigsToBot.set_place)




