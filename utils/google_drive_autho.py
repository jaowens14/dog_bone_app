from __future__ import print_function

import os
from os import path
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload


cred_path = path.abspath(path.join(path.dirname(__file__), 'assets','credentials.json'))
token_path = path.abspath(path.join(path.dirname(__file__), 'assets','token.json'))
settings_path = path.abspath(path.join(path.dirname(__file__), 'assets','settings.yaml'))

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """



    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds, static_discovery=False)

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


def create_folder(folder_name):
    """ Create a folder and prints the folder ID
    Returns : Folder Id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)


    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds, static_discovery=False)
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents' : ['1TiH0dWR9M-oDiAZZBLXCjYJgy6QqBtNW']
        }

        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, fields='id'
                                      ).execute()
        print(F'Folder ID: "{file.get("id")}".')
        return file.get('id')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None
    

def upload_to_folder(folder_id, file_path):
    """Upload a file to the specified folder and prints file ID, folder ID
    Args: Id of the folder
    Returns: ID of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds, static_discovery=False)
        file_name = str(os.path.basename(os.path.normpath(file_path)))

        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path, resumable=True)
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print(F'File ID: "{file.get("id")}".')
        return file.get('id')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None
    


### theres a lot of extra stuff in here but it works.


def upload_build(path):


    log = open(os.path.join(path,'app_log.txt'), 'x')
    #log = open(path.abspath(path.join(path.dirname(__file__), 'assets','app_log.txt')))

    log.write("os.path.abspath(path.join(path.dirname(__file__), 'assets'))")
    log.write('\n')
    f = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets'))
    log.write(os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets')))
    log.write('\n')
    log.write("cred path")
    log.write('\n')
    log.write(cred_path)
    log.write('\n')
    log.write("result of os.path.exsists")
    log.write('\n')
    log.write(str(os.path.exists(f)))
    log.close() 
    build_number = os.path.basename(os.path.normpath(path))
    build_folder_id = create_folder(build_number)
    print("This is the path in the google file: ", path)
    for f in os.listdir(path):
        f = os.path.join(path, f)
        upload_to_folder(build_folder_id, f)

