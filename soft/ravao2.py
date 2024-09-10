import tkinter as tk
from datetime import datetime
import pyodbc
from module_recognize import detect_and_process_license_plate
import threading
from tkinter import font
import time
import locale
from PIL import Image, ImageTk
import serial
from tkinter import messagebox
import cv2
import io

# Thiết lập ngôn ngữ mặc định là tiếng Việt
locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')

global ser
global ser2

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-BINPIL1;DATABASE=Python5;Trusted_Connection=yes;')
cursor = conn.cursor()

global info_text_vao
info_text_vao = ""

global info_text_ra
info_text_ra = ""
image_label = None
# Label đồng hồ
global clock_label
global image_label_vao
global image_label_ra

def connect_arduino(port='COM5', baudrate=9600, timeout=1):
    global ser
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        messagebox.showinfo("Thông báo", f"Đã kết nối tới Arduino vào trên cổng {port}")
        print("Đã kết nối tới Arduino trên cổng", port)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi kết nối tới Arduino vào: {e}")
        print("Đã xảy ra lỗi khi kết nối tới Arduino:", e)

def end_connect():
    global ser
    try:
        ser.close()
        print("Đã ngắt kết nối tới Arduino")
        messagebox.showinfo("Thông báo", f"Đã đóng kết nối tới Arduino")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi đóng kết nối tới Arduino: {e}")
        print("Đã xảy ra lỗi khi ngắt kết nối tới Arduino:", e)

def connect_both():
    connect_arduino()
    connect_arduino2()
    
def end_both():
    end_connect()
    end_connect2()

def connect_arduino2(port='COM6', baudrate=9600, timeout=1):
    global ser2
    try:
        ser2 = serial.Serial(port, baudrate, timeout=timeout)
        messagebox.showinfo("Thông báo", f"Đã kết nối tới Arduino ra trên cổng {port}")
        print("Đã kết nối tới Arduino trên cổng", port)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi kết nối tới Arduino: {e}")
        print("Đã xảy ra lỗi khi kết nối tới Arduino:", e)

def end_connect2():
    global ser2
    try:
        ser2.close()
        print("Đã ngắt kết nối tới Arduino")
        messagebox.showinfo("Thông báo", f"Đã đóng kết nối tới Arduino ra")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi đóng kết nối tới Arduino: {e}")
        print("Đã xảy ra lỗi khi ngắt kết nối tới Arduino:", e)

def send_command_to_arduino():
    try:
        if ser.is_open:
            ser.write(b'3')
            print("Đã gửi lệnh mở cổng ra bãi.")
        else:
            print("Chưa kết nối tới Arduino. Không thể gửi lệnh.")
    except Exception as e:
        print("Đã xảy ra lỗi khi gửi lệnh tới Arduino:", e)

def lcd_bien(license_plate):
    try:
        if ser.is_open:
            # Gửi thông tin biển số qua cổng serial
            ser.write(license_plate.encode())
            print("Đã gửi thông tin biển số tới Arduino:", license_plate)
        else:
            print("Chưa kết nối tới Arduino. Không thể gửi lệnh.")
    except Exception as e:
        print("Đã xảy ra lỗi khi gửi lệnh tới Arduino:", e)

def send_command_to_arduino2():
    try:
        if ser2.is_open:
            ser2.write(b'3')
            print("Đã gửi lệnh mở cổng ra bãi.")
        else:
            print("Chưa kết nối tới Arduino. Không thể gửi lệnh.")
    except Exception as e:
        print("Đã xảy ra lỗi khi gửi lệnh tới Arduino:", e)

def update_clock(clock_label):
    current_time = time.strftime('%A, %d %B %Y,  %H:%M:%S')
    clock_label.config(text=current_time)
    clock_label.after(1000, update_clock, clock_label)  

def them_xe_vao():
    threading.Thread(target=process_license_plate_and_update_label_vao).start()

def xe_ra_bai():
    threading.Thread(target=process_license_plate_and_update_label_ra).start()
    
def clear_image(image_label_vao):
    image_label_vao.configure(image=None)

def update_image(image_label_vao):
    try:
        image = Image.open("crop.jpg")
        image = ImageTk.PhotoImage(image)
        image_label_vao.configure(image=image)
        image_label_vao.image = image
        image_label_vao.after(7000, lambda: clear_image(image_label_vao))
    except FileNotFoundError:
        print("Không tìm thấy file crop.jpg")

def update_image_ra(image_label_ra):
    try:
        image = Image.open("crop.jpg")
        image = ImageTk.PhotoImage(image)
        image_label_ra.configure(image=image)
        image_label_ra.image = image
        image_label_ra.after(7000, lambda: clear_image(image_label_ra))
    except FileNotFoundError:
        print("Không tìm thấy file crop.jpg")

def clear_image_ra(image_label_ra):
    image_label_ra.configure(image=None)

def capture_image():
    camera = cv2.VideoCapture(1) 
    return_value, image = camera.read()
    camera.release()

    if return_value:
        # Chuyển ảnh thành bytes
        ret, buf = cv2.imencode('.jpg', image)
        image_bytes = buf.tobytes()
        return image_bytes
    else:
        print("Không thể chụp ảnh từ camera.")
        return None

def them_xe_vao_thu_cong():
    threading.Thread(target=vao_thu_cong).start()
    
def vao_thu_cong():
    global page_frame
    def on_submit():
        ma_bien = ma_bien_var.get()
        so_bien = so_bien_var.get()
        ten_cu_dan = ten_cu_dan_var.get()
        dia_chi = dia_chi_var.get()
        
        if ma_bien and so_bien and ten_cu_dan and dia_chi:
            try:
                # Truy vấn cơ sở dữ liệu để kiểm tra thông tin
                cursor.execute("""
                    SELECT BienSo.MaBien, BienSo.SoBien, BienSo.TrangThai
                    FROM BienSo
                    WHERE BienSo.MaBien = ? AND BienSo.SoBien = ?
                """, (ma_bien, so_bien))
                row = cursor.fetchone()
                
                if row:
                    trang_thai = row[2]  # Trang thái của biển số
                    if trang_thai == 1:
                        print('Lỗi, xe đang ở trong bãi xe \nYêu cầu kiểm tra lại xe trong bãi hoặc biển số xe.')
                        messagebox.showerror("Lỗi", "Xe đang ở trong bãi xe\n Yêu cầu kiểm tra lại xe trong bãi hoặc biển số xe.")
                    else:
                        # Lấy ảnh vào (giả sử hàm capture_image() đã được định nghĩa)
                        image_bytes_in = capture_image()
                        
                        # Cập nhật thông tin vào cơ sở dữ liệu
                        cursor.execute("INSERT INTO XeVao (MaBien, ThoiGianVao, AnhVao) VALUES (?, CURRENT_TIMESTAMP, ?)", (ma_bien, image_bytes_in))
                        cursor.execute("UPDATE BienSo SET TrangThai = 1 WHERE MaBien = ?", (ma_bien,))
                        
                        print('Xe đã vào bãi thành công vào lúc', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        info_text_vao = f"Biển số: {so_bien}\nTên cư dân: {ten_cu_dan}\nĐịa chỉ: {dia_chi}\n\nXe đã vào bãi lúc {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        messagebox.showinfo("Thông tin", info_text_vao)
                        send_command_to_arduino()
                        print("Mở cửa")
                else:
                    print('Thông tin không hợp lệ. Không thể cho xe vào.')
                    messagebox.showerror("Lỗi", "Thông tin không hợp lệ. Không thể cho xe vào.")    
                conn.commit()
            except Exception as e:
                print('Đã xảy ra lỗi:', e)
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi về dữ liệu nhập!")
        else:
            print("Vui lòng điền đầy đủ thông tin.")
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin.")

    # Tạo cửa sổ chính
    manual_window = tk.Toplevel(page_frame,bg="white")
    manual_window.title("Vào thủ công")
    manual_window.geometry("350x250")

    # Tạo các biến để lưu trữ giá trị
    ma_bien_var = tk.StringVar()
    so_bien_var = tk.StringVar()
    ten_cu_dan_var = tk.StringVar()
    dia_chi_var = tk.StringVar()

    # Tạo giao diện người dùng
    frame = tk.Frame(manual_window, bg="white", padx=10, pady=10)
    frame.grid(row=0, column=0, sticky="nsew")

    tk.Label(frame, text="Mã biển số:", bg="white").grid(row=0, column=0, sticky="w", pady=5)
    tk.Entry(frame, textvariable=ma_bien_var, width=40).grid(row=0, column=1, sticky="w", pady=5)

    tk.Label(frame, text="Số biển số:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
    tk.Entry(frame, textvariable=so_bien_var, width=40).grid(row=1, column=1, sticky="w", pady=5)

    tk.Label(frame, text="Tên cư dân:", bg="white").grid(row=2, column=0, sticky="w", pady=5)
    tk.Entry(frame, textvariable=ten_cu_dan_var, width=40).grid(row=2, column=1, sticky="w", pady=5)

    tk.Label(frame, text="Địa chỉ:", bg="white").grid(row=3, column=0, sticky="w", pady=5)
    tk.Entry(frame, textvariable=dia_chi_var, width=40).grid(row=3, column=1, sticky="w", pady=5)

    tk.Button(frame, text="Cho xe vào", command=on_submit, font=("Arial", 14, "bold"), bg="#00C957", fg="white", padx=10, pady=5).grid(row=4, column=0, columnspan=2, pady=10)

    lbl_info_vao = tk.Label(frame, text="", bg="white")
    lbl_info_vao.grid(row=5, column=0, columnspan=2, sticky="w", pady=5)

def cam_bien():
    while True:
        if ser.in_waiting > 0:  # Kiểm tra nếu có dữ liệu sẵn sàng để đọc
            data = ser.readline().decode('utf-8').strip()
            print(data)  # In giá trị cảm biến
            return data  # Trả về giá trị cảm biến nếu đã đọc được

        # Chờ một chút trước khi đọc lại
        time.sleep(0.05)  # Giảm thời gian chờ để tăng tốc độ đọc dữ liệu

def process_license_plate_and_update_label_vao():
    global info_text_vao
    generator = detect_and_process_license_plate()  # Lưu trữ generator
    for bien_so in generator:  # Lặp qua từng biển số đã nhận dạng
        ir_sensor_value = cam_bien()  # Đọc giá trị từ cảm biến
        update_image(image_label_vao)
        if bien_so:
            try:
                print(f"Nhận diện được biển số: {bien_so}")
                cursor.execute("""
                        SELECT BienSo.MaBien, BienSo.SoBien, XeVao.ThoiGianVao, CuDan.TenCuDan, CuDan.DiaChi, LoaiXe.TenLoai, BienSo.TrangThai
                        FROM BienSo
                        LEFT JOIN XeVao ON XeVao.MaBien = BienSo.MaBien
                        JOIN CuDan ON CuDan.MaBien = BienSo.MaBien
                        JOIN LoaiXe ON LoaiXe.MaLoai = BienSo.MaLoai
                        WHERE BienSo.SoBien = ?
                    """, (bien_so,))
                row = cursor.fetchone()
                print(f"Kết quả truy vấn: {row}")
                if row:
                    ma_bien = row[0]
                    trang_thai = row[6]  # Trang thái của biển số
                    if trang_thai == 1:
                        print('Lỗi, xe đang ở trong bãi xe \nYêu cầu kiểm tra lại xe trong bãi hoặc biển số xe.')
                        info_text_vao = "Lỗi, xe đang ở trong bãi xe, yêu cầu kiểm tra lại xe trong bãi hoặc biển số xe."
                        lbl_info_vao.config(text=info_text_vao)  # Cập nhật nội dung của label
                        lbl_info_vao.after(7000, clear_info_label_vao)
                    else:
                        ten_cu_dan = row[3]  # Tên cư dân
                        dia_chi = row[4]  # Địa chỉ
                        loai_xe = row[5]  # Loại xe
                        image_bytes_in = capture_image()
                        cursor.execute("INSERT INTO XeVao (MaBien, ThoiGianVao, AnhVao) VALUES (?, CURRENT_TIMESTAMP, ?)", (ma_bien, image_bytes_in))
                        cursor.execute("UPDATE BienSo SET TrangThai = 1 WHERE MaBien = ?", (ma_bien,))
                        print('Xe đã vào bãi thành công vào lúc', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        info_text_vao = f"Biển số: {bien_so}\nTên cư dân: {ten_cu_dan}\nĐịa chỉ: {dia_chi}\nLoại xe: {loai_xe}\n\nXe đã vào bãi lúc {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        lbl_info_vao.config(text=info_text_vao)  # Cập nhật nội dung của label
                        lbl_info_vao.after(7000, clear_info_label_vao)
                        # lcd_bien(bien_so)
                        send_command_to_arduino()
                        print("Mở cửa")
                else:
                    print('Biển số không tồn tại trong cơ sở dữ liệu. Không thể cho xe vào.')
                    info_text_vao = "Biển số không tồn tại trong cơ sở dữ liệu. Không thể cho xe vào."
                    lbl_info_vao.config(text=info_text_vao)  # Cập nhật nội dung của label
                    lbl_info_vao.after(7000, clear_info_label_vao)
                conn.commit()
            except Exception as e:
                print('Đã xảy ra lỗi:', e)
                info_text_vao = "Đã xảy ra lỗi: " + str(e)
                lbl_info_vao.config(text=info_text_vao)  # Cập nhật nội dung của label
                lbl_info_vao.after(7000, clear_info_label_vao)
        else:
            print("Không thể nhận diện biển số xe.")
            info_text_vao = "Không thể nhận diện biển số xe."
            lbl_info_vao.config(text=info_text_vao)  # Cập nhật nội dung của label
            lbl_info_vao.after(7000, clear_info_label_vao)

def clear_info_label_vao():
    global info_text_vao
    info_text_vao = ""
    lbl_info_vao.config(text="")

def process_license_plate_and_update_label_ra():
    global info_text_ra
    generator = detect_and_process_license_plate()  # Lưu trữ generator
    for bien_so in generator:  # Lặp qua từng biển số đã nhận dạng
        update_image_ra(image_label_ra)
        if bien_so:
            try:
                cursor.execute("""
                        SELECT TOP 1 BienSo.MaBien, BienSo.SoBien, XeVao.ThoiGianVao, CuDan.TenCuDan, CuDan.DiaChi, LoaiXe.TenLoai
                        FROM BienSo
                        JOIN XeVao ON XeVao.MaBien = BienSo.MaBien
                        JOIN CuDan ON CuDan.MaBien = BienSo.MaBien
                        JOIN LoaiXe ON LoaiXe.MaLoai = BienSo.MaLoai
                        WHERE BienSo.SoBien = ? AND TrangThai = 1
                        ORDER BY XeVao.ThoiGianVao DESC  -- Sắp xếp theo thời gian vào giảm dần
                    """, (bien_so,))
                row = cursor.fetchone()

                if row:
                    image_bytes_out = capture_image()
                    ma_bien = row[0]
                    ten_cu_dan = row[3]  # Tên cư dân
                    dia_chi = row[4]  # Địa chỉ
                    loai_xe = row[5]  # Loại xe
                    cursor.execute("UPDATE BienSo SET TrangThai = 0 WHERE MaBien = ?", (ma_bien,))
                    cursor.execute("INSERT INTO XeRa (MaBien, ThoiGianRa, AnhRa) VALUES (?, CURRENT_TIMESTAMP, ?)", (ma_bien,image_bytes_out))
                    
                    thoi_gian_vao = row[2]  # Thời gian vào từ kết quả truy vấn
                    
                    print('Xe đã ra khỏi bãi vào lúc', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    print('Thời gian vào bãi:', thoi_gian_vao.strftime('%Y-%m-%d %H:%M:%S'))
                    send_command_to_arduino2()
                    print("Mở cổng ra")
                    info_text_ra = f"Biển số: {bien_so}\nTên cư dân: {ten_cu_dan}\nĐịa chỉ: {dia_chi}\nLoại xe: {loai_xe}\n\nXe đã ra khỏi bãi vào lúc {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nThời gian vào bãi: {thoi_gian_vao.strftime('%Y-%m-%d %H:%M:%S')}"
                    lbl_info_ra.config(text=info_text_ra)
                    lbl_info_ra.after(7000, clear_info_label_ra)
                else:
                    print('Xe không có ở trong bãi.')
                    info_text_ra = "Xe không có ở trong bãi."
                    lbl_info_ra.config(text=info_text_ra)
                    lbl_info_ra.after(7000, clear_info_label_ra)

                conn.commit()
            except Exception as e:
                print('Đã xảy ra lỗi:', e)
                info_text_ra = 'Đã xảy ra lỗi: ' + str(e)
                lbl_info_ra.config(text=info_text_ra)
                lbl_info_ra.after(7000, clear_info_label_ra)
        else:
            print("Không thể nhận diện biển số xe.")
            info_text_ra = 'Không thể nhận diện biển số xe.'
            lbl_info_ra.config(text=info_text_ra)
            lbl_info_ra.after(7000, clear_info_label_ra)

def cho_xe_ra_thu_cong():
    threading.Thread(target=ra_thu_cong).start()
    
def ra_thu_cong():
    global page_frame
    def on_submit():
        ma_bien = ma_bien_var.get()
        so_bien = so_bien_var.get()
        ten_cu_dan = ten_cu_dan_var.get()
        dia_chi = dia_chi_var.get()
        
        if ma_bien and so_bien and ten_cu_dan and dia_chi:
            try:
                # Truy vấn cơ sở dữ liệu để kiểm tra thông tin
                cursor.execute("""
                    SELECT TOP 1 BienSo.MaBien, BienSo.SoBien, BienSo.TrangThai
                    FROM BienSo
                    JOIN XeVao ON BienSo.MaBien = XeVao.MaBien
                    WHERE BienSo.MaBien = ? AND BienSo.SoBien = ?
                    ORDER BY XeVao.ThoiGianVao DESC
                """, (ma_bien, so_bien))


                row = cursor.fetchone()
                
                if row:
                    trang_thai = row[2]  # Trang thái của biển số
                    if trang_thai == 0:
                        print('Lỗi, xe không ở trong bãi xe \nYêu cầu kiểm tra lại xe trong bãi hoặc biển số xe.')
                        messagebox.showerror("Lỗi", "Xe không ở trong bãi xe\n Yêu cầu kiểm tra lại xe trong bãi hoặc biển số xe.")
                    else:
                        # Lấy ảnh ra (giả sử hàm capture_image() đã được định nghĩa)
                        image_bytes_out = capture_image()
                        
                        # Cập nhật thông tin vào cơ sở dữ liệu
                        cursor.execute("INSERT INTO XeRa (MaBien, ThoiGianRa, AnhRa) VALUES (?, CURRENT_TIMESTAMP, ?)", (ma_bien, image_bytes_out))
                        cursor.execute("UPDATE BienSo SET TrangThai = 0 WHERE MaBien = ?", (ma_bien,))
                        
                        print('Xe đã ra khỏi bãi thành công vào lúc', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        info_text_ra = f"Biển số: {so_bien}\nXe đã ra khỏi bãi lúc {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        messagebox.showinfo("Thông tin", info_text_ra)
                        send_command_to_arduino2()
                        print("Đóng cửa")
                else:
                    print('Thông tin không hợp lệ. Không thể cho xe ra.')
                    messagebox.showerror("Lỗi", "Thông tin không hợp lệ. Không thể cho xe ra.")    
                conn.commit()
            except Exception as e:
                print('Đã xảy ra lỗi:', e)
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi về dữ liệu nhập!")

    # Tạo cửa sổ chính
    manual_window = tk.Toplevel(page_frame,bg="white")
    manual_window.title("Ra thủ công")
    manual_window.geometry("350x250")

    # Tạo các biến để lưu trữ giá trị
    ma_bien_var = tk.StringVar()
    so_bien_var = tk.StringVar()
    ten_cu_dan_var = tk.StringVar()
    dia_chi_var = tk.StringVar()

    # Tạo giao diện người dùng
    frame = tk.Frame(manual_window, bg="white", padx=10, pady=10)
    frame.grid(row=0, column=0, sticky="nsew")

    tk.Label(frame, text="Mã biển số:", bg="white").grid(row=0, column=0, sticky="w", pady=5)
    tk.Entry(frame, textvariable=ma_bien_var, width=40).grid(row=0, column=1, sticky="w", pady=5)

    tk.Label(frame, text="Số biển số:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
    tk.Entry(frame, textvariable=so_bien_var, width=40).grid(row=1, column=1, sticky="w", pady=5)

    tk.Label(frame, text="Tên cư dân:", bg="white").grid(row=2, column=0, sticky="w", pady=5)
    tk.Entry(frame, textvariable=ten_cu_dan_var, width=40).grid(row=2, column=1, sticky="w", pady=5)

    tk.Label(frame, text="Địa chỉ:", bg="white").grid(row=3, column=0, sticky="w", pady=5)
    tk.Entry(frame, textvariable=dia_chi_var, width=40).grid(row=3, column=1, sticky="w", pady=5)

    tk.Button(frame, text="Cho xe ra", command=on_submit, font=("Arial", 14, "bold"), bg="#FF3030", fg="white", padx=10, pady=5).grid(row=4, column=0, columnspan=2, pady=10)

    lbl_info_ra = tk.Label(frame, text="", bg="white")
    lbl_info_ra.grid(row=5, column=0, columnspan=2, sticky="w", pady=5)

def clear_info_label_ra():
    global info_text_ra
    info_text_ra = ""
    lbl_info_ra.config(text="")

def create_gui(parent):
    global page_frame
    page_frame = tk.Frame(parent)
    label_font = font.Font(family="Arial", size=14, weight="bold")
    info_font = font.Font(family="Arial", size = 12,weight="bold")
    ##############################################################################################
    # Tạo pack cổng vào
    frame_vao = tk.Frame(page_frame,borderwidth=1, relief="solid")
    frame_vao.pack(side="left", fill="both", expand=True)

    # Tạo frame lable vao
    frame_label_vao = tk.Frame(frame_vao,bg="white", borderwidth=0, relief="solid")
    frame_label_vao.place(x=0,rely=0.7, relwidth=1, relheight=0.3)    
    # Tạo frame thông tin vao
    frame_thongtin_vao = tk.Frame(frame_vao,bg="white", borderwidth=0, relief="solid")
    frame_thongtin_vao.place(x=0,rely=0.1, relwidth=1, relheight=0.6)
    # Tạo frame button vao
    frame_button_vao = tk.Frame(frame_vao,bg="white", borderwidth=0, relief="solid")
    frame_button_vao.place(x=0,y=0, relwidth= 1, relheight= 0.1)
    #frame info vao
    frame_info_vao = tk.Frame(frame_label_vao, borderwidth=3, relief="raised")
    frame_info_vao.place(relx=0.05, rely= 0.3, relheight=0.65, relwidth=0.55)
    # Tạo frame video vao 
    #frame_video_vao = tk.Frame(frame_thongtin_vao,borderwidth=3, relief="raised")
    #frame_video_vao.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
    # Tạo frame ảnh biển vào
    frame_anh_vao = tk.Frame(frame_label_vao, borderwidth=3, relief="raised")
    frame_anh_vao.place(relx=0.65, rely=0.3,relheight=0.65, relwidth=0.3) 
    
    # Button "Xe vào"
    btn_vao = tk.Button(frame_button_vao,bg="#00C957",fg="white", text="Xe Vào", font=label_font, width=10, height=2, command=main)
    btn_vao.pack(side="left", padx=10,pady=20)

    btn_vao_thu_cong = tk.Button(frame_button_vao,bg="#00C957",fg="white", text="Thủ công", font=label_font, width=10, height=2, command=them_xe_vao_thu_cong)
    btn_vao_thu_cong.pack(side="left", padx=10,pady=20)
    
    # Label đồng hồ
    global clock_label
    clock_label = tk.Label(frame_button_vao,bg="white", font=label_font)
    clock_label.pack(side="right",padx=20, pady=20)
    update_clock(clock_label)  # Bắt đầu cập nhật đồng hồ
    
    # Label thông tin cổng vào
    global lbl_info_vao
    lbl_info_vao = tk.Label(frame_info_vao, text=info_text_vao, justify="left", wraplength=500, font = info_font)   
    lbl_info_vao.pack(side="left", pady=10, padx=15)
    
    lbl_info_vao2 = tk.Label(frame_label_vao,bg="white", text="Thông tin cổng vào", justify="left", wraplength=300, font=label_font)
    lbl_info_vao2.place(relx = 0.05, rely=0.1)
    # Label "Biển số vào"
    lbl_anh_vao = tk.Label(frame_label_vao,bg="white", text="Biển số vào", justify="left", wraplength=300, font=label_font)
    lbl_anh_vao.place(relx = 0.65, rely=0.1)
    
    # Tạo label để hiển thị ảnh vào
    global image_label_vao
    image_label_vao = tk.Label(frame_anh_vao)
    image_label_vao.pack(fill="both", expand=True)
    
    ################################################################################################
    # Tạo pack cổng ra
    frame_ra = tk.Frame(page_frame,borderwidth=1, relief="solid")
    frame_ra.pack(side="right", fill="both", expand=True)

    # Tạo frame lable ra
    frame_label_ra = tk.Frame(frame_ra,bg="white", borderwidth=0, relief="solid")
    frame_label_ra.place(x=0,rely=0.7, relwidth=1, relheight=0.3)
    # Tạo frame thông tin ra
    frame_thongtin_ra = tk.Frame(frame_ra,bg="white", borderwidth=0, relief="solid")
    frame_thongtin_ra.place(x=0,rely=0.1, relwidth=1, relheight=0.6)
    # Tạo frame anh ra
    frame_anh_ra = tk.Frame(frame_thongtin_ra,borderwidth=0,bg="grey", relief="raised")
    frame_anh_ra.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
    global image_label  # Sử dụng biến global image_label
    image_label = tk.Label(frame_anh_ra)
    image_label.pack(fill=tk.BOTH, expand=True)
    # Tạo frame button ra
    frame_button_ra = tk.Frame(frame_ra,bg="white", borderwidth=0, relief="solid")
    frame_button_ra.place(x=0,y=0, relwidth= 1, relheight= 0.1)
    #frame info ra
    frame_info_ra = tk.Frame(frame_label_ra, borderwidth=3, relief="raised")
    frame_info_ra.place(relx=0.05, rely= 0.3, relheight=0.65, relwidth=0.55)
    # Tạp frame video ra
    #frame_video_ra = tk.Frame(frame_thongtin_ra,borderwidth=3, relief="raised")
    #frame_video_ra.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
    # Tạo frame ảnh biển ra
    frame_anh_ra = tk.Frame(frame_label_ra, borderwidth=3, relief="raised")
    frame_anh_ra.place(relx=0.65, rely=0.3,relheight=0.65, relwidth=0.3)
    
    # Button "Xe ra"
    btn_ra = tk.Button(frame_button_ra,bg="#FF3030",fg="white", text="Xe Ra", font=label_font, width=10, height=2, command=xe_ra_bai)
    btn_ra.pack(side="left", padx=20,pady=20)

    btn_ra_thu_cong = tk.Button(frame_button_ra,bg="#FF3030",fg="white", text="Thủ công", font=label_font, width=10, height=2, command = cho_xe_ra_thu_cong)
    btn_ra_thu_cong.pack(side="left", padx=10,pady=20)

    btn_end = tk.Button(frame_button_ra,bg="#FF3030",fg="white", text="Đóng kêt nối", font=label_font, width=10, height=2, command=end_both)
    btn_end.pack(side="right", padx=20,pady=20)

#    btn_start = tk.Button(frame_button_ra,bg="#00C957",fg="white", text="Kết nối", font=label_font, width=10, height=2, command=connect_arduino)
    btn_start = tk.Button(frame_button_ra,bg="#00C957",fg="white", text="Kết nối", font=label_font, width=10, height=2, command=connect_both)
    btn_start.pack(side="right", padx=20,pady=20)
     
    # Label thông tin cổng ra
    global lbl_info_ra
    lbl_info_ra = tk.Label(frame_info_ra, text=info_text_ra, justify="left", wraplength=500,font=info_font)
    lbl_info_ra.pack(side="left", pady=10, padx=15)
    
    lbl_info_ra2 = tk.Label(frame_label_ra,bg="white", text="Thông tin cổng ra", justify="left", wraplength=300, font=label_font)
    lbl_info_ra2.place(relx = 0.05, rely=0.1)
    # Tạo label biển số ra
    lbl_anh_ra = tk.Label(frame_label_ra,bg="white", text="Biển số ra", justify="left", wraplength=300, font=label_font)
    lbl_anh_ra.place(relx = 0.65, rely=0.1)

    # Tạo label để hiển thị ảnh ra
    global image_label_ra
    image_label_ra = tk.Label(frame_anh_ra)
    image_label_ra.pack(fill="both", expand=True)
    #################################################################################################
    page_frame.pack(fill=tk.BOTH, expand=True)

    return page_frame

def process_entry(card_id):
    global info_text_vao
    try:
        cursor.execute("SELECT status FROM CARD_DATA WHERE card_id = ?", (card_id,))
        status = cursor.fetchone()

        if status and status[0] == 0:
            # Chụp ảnh và lưu vào trường image của thẻ
            image_bytes = capture_image()
            if image_bytes:
                # Cập nhật ảnh vào bảng CARD_DATA
                cursor.execute("UPDATE CARD_DATA SET image = ? WHERE card_id = ?", (image_bytes, card_id))

                # Thêm dữ liệu vào bảng Entry
                entry_time = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),)
                cursor.execute("INSERT INTO Entry (entry_time, entry_photo, card_id) VALUES (CURRENT_TIMESTAMP, ?, ?)",
                               (image_bytes, card_id))
                # Cập nhật status thành 1
                cursor.execute("UPDATE CARD_DATA SET status = 1 WHERE card_id = ?", (card_id,))
                
                info_text_vao = f"Mã thẻ: {card_id}\n\nThời gian vào: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                # Cập nhật thông tin trên các label trong frame_info_vao
                lbl_info_vao.config(text=info_text_vao)
                lbl_info_vao.after(7000, clear_info_label_vao)
        else:
            print("Thẻ không hợp lệ hoặc đã được sử dụng.")
            info_text_vao = "Thẻ không hợp lệ hoặc đã được sử dụng."
            lbl_info_vao.config(text=info_text_vao)  # Cập nhật nội dung của label
            lbl_info_vao.after(7000, clear_info_label_vao)
        conn.commit()
    except Exception as e:
        print("Lỗi khi thao tác với cơ sở dữ liệu:", e)
        info_text_vao = "Đã xảy ra lỗi: " + str(e)
        lbl_info_vao.config(text=info_text_vao)  # Cập nhật nội dung của label
        lbl_info_vao.after(7000, clear_info_label_vao)
        conn.rollback()  # Rollback thay đổi nếu có lỗi

def capture_image_out():
    camera = cv2.VideoCapture(1)  # Webcam laptop
    return_value, image = camera.read()
    camera.release()

    if return_value:
        # Chuyển ảnh thành bytes
        ret, buf = cv2.imencode('.jpg', image)
        image_bytes_out = buf.tobytes()
        return image_bytes_out
    else:
        print("Không thể chụp ảnh từ camera.")
        return None

def process_exit(card_id):
    global info_text_ra
    global image_label  # Sử dụng biến global image_label
    try:
        cursor.execute("SELECT status, image FROM CARD_DATA WHERE card_id = ?", (card_id,))
        result = cursor.fetchone()

        if result and result[0] == 1:
            # Thực hiện các hành động khi thẻ ra
            image_bytes = result[1]
            if image_bytes:
                # Chuyển đổi dữ liệu ảnh từ bytes sang định dạng hình ảnh phù hợp cho tkinter
                image_pil = Image.open(io.BytesIO(image_bytes))
                image_tk = ImageTk.PhotoImage(image_pil)
                
                # Cập nhật Label với ảnh mới
                image_label.configure(image=image_tk)
                image_label.image = image_tk  # Đảm bảo giữ tham chiếu đến ảnh để tránh bị giải phóng bộ nhớ
#                parent.after(6000, clear_image)

            cursor.execute("UPDATE CARD_DATA SET status = 0, image = NULL WHERE card_id = ?", (card_id,))
            
            # Chụp ảnh khi thẻ ra và lưu vào trường exit_photo của bảng OUT
            exit_photo = capture_image_out()
            if exit_photo:
                # Thêm dữ liệu vào bảng Out
                exit_time = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                cursor.execute("INSERT INTO OUT (card_id, exit_time, exit_photo) VALUES (?, ?, ?)", (card_id, exit_time, exit_photo))

                cursor.execute("SELECT TOP 1 entry_time FROM Entry WHERE card_id = ? ORDER BY entry_time DESC", (card_id,))
                entry_time = cursor.fetchone()[0]

                info_text_ra = f"Mã thẻ: {card_id}\n\nThời gian vào: {entry_time.strftime('%Y-%m-%d %H:%M:%S')}\nThời gian ra: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                lbl_info_ra.config(text=info_text_ra)
                lbl_info_ra.after(7000, clear_info_label_ra)
            else:
                print("Không thể chụp ảnh từ camera.")
                info_text_ra = "Không thể chụp ảnh từ camera."
                lbl_info_ra.config(text=info_text_ra)
                lbl_info_ra.after(7000, clear_info_label_ra)
        else:
            print("Thẻ không hợp lệ hoặc chưa được sử dụng.")
            info_text_ra = "Thẻ không hợp lệ hoặc chưa được sử dụng."
            lbl_info_ra.config(text=info_text_ra)
            lbl_info_ra.after(7000, clear_info_label_ra)
        conn.commit()
    except Exception as e:
        print("Lỗi khi thao tác với cơ sở dữ liệu:", e)
        info_text_ra = "Đã xảy ra lỗi: " + str(e)
        lbl_info_ra.config(text=info_text_ra)
        lbl_info_ra.after(7000, clear_info_label_ra)
        conn.rollback()  # Rollback thay đổi nếu có lỗi

def read_rfid_in():
    global ser
    if ser is None or not ser.is_open:
        print("Chưa kết nối tới Arduino. Không thể đọc RFID.")
        return
    
    while True:
        rfid_data = ser.readline().decode().strip()

        if rfid_data.startswith("RFID Detected! Card UID:"):
            card_id = rfid_data.split(":")[1].strip().replace(" ", "")
            process_entry(card_id)
            print(card_id)

def read_rfid_out():
    global ser2
    if ser2 is None or not ser2.is_open:
        print("Chưa kết nối tới Arduino. Không thể đọc RFID.")
        return
    
    while True:
        rfid_data = ser2.readline().decode().strip()

        if rfid_data.startswith("RFID Detected! Card UID:"):
            card_id = rfid_data.split(":")[1].strip().replace(" ", "")
            process_exit(card_id)
            print(card_id)

def main():
    try:
        # Khởi tạo và chạy các luồng đọc RFID
        thread_in = threading.Thread(target=read_rfid_in)
        thread_in.start()

        # Nếu cần, khởi tạo và chạy luồng đọc RFID ra
        thread_out = threading.Thread(target=read_rfid_out)
        thread_out.start()
        
        # Khởi tạo và chạy luồng xử lý nhận diện biển số xe
        threading.Thread(target=them_xe_vao).start()
        #Chờ cho các luồng hoàn thành
        #thread_in.join()
        #thread_out.join()
        
    except KeyboardInterrupt:
        # Ngắt khi nhận phím tắt từ người dùng
        print("Đã dừng bởi người dùng.")

    # Đóng kết nối cơ sở dữ liệu khi kết thúc chương trình


def main2():
    try:
        # Khởi tạo và chạy các luồng đọc RFID
        thread_in = threading.Thread(target=read_rfid_in)
        thread_in.start()

        # Nếu cần, khởi tạo và chạy luồng đọc RFID ra
        thread_out = threading.Thread(target=read_rfid_out)
        thread_out.start()
        
        # Khởi tạo và chạy luồng xử lý nhận diện biển số xe
        threading.Thread(target=xe_ra_bai).start()
        #Chờ cho các luồng hoàn thành
        #thread_in.join()
        #thread_out.join()
        
    except KeyboardInterrupt:
        # Ngắt khi nhận phím tắt từ người dùng
        print("Đã dừng bởi người dùng.")

    # Đóng kết nối cơ sở dữ liệu khi kết thúc chương trình

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quản lý bãi đỗ xe")
    root.geometry("800x600")

    create_gui(root)

    root.mainloop()
