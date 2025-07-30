# Automated Asset Generation and Reporting Workflow

## Mục tiêu Dự án

Dự án này nhằm mục đích thiết kế và xây dựng một quy trình tự động hóa hoàn chỉnh để tạo, quản lý và báo cáo các sản phẩm kỹ thuật số dựa trên dữ liệu đầu vào từ Google Sheets.

## Quy trình Làm việc

Quy trình tự động hóa được xây dựng theo các bước sau:

1.  **Đầu vào từ Google Sheets**: Dữ liệu được đọc tự động từ một tệp Google Sheets, bao gồm các trường như mô tả sản phẩm, URL tài sản mẫu, định dạng đầu ra mong muốn (PNG, JPG, GIF, MP3), và chỉ định mô hình AI (OpenAI/Claude/...).
2.  **Tạo sản phẩm đầu ra**: Hệ thống sẽ tự động tạo ra các sản phẩm đầu ra (văn bản, hình ảnh, âm thanh) dựa trên thông tin đầu vào và sử dụng các mô hình AI đã được chỉ định.
3.  **Lưu trữ vào Google Drive**: Các sản phẩm đầu ra sau khi được tạo sẽ được lưu trữ một cách có hệ thống vào một thư mục cụ thể trên Google Drive.
4.  **Thông báo hoàn thành tác vụ**: Khi một tác vụ hoàn thành (thành công hoặc thất bại), hệ thống sẽ tự động gửi email và thông báo qua Slack để cập nhật trạng thái.
5.  **Ghi log chi tiết**: Chi tiết về trạng thái (thành công/thất bại) của mỗi tác vụ sẽ được ghi lại vào một cơ sở dữ liệu SQLite cục bộ.
6.  **Báo cáo tổng hợp hàng ngày**: Hàng ngày, hệ thống sẽ tổng hợp các ghi chép, tạo biểu đồ phân tích tỷ lệ thành công và lỗi, sau đó gửi email bản tóm tắt này cho quản trị viên.

## Công nghệ Sử dụng

Dự án này được xây dựng bằng Python và sử dụng các thư viện chính sau:

*   **Google APIs**: `gspread`, `google-api-python-client`, `google-auth`, `google-auth-oauthlib` để tương tác với Google Sheets và Google Drive.
*   **AI Model APIs**: `openai` cho tích hợp OpenAI. (Có thể mở rộng với `anthropic` cho Claude).
*   **Xử lý dữ liệu**: `pandas`, `numpy` để xử lý dữ liệu từ Google Sheets.
*   **Vẽ biểu đồ**: `matplotlib` để tạo biểu đồ báo cáo.
*   **Cơ sở dữ liệu**: `sqlite-utils` để quản lý cơ sở dữ liệu SQLite cục bộ.
*   **Thông báo**: `slack_sdk` cho Slack và `yagmail` để gửi email.
*   **Khác**: `requests`, `python-dotenv`, `Pillow`.

Xem chi tiết trong `requirements.txt`.

## Hướng dẫn Thiết lập và Thực thi

Thực hiện theo các bước sau để thiết lập và chạy dự án.

### 1. Cài đặt Python và pip

Đảm bảo bạn đã cài đặt Python (phiên bản 3.8 trở lên) và pip trên hệ thống của mình.

### 2. Clone Repository

```bash
git clone <URL_TO_YOUR_REPOSITORY>
cd <YOUR_PROJECT_DIRECTORY>
```

### 3. Cài đặt các thư viện phụ thuộc

```bash
pip install -r requirements.txt
```

### 4. Thiết lập Google Cloud Project

Để tương tác với Google Sheets và Google Drive, bạn cần thiết lập một dự án trên Google Cloud Platform:

1.  **Tạo dự án Google Cloud**: Nếu bạn chưa có, hãy tạo một dự án mới trên [Google Cloud Console](https://console.cloud.google.com/).
2.  **Bật APIs**: Trong dự án của bạn, vào `APIs & Services` -> `Enabled APIs & Services` và bật các API sau:
    *   `Google Sheets API`
    *   `Google Drive API`
3.  **Tạo Service Account Key**:
    *   Đi tới `IAM & Admin` -> `Service Accounts`.
    *   Tạo một tài khoản dịch vụ mới.
    *   Sau khi tạo, nhấp vào tài khoản dịch vụ đó, sau đó vào tab `Keys` -> `Add Key` -> `Create new key`.
    *   Chọn `JSON` và tải xuống tệp JSON. Đổi tên tệp này thành `service_account.json` và đặt nó vào thư mục gốc của dự án của bạn (ngang hàng với `main.py`).
    *   **Chia sẻ Google Sheet và Google Drive Folder**: Chia sẻ Google Sheet đầu vào của bạn và thư mục Google Drive nơi bạn muốn lưu trữ tài sản với email của tài khoản dịch vụ mà bạn vừa tạo (email này có trong tệp `service_account.json`).

### 5. Cấu hình `config.yaml`

Mở tệp `config.yaml` và cập nhật các giá trị placeholder với thông tin của bạn:

*   **`google_sheets`**:
    *   `spreadsheet_id`: ID của Google Sheet của bạn. Bạn có thể tìm thấy nó trong URL của Google Sheet (ví dụ: `https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID/edit`).
    *   `range_name`: Phạm vi dữ liệu trong sheet của bạn (ví dụ: `"Sheet1!A:E"`). Đảm bảo các cột `Mô tả`, `URL tài sản mẫu`, `Định dạng đầu ra mong muốn`, `Chỉ định mô hình AI` tồn tại trong sheet của bạn.
*   **`google_drive`**:
    *   `folder_id`: ID của thư mục Google Drive nơi các tệp sẽ được tải lên. Bạn có thể tìm thấy nó trong URL của thư mục Google Drive.
*   **`openai`**:
    *   `api_key`: Khóa API OpenAI của bạn.
    *   `model`: Tên mô hình OpenAI bạn muốn sử dụng (ví dụ: `"gpt-4o"`).
*   **`anthropic` (Tùy chọn)**: Nếu bạn muốn sử dụng Claude, hãy bỏ ghi chú phần này và điền `api_key` và `model` của bạn.
*   **`notifications`**:
    *   `admin_email`: Địa chỉ email của quản trị viên để nhận báo cáo và thông báo.
    *   `slack_webhook_url`: URL webhook Slack của bạn để gửi thông báo.
*   **`database`**:
    *   `path`: Đường dẫn đến tệp cơ sở dữ liệu SQLite (mặc định là `"workflow_log.db"`).

### 6. Cấu hình Email (yagmail)

Nếu bạn sử dụng Gmail, bạn cần thiết lập mật khẩu ứng dụng:

1.  Truy cập [Google Account Security](https://myaccount.google.com/security).
2.  Trong phần "Cách bạn đăng nhập vào Google", chọn "Mật khẩu ứng dụng". (Nếu bạn không thấy tùy chọn này, có thể bạn chưa bật Xác minh 2 bước.)
3.  Tạo một mật khẩu ứng dụng mới và sao chép nó.
4.  Đặt các biến môi trường sau hoặc thay đổi code trong `services/notifier.py` để truyền trực tiếp:
    ```bash
    export YAGMAIL_USER="your_gmail_address@gmail.com"
    export YAGMAIL_PASSWORD="your_app_password"
    ```
    Thay thế `your_gmail_address@gmail.com` bằng địa chỉ Gmail của bạn và `your_app_password` bằng mật khẩu ứng dụng bạn vừa tạo.

### 7. Thực thi Workflow

Sau khi tất cả các cấu hình đã hoàn tất, bạn có thể chạy workflow bằng cách thực thi tệp `main.py`:

```bash
python main.py
```

Quy trình sẽ:
1.  Đọc dữ liệu từ Google Sheet.
2.  Với mỗi hàng, gọi API AI để tạo tài sản (văn bản, hình ảnh giả, âm thanh giả).
3.  Tải tài sản đã tạo lên Google Drive.
4.  Ghi lại trạng thái vào cơ sở dữ liệu `workflow_log.db`.
5.  Gửi thông báo qua email và Slack về trạng thái của mỗi tác vụ.
6.  Sau khi xử lý tất cả các tác vụ, tạo báo cáo tổng hợp hàng ngày và gửi qua email.

### 8. Lập lịch chạy (Tùy chọn)

Để chạy quy trình tự động theo lịch trình (ví dụ: hàng ngày), bạn có thể sử dụng các công cụ như `cron` (trên Linux/macOS) hoặc Task Scheduler (trên Windows), hoặc tích hợp với các thư viện lập lịch Python như `APScheduler` (đã có trong `requirements.txt`).

Ví dụ với `cron` (Linux/macOS):

```bash
# Mở crontab để chỉnh sửa
crontab -e

# Thêm dòng sau để chạy script mỗi ngày vào lúc 2 giờ sáng
# Đảm bảo đường dẫn đến python và dự án của bạn là chính xác
0 2 * * * /usr/bin/python3 /path/to/your/project/main.py
```

Thay `/usr/bin/python3` bằng đường dẫn đến trình thông dịch Python của bạn và `/path/to/your/project/` bằng đường dẫn tuyệt đối đến thư mục dự án của bạn.
