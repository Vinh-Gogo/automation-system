import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

def read_sheet(spreadsheet_id, range_name):
    # Define the scope for Google Sheets and Drive API
    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Authenticate with Google using service account credentials
    # Ensure your service account key file (e.g., 'service_account.json') is in the project root
    # and is properly configured in Google Cloud Platform with Sheets and Drive API enabled.
    try:
        creds = Credentials.from_service_account_file('service_account.json', scopes=SCOPE)
        client = gspread.authorize(creds)
    except Exception as e:
        print(f"Error authenticating with Google: {e}")
        print("Please ensure 'service_account.json' is present and valid, and APIs are enabled.")
        return pd.DataFrame()

    try:
        sheet = client.open_by_id(spreadsheet_id).worksheet(range_name.split('!')[0])
        data = sheet.range(range_name)

        # Extract headers from the first row
        headers = [cell.value for cell in data[:len(data) // sheet.col_count]]

        # Extract data rows
        rows_data = []
        for i in range(len(headers), len(data), sheet.col_count):
            row_values = [cell.value for cell in data[i:i + sheet.col_count]]
            rows_data.append(row_values)
        
        df = pd.DataFrame(rows_data, columns=headers)
        return df

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Error: Spreadsheet with ID '{spreadsheet_id}' not found.")
        return pd.DataFrame()
    except gspread.exceptions.WorksheetNotFound:
        print(f"Error: Worksheet '{range_name.split('!')[0]}' not found in spreadsheet '{spreadsheet_id}'.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error reading Google Sheet: {e}")
        return pd.DataFrame()
