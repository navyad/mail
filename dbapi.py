import os

import sqlite3
from sqlite3 import Error


def get_connection():
    return sqlite3.connect('database.db')

def create_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Email (
                sender VARCHAR(255),
                subject VARCHAR(255),
                received_date DATE
            )
        ''')
    print("Email table created successfully.")


def populate_email(records):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO Email VALUES(:sender, :subject, :received_date)", records)
        conn.commit()
        print("Bulk inserts completed successfully.")
