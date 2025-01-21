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


#from datetime import datetime, timedelta

# today = datetime.now()
# # Находим номер сегодняшнего дня недели (0 - понедельник, 6 - воскресенье)
# today_weekday = today.weekday()
# # Вычисляем дату понедельника текущей недели
# monday = today - timedelta(days=today_weekday)
# # Вычисляем дату воскресенья текущей недели
# sunday = monday + timedelta(days=6)
# sqldata = select_data_dict("SELECT * FROM userpoints_weekly INNER JOIN usernames ON userpoints_weekly.telega_id = usernames.telega_id INNER JOIN points ON points.name = userpoints_weekly.point_name WHERE date BETWEEN ? AND ?", (monday.date(), sunday.date(), ))
# dic = [dict(row) for row in sqldata]
# print(dic)

from datetime import datetime, timedelta

# Получаем текущую дату
today = datetime.now()

# Находим первый день недели (понедельник)
monday = today - timedelta(days=today.weekday())
sunday = monday + timedelta(days=6)
# Создаем массив дат этой недели
week_dates = [monday + timedelta(days=i) for i in range(7)]

# Преобразуем даты в строки для удобного отображения (опционально)

sqldata = select_data_dict("SELECT * FROM userpoints_weekly INNER JOIN usernames ON userpoints_weekly.telega_id = usernames.telega_id INNER JOIN points ON points.name = userpoints_weekly.point_name WHERE date BETWEEN ? AND ?", (monday.date(), sunday.date(), ))

sqldata1 = select_data_dict("SELECT usernames.name, userpoints_weekly.point_name, COUNT(DISTINCT userpoints_weekly.date) AS date_count, SUM(userpoints_weekly.point_score) AS total_point_score FROM userpoints_weekly INNER JOIN usernames ON userpoints_weekly.telega_id = usernames.telega_id INNER JOIN points ON points.name = userpoints_weekly.point_name WHERE date BETWEEN ? AND ? GROUP BY usernames.name,  userpoints_weekly.point_name", (monday.date(), sunday.date(), ))

data1 = [
    {'name': 'Admin', 'point_name': 'djf', 'date_count': 1, 'total_point_score': 11}, 
    {'name': 'Admin', 'point_name': 'qq', 'date_count': 2, 'total_point_score': 44}, 
    {'name': 'dd', 'point_name': 'djf', 'date_count': 1, 'total_point_score': 11}, 
    {'name': 'dd', 'point_name': 'ффф', 'date_count': 1, 'total_point_score': 11}
    ]


# dic = [dict(row) for row in sqldata1]
# print(dic)


week_dates_str = [date.strftime('%Y-%m-%d') for date in week_dates]
points = select_data_single("SELECT name FROM points")
usernames = select_data_single("SELECT name FROM usernames ORDER BY name")




pred_result = []

data = [
    {'id': 12, 'point_name': 'qq', 'telega_id': 6293086969, 'point_score': 11, 'date': '2025-01-20', 'name': 'dd', 'hour': None, 'minute': None, 'period': None, 'ratio': 1, 'mins': 10},
    {'id': 16, 'point_name': 'qq', 'telega_id': 6293086969, 'point_score': 12, 'date': '2025-01-20', 'name': 'dd', 'hour': None, 'minute': None, 'period': None, 'ratio': 1, 'mins': 10}, 
    {'id': 13, 'point_name': 'djf', 'telega_id': 6293086969, 'point_score': 21, 'date': '2025-01-20', 'name': 'dd', 'hour': None, 'minute': None, 'period': None, 'ratio': 2, 'mins': 30}, 
    {'id': 14, 'point_name': 'qq', 'telega_id': 1949640271, 'point_score': 10, 'date': '2025-01-20', 'name': 'Admin', 'hour': None, 'minute': None, 'period': None, 'ratio': 1, 'mins': 10},
    {'id': 15, 'point_name': 'djf', 'telega_id': 1949640271, 'point_score': 20, 'date': '2025-01-20', 'name': 'Admin', 'hour': None, 'minute': None, 'period': None, 'ratio': 2, 'mins': 30}
    ]

for name in usernames:
    # print(name)
    dd = {name: ''}
    
    for week_day in week_dates_str:
        dp = {}
        for point in points:
            dp[point] = 0
        for data_element in data:
            # print(f"{week_day} == {data_element['date']} and {name} == {data_element['name']}")
            # print(week_day == data_element['date'])
            if name == data_element['name'] and week_day == data_element['date']:
                dp[data_element['point_name']] += data_element['point_score']
            #     print(dp)
            # print()
        dd[week_day] = dp 
        # print(dd)   
    pred_result.append(dd)

#print(pred_result)

prrrr = [
    {
        'name': 'Admin', 
     '2025-01-20': {'qq': 10, 'djf': 20, 'ввв': 0, 'ффф': 0}, 
     '2025-01-21': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
     '2025-01-22': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
     '2025-01-23': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
     '2025-01-24': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
     '2025-01-25': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
     '2025-01-26': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}
     }, 
    {
        'name': 'dd', 
     '2025-01-20': {'qq': 23, 'djf': 21, 'ввв': 0, 'ффф': 0}, 
     '2025-01-21': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
     '2025-01-22': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
     '2025-01-23': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
     '2025-01-24': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
     '2025-01-25': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
     '2025-01-26': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}
     }
    ]

result = []
for c in prrrr:
    result.append([*c.keys()])

print(result)

    

