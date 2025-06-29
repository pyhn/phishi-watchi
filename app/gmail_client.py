import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GmailClient:
    def __init__(self, SCOPES, client_secrets_path, token_path=""):
        self.scopes = SCOPES
        self.user_creds = None
        self.client_secrets_path = client_secrets_path
        self.token_path = token_path
        self.service = self._authorize()

    def _authorize(self):
        if self.token_path and os.path.exists(self.token_path):
            self.user_creds = Credentials.from_authorized_user_file(self.token_path, self.scopes)
        
        if not self.user_creds or not self.user_creds.valid:
            if self.user_creds and self.user_creds.expired and self.user_creds.refresh_token:
                self.user_creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_path, self.scopes)
                self.user_creds = flow.run_local_server(port=0)
        
            with open(self.token_path, "w") as token:
                token.write(self.user_creds.to_json())

        try:

            service = build("gmail","v1", credentials=self.user_creds)
            return service
        
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None



        