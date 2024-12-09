from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from states import SetConfigsToBot
from db_func import select_data

from apscheduler.schedulers.asyncio import AsyncIOScheduler
scheduler = AsyncIOScheduler(timezone = "Asia/Yekaterinburg")

days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

def schedule_jobs():
    # message = Message()
    # state = FSMContext()
    # bot = Bot()
    #scheduler.add_job(noon_print, 'cron', day_of_week='mon-sat', hour=8, minute=20)
    # scheduler.add_job(noon_print, 'cron', day_of_week='mon-sat', hour=9, minute=15)
    # scheduler.add_job(schedule_for_admins, 'cron', day_of_week='mon-sat', hour=9, minute=30)
    #scheduler.add_job(schedule_for_admins, 'interval', seconds = 180, args=(message, state, bot))
    scheduler.add_job(schedule_for_users, 'interval', seconds = 300)
    scheduler.add_job(schedule_for_admins, 'interval', seconds = 120000)


async def schedule_for_admins():
    admin_data = select_data("SELECT*FROM admin")[0]#[(1, 'admin', 1949640271, '11', '30', 'Среда')]
    user_data = select_data("SELECT telega_id FROM usernames WHERE hour IS NOT NULL AND minute IS NOT NULL")#[(6293086969,), (1949640271,)]
    redtime_str = f"{admin_data[3]}:{admin_data[4]}"
    arr_to_notify = time_corrector(redtime_str)
    #scheduler.add_job(admin_notify, 'cron', day_of_week=str(days_of_week.index(admin_data[5])), hour=arr_to_notify[0], minute=arr_to_notify[1], args=(message, state, bot, x[2], redtime_str))
    for x in user_data:
        message = Message()
        state = FSMContext()
        bot = Bot()
        scheduler.add_job(redday_notify, 'cron', day_of_week=str(days_of_week.index(admin_data[5])), hour=arr_to_notify[0], minute=arr_to_notify[1], args=(message, state, bot, x[2], redtime_str))


async def schedule_for_users():
    data = select_data("SELECT*FROM usernames")#[(1, 'цска', 6293086969, '16', '00', 'Воскресенье-Воскресенье'), (2, 'динамо', None, None, None, None), (10, 'Admin', 1949640271, '9', '00', 'Понедельник-Воскресенье')]
    #print(data)
    for x in data:
        if x[3] != None and x[2] != None:
            #x[5] - den nedeli ('Воскресенье-Воскресенье')
            period_arr_str = x[5].split('-')
            period_str_int = f"{days_of_week.index(period_arr_str[0])}-{days_of_week.index(period_arr_str[1])}"  
            message = Message()
            state = FSMContext()
            bot = Bot()
            scheduler.add_job(noon_print, 'cron', day_of_week=period_str_int, hour=x[3], minute=x[4], args=(message, state, bot, x[2]))




from btns.users_replybtn import user_replybtns
async def noon_print(message: Message, state: FSMContext, bot: Bot, chat_id):
    await bot.send_message(chat_id, "Отправьте пожалуйста отчет по прогрессам.",reply_markup=user_replybtns)
    #await message.answer("Отправьте пожалуйста отчет по прогрессам.", reply_markup=user_replybtns)
    await state.clear()


async def admin_notify(message: Message, state: FSMContext, bot: Bot, chat_id):#---------------------------------------------------------------------------------------tut formirovat excel otchet
    await bot.send_message(chat_id, "Отчет ",reply_markup=user_replybtns)
    await state.clear()


async def redday_notify(message: Message, state: FSMContext, bot: Bot, chat_id, red_time):
    await bot.send_message(chat_id, f"Сегодня дедлайн нужно сдать отчет до {red_time}",reply_markup=user_replybtns)
    await state.clear()


def time_corrector(time_str):
    from datetime import datetime, timedelta
    # Исходная строка
    #time_str = "11:30"
    # Преобразуем строку в объект времени
    time_obj = datetime.strptime(time_str, "%H:%M")
    # Вычтем два часа
    new_time = time_obj - timedelta(hours=2)
    # Печатаем результат
    new_time_str = new_time.strftime("%H:%M")  # Вывод: 09:30
    new_time_arr = new_time_str.split(":")
    if '0' in new_time_arr[0][0]:
        new_time_arr[0] = new_time_arr[0].replace('0', '')
    return new_time_arr


#print(time_corrector("11:30"))



# period_arr_str = 'Понедельник-Воскресенье'.split('-')
# period_str_int = f"{days_of_week.index(period_arr_str[0])}-{days_of_week.index(period_arr_str[1])}"  
# print(period_str_int)

# if __name__ == '__main__':
#     scheduler.start()
#     executor.start_polling(
#         dispatcher=bot_dispatcher,
#         skip_updates=True,
#         on_startup=on_strtp
#    )
