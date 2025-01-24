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



# result = [
#         ['Admin', '2025-01-20', '2025-01-21', '2025-01-22', '2025-01-23', '2025-01-24', '2025-01-25', '2025-01-26', 'Сумма', 'Сумма с коэффициентом', 'Сумма с бонусом'], 
#         ['qq', 22, 22, 11, 11, 11, 11, 22, 110, 330, 350], 
#         ['djf', 0, 11, 0, 0, 0, 0, 0, 11, 22, None], 
#         ['ввв', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
#         ['ффф', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
#         [], [], 
#         ['dd', '2025-01-20', '2025-01-21', '2025-01-22', '2025-01-23', '2025-01-24', '2025-01-25', '2025-01-26', 'Сумма', 'Сумма с коэффициентом', 'Сумма с бонусом'], 
#         ['qq', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
#         ['djf', 0, 11, 0, 0, 0, 0, 0, 11, 22, None], 
#         ['ввв', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
#         ['ффф', 0, 11, 0, 0, 0, 0, 0, 11, 22, None], 
#         [], []
#     ]

# pred_result1 = [
#         {
#             'username': 'Admin', 
#             'qq': {'2025-01-20': 22, '2025-01-21': 22, '2025-01-22': 11, '2025-01-23': 11, '2025-01-24': 11, '2025-01-25': 11, '2025-01-26': 22, 'Сумма': 110, 'Сумма с коэффициентом': 330, 'Сумма с бонусом': 350}, 
#             'djf': {'2025-01-20': 0, '2025-01-21': 11, '2025-01-22': 0, '2025-01-23': 0, '2025-01-24': 0, '2025-01-25': 0, '2025-01-26': 0, 'Сумма': 11, 'Сумма с коэффициентом': 22, 'Сумма с бонусом': None}, 
#             'ввв': {'2025-01-20': 0, '2025-01-21': 0, '2025-01-22': 0, '2025-01-23': 0, '2025-01-24': 0, '2025-01-25': 0, '2025-01-26': 0, 'Сумма': 0, 'Сумма с коэффициентом': 0, 'Сумма с бонусом': 0}, 
#             'ффф': {'2025-01-20': 0, '2025-01-21': 0, '2025-01-22': 0, '2025-01-23': 0, '2025-01-24': 0, '2025-01-25': 0, '2025-01-26': 0, 'Сумма': 0, 'Сумма с коэффициентом': 0, 'Сумма с бонусом': 0}
#         }, 
#         {
#             'username': 'dd', 
#             'qq': {'2025-01-20': 0, '2025-01-21': 0, '2025-01-22': 0, '2025-01-23': 0, '2025-01-24': 0, '2025-01-25': 0, '2025-01-26': 0, 'Сумма': 0, 'Сумма с коэффициентом': 0, 'Сумма с бонусом': 0}, 
#             'djf': {'2025-01-20': 0, '2025-01-21': 11, '2025-01-22': 0, '2025-01-23': 0, '2025-01-24': 0, '2025-01-25': 0, '2025-01-26': 0, 'Сумма': 11, 'Сумма с коэффициентом': 22, 'Сумма с бонусом': None}, 
#             'ввв': {'2025-01-20': 0, '2025-01-21': 0, '2025-01-22': 0, '2025-01-23': 0, '2025-01-24': 0, '2025-01-25': 0, '2025-01-26': 0, 'Сумма': 0, 'Сумма с коэффициентом': 0, 'Сумма с бонусом': 0}, 
#             'ффф': {'2025-01-20': 0, '2025-01-21': 11, '2025-01-22': 0, '2025-01-23': 0, '2025-01-24': 0, '2025-01-25': 0, '2025-01-26': 0, 'Сумма': 11, 'Сумма с коэффициентом': 22, 'Сумма с бонусом': None}
#         }
# ]

# expected_result = [
#     ['dd', '20.01','21.01','22.01', 'summa', 'summa s koeff', 'summa s bonusom'],
#     ['kit', 20, 21, 22, 63, 43, 73],
#     ['qq', 12, 13, 14, 63, 43, 73],
#     ['djf', 20, 22, 24, 63, 43, 73]
# ]




# data = [
#     {'id': 12, 'point_name': 'qq', 'telega_id': 6293086969, 'point_score': 11, 'date': '2025-01-20', 'name': 'dd', 'hour': None, 'minute': None, 'period': None, 'ratio': 1, 'mins': 10},
#     {'id': 16, 'point_name': 'qq', 'telega_id': 6293086969, 'point_score': 12, 'date': '2025-01-20', 'name': 'dd', 'hour': None, 'minute': None, 'period': None, 'ratio': 1, 'mins': 10}, 
#     {'id': 13, 'point_name': 'djf', 'telega_id': 6293086969, 'point_score': 21, 'date': '2025-01-20', 'name': 'dd', 'hour': None, 'minute': None, 'period': None, 'ratio': 2, 'mins': 30}, 
#     {'id': 14, 'point_name': 'qq', 'telega_id': 1949640271, 'point_score': 10, 'date': '2025-01-20', 'name': 'Admin', 'hour': None, 'minute': None, 'period': None, 'ratio': 1, 'mins': 10},
#     {'id': 15, 'point_name': 'djf', 'telega_id': 1949640271, 'point_score': 20, 'date': '2025-01-20', 'name': 'Admin', 'hour': None, 'minute': None, 'period': None, 'ratio': 2, 'mins': 30}
#     ]

# for name in usernames:
#     # print(name)
#     dd = {name: ''}
    
#     for week_day in week_dates_str:
#         dp = {}
#         for point in points:
#             dp[point] = 0
#         for data_element in data:
#             # print(f"{week_day} == {data_element['date']} and {name} == {data_element['name']}")
#             # print(week_day == data_element['date'])
#             if name == data_element['name'] and week_day == data_element['date']:
#                 dp[data_element['point_name']] += data_element['point_score']
#             #     print(dp)
#             # print()
#         dd[week_day] = dp 
#         # print(dd)   
#     pred_result.append(dd)

# #print(pred_result)

# prrrr = [
#     {
#         'name': 'Admin', 
#      '2025-01-20': {'qq': 10, 'djf': 20, 'ввв': 0, 'ффф': 0}, 
#      '2025-01-21': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
#      '2025-01-22': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
#      '2025-01-23': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
#      '2025-01-24': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
#      '2025-01-25': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
#      '2025-01-26': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}
#      }, 
#     {
#         'name': 'dd', 
#      '2025-01-20': {'qq': 23, 'djf': 21, 'ввв': 0, 'ффф': 0}, 
#      '2025-01-21': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
#      '2025-01-22': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
#      '2025-01-23': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
#      '2025-01-24': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
#      '2025-01-25': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, 
#      '2025-01-26': {'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}
#      }
#     ]

# result = []
# for my_element in pred_result:
#     result.append([*my_element.keys()])
#     for week_day in week_dates_str:
#         aq = []
#         point_name = ''
#         for point in points:
#             aq = [point, ]
#             aq.append(my_element[week_day][point])
#         result.append(aq)

# print(result)

