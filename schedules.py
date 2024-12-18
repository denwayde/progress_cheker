from aiogram import Bot
from db_func import select_data
from dotenv import load_dotenv
import os
import excel_creator
from aiogram.types import FSInputFile
from btns.admin_replybtn import admin_replybtns

load_dotenv() 
bot_key = os.getenv('BOT_TOKEN')
admin_id = os.getenv("ADMIN_ID")

from apscheduler.schedulers.asyncio import AsyncIOScheduler
scheduler = AsyncIOScheduler(timezone = "Asia/Yekaterinburg")


days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

def schedule_jobs():
    # scheduler.remove_all_jobs()
    #scheduler.add_job(schedule_for_users, 'interval', seconds = 30)
    #scheduler.add_job(hello, 'interval', seconds = 30)
    scheduler.add_job(schedule_for_admins, 'interval', seconds = 30)
    #scheduler.add_job(admin_red_alert, 'interval', seconds = 30)

# async def hello():
#     print("Heelo")

async def schedule_for_admins():
    scheduler.remove_all_jobs()
    admin_data = select_data("SELECT*FROM admin")[0]#[(1, 'admin', 1949640271, '11', '30', 'Среда')]
    user_data = select_data("SELECT telega_id FROM usernames WHERE hour IS NOT NULL AND minute IS NOT NULL")#[(6293086969,), (1949640271,)]
    redtime_str = f"{admin_data[3]}:{admin_data[4]}"
    arr_to_notify = time_corrector(redtime_str)
    
    #scheduler.add_job(admin_notify, 'cron', day_of_week=str(days_of_week.index(admin_data[5])), hour=arr_to_notify[0], minute=arr_to_notify[1], args=(message, state, bot, x[2], redtime_str))
    for x in user_data:
        bot = Bot(token=bot_key)
        minute = zero_cleaner(arr_to_notify[1])
        scheduler.add_job(redday_notify, 'cron', day_of_week=str(days_of_week.index(admin_data[5])), hour=arr_to_notify[0], minute=minute, args=(bot, x[0], redtime_str))
    
    await schedule_for_users()
    await admin_red_alert()
    schedule_jobs()


async def schedule_for_users():
    #scheduler.remove_all_jobs()
    data = select_data("SELECT*FROM usernames")#[(1, 'цска', 6293086969, '16', '00', 'Воскресенье-Воскресенье'), (2, 'динамо', None, None, None, None), (10, 'Admin', 1949640271, '9', '00', 'Понедельник-Воскресенье')]
    #print(data)
    for x in data:
        if x[3] != None and x[2] != None:
            #x[5] - den nedeli ('Воскресенье-Воскресенье')
            try:
                period_arr_str = x[5].split('-')
                period_str_int = f"{days_of_week.index(period_arr_str[0])}-{days_of_week.index(period_arr_str[1])}"
            except IndexError:
                period_str_int = f"{days_of_week.index(x[5])}"      
            bot = Bot(token=bot_key)
            minute = zero_cleaner(x[4])
            scheduler.add_job(noon_print, 'cron', day_of_week=period_str_int, hour=x[3], minute=minute, args=(bot, x[2]))




from btns.users_replybtn import user_replybtns
from btns.admin_replybtn import admin_replybtns 

async def noon_print(bot: Bot, chat_id):    
    await bot.send_message(chat_id, "Отправьте пожалуйста отчет по прогрессам.",reply_markup=user_replybtns())
    #await message.answer("Отправьте пожалуйста отчет по прогрессам.", reply_markup=user_replybtns)
    

async def admin_red_alert():
    #scheduler.remove_all_jobs()
    try:
        red_time =  select_data("SELECT red_hour, red_minute, red_day FROM admin")[0]
        print(red_time)
    except IndexError:
        red_time = ('21', '00', 'Воскресенье')
        print(red_time)
    bot = Bot(token=bot_key)
    minute = zero_cleaner(red_time[1])
    scheduler.add_job(admin_excel_notify, 'cron', day_of_week=days_of_week.index(red_time[2]), hour=int(red_time[0]), minute=int(minute), args=(bot, ))


def zero_cleaner(minute):
    if minute[0] == '0':
        minute = list(minute)
        minute.remove(minute[0])
        minute = minute[0]
    return minute


async def admin_excel_notify(bot: Bot):#------------------------------------------------------------------------------------tut formirovat excel otchet
    excel_creator.exsel_creator()
    import datetime
    day = datetime.datetime.now().strftime("%Y-%m-%d")
    file_path = f'excels/{day}.xlsx'  # Обязательно проверьте, что путь и расширение файла указаны правильно
    if os.path.exists(file_path):
        await bot.send_document(int(admin_id), FSInputFile(file_path), caption=f"Отчет на {day}")
    else:
        await bot.send_message(int(admin_id), "Что-то пошло не так. Попробуйте снова или напишите разработчику: @Dinis_Fizik", reply_markup=admin_replybtns())
    



async def redday_notify(bot: Bot, chat_id, red_time):
    await bot.send_message(chat_id, f"Сегодня дедлайн нужно сдать отчет до {red_time}",reply_markup=user_replybtns())
    


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
