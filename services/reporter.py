import pandas as pd
import matplotlib.pyplot as plt
import os
from services.logger import get_tasks_for_reporting
from services.notifier import send_email_notification

def generate_and_send_daily_report(db_path, admin_email):
    tasks = get_tasks_for_reporting(db_path)
    if not tasks:
        print("Không có tác vụ nào để báo cáo cho hôm nay.")
        return

    df = pd.DataFrame(tasks)

    # Tính toán tỷ lệ thành công và thất bại
    success_count = df[df['status'] == 'succeeded'].shape[0]
    failure_count = df[df['status'] == 'failed'].shape[0]
    total_tasks = success_count + failure_count

    if total_tasks == 0:
        print("Không có tác vụ hoàn thành để báo cáo.")
        return

    success_rate = (success_count / total_tasks) * 100
    failure_rate = (failure_count / total_tasks) * 100

    # Tạo văn bản báo cáo tóm tắt
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

    # Tạo biểu đồ hình tròn cho tỷ lệ thành công/thất bại
    labels = ['Thành công', 'Thất bại']
    sizes = [success_count, failure_count]
    colors = ['#4CAF50', '#F44336'] # Xanh lá cây cho thành công, Đỏ cho thất bại
    explode = (0.1, 0) if failure_count > 0 else (0, 0)  # Tách lát 'Thất bại' ra nếu có lỗi

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Tỷ lệ khung hình bằng nhau đảm bảo biểu đồ được vẽ dưới dạng hình tròn.
    plt.title('Tỷ lệ thành công và thất bại của tác vụ')

    chart_path = "daily_report_chart.png"
    plt.savefig(chart_path)
    plt.close(fig1)

    # Gửi báo cáo qua email
    send_email_notification(
        admin_email,
        f"Báo cáo hàng ngày về Quy trình tự động hóa - {pd.Timestamp.today().strftime('%Y-%m-%d')}",
        report_summary
    )
    print(f"Báo cáo hàng ngày đã được gửi đến {admin_email}")

    # Dọn dẹp tệp biểu đồ
    if os.path.exists(chart_path):
        os.remove(chart_path)
