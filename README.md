# HỆ THỐNG QUẢN LÝ HẬU CẦN POLY-SHIP - ASSIGNMENT DSA

Đồ án Assignment môn học **Cấu trúc dữ liệu và giải thuật (ITA107)** tại FPT Polytechnic.

## 👤 Thông tin sinh viên
- **Họ và tên**: Nguyễn Thành Hưng
- **Mã số sinh viên (MSSV)**: PS47270
- **Lớp**: ITA107
- **Môn học**: Cấu trúc dữ liệu và giải thuật

---

## 📅 Tiến độ thực hiện Dự án (Project Progress)

Dự án hiện đã hoàn thiện **100%** toàn bộ các yêu cầu trong đề bài Assignment môn Cấu trúc dữ liệu và giải thuật (ITA107):

### 📍 Phần 1: Định tuyến giữa các kho và Mạng truyền dẫn (routing.py, mst.py) - **ĐÃ HOÀN THÀNH 100%**
- **Thuật toán Dijkstra (Tìm chặng ngắn nhất)**:
  - Cài đặt hàm `build_graph(edges)` xây dựng danh sách kề vô hướng từ dữ liệu tệp CSV.
  - Cài đặt giải thuật `dijkstra(graph, source)` tìm khoảng cách ngắn nhất sử dụng hàng đợi ưu tiên (`heapq`).
  - Cài đặt hàm `shortest_route(graph, source, target)` truy vết hành trình tối ưu và tổng chi phí.
- **Thuật toán Kruskal MST & DSU (Mạng truyền dẫn tối ưu)**:
  - Triển khai giải thuật tìm Cây khung tối thiểu Kruskal kết hợp cấu trúc Union-Find (Disjoint Set Union) tối ưu hóa việc kết nối liên thông các kho hàng chính với chi phí truyền dẫn thấp nhất.
- **Trực quan hóa Đồ thị mạng kho (Visual Graph Canvas)**:
  - Vẽ trực quan đồ thị mạng lưới kho trên Canvas: tự động tính toán vị trí, highlight lộ trình ngắn nhất và cây khung MST bằng **màu cam thương hiệu FPT**.
  - Hỗ trợ chọn kho hàng trực quan bằng cách nhấp chuột lên đỉnh kho trên Canvas hoặc qua Combobox lựa chọn.

### 🔑 Phần 2: Hashing cho đơn hàng và dữ liệu (hashing_tools.py, anagrams.py, consecutive_days.py, subarray_sum.py, rolling_hash.py) - **ĐÃ HOÀN THÀNH 100%**
- **Bảng băm Separate Chaining (`OrderHashTable`)**:
  - Cấu hình bảng băm độ dài 10 với kỹ thuật xử lý đụng độ bằng Danh sách liên kết đơn (Node Linked List).
  - Tích hợp giao diện quản trị 10 Buckets thời gian thực, đồng bộ tự động 2 chiều lâu dài với file [don_hang_database.csv](file:///d:/FPT%20Polytechnic/2026/HK%20Summer%202026/ITA107_%20C%E1%BA%A5u%20tr%C3%BAc%20d%E1%BB%AF%20li%E1%BB%87u%20v%C3%A0%20gi%E1%BA%A3i%20thu%E1%BA%ADt/ASM/data_training/don_hang_database.csv).
  - Nút **"📁 Nạp CSDL từ File (.csv)"** cho phép nạp thêm dữ liệu từ tệp ngoài (như [don_hang_bo_sung.csv](file:///d:/FPT%20Polytechnic/2026/HK%20Summer%202026/ITA107_%20C%E1%BA%A5u%20tr%C3%BAc%20d%E1%BB%AF%20li%E1%BB%87u%20v%C3%A0%20gi%E1%BA%A3i%20thu%E1%BA%ADt/ASM/data_training/don_hang_bo_sung.csv)) gộp vào bảng băm hiện tại và lưu trữ vĩnh viễn.
- **Các bài toán băm tổng hợp**:
  - `group_coupon_anagrams`: Gom nhóm các mã giảm giá na ná nhau bằng bảng băm.
  - `longest_consecutive_days`: Tìm chuỗi ngày giao hàng cao điểm liên tiếp dài nhất bằng HashSet trong độ phức tạp $O(N)$.
  - `count_revenue_windows`: Đếm số khoảng ngày liên tiếp có tổng doanh thu bằng K bằng Prefix Sum + HashMap trong $O(N)$.
  - **Dashboard Hashing Tổng Hợp**: Thiết kế 2 cột độc lập cho phép người dùng chọn chức năng trước, nạp dữ liệu riêng biệt cho từng chức năng con bằng tệp tin tương ứng rồi chạy giải thuật.
- **Rolling Hash Rabin-Karp**:
  - `rolling_hash_search`: Tìm kiếm chuỗi log bằng thuật toán Rabin-Karp trong thời gian trung bình $O(N+M)$.
  - Thiết kế Dashboard quét log chuyên nghiệp cho phép nạp file log lớn (như [du_lieu_logs.txt](file:///d:/FPT%20Polytechnic/2026/HK%20Summer%202026/ITA107_%20C%E1%BA%A5u%20tr%C3%BAc%20d%E1%BB%AF%20li%E1%BB%87u%20v%C3%A0%20gi%E1%BA%A3i%20thu%E1%BA%ADt/ASM/data_training/du_lieu_logs.txt)) và highlight tô nền màu vàng chữ đỏ tại mọi vị trí khớp.

### 🎁 Phần 3: Dynamic Programming gợi ý khuyến mãi (promo_optimizer.py) - **ĐÃ HOÀN THÀNH 100%**
- **Quy hoạch động cơ bản (DP Basics)**:
  - Cài đặt `fib_tab(n)` và `climb_stairs(n)` bằng phương pháp bottom-up tabulation, trực quan hóa từng bước chuyển trạng thái và giải thích sự tương đồng của hai bài toán.
- **Tối ưu Combo khuyến mãi (Knapsack 0/1)**:
  - Cài đặt Knapsack 2D `build_combo_dp_table` và truy vết `trace_combo_from_dp`. Hiển thị danh sách sản phẩm bằng Treeview, nạp file CSV sản phẩm và vẽ trực quan ma trận phương án $DP[i][b]$ (khi $B \le 25$).
  - Cài đặt Knapsack 1D `combo_knapsack_1d` tối ưu hóa không gian bộ nhớ chỉ còn $O(B)$ thay vì $O(N \times B)$, so sánh hiệu năng bộ nhớ và chứng minh kết quả trùng khớp với bản 2D.

---

## 📂 Cấu trúc thư mục Dự án (Project Directory Structure)

Dự án được phân rã thành các tệp tin giải thuật độc lập và thư mục lưu trữ dữ liệu kiểm thử chuẩn như sau:

```text
POLY-SHIP/
├── data_training/                  # Thư mục dữ liệu kiểm thử
│   ├── ban_do_phuc_tap.csv         # Bản đồ mạng lưới 10 kho 16 chặng
│   ├── du_lieu_mau.csv             # Bản đồ 6 kho mặc định
│   ├── don_hang_database.csv       # Cơ sở dữ liệu đơn hàng của Bảng băm
│   ├── don_hang_bo_sung.csv        # Dữ liệu đơn hàng nạp bổ sung
│   ├── du_lieu_coupon.csv          # Dữ liệu coupon Anagrams mẫu
│   ├── du_lieu_ngay.csv            # Dữ liệu chuỗi ngày liên tiếp mẫu
│   ├── du_lieu_doanh_thu.csv       # Dữ liệu doanh thu tích lũy mẫu
│   ├── du_lieu_logs.txt            # Tệp logs hệ thống lớn mẫu
│   └── du_lieu_san_pham.csv        # Danh sách sản phẩm Knapsack mẫu
├── routing.py                      # Module Dijkstra định tuyến ngắn nhất
├── mst.py                          # Module Kruskal MST và DSU
├── hashing_tools.py                # Module quản lý bảng băm đơn hàng
├── anagrams.py                     # Thuật toán nhóm coupon anagrams
├── consecutive_days.py             # Thuật toán tính chuỗi ngày liên tiếp
├── subarray_sum.py                 # Thuật toán tổng chặng doanh thu bằng K
├── rolling_hash.py                 # Thuật toán tìm kiếm Rabin-Karp
├── promo_optimizer.py              # Module Quy hoạch động (Fib, Stairs, Knapsack 2D/1D)
├── main_assignment.py              # Chương trình chính tích hợp giao diện GUI
├── README.md                       # Tài liệu hướng dẫn sử dụng
└── .gitignore                      # Loại bỏ các file rác và file log tạm thời khỏi Git
```

---

## 🛠️ Hướng dẫn khởi chạy & Kiểm thử chi tiết

### 1. Khởi chạy ứng dụng
Mở Command Prompt/Terminal trong thư mục dự án và chạy lệnh sau:
```bash
python main_assignment.py
```

### 2. Kiểm thử Chức năng 1 (📍 Tuyến giao hàng ngắn nhất)
1. Bấm nút **"📍 1. Tuyến giao hàng ngắn nhất"**.
2. Chọn file `ban_do_phuc_tap.csv` (hoặc `du_lieu_mau.csv`) trong thư mục `data_training/`.
3. Sơ đồ Canvas đồ thị kho hàng sẽ mở ra với lộ trình tối ưu được tô màu cam nét đậm.
4. Bạn có thể thay đổi điểm đầu/cuối bằng cách nhấp chuột lên các nút tròn đỉnh trên Canvas hoặc qua Combobox lựa chọn rồi nhấn **"🚀 Định Tuyến"**.

### 3. Kiểm thử Chức năng 2 (🕸️ Đường truyền nội bộ riêng)
1. Bấm nút **"🕸️ 2. Đường truyền nội bộ riêng giữa các kho"**.
2. Chọn file bản đồ từ hộp thoại.
3. Sơ đồ cây khung tối thiểu MST sẽ được vẽ trực quan. Các cạnh được chọn trong MST sẽ được tô đậm màu cam FPT. Tổng chi phí lắp đặt hiển thị rõ ràng dưới chân sơ đồ.

### 4. Kiểm thử Chức năng 3 (🔑 Tra cứu đơn hàng)
1. Bấm nút **"🔑 3. Tra cứu đơn hàng"**.
2. Thêm mới đơn hàng bằng cách nhập ID, Thông tin và nhấn **"Thêm/Cập Nhật"**.
3. Tìm kiếm đơn hàng bằng nút **"Tìm Kiếm"** (chương trình sẽ chạy tiến trình mô phỏng và nhấp nháy highlight Bucket tương ứng chứa đơn hàng).
4. Nhấn **"Nạp CSDL từ File (.csv)"**, chọn tệp `data_training/don_hang_bo_sung.csv` $\rightarrow$ Quan sát các đơn hàng bổ sung được gộp vào và lưu trữ vĩnh viễn xuống file CSDL chính.

### 5. Kiểm thử Chức năng 4 (🧮 Hashing tổng hợp)
1. Bấm nút **"🧮 4. Hashing tổng hợp"** $\rightarrow$ Dashboard Hashing mở ra.
2. Thử nghiệm nạp file cho từng chức năng con:
   * Nhấn **"Nạp Coupon từ File"**, chọn `du_lieu_coupon.csv` rồi nhấn **"Nhóm Anagrams"**.
   * Nhấn **"Nạp Ngày từ File"**, chọn `du_lieu_ngay.csv` rồi nhấn **"Tìm Streak"**.
   * Nhấn **"Nạp Doanh thu từ File"**, chọn `du_lieu_doanh_thu.csv` rồi nhấn **"Đếm chặng"**.
3. Đọc báo cáo kết quả và giải thích thuật toán tương ứng ở cột phải.

### 6. Kiểm thử Chức năng 5 (🔍 Rolling hash tìm log)
1. Bấm nút **"🔍 5. Rolling hash tìm pattern log"**.
2. Nhấn **"Nạp Logs từ File (.txt/.log)"**, chọn tệp `du_lieu_logs.txt`.
3. Nhập từ khóa cần tìm (ví dụ: `SAVE10` hoặc `ERROR`) $\rightarrow$ Nhấn **"Tìm kiếm Rabin-Karp"**.
4. Quan sát danh sách vị trí khớp và phần highlight màu vàng chữ đỏ tại vùng trực quan ở cột phải.

### 7. Kiểm thử Chức năng 6 (🪜 DP cơ bản)
1. Bấm nút **"🪜 6. DP cơ bản (Fib, Stairs)"**.
2. Nhập số nguyên N (ví dụ: `10`), nhấn **"Chạy thuật toán DP"**.
3. Quan sát các bước cộng dồn bottom-up của Fibonacci và Climbing Stairs được in chi tiết ở cột phải.

### 8. Kiểm thử Chức năng 7 (🎁 Combo khuyến mãi)
1. Bấm nút **"🎁 7. Combo khuyến mãi (Knapsack)"**.
2. Nhấn **"Nạp sản phẩm từ File (.csv)"**, chọn tệp `du_lieu_san_pham.csv`.
3. Nhập ngân sách B (ví dụ: `50`).
4. Nhấn **"Chạy Knapsack 2D"** để xem các sản phẩm được chọn và ma trận phương án $DP[i][b]$ được vẽ dạng bảng chữ trực quan.
5. Nhấn **"Chạy Knapsack 1D"** để so sánh dung lượng bộ nhớ được tiết kiệm và đối chiếu tính chính xác của kết quả.
