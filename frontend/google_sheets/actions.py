import gspread
from oauth2client.service_account import ServiceAccountCredentials

from frontend.google_sheets.constants import GoogleSheetsConstants


class GoogleSheet:
    def __init__(self, tab_name=None):
        self.constants = GoogleSheetsConstants()
        self.sheet_name = self.constants.SHEET_NAME

        if tab_name is None:
            self.tab_name = self.constants.TAB_NAME
        else:
            self.tab_name = tab_name

        self.col_number = self.constants.COL_NUMBER
        self.row_number = self.constants.ROW_NUMBER

        self.creds = self.__authorize(self.constants.CREDS_FILE_LOCATION, self.constants.SCOPE)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(self.sheet_name).worksheet(self.tab_name)

    @staticmethod
    def __authorize(creds_file_location, scope):
        """
        This function authorizes the credentials and returns the authorized object.
        """
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file_location, scope)
        return creds

    def get_data(self):
        """
        This function returns data present in the sheet in the json format.
        """
        data = self.sheet.get_all_records()
        return data

    def write_data(self, data):
        """
        This function writes data to the sheet.
        """
        self.sheet.update_cell(self.row_number, self.col_number, data)

    def write_row(self, data):
        """
        This function writes data to the sheet.
        """
        self.sheet.append_row(data)
