from openpyxl import Workbook
from db_func import select_data, select_data_dict, select_data_single
# import datetime
from datetime import datetime, timedelta
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
# def result_total(just_usenames, just_points, sqldata1):
#     # wb = Workbook()
#     # ws = wb.active
#     #users_points = select_data("SELECT* FROM user_points INNER JOIN points ON points.name = user_points.point_name INNER JOIN usernames ON user_points.telega_id = usernames.telega_id ORDER BY usernames.name")
#     #day = datetime.datetime.now().strftime("%Y-%m-%d")
#     # print(users_points)
#     # just_usenames = [x[0] for x in usernames]
#     # just_points = [x[0] for x in points]
#     # points_release = ["", *just_points, "Сумма", "Сумма c учетом коэффициентов"]
#     # ws.append(points_release)
#     users = []
#     for x in just_usenames:
#         my_dict = {}
#         my_dict["name"] = x
#         for z in just_points:
#             my_dict[z] = ""
#         my_dict["sum"] = 0
#         my_dict["ksum"] = 0
#         my_dict["bonus"] = 0
#         users.append(
#             my_dict
#         )
#     usr_points =[
#         (43, 'qq', 1949640271, 23, '2024-12-26', 10, 'qq', 3, 10, 20, 15, 'Admin', 1949640271, '', '', ''), 
#         (44, 'djf', 1949640271, 34, '2024-12-26', 11, 'djf', 2, 30, 14, 15, 'Admin', 1949640271, '', '', ''), 
#         (45, 'ввв', 1949640271, 45, '2024-12-26', 12, 'ввв', 1, 20, 0, 15, 'Admin', 1949640271, '', '', ''), 
#         (46, 'ффф', 1949640271, 56, '2024-12-26', 13, 'ффф', 2, 30, 0, 15, 'Admin', 1949640271, '', '', ''), 
#         (39, 'ввв', 6293086969, 33, '2024-12-26', 12, 'ввв', 1, 20, 0, 17, 'Dinamo', 6293086969, '', '', ''), 
#         (40, 'qq', 6293086969, 45, '2024-12-26', 10, 'qq', 3, 10, 20, 17, 'Dinamo', 6293086969, '', '', ''), 
#         (41, 'djf', 6293086969, 21, '2024-12-26', 11, 'djf', 2, 30, 14, 17, 'Dinamo', 6293086969, '', '', ''), 
#         (42, 'ффф', 6293086969, 23, '2024-12-26', 13, 'ффф', 2, 30, 0, 17, 'Dinamo', 6293086969, '', '', '')
#         ]
#     sqldata1 = [
#         {'name': 'Admin', 'point_name': 'qq', 'total_point_score': 77, 'total_point_score_with_koef': 231, 'bonus_score': 251}, 
#         {'name': 'Dinamo', 'point_name': 'djf', 'total_point_score': 11, 'total_point_score_with_koef': 22, 'bonus_score': None}, 
#         {'name': 'Dinamo', 'point_name': 'qq', 'total_point_score': 11, 'total_point_score_with_koef': 33, 'bonus_score': None}, 
#         {'name': 'Dinamo', 'point_name': 'ффф', 'total_point_score': 11, 'total_point_score_with_koef': 22, 'bonus_score': None}
#     ]
#     for x in users:
#         for v in users_points:
#             if x['name'] in v:
#                 x[v[1]] = v[3]
#                 x['sum'] = x['sum'] + v[3]
#                 x['ksum'] = x['ksum'] + (v[3]*v[7])
#                 x['bonus'] = ""
#     #[{'name': 'Admin', 'kkk': 12, 'джф': 20, 'kit': 25, 'hggg': 1}, {'name': 'динамо', 'kkk': '', 'джф': '', 'kit': '', 'hggg': ''}, {'name': 'цска', 'kkk': 8, 'джф': 20, 'kit': 40, 'hggg': 2}]
#     result = []
#     for x in users:
#         result.append([*x.values()])
#     return result
#     #print(result)
#     # for x in result:
#     #     ws.append(x) 

#     # wb.save(f"excels/{day}.xlsx")      



# def result_weekly(points, usernames, sqldata1):
#     sqldata = select_data_dict("SELECT * FROM userpoints_weekly INNER JOIN usernames ON userpoints_weekly.telega_id = usernames.telega_id INNER JOIN points ON points.name = userpoints_weekly.point_name WHERE date BETWEEN ? AND ?", (monday.date(), sunday.date(), ))  #--------------------VOT ETO TEBE OCHEN NUJNO
#     dic = [dict(row) for row in sqldata]
#     pred_result = []
#     for x in usernames:
#         dd = {"name": x}
#         for z in points:
#             dd[z] = 0
#         dd["sum"] = 0
#         dd["ksum"] = 0
#         pred_result.append(dd)
#     for c in dic:
#         for z in pred_result:
#             if z['name'] == c['name']:
#                 z[c['point_name']]+=c['point_score']#-------------------ZAPOLNYAEM RESULT CHISLAMI
#                 z['sum']+=c['point_score']
#                 z['ksum']+=c['point_score']*c['ratio']
#     result = []
#     for x in pred_result:
#         result.append([*x.values()])   
#     return result
# sqldata1 = select_data_dict("SELECT usernames.name, userpoints_weekly.point_name, SUM(userpoints_weekly.point_score) AS total_point_score, (SUM(userpoints_weekly.point_score) * points.ratio) AS total_point_score_with_koef, CASE WHEN COUNT(DISTINCT userpoints_weekly.date) = 7 THEN (SUM(userpoints_weekly.point_score) * points.ratio) END AS bonus_score FROM userpoints_weekly INNER JOIN usernames ON userpoints_weekly.telega_id = usernames.telega_id INNER JOIN points ON points.point_name = userpoints_weekly.point_name WHERE userpoints_weekly.date BETWEEN ? AND ? GROUP BY usernames.name,  userpoints_weekly.point_name", (monday.date(), sunday.date(), ))
sqldata1 = select_data_dict("""
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


def bonus_ratio_editor(bonus, my_num):
    if bonus<1 and bonus>0:
        my_num = my_num*bonus
    elif bonus>1:
        my_num = bonus
    elif bonus==1 or bonus==0:
        my_num=0
    return my_num

#print(bonus_ratio_editor(0.5, 10))

def womans_report(usernames, points, sqldata1):
    # today = datetime.now()
    # monday = today - timedelta(days=today.weekday())
    # sunday = monday + timedelta(days=6)
    week_dates = [monday + timedelta(days=i) for i in range(7)]

    # Преобразуем даты в строки для удобного отображения (опционально)
    sqldata2 = select_data_dict("SELECT usernames.name, userpoints_weekly.point_name, userpoints_weekly.date, userpoints_weekly.point_score, points.ratio FROM userpoints_weekly INNER JOIN usernames ON userpoints_weekly.telega_id = usernames.telega_id INNER JOIN points ON points.point_name = userpoints_weekly.point_name WHERE date BETWEEN ? AND ?", (monday.date(), sunday.date(), ))

    week_dates_str = [date.strftime('%Y-%m-%d') for date in week_dates]
    # points = select_data_single("SELECT name FROM points")
    # usernames = select_data_single("SELECT name FROM usernames ORDER BY name")
    pred_result = []
    result = []

    for username in usernames:
        my_dict = {}
        my_dict['username'] = username
        my_dict['Общая сумма'] = 0
        my_dict['Общая сумма с коэффициентом'] = 0
        my_dict['Бонус столбца'] = 0
        my_dict['Бонус строки'] = 0
        my_dict['Бонус минимумов'] = 0
        for point in points:
            my_dict[point] = {}
            for week_day in week_dates_str:
                my_dict[point][week_day] = 0
            my_dict[point]["Недельная сумма поинта"] = 0
            my_dict[point]["Недельная сумма поинта с коэффициентом"] = 0
        pred_result.append(my_dict)
    #print(pred_result)#[{'username': 'Admin', 'qq': {'2025-02-03': 0, '2025-02-04': 0, '2025-02-05': 0, '2025-02-06': 0, '2025-02-07': 0, '2025-02-08': 0, '2025-02-09': 0, 'Сумма': 0, 'Сумма с коэффициентом': 0}, 'djf': {'2025-02-03': 0, '2025-02-04': 0, '2025-02-05': 0, '2025-02-06': 0, '2025-02-07': 0, '2025-02-08': 0, '2025-02-09': 0, 'Сумма': 0, 'Сумма с коэффициентом': 0}, 'ввв': {'2025-02-03': 0, '2025-02-04': 0, '2025-02-05': 0, '2025-02-06': 0, '2025-02-07': 0, '2025-02-08': 0, '2025-02-09': 0, 'Сумма': 0, 'Сумма с коэффициентом': 0}, 'ффф': {'2025-02-03': 0, '2025-02-04': 0, '2025-02-05': 0, '2025-02-06': 0, '2025-02-07': 0, '2025-02-08': 0, '2025-02-09': 0, 'Сумма': 0, 'Сумма с коэффициентом': 0}}, {'username': 'Dinamo', 'qq': {'2025-02-03': 0, '2025-02-04': 0, '2025-02-05': 0, '2025-02-06': 0, '2025-02-07': 0, '2025-02-08': 0, '2025-02-09': 0, 'Сумма': 0, 'Сумма с коэффициентом': 0}, 'djf': {'2025-02-03': 0, '2025-02-04': 0, '2025-02-05': 0, '2025-02-06': 0, '2025-02-07': 0, '2025-02-08': 0, '2025-02-09': 0, 'Сумма': 0, 'Сумма с коэффициентом': 0}, 'ввв': {'2025-02-03': 0, '2025-02-04': 0, '2025-02-05': 0, '2025-02-06': 0, '2025-02-07': 0, '2025-02-08': 0, '2025-02-09': 0, 'Сумма': 0, 'Сумма с коэффициентом': 0}, 'ффф': {'2025-02-03': 0, '2025-02-04': 0, '2025-02-05': 0, '2025-02-06': 0, '2025-02-07': 0, '2025-02-08': 0, '2025-02-09': 0, 'Сумма': 0, 'Сумма с коэффициентом': 0}}]        
    for row in sqldata2:
        for result_row in pred_result:
            if result_row['username'] == row['name']:
                result_row[row['point_name']][row['date']] += row['point_score']
    otvet = [
         {'name': 'Admin', 'point_name': 'djf', 'totalsum_point_score': 75, 'point_week_sum': 10, 'ratio': 2, 'mins': 30, 'bonus_of_mins': 30, 'count_row_bonus': 1, 'bonus_of_rows': 0.2, 'count_column_bonus': 1, 'bonus_of_cols': 20, 'total_total_ratiosum': 1027, 'weekly_total_ratiosum': 311}, 
         {'name': 'Admin', 'point_name': 'qq', 'totalsum_point_score': 230, 'point_week_sum': 87, 'ratio': 3, 'mins': 10, 'bonus_of_mins': 30, 'count_row_bonus': 1, 'bonus_of_rows': 0.2, 'count_column_bonus': 1, 'bonus_of_cols': 20, 'total_total_ratiosum': 1027, 'weekly_total_ratiosum': 311},
        ]
    
    for summs in sqldata1:
        date_sum_count = 0
        for result_row in pred_result:
            if result_row['username'] == summs['name']:
                result_row[summs['point_name']]["Недельная сумма поинта"] = summs['point_week_sum']
                result_row[summs['point_name']]["Недельная сумма поинта с коэффициентом"] = summs['point_week_sum']*summs['ratio']
                # my_dict['username'] = username
                # my_dict['Общая сумма'] = 0
                # my_dict['Общая сумма с коэффициентом'] = 0
                # my_dict['Бонус столбца'] = 0
                # my_dict['Бонус строки'] = 0
                # my_dict['Бонус минимумов'] = 0
                result_row['Общая сумма'] += summs['totalsum_point_score']
                result_row['Общая сумма с коэффициентом'] = summs['weekly_total_ratiosum']
                result_row['Бонус столбца'] = bonus_ratio_editor(bonus=summs['bonus_of_cols'], my_num=summs['weekly_total_ratiosum'])*summs['count_column_bonus']
                result_row['Бонус строки'] = bonus_ratio_editor(bonus=summs['bonus_of_rows'], my_num=summs['weekly_total_ratiosum'])*summs['count_row_bonus']
                my_dict['Бонус минимумов'] = 0
                # row_bonus += bonus_ratio_editor(bonus=summs['bonus_of_cols'], my_num=)
                # result_row['Общая сумма с бонусами'] += summs['totalsum_point_score']

                
    for res in pred_result:
        heading = [res['username'], *week_dates_str, "Недельная сумма поинта", "Недельная сумма поинта с коэффициентом"]
        empty_list = ['']*7
        footer = ['Общее', *empty_list, ]
        result.append(heading)
        for point in points:
            row = []
            row = [point, *res[point].values()]
            result.append(row)
        result.append([])
        result.append([])
    return result

#womans_report(points=just_points, usernames=just_usenames, sqldata1=sqldata1)





# def exsel_creator():
#     just_points = select_data_single("SELECT name FROM points")
#     just_usenames = select_data_single("SELECT name FROM usernames ORDER BY name")

#     sqldata1 = select_data_dict("SELECT usernames.name, userpoints_weekly.point_name, SUM(userpoints_weekly.point_score) AS total_point_score, (SUM(userpoints_weekly.point_score) * points.ratio) AS total_point_score_with_koef, CASE WHEN COUNT(DISTINCT userpoints_weekly.date) = 7 THEN (SUM(userpoints_weekly.point_score) * points.ratio + points.bonus) END AS bonus_score FROM userpoints_weekly INNER JOIN usernames ON userpoints_weekly.telega_id = usernames.telega_id INNER JOIN points ON points.name = userpoints_weekly.point_name WHERE userpoints_weekly.date BETWEEN ? AND ? GROUP BY usernames.name,  userpoints_weekly.point_name", (monday.date(), sunday.date(), ))
    
#     # Создаем новую рабочую книгу
#     workbook = Workbook()
#     points_release = ["", *just_points, "Сумма", "Сумма c коэффициентом", "Сумма с бонусом"]
#     # Добавляем новый лист
#     sheet1 = workbook.active  # по умолчанию уже есть активный лист
#     sheet1.title = "Недельный отчет"  # переименовываем лист
#     # Вставляем данные в Лист 1
#     sheet1.append(points_release)
#     for row in result_weekly(just_points ,just_usenames, sqldata1):
#         sheet1.append(row)
#     # Создаем еще один лист
#     sheet2 = workbook.create_sheet(title="Подробный недельный отчет")
#     # Вставляем данные в Лист 2
#     # sheet2.append(points_release)
#     for row in womans_report(points=just_points, usernames=just_usenames, sqldata1=sqldata1):
#         sheet2.append(row)
#     # Создаем третий лист
#     sheet3 = workbook.create_sheet(title="Общий отчет")
#     # Вставляем данные в Лист 3
#     sheet3.append(points_release)
#     #print(result_total(just_usenames=just_usenames, just_points=just_points, sqldata1 = sqldata1))
#     for row in result_total(just_usenames=just_usenames, just_points=just_points, sqldata1 = sqldata1):
#         sheet3.append(row)
#     # Сохраняем рабочую книгу
#     workbook.save("excels/example.xlsx")

#exsel_creator()

# print(result_weekly())
# print(result_total())
#print(womans_report())