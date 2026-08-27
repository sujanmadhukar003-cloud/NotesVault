import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "notevaultuser"),
        password=os.getenv("MYSQL_PASSWORD", "notevaultpass"),
        database=os.getenv("MYSQL_DATABASE", "notevault")
    )