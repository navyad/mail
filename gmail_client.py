import os

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GmailClient:

    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    CREDENTIALS_FILE = os.environ.get('GMAIL_API_CREDS_FILE')

    def authenticate(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            self.CREDENTIALS_FILE, self.SCOPES)
        return flow.run_local_server(port=0)

    def build_service(self):
        credentials = self.authenticate()
        return build('gmail', 'v1', credentials=credentials)

    def get_messages(self, service):
        resource = service.users().messages()
        results = resource.list(userId='me', labelIds=['INBOX']).execute()
        return results.get('messages', [])

    def get_email(self, service, message_id):
        email = service.users().messages().get(
            userId='me', id=message_id).execute()
        return email
