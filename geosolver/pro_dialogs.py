# -*- coding: utf-8 -*-
"""
GeoSolver 2D CAD Pro - Giao diện Nâng cấp Bản quyền & Hộp thoại Kích hoạt
Tích hợp Microsoft Store IAP ($1.99), mã kích hoạt Hardware ID và chuyển đổi giao diện Pro.
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional


class ActivateCodeDialog(tk.Toplevel):
    """Hộp thoại hiển thị Hardware ID và nhập mã kích hoạt khóa theo 1 máy tính."""
    WIN32_BG = "#ECE9D8"
    FONT_BOLD = ("Tahoma", 8, "bold")
    FONT_UI = ("Tahoma", 8)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent_upgrade = parent
        self.app = getattr(parent, "app", parent)
        self.lang = getattr(parent, "current_lang", getattr(self.app, "current_lang", "vi"))
        is_vn = (self.lang == "vi")

        self.title("Kích Hoạt Bản Quyền GeoSolver 2D Pro" if is_vn else "Activate GeoSolver 2D Pro")
        self.geometry("490x300")
        self.resizable(False, False)
        self.configure(bg=self.WIN32_BG)
        self.transient(parent)
        self.grab_set()

        try:
            from geosolver.license_manager import LicenseManager
            hwid = LicenseManager.get_hardware_id()
        except Exception:
            hwid = "N/A"

        # Frame HWID
        hw_box = tk.LabelFrame(
            self,
            text="Mã máy tính của bạn (Hardware ID)" if is_vn else "Your Machine Hardware ID",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            padx=10,
            pady=6,
        )
        hw_box.pack(side=tk.TOP, fill=tk.X, padx=12, pady=10)

        hw_row = tk.Frame(hw_box, bg=self.WIN32_BG)
        hw_row.pack(fill=tk.X)

        tk.Label(
            hw_row,
            text=hwid,
            font=("Consolas", 11, "bold"),
            fg="#000080",
            bg="#FFFFFF",
            relief=tk.SUNKEN,
            bd=1,
            padx=8,
            pady=2
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        def copy_hwid():
            self.clipboard_clear()
            self.clipboard_append(hwid)
            messagebox.showinfo(
                "Đã sao chép" if is_vn else "Copied",
                "Đã sao chép mã máy tính vào bộ nhớ đệm!\nHãy gửi mã này để nhận key kích hoạt." if is_vn else "Hardware ID copied to clipboard!",
                parent=self
            )

        tk.Button(
            hw_row,
            text="[ 📋 Sao chép ]" if is_vn else "[ 📋 Copy ]",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            padx=6,
            command=copy_hwid
        ).pack(side=tk.RIGHT, padx=(6, 0))

        tk.Label(
            hw_box,
            text="* Gửi mã này cho nhà phát triển/trường học để nhận key riêng cho máy." if is_vn else "* Send this Hardware ID to get a machine-locked license key.",
            font=("Tahoma", 7, "italic"),
            fg="#555555",
            bg=self.WIN32_BG
        ).pack(anchor="w", pady=(4, 0))

        # Frame Input Code
        code_box = tk.Frame(self, bg=self.WIN32_BG, padx=12)
        code_box.pack(side=tk.TOP, fill=tk.X)

        tk.Label(
            code_box,
            text="Nhập mã kích hoạt Pro nhận được (PRO2D-XXXX-YYYY-ZZZZ):" if is_vn else "Enter received Pro Activation Code:",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG
        ).pack(anchor="w", pady=(2, 2))
        self.entry_code = tk.Entry(code_box, font=("Consolas", 11, "bold"), justify="center")
        self.entry_code.pack(fill=tk.X, pady=2)
        self.entry_code.focus_set()

        # Buttons
        btn_box = tk.Frame(self, bg=self.WIN32_BG, padx=12, pady=10)
        btn_box.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(
            btn_box,
            text="[ Kích Hoạt Ngay ]" if is_vn else "[ Activate Now ]",
            font=self.FONT_BOLD,
            bg="#2E7D32",
            fg="#FFFFFF",
            padx=10,
            pady=4,
            command=self._do_activate
        ).pack(side=tk.LEFT)

        tk.Button(
            btn_box,
            text="[ Hủy ]" if is_vn else "[ Cancel ]",
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            padx=8,
            pady=4,
            command=self.destroy
        ).pack(side=tk.RIGHT)

    def _do_activate(self):
        code = self.entry_code.get().strip()
        is_vn = (self.lang == "vi")
        if not code:
            messagebox.showwarning(
                "Thiếu dữ liệu" if is_vn else "Warning",
                "Vui lòng nhập mã kích hoạt!" if is_vn else "Please enter activation code!",
                parent=self
            )
            return

        try:
            from geosolver.license_manager import LicenseManager
            ok, msg = LicenseManager.activate_with_code(code)
        except Exception as ex:
            ok, msg = False, str(ex)

        if ok:
            messagebox.showinfo("Kích hoạt thành công" if is_vn else "Success", msg, parent=self)
            if hasattr(self.app, "update_pro_ui_state"):
                self.app.update_pro_ui_state()
            self.destroy()
            if self.parent_upgrade and hasattr(self.parent_upgrade, "destroy"):
                self.parent_upgrade.destroy()
        else:
            messagebox.showwarning("Kích hoạt thất bại" if is_vn else "Failed", msg, parent=self)


class ProUpgradeDialog(tk.Toplevel):
    """Hộp thoại giới thiệu và nâng cấp Gói Pro ($1.99) qua Microsoft Store IAP hoặc mã kích hoạt."""
    WIN32_BG = "#ECE9D8"
    FONT_TITLE = ("Tahoma", 10, "bold")
    FONT_BOLD = ("Tahoma", 8, "bold")
    FONT_UI = ("Tahoma", 8)

    def __init__(self, parent, feature: str = "general"):
        super().__init__(parent)
        self.app = parent
        self.lang = getattr(parent, "current_lang", "vi")
        self.feature = feature
        is_vn = (self.lang == "vi")

        self.title("Nâng Cấp GeoSolver 2D Pro ($1.99) - Gói In Ấn Sạch & AI" if is_vn else "Upgrade to GeoSolver 2D Pro ($1.99)")
        self.geometry("540x480")
        self.resizable(False, False)
        self.configure(bg=self.WIN32_BG)
        self.transient(parent)
        self.grab_set()

        try:
            x = parent.winfo_rootx() + (parent.winfo_width() - 540) // 2
            y = parent.winfo_rooty() + (parent.winfo_height() - 480) // 2
            self.geometry(f"+{max(10, x)}+{max(10, y)}")
        except Exception:
            pass

        # 1. HEADER BANNER
        hdr = tk.Frame(self, bg="#002D62", pady=10, padx=14)
        hdr.pack(side=tk.TOP, fill=tk.X)

        tk.Label(
            hdr,
            text="💎 GEOSOLVER 2D PRO — GÓI IN ẤN SẠCH & KẾT NỐI AI",
            font=("Tahoma", 11, "bold"),
            bg="#002D62",
            fg="#FFD700",
        ).pack(anchor="w")

        subtitle_vn = "Sở hữu trọn đời chỉ $1.99 — In ấn & xuất file JPEG 100% Sạch (Không Trademark)"
        subtitle_en = "Lifetime access for only $1.99 — 100% Trademark-Free Direct Printing & JPEG Export"
        tk.Label(
            hdr,
            text=subtitle_vn if is_vn else subtitle_en,
            font=("Tahoma", 8),
            bg="#002D62",
            fg="#FFFFFF",
        ).pack(anchor="w", pady=(2, 0))

        # Context message if triggered by a specific feature
        ctx_frame = tk.Frame(self, bg="#FFF8E1", relief=tk.SOLID, bd=1)
        ctx_frame.pack(side=tk.TOP, fill=tk.X, padx=14, pady=8)

        if feature == "print":
            msg_vn = "ℹ️ Bản Tiêu Chuẩn cho phép in ấn kèm trademark mờ bán trong suốt. Gói Pro ($1.99) giúp in bản vẽ SẠCH 100%."
            msg_en = "ℹ️ Standard Edition prints with subtle trademark. Pro Edition ($1.99) prints 100% CLEAN diagrams."
        elif feature == "export_jpeg":
            msg_vn = "ℹ️ Gói Pro ($1.99) hỗ trợ xuất file ảnh JPEG / PNG sắc nét 300 DPI sạch 100%, không dính hình mờ bản quyền."
            msg_en = "ℹ️ Pro Edition ($1.99) exports crisp 300 DPI JPEG diagrams completely free of watermarks."
        else:
            msg_vn = "ℹ️ Nâng cấp Pro ($1.99) để sở hữu tính năng In ấn sạch 100%, xuất file JPEG và kết nối AI thông minh trọn đời."
            msg_en = "ℹ️ Upgrade to Pro ($1.99) for lifetime 100% trademark-free printing, JPEG export, and unlimited AI connection."

        tk.Label(
            ctx_frame,
            text=msg_vn if is_vn else msg_en,
            font=self.FONT_BOLD,
            bg="#FFF8E1",
            fg="#795548",
            padx=10,
            pady=5,
            wraplength=490,
            justify=tk.LEFT,
        ).pack(fill=tk.X)

        # Feature bullet list
        body = tk.Frame(self, bg=self.WIN32_BG, padx=16, pady=2)
        body.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        features_vn = (
            "Đặc quyền của Gói Pro In Ấn & AI Thông Minh ($1.99):\n\n"
            "• 🖨️ In ấn trực tiếp sạch 100% (Ctrl+P): In ra máy in qua Windows Print Wizard không dính trademark bản quyền.\n"
            "• 📐 Xuất ảnh PNG & JPEG siêu nét 300 DPI: Không có watermark, nền trắng tinh khiết chuẩn bị giáo án và đề thi.\n"
            "• ⚡ Hỗ trợ kết nối AI không giới hạn: Tích hợp đầy đủ mô hình Local AI (Ollama DeepSeek-R1, Qwen2.5-Coder) và Cloud AI.\n"
            "• 💎 Biểu tượng Pro sang trọng: Tự động đổi icon cửa sổ và thanh tác vụ sang icon PRO mạ vàng sang trọng khi kích hoạt.\n"
            "• 🌐 Sở hữu trọn đời: Mua 1 lần sở hữu vĩnh viễn, miễn phí nâng cấp toàn bộ tính năng trong tương lai."
        )
        features_en = (
            "Exclusive benefits of GeoSolver 2D Pro ($1.99):\n\n"
            "• 🖨️ 100% Clean Direct Printing (Ctrl+P): Print technical drawings via Windows Print Wizard without any watermark.\n"
            "• 📐 Ultra High-Res PNG & JPEG Export (300 DPI): Clean diagrams without trademark for exams and textbooks.\n"
            "• ⚡ Unlimited AI Connection: Seamless integration with Local Ollama (DeepSeek-R1, Qwen2.5) and Cloud AI.\n"
            "• 💎 Luxury Pro App Icon: Window icon automatically changes to rounded gold PRO badge upon activation.\n"
            "• 🌐 Lifetime Ownership: Free access to all future updates and educational packages."
        )

        tk.Label(
            body,
            text=features_vn if is_vn else features_en,
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            fg="#1A1A1A",
            justify=tk.LEFT,
            wraplength=500
        ).pack(anchor="w", pady=(2, 6))

        # Bottom buttons
        btn_area = tk.Frame(self, bg=self.WIN32_BG, padx=14, pady=10)
        btn_area.pack(side=tk.BOTTOM, fill=tk.X)

        from geosolver.license_manager import LicenseManager
        is_already_pro = LicenseManager.is_pro_active()

        if is_already_pro:
            tk.Label(
                btn_area,
                text="💎 BẢN QUYỀN PRO ĐANG HOẠT ĐỘNG (ĐÃ KÍCH HOẠT VĨNH VIỄN)" if is_vn else "💎 PRO EDITION ACTIVE (LIFETIME LICENSE)",
                font=self.FONT_BOLD,
                bg=self.WIN32_BG,
                fg="#2E7D32"
            ).pack(side=tk.LEFT, pady=4)
            tk.Button(
                btn_area,
                text="[ Đóng ]" if is_vn else "[ Close ]",
                font=self.FONT_UI,
                bg=self.WIN32_BG,
                padx=12,
                pady=4,
                command=self.destroy
            ).pack(side=tk.RIGHT)
        else:
            # Row 1 of actions: Store purchase and Quick activate
            act_row = tk.Frame(btn_area, bg=self.WIN32_BG)
            act_row.pack(fill=tk.X, pady=(0, 6))

            tk.Button(
                act_row,
                text="🛒 Mua Gói Pro ($1.99 qua Microsoft Store)" if is_vn else "🛒 Buy Pro ($1.99 via Store)",
                font=self.FONT_BOLD,
                bg="#002D62",
                fg="#FFD700",
                padx=10,
                pady=4,
                cursor="hand2",
                command=self._do_store_purchase
            ).pack(side=tk.LEFT)

            tk.Button(
                act_row,
                text="⚡ Kích Hoạt Nhanh ($1.99)" if is_vn else "⚡ Quick Activate",
                font=self.FONT_BOLD,
                bg="#2E7D32",
                fg="#FFFFFF",
                padx=8,
                pady=4,
                cursor="hand2",
                command=self._do_simulate_purchase
            ).pack(side=tk.LEFT, padx=6)

            # Row 2 of actions: Enter Code and Close
            act_row2 = tk.Frame(btn_area, bg=self.WIN32_BG)
            act_row2.pack(fill=tk.X)

            tk.Button(
                act_row2,
                text="🔑 Nhập Mã Kích Hoạt (Hardware ID)..." if is_vn else "🔑 Enter Activation Code...",
                font=self.FONT_BOLD,
                bg=self.WIN32_BG,
                fg="#000080",
                padx=8,
                pady=4,
                command=self._open_code_dialog
            ).pack(side=tk.LEFT)

            tk.Button(
                act_row2,
                text="[ Đóng ]" if is_vn else "[ Close ]",
                font=self.FONT_UI,
                bg=self.WIN32_BG,
                padx=10,
                pady=4,
                command=self.destroy
            ).pack(side=tk.RIGHT)

    def _do_store_purchase(self):
        from geosolver.license_manager import LicenseManager
        LicenseManager.open_store_purchase()

    def _do_simulate_purchase(self):
        is_vn = (self.lang == "vi")
        from geosolver.license_manager import LicenseManager
        ok, msg = LicenseManager.simulate_store_purchase()
        if ok:
            messagebox.showinfo("Thành công" if is_vn else "Success", msg, parent=self)
            if hasattr(self.app, "update_pro_ui_state"):
                self.app.update_pro_ui_state()
            self.destroy()
        else:
            messagebox.showwarning("Lỗi" if is_vn else "Error", msg, parent=self)

    def _open_code_dialog(self):
        ActivateCodeDialog(self)
