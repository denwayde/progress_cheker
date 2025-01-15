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


# last_checkpoint = select_data("SELECT*FROM user_points WHERE point_name = ? AND telega_id = ? AND date = ? ORDER BY id DESC LIMIT 1", ('qq', 1949640271, '2024-12-22'))[0]

# print(last_checkpoint[3])
# sqldata = select_data_dict("SELECT*FROM userpoints_weekly INNER JOIN usernames ON userpoints_weekly.telega_id = usernames.telega_id WHERE date_date BETWEEN '2023-10-01' AND '2023-10-31'")
# #print(sqldata)
# res = [dict(row) for row in sqldata]
# print(res)

# print()
# print()

dic = [
    {'id': 1, 'point_name': 'qq', 'telega_id': 6293086969, 'point_score': 12, 'date': '2024-12-26', 'name': 'dd', 'hour': None, 'minute': None, 'period': None},
    {'id': 2, 'point_name': 'djf', 'telega_id': 6293086969, 'point_score': 10, 'date': '2024-12-26', 'name': 'dd', 'hour': None, 'minute': None, 'period': None},
    {'id': 3, 'point_name': 'ввв', 'telega_id': 6293086969, 'point_score': 23, 'date': '2024-12-26', 'name': 'dd', 'hour': None, 'minute': None, 'period': None}, {'id': 4, 'point_name': 'ффф', 'telega_id': 6293086969, 'point_score': 23, 'date': '2024-12-26', 'name': 'dd', 'hour': None, 'minute': None, 'period': None}, {'id': 5, 'point_name': 'qq', 'telega_id': 1949640271, 'point_score': 11, 'date': '2024-12-26', 'name': 'Admin', 'hour': None, 'minute': None, 'period': None}, {'id': 6, 'point_name': 'djf', 'telega_id': 1949640271, 'point_score': 34, 'date': '2024-12-26', 'name': 'Admin', 'hour': None, 'minute': None, 'period': None}, {'id': 7, 'point_name': 'ввв', 'telega_id': 1949640271, 'point_score': 45, 'date': '2024-12-26', 'name': 'Admin', 'hour': None, 'minute': None, 'period': None}, {'id': 8, 'point_name': 'ффф', 'telega_id': 1949640271, 'point_score': 56, 'date': '2024-12-26', 'name': 'Admin', 'hour': None, 'minute': None, 'period': None}, {'id': 9, 'point_name': 'qq', 'telega_id': 1949640271, 'point_score': 12, 'date': '2024-12-26', 'name': 'Admin', 'hour': None, 'minute': None, 'period': None}, {'id': 10, 'point_name': 'qq', 'telega_id': 6293086969, 'point_score': 33, 'date': '2024-12-26', 'name': 'dd', 'hour': None, 'minute': None, 'period': None}, {'id': 11, 'point_name': 'djf', 'telega_id': 6293086969, 'point_score': 11, 'date': '2024-12-26', 'name': 'dd', 'hour': None, 'minute': None, 'period': None}
    ]

points = select_data_single("SELECT name FROM points")#[('kkk',), ('джф',), ('kit',), ('hggg',)]
usernames = select_data_single("SELECT name FROM usernames ORDER BY name")
result = []



from datetime import datetime, timedelta

# Получаем сегодняшнюю дату
today = datetime.now()

# Находим номер сегодняшнего дня недели (0 - понедельник, 6 - воскресенье)
today_weekday = today.weekday()

# Вычисляем дату понедельника текущей недели
monday = today - timedelta(days=today_weekday)

# Вычисляем дату воскресенья текущей недели
sunday = monday + timedelta(days=6)

# sqldata = select_data_dict(f"SELECT*FROM userpoints_weekly INNER JOIN usernames ON userpoints_weekly.telega_id = usernames.telega_id WHERE date_date BETWEEN {monday.date()} AND {sunday.date()}")


# Форматируем вывод в нужном виде
# print("Понедельник текущей недели:", monday.date())
# print("Воскресенье текущей недели:", sunday.date())
    




    

