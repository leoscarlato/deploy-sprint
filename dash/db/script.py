import sqlite3

conn = sqlite3.connect('dash/db/database.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL      
)""")

# create a table of authentication logs
# it just stores the username and the time of the login
# add type login, logout, register
cursor.execute("""CREATE TABLE IF NOT EXISTS auth_logs (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    time TEXT NOT NULL,
    type TEXT NOT NULL
)""")

conn.commit()

