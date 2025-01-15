from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
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
from aiogram.exceptions import TelegramBadRequest

load_dotenv()  # Загрузка переменных из файла .env
admin_id = os.getenv('ADMIN_ID')


router = Router()  # [1]

from handlers.for_start import start_func
@router.message(Command("start"))  # [2]
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    exist_user = select_data("SELECT*FROM usernames WHERE telega_id = ?", (message.chat.id, ))
    if exist_user == []:
        await start_func(message, state, 'Здравствуйте. Введите пожалуйста пароль, выданный администратором', SetConfigsToBot.set_password, bot)
    else:
        if message.chat.id == int(admin_id):
           await message.answer("⚔⚔⚔", reply_markup=admin_replybtns())
        else:
           await message.answer("🚀🛸🛰", reply_markup=user_replybtns())
    await bot.delete_message(message.chat.id, message.message_id)



from handlers.for_get_password import correct_password_proccess
@router.message(SetConfigsToBot.set_password)
async def sss_psw(message: Message, state: FSMContext, bot: Bot):
    await correct_password_proccess(message, state, bot)#tut prodoljaetsya algoritm dlya userov-----SetConfigsToBot.set_name

from handlers.for_get_password import if_user
from btns.weekdays_btns import weekdays, hours, mins
from btns.notify_yesno import should_notify
@router.message(SetConfigsToBot.set_name)
async def set_name(message: Message, state: FSMContext, bot: Bot):
    isusers_exist = select_data("SELECT name FROM usernames")
    if isusers_exist == []:
        await message.answer("Администратор еще не задал имена")
        await bot.delete_messages(message.chat.id, (message.message_id-1, ))
    else:
        data = select_data("SELECT name FROM usernames WHERE name = ?", (message.text,))
        
        if data == [] or message.text == 'Admin':
            # print(data)
            # print(message.text)
            #await message.answer('Такого никнейма нет. Проверьте правильность написанияния или обратитесь к администратору')
            await if_user(message, bot, state, 'Такого никнейма нет. Проверьте правильность написанияния и попробуйте повторить ввод. Если после многократного ввода вы не оказались на следующем шаге авторизации, обратитесь к администратору.', SetConfigsToBot.set_name)
            
        else:
            await message.answer("Нужно ли Вам, чтобы бот напоминал о заполнении отчета", reply_markup=should_notify())
            await bot.delete_messages(message.chat.id, (message.message_id, message.message_id-1))
            await state.update_data(name1 = message.text)
            

@router.callback_query(F.data == 'notifyme')
async def notifyme(call: CallbackQuery, state: FSMContext, bot: Bot):
    await set_firstday_of_notification(call.message, state, bot, "Отлично! Выберите с какого дня недели бот будет напоминать о выполнении отчета. Если день один то выберите день, а на следующем этапе нажмите кнопку СОХРАНИТЬ")


@router.callback_query(F.data == 'backtofirstday')
async def frst_day(call: CallbackQuery, state: FSMContext, bot: Bot):
    await set_firstday_of_notification(call.message, state, bot, "Выберите с какого дня недели бот будет напоминать о выполнении отчета. Если день один то выберите день, а на следующем этапе нажмите кнопку СОХРАНИТЬ")


from aiogram.types import InlineKeyboardButton
@router.callback_query(F.data.startswith('dayofweek_'), SetConfigsToBot.set_notification)
async def set_firstdaycaller(call: CallbackQuery, state: FSMContext, bot: Bot):
    # first_day = call.data.split('_')[1]
    await set_firstday(call, state, bot, )


async def set_firstday(call, state, bot):
    try:
        first_day = call.data.split('_')[1]
        await state.update_data(first_day = first_day)
    except IndexError:
        state_data = await state.get_data()
        first_day = state_data['first_day']
    # print(first_day)
    # print(first_day)
    save_btn = None
    end_text = ''
    backto_firstday = InlineKeyboardButton(text='⬅ Назад', callback_data="backtofirstday")
    if first_day != '':
        save_btn = InlineKeyboardButton(text='✅ Сохранить', callback_data=f"savedates")
        end_text = 'Если напоминать нужно только в один день, то нажмите кнопку СОХРАНИТЬ'
    await call.message.answer(f"Выбран {first_day}. Выберите до какого дня бот будет напоминать о выполнении отчета. {end_text}", reply_markup=weekdays(first_day, nazad=backto_firstday, sohranit=save_btn))#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!save_dates
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await state.set_state(SetConfigsToBot.set_notification1)
    await call.answer()


@router.callback_query(F.data == "backtosecondday")
async def secondday_caller(call: CallbackQuery, state: FSMContext, bot: Bot):
    await set_firstday(call, state, bot)


async def second_day_proccess(call, state, bot, text):
    save_button = InlineKeyboardButton(text='✅ Сохранить', callback_data="save_hour")
    back_button = InlineKeyboardButton(text='⬅ Назад', callback_data="backtosecondday")
    await call.message.answer(text, reply_markup = hours(sohranit=save_button, nazad=back_button))
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await state.set_state(SetConfigsToBot.set_notification2)
    await call.answer()


@router.callback_query(F.data == "save_hour")
async def save_hour(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.update_data(hour = '20', minute = '00')
    #await state.update_data(minute = '00')
    await notificationtime_saver(call, state, bot)




@router.callback_query(F.data == "savedates" , SetConfigsToBot.set_notification1)
async def set_secondday(call: CallbackQuery, state: FSMContext, bot: Bot):
    await second_day_proccess(call, state, bot, "Теперь нужно выбрать время в которое будет приходить оповещение. По умолчанию оно стоит на 20.00, если это время Вам подходит, то нажмите на кнопку СОХРАНИТЬ иначе выберите час.")


@router.callback_query(F.data.startswith('dayofweek_'), SetConfigsToBot.set_notification1)
async def set_secondday(call: CallbackQuery, state: FSMContext, bot: Bot):
    second_day = call.data.split('_')[1]
    await state.update_data(second_day = second_day)
    await second_day_proccess(call, state, bot, f"Выбран {second_day}. Теперь нужно выбрать время в которое будет приходить оповещение. По умолчанию оно стоит на 20.00, если это время Вам подходит, то нажмите на кнопку СОХРАНИТЬ иначе выберите час.")

@router.callback_query(F.data == "backtohours")
async def set_secondday(call: CallbackQuery, state: FSMContext, bot: Bot):
    await second_day_proccess(call, state, bot, "Теперь нужно выбрать время в которое будет приходить оповещение. По умолчанию оно стоит на 20.00, если это время Вам подходит, то нажмите на кнопку СОХРАНИТЬ иначе выберите час.")


@router.callback_query(F.data.startswith('hour_'), SetConfigsToBot.set_notification2)
async def set_hour(call: CallbackQuery, state: FSMContext, bot: Bot):
    hour = call.data.split('_')[1]
    await state.update_data(hour = hour)
    backto_hours = InlineKeyboardButton(text='⬅ Назад', callback_data="backtohours")
    await call.message.answer(f"Выбран час {hour}. Выберите во сколько минут", reply_markup=mins(nazad=backto_hours))#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await state.set_state(SetConfigsToBot.set_notification_final)
    await call.answer()

from btns.users_replybtn import user_replybtns

@router.callback_query(F.data == "dontnotifyme")
async def dontnotifyme(call: CallbackQuery, state: FSMContext, bot: Bot):
    name1 = await state.get_data()
    delete_or_insert_data("UPDATE usernames SET telega_id = ? WHERE name = ?", (call.message.chat.id, name1['name1'],))
    await call.message.answer("Вам доступно выполнение отчета. В меню \"Остальное\" Вы сможете просмотреть свой рейтинг, прогресс выполнения отчета и др", reply_markup=user_replybtns())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1,))
    await state.clear()
    await call.answer()


@router.callback_query(F.data.startswith('minute_'), SetConfigsToBot.set_notification_final)
async def set_mins(call: CallbackQuery, state: FSMContext, bot: Bot):
    await notificationtime_saver(call, state, bot)


async def notificationtime_saver(call, state, bot):
    user_data = await state.get_data()
    print(user_data)
    try:
        minute = user_data["minute"]
    except KeyError:
        minute = call.data.split('_')[1]
    
    try:
        period = f"{user_data['first_day']}-{user_data['second_day']}"
    except KeyError:
        period = f"{user_data['first_day']}"

    if call.message.chat.id  == int(admin_id):
        data = select_data("SELECT * FROM usernames WHERE telega_id = ?", (admin_id,))
        if data == []:
            delete_or_insert_data("INSERT INTO usernames (name, telega_id, hour, minute, period) VALUES (?, ?, ?, ?, ?)", ('Admin', call.message.chat.id, user_data['hour'], minute, f"{period}",))
        else:
            delete_or_insert_data("UPDATE usernames SET telega_id = ?, hour=?, minute=?, period=? WHERE name = ?", (call.message.chat.id, user_data['hour'], minute, f"{period}", 'Admin'))
        await call.message.answer(f"Выбрано время {user_data['hour']}:{minute}.\nДни оповещений: {period}", reply_markup=admin_replybtns())
    else:
        print(user_data['name'])
        if user_data['name'] == "Другие возможности":#----------------------------------------------------- !!! TUT VOZMOJENi OSHIBKI !!! --------------------------------------
            delete_or_insert_data("UPDATE usernames SET hour=?, minute=?, period=? WHERE telega_id = ?", (user_data['hour'], minute, f"{period}", call.message.chat.id, ))
        else:
            delete_or_insert_data("UPDATE usernames SET telega_id = ?, hour=?, minute=?, period=? WHERE name = ?", (call.message.chat.id, user_data['hour'], minute, f"{period}", user_data['name']))
        await call.message.answer(f"Выбрано время {user_data['hour']}:{minute}. \nДни оповещений: {period}", reply_markup=user_replybtns())#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await state.clear()
    await call.answer()

from handlers.user_settings import call_users_settings
@router.callback_query(F.data == 'users')
async def usr_stgs(call: CallbackQuery, bot: Bot):
    await call_users_settings(call, bot) # add_users | delete_user | edit_user | back

#------------------------------------------------------------------------------------------------------АДМИН ПРОСМАТРИВАЕТ ПОЛЬЗОВАТЕЛЕЙ----------------------------------------------
@router.callback_query(F.data == 'list_users')
async def show_users(call: CallbackQuery, state: FSMContext, bot: Bot):
    usernames = select_data("SELECT name FROM usernames")#[('цска',), ('динамо',), ('Admin',), ('Барселона',)]
    if usernames == []:
        await call.message.answer("Список пользователей пуст", reply_markup=back_btn('⬅Назад', 'users'))
    else:
        usernames_msg = ''
        for i, (name, ) in enumerate(usernames):
            usernames_msg += str(i+1) + ") "+ name +'\n'
        await call.message.answer(f"Список пользователей:\n {usernames_msg}", reply_markup=back_btn('⬅Назад', 'users'))
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()
#------------------------------------------------------------------------------------------------------АДМИН ДОБАВЛЯЕТ ПОЛЬЗОВАТЕЛЕЙ-----------------------------------------------------
@router.callback_query(F.data == 'add_users', StateFilter(None))
async def usr_stgs(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await call.message.answer(f"Напишите пожалуйста через запятую имена пользоватей (если пользователь один просто впишите имя без знаков препинания).", reply_markup=back_btn('⬅Назад', 'users'))
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


#------------------------------------------------------------------------------------------------------АДМИН ИЗМЕНЯЕТ ИМЯ ПОЛЬЗОВАТЕЛЯ-------------------------------------------------
from btns.users_for_edit import users_for_edit
@router.callback_query(F.data == 'edit_user')
async def usr_stgs_edit(call: CallbackQuery, bot: Bot):
    usernames = select_data("SELECT name FROM usernames")#[('цска',), ('динамо',), ('Admin',), ('Барселона',)]
    for x in usernames:
        if x[0] == 'Admin':
            usernames.remove(x)
    if usernames == []:
        await call.message.answer("Список пользователей пуст", reply_markup=back_btn('⬅Назад', 'users'))
    else:
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


#------------------------------------------------------------------------------------------------------АДМИН УДАЛЯЕТ ИМЯ ПОЛЬЗОВАТЕЛЯ--------------------------------------------------------
@router.callback_query(F.data == 'delete_user')
async def usr_stgs_delete(call: CallbackQuery, bot: Bot):
    usernames = select_data("SELECT name FROM usernames")#[('цска',), ('динамо',), ('Admin',), ('Барселона',)]
    for x in usernames:
        if x[0] == 'Admin':
            usernames.remove(x)
    if usernames == []:
        await call.message.answer("Список пользователей пуст", reply_markup=back_btn('⬅Назад', 'users'))
    else:
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
#------------------------------------------------------------------------------------------------------АДМИН выполняет очистку прогресса------------------------------------------------------
from btns.delete_menu import delete_options
@router.callback_query(F.data == 'deleteprogress_menu')
async def deleteprogress_menu(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await call.message.answer("Вы уверены что ходите удалить прогресс польззователей?", reply_markup=delete_options())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()

from btns.cancel import zakrit_btn
@router.callback_query(F.data == 'delete_allprogress')
async def deleteallprogress(call: CallbackQuery, bot: Bot, state: FSMContext):
    delete_or_insert_data("DELETE FROM user_points")
    await state.clear()
    await call.message.answer("Прогресс пользователей очищен", reply_markup=zakrit_btn())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()
#------------------------------------------------------------------------------------------------------АДМИН ДЕЛАЕТ ВОЗВРАТ НА ГЛАВНУЮ--------------------------------------------------------
@router.callback_query(F.data == 'back_to_main_menu')
async def back_to_main_menu(call: CallbackQuery, bot: Bot):
    await call.message.answer(f"Главное меню администратора", reply_markup=admin_btns())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()


@router.message(F.text == "Администрация")
async def admin_menu_proccess(message: Message, state: FSMContext, bot: Bot):
    if message.chat.id == int(admin_id):
        await message.answer("Главное меню администратора", reply_markup=admin_btns())
    await state.clear() 
    await bot.delete_messages(message.chat.id, (message.message_id, ))
    #await bot.delete_messages(message.chat.id, (message.message_id-1, ))

#------------------------------------------------------------------------------------------------------АДМИН  получает EXCEL отчет------------------------------------------------------
from excel_creator import exsel_creator
@router.callback_query(F.data == 'excel_report')
async def send_excel(call: CallbackQuery, bot: Bot):
    exsel_creator()
    import datetime
    day = datetime.datetime.now().strftime("%Y-%m-%d")
    file_path = f'excels/{day}.xlsx'  # Обязательно проверьте, что путь и расширение файла указаны правильно
    if os.path.exists(file_path):
        await bot.send_document(call.message.chat.id, FSInputFile(file_path))
        await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    else:
        await call.message.answer("Что-то пошло не так. Попробуйте снова или напишите разработчику: @Dinis_Fizik", reply_markup=admin_btns())
    # else:
    #     await call.message.answer("Файл не найден.")
    await call.answer()



#------------------------------------------------------------------------------------------------------АДМИН выполняет возврат к гглавной поинтов----------------------------------------------

@router.callback_query(F.data == 'back_to_points_main_menu')
async def usr_stgs_delete(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.answer(f"Меню пункты", reply_markup=points_main_menu())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await state.clear()
    await call.answer()

#------------------------------------------------------------------------------------------------------АДМИН просматривает ПУНКТЫ ПРОГРЕССА---------------------------------------------------
@router.callback_query(F.data == 'list_progresspoints')
async def show_progresspoints(call:CallbackQuery, state: FSMContext, bot: Bot):
    progress_points = select_data("SELECT * FROM points")
    if progress_points == []:
        await call.message.answer("Пунктов еще нет", reply_markup=back_btn("⬅ Назад", 'back_to_points_main_menu'))
    else:
        msg = '№   ИМЯ   КОЭФТ   МИНИМУМ\n'
        for i, (id, name, score, mins,) in enumerate(progress_points):
            msg += f"{i+1})  {name}    {score}     {mins}\n"
        await call.message.answer(msg, reply_markup=back_btn("⬅ Назад", 'back_to_points_main_menu'))
    await call.answer()
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
#------------------------------------------------------------------------------------------------------АДМИН ДОБАВЛЯЕТ ПУНКТЫ ПРОГРЕССА---------------------------------------------------
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
    point_name = await state.get_data()
    await set_score_topoint(message, bot, state, point_name["point_name"])

async def set_score_topoint(message, bot, state, text):
    await message.answer(f"Напишите боту коэффициент для {text}, в виде (2 или 1.2)", reply_markup=back_btn("Назад","back_to_points_main_menu"))
    await bot.delete_messages(message.chat.id, (message.message_id, message.message_id-1, ))
    await state.set_state(SetConfigsToBot.set_points_min)


@router.callback_query(F.data == "back_to_set_point_score")
async def back_to_set_point_score(call:CallbackQuery, state: FSMContext, bot: Bot):
    point_name = await state.get_data()
    await set_score_topoint(call.message, bot, state, point_name["point_name"])
    await call.answer()

@router.message(SetConfigsToBot.set_points_min)
async def usr_stgs_sub(message: Message, state: FSMContext, bot: Bot):
    if re.match(r'^(\d+(\.\d*)?|\.\d+)$', message.text):
        score = message.text
        if ',' in message.text:
            score = message.text.replace(",", ".").replace(" ", "")
        await state.update_data(point_score = score)
        await set_min1(message, state)
        await state.set_state(SetConfigsToBot.set_points_names)
    else:
        await message.answer(f"Введено невалидное значение коэффициента, пожалуйста повторите ввод", reply_markup=back_btn("Назад", "add_progress_points"))
        await state.set_state(SetConfigsToBot.set_points_min)
    await bot.delete_messages(message.chat.id, (message.message_id, message.message_id-1, ))


# @router.callback_query(F.data == "back_to_set_min")
# async def set_min(call: CallbackQuery, state: FSMContext):
#     await set_min1(call, state)
#     call.answer()

async def set_min1(message, state):
    score_data = await state.get_data()
    txt = message.text
    if message.text == "" or message.text == None:
        txt = score_data['point_score']
    await message.answer(f"Напишите боту минимум для {score_data['point_name']}, коэффициент которого {txt}", reply_markup=back_btn("Назад","back_to_set_point_score"))
    await state.set_state(SetConfigsToBot.set_points_names)


@router.message(SetConfigsToBot.set_points_names)
async def usr_stgs_sub(message: Message, state: FSMContext, bot: Bot):
    #points_list = [(name.strip(), ) for name in message.text.split(',')]
    if re.match(r'^(\d+(\.\d*)?|\.\d+)$', message.text):
        min = message.text
        if ',' in message.text:
            min = message.text.replace(",", ".").replace(" ", "")
        score_data = await state.get_data()

        #print(score_data['edit_pointname'])

        try:
            delete_or_insert_data("UPDATE points SET name = ?, ratio = ?, mins = ? WHERE name = ?", (score_data['point_name'], score_data['point_score'], min, score_data['edit_pointname'], ))
        except KeyError:
            delete_or_insert_data("INSERT INTO points (name, ratio, mins) VALUES(?,?,?)", (score_data['point_name'], score_data['point_score'], min, ))
        await state.clear()
        await message.answer(f"{score_data['point_name']}, коэффициент - {score_data['point_score']} и минимум - {min} был добален", reply_markup=points_main_menu())
    else:
        await message.answer("Введено невалидное значение минимума, пожалуйста повторите ввод", reply_markup=back_btn("Назад", "back_to_set_min"))
    await bot.delete_messages(message.chat.id, (message.message_id, message.message_id-1, ))

#------------------------------------------------------------------------------------------------------АДМИН ИЗМЕНЯЕТ ИМЯ ПУНКТОВ ПРОГРЕССА------------------------------------------------------------------------------------
from btns.points_for_edit import points_for_edit
@router.callback_query(F.data == 'edit_progress_points')
async def usr_stgs_edit(call: CallbackQuery, bot: Bot):
    progress_points = select_data("SELECT * FROM points")
    if progress_points == []:
        await call.message.answer("Пунктов еще нет", reply_markup=back_btn("⬅ Назад", 'back_to_points_main_menu'))
    else:
        await call.message.answer(f"Выберите пункт прогресса который вы хотите изменить", reply_markup=points_for_edit('editpoints_','Назад', 'back_to_points_main_menu'))
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()

@router.callback_query(F.data.startswith('editpoints_'), StateFilter(None))
async def edit_username(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    user = call.data.split('_')[1]
    await state.update_data(edit_pointname = user)
    await call.message.answer(f"Вы хотите изменить пункт прогресса \'{user}\'. В поле ввода внесите новое имя для пункта прогресса \'{user}\'")
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    #await state.set_state(SetConfigsToBot.set_new_pointname)
    await state.set_state(SetConfigsToBot.set_points_score)
    await call.answer()

# @router.message(SetConfigsToBot.set_new_pointname)
# async def new_usrname(message: Message, state: FSMContext, bot: Bot):
#     #await state.clear()
#     user = await state.get_data()
#     await bot.delete_messages(message.chat.id, (message.message_id-1, ))
#     delete_or_insert_data("UPDATE points SET name = ? WHERE name = ?", (message.text, user['name']))
#     await message.answer(f"Вы изменили имя {user['name']} на {message.text}", reply_markup=points_main_menu())
#     await state.clear()



#------------------------------------------------------------------------------------------------------АДМИН УДАЛЯЕТ ПУНКТ ПРОГРЕССА----------------------------------------------------------
@router.callback_query(F.data == 'delete_progress_points')
async def usr_stgs_delete(call: CallbackQuery, bot: Bot):
    progress_points = select_data("SELECT * FROM points")
    if progress_points == []:
        await call.message.answer("Пунктов еще нет", reply_markup=back_btn("⬅ Назад", 'back_to_points_main_menu'))
    else:
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

#------------------------------------------------------------------------------------------------------АДМИН ПРОСМАТРИВАЕТ РЕЙТИНГ----------------------------------------------------------
@router.callback_query(F.data == 'users_progress')
async def usr_stgs_delete(call: CallbackQuery, bot: Bot):
    data = select_data("SELECT* FROM user_points INNER JOIN points ON points.name = user_points.point_name INNER JOIN usernames ON user_points.telega_id = usernames.telega_id")
    #progress_points = select_data("SELECT*FROM user_points")
    if data == []:
        await call.message.answer("Пока прогресс пользователей пуст", reply_markup=admin_btns())
    else:
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



#------------------------------------------------------------------------------------------------------ЮЗЕР ВЫБИРАЕТ СВОЙ НИКНЕЙМ--------------------------------------------------------

from btns.user_main import user_main
@router.callback_query(F.data.startswith('userchosen_name_'))
async def edit_username(call: CallbackQuery, state: FSMContext, bot: Bot):
    user = call.data.split('_')[2]
    delete_or_insert_data("UPDATE usernames SET telega_id = ? WHERE name = ?", (call.message.chat.id, user, ))
    await call.message.answer(f"Теперь Ваш никнейм \'{user}\'", reply_markup = user_main())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()

#------------------------------------------------------------------------------------------------------ЮЗЕР ВЫПОЛНЯЕТ ВОЗВРАТ НА СВОЕ МЕНЮ-----------------------------------------------------
@router.callback_query(F.data == 'back_to_users_menu')
async def back_to_users_menu(call: CallbackQuery, bot: Bot):
    await call.message.answer(f"Главная пользователя", reply_markup=user_main())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()
#------------------------------------------------------------------------------------------------------ЮЗЕР ВЫПОЛНЯЕТ ОТЧЕТ-----------------------------------------------------------

@router.callback_query(F.data == "otmena")
async def otmena(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id, ))
    await state.clear()
    await call.answer()

async def handle_usr_report(chat_id: int, message_id: int, bot: Bot):
    points_exist = select_data("SELECT*FROM points")
    if points_exist == []:
        await bot.send_message(chat_id, "Администратор еще не выставил пункты прогресса")
    else:
        await bot.send_message(chat_id, "Выберите пункт прогресса который вы хотите отметить", reply_markup=points_for_edit('checkpoint_', '❌ Отмена','otmena'))
    await bot.delete_messages(chat_id, (message_id, ))


@router.callback_query(F.data == 'user_report')
async def usr_report_process(call: CallbackQuery, bot: Bot):
    await handle_usr_report(call.message.chat.id, call.message.message_id, bot)
    await call.answer()


import re
@router.message(lambda message: re.search(r"^(Отчет|Мой отчет)$", message.text))
async def report_message_handler(message: Message, bot: Bot):
    user = select_data("SELECT * FROM usernames WHERE telega_id = ?", (message.chat.id,))
    if user != []:
        await handle_usr_report(message.chat.id, message.message_id, bot)



@router.callback_query(F.data.startswith('checkpoint_'), StateFilter(None))
async def edit_checkpoint(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    checkpoint = call.data.split('_')[1]
    await state.update_data(check = checkpoint)
    await call.message.answer(f"Вы хотите отметить \'{checkpoint}\'. В поле ввода внесите выполненный прогресс")
    try:
        await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    except TelegramBadRequest:
        print(f"У юзера {call.message.chat.id} плохо удаляется сообщение")
    await call.answer()
    await state.set_state(SetConfigsToBot.set_checkpoint)
    


#from functions import is_date_in_current_week
from datetime import datetime, timedelta, date

# async def userpoints_weekly_insertor(point_name, message, point_score):
#     delete_or_insert_data("INSERT INTO userpoints_weekly (point_name, telega_id, point_score, date)", (point_name, message.chat.id, point_score, date.today(), ))

@router.message(SetConfigsToBot.set_checkpoint)
async def edit_checkpoint_result(message: Message, state: FSMContext, bot: Bot):
    if re.match(r"^-?\d+(\.\,\d+)?$", message.text):
        score = message.text
        if ',' in score:
            score = score.replace(",", ".")
        #await state.clear()
        user = await state.get_data()
        await bot.delete_messages(message.chat.id, (message.message_id, message.message_id-1))
        delete_or_insert_data("INSERT INTO userpoints_weekly (point_name, telega_id, point_score, date) VALUES(?, ?, ?, ?)", (user['check'], message.chat.id, score, date.today(), ))
        last_user_point_record_list = select_data("SELECT* FROM user_points WHERE point_name = ? AND telega_id = ? ORDER BY id DESC LIMIT 1", (user['check'], message.chat.id,))#(2, 'kkk', 6293086969, 6, '2024-11-06')
        #print(last_user_point_record_list)
        if last_user_point_record_list == []:
            delete_or_insert_data("insert into user_points (point_name, telega_id, score, date) values (?, ?, ?, ?)", (user['check'], message.chat.id, score, date.today()))
        else:
            last_user_point_record_list = last_user_point_record_list[0]       
            new_score = int(last_user_point_record_list[3]) + int(score)
            delete_or_insert_data("UPDATE user_points SET score = ?, date = ? WHERE id = ?", (new_score, date.today(), last_user_point_record_list[0])) 
        if message.chat.id == int(admin_id):
            await message.answer(f"Ваша отметка {score} на {user['check']} выставлена", reply_markup=points_for_edit('checkpoint_', '⬅ Назад', 'back_to_main_menu', data = f"{score}_{user['check']}", zakrit=11))
        else:      
            await message.answer(f"Ваша отметка {score} на {user['check']} выставлена", reply_markup=points_for_edit('checkpoint_', '⬅ Назад', 'back_to_users_menu', data = f"{score}_{user['check']}", zakrit=11))
        await state.clear()
    else:
        await message.answer("Вы ввели невалидное значение. Внесите числовое значение.")
        await state.set_state(SetConfigsToBot.set_checkpoint)
        
#--------------------------------------------------------------------------------------Измение только выставленного поинта----------------------------------------------------------
from btns.cancel import otmena_btn
@router.callback_query(F.data.startswith('changecheckedpoint_'), StateFilter(None))
async def change_justadded_checkpoint(call: CallbackQuery, state: FSMContext, bot: Bot):
    #print(call.data)
    data = call.data.split("_")
    await call.message.answer(f"Напишите другое значение для {data[2]}. Последнее введенное значение равно {data[1]}", reply_markup=otmena_btn())
    await call.answer()
    await state.update_data(point_name = data[2], point_score = data[1])
    await state.set_state(SetConfigsToBot.set_changecheckpoint)
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1))

@router.message(SetConfigsToBot.set_changecheckpoint)
async def change_justadded_checkpoint1(message: Message, state: FSMContext, bot: Bot):
    if re.match(r"^-?\d+(\.\,\d+)?$", message.text):
        score = message.text
        if ',' in score:
            score = score.replace(",", ".")
        data_tochange = await state.get_data()
        try:
            last_checkpoint = select_data("SELECT*FROM user_points WHERE point_name = ? AND telega_id = ? AND date = ? ORDER BY id DESC LIMIT 1", (data_tochange['point_name'], message.chat.id, date.today()))[0]
            last_score = last_checkpoint[3]
            new_score = last_score - int(data_tochange['point_score']) + int(message.text)
            delete_or_insert_data("UPDATE user_points SET score = ? WHERE point_name = ? AND telega_id = ? AND date = ?", (new_score, data_tochange['point_name'], message.chat.id, date.today(), ))
            if message.chat.id == int(admin_id):
                await message.answer(f"Новое значение {message.text} для {data_tochange['point_name']} внесено", reply_markup=points_for_edit('checkpoint_', '⬅ Назад', 'back_to_main_menu', f"{score}_{data_tochange['point_name']}", zakrit=11))
            else:
                await message.answer(f"Новое значение {message.text} для {data_tochange['point_name']} внесено", reply_markup=points_for_edit('checkpoint_', '⬅ Назад', 'back_to_users_menu', f"{score}_{data_tochange['point_name']}", zakrit=11))
        except IndexError:
            if message.chat.id == int(admin_id):
                await message.answer(f"Не удалось выполнить изменение. Попробуйте внести отрицательное значение {data_tochange['point_score']} на {data_tochange['point_name']}", reply_markup=points_for_edit('checkpoint_', '⬅ Назад', 'back_to_main_menu', zakrit=11))
            else:      
                await message.answer(f"Не удалось выполнить изменение. Попробуйте внести отрицательное значение {data_tochange['point_score']} на {data_tochange['point_name']}", reply_markup=points_for_edit('checkpoint_', '⬅ Назад', 'back_to_users_menu', zakrit=11))
        await state.clear()    
    else:
        await message.answer("Вы ввели невалидное значение. Внесите числовое значение.")
        await state.set_state(SetConfigsToBot.set_changecheckpoint)
    await bot.delete_messages(message.chat.id, (message.message_id, message.message_id-1))

#------------------------------------------------------------------------------------------------------ЮЗЕР ПРОСМАТРИВАЕТ СВОЙ РЕЙТИНГ--------------------------------------------------------

# from btns.points_for_edit import points_for_edit
@router.callback_query(F.data == 'user_rating')
async def usr_report_process(call: CallbackQuery, bot: Bot):
    data = select_data("SELECT* FROM user_points INNER JOIN points ON points.name = user_points.point_name")
    if data == []:
        await call.message.answer("В настоящий момент эта функция неактивна", reply_markup=user_main())
    else:
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


#------------------------------------------------------------------------------------------------------ЮЗЕР ПРОСМАТРИВАЕТ МИНИМУМЫ------------------------------------------------------------
@router.callback_query(F.data == 'mins')
async def usr_stgs_delete(call: CallbackQuery, bot: Bot):
    data = select_data("SELECT*FROM points")#[(1, 'kkk', 2, 10), (3, 'джф', 1.3, 30), (4, 'kit', 1, 60)]
    if data == []:
        await call.message.answer("Минимумы еще не заданы", reply_markup=user_main())
    else:
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
    user = select_data("SELECT * FROM usernames WHERE telega_id = ?", (message.chat.id,))
    if user != []:
        await anotherfunc_proccess(message, bot)
    #await bot.delete_messages(message.chat.id, (message.message_id-1, ))


@router.callback_query(F.data == "backto_another")
async def hhh(call: CallbackQuery, bot: Bot):
    await anotherfunc_proccess(call.message, bot)

async def anotherfunc_proccess(message, bot):
    await bot.delete_messages(message.chat.id, (message.message_id, ))
    await message.answer("Другие возможности", reply_markup=user_main())



@router.callback_query(F.data == "user_progress")
async def user_progress(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    my_progress = select_data("SELECT*FROM user_points WHERE telega_id = ?", (call.message.chat.id, ))
    from btns.back_btn import back_btn
    if my_progress != []:
        msg = ''
        for x in my_progress:
            msg+=f"🔸 {x[1]} - {x[3]}\n"
        await call.message.answer(msg, reply_markup=back_btn(data="backto_another"))
    else:
        await call.message.answer("Пока Ваш прогресс пуст", reply_markup=back_btn(data="backto_another"))
    await call.answer()
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))

#------------------------------------------------------------------------------------------------------АДМИН ЗАДАЕТ ОПОВЕЩЕНИЯ----------------------------------------------------------------
from btns.admin_notifations import notifications_btns
@router.callback_query(F.data == 'admin_notifications')
async def notification_inial_proccess(call: CallbackQuery, bot: Bot):
    await call.message.answer('Меню оповещении', reply_markup=notifications_btns())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, ))
    await call.answer()

#------------------------------------------------------------------------------------------------------АДМИН ЗАДАЕТ редлайн для пользователей------------------------------------------------
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
    await call.message.answer('Выберите пожалуйста ДЕНЬ в котороый Вам будет приходить напоминание', reply_markup=weekdays(nazad=InlineKeyboardButton(text="Назад", callback_data="minutes_dialog_proccess")))
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
    await state.clear()
    await set_firstday_of_notification(call.message, state, bot, "Здесь вы можете поставить напоминия о выполненении своего отчета. Выберите с какого дня недели бот будет напоминать о выполнении отчета. Если день один то выберите день, а на следующем этапе нажмите кнопку СОХРАНИТЬ")
    call.answer()

async def set_firstday_of_notification(message, state, bot, text):
    await message.answer(text, reply_markup=weekdays(remove_day='', otmena=InlineKeyboardButton(text="❌ Отмена", callback_data="otmena")))
    await state.update_data(name = message.text)
    await state.set_state(SetConfigsToBot.set_notification) 
    await bot.delete_messages(message.chat.id, (message.message_id, ))


