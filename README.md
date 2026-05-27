# HỆ THỐNG QUẢN LÝ HẬU CẦN POLY-SHIP - ASSIGNMENT HOÀN THÀNH

Đồ án Assignment môn học **Cấu trúc dữ liệu và giải thuật (ITA107)** tại FPT Polytechnic.

## 👤 Thông tin sinh viên
- **Họ và tên**: Nguyễn Thành Hưng
- **Mã số sinh viên (MSSV)**: PS47270
- **Lớp**: ITA107
- **Môn học**: Cấu trúc dữ liệu và giải thuật

---

## 🌟 Tính năng chính (Giao diện đơn giản & Mô phỏng trực quan)

Ứng dụng được thiết kế tự chứa (Self-contained) trong duy nhất một tệp tin [main_assignment.py](file:///d:/FPT%20Polytechnic/2026/HK%20Summer%202026/ITA107_%20C%E1%BA%A5u%20tr%C3%BAc%20d%E1%BB%AF%20li%E1%BB%87u%20v%C3%A0%20gi%E1%BA%A3i%20thu%E1%BA%ADt/ASM/main_assignment.py) giúp đảm bảo sự ổn định và dễ dàng chấm bài:

1. **Giao diện Flat UI nhỏ gọn (`520x760`)**:
   - Khung Banner chứa Logo FPT Polytechnic và đèn tín hiệu online thời gian thực.
   - Container dạng Card gom nhóm 8 nút bấm chức năng đại diện cho menu console của đề bài.
   - Nhãn thông tin sinh viên ở chân trang.

2. **Mô phỏng 7 Demo thuật toán chi tiết**:
   - **📍 1. Demo routing**: Mô phỏng tìm chặng đi ngắn nhất Dijkstra giữa các kho.
   - **🕸️ 2. Demo MST**: Mô phỏng tìm cây khung tối thiểu Kruskal kết nối mạng cáp chính của kho hàng.
   - **🔑 3. Demo hash table**: Trực quan hóa chèn/xóa và xung đột băm trên chuỗi bucket băm Separate Chaining.
   - **🧮 4. Demo hashing tổng hợp**: Nhóm mã coupon Anagram, tính chuỗi ngày giao liên tục dài nhất và đếm khoảng doanh thu bằng K.
   - **🔍 5. Demo rolling hash**: Mô phỏng tìm pattern trong logs log bằng thuật toán Rabin-Karp.
   - **🪜 6. Demo DP cơ bản**: Mô phỏng tính Fibonacci (Memoization) và Leo thang (Tabulation).
   - **🎁 7. Demo combo khuyến mãi**: Tối ưu combo cái túi Knapsack 0/1 (so sánh 2D và 1D).
   - **🚪 8. Thoát**: Hộp thoại xác nhận đóng phần mềm.

3. **Cơ chế tiến trình và âm báo**:
   - Khóa toàn bộ các nút bấm chống double-click khi đang xử lý.
   - Chạy thanh tiến trình giả lập từ 0% đến 100% màu cam FPT.
   - Tự động phát âm thanh cảnh báo hệ thống (`winsound`) khi hoàn thành xử lý.

4. **Nhật ký Console phân cấp màu sắc**:
   - Ghi nhận chi tiết kết quả chạy mẫu, mô phỏng dữ liệu vào/ra và phần giải thích ngắn về thuật toán.
   - Hỗ trợ xuất nhật ký ra tệp tin `log_hoat_dong.txt`.

---

## 🛠️ Hướng dẫn khởi chạy
Mở Command Prompt/Terminal trong thư mục dự án và chạy:
```bash
python main_assignment.py
```
*(Khuyên dùng hệ điều hành Windows và Python 3.8+)*
