from unittest import mock

import pytest
from google.oauth2.credentials import Credentials
from mail.gmail_client import GmailClient


@pytest.fixture
def mock_credentials():
    return mock.Mock(spec=Credentials)


@pytest.fixture
def mock_service(mock_credentials):
    mock_service = mock.Mock()
    mock_service.users.return_value.messages.return_value.list.return_value.execute.return_value = {'messages': [{"id": "val"}]}
    mock_service.users.return_value.messages.return_value.get.return_value.execute.return_value = "abc@gmail.com"
    mock_service.users.return_value.messages.return_value.return_value = mock_service.users.return_value.messages.return_value
    mock_service.users.return_value.return_value = mock_service.users.return_value
    mock_service.return_value = mock_service
    return mock_service


@pytest.fixture
def gmail_client(mock_credentials, mock_service):
    client = GmailClient()
    client.authenticate = mock.Mock(return_value=mock_credentials)
    client.build_service = mock.Mock(return_value=mock_service)
    return client


def test_build_service(gmail_client, mock_credentials, mock_service):
    service = gmail_client.build_service()
    assert service == mock_service


def test_get_messages(gmail_client, mock_service):
    messages = gmail_client.get_messages(mock_service)
    mock_service.users.return_value.messages.return_value.list.assert_called_once_with(userId='me', labelIds=['INBOX'])
    assert messages == [{"id": "val"}]


def test_get_email(gmail_client, mock_service):
    message_id = '123456789'
    email = gmail_client.get_email(mock_service, message_id)
    mock_service.users.return_value.messages.return_value.get.assert_called_once_with(userId='me', id=message_id)
    assert email == "abc@gmail.com"
