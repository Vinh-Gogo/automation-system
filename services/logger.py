import sqlite_utils
import datetime
import json

def init_db(db_path):
    db = sqlite_utils.Database(db_path)
    if "tasks" not in db.table_names():
        db["tasks"].create(
            {
                "id": int,
                "start_time": str,
                "end_time": str,
                "status": str,
                "input_data": str,
                "generated_asset_path": str,
                "uploaded_file_url": str,
                "error_message": str,
            },
            pk="id",
        )
        # Kích hoạt tìm kiếm toàn văn cho các cột input_data và error_message
        db["tasks"].enable_fts(["input_data", "error_message"])
    return db

def log_task_start(input_data, db_path="workflow_log.db"):
    db = sqlite_utils.Database(db_path)
    task = {
        "start_time": datetime.datetime.now().isoformat(),
        "status": "started",
        "input_data": json.dumps(input_data),
    }
    # Chèn một tác vụ mới và trả về ID của nó
    task_id = db["tasks"].insert(task, alter=True, pk="id", rowid=True)
    return task_id

def log_task_success(task_id, generated_asset_path, uploaded_file_url, db_path="workflow_log.db"):
    db = sqlite_utils.Database(db_path)
    # Cập nhật trạng thái tác vụ thành công
    db["tasks"].update(
        task_id,
        {
            "end_time": datetime.datetime.now().isoformat(),
            "status": "succeeded",
            "generated_asset_path": generated_asset_path,
            "uploaded_file_url": uploaded_file_url,
        },
    )

def log_task_failure(task_id, error_message, db_path="workflow_log.db"):
    db = sqlite_utils.Database(db_path)
    # Cập nhật trạng thái tác vụ thất bại
    db["tasks"].update(
        task_id,
        {
            "end_time": datetime.datetime.now().isoformat(),
            "status": "failed",
            "error_message": error_message,
        },
    )

def get_tasks_for_reporting(db_path="workflow_log.db"):
    db = sqlite_utils.Database(db_path)
    # Lấy tất cả các tác vụ bắt đầu trong ngày hiện tại
    return list(db.query("SELECT * FROM tasks WHERE DATE(start_time) = DATE('now', 'localtime')"))
