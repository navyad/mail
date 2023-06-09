from gmail_client import GmailClient

from populate import fetch_messages, process_messages


def fetch_populate_emails():
    """
    fetch the emails from gmail and load in db
    """
    client = GmailClient()
    service = client.build_service()
    messages = fetch_messages(client=client, service=service)
    records = process_messages(client=client, service=service, messages=messages)
    print(records)


if __name__ == '__main__':
    fetch_populate_emails()
