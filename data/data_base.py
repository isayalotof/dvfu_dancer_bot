import sqlite3

db = sqlite3.connect('data.db')

c = db.cursor()


c.execute("""CREATE TABLE IF NOT EXISTS user(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name text,
    count_rec integer
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS Record(
    Sunday_id INTEGER PRIMARY KEY AUTOINCREMENT,
    day text,
    place text,
    time text,
    free int
    username text,
    people text
    )""")

db.commit()

db.close()
























