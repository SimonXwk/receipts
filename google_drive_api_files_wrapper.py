from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage


from config import Config

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES = Config.SCOPES
CLIENT_SECRET_FILE = Config.CLIENT_SECRET_FILE
APPLICATION_NAME = Config.APPLICATION_NAME
SAVED_CREDENTIAL_NAME = Config.SAVED_CREDENTIAL_NAME


def get_credentials():
    """ ( *_*)/ Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')

    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, SAVED_CREDENTIAL_NAME)

    print("\n>>> Configurations:\n{}\nHome Directory : {}\nCredential Directory : {}\nDirectory to be used for Credential : {}".format(flags, home_dir, credential_dir, credential_path))

    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to : ' + credential_path)
    return credentials


class File:
    def __init__(self):
        self.credentials = get_credentials()
        print("\n>>> Fetching Credentials Successfully!\n".format('-' * 60, '-' * 60))
        self.http = self.credentials.authorize(httplib2.Http())
        self.drive_service = discovery.build('drive', 'v3', http=self.http)

    def list(self, **kwargs):
        response = self.drive_service.files().list(**kwargs).execute()
        items = list(response.get('files', []))

        # Process the Query result from Google Drive query
        if not items:
            print("{}\n>>> Listing Files (no files found!)\n".format('-' * 60, '-' * 60))
            return None
        else:
            print("{}\n>>> Listing Files ({} found from the google drive query result)\n{}".format('-' * 60, len(items), '-' * 60))
            return items
