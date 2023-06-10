import argparse

from gmail_client import GmailClient

from messages import fetch_messages, process_messages
from dbapi import insert_emails, RuleQuery, create_table
from rules import find_rule_by_description


def fetch_populate_emails():
    """
    Fetch the emails from gmail and load in db
    """
    client = GmailClient()
    service = client.build_service()
    messages = fetch_messages(client=client, service=service)
    records = process_messages(client=client, service=service, messages=messages)
    insert_emails(records)


def apply_rule(rule_description):
    """
    Apply rule on stored emails and returns those rows from db
    """
    rule = find_rule_by_description(description=rule_description)
    instance = RuleQuery(rule=rule)
    query = instance.build_query()
    print(f"query for {rule_description} : {query}\n")
    rows = instance.run_query(query=query)
    return instance, rows


def perform_operations(rule_query_instance, rows):
    """
    Run actions on identified rows
    """
    client = GmailClient()
    creds = client.authenticate()
    for action in rule_query_instance.get_actions():
        for message_id, subject in rows:
            print(f"\nmessage_id={message_id}, subject={subject}, action={action}")
            payload = client.get_payload(action=action)
            client.make_modify_request(access_token=creds.token, message_id=message_id, payload=payload)


if __name__ == '__main__':
    choices = ['Rule_1', 'Rule_2', 'Rule_3']
    parser = argparse.ArgumentParser(description="Apple mail app")
    required_group = parser.add_argument_group("Required arguments")
    required_group.add_argument("--create-table", action="store_true", help="Create table")
    required_group.add_argument("--populate-db", action="store_true", help="Populate the database")
    required_group.add_argument("--apply-rule", metavar='', choices=choices, help="Apply rule")

    args = parser.parse_args()

    rule_id = args.apply_rule
    if args.create_table:
        create_table()
    elif args.populate_db:
        fetch_populate_emails()
    elif rule_id:
        rule_query_instance, rows = apply_rule(rule_description=rule_id)
        if not rows:
            print("Rows not found")
        perform_operations(rule_query_instance, rows)
    else:
        parser.error("At least one argument  is required.")
