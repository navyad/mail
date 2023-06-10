import sqlite3

from datetime import datetime, timedelta

from constants import PREDICATE_MAP


def get_connection():
    return sqlite3.connect('database.db')


def create_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email (
                message_id VARCHAR(50),
                sender VARCHAR(255),
                subject VARCHAR(255),
                received_date DATE
            )
        ''')
    print("Email table created successfully.")


def insert_emails(records):
    with get_connection() as conn:
        cursor = conn.cursor()
        print("inserting records...")
        cursor.executemany("INSERT INTO email VALUES(:message_id, :sender, :subject, :received_date)", records)
        conn.commit()
        print("Bulk inserts completed successfully.")


class RuleQuery:

    def __init__(self, rule):
        self.rule = rule
        self.all_any_map = {"All": " AND ", "Any": " OR "}

    def __handle_n_days_old(self, value):
        n_days_ago = datetime.now() - timedelta(days=int(value))
        return n_days_ago.strftime('%Y-%m-%d')

    def get_query_for_condition(self, query, condition):
        field = condition["field"]
        predicate = condition["predicate"]
        value = condition["value"]

        if predicate == "contains":
            query += f"{field} {PREDICATE_MAP[predicate]} '%{value}%'"
        elif predicate == "not equals":
            query += f"{field} {PREDICATE_MAP[predicate]} '{value}'"
        elif predicate == "less than":
            n_days_ago_str = self.__handle_n_days_old(value=value)
            query += f"{field} {PREDICATE_MAP[predicate]} '{n_days_ago_str}'"

        query += self.all_any_map[self.rule["predicate"]]
        return query

    def remove_trailing_predicate(self, query):
        return query[:-5] if self.rule["predicate"] == "All" else query[:-4]

    def build_query(self):
        query = "SELECT * FROM email WHERE "
        for condition in self.rule["conditions"]:
            query = self.get_query_for_condition(query=query, condition=condition)
        query = self.remove_trailing_predicate(query=query)
        return query

    def run_query(self, query):
        with get_connection() as conn:
            cursor = conn.cursor()
            print("running query...")
            return cursor.execute(query).fetchall()
