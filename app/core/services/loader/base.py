import os.path
import requests
import pickle
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
    public_sheet_endpoint = 'https://docs.google.com/spreadsheets/d'

    def __init__(self):
        """
        see more here https://developers.google.com/sheets/api/guides/concepts
        """
        self.scope = Scope.read  # default set to readonly
        self.spreadsheetsID = '1-3mrtO5tBDb1_Sn5YKZrp1avQ4chKD-x-U7c-gWpkuo'
        self.sheetID = '216733205'  # use this with public Sheet
        self.sheet_name = 'Sheet1'  # the sheet name used for private sheet with oauth2
        self.credentials_path = './setting/secret/client_credential.json'
        self.token_path = './setting/secret/google_token.pickle'  # checkpoint so we do not have to login again
        self.endpoint = 'https://docs.google.com/spreadsheets/d'  # for public use
        self.use_oauth2 = False  # enable oauth2 to pull data from private sheets. You will need client key
        self.store_file = True

        # the sheet file name. This is not the google sheet name but
        # the file name of which will be stored in the folder core
        self.file_saved_name = self.sheet_name
        self.file_saved_endpoint = './csv_data/core'
        self.debug = False

        self.range = None  # must be a string
    
    def set_range(self, start: str, end: str):
        """
        This must follow the format A1:B2 which refers to the group of cells in sheets

        Keep in mind that. Specify sheet name is good thing but not in this method
        For example: Sheet1!A2:B2 is not supported. Recommended to set

        :param start: start cell (string)

        :param end: end cell (string)
        """
        self.range = f'{start}:{end}'
    
    def set_sheet_name(self, name: str):
        """
        Set the name of the sheet in the spreadsheetsId if provided. If you intend to use Oauth2
        to access to Google sheets. Then this must be specified

        SheetID represent for each sheet in the spreadsheet. The name of the sheet must be a valid name
        which means it needs to be correctly written

        :param name: name of sheet (string)
        """
        self.sheet_name = name
    
    def set_stored_file(self, name: str = None):
        """
        Set the name of the file needs to be store upon successfully download
        If none is provided, it will instead use the sheet name provided to name the file
        """
        self.store_file = name
    
    def set_sheet_ID(self, sheetID: str):
        """
        The id of the sheet in the given spreadsheet. If you intend to use the public sheet provided
        by VirtComp or your custom public sheet then this must be specified.

        see here: https://docs.google.com/spreadsheets/d/{spreadsheetId}/edit#gid={sheetId}
        """
        self.sheetID = sheetID
    
    def set_scope(self, scope: str):
        """
        Set scope permission for the current session.
        
        Recommended not to set scope like this loader.scope = 'myscope'.

        Supported scope = ['read', 'write']
        """
        given_scope = scope.lower()
        if given_scope in ['read', 'write']:
            self.scope = getattr(Scope, given_scope)

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
                from google.auth.transport.requests import Request
                
                # we check if the save checkpoint from last login exists
                if os.path.exists(self.token_path):
                    with open(self.token_path, 'rb') as token:
                        self.credentials = pickle.load(token)

                # if the token credentials not found or invalid
                if not self.credentials or not self.credentials.valid:
                    # if the token expired
                    if self.credentials and self.credentials.expired() and self.credentials.refresh_token:
                        self.credentials.refresh(Request())
                    else:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            self.credentials_path, self.scope)
                        
                        # if no token found and not expired, it means
                        # we have fresh login flow
                        # run the server to obtain key access
                        self.credentials = flow.run_local_server()
                    
                    # save token details so next time we do not have to run the server again
                    with open(self.token_path, 'wb') as token:
                        pickle.dump(self.credentials, token)

            service = build('sheets', 'v4', credentials=self.credentials)
            # Call the Sheets API
            sheet = service.spreadsheets()
            if self.range:
                result = sheet.values().get(spreadsheetId=self.spreadsheetsID, range='A2:B').execute()
            else:
                result = sheet.values().get(spreadsheetId=self.spreadsheetsID, range=self.sheet_name).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
            else:
                for row in values:
                    print(row)