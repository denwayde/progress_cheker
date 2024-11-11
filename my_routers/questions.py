from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, PreCheckoutQuery, ContentType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from states import SetConfigsToBot
import os
from re import fullmatch
from dotenv import load_dotenv
from db_func import delete_or_insert_data, insert_many, select_data
from btns.admin_options import admin_btns
load_dotenv()  # Загрузка переменных из файла .env

router = Router()  # [1]

from handlers.for_start import start_func
@router.message(Command("start"), StateFilter(None))  # [2]
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    await start_func(message, state, 'Здравствуйте. Введите пожалуйста пароль, выданный администратором', SetConfigsToBot.set_password, bot)


from handlers.for_get_password import correct_password_proccess
@router.message(SetConfigsToBot.set_password)
async def sss_psw(message: Message, state: FSMContext, bot: Bot):
    await correct_password_proccess(message, state, bot, SetConfigsToBot.set_name)#tut prodoljaetsya algoritm dlya userov


from handlers.user_settings import call_users_settings
@router.callback_query(F.data == 'users')
async def usr_stgs(call: CallbackQuery, bot: Bot):
    await call_users_settings(call, bot) # add_users | delete_user | edit_user | back

#------------------------------------------------------------------------------------------------------АДМИН ДОБАВЛЯЕТ ПОЛЬЗОВАТЕЛЕЙ------------------------------------------------------------------------------------
@router.callback_query(F.data == 'add_users', StateFilter(None))
async def usr_stgs(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await call.message.answer(f"Напишите пожалуйста через запятую имена пользоватей (если пользователь один просто впишите имя без знаков препинания).")
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1, ))
    await call.answer()
    await state.set_state(SetConfigsToBot.set_user_names)


from btns.users_edit_btns import get_users_settings

@router.message(SetConfigsToBot.set_user_names)
async def usr_stgs_sub(message: Message, state: FSMContext, bot: Bot):
    users_list = [(name.strip(), ) for name in message.text.split(',')]
    insert_many("INSERT INTO usernames (name) VALUES(?)", users_list)
    await state.clear()
    await message.answer(f"{message.text} был(и) добален(ы)", reply_markup=get_users_settings())
    await bot.delete_messages(message.chat.id, (message.message_id, message.message_id-1, ))


#------------------------------------------------------------------------------------------------------АДМИН ИЗМЕНЯЕТ ИМЯ ПОЛЬЗОВАТЕЛЯ------------------------------------------------------------------------------------
from btns.users_for_edit import users_for_edit
@router.callback_query(F.data == 'edit_user')
async def usr_stgs_edit(call: CallbackQuery, bot: Bot):
    await call.message.answer(f"Выберите пользователя имя которого вы хотите изменить", reply_markup=users_for_edit('editusername_'))
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1, ))
    await call.answer()

@router.callback_query(F.data.startswith('editusername_'), StateFilter(None))
async def edit_username(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    user = call.data.split('_')[1]
    await state.update_data(name = user)
    await call.message.answer(f"Вы хотите изменить имя \'{user}\'. В поле ввода внесите новое имя для пользователя \'{user}\'")
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1, ))
    await state.set_state(SetConfigsToBot.set_new_username)
    await call.answer()

@router.message(SetConfigsToBot.set_new_username)
async def new_usrname(message: Message, state: FSMContext, bot: Bot):
    #await state.clear()
    user = await state.get_data()
    await bot.delete_messages(message.chat.id, (message.message_id, message.message_id-1, ))
    delete_or_insert_data("UPDATE usernames SET name = ? WHERE name = ?", (message.text, user['name']))
    await message.answer(f"Вы изменили имя {user['name']} на {message.text}", reply_markup=get_users_settings())
    await state.clear()


#------------------------------------------------------------------------------------------------------АДМИН УДАЛЯЕТ ИМЯ ПОЛЬЗОВАТЕЛЯ------------------------------------------------------------------------------------
@router.callback_query(F.data == 'delete_user')
async def usr_stgs_delete(call: CallbackQuery, bot: Bot):
    await call.message.answer(f"Выберите пользователя имя которого вы хотите удалить", reply_markup=users_for_edit('deleteusername_'))
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1, ))
    await call.answer()

@router.callback_query(F.data.startswith('deleteusername_'), StateFilter(None))
async def edit_username(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    user = call.data.split('_')[1]
    delete_or_insert_data("DELETE FROM usernames WHERE name = ?", (user, ))
    await call.message.answer(f"Вы удалили \'{user}\'.'", reply_markup=get_users_settings())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1, ))
    await call.answer()

#------------------------------------------------------------------------------------------------------АДМИН ДЕЛАЕТ ВОЗВРАТ НА ГЛАВНУЮ------------------------------------------------------------------------------------
@router.callback_query(F.data == 'back_to_main_menu')
async def back_to_main_menu(call: CallbackQuery, bot: Bot):
    await call.message.answer(f"Главное меню администратора", reply_markup=admin_btns())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1, ))
    await call.answer()

#------------------------------------------------------------------------------------------------------АДМИН ДОБАВЛЯЕТ ПУНКТЫ ПРОГРЕССА------------------------------------------------------------------------------------
from btns.points_main import points_main_menu
@router.callback_query(F.data == 'points')
async def back_to_main_menu(call: CallbackQuery, bot: Bot):
    await call.message.answer(f"Выберите опцию для пунктов прогресса", reply_markup=points_main_menu())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1, ))
    await call.answer()


@router.callback_query(F.data == 'add_progress_points', StateFilter(None))
async def usr_stgs(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await call.message.answer(f"Напишите боту названия пунктов прогресса через запятую (если пункт один запятую ставить необязательно).")
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1, ))
    await call.answer()
    await state.set_state(SetConfigsToBot.set_points_names)


@router.message(SetConfigsToBot.set_points_names)
async def usr_stgs_sub(message: Message, state: FSMContext, bot: Bot):
    points_list = [(name.strip(), ) for name in message.text.split(',')]
    insert_many("INSERT INTO points (name) VALUES(?)", points_list)
    await state.clear()
    await message.answer(f"{message.text} был(и) добален(ы)", reply_markup=points_main_menu())
    await bot.delete_messages(message.chat.id, (message.message_id, message.message_id-1, ))

#------------------------------------------------------------------------------------------------------АДМИН ИЗМЕНЯЕТ ИМЯ ПУНКТОВ ПРОГРЕССА------------------------------------------------------------------------------------
from btns.points_for_edit import points_for_edit
@router.callback_query(F.data == 'edit_progress_points')
async def usr_stgs_edit(call: CallbackQuery, bot: Bot):
    await call.message.answer(f"Выберите пункт прогресса который вы хотите изменить", reply_markup=points_for_edit('editpoints_'))
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1, ))
    await call.answer()

@router.callback_query(F.data.startswith('editpoints_'), StateFilter(None))
async def edit_username(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    user = call.data.split('_')[1]
    await state.update_data(name = user)
    await call.message.answer(f"Вы хотите изменить имя \'{user}\'. В поле ввода внесите новое имя для пункта прогресса \'{user}\'")
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1, ))
    await state.set_state(SetConfigsToBot.set_new_pointname)
    await call.answer()

@router.message(SetConfigsToBot.set_new_pointname)
async def new_usrname(message: Message, state: FSMContext, bot: Bot):
    #await state.clear()
    user = await state.get_data()
    await bot.delete_messages(message.chat.id, (message.message_id, message.message_id-1, ))
    delete_or_insert_data("UPDATE points SET name = ? WHERE name = ?", (message.text, user['name']))
    await message.answer(f"Вы изменили имя {user['name']} на {message.text}", reply_markup=points_main_menu())
    await state.clear()

#------------------------------------------------------------------------------------------------------АДМИН УДАЛЯЕТ ПУНКТ ПРОГРЕССА------------------------------------------------------------------------------------
@router.callback_query(F.data == 'delete_progress_points')
async def usr_stgs_delete(call: CallbackQuery, bot: Bot):
    await call.message.answer(f"Выберите пункт прогресса который вы хотите удалить", reply_markup=points_for_edit('deletepoint_'))
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1, ))
    await call.answer()

@router.callback_query(F.data.startswith('deletepoint_'), StateFilter(None))
async def edit_username(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    user = call.data.split('_')[1]
    delete_or_insert_data("DELETE FROM points WHERE name = ?", (user, ))
    await call.message.answer(f"Вы удалили \'{user}\'.'", reply_markup=points_main_menu())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1, ))
    await call.answer()



#------------------------------------------------------------------------------------------------------ЮЗЕР ВЫБИРАЕТ СВОЙ НИКНЕЙМ------------------------------------------------------------------------------------

from btns.user_main import user_main
@router.callback_query(F.data.startswith('userchosen_name_'))
async def edit_username(call: CallbackQuery, state: FSMContext, bot: Bot):
    user = call.data.split('_')[2]
    delete_or_insert_data("UPDATE usernames SET telega_id = ? WHERE name = ?", (call.message.chat.id, user, ))
    await call.message.answer(f"Теперь Ваш никнейм \'{user}\'", reply_markup = user_main())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1, ))
    await call.answer()


# @router.message(SetConfigsToBot.set_name)
# async def sss_name(message: Message, state: FSMContext, bot: Bot):
#     await correct_password_proccess(message, state, bot, "!!!!!!!!!!!!!!!!!!!!!!!", SetConfigsToBot.set_name)

# from handlers.for_get_name import name_proccessor
# @router.message(SetConfigsToBot.set_name)
# async def sss_name(message: Message, state: FSMContext, bot: Bot):
#     await name_proccessor(message, state, bot, f"Приятно познакомиться, {message.text}. Выберите пожалуйста область зала", SetConfigsToBot.set_place)




