from dateutil import parser
from unittest import mock

import pytest

from mail.messages import parse_date, parse_from, process_email, process_messages


@pytest.fixture
def email():
    return {
        'payload': {
            'headers': [
                {'name': 'From', 'value': 'MUBI <hello@releases.mubi.com>'},
                {'name': 'Subject', 'value': 'Pride Unprejudiced'},
                {'name': 'Date', 'value': 'Fri, 09 Jun 2023 11:30:16 +0000'}
            ]
        }
    }


@pytest.fixture
def client():
    return mock.Mock()


@pytest.fixture
def service():
    return mock.Mock()


def test_parse_date():
    date_string = 'Fri, 09 Jun 2023 11:30:16 +0000'
    expected_field = 'received_date'
    expected_value = parser.parse(date_string).date()
    field, value = parse_date(date_string)
    assert field == expected_field
    assert value == expected_value


def test_parse_from():
    from_string = 'MUBI <hello@releases.mubi.com>'
    expected_field = 'sender'
    expected_value = 'hello@releases.mubi.com'
    field, value = parse_from(from_string)
    assert field == expected_field
    assert value == expected_value


def test_process_email(email):
    expected_result = {'sender': 'hello@releases.mubi.com', 'subject': 'Pride Unprejudiced', 'received_date': parser.parse('Fri, 09 Jun 2023 11:30:16 +0000').date()}
    result = process_email(email)
    assert result == expected_result


def test_process_messages(client, service, email):
    messages = [{'id': '123456789'}]
    client.get_email.return_value = email
    expected_records = [{'sender': 'hello@releases.mubi.com', 'subject': 'Pride Unprejudiced', 'received_date': parser.parse('Fri, 09 Jun 2023 11:30:16 +0000').date()}]
    records = process_messages(client, service, messages)
    assert records == expected_records
    client.get_email.assert_called_once_with(service=service, message_id='123456789')
