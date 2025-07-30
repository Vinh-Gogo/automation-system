from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

def upload_file_to_drive(file_path, folder_id):
    # Define the scope for Google Drive API
    SCOPE = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file"
    ]

    # Authenticate with Google using service account credentials
    try:
        creds = Credentials.from_service_account_file('service_account.json', scopes=SCOPE)
        service = build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"Error authenticating with Google Drive: {e}")
        print("Please ensure 'service_account.json' is present and valid, and Drive API is enabled.")
        raise

    file_name = os.path.basename(file_path)
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)

    try:
        file = service.files().create(body=file_metadata, media=media, fields='id,webViewLink').execute()
        print(f'File ID: {file.get('id')}')
        return file.get('webViewLink')
    except Exception as e:
        print(f"Error uploading file to Google Drive: {e}")
        raise
