import gspread
from oauth2client.service_account import ServiceAccountCredentials

from frontend.google_sheets.constants import COL_NUMBER


class GoogleSheet:
    def __init__(self, creds_file_location, scope, sheet_name, tab_name):
        self.creds = self.__authorize(creds_file_location, scope)
        self.client = gspread.authorize(self.creds)
        self.sheet_name = sheet_name
        self.tab_name = tab_name
        self.sheet = self.client.open(self.sheet_name).worksheet(self.tab_name)
        self.col_number = COL_NUMBER

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

    def row_number(self, process_id):
        """
        This function returns the row of the matching process_id
        """
        cell = self.sheet.find(process_id)
        return cell.row

    def write_data(self, data, process_id):
        """
        This function writes data to the sheet.
        """
        row = self.row_number(process_id)
        self.sheet.update_cell(row, self.col_number, data)
