import asyncio
from aiogram import Bot, Dispatcher
# from config_handler import settings
from dotenv import load_dotenv
import os
import my_routers.questions
from schedules import schedule_jobs, scheduler

load_dotenv()  # Загрузка переменных из файла .env


bot_key = os.getenv('BOT_TOKEN')
# password = os.getenv('PASSWORD')



# from aiogram import BaseMiddleware

# #нужно установить пакет apscheduler
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# ## позволяет доставать scheduler из агрументов фунции
# class SchedulerMiddleware(BaseMiddleware):
#     def __init__(self, scheduler: AsyncIOScheduler):
#         super().__init__()
#         self._scheduler = scheduler

#     async def __call__(self,handler,event,data):
#         # прокидываем в словарь состояния scheduler
#         data["scheduler"] = self._scheduler
#         return await handler(event, data)


# Запуск бота
async def main():
    bot = Bot(token=bot_key)
    dp = Dispatcher()
    dp.include_router(my_routers.questions.router)
    scheduler.start()
    schedule_jobs(bot)
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())