import os

import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class APIException(Exception):

    def __init__(self, error_message):
        self.error_message = error_message


class GmailClient:

    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
              'https://www.googleapis.com/auth/gmail.modify']
    CREDENTIALS_FILE = os.environ.get('GMAIL_API_CREDS_FILE')

    def authenticate(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            self.CREDENTIALS_FILE, self.SCOPES)
        return flow.run_local_server(port=0)

    def build_service(self, credentials):
        return build('gmail', 'v1', credentials=credentials)

    def get_messages(self, service):
        resource = service.users().messages()
        results = resource.list(userId='me', labelIds=['INBOX']).execute()
        return results.get('messages', [])

    def get_email(self, service, message_id):
        email = service.users().messages().get(
            userId='me', id=message_id).execute()
        return email

    def make_modify_request(self, access_token, message_id, payload):
        url = f'https://www.googleapis.com/gmail/v1/users/me/messages/{message_id}/modify'
        headers = {'Authorization': f'Bearer {access_token}'}
        print(f"modify request: {url}: {payload}")
        response = requests.post(url=url, json=payload, headers=headers)
        if response.status_code == 200:
            print("modify request successful")
            return
        error_message = response.json()['error']['message']
        raise APIException(error_message=error_message)

    def get_payload(self, action):
        payload = {"Mark as unread": {'addLabelIds': ['UNREAD']},
                   "Mark as read": {'removeLabelIds': ['UNREAD']},
                   "Move to TRASH": {'addLabelIds': ['TRASH']},
                   "Move to INBOX": {'addLabelIds': ['INBOX']}}
        return payload[action]
