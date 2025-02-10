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





from datetime import datetime, timedelta

today = datetime.now()
# Находим номер сегодняшнего дня недели (0 - понедельник, 6 - воскресенье)
today_weekday = today.weekday()
# Вычисляем дату понедельника текущей недели
monday = today - timedelta(days=today_weekday)
# Вычисляем дату воскресенья текущей недели
sunday = monday + timedelta(days=6)
# sqldata = select_data_dict("SELECT * FROM userpoints_weekly INNER JOIN usernames ON userpoints_weekly.telega_id = usernames.telega_id INNER JOIN points ON points.name = userpoints_weekly.point_name WHERE date BETWEEN ? AND ?", (monday.date(), sunday.date(), ))
# dic = [dict(row) for row in sqldata]
# print(dic)
# print()
# print()

# sqldata1 = select_data_dict("")
# dic1 = [dict(row) for row in sqldata1]
# print(dic1)

sqldata = select_data_dict("SELECT uw.telega_id, uw.point_name, (SELECT bonus_ratio FROM bonus WHERE bonus_name = 'Бонус строки') AS bonus_row_ratio, SUM(CASE WHEN (SELECT COUNT(DISTINCT date) FROM userpoints_weekly WHERE date BETWEEN ? AND ? GROUP BY point_name) = 7 THEN 1 ELSE 0 END) AS bonus_score FROM userpoints_weekly uw INNER JOIN usernames ON uw.telega_id = usernames.telega_id INNER JOIN points ON points.point_name = uw.point_name WHERE uw.date BETWEEN ? AND ? GROUP BY uw.telega_id, uw.point_name", (monday.date(), sunday.date(), monday.date(), sunday.date(),))

# dic1 = [dict(row) for row in sqldata]
# print(dic1)
# dt = select_data("SELECT telega_id, point_name, COUNT(DISTINCT date) FROM userpoints_weekly WHERE date BETWEEN ? AND ? GROUP BY point_name HAVING COUNT(DISTINCT date) = 7", (monday.date(), sunday.date(),))
# print(dt)


# data1 = select_data_dict("""
# SELECT
#     u.name,
#     uw.point_name,
#     bonus_row.point_bonus_row,
#     bonus_row.date_count,
#     SUM(uw.point_score) AS sum_point,
#     (SELECT SUM(point_score) FROM userpoints_weekly WHERE telega_id = u.telega_id AND date BETWEEN ? AND ? GROUP BY point_name) AS total_sum,
#     CASE
#         WHEN (SELECT COUNT(DISTINCT point_name) FROM userpoints_weekly WHERE telega_id = u.telega_id AND date BETWEEN ? AND ?) = (SELECT COUNT(DISTINCT point_name) FROM points)
#         THEN (SELECT bonus_ratio FROM bonus WHERE bonus_name = 'Бонус столбца')
#         ELSE 0
#     END AS bonus_column,
#     SUM(CASE
#         WHEN (SELECT COUNT(DISTINCT point_name) FROM userpoints_weekly WHERE telega_id = u.telega_id AND date BETWEEN ? AND ?) = (SELECT COUNT(DISTINCT point_name) FROM points)
#         THEN 1
#         ELSE 0
#     END) AS bonus_column_count
# FROM
#     userpoints_weekly uw
# LEFT JOIN
#     usernames u ON u.telega_id = uw.telega_id
# LEFT JOIN
#     (SELECT telega_id, point_name AS point_bonus_row, COUNT(DISTINCT date) AS date_count FROM userpoints_weekly WHERE date BETWEEN ? AND ? GROUP BY date) AS bonus_row ON bonus_row.telega_id = uw.telega_id
# WHERE 
#     uw.date BETWEEN ? AND ?
# GROUP BY
#     u.name, uw.point_name
# """, (monday.date(), sunday.date(), monday.date(), sunday.date(), monday.date(), sunday.date(), monday.date(), sunday.date(), monday.date(), sunday.date(),))

# dic1 = [dict(row) for row in data1]
# print(dic1)
# sqldata1 = select_data("SELECT SUM(point_score) FROM userpoints_weekly WHERE telega_id = 6293086969 AND point_name = 'djf' AND date BETWEEN ? AND ?", (monday.date(), sunday.date(),))
# print(sqldata1)

data = select_data_dict("""
SELECT 
u.name, 
p.point_name,
(SELECT SUM(point_score) FROM userpoints_weekly WHERE telega_id = uw.telega_id AND point_name = uw.point_name GROUP BY point_name, telega_id)  AS totalsum_point_score,
SUM(uw.point_score) as point_week_sum,
p.ratio, 
p.mins,
(SELECT bonus_ratio FROM bonus WHERE bonus_name = 'Бонус минимумов') as bonus_of_mins,                       
(SELECT SUM(CASE WHEN count_date=7 THEN 1 ELSE 0 END) FROM (SELECT telega_id, COUNT(DISTINCT date) AS count_date FROM userpoints_weekly WHERE telega_id = uw.telega_id AND date BETWEEN ? AND ? GROUP BY point_name) AS date_sum GROUP BY telega_id) AS count_row_bonus,                       
(SELECT bonus_ratio FROM bonus WHERE bonus_name = 'Бонус строки') as bonus_of_rows,
(SELECT SUM(column_bonus) AS total_bonus FROM (SELECT usrw.telega_id, usrw.date, CASE WHEN (SELECT COUNT(DISTINCT point_name) FROM userpoints_weekly WHERE telega_id = usrw.telega_id AND date = usrw.date) = (SELECT COUNT(point_name) FROM points) THEN 1 ELSE 0 END AS column_bonus FROM userpoints_weekly usrw WHERE date BETWEEN ? AND ? GROUP BY usrw.date, usrw.telega_id) AS bonuses WHERE telega_id = uw.telega_id GROUP BY telega_id) AS count_column_bonus,
(SELECT bonus_ratio FROM bonus WHERE bonus_name = 'Бонус столбца') as bonus_of_cols,
(SELECT SUM(point_score*ratio) FROM userpoints_weekly LEFT JOIN points ON points.point_name = userpoints_weekly.point_name WHERE userpoints_weekly.telega_id = uw.telega_id GROUP BY telega_id) AS total_total_ratiosum,
(SELECT SUM(point_score*ratio) FROM userpoints_weekly LEFT JOIN points ON points.point_name = userpoints_weekly.point_name WHERE userpoints_weekly.telega_id = uw.telega_id AND date BETWEEN ? AND ? GROUP BY telega_id) AS weekly_total_ratiosum                                           
FROM userpoints_weekly uw 
LEFT JOIN usernames u ON uw.telega_id = u.telega_id 
LEFT JOIN points p ON p.point_name = uw.point_name 
WHERE date BETWEEN ? AND ?
GROUP BY u.name, p.point_name
ORDER BY weekly_total_ratiosum DESC
""", (monday.date(), sunday.date(), monday.date(), sunday.date(), monday.date(), sunday.date(), monday.date(), sunday.date(),))

# just_points = select_data_single("SELECT point_name FROM points")
# just_usenames = select_data_single("SELECT name FROM usernames ORDER BY name")
sorted_data = sorted(data, key=lambda x: x['total_total_ratiosum'], reverse=True)
# dic1 = [dict(row) for row in sorted_data]
# print(dic1)#30




def bonus_ratio_editor(bonus, my_num):
    if bonus<1 and bonus>0:
        my_num = my_num*bonus
    elif bonus>1:
        my_num = bonus
    elif bonus==1 or bonus==0:
        my_num=0
    return my_num

#print(bonus_ratio_editor(20, 100))

otvet = [
    {'name': 'Admin', 'point_name': 'djf', 'totalsum_point_score': 75, 'point_week_sum': 10, 'ratio': 2, 'mins': 30, 'bonus_of_mins': 30, 'count_row_bonus': 1, 'bonus_of_rows': 0.2, 'count_column_bonus': 1, 'bonus_of_cols': 20, 'total_total_ratiosum': 1027, 'weekly_total_ratiosum': 311}, 
    {'name': 'Admin', 'point_name': 'qq', 'totalsum_point_score': 230, 'point_week_sum': 87, 'ratio': 3, 'mins': 10, 'bonus_of_mins': 30, 'count_row_bonus': 1, 'bonus_of_rows': 0.2, 'count_column_bonus': 1, 'bonus_of_cols': 20, 'total_total_ratiosum': 1027, 'weekly_total_ratiosum': 311}, 
    {'name': 'Admin', 'point_name': 'ввв', 'totalsum_point_score': 55, 'point_week_sum': 10, 'ratio': 1, 'mins': 20, 'bonus_of_mins': 30, 'count_row_bonus': 1, 'bonus_of_rows': 0.2, 'count_column_bonus': 1, 'bonus_of_cols': 20, 'total_total_ratiosum': 1027, 'weekly_total_ratiosum': 311}, 
    {'name': 'Admin', 'point_name': 'ффф', 'totalsum_point_score': 66, 'point_week_sum': 10, 'ratio': 2, 'mins': 30, 'bonus_of_mins': 30, 'count_row_bonus': 1, 'bonus_of_rows': 0.2, 'count_column_bonus': 1, 'bonus_of_cols': 20, 'total_total_ratiosum': 1027, 'weekly_total_ratiosum': 311}, 
    {'name': 'Dinamo', 'point_name': 'djf', 'totalsum_point_score': 154, 'point_week_sum': 101, 'ratio': 2, 'mins': 30, 'bonus_of_mins': 30, 'count_row_bonus': 2, 'bonus_of_rows': 0.2, 'count_column_bonus': 2, 'bonus_of_cols': 20, 'total_total_ratiosum': 830, 'weekly_total_ratiosum': 465}, 
    {'name': 'Dinamo', 'point_name': 'qq', 'totalsum_point_score': 77, 'point_week_sum': 21, 'ratio': 3, 'mins': 10, 'bonus_of_mins': 30, 'count_row_bonus': 2, 'bonus_of_rows': 0.2, 'count_column_bonus': 2, 'bonus_of_cols': 20, 'total_total_ratiosum': 830, 'weekly_total_ratiosum': 465}, 
    {'name': 'Dinamo', 'point_name': 'ввв', 'totalsum_point_score': 43, 'point_week_sum': 20, 'ratio': 1, 'mins': 20, 'bonus_of_mins': 30, 'count_row_bonus': 2, 'bonus_of_rows': 0.2, 'count_column_bonus': 2, 'bonus_of_cols': 20, 'total_total_ratiosum': 830, 'weekly_total_ratiosum': 465}, 
    {'name': 'Dinamo', 'point_name': 'ффф', 'totalsum_point_score': 124, 'point_week_sum': 90, 'ratio': 2, 'mins': 30, 'bonus_of_mins': 30, 'count_row_bonus': 2, 'bonus_of_rows': 0.2, 'count_column_bonus': 2, 'bonus_of_cols': 20, 'total_total_ratiosum': 830, 'weekly_total_ratiosum': 465}
] 


ddq = select_data_dict("""
SELECT*FROM userpoints_weekly 
LEFT JOIN points ON userpoints_weekly.point_name = points.point_name 
WHERE date BETWEEN ? AND ?
""", (monday.date(), sunday.date(),))
dic1 = [dict(row) for row in ddq]
print(dic1)#30

ff = [
    {'SUM(uspt.point_score)*pnt.ratio': 150, 'ratio': 2, 'telega_id': 1949640271}, 
    {'SUM(uspt.point_score)*pnt.ratio': 690, 'ratio': 3, 'telega_id': 1949640271}, 
    {'SUM(uspt.point_score)*pnt.ratio': 55, 'ratio': 1, 'telega_id': 1949640271}, 
    {'SUM(uspt.point_score)*pnt.ratio': 132, 'ratio': 2, 'telega_id': 1949640271},

    {'SUM(uspt.point_score)*pnt.ratio': 308, 'ratio': 2, 'telega_id': 6293086969}, 
    {'SUM(uspt.point_score)*pnt.ratio': 231, 'ratio': 3, 'telega_id': 6293086969}, 
    {'SUM(uspt.point_score)*pnt.ratio': 43, 'ratio': 1, 'telega_id': 6293086969}, 
    {'SUM(uspt.point_score)*pnt.ratio': 248, 'ratio': 2, 'telega_id': 6293086969}
    ]
#for x in select_data_single("SELECT ratio FROM points"):
# print(select_data_single("SELECT ratio FROM points"))
# for x in select_data_dict("SELECT ratio, point_name FROM points"):
#     num = 0
#     for z in select_data_dict("SELECT point_name, SUM(point_score) AS sum_points FROM userpoints_weekly GROUP BY telega_id, point_name"):
#         if x['point_name'] == z['point_name']:
#             num+=x['ratio']*z['sum_points']
#     print(num)