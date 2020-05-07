import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ Устанавливает соединение с базой данных SQLite"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

# todo: https://medium.com/@mahmudahsan/how-to-use-python-sqlite3-using-sqlalchemy-158f9c54eb32
# todo: https://www.sqlitetutorial.net/sqlite-python/creating-database/