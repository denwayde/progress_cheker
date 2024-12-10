from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from states import SetConfigsToBot
import os
from re import fullmatch
from dotenv import load_dotenv
from db_func import delete_or_insert_data, insert_many, select_data
from btns.admin_options import admin_btns
from btns.back_btn import back_btn
from btns.admin_replybtn import admin_replybtns

load_dotenv()  # Загрузка переменных из файла .env
admin_id = os.getenv('ADMIN_ID')


router = Router()  # [1]

from handlers.for_start import start_func
@router.message(Command("start"), StateFilter(None))  # [2]
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    await start_func(message, state, 'Здравствуйте. Введите пожалуйста пароль, выданный администратором', SetConfigsToBot.set_password, bot)


from handlers.for_get_password import correct_password_proccess
@router.message(SetConfigsToBot.set_password)
async def sss_psw(message: Message, state: FSMContext, bot: Bot):
    await correct_password_proccess(message, state, bot)#tut prodoljaetsya algoritm dlya userov-----SetConfigsToBot.set_name

from handlers.for_get_password import if_user
from btns.weekdays_btns import weekdays, hours, mins
@router.message(SetConfigsToBot.set_name)
async def set_name(message: Message, state: FSMContext, bot: Bot):
    data = select_data("SELECT name FROM usernames WHERE name = ?", (message.text,))
    if data == []:
        #await message.answer('Такого никнейма нет. Проверьте правильность написанияния или обратитесь к администратору')
        await if_user(message, bot, state, 'Такого никнейма нет. Проверьте правильность написанияния или обратитесь к администратору.', SetConfigsToBot.set_name)
        await bot.delete_messages(message.chat.id, (message.message_id-1, ))
    else:
        #await message.answer("Отлично! Выберите с какого дня недели бот будет напоминать о выполнении отчета. Если день один то выберите день, а на следующем этапе нажмите кнопку СОХРАНИТЬ", reply_markup=weekdays())
        await set_firstday_of_notification(message, state, bot, "Отлично! Выберите с какого дня недели бот будет напоминать о выполнении отчета. Если день один то выберите день, а на следующем этапе нажмите кнопку СОХРАНИТЬ")

async def set_firstday_of_notification(message, state, bot, text):
    await message.answer(text, reply_markup=weekdays())
    await state.update_data(name = message.text)
    await state.set_state(SetConfigsToBot.set_notification) 
    await bot.delete_messages(message.chat.id, (message.message_id-1, ))

from aiogram.types import InlineKeyboardButton
@router.callback_query(F.data.startswith('dayofweek_'), SetConfigsToBot.set_notification)
async def set_firstday(call: CallbackQuery, state: FSMContext, bot: Bot):
    first_day = call.data.split('_')[1]
    await state.update_data(first_day = first_day)
    await call.message.answer(f"Выбран {first_day}. Выберите до какого дня бот будет напоминать о выполнении отчета. Если напоминать нужно только в один день, то нажмите кнопку СОХРАНИТЬ", reply_markup=weekdays(InlineKeyboardButton(text='Сохранить', callback_data=f"save_dates")))#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!save_dates
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await state.set_state(SetConfigsToBot.set_notification1)
    await call.answer()


@router.callback_query(F.data.startswith('dayofweek_'), SetConfigsToBot.set_notification1)
async def set_secondday(call: CallbackQuery, state: FSMContext, bot: Bot):
    second_day = call.data.split('_')[1]
    await state.update_data(second_day = second_day)
    await call.message.answer(f"Выбран {second_day}. Теперь нужно выбрать время в которое будет приходить оповещение. По умолчанию оно стоит на 20.00, если это время Вам подходит, то нажмите на кнопку СОХРАНИТЬ иначе выберите час.", reply_markup=hours(InlineKeyboardButton(text='Сохранить', callback_data="save_hour")))#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!save_hour
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await state.set_state(SetConfigsToBot.set_notification2)
    await call.answer()

@router.callback_query(F.data.startswith('hour_'), SetConfigsToBot.set_notification2)
async def set_hour(call: CallbackQuery, state: FSMContext, bot: Bot):
    hour = call.data.split('_')[1]
    await state.update_data(hour = hour)
    await call.message.answer(f"Выбран час {hour}. Выберите во сколько минут", reply_markup=mins())#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await state.set_state(SetConfigsToBot.set_notification_final)
    await call.answer()

from btns.users_replybtn import user_replybtns
@router.callback_query(F.data.startswith('minute_'), SetConfigsToBot.set_notification_final)
async def set_mins(call: CallbackQuery, state: FSMContext, bot: Bot):
    minute = call.data.split('_')[1]
    #await state.update_data(minute = minute)
    user_data = await state.get_data()
    # print(type(call.message.chat.id))#------------------------------------------integer
    # print(type(admin_id))#------------------------------------------------------string
    if call.message.chat.id  == int(admin_id):
        data = select_data("SELECT * FROM usernames WHERE telega_id = ?", (admin_id,))
        if data == []:
            delete_or_insert_data("INSERT INTO usernames (name, telega_id, hour, minute, period) VALUES (?, ?, ?, ?, ?)", ('Admin', call.message.chat.id, user_data['hour'], minute, f"{user_data['first_day']}-{user_data['second_day']}",))
        else:
            delete_or_insert_data("UPDATE usernames SET telega_id = ?, hour=?, minute=?, period=? WHERE name = ?", (call.message.chat.id, user_data['hour'], minute, f"{user_data['first_day']}-{user_data['second_day']}", 'admin'))
        await call.message.answer(f"Выбрано время {user_data['hour']}:{minute}.\nДни оповещений: {user_data['first_day']}-{user_data['second_day']}", reply_markup=admin_replybtns())
    else:
        delete_or_insert_data("UPDATE usernames SET telega_id = ?, hour=?, minute=?, period=? WHERE name = ?", (call.message.chat.id, user_data['hour'], minute, f"{user_data['first_day']}-{user_data['second_day']}", user_data['name']))
        await call.message.answer(f"Выбрано время {user_data['hour']}:{minute}. Настройки бота завершены.", reply_markup=user_replybtns())#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await state.clear()
    await call.answer()


from handlers.user_settings import call_users_settings
@router.callback_query(F.data == 'users')
async def usr_stgs(call: CallbackQuery, bot: Bot):
    await call_users_settings(call, bot) # add_users | delete_user | edit_user | back

#------------------------------------------------------------------------------------------------------АДМИН ДОБАВЛЯЕТ ПОЛЬЗОВАТЕЛЕЙ------------------------------------------------------------------------------------
@router.callback_query(F.data == 'add_users', StateFilter(None))
async def usr_stgs(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await call.message.answer(f"Напишите пожалуйста через запятую имена пользоватей (если пользователь один просто впишите имя без знаков препинания).")
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()
    await state.set_state(SetConfigsToBot.set_user_names)


from btns.users_edit_btns import get_users_settings

@router.message(SetConfigsToBot.set_user_names)
async def usr_stgs_sub(message: Message, state: FSMContext, bot: Bot):
    users_list = [(name.strip(), ) for name in message.text.split(',')]
    insert_many("INSERT INTO usernames (name) VALUES(?)", users_list)
    await state.clear()
    await message.answer(f"{message.text} был(и) добален(ы)", reply_markup=get_users_settings())
    await bot.delete_messages(message.chat.id, (message.message_id-1, ))


#------------------------------------------------------------------------------------------------------АДМИН ИЗМЕНЯЕТ ИМЯ ПОЛЬЗОВАТЕЛЯ------------------------------------------------------------------------------------
from btns.users_for_edit import users_for_edit
@router.callback_query(F.data == 'edit_user')
async def usr_stgs_edit(call: CallbackQuery, bot: Bot):
    await call.message.answer(f"Выберите пользователя имя которого вы хотите изменить", reply_markup=users_for_edit('editusername_'))
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()

@router.callback_query(F.data.startswith('editusername_'), StateFilter(None))
async def edit_username(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    user = call.data.split('_')[1]
    await state.update_data(name = user)
    await call.message.answer(f"Вы хотите изменить имя \'{user}\'. В поле ввода внесите новое имя для пользователя \'{user}\'")
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await state.set_state(SetConfigsToBot.set_new_username)
    await call.answer()

@router.message(SetConfigsToBot.set_new_username)
async def new_usrname(message: Message, state: FSMContext, bot: Bot):
    #await state.clear()
    user = await state.get_data()
    await bot.delete_messages(message.chat.id, (message.message_id-1, ))
    delete_or_insert_data("UPDATE usernames SET name = ? WHERE name = ?", (message.text, user['name']))
    await message.answer(f"Вы изменили имя {user['name']} на {message.text}", reply_markup=get_users_settings())
    await state.clear()


#------------------------------------------------------------------------------------------------------АДМИН УДАЛЯЕТ ИМЯ ПОЛЬЗОВАТЕЛЯ------------------------------------------------------------------------------------
@router.callback_query(F.data == 'delete_user')
async def usr_stgs_delete(call: CallbackQuery, bot: Bot):
    await call.message.answer(f"Выберите пользователя имя которого вы хотите удалить", reply_markup=users_for_edit('deleteusername_'))
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()

@router.callback_query(F.data.startswith('deleteusername_'), StateFilter(None))
async def edit_username(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    user = call.data.split('_')[1]
    delete_or_insert_data("DELETE FROM usernames WHERE name = ?", (user, ))
    await call.message.answer(f"Вы удалили \'{user}\'.'", reply_markup=get_users_settings())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()

#------------------------------------------------------------------------------------------------------АДМИН ДЕЛАЕТ ВОЗВРАТ НА ГЛАВНУЮ------------------------------------------------------------------------------------
@router.callback_query(F.data == 'back_to_main_menu')
async def back_to_main_menu(call: CallbackQuery, bot: Bot):
    await call.message.answer(f"Главное меню администратора", reply_markup=admin_btns())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()


@router.message(F.text == "Администрация")
async def admin_menu_proccess(message: Message, bot: Bot):
    await message.answer("Главное меню администратора", reply_markup=admin_btns())
    #await bot.delete_messages(message.chat.id, (message.message_id-1, ))

#------------------------------------------------------------------------------------------------------АДМИН выполняет возврат к гглавной поинтов------------------------------------------------------------------------------------

@router.callback_query(F.data == 'back_to_points_main_menu')
async def usr_stgs_delete(call: CallbackQuery, bot: Bot):
    await call.message.answer(f"Меню пункты", reply_markup=points_main_menu())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()

#------------------------------------------------------------------------------------------------------АДМИН ДОБАВЛЯЕТ ПУНКТЫ ПРОГРЕССА------------------------------------------------------------------------------------
from btns.points_main import points_main_menu
@router.callback_query(F.data == 'points')
async def back_to_main_menu(call: CallbackQuery, bot: Bot):
    await call.message.answer(f"Выберите опцию для пунктов прогресса", reply_markup=points_main_menu())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()


@router.callback_query(F.data == 'add_progress_points', StateFilter(None))
async def usr_stgs(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await call.message.answer(f"Напишите боту название пункта прогресса.")
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()
    await state.set_state(SetConfigsToBot.set_points_score)


@router.message(SetConfigsToBot.set_points_score)
async def usr_stgs_sub(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(point_name = message.text)
    await message.answer(f"Напишите боту коэффициент для {message.text}", reply_markup=back_btn("back_to_points_main_menu"))
    await bot.delete_messages(message.chat.id, (message.message_id-1, ))
    await state.set_state(SetConfigsToBot.set_points_min)


@router.message(SetConfigsToBot.set_points_min)
async def usr_stgs_sub(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(point_score = message.text)
    score_data = await state.get_data()
    await message.answer(f"Напишите боту минимум для {score_data['point_name']}, коэффициент которого {message.text}", reply_markup=back_btn("back_to_points_main_menu"))#!!!!!!!!!!!tut knopku nazad k predidushemu hodu nujno budet delat
    await bot.delete_messages(message.chat.id, (message.message_id-1, ))
    await state.set_state(SetConfigsToBot.set_points_names)


@router.message(SetConfigsToBot.set_points_names)
async def usr_stgs_sub(message: Message, state: FSMContext, bot: Bot):
    #points_list = [(name.strip(), ) for name in message.text.split(',')]
    score_data = await state.get_data()
    delete_or_insert_data("INSERT INTO points (name, ratio, mins) VALUES(?,?,?)", (score_data['point_name'], score_data['point_score'], message.text, ))
    await state.clear()
    await message.answer(f"{score_data['point_name']}, коэффициент - {score_data['point_score']} и минимум - {message.text} был добален", reply_markup=points_main_menu())
    await bot.delete_messages(message.chat.id, (message.message_id-1, ))

#------------------------------------------------------------------------------------------------------АДМИН ИЗМЕНЯЕТ ИМЯ ПУНКТОВ ПРОГРЕССА------------------------------------------------------------------------------------
from btns.points_for_edit import points_for_edit
@router.callback_query(F.data == 'edit_progress_points')
async def usr_stgs_edit(call: CallbackQuery, bot: Bot):
    await call.message.answer(f"Выберите пункт прогресса который вы хотите изменить", reply_markup=points_for_edit('editpoints_','Назад' 'back_to_points_main_menu'))
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()

@router.callback_query(F.data.startswith('editpoints_'), StateFilter(None))
async def edit_username(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    user = call.data.split('_')[1]
    await state.update_data(name = user)
    await call.message.answer(f"Вы хотите изменить имя \'{user}\'. В поле ввода внесите новое имя для пункта прогресса \'{user}\'")
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await state.set_state(SetConfigsToBot.set_new_pointname)
    await call.answer()

@router.message(SetConfigsToBot.set_new_pointname)
async def new_usrname(message: Message, state: FSMContext, bot: Bot):
    #await state.clear()
    user = await state.get_data()
    await bot.delete_messages(message.chat.id, (message.message_id-1, ))
    delete_or_insert_data("UPDATE points SET name = ? WHERE name = ?", (message.text, user['name']))
    await message.answer(f"Вы изменили имя {user['name']} на {message.text}", reply_markup=points_main_menu())
    await state.clear()



#------------------------------------------------------------------------------------------------------АДМИН УДАЛЯЕТ ПУНКТ ПРОГРЕССА------------------------------------------------------------------------------------
@router.callback_query(F.data == 'delete_progress_points')
async def usr_stgs_delete(call: CallbackQuery, bot: Bot):
    await call.message.answer(f"Выберите пункт прогресса который вы хотите удалить", reply_markup=points_for_edit('deletepoint_',"Назад", 'back_to_points_main_menu'))
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()


@router.callback_query(F.data.startswith('deletepoint_'), StateFilter(None))
async def edit_username(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    user = call.data.split('_')[1]
    delete_or_insert_data("DELETE FROM points WHERE name = ?", (user, ))
    await call.message.answer(f"Вы удалили \'{user}\'.'", reply_markup=points_main_menu())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()

#------------------------------------------------------------------------------------------------------АДМИН ПРОСМАТРИВАЕТ РЕЙТИНГ------------------------------------------------------------------------------------
@router.callback_query(F.data == 'users_progress')
async def usr_stgs_delete(call: CallbackQuery, bot: Bot):
    data = select_data("SELECT* FROM user_points INNER JOIN points ON points.name = user_points.point_name INNER JOIN usernames ON user_points.telega_id = usernames.telega_id")
    sovpadenie = False
    result = []
    for x in data:
        for z in result:
            if x[10] in z:
                sovpadenie = True
                z[1] = z[1] + (x[3] * x[7])
        if sovpadenie == False:
            result.append([x[10], x[3] * x[7]])
        sovpadenie = False
    sorted_data = sorted(result, key=lambda x: x[1], reverse=True)
    final_message = ''
    for i, (name, points) in enumerate(sorted_data):
        final_message = final_message + str(i+1) + " " + name + " "+ str(round(points, 2)) + "\n"
    await call.message.answer(final_message, reply_markup=admin_btns())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()



#------------------------------------------------------------------------------------------------------ЮЗЕР ВЫБИРАЕТ СВОЙ НИКНЕЙМ------------------------------------------------------------------------------------

from btns.user_main import user_main
@router.callback_query(F.data.startswith('userchosen_name_'))
async def edit_username(call: CallbackQuery, state: FSMContext, bot: Bot):
    user = call.data.split('_')[2]
    delete_or_insert_data("UPDATE usernames SET telega_id = ? WHERE name = ?", (call.message.chat.id, user, ))
    await call.message.answer(f"Теперь Ваш никнейм \'{user}\'", reply_markup = user_main())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()

#------------------------------------------------------------------------------------------------------ЮЗЕР ВЫПОЛНЯЕТ ВОЗВРАТ НА СВОЕ МЕНЮ------------------------------------------------------------------------------------
@router.callback_query(F.data == 'back_to_users_menu')
async def back_to_users_menu(call: CallbackQuery, bot: Bot):
    await call.message.answer(f"Главная пользователя", reply_markup=user_main())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()
#------------------------------------------------------------------------------------------------------ЮЗЕР ВЫПОЛНЯЕТ ОТЧЕТ------------------------------------------------------------------------------------

@router.callback_query(F.data == "otmena")
async def otmena(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id, ))
    await state.clear()
    await call.answer()

async def handle_usr_report(chat_id: int, message_id: int, bot: Bot):
    # await bot.delete_messages(chat_id, (message_id, message_id-1))
    await bot.send_message(chat_id, "Выберите пункт прогресса который вы хотите отметить", reply_markup=points_for_edit('checkpoint_', '❌ Отмена','otmena'))

@router.callback_query(F.data == 'user_report')
async def usr_report_process(call: CallbackQuery, bot: Bot):
    await handle_usr_report(call.message.chat.id, call.message.message_id, bot)
    await call.answer()


import re
@router.message(lambda message: re.search(r"^(Отчет|Мой отчет)$", message.text))
async def report_message_handler(message: Message, bot: Bot):
    await handle_usr_report(message.chat.id, message.message_id, bot)



@router.callback_query(F.data.startswith('checkpoint_'), StateFilter(None))
async def edit_checkpoint(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    checkpoint = call.data.split('_')[1]
    await state.update_data(check = checkpoint)
    await call.message.answer(f"Вы хотите отметить \'{checkpoint}\'. В поле ввода внесите выполненный прогресс")
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()
    await state.set_state(SetConfigsToBot.set_checkpoint)
    


from functions import is_date_in_current_week
from datetime import datetime, timedelta, date
@router.message(SetConfigsToBot.set_checkpoint)
async def edit_checkpoint_result(message: Message, state: FSMContext, bot: Bot):
    if re.match(r"^-?\d+(\.\,\d+)?$", message.text):
        score = message.text
        if ',' in score:
            score = score.replace(",", ".")
        #await state.clear()
        user = await state.get_data()
        await bot.delete_messages(message.chat.id, (message.message_id-1, ))
        last_user_point_record_list = select_data("SELECT* FROM user_points WHERE point_name = ? AND telega_id = ? ORDER BY id DESC LIMIT 1", (user['check'], message.chat.id,))#(2, 'kkk', 6293086969, 6, '2024-11-06')
        #print(last_user_point_record_list)
        if last_user_point_record_list == []:
            delete_or_insert_data("insert into user_points (point_name, telega_id, score, date) values (?, ?, ?, ?)", (user['check'], message.chat.id, score, date.today()))
        else:
            last_user_point_record_list = last_user_point_record_list[0]    
            date_convert = date.fromisoformat(last_user_point_record_list[-1])
            if is_date_in_current_week(date_convert):
                new_score = int(last_user_point_record_list[3]) + int(score)
                delete_or_insert_data("UPDATE user_points SET score = ?, date = ? WHERE id = ?", (new_score, date.today(), last_user_point_record_list[0]))
            else:
                delete_or_insert_data("insert into user_points (point_name, telega_id, score, date) values (?, ?, ?, ?)", (user['check'], message.chat.id, score, date.today()))
        await message.answer(f"Ваша отметка на {user['check']} выставлена", reply_markup=points_for_edit('checkpoint_', 'Назад', 'back_to_users_menu'))
        await state.clear()
    else:
        await message.answer("Вы ввели невалидное значение. Внесите числовое значение.")
        await state.set_state(SetConfigsToBot.set_checkpoint)
        
    


#------------------------------------------------------------------------------------------------------ЮЗЕР ПРОСМАТРИВАЕТ СВОЙ РЕЙТИНГ------------------------------------------------------------------------------------

# from btns.points_for_edit import points_for_edit
@router.callback_query(F.data == 'user_rating')
async def usr_report_process(call: CallbackQuery, bot: Bot):
    data = select_data("SELECT* FROM user_points INNER JOIN points ON points.name = user_points.point_name")
    sovpadenie = False
    result = []
    for x in data:
        for z in result:
            if x[2] in z:
                sovpadenie = True
                z[1] = z[1] + (x[3] * x[-2])
        if sovpadenie == False:
            result.append([x[2], x[3] * x[-2]])
        sovpadenie = False
    sorted_data = sorted(result, key=lambda x: x[1], reverse=True)
    # Значение, которое мы хотим найти
    search_id = call.message.chat.id
    # Поиск элемента и определение индекса
    index = -1  # Начальное значение, если элемент не найден
    from_all = len(sorted_data)
    for i, (id_value, value) in enumerate(sorted_data):
        if id_value == search_id:
            index = i
            break
    await call.message.answer(f"В настоящий момент Вы на {index+1} месте из {from_all}", reply_markup=user_main())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()


#------------------------------------------------------------------------------------------------------ЮЗЕР ПРОСМАТРИВАЕТ МИНИМУМЫ------------------------------------------------------------------------------------
@router.callback_query(F.data == 'mins')
async def usr_stgs_delete(call: CallbackQuery, bot: Bot):
    data = select_data("SELECT*FROM points")#[(1, 'kkk', 2, 10), (3, 'джф', 1.3, 30), (4, 'kit', 1, 60)]
    output = ""
    for x in data:
        out_el = str(x[1]) + ": " +str(x[-1]) + "\n"
        output = output + out_el

    #print(output)
    await call.message.answer(f"Минимумы:\n {output}", reply_markup=user_main())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()


@router.message(F.text == "Остальное")
async def another_proccess(message:Message, bot: Bot):
    await message.answer("Другие возможности", reply_markup=user_main())
    #await bot.delete_messages(message.chat.id, (message.message_id-1, ))


#------------------------------------------------------------------------------------------------------АДМИН ЗАДАЕТ ОПОВЕЩЕНИЯ------------------------------------------------------------------------------------
from btns.admin_notifations import notifications_btns
@router.callback_query(F.data == 'admin_notifications')
async def notification_inial_proccess(call: CallbackQuery, bot: Bot):
    await call.message.answer('Меню оповещении', reply_markup=notifications_btns())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()

#------------------------------------------------------------------------------------------------------АДМИН ЗАДАЕТ редлайн для пользователей------------------------------------------------------------------------------------
@router.callback_query(F.data == 'users_notification_redline')
async def notification_inial_proccess(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await call.message.answer('Здесь вы задаете время в которое отчет в виде Excel файла будет приходить Вам. Для этого давайте отметим время и день напоминия редлайна.\nВыберите пожалуйста ЧАС в который Вам будет приходить напоминание', reply_markup=hours())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await state.set_state(SetConfigsToBot.set_redline_hour)
    await call.answer()

@router.callback_query(F.data.startswith('hour_'), SetConfigsToBot.set_redline_hour)
async def set_redline_hour(call:CallbackQuery, bot: Bot, state: FSMContext):
    redline_hour = call.data.split('_')[1]
    await state.update_data(redline_hour = redline_hour)
    await minutes_dialogue_process(call, bot, state, f'Вы выбрали {redline_hour} час. Выберите пожалуйста МИНУТЫ в которые Вам будет приходить напоминание')

async def minutes_dialogue_process(call, bot, state, msg):
    await call.message.answer(msg, reply_markup=mins(InlineKeyboardButton(text="Назад", callback_data="users_notification_redline")))
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()
    await state.set_state(SetConfigsToBot.set_redline_day)

@router.callback_query(F.data == "minutes_dialog_proccess")
async def fff(call: CallbackQuery, bot: Bot, state: FSMContext):
    await minutes_dialogue_process(call, bot, state, 'Выберите пожалуйста МИНУТЫ в которые Вам будет приходить напоминание')


@router.callback_query(F.data.startswith('minute_'), SetConfigsToBot.set_redline_day)
async def set_redline_minute(call: CallbackQuery, bot: Bot, state: FSMContext):
    minute = call.data.split('_')[1]
    await state.update_data(minute = minute)
    await call.message.answer('Выберите пожалуйста ДЕНЬ в котороый Вам будет приходить напоминание', reply_markup=weekdays(InlineKeyboardButton(text="Назад", callback_data="minutes_dialog_proccess")))
    await call.answer()
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await state.set_state(SetConfigsToBot.set_redline_final)


from btns.weekdays_btns import back_btn
@router.callback_query(F.data.startswith('dayofweek_'), SetConfigsToBot.set_redline_final)
async def set_finally_redline_notification(call: CallbackQuery, bot: Bot, state: FSMContext):
    redline_day = call.data.split('_')[1]
    redline_notification = await state.get_data()
    await call.message.answer(f"Время получения отчета: {redline_notification['redline_hour']}:{redline_notification['minute']}.\nДень получения отчета: {redline_day}.", reply_markup=admin_replybtns())#, reply_markup=back_btn("Назад", f"")
    delete_or_insert_data("UPDATE admin SET red_hour = ?, red_minute = ?, red_day = ? WHERE telega_id = ?", (redline_notification['redline_hour'], redline_notification['minute'], redline_day, call.message.chat.id))
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1))
    await call.answer()
    await state.clear()


@router.callback_query(F.data == "admin_notifacion")
async def start_admin_notification(call: CallbackQuery, bot: Bot, state: FSMContext):
    await set_firstday_of_notification(call.message, state, bot, "Здесь вы можете поставить напоминия о выполненении своего отчета. Выберите с какого дня недели бот будет напоминать о выполнении отчета. Если день один то выберите день, а на следующем этапе нажмите кнопку СОХРАНИТЬ")

