import sqlite3

db = sqlite3.connect('data.db')

c = db.cursor()


c.execute("""CREATE TABLE IF NOT EXISTS user(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name text,
    count_rec integer
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS Monday(
    monday_id INTEGER PRIMARY KEY AUTOINCREMENT,
    place text,
    time text,
    free int
    username text,
    people text
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS Tuesday(
    Tuesday_id INTEGER PRIMARY KEY AUTOINCREMENT,
    place text,
    time text,
    free int
    username text,
    people text
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS Wednesday(
    Wednesday_id INTEGER PRIMARY KEY AUTOINCREMENT,
    place text,
    time text,
    free int
    username text,
    people text
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS Thursday(
    Thursday_id INTEGER PRIMARY KEY AUTOINCREMENT,
    place text,
    time text,
    free int
    username text,
    people text
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS Friday(
    Friday_id INTEGER PRIMARY KEY AUTOINCREMENT,
    place text,
    time text,
    free int
    username text,
    people text
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS Saturday(
    Saturday_id INTEGER PRIMARY KEY AUTOINCREMENT,
    place text,
    time text,
    free int
    username text,
    people text
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS Sunday(
    Sunday_id INTEGER PRIMARY KEY AUTOINCREMENT,
    place text,
    time text,
    free int
    username text,
    people text
    )""")

db.commit()

db.close()
























