# HỆ THỐNG QUẢN LÝ HẬU CẦN POLY-SHIP - GIAI ĐOẠN 1

Đồ án Assignment môn học **Cấu trúc dữ liệu và giải thuật (ITA107)** tại FPT Polytechnic.

## 👤 Thông tin sinh viên
- **Họ và tên**: Nguyễn Thành Hưng
- **Mã số sinh viên (MSSV)**: PS47270
- **Lớp**: ITA107
- **Môn học**: Cấu trúc dữ liệu và giải thuật

---

## 🌟 Các tính năng chính (Giai đoạn 1 - Sườn Chức Năng & Giao Diện)

Hệ thống được thiết kế dưới dạng ứng dụng Desktop UI viết bằng Python **Tkinter** tiêu chuẩn, tự chứa (Self-contained) trong một tệp duy nhất để đảm bảo không bị lỗi tương thích khi chấm điểm. Giao diện sử dụng thiết kế phẳng, hiện đại với tông màu cam đặc trưng của FPT Polytechnic.

1. **Giao diện Flat UI chuyên nghiệp**:
   - Sử dụng Card Container để gom nhóm các nút bấm hành động.
   - Nút bấm phẳng hiện đại với hiệu ứng Hover thay đổi màu nền khi di chuột.
   - Tích hợp Logo FPT Polytechnic ở phần Header.
   - Đèn trạng thái tín hiệu hệ thống thời gian thực (`● Máy chủ: Online | DB: Connected`).

2. **Cơ chế mô phỏng tiến trình động (Progress Bar)**:
   - Khi click thực hiện các chức năng, hệ thống tự động **khóa tất cả các nút bấm** để chống double-click gây lỗi.
   - Thanh tiến trình mô phỏng chạy từ 0% đến 100% màu cam FPT kèm theo nhãn trạng thái động dưới mỗi hành động.

3. **Phím tắt Nạp nhanh dữ liệu mẫu (Demo Shortcut)**:
   - Dòng link `⚡ Nạp nhanh dữ liệu mẫu` dưới nút Nhập dữ liệu tự động sinh ra tệp dữ liệu `du_lieu_mau.txt` và nạp vào hệ thống mà không cần người dùng tự tạo file thủ công.

4. **Bảng Nhật ký Console phân cấp màu sắc (Colored Logs)**:
   - Toàn bộ hành động được ghi nhận theo thời gian thực (Giờ:Phút:Giây).
   - Màu sắc chữ được phân cấp rõ ràng:
     - **Trắng**: Nhật ký thông tin hệ thống mặc định (`Info`).
     - **Xanh lá**: Nhật ký hoàn thành thành công (`Success`).
     - **Vàng**: Nhật ký cảnh báo hệ thống (`Warning`).
     - **Đỏ**: Nhật ký thông báo lỗi nhập liệu/đọc file (`Error`).

5. **Xuất Nhật ký hoạt động (Backup Logs)**:
   - Nút `📤 Xuất Nhật Ký` lưu toàn bộ nội dung console đang hiển thị thành tệp tin `log_hoat_dong.txt` trong thư mục hiện hành dưới định dạng UTF-8.

6. **Hệ thống cảnh báo âm thanh (System Sound Alerts)**:
   - Tự động phát ra âm thanh thông báo mặc định của hệ thống Windows (`winsound`) khi hoàn thành xử lý (`success`), gặp lỗi (`error`) hoặc cảnh báo (`warning`).

7. **Xử lý lỗi toàn diện (Robust Error Handling)**:
   - Bắt lỗi khi file nạp không tồn tại, file trống 0 bytes, định dạng không khớp và xử lý xác nhận đồng ý/hủy trước khi đóng ứng dụng.

---

## 🛠️ Hướng dẫn Khởi chạy và Nghiệm thu

### 1. Yêu cầu hệ thống
- Hệ điều hành: Windows (khuyên dùng để chạy đầy đủ tính năng winsound).
- Phiên bản Python: 3.8 trở lên.
- Thư viện Pillow (Tùy chọn, dùng để resize logo FPT chất lượng cao. Nếu không có Pillow, phần mềm tự động sử dụng trình dựng ảnh mặc định của Tkinter để tránh crash).

### 2. Khởi chạy ứng dụng
Mở Command Prompt hoặc Terminal trong thư mục chứa mã nguồn và chạy lệnh:
```bash
python main_assignment.py
```

### 3. Quy trình nghiệm thu nhanh
1. **Bước 1**: Khởi chạy ứng dụng. Console ghi nhận log Info màu trắng.
2. **Bước 2**: Nhấp vào `⚡ Nạp nhanh dữ liệu mẫu` để tạo dữ liệu tự động. Thanh tiến trình chạy, hệ thống khóa nút, phát âm báo thành công và in log Xanh lá.
3. **Bước 3**: Nhấp vào **2. Xử lý** và **3. Tối ưu** để xem mô phỏng chạy thuật toán.
4. **Bước 4**: Click nút **📤 Xuất Nhật Ký** để sao lưu log ra file `log_hoat_dong.txt`.
5. **Bước 5**: Click nút **4. Thông tin & Hướng dẫn** để xem thông tin SV.
6. **Bước 6**: Click **5. Thoát chương trình**, chọn **Yes** để đóng an toàn.
