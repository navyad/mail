from unittest import mock

import pytest
import requests
from google.oauth2.credentials import Credentials

from mail.gmail_client import GmailClient, APIException


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


@pytest.fixture
def request_data():
    return dict(access_token="access_token",
                message_id="message_id",
                payload={"addLabelIds": ["UNREAD"]})


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


def test_payload(gmail_client):
    assert gmail_client.get_payload('Mark as unread') == {'addLabelIds': ['UNREAD']}
    assert gmail_client.get_payload('Mark as read') == {'removeLabelIds': ['UNREAD']}
    assert gmail_client.get_payload('Move to TRASH') == {'addLabelIds': ['TRASH']}
    assert gmail_client.get_payload('Move to INBOX') == {'addLabelIds': ['INBOX']}


def test_get_payload_invalid_action(gmail_client):
    with pytest.raises(KeyError):
        gmail_client.get_payload("Invalid Action")


def test_make_modify_request_success(gmail_client, request_data, mocker):
    access_token = request_data["access_token"]
    message_id = request_data["message_id"]
    payload = request_data['payload']
    expected_response = {'success': True}

    mocker.patch('requests.post')
    response_mock = mocker.Mock()
    response_mock.status_code = 200
    mocker.patch.object(response_mock, 'json', return_value=expected_response)
    requests.post.return_value = response_mock

    json_response = gmail_client.make_modify_request(access_token, message_id, payload)
    assert json_response == expected_response

    url = f'https://www.googleapis.com/gmail/v1/users/me/messages/{message_id}/modify'
    headers = {'Authorization': f'Bearer {access_token}'}
    requests.post.assert_called_once_with(url=url, json=payload, headers=headers)


def test_make_modify_request_exception(gmail_client, request_data, mocker):
    access_token = request_data["access_token"]
    message_id = request_data["message_id"]
    payload = request_data['payload']

    mocker.patch('requests.post')
    response_mock = mocker.Mock()
    response_mock.status_code = 400
    mocker.patch.object(response_mock, 'json', return_value={'error': {'message': 'Bad Request'}})
    requests.post.return_value = response_mock

    with pytest.raises(APIException) as exp:
        gmail_client.make_modify_request(access_token, message_id, payload)
    assert exp.value.error_message == "Bad Request"