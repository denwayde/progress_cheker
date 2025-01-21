from openpyxl import Workbook
from db_func import select_data, select_data_dict, select_data_single
# import datetime
from datetime import datetime, timedelta

def result_total():
    # wb = Workbook()
    # ws = wb.active
    just_points = select_data_single("SELECT name FROM points")#[('kkk',), ('джф',), ('kit',), ('hggg',)]
    just_usenames = select_data_single("SELECT name FROM usernames ORDER BY name")
    users_points = select_data("SELECT* FROM user_points INNER JOIN points ON points.name = user_points.point_name INNER JOIN usernames ON user_points.telega_id = usernames.telega_id ORDER BY usernames.name")
    #day = datetime.datetime.now().strftime("%Y-%m-%d")
    # print(users_points)
    # just_usenames = [x[0] for x in usernames]
    # just_points = [x[0] for x in points]
    # points_release = ["", *just_points, "Сумма", "Сумма c учетом коэффициентов"]
    # ws.append(points_release)
    users = []
    for x in just_usenames:
        my_dict = {}
        my_dict["name"] = x
        for z in just_points:
            my_dict[z] = ""
        my_dict["sum"] = 0
        my_dict["ksum"] = 0
        users.append(
            my_dict
        )
    for x in users:
        for v in users_points:
            if x['name'] in v:
                x[v[1]] = v[3]
                x['sum'] = x['sum'] + v[3]
                x['ksum'] = x['ksum'] + (v[3]*v[7])
    #[{'name': 'Admin', 'kkk': 12, 'джф': 20, 'kit': 25, 'hggg': 1}, {'name': 'динамо', 'kkk': '', 'джф': '', 'kit': '', 'hggg': ''}, {'name': 'цска', 'kkk': 8, 'джф': 20, 'kit': 40, 'hggg': 2}]
    result = []
    for x in users:
        result.append([*x.values()])
    return result
    #print(result)
    # for x in result:
    #     ws.append(x) 

    # wb.save(f"excels/{day}.xlsx")      



def result_weekly():
    # Получаем сегодняшнюю дату
    today = datetime.now()
    # Находим номер сегодняшнего дня недели (0 - понедельник, 6 - воскресенье)
    today_weekday = today.weekday()
    # Вычисляем дату понедельника текущей недели
    monday = today - timedelta(days=today_weekday)
    # Вычисляем дату воскресенья текущей недели
    sunday = monday + timedelta(days=6)
    sqldata = select_data_dict("SELECT * FROM userpoints_weekly INNER JOIN usernames ON userpoints_weekly.telega_id = usernames.telega_id INNER JOIN points ON points.name = userpoints_weekly.point_name WHERE date BETWEEN ? AND ?", (monday.date(), sunday.date(), ))  #--------------------VOT ETO TEBE OCHEN NUJNO
    #print([dict(row) for row in sqldata])
    dic = [dict(row) for row in sqldata]
    points = select_data_single("SELECT name FROM points")#[('kkk',), ('джф',), ('kit',), ('hggg',)]
    usernames = select_data_single("SELECT name FROM usernames ORDER BY name")
    pred_result = []

    for x in usernames:
        dd = {"name": x}
        for z in points:
            dd[z] = 0
        dd["sum"] = 0
        dd["ksum"] = 0
        pred_result.append(dd)
    # print(pred_result) #------------[ {'name': 'Admin', 'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0}, {'name': 'dd', 'qq': 0, 'djf': 0, 'ввв': 0, 'ффф': 0} ]
    for c in dic:
        for z in pred_result:
            if z['name'] == c['name']:
                z[c['point_name']]+=c['point_score']#-------------------ZAPOLNYAEM RESULT CHISLAMI
                z['sum']+=c['point_score']
                z['ksum']+=c['point_score']*c['ratio']
    #print(pred_result) #-------[{'name': 'Admin', 'qq': 23, 'djf': 34, 'ввв': 45, 'ффф': 56}, {'name': 'dd', 'qq': 45, 'djf': 21, 'ввв': 23, 'ффф': 23}]

    result = []
    for x in pred_result:
        result.append([*x.values()])    #tut vmesto novogo cikla luche srazu sdelat ws.append([*x.values()])
    return result

# print(result_weekly())
#print(result_total())