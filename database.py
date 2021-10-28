from sqlite3.dbapi2 import Connection, Cursor
import sqlite3

DATABASE_PATH = "passwords.db"

UserData = tuple[str, str]

class Database:
    con: Connection
    cur: Cursor

class User:
    name: str
    password: str

    def __init__(self, user_data: UserData):
        self.name = user_data[0]
        self.password = user_data[1]

user_db = Database()
user_db.con = sqlite3.connect(DATABASE_PATH)
user_db.cur = user_db.con.cursor()
user_db.cur.execute("""
    create table if not exists Users (name text not null primary key, password text);
""")