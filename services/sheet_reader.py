import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

def read_sheet(spreadsheet_id, range_name):
    # Định nghĩa phạm vi cho Google Sheets và Google Drive API
    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Xác thực với Google bằng thông tin đăng nhập tài khoản dịch vụ
    # Đảm bảo tệp khóa tài khoản dịch vụ của bạn (ví dụ: 'service_account.json') nằm trong thư mục gốc của dự án
    # và được cấu hình đúng cách trong Google Cloud Platform với Google Sheets và Google Drive API đã được bật.
    try:
        creds = Credentials.from_service_account_file('service_account.json', scopes=SCOPE)
        client = gspread.authorize(creds)
    except Exception as e:
        print(f"Lỗi khi xác thực với Google: {e}")
        print("Vui lòng đảm bảo 'service_account.json' tồn tại và hợp lệ, và các API đã được bật.")
        return pd.DataFrame()

    try:
        sheet = client.open_by_id(spreadsheet_id).worksheet(range_name.split('!')[0])
        data = sheet.range(range_name)

        # Trích xuất tiêu đề từ hàng đầu tiên
        headers = [cell.value for cell in data[:len(data) // sheet.col_count]]

        # Trích xuất các hàng dữ liệu
        rows_data = []
        for i in range(len(headers), len(data), sheet.col_count):
            row_values = [cell.value for cell in data[i:i + sheet.col_count]]
            rows_data.append(row_values)
        
        df = pd.DataFrame(rows_data, columns=headers)
        return df

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Lỗi: Không tìm thấy Trang tính với ID '{spreadsheet_id}'.")
        return pd.DataFrame()
    except gspread.exceptions.WorksheetNotFound:
        print(f"Lỗi: Không tìm thấy Trang tính '{range_name.split('!')[0]}' trong bảng tính '{spreadsheet_id}'.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Lỗi khi đọc Google Sheet: {e}")
        return pd.DataFrame()
