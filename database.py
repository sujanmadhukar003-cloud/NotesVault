import os
import sqlite3
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "127.0.0.1"),
            port=int(os.getenv("MYSQL_PORT", "3306")),
            user=os.getenv("MYSQL_USER", "notevaultuser"),
            password=os.getenv("MYSQL_PASSWORD", "notevaultpass"),
            database=os.getenv("MYSQL_DATABASE", "notevault"),
            connection_timeout=2
        )
    except mysql.connector.Error:
        return SQLiteConnection(os.getenv("SQLITE_DATABASE", "notes.db"))


class SQLiteCursor:
    def __init__(self, cursor):
        self._cursor = cursor

    def execute(self, query, params=()):
        return self._cursor.execute(query.replace("%s", "?"), params)

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    @property
    def lastrowid(self):
        return self._cursor.lastrowid

    def close(self):
        self._cursor.close()


class SQLiteConnection:
    def __init__(self, database_path):
        self._connection = sqlite3.connect(database_path)

    def cursor(self):
        return SQLiteCursor(self._connection.cursor())

    def commit(self):
        self._connection.commit()

    def rollback(self):
        self._connection.rollback()

    def close(self):
        self._connection.close()