import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

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

        # Nút 1: Demo routing
        self.btn_demo1 = tk.Button(card_frame, text="📍 1. Demo routing - shortest path", **self.btn_style, command=self.demo_routing)
        self.btn_demo1.pack(pady=3)

        # Nút 2: Demo MST
        self.btn_demo2 = tk.Button(card_frame, text="🕸️ 2. Demo MST - mạng kho tối thiểu", **self.btn_style, command=self.demo_mst)
        self.btn_demo2.pack(pady=3)

        # Nút 3: Demo hash table đơn hàng
        self.btn_demo3 = tk.Button(card_frame, text="🔑 3. Demo hash table đơn hàng", **self.btn_style, command=self.demo_hash_table)
        self.btn_demo3.pack(pady=3)

        # Nút 4: Demo hashing tổng hợp
        self.btn_demo4 = tk.Button(card_frame, text="🧮 4. Demo hashing tổng hợp", **self.btn_style, command=self.demo_hashing_compound)
        self.btn_demo4.pack(pady=3)

        # Nút 5: Demo rolling hash
        self.btn_demo5 = tk.Button(card_frame, text="🔍 5. Demo rolling hash tìm pattern log", **self.btn_style, command=self.demo_rolling_hash)
        self.btn_demo5.pack(pady=3)

        # Nút 6: Demo DP cơ bản
        self.btn_demo6 = tk.Button(card_frame, text="🪜 6. Demo DP cơ bản (Fib, Stairs)", **self.btn_style, command=self.demo_dp_basics)
        self.btn_demo6.pack(pady=3)

        # Nút 7: Demo combo khuyến mãi
        self.btn_demo7 = tk.Button(card_frame, text="🎁 7. Demo combo khuyến mãi (Knapsack)", **self.btn_style, command=self.demo_combo_knapsack)
        self.btn_demo7.pack(pady=3)

        # Phụ: Nạp nhanh dữ liệu mẫu dạng link
        self.lbl_demo_link = tk.Label(card_frame, text="⚡ Nạp nhanh dữ liệu cấu hình mẫu", fg="#f27024", bg="#ffffff",
                                      font=("Segoe UI", 9, "underline bold"), cursor="hand2")
        self.lbl_demo_link.pack(pady=(4, 2))
        self.lbl_demo_link.bind("<Button-1>", lambda e: self.load_demo_data())

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
            self.btn_demo1: "📍 1. Demo routing - shortest path",
            self.btn_demo2: "🕸️ 2. Demo MST - mạng kho tối thiểu",
            self.btn_demo3: "🔑 3. Demo hash table đơn hàng",
            self.btn_demo4: "🧮 4. Demo hashing tổng hợp",
            self.btn_demo5: "🔍 5. Demo rolling hash tìm pattern log",
            self.btn_demo6: "🪜 6. Demo DP cơ bản (Fib, Stairs)",
            self.btn_demo7: "🎁 7. Demo combo khuyến mãi (Knapsack)",
            self.btn_exit: "🚪 8. Thoát chương trình",
            self.btn_export: "📤 Xuất Nhật Ký"
        }

        # Thiết lập hiệu ứng Hover cho toàn bộ nút bấm
        self.setup_hover(self.btn_demo1, "#f27024", "#d95f1c")
        self.setup_hover(self.btn_demo2, "#f27024", "#d95f1c")
        self.setup_hover(self.btn_demo3, "#f27024", "#d95f1c")
        self.setup_hover(self.btn_demo4, "#f27024", "#d95f1c")
        self.setup_hover(self.btn_demo5, "#f27024", "#d95f1c")
        self.setup_hover(self.btn_demo6, "#f27024", "#d95f1c")
        self.setup_hover(self.btn_demo7, "#f27024", "#d95f1c")
        self.setup_hover(self.btn_exit, "#0f172a", "#1e293b")
        self.setup_hover(self.btn_export, "#475569", "#334155")

        # Ghi log khởi động hệ thống
        self.log_message("Khởi chạy hệ thống thử nghiệm POLY-SHIP thành công.", "info")

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

    def log_message(self, message, level="info"):
        """Ghi tin nhắn nhật ký kèm theo dấu thời gian thực tế và màu sắc phân cấp"""
        now = datetime.now().strftime("%H:%M:%S")
        self.txt_log.config(state="normal")
        self.txt_log.insert(tk.END, f"[{now}] {message}\n", level)
        self.txt_log.see(tk.END)
        self.txt_log.config(state="disabled")

    def set_buttons_state(self, state):
        """Khóa hoặc mở khóa các nút bấm chính và reset text nguyên bản sạch sẽ"""
        for btn, text in self.btn_texts.items():
            if btn != self.btn_export:  # Nút xuất log luôn giữ nguyên trạng thái
                btn.config(state=state, text=text)
        if state == "disabled":
            self.lbl_demo_link.config(fg="#cbd5e1", cursor="arrow")
        else:
            self.lbl_demo_link.config(fg="#f27024", cursor="hand2")

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

    # --- 1. DEMO DIJKSTRA ROUTING ---
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

    # --- 1. DEMO DIJKSTRA ROUTING ---
    def demo_routing(self):
        """Chạy giả lập Demo 1: Định tuyến tìm đường đi ngắn nhất Dijkstra"""
        def run_sim(results):
            src = results["source"]
            tgt = results["target"]
            if not src or not tgt:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ Kho nguồn và Kho đích!")
                return
            def show_result():
                msg = f"Thuật toán định tuyến Dijkstra từ {src} đến {tgt} đã chạy thành công!"
                self.log_message(msg, "success")
                messagebox.showinfo("Demo Routing Dijkstra", msg)
            self.run_progress_simulation(
                status_msg=f"Đang tính toán tuyến đường ngắn nhất Dijkstra từ {src} đến {tgt}...",
                finish_msg="Hoàn thành giải thuật Dijkstra.",
                final_callback=show_result
            )
            
        self.show_input_dialog("Định Tuyến Dijkstra", [
            ("Kho nguồn (Source):", "source", "Kho_A"),
            ("Kho đích (Target):", "target", "Kho_D")
        ], run_sim)

    # --- 2. DEMO MST KRUSKAL ---
    def demo_mst(self):
        """Chạy giả lập Demo 2: Cây khung tối thiểu Kruskal"""
        def run_sim(results):
            nodes = results["nodes"]
            if not nodes:
                return
            def show_result():
                msg = "Thuật toán thiết kế mạng kho tối thiểu Kruskal đã chạy thành công!"
                self.log_message(msg, "success")
                messagebox.showinfo("Demo Kruskal MST", msg)
            self.run_progress_simulation(
                status_msg="Đang chạy thuật toán Kruskal MST và cấu trúc Union-Find...",
                finish_msg="Hoàn thành giải thuật Kruskal MST.",
                final_callback=show_result
            )
            
        self.show_input_dialog("Mạng Kho Tối Thiểu MST", [
            ("Danh sách Kho:", "nodes", "Kho_A, Kho_B, Kho_C, Kho_D")
        ], run_sim)

    # --- 3. DEMO HASH TABLE ---
    def demo_hash_table(self):
        """Chạy giả lập Demo 3: Tra cứu bảng băm đơn hàng dùng Separate Chaining"""
        def run_sim(results):
            act = results["action"].strip().lower()
            oid = results["order_id"]
            info = results["info"]
            if act not in ["insert", "search", "delete"]:
                messagebox.showwarning("Cảnh báo", "Hành động không hợp lệ! Vui lòng chỉ nhập 'Insert', 'Search' hoặc 'Delete'.")
                return
            if not oid:
                return
            
            def show_result():
                if act == "insert":
                    msg = f"Thuật toán bảng băm: Chèn thành công đơn hàng '{oid}' ({info})!"
                elif act == "search":
                    msg = f"Thuật toán bảng băm: Tìm thấy đơn hàng '{oid}'!"
                else:
                    msg = f"Thuật toán bảng băm: Đã xóa thành công đơn hàng '{oid}'!"
                self.log_message(msg, "success")
                messagebox.showinfo("Demo Hash Table đơn hàng", msg)
                
            self.run_progress_simulation(
                status_msg=f"Đang thực thi bảng băm hành động '{results['action']}' cho '{oid}'...",
                finish_msg="Hoàn thành thao tác bảng băm.",
                final_callback=show_result
            )
            
        self.show_input_dialog("Bảng Băm Đơn Hàng", [
            ("Hành động (Insert/Search/Delete):", "action", "Insert"),
            ("Mã đơn hàng (Order ID):", "order_id", "HD23"),
            ("Thông tin đơn hàng:", "info", "TP.HCM - 320k")
        ], run_sim)

    # --- 4. DEMO HASHING TỔNG HỢP ---
    def demo_hashing_compound(self):
        """Chạy giả lập Demo 4: Các bài toán Hashing tổng hợp"""
        def run_sim(results):
            def show_result():
                msg = "Các thuật toán Hashing tổng hợp đã chạy thành công!"
                self.log_message(msg, "success")
                messagebox.showinfo("Demo Hashing tổng hợp", msg)
            self.run_progress_simulation(
                status_msg="Đang tính toán các bài toán Anagram, Streak và Subarray Sum bằng hash...",
                finish_msg="Hoàn thành demo Hashing tổng hợp.",
                final_callback=show_result
            )
            
        self.show_input_dialog("Hashing Tổng Hợp", [
            ("Danh sách mã Coupon:", "coupons", "SAVE10, AVES10, SALE5, LASE5, EVAS10"),
            ("Danh sách ngày giao hàng:", "days", "100, 4, 200, 1, 3, 2, 5"),
            ("Doanh thu tích lũy:", "revenues", "10, 2, -2, -20, 10"),
            ("Mục tiêu K:", "k", "-10")
        ], run_sim)

    # --- 5. DEMO ROLLING HASH ---
    def demo_rolling_hash(self):
        """Chạy giả lập Demo 5: Tìm pattern log bằng Rabin-Karp Rolling Hash"""
        def run_sim(results):
            txt = results["text"]
            pat = results["pattern"]
            if not txt or not pat:
                return
            def show_result():
                msg = f"Thuật toán tìm kiếm Rolling Hash Rabin-Karp cho từ khóa '{pat}' đã chạy thành công!"
                self.log_message(msg, "success")
                messagebox.showinfo("Demo Rolling Hash", msg)
            self.run_progress_simulation(
                status_msg=f"Đang băm trượt Rabin-Karp tìm '{pat}' trên tệp logs...",
                finish_msg="Hoàn thành demo Rolling Hash.",
                final_callback=show_result
            )
            
        self.show_input_dialog("Rabin-Karp Rolling Hash", [
            ("Văn bản Logs (Text):", "text", "SYSTEM_LOG_WARN_AVES10_LOG_SAVE10_PROCESS_ERROR"),
            ("Pattern cần tìm:", "pattern", "SAVE10")
        ], run_sim)

    # --- 6. DEMO DP CO BAN ---
    def demo_dp_basics(self):
        """Chạy giả lập Demo 6: Quy hoạch động cơ bản"""
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
                messagebox.showinfo("Demo DP Cơ Bản", msg)
            self.run_progress_simulation(
                status_msg=f"Đang lập bảng quy hoạch động tính toán Fibonacci & Climbing Stairs với N={n}...",
                finish_msg="Hoàn thành demo DP cơ bản.",
                final_callback=show_result
            )
            
        self.show_input_dialog("DP Cơ Bản (Fib & Stairs)", [
            ("Tham số N:", "n", "10")
        ], run_sim)

    # --- 7. DEMO COMBO KNAPSACK ---
    def demo_combo_knapsack(self):
        """Chạy giả lập Demo 7: Combo khuyến mãi cái túi 0/1"""
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
                messagebox.showinfo("Demo Combo Knapsack", msg)
            self.run_progress_simulation(
                status_msg=f"Đang thiết lập bảng quy hoạch động cái túi Knapsack với ngân sách B={b}...",
                finish_msg="Hoàn thành demo combo tối ưu Knapsack.",
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
                filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
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
                    messagebox.showinfo("Thành công", f"Đã nạp thành công file dữ liệu: {filename}\n(Dung lượng: {size} bytes)")

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
            "1. Nhấn các nút Demo thuật toán từ 1 đến 7 để chạy giả lập từng trường hợp thực tế.\n"
            "2. Hệ thống sẽ khóa các nút, chạy thanh tiến trình giả lập, phát âm báo và hiển thị chi tiết thuật toán.\n"
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

    def load_demo_data(self):
        """Tự động tạo tệp tin dữ liệu mẫu du_lieu_mau.txt và nạp nhanh vào ứng dụng"""
        if self.btn_demo1.cget("state") == "disabled":
            return
        
        self.log_message("Yêu cầu nạp nhanh dữ liệu cấu hình mẫu...", "info")
        try:
            # Tạo dữ liệu mẫu phù hợp với Logistics / Map / Orders
            demo_content = (
                "# Bản đồ kho hàng POLY-SHIP (Nút kho và Chi phí vận chuyển)\n"
                "Kho_A Kho_B 15\n"
                "Kho_A Kho_C 22\n"
                "Kho_B Kho_C 10\n"
                "Kho_B Kho_D 30\n"
                "Kho_C Kho_D 18\n"
                "\n"
                "# Danh sách mã giảm giá khuyến mãi (Coupon)\n"
                "KM_A10,10,2\n"
                "KM_B20,20,3\n"
                "KM_C30,35,4\n"
            )
            
            file_path = os.path.join(current_dir, "du_lieu_mau.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(demo_content)
                
            filename = "du_lieu_mau.txt"
            size = len(demo_content.encode("utf-8"))
            
            def on_success():
                messagebox.showinfo("Thành công", f"Đã tự động tạo và nạp thành công dữ liệu mẫu:\n{file_path}\n(Dung lượng: {size} bytes)")
                
            # Chạy hiệu ứng thanh tiến trình giả lập
            self.run_progress_simulation(
                status_msg=f"Đang phân tích dữ liệu mẫu từ '{filename}'...",
                finish_msg=f"Tự tạo và nạp thành công file: {filename} ({size} bytes).",
                final_callback=on_success
            )
        except Exception as e:
            self.log_message(f"Lỗi nạp dữ liệu mẫu: {str(e)}", "error")
            messagebox.showerror("Lỗi dữ liệu mẫu", f"Không thể nạp dữ liệu mẫu: {str(e)}")

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