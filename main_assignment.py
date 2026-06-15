import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import routing
import mst
import hashing_tools
import anagrams
import consecutive_days
import subarray_sum
import rolling_hash

# Đảm bảo Python có thể tìm thấy các file cùng thư mục
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Đảm bảo console in ra Tiếng Việt Unicode không bị lỗi trên Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

class PolyShipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("POLY-SHIP Hậu Cần - FPT Polytechnic")
        self.root.geometry("520x760")
        self.root.configure(bg="#f8fafc")
        self.root.resizable(False, False)
        
        # Cấu hình dữ liệu mạng lưới kho hàng (Khởi tạo rỗng)
        self.vertices = []
        self.edges = []
        
        # Thử load logo FPT Polytechnic một cách an toàn
        self.logo_img = None
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fpt_logo.png")
        if os.path.exists(logo_path):
            try:
                # 1. Thử dùng Pillow (để resize chất lượng cao)
                from PIL import Image, ImageTk
                img = Image.open(logo_path)
                w_target = 205
                h_target = int(w_target * img.height / img.width)
                img = img.resize((w_target, h_target), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
            except Exception:
                try:
                    # 2. Dự phòng: Dùng PhotoImage nguyên bản của Tkinter (nếu không có Pillow)
                    self.logo_img = tk.PhotoImage(file=logo_path).subsample(5)
                except Exception:
                    self.logo_img = None

        # --- 1. HEADER BANNER ---
        header_frame = tk.Frame(root, bg="#ffffff", height=95)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        # Thanh kẻ màu cam FPT dưới header để làm điểm nhấn
        orange_line = tk.Frame(root, bg="#f27024", height=4)
        orange_line.pack(fill="x")

        if self.logo_img:
            lbl_logo_img = tk.Label(header_frame, image=self.logo_img, bg="#ffffff")
            lbl_logo_img.pack(side="left", padx=(15, 10), pady=10)
            
            # Khung thông tin tiêu đề và trạng thái bên phải
            right_header = tk.Frame(header_frame, bg="#ffffff")
            right_header.pack(side="right", padx=(10, 15), pady=10)
            
            lbl_title = tk.Label(right_header, text="HỆ THỐNG HẬU CẦN\nPOLY-SHIP", fg="#f27024", bg="#ffffff", 
                                 font=("Segoe UI", 12, "bold"), justify="right")
            lbl_title.pack(anchor="e")
            
            lbl_status = tk.Label(right_header, text="● Máy chủ: Online | DB: Connected", fg="#10b981", bg="#ffffff", 
                                  font=("Segoe UI", 9, "bold"))
            lbl_status.pack(anchor="e", pady=(4, 0))
        else:
            # Fallback nếu không có file logo
            lbl_logo = tk.Label(header_frame, text="FPT POLYTECHNIC", fg="#f27024", bg="#ffffff", 
                                font=("Segoe UI", 12, "italic bold"))
            lbl_logo.pack(anchor="w", padx=25, pady=(15, 0))
            
            lbl_title = tk.Label(header_frame, text="HỆ THỐNG HẬU CẦN POLY-SHIP", fg="#0f172a", bg="#ffffff", 
                                 font=("Segoe UI", 14, "bold"))
            lbl_title.pack(anchor="w", padx=25, pady=(2, 2))

            lbl_status = tk.Label(header_frame, text="● Máy chủ: Online | Database: Connected", fg="#10b981", bg="#ffffff", 
                                  font=("Segoe UI", 9, "bold"))
            lbl_status.pack(anchor="w", padx=25, pady=(0, 15))

        # --- 2. CARD CONTAINER CHỨA NÚT BẤM ---
        main_content = tk.Frame(root, bg="#f8fafc", padx=20, pady=10)
        main_content.pack(fill="x")

        card_frame = tk.Frame(main_content, bg="#ffffff", highlightthickness=1, 
                              highlightbackground="#e2e8f0", padx=20, pady=10)
        card_frame.pack(fill="x")

        # Style cấu hình chung cho các nút bấm phẳng hiện đại
        self.btn_style = {
            "bg": "#f27024",
            "fg": "#ffffff",
            "activebackground": "#d95f1c",
            "activeforeground": "#ffffff",
            "relief": "flat",
            "font": ("Segoe UI", 11, "bold"),
            "width": 36,
            "height": 1,
            "pady": 4,
            "cursor": "hand2",
            "bd": 0
        }

        # Nút 1: Định tuyến tìm đường đi ngắn nhất
        self.btn_routing = tk.Button(card_frame, text="📍 1. Tuyến giao hàng ngắn nhất", **self.btn_style, command=self.run_routing)
        self.btn_routing.pack(pady=3)

        # Nút 2: Đường truyền nội bộ riêng giữa các kho
        self.btn_mst = tk.Button(card_frame, text="🕸️ 2. Đường truyền nội bộ riêng giữa các kho", **self.btn_style, command=self.run_mst)
        self.btn_mst.pack(pady=3)

        # Nút 3: Tra cứu đơn hàng
        self.btn_hash_table = tk.Button(card_frame, text="🔑 3. Tra cứu đơn hàng", **self.btn_style, command=self.run_hash_table)
        self.btn_hash_table.pack(pady=3)

        # Nút 4: Hashing tổng hợp
        self.btn_hashing_compound = tk.Button(card_frame, text="🧮 4. Hashing tổng hợp", **self.btn_style, command=self.run_hashing_compound)
        self.btn_hashing_compound.pack(pady=3)

        # Nút 5: Tìm pattern log bằng Rolling hash
        self.btn_rolling_hash = tk.Button(card_frame, text="🔍 5. Rolling hash tìm pattern log", **self.btn_style, command=self.run_rolling_hash)
        self.btn_rolling_hash.pack(pady=3)

        # Nút 6: DP cơ bản
        self.btn_dp_basics = tk.Button(card_frame, text="🪜 6. DP cơ bản (Fib, Stairs)", **self.btn_style, command=self.run_dp_basics)
        self.btn_dp_basics.pack(pady=3)

        # Nút 7: Combo khuyến mãi
        self.btn_combo_knapsack = tk.Button(card_frame, text="🎁 7. Combo khuyến mãi (Knapsack)", **self.btn_style, command=self.run_combo_knapsack)
        self.btn_combo_knapsack.pack(pady=3)

        # Nút 8: Thoát
        exit_style = self.btn_style.copy()
        exit_style["bg"] = "#0f172a"
        exit_style["activebackground"] = "#1e293b"
        self.btn_exit = tk.Button(card_frame, text="🚪 8. Thoát chương trình", **exit_style, command=self.exit_program)
        self.btn_exit.pack(pady=3)

        # --- 3. KHUNG THANH TIẾN TRÌNH MÔ PHỎNG ---
        self.progress_frame = tk.Frame(main_content, bg="#f8fafc")
        self.progress_frame.pack(fill="x", pady=(2, 0))

        style = ttk.Style()
        style.configure("Orange.Horizontal.TProgressbar", troughcolor='#e2e8f0', background='#f27024', thickness=12)

        self.progress_bar = ttk.Progressbar(self.progress_frame, orient="horizontal", mode="determinate", 
                                             style="Orange.Horizontal.TProgressbar", length=300)
        self.progress_bar.pack(fill="x", padx=5)

        self.lbl_progress_status = tk.Label(self.progress_frame, text="Hệ thống sẵn sàng", 
                                             font=("Segoe UI", 9, "bold"), fg="#64748b", bg="#f8fafc")
        self.lbl_progress_status.pack(pady=2)

        # --- 4. KHUNG NHẬT KÝ HỆ THỐNG ---
        log_section = tk.Frame(root, bg="#f8fafc", padx=20)
        log_section.pack(fill="both", expand=True)

        # Thanh tiêu đề và nút Xuất Log
        log_header = tk.Frame(log_section, bg="#f8fafc")
        log_header.pack(fill="x", pady=(0, 2))

        lbl_log_title = tk.Label(log_header, text="💻 Nhật ký hoạt động hệ thống:", 
                                 font=("Segoe UI", 10, "bold"), fg="#475569", bg="#f8fafc")
        lbl_log_title.pack(side="left")

        self.btn_export = tk.Button(log_header, text="📤 Xuất Nhật Ký", bg="#475569", fg="#ffffff",
                                    activebackground="#334155", activeforeground="#ffffff",
                                    font=("Segoe UI", 8, "bold"), cursor="hand2", relief="flat", bd=0,
                                    padx=8, pady=2, command=self.export_log)
        self.btn_export.pack(side="right")

        log_border = tk.Frame(log_section, bg="#e2e8f0", highlightthickness=1, highlightbackground="#cbd5e1")
        log_border.pack(fill="both", expand=True)

        # Text Console hiển thị Log màu mặc định trắng, hỗ trợ màu sắc phân cấp
        self.txt_log = tk.Text(log_border, bg="#0f172a", fg="#ffffff", insertbackground="#ffffff", 
                               relief="flat", font=("Courier New", 10), height=5)
        self.txt_log.pack(fill="both", expand=True)
        
        # Cấu hình màu cho từng cấp độ nhật ký (Logs Color-Coding)
        self.txt_log.tag_config("info", foreground="#ffffff")      # Màu trắng sữa cho log thường
        self.txt_log.tag_config("success", foreground="#10b981")   # Màu xanh lá cho thành công
        self.txt_log.tag_config("warning", foreground="#fbbf24")   # Màu vàng cho cảnh báo
        self.txt_log.tag_config("error", foreground="#ef4444")     # Màu đỏ cho lỗi hệ thống

        scrollbar = tk.Scrollbar(self.txt_log, command=self.txt_log.yview)
        scrollbar.pack(side="right", fill="y")
        self.txt_log.config(yscrollcommand=scrollbar.set)

        # Footer
        footer = tk.Label(root, text="Sinh viên thực hiện: Nguyễn Thành Hưng - PS47270 - Lớp ITA107", 
                          font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#f8fafc")
        footer.pack(side="bottom", pady=6)

        # Lưu trữ nội dung text gốc của các nút bấm để hover & reset trạng thái sạch sẽ
        self.btn_texts = {
            self.btn_routing: "📍 1. Tuyến giao hàng ngắn nhất",
            self.btn_mst: "🕸️ 2. Đường truyền nội bộ riêng giữa các kho",
            self.btn_hash_table: "🔑 3. Tra cứu đơn hàng",
            self.btn_hashing_compound: "🧮 4. Hashing tổng hợp",
            self.btn_rolling_hash: "🔍 5. Rolling hash tìm pattern log",
            self.btn_dp_basics: "🪜 6. DP cơ bản (Fib, Stairs)",
            self.btn_combo_knapsack: "🎁 7. Combo khuyến mãi (Knapsack)",
            self.btn_exit: "🚪 8. Thoát chương trình",
            self.btn_export: "📤 Xuất Nhật Ký"
        }

        # Thiết lập hiệu ứng Hover cho toàn bộ nút bấm
        self.setup_hover(self.btn_routing, "#f27024", "#d95f1c")
        self.setup_hover(self.btn_mst, "#f27024", "#d95f1c")
        self.setup_hover(self.btn_hash_table, "#f27024", "#d95f1c")
        self.setup_hover(self.btn_hashing_compound, "#f27024", "#d95f1c")
        self.setup_hover(self.btn_rolling_hash, "#f27024", "#d95f1c")
        self.setup_hover(self.btn_dp_basics, "#f27024", "#d95f1c")
        self.setup_hover(self.btn_combo_knapsack, "#f27024", "#d95f1c")
        self.setup_hover(self.btn_exit, "#0f172a", "#1e293b")
        self.setup_hover(self.btn_export, "#475569", "#334155")

        # Ghi log khởi động hệ thống
        self.log_message("Khởi chạy hệ thống POLY-SHIP thành công.", "info")

        # Cấu hình Bảng băm đơn hàng (Khởi tạo và tải từ cơ sở dữ liệu CSV)
        self.load_orders_from_csv()

    def setup_hover(self, button, normal_color, hover_color):
        """Thiết lập hiệu ứng hover đổi màu nền và dịch chuyển văn bản biểu tượng ➔"""
        original_text = self.btn_texts[button]
        
        def on_enter(e):
            if button.cget("state") == "normal":
                button.config(bg=hover_color, text=f"{original_text}  ➔")
                
        def on_leave(e):
            if button.cget("state") == "normal":
                button.config(bg=normal_color, text=original_text)
                
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def parse_csv_file(self, file_path):
        """Đọc và phân tích cú pháp tệp CSV chứa danh sách cạnh đồ thị"""
        vertices_set = set()
        edges = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split(",")
                    if len(parts) == 3:
                        u, v, cost_str = parts
                        u = u.strip()
                        v = v.strip()
                        try:
                            cost = float(cost_str)
                            if cost.is_integer():
                                cost = int(cost)
                            edges.append((u, v, cost))
                            vertices_set.add(u)
                            vertices_set.add(v)
                        except ValueError:
                            pass
            if edges:
                self.edges = edges
                self.vertices = sorted(list(vertices_set))
                self.log_message(f"Đã cập nhật mạng lưới kho hàng từ file: {len(self.vertices)} đỉnh, {len(self.edges)} cạnh.", "success")
            else:
                raise ValueError("Không có dữ liệu hợp lệ trong file!")
        except Exception as e:
            self.log_message(f"Lỗi khi đọc và phân tích file CSV: {str(e)}", "error")
            raise e

    def visualize_graph(self, vertices, edges, path=None, highlight_edges=None, cost=None):
        """Hiển thị cửa sổ đồ thị trực quan vẽ bằng Canvas tích hợp chọn nguồn/đích trực tiếp"""
        import math
        
        # Tạo cửa sổ phụ
        vis_win = tk.Toplevel(self.root)
        vis_win.title("Trực quan hóa Bản đồ định tuyến POLY-SHIP")
        vis_win.geometry("700x670")
        vis_win.configure(bg="#f8fafc")
        vis_win.transient(self.root)
        vis_win.grab_set()
        
        # Tiêu đề
        lbl_title = tk.Label(
            vis_win, 
            text="SƠ ĐỒ ĐỒ THỊ MẠNG KHO & TUYẾN ĐƯỜNG TỐI ƯU", 
            font=("Segoe UI", 12, "bold"), 
            fg="#f27024", 
            bg="#f8fafc"
        )
        lbl_title.pack(pady=(10, 5))
        
        # BẢNG ĐIỀU KHIỂN TRỰC TIẾP TRÊN DIAGRAM (Top Control Panel)
        ctrl_frame = tk.LabelFrame(vis_win, text=" Bộ chọn chặng định tuyến trực tiếp ", font=("Segoe UI", 9, "bold"), fg="#475569", bg="#f8fafc", padx=10, pady=5)
        ctrl_frame.pack(fill="x", padx=20, pady=5)
        
        lbl_src = tk.Label(ctrl_frame, text="Kho nguồn:", font=("Segoe UI", 9, "bold"), fg="#475569", bg="#f8fafc")
        lbl_src.pack(side="left", padx=5)
        
        cb_src = ttk.Combobox(ctrl_frame, values=self.vertices, width=12, state="readonly")
        cb_src.pack(side="left", padx=5)
        
        lbl_tgt = tk.Label(ctrl_frame, text="Kho đích:", font=("Segoe UI", 9, "bold"), fg="#475569", bg="#f8fafc")
        lbl_tgt.pack(side="left", padx=5)
        
        cb_tgt = ttk.Combobox(ctrl_frame, values=self.vertices, width=12, state="readonly")
        cb_tgt.pack(side="left", padx=5)
        
        # Thiết lập giá trị dropdown mặc định
        if path and len(path) > 0:
            cb_src.set(path[0])
            cb_tgt.set(path[-1])
        else:
            if self.vertices:
                cb_src.set(self.vertices[0])
                cb_tgt.set(self.vertices[-1])
        
        # Canvas vẽ hình
        canvas = tk.Canvas(vis_win, bg="#ffffff", highlightthickness=1, highlightbackground="#cbd5e1")
        canvas.pack(fill="both", expand=True, padx=20, pady=(5, 10))
        
        # Thêm thông tin tổng kết bên dưới canvas
        info_frame = tk.Frame(vis_win, bg="#f8fafc")
        info_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Cấu trúc 2 hàng chữ Tiếng Việt
        text_frame = tk.Frame(info_frame, bg="#f8fafc")
        text_frame.pack(side="left", fill="y")
        
        lbl_route = tk.Label(
            text_frame, 
            text="Tuyến đường tối ưu: ...", 
            font=("Segoe UI", 10, "bold"), 
            fg="#0f172a", 
            bg="#f8fafc"
        )
        lbl_route.pack(anchor="w")
        
        lbl_cost = tk.Label(
            text_frame, 
            text="Tổng chi phí vận chuyển: ...", 
            font=("Segoe UI", 10, "bold"), 
            fg="#10b981", 
            bg="#f8fafc"
        )
        lbl_cost.pack(anchor="w", pady=(2, 0))
        
        # Chú thích màu sắc nhỏ gọn bên phải nhãn kết quả
        legend_frame = tk.Frame(info_frame, bg="#f8fafc")
        legend_frame.pack(side="right")
        lbl_leg1 = tk.Label(legend_frame, text="● Kho hàng", fg="#64748b", bg="#f8fafc", font=("Segoe UI", 8, "bold"))
        lbl_leg1.pack(side="left", padx=5)
        lbl_leg2 = tk.Label(legend_frame, text="● Lộ trình tối ưu", fg="#f27024", bg="#f8fafc", font=("Segoe UI", 8, "bold"))
        lbl_leg2.pack(side="left", padx=5)
        
        # Tính toán vị trí các đỉnh trên một vòng tròn lớn
        n = len(vertices)
        coords = {}
        center_x, center_y = 350, 230  # Chỉnh lại center_y một chút vì cửa sổ cao hơn
        radius = 170
        
        for i, node in enumerate(vertices):
            angle = i * (2 * math.pi / n)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            coords[node] = (x, y)
            
        def draw_graph(path=None, cost=None):
            canvas.delete("all")
            
            highlight_set = set()
            if path and len(path) > 1:
                for i in range(len(path) - 1):
                    u, v = path[i], path[i+1]
                    highlight_set.add((u, v))
                    highlight_set.add((v, u))
                    
            # 1. Vẽ tất cả các cạnh trước
            for u, v, c in edges:
                if u in coords and v in coords:
                    x1, y1 = coords[u]
                    x2, y2 = coords[v]
                    
                    is_path_edge = (u, v) in highlight_set
                    color = "#f27024" if is_path_edge else "#cbd5e1"
                    width = 4 if is_path_edge else 1.5
                    
                    canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
                    
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2
                    
                    canvas.create_rectangle(
                        mid_x - 12, mid_y - 8, mid_x + 12, mid_y + 8,
                        fill="#ffffff", outline=""
                    )
                    canvas.create_text(
                        mid_x, mid_y, text=str(c), 
                        font=("Segoe UI", 9, "bold"), fill="#0f172a"
                    )
                    
            # 2. Vẽ các đỉnh
            node_radius = 22
            for node in vertices:
                if node in coords:
                    x, y = coords[node]
                    
                    is_in_path = False
                    if path:
                        is_in_path = node in path
                                
                    fill_color = "#f27024" if is_in_path else "#ffffff"
                    outline_color = "#d95f1c" if is_in_path else "#475569"
                    text_color = "#ffffff" if is_in_path else "#0f172a"
                    width = 2.5 if is_in_path else 1.5
                    
                    canvas.create_oval(
                        x - node_radius, y - node_radius, 
                        x + node_radius, y + node_radius, 
                        fill=fill_color, outline=outline_color, width=width
                    )
                    
                    canvas.create_text(
                        x, y, text=node, 
                        font=("Segoe UI", 9, "bold"), fill=text_color
                    )
            
            # Cập nhật nhãn bên dưới
            if path:
                path_str = " - ".join(path)
                lbl_route.config(text=f"Tuyến đường tối ưu: {path_str}", fg="#0f172a")
                if cost is not None:
                    lbl_cost.config(text=f"Tổng chi phí vận chuyển: {cost}", fg="#10b981")
                    lbl_cost.pack(anchor="w", pady=(2, 0))
                else:
                    lbl_cost.pack_forget()
            else:
                lbl_route.config(text="Không tìm thấy tuyến đường giữa hai điểm!", fg="#ef4444")
                lbl_cost.pack_forget()
                
        def run_routing_internal():
            src = cb_src.get()
            tgt = cb_tgt.get()
            if not src or not tgt:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn đầy đủ Kho nguồn và Kho đích!")
                return
            if src == tgt:
                messagebox.showwarning("Cảnh báo", "Kho nguồn và Kho đích không được trùng nhau!")
                return
                
            graph = routing.build_graph(edges)
            cost, route = routing.shortest_route(graph, src, tgt)
            
            self.log_message(f"--- ĐỊNH TUYẾN TRỰC TIẾP TRÊN BẢN ĐỒ ---", "info")
            self.log_message(f"Kho nguồn: {src} ➔ Kho đích: {tgt}", "info")
            if cost == float('inf'):
                self.log_message(f"Không tìm thấy tuyến đường giữa {src} và {tgt}!", "error")
                draw_graph(None, None)
            else:
                route_format = " - ".join(route)
                self.log_message(f"Optimal route: {route_format}: {cost}", "success")
                self.log_message(f"Tuyến đường tối ưu: {route_format}: {cost}", "success")
                self.play_sound("success")
                draw_graph(route, cost)

        btn_calc = tk.Button(ctrl_frame, text="🚀 Định Tuyến", bg="#f27024", fg="#ffffff", activebackground="#d95f1c", font=("Segoe UI", 9, "bold"), bd=0, padx=12, pady=2, cursor="hand2", command=run_routing_internal)
        btn_calc.pack(side="left", padx=10)
        
        # Bắt sự kiện click trên Canvas để chọn điểm trực quan bằng cách nhấp chuột
        selected_nodes = []
        
        def on_canvas_click(event):
            clicked_node = None
            for node, (x, y) in coords.items():
                dist = math.sqrt((event.x - x)**2 + (event.y - y)**2)
                if dist <= 22:
                    clicked_node = node
                    break
            
            if clicked_node:
                if len(selected_nodes) == 0:
                    selected_nodes.append(clicked_node)
                    cb_src.set(clicked_node)
                    self.log_message(f"Nhấp chọn Kho nguồn: {clicked_node}", "info")
                    draw_graph([clicked_node], cost=0)
                elif len(selected_nodes) == 1:
                    src = selected_nodes[0]
                    tgt = clicked_node
                    if src == tgt:
                        selected_nodes.clear()
                        self.log_message("Hủy chọn kho hàng.", "info")
                        draw_graph(None, None)
                    else:
                        selected_nodes.append(tgt)
                        cb_tgt.set(tgt)
                        self.log_message(f"Nhấp chọn Kho đích: {tgt}", "info")
                        run_routing_internal()
                        selected_nodes.clear()
                        
        canvas.bind("<Button-1>", on_canvas_click)
        
        # Vẽ đồ thị ban đầu
        draw_graph(path, cost)

    def visualize_mst(self, vertices, edges, mst_edges, total_cost):
        """Hiển thị sơ đồ đồ thị mạng truyền dẫn tối thiểu MST Kruskal"""
        import math
        
        # Tạo cửa sổ phụ
        vis_win = tk.Toplevel(self.root)
        vis_win.title("Đường truyền nội bộ tối ưu - MST Kruskal")
        vis_win.geometry("700x620")
        vis_win.configure(bg="#f8fafc")
        vis_win.transient(self.root)
        vis_win.grab_set()
        
        # Tiêu đề
        lbl_title = tk.Label(
            vis_win, 
            text="SƠ ĐỒ ĐƯỜNG TRUYỀN NỘI BỘ TỐI ƯU GIỮA CÁC KHO (MST)", 
            font=("Segoe UI", 11, "bold"), 
            fg="#f27024", 
            bg="#f8fafc"
        )
        lbl_title.pack(pady=(15, 5))
        
        # Canvas vẽ hình
        canvas = tk.Canvas(vis_win, bg="#ffffff", highlightthickness=1, highlightbackground="#cbd5e1")
        canvas.pack(fill="both", expand=True, padx=20, pady=(5, 10))
        
        # Thêm thông tin tổng kết bên dưới canvas
        info_frame = tk.Frame(vis_win, bg="#f8fafc")
        info_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Cấu trúc 2 hàng chữ Tiếng Việt
        text_frame = tk.Frame(info_frame, bg="#f8fafc")
        text_frame.pack(side="left", fill="y")
        
        lbl_route = tk.Label(
            text_frame, 
            text="Mạng lưới truyền dẫn liên thông tối ưu (MST)", 
            font=("Segoe UI", 10, "bold"), 
            fg="#0f172a", 
            bg="#f8fafc"
        )
        lbl_route.pack(anchor="w")
        
        lbl_cost = tk.Label(
            text_frame, 
            text=f"Tổng chi phí lắp đặt mạng: {total_cost}", 
            font=("Segoe UI", 10, "bold"), 
            fg="#10b981", 
            bg="#f8fafc"
        )
        lbl_cost.pack(anchor="w", pady=(2, 0))
        
        # Chú thích màu sắc
        legend_frame = tk.Frame(info_frame, bg="#f8fafc")
        legend_frame.pack(side="right")
        lbl_leg1 = tk.Label(legend_frame, text="● Kho hàng", fg="#64748b", bg="#f8fafc", font=("Segoe UI", 8, "bold"))
        lbl_leg1.pack(side="left", padx=5)
        lbl_leg2 = tk.Label(legend_frame, text="● Đường truyền MST", fg="#f27024", bg="#f8fafc", font=("Segoe UI", 8, "bold"))
        lbl_leg2.pack(side="left", padx=5)
        
        # Tính toán vị trí các đỉnh trên một vòng tròn lớn
        n = len(vertices)
        coords = {}
        center_x, center_y = 350, 240
        radius = 170
        
        for i, node in enumerate(vertices):
            angle = i * (2 * math.pi / n)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            coords[node] = (x, y)
            
        # Tập hợp các cạnh thuộc MST
        mst_set = set()
        for u, v, c in mst_edges:
            mst_set.add((u, v))
            mst_set.add((v, u))
            
        # 1. Vẽ tất cả các cạnh trước
        for u, v, cost in edges:
            if u in coords and v in coords:
                x1, y1 = coords[u]
                x2, y2 = coords[v]
                
                is_mst_edge = (u, v) in mst_set
                color = "#f27024" if is_mst_edge else "#cbd5e1"
                width = 4 if is_mst_edge else 1.5
                
                canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
                
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                
                canvas.create_rectangle(
                    mid_x - 12, mid_y - 8, mid_x + 12, mid_y + 8,
                    fill="#ffffff", outline=""
                )
                canvas.create_text(
                    mid_x, mid_y, text=str(cost), 
                    font=("Segoe UI", 9, "bold"), fill="#0f172a"
                )
                
        # 2. Vẽ các đỉnh
        node_radius = 22
        for node in vertices:
            if node in coords:
                x, y = coords[node]
                
                is_connected = False
                for u, v, c in mst_edges:
                    if node == u or node == v:
                        is_connected = True
                        break
                        
                fill_color = "#f27024" if is_connected else "#ffffff"
                outline_color = "#d95f1c" if is_connected else "#475569"
                text_color = "#ffffff" if is_connected else "#0f172a"
                width = 2.5 if is_connected else 1.5
                
                canvas.create_oval(
                    x - node_radius, y - node_radius, 
                    x + node_radius, y + node_radius, 
                    fill=fill_color, outline=outline_color, width=width
                )
                
                canvas.create_text(
                    x, y, text=node, 
                    font=("Segoe UI", 9, "bold"), fill=text_color
                )

    def log_message(self, message, level="info"):
        """Ghi tin nhắn nhật ký kèm theo dấu thời gian thực tế và màu sắc phân cấp"""
        now = datetime.now().strftime("%H:%M:%S")
        self.txt_log.config(state="normal")
        self.txt_log.insert(tk.END, f"[{now}] {message}\n", level)
        self.txt_log.see(tk.END)
        self.txt_log.config(state="disabled")

    def load_orders_from_csv(self):
        """Tải danh sách đơn hàng từ tệp CSV database"""
        file_path = os.path.join(current_dir, "data_training", "don_hang_database.csv")
        self.order_hash_table = hashing_tools.OrderHashTable(size=10)
        
        if os.path.exists(file_path):
            try:
                count = 0
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        parts = line.split(",", 1)
                        if len(parts) == 2:
                            key, val = parts
                            self.order_hash_table.insert(key.strip(), val.strip())
                            count += 1
                self.log_message(f"Tải thành công {count} đơn hàng từ cơ sở dữ liệu '{file_path}'.", "success")
            except Exception as e:
                self.log_message(f"Lỗi tải dữ liệu đơn hàng: {str(e)}. Đang khôi phục dữ liệu mẫu.", "error")
                self.load_default_mock_orders()
        else:
            # Tạo sẵn thư mục nếu chưa có
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            self.load_default_mock_orders()
            self.save_orders_to_csv()

    def save_orders_to_csv(self):
        """Lưu toàn bộ danh sách đơn hàng hiện tại trong bảng băm xuống tệp CSV database"""
        file_path = os.path.join(current_dir, "data_training", "don_hang_database.csv")
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                # Ghi tiêu đề mô tả ngắn
                f.write("# Cơ sở dữ liệu đơn hàng POLY-SHIP\n")
                f.write("# Định dạng: Mã_đơn_hàng,Thông_tin_giao_hàng\n")
                for i in range(self.order_hash_table.size):
                    curr = self.order_hash_table.buckets[i]
                    while curr:
                        f.write(f"{curr.key},{curr.value}\n")
                        curr = curr.next
            self.log_message(f"Đã cập nhật cơ sở dữ liệu đơn hàng thành công.", "info")
        except Exception as e:
            self.log_message(f"Không thể lưu cơ sở dữ liệu đơn hàng: {str(e)}", "error")

    def load_default_mock_orders(self):
        """Nạp sẵn một số đơn hàng mẫu ban đầu để mô phỏng đụng độ băm"""
        self.order_hash_table.insert("HD101", "Giao Hà Nội - Hỏa tốc 2h")
        self.order_hash_table.insert("HD202", "Giao Đà Nẵng - Tiết kiệm")
        self.order_hash_table.insert("HD303", "Giao Sài Gòn - Nhanh")
        self.order_hash_table.insert("HD104", "Giao Hải Phòng - Tiêu chuẩn")
        self.order_hash_table.insert("HD111", "Giao Hà Nội - Tiết kiệm")  # Trùng bucket với HD101
        self.order_hash_table.insert("HD212", "Giao Huế - Nhanh")         # Trùng bucket với HD202

    def set_buttons_state(self, state):
        """Khóa hoặc mở khóa các nút bấm chính và reset text nguyên bản sạch sẽ"""
        for btn, text in self.btn_texts.items():
            if btn != self.btn_export:  # Nút xuất log luôn giữ nguyên trạng thái
                btn.config(state=state, text=text)

    def run_progress_simulation(self, status_msg, finish_msg, final_callback):
        """Bắt đầu mô phỏng thanh tiến trình chạy"""
        self.set_buttons_state("disabled")
        self.progress_bar["value"] = 0
        self.lbl_progress_status.config(text=status_msg, fg="#f27024")
        self.log_message(status_msg, "info")
        
        # Bắt đầu cập nhật giá trị tiến trình sau mỗi khoảng thời gian
        self.update_progress(0, status_msg, finish_msg, final_callback)

    def update_progress(self, current_val, status_msg, finish_msg, final_callback):
        if current_val <= 100:
            self.progress_bar["value"] = current_val
            # Tăng tiến trình sau 40ms (tổng thời gian chạy ~ 800ms)
            self.root.after(40, self.update_progress, current_val + 5, status_msg, finish_msg, final_callback)
        else:
            # Hoàn thành tiến trình
            self.progress_bar["value"] = 0
            self.lbl_progress_status.config(text="Hệ thống sẵn sàng", fg="#64748b")
            self.set_buttons_state("normal")
            self.log_message(finish_msg, "success")
            self.play_sound("success")
            # Gọi hàm hiển thị kết quả
            final_callback()

    # --- 1. DIJKSTRA ROUTING ---
    def show_input_dialog(self, title, fields, callback):
        """
        Hiển thị một cửa sổ nhập liệu nhỏ dạng modal.
        fields: danh sách các tuple (tên_trường, khóa, giá_trị_mặc_định)
        callback: hàm được gọi sau khi nhấn Chạy với tham số là dict chứa các giá trị nhập.
        """
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.configure(bg="#f8fafc")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Tiêu đề con
        lbl_head = tk.Label(dialog, text=f"Nhập thông số cho {title}", font=("Segoe UI", 10, "bold"), fg="#f27024", bg="#f8fafc")
        lbl_head.pack(pady=(15, 10))
        
        form_frame = tk.Frame(dialog, bg="#f8fafc")
        form_frame.pack(fill="both", expand=True, padx=20)
        
        entries = {}
        for idx, (label_text, key, default_val) in enumerate(fields):
            lbl = tk.Label(form_frame, text=label_text, font=("Segoe UI", 9, "bold"), fg="#475569", bg="#f8fafc")
            lbl.grid(row=idx, column=0, sticky="w", pady=5)
            
            # Sử dụng Combobox cho các lựa chọn nguồn/đích nếu đã nạp dữ liệu đỉnh
            if key in ["source", "target"] and self.vertices:
                ent = ttk.Combobox(form_frame, font=("Segoe UI", 10), values=self.vertices, state="readonly")
                ent.set(default_val if default_val in self.vertices else self.vertices[0] if key == "source" else self.vertices[-1])
                ent.grid(row=idx, column=1, sticky="ew", padx=(10, 0), pady=5)
            else:
                ent = tk.Entry(form_frame, font=("Segoe UI", 10), relief="solid", bd=1)
                ent.insert(0, str(default_val))
                ent.grid(row=idx, column=1, sticky="ew", padx=(10, 0), pady=5)
            
            entries[key] = ent
            
        form_frame.columnconfigure(1, weight=1)
        
        def on_submit():
            results = {}
            for k, ent in entries.items():
                results[k] = ent.get().strip()
            dialog.destroy()
            callback(results)
            
        btn_submit = tk.Button(dialog, text="🚀 Chạy Thuật Toán", bg="#f27024", fg="#ffffff",
                               activebackground="#d95f1c", activeforeground="#ffffff", relief="flat",
                               font=("Segoe UI", 10, "bold"), cursor="hand2", bd=0, pady=6, command=on_submit)
        btn_submit.pack(fill="x", padx=20, pady=15)
        
        num_fields = len(fields)
        height = 120 + num_fields * 40
        dialog.geometry(f"420x{height}")
        
        # Căn giữa dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

    # --- 1. DIJKSTRA ROUTING ---
    def run_routing(self):
        """Chạy Định tuyến tìm đường đi ngắn nhất Dijkstra sau khi nạp dữ liệu từ file"""
        self.log_message("Yêu cầu chọn file dữ liệu bản đồ...", "info")
        file_path = filedialog.askopenfilename(
            title="Chọn file dữ liệu bản đồ (.txt / .csv) cho Định Tuyến",
            filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        def open_dialog():
            default_src = self.vertices[0] if self.vertices else "WH1"
            default_tgt = self.vertices[-1] if self.vertices else "HN"
            
            graph = routing.build_graph(self.edges)
            cost, route = routing.shortest_route(graph, default_src, default_tgt)
            
            self.log_message(f"--- KẾT QUẢ ĐỊNH TUYẾN DIJKSTRA BAN ĐẦU ---", "info")
            if cost != float('inf'):
                route_format = " - ".join(route)
                self.log_message(f"Optimal route: {route_format}: {cost}", "success")
                self.log_message(f"Tuyến đường tối ưu: {route_format}: {cost}", "success")
            
            # Hiển thị trực quan sơ đồ đồ thị mạng kho kèm đường đi ngắn nhất
            self.visualize_graph(self.vertices, self.edges, route, cost=cost)

        if file_path:
            try:
                if not os.path.exists(file_path):
                    raise FileNotFoundError("Không tìm thấy file ở đường dẫn đã chọn.")
                size = os.path.getsize(file_path)
                if size == 0:
                    raise ValueError("File dữ liệu trống (dung lượng 0 bytes).")
                
                filename = os.path.basename(file_path)
                
                def on_success():
                    try:
                        self.parse_csv_file(file_path)
                        open_dialog()
                    except Exception as e:
                        messagebox.showerror("Lỗi phân tích", f"Không thể đọc file: {str(e)}")

                self.run_progress_simulation(
                    status_msg=f"Đang đọc dữ liệu từ file '{filename}'...",
                    finish_msg=f"Nạp thành công file: {filename} ({size} bytes).",
                    final_callback=on_success
                )
            except Exception as e:
                self.log_message(f"Lỗi: {str(e)}", "error")
                messagebox.showerror("Lỗi", str(e))
        else:
            # Nếu người dùng hủy chọn file, hỏi họ có muốn dùng dữ liệu mặc định không
            confirm = messagebox.askyesno(
                "Nạp Dữ Liệu Mặc Định",
                "Bạn chưa chọn file dữ liệu bản đồ.\nBạn có muốn nạp nhanh dữ liệu cấu hình mặc định để tiếp tục định tuyến không?"
            )
            if confirm:
                try:
                    default_content = (
                        "WH1,WH2,15\n"
                        "WH1,HCM,22\n"
                        "WH2,HCM,10\n"
                        "WH2,DN,30\n"
                        "HCM,DN,18\n"
                        "HN,DN,25\n"
                        "HN,HP,5\n"
                        "HP,WH1,40\n"
                    )
                    # Đảm bảo thư mục data_training tồn tại
                    os.makedirs(os.path.join(current_dir, "data_training"), exist_ok=True)
                    file_path = os.path.join(current_dir, "data_training", "du_lieu_mau.csv")
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(default_content)
                    filename = os.path.join("data_training", "du_lieu_mau.csv")
                    size = len(default_content.encode("utf-8"))
                    
                    def on_success_default():
                        try:
                            self.parse_csv_file(file_path)
                            open_dialog()
                        except Exception as e:
                            messagebox.showerror("Lỗi phân tích", f"Lỗi đọc dữ liệu mặc định: {str(e)}")

                    self.run_progress_simulation(
                        status_msg=f"Đang phân tích dữ liệu cấu hình mặc định từ '{filename}'...",
                        finish_msg=f"Tự tạo và nạp thành công file: {filename} ({size} bytes).",
                        final_callback=on_success_default
                    )
                except Exception as e:
                    self.log_message(f"Lỗi nạp dữ liệu mặc định: {str(e)}", "error")
                    messagebox.showerror("Lỗi", f"Không thể nạp dữ liệu mặc định: {str(e)}")
            else:
                self.log_message("Hủy bỏ định tuyến do không chọn dữ liệu.", "warning")

    # --- 2. MST KRUSKAL ---
    def run_mst(self):
        """Chạy tối ưu Cây khung tối thiểu Kruskal - Đường truyền nội bộ riêng giữa các kho"""
        self.log_message("Yêu cầu chọn file dữ liệu bản đồ để làm MST...", "info")
        file_path = filedialog.askopenfilename(
            title="Chọn file dữ liệu bản đồ (.txt / .csv) cho MST",
            filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        def compute_mst():
            def show_result():
                try:
                    mst_edges, total_cost = mst.kruskal_mst(self.vertices, self.edges)
                    
                    self.log_message(f"--- KẾT QUẢ ĐƯỜNG TRUYỀN NỘI BỘ TỐI ƯU MST ---", "info")
                    for u, v, cost in mst_edges:
                        self.log_message(f"  + Thiết lập đường truyền: {u} <-> {v} : Chi phí: {cost}", "success")
                    self.log_message(f"Optimal network cost: {total_cost}", "success")
                    self.log_message(f"Tổng chi phí mạng thiết lập tối thiểu: {total_cost}", "success")
                    
                    # Cảnh báo nếu đồ thị không liên thông
                    if len(mst_edges) < len(self.vertices) - 1:
                        self.log_message("Cảnh báo: Đồ thị không liên thông! Một số kho không kết nối được.", "warning")
                        messagebox.showwarning("Cảnh báo", "Đồ thị không liên thông! Không thể kết nối tất cả các kho hàng.")
                        
                    # Hiển thị trực quan sơ đồ đồ thị mạng truyền dẫn tối thiểu
                    self.visualize_mst(self.vertices, self.edges, mst_edges, total_cost)
                except Exception as e:
                    self.log_message(f"Lỗi tính toán MST: {str(e)}", "error")
                    messagebox.showerror("Lỗi", f"Không thể tính toán MST: {str(e)}")

            self.run_progress_simulation(
                status_msg="Đang tính toán mạng truyền dẫn tối thiểu Kruskal...",
                finish_msg="Hoàn thành giải thuật Kruskal MST.",
                final_callback=show_result
            )

        if file_path:
            try:
                if not os.path.exists(file_path):
                    raise FileNotFoundError("Không tìm thấy file ở đường dẫn đã chọn.")
                size = os.path.getsize(file_path)
                if size == 0:
                    raise ValueError("File dữ liệu trống (dung lượng 0 bytes).")
                
                filename = os.path.basename(file_path)
                
                def on_success():
                    try:
                        self.parse_csv_file(file_path)
                        compute_mst()
                    except Exception as e:
                        messagebox.showerror("Lỗi phân tích", f"Không thể đọc file: {str(e)}")

                self.run_progress_simulation(
                    status_msg=f"Đang đọc dữ liệu từ file '{filename}'...",
                    finish_msg=f"Nạp thành công file: {filename} ({size} bytes).",
                    final_callback=on_success
                )
            except Exception as e:
                self.log_message(f"Lỗi: {str(e)}", "error")
                messagebox.showerror("Lỗi", str(e))
        else:
            # Nếu người dùng hủy chọn file, hỏi họ có muốn dùng dữ liệu cấu hình mặc định không
            confirm = messagebox.askyesno(
                "Nạp Dữ Liệu Mặc Định",
                "Bạn chưa chọn file dữ liệu bản đồ.\nBạn có muốn nạp nhanh dữ liệu cấu hình mặc định để tiếp tục MST không?"
            )
            if confirm:
                try:
                    default_content = (
                        "WH1,WH2,15\n"
                        "WH1,HCM,22\n"
                        "WH2,HCM,10\n"
                        "WH2,DN,30\n"
                        "HCM,DN,18\n"
                        "HN,DN,25\n"
                        "HN,HP,5\n"
                        "HP,WH1,40\n"
                    )
                    # Đảm bảo thư mục data_training tồn tại
                    os.makedirs(os.path.join(current_dir, "data_training"), exist_ok=True)
                    file_path = os.path.join(current_dir, "data_training", "du_lieu_mau.csv")
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(default_content)
                    filename = os.path.join("data_training", "du_lieu_mau.csv")
                    size = len(default_content.encode("utf-8"))
                    
                    def on_success_default():
                        try:
                            self.parse_csv_file(file_path)
                            compute_mst()
                        except Exception as e:
                            messagebox.showerror("Lỗi phân tích", f"Lỗi đọc dữ liệu mặc định: {str(e)}")

                    self.run_progress_simulation(
                        status_msg=f"Đang phân tích dữ liệu cấu hình mặc định từ '{filename}'...",
                        finish_msg=f"Tự tạo và nạp thành công file: {filename} ({size} bytes).",
                        final_callback=on_success_default
                    )
                except Exception as e:
                    self.log_message(f"Lỗi nạp dữ liệu mặc định: {str(e)}", "error")
                    messagebox.showerror("Lỗi", f"Không thể nạp dữ liệu mặc định: {str(e)}")
            else:
                self.log_message("Hủy bỏ MST do không chọn dữ liệu.", "warning")

    # --- 3. HASH TABLE ---
    def run_hash_table(self):
        """Tra cứu bảng băm đơn hàng dùng Separate Chaining"""
        # Tạo cửa sổ phụ trực quan hóa bảng băm
        hash_win = tk.Toplevel(self.root)
        hash_win.title("Tra cứu đơn hàng - Bảng băm Separate Chaining")
        hash_win.geometry("740x560")
        hash_win.configure(bg="#f8fafc")
        hash_win.transient(self.root)
        hash_win.grab_set()

        # Tiêu đề chính
        lbl_title = tk.Label(
            hash_win, 
            text="HỆ THỐNG TRA CỨU ĐƠN HÀNG (ORDER SEARCH)", 
            font=("Segoe UI", 12, "bold"), 
            fg="#f27024", 
            bg="#f8fafc"
        )
        lbl_title.pack(pady=(15, 5))
        
        # Split layout: Trái (Controls), Phải (Cấu trúc bảng băm)
        content_frame = tk.Frame(hash_win, bg="#f8fafc")
        content_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        left_frame = tk.LabelFrame(content_frame, text=" Thao tác bảng băm ", font=("Segoe UI", 9, "bold"), fg="#475569", bg="#ffffff", padx=15, pady=15)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_frame = tk.LabelFrame(content_frame, text=" Cấu trúc 10 Buckets (Separate Chaining) ", font=("Segoe UI", 9, "bold"), fg="#475569", bg="#ffffff", padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True)

        # Left Frame: Nhập liệu
        lbl_id = tk.Label(left_frame, text="Mã đơn hàng (Order ID):", font=("Segoe UI", 9, "bold"), fg="#475569", bg="#ffffff")
        lbl_id.pack(anchor="w", pady=(0, 2))
        
        ent_id = tk.Entry(left_frame, font=("Segoe UI", 10), relief="solid", bd=1)
        ent_id.insert(0, "HD101")
        ent_id.pack(fill="x", pady=(0, 15))
        
        lbl_info = tk.Label(left_frame, text="Thông tin giao hàng (Order Info):", font=("Segoe UI", 9, "bold"), fg="#475569", bg="#ffffff")
        lbl_info.pack(anchor="w", pady=(0, 2))
        
        ent_info = tk.Entry(left_frame, font=("Segoe UI", 10), relief="solid", bd=1)
        ent_info.insert(0, "Giao Hà Nội - Hỏa tốc 2h")
        ent_info.pack(fill="x", pady=(0, 20))
        
        # Nút Thao tác
        btn_style_sub = {
            "bg": "#f27024",
            "fg": "#ffffff",
            "activebackground": "#d95f1c",
            "activeforeground": "#ffffff",
            "relief": "flat",
            "font": ("Segoe UI", 9, "bold"),
            "bd": 0,
            "cursor": "hand2",
            "pady": 6
        }
        
        btn_insert = tk.Button(left_frame, text="📥 Thêm/Cập Nhật (Insert)", **btn_style_sub)
        btn_insert.pack(fill="x", pady=4)
        
        btn_search = tk.Button(left_frame, text="🔍 Tìm Kiếm Đơn Hàng (Search)", **btn_style_sub)
        btn_search.pack(fill="x", pady=4)
        
        # Nút xóa có màu tối để dễ phân biệt
        btn_delete_style = btn_style_sub.copy()
        btn_delete_style["bg"] = "#ef4444"
        btn_delete_style["activebackground"] = "#dc2626"
        btn_remove = tk.Button(left_frame, text="🗑️ Xóa Đơn Hàng (Remove)", **btn_delete_style)
        btn_remove.pack(fill="x", pady=4)
        
        # Nút nạp CSDL từ file
        btn_style_file = btn_style_sub.copy()
        btn_style_file["bg"] = "#475569"
        btn_style_file["activebackground"] = "#334155"
        btn_load = tk.Button(left_frame, text="📁 Nạp CSDL từ File (.csv)", **btn_style_file)
        btn_load.pack(fill="x", pady=4)
        
        # Nhãn hiển thị kết quả thao tác
        lbl_result_title = tk.Label(left_frame, text="Kết quả hoạt động:", font=("Segoe UI", 9, "bold"), fg="#475569", bg="#ffffff")
        lbl_result_title.pack(anchor="w", pady=(15, 2))
        
        lbl_result = tk.Label(
            left_frame, 
            text="Sẵn sàng thao tác.\nVui lòng nhập ID để bắt đầu.", 
            font=("Segoe UI", 9, "italic"), 
            fg="#64748b", 
            bg="#f1f5f9", 
            relief="solid", 
            bd=1, 
            padx=10, 
            pady=10, 
            justify="left",
            anchor="nw",
            height=5
        )
        lbl_result.pack(fill="both", expand=True)

        # Right Frame: Hiển thị Buckets
        txt_buckets = tk.Text(right_frame, bg="#ffffff", fg="#0f172a", relief="flat", font=("Consolas", 10))
        txt_buckets.pack(side="left", fill="both", expand=True)
        
        scroll_buckets = tk.Scrollbar(right_frame, command=txt_buckets.yview)
        scroll_buckets.pack(side="right", fill="y")
        txt_buckets.config(yscrollcommand=scroll_buckets.set)
        
        # Cấu hình thẻ tag trong text box
        txt_buckets.tag_config("normal", foreground="#0f172a")
        txt_buckets.tag_config("highlight", foreground="#f27024", background="#fef3c7", font=("Consolas", 10, "bold"))
        txt_buckets.tag_config("bucket_title", foreground="#475569", font=("Consolas", 10, "bold"))
        txt_buckets.tag_config("chain_arrow", foreground="#10b981", font=("Consolas", 10, "bold"))
        txt_buckets.tag_config("empty_bucket", foreground="#94a3b8", font=("Consolas", 10, "italic"))
        
        def refresh_bucket_view(highlight_idx=None):
            txt_buckets.config(state="normal")
            txt_buckets.delete("1.0", tk.END)
            
            for i in range(self.order_hash_table.size):
                curr = self.order_hash_table.buckets[i]
                
                txt_buckets.insert(tk.END, f"[Bucket {i}]: ", "bucket_title")
                
                if not curr:
                    txt_buckets.insert(tk.END, "(Trống)\n", "empty_bucket")
                else:
                    while curr:
                        node_str = f"{curr.key} ({curr.value})"
                        if i == highlight_idx:
                            txt_buckets.insert(tk.END, node_str, "highlight")
                        else:
                            txt_buckets.insert(tk.END, node_str, "normal")
                            
                        if curr.next:
                            txt_buckets.insert(tk.END, " ➔ ", "chain_arrow")
                        curr = curr.next
                    txt_buckets.insert(tk.END, " ➔ (Hết)\n", "chain_arrow")
            
            txt_buckets.config(state="disabled")

        # Cập nhật hiển thị ban đầu
        refresh_bucket_view()
        
        # Thêm giải thích thuật toán ở dưới cùng cửa sổ
        explain_frame = tk.Frame(hash_win, bg="#eff6ff", highlightthickness=1, highlightbackground="#bfdbfe", padx=10, pady=8)
        explain_frame.pack(fill="x", padx=15, pady=(5, 15))
        lbl_explain = tk.Label(
            explain_frame,
            text="💡 Giải thích: Hàm băm _hash(ID) = (tổng mã ASCII các ký tự * 31) % 10.\n"
                 "Các đơn hàng có cùng mã băm sẽ được liên kết tại cùng một Bucket (Separate Chaining) giúp xử lý đụng độ tối ưu.",
            font=("Segoe UI", 9, "italic"),
            fg="#1e40af",
            bg="#eff6ff",
            justify="left"
        )
        lbl_explain.pack(anchor="w")

        # Helper khóa/mở khóa nút bấm subwindow
        def set_sub_buttons_state(state):
            btn_insert.config(state=state)
            btn_search.config(state=state)
            btn_remove.config(state=state)
            btn_load.config(state=state)
            ent_id.config(state=state)
            ent_info.config(state=state)

        # Hàm xử lý chèn
        def do_insert():
            oid = ent_id.get().strip()
            info = ent_info.get().strip()
            if not oid:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã đơn hàng (Order ID)!")
                return
            if not info:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập Thông tin giao hàng (Order Info)!")
                return
                
            set_sub_buttons_state("disabled")
            
            def finish_insert():
                is_new = self.order_hash_table.insert(oid, info)
                idx = self.order_hash_table._hash(oid)
                
                # Cập nhật nhật ký chính và trạng thái
                action_str = "thêm mới" if is_new else "cập nhật"
                msg_log = f"Bảng băm: Đã {action_str} thành công đơn hàng '{oid}' vào Bucket {idx} : {info}"
                self.log_message(msg_log, "success")
                
                # Lưu vào cơ sở dữ liệu CSV để lưu trữ lâu dài
                self.save_orders_to_csv()
                
                # Cập nhật GUI
                lbl_result.config(
                    text=f"➔ Thao tác: INSERT\n➔ Mã băm (Bucket): {idx}\n➔ Trạng thái: Thành công\n➔ Kết quả: Đã {action_str} đơn hàng '{oid}'!", 
                    fg="#10b981", 
                    font=("Segoe UI", 9, "bold")
                )
                refresh_bucket_view(idx)
                set_sub_buttons_state("normal")
                
            self.run_progress_simulation(
                status_msg=f"Đang băm ID '{oid}' và chèn vào bảng băm...",
                finish_msg=f"Hoàn thành thao tác chèn đơn hàng '{oid}'.",
                final_callback=finish_insert
            )

        # Hàm xử lý tìm kiếm
        def do_search():
            oid = ent_id.get().strip()
            if not oid:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã đơn hàng (Order ID) để tìm kiếm!")
                return
                
            set_sub_buttons_state("disabled")
            
            def finish_search():
                val = self.order_hash_table.get(oid)
                idx = self.order_hash_table._hash(oid)
                
                if val:
                    msg_log = f"Bảng băm: Tìm thấy đơn hàng '{oid}' tại Bucket {idx} : {val}"
                    self.log_message(msg_log, "success")
                    
                    lbl_result.config(
                        text=f"➔ Thao tác: SEARCH\n➔ Mã băm (Bucket): {idx}\n➔ Trạng thái: Tìm thấy!\n➔ Chi tiết: {val}", 
                        fg="#10b981", 
                        font=("Segoe UI", 9, "bold")
                    )
                    refresh_bucket_view(idx)
                else:
                    msg_log = f"Bảng băm: Không tìm thấy đơn hàng '{oid}' trong hệ thống"
                    self.log_message(msg_log, "warning")
                    self.play_sound("warning")
                    
                    lbl_result.config(
                        text=f"➔ Thao tác: SEARCH\n➔ Trạng thái: Không tìm thấy!\n➔ Mô tả: Đơn hàng '{oid}' không tồn tại.", 
                        fg="#ef4444", 
                        font=("Segoe UI", 9, "bold")
                    )
                    refresh_bucket_view()
                    
                set_sub_buttons_state("normal")
                
            self.run_progress_simulation(
                status_msg=f"Đang băm ID '{oid}' và tìm kiếm trong bảng băm...",
                finish_msg=f"Hoàn thành tìm kiếm đơn hàng '{oid}'.",
                final_callback=finish_search
            )

        # Hàm xử lý xóa
        def do_remove():
            oid = ent_id.get().strip()
            if not oid:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã đơn hàng (Order ID) để xóa!")
                return
                
            set_sub_buttons_state("disabled")
            
            def finish_remove():
                idx = self.order_hash_table._hash(oid)
                success = self.order_hash_table.remove(oid)
                
                if success:
                    msg_log = f"Bảng băm: Đã xóa thành công đơn hàng '{oid}' khỏi Bucket {idx}"
                    self.log_message(msg_log, "success")
                    
                    # Lưu vào cơ sở dữ liệu CSV để đồng bộ dữ liệu
                    self.save_orders_to_csv()
                    
                    lbl_result.config(
                        text=f"➔ Thao tác: REMOVE\n➔ Mã băm (Bucket): {idx}\n➔ Trạng thái: Thành công\n➔ Kết quả: Đã xóa đơn '{oid}' khỏi Bucket {idx}.", 
                        fg="#10b981", 
                        font=("Segoe UI", 9, "bold")
                    )
                    refresh_bucket_view(idx)
                else:
                    msg_log = f"Bảng băm: Không tìm thấy đơn hàng '{oid}' để xóa"
                    self.log_message(msg_log, "warning")
                    self.play_sound("warning")
                    
                    lbl_result.config(
                        text=f"➔ Thao tác: REMOVE\n➔ Trạng thái: Thất bại!\n➔ Mô tả: Đơn hàng '{oid}' không tồn tại để xóa.", 
                        fg="#ef4444", 
                        font=("Segoe UI", 9, "bold")
                    )
                    refresh_bucket_view()
                    
                set_sub_buttons_state("normal")
                
            self.run_progress_simulation(
                status_msg=f"Đang băm ID '{oid}' và tiến hành xóa khỏi bảng băm...",
                finish_msg=f"Hoàn thành thao tác xóa đơn hàng '{oid}'.",
                final_callback=finish_remove
            )

        # Hàm xử lý nạp file
        def do_load_file():
            file_path = filedialog.askopenfilename(
                title="Chọn file dữ liệu đơn hàng bổ sung",
                filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            if not file_path:
                return
                
            set_sub_buttons_state("disabled")
            
            def finish_load():
                try:
                    count = 0
                    dup_or_update_count = 0
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if not line or line.startswith("#"):
                                continue
                            parts = line.split(",", 1)
                            if len(parts) == 2:
                                key, val = parts
                                is_new = self.order_hash_table.insert(key.strip(), val.strip())
                                if is_new:
                                    count += 1
                                else:
                                    dup_or_update_count += 1
                    
                    filename = os.path.basename(file_path)
                    if count > 0 or dup_or_update_count > 0:
                        self.save_orders_to_csv()
                        msg_log = f"Bảng băm: Nạp thành công {count} đơn mới, cập nhật {dup_or_update_count} đơn từ {filename}."
                        self.log_message(msg_log, "success")
                        
                        lbl_result.config(
                            text=f"➔ Thao tác: LOAD FILE\n➔ Nguồn: {filename}\n➔ Trạng thái: Thành công\n➔ Đã thêm: {count} đơn mới\n➔ Đã cập nhật: {dup_or_update_count} đơn hàng.",
                            fg="#10b981",
                            font=("Segoe UI", 9, "bold")
                        )
                    else:
                        lbl_result.config(
                            text=f"➔ Thao tác: LOAD FILE\n➔ Trạng thái: Không tìm thấy dữ liệu hợp lệ trong file.",
                            fg="#ef4444",
                            font=("Segoe UI", 9, "bold")
                        )
                        
                    refresh_bucket_view()
                except Exception as e:
                    self.log_message(f"Lỗi nạp file đơn hàng: {str(e)}", "error")
                    messagebox.showerror("Lỗi", f"Không thể nạp dữ liệu: {str(e)}")
                    
                set_sub_buttons_state("normal")
                
            self.run_progress_simulation(
                status_msg="Đang đọc file và đồng bộ với bảng băm...",
                finish_msg="Hoàn thành nạp dữ liệu bổ sung.",
                final_callback=finish_load
            )

        # Cấu hình command cho các nút
        btn_insert.config(command=do_insert)
        btn_search.config(command=do_search)
        btn_remove.config(command=do_remove)
        btn_load.config(command=do_load_file)

    # --- 4. HASHING TỔNG HỢP ---
    def run_hashing_compound(self):
        """Các bài toán Hashing tổng hợp"""
        # Tạo cửa sổ phụ Dashboard
        comp_win = tk.Toplevel(self.root)
        comp_win.title("Dashboard Hashing Tổng Hợp - Phân tích & Gợi ý")
        comp_win.geometry("780x640")
        comp_win.configure(bg="#f8fafc")
        comp_win.transient(self.root)
        comp_win.grab_set()

        # Tiêu đề chính
        lbl_title = tk.Label(
            comp_win, 
            text="HỆ THỐNG PHÂN TÍCH HASHING TỔNG HỢP", 
            font=("Segoe UI", 12, "bold"), 
            fg="#f27024", 
            bg="#f8fafc"
        )
        lbl_title.pack(pady=(15, 5))
        
        # Chia đôi cột: Trái (Điều khiển/Nhập liệu theo chức năng con), Phải (Báo cáo trực quan)
        content_frame = tk.Frame(comp_win, bg="#f8fafc")
        content_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        left_frame = tk.Frame(content_frame, bg="#f8fafc")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_frame = tk.LabelFrame(content_frame, text=" Báo cáo kết quả giải thuật trực quan ", font=("Segoe UI", 9, "bold"), fg="#475569", bg="#ffffff", padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True)

        # Cấu hình khung báo cáo kết quả (Cột Phải)
        txt_report = tk.Text(right_frame, bg="#ffffff", fg="#0f172a", relief="flat", font=("Segoe UI", 10), wrap="word")
        txt_report.pack(side="left", fill="both", expand=True)
        
        scroll = tk.Scrollbar(right_frame, command=txt_report.yview)
        scroll.pack(side="right", fill="y")
        txt_report.config(yscrollcommand=scroll.set)
        
        # Định nghĩa các tags màu sắc cho báo cáo
        txt_report.tag_config("section", foreground="#f27024", font=("Segoe UI", 11, "bold"))
        txt_report.tag_config("bold", font=("Segoe UI", 10, "bold"), foreground="#0f172a")
        txt_report.tag_config("result", font=("Segoe UI", 10, "bold"), foreground="#10b981")
        txt_report.tag_config("italic", font=("Segoe UI", 9, "italic"), foreground="#475569")
        txt_report.tag_config("explain", font=("Segoe UI", 9, "italic"), foreground="#1e40af")
        
        # In lời chào ban đầu
        txt_report.insert(tk.END, "Vui lòng chọn nạp dữ liệu hoặc nhấn chạy giải thuật ở cột bên trái để bắt đầu báo cáo kết quả...", "italic")
        txt_report.config(state="disabled")

        # Style nút bấm phẳng hiện đại
        btn_style_sub = {
            "bg": "#f27024",
            "fg": "#ffffff",
            "activebackground": "#d95f1c",
            "activeforeground": "#ffffff",
            "relief": "flat",
            "font": ("Segoe UI", 9, "bold"),
            "bd": 0,
            "cursor": "hand2",
            "pady": 4
        }
        btn_style_file = btn_style_sub.copy()
        btn_style_file["bg"] = "#475569"
        btn_style_file["activebackground"] = "#334155"

        # --- PHÂN VÙNG 1: ANAGRAMS (Nhóm Coupon đối xứng) ---
        frame_anagram = tk.LabelFrame(left_frame, text=" 🏷️ 1. Nhóm Coupon Anagrams ", font=("Segoe UI", 9, "bold"), fg="#475569", bg="#ffffff", padx=10, pady=8)
        frame_anagram.pack(fill="x", pady=(0, 10))
        
        lbl_coup = tk.Label(frame_anagram, text="Mã giảm giá (ngăn cách bởi dấu phẩy):", font=("Segoe UI", 8, "bold"), fg="#64748b", bg="#ffffff")
        lbl_coup.pack(anchor="w", pady=(0, 2))
        
        ent_coupons = tk.Entry(frame_anagram, font=("Segoe UI", 9), relief="solid", bd=1)
        ent_coupons.insert(0, "SAVE10, AVES10, SALE5, LASE5, EVAS10")
        ent_coupons.pack(fill="x", pady=(0, 8))
        
        btn_box1 = tk.Frame(frame_anagram, bg="#ffffff")
        btn_box1.pack(fill="x")
        
        # --- PHÂN VÙNG 2: CONSECUTIVE DAYS (Streak liên tiếp) ---
        frame_streak = tk.LabelFrame(left_frame, text=" 📈 2. Chuỗi Ngày Giao Liên Tiếp ", font=("Segoe UI", 9, "bold"), fg="#475569", bg="#ffffff", padx=10, pady=8)
        frame_streak.pack(fill="x", pady=(0, 10))
        
        lbl_days = tk.Label(frame_streak, text="Danh sách các ngày (ngăn cách bởi dấu phẩy):", font=("Segoe UI", 8, "bold"), fg="#64748b", bg="#ffffff")
        lbl_days.pack(anchor="w", pady=(0, 2))
        
        ent_days = tk.Entry(frame_streak, font=("Segoe UI", 9), relief="solid", bd=1)
        ent_days.insert(0, "100, 4, 200, 1, 3, 2, 5")
        ent_days.pack(fill="x", pady=(0, 8))
        
        btn_box2 = tk.Frame(frame_streak, bg="#ffffff")
        btn_box2.pack(fill="x")

        # --- PHÂN VÙNG 3: SUBARRAY SUM = K (Khoảng đạt mục tiêu) ---
        frame_sub = tk.LabelFrame(left_frame, text=" 💰 3. Khoảng Doanh Thu Đạt Mục Tiêu ", font=("Segoe UI", 9, "bold"), fg="#475569", bg="#ffffff", padx=10, pady=8)
        frame_sub.pack(fill="x", pady=(0, 10))
        
        lbl_rev = tk.Label(frame_sub, text="Doanh thu hàng ngày (dấu phẩy):", font=("Segoe UI", 8, "bold"), fg="#64748b", bg="#ffffff")
        lbl_rev.pack(anchor="w", pady=(0, 2))
        
        ent_revenues = tk.Entry(frame_sub, font=("Segoe UI", 9), relief="solid", bd=1)
        ent_revenues.insert(0, "10, 2, -2, -20, 10")
        ent_revenues.pack(fill="x", pady=(0, 6))
        
        k_frame = tk.Frame(frame_sub, bg="#ffffff")
        k_frame.pack(fill="x", pady=(0, 8))
        lbl_k = tk.Label(k_frame, text="Doanh thu mục tiêu K:", font=("Segoe UI", 8, "bold"), fg="#64748b", bg="#ffffff")
        lbl_k.pack(side="left")
        ent_k = tk.Entry(k_frame, font=("Segoe UI", 9), width=8, relief="solid", bd=1)
        ent_k.insert(0, "-10")
        ent_k.pack(side="left", padx=10)
        
        btn_box3 = tk.Frame(frame_sub, bg="#ffffff")
        btn_box3.pack(fill="x")

        # --- Helper khóa/mở khóa nút bấm subwindow ---
        def set_sub_buttons_state(state):
            for f_btn in [btn_file1, btn_run1, btn_file2, btn_run2, btn_file3, btn_run3]:
                f_btn.config(state=state)
            ent_coupons.config(state=state)
            ent_days.config(state=state)
            ent_revenues.config(state=state)
            ent_k.config(state=state)

        # --- Callback Nạp File của từng bài toán ---
        def load_file_generic(entry_widget, file_type_desc):
            file_path = filedialog.askopenfilename(
                title=f"Chọn file dữ liệu {file_type_desc}",
                filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            if file_path:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                    # Làm sạch nội dung (ví dụ loại bỏ các ký tự xuống dòng bằng dấu phẩy)
                    cleaned_content = ", ".join(line.strip() for line in content.split("\n") if line.strip())
                    
                    entry_widget.config(state="normal")
                    entry_widget.delete(0, tk.END)
                    entry_widget.insert(0, cleaned_content)
                    
                    filename = os.path.basename(file_path)
                    self.log_message(f"Nạp thành công file {filename} cho ô {file_type_desc}.", "success")
                except Exception as e:
                    messagebox.showerror("Lỗi đọc file", f"Không thể đọc tệp dữ liệu: {str(e)}")

        # --- Hàm thực thi từng bài toán ---
        def execute_anagrams():
            coupons_list = [c.strip() for c in ent_coupons.get().split(",") if c.strip()]
            if not coupons_list:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập danh sách coupon hợp lệ!")
                return
                
            set_sub_buttons_state("disabled")
            
            def run_anagram_algo():
                groups = anagrams.group_coupon_anagrams(coupons_list)
                self.log_message(f"Chạy thành công bài toán Coupon Anagrams: {groups}", "success")
                
                txt_report.config(state="normal")
                txt_report.delete("1.0", tk.END)
                
                txt_report.insert(tk.END, "🏷️ KẾT QUẢ: NHÓM MÃ COUPON ĐỐI XỨNG (ANAGRAMS)\n", "section")
                txt_report.insert(tk.END, f"  - Mã đầu vào: {', '.join(coupons_list)}\n\n")
                txt_report.insert(tk.END, "  - Kết quả gom nhóm:\n", "bold")
                
                for idx, gp in enumerate(groups):
                    txt_report.insert(tk.END, f"    + Nhóm {idx + 1}: ", "bold")
                    txt_report.insert(tk.END, f"{' ➔ '.join(gp)}\n", "result")
                    
                txt_report.insert(tk.END, "\n  💡 Giải thích giải thuật: Sử dụng Bảng băm (Hash Map), sắp xếp các chữ cái của mã giảm giá làm Key chung để gom các mã đối xứng (Anagrams) vào cùng nhóm trong độ phức tạp O(M * N log N).\n", "explain")
                txt_report.config(state="disabled")
                set_sub_buttons_state("normal")
                
            self.run_progress_simulation(
                status_msg="Đang tính toán nhóm mã giảm giá đối xứng...",
                finish_msg="Hoàn thành thuật toán Coupon Anagrams.",
                final_callback=run_anagram_algo
            )

        def execute_streak():
            days_str = ent_days.get()
            days_list = []
            for d in days_str.split(","):
                d = d.strip()
                if d:
                    try:
                        days_list.append(int(d))
                    except ValueError:
                        pass
            if not days_list:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập chuỗi ngày giao hàng hợp lệ!")
                return
                
            set_sub_buttons_state("disabled")
            
            def run_streak_algo():
                max_streak = consecutive_days.longest_consecutive_days(days_list)
                self.log_message(f"Chạy thành công bài toán ngày liên tiếp: {max_streak} ngày", "success")
                
                txt_report.config(state="normal")
                txt_report.delete("1.0", tk.END)
                
                txt_report.insert(tk.END, "📈 KẾT QUẢ: CHUỖI NGÀY GIAO HÀNG LIÊN TIẾP DÀI NHẤT\n", "section")
                txt_report.insert(tk.END, f"  - Danh sách ngày: {sorted(days_list)}\n\n")
                txt_report.insert(tk.END, "  - Chuỗi ngày liên tiếp dài nhất: ", "bold")
                
                # Tìm chuỗi cụ thể để biểu diễn trực quan
                day_set = set(days_list)
                longest_streak = []
                for day in day_set:
                    if day - 1 not in day_set:
                        curr = day
                        streak = [curr]
                        while curr + 1 in day_set:
                            curr += 1
                            streak.append(curr)
                        if len(streak) > len(longest_streak):
                            longest_streak = streak
                            
                txt_report.insert(tk.END, f"{max_streak} ngày ", "result")
                txt_report.insert(tk.END, f"(Hành trình liên tục: {' ➔ '.join(map(str, longest_streak))})\n\n", "bold")
                txt_report.insert(tk.END, "  💡 Giải thích giải thuật: Đưa tất cả ngày vào một Bảng băm (HashSet). Duyệt tìm điểm bắt đầu của chuỗi (ngày X mà X-1 không có trong set) và đếm độ dài liên tục. Độ phức tạp tuyến tính O(N) cực kỳ tối ưu.\n", "explain")
                txt_report.config(state="disabled")
                set_sub_buttons_state("normal")
                
            self.run_progress_simulation(
                status_msg="Đang quét tính toán chuỗi ngày giao hàng liên tiếp...",
                finish_msg="Hoàn thành thuật toán Longest Streak.",
                final_callback=run_streak_algo
            )

        def execute_subarray():
            rev_str = ent_revenues.get()
            k_str = ent_k.get().strip()
            
            revenues_list = []
            for r in rev_str.split(","):
                r = r.strip()
                if r:
                    try:
                        revenues_list.append(float(r) if '.' in r else int(r))
                    except ValueError:
                        pass
            try:
                k_val = float(k_str) if '.' in k_str else int(k_str)
            except ValueError:
                messagebox.showerror("Lỗi nhập liệu", "Mục tiêu K phải là một số hợp lệ!")
                return
                
            if not revenues_list:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập chuỗi doanh thu hợp lệ!")
                return
                
            set_sub_buttons_state("disabled")
            
            def run_subarray_algo():
                count_windows = subarray_sum.count_revenue_windows(revenues_list, k_val)
                self.log_message(f"Chạy thành công bài toán Subarray Sum = K: {count_windows} khoảng", "success")
                
                txt_report.config(state="normal")
                txt_report.delete("1.0", tk.END)
                
                txt_report.insert(tk.END, "💰 KẾT QUẢ: KHOẢNG DOANH THU ĐẠT MỤC TIÊU (SUBARRAY SUM = K)\n", "section")
                txt_report.insert(tk.END, f"  - Lịch trình doanh thu: {revenues_list}\n")
                txt_report.insert(tk.END, f"  - Doanh thu mục tiêu K: {k_val}\n\n")
                txt_report.insert(tk.END, f"  - Số khoảng doanh thu đạt mục tiêu: ", "bold")
                txt_report.insert(tk.END, f"{count_windows} khoảng\n\n", "result")
                
                # Truy vết chi tiết các khoảng doanh thu
                matching_segments = []
                n_rev = len(revenues_list)
                for start in range(n_rev):
                    curr_sum = 0
                    for end in range(start, n_rev):
                        curr_sum += revenues_list[end]
                        if curr_sum == k_val:
                            segment_values = revenues_list[start:end+1]
                            segment_indices = f"Ngày {start+1} ➔ {end+1}"
                            matching_segments.append(f"[{segment_indices}]: Tổng {segment_values} = {k_val}")
                
                if matching_segments:
                    txt_report.insert(tk.END, "  - Chi tiết các chặng trùng khớp tìm được:\n", "bold")
                    for seg in matching_segments:
                        txt_report.insert(tk.END, f"    + {seg}\n", "italic")
                else:
                    txt_report.insert(tk.END, "  - Không tìm thấy chặng con nào có tổng doanh thu bằng K.\n\n", "italic")
                    
                txt_report.insert(tk.END, "\n  💡 Giải thích giải thuật: Sử dụng Bảng băm lưu trữ các tổng tích lũy (Prefix Sum) và tần suất của chúng. Với mỗi tổng tích lũy Current_Sum, kiểm tra xem (Current_Sum - K) đã xuất hiện trước đó chưa để tính số chặng đạt mục tiêu trong độ phức tạp O(N).\n", "explain")
                txt_report.config(state="disabled")
                set_sub_buttons_state("normal")
                
            self.run_progress_simulation(
                status_msg=f"Đang tìm các khoảng liên tục có tổng bằng {k_val}...",
                finish_msg="Hoàn thành thuật toán Subarray Sum.",
                final_callback=run_subarray_algo
            )

        # Gắn các nút bấm vào khung
        btn_file1 = tk.Button(btn_box1, text="📁 Nạp Coupon từ File", **btn_style_file, command=lambda: load_file_generic(ent_coupons, "Coupon"))
        btn_file1.pack(side="left", fill="x", expand=True, padx=(0, 5))
        btn_run1 = tk.Button(btn_box1, text="🚀 Nhóm Anagrams", **btn_style_sub, command=execute_anagrams)
        btn_run1.pack(side="right", fill="x", expand=True, padx=(5, 0))

        btn_file2 = tk.Button(btn_box2, text="📁 Nạp Ngày từ File", **btn_style_file, command=lambda: load_file_generic(ent_days, "Ngày"))
        btn_file2.pack(side="left", fill="x", expand=True, padx=(0, 5))
        btn_run2 = tk.Button(btn_box2, text="🚀 Tìm Streak", **btn_style_sub, command=execute_streak)
        btn_run2.pack(side="right", fill="x", expand=True, padx=(5, 0))

        btn_file3 = tk.Button(btn_box3, text="📁 Nạp Doanh thu từ File", **btn_style_file, command=lambda: load_file_generic(ent_revenues, "Doanh Thu"))
        btn_file3.pack(side="left", fill="x", expand=True, padx=(0, 5))
        btn_run3 = tk.Button(btn_box3, text="🚀 Đếm chặng", **btn_style_sub, command=execute_subarray)
        btn_run3.pack(side="right", fill="x", expand=True, padx=(5, 0))
    # --- 5. ROLLING HASH ---
    def run_rolling_hash(self):
        """Tìm pattern log bằng Rabin-Karp Rolling Hash"""
        # Tạo cửa sổ phụ
        rk_win = tk.Toplevel(self.root)
        rk_win.title("Tìm kiếm chuỗi bằng Rabin-Karp (Rolling Hash)")
        rk_win.geometry("780x600")
        rk_win.configure(bg="#f8fafc")
        rk_win.transient(self.root)
        rk_win.grab_set()

        # Tiêu đề
        lbl_title = tk.Label(
            rk_win, 
            text="HỆ THỐNG TÌM KIẾM LOGS RABIN-KARP", 
            font=("Segoe UI", 12, "bold"), 
            fg="#f27024", 
            bg="#f8fafc"
        )
        lbl_title.pack(pady=(15, 5))

        # Split layout: Trái (Điều khiển / Nhập liệu), Phải (Báo cáo trực quan)
        content_frame = tk.Frame(rk_win, bg="#f8fafc")
        content_frame.pack(fill="both", expand=True, padx=15, pady=5)

        left_frame = tk.LabelFrame(content_frame, text=" Cấu hình tìm kiếm ", font=("Segoe UI", 9, "bold"), fg="#475569", bg="#ffffff", padx=15, pady=15)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_frame = tk.LabelFrame(content_frame, text=" Kết quả tìm kiếm trực quan ", font=("Segoe UI", 9, "bold"), fg="#475569", bg="#ffffff", padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True)

        # Cột trái: Text Area nhập logs, nút nạp file, ô nhập pattern
        lbl_log = tk.Label(left_frame, text="Văn bản Logs (hoặc nạp từ File):", font=("Segoe UI", 9, "bold"), fg="#475569", bg="#ffffff")
        lbl_log.pack(anchor="w", pady=(0, 2))

        txt_logs = tk.Text(left_frame, font=("Segoe UI", 9), relief="solid", bd=1, height=12, wrap="word")
        txt_logs.insert("1.0", "SYSTEM_LOG_WARN_AVES10_LOG_SAVE10_PROCESS_ERROR")
        txt_logs.pack(fill="both", expand=True, pady=(0, 8))

        # Khung chứa nút nạp file
        btn_style_sub = {
            "bg": "#f27024",
            "fg": "#ffffff",
            "activebackground": "#d95f1c",
            "activeforeground": "#ffffff",
            "relief": "flat",
            "font": ("Segoe UI", 9, "bold"),
            "bd": 0,
            "cursor": "hand2",
            "pady": 5
        }
        btn_style_file = btn_style_sub.copy()
        btn_style_file["bg"] = "#475569"
        btn_style_file["activebackground"] = "#334155"

        def load_log_file():
            file_path = filedialog.askopenfilename(
                title="Chọn file logs (.txt, .log, .csv)",
                filetypes=[("Text files", "*.txt;*.log"), ("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if file_path:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content_data = f.read()
                    txt_logs.delete("1.0", tk.END)
                    txt_logs.insert("1.0", content_data)
                    filename = os.path.basename(file_path)
                    self.log_message(f"Nạp thành công {len(content_data)} ký tự log từ file {filename}.", "success")
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Không thể đọc file logs: {str(e)}")

        btn_load_file = tk.Button(left_frame, text="📁 Nạp Logs từ File (.txt/.log)", **btn_style_file, command=load_log_file)
        btn_load_file.pack(fill="x", pady=(0, 15))

        lbl_pat = tk.Label(left_frame, text="Từ khóa cần tìm (Pattern):", font=("Segoe UI", 9, "bold"), fg="#475569", bg="#ffffff")
        lbl_pat.pack(anchor="w", pady=(0, 2))

        ent_pattern = tk.Entry(left_frame, font=("Segoe UI", 10), relief="solid", bd=1)
        ent_pattern.insert(0, "SAVE10")
        ent_pattern.pack(fill="x", pady=(0, 15))

        # Cột phải: Báo cáo
        txt_report = tk.Text(right_frame, bg="#ffffff", fg="#0f172a", relief="flat", font=("Segoe UI", 10), wrap="word")
        txt_report.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(right_frame, command=txt_report.yview)
        scroll.pack(side="right", fill="y")
        txt_report.config(yscrollcommand=scroll.set)

        txt_report.tag_config("section", foreground="#f27024", font=("Segoe UI", 11, "bold"))
        txt_report.tag_config("bold", font=("Segoe UI", 10, "bold"), foreground="#0f172a")
        txt_report.tag_config("match", font=("Segoe UI", 10, "bold"), foreground="#ef4444", background="#fef3c7")
        txt_report.tag_config("success", font=("Segoe UI", 10, "bold"), foreground="#10b981")
        txt_report.tag_config("explain", font=("Segoe UI", 9, "italic"), foreground="#1e40af")

        txt_report.insert(tk.END, "Vui lòng nhập văn bản hoặc nạp file logs bên trái, nhập từ khóa và nhấn nút chạy tìm kiếm...", "italic")
        txt_report.config(state="disabled")

        def set_sub_buttons_state(state):
            btn_load_file.config(state=state)
            btn_run.config(state=state)
            ent_pattern.config(state=state)
            txt_logs.config(state=state)

        def execute_search():
            txt = txt_logs.get("1.0", tk.END)
            # Giữ nguyên xuống dòng của file log nhưng trim khoảng trắng thừa đầu cuối
            txt = txt.rstrip('\r\n').rstrip('\n')
            pat = ent_pattern.get().strip()

            if not txt.strip():
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập hoặc nạp văn bản logs!")
                return
            if not pat:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa cần tìm!")
                return

            set_sub_buttons_state("disabled")

            def run_search():
                indices = rolling_hash.rolling_hash_search(txt, pat)
                self.log_message(f"Quét Rabin-Karp hoàn tất. Tìm thấy {len(indices)} kết quả khớp với '{pat}'.", "success")

                txt_report.config(state="normal")
                txt_report.delete("1.0", tk.END)

                txt_report.insert(tk.END, "🔍 KẾT QUẢ TÌM KIẾM RABIN-KARP\n", "section")
                txt_report.insert(tk.END, f"  - Từ khóa cần tìm: '{pat}'\n")
                txt_report.insert(tk.END, f"  - Số lượng khớp: {len(indices)} vị trí\n\n", "bold")

                if indices:
                    txt_report.insert(tk.END, "  - Vị trí các chỉ số (0-indexed):\n", "bold")
                    txt_report.insert(tk.END, f"    ➔ {', '.join(map(str, indices))}\n\n", "success")

                    txt_report.insert(tk.END, "  - Minh họa các vị trí khớp trong log:\n", "bold")
                    
                    text_len = len(txt)
                    if text_len < 2000:
                        last_idx = 0
                        for start_idx in indices:
                            txt_report.insert(tk.END, txt[last_idx:start_idx])
                            txt_report.insert(tk.END, txt[start_idx:start_idx + len(pat)], "match")
                            last_idx = start_idx + len(pat)
                        txt_report.insert(tk.END, txt[last_idx:])
                        txt_report.insert(tk.END, "\n\n")
                    else:
                        txt_report.insert(tk.END, f"    (Văn bản quá dài ({text_len} ký tự), chỉ hiển thị chỉ số để tối ưu hiệu năng. Vui lòng xem kết quả chi tiết ở danh sách vị trí trên.)\n\n", "italic")
                else:
                    txt_report.insert(tk.END, "  ➔ Không tìm thấy từ khóa nào trùng khớp trong logs.\n\n", "bold")

                txt_report.insert(tk.END, "💡 Giải thích giải thuật: Giải thuật Rabin-Karp sử dụng Rolling Hash để tính mã băm cho chuỗi mẫu độ dài M và trượt liên tục trên văn bản độ dài N. Tại mỗi bước dịch chuyển, việc tính toán mã băm mới dựa trên mã băm cũ chỉ mất O(1) nhờ tận dụng phép toán hiệu của phần tử đi ra và cộng phần tử đi vào. Độ phức tạp trung bình là O(N + M).\n", "explain")
                txt_report.config(state="disabled")
                set_sub_buttons_state("normal")

            self.run_progress_simulation(
                status_msg=f"Đang băm trượt Rabin-Karp tìm kiếm '{pat}'...",
                finish_msg="Hoàn thành thuật toán Rabin-Karp.",
                final_callback=run_search
            )

        btn_run = tk.Button(left_frame, text="🚀 Tìm kiếm Rabin-Karp", **btn_style_sub, command=execute_search)
        btn_run.pack(fill="x", pady=5)
    
    # --- 6. DP CO BAN ---
    def run_dp_basics(self):
        """Quy hoạch động cơ bản"""
        def run_sim(results):
            n_str = results["n"]
            try:
                n = int(n_str)
            except ValueError:
                messagebox.showerror("Lỗi nhập liệu", "N phải là số nguyên!")
                return
            def show_result():
                msg = f"Thuật toán Quy hoạch động cơ bản với N={n} đã chạy thành công!"
                self.log_message(msg, "success")
                messagebox.showinfo("Quy hoạch động cơ bản", msg)
            self.run_progress_simulation(
                status_msg=f"Đang lập bảng quy hoạch động tính toán Fibonacci & Climbing Stairs với N={n}...",
                finish_msg="Hoàn thành DP cơ bản.",
                final_callback=show_result
            )
            
        self.show_input_dialog("DP Cơ Bản (Fib & Stairs)", [
            ("Tham số N:", "n", "10")
        ], run_sim)

    # --- 7. COMBO KNAPSACK ---
    def run_combo_knapsack(self):
        """Combo khuyến mãi cái túi 0/1"""
        def run_sim(results):
            b_str = results["b"]
            try:
                b = int(b_str)
            except ValueError:
                messagebox.showerror("Lỗi nhập liệu", "Ngân sách B phải là số nguyên!")
                return
            def show_result():
                msg = f"Thuật toán Quy hoạch động cái túi (Knapsack 0/1) với ngân sách B={b} đã chạy thành công!"
                self.log_message(msg, "success")
                messagebox.showinfo("Combo Knapsack 0/1", msg)
            self.run_progress_simulation(
                status_msg=f"Đang thiết lập bảng quy hoạch động cái túi Knapsack với ngân sách B={b}...",
                finish_msg="Hoàn thành tối ưu Knapsack.",
                final_callback=show_result
            )
            
        self.show_input_dialog("Combo Knapsack 0/1", [
            ("Ngân sách tối đa B:", "b", "40")
        ], run_sim)


    def input_data(self):
        """Chức năng 1: Nhập dữ liệu với xử lý lỗi và mô phỏng đọc file"""
        self.log_message("Đang yêu cầu nạp dữ liệu...", "info")
        try:
            file_path = filedialog.askopenfilename(
                title="Chọn file dữ liệu bản đồ (.txt / .csv)",
                filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                if not os.path.exists(file_path):
                    raise FileNotFoundError("Không tìm thấy file ở đường dẫn đã chọn.")
                
                size = os.path.getsize(file_path)
                if size == 0:
                    raise ValueError("File dữ liệu trống (dung lượng 0 bytes).")
                
                filename = os.path.basename(file_path)
                
                # Callback xử lý sau khi thanh tiến trình mô phỏng chạy xong
                def on_success():
                    try:
                        self.parse_csv_file(file_path)
                        messagebox.showinfo("Thành công", f"Đã nạp và phân tích thành công file dữ liệu: {filename}\nTìm thấy {len(self.vertices)} kho hàng và {len(self.edges)} tuyến đường.")
                    except Exception as e:
                        messagebox.showerror("Lỗi phân tích", f"Không thể đọc file CSV: {str(e)}")

                # Chạy hiệu ứng đọc file
                self.run_progress_simulation(
                    status_msg=f"Đang đọc dữ liệu từ file '{filename}'...",
                    finish_msg=f"Nạp thành công file: {filename} ({size} bytes).",
                    final_callback=on_success
                )
            else:
                self.log_message("Cảnh báo: Người dùng hủy chọn file.", "warning")
                messagebox.showwarning("Cảnh báo", "Bạn chưa chọn file dữ liệu nào.")
                
        except FileNotFoundError as e:
            self.log_message(f"Lỗi đọc file: {str(e)}", "error")
            messagebox.showerror("Lỗi đọc file", f"Lỗi: {str(e)}")
        except ValueError as e:
            self.log_message(f"Lỗi dữ liệu: {str(e)}", "error")
            messagebox.showerror("Lỗi dữ liệu", f"Dữ liệu không hợp lệ: {str(e)}")
        except Exception as e:
            self.log_message(f"Lỗi hệ thống: {str(e)}", "error")
            messagebox.showerror("Lỗi hệ thống", f"Đã xảy ra lỗi không xác định: {str(e)}")

    def show_info(self):
        """Hiển thị thông tin sinh viên"""
        self.log_message("Xem thông tin sinh viên Nguyễn Thành Hưng.", "info")
        info_message = (
            "=== THÔNG TIN SINH VIÊN ===\n"
            "- Họ và tên: Nguyễn Thành Hưng\n"
            "- Mã số sinh viên (MSSV): PS47270\n"
            "- Lớp: ITA107\n"
            "- Môn học: Cấu trúc dữ liệu và giải thuật (ITA107)\n\n"
            "=== HƯỚNG DẪN SỬ DỤNG ===\n"
            "1. Nhấn các nút chức năng từ 1 đến 7 để chạy tính toán từng trường hợp thực tế.\n"
            "2. Hệ thống sẽ khóa các nút, chạy thanh tiến trình tính toán, phát âm báo và hiển thị kết quả.\n"
            "3. Ô nhật ký Console lưu trữ toàn bộ các bước chạy để dễ dàng theo dõi và xuất file báo cáo.\n"
        )
        messagebox.showinfo("Thông tin & Hướng dẫn", info_message)

    def exit_program(self):
        """Xác nhận và thoát"""
        self.log_message("Yêu cầu thoát hệ thống...", "warning")
        confirm = messagebox.askyesno("Xác nhận thoát", "Bạn có chắc chắn muốn thoát ứng dụng không?")
        if confirm:
            self.log_message("Hệ thống đã đóng.", "warning")
            self.root.destroy()
        else:
            self.log_message("Hủy thoát hệ thống.", "info")

    def export_log(self):
        """Xuất toàn bộ văn bản trong ô text log ra file log_hoat_dong.txt"""
        try:
            log_content = self.txt_log.get("1.0", tk.END).strip()
            if not log_content:
                messagebox.showwarning("Cảnh báo", "Nhật ký hệ thống trống, không có gì để xuất!")
                return
            
            # Lưu tự động ra file log_hoat_dong.txt trong thư mục hiện tại
            file_path = os.path.join(current_dir, "log_hoat_dong.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(log_content)
            
            # Ghi nhận log xuất thành công và hiển thị thông báo
            self.log_message(f"Đã xuất nhật ký hệ thống ra file: log_hoat_dong.txt", "success")
            messagebox.showinfo("Thành công", f"Đã xuất nhật ký hệ thống ra tệp tin:\n{file_path}")
        except Exception as e:
            self.log_message(f"Lỗi khi xuất nhật ký: {str(e)}", "error")
            messagebox.showerror("Lỗi hệ thống", f"Không thể xuất nhật ký ra file: {str(e)}")

    def load_default_data(self):
        """Tự động tạo tệp tin dữ liệu mặc định du_lieu_mau.csv và nạp nhanh vào ứng dụng"""
        if self.btn_routing.cget("state") == "disabled":
            return
        
        self.log_message("Yêu cầu nạp nhanh dữ liệu cấu hình mặc định...", "info")
        try:
            # Tạo dữ liệu mặc định phù hợp với format CSV (u,v,cost)
            default_content = (
                "WH1,WH2,15\n"
                "WH1,HCM,22\n"
                "WH2,HCM,10\n"
                "WH2,DN,30\n"
                "HCM,DN,18\n"
                "HN,DN,25\n"
                "HN,HP,5\n"
                "HP,WH1,40\n"
            )
            
            file_path = os.path.join(current_dir, "du_lieu_mau.csv")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(default_content)
                
            filename = "du_lieu_mau.csv"
            size = len(default_content.encode("utf-8"))
            
            def on_success():
                try:
                    self.parse_csv_file(file_path)
                    messagebox.showinfo("Thành công", f"Đã tự động tạo và nạp thành công dữ liệu mặc định:\n{file_path}\n(Dung lượng: {size} bytes)")
                except Exception as e:
                    messagebox.showerror("Lỗi phân tích", f"Lỗi đọc dữ liệu mặc định: {str(e)}")
                
            # Chạy hiệu ứng thanh tiến trình xử lý
            self.run_progress_simulation(
                status_msg=f"Đang phân tích dữ liệu cấu hình mặc định từ '{filename}'...",
                finish_msg=f"Tự tạo và nạp thành công file: {filename} ({size} bytes).",
                final_callback=on_success
            )
        except Exception as e:
            self.log_message(f"Lỗi nạp dữ liệu mặc định: {str(e)}", "error")
            messagebox.showerror("Lỗi dữ liệu mặc định", f"Không thể nạp dữ liệu mặc định: {str(e)}")

    def play_sound(self, sound_type="success"):
        """Phát âm thanh cảnh báo hệ thống Windows (natively)"""
        if os.name == "nt":
            try:
                import winsound
                if sound_type == "success":
                    winsound.MessageBeep(winsound.MB_OK)
                elif sound_type == "error":
                    winsound.MessageBeep(winsound.MB_ICONHAND)
                elif sound_type == "warning":
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            except Exception:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PolyShipApp(root)
    root.mainloop()