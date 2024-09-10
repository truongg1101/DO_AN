import tkinter as tk
from tkinter import ttk,messagebox,simpledialog
import Ravao_cudan
import Qly_baixe
import Thke_xera_anh
import Thke_xevao_anh
import Qly_thexe_anh
import readRFID_anh
import Qly_bienso_anh
import picture
import pyodbc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import os

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-BINPIL1;DATABASE=Python5;Trusted_Connection=yes;')
cursor = conn.cursor()

def main_function():
    def doSomething():
        print("Đã chọn mục")

    def confirm_exit():
        # Hiện hộp thoại cảnh báo
        result = messagebox.askquestion("Xác nhận", "Bạn có muốn thoát không ?")
        if result == 'yes':
            root.destroy()   
        
    frame_created_xeravao = False
    frame_xeravao = None

    frame_created_Qly_bienso = False
    frame_Qly_bienso = None

    frame_created_Qly_baixe = False
    frame_Qly_baixe = None

    frame_created_Thke_xevao = False
    frame_Thke_xevao = None

    frame_created_Thke_xera = False
    frame_Thke_xera = None
    
    frame_created_Qly_thexe = False
    frame_Qly_thexe = None
    
    frame_created_readRFID = False
    frame_readRFID = None

    def show_hethong_xeravao():
        nonlocal frame_created_Qly_bienso, frame_Qly_bienso, frame_created_xeravao, frame_xeravao, frame_created_Qly_baixe, frame_Qly_baixe, frame_created_Thke_xevao, frame_Thke_xevao, frame_created_Thke_xera, frame_Thke_xera, frame_created_Qly_thexe, frame_Qly_thexe, frame_created_readRFID, frame_readRFID
        if not frame_created_xeravao:
            
            frame_xeravao = Ravao_cudan.create_gui(root)
            frame_created_xeravao = True
        else:
            frame_xeravao.pack(fill=tk.BOTH, expand=True)
            
        if frame_created_Qly_baixe:
            frame_Qly_baixe.pack_forget()
        if frame_created_Qly_bienso:
            frame_Qly_bienso.pack_forget()
        if frame_created_Thke_xevao:
            frame_Thke_xevao.pack_forget()
        if frame_created_Thke_xera:
            frame_Thke_xera.pack_forget()
        if frame_created_Qly_thexe:
            frame_Qly_thexe.pack_forget()
        if frame_created_readRFID:
            frame_readRFID.pack_forget()

    def show_Qly_bienso():
        nonlocal frame_created_Qly_bienso, frame_Qly_bienso, frame_created_xeravao, frame_xeravao, frame_created_Qly_baixe, frame_Qly_baixe, frame_created_Thke_xevao, frame_Thke_xevao, frame_created_Thke_xera, frame_Thke_xera,frame_created_Qly_thexe, frame_Qly_thexe, frame_created_readRFID, frame_readRFID
        
        if not frame_created_Qly_bienso:
            frame_Qly_bienso = Qly_bienso_anh.createGUI(root)
            frame_created_Qly_bienso = True
        else:
            frame_Qly_bienso.pack(fill=tk.BOTH, expand=True)
            
        if frame_created_xeravao:
            frame_xeravao.pack_forget()
        if frame_created_Qly_baixe:
            frame_Qly_baixe.pack_forget()
        if frame_created_Thke_xevao:
            frame_Thke_xevao.pack_forget()
        if frame_created_Thke_xera:
            frame_Thke_xera.pack_forget()
        if frame_created_Qly_thexe:
            frame_Qly_thexe.pack_forget()
        if frame_created_readRFID:
            frame_readRFID.pack_forget()

    def show_Qly_baixe():
        nonlocal frame_created_Qly_baixe, frame_Qly_baixe, frame_created_xeravao, frame_xeravao, frame_created_Qly_bienso, frame_Qly_bienso, frame_created_Thke_xevao, frame_Thke_xevao, frame_created_Thke_xera, frame_Thke_xera, frame_created_Qly_thexe, frame_Qly_thexe, frame_created_readRFID, frame_readRFID
        
        if not frame_created_Qly_baixe:
            frame_Qly_baixe = Qly_baixe.create_gui(root)
            frame_created_Qly_baixe = True
        else:
            frame_Qly_baixe.pack(fill=tk.BOTH, expand=True)
            
        if frame_created_xeravao:
            frame_xeravao.pack_forget()
        if frame_created_Qly_bienso:
            frame_Qly_bienso.pack_forget()
        if frame_created_Thke_xevao:
            frame_Thke_xevao.pack_forget()
        if frame_created_Thke_xera:
            frame_Thke_xera.pack_forget()
        if frame_created_Qly_thexe:
            frame_Qly_thexe.pack_forget()
        if frame_created_readRFID:
            frame_readRFID.pack_forget()

    def show_Thke_xevao():
        nonlocal frame_created_Qly_baixe, frame_Qly_baixe, frame_created_xeravao, frame_xeravao, frame_created_Qly_bienso, frame_Qly_bienso, frame_created_Thke_xevao, frame_Thke_xevao, frame_created_Thke_xera, frame_Thke_xera, frame_created_Qly_thexe, frame_Qly_thexe, frame_created_readRFID, frame_readRFID
        if not frame_created_Thke_xevao:
            frame_Thke_xevao = Thke_xevao_anh.create_gui(root)
            frame_created_Thke_xevao = True
        else:
            frame_Thke_xevao.pack(fill=tk.BOTH, expand=True)
            
        if frame_created_xeravao:
           frame_xeravao.pack_forget()
        if frame_created_Qly_bienso:
            frame_Qly_bienso.pack_forget()
        if frame_created_Qly_baixe:
            frame_Qly_baixe.pack_forget()
        if frame_created_Thke_xera:
            frame_Thke_xera.pack_forget()
        if frame_created_Qly_thexe:
            frame_Qly_thexe.pack_forget()
        if frame_created_readRFID:
            frame_readRFID.pack_forget()
            
    def show_Thke_xera():
        nonlocal frame_created_Qly_baixe, frame_Qly_baixe, frame_created_xeravao, frame_xeravao, frame_created_Qly_bienso, frame_Qly_bienso, frame_created_Thke_xevao, frame_Thke_xevao, frame_created_Thke_xera, frame_Thke_xera, frame_created_Qly_thexe, frame_Qly_thexe, frame_created_readRFID, frame_readRFID
        if not frame_created_Thke_xera:
            frame_Thke_xera = Thke_xera_anh.create_gui(root)
            frame_created_Thke_xera = True
        else:
            frame_Thke_xera.pack(fill=tk.BOTH, expand=True)
            
        if frame_created_xeravao:
            frame_xeravao.pack_forget()
        if frame_created_Qly_bienso:
            frame_Qly_bienso.pack_forget()
        if frame_created_Qly_baixe:
            frame_Qly_baixe.pack_forget()
        if frame_created_Thke_xevao:
            frame_Thke_xevao.pack_forget()
        if frame_created_Qly_thexe:
            frame_Qly_thexe.pack_forget()
        if frame_created_readRFID:
            frame_readRFID.pack_forget()
            
    def show_Qly_thexe():
        nonlocal frame_created_Qly_baixe, frame_Qly_baixe, frame_created_xeravao, frame_xeravao, frame_created_Qly_bienso, frame_Qly_bienso, frame_created_Thke_xevao, frame_Thke_xevao, frame_created_Thke_xera, frame_Thke_xera, frame_created_Qly_thexe, frame_Qly_thexe, frame_created_readRFID, frame_readRFID
        if not frame_created_Qly_thexe:
            frame_Qly_thexe = Qly_thexe_anh.create_gui(root)
            frame_created_Qly_thexe = True
        else:
            frame_Qly_thexe.pack(fill=tk.BOTH, expand = True)
        
        if frame_created_xeravao:
            frame_xeravao.pack_forget()
        if frame_created_Qly_bienso:
            frame_Qly_bienso.pack_forget()
        if frame_created_Qly_baixe:
            frame_Qly_baixe.pack_forget()
        if frame_created_Thke_xevao:
            frame_Thke_xevao.pack_forget()
        if frame_created_Thke_xera:
            frame_Thke_xera.pack_forget()
        if frame_created_readRFID:
            frame_readRFID.pack_forget()
            
    def show_readRFID():
        nonlocal frame_created_Qly_baixe, frame_Qly_baixe, frame_created_xeravao, frame_xeravao, frame_created_Qly_bienso, frame_Qly_bienso, frame_created_Thke_xevao, frame_Thke_xevao, frame_created_Thke_xera, frame_Thke_xera, frame_created_Qly_thexe, frame_Qly_thexe, frame_created_readRFID, frame_readRFID
        if not frame_created_readRFID:
            frame_readRFID = readRFID_anh.create_gui(root)
            frame_created_readRFID = True
        else:
            frame_readRFID.pack(fill=tk.BOTH, expand = True)
        
        if frame_created_xeravao:
            frame_xeravao.pack_forget()
        if frame_created_Qly_bienso:
            frame_Qly_bienso.pack_forget()
        if frame_created_Qly_baixe:
            frame_Qly_baixe.pack_forget()
        if frame_created_Thke_xevao:
            frame_Thke_xevao.pack_forget()
        if frame_created_Thke_xera:
            frame_Thke_xera.pack_forget()
        if frame_created_Qly_thexe:
            frame_Qly_thexe.pack_forget()            
    
    def show_account_frame():
        # Establish connection and cursor once
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAGGER\CHIEN;DATABASE=Python5;Trusted_Connection=yes;')
        cursor = conn.cursor()

        # Tạo một window mới cho mục "Tài khoản"
        account_window = tk.Toplevel(root, bg="white")
        account_window.title("Thông tin tài khoản nhân viên")
        account_window.geometry("400x400")
        
        # Tạo Treeview để hiển thị dữ liệu
        columns = ("MaTK", "taikhoan", "matkhau")
        tree = ttk.Treeview(account_window, columns=columns, show="headings", height=15)
        tree.heading("MaTK", text="Mã TK")
        tree.heading("taikhoan", text="Tài khoản")
        tree.heading("matkhau", text="Mật khẩu")
        tree.column("MaTK", width=20)
        tree.column("taikhoan", width=50)
        tree.column("matkhau", width=50)
        tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        def load_data():
            for row in tree.get_children():
                tree.delete(row)
            cursor.execute("SELECT * FROM Account")
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=(row[0], row[1], row[2]))

        def add_account():
            def save_new_account():
                taikhoan = entry_taikhoan.get()
                matkhau = entry_matkhau.get()
                
                cursor.execute("SELECT COUNT(*) FROM Account WHERE taikhoan = ?", (taikhoan,))
                result = cursor.fetchone()
                if result[0] > 0:
                    tk.messagebox.showerror("Lỗi", "Tài khoản đã tồn tại")
                    return
                
                cursor.execute("INSERT INTO Account (taikhoan, matkhau) VALUES (?, ?)", (taikhoan, matkhau))
                conn.commit()
                load_data()
                add_window.destroy()
            
            add_window = tk.Toplevel(account_window)
            add_window.title("Thêm tài khoản")
            add_window.geometry("300x200")
            
            tk.Label(add_window, text="Tài khoản:").pack(pady=5)
            entry_taikhoan = tk.Entry(add_window)
            entry_taikhoan.pack(pady=5)
            
            tk.Label(add_window, text="Mật khẩu:").pack(pady=5)
            entry_matkhau = tk.Entry(add_window)
            entry_matkhau.pack(pady=5)
            
            tk.Button(add_window, text="Lưu", command=save_new_account).pack(pady=20)
            messagebox.showinfo("Thông báo", "Thêm tài khoản thành công!")
        
        def edit_account():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Chưa chọn mục", "Vui lòng chọn tài khoản để sửa")
                return
            
            def save_edited_account():
                taikhoan = entry_taikhoan.get()
                matkhau = entry_matkhau.get()
                cursor.execute("UPDATE Account SET taikhoan = ?, matkhau = ? WHERE MaTK = ?", (taikhoan, matkhau, selected_values[0]))
                conn.commit()
                load_data()
                edit_window.destroy()
            
            selected_values = tree.item(selected_item, "values")
            edit_window = tk.Toplevel(account_window)
            edit_window.title("Sửa tài khoản")
            edit_window.geometry("300x200")
            
            tk.Label(edit_window, text="Tài khoản:").pack(pady=5)
            entry_taikhoan = tk.Entry(edit_window)
            entry_taikhoan.insert(0, selected_values[1])
            entry_taikhoan.pack(pady=5)
            
            tk.Label(edit_window, text="Mật khẩu:").pack(pady=5)
            entry_matkhau = tk.Entry(edit_window)
            entry_matkhau.insert(0, selected_values[2])
            entry_matkhau.pack(pady=5)
            
            tk.Button(edit_window, text="Lưu", command=save_edited_account).pack(pady=20)
            messagebox.showinfo("Thông báo", "Sửa tài khoản thành công!")
        
        def delete_account():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Chưa chọn mục", "Vui lòng chọn tài khoản để xóa")
                return

            selected_values = tree.item(selected_item, "values")
            
            # Hiển thị hộp thoại xác nhận xóa
            confirm = messagebox.askyesno("Xóa tài khoản", f"Bạn có chắc muốn xóa tài khoản {selected_values[1]}?")
            if confirm:
                cursor.execute("DELETE FROM Account WHERE MaTK = ?", (selected_values[0],))
                conn.commit()
                load_data()
                messagebox.showinfo("Thông báo", "Xóa tài khoản thành công!")
        
        # Tạo các nút thêm, sửa, xóa ở phía bên phải
        button_frame = tk.Frame(account_window, bg="white")
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
        
        button_width = 10
        tk.Button(button_frame, text="Thêm", width=button_width, command=add_account).pack(pady=5)
        tk.Button(button_frame, text="Sửa", width=button_width, command=edit_account).pack(pady=5)
        tk.Button(button_frame, text="Xóa", width=button_width, command=delete_account).pack(pady=5)
        
        # Configuring grid weights for better resizing
        account_window.grid_columnconfigure(0, weight=1)
        account_window.grid_rowconfigure(0, weight=1)
        
        # Load data into Treeview
        load_data()
    '''        
    def show_login_form():
        def check_credentials():
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAGGER\CHIEN;DATABASE=Python5;Trusted_Connection=yes;')
            cursor = conn.cursor()
            username = entry_username.get()
            password = entry_password.get()
            cursor.execute("SELECT COUNT(*) FROM Admin_Account WHERE taikhoanadmin = ? AND matkhau = ?", (username, password))
            if cursor.fetchone():
                login_window.destroy()
                show_account_frame()
            else:
                messagebox.showerror("Lỗi đăng nhập", "Tài khoản hoặc mật khẩu không đúng")

        login_window = tk.Toplevel(root,bg="white")
        login_window.title("Đăng nhập")
        login_window.geometry("700x200")
        login_window.resizable(False,False)
        
        # Label at the top
        tk.Label(login_window, bg="white",font=("Microsoft YeHei UI Light", 18, "bold"),text="Bạn cần đăng nhập để xem thông tin tài khoản").pack(pady=10)

        # Create a frame to hold labels and entries
        frame = tk.Frame(login_window,bg="white")
        frame.pack(pady=5)

        # Labels
        tk.Label(frame, bg="white",text="Tài khoản:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        tk.Label(frame, bg="white",text="Mật khẩu:").grid(row=1, column=0, padx=5, pady=5, sticky='e')

        # Entries
        entry_username = tk.Entry(frame,bg="white")
        entry_username.grid(row=0, column=1, padx=5, pady=5)
        entry_password = tk.Entry(frame, show="*",bg="white")
        entry_password.grid(row=1, column=1, padx=5, pady=5)

        # Login button
        tk.Button(login_window, text="Đăng nhập",font=("Microsoft YeHei UI Light", 13, "bold") ,bg='#57a1f8', fg='white', border=0,command=check_credentials).pack(pady=10)
 '''   
    def get_statistics(query, params):
        # Kết nối tới SQL Server
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAGGER\CHIEN;DATABASE=Python5;Trusted_Connection=yes;')
        cursor = conn.cursor()
        
        cursor.execute(query, params)
        result = cursor.fetchone()[0]

        conn.close()
        return result

    tree_data = []  # Khai báo tree_data là biến toàn cục

    def show_dashboard_frame(event):
        global tree_data  # Sử dụng biến tree_data toàn cục

        # Tạo giao diện Tkinter
        dash_window = tk.Toplevel(root, bg="white")
        dash_window.title("Dashboard")
        dash_window.geometry("1920x1080")

        frame = tk.Frame(dash_window, bg="white")
        frame.pack(padx=10, pady=10)

        # Chọn khoảng thời gian
        options = ["Hôm Nay", "Tuần Này", "Tháng Này", "Năm Nay"]
        selected_option = tk.StringVar(value="Hôm Nay")

        tk.Label(frame, text="Chọn Khoảng Thời Gian:", font=("Helvetica", 12), bg="white").grid(row=0, column=0, pady=10, sticky="e")
        option_menu = tk.OptionMenu(frame, selected_option, *options, command=lambda _: update_statistics())
        option_menu.grid(row=0, column=1, pady=10, sticky="w")
        
        # Hiển thị thông tin thống kê
        tree = ttk.Treeview(frame, columns=("Thời Gian", "Xe Vào", "Xe Ra"), show="headings")
        tree.heading("Thời Gian", text="Thời Gian")
        tree.heading("Xe Vào", text="Xe Vào")
        tree.heading("Xe Ra", text="Xe Ra")
        tree.grid(row=1, column=0, columnspan=2, pady=10)

        # Tạo nút hiển thị biểu đồ
        def show_chart(data):
            # Xóa biểu đồ cũ nếu có
            for widget in frame.winfo_children():
                if isinstance(widget, FigureCanvasTkAgg):
                    widget.get_tk_widget().destroy()
                
            # Tạo biểu đồ mới
            fig, ax = plt.subplots(figsize=(14, 5))  # Đặt kích thước cho biểu đồ
            labels = [item[0] for item in data]
            xe_vao_values = [item[1] for item in data]
            xe_ra_values = [item[2] for item in data]

            bar_width = 0.35
            index = range(len(labels))

            ax.bar(index, xe_vao_values, bar_width, label='Xe Vào', color='green')
            ax.bar([i + bar_width for i in index], xe_ra_values, bar_width, label='Xe Ra', color='red', alpha=0.7)
            ax.set_ylabel('Số lượng')
            ax.set_title('Thống Kê Xe')
            ax.set_xticks([i + bar_width / 2 for i in index])  # Đặt vị trí của nhãn trục x
            ax.set_xticklabels(labels, rotation=30, ha='right')
            ax.legend()

            # Nhúng biểu đồ vào Tkinter
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, pady=10)

        chart_button = tk.Button(frame, text="Hiển Thị Biểu Đồ", command=lambda: show_chart(tree_data))
        chart_button.grid(row=2, column=0, columnspan=2, pady=0) 

        def update_statistics():
            global tree_data  # Sử dụng biến tree_data ở ngoài hàm update_statistics

            period = selected_option.get()

            if period == "Hôm Nay":
                today_str = datetime.now().strftime('%Y-%m-%d')
                # Lấy số lượng xe vào, ra theo từng giờ trong ngày
                tree_data = []
                for i in range(24):
                    start_time = f'{i:02d}:00:00'
                    end_time = f'{i:02d}:59:59'
                    xe_vao_query = "SELECT COUNT(*) FROM XeVao WHERE CONVERT(date, ThoiGianVao) = ? AND CAST(ThoiGianVao AS time) BETWEEN ? AND ?"
                    xe_ra_query = "SELECT COUNT(*) FROM XeRa WHERE CONVERT(date, ThoiGianRa) = ? AND CAST(ThoiGianRa AS time) BETWEEN ? AND ?"
                    xe_vao_count = get_statistics(xe_vao_query, [today_str, start_time, end_time])
                    xe_ra_count = get_statistics(xe_ra_query, [today_str, start_time, end_time])
                    tree_data.append((f"{i:02d}:00-{i+1:02d}:00", xe_vao_count, xe_ra_count))

            elif period == "Tuần Này":
                today = datetime.now()
                start_of_week = today - timedelta(days=today.weekday())
                tree_data = []
                for i in range(7):
                    day = start_of_week + timedelta(days=i)
                    day_str = day.strftime('%Y-%m-%d')
                    xe_vao_query = "SELECT COUNT(*) FROM XeVao WHERE CONVERT(date, ThoiGianVao) = ?"
                    xe_ra_query = "SELECT COUNT(*) FROM XeRa WHERE CONVERT(date, ThoiGianRa) = ?"
                    xe_vao_count = get_statistics(xe_vao_query, [day_str])
                    xe_ra_count = get_statistics(xe_ra_query, [day_str])
                    tree_data.append((day.strftime('%A'), xe_vao_count, xe_ra_count))

            elif period == "Tháng Này":
                today = datetime.now()
                start_of_month = today.replace(day=1)
                end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                tree_data = []
                week_count = (end_of_month.day + start_of_month.weekday() - 1) // 7 + 1  # Tính số tuần trong tháng
                for i in range(week_count):
                    start_of_week = start_of_month + timedelta(days=i*7 - start_of_month.weekday())
                    end_of_week = start_of_week + timedelta(days=6)
                    start_of_week_str = start_of_week.strftime('%Y-%m-%d')
                    end_of_week_str = end_of_week.strftime('%Y-%m-%d')
                    xe_vao_query = "SELECT COUNT(*) FROM XeVao WHERE CONVERT(date, ThoiGianVao) BETWEEN ? AND ?"
                    xe_ra_query = "SELECT COUNT(*) FROM XeRa WHERE CONVERT(date, ThoiGianRa) BETWEEN ? AND ?"
                    xe_vao_count = get_statistics(xe_vao_query, [start_of_week_str, end_of_week_str])
                    xe_ra_count = get_statistics(xe_ra_query, [start_of_week_str, end_of_week_str])
                    tree_data.append((f'Tuần {i+1}', xe_vao_count, xe_ra_count))

            elif period == "Năm Nay":
                today = datetime.now()
                start_of_year = today.replace(month=1, day=1)
                tree_data = []
                for i in range(12):
                    month = start_of_year.replace(month=i+1)
                    month_str = month.strftime('%Y-%m')
                    xe_vao_query = "SELECT COUNT(*) FROM XeVao WHERE CONVERT(date, ThoiGianVao) LIKE ?"
                    xe_ra_query = "SELECT COUNT(*) FROM XeRa WHERE CONVERT(date, ThoiGianRa) LIKE ?"
                    xe_vao_count = get_statistics(xe_vao_query, [month_str + '%'])
                    xe_ra_count = get_statistics(xe_ra_query, [month_str + '%'])
                    tree_data.append((month.strftime('%B'), xe_vao_count, xe_ra_count))

            # Cập nhật treeview
            for item in tree.get_children():
                tree.delete(item)
            for row in tree_data:
                tree.insert("", "end", values=row)
    
        update_statistics()  # Cập nhật thống kê ban đầu
        
    def dashboard_baixe(event):
        global tree_data_baixe  # Sử dụng biến tree_data_baixe toàn cục

        # Tạo giao diện Tkinter
        dash_window = tk.Toplevel(root, bg="white")
        dash_window.title("Dashboard - Số Lượng Xe Trong Bãi")
        dash_window.geometry("1920x1080")

        frame = tk.Frame(dash_window, bg="white")
        frame.pack(padx=10, pady=10)

        # Chọn khoảng thời gian
        options = ["Hôm Nay", "Tuần Này", "Tháng Này", "Năm Nay"]
        selected_option = tk.StringVar(value="Hôm Nay")

        tk.Label(frame, text="Chọn Khoảng Thời Gian:", font=("Helvetica", 12), bg="white").grid(row=0, column=0, pady=10, sticky="e")
        option_menu = tk.OptionMenu(frame, selected_option, *options, command=lambda _: update_statistics_baixe())
        option_menu.grid(row=0, column=1, pady=10, sticky="w")

        # Hiển thị thông tin thống kê
        tree_baixe = ttk.Treeview(frame, columns=("Thời Gian", "Số lượng xe trong bãi"), show="headings")
        tree_baixe.heading("Thời Gian", text="Thời Gian")
        tree_baixe.heading("Số lượng xe trong bãi", text="Số lượng xe trong bãi")
        tree_baixe.grid(row=1, column=0, columnspan=2, pady=10)

        # Tạo nút hiển thị biểu đồ
        def show_chart_baixe(data):
            # Xóa biểu đồ cũ nếu có
            for widget in frame.winfo_children():
                if isinstance(widget, FigureCanvasTkAgg):
                    widget.get_tk_widget().destroy()

            # Tạo biểu đồ mới
            fig, ax = plt.subplots(figsize=(14, 5))  # Đặt kích thước cho biểu đồ
            labels = [item[0] for item in data]
            xe_trong_bai_values = [item[1] for item in data]

            bar_width = 0.35
            index = range(len(labels))

            ax.bar(index, xe_trong_bai_values, bar_width, label='Xe Trong Bãi', color='blue')
            ax.set_ylabel('Số lượng')
            ax.set_title('Thống Kê Xe Trong Bãi')
            ax.set_xticks(index)
            ax.set_xticklabels(labels, rotation=30, ha='right')
            ax.legend()

            # Nhúng biểu đồ vào Tkinter
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, pady=10)

        chart_button = tk.Button(frame, text="Hiển Thị Biểu Đồ", command=lambda: show_chart_baixe(tree_data_baixe))
        chart_button.grid(row=2, column=0, columnspan=2, pady=0)

        def update_statistics_baixe():
            global tree_data_baixe  # Sử dụng biến tree_data_baixe ở ngoài hàm update_statistics_baixe

            period = selected_option.get()

            if period == "Hôm Nay":
                today_str = datetime.now().strftime('%Y-%m-%d')
                tree_data_baixe = []
                for i in range(24):
                    start_time = f'{i:02d}:00:00'
                    end_time = f'{i:02d}:59:59'
                    xe_vao_query = "SELECT COUNT(*) FROM XeVao WHERE CONVERT(date, ThoiGianVao) = ? AND CAST(ThoiGianVao AS time) BETWEEN ? AND ?"
                    xe_ra_query = "SELECT COUNT(*) FROM XeRa WHERE CONVERT(date, ThoiGianRa) = ? AND CAST(ThoiGianRa AS time) BETWEEN ? AND ?"
                    xe_vao_count = get_statistics(xe_vao_query, [today_str, start_time, end_time])
                    xe_ra_count = get_statistics(xe_ra_query, [today_str, start_time, end_time])
                    xe_trong_bai = xe_vao_count - xe_ra_count
                    tree_data_baixe.append((f"{i:02d}:00-{i+1:02d}:00", xe_trong_bai))

            elif period == "Tuần Này":
                today = datetime.now()
                start_of_week = today - timedelta(days=today.weekday())
                tree_data_baixe = []
                for i in range(7):
                    day = start_of_week + timedelta(days=i)
                    day_str = day.strftime('%Y-%m-%d')
                    xe_vao_query = "SELECT COUNT(*) FROM XeVao WHERE CONVERT(date, ThoiGianVao) = ?"
                    xe_ra_query = "SELECT COUNT(*) FROM XeRa WHERE CONVERT(date, ThoiGianRa) = ?"
                    xe_vao_count = get_statistics(xe_vao_query, [day_str])
                    xe_ra_count = get_statistics(xe_ra_query, [day_str])
                    xe_trong_bai = xe_vao_count - xe_ra_count
                    tree_data_baixe.append((day.strftime('%A'), xe_trong_bai))

            elif period == "Tháng Này":
                today = datetime.now()
                start_of_month = today.replace(day=1)
                end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                tree_data_baixe = []
                week_count = (end_of_month.day + start_of_month.weekday() - 1) // 7 + 1  # Tính số tuần trong tháng
                for i in range(week_count):
                    start_of_week = start_of_month + timedelta(days=i*7 - start_of_month.weekday())
                    end_of_week = start_of_week + timedelta(days=6)
                    start_of_week_str = start_of_week.strftime('%Y-%m-%d')
                    end_of_week_str = end_of_week.strftime('%Y-%m-%d')
                    xe_vao_query = "SELECT COUNT(*) FROM XeVao WHERE CONVERT(date, ThoiGianVao) BETWEEN ? AND ?"
                    xe_ra_query = "SELECT COUNT(*) FROM XeRa WHERE CONVERT(date, ThoiGianRa) BETWEEN ? AND ?"
                    xe_vao_count = get_statistics(xe_vao_query, [start_of_week_str, end_of_week_str])
                    xe_ra_count = get_statistics(xe_ra_query, [start_of_week_str, end_of_week_str])
                    xe_trong_bai = xe_vao_count - xe_ra_count
                    tree_data_baixe.append((f'Tuần {i+1}', xe_trong_bai))

            elif period == "Năm Nay":
                today = datetime.now()
                start_of_year = today.replace(month=1, day=1)
                tree_data_baixe = []
                for i in range(12):
                    month = start_of_year.replace(month=i+1)
                    month_str = month.strftime('%Y-%m')
                    xe_vao_query = "SELECT COUNT(*) FROM XeVao WHERE CONVERT(date, ThoiGianVao) LIKE ?"
                    xe_ra_query = "SELECT COUNT(*) FROM XeRa WHERE CONVERT(date, ThoiGianRa) LIKE ?"
                    xe_vao_count = get_statistics(xe_vao_query, [month_str + '%'])
                    xe_ra_count = get_statistics(xe_ra_query, [month_str + '%'])
                    xe_trong_bai = xe_vao_count - xe_ra_count
                    tree_data_baixe.append((month.strftime('%B'), xe_trong_bai))

            # Cập nhật treeview
            for item in tree_baixe.get_children():
                tree_baixe.delete(item)
            for row in tree_data_baixe:
                tree_baixe.insert("", "end", values=row)

        update_statistics_baixe()  # Cập nhật thống kê ban đầu

    def dashboard_card(event):
        global tree_data_card  # Sử dụng biến tree_data_card toàn cục

        # Tạo giao diện Tkinter
        dash_window = tk.Toplevel(root, bg="white")
        dash_window.title("Dashboard - Số Lượng Thẻ Ra Vào")
        dash_window.geometry("1920x1080")

        frame = tk.Frame(dash_window, bg="white")
        frame.pack(padx=10, pady=10)

        # Chọn khoảng thời gian
        options = ["Hôm Nay", "Tuần Này", "Tháng Này", "Năm Nay"]
        selected_option = tk.StringVar(value="Hôm Nay")

        tk.Label(frame, text="Chọn Khoảng Thời Gian:", font=("Helvetica", 12), bg="white").grid(row=0, column=0, pady=10, sticky="e")
        option_menu = tk.OptionMenu(frame, selected_option, *options, command=lambda _: update_statistics_card())
        option_menu.grid(row=0, column=1, pady=10, sticky="w")

        # Hiển thị thông tin thống kê
        tree_card = ttk.Treeview(frame, columns=("Thời Gian", "Thẻ Vào", "Thẻ Ra"), show="headings")
        tree_card.heading("Thời Gian", text="Thời Gian")
        tree_card.heading("Thẻ Vào", text="Thẻ Vào")
        tree_card.heading("Thẻ Ra", text="Thẻ Ra")
        tree_card.grid(row=1, column=0, columnspan=2, pady=10)

        # Tạo nút hiển thị biểu đồ
        def show_chart_card(data):
            # Xóa biểu đồ cũ nếu có
            for widget in frame.winfo_children():
                if isinstance(widget, FigureCanvasTkAgg):
                    widget.get_tk_widget().destroy()

            # Tạo biểu đồ mới
            fig, ax = plt.subplots(figsize=(14, 5))  # Đặt kích thước cho biểu đồ
            labels = [item[0] for item in data]
            card_in_values = [item[1] for item in data]
            card_out_values = [item[2] for item in data]

            bar_width = 0.35
            index = range(len(labels))

            ax.bar(index, card_in_values, bar_width, label='Thẻ Vào', color='green')
            ax.bar([i + bar_width for i in index], card_out_values, bar_width, label='Thẻ Ra', color='red', alpha=0.7)
            ax.set_ylabel('Số lượng')
            ax.set_title('Thống Kê Thẻ')
            ax.set_xticks([i + bar_width / 2 for i in index])  # Đặt vị trí của nhãn trục x
            ax.set_xticklabels(labels, rotation=30, ha='right')
            ax.legend()

            # Nhúng biểu đồ vào Tkinter
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, pady=10)

        chart_button = tk.Button(frame, text="Hiển Thị Biểu Đồ", command=lambda: show_chart_card(tree_data_card))
        chart_button.grid(row=2, column=0, columnspan=2, pady=0)

        def update_statistics_card():
            global tree_data_card  # Sử dụng biến tree_data_card ở ngoài hàm update_statistics_card

            period = selected_option.get()

            if period == "Hôm Nay":
                today_str = datetime.now().strftime('%Y-%m-%d')
                tree_data_card = []
                for i in range(24):
                    start_time = f'{i:02d}:00:00'
                    end_time = f'{i:02d}:59:59'
                    card_in_query = "SELECT COUNT(*) FROM Entry WHERE CONVERT(date, entry_time) = ? AND CAST(entry_time AS time) BETWEEN ? AND ?"
                    card_out_query = "SELECT COUNT(*) FROM OUT WHERE CONVERT(date, exit_time) = ? AND CAST(exit_time AS time) BETWEEN ? AND ?"
                    card_in_count = get_statistics(card_in_query, [today_str, start_time, end_time])
                    card_out_count = get_statistics(card_out_query, [today_str, start_time, end_time])
                    tree_data_card.append((f"{i:02d}:00-{i+1:02d}:00", card_in_count, card_out_count))

            elif period == "Tuần Này":
                today = datetime.now()
                start_of_week = today - timedelta(days=today.weekday())
                tree_data_card = []
                for i in range(7):
                    day = start_of_week + timedelta(days=i)
                    day_str = day.strftime('%Y-%m-%d')
                    card_in_query = "SELECT COUNT(*) FROM Entry WHERE CONVERT(date, entry_time) = ?"
                    card_out_query = "SELECT COUNT(*) FROM OUT WHERE CONVERT(date, exit_time) = ?"
                    card_in_count = get_statistics(card_in_query, [day_str])
                    card_out_count = get_statistics(card_out_query, [day_str])
                    tree_data_card.append((day.strftime('%A'), card_in_count, card_out_count))

            elif period == "Tháng Này":
                today = datetime.now()
                start_of_month = today.replace(day=1)
                end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                tree_data_card = []
                week_count = (end_of_month.day + start_of_month.weekday() - 1) // 7 + 1  # Tính số tuần trong tháng
                for i in range(week_count):
                    start_of_week = start_of_month + timedelta(days=i*7 - start_of_month.weekday())
                    end_of_week = start_of_week + timedelta(days=6)
                    start_of_week_str = start_of_week.strftime('%Y-%m-%d')
                    end_of_week_str = end_of_week.strftime('%Y-%m-%d')
                    card_in_query = "SELECT COUNT(*) FROM Entry WHERE CONVERT(date, entry_time) BETWEEN ? AND ?"
                    card_out_query = "SELECT COUNT(*) FROM OUT WHERE CONVERT(date, exit_time) BETWEEN ? AND ?"
                    card_in_count = get_statistics(card_in_query, [start_of_week_str, end_of_week_str])
                    card_out_count = get_statistics(card_out_query, [start_of_week_str, end_of_week_str])
                    tree_data_card.append((f'Tuần {i+1}', card_in_count, card_out_count))

            elif period == "Năm Nay":
                today = datetime.now()
                start_of_year = today.replace(month=1, day=1)
                tree_data_card = []
                for i in range(12):
                    month = start_of_year.replace(month=i+1)
                    month_str = month.strftime('%Y-%m')
                    card_in_query = "SELECT COUNT(*) FROM Entry WHERE CONVERT(date, entry_time) LIKE ?"
                    card_out_query = "SELECT COUNT(*) FROM OUT WHERE CONVERT(date, exit_time) LIKE ?"
                    card_in_count = get_statistics(card_in_query, [month_str + '%'])
                    card_out_count = get_statistics(card_out_query, [month_str + '%'])
                    tree_data_card.append((month.strftime('%B'), card_in_count, card_out_count))

            # Cập nhật treeview
            for item in tree_card.get_children():
                tree_card.delete(item)
            for row in tree_data_card:
                tree_card.insert("", "end", values=row)

        update_statistics_card()  # Cập nhật thống kê ban đầu
    
    def show_admin_frame():
        # Establish connection and cursor once
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAGGER\CHIEN;DATABASE=Python5;Trusted_Connection=yes;')
        cursor = conn.cursor()

        # Tạo một window mới cho mục "Admin Account"
        admin_window = tk.Toplevel(root, bg="white")
        admin_window.title("Thông tin tài khoản quản lý")
        admin_window.geometry("400x400")
        
        # Tạo Treeview để hiển thị dữ liệu
        columns = ("ma_admin", "taikhoanadmin", "matkhau")
        tree = ttk.Treeview(admin_window, columns=columns, show="headings", height=15)
        tree.heading("ma_admin", text="Mã Admin")
        tree.heading("taikhoanadmin", text="Tài khoản")
        tree.heading("matkhau", text="Mật khẩu")
        tree.column("ma_admin", width=20)
        tree.column("taikhoanadmin", width=50)
        tree.column("matkhau", width=50)
        tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        def load_data():
            for row in tree.get_children():
                tree.delete(row)
            cursor.execute("SELECT * FROM Admin_Account")
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=(row[0], row[1], row[2]))

        def add_admin_account():
            def save_new_admin_account():
                taikhoan = entry_taikhoan.get()
                matkhau = entry_matkhau.get()
                
                cursor.execute("SELECT COUNT(*) FROM Admin_Account WHERE taikhoanadmin = ?", (taikhoan,))
                result = cursor.fetchone()
                if result[0] > 0:
                    tk.messagebox.showerror("Lỗi", "Tài khoản đã tồn tại")
                    return
                
                cursor.execute("INSERT INTO Admin_Account (taikhoanadmin, matkhau) VALUES (?, ?)", (taikhoan, matkhau))
                conn.commit()
                load_data()
                add_window.destroy()
                messagebox.showinfo("Thông báo", "Thêm tài khoản thành công!")
            
            add_window = tk.Toplevel(admin_window)
            add_window.title("Thêm tài khoản quản lý")
            add_window.geometry("300x200")
            
            tk.Label(add_window, text="Tài khoản:").pack(pady=5)
            entry_taikhoan = tk.Entry(add_window)
            entry_taikhoan.pack(pady=5)
            
            tk.Label(add_window, text="Mật khẩu:").pack(pady=5)
            entry_matkhau = tk.Entry(add_window)
            entry_matkhau.pack(pady=5)
            
            tk.Button(add_window, text="Lưu", command=save_new_admin_account).pack(pady=20)

        def edit_admin_account():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Chưa chọn mục", "Vui lòng chọn tài khoản để sửa")
                return
            
            def save_edited_admin_account():
                taikhoan = entry_taikhoan.get()
                matkhau = entry_matkhau.get()
                cursor.execute("UPDATE Admin_Account SET taikhoanadmin = ?, matkhau = ? WHERE ma_admin = ?", (taikhoan, matkhau, selected_values[0]))
                conn.commit()
                load_data()
                edit_window.destroy()
                messagebox.showinfo("Thông báo", "Sửa tài khoản thành công!")
            
            selected_values = tree.item(selected_item, "values")
            edit_window = tk.Toplevel(admin_window)
            edit_window.title("Sửa tài khoản quản lý")
            edit_window.geometry("300x200")
            
            tk.Label(edit_window, text="Tài khoản:").pack(pady=5)
            entry_taikhoan = tk.Entry(edit_window)
            entry_taikhoan.insert(0, selected_values[1])
            entry_taikhoan.pack(pady=5)
            
            tk.Label(edit_window, text="Mật khẩu:").pack(pady=5)
            entry_matkhau = tk.Entry(edit_window)
            entry_matkhau.insert(0, selected_values[2])
            entry_matkhau.pack(pady=5)
            
            tk.Button(edit_window, text="Lưu", command=save_edited_admin_account).pack(pady=20)

        def delete_admin_account():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Chưa chọn mục", "Vui lòng chọn tài khoản để xóa")
                return

            selected_values = tree.item(selected_item, "values")
            
            # Hiển thị hộp thoại xác nhận xóa
            confirm = messagebox.askyesno("Xóa tài khoản", f"Bạn có chắc muốn xóa tài khoản {selected_values[1]}?")
            if confirm:
                cursor.execute("DELETE FROM Admin_Account WHERE ma_admin = ?", (selected_values[0],))
                conn.commit()
                load_data()
                messagebox.showinfo("Thông báo", "Xóa tài khoản thành công!")
    
        # Tạo các nút thêm, sửa, xóa ở phía bên phải
        button_frame = tk.Frame(admin_window, bg="white")
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
        
        button_width = 10
        tk.Button(button_frame, text="Thêm", width=button_width, command=add_admin_account).pack(pady=5)
        tk.Button(button_frame, text="Sửa", width=button_width, command=edit_admin_account).pack(pady=5)
        tk.Button(button_frame, text="Xóa", width=button_width, command=delete_admin_account).pack(pady=5)
        
        # Configuring grid weights for better resizing
        admin_window.grid_columnconfigure(0, weight=1)
        admin_window.grid_rowconfigure(0, weight=1)
        
        # Load data into Treeview
        load_data()
    
    def check_password(func):
        def wrapper():
            # Tạo hộp thoại nhập tài khoản và mật khẩu
            dialog = tk.Toplevel(root)
            dialog.title("Authentication Required")
            dialog.geometry("400x250")
            dialog.grab_set()  # Vô hiệu hóa cửa sổ chính khi cửa sổ mật khẩu đang mở

            ttk.Label(dialog, text="Yêu cầu đăng nhập tài khoản quản lý", font=("Helvetica", 12, "bold")).pack(pady=10)

            ttk.Label(dialog, text="Enter username:").pack(pady=5)
            username_entry = ttk.Entry(dialog)
            username_entry.pack(pady=5)

            ttk.Label(dialog, text="Enter password:").pack(pady=5)
            password_entry = ttk.Entry(dialog, show='*')
            password_entry.pack(pady=5)

            def on_ok():
                username = username_entry.get()
                password = password_entry.get()
                cursor.execute("SELECT COUNT(*) FROM Admin_Account WHERE taikhoanadmin = ? AND matkhau = ?", (username, password))
                result = cursor.fetchone()

                if result[0] > 0:
                    dialog.destroy()  # Đóng hộp thoại nếu thông tin xác thực đúng
                    func()
                else:
                    messagebox.showerror("Error", "Incorrect username or password")

            ttk.Button(dialog, text="OK", command=on_ok).pack(pady=10)
            ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack()

        return wrapper
    
    def dash_board():
        # Tạo giao diện Tkinter
        dash2_window = tk.Toplevel(root, bg="white")

        # width & height
        w = 1050
        h = 600

        mainframe = tk.Frame(dash2_window)

        # center window
        sw = mainframe.winfo_screenwidth()
        sh = mainframe.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        dash2_window.geometry('%dx%d+%d+%d' % (w,h,x,y))
        # end center window
        
        dash2_window.overrideredirect(1) # remove border

        frame = tk.Frame(mainframe, bg='#ffffff')
        topbarframe = tk.Frame(frame, bg='#57a1f8', width=w, height=50)
        sidebarframe = tk.Frame(frame, bg='#EEE5DE', width=250, height=700)
        contentframe = tk.Frame(frame, bg='#ffffff', width=900, height=550)

        app_title = tk.Label(topbarframe, text='Dashboard', font=('Arial', 20), bg='#57a1f8', fg='white', padx=5)

        def close_dashboard():
            dash2_window.destroy()
            
        btn_close = tk.Button(topbarframe, text='X',bg='#57a1f8', font=('Arial',12), 
            fg='red', borderwidth=1, relief="solid", command=close_dashboard)
        
        soxe_frame = tk.Frame(contentframe, bg='#ffb229', width=245, height=200)
        soxe_title = tk.Label(soxe_frame, text='Số xe trong bãi', font=('Verdana', 16),
                            bg='#f69110', fg='#ffffff', width=19, pady=12)
        soxe_count = tk.Label(soxe_frame, text='199', font=('Verdana', 16, 'bold'), bg='#ffb229',
                            fg='#ffffff', padx=0, pady=10)

        the_frame = tk.Frame(contentframe, bg='#4bc012', width=245, height=200)
        the_title = tk.Label(the_frame, text='Số thẻ được sử dụng', font=('Verdana', 16),
                            bg='#41a00a', fg='#ffffff', width=19, pady=12)
        the_count = tk.Label(the_frame, text='441', font=('Verdana', 16, 'bold'),
                            bg='#4bc012', fg='#ffffff', padx=11, pady=10)

        vao_frame = tk.Frame(contentframe, bg='#9b59b6', width=245, height=200)
        vao_title = tk.Label(vao_frame, text='Dân vào, ra hôm nay', font=('Verdana', 16), bg='#7d3c9b',
                            fg='#ffffff', width=19, pady=12)
        vao_count = tk.Label(vao_frame, text='2369', font=('Verdana', 16, 'bold'), bg='#9b59b6',
                            fg='#ffffff', padx=11, pady=10)

        vao_the_frame = tk.Frame(contentframe, bg='#98F5FF', width=245, height=200)
        vao_the_title = tk.Label(vao_the_frame, text='Thẻ vào, ra hôm nay', font=('Verdana', 16), bg='#7AC5CD',
                            fg='#ffffff', width=19, pady=12)
        vao_the_count = tk.Label(vao_the_frame, text='2369', font=('Verdana', 16, 'bold'), bg='#98F5FF',
                            fg='#ffffff', padx=11, pady=10)
        
        vao_thang_frame = tk.Frame(contentframe, bg='#54FF9F', width=245, height=200)
        vao_thang_title = tk.Label(vao_thang_frame, text='Cư dân vào, ra tháng', font=('Verdana', 16), bg='#66CDAA',
                            fg='#ffffff', width=19, pady=12)
        vao_thang_count = tk.Label(vao_thang_frame, text='2369', font=('Verdana', 16, 'bold'), bg='#54FF9F',
                            fg='#ffffff', padx=11, pady=10)
        
        vao_the_thang_frame = tk.Frame(contentframe, bg='#EEE5DE', width=245, height=200)
        vao_the_thang_title = tk.Label(vao_the_thang_frame, text='Thẻ vào, ra tháng', font=('Verdana', 16), bg='#C1CDCD',
                            fg='#ffffff', width=19, pady=12)
        vao_the_thang_count = tk.Label(vao_the_thang_frame, text='2369', font=('Verdana', 16, 'bold'), bg='#EEE5DE',
                            fg='#ffffff', padx=11, pady=10)
        # menu items
        menuitem_1 = tk.Label(sidebarframe, text='Số lượt ra vào', fg='black', bg='white',
                            font=('Arial', 17), padx=5, width=15)
        menuitem_2 = tk.Label(sidebarframe, text='Số lượt thẻ ra vào', fg='black', bg='white',
                            font=('Arial', 17), padx=5, width=15)
        menuitem_3 = tk.Label(sidebarframe, text='Số xe trong bãi', fg='black', bg='white',
                            font=('Arial', 17), padx=5, width=15)

        # add hover effect to the menu
        menuitem_1.bind("<Enter>", func=lambda e: menuitem_1.config(background='#57a1f8'))
        menuitem_1.bind("<Leave>", func=lambda e: menuitem_1.config(background='white'))

        menuitem_2.bind("<Enter>", func=lambda e: menuitem_2.config(background='#57a1f8'))
        menuitem_2.bind("<Leave>", func=lambda e: menuitem_2.config(background='white'))

        menuitem_3.bind("<Enter>", func=lambda e: menuitem_3.config(background='#57a1f8'))
        menuitem_3.bind("<Leave>", func=lambda e: menuitem_3.config(background='white'))


        # Fetch counts from database
        def fetch_data():
            cursor.execute("SELECT COUNT(*) FROM BienSo WHERE TrangThai = 1")
            so_xe_trang_thai_1 = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM BienSo")
            tong_so_xe = cursor.fetchone()[0]
            soxe_count.config(text=f"{so_xe_trang_thai_1}/Tổng: {tong_so_xe}")
            cursor.execute("SELECT COUNT(*) FROM CARD_DATA WHERE status = 1")
            so_the_trang_thai_1 = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM CARD_DATA")
            tong_so_the = cursor.fetchone()[0]
            the_count.config(text=f"{so_the_trang_thai_1}/Tổng: {tong_so_the}")

            cursor.execute("SELECT COUNT(*) FROM XeVao WHERE CONVERT(date, ThoiGianVao) = CONVERT(date, GETDATE())")
            vao_so_xe_hn = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM XeRa WHERE CONVERT(date, ThoiGianRa) = CONVERT(date, GETDATE())")
            ra_so_xe_hn = cursor.fetchone()[0]
            vao_count.config (text=f"Vào: {vao_so_xe_hn}/Ra: {ra_so_xe_hn}")
            
            cursor.execute("SELECT COUNT(*) FROM Entry WHERE CONVERT(date, entry_time) = CONVERT(date, GETDATE())")
            vao_so_the_hn = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM [OUT] WHERE CONVERT(date, exit_time) = CONVERT(date, GETDATE())")
            ra_so_the_hn = cursor.fetchone()[0]
            vao_the_count.config(text=f"Vào: {vao_so_the_hn}/Ra: {ra_so_the_hn}")

            cursor.execute("SELECT COUNT(*) FROM XeVao WHERE MONTH(ThoiGianVao) = MONTH(GETDATE()) AND YEAR(ThoiGianVao) = YEAR(GETDATE())")
            vao_so_xe_thang_nay = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM XeRa WHERE MONTH(ThoiGianRa) = MONTH(GETDATE()) AND YEAR(ThoiGianRa) = YEAR(GETDATE())")
            ra_so_xe_thang_nay = cursor.fetchone()[0]
            vao_thang_count.config(text=f"Vào: {vao_so_xe_thang_nay}/Ra: {ra_so_xe_thang_nay}")

            cursor.execute("SELECT COUNT(*) FROM Entry WHERE MONTH(entry_time) = MONTH(GETDATE()) AND YEAR(entry_time) = YEAR(GETDATE())")
            vao_so_the_thang = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM [OUT] WHERE MONTH(exit_time) = MONTH(GETDATE()) AND YEAR(exit_time) = YEAR(GETDATE())")
            ra_so_the_thang = cursor.fetchone()[0]
            vao_the_thang_count.config(text=f"Vào: {vao_so_the_thang}/ Ra: {ra_so_the_thang}")

        fetch_data()
        
        # bind click events to menu items
        menuitem_1.bind("<Button-1>", show_dashboard_frame)
        menuitem_2.bind("<Button-1>", dashboard_card)
        menuitem_3.bind("<Button-1>", dashboard_baixe)
        btn_reload = tk.Button(topbarframe, text='Reload',bg='#57a1f8', font=('Arial',12), 
            fg='red', borderwidth=1, relief="solid", command=fetch_data)
        # ------------------------------------ #

        mainframe.pack(fill="both", expand=True)

        frame.pack(fill="both", expand=True)

        topbarframe.pack()
        topbarframe.grid_propagate(False)

        app_title.place(x=10, y=7)
        btn_close.place(x=1010,y=10)
        btn_reload.place(x=900,y=10)
        
        
        sidebarframe.pack()
        sidebarframe.grid_propagate(False)
        sidebarframe.place(x=0, y=60)

        contentframe.pack()
        contentframe.grid_propagate(False)
        contentframe.place(x=250, y=50)
        
        

        soxe_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        soxe_frame.grid_propagate(False)
        soxe_title.grid(row=0, column=0)
        soxe_count.grid(row=1, column=0, padx=15, pady=15)

        the_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        the_frame.grid_propagate(False)
        the_title.grid(row=0, column=0)
        the_count.grid(row=1, column=0, padx=15, pady=15)

        vao_frame.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')
        vao_frame.grid_propagate(False)
        vao_title.grid(row=0, column=0)
        vao_count.grid(row=1, column=0, padx=15, pady=15)
        
        vao_the_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        vao_the_frame.grid_propagate(False)
        vao_the_title.grid(row=0, column=0)
        vao_the_count.grid(row=1, column=0, padx=15, pady=15)
        
        vao_thang_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        vao_thang_frame.grid_propagate(False)
        vao_thang_title.grid(row=0, column=0)
        vao_thang_count.grid(row=1, column=0, padx=15, pady=15)
        
        vao_the_thang_frame.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')
        vao_the_thang_frame.grid_propagate(False)
        vao_the_thang_title.grid(row=0, column=0)
        vao_the_thang_count.grid(row=1, column=0, padx=15, pady=15)

        menuitem_1.grid(row=0, column=0, padx=10, pady=10)
        menuitem_2.grid(row=1, column=0)
        menuitem_3.grid(row=2, column=0, padx=10, pady=10)
    
    def restore_data():
        server = 'LAGGER\CHIEN'
        database = 'Python5'
        backup_dir = 'E:/TTTN/Plate_Recognize/5/backup'
        
        try:
            # Tìm tệp backup mới nhất trong thư mục
            backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.bak')]
            if not backup_files:
                print("Không tìm thấy tệp sao lưu trong thư mục.")
                return
            
            latest_backup_file = max(backup_files, key=os.path.getctime)

            # Kết nối tới cơ sở dữ liệu
            conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes')
            cursor = conn.cursor()

            # Tạo câu lệnh restore
            restore_command = f"RESTORE DATABASE {database} FROM DISK='{os.path.join(backup_dir, latest_backup_file)}' WITH REPLACE"

            # Thực thi câu lệnh restore
            cursor.execute(restore_command)

            print(f"Khôi phục dữ liệu thành công từ file: {latest_backup_file}")
            messagebox.showinfo("Thông báo", "Đã khôi phục dữ liệu từ file mới nhất.")
        except Exception as e:
            print(f"Có lỗi xảy ra trong quá trình khôi phục dữ liệu: {e}")
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra trong quá trình khôi phục dữ liệu: {e}")
        finally:
            # Đóng kết nối tới cơ sở dữ liệu
            cursor.close()
            conn.close()
    
    root = tk.Tk()
    root.title("Hệ thống bãi xe thông minh")
    # Tạo một menu chính
    main_menu = tk.Menu(root)
    root.config(menu=main_menu)

    # Tạo các mục trong menu chính
    dashboard_menu = tk.Menu(main_menu, tearoff=False)
    main_menu.add_cascade(label="Dashboard", menu=dashboard_menu)
    dashboard_menu.add_command(label="Dashboard",command=dash_board)
      
    file_menu = tk.Menu(main_menu, tearoff=False)  # Tearoff để ngăn mục menu bị rời rạc
    main_menu.add_cascade(label="Hệ thống", menu=file_menu)
    file_menu.add_command(label="Cư dân", command=show_hethong_xeravao)
    file_menu.add_command(label="Khách vãng lai", command=show_readRFID)
    file_menu.add_command(label="Restore Data", command=restore_data)
    file_menu.add_command(label="Thoát", command=confirm_exit)

    edit_menu = tk.Menu(main_menu, tearoff=False)
    main_menu.add_cascade(label="Quản lý", menu=edit_menu)
    edit_menu.add_command(label="Quản lý bãi xe", command=check_password(show_Qly_baixe))
    edit_menu.add_command(label="Quản lý biển số", command=check_password(show_Qly_bienso))
    edit_menu.add_command(label="Quản lý thẻ xe", command=check_password(show_Qly_thexe))

    help_menu = tk.Menu(main_menu, tearoff=False)
    main_menu.add_cascade(label="Thống kê", menu=help_menu)
    help_menu.add_command(label="Thống kê số lượng ra", command=check_password(show_Thke_xera))
    help_menu.add_command(label="Thống kê số lượng vào", command=check_password(show_Thke_xevao))
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    account_menu = tk.Menu(main_menu, tearoff=False)
    main_menu.add_cascade(label="Tài khoản", menu=account_menu)
    account_menu.add_command(label="Thông tin tài khoản", command=check_password(show_account_frame))
    account_menu.add_command(label="Thông tin tài khoản quản lý", command=check_password(show_admin_frame))

    root.geometry(f"{screen_width}x{screen_height}")  

    # Thêm nhãn "Hệ thống bãi xe thông minh"
    label_system = tk.Label(root, text="HỆ THỐNG BÃI XE THÔNG MINH", font=("Arial", 20, "bold"), bg="#57a1f8",fg='white')
    label_system.pack(fill=tk.X)

    root.mainloop()

# Call the main function when needed
if __name__ == "__main__":
    main_function() 