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




