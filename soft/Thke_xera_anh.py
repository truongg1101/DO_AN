import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from tkinter import font
from datetime import datetime, timedelta
import time
import locale
from PIL import Image, ImageTk
from io import BytesIO
import pandas as pd

locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
# Kết nối đến cơ sở dữ liệu Python3 trên máy chủ LAGGER\CHIEN
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-BINPIL1;DATABASE=Python5;Trusted_Connection=yes;')
cursor = conn.cursor()

global clock_label
global lbl_so_xe_hom_nay
global lbl_so_xe_may_ra
global lbl_so_xe_oto_ra
day_combo = None
month_combo = None
year_combo = None

def show_detail_month():
    global page_frame
    def fetch_data():
        selected_month = int(month_cb.get())
        selected_year = int(year_cb.get())

        query = f"""
        SELECT LX.TenLoai, COUNT(XR.MaXeRa) as SoLuongXe
        FROM XeRa XR
        JOIN BienSo BS ON XR.MaBien = BS.MaBien
        JOIN LoaiXe LX ON BS.MaLoai = LX.MaLoai
        WHERE MONTH(XR.ThoiGianRa) = {selected_month} AND YEAR(XR.ThoiGianRa) = {selected_year}
        GROUP BY LX.TenLoai
        """

        df = pd.read_sql(query, conn)
#        conn.close()

        total_vehicles = df['SoLuongXe'].sum()
        ot_vehicles = df[df['TenLoai'] == 'Ô Tô']['SoLuongXe'].sum() if 'Ô Tô' in df['TenLoai'].values else 0
        xm_vehicles = df[df['TenLoai'] == 'Xe Máy']['SoLuongXe'].sum() if 'Xe Máy' in df['TenLoai'].values else 0

        result_text.set(f"Tổng số lượt ra của tháng: {total_vehicles}\n\nSố lượt Ô tô ra bãi: {ot_vehicles}\n\nSố lượt Xe máy ra bãi: {xm_vehicles}")

    # Tạo cửa sổ mới
    new_window = tk.Toplevel(page_frame, bg="white")
    new_window.title("Chi tiết lưu lượng xe theo tháng")
    
    # Tạo khung cho lựa chọn tháng và năm
    frame_selection = ttk.Frame(new_window, padding="10 10 10 10")
    frame_selection.pack(fill=tk.BOTH, expand=True)
    
    # Tạo combobox để chọn tháng
    ttk.Label(frame_selection, text="Chọn tháng:").grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
    month_cb = ttk.Combobox(frame_selection, values=[str(i) for i in range(1, 13)], state='readonly')
    month_cb.grid(column=1, row=0, padx=5, pady=5)
    month_cb.current(0)  # Set default value

    # Tạo combobox để chọn năm
     # Tạo combobox để chọn năm
    current_year = datetime.now().year
    year_values = [str(i) for i in range(2023, current_year + 1)]
    ttk.Label(frame_selection, text="Chọn năm:").grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)
    year_cb = ttk.Combobox(frame_selection, values=year_values, state='readonly')
    year_cb.grid(column=1, row=1, padx=5, pady=5)
    year_cb.current(len(year_values) - 1)  # Set default value to the most recent year

    # Tạo nút để lấy dữ liệu
    ttk.Button(frame_selection, text="Hiển thị", command=fetch_data).grid(column=0, row=2, columnspan=2, pady=10)

    # Kết quả hiển thị
    frame_result = ttk.Frame(new_window, padding="10 10 10 10")
    frame_result.pack(fill=tk.BOTH, expand=True)
    
    result_text = tk.StringVar()
    ttk.Label(frame_result, textvariable=result_text, justify=tk.LEFT, font=("Helvetica", 12)).pack(pady=10, padx=10)

def show_detail(event):
    global page_frame
    # Lấy dòng được chọn trong Treeview
    selected_item = tree.focus()

    # Lấy dữ liệu từ dòng được chọn
    data = tree.item(selected_item)
    if not data["values"]:
        return

    ma_xe_ra = data["values"][0]  # Lấy MaXeRa từ dữ liệu

    # Truy vấn dữ liệu từ bảng XeVao dựa trên MaXeVao
    cursor.execute("""
        SELECT XeRa.MaXeRa, XeRa.ThoiGianRa, XeRa.AnhRa, BienSo.SoBien, LoaiXe.TenLoai
        FROM XeRa
        JOIN BienSo ON XeRa.MaBien = BienSo.MaBien
        JOIN LoaiXe ON BienSo.MaLoai = LoaiXe.MaLoai
        WHERE XeRa.MaXeRa = ?
    """, (ma_xe_ra,))
    row = cursor.fetchone()

    if not row:
        messagebox.showerror("Lỗi", "Không tìm thấy thông tin lượt ra")
        return

    # Tạo cửa sổ mới để hiển thị thông tin chi tiết
    detail_window = tk.Toplevel(page_frame,bg="white")
    detail_window.title("Thông tin chi tiết lượt ra")
    detail_window.geometry("750x400")

    # Phân chia layout thành 2 phần
    frame_label = tk.Frame(detail_window, borderwidth=0, relief="raised",bg="white")
    frame_label.pack(side="top", fill="both", expand=True, padx=0, pady=10)

    frame_info = tk.Frame(detail_window, borderwidth=0, relief="raised",bg="white")
    frame_info.pack(side="bottom", fill="both", expand=True, padx=10, pady=0)

    # Định dạng lại thời gian để chỉ hiển thị đến giây
    formatted_time = row[1].strftime('%Y-%m-%d %H:%M:%S')
    
    # Tạo và cấu hình label
    label_ten = tk.Label(frame_label, bg="white",text="THÔNG TIN XE RA", font=("Helvetica", 20, "bold"))
    label_ten.place(relx=0.5, rely=0.5, anchor="center")

    # Hiển thị thông tin chi tiết
    frame_anh = tk.Frame(detail_window, bg="white",borderwidth=0, relief="solid")
    frame_anh.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    frame_thongtin = tk.Frame(detail_window, bg="white",borderwidth=0, relief="solid")
    frame_thongtin.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    info_label = tk.Label(frame_thongtin,bg="white",
                          text=f"Mã Xe Ra: {row[0]}\n\n"
                               f"Thời Gian Ra: {formatted_time}\n\n"
                               f"Số Biển: {row[3]}\n\n"
                               f"Loại Xe: {row[4]}",
                          font=("Arial", 16),
                          anchor="nw",
                          justify="left")
    info_label.pack(fill="both", expand=True, anchor="nw")

    # Hiển thị ảnh từ dữ liệu binary
    anh_ra_data = row[2]
    if anh_ra_data:
        image_data = BytesIO(anh_ra_data)
        img = Image.open(image_data)
        img = img.resize((300, 300), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(frame_anh, image=photo)
        img_label.image = photo  # Giữ tham chiếu tới ảnh để không bị garbage collected
        img_label.pack()
    else:
        no_image_label = tk.Label(frame_anh, bg="white",text="Không có ảnh")
        no_image_label.pack()

def get_total_out_today():
    # Lấy ngày hiện tại
    today_date = datetime.now().date()

    # Truy vấn cơ sở dữ liệu để lấy tổng số lượt ra hôm nay
    query = f"SELECT COUNT(*) FROM XeRa WHERE CAST(ThoiGianRa AS DATE) = '{today_date}'"
    cursor.execute(query)
    total_out = cursor.fetchone()[0]

    return total_out

def get_total_motorbike_out_today():
    # Lấy ngày hiện tại
    today_date = datetime.now().date()

    # Truy vấn cơ sở dữ liệu để lấy tổng số lượt xe máy ra hôm nay
    query = f"""
        SELECT COUNT(*) 
        FROM XeRa 
        JOIN BienSo ON XeRa.MaBien = BienSo.MaBien
        WHERE CAST(XeRa.ThoiGianRa AS DATE) = '{today_date}' AND BienSo.MaLoai = 'XM'
    """
    cursor.execute(query)
    total_motorbike_out = cursor.fetchone()[0]

    return total_motorbike_out

def get_total_car_out_today():
    # Lấy ngày hiện tại
    today_date = datetime.now().date()

    # Truy vấn cơ sở dữ liệu để lấy tổng số lượt ô tô vào hôm nay
    query = f"""
        SELECT COUNT(*) 
        FROM XeRa 
        JOIN BienSo ON XeRa.MaBien = BienSo.MaBien
        WHERE CAST(XeRa.ThoiGianRa AS DATE) = '{today_date}' AND BienSo.MaLoai = 'OT'
    """
    cursor.execute(query)
    total_car_out = cursor.fetchone()[0]

    return total_car_out
# Sau khi đã có các hàm trên, bạn có thể gọi chúng từ các nút hoặc hàm chức năng chính và cập nhật các label:
def update_total_out_labels():
    total_out = get_total_out_today()
    total_motorbike_out = get_total_motorbike_out_today()
    total_car_out = get_total_car_out_today()

    # Sử dụng biến toàn cục để cập nhật label
    global lbl_so_xe_hom_nay
    lbl_so_xe_hom_nay.config(text=f"Số xe ra hôm nay: {total_out if total_out > 0 else 0}", bg="white")

    global lbl_so_xe_may_ra
    lbl_so_xe_may_ra.config(text=f"Số xe máy ra: {total_motorbike_out if total_motorbike_out > 0 else 0}", bg="white")

    global lbl_so_xe_oto_ra
    lbl_so_xe_oto_ra.config(text=f"Số xe ô tô ra: {total_car_out if total_car_out > 0 else 0}", bg="white")

def update_clock(clock_label):
    current_time = time.strftime('%A, %d %B %Y,  %H:%M:%S')
    clock_label.config(text=current_time)
    clock_label.after(1000, update_clock, clock_label)  # Gọi lại hàm update_clock sau 1 giây

def load_recent_out(tree):
    # Xóa dữ liệu cũ trong treeview
    tree.delete(*tree.get_children())

    # Truy vấn dữ liệu từ bảng XeRa với 10 lượt vào gần nhất
    query = """
    SELECT TOP 10 MaXeRa, ThoiGianRa, SoBien 
    FROM XeRa 
    JOIN BienSo ON XeRa.MaBien = BienSo.MaBien 
    ORDER BY ThoiGianRa DESC
    """
    cursor.execute(query)
    xe_ra_data = cursor.fetchall()

    # Hiển thị dữ liệu từ XeRa trong Treeview
    for row in xe_ra_data:
        ma_xe_ra, thoi_gian_ra, so_bien = row
        thoi_gian_ra = thoi_gian_ra.strftime('%Y-%m-%d %H:%M:%S')
        tree.insert('', 'end', values=(ma_xe_ra, so_bien, thoi_gian_ra))
        
    tree.bind("<<TreeviewSelect>>", show_detail)

def load_today_out(tree):
    # Lấy ngày hiện tại
    today_date = datetime.now().date()

    # Lấy lượt ra của hôm nay
    query = f"SELECT MaXeRa, ThoiGianRa, SoBien FROM XeRa JOIN BienSo ON XeRa.MaBien = BienSo.MaBien WHERE CAST(ThoiGianRa AS DATE) = '{today_date}'"
    cursor.execute(query)
    xe_ra_data = cursor.fetchall()

    # Kiểm tra nếu không có lượt ra nào trong ngày hôm nay
    if not xe_ra_data:
        messagebox.showinfo("Thông báo", "Hôm nay chưa có lượt ra nào.")
        return

    # Hiển thị dữ liệu từ XeRa trong Treeview
    tree.delete(*tree.get_children())     
    for row in xe_ra_data:
        ma_xe_ra, thoi_gian_ra, so_bien = row
        thoi_gian_ra = thoi_gian_ra.strftime('%Y-%m-%d %H:%M:%S')
        tree.insert('', 'end', values=(ma_xe_ra, so_bien, thoi_gian_ra))
        
    tree.bind("<<TreeviewSelect>>", show_detail)

def load_data(xe_ra_tree):
    # Xóa dữ liệu cũ trong treeview
    for row in xe_ra_tree.get_children():
        xe_ra_tree.delete(row)
    tree.delete(*tree.get_children())
    # Truy vấn dữ liệu từ bảng XeRa
    cursor.execute("SELECT MaXeRa, ThoiGianRa, SoBien FROM XeRa JOIN BienSo ON XeRa.MaBien = BienSo.MaBien")
    xe_ra_data = cursor.fetchall()

    # Hiển thị dữ liệu từ XeRa trong Treeview
    for row in xe_ra_data:
        ma_xe_ra, thoi_gian_ra, so_bien = row
        thoi_gian_ra = thoi_gian_ra.strftime('%Y-%m-%d %H:%M:%S')
        tree.insert('', 'end', values=(ma_xe_ra, so_bien, thoi_gian_ra))
        
    tree.bind("<<TreeviewSelect>>", show_detail) 

def search_data(entry_value, checkbox_var_1, checkbox_var_2, tree):
    global day_combo, month_combo, year_combo
    query = "SELECT MaXeRa, ThoiGianRa, SoBien FROM XeRa JOIN BienSo ON XeRa.MaBien = BienSo.MaBien"
    if checkbox_var_1.get():
        so_bien = entry_value.get()
        if so_bien == "":
            messagebox.showwarning("Thông báo", "Vui lòng nhập biển số xe.")
            return
        query += f" WHERE SoBien = '{so_bien}'"

    if checkbox_var_2.get():
        if not checkbox_var_1.get():
            query += " WHERE"
        else:
            query += " AND"

        # Lấy giá trị của combobox ngày, tháng, năm
        day = day_combo.get()
        month = month_combo.get()
        year = year_combo.get()

        # Tạo chuỗi ngày tháng năm
        selected_date = f"'{year}-{month}-{day}'"

        # Thêm điều kiện cho ngày vào truy vấn
        query += f" CAST(ThoiGianRa AS DATE) = {selected_date}"

    cursor.execute(query)
    xe_ra_data = cursor.fetchall()
    for item in tree.get_children():
        tree.delete(item)
    # Hiển thị dữ liệu từ XeRa trong Treeview
    for row in xe_ra_data:
        ma_xe_ra, thoi_gian_ra, so_bien = row
        thoi_gian_ra = thoi_gian_ra.strftime('%Y-%m-%d %H:%M:%S')
        tree.insert('', 'end', values=(ma_xe_ra, so_bien, thoi_gian_ra))
        
    tree.bind("<<TreeviewSelect>>", show_detail)

def refresh_button_action():
    update_total_out_labels()
    get_total_car_out_today()
    get_total_motorbike_out_today()

def create_gui(parent):
    global page_frame
    page_frame = tk.Frame(parent)
    label_font = font.Font(family="Arial", size=14, weight="bold")
    info_font = font.Font(family="Arial", size = 12,weight="bold")
    clock_font = font.Font(family="Arial", size = 14,weight="bold")
    
    # CHIA KHUNG #####
    # Phần 1: Frame chứa thông tin (frame_info)
    frame_info = tk.Frame(page_frame)
    frame_info.grid(row=0, column=0, sticky="nsew", rowspan=4)

    # Phần 2: Frame chứa chức năng (frame_chucnang)
    frame_chucnang = tk.Frame(page_frame)
    frame_chucnang.grid(row=0, column=1, sticky="nsew", rowspan=4)

    # Thiết lập tỷ lệ kích thước cho cột 1 và cột 2
    page_frame.grid_columnconfigure(0, weight=2)
    page_frame.grid_columnconfigure(1, weight=4)

    # Thiết lập tỷ lệ kích thước cho hàng 1, 2, 3, 4
    for i in range(4):
        page_frame.grid_rowconfigure(i, weight=1)
        
    # Phần 1: Frame chứa thông tin (frame_timkiem)
    frame_timkiem = tk.Frame(frame_info)
    frame_timkiem.grid(row=0, column=0, sticky="nsew", columnspan= 4)

    # Phần 2: Frame chứa danh sách (frame_danhsach)
    frame_danhsach = tk.Frame(frame_info)
    frame_danhsach.grid(row=1, column=0, sticky="nsew", columnspan= 4)
    
    # Thiết lập tỷ lệ kích thước cho dòng 1 và dòng 2
    frame_info.grid_rowconfigure(0, weight=1)
    frame_info.grid_rowconfigure(1, weight=17)
    
    # Thiết lập tỷ lệ kích thước cho hàng 1, 2, 3, 4
    for i in range(4):
        frame_info.grid_columnconfigure(i, weight=1)
    
    # Phần 1: Frame chứa thông tin (frame_timkiem)
    frame_labelthongtin = tk.Frame(frame_chucnang)
    frame_labelthongtin.grid(row=0, column=0, sticky="nsew", columnspan= 4)

    # Phần 2: Frame chứa danh sách (frame_danhsach)
    frame_entry = tk.Frame(frame_chucnang)
    frame_entry.grid(row=1, column=0, sticky="nsew", columnspan= 4)
    
    # Thiết lập tỷ lệ kích thước cho dòng 1 và dòng 2
    frame_chucnang.grid_rowconfigure(0, weight=2)
    frame_chucnang.grid_rowconfigure(1, weight=2)
    
    # Thiết lập tỷ lệ kích thước cho hàng 1, 2, 3, 4
    for i in range(4):
        frame_chucnang.grid_columnconfigure(i, weight=1)    
    ###############
    
    ###CHIA Ô#######
    frame_timkiem1 = tk.Frame(frame_timkiem, bg="white",borderwidth=3, relief="ridge")
    frame_timkiem1.pack(fill="both",expand=True,padx=15,pady=15)
    frame_danhsach1 = tk.Frame(frame_danhsach,borderwidth=3, relief="ridge")
    frame_danhsach1.pack(fill="both",expand=True,padx=15,pady=15)
    frame_labelthongtin1 = tk.Frame(frame_labelthongtin, bg="white",borderwidth=3, relief="ridge")
    frame_labelthongtin1.pack(fill="both",expand=True,padx=15,pady=15)
    frame_labelthongtin1.grid_propagate(False)
    frame_entry1 = tk.Frame(frame_entry, bg="white",borderwidth=3, relief="ridge")
    frame_entry1.pack(fill="both",expand=True,padx=15,pady=15)
    frame_entry1.grid_propagate(False)
    ##################
    
    
    #####TÌM KIẾM##############
    # Phần tìm kiếm
    global day_combo, month_combo, year_combo
    lbl_timkiem = tk.Label(frame_timkiem1, bg="white", text="Tìm kiếm thông tin", font=label_font)
    lbl_timkiem.grid(row=0, column=0, padx=(10, 5), pady=(10, 5))

    entry_timkiem = tk.Entry(frame_timkiem1, bg="white", font=info_font)
    entry_timkiem.grid(row=0, column=1, padx=5, pady=(10, 5))

    btn_timkiem = tk.Button(frame_timkiem1, bg="white", text="Tìm kiếm", font=info_font, command=lambda: search_data(entry_timkiem, var_tim_bienso,var_tim_ngay,tree))
    btn_timkiem.grid(row=0, column=2, padx=(5, 10), pady=(10, 5))

    # Checkbox "Tìm theo biển số"
    var_tim_bienso = tk.IntVar()
    check_tim_bienso = tk.Checkbutton(frame_timkiem1, bg="white", text="Tìm theo biển số", variable=var_tim_bienso, font=info_font)
    check_tim_bienso.grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)

    # Checkbox "Tìm theo ngày"
    var_tim_ngay = tk.IntVar()
    check_tim_ngay = tk.Checkbutton(frame_timkiem1, bg="white", text="Tìm theo ngày", variable=var_tim_ngay, font=info_font)
    check_tim_ngay.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
    
    # Tạo label cho ngày
    label_day = tk.Label(frame_timkiem1, bg="white", text="Ngày:")
    label_day.grid(row=2, column=3, padx=5, pady=5)
    # Tạo Combobox cho ngày
    days = [str(day) for day in range(1, 32)]
    day_combo = ttk.Combobox(frame_timkiem1, values=days, width=2)
    day_combo.grid(row=2, column=4, padx=5, pady=5)

    # Tạo label cho tháng
    label_month = tk.Label(frame_timkiem1, bg="white", text="Tháng:")
    label_month.grid(row=2, column=5, padx=5, pady=5)
    # Tạo Combobox cho tháng
    months = [str(month) for month in range(1, 13)]
    month_combo = ttk.Combobox(frame_timkiem1, values=months, width=2)
    month_combo.grid(row=2, column=6, padx=5, pady=5)
    
    # Tạo label cho năm
    label_year = tk.Label(frame_timkiem1, bg="white", text="Năm:")
    label_year.grid(row=2, column=7, padx=5, pady=5)
    # Tạo Combobox cho năm
    years = [str(year) for year in range(2024, 2025)]
    year_combo = ttk.Combobox(frame_timkiem1, values=years, width=4)
    year_combo.grid(row=2, column=8, padx=5, pady=5)

    btn_referesh = tk.Button(frame_timkiem1, text="Tải lại", font=info_font, command=lambda: load_data(tree))
    btn_referesh.grid(row=3, column=0, padx=5, pady=5)
    ###########################
    global tree
    ########DANH SÁCH##########
    tree = ttk.Treeview(frame_danhsach1, columns=("STT", "BienSo", "ThoiGianRa"))
    tree.heading("#0", text="", anchor=tk.CENTER)
    tree.heading('STT', text='STT')
    tree.heading('BienSo', text='Biển số xe')
    tree.heading('ThoiGianRa', text='Thời gian ra')
    #tree.heading('MaXeRa', text='Mã xe ra')
    # Đặt font cho tiêu đề cột
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
    # Ẩn cột STT thứ hai
    tree.column("#0", width=0, stretch=tk.NO)
    tree.pack(fill="both", expand=True)
    tree.bind("<<TreeviewSelect>>", lambda event: show_detail())
    # Load dữ liệu
    load_data(tree)
    ###########################
    
    ########LABEL##############
    # Label đồng hồ
    global clock_label
    clock_label = tk.Label(frame_labelthongtin1, font=label_font, bg="white")
    clock_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
    update_clock(clock_label)  # Bắt đầu cập nhật đồng hồ
    global lbl_so_xe_hom_nay
    global lbl_so_xe_may_ra
    global lbl_so_xe_oto_ra
    # Label "Số xe vào hôm nay"
    lbl_so_xe_hom_nay = tk.Label(frame_labelthongtin1, text="Số xe ra hôm nay: ", font=label_font)
    lbl_so_xe_hom_nay.place(relx=0.36, rely=0.25, anchor=tk.CENTER)

    # Label "Số xe máy ra"
    lbl_so_xe_may_ra = tk.Label(frame_labelthongtin1, text="Số xe máy ra: ", font=label_font)
    lbl_so_xe_may_ra.place(relx=0.3, rely=0.4, anchor=tk.CENTER)

    # Label "Số xe ô tô ra"
    lbl_so_xe_oto_ra = tk.Label(frame_labelthongtin1, text="Số xe ô tô ra: ", font=label_font)
    lbl_so_xe_oto_ra.place(relx=0.3, rely=0.55, anchor=tk.CENTER)
    
    # Cập nhật dữ liệu cho các label
    update_total_out_labels()
    get_total_car_out_today()
    get_total_motorbike_out_today()
    ###########################
    
    ########ENTRY##########
    # Button "Hiển thị 10 lượt ra gần nhất"
    btn_recent_entries = tk.Button(frame_entry1, text="Hiển thị 10 lượt ra gần nhất",bg='#57a1f8', fg="white", font=info_font, command=lambda: load_recent_out(tree), width=30, height=2)
    btn_recent_entries.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    # Button "Hiển thị toàn bộ lượt ra hôm nay"
    btn_today_entries = tk.Button(frame_entry1, text="Hiển thị toàn bộ lượt ra hôm nay",bg='#57a1f8', fg="white", font=info_font, command=lambda: load_today_out(tree), width=30, height=2)
    btn_today_entries.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

    # Button "Hiển thị toàn bộ thông tin"
    btn_all_entries = tk.Button(frame_entry1, text="Hiển thị toàn bộ thông tin",bg='#57a1f8', fg="white", font=info_font, command=lambda: load_data(tree), width=30, height=2)
    btn_all_entries.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    
    # Button "Hiển thị theo tháng"
    btn_month_entries = tk.Button(frame_entry1, text="Hiển thị thông tin theo tháng", bg='#57a1f8', fg='white', border=1,font=info_font, command=show_detail_month, width=30, height=2)
    btn_month_entries.place(relx=0.5, rely=0.55, anchor=tk.CENTER)    

    # Button "Tải lại"
    btn_refresh = tk.Button(frame_entry1, text="Tải lại", bg='#00C957', fg="white", font=info_font, command=refresh_button_action, width=30, height=2)
    btn_refresh.place(relx=0.5, rely=0.70, anchor=tk.CENTER)

    ###########################
    
    
    page_frame.pack(fill=tk.BOTH, expand=True)
    return page_frame

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Thống kê xe ra")
    root.geometry("800x600")

    create_gui(root)

    root.mainloop()