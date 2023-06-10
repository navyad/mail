import argparse

from gmail_client import GmailClient

from messages import fetch_messages, process_messages
from dbapi import insert_emails, RuleQuery, create_table
from rules import find_rule_by_description


def fetch_populate_emails():
    """
    fetch the emails from gmail and load in db
    """
    client = GmailClient()
    service = client.build_service()
    messages = fetch_messages(client=client, service=service)
    records = process_messages(client=client, service=service, messages=messages)
    insert_emails(records)


def apply_rule(rule_description):
    """
    apply rule on stored emails
    """
    rule = find_rule_by_description(description=rule_description)
    instance = RuleQuery(rule=rule)
    query = instance.build_query()
    print(query)
    rows = instance.run_query(query=query)
    print(rows)


if __name__ == '__main__':
    choices = ['Rule_1', 'Rule_2']
    parser = argparse.ArgumentParser(description="Apple mail app")
    required_group = parser.add_argument_group("Required arguments")
    required_group.add_argument("--create-table", action="store_true", help="Create Table")
    required_group.add_argument("--populate-db", action="store_true", help="Populate the database")
    required_group.add_argument("--rule-description", metavar='', choices=choices, help="Description of the rule")

    args = parser.parse_args()

    rule_description = args.rule_description
    if args.create_table:
        create_table()
    elif args.populate_db:
        fetch_populate_emails()
    elif rule_description:
        apply_rule(rule_description)
    else:
        parser.error("At least one argument  is required.")
