import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc
import os


def restore_data(backup_file):
    server = 'DESKTOP-BINPIL1'
    database = 'RFID1'
    backup_dir = 'E:/TTTN/GUI TEST/Qlybaixe/backup'

    try:
        # Kết nối tới cơ sở dữ liệu
        conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE=master;Trusted_Connection=yes')
        cursor = conn.cursor()

        # Tạo câu lệnh restore
        restore_command = f"RESTORE DATABASE {database} FROM DISK='{os.path.join(backup_dir, backup_file)}' WITH REPLACE"

        # Thực thi câu lệnh restore
        cursor.execute(restore_command)
        conn.commit()  # Commit thay đổi

        print(f"Khôi phục dữ liệu thành công từ file: {backup_file}")
        messagebox.showinfo("Thông báo", f"Đã khôi phục dữ liệu từ file {backup_file} vào cơ sở dữ liệu {database}.")
    except pyodbc.Error as e:
        error_message = str(e)
        if '4060' in error_message:  # Kiểm tra lỗi đăng nhập
            messagebox.showerror("Lỗi", "Không thể kết nối đến cơ sở dữ liệu. Vui lòng kiểm tra cài đặt SQL Server.")
        else:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra trong quá trình khôi phục dữ liệu: {error_message}")
        print("PyODBC Error:", e)
    except Exception as e:
        print(f"Có lỗi xảy ra trong quá trình khôi phục dữ liệu: {e}")
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra trong quá trình khôi phục dữ liệu: {e}")
        print("Exception:", e)
    finally:
        try:
            # Đóng kết nối tới cơ sở dữ liệu
            cursor.close()
            conn.close()
        except NameError:
            pass  # Tránh lỗi khi biến cursor không được khởi tạo


def main():
    def on_restore():
        selected_backup = backup_combobox.get()
        if selected_backup:
            restore_data(selected_backup)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một tệp backup để khôi phục.")

    # Tạo cửa sổ
    root = tk.Tk()
    root.title("Khôi phục dữ liệu")

    # Tạo một combobox để chọn tệp backup
    backup_combobox = ttk.Combobox(root, state="readonly", width=40)
    backup_combobox.pack(pady=10)

    # Tìm tệp backup trong thư mục
    backup_dir = 'E:/TTTN/GUI TEST/Qlybaixe/backup'
    backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.bak')]
    if backup_files:
        backup_combobox['values'] = backup_files
        backup_combobox.current(0)  # Chọn tệp backup đầu tiên mặc định

    # Tạo một button để khôi phục dữ liệu
    restore_button = tk.Button(root, text="Khôi phục dữ liệu", command=on_restore)
    restore_button.pack(pady=10)

    # Hiển thị cửa sổ
    root.mainloop()


if __name__ == "__main__":
    main()
