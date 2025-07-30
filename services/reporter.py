import pandas as pd
import matplotlib.pyplot as plt
import os
from services.logger import get_tasks_for_reporting
from services.notifier import send_email_notification

def generate_and_send_daily_report(db_path, admin_email):
    tasks = get_tasks_for_reporting(db_path)
    if not tasks:
        print("No tasks to report for today.")
        return

    df = pd.DataFrame(tasks)

    # Calculate success and failure rates
    success_count = df[df['status'] == 'succeeded'].shape[0]
    failure_count = df[df['status'] == 'failed'].shape[0]
    total_tasks = success_count + failure_count

    if total_tasks == 0:
        print("No completed tasks to report.")
        return

    success_rate = (success_count / total_tasks) * 100
    failure_rate = (failure_count / total_tasks) * 100

    # Create a summary report text
    report_summary = f"""
    Báo cáo hàng ngày về Quy trình tự động hóa sản phẩm
    Ngày: {pd.Timestamp.today().strftime('%Y-%m-%d')}

    Tổng số tác vụ đã hoàn thành: {total_tasks}
    Số tác vụ thành công: {success_count} ({success_rate:.2f}%)
    Số tác vụ thất bại: {failure_count} ({failure_rate:.2f}%)

    Chi tiết các tác vụ thất bại:
    """

    failed_tasks_details = df[df['status'] == 'failed']
    if not failed_tasks_details.empty:
        for index, row in failed_tasks_details.iterrows():
            report_summary += f"- Task ID: {row['id']}, Mô tả: {row['input_data']}, Lỗi: {row['error_message']}
"
    else:
        report_summary += "Không có tác vụ thất bại nào.
"

    # Generate a pie chart for success/failure rates
    labels = ['Thành công', 'Thất bại']
    sizes = [success_count, failure_count]
    colors = ['#4CAF50', '#F44336'] # Green for success, Red for failure
    explode = (0.1, 0) if failure_count > 0 else (0, 0)  # Explode the 'Thất bại' slice if there are failures

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Tỷ lệ thành công và thất bại của tác vụ')

    chart_path = "daily_report_chart.png"
    plt.savefig(chart_path)
    plt.close(fig1)

    # Send the report via email
    send_email_notification(
        admin_email,
        f"Báo cáo hàng ngày về Quy trình tự động hóa - {pd.Timestamp.today().strftime('%Y-%m-%d')}",
        report_summary
    )
    print(f"Daily report sent to {admin_email}")

    # Clean up the chart file
    if os.path.exists(chart_path):
        os.remove(chart_path)
