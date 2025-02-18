from datetime import datetime, timedelta
from  db_func import select_data_single, select_data_dict
# Получаем сегодняшнюю дату
today = datetime.now()
# Находим номер сегодняшнего дня недели (0 - понедельник, 6 - воскресенье)
today_weekday = today.weekday()
# Вычисляем дату понедельника текущей недели
monday = today - timedelta(days=today_weekday)
# Вычисляем дату воскресенья текущей недели
sunday = monday + timedelta(days=6)
just_points = select_data_single("SELECT point_name FROM points")
just_usenames = select_data_single("SELECT name FROM usernames ORDER BY name")
sqldata1 = select_data_dict("""
SELECT 
u.name,
uw.telega_id, 
p.point_name,
(SELECT SUM(point_score) FROM userpoints_weekly WHERE telega_id = uw.telega_id AND point_name = uw.point_name GROUP BY point_name, telega_id)  AS totalsum_point_score,
SUM(uw.point_score) as point_week_sum,
p.ratio, 
p.mins,
(SELECT bonus_ratio FROM bonus WHERE bonus_name = 'Бонус минимумов') as bonus_of_mins,                      
(SELECT CAST(SUM(bonusmins_elment) AS FLOAT) / (SELECT COUNT(point_name) FROM points) FROM (SELECT userpoints_weekly.telega_id, userpoints_weekly.point_name, COUNT(points.point_name) AS point_count, CASE WHEN SUM(userpoints_weekly.point_score) / points.mins > 1 THEN 1 ELSE 0 END AS bonusmins_elment FROM userpoints_weekly LEFT JOIN points ON userpoints_weekly.point_name = points.point_name WHERE date BETWEEN ? AND ? GROUP BY userpoints_weekly.point_name, userpoints_weekly.telega_id) as bonus_of_mins_table WHERE bonus_of_mins_table.telega_id = uw.telega_id GROUP BY telega_id) AS bonus_of_mins_ratio,                                              
(SELECT SUM(CASE WHEN count_date=7 THEN 1 ELSE 0 END) FROM (SELECT telega_id, COUNT(DISTINCT date) AS count_date FROM userpoints_weekly WHERE telega_id = uw.telega_id AND date BETWEEN ? AND ? GROUP BY point_name) AS date_sum GROUP BY telega_id) AS count_row_bonus,                       
(SELECT bonus_ratio FROM bonus WHERE bonus_name = 'Бонус строки') as bonus_of_rows,
(SELECT SUM(column_bonus) AS total_bonus FROM (SELECT usrw.telega_id, usrw.date, CASE WHEN (SELECT COUNT(DISTINCT point_name) FROM userpoints_weekly WHERE telega_id = usrw.telega_id AND date = usrw.date) = (SELECT COUNT(point_name) FROM points) THEN 1 ELSE 0 END AS column_bonus FROM userpoints_weekly usrw WHERE date BETWEEN ? AND ? GROUP BY usrw.date, usrw.telega_id) AS bonuses WHERE telega_id = uw.telega_id GROUP BY telega_id) AS count_column_bonus,
(SELECT bonus_ratio FROM bonus WHERE bonus_name = 'Бонус столбца') as bonus_of_cols,
(SELECT SUM(point_score*ratio) FROM userpoints_weekly LEFT JOIN points ON points.point_name = userpoints_weekly.point_name WHERE userpoints_weekly.telega_id = uw.telega_id GROUP BY telega_id) AS total_total_ratiosum,
(SELECT SUM(point_score*ratio) FROM userpoints_weekly LEFT JOIN points ON points.point_name = userpoints_weekly.point_name WHERE userpoints_weekly.telega_id = uw.telega_id AND date BETWEEN ? AND ? GROUP BY telega_id) AS weekly_total_ratiosum,
(SELECT SUM(userbonus_score) FROM user_bonus WHERE telega_id = uw.telega_id GROUP BY telega_id) AS last_bonuses_sum                                           
FROM userpoints_weekly uw 
LEFT JOIN usernames u ON uw.telega_id = u.telega_id 
LEFT JOIN points p ON p.point_name = uw.point_name 
WHERE date BETWEEN ? AND ?
GROUP BY u.name, p.point_name
ORDER BY weekly_total_ratiosum DESC
""", (monday.date(), sunday.date(), monday.date(), sunday.date(), monday.date(), sunday.date(), monday.date(), sunday.date(), monday.date(), sunday.date(),))

def bonus_ratio_editor(bonus, my_num):
    if bonus<1 and bonus>0:
        my_num = my_num*bonus
    elif bonus>1:
        my_num = bonus
    elif bonus==1 or bonus==0:
        my_num=0
    return my_num

def bonus_data_process():
    bonus_data = select_data_dict("""
    SELECT 
    u.name,
    uw.telega_id, 
    p.ratio, 
    p.mins,
    (SELECT bonus_ratio FROM bonus WHERE bonus_name = 'Бонус минимумов') as bonus_of_mins,                      
    (SELECT CAST(SUM(bonusmins_elment) AS FLOAT) / (SELECT COUNT(point_name) FROM points) FROM (SELECT userpoints_weekly.telega_id, userpoints_weekly.point_name, COUNT(points.point_name) AS point_count, CASE WHEN SUM(userpoints_weekly.point_score) / points.mins > 1 THEN 1 ELSE 0 END AS bonusmins_elment FROM userpoints_weekly LEFT JOIN points ON userpoints_weekly.point_name = points.point_name WHERE date BETWEEN ? AND ? GROUP BY userpoints_weekly.point_name, userpoints_weekly.telega_id) as bonus_of_mins_table WHERE bonus_of_mins_table.telega_id = uw.telega_id GROUP BY telega_id) AS bonus_of_mins_ratio,                                              
    (SELECT SUM(CASE WHEN count_date=7 THEN 1 ELSE 0 END) FROM (SELECT telega_id, COUNT(DISTINCT date) AS count_date FROM userpoints_weekly WHERE telega_id = uw.telega_id AND date BETWEEN ? AND ? GROUP BY point_name) AS date_sum GROUP BY telega_id) AS count_row_bonus,                       
    (SELECT bonus_ratio FROM bonus WHERE bonus_name = 'Бонус строки') as bonus_of_rows,
    (SELECT SUM(column_bonus) AS total_bonus FROM (SELECT usrw.telega_id, usrw.date, CASE WHEN (SELECT COUNT(DISTINCT point_name) FROM userpoints_weekly WHERE telega_id = usrw.telega_id AND date = usrw.date) = (SELECT COUNT(point_name) FROM points) THEN 1 ELSE 0 END AS column_bonus FROM userpoints_weekly usrw WHERE date BETWEEN ? AND ? GROUP BY usrw.date, usrw.telega_id) AS bonuses WHERE telega_id = uw.telega_id GROUP BY telega_id) AS count_column_bonus,
    (SELECT bonus_ratio FROM bonus WHERE bonus_name = 'Бонус столбца') as bonus_of_cols,
    (SELECT SUM(point_score*ratio) FROM userpoints_weekly LEFT JOIN points ON points.point_name = userpoints_weekly.point_name WHERE userpoints_weekly.telega_id = uw.telega_id GROUP BY telega_id) AS total_total_ratiosum,
    (SELECT SUM(point_score*ratio) FROM userpoints_weekly LEFT JOIN points ON points.point_name = userpoints_weekly.point_name WHERE userpoints_weekly.telega_id = uw.telega_id AND date BETWEEN ? AND ? GROUP BY telega_id) AS weekly_total_ratiosum,
    (SELECT SUM(userbonus_score) FROM user_bonus WHERE telega_id = uw.telega_id GROUP BY telega_id) AS last_bonuses_sum                                           
    FROM userpoints_weekly uw 
    LEFT JOIN usernames u ON uw.telega_id = u.telega_id 
    LEFT JOIN points p ON p.point_name = uw.point_name 
    WHERE date BETWEEN ? AND ?
    GROUP BY u.name
    ORDER BY weekly_total_ratiosum DESC
    """, (monday.date(), sunday.date(), monday.date(), sunday.date(), monday.date(), sunday.date(), monday.date(), sunday.date(), monday.date(), sunday.date(),))
    return bonus_data

def ttl_ratiosum_process():
    total_ratiosum_data = select_data_dict("""
    SELECT 
    u.name,
    uw.telega_id, 
    p.ratio, 
    p.mins,
    (SELECT bonus_ratio FROM bonus WHERE bonus_name = 'Бонус минимумов') as bonus_of_mins,                      
    (SELECT CAST(SUM(bonusmins_elment) AS FLOAT) / (SELECT COUNT(point_name) FROM points) FROM (SELECT userpoints_weekly.telega_id, userpoints_weekly.point_name, COUNT(points.point_name) AS point_count, CASE WHEN SUM(userpoints_weekly.point_score) / points.mins > 1 THEN 1 ELSE 0 END AS bonusmins_elment FROM userpoints_weekly LEFT JOIN points ON userpoints_weekly.point_name = points.point_name WHERE date BETWEEN ? AND ? GROUP BY userpoints_weekly.point_name, userpoints_weekly.telega_id) as bonus_of_mins_table WHERE bonus_of_mins_table.telega_id = uw.telega_id GROUP BY telega_id) AS bonus_of_mins_ratio,                                              
    (SELECT SUM(CASE WHEN count_date=7 THEN 1 ELSE 0 END) FROM (SELECT telega_id, COUNT(DISTINCT date) AS count_date FROM userpoints_weekly WHERE telega_id = uw.telega_id AND date BETWEEN ? AND ? GROUP BY point_name) AS date_sum GROUP BY telega_id) AS count_row_bonus,                       
    (SELECT bonus_ratio FROM bonus WHERE bonus_name = 'Бонус строки') as bonus_of_rows,
    (SELECT SUM(column_bonus) AS total_bonus FROM (SELECT usrw.telega_id, usrw.date, CASE WHEN (SELECT COUNT(DISTINCT point_name) FROM userpoints_weekly WHERE telega_id = usrw.telega_id AND date = usrw.date) = (SELECT COUNT(point_name) FROM points) THEN 1 ELSE 0 END AS column_bonus FROM userpoints_weekly usrw WHERE date BETWEEN ? AND ? GROUP BY usrw.date, usrw.telega_id) AS bonuses WHERE telega_id = uw.telega_id GROUP BY telega_id) AS count_column_bonus,
    (SELECT bonus_ratio FROM bonus WHERE bonus_name = 'Бонус столбца') as bonus_of_cols,
                                                    
    (SELECT SUM(point_score*ratio) FROM userpoints_weekly LEFT JOIN points ON points.point_name = userpoints_weekly.point_name WHERE userpoints_weekly.telega_id = uw.telega_id AND date BETWEEN ? AND ? GROUP BY telega_id) AS weekly_total_ratiosum,
                            
    COALESCE((SELECT SUM(userbonus_score) FROM user_bonus WHERE telega_id = uw.telega_id GROUP BY telega_id), 0) + COALESCE((SELECT SUM(userpoints_weekly.point_score * points.ratio) FROM userpoints_weekly LEFT JOIN points ON points.point_name = userpoints_weekly.point_name WHERE userpoints_weekly.telega_id = uw.telega_id GROUP BY telega_id), 0) AS total_ratiosun_with_bonuses                                         
    FROM userpoints_weekly uw 
    LEFT JOIN usernames u ON uw.telega_id = u.telega_id 
    LEFT JOIN points p ON p.point_name = uw.point_name 
    WHERE date BETWEEN ? AND ?
    GROUP BY u.name
    ORDER BY total_ratiosun_with_bonuses DESC
    """, (monday.date(), sunday.date(), monday.date(), sunday.date(), monday.date(), sunday.date(), monday.date(), sunday.date(), monday.date(), sunday.date(),))
    return total_ratiosum_data

# ddd = select_data_dict("SELECT SUM(userpoints_weekly.point_score*points.ratio) FROM userpoints_weekly LEFT JOIN points ON points.point_name = userpoints_weekly.point_name GROUP BY telega_id")
# print([dict(x) for x in ttl_ratiosum_process()])
#(SELECT SUM(userbonus_score) FROM user_bonus WHERE telega_id = uw.telega_id GROUP BY telega_id) + (SELECT SUM(userpoints_weekly.point_score*points.ratio) FROM userpoints_weekly LEFT JOIN points ON points.point_name = userpoints_weekly.point_name WHERE userpoints_weekly.telega_id = uw.telega_id GROUP BY telega_id) AS total_ratiosun_with_bonuses
bns = [
    {'name': 'Dinamo', 'telega_id': 6293086969, 'ratio': 3, 'mins': 10, 'bonus_of_mins': 30, 'bonus_of_mins_ratio': 0.75, 'count_row_bonus': 2, 'bonus_of_rows': 0.2, 'count_column_bonus': 2, 'bonus_of_cols': 20, 'total_total_ratiosum': 896, 'weekly_total_ratiosum': 531, 'last_bonuses_sum': 248.5}, 
    {'name': 'Admin', 'telega_id': 1949640271, 'ratio': 3, 'mins': 10, 'bonus_of_mins': 30, 'bonus_of_mins_ratio': 0.25, 'count_row_bonus': 1, 'bonus_of_rows': 0.2, 'count_column_bonus': 1, 'bonus_of_cols': 20, 'total_total_ratiosum': 1142, 'weekly_total_ratiosum': 426, 'last_bonuses_sum': 89.7}
    ]

ttl_ratiosum = [
    {'name': 'Admin', 'telega_id': 1949640271, 'ratio': 3, 'mins': 10, 'bonus_of_mins': 30, 'bonus_of_mins_ratio': 0.25, 'count_row_bonus': 1, 'bonus_of_rows': 0.2, 'count_column_bonus': 1, 'bonus_of_cols': 20, 'weekly_total_ratiosum': 426, 'total_ratiosun_with_bonuses': 1231.7}, 
    {'name': 'Dinamo', 'telega_id': 6293086969, 'ratio': 3, 'mins': 10, 'bonus_of_mins': 30, 'bonus_of_mins_ratio': 0.75, 'count_row_bonus': 2, 'bonus_of_rows': 0.2, 'count_column_bonus': 2, 'bonus_of_cols': 20, 'weekly_total_ratiosum': 531, 'total_ratiosun_with_bonuses': 1144.5}
    ]

# print(sqldata1)
sqldt1 = [
    {'name': 'Dinamo', 'telega_id': 6293086969, 'point_name': 'djf', 'totalsum_point_score': 255, 'point_week_sum': 67, 'ratio': 2, 'mins': 30, 'bonus_of_mins': 102, 'bonus_of_mins_ratio': 1.0, 'count_row_bonus': 0, 'bonus_of_rows': 0.2, 'count_column_bonus': 1, 'bonus_of_cols': 0, 'total_total_ratiosum': 1761, 'weekly_total_ratiosum': 679, 'last_bonuses_sum': 248.5}, 
    {'name': 'Dinamo', 'telega_id': 6293086969, 'point_name': 'qq', 'totalsum_point_score': 176, 'point_week_sum': 99, 'ratio': 3, 'mins': 10, 'bonus_of_mins': 102, 'bonus_of_mins_ratio': 1.0, 'count_row_bonus': 0, 'bonus_of_rows': 0.2, 'count_column_bonus': 1, 'bonus_of_cols': 0, 'total_total_ratiosum': 1761, 'weekly_total_ratiosum': 679, 'last_bonuses_sum': 248.5}, 
    {'name': 'Dinamo', 'telega_id': 6293086969, 'point_name': 'ввв', 'totalsum_point_score': 123, 'point_week_sum': 46, 'ratio': 1, 'mins': 20, 'bonus_of_mins': 102, 'bonus_of_mins_ratio': 1.0, 'count_row_bonus': 0, 'bonus_of_rows': 0.2, 'count_column_bonus': 1, 'bonus_of_cols': 0, 'total_total_ratiosum': 1761, 'weekly_total_ratiosum': 679, 'last_bonuses_sum': 248.5}, 
    {'name': 'Dinamo', 'telega_id': 6293086969, 'point_name': 'ффф', 'totalsum_point_score': 300, 'point_week_sum': 101, 'ratio': 2, 'mins': 30, 'bonus_of_mins': 102, 'bonus_of_mins_ratio': 1.0, 'count_row_bonus': 0, 'bonus_of_rows': 0.2, 'count_column_bonus': 1, 'bonus_of_cols': 0, 'total_total_ratiosum': 1761, 'weekly_total_ratiosum': 679, 'last_bonuses_sum': 248.5}, 
    {'name': 'Admin', 'telega_id': 1949640271, 'point_name': 'djf', 'totalsum_point_score': 132, 'point_week_sum': 34, 'ratio': 2, 'mins': 30, 'bonus_of_mins': 102, 'bonus_of_mins_ratio': 0.5, 'count_row_bonus': 0, 'bonus_of_rows': 0.2, 'count_column_bonus': 1, 'bonus_of_cols': 0, 'total_total_ratiosum': 1412, 'weekly_total_ratiosum': 270, 'last_bonuses_sum': 89.7}, 
    {'name': 'Admin', 'telega_id': 1949640271, 'point_name': 'qq', 'totalsum_point_score': 276, 'point_week_sum': 23, 'ratio': 3, 'mins': 10, 'bonus_of_mins': 102, 'bonus_of_mins_ratio': 0.5, 'count_row_bonus': 0, 'bonus_of_rows': 0.2, 'count_column_bonus': 1, 'bonus_of_cols': 0, 'total_total_ratiosum': 1412, 'weekly_total_ratiosum': 270, 'last_bonuses_sum': 89.7}, 
    {'name': 'Admin', 'telega_id': 1949640271, 'point_name': 'ввв', 'totalsum_point_score': 98, 'point_week_sum': 43, 'ratio': 1, 'mins': 20, 'bonus_of_mins': 102, 'bonus_of_mins_ratio': 0.5, 'count_row_bonus': 0, 'bonus_of_rows': 0.2, 'count_column_bonus': 1, 'bonus_of_cols': 0, 'total_total_ratiosum': 1412, 'weekly_total_ratiosum': 270, 'last_bonuses_sum': 89.7}, 
    {'name': 'Admin', 'telega_id': 1949640271, 'point_name': 'ффф', 'totalsum_point_score': 111, 'point_week_sum': 45, 'ratio': 2, 'mins': 30, 'bonus_of_mins': 102, 'bonus_of_mins_ratio': 0.5, 'count_row_bonus': 0, 'bonus_of_rows': 0.2, 'count_column_bonus': 1, 'bonus_of_cols': 0, 'total_total_ratiosum': 1412, 'weekly_total_ratiosum': 270, 'last_bonuses_sum': 89.7}
    ]