# Dự án Bãi Đỗ Xe Thông Minh

Dự án này là một bãi đỗ xe thông minh sử dụng nhận diện biển số xe hoặc thẻ RFID để quản lý xe ra vào bãi xe.

## Tính năng

- Nhận diện biển số xe
- Giao diện thân thiện với người dùng
- Điều khiển phần cứng Arduino
- Cập nhật trạng thái bãi đỗ xe theo thời gian thực

## Công nghệ sử dụng

- Python cho nhận diện biển số xe
- Arduino IDE cho lập trình phần cứng
- Tkinter cho giao diện người dùng

## Phần cứng sử dụng

- Arduino UNO
- Servo
- RFID-RC522
- Cảm biến IR

### Kết nối Arduino với phần cứng

- Kết nối RFID-RC522 với Arduino
- Kết nối Servo với Arduino
- Kết nối Cảm biến IR với Arduino

### Cài đặt các thư viện cần thiết để sử dụng phần cứng

1. Cài đặt thư viện cho Arduino
    - Mở Arduino IDE
    - Vào `Sketch` -> `Include Library` -> `Manage Libraries...`
    - Tìm và cài đặt các thư viện `MFRC522`, `Servo`, và `IRremote`

## Cách sử dụng

1. Clone lại repository:
    ```sh
    git clone https://github.com/truongg1101/DO_AN.git
    ```

2. Di chuyển đến thư mục dự án:
    ```sh
    cd DO_AN
    ```

3. Cài đặt các thư viện cần thiết:
    ```sh
    pip install -r requirements.txt
    ```

4. Kết nối Arduino vào máy và chọn cổng COM.

5. Mở Arduino IDE và sao chép mã `.ino` từ thư mục dự án để đẩy mã vào Arduino. **Lưu ý:** Cần sử dụng 2 Arduino để hoạt động, đẩy mã vào từng Arduino một.

6. Kết nối Arduino với máy.

7. Chạy các file Python để chương trình hoạt động:
    - Chạy file `login.py` để bắt đầu từ phần đăng nhập:
        ```sh
        python login.py
        ```
    - Chạy file `mainGUI.py` để chạy không cần đăng nhập:
        ```sh
        python mainGUI.py
        ```

## Sử dụng cơ sở dữ liệu

Chương trình đang sử dụng cơ sở dữ liệu với SQL Server. Khi sử dụng, hãy tạo cơ sở dữ liệu trên máy và thay đổi đường dẫn tới cơ sở dữ liệu trong các file Python.

Có thể sử dụng các cơ sở dữ liệu khác tùy theo nhu cầu.

Chúc bạn sử dụng dự án thành công!
