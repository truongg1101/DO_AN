import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyodbc
from tkinter import simpledialog
from tkinter import filedialog
from PIL import Image, ImageTk
from io import BytesIO

def createGUI(parent):
    # Kết nối đến CSDL
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-BINPIL1;DATABASE=Python5;Trusted_Connection=yes;')
    cursor = conn.cursor()
    
    def show_detail_plate():
        # Lấy dòng được chọn trong Treeview
        selected_item = bien_so_tree.focus()

        # Lấy dữ liệu từ dòng được chọn
        data = bien_so_tree.item(selected_item)
        ma_bien = data["values"][0]  # Lấy MaBien từ dữ liệu

        # Truy vấn dữ liệu từ bảng BienSo và LoaiXe dựa trên MaBien
        cursor.execute("""
        SELECT BienSo.MaBien, BienSo.SoBien, BienSo.TrangThai, BienSo.MaLoai, 
            BienSo.AnhPhuongTien, BienSo.AnhBienSo, LoaiXe.TenLoai 
        FROM BienSo
        JOIN LoaiXe ON BienSo.MaLoai = LoaiXe.MaLoai
        WHERE BienSo.MaBien = ?
        """, (ma_bien,))
        row = cursor.fetchone()

        if not row:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin biển số")
            return

        # Tạo cửa sổ mới để hiển thị thông tin chi tiết
        detail_window = tk.Toplevel(page_frame)
        detail_window.title("Thông tin chi tiết biển số")
        detail_window.geometry("800x600")
        detail_window.resizable(False, False)

        # Phân chia layout thành 2 phần
        frame_label = tk.Frame(detail_window, borderwidth=0, relief="raised")
        frame_label.pack(side="top", fill="both", expand=True, padx=0, pady=10)

        frame_info = tk.Frame(detail_window, borderwidth=0, relief="raised")
        frame_info.pack(side="bottom", fill="both", expand=True, padx=10, pady=0)

        # Tạo và cấu hình label
        label_ten = tk.Label(frame_label, text="THÔNG TIN BIỂN SỐ", font=("Helvetica", 20, "bold"))
        label_ten.place(relx=0.5, rely=0.5, anchor="center")

        # Hiển thị thông tin chi tiết
        frame_anh = tk.Frame(detail_window, borderwidth=0, relief="solid")
        frame_anh.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        frame_thongtin = tk.Frame(detail_window, borderwidth=0, relief="solid")
        frame_thongtin.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        info_label = tk.Label(frame_thongtin,
                            text=f"Mã Biển: {row[0]}\n\n"
                                f"Số Biển: {row[1]}\n\n"
                                f"Trạng Thái: {'Đang ở trong bãi' if row[2] else 'không ở trong bãi'}\n\n"
                                f"Loại Xe: {row[6]}",
                            font=("Arial", 16),  # Đặt font chữ to hơn và in đậm
                            anchor="nw",  # Căn văn bản về phía trên cùng bên trái
                            justify="left")  # Đặt căn chỉnh văn bản về bên trái
        info_label.pack(fill="both", expand=True, anchor="nw")

        # Hiển thị ảnh phương tiện từ dữ liệu binary
        anh_phuong_tien_data = row[4]
        if anh_phuong_tien_data:
            image_data = BytesIO(anh_phuong_tien_data)
            img = Image.open(image_data)
            img = img.resize((400, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame_anh, image=photo)
            img_label.image = photo  # Giữ tham chiếu tới ảnh để không bị garbage collected
            img_label.pack()
        else:
            no_image_label = tk.Label(frame_anh, text="Không có ảnh phương tiện")
            no_image_label.pack()

        # Hiển thị ảnh biển số từ dữ liệu binary
        anh_bien_so_data = row[5]
        if anh_bien_so_data:
            image_data = BytesIO(anh_bien_so_data)
            img = Image.open(image_data)
            img = img.resize((250, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame_anh, image=photo)
            img_label.image = photo  # Giữ tham chiếu tới ảnh để không bị garbage collected
            img_label.pack()
        else:
            no_image_label = tk.Label(frame_anh, text="Không có ảnh biển số")
            no_image_label.pack()

    def show_detail():
        # Lấy dòng được chọn trong Treeview
        selected_item = cu_dan_tree.focus()
        
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn một cư dân")
            return

        # Lấy dữ liệu từ dòng được chọn
        data = cu_dan_tree.item(selected_item)
        ma_cu_dan = data["values"][0]  # Lấy MaCuDan từ dữ liệu

        # Truy vấn dữ liệu từ bảng CuDan, BienSo và LoaiXe dựa trên MaCuDan
        cursor.execute("""
        SELECT CuDan.MaCuDan, CuDan.TenCuDan, CuDan.DiaChi, CuDan.MaBien, CuDan.AnhCuDan, BienSo.SoBien, LoaiXe.TenLoai 
        FROM CuDan 
        JOIN BienSo ON CuDan.MaBien = BienSo.MaBien 
        JOIN LoaiXe ON BienSo.MaLoai = LoaiXe.MaLoai
        WHERE CuDan.MaCuDan = ?
        """, (ma_cu_dan,))
        row = cursor.fetchone()

        if not row:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin cư dân")
            return

        # Tạo cửa sổ mới để hiển thị thông tin chi tiết
        detail_window = tk.Toplevel(page_frame)
        detail_window.title("Thông tin chi tiết cư dân")
        detail_window.geometry("600x400")
        detail_window.resizable(False,False)
        
        # Phân chia layout thành 2 phần
        frame_label = tk.Frame(detail_window,borderwidth=0, relief="raised")
        frame_label.pack(side="top", fill="both", expand=True, padx=0, pady=10)

        frame_info = tk.Frame(detail_window,borderwidth=0, relief="raised")
        frame_info.pack(side="bottom", fill="both", expand=True, padx=10, pady=0)
        
        # Tạo và cấu hình label
        label_ten = tk.Label(frame_label, text="THÔNG TIN CƯ DÂN", font=("Helvetica", 20, "bold"))
        label_ten.place(relx=0.5, rely=0.5, anchor="center")
        
        # Hiển thị thông tin chi tiết
        
        frame_anh = tk.Frame(detail_window,borderwidth=0, relief="solid")
        frame_anh.pack(side="left",fill="both", expand=True, padx=5, pady=5)
        
        frame_thongin = tk.Frame(detail_window,borderwidth=0, relief="solid")
        frame_thongin.pack(side="right",fill="both", expand=True, padx=5, pady=5)
        
        info_label = tk.Label(frame_thongin, 
                          text=f"Mã Cư Dân: {row[0]}\n\n"
                               f"Tên Cư Dân: {row[1]}\n\n"
                               f"Địa Chỉ: {row[2]}\n\n"
                               f"Mã Biển: {row[3]}\n\n"
                               f"Số Biển: {row[5]}\n\n"
                               f"Loại Xe: {row[6]}",
                          font=("Arial", 16),  # Đặt font chữ to hơn và in đậm
                          anchor="nw",  # Căn văn bản về phía trên cùng bên trái
                          justify="left")  # Đặt căn chỉnh văn bản về bên trái
        info_label.pack(fill="both", expand=True, anchor="nw")


        # Hiển thị ảnh từ dữ liệu binary
        anh_cu_dan_data = row[4]
        if anh_cu_dan_data:
            image_data = BytesIO(anh_cu_dan_data)
            img = Image.open(image_data)
            img = img.resize((250, 250), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame_anh, image=photo)
            img_label.image = photo  # Giữ tham chiếu tới ảnh để không bị garbage collected
            img_label.pack()
        else:
            no_image_label = tk.Label(frame_anh, text="Không có ảnh")
            no_image_label.pack()
            
            
    # Hàm để làm mới dữ liệu cho combobox biển số
    def refresh_bien_so_combobox():
        # Truy vấn dữ liệu từ bảng BienSo
        cursor.execute("SELECT MaBien, SoBien FROM BienSo")
        bien_so_data = cursor.fetchall()
        bien_so_values = [row[1] for row in bien_so_data]  # Sử dụng số biển (index 1) thay vì mã biển (index 0)
        ma_bien_combobox['values'] = bien_so_values
    
    # Hàm để làm mới dữ liệu trong Treeview của Biển số
    def refresh_bien_so_data():
        # Xóa dữ liệu cũ trong Treeview
        for row in bien_so_tree.get_children():
            bien_so_tree.delete(row)

        # Truy vấn dữ liệu từ bảng BienSo
        cursor.execute("SELECT MaBien, SoBien, TrangThai, MaLoai FROM BienSo")
        bien_so_data = cursor.fetchall()

        # Hiển thị dữ liệu từ BienSo trong Treeview
        for row in bien_so_data:
            ma_bien, so_bien, trang_thai, ma_loai = row
            trang_thai_text = "Trong bãi" if trang_thai else "Không ở trong bãi"
            ma_loai_text = "Ô Tô" if ma_loai == "OT" else "Xe Máy" if ma_loai == "XM" else ma_loai
            bien_so_tree.insert('', 'end', values=(ma_bien, so_bien, trang_thai_text, ma_loai_text))

    # Hàm thêm dữ liệu vào bảng BienSo
    def add_bien_so():
        # Lấy dữ liệu từ các Entry và Combobox
        so_bien = so_bien_entry.get()
        trang_thai = trang_thai_entry.get()
        ten_loai_xe = ma_loai_combobox.get()

        # Kiểm tra xem tên loại xe có trong từ điển ánh xạ không
        if ten_loai_xe in ma_loai_dict:
            # Nếu có, lấy mã loại xe từ từ điển ánh xạ
            ma_loai = ma_loai_dict[ten_loai_xe]
            
            # Kiểm tra xem số biển có tồn tại trong cơ sở dữ liệu không
            cursor.execute("SELECT COUNT(*) FROM BienSo WHERE SoBien = ?", (so_bien,))
            result = cursor.fetchone()
            if result[0] > 0:
                messagebox.showerror("Lỗi", "Số biển trùng, yêu cầu thêm số biển khác!")
                return
            
            # Chọn ảnh phương tiện
            anh_phuong_tien_path = filedialog.askopenfilename(title="Chọn ảnh phương tiện")
            if not anh_phuong_tien_path:
                messagebox.showerror("Lỗi", "Bạn phải chọn ảnh phương tiện!")
                return
            
            # Chọn ảnh biển số
            anh_bien_so_path = filedialog.askopenfilename(title="Chọn ảnh biển số")
            if not anh_bien_so_path:
                messagebox.showerror("Lỗi", "Bạn phải chọn ảnh biển số!")
                return

            # Chuyển đổi ảnh thành dữ liệu nhị phân
            def image_to_binary(image_path):
                with open(image_path, 'rb') as file:
                    binary_data = file.read()
                return binary_data

            anh_phuong_tien = image_to_binary(anh_phuong_tien_path)
            anh_bien_so = image_to_binary(anh_bien_so_path)

            # Thêm dữ liệu vào bảng BienSo với mã loại lấy được từ tên loại xe
            cursor.execute("INSERT INTO BienSo (SoBien, TrangThai, MaLoai, AnhPhuongTien, AnhBienSo) VALUES (?, ?, ?, ?, ?)",
                        (so_bien, trang_thai, ma_loai, anh_phuong_tien, anh_bien_so))
            conn.commit()
            refresh_bien_so_data()
            messagebox.showinfo("Thông báo", "Đã thêm dữ liệu Biển số thành công!")
            
            # Xóa nội dung của các Entry sau khi thêm thành công
            so_bien_entry.delete(0, 'end')
            trang_thai_entry.delete(0, 'end')
            ma_loai_combobox.set('')

        else:
            messagebox.showerror("Lỗi", "Tên loại xe không hợp lệ!")
        refresh_bien_so_combobox()
        

    # Hàm xóa dữ liệu từ bảng BienSo
    def delete_bien_so():
        selected_item = bien_so_tree.selection()
        if selected_item:
            for item in selected_item:
                so_bien = bien_so_tree.item(item, 'values')[0]
                cursor.execute("DELETE FROM BienSo WHERE MaBien = ?", (so_bien,))
                conn.commit()
                bien_so_tree.delete(item)
            messagebox.showinfo("Thông báo", "Đã xóa dữ liệu Biển số thành công!")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một dòng để xóa!")


    # Hàm để làm mới dữ liệu trong Treeview của Dân cư
    def refresh_cu_dan_data():
        # Xóa dữ liệu cũ trong Treeview
        for row in cu_dan_tree.get_children():
            cu_dan_tree.delete(row)

        # Truy vấn dữ liệu từ bảng CuDan
        cursor.execute("SELECT CuDan.MaCuDan, CuDan.TenCuDan, CuDan.DiaChi, BienSo.SoBien FROM CuDan LEFT JOIN BienSo ON CuDan.MaBien = BienSo.MaBien")
        cu_dan_data = cursor.fetchall()

        # Hiển thị dữ liệu từ CuDan trong Treeview
        for row in cu_dan_data:
            # Lấy các giá trị từ cột MaCuDan, TenCuDan, DiaChi và SoBien
            ma_cu_dan, ten_cu_dan, dia_chi, so_bien = row
            # Chèn dữ liệu vào Treeview
            cu_dan_tree.insert('', 'end', values=(ma_cu_dan, ten_cu_dan, dia_chi, so_bien))

    def select_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        return file_path
    
    # Hàm thêm dữ liệu vào bảng CuDan
    def add_cu_dan():
        # Lấy dữ liệu từ các Entry
        ma_cu_dan = ma_cu_dan_entry.get()
        ten_cu_dan = ten_cu_dan_entry.get()
        dia_chi = dia_chi_entry.get()
        sobien = ma_bien_combobox.get()
        anh_cu_dan_path = select_image()  # Chọn ảnh từ file

        if sobien in ma_bien_dict:
             # Kiểm tra xem cư dân với cùng tên và địa chỉ có tồn tại trong cơ sở dữ liệu không
            cursor.execute("SELECT COUNT(*) FROM CuDan WHERE TenCuDan = ? AND DiaChi = ?", (ten_cu_dan, dia_chi))
            result = cursor.fetchone()
            if result[0] > 0:
                messagebox.showerror("Lỗi", "Cư dân này đã tồn tại!")
                return
            
            # Đọc ảnh và chuyển thành binary
            with open(anh_cu_dan_path, 'rb') as file:
                anh_cu_dan_data = file.read()

            # Thêm dữ liệu vào bảng CuDan
            ma_bien = ma_bien_dict[sobien]
            cursor.execute("INSERT INTO CuDan (MaCuDan, TenCuDan, DiaChi, MaBien, AnhCuDan) VALUES (?, ?, ?, ?, ?)",
                        (ma_cu_dan, ten_cu_dan, dia_chi, ma_bien, anh_cu_dan_data))
            conn.commit()
            refresh_cu_dan_data()
            messagebox.showinfo("Thông báo", "Đã thêm dữ liệu Dân cư thành công!")
            
            # Xóa nội dung của các Entry sau khi thêm thành công
            ma_cu_dan_entry.delete(0, 'end')
            ten_cu_dan_entry.delete(0, 'end')
            dia_chi_entry.delete(0, 'end')
            ma_bien_combobox.set('')  # Đặt lại combobox
        else:
            messagebox.showerror("Lỗi", "Số biển không hợp lệ")
    
    # Hàm xóa dữ liệu từ bảng CuDan
    def delete_cu_dan():
        selected_item = cu_dan_tree.selection()
        if selected_item:
            for item in selected_item:
                ma_cu_dan = cu_dan_tree.item(item, 'values')[0]
                cursor.execute("DELETE FROM CuDan WHERE MaCuDan = ?", (ma_cu_dan,))
                conn.commit()
                cu_dan_tree.delete(item)
            messagebox.showinfo("Thông báo", "Đã xóa dữ liệu Dân cư thành công!")
            
    # Truy vấn dữ liệu từ bảng LoaiXe
    cursor.execute("SELECT MaLoai, TenLoai FROM LoaiXe")
    ma_loai_data = cursor.fetchall()
    #ma_loai_values = [row[1] for row in ma_loai_data]
    ma_loai_dict = {row[1]: row[0] for row in ma_loai_data}
    ma_loai_values = list(ma_loai_dict.keys())
    # Truy vấn dữ liệu từ bảng BienSo
    cursor.execute("SELECT MaBien, SoBien FROM BienSo")
    ma_bien_data = cursor.fetchall()
    #ma_bien_values = [row[1] for row in ma_bien_data]
    ma_bien_dict = {row[1]: row[0] for row in ma_bien_data}
    ma_bien_values = list(ma_bien_dict.keys())

    def edit_bien_so():
        selected_item = bien_so_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một hàng để sửa đổi")
            return

        selected_item = selected_item[0]
        
        so_bien = bien_so_tree.item(selected_item, "values")[1]  # Chỉ số cột của Số Biển là 1
        trangThai = bien_so_tree.item(selected_item, "values")[2]  # Chỉ số cột của Trạng Thái là 2
        ma_loai = bien_so_tree.item(selected_item, "values")[3]  # Chỉ số cột của Mã Loại là 3

        new_so_bien = simpledialog.askstring("Sửa thông tin", f"Nhập số biển mới cho biển số {so_bien}")
        new_trangThai = simpledialog.askstring("Sửa thông tin", f"Nhập trạng thái mới (0: Ngoài bãi) (1:Trong bãi) {so_bien}")
        new_ma_loai = simpledialog.askstring("Sửa thông tin", f"Nhập mã loại mới (OT: Ôtô) (XM: Xe Máy) {so_bien}")

        # Tạo biến cursor
        cursor = conn.cursor()

        # Kiểm tra xem new_ma_loai có tồn tại trong bảng LoaiXe không
        if new_ma_loai:
            cursor.execute("SELECT COUNT(*) FROM LoaiXe WHERE MaLoai = ?", (new_ma_loai,))
            result = cursor.fetchone()
            if result[0] == 0:
                messagebox.showerror("Lỗi", f"Mã loại {new_ma_loai} không tồn tại trong bảng LoaiXe")
                return

        # Chọn ảnh phương tiện mới
        new_anh_phuong_tien_path = filedialog.askopenfilename(title="Chọn ảnh phương tiện mới", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if new_anh_phuong_tien_path:
            with open(new_anh_phuong_tien_path, 'rb') as file:
                new_anh_phuong_tien = file.read()
        else:
            new_anh_phuong_tien = None

        # Chọn ảnh biển số mới
        new_anh_bien_so_path = filedialog.askopenfilename(title="Chọn ảnh biển số mới", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if new_anh_bien_so_path:
            with open(new_anh_bien_so_path, 'rb') as file:
                new_anh_bien_so = file.read()
        else:
            new_anh_bien_so = None

        if new_so_bien is not None or new_trangThai is not None or new_ma_loai is not None or new_anh_phuong_tien is not None or new_anh_bien_so is not None:
            # Thực hiện cập nhật vào cơ sở dữ liệu

            update_query = "UPDATE BienSo SET "
            updates = []
            params = []
            if new_so_bien is not None:
                updates.append("SoBien = ?")
                params.append(new_so_bien)
            if new_trangThai is not None:
                updates.append("TrangThai = ?")
                params.append(new_trangThai)
            if new_ma_loai is not None:
                updates.append("MaLoai = ?")
                params.append(new_ma_loai)
            if new_anh_phuong_tien is not None:
                updates.append("AnhPhuongTien = ?")
                params.append(new_anh_phuong_tien)
            if new_anh_bien_so is not None:
                updates.append("AnhBienSo = ?")
                params.append(new_anh_bien_so)

            update_query += ", ".join(updates)
            update_query += " WHERE SoBien = ?"
            params.append(so_bien)

            cursor.execute(update_query, tuple(params))
            conn.commit()

            current_ma_bien = bien_so_tree.item(selected_item, "values")[0]  # Lấy giá trị hiện tại của cột đầu tiên (mã biển số)
            
            # Cập nhật lại dữ liệu trong treeview
            updated_values = (current_ma_bien,
                            new_so_bien if new_so_bien is not None else so_bien,
                            new_trangThai if new_trangThai is not None else trangThai,
                            new_ma_loai if new_ma_loai is not None else ma_loai)
            bien_so_tree.item(selected_item, values=updated_values)  # Sửa đổi chỉ số cột nếu cần
            messagebox.showinfo("Thông báo", "Cập nhật thông tin biển số thành công!")
            refresh_bien_so_data()

    def edit_cu_dan():
        selected_item = cu_dan_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một hàng để sửa đổi")
            return
        
        selected_item = selected_item[0]

        ten_cu_dan = cu_dan_tree.item(selected_item, "values")[1]  # Lấy tên cư dân từ cột thứ hai
        dia_chi = cu_dan_tree.item(selected_item, "values")[2]  # Lấy địa chỉ từ cột thứ ba
        so_bien = cu_dan_tree.item(selected_item, "values")[3]  # Lấy số biển từ cột thứ tư

        new_ten_cu_dan = simpledialog.askstring("Sửa thông tin", "Nhập tên mới cho cư dân", initialvalue=ten_cu_dan)
        new_dia_chi = simpledialog.askstring("Sửa thông tin", "Nhập địa chỉ mới cho cư dân", initialvalue=dia_chi)
        new_so_bien = simpledialog.askstring("Sửa thông tin", "Nhập số biển mới cho cư dân", initialvalue=so_bien)

        if not new_ten_cu_dan or not new_dia_chi or not new_so_bien:
            messagebox.showwarning("Cảnh báo", "Các trường thông tin không được để trống")
            return

        # Kiểm tra xem số biển có tồn tại trong cơ sở dữ liệu không
        cursor = conn.cursor()
        cursor.execute("SELECT MaBien FROM BienSo WHERE SoBien = ?", (new_so_bien,))
        row = cursor.fetchone()
        if not row:
            messagebox.showwarning("Cảnh báo", "Biển số không có trong dữ liệu")
            return

        ma_bien = row[0]  # Lấy MaBien từ kết quả truy vấn

        # Chọn tệp ảnh mới
        new_anh_cu_dan_path = filedialog.askopenfilename(title="Chọn ảnh cư dân", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        new_anh_cu_dan = None
        if new_anh_cu_dan_path:
            with open(new_anh_cu_dan_path, "rb") as file:
                new_anh_cu_dan = file.read()

        # Thực hiện cập nhật vào cơ sở dữ liệu
        cursor = conn.cursor()
        if new_anh_cu_dan is not None:
            update_query = """
            UPDATE CuDan
            SET TenCuDan = ?, DiaChi = ?, MaBien = ?, AnhCuDan = ?
            WHERE MaCuDan = ?
            """
            cursor.execute(update_query, (new_ten_cu_dan, new_dia_chi, ma_bien, new_anh_cu_dan, cu_dan_tree.item(selected_item, "values")[0]))
        else:
            update_query = """
            UPDATE CuDan
            SET TenCuDan = ?, DiaChi = ?, MaBien = ?
            WHERE MaCuDan = ?
            """
            cursor.execute(update_query, (new_ten_cu_dan, new_dia_chi, ma_bien, cu_dan_tree.item(selected_item, "values")[0]))
        
        conn.commit()

        # Cập nhật lại dữ liệu trong treeview
        current_ma_cu_dan = cu_dan_tree.item(selected_item, "values")[0]  # Lấy giá trị hiện tại của cột đầu tiên (mã cư dân)
        cu_dan_tree.item(selected_item, values=(current_ma_cu_dan, new_ten_cu_dan, new_dia_chi, new_so_bien))
        messagebox.showinfo("Thông báo", "Cập nhật thông tin cư dân thành công!")

    
    # Tạo cửa sổ
    #root = tk.Tk()
    #root.title("Quản lý dữ liệu")
    page_frame = tk.Frame(parent,bg="white")
    
    button_font = ("Arial", 12, "bold")
    # Phân chia layout thành 2 phần
    frame_bien_so = tk.Frame(page_frame,borderwidth=3, relief="raised")
    frame_bien_so.pack(side="top", fill="both", expand=True, padx=20, pady=30)

    frame_cu_dan = tk.Frame(page_frame,borderwidth=3, relief="raised")
    frame_cu_dan.pack(side="bottom", fill="both", expand=True, padx=20, pady=30)

    # Phân chia layout của Biển số
    frame_bien_so_left = tk.Frame(frame_bien_so)
    frame_bien_so_left.pack(side="left", fill="both", expand=True)

    frame_bien_so_right = tk.Frame(frame_bien_so)
    frame_bien_so_right.pack(side="right", fill="both", expand=True,padx=50, pady=40)

    # Tạo frame_thongtinbien
    frame_thongtinbien = tk.Frame(frame_bien_so_right,borderwidth=3, relief="raised")
    frame_thongtinbien.pack(expand=True, padx=10, pady=10)

    # Căn chỉnh frame_thongtinbien ở giữa của frame_bien_so_right
    frame_bien_so_right.grid_rowconfigure(0, weight=1)
    frame_bien_so_right.grid_columnconfigure(0, weight=1)
    frame_thongtinbien.grid(row=0, column=0, sticky="nsew")

    # Phân chia layout của Dân cư
    frame_cu_dan_left = tk.Frame(frame_cu_dan)
    frame_cu_dan_left.pack(side="left", fill="both", expand=True)

    frame_cu_dan_right = tk.Frame(frame_cu_dan)
    frame_cu_dan_right.pack(side="right", fill="both", expand=True,padx=50, pady=40)

    # Tạo frame_thongtincudan
    frame_thongtincudan = tk.Frame(frame_cu_dan_right,borderwidth=3, relief="raised")
    frame_thongtincudan.pack(fill="both",expand=True, padx=10, pady=10)

    # Căn chỉnh frame_thongtinbien ở giữa của frame_bien_so_right
    frame_cu_dan_right.grid_rowconfigure(0, weight=1)
    frame_cu_dan_right.grid_columnconfigure(0, weight=1)
    frame_thongtincudan.grid(row=0, column=0, sticky="nsew")
    # Phần Biển số
    tk.Label(frame_bien_so_left, text="Danh sách Biển số", font=("Arial", 14, "bold")).pack(side="top", pady=5)

    bien_so_tree = ttk.Treeview(frame_bien_so_left, columns=("Mã Biển", "Số Biển", "Trạng Thái", "Loại xe"), selectmode="extended")
    bien_so_tree.pack(side="top", fill="both", expand=True,padx=20,pady=20)

    bien_so_tree.heading("#0", text="", anchor="center")
    bien_so_tree.column("#0", width=0, stretch=tk.NO)
    bien_so_tree.heading("#1", text="Mã Biển")
    bien_so_tree.heading("#2", text="Số Biển")
    bien_so_tree.heading("#3", text="Trạng Thái")
    bien_so_tree.heading("#4", text="Loại xe")
    
    bien_so_tree.bind("<<TreeviewSelect>>", lambda event: show_detail_plate())
    refresh_bien_so_data()

    # Phần entry và button thêm dữ liệu cho Biển số
    tk.Label(frame_thongtinbien, text="THÊM THÔNG TIN BIỂN SỐ", font=("Arial", 14, "bold")).grid(row=1, column=2, sticky="n", padx=10, pady=10)
    
    tk.Label(frame_thongtinbien, text="Số biển:", font=("Arial", 11, "bold")).grid(row=3, column=1, sticky="e", padx=10, pady=10)
    so_bien_entry = tk.Entry(frame_thongtinbien, width=40)
    so_bien_entry.grid(row=3, column=2, sticky="w", padx=10, pady=10)

    tk.Label(frame_thongtinbien, text="Trạng thái:", font=("Arial", 11, "bold")).grid(row=4, column=1, sticky="e", padx=10, pady=10)
    trang_thai_entry = tk.Entry(frame_thongtinbien, width=40)
    trang_thai_entry.grid(row=4, column=2, sticky="w", padx=10, pady=10)

    tk.Label(frame_thongtinbien, text="Loại xe:", font=("Arial", 11, "bold")).grid(row=5, column=1, sticky="e", padx=10, pady=10)
    ma_loai_combobox = ttk.Combobox(frame_thongtinbien, values=ma_loai_values, width=30)
    ma_loai_combobox.grid(row=5, column=2, sticky="w", padx=10, pady=10)

    add_bien_so_button = tk.Button(frame_thongtinbien, text="Thêm",bg='#00C957', fg='white', border=1, command=add_bien_so, font=button_font)
    add_bien_so_button.grid(row=6, column=1, pady=5, sticky="e")

    delete_bien_so_button = tk.Button(frame_thongtinbien, text="Xóa", bg='#FF3030', fg='white', border=1,command=delete_bien_so, font=button_font)
    delete_bien_so_button.grid(row=6, column=3, pady=5, sticky="w")

    edit_bien_so_button = tk.Button(frame_thongtinbien, text="Sửa", bg='#00CED1', fg='white', border=1,command=edit_bien_so, font=button_font)
    edit_bien_so_button.grid(row=6, column=2, pady=5, sticky="w")
    # Phần Dân cư
    tk.Label(frame_cu_dan_left, text="Danh sách Dân cư", font=("Arial", 14, "bold")).pack(side="top", pady=5)

    cu_dan_tree = ttk.Treeview(frame_cu_dan_left, columns=("Mã Cư Dân", "Tên", "Địa chỉ", "Mã Biển"), selectmode="extended")
    cu_dan_tree.pack(side="top", fill="both", expand=True,padx=20,pady=20)

    cu_dan_tree.heading("#0", text="", anchor="center")
    cu_dan_tree.column("#0", width=0, stretch=tk.NO)
    cu_dan_tree.heading("#1", text="Mã Cư Dân")
    cu_dan_tree.heading("#2", text="Tên")
    cu_dan_tree.heading("#3", text="Địa chỉ")
    cu_dan_tree.heading("#4", text="Số Biển")

    cu_dan_tree.bind("<<TreeviewSelect>>", lambda event: show_detail())
    refresh_cu_dan_data()

    # Phần entry và button thêm dữ liệu cho Dân cư
    tk.Label(frame_thongtincudan, text="THÊM THÔNG TIN CƯ DÂN", font=("Arial", 14, "bold")).grid(row=1, column=2, sticky="n", padx=10, pady=10)
    
    tk.Label(frame_thongtincudan, text="Mã cư dân:", font=("Arial", 11, "bold")).grid(row=3, column=1, sticky="e", padx=10, pady=10)
    ma_cu_dan_entry = tk.Entry(frame_thongtincudan,width=40)
    ma_cu_dan_entry.grid(row=3, column=2, sticky="w", padx=10, pady=10)

    tk.Label(frame_thongtincudan, text="Tên:", font=("Arial", 11, "bold")).grid(row=4, column=1, sticky="e", padx=10, pady=10)
    ten_cu_dan_entry = tk.Entry(frame_thongtincudan,width=40)
    ten_cu_dan_entry.grid(row=4, column=2, sticky="w",padx=10, pady=10)

    tk.Label(frame_thongtincudan, text="Địa chỉ:", font=("Arial", 11, "bold")).grid(row=5, column=1, sticky="e",padx=10, pady=10)
    dia_chi_entry = tk.Entry(frame_thongtincudan,width=40)
    dia_chi_entry.grid(row=5, column=2, sticky="w",padx=10, pady=10)

    tk.Label(frame_thongtincudan, text="Số biển:", font=("Arial", 11, "bold")).grid(row=6, column=1, sticky="e",padx=10, pady=10)
    ma_bien_combobox = ttk.Combobox(frame_thongtincudan,  values=ma_bien_values,width=30)
    ma_bien_combobox.grid(row=6, column=2, sticky="w",padx=10, pady=10)

    add_cu_dan_button = tk.Button(frame_thongtincudan, text="Thêm",bg='#00C957', fg='white', border=1, command=add_cu_dan,font=button_font)
    add_cu_dan_button.grid(row=7, column=1, pady=5)

    edit_cu_dan_button = tk.Button(frame_thongtincudan, text="Sửa",bg='#00CED1', fg='white', border=1, command=edit_cu_dan,font=button_font)
    edit_cu_dan_button.grid(row=7, column=2, pady=5)
    
    delete_cu_dan_button = tk.Button(frame_thongtincudan, text="Xóa", bg='#FF3030', fg='white', border=1, command=delete_cu_dan,font=button_font)
    delete_cu_dan_button.grid(row=7, column=3, pady=5)

    reload_button = tk.Button(frame_thongtincudan, text="Tải lại", bg='#57a1f8', fg='white', border=1, command=refresh_bien_so_combobox, font=button_font)
    reload_button.grid(row=8, column=1, padx=5, pady=5)
    #root.mainloop()
    # Đóng kết nối CSDL
    #conn.close()
    page_frame.pack(fill=tk.BOTH, expand=True)
    return page_frame

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Thống kê xe vào")
    root.geometry("800x600")

    createGUI(root)

    root.mainloop()
