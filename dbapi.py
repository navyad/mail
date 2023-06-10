import sqlite3

from constants import PREDICATE_MAP


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


class RuleQuery:

    def __init__(self, rule):
        self.rule = rule

    def get_query_for_condition(self, query, condition):
        field = condition["field"]
        predicate = condition["predicate"]
        value = condition["value"]

        if predicate == "contains":
            query += f"{field} {PREDICATE_MAP[predicate]} '%{value}%'"
        elif predicate in ("not equals", "less than"):
            query += f"{field} {PREDICATE_MAP[predicate]} '{value}'"

        if self.rule["predicate"] == "All":
            query += " AND "
        elif self.rule["predicate"] == "Any":
            query += " OR "
        return query

    def remove_trailing_predicate(self, query):
        return query[:-5] if self.rule["predicate"] == "All" else query[:-4]

    def build_query(self):
        query = "SELECT * FROM your_table WHERE "
        for condition in self.rule["conditions"]:
            query = self.get_query_for_condition(query=query, condition=condition)
        query = self.remove_trailing_predicate(query=query)
        return query


def get_query(rule):
    return RuleQuery(rule=rule).build_query()
