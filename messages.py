import re

from dateutil import parser


def fetch_messages(client, service):
    print("fetching messages ....")
    return client.get_messages(service=service)


def parse_date(date_string):
    field = "received_date"
    date_object = parser.parse(date_string)
    value = date_object.date()
    return field, value


def parse_from(from_string):
    field = 'sender'
    match = re.search(r'<([^>]+)>', from_string)
    if match:
        value = match.group(1)
    else:
        value = from_string
    return field, value


def process_email(email):
    item = {"message_id": email['id']}
    for header in email['payload']['headers']:
        if header['name'] in ['From', 'Subject', 'Date']:
            field = header['name'].lower()
            value = header['value']
            if field == 'date':
                field, value = parse_date(date_string=value)
            if field == 'from':
                field, value = parse_from(from_string=value)
            item.update({field: value})
    return item


def process_messages(client, service, messages):
    if not messages:
        print('No messages found.')
        return
    print("processing messages ....")
    records = []
    for message in messages:
        email = client.get_email(service=service, message_id=message['id'])
        email_data = process_email(email=email)
        records.append(email_data)
    return records
