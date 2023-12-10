import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://mail.google.com/"]

EMAIL = "tmd526@gmail.com"


def get_credentials():
    """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        if not labels:
            print("No labels found.")
            return
        return service

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")


def send_email(service, image_path):
    """
    takes image_path which should be an image file.

    :param service:
    :param image_path:
    :return:
    """

    message = MIMEMultipart()
    message['to'] = EMAIL
    message['from'] = EMAIL
    message['subject'] = "New client!"
    message.attach(MIMEText("New client came into the store!"))

    fp = open(image_path, 'rb')
    image = MIMEImage(fp.read())
    fp.close()
    message.attach(image)
    body_message = {'raw': urlsafe_b64encode(message.as_bytes()).decode()}
    service.users().messages().send(userId="me", body=body_message).execute()


if __name__ == "__main__":
    send_email("test.jpg")
