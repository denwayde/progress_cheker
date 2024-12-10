from openpyxl import Workbook
from db_func import select_data


# wb = Workbook()
# ws = wb.active

points = select_data("SELECT * FROM points")#[(1, 'kkk', 2, 10), (3, 'джф', 1.3, 30), (4, 'kit', 1, 60), (6, 'hggg', 1.2, 40)]
#print(points)

data = data = select_data("SELECT* FROM user_points INNER JOIN points ON points.name = user_points.point_name INNER JOIN usernames ON user_points.telega_id = usernames.telega_id")

print(data)#[(16, 'kkk', 6293086969, 23, '2024-11-30', 1, 'kkk', 2, 10, 1, 'цска', 6293086969, '17', '00', 'Понедельник-Воскресенье'), (17, 'kit', 6293086969, 12, '2024-12-10', 4, 'kit', 1, 60, 1, 'цска', 6293086969, '17', '00', 'Понедельник-Воскресенье'), (18, 'hggg', 6293086969, 23, '2024-12-10', 6, 'hggg', 1.2, 40, 1, 'цска', 6293086969, '17', '00', 'Понедельник-Воскресенье'), (19, 'kit', 1949640271, 73, '2024-12-10', 4, 'kit', 1, 60, 10, 'Admin', 1949640271, '16', '07', 'Понедельник-Воскресенье'), (20, 'джф', 1949640271, 12, '2024-12-10', 3, 'джф', 1.3, 30, 10, 'Admin', 1949640271, '16', '07', 'Понедельник-Воскресенье'), (21, 'hggg', 1949640271, 12, '2024-12-10', 6, 'hggg', 1.2, 40, 10, 'Admin', 1949640271, '16', '07', 'Понедельник-Воскресенье')]

