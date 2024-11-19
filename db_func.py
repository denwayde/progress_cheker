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

def insert_many(insertion_query, lst):
    global connection
    cur = connection.cursor()
    cur.executemany(insertion_query, lst)
    connection.commit()
    
#print(select_data("SELECT name FROM usernames"))
#print(select_data("SELECT* FROM user_points WHERE point_name = ? AND telega_id = ? ORDER BY id DESC LIMIT 1", ('kkk', '6293086969', )))
#print(select_data("SELECT * FROM points"))#[(1, 'kkk', 2), (3, 'джф', 1.3), (4, 'kit', 1)] тут опять нужна проверка на нулевое значение

#print(select_data("SELECT* FROM user_points INNER JOIN points ON points.name = user_points.point_name"))
data = [
    (2, 'kkk', 6293086969, 63, '2024-11-16', 1, 'kkk', 2), #126
    (3, 'джф', 6293086969, 44, '2024-11-09', 3, 'джф', 1.3),#57.2
    (4, 'джф', 6293086969, 12, '2024-11-16', 3, 'джф', 1.3),#15.6
    (5, 'kit', 6293086969, 54, '2024-11-16', 4, 'kit', 1),#54
    (6, 'kkk', 6293086969, 92, '2024-11-18', 1, 'kkk', 2),#184
    (7, 'kkk', 6293086970, 23, '2024-11-18', 1, 'kkk', 2),
    (8, 'джф', 6293086970, 50, '2024-11-18', 3, 'джф', 1.3),
    (9, 'kit', 6293086970, 70, '2024-11-18', 4, 'kit', 1)
]


sovpadenie = False
result = []

for x in data:
    for z in result:
        if x[2] in z:
            sovpadenie = True
            z[1] = z[1] + (x[3] * x[-1])
    if sovpadenie == False:
        result.append([x[2], x[3]])
    sovpadenie = False

print(result)




# for x in range(len(data)):
#     try:
#         if data[x][2] == data[x+1][2]:
#             s = s + (data[x][3] * data[x][-1])
#     except IndexError:
#         pass

# print(s)
