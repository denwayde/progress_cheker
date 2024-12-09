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


# data = select_data("SELECT*FROM admin")
# print(data)


# data = select_data("SELECT telega_id FROM usernames WHERE hour IS NOT NULL AND minute IS NOT NULL")#[(1, 'цска', 6293086969, '16', '00', 'Воскресенье-Воскресенье')]
# print(data)

# data =select_data("SELECT name FROM usernames WHERE name = ?", ('jij',)) 
# print(data)  
#data0 = select_data("SELECT* FROM user_points INNER JOIN points ON points.name = user_points.point_name")
#print(data0)#(2, 'kkk', 6293086969, 63, '2024-11-16', 1, 'kkk', 2, 10)
#data = select_data("SELECT* FROM user_points INNER JOIN points ON points.name = user_points.point_name INNER JOIN usernames ON user_points.telega_id = usernames.telega_id")
#print(userpoints[0])#(2, 'kkk', 6293086969, 63, '2024-11-16', 1, 'kkk', 2, 10, 6, 'ЦСКА', 6293086969, None)
# sovpadenie = False
# result = []
# for x in data:
#     for z in result:
#         if x[10] in z:
#             sovpadenie = True
#             z[1] = z[1] + (x[3] * x[7])
#     if sovpadenie == False:
#         result.append([x[10], x[3] * x[7]])
#     sovpadenie = False
# sorted_data = sorted(result, key=lambda x: x[1], reverse=True)

# #print(sorted_data)

# for i, (name, points) in enumerate(sorted_data):
#     print(str(i+1) + " " + name + " "+ str(round(points, 2)))

# data = select_data("SELECT*FROM points")#[(1, 'kkk', 2, 10), (3, 'джф', 1.3, 30), (4, 'kit', 1, 60)]
# output = ""
# for x in data:
#     out_el = str(x[1]) + ": " +str(x[-1]) + "\n"
#     output = output + out_el

# print(output)
