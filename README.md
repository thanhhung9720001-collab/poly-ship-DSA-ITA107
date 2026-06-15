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

### 📍 Phần 1: Định tuyến giữa các kho và Mạng truyền dẫn (routing.py, mst.py) - **ĐÃ HOÀN THÀNH 100%**
- [x] **Thuật toán Dijkstra (Tìm chặng ngắn nhất)**:
  - Cài đặt hàm `build_graph(edges)` để xây dựng danh sách kề vô hướng từ danh sách cạnh thô.
  - Cài đặt giải thuật `dijkstra(graph, source)` tìm khoảng cách ngắn nhất sử dụng hàng đợi ưu tiên (`heapq`).
  - Cài đặt hàm `shortest_route(graph, source, target)` truy vết hành trình tối ưu và tổng chi phí.
- [x] **Thuật toán Kruskal MST & DSU (Mạng truyền dẫn tối ưu)**:
  - Triển khai giải thuật tìm Cây khung tối thiểu Kruskal kết hợp cấu trúc Union-Find (Disjoint Set Union) để tối ưu hóa việc kết nối liên thông các kho hàng.
- [x] **Trực quan hóa Đồ thị mạng kho (Visual Graph Canvas)**:
  - Hiện thực vẽ trực quan mạng lưới kho dạng đồ thị trực tiếp trên cửa sổ phụ Tkinter Canvas.
  - Tự động định vị các kho hàng theo vòng tròn, vẽ kết nối và in trọng số chi phí trên từng cung đường.
  - Highlight lộ trình ngắn nhất và mạng cây khung MST bằng **màu cam thương hiệu FPT**.
  - Hỗ trợ tương tác nhấp chuột trực quan lên đỉnh của đồ thị để chọn điểm đầu/cuối trực tiếp hoặc chọn qua Combobox thả xuống.
- [x] **Đọc dữ liệu CSV linh hoạt**:
  - Tích hợp hộp thoại tự động mở chọn file dữ liệu bản đồ (.csv) khi chọn chức năng, loại bỏ nút nạp dữ liệu rườm rà ở giao diện chính.
  - Hỗ trợ thư mục dữ liệu chuẩn `data_training/` với các bộ dữ liệu mẫu đa dạng.

### 🔑 Phần 2: Hashing cho đơn hàng và dữ liệu (hashing_tools.py) - **ĐÃ HOÀN THÀNH 100%**
- [x] **Bảng băm Separate Chaining (`OrderHashTable`)**:
  - Cài đặt cấu hình bảng băm độ dài 10 với kỹ thuật xử lý đụng độ bằng Danh sách liên kết đơn (Node Linked List).
- [x] **Dashboard Tra cứu đơn hàng (Order Search)**:
  - Cửa sổ trực quan chia đôi: Bảng điều khiển tác vụ (Thêm/Cập nhật, Tìm kiếm, Xóa) ở bên trái và sơ đồ cấu trúc của cả 10 buckets thời gian thực ở bên phải.
  - Đồng bộ tự động với cơ sở dữ liệu tệp tin `data_training/don_hang_database.csv` giúp lưu trữ lâu dài kể cả khi tắt ứng dụng.
- [x] **Các bài toán băm phụ trợ và tìm kiếm**:
  - Đã triển khai thuật toán nhóm mã coupon Anagrams, tìm chuỗi ngày liên tiếp dài nhất, đếm số ngày đạt doanh thu mục tiêu bằng Prefix Sum + HashMap, và tìm kiếm chuỗi log bằng thuật toán trượt Rabin-Karp Rolling Hash.

### 🎁 Phần 3: Dynamic Programming gợi ý khuyến mãi (promo_optimizer.py) - *Sắp triển khai*
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
