import os

import sqlite3


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


def insert_emails(records):
    create_table()
    with get_connection() as conn:
        cursor = conn.cursor()
        print("inserting records...")
        cursor.executemany("INSERT INTO Email VALUES(:sender, :subject, :received_date)", records)
        conn.commit()
        print("Bulk inserts completed successfully.")
