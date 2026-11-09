# -*- coding: utf-8 -*-
"""
Module: higher_math_dialog.py
Mô tả: Hộp thoại Toán cao cấp (Higher Mathematics Studio Dialog)
Thiết kế: Giao diện chuẩn CAD Cổ điển (#ECE9D8), tối giản, trực quan, hỗ trợ tính toán bất đồng bộ không gây khóa luồng giao diện.
Hỗ trợ 6 chuyên đề:
  1. Đại số tuyến tính & Ma trận
  2. Giải tích đơn biến & Tích phân suy rộng
  3. Chuỗi số & Fourier
  4. Giải tích đa biến & Tích phân bội
  5. Tích phân đường - mặt & Lý thuyết trường
  6. Phương trình vi phân & Biến đổi Laplace
"""

from __future__ import annotations

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Any, Dict, Tuple

import sympy as sp
from stem_shared_core.higher_math_kernel import (
    LinearAlgebraEngine,
    AdvancedCalculusEngine,
    SeriesEngine,
    MultivariableEngine,
    FieldTheoryEngine,
    DifferentialEquationsEngine,
    HigherMathKernelError,
    format_matrix_plain,
)


class HigherMathDialog:
    """Hộp thoại công cụ Toán cao cấp."""

    def __init__(self, parent: tk.Widget, initial_topic_idx: int = 0, lang: str = "vi"):
        self.parent = parent
        self.lang = lang
        self.top = tk.Toplevel(parent)
        self.top.title(self._s("Toán cao cấp - Higher Mathematics Studio", "Advanced Mathematics Studio"))
        self.top.geometry("1060x680")
        self.top.minsize(920, 600)
        self.top.configure(bg="#ECE9D8")

        # Giữ icon cửa sổ chính nếu có
        try:
            p_top = parent.winfo_toplevel()
            if hasattr(p_top, "_app_icon_photo") and p_top._app_icon_photo:
                self.top.iconphoto(False, p_top._app_icon_photo)
            elif hasattr(p_top, "ico_path") and p_top.ico_path:
                self.top.iconbitmap(p_top.ico_path)
        except Exception:
            pass

        # Căn giữa cửa sổ
        try:
            p_top = parent.winfo_toplevel()
            x = p_top.winfo_rootx() + (p_top.winfo_width() - 1060) // 2
            y = p_top.winfo_rooty() + (p_top.winfo_height() - 680) // 2
            self.top.geometry(f"+{max(10, x)}+{max(10, y)}")
        except Exception:
            pass

        self._last_result_dict: Optional[Dict[str, Any]] = None
        self._loaded_problems: Optional[list] = None
        self._gemini_loaded_problems = None  # Bí danh tương thích
        self._build_ui(initial_topic_idx)

    def _s(self, vi_text: str, en_text: str) -> str:
        """Trả về chuỗi song ngữ tương ứng ngôn ngữ hộp thoại."""
        return en_text if getattr(self, "lang", "vi") == "en" else vi_text

    def _translate_step_en(self, step: str) -> str:
        """Chuyển đổi từng bước tính toán giải tích sang tiếng Anh chuẩn."""
        trans_map = [
            ("Ma trận hệ số A kích thước:", "Coefficient matrix A dimension:"),
            ("Ma trận mở rộng [A|B] kích thước:", "Augmented matrix [A|B] dimension:"),
            ("Hạng của A: rank(A) =", "Rank of matrix A: rank(A) ="),
            ("Hạng của ma trận mở rộng: rank(A|B) =", "Rank of augmented matrix: rank(A|B) ="),
            ("Theo định lý Kronecker - Capelli:", "By Kronecker-Capelli theorem:"),
            ("Hệ PHƯƠNG TRÌNH VÔ NGHIỆM.", "THE SYSTEM HAS NO SOLUTION."),
            ("Hệ có nghiệm duy nhất", "The system has a unique solution"),
            ("Hệ có vô số nghiệm phụ thuộc", "The system has infinitely many solutions depending on"),
            ("Nghiệm tổng quát:", "General solution:"),
            ("Đưa [A|B] về dạng ma trận bậc thang rút gọn (RREF)", "Transform [A|B] to Reduced Row Echelon Form (RREF)"),
            ("các cột chốt:", "pivot columns:"),
            ("Đa thức đặc trưng:", "Characteristic polynomial:"),
            ("Các giá trị riêng và bội số:", "Eigenvalues and algebraic multiplicities:"),
            ("Các không gian con riêng tương ứng:", "Corresponding eigenspaces:"),
            ("Ma trận đường chéo D =", "Diagonal matrix D ="),
            ("Ma trận làm chéo hóa P =", "Diagonalizing matrix P ="),
            ("Ma trận KHÔNG THỂ chéo hóa", "Matrix CANNOT be diagonalized"),
            ("Ma trận đối xứng biểu diễn dạng toàn phương:", "Symmetric matrix of quadratic form:"),
            ("Các định thức con chính:", "Leading principal minors:"),
            ("Theo tiêu chuẩn Sylvester:", "By Sylvester's criterion:"),
            ("Dạng toàn phương XÁC ĐỊNH DƯƠNG", "Quadratic form is POSITIVE DEFINITE"),
            ("Dạng toàn phương XÁC ĐỊNH ÂM", "Quadratic form is NEGATIVE DEFINITE"),
            ("Dạng toàn phương NỬA XÁC ĐỊNH DƯƠNG", "Quadratic form is POSITIVE SEMI-DEFINITE"),
            ("Dạng toàn phương NỬA XÁC ĐỊNH ÂM", "Quadratic form is NEGATIVE SEMI-DEFINITE"),
            ("Dạng toàn phương KHÔNG XÁC ĐỊNH DẤU", "Quadratic form is INDEFINITE"),
            ("Dạng vô định", "Indeterminate form"),
            ("Áp dụng khai triển Taylor / quy tắc L'Hopital", "Applying Taylor expansion / L'Hopital's rule"),
            ("Giá trị giới hạn:", "Limit value:"),
            ("Khai triển Maclaurin", "Maclaurin series expansion"),
            ("Khai triển Taylor", "Taylor series expansion"),
            ("Tích phân suy rộng", "Improper integral"),
            ("Tích phân HỘI TỤ", "Integral CONVERGES"),
            ("Tích phân PHÂN KỲ", "Integral DIVERGES"),
            ("Xét chuỗi số với số hạng tổng quát:", "Consider series with general term:"),
            ("Theo tiêu chuẩn D'Alembert:", "By D'Alembert ratio test:"),
            ("Theo tiêu chuẩn Cauchy:", "By Cauchy root test:"),
            ("Chuỗi số HỘI TỤ", "Series CONVERGES"),
            ("Chuỗi số PHÂN KỲ", "Series DIVERGES"),
            ("Bán kính hội tụ:", "Radius of convergence:"),
            ("Khoảng hội tụ:", "Interval of convergence:"),
            ("Chuỗi Fourier của hàm", "Fourier series of function"),
            ("Hệ số a_0 =", "Coefficient a_0 ="),
            ("Hệ số a_n =", "Coefficient a_n ="),
            ("Hệ số b_n =", "Coefficient b_n ="),
            ("Đạo hàm riêng cấp 1:", "First-order partial derivatives:"),
            ("Đạo hàm riêng cấp 2:", "Second-order partial derivatives:"),
            ("Ma trận Hessian:", "Hessian matrix:"),
            ("Các điểm dừng:", "Critical points:"),
            ("Điểm cực tiểu địa phương", "Local minimum point"),
            ("Điểm cực đại địa phương", "Local maximum point"),
            ("Điểm yên ngựa", "Saddle point"),
            ("Hàm Lagrange:", "Lagrange function:"),
            ("Hệ điều kiện dừng Lagrange:", "Lagrange stationary system:"),
            ("Tích phân kép lặp:", "Iterated double integral:"),
            ("Trường vector:", "Vector field:"),
            ("Độ phân kỳ (Divergence):", "Divergence (div F):"),
            ("Độ xoáy (Curl/Rot):", "Curl (rot F):"),
            ("Trường là TRƯỜNG THẾ VỊ", "Field is CONSERVATIVE (Gradient field)"),
            ("Hàm thế vị U:", "Potential function U:"),
            ("Trường KHÔNG PHẢI trường thế", "Field is NOT conservative"),
            ("Phương trình vi phân:", "Differential equation:"),
            ("Nghiệm bài toán Cauchy:", "Cauchy problem solution:"),
            ("Biến đổi Laplace:", "Laplace transform:"),
            ("Biến đổi Laplace ngược:", "Inverse Laplace transform:")
        ]
        res = step
        for vi_pat, en_rep in trans_map:
            res = res.replace(vi_pat, en_rep)
        return res

    def _build_ui(self, initial_topic_idx: int):
        # 1. HEADER BANNER
        header = tk.Frame(self.top, bg="#003366", height=42, padx=12)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        lbl_title = tk.Label(
            header,
            text=self._s("CHUYÊN ĐỀ TOÁN CAO CẤP", "ADVANCED MATHEMATICS"),
            font=("Segoe UI", 10, "bold"),
            fg="#FFFFFF",
            bg="#003366",
        )
        lbl_title.pack(side=tk.LEFT, pady=10)

        tk.Button(
            header,
            text=self._s("Nạp tệp JSON...", "Load JSON File..."),
            font=("Segoe UI", 8),
            bg="#D4D0C8",
            relief="raised",
            bd=1,
            command=self.load_problems_json_dialog,
        ).pack(side=tk.RIGHT, padx=6, pady=8)

        lbl_sub = tk.Label(
            header,
            text=self._s("6 chuyên đề đại học • Tính toán SymPy CAS", "University Curriculum • SymPy CAS Engine"),
            font=("Segoe UI", 8, "italic"),
            fg="#BDD7EE",
            bg="#003366",
        )
        lbl_sub.pack(side=tk.RIGHT, pady=12)

        # 2. KHUNG CHÍNH (NOTEBOOK 6 CHUYÊN ĐỀ)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("HigherMath.TNotebook", background="#ECE9D8", borderwidth=0)
        style.configure("HigherMath.TNotebook.Tab", background="#D4D0C8", foreground="#000000", padding=[10, 5], font=("Segoe UI", 9, "bold"))
        style.map("HigherMath.TNotebook.Tab", background=[("selected", "#ECE9D8")], foreground=[("selected", "#003366")])

        self.notebook = ttk.Notebook(self.top, style="HigherMath.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=(6, 4))

        # Khởi tạo 6 Tab
        self.tab_linear = tk.Frame(self.notebook, bg="#ECE9D8")
        self.tab_calculus1 = tk.Frame(self.notebook, bg="#ECE9D8")
        self.tab_series = tk.Frame(self.notebook, bg="#ECE9D8")
        self.tab_multivar = tk.Frame(self.notebook, bg="#ECE9D8")
        self.tab_field = tk.Frame(self.notebook, bg="#ECE9D8")
        self.tab_ode = tk.Frame(self.notebook, bg="#ECE9D8")

        self.notebook.add(self.tab_linear, text=self._s(" 1. Đại số tuyến tính ", " 1. Linear Algebra "))
        self.notebook.add(self.tab_calculus1, text=self._s(" 2. Giải tích 1 ", " 2. Single-Var Calc "))
        self.notebook.add(self.tab_series, text=self._s(" 3. Chuỗi & Fourier ", " 3. Series & Fourier "))
        self.notebook.add(self.tab_multivar, text=self._s(" 4. Giải tích đa biến ", " 4. Multivariable Calc "))
        self.notebook.add(self.tab_field, text=self._s(" 5. Trường vector ", " 5. Vector Fields "))
        self.notebook.add(self.tab_ode, text=self._s(" 6. PT vi phân & Laplace ", " 6. ODE & Laplace "))

        # Xây dựng nội dung từng Tab
        self._build_tab_linear()
        self._build_tab_calculus1()
        self._build_tab_series()
        self._build_tab_multivar()
        self._build_tab_field()
        self._build_tab_ode()

        # Chọn tab khởi tạo
        if 0 <= initial_topic_idx < 6:
            self.notebook.select(initial_topic_idx)

        # 3. STATUS BAR DƯỚI CÙNG
        status_bar = tk.Frame(self.top, bg="#D4D0C8", bd=1, relief="sunken", height=24)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        status_bar.pack_propagate(False)

        self.status_lbl = tk.Label(
            status_bar,
            text=self._s("Sẵn sàng tính toán.", "Ready for computation."),
            font=("Segoe UI", 8),
            fg="#222222",
            bg="#D4D0C8",
            anchor="w",
            padx=6,
        )
        self.status_lbl.pack(fill=tk.X, side=tk.LEFT)

    # ==========================================================================
    # CÁC HÀM TIỆN ÍCH DÙNG CHUNG CHO CẢ 6 TAB
    # ==========================================================================
    def _create_split_layout(self, parent_tab) -> Tuple[tk.Frame, tk.Frame]:
        """Tạo giao diện chia đôi: Bên trái nhập liệu (430px), Bên phải kết quả (fill)."""
        container = tk.Frame(parent_tab, bg="#ECE9D8", padx=6, pady=6)
        container.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.LabelFrame(
            container,
            text=" KHÔNG GIAN NHẬP LIỆU & CÔNG CỤ ",
            font=("Segoe UI", 8, "bold"),
            fg="#003366",
            bg="#ECE9D8",
            padx=8,
            pady=6,
            width=430,
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 4))
        left_frame.pack_propagate(False)

        right_frame = tk.LabelFrame(
            container,
            text=" KẾT QUẢ TÍNH TOÁN & CÁC BƯỚC BIẾN ĐỔI ",
            font=("Segoe UI", 8, "bold"),
            fg="#003366",
            bg="#ECE9D8",
            padx=8,
            pady=6,
        )
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        return left_frame, right_frame

    def _create_quick_symbol_palette(self, parent, target_entry_getter):
        """Tạo thanh ký hiệu toán học nhanh tiện lợi."""
        p_frame = tk.Frame(parent, bg="#D4D0C8", bd=1, relief="groove", pady=2)
        p_frame.pack(fill=tk.X, pady=(2, 6))

        symbols = [
            ("∂", "∂"), ("∫", "∫"), ("∬", "∬"), ("∭", "∭"),
            ("∇", "∇"), ("λ", "λ"), ("∞", "oo"), ("π", "pi"),
            ("±", "±"), ("√", "sqrt("), ("x²", "^2"), ("y²", "^2"),
            ("e^x", "exp("), ("y'", "y'"), ("y''", "y''"),
        ]

        def _insert(sym):
            w = target_entry_getter()
            if w:
                w.insert(tk.INSERT, sym)
                w.focus_set()

        for label, val in symbols:
            btn = tk.Button(
                p_frame,
                text=label,
                font=("Consolas", 8, "bold"),
                width=3,
                bg="#ECE9D8",
                relief="raised",
                bd=1,
                command=lambda s=val: _insert(s),
            )
            btn.pack(side=tk.LEFT, padx=1)

    def _create_result_display_box(self, parent_frame) -> Tuple[tk.Text, tk.Frame]:
        """Tạo hộp thoại hiển thị kết quả có cuộn và các nút xuất báo cáo."""
        txt_box = tk.Text(
            parent_frame,
            font=("Consolas", 10),
            bg="#FFFFFF",
            fg="#000000",
            wrap=tk.WORD,
            bd=1,
            relief="sunken",
        )
        scrollbar = ttk.Scrollbar(parent_frame, orient=tk.VERTICAL, command=txt_box.yview)
        txt_box.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        txt_box.pack(fill=tk.BOTH, expand=True)

        # Nút hành động dưới khu vực kết quả
        btn_bar = tk.Frame(parent_frame, bg="#ECE9D8", pady=4)
        btn_bar.pack(fill=tk.X)

        btn_copy = tk.Button(
            btn_bar,
            text="📋 Sao chép kết quả",
            font=("Segoe UI", 8),
            bg="#D4D0C8",
            relief="raised",
            bd=1,
            command=lambda: self._copy_to_clipboard(txt_box.get("1.0", tk.END)),
        )
        btn_copy.pack(side=tk.LEFT, padx=2)

        btn_latex = tk.Button(
            btn_bar,
            text="📄 Sao chép mã LaTeX",
            font=("Segoe UI", 8),
            bg="#D4D0C8",
            relief="raised",
            bd=1,
            command=self._copy_latex,
        )
        btn_latex.pack(side=tk.LEFT, padx=2)

        btn_save = tk.Button(
            btn_bar,
            text="💾 Lưu báo cáo...",
            font=("Segoe UI", 8),
            bg="#D4D0C8",
            relief="raised",
            bd=1,
            command=lambda: self._export_solution_report(txt_box.get("1.0", tk.END)),
        )
        btn_save.pack(side=tk.LEFT, padx=2)

        return txt_box, btn_bar

    def _copy_to_clipboard(self, text: str):
        self.top.clipboard_clear()
        self.top.clipboard_append(text.strip())
        self.status_lbl.config(text="Đã sao chép nội dung vào Clipboard.")

    def _copy_latex(self):
        if self._last_result_dict and "latex" in self._last_result_dict:
            latex_code = str(self._last_result_dict["latex"])
            self.top.clipboard_clear()
            self.top.clipboard_append(latex_code)
            self.status_lbl.config(text="Đã sao chép mã LaTeX vào Clipboard.")
        else:
            messagebox.showinfo("Thông báo", "Chưa có kết quả hoặc mã LaTeX để sao chép.", parent=self.top)

    def _export_solution_report(self, text: str):
        path = filedialog.asksaveasfilename(
            parent=self.top,
            title="Lưu báo cáo tính toán",
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt"), ("Markdown Report", "*.md"), ("All Files", "*.*")],
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)
                self.status_lbl.config(text=f"Đã lưu báo cáo tại: {path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu tệp: {e}", parent=self.top)

    def load_problems_json_dialog(self, file_path: Optional[str] = None):
        """Nạp ngân hàng bài toán từ tệp JSON."""
        import json
        if not file_path:
            file_path = filedialog.askopenfilename(
                parent=self.top,
                title="Chọn tệp đề bài JSON",
                initialdir=r"D:\AI DATA\toan cao cap",
                filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            count = len(data) if isinstance(data, list) else 0
            self._loaded_problems = data
            self._gemini_loaded_problems = data
            self.status_lbl.config(text=f"Đã nạp thành công {count} bài toán từ: {os.path.basename(file_path)}")

            msg = f"Đã nạp thành công {count} bài toán từ tệp JSON!\n\n"
            for idx, item in enumerate(data, 1):
                msg += f"{idx}. [{item.get('chuyen_de', '')}] {item.get('ten_bai', '')}\n"
            msg += "\nCác ví dụ đã sẵn sàng để tra cứu trên giao diện!"
            messagebox.showinfo("Nạp Đề Thành Công", msg, parent=self.top)
        except Exception as e:
            messagebox.showerror("Lỗi nạp tệp JSON", f"Không thể đọc tệp JSON: {e}", parent=self.top)

    # Bí danh tương thích
    load_gemini_json_dialog = load_problems_json_dialog

    def _run_async(self, target_fn, result_box: tk.Text, success_msg: str = "Tính toán hoàn tất."):
        """Thực thi tính toán trong luồng nền để giữ giao diện luôn mượt mà."""
        self.status_lbl.config(text="Đang tính toán...")
        result_box.delete("1.0", tk.END)
        result_box.insert(tk.END, "Đang tính toán, vui lòng đợi...\n")

        def _worker():
            try:
                res = target_fn()
                self.top.after(0, lambda: self._display_result(result_box, res))
                self.top.after(0, lambda: self.status_lbl.config(text=success_msg))
            except Exception as e:
                err_text = str(e)
                def _handle_err():
                    result_box.delete("1.0", tk.END)
                    result_box.insert(tk.END, f"[LỖI TÍNH TOÁN]: {err_text}\n")
                    self.status_lbl.config(text=f"Lỗi: {err_text[:50]}")
                    messagebox.showerror("Lỗi tính toán", err_text, parent=self.top)
                self.top.after(0, _handle_err)

        threading.Thread(target=_worker, daemon=True).start()

    def _display_result(self, txt_box: tk.Text, res_dict: Dict[str, Any]):
        """Hiển thị kết quả chi tiết vào khung kết quả."""
        self._last_result_dict = res_dict
        txt_box.delete("1.0", tk.END)

        is_en = (getattr(self, "lang", "vi") == "en")
        # 1. Tiêu đề trạng thái
        txt_box.insert(tk.END, "════════════════════════════════════════════════════════════════════════\n")
        txt_box.insert(tk.END, ("  COMPUTATION RESULTS & DETAILED DERIVATION\n" if is_en else "  KẾT QUẢ TÍNH TOÁN & CÁC BƯỚC BIẾN ĐỔI CHI TIẾT\n"))
        txt_box.insert(tk.END, "════════════════════════════════════════════════════════════════════════\n\n")

        # 2. Các bước lập luận chi tiết
        if "steps" in res_dict and res_dict["steps"]:
            txt_box.insert(tk.END, ("▶ STEP-BY-STEP DERIVATION & PROOFS:\n" if is_en else "▶ CÁC BƯỚC BIẾN ĐỔI & LẬP LUẬN:\n"))
            for step in res_dict["steps"]:
                formatted_step = self._translate_step_en(step) if is_en else step
                txt_box.insert(tk.END, f"  {formatted_step}\n")
            txt_box.insert(tk.END, "\n")

        # 3. Dạng hiển thị ma trận nếu có
        if "plain_text" in res_dict:
            txt_box.insert(tk.END, ("▶ MATRIX REPRESENTATION:\n" if is_en else "▶ DẠNG BIỂU DIỄN MA TRẬN:\n"))
            txt_box.insert(tk.END, f"{res_dict['plain_text']}\n\n")

        # 4. Mã LaTeX chuẩn
        if "latex" in res_dict:
            txt_box.insert(tk.END, ("▶ LATEX CODE:\n" if is_en else "▶ MÃ LATEX CÔNG THỨC:\n"))
            txt_box.insert(tk.END, f"  {res_dict['latex']}\n\n")

        txt_box.insert(tk.END, "════════════════════════════════════════════════════════════════════════\n")
        self.status_lbl.config(text=("Computation completed." if is_en else "Tính toán hoàn tất."))

    # ==========================================================================
    # TAB 1: ĐẠI SỐ TUYẾN TÍNH & MA TRẬN
    # ==========================================================================
    def _build_tab_linear(self):
        left, right = self._create_split_layout(self.tab_linear)

        # Thanh nạp ví dụ mẫu
        ex_bar = tk.Frame(left, bg="#ECE9D8")
        ex_bar.pack(fill=tk.X, pady=(0, 4))
        tk.Label(ex_bar, text=self._s("Ví dụ:", "Samples:"), font=("Segoe UI", 8, "bold"), bg="#ECE9D8").pack(side=tk.LEFT)

        def _load_ex(kind):
            if kind == "det":
                self.mat_txt.delete("1.0", tk.END)
                self.mat_txt.insert(tk.END, "1  2  3\n0  1  4\n5  6  0")
            elif kind == "system":
                self.mat_txt.delete("1.0", tk.END)
                self.mat_txt.insert(tk.END, "1  1  1\n2  1 -1\n3  2  1")
                self.b_txt.delete("0", tk.END)
                self.b_txt.insert(0, "6; 1; 10")
            elif kind == "sylvester":
                self.mat_txt.delete("1.0", tk.END)
                self.mat_txt.insert(tk.END, "2  0  0\n0  3  0\n0  0  4")
            elif kind == "power":
                self.mat_txt.delete("1.0", tk.END)
                self.mat_txt.insert(tk.END, "1  2  0\n0  2  0\n-2 -2 -1")

        tk.Button(ex_bar, text=self._s("[ 3x3 ]", "[ 3x3 Matrix ]"), font=("Segoe UI", 7), bg="#D4D0C8", relief="raised", bd=1, command=lambda: _load_ex("det")).pack(side=tk.LEFT, padx=2)
        tk.Button(ex_bar, text=self._s("[ Hệ 3 PT ]", "[ 3-Eq System ]"), font=("Segoe UI", 7), bg="#D4D0C8", relief="raised", bd=1, command=lambda: _load_ex("system")).pack(side=tk.LEFT, padx=2)
        tk.Button(ex_bar, text=self._s("[ Toàn phương ]", "[ Quadratic ]"), font=("Segoe UI", 7), bg="#D4D0C8", relief="raised", bd=1, command=lambda: _load_ex("sylvester")).pack(side=tk.LEFT, padx=2)
        tk.Button(ex_bar, text=self._s("[ Lũy thừa Aⁿ ]", "[ Power Aⁿ ]"), font=("Segoe UI", 7), bg="#D4D0C8", relief="raised", bd=1, command=lambda: _load_ex("power")).pack(side=tk.LEFT, padx=2)

        # Nhập ma trận A
        tk.Label(left, text=self._s("Nhập Ma Trận A (từng dòng hoặc cách nhau bởi ';'):", "Matrix A (one row per line, or separated by ';'):"), font=("Segoe UI", 8), bg="#ECE9D8").pack(anchor="w", pady=(4, 2))
        self.mat_txt = tk.Text(left, font=("Consolas", 10), height=7, bg="#FFFFFF", bd=1, relief="sunken")
        self.mat_txt.pack(fill=tk.X, pady=(0, 4))
        self.mat_txt.insert(tk.END, "1  2  3\n0  1  4\n5  6  0")

        # Nhập cột tự do B
        tk.Label(left, text=self._s("Cột tự do B (cho giải hệ Ax = B, phân cách ';'):", "Column B (for Ax = B, separated by ';'):"), font=("Segoe UI", 8), bg="#ECE9D8").pack(anchor="w", pady=(2, 2))
        self.b_txt = tk.Entry(left, font=("Consolas", 9), bg="#FFFFFF", bd=1, relief="sunken")
        self.b_txt.pack(fill=tk.X, pady=(0, 6))

        # Thanh ký hiệu
        self._create_quick_symbol_palette(left, lambda: self.mat_txt)

        # Các nút hành động
        btn_frame = tk.Frame(left, bg="#ECE9D8")
        btn_frame.pack(fill=tk.X, pady=6)

        txt_result, _ = self._create_result_display_box(right)

        def _do_analyze():
            mat_raw = self.mat_txt.get("1.0", tk.END)
            self._run_async(lambda: LinearAlgebraEngine.analyze_matrix(mat_raw), txt_result)

        def _do_solve_system():
            b_val = self.b_txt.get().strip()
            if not b_val:
                messagebox.showwarning("Thiếu cột tự do B", "Vui lòng nhập cột tự do B để giải hệ phương trình.", parent=self.top)
                return
            mat_raw = self.mat_txt.get("1.0", tk.END)
            self._run_async(lambda: LinearAlgebraEngine.solve_linear_system(mat_raw, b_val), txt_result)

        def _do_eigen():
            mat_raw = self.mat_txt.get("1.0", tk.END)
            self._run_async(lambda: LinearAlgebraEngine.eigen_analysis(mat_raw), txt_result)

        def _do_sylvester():
            mat_raw = self.mat_txt.get("1.0", tk.END)
            self._run_async(lambda: LinearAlgebraEngine.analyze_quadratic_form(mat_raw), txt_result)

        tk.Button(btn_frame, text=self._s("⚡ Phân tích ma trận (Det, Rank, Inv)", "⚡ Matrix Analysis (Det, Rank, Inv)"), font=("Segoe UI", 8, "bold"), bg="#D4D0C8", relief="raised", bd=1, command=_do_analyze).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text=self._s("📐 Giải hệ PT Ax = B (Gauss)", "📐 Solve Linear System Ax = B"), font=("Segoe UI", 8, "bold"), bg="#D4D0C8", relief="raised", bd=1, command=_do_solve_system).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text=self._s("✨ Trị riêng & Chéo hóa", "✨ Eigenvalues & Diagonalization"), font=("Segoe UI", 8), bg="#D4D0C8", relief="raised", bd=1, command=_do_eigen).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text=self._s("🎯 Dạng toàn phương & Sylvester", "🎯 Quadratic Form & Sylvester"), font=("Segoe UI", 8), bg="#D4D0C8", relief="raised", bd=1, command=_do_sylvester).pack(fill=tk.X, pady=2)

    # ==========================================================================
    # TAB 2: GIẢI TÍCH 1 & TÍCH PHÂN SUY RỘNG
    # ==========================================================================
    def _build_tab_calculus1(self):
        left, right = self._create_split_layout(self.tab_calculus1)
        txt_result, _ = self._create_result_display_box(right)

        # Thanh nạp ví dụ mẫu
        ex_bar2 = tk.Frame(left, bg="#ECE9D8")
        ex_bar2.pack(fill=tk.X, pady=(0, 4))
        tk.Label(ex_bar2, text=self._s("Ví dụ:", "Samples:"), font=("Segoe UI", 8, "bold"), bg="#ECE9D8").pack(side=tk.LEFT)

        def _load_calc1_ex(kind):
            if kind == "limit0":
                f_entry.delete(0, tk.END)
                f_entry.insert(0, "(exp(x) - 1 - x) / x^2")
                pt_entry.delete(0, tk.END)
                pt_entry.insert(0, "0")
            elif kind == "improper_sample":
                f_entry.delete(0, tk.END)
                f_entry.insert(0, "x^2 * exp(-2*x)")
                a_entry.delete(0, tk.END)
                a_entry.insert(0, "0")
                b_entry.delete(0, tk.END)
                b_entry.insert(0, "oo")

        tk.Button(ex_bar2, text=self._s("[ Giới hạn 0/0 ]", "[ Limit 0/0 ]"), font=("Segoe UI", 7), bg="#D4D0C8", relief="raised", bd=1, command=lambda: _load_calc1_ex("limit0")).pack(side=tk.LEFT, padx=2)
        tk.Button(ex_bar2, text=self._s("[ TP suy rộng ]", "[ Improper Int ]"), font=("Segoe UI", 7), bg="#D4D0C8", relief="raised", bd=1, command=lambda: _load_calc1_ex("improper_sample")).pack(side=tk.LEFT, padx=2)

        # Biểu thức f(x)
        tk.Label(left, text=self._s("Hàm số f(x):", "Function f(x):"), font=("Segoe UI", 8, "bold"), bg="#ECE9D8").pack(anchor="w", pady=(2, 2))
        f_entry = tk.Entry(left, font=("Consolas", 10), bg="#FFFFFF", bd=1, relief="sunken")
        f_entry.pack(fill=tk.X, pady=(0, 4))
        f_entry.insert(0, "(exp(x) - 1 - x) / x^2")

        # Biến và cận
        row1 = tk.Frame(left, bg="#ECE9D8")
        row1.pack(fill=tk.X, pady=2)
        tk.Label(row1, text=self._s("Biến:", "Var:"), font=("Segoe UI", 8), bg="#ECE9D8", width=6).pack(side=tk.LEFT)
        var_entry = tk.Entry(row1, font=("Consolas", 9), width=6)
        var_entry.pack(side=tk.LEFT)
        var_entry.insert(0, "x")

        tk.Label(row1, text=self._s("Điểm x₀:", "Point x₀:"), font=("Segoe UI", 8), bg="#ECE9D8", width=10).pack(side=tk.LEFT, padx=(8, 0))
        pt_entry = tk.Entry(row1, font=("Consolas", 9), width=8)
        pt_entry.pack(side=tk.LEFT)
        pt_entry.insert(0, "0")

        # Cận tích phân
        row2 = tk.Frame(left, bg="#ECE9D8")
        row2.pack(fill=tk.X, pady=2)
        tk.Label(row2, text=self._s("Cận dưới a:", "Lower a:"), font=("Segoe UI", 8), bg="#ECE9D8", width=10).pack(side=tk.LEFT)
        a_entry = tk.Entry(row2, font=("Consolas", 9), width=8)
        a_entry.pack(side=tk.LEFT)
        a_entry.insert(0, "0")

        tk.Label(row2, text=self._s("Cận trên b:", "Upper b:"), font=("Segoe UI", 8), bg="#ECE9D8", width=10).pack(side=tk.LEFT, padx=(8, 0))
        b_entry = tk.Entry(row2, font=("Consolas", 9), width=8)
        b_entry.pack(side=tk.LEFT)
        b_entry.insert(0, "oo")

        self._create_quick_symbol_palette(left, lambda: f_entry)

        # Nút tính toán
        btn_frame = tk.Frame(left, bg="#ECE9D8")
        btn_frame.pack(fill=tk.X, pady=6)

        def _do_limit():
            f_val, var_val, pt_val = f_entry.get(), var_entry.get(), pt_entry.get()
            self._run_async(lambda: AdvancedCalculusEngine.compute_advanced_limit(f_val, var_val, pt_val), txt_result)

        def _do_taylor():
            f_val, var_val, pt_val = f_entry.get(), var_entry.get(), pt_entry.get()
            self._run_async(lambda: AdvancedCalculusEngine.compute_taylor_series(f_val, var_val, pt_val, order=5), txt_result)

        def _do_improper():
            f_val, var_val, a_val, b_val = f_entry.get(), var_entry.get(), a_entry.get(), b_entry.get()
            self._run_async(lambda: AdvancedCalculusEngine.compute_improper_integral(f_val, var_val, a_val, b_val), txt_result)

        tk.Button(btn_frame, text=self._s("⚡ Giới hạn vô định (L'Hôpital / Taylor)", "⚡ Limit Evaluation (L'Hôpital / Taylor)"), font=("Segoe UI", 8, "bold"), bg="#D4D0C8", relief="raised", bd=1, command=_do_limit).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text=self._s("📈 Khai triển Taylor / Maclaurin", "📈 Taylor / Maclaurin Expansion"), font=("Segoe UI", 8), bg="#D4D0C8", relief="raised", bd=1, command=_do_taylor).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text=self._s("∫ Tích phân suy rộng (Hội tụ & Tính I)", "∫ Improper Integral Analysis"), font=("Segoe UI", 8, "bold"), bg="#D4D0C8", relief="raised", bd=1, command=_do_improper).pack(fill=tk.X, pady=2)

    # ==========================================================================
    # TAB 3: CHUỖI SỐ & FOURIER
    # ==========================================================================
    def _build_tab_series(self):
        left, right = self._create_split_layout(self.tab_series)
        txt_result, _ = self._create_result_display_box(right)

        tk.Label(left, text=self._s("Số hạng tổng quát a_n (hoặc hàm f(x)):", "General term a_n (or function f(x)):"), font=("Segoe UI", 8, "bold"), bg="#ECE9D8").pack(anchor="w", pady=(2, 2))
        expr_entry = tk.Entry(left, font=("Consolas", 10), bg="#FFFFFF", bd=1, relief="sunken")
        expr_entry.pack(fill=tk.X, pady=(0, 4))
        expr_entry.insert(0, "n / 2^n")

        row = tk.Frame(left, bg="#ECE9D8")
        row.pack(fill=tk.X, pady=2)
        tk.Label(row, text=self._s("Biến n/x:", "Variable:"), font=("Segoe UI", 8), bg="#ECE9D8", width=10).pack(side=tk.LEFT)
        var_entry = tk.Entry(row, font=("Consolas", 9), width=8)
        var_entry.pack(side=tk.LEFT)
        var_entry.insert(0, "n")

        tk.Label(row, text=self._s("Chu kỳ L:", "Period L:"), font=("Segoe UI", 8), bg="#ECE9D8", width=14).pack(side=tk.LEFT, padx=(6, 0))
        L_entry = tk.Entry(row, font=("Consolas", 9), width=8)
        L_entry.pack(side=tk.LEFT)
        L_entry.insert(0, "pi")

        self._create_quick_symbol_palette(left, lambda: expr_entry)

        btn_frame = tk.Frame(left, bg="#ECE9D8")
        btn_frame.pack(fill=tk.X, pady=6)

        def _do_series_test():
            e_val, v_val = expr_entry.get(), var_entry.get()
            self._run_async(lambda: SeriesEngine.test_series_convergence(e_val, v_val), txt_result)

        def _do_power_radius():
            e_val, v_val = expr_entry.get(), var_entry.get()
            self._run_async(lambda: SeriesEngine.compute_power_series_radius(e_val, v_val, "0"), txt_result)

        def _do_fourier():
            e_val, L_val = expr_entry.get(), L_entry.get()
            self._run_async(lambda: SeriesEngine.compute_fourier_series(e_val, "x", L_val, terms=3), txt_result)

        tk.Button(btn_frame, text=self._s("⚡ Khảo sát hội tụ chuỗi số", "⚡ Series Convergence Test"), font=("Segoe UI", 8, "bold"), bg="#D4D0C8", relief="raised", bd=1, command=_do_series_test).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text=self._s("⭕ Bán kính & Khoảng hội tụ", "⭕ Convergence Radius & Interval"), font=("Segoe UI", 8), bg="#D4D0C8", relief="raised", bd=1, command=_do_power_radius).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text=self._s("🌊 Khai triển chuỗi Fourier", "🌊 Fourier Series Expansion"), font=("Segoe UI", 8, "bold"), bg="#D4D0C8", relief="raised", bd=1, command=_do_fourier).pack(fill=tk.X, pady=2)

    # ==========================================================================
    # TAB 4: GIẢI TÍCH ĐA BIẾN & TÍCH PHÂN BỘI
    # ==========================================================================
    def _build_tab_multivar(self):
        left, right = self._create_split_layout(self.tab_multivar)
        txt_result, _ = self._create_result_display_box(right)

        # Thanh nạp ví dụ mẫu
        ex_bar4 = tk.Frame(left, bg="#ECE9D8")
        ex_bar4.pack(fill=tk.X, pady=(0, 4))
        tk.Label(ex_bar4, text=self._s("Ví dụ:", "Samples:"), font=("Segoe UI", 8, "bold"), bg="#ECE9D8").pack(side=tk.LEFT)

        def _load_multi_ex(kind):
            if kind == "extrema":
                f_entry.delete(0, tk.END)
                f_entry.insert(0, "x^3 + y^3 - 3*x*y")
            elif kind == "lagrange_sample":
                f_entry.delete(0, tk.END)
                f_entry.insert(0, "x*y*z")
                g_entry.delete(0, tk.END)
                g_entry.insert(0, "x + y + z = 3")

        tk.Button(ex_bar4, text=self._s("[ Tự do ]", "[ Free Extrema ]"), font=("Segoe UI", 7), bg="#D4D0C8", relief="raised", bd=1, command=lambda: _load_multi_ex("extrema")).pack(side=tk.LEFT, padx=2)
        tk.Button(ex_bar4, text=self._s("[ Lagrange ]", "[ Lagrange ]"), font=("Segoe UI", 7), bg="#D4D0C8", relief="raised", bd=1, command=lambda: _load_multi_ex("lagrange_sample")).pack(side=tk.LEFT, padx=2)

        tk.Label(left, text=self._s("Hàm số z = f(x, y):", "Function z = f(x, y):"), font=("Segoe UI", 8, "bold"), bg="#ECE9D8").pack(anchor="w", pady=(2, 2))
        f_entry = tk.Entry(left, font=("Consolas", 10), bg="#FFFFFF", bd=1, relief="sunken")
        f_entry.pack(fill=tk.X, pady=(0, 4))
        f_entry.insert(0, "x^3 + y^3 - 3*x*y")

        tk.Label(left, text=self._s("Ràng buộc g(x, y) = 0 (cho Lagrange):", "Constraint g(x, y) = 0 (for Lagrange):"), font=("Segoe UI", 8), bg="#ECE9D8").pack(anchor="w", pady=(2, 2))
        g_entry = tk.Entry(left, font=("Consolas", 9), bg="#FFFFFF", bd=1, relief="sunken")
        g_entry.pack(fill=tk.X, pady=(0, 4))
        g_entry.insert(0, "x^2 + y^2 = 5")

        self._create_quick_symbol_palette(left, lambda: f_entry)

        btn_frame = tk.Frame(left, bg="#ECE9D8")
        btn_frame.pack(fill=tk.X, pady=6)

        def _do_partial():
            f_val = f_entry.get()
            self._run_async(lambda: MultivariableEngine.compute_partial_derivatives(f_val, "x, y"), txt_result)

        def _do_extrema():
            f_val = f_entry.get()
            self._run_async(lambda: MultivariableEngine.find_local_extrema_2vars(f_val, "x, y"), txt_result)

        def _do_lagrange():
            f_val, g_val = f_entry.get(), g_entry.get()
            self._run_async(lambda: MultivariableEngine.solve_lagrange_multipliers(f_val, g_val, "x, y"), txt_result)

        def _do_double_int():
            self._run_async(lambda: MultivariableEngine.compute_double_integral("x*y", "y", "0", "x", "x", "0", "1"), txt_result)

        tk.Button(btn_frame, text=self._s("⚡ Đạo hàm riêng & Hessian", "⚡ Partial Derivatives & Hessian"), font=("Segoe UI", 8, "bold"), bg="#D4D0C8", relief="raised", bd=1, command=_do_partial).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text=self._s("🎯 Tìm cực trị tự do", "🎯 Find Free Extrema"), font=("Segoe UI", 8, "bold"), bg="#D4D0C8", relief="raised", bd=1, command=_do_extrema).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text=self._s("🔗 Cực trị Lagrange", "🔗 Lagrange Multipliers"), font=("Segoe UI", 8), bg="#D4D0C8", relief="raised", bd=1, command=_do_lagrange).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text=self._s("∬ Tích phân kép lặp", "∬ Iterated Double Integral"), font=("Segoe UI", 8), bg="#D4D0C8", relief="raised", bd=1, command=_do_double_int).pack(fill=tk.X, pady=2)

    # ==========================================================================
    # TAB 5: TRƯỜNG VECTOR & ĐƯỜNG MẶT
    # ==========================================================================
    def _build_tab_field(self):
        left, right = self._create_split_layout(self.tab_field)
        txt_result, _ = self._create_result_display_box(right)

        tk.Label(left, text=self._s("Thành phần P(x, y, z):", "Component P(x, y, z):"), font=("Segoe UI", 8), bg="#ECE9D8").pack(anchor="w")
        p_entry = tk.Entry(left, font=("Consolas", 9), bg="#FFFFFF", bd=1, relief="sunken")
        p_entry.pack(fill=tk.X, pady=(0, 2))
        p_entry.insert(0, "2*x*y + z")

        tk.Label(left, text=self._s("Thành phần Q(x, y, z):", "Component Q(x, y, z):"), font=("Segoe UI", 8), bg="#ECE9D8").pack(anchor="w")
        q_entry = tk.Entry(left, font=("Consolas", 9), bg="#FFFFFF", bd=1, relief="sunken")
        q_entry.pack(fill=tk.X, pady=(0, 2))
        q_entry.insert(0, "x^2")

        tk.Label(left, text=self._s("Thành phần R(x, y, z):", "Component R(x, y, z):"), font=("Segoe UI", 8), bg="#ECE9D8").pack(anchor="w")
        r_entry = tk.Entry(left, font=("Consolas", 9), bg="#FFFFFF", bd=1, relief="sunken")
        r_entry.pack(fill=tk.X, pady=(0, 4))
        r_entry.insert(0, "x")

        self._create_quick_symbol_palette(left, lambda: p_entry)

        btn_frame = tk.Frame(left, bg="#ECE9D8")
        btn_frame.pack(fill=tk.X, pady=6)

        def _do_field_analysis():
            p_val, q_val, r_val = p_entry.get(), q_entry.get(), r_entry.get()
            self._run_async(lambda: FieldTheoryEngine.analyze_vector_field(p_val, q_val, r_val), txt_result)

        tk.Button(btn_frame, text=self._s("⚡ Tính Div, Rot & Tìm thế vị U", "⚡ Compute Div, Rot & Potential U"), font=("Segoe UI", 8, "bold"), bg="#D4D0C8", relief="raised", bd=1, command=_do_field_analysis).pack(fill=tk.X, pady=2)

    # ==========================================================================
    # TAB 6: PHƯƠNG TRÌNH VI PHÂN & BIẾN ĐỔI LAPLACE
    # ==========================================================================
    def _build_tab_ode(self):
        left, right = self._create_split_layout(self.tab_ode)
        txt_result, _ = self._create_result_display_box(right)

        # Thanh nạp ví dụ mẫu
        ex_bar = tk.Frame(left, bg="#ECE9D8")
        ex_bar.pack(fill=tk.X, pady=(0, 4))
        tk.Label(ex_bar, text=self._s("Ví dụ:", "Samples:"), font=("Segoe UI", 8, "bold"), bg="#ECE9D8").pack(side=tk.LEFT)

        def _load_ode_ex(kind):
            if kind == "cauchy_laplace":
                ode_entry.delete(0, tk.END)
                ode_entry.insert(0, "y'' - 3*y' + 2*y = exp(3*t)")
                y0_entry.delete(0, tk.END)
                y0_entry.insert(0, "1")
                yp0_entry.delete(0, tk.END)
                yp0_entry.insert(0, "0")
                laplace_entry.delete(0, tk.END)
                laplace_entry.insert(0, "1 / ((s-1)*(s-2)*(s-3))")
            elif kind == "harmonic":
                ode_entry.delete(0, tk.END)
                ode_entry.insert(0, "y'' + 4*y = sin(2*x)")
                y0_entry.delete(0, tk.END)
                y0_entry.insert(0, "0")
                yp0_entry.delete(0, tk.END)
                yp0_entry.insert(0, "1")
            elif kind == "ode2_const":
                ode_entry.delete(0, tk.END)
                ode_entry.insert(0, "y'' - 5*y' + 6*y = 0")
                y0_entry.delete(0, tk.END)
                y0_entry.insert(0, "2")
                yp0_entry.delete(0, tk.END)
                yp0_entry.insert(0, "5")
            elif kind == "pde_sample":
                ode_entry.delete(0, tk.END)
                ode_entry.insert(0, "u_t = a^2 * u_xx")
                laplace_entry.delete(0, tk.END)
                laplace_entry.insert(0, "u(x,t) = exp(-a^2*t)*sin(x) - 2*exp(-9*a^2*t)*sin(3*x)")

        tk.Button(ex_bar, text=self._s("[ Cauchy ]", "[ Cauchy ]"), font=("Segoe UI", 7), bg="#D4D0C8", relief="raised", bd=1, command=lambda: _load_ode_ex("cauchy_laplace")).pack(side=tk.LEFT, padx=2)
        tk.Button(ex_bar, text=self._s("[ Dao động ]", "[ Resonance ]"), font=("Segoe UI", 7), bg="#D4D0C8", relief="raised", bd=1, command=lambda: _load_ode_ex("harmonic")).pack(side=tk.LEFT, padx=2)
        tk.Button(ex_bar, text=self._s("[ Cấp 2 ]", "[ Second-Order ]"), font=("Segoe UI", 7), bg="#D4D0C8", relief="raised", bd=1, command=lambda: _load_ode_ex("ode2_const")).pack(side=tk.LEFT, padx=2)
        tk.Button(ex_bar, text=self._s("[ Truyền nhiệt ]", "[ Heat Eq ]"), font=("Segoe UI", 7), bg="#D4D0C8", relief="raised", bd=1, command=lambda: _load_ode_ex("pde_sample")).pack(side=tk.LEFT, padx=2)

        tk.Label(left, text=self._s("Phương trình vi phân (vd: y'' - 5*y' + 6*y = 0):", "Differential Equation (e.g. y'' - 5*y' + 6*y = 0):"), font=("Segoe UI", 8, "bold"), bg="#ECE9D8").pack(anchor="w", pady=(2, 2))
        ode_entry = tk.Entry(left, font=("Consolas", 10), bg="#FFFFFF", bd=1, relief="sunken")
        ode_entry.pack(fill=tk.X, pady=(0, 4))
        ode_entry.insert(0, "y'' - 5*y' + 6*y = 0")

        row = tk.Frame(left, bg="#ECE9D8")
        row.pack(fill=tk.X, pady=2)
        tk.Label(row, text=self._s("Điều kiện y(0):", "Initial y(0):"), font=("Segoe UI", 8), bg="#ECE9D8", width=12).pack(side=tk.LEFT)
        y0_entry = tk.Entry(row, font=("Consolas", 9), width=6)
        y0_entry.pack(side=tk.LEFT)
        y0_entry.insert(0, "2")

        tk.Label(row, text="y'(0):", font=("Segoe UI", 8), bg="#ECE9D8", width=8).pack(side=tk.LEFT, padx=(6, 0))
        yp0_entry = tk.Entry(row, font=("Consolas", 9), width=6)
        yp0_entry.pack(side=tk.LEFT)
        yp0_entry.insert(0, "5")

        tk.Label(left, text=self._s("Hàm f(t) hoặc F(s) (cho Laplace):", "Function f(t) or F(s) (for Laplace):"), font=("Segoe UI", 8), bg="#ECE9D8").pack(anchor="w", pady=(4, 2))
        laplace_entry = tk.Entry(left, font=("Consolas", 9), bg="#FFFFFF", bd=1, relief="sunken")
        laplace_entry.pack(fill=tk.X, pady=(0, 4))
        laplace_entry.insert(0, "exp(3*t)*sin(2*t)")

        self._create_quick_symbol_palette(left, lambda: ode_entry)

        btn_frame = tk.Frame(left, bg="#ECE9D8")
        btn_frame.pack(fill=tk.X, pady=6)

        def _do_solve_ode():
            ics = {}
            if y0_entry.get().strip():
                ics["y(0)"] = y0_entry.get().strip()
            if yp0_entry.get().strip():
                ics["y'(0)"] = yp0_entry.get().strip()
            ode_val = ode_entry.get()
            self._run_async(lambda: DifferentialEquationsEngine.solve_ode(ode_val, "y", "x", ics_dict=ics if ics else None), txt_result)

        def _do_laplace_fwd():
            lp_val = laplace_entry.get()
            self._run_async(lambda: DifferentialEquationsEngine.compute_laplace(lp_val, "t", "s", mode="forward"), txt_result)

        def _do_laplace_inv():
            lp_val = laplace_entry.get()
            self._run_async(lambda: DifferentialEquationsEngine.compute_laplace(lp_val, "t", "s", mode="inverse"), txt_result)

        tk.Button(btn_frame, text=self._s("⚡ Giải phương trình vi phân", "⚡ Solve Differential Equation"), font=("Segoe UI", 8, "bold"), bg="#D4D0C8", relief="raised", bd=1, command=_do_solve_ode).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text=self._s("📈 Biến đổi Laplace thuận", "📈 Forward Laplace Transform"), font=("Segoe UI", 8), bg="#D4D0C8", relief="raised", bd=1, command=_do_laplace_fwd).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text=self._s("📉 Biến đổi Laplace ngược", "📉 Inverse Laplace Transform"), font=("Segoe UI", 8, "bold"), bg="#D4D0C8", relief="raised", bd=1, command=_do_laplace_inv).pack(fill=tk.X, pady=2)


def show_higher_math_dialog(parent: tk.Widget, initial_topic_idx: int = 0, lang: str = "vi") -> HigherMathDialog:
    """Hàm khởi động hộp thoại Toán Cao Cấp từ menu bên ngoài."""
    return HigherMathDialog(parent, initial_topic_idx, lang=lang)


if __name__ == "__main__":
    # Test độc lập giao diện
    root = tk.Tk()
    root.title("Test HigherMathDialog")
    root.geometry("200x100")
    btn = tk.Button(root, text="Mở Hộp Thoại Toán Cao Cấp", command=lambda: show_higher_math_dialog(root))
    btn.pack(expand=True)
    root.mainloop()
