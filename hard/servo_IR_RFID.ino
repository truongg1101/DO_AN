#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
int cambien = 2; //Chân cảm biến nối chân số 5 Arduino
int giatri;
// Set the LCD address to 0x3F for a 16 chars and 2 line display
LiquidCrystal_I2C lcd(0x3F, 16, 2);
const int backlightPin = 3; // Example: using pin 3 for PWM

#define RST_PIN         9          // Thiết lập chân RST của RC522 trên chân D9
#define SS_PIN          10         // Thiết lập chân SS (chân chip select) của RC522 trên chân D10

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Tạo đối tượng MFRC522
Servo servo;                        // Tạo đối tượng Servo

bool rfidDetected = false;          // Biến để kiểm tra RFID đã được quét hay chưa
unsigned long lastRFIDTime = 0;     // Biến để lưu thời gian cuối cùng RFID được quét

void setup() {
  Serial.begin(9600);               // Khởi tạo giao tiếp Serial
  SPI.begin();                      // Khởi tạo giao tiếp SPI
  mfrc522.PCD_Init();               // Khởi tạo MFRC522
    // Initialize the LCD
  lcd.init();
  // Turn on the backlight
  lcd.backlight();
   // Tắt chức năng nhấp nháy và ẩn con trỏ
  lcd.noBlink();
  lcd.noCursor();
  // Set backlight pin as output
  pinMode(backlightPin, OUTPUT);
  // Set brightness to maximum (255)
  analogWrite(backlightPin, 255); // Full brightness
  servo.attach(6);                  // Servo được kết nối với chân số 6
  servo.write(90);                   // Khởi tạo servo ở vị trí 0 độ
  pinMode(cambien, INPUT);
}

void loop() {
  giatri = digitalRead(cambien); //Đọc giá trị digital từ cảm biến và gán vào biến giatri
  if (giatri == LOW) {
    Serial.println("1"); // Gửi tín hiệu 1 cho máy tính
  } else {
    Serial.println("0"); // Gửi tín hiệu 0 cho máy tính
  }
  if (Serial.available() > 0) {
    char command = Serial.read(); // Đọc dữ liệu từ Serial
    
    // Kiểm tra nếu lệnh là '1'
    if (command == '3' && (giatri == LOW)) {
      // Gửi lệnh cho servo di chuyển đến góc 90 độ
      lcd.setCursor(0, 0); // Di chuyển con trỏ văn bản đến dòng 1, cột 0
      lcd.print("XIN CHAO CU DAN");
      
      // Hiển thị "MOI VAO" ở dòng số 2
      lcd.setCursor(0, 1); // Di chuyển con trỏ văn bản đến dòng 2, cột 0
      lcd.print("MOI VAO");
      servo.write(90);
    }
  }
  if (giatri == HIGH) {
      delay(1000);
      servo.write(180);
      lcd.clear(); // Xóa nội dung trên màn hình LCD
      lcd.home();  // Di chuyển con trỏ về vị trí ban đầu
    }
  // Kiểm tra nếu có thẻ RFID được quét
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    // Lấy mã thẻ RFID
    MFRC522::Uid uid = mfrc522.uid;

    // Hiển thị mã thẻ RFID trong Serial Monitor
    Serial.print("RFID Detected! Card UID:");
    for (byte i = 0; i < uid.size; i++) {
      Serial.print(uid.uidByte[i] < 0x10 ? " 0" : " ");
      Serial.print(uid.uidByte[i], HEX);
    }
    Serial.println();

    // Nếu có thẻ RFID được quét, mở servo ở góc 90 độ
    lcd.setCursor(0, 0); // Di chuyển con trỏ văn bản đến dòng 1, cột 0
    lcd.print("KHACH VANG LAI");
      
    // Hiển thị "MOI VAO" ở dòng số 2
    lcd.setCursor(0, 1); // Di chuyển con trỏ văn bản đến dòng 2, cột 0
    lcd.print("MOI VAO");
    servo.write(90);

    rfidDetected = true;
    lastRFIDTime = millis();        // Lưu thời gian khi RFID được quét
    Serial.println("RFID Detected");
    delay(1000);                    // Đợi 1 giây để tránh việc quét liên tiếp
  }

  // Kiểm tra nếu đã quét RFID và đã đủ thời gian để đóng lại servo
  if (rfidDetected && (giatri == HIGH)) {
    delay(1000);
    // Đóng lại servo ở vị trí 0 độ sau 5 giây
    servo.write(180);
    lcd.clear(); // Xóa nội dung trên màn hình LCD
    lcd.home();  // Di chuyển con trỏ về vị trí ban đầu
    rfidDetected = false;           // Thiết lập lại biến RFID đã được quét
    Serial.println("Servo Closed");
    
  }

  mfrc522.PICC_HaltA();            // Dừng thẻ RFID hiện tại
  mfrc522.PCD_StopCrypto1();        // Dừng mã hóa cho thẻ RFID hiện tại
}
