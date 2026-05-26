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
        self.root.geometry("500x620")
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
                w_target = 180
                h_target = int(w_target * img.height / img.width)
                img = img.resize((w_target, h_target), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
            except Exception:
                try:
                    # 2. Dự phòng: Dùng PhotoImage nguyên bản của Tkinter (nếu không có Pillow)
                    self.logo_img = tk.PhotoImage(file=logo_path).subsample(4)
                except Exception:
                    self.logo_img = None

        # --- 1. HEADER BANNER ---
        header_frame = tk.Frame(root, bg="#ffffff", height=85)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        # Thanh kẻ màu cam FPT dưới header để làm điểm nhấn
        orange_line = tk.Frame(root, bg="#f27024", height=4)
        orange_line.pack(fill="x")

        if self.logo_img:
            lbl_logo_img = tk.Label(header_frame, image=self.logo_img, bg="#ffffff")
            lbl_logo_img.pack(side="left", padx=20, pady=10)
            
            # Khung thông tin tiêu đề và trạng thái bên phải
            right_header = tk.Frame(header_frame, bg="#ffffff")
            right_header.pack(side="right", padx=20, pady=10)
            
            lbl_title = tk.Label(right_header, text="HỆ THỐNG HẬU CẦN\nPOLY-SHIP", fg="#f27024", bg="#ffffff", 
                                 font=("Segoe UI", 12, "bold"), justify="left")
            lbl_title.pack(anchor="e")
            
            lbl_status = tk.Label(right_header, text="● Máy chủ: Online | DB: Connected", fg="#10b981", bg="#ffffff", 
                                  font=("Segoe UI", 9, "bold"))
            lbl_status.pack(anchor="e", pady=(2, 0))
        else:
            # Fallback nếu không có file logo
            lbl_logo = tk.Label(header_frame, text="FPT POLYTECHNIC", fg="#f27024", bg="#ffffff", 
                                font=("Segoe UI", 12, "italic bold"))
            lbl_logo.pack(anchor="w", padx=25, pady=(12, 0))
            
            lbl_title = tk.Label(header_frame, text="HỆ THỐNG HẬU CẦN POLY-SHIP", fg="#0f172a", bg="#ffffff", 
                                 font=("Segoe UI", 14, "bold"))
            lbl_title.pack(anchor="w", padx=25, pady=(2, 2))

            lbl_status = tk.Label(header_frame, text="● Máy chủ: Online | Database: Connected", fg="#10b981", bg="#ffffff", 
                                  font=("Segoe UI", 9, "bold"))
            lbl_status.pack(anchor="w", padx=25, pady=(0, 10))

        # --- 2. CARD CONTAINER CHỨA NÚT BẤM ---
        main_content = tk.Frame(root, bg="#f8fafc", padx=20, pady=12)
        main_content.pack(fill="x")

        card_frame = tk.Frame(main_content, bg="#ffffff", highlightthickness=1, 
                              highlightbackground="#e2e8f0", padx=20, pady=12)
        card_frame.pack(fill="x")

        # Style cấu hình chung cho các nút bấm phẳng hiện đại
        self.btn_style = {
            "bg": "#f27024",
            "fg": "#ffffff",
            "activebackground": "#d95f1c",
            "activeforeground": "#ffffff",
            "relief": "flat",
            "font": ("Segoe UI", 11, "bold"),
            "width": 32,
            "height": 2,
            "cursor": "hand2",
            "bd": 0
        }

        # Nút 1: Nhập dữ liệu
        self.btn_input = tk.Button(card_frame, text="1. Nhập dữ liệu", **self.btn_style, command=self.input_data)
        self.btn_input.pack(pady=(4, 0))

        # Phụ: Nạp nhanh dữ liệu mẫu dạng link
        self.lbl_demo_link = tk.Label(card_frame, text="⚡ Nạp nhanh dữ liệu mẫu", fg="#f27024", bg="#ffffff",
                                      font=("Segoe UI", 9, "underline bold"), cursor="hand2")
        self.lbl_demo_link.pack(pady=(2, 4))
        self.lbl_demo_link.bind("<Button-1>", lambda e: self.load_demo_data())
        self.lbl_demo_link.bind("<Enter>", lambda e: self.lbl_demo_link.config(fg="#d95f1c") if self.btn_input.cget("state") == "normal" else None)
        self.lbl_demo_link.bind("<Leave>", lambda e: self.lbl_demo_link.config(fg="#f27024") if self.btn_input.cget("state") == "normal" else None)

        # Nút 2: Xử lý
        self.btn_process = tk.Button(card_frame, text="2. Xử lý (Routing & Hashing)", **self.btn_style, command=self.process_data)
        self.btn_process.pack(pady=4)

        # Nút 3: Tối ưu
        self.btn_optimize = tk.Button(card_frame, text="3. Tối ưu (MST & Knapsack)", **self.btn_style, command=self.optimize_data)
        self.btn_optimize.pack(pady=4)

        # Nút 4: Thông tin sinh viên
        self.btn_info = tk.Button(card_frame, text="4. Thông tin & Hướng dẫn", **self.btn_style, command=self.show_info)
        self.btn_info.pack(pady=4)

        # Nút 5: Thoát
        exit_style = self.btn_style.copy()
        exit_style["bg"] = "#0f172a"
        exit_style["activebackground"] = "#1e293b"
        self.btn_exit = tk.Button(card_frame, text="5. Thoát chương trình", **exit_style, command=self.exit_program)
        self.btn_exit.pack(pady=4)

        # Thiết lập hiệu ứng Hover
        self.setup_hover(self.btn_input, "#f27024", "#d95f1c")
        self.setup_hover(self.btn_process, "#f27024", "#d95f1c")
        self.setup_hover(self.btn_optimize, "#f27024", "#d95f1c")
        self.setup_hover(self.btn_info, "#f27024", "#d95f1c")
        self.setup_hover(self.btn_exit, "#0f172a", "#1e293b")

        # --- 3. KHUNG THANH TIẾN TRÌNH MÔ PHỎNG ---
        self.progress_frame = tk.Frame(main_content, bg="#f8fafc")
        self.progress_frame.pack(fill="x", pady=(8, 0))

        style = ttk.Style()
        style.configure("Orange.Horizontal.TProgressbar", troughcolor='#e2e8f0', background='#f27024', thickness=12)

        self.progress_bar = ttk.Progressbar(self.progress_frame, orient="horizontal", mode="determinate", 
                                             style="Orange.Horizontal.TProgressbar", length=300)
        self.progress_bar.pack(fill="x", padx=5)

        self.lbl_progress_status = tk.Label(self.progress_frame, text="Hệ thống sẵn sàng", 
                                             font=("Segoe UI", 10, "bold"), fg="#64748b", bg="#f8fafc")
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
        self.setup_hover(self.btn_export, "#475569", "#334155")

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
        footer = tk.Label(root, text="Thiết kế sườn bài bởi Sinh viên FPT Polytechnic", 
                          font=("Segoe UI", 8), fg="#94a3b8", bg="#f8fafc")
        footer.pack(side="bottom", pady=6)

        # Ghi log khởi động hệ thống
        self.log_message("Khởi chạy hệ thống POLY-SHIP thành công.", "info")

    def setup_hover(self, button, normal_color, hover_color):
        button.bind("<Enter>", lambda e: button.config(bg=hover_color) if button.cget("state") == "normal" else None)
        button.bind("<Leave>", lambda e: button.config(bg=normal_color) if button.cget("state") == "normal" else None)

    def log_message(self, message, level="info"):
        """Ghi tin nhắn nhật ký kèm theo dấu thời gian thực tế và màu sắc phân cấp"""
        now = datetime.now().strftime("%H:%M:%S")
        self.txt_log.config(state="normal")
        self.txt_log.insert(tk.END, f"[{now}] {message}\n", level)
        self.txt_log.see(tk.END)
        self.txt_log.config(state="disabled")

    def set_buttons_state(self, state):
        """Khóa hoặc mở khóa các nút bấm chính"""
        self.btn_input.config(state=state)
        self.btn_process.config(state=state)
        self.btn_optimize.config(state=state)
        self.btn_info.config(state=state)
        self.btn_exit.config(state=state)
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

    def process_data(self):
        """Chức năng 2: Xử lý dữ liệu"""
        def show_result():
            messagebox.showinfo("Xử lý dữ liệu", "Hệ thống đang tiến hành xử lý dữ liệu:\n- Phân tích đường đi ngắn nhất (Dijkstra)\n- Tra cứu băm đơn hàng (Hashing)")

        self.run_progress_simulation(
            status_msg="Đang tính toán phân tích Dijkstra & Hashing đơn hàng...",
            finish_msg="Hoàn thành sườn xử lý dữ liệu.",
            final_callback=show_result
        )

    def optimize_data(self):
        """Chức năng 3: Tối ưu hóa"""
        def show_result():
            messagebox.showinfo("Tối ưu hóa", "Hệ thống đang chạy thuật toán tối ưu:\n- Tính toán mạng liên kết kho tối thiểu (Kruskal MST)\n- Đề xuất combo khuyến mãi (Quy hoạch động Knapsack)")

        self.run_progress_simulation(
            status_msg="Đang tính toán mạng liên kết kho Kruskal MST & lập bảng Knapsack...",
            finish_msg="Hoàn thành sườn tối ưu hóa.",
            final_callback=show_result
        )

    def show_info(self):
        """Chức năng 4: Hiển thị thông tin sinh viên"""
        self.log_message("Xem thông tin sinh viên Nguyễn Thành Hưng.", "info")
        info_message = (
            "=== THÔNG TIN SINH VIÊN ===\n"
            "- Họ và tên: Nguyễn Thành Hưng\n"
            "- Mã số sinh viên (MSSV): PS47270\n"
            "- Lớp: ITA107\n"
            "- Môn học: Cấu trúc dữ liệu và giải thuật (ITA107)\n\n"
            "=== HƯỚNG DẪN SỬ DỤNG ===\n"
            "1. Nhấn '1. Nhập dữ liệu' để chọn file dữ liệu bản đồ (.txt hoặc .csv).\n"
            "2. Nhấn '2. Xử lý' để giả lập tìm đường đi ngắn nhất Dijkstra và tra cứu đơn hàng bằng băm.\n"
            "3. Nhấn '3. Tối ưu' để giả lập thiết kế liên kết kho Kruskal MST và combo Knapsack.\n"
            "4. Nhấn '5. Thoát chương trình' để đóng ứng dụng một cách an toàn.\n"
        )
        messagebox.showinfo("Thông tin & Hướng dẫn", info_message)

    def exit_program(self):
        """Chức năng 5: Xác nhận và thoát"""
        self.log_message("Yêu cầu thoát hệ thống...", "warning")
        confirm = messagebox.askyesno("Xác nhận thoát", "Bạn có chắc chắn muốn thoát ứng dụng không?")
        if confirm:
            self.log_message("Hệ thống đã đóng.", "warning")
            self.root.destroy()
        else:
            self.log_message("Hủy thoát hệ thống.", "info")

    def export_log(self):
        """Chức năng nâng cao: Xuất toàn bộ văn bản trong ô text log ra file log_hoat_dong.txt"""
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
        """Chức năng nâng cao: Tự động tạo tệp tin dữ liệu mẫu du_lieu_mau.txt và nạp nhanh vào ứng dụng"""
        if self.btn_input.cget("state") == "disabled":
            return
        
        self.log_message("Yêu cầu nạp nhanh dữ liệu mẫu...", "info")
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
        """Chức năng nâng cao: Phát âm thanh cảnh báo hệ thống Windows (nativeliy)"""
        import os
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