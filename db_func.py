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






