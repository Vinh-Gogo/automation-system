import yagmail
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def send_email_notification(to_email, subject, body):
    try:
        # Ensure you have configured yagmail, e.g., by setting environment variables
        # YAGMAIL_USER and YAGMAIL_PASSWORD, or by passing credentials directly.
        # For Gmail, you might need to generate an app password.
        yag = yagmail.SMTP(os.environ.get("YAGMAIL_USER"), os.environ.get("YAGMAIL_PASSWORD"))
        yag.send(to=to_email, subject=subject, contents=body)
        print(f"Email notification sent to {to_email} with subject: {subject}")
    except Exception as e:
        print(f"Error sending email notification to {to_email}: {e}")

def send_slack_notification(webhook_url, message):
    try:
        # The WebClient can also be initialized with a token for more complex interactions,
        # but for webhooks, directly using requests might be simpler or a custom WebClient init.
        # For basic webhook, a direct POST request is often sufficient.
        import requests
        response = requests.post(webhook_url, json={'text': message})
        response.raise_for_status()
        print(f"Slack notification sent: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending Slack notification: {e}")
