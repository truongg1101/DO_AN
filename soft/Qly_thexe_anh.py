import tkinter as tk
from tkinter import ttk
import pyodbc
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
import datetime
from tkinter import font
from io import BytesIO
from PIL import Image, ImageTk
import pandas as pd
from datetime import datetime

# Kết nối đến cơ sở dữ liệu SQL Server
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-BINPIL1;DATABASE=Python5;Trusted_Connection=yes;')
cursor = conn.cursor()

# Định nghĩa biến global
entry_thexe = None
tree = None
#entry_tree = None
#out_tree = None

global entry_tree 
global out_tree 

entry_ma_the = None
combobox_ngay = None 
combobox_thang = None
combobox_nam = None

def show_month():
    global page_frame
    def fetch_data():
        selected_month = int(month_cb.get())
        selected_year = int(year_cb.get())

        # Truy vấn số lượng thẻ vào trong tháng
        entry_query = f"""
        SELECT COUNT(*) as EntryCount
        FROM Entry
        WHERE MONTH(entry_time) = {selected_month} AND YEAR(entry_time) = {selected_year}
        """
        
        # Truy vấn số lượng thẻ ra trong tháng
        exit_query = f"""
        SELECT COUNT(*) as ExitCount
        FROM OUT
        WHERE MONTH(exit_time) = {selected_month} AND YEAR(exit_time) = {selected_year}
        """
        entry_df = pd.read_sql(entry_query, conn)
        exit_df = pd.read_sql(exit_query, conn)

        entry_count = entry_df['EntryCount'].iloc[0]
        exit_count = exit_df['ExitCount'].iloc[0]

        result_text.set(f"Số lượng thẻ vào: {entry_count}\n\nSố lượng thẻ ra: {exit_count}")

    # Tạo cửa sổ mới
    new_window = tk.Toplevel(page_frame)
    new_window.title("Chi tiết thẻ vào và thẻ ra theo tháng")
    
    # Tạo khung cho lựa chọn tháng và năm
    frame_selection = ttk.Frame(new_window, padding="10 10 10 10")
    frame_selection.pack(fill=tk.BOTH, expand=True)
    
    # Định nghĩa font chữ
    bold_font = ("Helvetica", 12, "bold")
    normal_font = ("Helvetica", 13, "bold")

    # Tạo combobox để chọn tháng
    ttk.Label(frame_selection, text="Chọn tháng:", font=bold_font).grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
    month_cb = ttk.Combobox(frame_selection, values=[str(i) for i in range(1, 13)], state='readonly', font=normal_font)
    month_cb.grid(column=1, row=0, padx=5, pady=5)
    month_cb.current(0)  # Set default value

    # Tạo combobox để chọn năm
    current_year = datetime.now().year
    year_values = [str(i) for i in range(2023, current_year + 1)]
    ttk.Label(frame_selection, text="Chọn năm:", font=bold_font).grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)
    year_cb = ttk.Combobox(frame_selection, values=year_values, state='readonly', font=normal_font)
    year_cb.grid(column=1, row=1, padx=5, pady=5)
    year_cb.current(len(year_values) - 1)  # Set default value to the most recent year

    # Tạo nút để lấy dữ liệu
    ttk.Button(frame_selection, text="Hiển thị", command=fetch_data, style="TButton").grid(column=0, row=2, columnspan=2, pady=10)

    # Kết quả hiển thị
    frame_result = ttk.Frame(new_window, padding="10 10 10 10")
    frame_result.pack(fill=tk.BOTH, expand=True)
    
    result_text = tk.StringVar()
    ttk.Label(frame_result, textvariable=result_text, justify=tk.LEFT, font=normal_font).pack(pady=10, padx=10)
 
def show_detail_in(event):
    global page_frame
    # Lấy dòng được chọn trong Treeview
    selected_item = entry_tree.focus()

    # Lấy dữ liệu từ dòng được chọn
    data = entry_tree.item(selected_item)
    if not data["values"]:
        return

    entry_id = data["values"][0]  # Lấy entry_id từ dữ liệu

    # Truy vấn dữ liệu từ bảng Entry dựa trên entry_id
    try:
        cursor.execute("""
            SELECT e.entry_id, e.entry_time, e.entry_photo, c.card_id
            FROM Entry e
            JOIN CARD_DATA c ON e.card_id = c.card_id
            WHERE e.entry_id = ?
        """, (entry_id,))
        row = cursor.fetchone()

        if not row:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin lượt vào")
            return

        # Tạo cửa sổ mới để hiển thị thông tin chi tiết
        detail_window = tk.Toplevel(page_frame, bg="white")
        detail_window.title("Thông tin chi tiết lượt vào")
        detail_window.geometry("750x400")

        # Phân chia layout thành 2 phần
        frame_label = tk.Frame(detail_window, borderwidth=0, relief="raised", bg="white")
        frame_label.pack(side="top", fill="both", expand=True, padx=0, pady=10)

        frame_info = tk.Frame(detail_window, borderwidth=0, relief="raised", bg="white")
        frame_info.pack(side="bottom", fill="both", expand=True, padx=10, pady=0)

        # Định dạng lại thời gian để chỉ hiển thị đến giây
        formatted_time = row[1].strftime('%Y-%m-%d %H:%M:%S')
        
        # Tạo và cấu hình label
        label_ten = tk.Label(frame_label, bg="white", text="THÔNG TIN XE VÀO", font=("Helvetica", 20, "bold"))
        label_ten.place(relx=0.5, rely=0.5, anchor="center")

        # Hiển thị thông tin chi tiết
        frame_anh = tk.Frame(detail_window, bg="white", borderwidth=0, relief="solid")
        frame_anh.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        frame_thongtin = tk.Frame(detail_window, bg="white", borderwidth=0, relief="solid")
        frame_thongtin.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        info_label = tk.Label(frame_thongtin, bg="white",
                              text=f"Mã Lượt Vào: {row[0]}\n\n"
                                   f"Thời Gian Vào: {formatted_time}\n\n"
                                   f"Mã Thẻ: {row[3]}",
                              font=("Arial", 16),
                              anchor="nw",
                              justify="left")
        info_label.pack(fill="both", expand=True, anchor="nw")

        # Hiển thị ảnh từ dữ liệu binary
        entry_photo_data = row[2]
        if entry_photo_data:
            image_data = BytesIO(entry_photo_data)
            img = Image.open(image_data)
            img = img.resize((300, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame_anh, image=photo)
            img_label.image = photo  # Giữ tham chiếu tới ảnh để không bị garbage collected
            img_label.pack()
        else:
            no_image_label = tk.Label(frame_anh, bg="white", text="Không có ảnh")
            no_image_label.pack()
    except pyodbc.Error as e:
        messagebox.showerror("Lỗi cơ sở dữ liệu", f"Lỗi: {e}") 
            
def show_detail_out(event):
    global page_frame
    # Lấy dòng được chọn trong Treeview
    selected_item = out_tree.focus()

    # Lấy dữ liệu từ dòng được chọn
    data = out_tree.item(selected_item)
    if not data["values"]:
        return

    exit_id = data["values"][0]  # Lấy exit_id từ dữ liệu

    # Truy vấn dữ liệu từ bảng OUT dựa trên exit_id
    try:
        cursor.execute("""
            SELECT o.exit_id, o.exit_time, o.exit_photo, c.card_id
            FROM [OUT] o
            JOIN CARD_DATA c ON o.card_id = c.card_id
            WHERE o.exit_id = ?
        """, (exit_id,))
        row = cursor.fetchone()

        if not row:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin lượt ra")
            return

        # Tạo cửa sổ mới để hiển thị thông tin chi tiết
        detail_window = tk.Toplevel(page_frame, bg="white")
        detail_window.title("Thông tin chi tiết lượt ra")
        detail_window.geometry("750x400")

        # Phân chia layout thành 2 phần
        frame_label = tk.Frame(detail_window, borderwidth=0, relief="raised", bg="white")
        frame_label.pack(side="top", fill="both", expand=True, padx=0, pady=10)

        frame_info = tk.Frame(detail_window, borderwidth=0, relief="raised", bg="white")
        frame_info.pack(side="bottom", fill="both", expand=True, padx=10, pady=0)

        # Định dạng lại thời gian để chỉ hiển thị đến giây
        formatted_time = row[1].strftime('%Y-%m-%d %H:%M:%S')
        
        # Tạo và cấu hình label
        label_ten = tk.Label(frame_label, bg="white", text="THÔNG TIN XE RA", font=("Helvetica", 20, "bold"))
        label_ten.place(relx=0.5, rely=0.5, anchor="center")

        # Hiển thị thông tin chi tiết
        frame_anh = tk.Frame(detail_window, bg="white", borderwidth=0, relief="solid")
        frame_anh.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        frame_thongtin = tk.Frame(detail_window, bg="white", borderwidth=0, relief="solid")
        frame_thongtin.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        info_label = tk.Label(frame_thongtin, bg="white",
                              text=f"Mã Lượt Ra: {row[0]}\n\n"
                                   f"Thời Gian Ra: {formatted_time}\n\n"
                                   f"Mã Thẻ: {row[3]}",
                              font=("Arial", 16),
                              anchor="nw",
                              justify="left")
        info_label.pack(fill="both", expand=True, anchor="nw")

        # Hiển thị ảnh từ dữ liệu binary
        exit_photo_data = row[2]
        if exit_photo_data:
            image_data = BytesIO(exit_photo_data)
            img = Image.open(image_data)
            img = img.resize((300, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame_anh, image=photo)
            img_label.image = photo  # Giữ tham chiếu tới ảnh để không bị garbage collected
            img_label.pack()
        else:
            no_image_label = tk.Label(frame_anh, bg="white", text="Không có ảnh")
            no_image_label.pack()
    except pyodbc.Error as e:
        messagebox.showerror("Lỗi cơ sở dữ liệu", f"Lỗi: {e}")
   
def search_card():
    global entry_thexe, tree
    
    # Kiểm tra xem entry_thexe và tree đã được khởi tạo chưa
    if entry_thexe is None or tree is None:
        messagebox.showerror("Lỗi", "Vui lòng tạo biến entry_thexe và tree")
        return
    
    # Xóa dữ liệu cũ trên Treeview trước khi tìm kiếm mới
    clear_tree()
    
    # Lấy mã thẻ từ entry
    card_id = entry_thexe.get()
    
    # Kiểm tra nếu mã thẻ không được nhập vào
    if not card_id:
        messagebox.showerror("Lỗi", "Vui lòng nhập mã thẻ")
        return
    
    # Thực hiện truy vấn để kiểm tra xem thẻ có tồn tại không
    cursor = conn.cursor()
    cursor.execute("SELECT card_id, status FROM CARD_DATA WHERE card_id = ?", (card_id,))
    rows = cursor.fetchall()
    
    # Kiểm tra xem có dữ liệu trả về từ truy vấn không
    if not rows:
        messagebox.showinfo("Thông báo", "Thẻ không tồn tại")
        reload_cards()
        return
    
    # Hiển thị kết quả lên Treeview
    for row in rows:
        tree.insert("", "end", text=row[0], values=(row[0], "Active" if row[1] else "Inactive"))

def add_card():
    global entry_thexe, tree
    # Lấy mã thẻ từ entry
    card_id = entry_thexe.get()
    
    # Kiểm tra nếu mã thẻ không được nhập vào
    if not card_id:
        tk.messagebox.showerror("Lỗi", "Vui lòng nhập mã thẻ")
        return
    
    # Thêm thẻ vào cơ sở dữ liệu
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM CARD_DATA WHERE card_id = ?", (card_id,))
    result = cursor.fetchone()
    if result[0] > 0:
        tk.messagebox.showerror("Lỗi", "Thẻ này đã tồn tại")
        return
    
    cursor.execute("INSERT INTO CARD_DATA (card_id) VALUES (?)", (card_id,))
    conn.commit()
    messagebox.showinfo("Thông báo", "Thêm thẻ thành công!")
    # Hiển thị lại danh sách thẻ
    reload_cards()

def delete_card():
    global entry_thexe, tree
    # Lấy ID của thẻ được chọn
    selected_item = tree.selection()
    
    # Kiểm tra xem có mục nào được chọn không
    if not selected_item:
        tk.messagebox.showerror("Lỗi", "Vui lòng chọn thẻ để xóa")
        return
    
    # Lấy mã thẻ từ item được chọn
    card_id = tree.item(selected_item, "text")
    
    # Xóa thẻ từ cơ sở dữ liệu
    cursor = conn.cursor()
    cursor.execute("DELETE FROM CARD_DATA WHERE card_id = ?", (card_id,))
    conn.commit()
    
    # Xóa item từ Treeview
    tree.delete(selected_item)
    messagebox.showinfo("Thông báo", "Xóa thẻ thành công!")

def reload_cards():
    global entry_thexe, tree
    # Xóa dữ liệu cũ trên Treeview
    clear_tree()
    
    # Lấy dữ liệu từ bảng CARD_DATA và hiển thị trên Treeview
    cursor = conn.cursor()
    cursor.execute("SELECT card_id, status FROM CARD_DATA")
    for row in cursor.fetchall():
        tree.insert("", "end", text=row[0], values=(row[0], "Được sử dụng" if row[1] else "Không được sử dụng"))

def edit_card():
    global tree, entry_thexe
    
    # Lấy ID của thẻ được chọn từ Treeview
    selected_item = tree.selection()
    
    # Kiểm tra xem có mục nào được chọn không
    if not selected_item:
        messagebox.showerror("Lỗi", "Vui lòng chọn thẻ để sửa")
        return
    
    # Lấy mã thẻ từ item được chọn
    card_id = tree.item(selected_item, "text")
    
    # Hiển thị cửa sổ nhập thông tin mới cho thẻ
    new_card_id = simpledialog.askstring("Sửa thông tin thẻ", "Nhập mã thẻ mới:", initialvalue=card_id)
    new_status = simpledialog.askinteger("Sửa thông tin thẻ", "Nhập trạng thái mới (0 hoặc 1):")
    
    # Kiểm tra xem người dùng đã nhập đủ thông tin hay chưa
    if not new_card_id or new_status is None:
        messagebox.showerror("Lỗi", "Vui lòng nhập đủ thông tin")
        return
    
    # Thực hiện truy vấn SQL UPDATE để cập nhật thông tin thẻ trong cơ sở dữ liệu
    cursor = conn.cursor()
    cursor.execute("UPDATE CARD_DATA SET card_id = ?, status = ? WHERE card_id = ?", (new_card_id, new_status, card_id))
    conn.commit()
    
    # Cập nhật lại dữ liệu trên Treeview
    reload_cards()
    messagebox.showinfo("Thông báo", "Sửa thẻ thành công!")
    
def clear_tree():
    global entry_thexe, tree
    # Xóa dữ liệu trên Treeview
    for item in tree.get_children():
        tree.delete(item)    

def load_entry_data():
    global entry_tree
    # Xóa dữ liệu cũ trên Treeview trước khi tải dữ liệu mới
    clear_entry_tree()
    
    # Thực hiện truy vấn SQL để lấy dữ liệu từ bảng Entry
    cursor = conn.cursor()
    cursor.execute("SELECT entry_id, CONVERT(varchar, entry_time, 120) as entry_time, card_id FROM Entry")
    rows = cursor.fetchall()
    
    # Hiển thị dữ liệu lên Treeview
    for row in rows:
        entry_tree.insert("", "end", text=row[0], values=(row[0], row[1], row[2]))

def clear_entry_tree():
    global entry_tree
    # Xóa tất cả các mục trên Treeview
    for item in entry_tree.get_children():
        entry_tree.delete(item)

def load_out_data():
    global out_tree
    # Xóa dữ liệu cũ trên Treeview trước khi tải dữ liệu mới
    clear_out_tree()
    
    # Thực hiện truy vấn SQL để lấy dữ liệu từ bảng OUT
    cursor = conn.cursor()
    cursor.execute("SELECT exit_id, CONVERT(varchar, exit_time, 120) as exit_time, card_id FROM OUT")
    rows = cursor.fetchall()
    
    # Hiển thị dữ liệu lên Treeview
    for row in rows:
        out_tree.insert("", "end", text=row[0], values=(row[0], row[1], row[2]))

def clear_out_tree():
    global out_tree
    # Xóa tất cả các mục trên Treeview
    for item in out_tree.get_children():
        out_tree.delete(item)        
 
def show_recent():
    # Thực hiện truy vấn SQL để lấy 10 lượt thẻ ra, vào gần nhất
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 10 entry_id, CONVERT(VARCHAR, entry_time, 120), card_id FROM Entry ORDER BY entry_time DESC")
    entry_rows = cursor.fetchall()
    
    cursor.execute("SELECT TOP 10 exit_id, CONVERT(VARCHAR, exit_time, 120), card_id FROM OUT ORDER BY exit_time DESC")
    out_rows = cursor.fetchall()
    
    # Xóa dữ liệu cũ trên cả hai Treeview trước khi cập nhật
    clear_entry_tree()
    clear_out_tree()
    
    # Hiển thị dữ liệu mới lên cả hai Treeview
    for row in entry_rows:
        entry_tree.insert("", "end", text=row[0], values=(row[0], (row[1]), row[2]))
        
    for row in out_rows:
        out_tree.insert("", "end", text=row[0], values=(row[0], (row[1]), row[2]))

def show_today():
    # Lấy ngày hiện tại
    today = datetime.now().date()
    # Thực hiện truy vấn SQL để lấy tất cả các lượt thẻ ra, vào trong ngày hôm nay
    cursor = conn.cursor()
    cursor.execute("SELECT entry_id, CONVERT(VARCHAR, entry_time, 120), card_id FROM Entry WHERE CAST(entry_time AS DATE) = CAST(GETDATE() AS DATE)")
    entry_rows = cursor.fetchall()
    
    cursor.execute("SELECT exit_id, CONVERT(VARCHAR, exit_time, 120), card_id FROM OUT WHERE CAST(exit_time AS DATE) = CAST(GETDATE() AS DATE)")
    out_rows = cursor.fetchall()
    
    # Xóa dữ liệu cũ trên cả hai Treeview trước khi cập nhật
    clear_entry_tree()
    clear_out_tree()
    
    # Hiển thị dữ liệu mới lên cả hai Treeview
    for row in entry_rows:
        entry_tree.insert("", "end", text=row[0], values=(row[0], (row[1]), row[2]))
        
    for row in out_rows:
        out_tree.insert("", "end", text=row[0], values=(row[0], (row[1]), row[2]))

def show_all():
    # Thực hiện truy vấn SQL để lấy toàn bộ dữ liệu của hai bảng Entry và Out
    cursor = conn.cursor()
    cursor.execute("SELECT entry_id, CONVERT(VARCHAR, entry_time, 120), card_id FROM Entry")
    entry_rows = cursor.fetchall()
    
    cursor.execute("SELECT exit_id, CONVERT(VARCHAR, exit_time, 120), card_id FROM OUT")
    out_rows = cursor.fetchall()
    
    # Xóa dữ liệu cũ trên cả hai Treeview trước khi cập nhật
    clear_entry_tree()
    clear_out_tree()
    
    # Hiển thị dữ liệu mới lên cả hai Treeview
    for row in entry_rows:
        entry_tree.insert("", "end", text=row[0], values=(row[0], (row[1]), row[2]))
        
    for row in out_rows:
        out_tree.insert("", "end", text=row[0], values=(row[0], (row[1]), row[2]))

def search_data(entry_ma_the, checkbox_var_1, checkbox_var_2,entry_tree, out_tree):
    global combobox_ngay, combobox_thang, combobox_nam

    # Tạo truy vấn cơ sở dữ liệu cho bảng Entry
    query_entry = "SELECT entry_id, entry_time, card_id FROM Entry"

    # Kiểm tra xem người dùng có chọn tìm kiếm theo mã thẻ hay không
    if checkbox_var_1.get():
        card_id = entry_ma_the.get()
        if card_id == "":
            messagebox.showwarning("Thông báo", "Vui lòng nhập mã thẻ")
            return
        query_entry += f" WHERE card_id = '{card_id}'"

    # Kiểm tra xem người dùng có chọn tìm kiếm theo ngày hay không
    if checkbox_var_2.get():
        if not checkbox_var_1.get():
            query_entry += " WHERE"
        else:
            query_entry += " AND"

        # Lấy giá trị của các combobox ngày, tháng, năm
        day = combobox_ngay.get()
        month = combobox_thang.get()
        year = combobox_nam.get()
        if day == "" or month == "" or year == "":
            messagebox.showwarning("Thông báo", "Bạn chưa chọn ngày")
            return
        # Tạo chuỗi ngày tháng năm
        selected_date = f"'{year}-{month}-{day}'"

        # Thêm điều kiện cho ngày vào truy vấn
        query_entry += f" CAST(entry_time AS DATE) = {selected_date}"

    # Tạo truy vấn cơ sở dữ liệu cho bảng Out
    query_out = "SELECT exit_id, exit_time, card_id FROM OUT"

    # Kiểm tra xem người dùng có chọn tìm kiếm theo mã thẻ hay không
    if checkbox_var_1.get():
        card_id = entry_ma_the.get()
        if card_id == "":
            messagebox.showwarning("Thông báo", "Vui lòng nhập mã thẻ")
            return
        query_out += f" WHERE card_id = '{card_id}'"

    # Kiểm tra xem người dùng có chọn tìm kiếm theo ngày hay không
    if checkbox_var_2.get():
        if not checkbox_var_1.get():
            query_out += " WHERE"
        else:
            query_out += " AND"

        # Lấy giá trị của các combobox ngày, tháng, năm
        day = combobox_ngay.get()
        month = combobox_thang.get()
        year = combobox_nam.get()
        if day == "" or month == "" or year == "":
            messagebox.showwarning("Thông báo", "Bạn chưa chọn ngày")
            return
        # Tạo chuỗi ngày tháng năm
        selected_date = f"'{year}-{month}-{day}'"

        # Thêm điều kiện cho ngày vào truy vấn
        query_out += f" CAST(exit_time AS DATE) = {selected_date}"

    # Thực hiện truy vấn cho bảng Entry và hiển thị kết quả trong entry_tree
    cursor = conn.cursor()
    cursor.execute(query_entry)
    entry_rows = cursor.fetchall()
    entry_tree.delete(*entry_tree.get_children())
    entry_data_count = 0  # Biến đếm số dòng dữ liệu trong bảng Entry
    for row in entry_rows:
    # Chỉ hiển thị thời gian đến đơn vị giây (loại bỏ milisecond)
        entry_time = row[1].strftime('%Y-%m-%d %H:%M:%S')
        entry_tree.insert("", "end", text=row[0], values=(row[0], entry_time, row[2]))  # Sửa đổi chỉ số cột nếu cần
        entry_data_count += 1
    # Thực hiện truy vấn cho bảng Out và hiển thị kết quả trong out_tree
    cursor.execute(query_out)
    out_rows = cursor.fetchall()
    out_tree.delete(*out_tree.get_children())
    out_data_count = 0  # Biến đếm số dòng dữ liệu trong bảng Out
    for row in out_rows:
        # Chỉ hiển thị thời gian đến đơn vị giây (loại bỏ milisecond)
        exit_time = row[1].strftime('%Y-%m-%d %H:%M:%S')
        out_tree.insert("", "end", text=row[0], values=(row[0], exit_time, row[2]))  # Sửa đổi chỉ số cột nếu cần
        out_data_count += 1

    # Kiểm tra xem có dữ liệu từ cả hai bảng hay không
    if entry_data_count == 0 and out_data_count == 0:
        messagebox.showinfo("Thông báo", "Không có dữ liệu")

def create_gui(parent):
    global page_frame
    page_frame = tk.Frame(parent)
    label_font = font.Font(family="Arial", size=14, weight="bold")
    button_font = font.Font(family="Arial", size=12, weight="bold")
    
    global entry_thexe, tree , entry_tree, out_tree
    frame_Qly_the = tk.Frame(page_frame, bg="white", borderwidth=1, relief='solid')
    frame_Qly_the.place(x=0,y=0,relwidth=0.25,relheight=1)
    
    frame_Thke = tk.Frame(page_frame, bg="white", borderwidth=1, relief='solid')
    frame_Thke.place(relx=0.25,y=0,relwidth=0.75,relheight=1)
    
    frame_option = tk.Frame(frame_Thke, bg="red", borderwidth=0, relief='solid')
    frame_option.place(x=0,y=0,relwidth=1,relheight=0.3)
    
    frame_tim_thke = tk.Frame(frame_option, bg="white")
    frame_tim_thke.place(relx=0.5,y=0,relwidth=0.5,relheight=1)
    
    frame_button_thke = tk.Frame(frame_option, bg="white")
    frame_button_thke.place(x=0,y=0,relwidth=0.5,relheight=1)
    
    frame_table = tk.Frame(frame_Thke, bg="white",borderwidth=0, relief='solid')
    frame_table.place(x=0,rely=0.3,relwidth=1,relheight=0.7)
    
    frame_Qly_the_vao = tk.Frame(frame_table, bg="white",borderwidth=0, relief='solid')
    frame_Qly_the_vao.place(x=0,y=0,relwidth=0.5,relheight=1)
    
    frame_Qly_the_ra = tk.Frame(frame_table, bg="white",borderwidth=0, relief='solid')
    frame_Qly_the_ra.place(relx=0.5,y=0,relwidth=0.5,relheight=1)
    
    frame_the = tk.Frame(frame_Qly_the, bg="white")
    frame_the.place(x=0,y=0,relwidth=1,relheight=0.15)
    # Đặt chiều cao tuyệt đối cho frame_the
    frame_the.grid_propagate(False)
    
    frame_danhsach_the = tk.Frame(frame_Qly_the,bg="white")
    frame_danhsach_the.place(x=0,rely=0.15,relwidth=1,relheight=0.85)
    
    frame_tree1 = tk.Frame(frame_danhsach_the, bg="red")
    frame_tree1.pack(fill=tk.BOTH, expand=True, padx=10,pady=10)
    #############Button thẻ#####################################################
    label_thexe = tk.Label(frame_the, text="Thẻ xe", bg="white", font=label_font)
    label_thexe.grid(row=0, column=0, padx=10, pady=10)

    entry_thexe = tk.Entry(frame_the)
    entry_thexe.grid(row=0, column=1, padx=10, pady=10)

    button_search = tk.Button(frame_the, text="Tìm kiếm", command=search_card, font=button_font)
    button_search.grid(row=0, column=2, padx=10, pady=10)

    button_add = tk.Button(frame_the, text="Thêm thẻ", command=add_card, font=button_font)
    button_add.grid(row=1, column=0, padx=5, pady=10)

    button_delete = tk.Button(frame_the, text="Xóa thẻ", command=delete_card, font=button_font)
    button_delete.grid(row=1, column=1, padx=5, pady=10)

    button_reload = tk.Button(frame_the, text="Tải lại", command=reload_cards, font=button_font)
    button_reload.grid(row=1, column=3, padx=5, pady=10)

    button_edit = tk.Button(frame_the, text="Sửa thẻ", command=edit_card, font=button_font)
    button_edit.grid(row=1, column=2, padx=5, pady=10)
    
    #################Danh sách thẻ#################################################
    
    # Tạo Treeview trong frame_tree1
    tree = ttk.Treeview(frame_tree1, columns=("Mã Thẻ", "Trạng Thái"))
    # Đặt tiêu đề cho các cột
    tree.heading("#0", text="")
    tree.heading("Mã Thẻ", text="Mã Thẻ")
    tree.heading("Trạng Thái", text="Trạng Thái")

    # Đặt chiều rộng cho các cột
    tree.column("#0", width=0)
    tree.column("Mã Thẻ", width=100)
    tree.column("Trạng Thái", width=100)
    tree["show"] = "headings"       
    # Lấy dữ liệu từ bảng CARD_DATA và hiển thị trên Treeview
    cursor = conn.cursor()
    cursor.execute("SELECT card_id, status FROM CARD_DATA")
    for row in cursor.fetchall():
        tree.insert("", "end", text=row[0], values=(row[0], "Được sử dụng" if row[1] else "Không được sử dụng"))

    # Đặt Treeview vào trong frame_tree1
    tree.pack(fill=tk.BOTH, expand=True)

    #######################Danh sách thẻ vào####################################
    # Tạo Treeview để hiển thị dữ liệu của bảng Entry
    entry_tree = ttk.Treeview(frame_Qly_the_vao, columns=("ID", "Thời gian", "Mã thẻ"))
    
    # Đặt tiêu đề cho các cột
    entry_tree.heading("#0", text="")
    entry_tree.heading("ID", text="ID")
    entry_tree.heading("Thời gian", text="Thời gian vào")
    entry_tree.heading("Mã thẻ", text="Mã thẻ")
    
    # Đặt chiều rộng cho các cột
    entry_tree.column("#0", width=0)
    entry_tree.column("ID", width=100)
    entry_tree.column("Thời gian", width=150)
    entry_tree.column("Mã thẻ", width=100)
    entry_tree["show"] = "headings"
    # Đặt Treeview vào trong frame_tree1
    entry_tree.pack(fill=tk.BOTH, expand=True)
    
    entry_tree.bind("<<TreeviewSelect>>", show_detail_in)
    # Thêm dữ liệu vào Treeview
    load_entry_data()


    #######################Danh sách thẻ ra#####################################
    # Tạo Treeview để hiển thị dữ liệu của bảng Out
    out_tree = ttk.Treeview(frame_Qly_the_ra, columns=("ID", "Thời gian", "Mã thẻ"))
    
    # Đặt tiêu đề cho các cột
    out_tree.heading("#0", text="")
    out_tree.heading("ID", text="ID")
    out_tree.heading("Thời gian", text="Thời gian ra")
    out_tree.heading("Mã thẻ", text="Mã thẻ")
    
    # Đặt chiều rộng cho các cột
    out_tree.column("#0", width=0)
    out_tree.column("ID", width=100)
    out_tree.column("Thời gian", width=150)
    out_tree.column("Mã thẻ", width=100)
    out_tree["show"] = "headings"
    # Đặt Treeview vào trong frame_tree1
    out_tree.pack(fill=tk.BOTH, expand=True)
    out_tree    .bind("<<TreeviewSelect>>", show_detail_out)
    # Thêm dữ liệu vào Treeview
    load_out_data()
    
    ##########################Button thống kê###################################
    button_show_recent = tk.Button(frame_button_thke, text="Hiển thị 10 lượt vào, ra gần nhất", command=show_recent, font=button_font)
    button_show_recent.pack(fill=tk.BOTH, expand=True,side=tk.TOP, padx=10, pady=5)

    button_show_today = tk.Button(frame_button_thke, text="Hiển thị các lượt vào ra trong ngày hôm nay", command=show_today,font=button_font)
    button_show_today.pack(fill=tk.BOTH, expand=True,side=tk.TOP, padx=10, pady=5)

    button_show_all = tk.Button(frame_button_thke, text="Hiển thị toàn bộ", command=show_all, font=button_font)
    button_show_all.pack(fill=tk.BOTH, expand=True,side=tk.TOP, padx=10, pady=5)
    
    button_show_month = tk.Button(frame_button_thke, text="Hiển thị thống kê theo tháng", command=show_month, font=button_font)
    button_show_month.pack(fill=tk.BOTH, expand=True,side=tk.TOP, padx=10, pady=5)
    
    ###########################Tìm kiếm thống kê################################
    global entry_ma_the, combobox_ngay, combobox_thang, combobox_nam
    # Label "Tìm kiếm"
    label_tim_kiem = tk.Label(frame_tim_thke, text="Tìm kiếm", bg="white", font=label_font)
    label_tim_kiem.grid(row=0, column=0, padx=10, pady=10)

    # Entry nhập mã thẻ
    entry_ma_the = tk.Entry(frame_tim_thke,width=30)
    entry_ma_the.grid(row=0, column=1, padx=10, pady=10)

    # Checkbox "Tìm kiếm theo ngày"
    var_tim_ngay = tk.IntVar()  # Sửa đổi ở đây
    checkbox_ngay = tk.Checkbutton(frame_tim_thke, text="Tìm kiếm theo ngày", variable=var_tim_ngay, bg="white")
    checkbox_ngay.grid(row=1, column=0, padx=10, pady=10)

    # Checkbox "Tìm kiếm theo mã thẻ"
    var_tim_ma = tk.IntVar()  # Sửa đổi ở đây
    checkbox_ma_the = tk.Checkbutton(frame_tim_thke, text="Tìm kiếm theo mã thẻ", variable=var_tim_ma, bg="white")
    checkbox_ma_the.grid(row=2, column=0, padx=10, pady=10)


    # Label và Combobox cho ngày, tháng, năm
    label_ngay = tk.Label(frame_tim_thke, text="Ngày", bg="white", font=button_font)
    label_ngay.grid(row=3, column=0, padx=10, pady=10)

    combobox_ngay = ttk.Combobox(frame_tim_thke, values=list(range(1, 32)), width=10)
    combobox_ngay.grid(row=3, column=1, padx=10, pady=10)

    label_thang = tk.Label(frame_tim_thke, text="Tháng", bg="white", font=button_font)
    label_thang.grid(row=3, column=2, padx=10, pady=10)

    combobox_thang = ttk.Combobox(frame_tim_thke, values=list(range(1, 13)), width=10)
    combobox_thang.grid(row=3 ,column=3, padx=10, pady=10)

    label_nam = tk.Label(frame_tim_thke, text="Năm", bg="white", font=button_font)
    label_nam.grid(row=4, column=0, padx=10, pady=10)

    combobox_nam = ttk.Combobox(frame_tim_thke, values=list(range(2023, 2025)), width=10)
    combobox_nam.grid(row=4, column=1, padx=10, pady=10)

    # Button "Tìm kiếm"
    button_tim_kiem = tk.Button(frame_tim_thke, text="Tìm kiếm", command=lambda: search_data(entry_ma_the, var_tim_ma, var_tim_ngay, entry_tree, out_tree), font=button_font)
    button_tim_kiem.grid(row=0, column=2, padx=10, pady=10)
    
    
    ############################################################################
    page_frame.pack(fill=tk.BOTH, expand=True)
    return page_frame

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quản lý thẻ xe")
    root.geometry("800x600")

    create_gui(root)

    root.mainloop()