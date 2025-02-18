import sqlite3

connection = sqlite3.connect('progress_cheker.db')


def delete_or_insert_data(delete_or_insert_query, tup=()):
    global connection
    cur = connection.cursor()
    cur.execute(delete_or_insert_query, tup)
    connection.commit()
    
    

def select_data(selection_query, tup=()):
    global connection
    cur = connection.cursor()
    cur.execute(selection_query, tup)
    return cur.fetchall()

def select_data_dict(selection_query, tup=()):
    connection = sqlite3.connect('progress_cheker.db')
    with connection:
        connection.row_factory = sqlite3.Row
        curs = connection.cursor()
        curs.execute(selection_query, tup)
        rows = curs.fetchall()
        return rows
        # for row in rows:
        #     print(f"{row['companyid']}, {row['name']}, {row['address']}.")
    # cur = connection.cursor()
    # cur.execute(selection_query, tup)
    # return cur.fetchall()

def select_data_single(selection_query, tup=()):
    connection = sqlite3.connect('progress_cheker.db')
    with connection:
        connection.row_factory = lambda curs, row: row[0]
        curs = connection.cursor()
        curs.execute(selection_query, tup)
        rows = curs.fetchall()
        return rows


def insert_many(insertion_query, lst):
    global connection
    cur = connection.cursor()
    cur.executemany(insertion_query, lst)
    connection.commit()





# from datetime import datetime, timedelta

# today = datetime.now()
# # Находим номер сегодняшнего дня недели (0 - понедельник, 6 - воскресенье)
# today_weekday = today.weekday()
# # Вычисляем дату понедельника текущей недели
# monday = today - timedelta(days=today_weekday)
# # Вычисляем дату воскресенья текущей недели
# sunday = monday + timedelta(days=6)
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# scheduler = AsyncIOScheduler(timezone = "Asia/Yekaterinburg")

from apscheduler.schedulers.background import BackgroundScheduler

# Создайте экземпляр планировщика
scheduler = BackgroundScheduler()
from datetime import datetime
import time
# Определите время выполнения задачи
scheduled_time = datetime.now().replace(day=18, month=2, year=2025, hour=int(16), minute=int(20))

def admin_excel_notify():
    print('hello')
# Если scheduled_time уже прошлое, добавьте день
if scheduled_time < datetime.now():
    # Добавляем один день
    scheduled_time = scheduled_time.replace(day=scheduled_time.day + 1)

# Запланируйте задачу один раз на определенное время
scheduler.add_job(admin_excel_notify, 'date', run_date=scheduled_time)

scheduler.start()

# try:
#     # Поддерживаем основной поток активным
#     while True:
#         time.sleep(1)
# except (KeyboardInterrupt, SystemExit):
#     # Останавливаем планировщик при выходе
#     scheduler.shutdown()
#print(datetime.now().day)