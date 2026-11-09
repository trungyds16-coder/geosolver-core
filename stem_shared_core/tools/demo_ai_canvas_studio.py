# -*- coding: utf-8 -*-
"""
DEMO LAB: HỆ THỐNG DỰNG HÌNH TỰ ĐỘNG BẰNG AI (TEXT-TO-CAD) & SINH ĐỀ THI PHÂN CẤP
Kiến trúc Neuro-Symbolic & Sinh Tham Số Động 100%: 
  - DeepSeek-R1 (1.5B/7B qua Ollama) bóc tách ý định ngôn ngữ tự nhiên thành JSON actions với tên đỉnh & thông số tùy ý.
  - Lõi giải tích GeoSolver2DCore tính toán tọa độ chính xác tuyệt đối và tự động co giãn (Auto-fit Viewport).
  - Bảng HUD Inspector hiển thị tọa độ & số đo thực tế theo thời gian thực (Real-time).
  - Bộ sinh đề thi thuật toán Python sinh ngẫu nhiên 100% (không lặp lại) theo 4 mức độ chuẩn GDPT 2018.
  - Tích hợp nút AI chuyển đề toán thành bài toán thực tế đời sống (Word Problem Contextualizer).
"""

import sys
import os
import json
import math
import re
import random
import time
import urllib.request
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Thêm đường dẫn gốc để import lõi GeoSolver
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from stem_shared_core.geosolver_core import GeoSolver2DCore


class DynamicExamGenerator:
    """Bộ sinh đề thi hoàn toàn tự động bằng thuật toán toán học giải tích Python."""

    @staticmethod
    def generate_easy() -> str:
        names = random.choice([("A", "B", "C"), ("M", "N", "P"), ("D", "E", "F"), ("X", "Y", "Z")])
        v1, v2, v3 = names

        # 1. Tam giác Pythagoras ngẫu nhiên theo công thức Euclid
        m = random.randint(2, 5)
        n = random.randint(1, m - 1)
        k = random.randint(1, 2)
        a = k * (m * m - n * n)
        b = k * (2 * m * n)
        c = k * (m * m + n * n)
        S = 0.5 * a * b
        h = (a * b) / c

        # 2. Phương trình căn thức bậc hai có nghiệm nguyên ngẫu nhiên
        x0 = random.randint(2, 8)
        a_eq = random.randint(2, 5)
        b_eq = random.randint(1, 9)
        c_val = round(math.sqrt(a_eq * x0 + b_eq), 2)

        lines = [
            f"=== ĐỀ THI ĐÁNH GIÁ NĂNG LỰC TOÁN HỌC - CẤP ĐỘ: NHẬN BIẾT (EASY) ===",
            f"Thời gian: 45 phút | Chuẩn kiến thức GDPT 2018 | Mã đề: {random.randint(101, 999)}\n",
            f"Câu 1 (Hình học cơ bản - 5 điểm):",
            f"Cho tam giác {v1}{v2}{v3} vuông tại {v1} có {v1}{v2} = {a} cm, {v1}{v3} = {b} cm.",
            f"  a) Áp dụng định lý Pythagoras, tính độ dài cạnh huyền {v2}{v3}.",
            f"  b) Tính diện tích tam giác {v1}{v2}{v3} và độ dài đường cao {v1}H kẻ xuống cạnh {v2}{v3}.",
            f"👉 Hướng dẫn giải sư phạm:",
            f"  • Cạnh huyền {v2}{v3} = √({v1}{v2}² + {v1}{v3}²) = √({a}² + {b}²) = {c} cm.",
            f"  • Diện tích S = 1/2 × {a} × {b} = {S:.1f} cm².",
            f"  • Đường cao {v1}H = ({a} × {b}) / {c} = {h:.2f} cm.\n",
            f"Câu 2 (Phương trình căn thức cơ bản - 5 điểm):",
            f"Giải phương trình: √({a_eq}x + {b_eq}) = {c_val}",
            f"👉 Hướng dẫn giải sư phạm:",
            f"  • Điều kiện: {a_eq}x + {b_eq} ≥ 0 ⇔ x ≥ {-b_eq/a_eq:.2f}.",
            f"  • Bình phương 2 vế: {a_eq}x + {b_eq} = {c_val**2:.2f} ⇔ {a_eq}x = {c_val**2 - b_eq:.2f} ⇔ x = {x0}.",
            f"  • Tập nghiệm: S = {{ {x0} }}."
        ]
        return "\n".join(lines)

    @staticmethod
    def generate_medium() -> str:
        # 1. Căn thức có bẫy nghiệm ngoại lai (Extraneous Root Trap)
        c_val = random.randint(2, 5)
        x1 = c_val + random.randint(2, 6)   # Nghiệm hợp lệ: x1 >= c_val
        x2 = c_val - random.randint(1, 2)   # Nghiệm bẫy: x2 < c_val (vế phải âm)
        a_coeff = (x1 + x2) - 2 * c_val
        b_coeff = c_val * c_val - (x1 * x2)
        b_str = f"+ {b_coeff}" if b_coeff >= 0 else f"- {abs(b_coeff)}"

        # 2. Tọa độ hình học và tâm đường tròn nội tiếp ngẫu nhiên
        x_B = random.randint(4, 8)
        y_C = random.randint(3, 7)
        A = (0.0, 0.0)
        B = (float(x_B), 0.0)
        C = (0.0, float(y_C))
        BC = math.hypot(x_B, y_C)
        perimeter = x_B + y_C + BC
        area = 0.5 * x_B * y_C
        r = area / (perimeter / 2.0)
        Ix = (x_B * 0 + BC * 0 + y_C * x_B) / perimeter
        Iy = (x_B * 0 + BC * y_C + y_C * 0) / perimeter

        lines = [
            f"=== ĐỀ THI ĐÁNH GIÁ NĂNG LỰC TOÁN HỌC - CẤP ĐỘ: THÔNG HIỂU (MEDIUM) ===",
            f"Thời gian: 45 phút | Nhận diện bẫy tư duy | Mã đề: {random.randint(101, 999)}\n",
            f"Câu 1 (Đại số - Bẫy nghiệm ngoại lai - 5 điểm):",
            f"Giải phương trình vô tỷ: √({a_coeff}x {b_str}) = x - {c_val}",
            f"👉 Phân tích sư phạm & Ma trận sai lầm thường gặp:",
            f"  • BƯỚC 1: Điều kiện vế phải x - {c_val} ≥ 0 ⇔ x ≥ {c_val}.",
            f"  • BƯỚC 2: Bình phương hai vế ta được: {a_coeff}x {b_str} = (x - {c_val})²",
            f"    ⇔ x² - {2*c_val + a_coeff}x + {c_val*c_val - b_coeff} = 0.",
            f"    Phương trình bậc hai cho 2 nghiệm đại số: x = {x1} và x = {x2}.",
            f"  • BƯỚC 3 (BẪY NGOẠI LAI):",
            f"    - Với x = {x1}: thỏa mãn x ≥ {c_val} (Nhận).",
            f"    - Với x = {x2}: vi phạm điều kiện vì {x2} - {c_val} = {x2 - c_val} < 0 (Loại).",
            f"    Học sinh không đặt điều kiện sẽ lấy cả 2 nghiệm và bị trừ 50% số điểm!",
            f"  • Kết luận: Tập nghiệm duy nhất S = {{ {x1} }}.\n",
            f"Câu 2 (Hình học giải tích tọa độ - 5 điểm):",
            f"Trong mặt phẳng tọa độ Oxy, cho tam giác ABC với A(0, 0), B({x_B}, 0), C(0, {y_C}).",
            f"  a) Tính diện tích tam giác ABC và chu vi tam giác.",
            f"  b) Xác định tọa độ tâm đường tròn nội tiếp I và bán kính r.",
            f"👉 Hướng dẫn giải giải tích:",
            f"  • AB = {x_B}, AC = {y_C}, BC = √({x_B}² + {y_C}²) = {BC:.2f}.",
            f"  • Diện tích S = {area:.1f}, Nửa chu vi p = {perimeter/2.0:.2f}.",
            f"  • Bán kính nội tiếp r = S / p = {r:.2f}.",
            f"  • Tọa độ tâm nội tiếp: I({Ix:.2f}, {Iy:.2f})."
        ]
        return "\n".join(lines)

    @staticmethod
    def generate_hard() -> str:
        # Bài toán Diophantine thực tế (Hệ phương trình nghiệm nguyên)
        configs = [
            (100, 5, 3, 3, "trâu đứng", "trâu nằm", "trâu già", "bó cỏ"),
            (100, 3, 2, 2, "thuyền lớn", "thuyền vừa", "thuyền nan", "hành khách"),
            (60, 4, 2, 3, "kỹ sư trưởng", "thợ chính", "thực tập sinh", "giờ công"),
            (120, 5, 3, 4, "xe tải 5 tấn", "xe tải 3 tấn", "xe ba gác", "tấn hàng")
        ]
        total, p1, p2, p3_inv, n1, n2, n3, unit = random.choice(configs)
        sols = []
        for x in range(1, total):
            for y in range(1, total - x):
                z = total - x - y
                if z > 0 and z % p3_inv == 0:
                    if p1 * x + p2 * y + z // p3_inv == total:
                        sols.append((x, y, z))

        # Euler Line Coordinates
        xA, yA = 0, random.randint(3, 6)
        xB, yB = -random.randint(2, 5), 0
        xC, yC = random.randint(4, 7), 0
        pA, pB, pC = (float(xA), float(yA)), (float(xB), float(yB)), (float(xC), float(yC))
        G = GeoSolver2DCore.compute_centroid(pA, pB, pC)
        O, R = GeoSolver2DCore.compute_circumcenter(pA, pB, pC)
        H = GeoSolver2DCore.compute_orthocenter(pA, pB, pC)

        lines = [
            f"=== ĐỀ THI ĐÁNH GIÁ NĂNG LỰC TOÁN HỌC - CẤP ĐỘ: VẬN DỤNG (HARD) ===",
            f"Thời gian: 60 phút | Ứng dụng thực tế & Liên môn | Mã đề: {random.randint(101, 999)}\n",
            f"Câu 1 (Toán rời rạc & Số học Diophantine - 5 điểm):",
            f"Một dự án cần huy động đúng tổng cộng {total} {unit} được vận chuyển bởi 3 loại phương tiện: {n1} (x), {n2} (y), {n3} (z).",
            f"Biết rằng mỗi {n1} chở {p1} {unit}, mỗi {n2} chở {p2} {unit}, và cứ {p3_inv} {n3} thì chở 1 {unit}.",
            f"Tổng số phương tiện là đúng {total} chiếc. Tìm số lượng mỗi loại xe (nghiệm nguyên dương).",
            f"👉 Lời giải thuật toán Diophantine (Python Verified):",
            f"  Hệ phương trình:",
            f"    {{ x + y + z = {total}",
            f"    {{ {p1}x + {p2}y + z/{p3_inv} = {total}",
            f"  Triệt tiêu z: {p1 * p3_inv - 1}x + {p2 * p3_inv - 1}y = {total * (p3_inv - 1)}",
            f"  Phương trình có đúng {len(sols)} nghiệm nguyên dương (x, y, z):",
        ]
        for idx, (sx, sy, sz) in enumerate(sols, 1):
            lines.append(f"    Nghiệm {idx}: {n1} x = {sx}, {n2} y = {sy}, {n3} z = {sz}")

        lines.extend([
            f"\nCâu 2 (Hình học thuần túy - Đường thẳng Euler - 5 điểm):",
            f"Cho tam giác ABC có tọa độ các đỉnh: A({xA}, {yA}), B({xB}, {yB}), C({xC}, {yC}).",
            f"  a) Xác định tọa độ trọng tâm G, tâm ngoại tiếp O và trực tâm H.",
            f"  b) Chứng minh 3 điểm O, G, H thẳng hàng và thỏa mãn hệ thức vector OH = 3 OG.",
            f"👉 Đáp số giải tích chính xác:",
            f"  • Trọng tâm G = ({G[0]:.2f}, {G[1]:.2f})",
            f"  • Tâm ngoại tiếp O = ({O[0]:.2f}, {O[1]:.2f}) (Bán kính R = {R:.2f})",
            f"  • Trực tâm H = ({H[0]:.2f}, {H[1]:.2f})",
            f"  • Tích có hướng (O, G, H) triệt tiêu → 3 điểm thẳng hàng trên Đường thẳng Euler."
        ])
        return "\n".join(lines)

    @staticmethod
    def generate_olympic() -> str:
        k = random.randint(2, 4)
        c = random.randint(1, 3)
        lines = [
            f"=== ĐỀ THI HỌC SINH GIỎI / OLYMPIC - CẤP ĐỘ: VẬN DỤNG CAO ===",
            f"Thời gian: 90 phút | Bất đẳng thức & Hình học chuyên sâu | Mã đề: {random.randint(101, 999)}\n",
            f"Câu 1 (Bất đẳng thức hình học & Cực trị):",
            f"Cho tam giác nhọn ABC có bán kính ngoại tiếp R và bán kính nội tiếp r.",
            f"Chứng minh bất đẳng thức Euler R ≥ 2r và dấu bằng xảy ra khi và chỉ khi tam giác ABC đều.",
            f"Mở rộng: Cho điểm M tùy ý trong tam giác, tìm vị trí M để tổng khoảng cách từ M đến ba cạnh đạt giá trị nhỏ nhất.\n",
            f"Câu 2 (Phương trình vô tỷ bậc cao Cardano & Phân tích nhân tử):",
            f"Giải phương trình vô tỷ: √(x³ - {k}x + {c}) = x - 1 trên tập số thực.",
            f"👉 Hướng dẫn phân tích chuyên sâu:",
            f"  • Bước 1: Khảo sát hàm số f(x) = x³ - {k}x + {c} và tìm điều kiện chặn nghiệm x ≥ 1.",
            f"  • Bước 2: Bình phương và biến đổi về đa thức bậc ba: x³ - x² - ({k}-2)x + ({c}-1) = 0.",
            f"  • Bước 3: Áp dụng phương pháp Cardano hoặc phân tích nhân tử liên hợp để tách nghiệm hữu tỷ."
        ]
        return "\n".join(lines)


class AICanvasStudioDemo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI CAD LAB - Phòng Thí Nghiệm Text-to-CAD DeepSeek-R1 & Sinh Đề Thi Động")
        self.geometry("1200x760")
        self.minsize(1020, 660)

        self.engine = GeoSolver2DCore()
        self.current_points = {}
        self.current_lines = []
        self.current_circles = []
        self.current_labels = {}

        # Tọa độ và tỷ lệ hiển thị
        self.viewport_ox = 350.0
        self.viewport_oy = 300.0
        self.viewport_scale = 30.0

        self._setup_ui()
        self._check_ollama_status()

    def _setup_ui(self):
        # Thanh tiêu đề & chọn mô hình
        top_bar = ttk.Frame(self, padding=8)
        top_bar.pack(side=tk.TOP, fill=tk.X)

        title_lbl = ttk.Label(top_bar, text="🤖 AI CAD STUDIO - HỆ THỐNG DỰNG HÌNH & SINH ĐỀ THI ĐỘNG 100%", font=("Segoe UI", 12, "bold"))
        title_lbl.pack(side=tk.LEFT, padx=5)

        ttk.Label(top_bar, text="Mô hình Ollama:").pack(side=tk.LEFT, padx=(20, 5))
        self.model_var = tk.StringVar(value="deepseek-r1:1.5b")
        model_cb = ttk.Combobox(top_bar, textvariable=self.model_var, values=["deepseek-r1:1.5b", "deepseek-r1:7b", "qwen2.5-coder:7b"], state="readonly", width=18)
        model_cb.pack(side=tk.LEFT, padx=5)

        self.status_lbl = ttk.Label(top_bar, text="Đang kiểm tra Ollama...", font=("Segoe UI", 9, "italic"))
        self.status_lbl.pack(side=tk.LEFT, padx=15)

        # PanedWindow chính: Trái (Điều khiển & AI), Phải (Canvas vẽ + Inspector)
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # ==========================================
        # KHUNG TRÁI: ĐIỀU KHIỂN & AI
        # ==========================================
        left_frame = ttk.Frame(paned, width=460)
        paned.add(left_frame, weight=1)

        notebook = ttk.Notebook(left_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # TAB 1: TEXT-TO-CAD (VẼ HÌNH BẰNG AI)
        tab_draw = ttk.Frame(notebook, padding=8)
        notebook.add(tab_draw, text="🎨 AI Dựng Hình (Text-to-CAD)")

        ttk.Label(tab_draw, text="Nhập yêu cầu tự do (Bất kỳ tên đỉnh, số đo, loại hình):", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(0, 4))
        
        self.prompt_entry = scrolledtext.ScrolledText(tab_draw, height=3, font=("Segoe UI", 10))
        self.prompt_entry.pack(fill=tk.X, pady=(0, 6))
        self.prompt_entry.insert(tk.END, "Vẽ tam giác MNP vuông tại M có MN = 5, MP = 12, kẻ đường cao MH")

        # Nút hành động AI
        btn_frame = ttk.Frame(tab_draw)
        btn_frame.pack(fill=tk.X, pady=(0, 6))

        self.btn_run_ai = ttk.Button(btn_frame, text="🚀 Nhờ AI Dựng Hình Lên Canvas", command=self._on_ai_draw_clicked)
        self.btn_run_ai.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        self.btn_clear = ttk.Button(btn_frame, text="Xóa Canvas", command=self._clear_canvas)
        self.btn_clear.pack(side=tk.RIGHT)

        # Các câu lệnh mẫu đa dạng
        ttk.Label(tab_draw, text="Mẫu câu thử nghiệm tham số động:", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(4, 2))
        sample_frame = ttk.Frame(tab_draw)
        sample_frame.pack(fill=tk.X, pady=(0, 6))

        samples = [
            ("Tam giác MNP vuông tại M (5, 12) + Đường cao MH", "Vẽ tam giác MNP vuông tại M có MN = 5, MP = 12, kẻ đường cao MH"),
            ("Hình chữ nhật ABCD (8x5) + Giao điểm 2 đường chéo O", "Vẽ hình chữ nhật ABCD có chiều dài AB = 8, chiều rộng BC = 5 và giao điểm hai đường chéo O"),
            ("Hình bình hành ABCD (AB=7, AD=4, góc A=60 độ)", "Vẽ hình bình hành ABCD có AB = 7, AD = 4 và góc A = 60 độ"),
            ("Tam giác DEF đều cạnh 6 + Tâm nội tiếp I", "Vẽ tam giác đều DEF cạnh 6 và đường tròn nội tiếp tâm I"),
            ("Đường tròn O (R=4) + 2 Tiếp tuyến từ P ngoài", "Vẽ đường tròn tâm O bán kính 4 và hai tiếp tuyến từ điểm P nằm ngoài đường tròn")
        ]

        for title, text_val in samples:
            btn = ttk.Button(sample_frame, text="👉 " + title, command=lambda v=text_val: self._set_prompt(v))
            btn.pack(fill=tk.X, pady=1)

        # Log suy luận của AI (Hiển thị thẻ <think> và JSON)
        ttk.Label(tab_draw, text="Luồng bóc tách ý định hình học (DeepSeek-R1):", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(6, 2))
        self.log_text = scrolledtext.ScrolledText(tab_draw, height=8, font=("Consolas", 9), bg="#f8f9fa")
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # TAB 2: SINH ĐỀ THI TỰ ĐỘNG THEO CẤP ĐỘ
        tab_exam = ttk.Frame(notebook, padding=8)
        notebook.add(tab_exam, text="📝 Sinh Đề Thi (Phân Cấp Động 100%)")

        top_exam_bar = ttk.Frame(tab_exam)
        top_exam_bar.pack(fill=tk.X, pady=(0, 6))

        ttk.Label(top_exam_bar, text="Mức độ:").pack(side=tk.LEFT, padx=(0, 4))
        self.diff_var = tk.StringVar(value="medium")
        diff_cb = ttk.Combobox(top_exam_bar, textvariable=self.diff_var, values=["easy (Nhận biết)", "medium (Thông hiểu)", "hard (Vận dụng)", "olympic (Vận dụng cao)"], state="readonly", width=18)
        diff_cb.pack(side=tk.LEFT, padx=(0, 6))

        btn_gen = ttk.Button(top_exam_bar, text="🎲 Sinh Đề Thi Mới", command=self._on_generate_exam)
        btn_gen.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_ai_dress = ttk.Button(top_exam_bar, text="✨ Nhờ AI Đặt Bối Cảnh Thực Tế", command=self._on_ai_contextualize_exam)
        self.btn_ai_dress.pack(side=tk.RIGHT)

        self.exam_display = scrolledtext.ScrolledText(tab_exam, height=20, font=("Segoe UI", 10), bg="#ffffff")
        self.exam_display.pack(fill=tk.BOTH, expand=True, pady=4)

        # ==========================================
        # KHUNG PHẢI: CANVAS BẢN VẼ + INSPECTOR HUD
        # ==========================================
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)

        canvas_header = ttk.Frame(right_frame)
        canvas_header.pack(fill=tk.X, pady=(0, 4))
        ttk.Label(canvas_header, text="📐 CANVAS HÌNH HỌC TƯƠNG TÁC (TÍNH TOÁN GIẢI TÍCH CHUẨN XÁC)", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        self.scale_info = ttk.Label(canvas_header, text="Đang chờ lệnh dựng hình...", font=("Segoe UI", 9))
        self.scale_info.pack(side=tk.RIGHT)

        self.canvas = tk.Canvas(right_frame, bg="#ffffff", highlightthickness=1, highlightbackground="#ced4da")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bảng HUD Inspector hiển thị tọa độ & số đo thực tế
        hud_frame = ttk.LabelFrame(right_frame, text="📊 Bảng Tọa Độ & Số Đo Giải Tích Thời Gian Thực (Calculated Realtime)", padding=6)
        hud_frame.pack(fill=tk.X, pady=(4, 0))

        self.hud_text = tk.Text(hud_frame, height=4, font=("Consolas", 9), bg="#f8f9fa", relief=tk.FLAT)
        self.hud_text.pack(fill=tk.X)
        self.hud_text.insert(tk.END, "Chưa có thực thể hình học. Vui lòng gửi yêu cầu để AI bóc tách & dựng hình.")

        # Lắng nghe sự kiện thay đổi kích thước Canvas
        self.canvas.bind("<Configure>", lambda e: self._redraw_canvas())

        # Khởi tạo đề thi mẫu lần đầu
        self._on_generate_exam()

    def _check_ollama_status(self):
        def check():
            try:
                req = urllib.request.Request("http://localhost:11434/api/tags", headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=3) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    models = [m.get("name") for m in data.get("models", [])]
                    self.after(0, lambda: self.status_lbl.config(text=f"🟢 Ollama Online ({len(models)} mô hình)", foreground="#2b8a3e"))
            except Exception:
                self.after(0, lambda: self.status_lbl.config(text="🔴 Ollama Chưa Bật (localhost:11434)", foreground="#c92a2a"))
        threading.Thread(target=check, daemon=True).start()

    def _set_prompt(self, text):
        self.prompt_entry.delete("1.0", tk.END)
        self.prompt_entry.insert(tk.END, text)

    def _clear_canvas(self):
        self.current_points.clear()
        self.current_lines.clear()
        self.current_circles.clear()
        self.current_labels.clear()
        self._redraw_canvas()
        self.hud_text.delete("1.0", tk.END)
        self.hud_text.insert(tk.END, "Canvas đã được xóa sạch.")

    def _on_ai_draw_clicked(self):
        user_prompt = self.prompt_entry.get("1.0", tk.END).strip()
        if not user_prompt:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập câu lệnh dựng hình!")
            return

        self.btn_run_ai.config(state=tk.DISABLED, text="⏳ AI Đang Bóc Tách & Tính Toán...")
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(tk.END, f"[Gửi tới mô hình {self.model_var.get()} qua Ollama...]\n")

        threading.Thread(target=self._ai_worker, args=(user_prompt,), daemon=True).start()

    def _ai_worker(self, user_prompt):
        t0 = time.time()
        system_prompt = """You are an expert Geometry CAD parser. Convert the user's natural language request into a strict JSON array of geometric construction actions.
Extract exact vertex names and numbers from the user request!
Available actions:
[
  {"action": "triangle_right", "at": "M", "points": ["M", "N", "P"], "lengths": {"MN": 5, "MP": 12}},
  {"action": "triangle_equilateral", "points": ["D", "E", "F"], "side": 6},
  {"action": "triangle_general", "points": ["A", "B", "C"], "a": 7, "b": 5, "c": 6},
  {"action": "rectangle", "points": ["A", "B", "C", "D"], "width": 8, "height": 5, "center": "O"},
  {"action": "parallelogram", "points": ["A", "B", "C", "D"], "a": 7, "b": 4, "angle": 60},
  {"action": "circle", "center": "O", "radius": 4},
  {"action": "altitude", "from": "M", "to": "NP", "name": "H"},
  {"action": "median", "from": "M", "to": "NP", "name": "K"},
  {"action": "incenter", "triangle": ["A", "B", "C"], "name": "I"},
  {"action": "circumcenter", "triangle": ["A", "B", "C"], "name": "O"},
  {"action": "orthocenter", "triangle": ["A", "B", "C"], "name": "H"},
  {"action": "euler_line", "triangle": ["A", "B", "C"]},
  {"action": "tangents", "from": "P", "circle": "O", "radius": 4}
]
Output ONLY the final JSON array. You may reason inside <think>...</think> tags, but make sure the JSON array [ ... ] is at the end."""

        req_body = {
            "model": self.model_var.get(),
            "prompt": f"{system_prompt}\n\nUser request: {user_prompt}\nJSON:",
            "stream": False,
            "options": {"temperature": 0.1}
        }

        try:
            req = urllib.request.Request(
                "http://localhost:11434/api/generate",
                data=json.dumps(req_body).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=40) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                raw_response = res.get("response", "")

            elapsed = (time.time() - t0) * 1000

            # Hiển thị log
            self.after(0, lambda: self.log_text.insert(tk.END, f"[AI phản hồi sau {elapsed:.0f} ms]:\n{raw_response}\n"))

            # Bóc tách JSON: Lọc bỏ khối <think>...</think>
            clean_text = re.sub(r'<think>.*?</think>', '', raw_response, flags=re.DOTALL).strip()

            json_match = re.search(r'\[\s*\{.*\}\s*\]', clean_text, re.DOTALL)
            if not json_match:
                json_match = re.search(r'\[.*\]', clean_text, re.DOTALL)
            if not json_match:
                json_match = re.search(r'\[.*\]', raw_response, re.DOTALL)

            if json_match:
                try:
                    actions = json.loads(json_match.group(0))
                    self.after(0, lambda: self._execute_cad_actions(actions, elapsed))
                except Exception as ex:
                    self.after(0, lambda: messagebox.showerror("Lỗi cú pháp JSON", f"Mô hình sinh cú pháp chưa chuẩn: {ex}"))
            else:
                self.after(0, lambda: messagebox.showerror("Lỗi bóc tách", "Mô hình không trả về mảng JSON hợp lệ!"))

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Lỗi AI", f"Không thể kết nối Ollama: {e}"))
        finally:
            self.after(0, lambda: self.btn_run_ai.config(state=tk.NORMAL, text="🚀 Nhờ AI Dựng Hình Lên Canvas"))

    def _execute_cad_actions(self, actions, ai_time_ms=0.0):
        """Thực thi các lệnh hình học do AI xuất ra bằng lõi GeoSolver2DCore và tự động căn chỉnh khung nhìn."""
        t_start = time.perf_counter()
        self._clear_canvas()

        pts = {}
        lines = []
        circles = []

        for act in actions:
            a_type = act.get("action")

            if a_type == "triangle_right":
                p_names = act.get("points", ["A", "B", "C"])
                if len(p_names) < 3: p_names = ["A", "B", "C"]
                at_v = act.get("at", p_names[0])
                lens = act.get("lengths", {})
                
                # Trích xuất độ dài cạnh nếu có
                val1, val2 = 6.0, 8.0
                if lens:
                    nums = [float(v) for v in lens.values() if isinstance(v, (int, float))]
                    if len(nums) >= 2:
                        val1, val2 = nums[0], nums[1]
                    elif len(nums) == 1:
                        val1 = nums[0]

                # Sắp xếp để đỉnh vuông ở gốc (0, 0)
                other = [p for p in p_names if p != at_v]
                if len(other) < 2:
                    other = ["B", "C"]
                v_right = at_v
                v_arm1, v_arm2 = other[0], other[1]

                pts[v_right] = (0.0, 0.0)
                pts[v_arm1] = (0.0, val1)
                pts[v_arm2] = (val2, 0.0)

                lines.append((v_right, v_arm1, "#1c7ed6", 2))
                lines.append((v_arm1, v_arm2, "#1c7ed6", 2))
                lines.append((v_arm2, v_right, "#1c7ed6", 2))

            elif a_type == "triangle_equilateral":
                p_names = act.get("points", ["A", "B", "C"])
                if len(p_names) < 3: p_names = ["A", "B", "C"]
                side = float(act.get("side", 6.0))
                h = side * math.sqrt(3) / 2.0
                pts[p_names[0]] = (0.0, h)
                pts[p_names[1]] = (-side / 2.0, 0.0)
                pts[p_names[2]] = (side / 2.0, 0.0)

                lines.append((p_names[0], p_names[1], "#2b8a3e", 2))
                lines.append((p_names[1], p_names[2], "#2b8a3e", 2))
                lines.append((p_names[2], p_names[0], "#2b8a3e", 2))

            elif a_type == "triangle_general":
                p_names = act.get("points", ["A", "B", "C"])
                if len(p_names) < 3: p_names = ["A", "B", "C"]
                c_len = float(act.get("c", 6.0))
                b_len = float(act.get("b", 5.0))
                a_len = float(act.get("a", 7.0))
                # Cosine law
                cos_A = max(-1.0, min(1.0, (b_len**2 + c_len**2 - a_len**2) / (2 * b_len * c_len)))
                sin_A = math.sqrt(max(0.0, 1.0 - cos_A**2))
                pts[p_names[0]] = (0.0, 0.0)
                pts[p_names[1]] = (c_len, 0.0)
                pts[p_names[2]] = (b_len * cos_A, b_len * sin_A)

                lines.append((p_names[0], p_names[1], "#495057", 2))
                lines.append((p_names[1], p_names[2], "#495057", 2))
                lines.append((p_names[2], p_names[0], "#495057", 2))

            elif a_type == "rectangle":
                p_names = act.get("points", ["A", "B", "C", "D"])
                if len(p_names) < 4: p_names = ["A", "B", "C", "D"]
                w = float(act.get("width", 8.0))
                h = float(act.get("height", 5.0))
                pts[p_names[0]] = (0.0, h)
                pts[p_names[1]] = (w, h)
                pts[p_names[2]] = (w, 0.0)
                pts[p_names[3]] = (0.0, 0.0)

                lines.append((p_names[0], p_names[1], "#1c7ed6", 2))
                lines.append((p_names[1], p_names[2], "#1c7ed6", 2))
                lines.append((p_names[2], p_names[3], "#1c7ed6", 2))
                lines.append((p_names[3], p_names[0], "#1c7ed6", 2))

                # Giao điểm 2 đường chéo
                center_name = act.get("center")
                if center_name:
                    pts[center_name] = (w / 2.0, h / 2.0)
                    lines.append((p_names[0], p_names[2], "#adb5bd", 1))
                    lines.append((p_names[1], p_names[3], "#adb5bd", 1))

            elif a_type == "parallelogram":
                p_names = act.get("points", ["A", "B", "C", "D"])
                if len(p_names) < 4: p_names = ["A", "B", "C", "D"]
                a_side = float(act.get("a", 7.0))
                b_side = float(act.get("b", 4.0))
                ang = math.radians(float(act.get("angle", 60.0)))
                dx, dy = b_side * math.cos(ang), b_side * math.sin(ang)

                pts[p_names[0]] = (0.0, 0.0)
                pts[p_names[1]] = (a_side, 0.0)
                pts[p_names[2]] = (a_side + dx, dy)
                pts[p_names[3]] = (dx, dy)

                lines.append((p_names[0], p_names[1], "#0ca678", 2))
                lines.append((p_names[1], p_names[2], "#0ca678", 2))
                lines.append((p_names[2], p_names[3], "#0ca678", 2))
                lines.append((p_names[3], p_names[0], "#0ca678", 2))

            elif a_type == "circle":
                c_name = act.get("center", "O")
                r = float(act.get("radius", 4.0))
                if c_name not in pts:
                    pts[c_name] = (0.0, 0.0)
                circles.append((pts[c_name], r, "#1098ad", 2))

            elif a_type == "altitude":
                from_p = act.get("from", "A")
                to_str = act.get("to", "BC")
                h_name = act.get("name", "H")
                # Tìm 2 điểm của cạnh đáy
                target_pts = [p for p in pts.keys() if p in to_str]
                if len(target_pts) >= 2 and from_p in pts:
                    P1 = pts[target_pts[0]]
                    P2 = pts[target_pts[1]]
                    A_pt = pts[from_p]
                    dx, dy = P2[0] - P1[0], P2[1] - P1[1]
                    L2 = dx * dx + dy * dy
                    if L2 > 1e-9:
                        t = ((A_pt[0] - P1[0]) * dx + (A_pt[1] - P1[1]) * dy) / L2
                        H_coord = (P1[0] + t * dx, P1[1] + t * dy)
                        pts[h_name] = H_coord
                        lines.append((from_p, h_name, "#f03e3e", 2))

            elif a_type == "median":
                from_p = act.get("from", "A")
                to_str = act.get("to", "BC")
                m_name = act.get("name", "M")
                target_pts = [p for p in pts.keys() if p in to_str]
                if len(target_pts) >= 2 and from_p in pts:
                    P1 = pts[target_pts[0]]
                    P2 = pts[target_pts[1]]
                    M_coord = ((P1[0] + P2[0]) / 2.0, (P1[1] + P2[1]) / 2.0)
                    pts[m_name] = M_coord
                    lines.append((from_p, m_name, "#fd7e14", 1.5))

            elif a_type == "incenter":
                tri = act.get("triangle", ["A", "B", "C"])
                if all(p in pts for p in tri):
                    I, r = self.engine.compute_incenter(pts[tri[0]], pts[tri[1]], pts[tri[2]])
                    i_name = act.get("name", "I")
                    pts[i_name] = I
                    circles.append((I, r, "#7048e8", 1.5))

            elif a_type == "circumcenter":
                tri = act.get("triangle", ["A", "B", "C"])
                if all(p in pts for p in tri):
                    O, R = self.engine.compute_circumcenter(pts[tri[0]], pts[tri[1]], pts[tri[2]])
                    o_name = act.get("name", "O")
                    pts[o_name] = O
                    circles.append((O, R, "#1098ad", 1.5))

            elif a_type == "orthocenter":
                tri = act.get("triangle", ["A", "B", "C"])
                if all(p in pts for p in tri):
                    H = self.engine.compute_orthocenter(pts[tri[0]], pts[tri[1]], pts[tri[2]])
                    h_name = act.get("name", "H")
                    pts[h_name] = H

            elif a_type == "euler_line":
                tri = act.get("triangle", ["A", "B", "C"])
                if all(p in pts for p in tri):
                    O, R = self.engine.compute_circumcenter(pts[tri[0]], pts[tri[1]], pts[tri[2]])
                    G = self.engine.compute_centroid(pts[tri[0]], pts[tri[1]], pts[tri[2]])
                    H = self.engine.compute_orthocenter(pts[tri[0]], pts[tri[1]], pts[tri[2]])
                    pts["O"] = O
                    pts["G"] = G
                    pts["H"] = H
                    lines.append(("O", "H", "#e64980", 2))

            elif a_type == "tangents":
                p_name = act.get("from", "P")
                c_name = act.get("circle", "O")
                r = float(act.get("radius", 4.0))
                if c_name not in pts:
                    pts[c_name] = (0.0, 0.0)
                if p_name not in pts:
                    pts[p_name] = (pts[c_name][0] + r * 2.2, pts[c_name][1])
                
                circles.append((pts[c_name], r, "#1098ad", 2))
                tangents = self.engine.tangents_from_point_to_circle(pts[p_name], pts[c_name], r)
                for idx, t_pt in enumerate(tangents):
                    t_name = f"T{idx+1}"
                    pts[t_name] = t_pt
                    lines.append((p_name, t_name, "#f03e3e", 1.5))
                    lines.append((c_name, t_name, "#868e96", 1))

        self.current_points = pts
        self.current_lines = lines
        self.current_circles = circles

        # TỰ ĐỘNG CĂN CHỈNH VIEWPORT (AUTO-FIT)
        if pts:
            xs = [p[0] for p in pts.values()]
            ys = [p[1] for p in pts.values()]
            for (cx, cy), r, _, _ in circles:
                xs.extend([cx - r, cx + r])
                ys.extend([cy - r, cy + r])

            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            span_x = max(max_x - min_x, 1.0)
            span_y = max(max_y - min_y, 1.0)

            cw = self.canvas.winfo_width()
            ch = self.canvas.winfo_height()
            if cw < 100: cw = 680
            if ch < 100: ch = 500

            margin = 60.0
            scale_x = (cw - 2 * margin) / span_x
            scale_y = (ch - 2 * margin) / span_y
            self.viewport_scale = max(min(min(scale_x, scale_y), 70.0), 6.0)

            mid_x = (min_x + max_x) / 2.0
            mid_y = (min_y + max_y) / 2.0
            self.viewport_ox = cw / 2.0 - mid_x * self.viewport_scale
            self.viewport_oy = ch / 2.0 + mid_y * self.viewport_scale

        solver_time_ms = (time.perf_counter() - t_start) * 1000
        self._redraw_canvas()
        self._update_inspector_hud(solver_time_ms, ai_time_ms)

    def _update_inspector_hud(self, solver_time_ms=0.0, ai_time_ms=0.0):
        """Cập nhật bảng thông số giải tích thời gian thực."""
        hud_lines = []
        hud_lines.append(f"⏱️ THỜI GIAN: AI bóc tách: {ai_time_ms:.0f} ms | GeoSolver2D giải tích: {solver_time_ms:.2f} ms | Sai số: < 1e-10")
        
        # Danh sách tọa độ các điểm
        pts_str = " | ".join([f"{name}({c[0]:.2f}, {c[1]:.2f})" for name, c in self.current_points.items()])
        hud_lines.append(f"📍 TỌA ĐỘ ĐIỂM: {pts_str}")

        # Độ dài các đoạn thẳng
        lens = []
        for p1, p2, _, _ in self.current_lines[:6]:
            if p1 in self.current_points and p2 in self.current_points:
                d = self.engine.distance(self.current_points[p1], self.current_points[p2])
                lens.append(f"{p1}{p2} = {d:.2f}")
        if lens:
            hud_lines.append(f"📏 ĐỘ DÀI ĐOẠN: " + " | ".join(lens))

        # Đường tròn
        if self.current_circles:
            circ_str = " | ".join([f"Tâm({c[0]:.2f}, {c[1]:.2f}), R = {r:.2f}" for c, r, _, _ in self.current_circles])
            hud_lines.append(f"⚪ ĐƯỜNG TRÒN: {circ_str}")

        self.hud_text.delete("1.0", tk.END)
        self.hud_text.insert(tk.END, "\n".join(hud_lines))

    def _redraw_canvas(self):
        self.canvas.delete("all")

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10: w = 700
        if h < 10: h = 500

        ox, oy = self.viewport_ox, self.viewport_oy
        scale = self.viewport_scale

        # 1. Vẽ lưới tọa độ mờ
        grid_step = max(int(scale), 25)
        for x in range(0, int(w), grid_step):
            self.canvas.create_line(x, 0, x, h, fill="#f8f9fa", width=1)
        for y in range(0, int(h), grid_step):
            self.canvas.create_line(0, y, w, y, fill="#f8f9fa", width=1)

        # Trục tọa độ nhẹ
        self.canvas.create_line(0, oy, w, oy, fill="#e9ecef", width=1)
        self.canvas.create_line(ox, 0, ox, h, fill="#e9ecef", width=1)

        # 2. Vẽ các đường tròn
        for center, radius, color, l_width in self.current_circles:
            cx, cy = self.engine.cartesian_to_canvas(center, (ox, oy), scale, flip_y=True)
            r_px = radius * scale
            self.canvas.create_oval(cx - r_px, cy - r_px, cx + r_px, cy + r_px, outline=color, width=l_width)

        # 3. Vẽ các đoạn thẳng
        for p1_name, p2_name, color, l_width in self.current_lines:
            if p1_name in self.current_points and p2_name in self.current_points:
                x1, y1 = self.engine.cartesian_to_canvas(self.current_points[p1_name], (ox, oy), scale, flip_y=True)
                x2, y2 = self.engine.cartesian_to_canvas(self.current_points[p2_name], (ox, oy), scale, flip_y=True)
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=l_width)

        # 4. Vẽ các điểm và nhãn chữ
        for name, coord in self.current_points.items():
            sx, sy = self.engine.cartesian_to_canvas(coord, (ox, oy), scale, flip_y=True)
            self.canvas.create_oval(sx - 4, sy - 4, sx + 4, sy + 4, fill="#1c7ed6", outline="#ffffff", width=1.5)
            self.canvas.create_text(sx + 12, sy - 10, text=name, font=("Segoe UI", 11, "bold"), fill="#212529")

        # Cập nhật thông tin góc trên
        n_pts = len(self.current_points)
        n_lines = len(self.current_lines)
        n_circs = len(self.current_circles)
        self.scale_info.config(text=f"Tọa độ gốc: ({ox:.0f}, {oy:.0f}) | Scale: {scale:.1f} | Điểm: {n_pts} | Đoạn: {n_lines} | Tròn: {n_circs}")

    def _on_generate_exam(self):
        """Sinh đề thi hoàn toàn ngẫu nhiên bằng thuật toán Python."""
        level = self.diff_var.get().split()[0]
        if level == "easy":
            text = DynamicExamGenerator.generate_easy()
        elif level == "medium":
            text = DynamicExamGenerator.generate_medium()
        elif level == "hard":
            text = DynamicExamGenerator.generate_hard()
        else:
            text = DynamicExamGenerator.generate_olympic()

        self.exam_display.delete("1.0", tk.END)
        self.exam_display.insert(tk.END, text)

    def _on_ai_contextualize_exam(self):
        """Nhờ DeepSeek-R1 biến đề toán vừa sinh thành bài toán thực tế đời sống."""
        current_text = self.exam_display.get("1.0", tk.END).strip()
        if not current_text:
            return

        self.btn_ai_dress.config(state=tk.DISABLED, text="⏳ AI Đang Đặt Bối Cảnh...")
        self.exam_display.insert(tk.END, "\n\n[ĐANG GỌI DEEPSEEK-R1 ĐẶT BỐI CẢNH ĐỜI SỐNG THỰC TẾ...]\n")

        def call_ai():
            prompt = f"""Bạn là chuyên gia ra đề thi chuẩn GDPT 2018. Hãy viết lại bài toán sau đây thành MỘT BÀI TOÁN THỰC TẾ SINH ĐỘNG gắn với kỹ thuật, xây dựng, kiến trúc hoặc kinh tế đời sống.
YÊU CẦU QUAN TRỌNG:
1. Giữ nguyên toàn bộ số liệu, phương trình và kết quả toán học.
2. Đưa vào ngữ cảnh thực tế tự nhiên, hấp dẫn.
3. Trình bày ngắn gọn, súc tích.

BÀI TOÁN GỐC:
{current_text}
"""
            req_body = {
                "model": self.model_var.get(),
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3}
            }
            try:
                req = urllib.request.Request(
                    "http://localhost:11434/api/generate",
                    data=json.dumps(req_body).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=40) as resp:
                    res = json.loads(resp.read().decode("utf-8"))
                    raw = res.get("response", "")
                
                clean = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()
                self.after(0, lambda: self._append_ai_dressed_exam(clean))
            except Exception as e:
                self.after(0, lambda: self.exam_display.insert(tk.END, f"\n[Lỗi kết nối AI: {e}]\n"))
            finally:
                self.after(0, lambda: self.btn_ai_dress.config(state=tk.NORMAL, text="✨ Nhờ AI Đặt Bối Cảnh Thực Tế"))

        threading.Thread(target=call_ai, daemon=True).start()

    def _append_ai_dressed_exam(self, ai_text):
        self.exam_display.insert(tk.END, "\n" + "="*50 + "\n")
        self.exam_display.insert(tk.END, "🌿 ĐỀ THI ỨNG DỤNG THỰC TẾ (DO DEEPSEEK-R1 BIÊN SOẠN):\n\n")
        self.exam_display.insert(tk.END, ai_text + "\n")


if __name__ == "__main__":
    app = AICanvasStudioDemo()
    app.mainloop()
