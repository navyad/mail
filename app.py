import argparse

from gmail_client import GmailClient

from messages import fetch_messages, process_messages
from dbapi import insert_emails, get_query
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


def apply_rule(rule):
    """
    apply rule on stored emails
    """
    rule = find_rule_by_description(rule_description)
    query = get_query(rule)
    print(query)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Apple mail app")
    required_group = parser.add_argument_group("Required arguments")
    required_group.add_argument("--populate-db", action="store_true", help="Populate the database")
    required_group.add_argument("--rule-description", metavar='', choices=['Rule_1'], help="Description of the rule")

    args = parser.parse_args()

    if not (args.populate_db or args.rule_description):
        parser.error("At least one argument  is required.")

    rule_description = args.rule_description
    if args.populate_db:
        fetch_populate_emails()
    elif rule_description:
        apply_rule(rule_description)
