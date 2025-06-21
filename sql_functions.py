
import sqlite3 
import os


def create_database(db_name):
    if not os.path.exists(db_name):
        conn = sqlite3.connect(db_name)
        conn.close()


#create_database('test.db')