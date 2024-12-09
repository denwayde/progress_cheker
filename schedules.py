
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
    message = Message()
    state = FSMContext()
    bot = Bot()
    #scheduler.add_job(noon_print, 'cron', day_of_week='mon-sat', hour=8, minute=20)
    # scheduler.add_job(noon_print, 'cron', day_of_week='mon-sat', hour=9, minute=15)
    # scheduler.add_job(schedule_for_admins, 'cron', day_of_week='mon-sat', hour=9, minute=30)
    scheduler.add_job(schedule_for_admins, 'interval', seconds = 180, args=(message, state, bot))




async def schedule_for_admins(message: Message, state: FSMContext, bot: Bot):
    data = select_data("SELECT*FROM usernames")
    data_managed = []
    #print(data)
    for x in data:
        if x[3] != None and x[2] != None:
            #x[5]
            data_managed.append(scheduler.add_job(noon_print, 'cron', day_of_week='mon-sat', hour=8, minute=20))
    print(data_managed)

# if __name__ == '__main__':

#     scheduler.start()

#     executor.start_polling(
#         dispatcher=bot_dispatcher,
#         skip_updates=True,
#         on_startup=on_strtp
#     )
