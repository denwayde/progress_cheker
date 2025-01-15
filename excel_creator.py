from openpyxl import Workbook
from db_func import select_data
import datetime

def exsel_creator():
    wb = Workbook()
    ws = wb.active

    points = select_data("SELECT name FROM points")#[('kkk',), ('джф',), ('kit',), ('hggg',)]
    usernames = select_data("SELECT name FROM usernames ORDER BY name")
    users_points = select_data("SELECT* FROM user_points INNER JOIN points ON points.name = user_points.point_name INNER JOIN usernames ON user_points.telega_id = usernames.telega_id ORDER BY usernames.name")

    day = datetime.datetime.now().strftime("%Y-%m-%d")
    # print(users_points)

    just_usenames = [x[0] for x in usernames]
    just_points = [x[0] for x in points]
    users = []

    points_release = ["", *just_points, "Сумма", "Сумма c учетом коэффициентов"]
    ws.append(points_release)

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

    #print(result)
    for x in result:
        ws.append(x) 

    wb.save(f"excels/{day}.xlsx")      

from functions import is_date_in_current_week

sqldata = select_data("SELECT*FROM userpoints_weekly INNER JOIN usernames ON userpoints_weekly.telega_id = usernames.telega_id")
#print(sqldata)

result_data = []

points = select_data("SELECT name FROM points")#[('kkk',), ('джф',), ('kit',), ('hggg',)]
usernames = select_data("SELECT name FROM usernames ORDER BY name")
just_usenames = [x[0] for x in usernames]
just_points = [x[0] for x in points]
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

#print(users)#[{'name': 'Admin', 'qq': '', 'djf': '', 'ввв': '', 'ффф': '', 'sum': 0, 'ksum': 0}, {'name': 'dd', 'qq': '', 'djf': '', 'ввв': '', 'ффф': '', 'sum': 0, 'ksum': 0}]

for x in users:
    for z in sqldata:
        if is_date_in_current_week(z[4]):
            if x['name'] in z:

                

# def exel_weekly():
#     data = select_data("SELECT*FROM userpoints_weekly")#[]
#     print(data)


# exel_weekly()
[
    (1, 'qq', 6293086969, 12, '2024-12-26', 16, 'dd', 6293086969, None, None, None), 
    (2, 'djf', 6293086969, 10, '2024-12-26', 16, 'dd', 6293086969, None, None, None), 
    (3, 'ввв', 6293086969, 23, '2024-12-26', 16, 'dd', 6293086969, None, None, None), 
    (4, 'ффф', 6293086969, 23, '2024-12-26', 16, 'dd', 6293086969, None, None, None), 
    (5, 'qq', 1949640271, 11, '2024-12-26', 15, 'Admin', 1949640271, None, None, None), 
    (6, 'djf', 1949640271, 34, '2024-12-26', 15, 'Admin', 1949640271, None, None, None), 
    (7, 'ввв', 1949640271, 45, '2024-12-26', 15, 'Admin', 1949640271, None, None, None), 
    (8, 'ффф', 1949640271, 56, '2024-12-26', 15, 'Admin', 1949640271, None, None, None),
    (9, 'qq', 1949640271, 12, '2024-12-26', 15, 'Admin', 1949640271, None, None, None),
    (10, 'qq', 6293086969, 33, '2024-12-26', 16, 'dd', 6293086969, None, None, None),
    (11, 'djf', 6293086969, 11, '2024-12-26', 16, 'dd', 6293086969, None, None, None)
]