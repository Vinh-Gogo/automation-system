from services import sheet_reader
from services import asset_generator
from services import uploader
from services import notifier
from services import logger
from services import reporter
import pandas as pd
import yaml
import os

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

def run_workflow():
    config = load_config()
    db_path = config['database']['path']
    logger.init_db(db_path)

    # 1. Đọc dữ liệu từ Google Sheets
    print("Đang đọc dữ liệu từ Google Sheets...")
    sheet_data = sheet_reader.read_sheet(config['google_sheets']['spreadsheet_id'], config['google_sheets']['range_name'])
    
    if sheet_data.empty:
        print("Không tìm thấy dữ liệu trong Google Sheet. Đang thoát quy trình.")
        return

    for index, row in sheet_data.iterrows():
        task_id = logger.log_task_start(row.to_dict())
        try:
            description = row['Mô tả']
            sample_url = row['URL tài sản mẫu']
            output_format = row['Định dạng đầu ra mong muốn']
            ai_model = row['Chỉ định mô hình AI']

            print(f"Đang xử lý tác vụ {task_id}: Mô tả='{description}', Định dạng='{output_format}'")

            # 2. Tạo tài sản
            generated_asset_path = asset_generator.generate_asset(description, sample_url, output_format, ai_model, config)
            print(f"Đã tạo tài sản: {generated_asset_path}")

            # 3. Tải tài sản lên Google Drive
            drive_folder_id = config['google_drive']['folder_id']
            uploaded_file_url = uploader.upload_file_to_drive(generated_asset_path, drive_folder_id)
            print(f"Đã tải tài sản lên Google Drive: {uploaded_file_url}")

            # Cập nhật trạng thái tác vụ trong DB
            logger.log_task_success(task_id, generated_asset_path, uploaded_file_url)

            # 4. Gửi thông báo
            notifier.send_email_notification(
                config['notifications']['admin_email'],
                f"Tác vụ hoàn thành thành công: {task_id}",
                f"Sản phẩm đã được tạo và tải lên Google Drive: {uploaded_file_url}"
            )
            notifier.send_slack_notification(
                config['notifications']['slack_webhook_url'],
                f"✅ Tác vụ {task_id} hoàn thành thành công! URL: {uploaded_file_url}"
            )

        except Exception as e:
            print(f"Lỗi khi xử lý tác vụ {task_id}: {e}")
            logger.log_task_failure(task_id, str(e))
            notifier.send_email_notification(
                config['notifications']['admin_email'],
                f"Tác vụ thất bại: {task_id}",
                f"Đã xảy ra lỗi khi xử lý tác vụ {task_id}: {e}"
            )
            notifier.send_slack_notification(
                config['notifications']['slack_webhook_url'],
                f"❌ Tác vụ {task_id} thất bại: {e}"
            )
        finally:
            # Dọn dẹp tệp tài sản đã tạo cục bộ
            if 'generated_asset_path' in locals() and os.path.exists(generated_asset_path):
                os.remove(generated_asset_path)
                print(f"Đã dọn dẹp tệp tài sản cục bộ: {generated_asset_path}")

    # 5. Tạo và gửi báo cáo hàng ngày
    print("Đang tạo báo cáo hàng ngày...")
    reporter.generate_and_send_daily_report(db_path, config['notifications']['admin_email'])
    print("Quy trình đã hoàn tất.")

if __name__ == "__main__":
    run_workflow()
