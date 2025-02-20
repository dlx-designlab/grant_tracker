import os
from dotenv import load_dotenv
import json
import base64
import gspread
from google.oauth2.service_account import Credentials

class GoogleSheetsUpdater:
    def __init__(self, ):
        
        SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/18taAPoE91R-0lna41CsCIO-xjD-CcRy90ikaV3EnQl0/edit"
        SHEET_NAME = "Academic"
        
        # Load service account credentials from environment variable
        # service_account_info = json.loads(base64.b64decode(os.getenv("GOOGLE_SHEET_CREDS")).decode())
        service_account_info = json.loads(os.getenv("GOOGLE_SHEET_CREDS"))

        # Define the scope (allows read/write access)
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

        # Authenticate using service account
        creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
        self.client = gspread.authorize(creds)

        # Open Google Sheet by URL or ID
        self.spreadsheet = self.client.open_by_url(SPREADSHEET_URL)
        # Select sheet by name
        self.sheet = self.spreadsheet.worksheet(SHEET_NAME)

    def append_data_to_column(self, column_title, data):
        # Find the column by title
        cell = self.sheet.find(column_title)
        if not cell:
            raise ValueError(f"Column with title '{column_title}' not found.")
        
        # Get the column index
        col_index = cell.col
        
        # Find the last row in the sheet
        col_values = self.sheet.col_values(col_index)
        last_row = len(col_values) + 1
        
        # Update the cell in the last row of the column
        self.sheet.update_cell(last_row, col_index, data)

# Example usage
if __name__ == "__main__":

    # Load environment variables
    load_dotenv()

    updater = GoogleSheetsUpdater()
    updater.append_data_to_column("Topic", "New Topic 33!")

    print("Google Sheet updated successfully!")