from gmail_client import GmailClient


def fetch_messages():
    client = GmailClient()
    service = client.build_service()
    return client.get_messages(service=service)


if __name__ == '__main__':
    print("connecting to gmail client")
    fetch_messages()
