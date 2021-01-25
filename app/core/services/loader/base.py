import os.path
import requests
from app.core.util.color import Logger

logger = Logger()


class Scope(object):
    """URLs for read or read/write access to Google sheets
    
    see more here: https://developers.google.com/sheets/guides/authorizing
    """
   
    # Read only access to Google sheets
    read = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # read and write access to Google sheets
    write = ['https://www.googleapis.com/auth/spreadsheets']


class Loader(object):
    """The loader class responsible for pulling data from google sheets but
    not the sample csv sheet in csv directory.

    see: https://developers.google.com/sheets/api/guides/concepts
    
    This will try to locate the credential keys if none is found, it will pull
    from csv folder instead.
    """
    credentials = None

    def __init__(self):
        """
        see more here https://developers.google.com/sheets/api/guides/concepts
        """
        self.scope = Scope.read  # default set to readonly
        self.spreadsheetsID = '1-3mrtO5tBDb1_Sn5YKZrp1avQ4chKD-x-U7c-gWpkuo'
        self.sheetID = '216733205'
        self.range_name = None
        self.credentials_path = './setting/secret/google_credential.json'
        self.token_path = './setting/secret/google_token.pickle'
        self.endpoint = 'https://docs.google.com/spreadsheets/d'
        self.use_oath2 = False

        # the sheet file name. This is not the google sheet name but
        # the file name of which will be stored in the folder core
        self.sheet_name = 'sample'
        self.file_saved_endpoint = './csv_data/core'
        self.debug = False
    
    def pull_from_public_sheets(self):
        """This method will try to pull the content from public google sheets"""
        if self.debug:
            logger.warn('Warning: Pulling from public google sheets...')
        response = requests.get(f'{self.endpoint}/{self.spreadsheetsID}/export?format=csv&gid={self.sheetID}')
        assert response.status_code == 200, 'Wrong status code'
        try:
            open(f'./csv_data/core/{self.sheet_name}.csv', 'wb').write(response.content)
            if self.debug:
                logger.info('Successfully pulled data')
        except Exception as e:
            raise Exception(e)

    def download(self):
        """Will attempt to download the source file"""
        if self.use_oath2 is False:
            return self.pull_from_public_sheets()
        else:
            if os.path.exists(self.credentials_path):
                from googleapiclient.discovery import build
                from google_auth_oauthlib.flow import InstalledAppFlow
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.scope)
                self.credentials = flow.run_local_server(port=0)

            service = build('sheets', 'v4', credentials=self.credentials)
            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.spreadsheetId, sheetId=self.sheetID).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
            else:
                print('Name, Major:')
                for row in values:
                    print(row)