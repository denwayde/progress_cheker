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
print(select_data("SELECT* FROM user_points WHERE point_name = ? AND telega_id = ? ORDER BY id DESC LIMIT 1", ('kkk', '6293086969', )))