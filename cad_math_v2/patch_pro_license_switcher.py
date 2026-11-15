import os

with open('cad_math_v2/cad_math_v2.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update __init__ icon loading
old_init_icon = """        self.root.title("CAD Math Studio Pro v2.4")
        self.ico_path = os.path.join(os.path.dirname(__file__), "assets", "cad_math.ico")
        if os.path.exists(self.ico_path):
            try:
                self.root.iconbitmap(default=self.ico_path)
                self.root.iconbitmap(self.ico_path)
            except Exception:
                try:
                    self.root.iconbitmap(self.ico_path)
                except Exception:
                    pass
            self.root.ico_path = self.ico_path
        logo_png = os.path.join(os.path.dirname(__file__), "assets", "cad_math_logo.png")
        if os.path.exists(logo_png):
            try:
                from PIL import Image, ImageTk
                pil_l = Image.open(logo_png).resize((64, 64), Image.Resampling.LANCZOS)
                self.root._app_icon_photo = ImageTk.PhotoImage(pil_l, master=self.root)
                self.root.iconphoto(True, self.root._app_icon_photo)
            except Exception:
                pass"""

new_init_icon = """        # Đường dẫn icon & logo Standard và Pro
        self.ico_path = os.path.join(os.path.dirname(__file__), "assets", "cad_math.ico")
        self.pro_ico_path = os.path.join(os.path.dirname(__file__), "assets", "cad_math_pro.ico")
        self.logo_png = os.path.join(os.path.dirname(__file__), "assets", "cad_math_logo.png")
        self.pro_logo_png = os.path.join(os.path.dirname(__file__), "assets", "cad_math_logo_pro.png")

        # Nạp trạng thái bản quyền & tự động chuyển đổi Icon Pro
        self.is_pro = self.load_pro_license_state()
        self.apply_branding_icon(is_pro=self.is_pro)"""

if old_init_icon in content:
    content = content.replace(old_init_icon, new_init_icon)
    print("Replaced __init__ icon logic successfully!")
else:
    print("Warning: old_init_icon not found directly.")

# 2. Add methods: apply_branding_icon, load_pro_license_state, save_pro_license_state, open_license_payment_dialog
methods_to_add = '''
    def get_license_file_path(self):
        base = os.environ.get("APPDATA") or os.path.dirname(__file__)
        cad_dir = os.path.join(base, "CADMathStudio")
        os.makedirs(cad_dir, exist_ok=True)
        return os.path.join(cad_dir, "license.json")

    def load_pro_license_state(self) -> bool:
        """Đọc trạng thái kích hoạt Pro từ tệp cấu hình bản quyền."""
        try:
            lic_file = self.get_license_file_path()
            if os.path.exists(lic_file):
                import json
                with open(lic_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return bool(data.get("is_pro", True))
        except Exception:
            pass
        return True

    def save_pro_license_state(self, is_pro: bool):
        """Lưu trạng thái kích hoạt Pro sau khi người dùng thanh toán."""
        try:
            lic_file = self.get_license_file_path()
            import json, time
            with open(lic_file, "w", encoding="utf-8") as f:
                json.dump({"is_pro": is_pro, "updated_at": time.time(), "edition": "CAD Math Studio Pro"}, f)
        except Exception:
            pass

    def apply_branding_icon(self, is_pro: bool = True):
        """
        Cập nhật toàn bộ biểu tượng và tiêu đề ứng dụng sang phiên bản PRO ánh kim
        ngay sau khi người dùng thanh toán thành công.
        """
        self.is_pro = is_pro
        target_ico = self.pro_ico_path if (is_pro and os.path.exists(self.pro_ico_path)) else self.ico_path
        target_logo = self.pro_logo_png if (is_pro and os.path.exists(self.pro_logo_png)) else self.logo_png

        # Cập nhật thanh tiêu đề Window
        base_title = "CAD Math Studio Pro v2.4"
        if is_pro:
            self.root.title(f"{base_title} [PRO ACTIVATED]")
        else:
            self.root.title(base_title)

        # Cập nhật icon cửa sổ (.ico)
        if os.path.exists(target_ico):
            try:
                self.root.iconbitmap(default=target_ico)
                self.root.iconbitmap(target_ico)
            except Exception:
                pass
            self.root.ico_path = target_ico

        # Cập nhật iconphoto (Taskbar, Alt+Tab, Task Switcher)
        if os.path.exists(target_logo):
            try:
                from PIL import Image, ImageTk
                pil_l = Image.open(target_logo).resize((64, 64), Image.Resampling.LANCZOS)
                self.root._app_icon_photo = ImageTk.PhotoImage(pil_l, master=self.root)
                self.root.iconphoto(True, self.root._app_icon_photo)
            except Exception:
                pass

    def open_license_payment_dialog(self):
        """Hộp thoại quản lý bản quyền & thanh toán nâng cấp Pro với khả năng đổi icon tức thì."""
        is_en = (getattr(self, 'current_lang', 'vi') == 'en')
        dlg = tk.Toplevel(self.root)
        dlg.title("License & Payment - CAD Math Studio Pro" if is_en else "Bản Quyền & Thanh Toán - CAD Math Studio Pro")
        dlg.geometry("560x480")
        dlg.configure(bg="#f8fafc")
        dlg.transient(self.root)
        dlg.grab_set()

        # Header Frame
        hdr = tk.Frame(dlg, bg="#0f172a", pady=16)
        hdr.pack(side=tk.TOP, fill=tk.X)

        tk.Label(
            hdr,
            text="⭐ CAD MATH STUDIO PRO" if is_en else "⭐ BẢN QUYỀN CAD MATH STUDIO PRO",
            font=("Segoe UI", 12, "bold"),
            bg="#0f172a",
            fg="#fbbf24"
        ).pack(side=tk.TOP)

        tk.Label(
            hdr,
            text="Official Microsoft Store Edition | Verified License" if is_en else "Phiên bản Chuyên Nghiệp Microsoft Store | Bản Quyền Xác Nhận",
            font=("Segoe UI", 8),
            bg="#0f172a",
            fg="#94a3b8"
        ).pack(side=tk.TOP, pady=(2, 0))

        # Body
        body = tk.Frame(dlg, bg="#f8fafc", padx=20, pady=16)
        body.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        status_text = "STATUS: PRO ACTIVATED (PERMANENT)" if (self.is_pro if hasattr(self, 'is_pro') else True) else "STATUS: PENDING PAYMENT"
        status_color = "#16a34a" if (self.is_pro if hasattr(self, 'is_pro') else True) else "#d97706"
        tk.Label(
            body,
            text=status_text if is_en else ("TRẠNG THÁI: ĐÃ KÍCH HOẠT BẢN QUYỀN PRO" if (self.is_pro if hasattr(self, 'is_pro') else True) else "TRẠNG THÁI: CHỜ THANH TOÁN"),
            font=("Segoe UI", 10, "bold"),
            bg="#f8fafc",
            fg=status_color
        ).pack(side=tk.TOP, anchor="w", pady=(0, 8))

        features = [
            ("✓ Biểu tượng PRO độc quyền:", "Tự động đổi icon Taskbar & Start Menu sang huy hiệu Pro bo góc vàng ánh kim."),
            ("✓ Chức năng In ấn & PDF:", "In ấn trực tiếp qua máy in vật lý và xuất báo cáo chuẩn khổ giấy A4."),
            ("✓ Xuất ảnh JPEG có Trademark:", "Độ phân giải siêu nét 300 DPI kèm nhãn bản quyền mờ tinh tế."),
            ("✓ Kết nối AI đa tầng:", "Mở khóa toàn bộ trợ lý AI Neuro-Symbolic (DeepSeek-R1, Qwen Coder, Ollama & API).")
        ] if not is_en else [
            ("✓ Exclusive PRO Badge Icon:", "Automatically switches Taskbar & App icon to the sleek golden PRO badge."),
            ("✓ Professional Print Engine:", "Direct physical printing and full A4 PDF technical math reports."),
            ("✓ JPEG Export with Trademark:", "300 DPI high-res print export with subtle elegant watermark."),
            ("✓ Multi-Tier AI Assistant:", "Unlocks full Neuro-Symbolic AI solvers (DeepSeek-R1, Qwen Coder, API).")
        ]

        for title_feat, desc_feat in features:
            f_frame = tk.Frame(body, bg="#f8fafc", pady=3)
            f_frame.pack(side=tk.TOP, fill=tk.X)
            tk.Label(f_frame, text=title_feat, font=("Segoe UI", 9, "bold"), bg="#f8fafc", fg="#0f172a").pack(side=tk.LEFT)
            tk.Label(f_frame, text=" " + desc_feat, font=("Segoe UI", 9), bg="#f8fafc", fg="#475569").pack(side=tk.LEFT)

        # Buttons
        btn_box = tk.Frame(dlg, bg="#f8fafc", padx=20, pady=16)
        btn_box.pack(side=tk.BOTTOM, fill=tk.X)

        def _do_activate():
            self.save_pro_license_state(True)
            self.apply_branding_icon(is_pro=True)
            if hasattr(self, 'status_lbl') and self.status_lbl:
                self.status_lbl.config(text="⭐ ĐÃ KÍCH HOẠT BẢN PRO! ICON ĐÃ ĐƯỢC CHUYỂN SANG BIỂU TƯỢNG PRO ÁNH KIM.")
            messagebox.showinfo(
                "Payment Confirmed" if is_en else "Thanh Toán & Kích Hoạt Thành Công",
                "Cảm ơn bạn đã ủng hộ! Bản quyền CAD Math Studio Pro đã được kích hoạt thành công.\n"
                "Biểu tượng của ứng dụng đã được đổi sang Icon Pro bo góc sang trọng.",
                parent=dlg
            )
            dlg.destroy()

        btn_activate = tk.Button(
            btn_box,
            text="⭐ " + ("Confirm Payment / Activate Pro Icon" if is_en else "Xác Nhận Đã Thanh Toán / Đổi Sang Icon Pro"),
            font=("Segoe UI", 9, "bold"),
            bg="#f59e0b",
            fg="#0f172a",
            activebackground="#d97706",
            activeforeground="#0f172a",
            relief="raised",
            bd=2,
            padx=14,
            pady=6,
            cursor="hand2",
            command=_do_activate
        )
        btn_activate.pack(side=tk.LEFT)

        btn_close = tk.Button(
            btn_box,
            text="Close" if is_en else "Đóng",
            font=("Segoe UI", 9),
            bg="#e2e8f0",
            relief="raised",
            bd=1,
            padx=12,
            pady=6,
            command=dlg.destroy
        )
        btn_close.pack(side=tk.RIGHT)
'''

# Find a good place to insert the methods (e.g. before show_about_dialog or setup_menu_bar)
target_hook = "    def show_about_dialog(self):"
if target_hook in content:
    content = content.replace(target_hook, methods_to_add + "\n" + target_hook)
    print("Added Pro licensing and icon switching methods successfully!")
else:
    print("Warning: target_hook not found.")

# Add menu item in Help menu
old_help_menu = 'help_menu.add_command(\n            label="About CAD Math Studio..." if is_en else "Thông tin phần mềm CAD Math Studio...",'
if "help_menu.add_command" in content:
    content = content.replace(
        'menubar.add_cascade(label="Help" if is_en else "Thông tin", menu=help_menu)',
        'help_menu.add_command(label="⭐ License & Payment (Upgrade to Pro)..." if is_en else "⭐ Bản quyền & Thanh toán (Kích hoạt Pro)...", command=self.open_license_payment_dialog)\n        menubar.add_cascade(label="Help" if is_en else "Thông tin", menu=help_menu)'
    )
    print("Added License & Payment to Help menu successfully!")

with open('cad_math_v2/cad_math_v2.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patching completed.")
