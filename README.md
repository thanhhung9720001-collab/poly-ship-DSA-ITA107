# HỆ THỐNG QUẢN LÝ HẬU CẦN POLY-SHIP - ASSIGNMENT DSA

Đồ án Assignment môn học **Cấu trúc dữ liệu và giải thuật (ITA107)** tại FPT Polytechnic.

## 👤 Thông tin sinh viên
- **Họ và tên**: Nguyễn Thành Hưng
- **Mã số sinh viên (MSSV)**: PS47270
- **Lớp**: ITA107
- **Môn học**: Cấu trúc dữ liệu và giải thuật

---

## 📅 Tiến độ thực hiện Dự án (Project Progress)

Hiện tại dự án đang được triển khai theo mô hình module hóa và đạt được các kết quả cụ thể dưới đây:

### 📍 Phần 1: Định tuyến giữa các kho (routing.py) - **Đang hoàn thiện**
- [x] **Thuật toán Dijkstra (Tìm chặng ngắn nhất)**:
  - Cài đặt hàm `build_graph(edges)` để xây dựng danh sách kề vô hướng từ danh sách cạnh thô.
  - Cài đặt giải thuật `dijkstra(graph, source)` tìm khoảng cách ngắn nhất sử dụng hàng đợi ưu tiên (`heapq`).
  - Cài đặt hàm `shortest_route(graph, source, target)` truy vết hành trình tối ưu và tổng chi phí.
- [x] **Trực quan hóa Đồ thị mạng kho (Visual Graph Canvas)**:
  - Hiện thực vẽ trực quan mạng lưới kho dạng đồ thị trực tiếp trên cửa sổ phụ Tkinter Canvas.
  - Tự động định vị các kho hàng theo vòng tròn, vẽ kết nối và in trọng số chi phí trên từng cung đường.
  - Highlight toàn bộ lộ trình đi qua và các kho hàng đích bằng **màu cam thương hiệu FPT**.
- [x] **Phân tích dữ liệu tệp CSV**:
  - Thêm nút **📥 Nạp dữ liệu từ tệp CSV** trên GUI cho phép người dùng nạp file bản đồ tự chọn.
  - Xử lý kiểm tra dữ liệu trống và hiển thị cảnh báo an toàn cho người dùng khi chạy định tuyến mà chưa nạp dữ liệu.
- [ ] **Thuật toán Kruskal MST & DSU** (Sắp triển khai).

### 🔑 Phần 2: Hashing cho đơn hàng và dữ liệu (hashing_tools.py) - *Chưa triển khai*
- [ ] Lớp bảng băm `OrderHashTable` xử lý đụng độ bằng phương pháp Separate Chaining.
- [ ] Các hàm tối ưu hóa Hashing: Coupon Anagrams, Longest consecutive days, Subarray sum = k, Rabin-Karp Rolling Hash.

### 🎁 Phần 3: Dynamic Programming gợi ý khuyến mãi (promo_optimizer.py) - *Chưa triển khai*
- [ ] Các hàm DP cơ bản: Fibonacci, Climbing Stairs.
- [ ] Tối ưu hóa combo cái túi Knapsack 0/1 (bản 2D vẽ bảng/truy vết và bản 1D tối ưu bộ nhớ).

---

## 🛠️ Hướng dẫn khởi chạy & Kiểm thử

1. **Khởi chạy ứng dụng**:
   Mở Command Prompt/Terminal trong thư mục dự án và chạy:
   ```bash
   python main_assignment.py
   ```
2. **Kiểm thử chức năng định tuyến (Dijkstra)**:
   * Khi vừa mở ứng dụng, bấm nút **"1. Định tuyến - shortest path"** $\rightarrow$ Hệ thống cảnh báo chưa có dữ liệu.
   * Bấm nút **"📥 Nạp dữ liệu từ tệp CSV"** và chọn tệp `du_lieu_kho.csv` có sẵn trong thư mục, hoặc bấm liên kết **"Nạp nhanh dữ liệu cấu hình mẫu"** ở góc dưới.
   * Bấm lại nút **"1. Định tuyến - shortest path"**, nhập kho xuất phát (ví dụ: `WH1`) và kho đích (ví dụ: `HN`) $\rightarrow$ Sơ đồ đồ thị trực quan sẽ tự động hiển thị lộ trình ngắn nhất được highlight nổi bật.
