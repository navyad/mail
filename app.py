from gmail_client import GmailClient

from messages import fetch_messages, process_messages
from dbapi import insert_emails


def fetch_populate_emails():
    """
    fetch the emails from gmail and load in db
    """
    client = GmailClient()
    service = client.build_service()
    messages = fetch_messages(client=client, service=service)
    records = process_messages(client=client, service=service, messages=messages)
    insert_emails(records)


if __name__ == '__main__':
    fetch_populate_emails()
