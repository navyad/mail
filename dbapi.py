import sqlite3

from datetime import datetime


def get_connection():
    return sqlite3.connect('database.db')


def create_email_table():
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
    print("email table created successfully.")


def create_token_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS token (
                token VARCHAR(250),
                expire_on DATETIME,
                created_on DATETIME
            )
        ''')
    print("token table created successfully.")


def insert_emails(records):
    with get_connection() as conn:
        cursor = conn.cursor()
        print("inserting records...")
        cursor.executemany("INSERT INTO email VALUES(:message_id, :sender, :subject, :received_date)", records)
        conn.commit()
        print("Bulk inserts completed successfully.")


def save_token(token, expire_on):
    created_on = datetime.now()
    with get_connection() as conn:
        cursor = conn.cursor()
        print("saving token...")
        cursor.execute("INSERT INTO token (token, expire_on, created_on) VALUES (?, ?, ?)", (token, expire_on, created_on))
        print("token saved successfully.")


def get_token():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT token FROM token")
        return cursor.fetchall()[0][0]


class RuleQuery:

    def __init__(self, rule):
        self.rule = rule
        self.all_any_map = {"All": " AND ", "Any": " OR "}
        self.PREDICATE_MAP = {"contains": "LIKE",
                              "not equals": "<>",
                              "less than": "<"}

    def get_query_for_condition(self, query, condition):
        field = condition["field"]
        predicate = condition["predicate"]
        value = condition["value"]

        if predicate == "contains":
            query += f"{field} {self.PREDICATE_MAP[predicate]} '%{value}%'"
        elif predicate == "not equals":
            query += f"{field} {self.PREDICATE_MAP[predicate]} '{value}'"
        elif predicate == "less than":
            query += f'date(received_date) >= date("now", "-{value} days")'
        else:
            raise Exception(f"Invalid predicate: {predicate}")

        query += self.all_any_map[self.rule["predicate"]]
        return query

    def remove_trailing_predicate(self, query):
        return query[:-5] if self.rule["predicate"] == "All" else query[:-4]

    def build_query(self):
        """
        combine the conditions of a rule and returns query
        """
        query = "SELECT message_id, subject FROM email WHERE "
        for condition in self.rule["conditions"]:
            query = self.get_query_for_condition(query=query, condition=condition)
        query = self.remove_trailing_predicate(query=query)
        return query

    def run_query(self, query):
        """
        run query in db to fetch realted emails
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            print("running query...")
            return cursor.execute(query).fetchall()

    def get_actions(self):
        for action in self.rule['actions']:
            yield action
