import yagmail
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def send_email_notification(to_email, subject, body):
    try:
        # Đảm bảo bạn đã cấu hình yagmail, ví dụ: bằng cách đặt biến môi trường
        # YAGMAIL_USER và YAGMAIL_PASSWORD, hoặc bằng cách truyền trực tiếp thông tin xác thực.
        # Đối với Gmail, bạn có thể cần tạo mật khẩu ứng dụng.
        yag = yagmail.SMTP(os.environ.get("YAGMAIL_USER"), os.environ.get("YAGMAIL_PASSWORD"))
        yag.send(to=to_email, subject=subject, contents=body)
        print(f"Thông báo email đã được gửi đến {to_email} với chủ đề: {subject}")
    except Exception as e:
        print(f"Lỗi khi gửi thông báo email đến {to_email}: {e}")

def send_slack_notification(webhook_url, message):
    try:
        # WebClient cũng có thể được khởi tạo bằng một token cho các tương tác phức tạp hơn,
        # nhưng đối với webhook, việc sử dụng trực tiếp requests có thể đơn giản hơn hoặc khởi tạo WebClient tùy chỉnh.
        # Đối với webhook cơ bản, yêu cầu POST trực tiếp thường là đủ.
        import requests
        response = requests.post(webhook_url, json={'text': message})
        response.raise_for_status()
        print(f"Thông báo Slack đã được gửi: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gửi thông báo Slack: {e}")
