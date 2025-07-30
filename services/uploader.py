from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

def upload_file_to_drive(file_path, folder_id):
    # Định nghĩa phạm vi cho Google Drive API
    SCOPE = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file"
    ]

    # Xác thực với Google bằng thông tin đăng nhập tài khoản dịch vụ
    try:
        creds = Credentials.from_service_account_file('service_account.json', scopes=SCOPE)
        service = build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"Lỗi khi xác thực với Google Drive: {e}")
        print("Vui lòng đảm bảo 'service_account.json' tồn tại và hợp lệ, và Drive API đã được bật.")
        raise

    file_name = os.path.basename(file_path)
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    print(file_metadata)
    media = MediaFileUpload(file_path, resumable=True)

    try:
        file = service.files().create(body=file_metadata, media=media, fields='id,webViewLink').execute()
        print(f'ID tệp: {file.get('id')}')
        return file.get('webViewLink')
    except Exception as e:
        print(f"Lỗi khi tải tệp lên Google Drive: {e}")
        raise
