import pyodbc
import os
import pandas as pd
from datetime import datetime
import sys

def backup_database(server, database, backup_dir, trusted_connection='yes'):
    try:
        # Kết nối tới cơ sở dữ liệu
        conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection}')
        cursor = conn.cursor()

        # Tạo tên file backup với timestamp hiện tại
        backup_file = f'{database}_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.bak'

        # Bật chế độ autocommit
        conn.autocommit = True

        # Tạo câu lệnh backup
        backup_command = f"BACKUP DATABASE {database} TO DISK='{os.path.join(backup_dir, backup_file)}' WITH INIT, FORMAT, SKIP"

        # Thực thi câu lệnh backup
        cursor.execute(backup_command)

        # Ghi lại chi tiết backup
        backup_details = {
            'database': [database],
            'backup_file': [backup_file],
            'backup_datetime': [datetime.now()]
        }
        backup_df = pd.DataFrame(data=backup_details)

        # Lưu chi tiết backup vào file CSV
        backup_details_file = os.path.join(backup_dir, 'backup_details.csv')
        backup_df.to_csv(backup_details_file, index=False)

        print(f"Backup thành công. File backup đã được tạo: {backup_file}")
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")
    finally:
        # Đóng kết nối tới cơ sở dữ liệu
        cursor.close()
        conn.close()

# Ví dụ sử dụng:
server = 'DESKTOP-BINPIL1'
database = 'Python5'
backup_dir = 'E:/TTTN/Plate_Recognize/5/backup'

backup_database(server, database, backup_dir)
print(f"Current Python executable: {sys.executable}")
