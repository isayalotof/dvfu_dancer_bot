import sqlite3

db = sqlite3.connect('data.db')

c = db.cursor()


c.execute("""CREATE TABLE IF NOT EXISTS user(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name integer,
    Place1 integer,
    Place2 integer,
    Place3 integer,
    Place4 integer
    )""")


c.execute("""CREATE TABLE IF NOT EXISTS Place1(
    Place1_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username text,
    day text,
    time_start text,
    duration decimal(1,2),
    people_group text
    )""")


c.execute("""CREATE TABLE IF NOT EXISTS Place2(
    Place2_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username text,
    day text,
    time_start text,
    duration decimal(1,2),
    people_group text
    )""")


c.execute("""CREATE TABLE IF NOT EXISTS Place3(
    Place3_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username text,
    day text,
    time_start text,
    duration decimal(1,2),
    people_group text
    )""")


c.execute("""CREATE TABLE IF NOT EXISTS Place4(
    Place4_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username text,
    day text,
    time_start text,
    duration decimal(1,2),
    people_group text
    )""")


db.commit()

























