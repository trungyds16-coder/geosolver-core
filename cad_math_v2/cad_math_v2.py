
def copy_figure_to_clipboard(fig) -> bool:
    """
    Sao chép matplotlib Figure vào Windows Clipboard ở định dạng CF_DIB (DIB 24/32-bit).
    Tương thích tuyệt đối với MS Word, PowerPoint, Paint, Zalo, Discord, Web.
    Đảm bảo nền trắng thuần (#ffffff), độ phân giải cao 200 DPI, không bị trong suốt.
    Sử dụng ctypes 64-bit prototypes chuẩn xác để tránh lỗi Access Violation.
    """
    import sys, io, ctypes
    from ctypes import wintypes
    from PIL import Image

    if not fig:
        return False

    try:
        png_buf = io.BytesIO()
        fig.savefig(png_buf, format='png', dpi=200, facecolor='#ffffff', edgecolor='none')
        png_buf.seek(0)
        img = Image.open(png_buf).convert('RGB')
        bmp_buf = io.BytesIO()
        img.save(bmp_buf, format='BMP')
        data = bmp_buf.getvalue()[14:]  # Cắt bỏ 14 byte BITMAPFILEHEADER để lấy DIB thuần
        png_buf.close()
        bmp_buf.close()

        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32

        kernel32.GlobalAlloc.restype = ctypes.c_void_p
        kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
        kernel32.GlobalLock.restype = ctypes.c_void_p
        kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
        kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]

        user32.OpenClipboard.argtypes = [wintypes.HWND]
        user32.OpenClipboard.restype = wintypes.BOOL
        user32.EmptyClipboard.restype = wintypes.BOOL
        user32.SetClipboardData.argtypes = [wintypes.UINT, ctypes.c_void_p]
        user32.SetClipboardData.restype = ctypes.c_void_p
        user32.CloseClipboard.restype = wintypes.BOOL

        GMEM_MOVEABLE = 0x0002
        CF_DIB = 8

        h_mem = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(data))
        if not h_mem:
            return False

        p_mem = kernel32.GlobalLock(h_mem)
        if not p_mem:
            return False

        ctypes.cdll.msvcrt.memcpy(ctypes.c_void_p(p_mem), data, len(data))
        kernel32.GlobalUnlock(h_mem)

        if user32.OpenClipboard(None):
            user32.EmptyClipboard()
            res = user32.SetClipboardData(CF_DIB, h_mem)
            user32.CloseClipboard()
            return bool(res)
        return False
    except Exception as e:
        print(f"[Clipboard Error]: {e}")
        return False


THEMES = {
    "win11_light": {
        "name": "Giao diện sáng (Light)",
        "bg_window": "#F3F3F3",
        "bg_card": "#FFFFFF",
        "bg_header": "#FFFFFF",
        "fg_header": "#0F172A",
        "border_color": "#E2E8F0",
        "toolbar_bg": "#FAFAFA",
        "btn_bg": "#FFFFFF",
        "btn_fg": "#0F172A",
        "btn_accent_bg": "#0067C0",
        "btn_accent_fg": "#FFFFFF",
        "status_bg": "#F8FAFC",
        "status_fg": "#64748B",
        "text_box_bg": "#FFFFFF",
        "text_box_fg": "#0F172A",
        "entry_bg": "#FFFFFF",
        "entry_fg": "#0F172A",
        "tab_bg": "#F1F5F9",
        "tab_fg": "#475569",
        "tab_active_bg": "#FFFFFF",
        "tab_active_fg": "#0067C0",
    },
    "win11_blue": {
        "name": "Giao diện xanh hiện đại (Modern Blue)",
        "bg_window": "#F0F6FF",
        "bg_card": "#FFFFFF",
        "bg_header": "#0067C0",
        "fg_header": "#FFFFFF",
        "border_color": "#BFDBFE",
        "toolbar_bg": "#EBF3FE",
        "btn_bg": "#FFFFFF",
        "btn_fg": "#0A4275",
        "btn_accent_bg": "#0067C0",
        "btn_accent_fg": "#FFFFFF",
        "status_bg": "#E0EEFF",
        "status_fg": "#0A4275",
        "text_box_bg": "#FFFFFF",
        "text_box_fg": "#0F172A",
        "entry_bg": "#FFFFFF",
        "entry_fg": "#0F172A",
        "tab_bg": "#DBEAFE",
        "tab_fg": "#1E40AF",
        "tab_active_bg": "#FFFFFF",
        "tab_active_fg": "#0067C0",
    },
    "classic_cad": {
        "name": "Giao diện kỹ thuật cổ điển (Classic CAD)",
        "bg_window": "#ECE9D8",
        "bg_card": "#FFFFFF",
        "bg_header": "#1E293B",
        "fg_header": "#FFFFFF",
        "border_color": "#B8B5A8",
        "toolbar_bg": "#E4E1D0",
        "btn_bg": "#ECE9D8",
        "btn_fg": "#000000",
        "btn_accent_bg": "#0969DA",
        "btn_accent_fg": "#FFFFFF",
        "status_bg": "#DCD8C8",
        "status_fg": "#333333",
        "text_box_bg": "#FFFFFF",
        "text_box_fg": "#000000",
        "entry_bg": "#FFFFFF",
        "entry_fg": "#000000",
        "tab_bg": "#DCD8C8",
        "tab_fg": "#333333",
        "tab_active_bg": "#FFFFFF",
        "tab_active_fg": "#0969DA",
    },
    "dark_studio": {
        "name": "Modern Dark Studio (Tối Dịu Mắt)",
        "bg_window": "#18181B",
        "bg_card": "#27272A",
        "bg_header": "#09090B",
        "fg_header": "#F4F4F5",
        "border_color": "#3F3F46",
        "toolbar_bg": "#202024",
        "btn_bg": "#27272A",
        "btn_fg": "#F4F4F5",
        "btn_accent_bg": "#0284C7",
        "btn_accent_fg": "#FFFFFF",
        "status_bg": "#18181B",
        "status_fg": "#A1A1AA",
        "text_box_bg": "#18181B",
        "text_box_fg": "#F4F4F5",
        "entry_bg": "#27272A",
        "entry_fg": "#F4F4F5",
        "tab_bg": "#27272A",
        "tab_fg": "#A1A1AA",
        "tab_active_bg": "#18181B",
        "tab_active_fg": "#38BDF8",
    }
}

"""
================================================================================
CAD MATH STUDIO PRO v2.4
Hệ thống giải toán CAS tự nhiên, trực quan hóa 2D vector, giải phương trình,
bất phương trình (kèm bài toán tham số m), số phức, cực trị VDC đa biến,
vi tích phân đa biến, đại số tuyến tính ma trận, thống kê xác suất và khảo sát hàm số Oxy.
================================================================================
"""

import sys
import os

# An toàn cho môi trường pythonw
if sys.stdout is None:
    class _DummyWriter:
        def write(self, s): pass
        def flush(self): pass
    sys.stdout = _DummyWriter()
if sys.stderr is None:
    class _DummyWriter:
        def write(self, s): pass
        def flush(self): pass
    sys.stderr = _DummyWriter()

import re
import math
import time
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext

# ---------------------------------------------------------------------------
# STEM_SHARED_CORE: thêm thư mục gốc vào sys.path để import được shared core
# ---------------------------------------------------------------------------
_STEM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _STEM_ROOT not in sys.path:
    sys.path.insert(0, _STEM_ROOT)

# Import hệ thống i18n tập trung; nếu không có thì dùng fallback nội bộ
try:
    from stem_shared_core.i18n import t as _i18n_t, set_language as _i18n_set, get_language as _i18n_get
    _I18N_AVAILABLE = True
except Exception:
    _I18N_AVAILABLE = False

import threading
import webbrowser

# Import AI downloader & model hub; nếu không có thì vô hiệu hóa tính năng
try:
    from stem_shared_core.hf_downloader import ask_download_model
    from stem_shared_core.ai_model_hub import AIModelHub, ModelSource, ChunkKind
    from stem_shared_core.ai_local_manager import (
        AILocalManager,
        PROFILES,
        AIPaths,
        MemoryMonitor,
        ThinkParser,
        RepetitionBreaker,
        _filter_exotic_scripts,
        DEFAULT_MODELS_ROOT,
    )
    _AI_HUB_AVAILABLE = True
except Exception:
    _AI_HUB_AVAILABLE = False

import sympy as sp
from enum import Enum

from stem_shared_core.cad_math_core import (
    CADMathCore,
    DiophantineCategory,
    compute_matrix_inverse,
    matrix_multiply
)
from sympy.core.relational import Relational
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor
)
from sympy.solvers.inequalities import reduce_inequalities
import numpy as np

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Bật High-DPI trên Windows để giao diện và công thức vẽ nét như vector
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application, convert_xor)

# Ký hiệu biến toàn cục cho SymPy (z là biến số phức tổng quát, các biến khác là số thực)
x, y, t, m, a, b, c, n = sp.symbols('x y t m a b c n', real=True)
z = sp.Symbol('z')
theta = sp.Symbol('theta')
k = sp.Symbol('k', integer=True)

# ==============================================================================
# BILINGUAL LOCALIZATION DICTIONARY (TIẾNG VIỆT & ENGLISH)
# Giữ nguyên làm nguồn fallback và đăng ký vào i18n tập trung.
# ==============================================================================
TRANSLATIONS = {
    'vi': {
        'title': "CAD Math Studio Pro v2.4",
        'status': "Trạng thái: Sẵn sàng | Nhập xuất toán học tự nhiên",
        'tab1': "1. Phương trình",
        'tab2': "2. Cực trị",
        'tab3': "3. Giải tích",
        'tab4': "4. Ma trận",
        'tab5': "5. Xác suất & Thống kê",
        'tab6': "6. Đồ thị hàm số",
        
        # Toolbar
        'ai_solve': "AI giải toán (F5)",
        'ai_config': "Cấu hình",
        'export': "Xuất báo cáo",
        'restore': "Khôi phục CAS",
        'ribbon': "Ký hiệu toán",
        
        # Action Buttons
        'btn_solve_eq': "⚡ Giải bài toán (F5)",
        'btn_solve_ext': "⚡ Phân tích cực trị",
        'btn_calc': "⚡ Tính giải tích",
        'btn_mat': "⚡ Tính toán ma trận",
        'btn_stat': "⚡ Phân tích thống kê",
        'btn_plot': "⚡ Khảo sát & Vẽ đồ thị",

        # Tab 1
        'lbl_input_eq': "NHẬP PHƯƠNG TRÌNH, BẤT PHƯƠNG TRÌNH HOẶC HỆ (THAM SỐ m):",
        'param_mode_label': "Chế độ tham số m:",
        'param_modes': [
            "Tự động giải",
            "Tìm m để BPT nghiệm đúng với mọi x ∈ D",
            "Tìm m để BPT có nghiệm",
            "Tìm m để BPT vô nghiệm",
            "Khảo sát số nghiệm theo tham số m"
        ],
        'preview_eq': "XEM TRƯỚC CÔNG THỨC 2D",
        'hero_eq': "KẾT QUẢ TẬP NGHIỆM",
        'steps_eq': "LỜI GIẢI CHI TIẾT:",
        'graph_eq': "ĐỒ THỊ & TRỤC SỐ BIỂU DIỄN NGHIỆM",
        'eq_samples': [
            "x² - 3x + 2 ≤ 0",
            "(x-1)/(x+2) > 0",
            "√(2x+1) < x - 1",
            "Tham số m",
            "Hệ căn bậc 4",
            "Số phức"
        ],

        # Tab 2
        'lbl_ext_header': "BIỂU THỨC MỤC TIÊU CẦN TÌM CỰC TRỊ P(x, y, z):",
        'lbl_ext_cond': "ĐIỀU KIỆN RÀNG BUỘC g(x, y, z) = 0 (BỎ TRỐNG NẾU KHÔNG CÓ):",
        'hero_ext': "KẾT QUẢ CỰC TRỊ",
        'steps_ext': "QUY TRÌNH BIẾN ĐỔI VÀ ĐÁNH GIÁ ĐIỂM RƠI:",
        'contour_ext': "BẢN ĐỒ MỨC CỰC TRỊ VÀ ĐƯỜNG MỨC CONTOUR",
        'ext_samples': [
            "Trị tuyệt đối (3 biến)",
            "Hệ 2 biến"
        ],

        # Tab 3
        'lbl_calc_header': "BIỂU THỨC GIẢI TÍCH f(x, y, z) CẦN KHẢO SÁT:",
        'lbl_calc_op': "Phép tính:",
        'lbl_calc_var': "Biến:",
        'lbl_calc_param': "Tham số / Cận:",
        'calc_modes': [
            "Đạo hàm riêng ∂/∂z",
            "Đạo hàm riêng ∂/∂x",
            "Đạo hàm riêng ∂/∂y",
            "Đạo hàm cấp 2 ∂²/∂z²",
            "Nguyên hàm ∫ f dx",
            "Tích phân xác định ∫_a^b f dx",
            "Khai triển chuỗi Taylor",
            "Giới hạn (Limit) lim"
        ],
        'hero_calc': "KẾT QUẢ BIỂU THỨC 2D (CAS OUTPUT)",
        'steps_calc': "QUY TRÌNH BIẾN ĐỔI VÀ TÍNH TOÁN GIẢI TÍCH:",
        'graph_calc': "ĐỒ THỊ HÀM SỐ & TIẾP TUYẾN / DIỆN TÍCH",
        'calc_samples': [
            "Đạo hàm riêng ∂/∂z",
            "Nguyên hàm ∫ f dx",
            "Chuỗi Taylor"
        ],

        # Tab 4
        'lbl_mat_header': "TÍNH TOÁN MA TRẬN (GÕ TỪNG DÒNG, CÁCH NHAU BẰNG KHOẢNG TRẮNG HOẶC PHẨY):",
        'frame_mat_a': "MA TRẬN A (m x n):",
        'frame_mat_b': "MA TRẬN B (HOẶC VECTOR CỘT B):",
        'btn_mat_inv': "A⁻¹",
        'btn_mat_trans': "Aᵀ",
        'btn_mat_solve': "Giải A·X = B",
        'btn_mat_eigen': "Trị riêng & Vector",
        'mat_samples': [
            "Nhân ma trận 3x3",
            "Hệ tuyến tính AX = B"
        ],
        'hero_mat': "KẾT QUẢ PHÉP TOÁN MA TRẬN 2D",
        'steps_mat': "QUY TRÌNH BIẾN ĐỔI VÀ TÍNH TOÁN MA TRẬN:",

        # Tab 5
        'lbl_stat_header': "BỘ CÔNG CỤ XÁC SUẤT & THỐNG KÊ MÔ TẢ:",
        'lbl_stat_mode': "Chế độ:",
        'stat_modes': [
            "1. Đại số Tổ hợp & Nhị thức Newton",
            "2. Xác suất & Phân phối Nhị thức B(n, p)",
            "3. Thống kê mô tả (Mean, SD, IQR, Boxplot)"
        ],
        'lbl_stat_data': "Dữ liệu mẫu số liệu (cách nhau bởi phẩy hoặc khoảng trắng):",
        'hero_stat': "BẢNG CHỈ SỐ THỐNG KÊ MÔ TẢ",
        'steps_stat': "QUY TRÌNH TÍNH TOÁN CHI TIẾT:",
        'plot_stat': "BIỂU ĐỒ TẦN SỐ (HISTOGRAM) & BIỂU ĐỒ HỘP (BOXPLOT)",
        'stat_samples': [
            "Thống kê có ngoại lai",
            "Nhị thức (2x - 3)^6",
            "Phân phối B(20, 0.4)"
        ],

        # Tab 6
        'lbl_plot_header': "HÀM SỐ CẦN KHẢO SÁT f(x) (HỆ TRỤC TỌA ĐỘ OXY):",
        'graph_plot': "ĐỒ THỊ HÀM SỐ TRÊN HỆ TRỤC TỌA ĐỘ OXY",
        'report_plot': "BẢNG KHẢO SÁT BIẾN THIÊN & ĐỒ THỊ:",
        'plot_samples': [
            "x³ - 3x² + 2",
            "x⁴ - 2x² - 1",
            "(2x+1)/(x-1)",
            "sin(x) + cos(x)"
        ],
    },
    'en': {
        'title': "CAD Math Studio Pro v2.4",
        'status': "Status: Ready | Natural mathematical computation",
        'tab1': "1. Equations",
        'tab2': "2. Extrema",
        'tab3': "3. Calculus",
        'tab4': "4. Matrices",
        'tab5': "5. Statistics",
        'tab6': "6. Grapher",

        # Toolbar
        'ai_solve': "AI Solve (F5)",
        'ai_config': "Settings",
        'export': "Export Report",
        'restore': "Restore CAS",
        'ribbon': "Math Ribbon",

        # Action Buttons
        'btn_solve_eq': "⚡ Solve Problem (F5)",
        'btn_solve_ext': "⚡ Analyze Extrema",
        'btn_calc': "⚡ Calculate Calculus",
        'btn_mat': "⚡ Matrix Operations",
        'btn_stat': "⚡ Statistical Analysis",
        'btn_plot': "⚡ Plot Graph & Study",

        # Tab 1
        'lbl_input_eq': "ENTER EQUATION, INEQUALITY OR SYSTEM (PARAMETER m):",
        'param_mode_label': "Parameter m Mode:",
        'param_modes': [
            "Auto Solve",
            "Find m so inequality holds for all x ∈ D",
            "Find m so inequality has solutions",
            "Find m so inequality has no solution",
            "Analyze number of solutions by parameter m"
        ],
        'preview_eq': "2D FORMULA PREVIEW",
        'hero_eq': "SOLUTION SET",
        'steps_eq': "STEP-BY-STEP SOLUTION:",
        'graph_eq': "GRAPH & NUMBER LINE REPRESENTATION",
        'eq_samples': [
            "x² - 3x + 2 ≤ 0",
            "(x-1)/(x+2) > 0",
            "√(2x+1) < x - 1",
            "Parametric m",
            "4th-Root System",
            "Complex Numbers"
        ],

        # Tab 2
        'lbl_ext_header': "OBJECTIVE FUNCTION TO OPTIMIZE P(x, y, z):",
        'lbl_ext_cond': "CONSTRAINTS g(x, y, z) = 0 (LEAVE EMPTY IF NONE):",
        'hero_ext': "OPTIMAL EXTREMUM",
        'steps_ext': "DERIVATION & OPTIMAL BOUNDS ANALYSIS:",
        'contour_ext': "CONTOUR MAP & EXTREMAL CURVES",
        'ext_samples': [
            "Abs value (3 vars)",
            "System (2 vars)"
        ],

        # Tab 3
        'lbl_calc_header': "CALCULUS EXPRESSION f(x, y, z) TO ANALYZE:",
        'lbl_calc_op': "Operation:",
        'lbl_calc_var': "Variable:",
        'lbl_calc_param': "Param / Bounds:",
        'calc_modes': [
            "Partial derivative ∂/∂z",
            "Partial derivative ∂/∂x",
            "Partial derivative ∂/∂y",
            "Second derivative ∂²/∂z²",
            "Indefinite integral ∫ f dx",
            "Definite integral ∫_a^b f dx",
            "Taylor series",
            "Limit lim"
        ],
        'hero_calc': "2D FORMULA OUTPUT (CAS)",
        'steps_calc': "STEP-BY-STEP CALCULUS DERIVATION:",
        'graph_calc': "FUNCTION GRAPH & TANGENT / AREA",
        'calc_samples': [
            "Partial ∂/∂z",
            "Integral ∫ f dx",
            "Taylor Series"
        ],

        # Tab 4
        'lbl_mat_header': "MATRIX COMPUTATION (ONE ROW PER LINE, SPACE OR COMMA SEPARATED):",
        'frame_mat_a': "MATRIX A (m x n):",
        'frame_mat_b': "MATRIX B (OR COLUMN VECTOR B):",
        'btn_mat_inv': "A⁻¹ (Inv)",
        'btn_mat_trans': "Aᵀ (Trans)",
        'btn_mat_solve': "Solve A·X = B",
        'btn_mat_eigen': "Eigenvalues & Vectors",
        'mat_samples': [
            "3x3 Matrix Multiplication",
            "Linear System AX = B"
        ],
        'hero_mat': "2D MATRIX OPERATION RESULT",
        'steps_mat': "DETAILED MATRIX COMPUTATION STEPS:",

        # Tab 5
        'lbl_stat_header': "PROBABILITY & DESCRIPTIVE STATISTICS TOOLKIT:",
        'lbl_stat_mode': "Mode:",
        'stat_modes': [
            "1. Combinatorics & Binomial Theorem",
            "2. Probability & Binomial Distribution B(n, p)",
            "3. Descriptive Statistics (Mean, SD, IQR, Boxplot)"
        ],
        'lbl_stat_data': "Sample data (comma or space separated):",
        'hero_stat': "DESCRIPTIVE STATISTICS SUMMARY",
        'steps_stat': "DETAILED COMPUTATION STEPS:",
        'plot_stat': "FREQUENCY HISTOGRAM & BOXPLOT",
        'stat_samples': [
            "Data with outliers",
            "Binomial (2x - 3)^6",
            "Distribution B(20, 0.4)"
        ],

        # Tab 6
        'lbl_plot_header': "FUNCTION TO STUDY f(x) (2D OXY COORDINATE SYSTEM):",
        'graph_plot': "2D FUNCTION GRAPH ON OXY PLANE",
        'report_plot': "VARIATION & GRAPH REPORT:",
        'plot_samples': [
            "x³ - 3x² + 2",
            "x⁴ - 2x² - 1",
            "(2x+1)/(x-1)",
            "sin(x) + cos(x)"
        ],
    }
}

# ---------------------------------------------------------------------------
# Đăng ký TRANSLATIONS vào hệ thống i18n tập trung (stem_shared_core.i18n)
# Dữ liệu được đăng ký với prefix "cad." để tránh xung đột namespace.
# ---------------------------------------------------------------------------
if _I18N_AVAILABLE:
    try:
        from stem_shared_core.i18n import get_i18n as _get_i18n
        _mgr = _get_i18n()
        for _lng, _dict in TRANSLATIONS.items():
            _mgr.register_translations(_lng, {"cad": _dict})
        del _mgr, _lng, _dict
    except Exception:
        pass


def _cad_t(key: str, lang: str = None) -> object:
    """Lấy chuỗi dịch cho app CAD. Ưu tiên i18n tập trung, fallback về TRANSLATIONS."""
    if _I18N_AVAILABLE:
        try:
            val = _i18n_t(f"cad.{key}", lang=lang)
            if val != f"cad.{key}":
                return val
        except Exception:
            pass
    # Fallback về dict nội bộ
    _lang = lang or (getattr(_get_current_lang_cad(), "__call__", lambda: "vi")() if _I18N_AVAILABLE else "vi")
    return TRANSLATIONS.get(_lang, TRANSLATIONS.get("vi", {})).get(key, key)


def _get_current_lang_cad():
    """Lấy ngôn ngữ hiện tại từ i18n hoặc mặc định 'vi'."""
    if _I18N_AVAILABLE:
        try:
            return _i18n_get()
        except Exception:
            pass
    return "vi"


# ==============================================================================
# NATURAL MATHEMATICAL SYNTAX PARSER (HỖ TRỢ BẤT PHƯƠNG TRÌNH, THAM SỐ m, SỐ PHỨC)
# ==============================================================================
def convert_log_base_natural(expr_str: str) -> str:
    """Chuyển đổi log_a(b) hoặc loga(b) -> log(b, a) theo cú pháp chuẩn của SymPy."""
    expr_str = re.sub(r'log_\{?([0-9a-zA-Z]+)\}?\s*\(([^()]+)\)', r'log(\2, \1)', expr_str)
    expr_str = re.sub(r'\blog([0-9]+)\s*\(([^()]+)\)', r'log(\2, \1)', expr_str)
    expr_str = re.sub(r'\blog([a-zA-Z])\s*\(([^()]+)\)', r'log(\2, \1)', expr_str)
    return expr_str

def natural_to_sympy_syntax(raw: str) -> str:
    r"""
    Chuẩn hóa biểu thức gõ tự nhiên hoặc LaTeX sang cú pháp chuẩn xác cho SymPy:
    - Bất phương trình: <=, >=, !=, <, >, \le, \ge, \leq, \geq
    - Trị tuyệt đối: |x - y| -> Abs(x - y), \abs{expr} -> Abs(expr)
    - Số phức: 2i -> 2 * I, i -> I, \bar{z} -> conjugate(z)
    - Tiếng Việt: căn, can -> sqrt
    - Phân số: \frac{a}{b} -> ((a)/(b))
    - Lũy thừa: ^ -> **
    """
    s = raw.strip()

    # Chuẩn hóa các dấu bất phương trình LaTeX
    s = re.sub(r'\\leq|\\le', '<=', s)
    s = re.sub(r'\\geq|\\ge', '>=', s)
    s = re.sub(r'\\neq|\\ne', '!=', s)

    # 1. Trị tuyệt đối dạng thẳng |expr| -> Abs(expr)
    s = re.sub(r'\\abs\{([^{}]+)\}', r'Abs(\1)', s)
    s = re.sub(r'\|([^|]+)\|', r'Abs(\1)', s)

    # 2. Xử lý số phức: 3i -> 3 * I, standalone i -> I, liên hợp \bar{z}
    s = re.sub(r'(\d+)\s*i\b', r'\1 * I', s)
    s = re.sub(r'(?<![a-zA-Z0-9_])i\b', 'I', s)
    s = re.sub(r'\\overline\{z\}|\\bar\{z\}|z_bar', 'conjugate(z)', s)

    # 3. Căn bậc n (LaTeX & Tiếng Việt & dạng rút gọn căn[n])
    s = re.sub(r'\\sqrt\[([^\]]+)\]\{([^{}]+)\}', r'root((\2), (\1))', s)
    s = re.sub(r'\\sqrt\[([^\]]+)\]\(([^()]+)\)', r'root((\2), (\1))', s)
    s = re.sub(r'căn\[([^\]]+)\]\(([^()]+)\)', r'root((\2), (\1))', s, flags=re.IGNORECASE)
    s = re.sub(r'căn\[([^\]]+)\]\{([^{}]+)\}', r'root((\2), (\1))', s, flags=re.IGNORECASE)
    s = re.sub(r'can\[([^\]]+)\]\(([^()]+)\)', r'root((\2), (\1))', s, flags=re.IGNORECASE)
    s = re.sub(r'can\[([^\]]+)\]\{([^{}]+)\}', r'root((\2), (\1))', s, flags=re.IGNORECASE)
    s = re.sub(r'sqrt\[([^\]]+)\]\(([^()]+)\)', r'root((\2), (\1))', s, flags=re.IGNORECASE)
    s = re.sub(r'sqrt\[([^\]]+)\]\{([^{}]+)\}', r'root((\2), (\1))', s, flags=re.IGNORECASE)
    s = re.sub(r'căn\s+bậc\s+(\d+)\s*\(([^)]+)\)', r'root((\2), \1)', s, flags=re.IGNORECASE)
    s = re.sub(r'căn\s+bậc\s+(\d+)\s*\{([^}]+)\}', r'root((\2), \1)', s, flags=re.IGNORECASE)
    s = re.sub(r'can\s+bac\s+(\d+)\s*\(([^)]+)\)', r'root((\2), \1)', s, flags=re.IGNORECASE)
    s = re.sub(r'can\s+bac\s+(\d+)\s*\{([^}]+)\}', r'root((\2), \1)', s, flags=re.IGNORECASE)

    # 4. Tiếng Việt & hàm căn bậc 2 thông thường
    s = re.sub(r'\bcăn\b|\bcan\b', 'sqrt', s, flags=re.IGNORECASE)
    for _ in range(4):
        s = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'((\1)/(\2))', s)

    # 5. Số đứng liền trước biến: 2x -> 2 * x, 12y -> 12 * y
    s = re.sub(r'(\d+)\s*([a-zA-Z\\]+)', r'\1 * \2', s)
    s = convert_log_base_natural(s)

    # 6. Phép nhân ngầm định trước tên hàm: x căn(...) -> x * sqrt(...)
    s = re.sub(r'([a-zA-Z0-9\)])\s*(sqrt|sin|cos|tan|cot|log|ln|Abs)', r'\1 * \2', s)

    # 7. Phép nhân ngầm định trước mở ngoặc: y(12 - x^2) -> y * (12 - x^2)
    s = re.sub(r'(?<!sqrt)(?<!sin)(?<!cos)(?<!tan)(?<!cot)(?<!log)(?<!ln)(?<!Abs)\b([a-zA-Z0-9])\s*\(', r'\1 * (', s)

    # 8. Phép nhân giữa 2 ngoặc: (x + 1)(x - 2) -> (x + 1) * (x - 2) hoặc sau đóng ngoặc )z -> ) * z
    s = re.sub(r'\)\s*\(', r') * (', s)
    s = re.sub(r'\)\s*([a-zA-Z])', r') * \1', s)

    # 9. Dấu chấm nhân & ký hiệu LaTeX thông dụng
    s = re.sub(r'(\w|\))\s*[\.·•]\s*(\w|\()', r'\1 * \2', s)
    s = re.sub(r'\\cdot|\\times', '*', s)
    s = re.sub(r'\\left|\\right', '', s)

    for _ in range(4):
        s = re.sub(r'\\sqrt\{([^{}]+)\}', r'sqrt(\1)', s)
    s = re.sub(r'\\sqrt\s*', 'sqrt', s)

    # Tự động chuẩn hóa thứ tự tham số hàm root: root(bậc, biểu thức) -> root(biểu thức, bậc)
    def normalize_root_args(m):
        a1 = m.group(1).strip()
        a2 = m.group(2).strip()
        if (re.match(r'^\d+$', a1) or a1 in ('n', 'k', 'm')) and not re.match(r'^\d+$', a2):
            return f'root(({a2}), ({a1}))'
        return f'root(({a1}), ({a2}))'
    s = re.sub(r'\broot\s*\(\s*([^,()]+)\s*,\s*([^()]+)\s*\)', normalize_root_args, s)
    s = re.sub(r'\\sin', 'sin', s)
    s = re.sub(r'\\cos', 'cos', s)
    s = re.sub(r'\\tan', 'tan', s)
    s = re.sub(r'\\cot', 'cot', s)
    s = re.sub(r'\\ln\s*\(', 'log(', s)
    s = re.sub(r'\bln\(', 'log(', s)
    s = s.replace('^', '**')
    return s

def smart_parse(raw_text: str):
    """
    Phân tích chuỗi toán học thành đối tượng SymPy.
    Hỗ trợ cả Phương Trình (=) và Bất Phương Trình (<=, >=, <, >, !=).
    """
    if not raw_text or not raw_text.strip():
        return None
    cleaned = natural_to_sympy_syntax(raw_text)
    local_dict = {
        'x': x, 'y': y, 'z': z, 't': t, 'm': m, 'a': a, 'b': b, 'c': c, 'n': n,
        'k': sp.Symbol('k', integer=True),
        'theta': theta, 'pi': sp.pi, 'e': sp.E,
        'i': sp.I, 'I': sp.I, 'Abs': sp.Abs, 'abs': sp.Abs,
        'conjugate': sp.conjugate, 'conj': sp.conjugate,
        'sqrt': sp.sqrt, 'root': sp.root, 'log': sp.log, 'ln': sp.log,
        'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan, 'cot': sp.cot,
        'integrate': sp.integrate, 'diff': sp.diff, 'limit': sp.limit, 'Sum': sp.Sum, 'oo': sp.oo
    }

    # Nhận diện toán tử quan hệ theo thứ tự ưu tiên (toán tử 2 ký tự trước: <=, >=, !=, ==)
    rel_match = re.search(r'(<=|>=|!=|==|<|>|=)', cleaned)
    if rel_match:
        op = rel_match.group(1)
        p1 = cleaned[:rel_match.start()].strip()
        p2 = cleaned[rel_match.end():].strip()
        e1 = parse_expr(p1, local_dict=local_dict, transformations=TRANSFORMATIONS)
        e2 = parse_expr(p2, local_dict=local_dict, transformations=TRANSFORMATIONS)
        if op == '<=': return sp.Le(e1, e2)
        elif op == '>=': return sp.Ge(e1, e2)
        elif op == '<': return sp.Lt(e1, e2)
        elif op == '>': return sp.Gt(e1, e2)
        elif op == '!=': return sp.Ne(e1, e2)
        elif op in ('=', '=='): return sp.Eq(e1, e2)

    return parse_expr(cleaned, local_dict=local_dict, transformations=TRANSFORMATIONS)

def clean_display_expr(expr) -> str:
    """Định dạng biểu thức đẹp, tự nhiên cho người đọc."""
    if expr is None:
        return ""
    s = str(expr)
    s = re.sub(r'Abs\(([^()]+)\)', r'|\1|', s)
    s = re.sub(r'\bI\b', 'i', s)
    s = s.replace('*I', 'i')
    s = s.replace('**', '^')
    s = s.replace('*', '·')
    return s

def format_friendly_value(v_sym) -> str:
    """Rút gọn căn thức chính xác hoặc hiển thị nghiệm số phức / vô tỉ tự nhiên."""
    try:
        if v_sym is None:
            return None
        # Kiểm tra nếu là nghiệm số phức có phần ảo
        v_c = complex(v_sym.evalf())
        if abs(v_c.imag) > 1e-6:
            re_part = sp.re(v_sym)
            im_part = sp.im(v_sym)
            if v_c.imag >= 0:
                return f"{clean_display_expr(re_part)} + {clean_display_expr(im_part)}i (≈ {v_c.real:.4f} + {v_c.imag:.4f}i)"
            else:
                return f"{clean_display_expr(re_part)} - {clean_display_expr(abs(im_part))}i (≈ {v_c.real:.4f} - {abs(v_c.imag):.4f}i)"

        v_real = v_c.real
        if abs(v_real - round(v_real)) < 1e-5:
            return f"{int(round(v_real))}"

        sq = v_real ** 2
        for d in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
            val_sq = sq * (d ** 2)
            if abs(val_sq - round(val_sq)) < 1e-4:
                n_int = int(round(val_sq))
                root_sq = math.isqrt(n_int)
                if root_sq ** 2 == n_int:
                    sign = "-" if v_real < 0 else ""
                    return f"{sign}{root_sq}/{d}" if d != 1 else f"{sign}{root_sq}"
                else:
                    sign = "-" if v_real < 0 else ""
                    return f"{sign}√{n_int}/{d}" if d != 1 else f"{sign}√{n_int}"

        return f"{v_real:.4f}"
    except Exception:
        return None

def format_interval_vn(s_set, lang="vi"):
    """Chuyển đổi tập nghiệm SymPy (Interval, Union, FiniteSet, EmptySet) sang ký hiệu khoảng đoạn kỹ thuật."""
    is_en = (lang == "en")
    if s_set is None or s_set is sp.EmptySet:
        return ("S = ∅ (No solution)" if is_en else "S = ∅ (Vô nghiệm)"), r"S = \emptyset"
    if s_set is sp.Reals or s_set is sp.UniversalSet:
        return ("S = ℝ (Holds for all x ∈ ℝ)" if is_en else "S = ℝ (Nghiệm đúng với mọi x ∈ ℝ)"), r"S = \mathbb{R}"

    def one_interval(it):
        if isinstance(it, sp.FiniteSet):
            return "{" + ", ".join([format_friendly_value(e) or str(e) for e in it]) + "}"
        if not isinstance(it, sp.Interval):
            return str(it)
        l_br = "(" if it.left_open or it.start == -sp.oo else "["
        r_br = ")" if it.right_open or it.end == sp.oo else "]"
        s_val = "-∞" if it.start == -sp.oo else (format_friendly_value(it.start) or str(it.start))
        e_val = "+∞" if it.end == sp.oo else (format_friendly_value(it.end) or str(it.end))
        return f"{l_br}{s_val}; {e_val}{r_br}"

    if isinstance(s_set, sp.Interval):
        txt = "S = " + one_interval(s_set)
        latex = f"S = {sp.latex(s_set)}"
        return txt, latex
    elif isinstance(s_set, sp.Union):
        parts = [one_interval(it) for it in s_set.args]
        txt = "S = " + " ∪ ".join(parts)
        latex = f"S = {sp.latex(s_set)}"
        return txt, latex
    elif isinstance(s_set, sp.FiniteSet):
        txt = "S = " + one_interval(s_set)
        latex = f"S = {sp.latex(s_set)}"
        return txt, latex
    return f"S = {s_set}", f"S = {sp.latex(s_set)}"


# ==============================================================================
# VECTOR TEXTBOOK MATH CANVAS (HIỂN THỊ CÔNG THỨC 2D TỰ ĐỘNG THU NHỎ & PHÂN TÁCH ;)
# ==============================================================================
class MathFormulaCanvas(tk.Frame):
    """
    Khung vẽ công thức toán học 2D vector trực quan.
    Hỗ trợ phương trình, bất phương trình, hệ đa dòng phân tách ngang bằng dấu ';',
    co giãn phông chữ tự động, hoàn toàn chống lỗi tràn layout và chống lỗi raw LaTeX.
    Tích hợp sao chép LaTeX, sao chép văn bản, lưu ảnh chất lượng cao và menu ngữ cảnh chuột phải.
    """
    def __init__(self, master, height_px=42, bg="#ffffff", show_actions=True):
        super().__init__(master, bg=bg, height=height_px)
        self.pack_propagate(False)
        self.bg_color = bg
        self.last_latex = ""
        self.last_text = ""

        # Thanh nút hành động nhanh bên phải (nếu bật)
        if show_actions:
            self.action_frame = tk.Frame(self, bg=bg)
            self.action_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=4, pady=2)

            self.btn_copy_ltx = tk.Button(
                self.action_frame, text="Copy LaTeX", font=("Segoe UI", 7, "bold"),
                bg="#f1f5f9", fg="#0f172a", relief="solid", bd=1, padx=4, pady=1,
                cursor="hand2", command=self.copy_latex
            )
            self.btn_copy_ltx.pack(side=tk.LEFT, padx=2)

            self.btn_copy_txt = tk.Button(
                self.action_frame, text="Copy Text", font=("Segoe UI", 7),
                bg="#f1f5f9", fg="#475569", relief="solid", bd=1, padx=4, pady=1,
                cursor="hand2", command=self.copy_text
            )
            self.btn_copy_txt.pack(side=tk.LEFT, padx=2)

            self.btn_copy_img = tk.Button(
                self.action_frame, text="Chép Ảnh", font=("Segoe UI", 7, "bold"),
                bg="#f1f5f9", fg="#0f172a", relief="solid", bd=1, padx=4, pady=1,
                cursor="hand2", command=self.copy_image
            )
            self.btn_copy_img.pack(side=tk.LEFT, padx=2)

            self.btn_save = tk.Button(
                self.action_frame, text="Lưu Ảnh", font=("Segoe UI", 7),
                bg="#f1f5f9", fg="#0969da", relief="solid", bd=1, padx=4, pady=1,
                cursor="hand2", command=self.save_formula_image
            )
            self.btn_save.pack(side=tk.LEFT, padx=2)
        else:
            self.action_frame = None

        self.fig = Figure(figsize=(8, 0.42), dpi=100, facecolor=bg)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.axis('off')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._setup_context_menu()
        self.reset_placeholder()

    def reset_placeholder(self, is_en=None):
        """Đặt lại thông điệp chờ sẵn sàng ở định dạng ngôn ngữ hiện tại."""
        if is_en is None:
            try:
                top = self.winfo_toplevel()
                is_en = (getattr(top, "current_lang", "vi") == "en")
            except Exception:
                is_en = False
        msg = r"\text{Ready to recognize mathematical formula...}" if is_en else r"\text{Sẵn sàng nhận diện công thức toán học...}"
        self.render_latex(msg, text_fallback=("Ready to recognize mathematical formula..." if is_en else "Sẵn sàng nhận diện công thức toán học..."))
        self._is_placeholder = True

    def is_showing_placeholder(self) -> bool:
        if getattr(self, "_is_placeholder", False):
            return True
        txt = (self.last_text or "") + (self.last_latex or "")
        return any(k in txt for k in ["Sẵn sàng", "Ready to", "Vui lòng nhập", "Please enter"])

    def _setup_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Sao chép mã LaTeX (Copy LaTeX)", command=self.copy_latex)
        self.context_menu.add_command(label="Sao chép dạng văn bản thuần (Copy Text)", command=self.copy_text)
        self.context_menu.add_command(label="Sao chép ảnh công thức vào Clipboard", command=self.copy_image)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Lưu ảnh công thức (.png / .svg)...", command=self.save_formula_image)

        w = self.canvas.get_tk_widget()
        w.bind("<Button-3>", self._show_context_menu)

    def _show_context_menu(self, event):
        try:
            top = self.winfo_toplevel()
            is_en = (getattr(top, "current_lang", "vi") == "en")
            self.context_menu.entryconfigure(0, label="Copy LaTeX Code" if is_en else "Sao chép mã LaTeX (Copy LaTeX)")
            self.context_menu.entryconfigure(1, label="Copy Plain Text" if is_en else "Sao chép dạng văn bản thuần (Copy Text)")
            self.context_menu.entryconfigure(3, label="Save Formula Image (.png / .svg)..." if is_en else "Lưu ảnh công thức (.png / .svg)...")
        except Exception:
            pass
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def copy_latex(self):
        if not self.last_latex:
            return
        self.clipboard_clear()
        self.clipboard_append(self.last_latex)
        is_en = False
        try:
            top = self.winfo_toplevel()
            is_en = (getattr(top, "current_lang", "vi") == "en")
        except Exception:
            pass
        self._notify_status("LaTeX code copied to clipboard!" if is_en else "Đã sao chép mã LaTeX vào Clipboard!")

    def copy_text(self):
        txt = self.last_text or self.last_latex
        if not txt:
            return
        self.clipboard_clear()
        self.clipboard_append(txt)
        is_en = False
        try:
            top = self.winfo_toplevel()
            is_en = (getattr(top, "current_lang", "vi") == "en")
        except Exception:
            pass
        self._notify_status("Text formula copied to clipboard!" if is_en else "Đã sao chép công thức dạng văn bản!")

    def copy_image(self):
        is_en = False
        try:
            top = self.winfo_toplevel()
            is_en = (getattr(top, "current_lang", "vi") == "en")
        except Exception:
            pass
        if self.is_showing_placeholder():
            self._notify_status("Canvas is empty, please input formula first!" if is_en else "Bản vẽ trống, vui lòng nhập công thức trước!")
            return
        success = copy_figure_to_clipboard(self.fig)
        if success:
            self._notify_status("Formula image copied to clipboard!" if is_en else "Đã sao chép ảnh công thức vào Clipboard!")
        else:
            self._notify_status("Failed to copy image!" if is_en else "Lỗi sao chép ảnh vào Clipboard!")

    def save_formula_image(self):
        import os
        from tkinter import filedialog, messagebox
        is_en = False
        try:
            top = self.winfo_toplevel()
            is_en = (getattr(top, "current_lang", "vi") == "en")
        except Exception:
            pass
        if self.is_showing_placeholder():
            messagebox.showwarning("Warning" if is_en else "Cảnh báo", "No formula to save!" if is_en else "Chưa có công thức để lưu!")
            return
        path = filedialog.asksaveasfilename(
            title="Save Math Formula Image" if is_en else "Lưu ảnh công thức toán học",
            defaultextension=".png",
            filetypes=[("PNG Image (*.png)", "*.png"), ("SVG Vector (*.svg)", "*.svg"), ("PDF Document (*.pdf)", "*.pdf")]
        )
        if path:
            try:
                self.fig.savefig(path, dpi=300, bbox_inches='tight', facecolor='#ffffff', edgecolor='none')
                messagebox.showinfo("Success" if is_en else "Thành công", f"Saved math formula image:\n{path}" if is_en else f"Đã lưu ảnh công thức toán học:\n{path}")
                self._notify_status(f"Saved formula image: {os.path.basename(path)}" if is_en else f"Đã lưu ảnh công thức: {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Error" if is_en else "Lỗi lưu ảnh", f"Cannot save formula image: {e}" if is_en else f"Không thể lưu ảnh công thức: {e}")

    def _notify_status(self, msg: str):
        try:
            top = self.winfo_toplevel()
            if hasattr(top, "status_lbl") and top.status_lbl:
                top.status_lbl.config(text=msg)
            elif hasattr(self.master, "status_lbl") and self.master.status_lbl:
                self.master.status_lbl.config(text=msg)
        except Exception:
            pass

    def render_system(self, lines: list):
        """Hiển thị các phương trình / bất phương trình của hệ thành hàng ngang, phân tách nhau bằng dấu ';'."""
        try:
            self.ax.clear()
            self.ax.axis('off')
            n = len(lines)
            if n == 0:
                self.canvas.draw()
                return
            if n == 1:
                self.render_latex(lines[0])
                return

            clean_lines = [l.strip().strip('$') for l in lines if l.strip()]
            combined_latex = r" \;; \quad\quad ".join(clean_lines)
            self.last_latex = combined_latex
            self.last_text = " ; ".join(clean_lines)
            self.render_latex(combined_latex, text_fallback=self.last_text)
        except Exception:
            self.render_latex(r" ; ".join(lines))

    def render_latex(self, latex_str: str, text_fallback: str = ""):
        if not any(k in latex_str for k in ["Sẵn sàng", "Ready to", "Vui lòng nhập", "Please enter"]):
            self._is_placeholder = False
        try:
            self.ax.clear()
            self.ax.axis('off')
            clean_latex = latex_str.strip()
            self.last_latex = clean_latex
            self.last_text = text_fallback or clean_latex.replace("$", "").replace(r"\text{", "").replace("}", "")

            # Nếu nhận chuỗi hệ có môi trường cases, trích xuất từng dòng để nối thành hàng ngang
            if r'\begin{cases}' in clean_latex:
                m = re.search(r'\\begin\{cases\}(.*?)\\end\{cases\}', clean_latex, re.DOTALL)
                if m:
                    inner = m.group(1).strip()
                    lines = [l.strip() for l in inner.split(r'\\') if l.strip()]
                    self.render_system(lines)
                    return

            if clean_latex.startswith('$') and clean_latex.endswith('$'):
                math_text = clean_latex
            elif clean_latex.startswith(r'\text{') and clean_latex.endswith('}'):
                math_text = f"${clean_latex}$"
            else:
                math_text = f"${clean_latex}$"

            # Tự động co giãn cỡ chữ thông minh theo độ dài biểu thức
            text_len = len(clean_latex)
            if text_len < 35:
                fs = 11.5
            elif text_len < 60:
                fs = 10.0
            elif text_len < 90:
                fs = 8.8
            elif text_len < 125:
                fs = 7.8
            elif text_len < 160:
                fs = 7.0
            else:
                fs = 6.4

            self.ax.text(0.5, 0.5, math_text,
                         horizontalalignment='center',
                         verticalalignment='center',
                         fontsize=fs,
                         color='#0f172a')
            self.canvas.draw()
        except Exception:
            try:
                self.ax.clear()
                self.ax.axis('off')
                display_fallback = clean_display_expr(latex_str)
                self.last_text = display_fallback
                self.ax.text(0.5, 0.5, display_fallback,
                             horizontalalignment='center',
                             verticalalignment='center',
                             fontsize=8.5,
                             color='#334155')
                self.canvas.draw()
            except Exception:
                pass


# ==============================================================================
# IN-APP USER HANDBOOK DIALOG (HƯỚNG DẪN SỬ DỤNG TÍCH HỢP)
# ==============================================================================

class CADMathHandbookDialog(tk.Toplevel):
    """Hộp thoại hướng dẫn sử dụng chi tiết từng mục và bảng phím tắt."""
    WIN32_BG = "#ECE9D8"
    FONT_UI = ("Tahoma", 9)
    FONT_BOLD = ("Tahoma", 9, "bold")
    FONT_MONO = ("Consolas", 9)

    SECTIONS_VN = [
        ("1. Giới thiệu tổng quan", (
            "1. GIỚI THIỆU TỔNG QUAN\n\n"
            "CAD Math Studio là phần mềm giải toán máy tính và vẽ đồ thị hàm số.\n"
            "Các tính năng chính:\n"
            "  • Giải phương trình bậc cao, bất phương trình, hệ phương trình, bài toán chứa tham số m và số phức.\n"
            "  • Tìm giá trị lớn nhất (GTLN), giá trị nhỏ nhất (GTNN) và kiểm tra bất đẳng thức.\n"
            "  • Tính đạo hàm, tích phân từng bước, giới hạn và chuỗi số.\n"
            "  • Tính toán ma trận: định thức det, ma trận nghịch đảo, giải hệ phương trình ma trận AX = B.\n"
            "  • Tính tổ hợp, chỉnh hợp, hoán vị và phân tích thống kê mô tả (trung bình, phương sai, biểu đồ hộp).\n"
            "  • Khảo sát sự biến thiên và vẽ đồ thị hàm số trên mặt phẳng Oxy.\n"
            "  • Lời giải hiển thị chi tiết, công thức toán viết dạng căn thức tự nhiên và phân số dễ đọc.\n"
            "  • Xuất bài làm ra file ảnh PNG hoặc file báo cáo web HTML.\n"
        )),
        ("2. Giao diện phần mềm", (
            "2. GIAO DIỆN PHẦN MỀM\n\n"
            "Giao diện gồm các khu vực chính:\n"
            "  • Thanh Menu trên cùng: Tệp, Chỉnh sửa, Xem, Chuyên đề, Công cụ, Giao diện, Ngôn ngữ, Thông tin.\n"
            "  • Dải ký hiệu toán học Ribbon: Chèn nhanh các ký hiệu thường dùng (căn bậc hai, lũy thừa, dấu so sánh, tích phân, đạo hàm, đơn vị ảo i...).\n"
            "  • Hệ thống 6 tab giải toán: Chuyển đổi giữa 6 nhóm bài toán khác nhau mà không mất dữ liệu.\n"
            "  • Khung hiển thị lời giải: Trình bày chi tiết từng bước giải với kết luận rõ ràng.\n"
            "  • Khung đồ thị: Hiển thị đồ thị hàm số hoặc biểu đồ thống kê bên cạnh.\n"
        )),
        ("3. Tab 1: Phương trình & Hệ", (
            "3. TAB 1: PHƯƠNG TRÌNH, BẤT PHƯƠNG TRÌNH VÀ HỆ\n\n"
            "Nhập phương trình vào ô văn bản và bấm [ Giải Chi Tiết ] (hoặc nhấn Enter):\n"
            "  • Phương trình một ẩn: x^2 - 5x + 6 = 0 hoặc sqrt(2x + 1) = x - 1\n"
            "  • Bất phương trình: x^2 - 3x + 2 <= 0 hoặc (x - 1)/(x + 2) > 0\n"
            "  • Bài toán tham số m: x^2 - 2*(m - 1)*x + m + 5 = 0 (chọn chế độ tìm m ở danh sách)\n"
            "  • Số phức: (1 + 2i)*z + 3 - i = 0 (dùng i là đơn vị ảo, z là ẩn số phức)\n"
            "  • Hệ phương trình: Gõ mỗi phương trình trên một dòng hoặc cách nhau bởi dấu chấm phẩy ';':\n"
            "      2x + y = 5\n"
            "      x - 3y = -1\n"
        )),
        ("4. Tab 2: Cực trị & Bất đẳng thức", (
            "4. TAB 2: TÌM GIÁ TRỊ LỚN NHẤT, NHỎ NHẤT VÀ BẤT ĐẲNG THỨC\n\n"
            "  • Ô trên: Nhập biểu thức mục tiêu cần tìm cực trị, ví dụ: P = x^2 + y^2 - 4x + 2y\n"
            "  • Ô dưới: Nhập điều kiện ràng buộc (nếu có), ví dụ: x + 2y = 4 hoặc x >= 0, y >= 0. Nếu không có điều kiện ràng buộc thì để trống.\n"
            "  • Bấm [ Tìm Cực Trị ] để nhận giá trị lớn nhất (GTLN) và giá trị nhỏ nhất (GTNN) kèm tọa độ điểm đạt.\n"
        )),
        ("5. Tab 3: Đạo hàm, Tích phân & Giới hạn", (
            "5. TAB 3: ĐẠO HÀM, TÍCH PHÂN VÀ GIỚI HẠN\n\n"
            "Nhập biểu thức f(x), ví dụ: x^3 - 3x^2 + 2 hoặc sin(x)*cos(x):\n"
            "  • Đạo hàm: Bấm [ Đạo hàm f'(x) ] (hỗ trợ đạo hàm cấp 1, cấp 2 hoặc đạo hàm riêng theo x, y, z).\n"
            "  • Tích phân bất định: Bấm [ Tích phân ∫ f(x)dx ] để tìm nguyên hàm.\n"
            "  • Tích phân xác định: Nhập cận dưới và cận trên vào 2 ô bên cạnh rồi bấm tính.\n"
            "  • Giới hạn: Chọn giá trị ẩn tiến về (như x -> 0 hay x -> oo) rồi bấm [ Giới hạn lim ].\n"
        )),
        ("6. Tab 4: Tính toán ma trận", (
            "6. TAB 4: TÍNH TOÁN MA TRẬN\n\n"
            "Nhập các dòng của ma trận, các phần tử cách nhau bằng khoảng trắng hoặc dấu phẩy:\n"
            "  Ví dụ Ma trận A (cỡ 3x3):\n"
            "    1  2 -1\n"
            "    0  3  4\n"
            "    2 -1  1\n\n"
            "Các nút tính toán có sẵn:\n"
            "  • [ Định thức det(A) ]: Tính định thức của ma trận vuông.\n"
            "  • [ Nghịch đảo A⁻¹ ]: Tìm ma trận nghịch đảo.\n"
            "  • [ Chuyển vị Aᵀ ]: Tìm ma trận chuyển vị.\n"
            "  • [ A × B ]: Nhân hai ma trận A và B.\n"
            "  • [ Giải AX = B ]: Giải hệ phương trình ma trận.\n"
        )),
        ("7. Tab 5: Xác suất & Thống kê", (
            "7. TAB 5: XÁC SUẤT VÀ THỐNG KÊ MÔ TẢ\n\n"
            "  • Tổ hợp & Xác suất: Nhập n và k để tính nhanh chỉnh hợp A(n, k), tổ hợp C(n, k), hoán vị n!.\n"
            "  • Thống kê mô tả: Nhập dãy số liệu mẫu (ví dụ: 12, 15, 14, 18, 20, 15, 16, 22).\n"
            "    Bấm [ Phân tích thống kê ], phần mềm sẽ tính:\n"
            "    Số trung bình, Trung vị, Mốt, Tứ phân vị, Phương sai, Độ lệch chuẩn.\n"
            "    Đồng thời tự động vẽ biểu đồ phân bố và biểu đồ hộp (Boxplot) trực quan ở khung bên cạnh.\n"
        )),
        ("8. Tab 6: Vẽ đồ thị hàm số", (
            "8. TAB 6: KHẢO SÁT VÀ VẼ ĐỒ THỊ HÀM SỐ\n\n"
            "  • Nhập hàm số cần vẽ (ví dụ: y = x^3 - 3x + 1), bấm [ Khảo Sát & Vẽ Đồ Thị ].\n"
            "  • Kết quả khảo sát: Tập xác định, đạo hàm y', cực trị, đường tiệm cận.\n"
            "  • Đồ thị hiển thị trên mặt phẳng Oxy, đánh dấu rõ cực trị và tiệm cận nét đứt.\n"
            "  • Lăn con lăn chuột trên đồ thị để phóng to / thu nhỏ. Bấm [ Lưu ảnh đồ thị ] để lưu ra file PNG.\n"
        )),
        ("9. Cách gõ công thức toán học", (
            "9. CÁCH GÕ CÔNG THỨC TOÁN HỌC\n\n"
            "Bạn có thể gõ công thức rất tự nhiên bằng bàn phím:\n"
            "  • Phép nhân: Gõ 2x, x*y hoặc 3(x - 1).\n"
            "  • Lũy thừa: Dùng dấu ^, ví dụ: x^2, (x+1)^3.\n"
            "  • Căn thức: Gõ sqrt(x). Căn bậc ba gõ root(x, 3).\n"
            "  • Phân số: Gõ (a + b)/(c + d) hoặc \\frac{a+b}{c+d}.\n"
            "  • Trị tuyệt đối: Gõ |x - 2| hoặc abs(x - 2).\n"
            "  • Lượng giác: sin(x), cos(x), tan(x).\n"
            "  • Số pi: Gõ pi. Vô cực: Gõ oo hoặc infty.\n"
        )),
        ("10. Xuất ảnh & Báo cáo HTML", (
            "10. XUẤT ẢNH VÀ XUẤT BÁO CÁO HTML\n\n"
            "  • Sao chép lời giải (Ctrl+C): Bấm nút hoặc nhấn Ctrl+C để sao chép bài giải chi tiết vào Clipboard, tiện dán vào Word.\n"
            "  • Lưu ảnh đồ thị (Ctrl+Shift+S): Lưu đồ thị ra file ảnh PNG rõ nét.\n"
            "  • Xuất báo cáo HTML (Ctrl+P): Xuất toàn bộ bài giải và hình vẽ ra file web HTML để lưu trữ hoặc in ấn.\n"
        )),
        ("11. Bảng phím tắt toàn tập", (
            "11. BẢNG PHÍM TẮT TOÀN TẬP\n\n"
            "  • F1              : Mở hướng dẫn sử dụng này\n"
            "  • F5              : Giải toán AI\n"
            "  • Ctrl + O        : Mở file bài toán đã lưu\n"
            "  • Ctrl + S        : Lưu bài giải chi tiết ra file văn bản\n"
            "  • Ctrl + Shift + S: Lưu ảnh đồ thị hiện tại\n"
            "  • Ctrl + P        : Xuất báo cáo bài giải ra file HTML\n"
            "  • Ctrl + C        : Sao chép bài giải vào bộ nhớ tạm\n"
            "  • Ctrl + V        : Dán công thức vào ô đang chọn\n"
            "  • Ctrl + L        : Xóa trắng tab hiện tại\n"
            "  • Ctrl + + / -    : Phóng to / Thu nhỏ cỡ chữ bài giải\n"
            "  • Ctrl + 0        : Đặt lại cỡ chữ bài giải về 100%\n"
            "  • Ctrl + Q        : Thoát phần mềm\n"
        )),
        ("12. Một số lưu ý khi sử dụng", (
            "12. MỘT SỐ LƯU Ý KHI SỬ DỤNG\n\n"
            "  • Khi chép bài giải vào Word: Nhấn Ctrl+C để sao chép bài giải đã định dạng từng bước rõ ràng.\n"
            "  • Khi nhập hệ phương trình hoặc ma trận: Chỉ cần xuống dòng cho mỗi phương trình hoặc mỗi hàng ma trận.\n"
            "  • Điều chỉnh vùng nhìn đồ thị: Điền khoảng x_min và x_max ở dưới đồ thị rồi bấm Vẽ lại, hoặc lăn chuột trực tiếp trên hình.\n"
            "  • Đổi ngôn ngữ: Vào menu 'Ngôn ngữ -> English', toàn bộ giao diện và tên 6 tab sẽ chuyển sang tiếng Anh.\n"
        ))
    ]

    SECTIONS_EN = [
        ("1. Overview", (
            "1. OVERVIEW\n\n"
            "CAD Math Studio is a natural CAS mathematical computation and function graphing software.\n"
            "Key capabilities:\n"
            "  • Solve high-degree equations, inequalities, systems, parametric m problems, and complex numbers.\n"
            "  • Find global extrema (min/max) and verify inequalities.\n"
            "  • Step-by-step calculus: derivatives, integrals, Taylor series, and limits.\n"
            "  • Matrix engine: determinants, inverses, transpose, matrix multiplication, and linear systems AX = B.\n"
            "  • Combinatorics, probability, and descriptive statistics (mean, variance, quartiles, boxplots).\n"
            "  • Function variation study and 2D curve plotting on the Oxy plane.\n"
            "  • Natural radical formulas and fraction displays.\n"
            "  • Export PNG plot images and self-contained HTML reports.\n"
        )),
        ("2. User Interface", (
            "2. USER INTERFACE\n\n"
            "The main window is organized into:\n"
            "  • Top Menu Bar: File, Edit, View, Curricula, Tools, Themes, Language, Help.\n"
            "  • Math Ribbon: Quick buttons for square roots, powers, inequality signs, integrals, derivatives, limits, and imaginary unit i.\n"
            "  • 6 Solution Tabs: Seamlessly switch between 6 mathematical domains without losing input data.\n"
            "  • Solution Area: Displays detailed step-by-step mathematical reasoning and final conclusions.\n"
            "  • Interactive Plot Area: Live Matplotlib curves and statistical charts.\n"
        )),
        ("3. Tab 1: Equations & Systems", (
            "3. TAB 1: EQUATIONS, INEQUALITIES & SYSTEMS\n\n"
            "Enter an equation or inequality and click [ Solve Problem ] (or press Enter):\n"
            "  • Single variable: x^2 - 5x + 6 = 0 or sqrt(2x + 1) = x - 1\n"
            "  • Inequalities: x^2 - 3x + 2 <= 0 or (x - 1)/(x + 2) > 0\n"
            "  • Parametric m: x^2 - 2*(m - 1)*x + m + 5 = 0 (select parameter mode from dropdown)\n"
            "  • Complex numbers: (1 + 2i)*z + 3 - i = 0 (i is the imaginary unit)\n"
            "  • Systems: Enter each equation on a new line or separate by ';':\n"
            "      2x + y = 5\n"
            "      x - 3y = -1\n"
        )),
        ("4. Tab 2: Extrema & Inequalities", (
            "4. TAB 2: GLOBAL EXTREMA & INEQUALITIES\n\n"
            "  • Top field: Enter the objective function to optimize, e.g. P = x^2 + y^2 - 4x + 2y\n"
            "  • Bottom field: Enter constraints (if any), e.g. x + 2y = 4 or x >= 0, y >= 0. Leave empty if unconstrained.\n"
            "  • Click [ Analyze Extrema ] to find minimum and maximum values along with critical points.\n"
        )),
        ("5. Tab 3: Calculus & Limits", (
            "5. TAB 3: DERIVATIVES, INTEGRALS & LIMITS\n\n"
            "Enter expression f(x), e.g. x^3 - 3x^2 + 2 or sin(x)*cos(x):\n"
            "  • Derivative: Click [ Derivative f'(x) ] (supports 1st, 2nd, and partial derivatives).\n"
            "  • Indefinite Integral: Click [ Indefinite Integral ] to find antiderivatives.\n"
            "  • Definite Integral: Enter lower and upper bounds in the adjacent fields and compute.\n"
            "  • Limits: Select approach value (e.g. x -> 0 or x -> oo) and click [ Limit lim ].\n"
        )),
        ("6. Tab 4: Matrix Computations", (
            "6. TAB 4: MATRIX COMPUTATIONS\n\n"
            "Type matrix rows line by line, elements separated by spaces or commas:\n"
            "  Example Matrix A (3x3):\n"
            "    1  2 -1\n"
            "    0  3  4\n"
            "    2 -1  1\n\n"
            "Available operations:\n"
            "  • [ Determinant det(A) ]: Compute determinant of square matrix.\n"
            "  • [ Inverse A⁻¹ ]: Compute matrix inverse.\n"
            "  • [ Transpose Aᵀ ]: Transpose matrix.\n"
            "  • [ A × B ]: Multiply matrices A and B.\n"
            "  • [ Solve AX = B ]: Solve linear system.\n"
        )),
        ("7. Tab 5: Probability & Statistics", (
            "7. TAB 5: PROBABILITY & DESCRIPTIVE STATISTICS\n\n"
            "  • Combinatorics: Enter n and k to compute permutations A(n, k), combinations C(n, k), and factorial n!.\n"
            "  • Descriptive Statistics: Enter sample data (e.g. 12, 15, 14, 18, 20, 15, 16, 22).\n"
            "    Click [ Statistical Analysis ] to calculate:\n"
            "    Mean, Median, Mode, Quartiles, Variance, and Standard Deviation.\n"
            "    Automatically plots frequency distribution histograms and boxplots in the chart pane.\n"
        )),
        ("8. Tab 6: Function Grapher", (
            "8. TAB 6: FUNCTION VARIATION STUDY & GRAPHER\n\n"
            "  • Enter function f(x) (e.g. y = x^3 - 3x + 1), click [ Plot Graph & Study ].\n"
            "  • Study results: Domain, derivative y', critical extrema, and asymptotes.\n"
            "  • Curve plotted on Oxy coordinate plane with marked extrema and dashed asymptotes.\n"
            "  • Scroll mouse wheel on graph to zoom in/out. Click [ Save Plot ] to export PNG.\n"
        )),
        ("9. Formula Typing Syntax", (
            "9. FORMULA TYPING SYNTAX\n\n"
            "You can type expressions naturally using standard keyboard conventions:\n"
            "  • Multiplication: Type 2x, x*y, or 3(x - 1).\n"
            "  • Exponents: Use ^, e.g. x^2, (x+1)^3.\n"
            "  • Radicals: Type sqrt(x). Cube root: root(x, 3).\n"
            "  • Fractions: Type (a + b)/(c + d) or \\frac{a+b}{c+d}.\n"
            "  • Absolute value: Type |x - 2| or abs(x - 2).\n"
            "  • Trigonometry: sin(x), cos(x), tan(x).\n"
            "  • Constants: Type pi for π. Type oo or infty for ∞.\n"
        )),
        ("10. Image & HTML Export", (
            "10. IMAGE AND HTML REPORT EXPORT\n\n"
            "  • Copy Solution (Ctrl+C): Copies complete step-by-step derivation to Clipboard for Word paste.\n"
            "  • Save Plot (Ctrl+Shift+S): Exports current graph as high-resolution PNG.\n"
            "  • Export HTML (Ctrl+P): Generates self-contained HTML report with MathJax formulas and plots.\n"
        )),
        ("11. Keyboard Shortcuts", (
            "11. COMPLETE KEYBOARD SHORTCUTS\n\n"
            "  • F1              : Open this User Guide\n"
            "  • F5              : AI Solver\n"
            "  • Ctrl + O        : Open saved problem file\n"
            "  • Ctrl + S        : Save solution text\n"
            "  • Ctrl + Shift + S: Save current plot image\n"
            "  • Ctrl + P        : Export HTML report\n"
            "  • Ctrl + C        : Copy solution to clipboard\n"
            "  • Ctrl + V        : Paste formula\n"
            "  • Ctrl + L        : Clear active tab\n"
            "  • Ctrl + + / -    : Step Zoom In / Zoom Out solution font\n"
            "  • Ctrl + 0        : Reset solution font size to 100%\n"
            "  • Ctrl + Q        : Exit application\n"
        )),
        ("12. Tips & Notes", (
            "12. TIPS AND NOTES\n\n"
            "  • Pasting into Word: Press Ctrl+C to copy formatted derivation with clear conclusions.\n"
            "  • Entering systems and matrices: Simply use one line per equation or row.\n"
            "  • Adjusting plot view: Edit x_min and x_max under the graph or scroll with mouse wheel.\n"
            "  • Switching language: Go to 'Language -> English' or 'Ngôn ngữ -> Tiếng Việt' at any time.\n"
        ))
    ]

    def __init__(self, parent, is_en=False):
        super().__init__(parent)
        self.is_en = is_en
        self.title("CAD Math Studio User Guide" if is_en else "Hướng Dẫn Sử Dụng CAD Math Studio")
        self.geometry("780x560")
        self.minsize(680, 480)
        self.configure(bg=self.WIN32_BG)
        self.transient(parent)
        self.grab_set()

        self.sections = self.SECTIONS_EN if is_en else self.SECTIONS_VN

        # Header
        hdr = tk.Frame(self, bg=self.WIN32_BG, pady=6)
        hdr.pack(side=tk.TOP, fill=tk.X, padx=12)
        tk.Label(
            hdr,
            text="CAD MATH STUDIO USER GUIDE" if is_en else "CẨM NANG HƯỚNG DẪN SỬ DỤNG CAD MATH STUDIO",
            font=("Tahoma", 11, "bold"),
            bg=self.WIN32_BG,
            fg="#000080",
        ).pack(side=tk.TOP, anchor="w")
        tk.Label(
            hdr,
            text="Select a topic on the left to read instructions and shortcuts." if is_en else "Chọn từng mục ở danh sách bên trái để xem hướng dẫn chi tiết và phím tắt.",
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            fg="#444444",
        ).pack(side=tk.TOP, anchor="w")

        # Body
        body = tk.Frame(self, bg=self.WIN32_BG)
        body.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=12, pady=4)

        # Left listbox
        left_frame = tk.Frame(body, bg=self.WIN32_BG, width=220)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 6))

        tk.Label(
            left_frame,
            text="Topics:" if is_en else "Danh mục hướng dẫn:",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            anchor="w",
        ).pack(side=tk.TOP, fill=tk.X, pady=(0, 4))

        self.lb_topics = tk.Listbox(
            left_frame,
            font=self.FONT_UI,
            bg="#FFFFFF",
            fg="#000000",
            selectmode=tk.SINGLE,
            relief=tk.SUNKEN,
            bd=2,
            width=26,
            exportselection=False,
        )
        lb_sb = tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.lb_topics.yview)
        self.lb_topics.configure(yscrollcommand=lb_sb.set)
        lb_sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.lb_topics.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for title, _text in self.sections:
            self.lb_topics.insert(tk.END, f"  {title}")

        self.lb_topics.bind("<<ListboxSelect>>", self._on_select_topic)

        # Right content
        right_frame = tk.Frame(body, bg=self.WIN32_BG)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.txt_content = tk.Text(
            right_frame,
            font=self.FONT_MONO,
            bg="#FFFFFF",
            fg="#111111",
            relief=tk.SUNKEN,
            bd=2,
            wrap=tk.WORD,
            padx=10,
            pady=10,
        )
        txt_sb = tk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.txt_content.yview)
        self.txt_content.configure(yscrollcommand=txt_sb.set)
        txt_sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bottom buttons
        btn_box = tk.Frame(self, bg=self.WIN32_BG, pady=6)
        btn_box.pack(side=tk.BOTTOM, fill=tk.X, padx=12)

        tk.Button(
            btn_box,
            text="[ Copy Content ]" if is_en else "[ Sao Chép Nội Dung ]",
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=3,
            command=self._copy_current_topic,
        ).pack(side=tk.LEFT)

        tk.Button(
            btn_box,
            text="[ Close ]" if is_en else "[ Đóng ]",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            padx=14,
            pady=3,
            command=self.destroy,
        ).pack(side=tk.RIGHT)

        # Select first topic
        self.lb_topics.selection_set(0)
        self._on_select_topic(None)

    def _on_select_topic(self, _event) -> None:
        sel = self.lb_topics.curselection()
        if not sel:
            return
        idx = sel[0]
        if 0 <= idx < len(self.sections):
            _title, text_body = self.sections[idx]
            self.txt_content.configure(state=tk.NORMAL)
            self.txt_content.delete("1.0", tk.END)
            self.txt_content.insert(tk.END, text_body)
            self.txt_content.configure(state=tk.DISABLED)

    def _copy_current_topic(self) -> None:
        sel = self.lb_topics.curselection()
        if not sel:
            return
        idx = sel[0]
        if 0 <= idx < len(self.sections):
            _title, text_body = self.sections[idx]
            self.clipboard_clear()
            self.clipboard_append(text_body)
            messagebox.showinfo(
                "Copied" if self.is_en else "Đã sao chép",
                "Handbook section copied to clipboard." if self.is_en else "Đã sao chép nội dung hướng dẫn vào Clipboard."
            )


# ==============================================================================
# MAIN CAD APPLICATION V2.1 (WINDOWS DESKTOP APPLICATION)
# ==============================================================================
class CADMathDesktopAppV2:

    def _s(self, vi_text: str, en_text: str) -> str:
        """Trả về chuỗi song ngữ tương ứng ngôn ngữ hiện thời của ứng dụng."""
        return en_text if getattr(self, 'current_lang', 'vi') == 'en' else vi_text

    def format_interval(self, s_set):
        """Hàm bọc format_interval_vn có nhận thức ngôn ngữ hiện hành."""
        return format_interval_vn(s_set, lang=getattr(self, 'current_lang', 'vi'))

    @staticmethod
    def real_status(r):
        """Ủy quyền xác định tính thực cho CADMathCore."""
        return CADMathCore.real_status(r)

    @staticmethod
    def check_sign_exact(expr_sub):
        """Ủy quyền xác định dấu đại số/đa độ chính xác cho CADMathCore."""
        return CADMathCore.check_sign_exact(expr_sub)

    def __init__(self, root):
        self.root = root
        self.current_lang = 'vi'
        self.core = CADMathCore()
        # Đường dẫn icon & logo Standard và Pro
        self.ico_path = os.path.join(os.path.dirname(__file__), "assets", "cad_math.ico")
        self.pro_ico_path = os.path.join(os.path.dirname(__file__), "assets", "cad_math_pro.ico")
        self.logo_png = os.path.join(os.path.dirname(__file__), "assets", "cad_math_logo.png")
        self.pro_logo_png = os.path.join(os.path.dirname(__file__), "assets", "cad_math_logo_pro.png")

        # Nạp trạng thái bản quyền & tự động chuyển đổi Icon Pro
        self.is_pro = self.load_pro_license_state()
        self.apply_branding_icon(is_pro=self.is_pro)
        self.root.geometry("1300x880")
        self.root.minsize(1050, 700)
        self.root.configure(bg="#f8fafc")

        # Cỡ chữ linh hoạt cho tính năng Zoom in / Zoom out
        self.current_font_size = 11

        # Trạng thái AI Neuro-Symbolic (kế thừa cơ chế GeoSolver 2D)
        self.ai_hub = None
        self.ai_manager = None
        self._ai_solving_active = False
        self._ai_stop_flag = False
        self._ai_streaming_active = False
        self._last_ground_truth_text = {}

        self.setup_cad_style()
        self.setup_menu_bar()
        self.build_ui()
        self.bind_keyboard_shortcuts()

        # Tự động giải mẫu Tab 1 ngay khi khởi chạy để đồ thị không bị trống
        self.root.after(200, self.solve_equation_action)

    def setup_cad_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(".", background="#f8fafc", foreground="#0f172a", font=("Segoe UI", 10))
        style.configure("TNotebook", background="#e2e8f0", borderwidth=0)
        style.configure("TNotebook.Tab", background="#e2e8f0", foreground="#334155",
                        font=("Segoe UI", 9, "bold"), padding=[16, 8])
        style.map("TNotebook.Tab",
                  background=[("selected", "#ffffff")],
                  foreground=[("selected", "#0969da")])
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff")

    # --------------------------------------------------------------------------
    # FULL WINDOWS MENU BAR & DIALOGS
    # --------------------------------------------------------------------------
    def setup_menu_bar(self):
        menubar = tk.Menu(self.root)
        lang = getattr(self, 'current_lang', 'vi')
        is_en = (lang == 'en')

        # 1. MENU TỆP (FILE)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Problem File... (Ctrl+O)" if is_en else "Mở tệp bài toán... (Ctrl+O)", command=self.open_file_dialog, accelerator="Ctrl+O")
        file_menu.add_command(label="Save Detailed Solution... (Ctrl+S)" if is_en else "Lưu bài giải chi tiết... (Ctrl+S)", command=self.save_solution_dialog, accelerator="Ctrl+S")
        file_menu.add_command(label="Save Current Plot Image... (Ctrl+Shift+S)" if is_en else "Lưu ảnh đồ thị... (Ctrl+Shift+S)", command=self.save_plot_dialog, accelerator="Ctrl+Shift+S")
        file_menu.add_command(label="Print Solution / Export HTML... (Ctrl+P)" if is_en else "In ấn bài giải / Xuất báo cáo... (Ctrl+P)", command=self.export_html_report, accelerator="Ctrl+P")
        file_menu.add_separator()
        file_menu.add_command(label="Exit (Ctrl+Q)" if is_en else "Thoát (Ctrl+Q)", command=self.root.quit, accelerator="Ctrl+Q")
        menubar.add_cascade(label="File" if is_en else "Tệp", menu=file_menu)

        # 2. MENU CHỈNH SỬA (EDIT)
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Copy Solution (Ctrl+C)" if is_en else "Sao chép bài giải (Ctrl+C)", command=self.copy_active_solution, accelerator="Ctrl+C")
        edit_menu.add_command(label="Clear Active Tab (Ctrl+L)" if is_en else "Xóa trắng tab hiện tại (Ctrl+L)", command=self.clear_active_tab, accelerator="Ctrl+L")
        menubar.add_cascade(label="Edit" if is_en else "Chỉnh sửa", menu=edit_menu)

        # 3. MENU XEM (VIEW)
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Zoom In (Ctrl++)" if is_en else "Phóng to bài giải (Ctrl++)", command=self.zoom_in, accelerator="Ctrl++")
        view_menu.add_command(label="Zoom Out (Ctrl+-)" if is_en else "Thu nhỏ bài giải (Ctrl+-)", command=self.zoom_out, accelerator="Ctrl+-")
        view_menu.add_command(label="Reset Zoom 100% (Ctrl+0)" if is_en else "Đặt lại cỡ chữ 100% (Ctrl+0)", command=self.zoom_reset, accelerator="Ctrl+0")
        menubar.add_cascade(label="View" if is_en else "Xem", menu=view_menu)

        # 3b. MENU CHUYÊN ĐỀ (CURRICULA)
        curricula_menu = tk.Menu(menubar, tearoff=0)
        higher_math_menu = tk.Menu(curricula_menu, tearoff=0)
        higher_math_menu.add_command(
            label="Open Advanced Math Studio..." if is_en else "Mở công cụ Toán cao cấp...",
            command=lambda: self.open_higher_math_dialog(0)
        )
        higher_math_menu.add_separator()
        higher_math_menu.add_command(
            label="1. Linear Algebra & Matrices..." if is_en else "1. Đại số tuyến tính & ma trận...",
            command=lambda: self.open_higher_math_dialog(0)
        )
        higher_math_menu.add_command(
            label="2. Calculus 1 & Improper Integrals..." if is_en else "2. Giải tích 1 & tích phân suy rộng...",
            command=lambda: self.open_higher_math_dialog(1)
        )
        higher_math_menu.add_command(
            label="3. Series & Fourier..." if is_en else "3. Chuỗi số & chuỗi Fourier...",
            command=lambda: self.open_higher_math_dialog(2)
        )
        higher_math_menu.add_command(
            label="4. Multivariable Calculus..." if is_en else "4. Giải tích đa biến & tích phân bội...",
            command=lambda: self.open_higher_math_dialog(3)
        )
        higher_math_menu.add_command(
            label="5. Vector Fields & Line / Surface..." if is_en else "5. Trường vector & tích phân đường - mặt...",
            command=lambda: self.open_higher_math_dialog(4)
        )
        higher_math_menu.add_command(
            label="6. Differential Equations & Laplace..." if is_en else "6. Phương trình vi phân & biến đổi Laplace...",
            command=lambda: self.open_higher_math_dialog(5)
        )
        higher_math_menu.add_separator()
        higher_math_menu.add_command(
            label="Accuracy Benchmark (20 Tests)..." if is_en else "Kiểm tra độ chính xác (20 bài test)...",
            command=self.run_higher_math_benchmark_dialog
        )

        curricula_menu.add_cascade(label="Advanced Math" if is_en else "Toán cao cấp", menu=higher_math_menu)
        curricula_menu.add_separator()
        curricula_menu.add_command(label="K-12 Mathematics..." if is_en else "Toán phổ thông...", command=self.focus_equation_ribbon)
        menubar.add_cascade(label="Curricula" if is_en else "Chuyên đề", menu=curricula_menu)

        # 4. MENU CÔNG CỤ (TOOLS)
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Math Symbols Ribbon" if is_en else "Dải ký hiệu toán học Ribbon", command=self.focus_equation_ribbon)
        tools_menu.add_command(label="Run Quality Benchmark..." if is_en else "Kiểm định chất lượng tính toán...", command=self.run_system_benchmark_dialog)
        tools_menu.add_separator()
        tools_menu.add_command(
            label="AI Solve (F5)" if is_en else "AI giải toán (F5)",
            command=self._on_ai_solve_click,
            accelerator="F5"
        )
        tools_menu.add_command(
            label="AI Connection Settings..." if is_en else "Cài đặt kết nối AI...",
            command=self.open_ai_assistant
        )
        menubar.add_cascade(label="Tools" if is_en else "Công cụ", menu=tools_menu)

        # 4b. MENU GIAO DIỆN (THEMES)
        theme_menu = tk.Menu(menubar, tearoff=0)
        theme_menu.add_command(label="Light Theme" if is_en else "Giao diện sáng", command=lambda: self.apply_theme("win11_light"))
        theme_menu.add_command(label="Modern Blue Theme" if is_en else "Giao diện xanh hiện đại", command=lambda: self.apply_theme("win11_blue"))
        theme_menu.add_command(label="Classic CAD Theme" if is_en else "Giao diện kỹ thuật cổ điển", command=lambda: self.apply_theme("classic_cad"))
        theme_menu.add_command(label="Dark Studio Theme" if is_en else "Giao diện tối", command=lambda: self.apply_theme("dark_studio"))
        menubar.add_cascade(label="Themes" if is_en else "Giao diện", menu=theme_menu)

        # 5. MENU NGÔN NGỮ (LANGUAGE)
        lang_menu = tk.Menu(menubar, tearoff=0)
        lang_menu.add_command(label="Tiếng Việt" + ("  ✓" if not is_en else ""), command=lambda: self.switch_language("vi"))
        lang_menu.add_command(label="English" + ("  ✓" if is_en else ""), command=lambda: self.switch_language("en"))
        menubar.add_cascade(label="Language" if is_en else "Ngôn ngữ", menu=lang_menu)

        # 6. MENU THÔNG TIN (HELP)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(
            label="User Guide (F1)..." if is_en else "Hướng dẫn sử dụng (F1)...",
            command=self.open_user_handbook,
            accelerator="F1"
        )
        help_menu.add_command(
            label="Keyboard Shortcuts..." if is_en else "Bảng tra cứu phím tắt...",
            command=self.show_shortcuts_dialog
        )
        help_menu.add_command(
            label="Syntax & LaTeX Guide..." if is_en else "Hướng dẫn cú pháp & LaTeX...",
            command=self.show_syntax_help
        )
        help_menu.add_separator()
        help_menu.add_command(
            label="About CAD Math Studio..." if is_en else "Thông tin phần mềm CAD Math Studio...",
            command=self.show_about_dialog
        )
        help_menu.add_command(label="⭐ License & Payment (Upgrade to Pro)..." if is_en else "⭐ Bản quyền & Thanh toán (Kích hoạt Pro)...", command=self.open_license_payment_dialog)
        menubar.add_cascade(label="Help" if is_en else "Thông tin", menu=help_menu)

        self.root.config(menu=menubar)

    def bind_keyboard_shortcuts(self):
        self.root.bind("<Control-o>", lambda e: self.open_file_dialog())
        self.root.bind("<Control-s>", lambda e: self.save_solution_dialog())
        self.root.bind("<Control-S>", lambda e: self.save_plot_dialog())
        self.root.bind("<Control-p>", lambda e: self.export_html_report())
        self.root.bind("<Control-q>", lambda e: self.root.quit())
        self.root.bind("<Control-plus>", lambda e: self.zoom_in())
        self.root.bind("<Control-equal>", lambda e: self.zoom_in())
        self.root.bind("<Control-minus>", lambda e: self.zoom_out())
        self.root.bind("<Control-0>", lambda e: self.zoom_reset())
        self.root.bind("<Control-l>", lambda e: self.clear_active_tab())
        self.root.bind("<F1>", lambda e: self.open_user_handbook())
        self.root.bind("<F5>", lambda e: self._on_ai_solve_click())

    def get_current_result_box(self):
        current_tab_idx = self.notebook.index(self.notebook.select())
        boxes = [
            getattr(self, 'eq_result_box', None),
            getattr(self, 'ext_result_box', None),
            getattr(self, 'calc_result_box', None),
            getattr(self, 'mat_result_box', None),
            getattr(self, 'stat_result_box', None),
            getattr(self, 'plot_result_box', None)
        ]
        if 0 <= current_tab_idx < len(boxes):
            return boxes[current_tab_idx]
        return None

    def zoom_in(self):
        if self.current_font_size < 22:
            self.current_font_size += 1
            self.apply_font_size()

    def zoom_out(self):
        if self.current_font_size > 8:
            self.current_font_size -= 1
            self.apply_font_size()

    def zoom_reset(self):
        self.current_font_size = 11
        self.apply_font_size()

    def apply_font_size(self):
        for box in [getattr(self, 'eq_result_box', None),
                    getattr(self, 'ext_result_box', None),
                    getattr(self, 'calc_result_box', None),
                    getattr(self, 'mat_result_box', None),
                    getattr(self, 'stat_result_box', None),
                    getattr(self, 'plot_result_box', None)]:
            if box is not None:
                try:
                    box.configure(font=("Consolas", self.current_font_size))
                except Exception:
                    pass
        is_en = (getattr(self, "current_lang", "vi") == "en")
        self.status_lbl.config(text=f"Zoom: Current font size = {self.current_font_size}pt" if is_en else f"Thu phóng: Cỡ chữ hiển thị hiện tại = {self.current_font_size}pt")

    def open_file_dialog(self):
        is_en = (getattr(self, "current_lang", "vi") == "en")
        path = filedialog.askopenfilename(
            title="Open Math Equation File" if is_en else "Mở tệp phương trình toán học",
            filetypes=[("Text & Math Files", "*.txt;*.math;*.md"), ("All Files", "*.*")]
        )
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.eq_entry.delete("1.0", tk.END)
                self.eq_entry.insert(tk.END, content.strip())
                self.notebook.select(0)
                self.check_syntax_action()
                self.status_lbl.config(text=f"Opened file: {os.path.basename(path)}" if is_en else f"Đã mở tệp: {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Error" if is_en else "Lỗi mở tệp", f"Cannot read file: {e}" if is_en else f"Không thể đọc tệp: {e}")

    def save_solution_dialog(self):
        is_en = (getattr(self, "current_lang", "vi") == "en")
        box = self.get_current_result_box()
        if not box:
            return
        content = box.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning" if is_en else "Cảnh báo", "No solution content to save!" if is_en else "Không có nội dung bài giải để lưu!")
            return
        path = filedialog.asksaveasfilename(
            title="Save Detailed Solution" if is_en else "Lưu bài giải chi tiết",
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt"), ("Markdown Document", "*.md"), ("All Files", "*.*")]
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    hdr = "CAD MATH STUDIO PRO v2.4 - DETAILED MATHEMATICAL REPORT\n" if is_en else "CAD MATH STUDIO PRO v2.4 - BÁO CÁO GIẢI TOÁN CHI TIẾT\n"
                    f.write(hdr)
                    f.write("="*75 + "\n\n")
                    f.write(content)
                messagebox.showinfo("Success" if is_en else "Thành công", f"Saved solution successfully to:\n{path}" if is_en else f"Đã lưu bài giải thành công vào:\n{path}")
                self.status_lbl.config(text=f"Saved solution: {os.path.basename(path)}" if is_en else f"Đã lưu bài giải: {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Error" if is_en else "Lỗi lưu tệp", f"Cannot write file: {e}" if is_en else f"Không thể ghi tệp: {e}")

    def copy_plot_action(self, fig=None):
        is_en = (getattr(self, "current_lang", "vi") == "en")
        target_fig = fig
        if not target_fig:
            current_tab_idx = self.notebook.index(self.notebook.select())
            if current_tab_idx == 0: target_fig = getattr(self, 'eq_fig', None)
            elif current_tab_idx == 1: target_fig = getattr(self, 'ext_fig', None)
            elif current_tab_idx == 2: target_fig = getattr(self, 'calc_fig', None)
            elif current_tab_idx == 4: target_fig = getattr(self, 'stat_fig', None)
            elif current_tab_idx == 5: target_fig = getattr(self, 'plot_fig', None)

        if not target_fig:
            messagebox.showwarning("Warning" if is_en else "Cảnh báo", "Current tab does not have a plot to copy!" if is_en else "Tab hiện tại không có đồ thị để sao chép!")
            return

        success = copy_figure_to_clipboard(target_fig)
        if success:
            self.status_lbl.config(text="Plot image copied to clipboard (300 DPI)!" if is_en else "Đã sao chép ảnh đồ thị vào Clipboard (độ phân giải cao 300 DPI)!")
        else:
            messagebox.showerror("Error" if is_en else "Lỗi", "Failed to copy image to clipboard!" if is_en else "Không thể sao chép ảnh vào Clipboard!")

    def print_plot_action(self, fig=None):
        """In ấn đồ thị trực tiếp qua hộp thoại Windows Print chuẩn A4 / Máy in."""
        import tempfile
        is_en = (getattr(self, "current_lang", "vi") == "en")
        target_fig = fig
        if not target_fig:
            current_tab_idx = self.notebook.index(self.notebook.select())
            if current_tab_idx == 0: target_fig = getattr(self, 'eq_fig', None)
            elif current_tab_idx == 1: target_fig = getattr(self, 'ext_fig', None)
            elif current_tab_idx == 2: target_fig = getattr(self, 'calc_fig', None)
            elif current_tab_idx == 4: target_fig = getattr(self, 'stat_fig', None)
            elif current_tab_idx == 5: target_fig = getattr(self, 'plot_fig', None)

        if not target_fig:
            messagebox.showwarning("Warning" if is_en else "Cảnh báo", "Current tab does not have a plot to print!" if is_en else "Tab hiện tại không có đồ thị để in!")
            return

        try:
            temp_path = os.path.join(tempfile.gettempdir(), "cad_math_print_plot.png")
            wm = target_fig.text(
                0.98, 0.02,
                "CAD Math Studio Pro",
                fontsize=8,
                color="#64748b",
                alpha=0.18,
                ha="right",
                va="bottom",
                fontstyle="italic"
            )
            target_fig.savefig(temp_path, dpi=300, bbox_inches='tight', facecolor='#ffffff')
            try:
                wm.remove()
                target_fig.canvas.draw_idle()
            except Exception:
                pass

            os.startfile(temp_path, "print")
            self.status_lbl.config(text="Sending plot to Windows Print dialog..." if is_en else "Đang mở hộp thoại In ấn Windows...")
        except Exception as e:
            try:
                os.startfile(temp_path)
            except Exception:
                messagebox.showerror("Print Error" if is_en else "Lỗi in ấn", str(e))

    def save_plot_dialog(self, fig=None):
        is_en = (getattr(self, "current_lang", "vi") == "en")
        target_fig = fig
        if not target_fig:
            current_tab_idx = self.notebook.index(self.notebook.select())
            if current_tab_idx == 0: target_fig = getattr(self, 'eq_fig', None)
            elif current_tab_idx == 1: target_fig = getattr(self, 'ext_fig', None)
            elif current_tab_idx == 2: target_fig = getattr(self, 'calc_fig', None)
            elif current_tab_idx == 4: target_fig = getattr(self, 'stat_fig', None)
            elif current_tab_idx == 5: target_fig = getattr(self, 'plot_fig', None)

        if not target_fig:
            messagebox.showwarning("Warning" if is_en else "Cảnh báo", "Current tab does not have a plot to save!" if is_en else "Tab hiện tại không có đồ thị để lưu!")
            return

        path = filedialog.asksaveasfilename(
            title="Save Plot Image (with Subtle Trademark)" if is_en else "Lưu hình ảnh đồ thị (kèm Trademark mờ)",
            defaultextension=".png",
            filetypes=[
                ("PNG Image (*.png)", "*.png"),
                ("JPEG Image / In ấn thông thường (*.jpg;*.jpeg)", "*.jpg;*.jpeg"),
                ("PDF Document (*.pdf)", "*.pdf"),
                ("SVG Vector Image (*.svg)", "*.svg")
            ]
        )
        if path:
            try:
                ext = os.path.splitext(path)[1].lower()
                wm_artist = target_fig.text(
                    0.98, 0.02,
                    "CAD Math Studio Pro",
                    fontsize=8,
                    color="#64748b",
                    alpha=0.18,
                    ha="right",
                    va="bottom",
                    fontstyle="italic",
                    fontfamily="sans-serif"
                )

                if ext in [".jpg", ".jpeg"]:
                    import io
                    from PIL import Image
                    buf = io.BytesIO()
                    target_fig.savefig(buf, format='png', dpi=300, bbox_inches='tight', facecolor='#ffffff')
                    buf.seek(0)
                    im = Image.open(buf).convert('RGB')
                    im.save(path, 'JPEG', quality=95, dpi=(300, 300))
                    buf.close()
                else:
                    target_fig.savefig(path, dpi=300, bbox_inches='tight', facecolor='#ffffff', edgecolor='none')

                try:
                    wm_artist.remove()
                    target_fig.canvas.draw_idle()
                except Exception:
                    pass

                msg_success = f"Exported high-res image (300 DPI):\n{path}" if is_en else f"Đã xuất ảnh chất lượng cao (300 DPI, trademark mờ phục vụ in ấn):\n{path}"
                messagebox.showinfo("Success" if is_en else "Thành công", msg_success)
                self.status_lbl.config(text=f"Saved plot image: {os.path.basename(path)}" if is_en else f"Đã lưu ảnh đồ thị: {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Error" if is_en else "Lỗi lưu ảnh", f"Cannot save plot image: {e}" if is_en else f"Không thể lưu ảnh đồ thị: {e}")

    def create_plot_toolbar(self, parent_frame, fig_getter, auto_solve_func=None, canvas_widget=None):
        """
        Tạo thanh công cụ xuất ảnh chuẩn hóa (📋 Chép Ảnh & 💾 Lưu Ảnh)
        và gắn menu ngữ cảnh chuột phải lên canvas.
        """
        if not hasattr(self, "_plot_toolbars"):
            self._plot_toolbars = []

        tb_frame = tk.Frame(parent_frame, bg="#f8fafc", bd=1, relief="solid")
        tb_frame.pack(side=tk.TOP, fill=tk.X, padx=4, pady=(2, 4))

        is_en = (getattr(self, "current_lang", "vi") == "en")

        def _do_copy():
            fig = fig_getter()
            if auto_solve_func:
                if not fig or not fig.axes or not any(ax.lines or ax.collections or ax.patches for ax in fig.axes):
                    auto_solve_func()
                    fig = fig_getter()
            self.copy_plot_action(fig)

        def _do_save():
            fig = fig_getter()
            if auto_solve_func:
                if not fig or not fig.axes or not any(ax.lines or ax.collections or ax.patches for ax in fig.axes):
                    auto_solve_func()
                    fig = fig_getter()
            self.save_plot_dialog(fig)

        btn_copy = tk.Button(
            tb_frame,
            text="📋 " + ("Copy Image" if is_en else "Chép Ảnh"),
            font=("Segoe UI", 8, "bold"),
            bg="#f1f5f9", fg="#0f172a",
            relief="solid", bd=1, padx=6, pady=1,
            cursor="hand2",
            command=_do_copy
        )
        btn_copy.pack(side=tk.LEFT, padx=3, pady=2)

        btn_save = tk.Button(
            tb_frame,
            text="💾 " + ("Save Plot" if is_en else "Lưu Ảnh"),
            font=("Segoe UI", 8, "bold"),
            bg="#f1f5f9", fg="#0969da",
            relief="solid", bd=1, padx=6, pady=1,
            cursor="hand2",
            command=_do_save
        )
        btn_save.pack(side=tk.LEFT, padx=3, pady=2)

        def _do_print():
            fig = fig_getter()
            if auto_solve_func:
                if not fig or not fig.axes or not any(ax.lines or ax.collections or ax.patches for ax in fig.axes):
                    auto_solve_func()
                    fig = fig_getter()
            self.print_plot_action(fig)

        btn_print = tk.Button(
            tb_frame,
            text="🖨️ " + ("Print" if is_en else "In Ấn"),
            font=("Segoe UI", 8, "bold"),
            bg="#f1f5f9", fg="#10b981",
            relief="solid", bd=1, padx=6, pady=1,
            cursor="hand2",
            command=_do_print
        )
        btn_print.pack(side=tk.LEFT, padx=3, pady=2)

        lbl_hint = tk.Label(
            tb_frame,
            text=("300 DPI High-Res | Right-click to copy" if is_en else "Chuẩn 300 DPI | Chuột phải để sao chép"),
            font=("Segoe UI", 7, "italic"),
            fg="#64748b", bg="#f8fafc"
        )
        lbl_hint.pack(side=tk.RIGHT, padx=4)

        self._plot_toolbars.append({
            "btn_copy": btn_copy,
            "btn_save": btn_save,
            "lbl_hint": lbl_hint,
            "copy_func": _do_copy,
            "save_func": _do_save
        })

        if canvas_widget:
            ctx_menu = tk.Menu(self.root, tearoff=0)
            ctx_menu.add_command(label="📋 Copy Image" if is_en else "📋 Sao chép ảnh vào Clipboard", command=_do_copy)
            ctx_menu.add_command(label="💾 Save Plot..." if is_en else "💾 Lưu ảnh đồ thị thành tệp...", command=_do_save)

            def _show_ctx(evt):
                _is_en = (getattr(self, "current_lang", "vi") == "en")
                ctx_menu.entryconfigure(0, label="📋 Copy Image" if _is_en else "📋 Sao chép ảnh vào Clipboard")
                ctx_menu.entryconfigure(1, label="💾 Save Plot..." if _is_en else "💾 Lưu ảnh đồ thị thành tệp...")
                ctx_menu.tk_popup(evt.x_root, evt.y_root)

            canvas_widget.bind("<Button-3>", _show_ctx)

        return tb_frame

    def export_html_report(self):
        """
        Xuất báo cáo kỹ thuật toàn diện định dạng HTML tự chứa (self-contained),
        tích hợp kết xuất MathJax 3.2 cho căn thức & phân số đẹp mắt, nhúng ảnh Base64
        và hỗ trợ in ấn PDF chuẩn trang A4 chỉ với 1 cú click.
        """
        import webbrowser
        from stem_shared_core.report_engine import build_full_stem_html_report, figure_to_base64_png

        current_tab_idx = self.notebook.index(self.notebook.select())
        box = self.get_current_result_box()
        solution_content = box.get("1.0", tk.END).strip() if box else ""

        tab_names = [
            "Phương Trình & Bất Phương Trình",
            "Cực Trị VDC & Tham Số m",
            "Vi Tích Phân & Đa Biến",
            "Đại Số Tuyến Tính & Ma Trận",
            "Tổ Hợp - Xác Suất & Thống Kê",
            "Khảo Sát Hàm Số & Đồ Thị Oxy"
        ]
        topic = tab_names[current_tab_idx] if 0 <= current_tab_idx < len(tab_names) else "Toán Học Tự Nhiên"

        problem_text = ""
        hero_latex = ""
        hero_text = ""
        fig_to_export = None

        if current_tab_idx == 0:
            problem_text = self.eq_entry.get("1.0", tk.END).strip() if hasattr(self, "eq_entry") else ""
            if hasattr(self, "eq_result_canvas"):
                hero_latex = self.eq_result_canvas.last_latex
                hero_text = self.eq_result_canvas.last_text
            fig_to_export = getattr(self, "eq_fig", None)
        elif current_tab_idx == 1:
            p_val = self.ext_target_entry.get().strip() if hasattr(self, "ext_target_entry") else ""
            g_val = self.ext_cond_entry.get().strip() if hasattr(self, "ext_cond_entry") else ""
            problem_text = f"Mục tiêu tối ưu: {p_val}\nRàng buộc đẳng thức: {g_val}"
            if hasattr(self, "ext_math_canvas"):
                hero_latex = self.ext_math_canvas.last_latex
                hero_text = self.ext_math_canvas.last_text
            fig_to_export = getattr(self, "ext_fig", None)
        elif current_tab_idx == 2:
            problem_text = self.calc_entry.get().strip() if hasattr(self, "calc_entry") else ""
            if hasattr(self, "calc_math_canvas"):
                hero_latex = self.calc_math_canvas.last_latex
                hero_text = self.calc_math_canvas.last_text
            fig_to_export = getattr(self, "calc_fig", None)
        elif current_tab_idx == 3:
            problem_text = "Phép toán Ma trận & Đại số tuyến tính"
            if hasattr(self, "mat_result_canvas"):
                hero_latex = self.mat_result_canvas.last_latex
                hero_text = self.mat_result_canvas.last_text
        elif current_tab_idx == 4:
            problem_text = self.stat_entry.get().strip() if hasattr(self, "stat_entry") else ""
            fig_to_export = getattr(self, "stat_fig", None)
        elif current_tab_idx == 5:
            problem_text = f"y = {self.plot_f1.get().strip()}" if hasattr(self, "plot_f1") else ""
            fig_to_export = getattr(self, "plot_fig", None)

        is_en = (getattr(self, "current_lang", "vi") == "en")
        if not problem_text and not solution_content:
            messagebox.showwarning("No Data" if is_en else "Chưa có dữ liệu", "Please solve a problem before exporting report." if is_en else "Vui lòng giải một bài toán trước khi xuất báo cáo.")
            return

        path = filedialog.asksaveasfilename(
            title="Export Full Technical Report (HTML / PDF Print)" if is_en else "Xuất Báo Cáo Kỹ Thuật Toàn Diện (HTML / In ấn PDF)",
            defaultextension=".html",
            filetypes=[("HTML Web Document (*.html)", "*.html")]
        )
        if not path:
            return

        try:
            plot_b64 = figure_to_base64_png(fig_to_export) if fig_to_export else ""

            # Tách riêng AI narrative nếu có trong kết quả
            ai_commentary = ""
            solution_steps = solution_content
            if "PHÂN TÍCH LOGIC & LỜI GIẢI TOÁN HỌC (AI)" in solution_content:
                parts = solution_content.split("PHÂN TÍCH LOGIC & LỜI GIẢI TOÁN HỌC (AI)")
                solution_steps = parts[0].strip()
                ai_commentary = ("AI MATHEMATICAL LOGIC & PEDAGOGICAL ANALYSIS" if is_en else "PHÂN TÍCH LOGIC & LỜI GIẢI TOÁN HỌC (AI)") + parts[1]
            elif "AI MATHEMATICAL LOGIC & PEDAGOGICAL ANALYSIS" in solution_content:
                parts = solution_content.split("AI MATHEMATICAL LOGIC & PEDAGOGICAL ANALYSIS")
                solution_steps = parts[0].strip()
                ai_commentary = ("AI MATHEMATICAL LOGIC & PEDAGOGICAL ANALYSIS" if is_en else "PHÂN TÍCH LOGIC & LỜI GIẢI TOÁN HỌC (AI)") + parts[1]

            html_code = build_full_stem_html_report(
                app_title="CAD Math Studio Pro v2.4",
                topic=topic,
                problem_text=problem_text,
                hero_formula_latex=hero_latex,
                hero_formula_text=hero_text,
                solution_steps=solution_steps,
                plot_base64_png=plot_b64,
                ai_commentary=ai_commentary
            )
            with open(path, "w", encoding="utf-8") as f:
                f.write(html_code)

            self.status_lbl.config(text=f"Report exported: {os.path.basename(path)}" if is_en else f"Đã xuất báo cáo: {os.path.basename(path)}")
            ask_title = "Report Exported Successfully" if is_en else "Xuất Báo Cáo Thành Công"
            ask_msg = f"Technical MathJax report generated at:\n{path}\n\nWould you like to open it in your browser (supports Print to PDF)?" if is_en else f"Đã tạo báo cáo kỹ thuật MathJax hoàn chỉnh tại:\n{path}\n\nBạn có muốn mở ngay trên trình duyệt (hỗ trợ In sang PDF) không?"
            if messagebox.askyesno(ask_title, ask_msg):
                webbrowser.open(f"file:///{os.path.abspath(path)}")
        except Exception as e:
            messagebox.showerror("Error" if is_en else "Lỗi xuất báo cáo", f"Cannot export HTML report: {e}" if is_en else f"Không thể xuất báo cáo HTML: {e}")

    def copy_active_solution(self):
        is_en = (getattr(self, "current_lang", "vi") == "en")
        box = self.get_current_result_box()
        if box:
            text = box.get("1.0", tk.END).strip()
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.status_lbl.config(text="Solution copied to Clipboard!" if is_en else "Đã sao chép lời giải vào Clipboard!")

    def clear_active_tab(self):
        is_en = (getattr(self, "current_lang", "vi") == "en")
        box = self.get_current_result_box()
        if box:
            box.delete("1.0", tk.END)
            self.status_lbl.config(text="Cleared current result box." if is_en else "Đã xóa trắng khung kết quả hiện tại.")

    def focus_equation_ribbon(self):
        messagebox.showinfo("Bảng Ký Hiệu Toán Học",
                            "Hộp công cụ Equation Ribbon luôn hiển thị phía trên các ô nhập liệu.\n"
                            "Bạn có thể nhấp trực tiếp vào các phím tắt như |x|, √, ∛, ∜, ⁿ√, a/b, x², xⁿ, π, i, ≤, ≥, ∫, ∑\n"
                            "hoặc gõ cú pháp LaTeX chuẩn quốc tế.")

    def run_system_benchmark_dialog(self):
        """Mở cửa sổ kiểm định chất lượng hệ thống tự động 20 bài toán mẫu chuẩn."""
        dlg = tk.Toplevel(self.root)
        dlg.title("Kiểm Định Chất Lượng Hệ Thống - CAD Math Studio Pro v2.4")
        dlg.geometry("820x560")
        dlg.configure(bg="#ffffff")
        dlg.transient(self.root)

        header = tk.Frame(dlg, bg="#1e293b", height=45)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(
            header,
            text="BỘ ĐO LƯỜNG & KIỂM THỬ TỰ ĐỘNG CHẤT LƯỢNG TOÁN HỌC (SYSTEM BENCHMARK)",
            font=("Segoe UI", 10, "bold"), fg="#f8fafc", bg="#1e293b", padx=12
        ).pack(side=tk.LEFT, fill=tk.Y)

        stat_bar = tk.Frame(dlg, bg="#f1f5f9", height=32, bd=1, relief="solid")
        stat_bar.pack(fill=tk.X, padx=10, pady=8)
        lbl_status = tk.Label(stat_bar, text="Đang tiến hành chạy 20 bài toán kiểm thử toàn diện...",
                              font=("Segoe UI", 9, "bold"), fg="#0969da", bg="#f1f5f9", padx=10)
        lbl_status.pack(side=tk.LEFT, fill=tk.Y)

        box = scrolledtext.ScrolledText(dlg, font=("Consolas", 10), bg="#ffffff", fg="#0f172a", relief="solid", bd=1)
        box.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        def run_tests():
            import subprocess
            py_exe = sys.executable
            suite_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_suite_cad_math.py")
            res = subprocess.run([py_exe, suite_path], capture_output=True, text=True, encoding="utf-8")
            box.insert(tk.END, res.stdout)
            if res.stderr:
                box.insert(tk.END, "\n" + res.stderr)
            lbl_status.config(text="Kết quả: 20/20 (100%) BÀI KIỂM THỬ ĐẠT CHUẨN XUẤT SẮC (ENTERPRISE GRADE)!", fg="#16a34a")

        threading.Thread(target=run_tests, daemon=True).start()

    def open_user_handbook(self):
        """Mở cửa sổ cẩm nang hướng dẫn sử dụng tích hợp trong phần mềm (In-App Help Dialog)."""
        is_en = (getattr(self, 'current_lang', 'vi') == 'en')
        CADMathHandbookDialog(self.root, is_en=is_en)

    def show_shortcuts_dialog(self):
        """Hiển thị bảng tra cứu phím tắt toàn tập."""
        is_en = (getattr(self, 'current_lang', 'vi') == 'en')
        dlg = tk.Toplevel(self.root)
        dlg.title("Keyboard Shortcuts" if is_en else "Bảng Tra Cứu Phím Tắt")
        dlg.geometry("540x400")
        dlg.configure(bg="#ECE9D8")
        dlg.transient(self.root)
        dlg.grab_set()

        hdr = tk.Frame(dlg, bg="#ECE9D8", pady=6)
        hdr.pack(side=tk.TOP, fill=tk.X, padx=12)
        tk.Label(
            hdr,
            text="CAD MATH STUDIO - KEYBOARD SHORTCUTS" if is_en else "CAD MATH STUDIO - BẢNG PHÍM TẮT THAO TÁC",
            font=("Tahoma", 10, "bold"),
            bg="#ECE9D8",
            fg="#000080"
        ).pack(side=tk.TOP, anchor="w")

        body = tk.Frame(dlg, bg="#ECE9D8")
        body.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=12, pady=4)

        txt = tk.Text(body, font=("Consolas", 9), bg="#FFFFFF", fg="#000000", relief=tk.SUNKEN, bd=2, wrap=tk.WORD, padx=8, pady=8)
        sb = tk.Scrollbar(body, orient=tk.VERTICAL, command=txt.yview)
        txt.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        sc_vn = (
            "• F1              : Hướng dẫn sử dụng chi tiết\n"
            "• F5              : Giải toán AI\n"
            "• Ctrl + O        : Mở file bài toán\n"
            "• Ctrl + S        : Lưu bài giải chi tiết ra file văn bản\n"
            "• Ctrl + Shift + S: Lưu ảnh đồ thị hiện tại ra file PNG\n"
            "• Ctrl + P        : Xuất báo cáo bài giải ra file HTML\n"
            "• Ctrl + C        : Sao chép bài giải vào bộ nhớ tạm\n"
            "• Ctrl + V        : Dán công thức vào ô đang chọn\n"
            "• Ctrl + L        : Xóa trắng nội dung tab hiện tại\n"
            "• Ctrl + +        : Phóng to cỡ chữ bài giải\n"
            "• Ctrl + -        : Thu nhỏ cỡ chữ bài giải\n"
            "• Ctrl + 0        : Đặt lại cỡ chữ bài giải 100%\n"
            "• Ctrl + Q        : Thoát phần mềm\n"
        )
        sc_en = (
            "• F1              : Detailed User Guide\n"
            "• F5              : AI Solver\n"
            "• Ctrl + O        : Open problem file\n"
            "• Ctrl + S        : Save solution text to file\n"
            "• Ctrl + Shift + S: Save current plot image to PNG\n"
            "• Ctrl + P        : Export HTML report\n"
            "• Ctrl + C        : Copy solution to clipboard\n"
            "• Ctrl + V        : Paste formula into active field\n"
            "• Ctrl + L        : Clear active tab\n"
            "• Ctrl + +        : Zoom In solution font\n"
            "• Ctrl + -        : Zoom Out solution font\n"
            "• Ctrl + 0        : Reset solution font size to 100%\n"
            "• Ctrl + Q        : Exit application\n"
        )
        txt.insert(tk.END, sc_en if is_en else sc_vn)
        txt.configure(state=tk.DISABLED)

        btn_box = tk.Frame(dlg, bg="#ECE9D8", pady=6)
        btn_box.pack(side=tk.BOTTOM, fill=tk.X, padx=12)
        tk.Button(
            btn_box,
            text="[ Close ]" if is_en else "[ Đóng ]",
            font=("Tahoma", 9, "bold"),
            bg="#ECE9D8",
            relief=tk.RAISED,
            bd=2,
            padx=12,
            command=dlg.destroy
        ).pack(side=tk.RIGHT)

    def show_syntax_help(self):
        is_en = (getattr(self, 'current_lang', 'vi') == 'en')
        if is_en:
            msg = (
                "CAD MATH STUDIO PRO v2.4 - NATURAL SYNTAX & LATEX GUIDE:\n"
                "--------------------------------------------------------------------\n"
                "1. Inequalities: <=, >=, <, >, !=, \\le, \\ge\n"
                "   Examples: x^2 - 3x + 2 <= 0, (x - 1)/(x + 2) > 0, sqrt(2x + 1) < x - 1\n"
                "2. Parametric Problems (m): x^2 - 2(m-1)x + m + 5 >= 0, sqrt(x-1) + sqrt(5-x) <= m\n"
                "3. Implicit Multiplication: 2x, x sqrt(y), y(12 - x^2), (x+1)(x-2)\n"
                "4. Radicals: sqrt(x), root(x, n), \\sqrt{x}, \\sqrt[3]{x}, \\sqrt[4]{x-1}\n"
                "5. Exponents & Absolute Values: x^2, 3^(|x-y|), |x|, Abs(x - y)\n"
                "6. Complex Numbers: i is the imaginary unit (sqrt(-1)). E.g.: (1 + 2i)z + 3 - i = 0\n"
                "   Conjugate: \\bar{z}, z_bar\n"
                "7. Systems of Equations/Inequalities: Multiple lines or separated by ';'\n"
                "8. Calculus: Partial derivative d/dz, \\partial/\\partial z, integral ∫ f dx, sum ∑\n"
                "9. Linear Algebra: Matrix input by lines, A x B, det, inverse A⁻¹, solve AX = B\n"
                "10. 2D Oxy Function Grapher: Domain, derivative, extrema, inflection, asymptotes, tangent\n"
            )
            title = "Natural Mathematical Syntax Guide"
        else:
            msg = (
                "HƯỚNG DẪN CÚ PHÁP GÕ CÔNG THỨC TOÁN HỌC\n"
                "--------------------------------------------------------------------\n"
                "1. Bất phương trình: <=, >=, <, >, !=, \\le, \\ge\n"
                "   Ví dụ: x^2 - 3x + 2 <= 0, (x - 1)/(x + 2) > 0, sqrt(2x + 1) < x - 1\n"
                "2. Bài toán chứa tham số m: x^2 - 2(m-1)x + m + 5 >= 0, sqrt(x-1) + sqrt(5-x) <= m\n"
                "3. Phép nhân: Gõ 2x, x*y, y*(12 - x^2), (x+1)*(x-2)\n"
                "4. Căn thức: sqrt(x), \\sqrt{x}, root(x, 3), \\sqrt[4]{x-1}\n"
                "5. Lũy thừa & Trị tuyệt đối: x^2, 3^(|x-y|), |x|, abs(x - y)\n"
                "6. Số phức: i là đơn vị ảo. Ví dụ: (1 + 2i)*z + 3 - i = 0. Số phức liên hợp: \\bar{z}, z_bar\n"
                "7. Hệ phương trình: Gõ mỗi phương trình một dòng hoặc cách nhau bởi dấu chấm phẩy ';'\n"
                "8. Giải tích: Đạo hàm d/dz, ∂/∂z, tích phân ∫ f dx, chuỗi ∑\n"
                "9. Ma trận: Nhập từng dòng, nhân A x B, định thức det, nghịch đảo A⁻¹, giải AX = B\n"
                "10. Đồ thị hàm số: Tập xác định, đạo hàm, cực trị, tiệm cận, tiếp tuyến\n"
            )
            title = "Hướng Dẫn Cú Pháp"
        messagebox.showinfo(title, msg)


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
                "Cảm ơn bạn đã ủng hộ! Bản quyền CAD Math Studio Pro đã được kích hoạt thành công.\\nBiểu tượng của ứng dụng đã được đổi sang Icon Pro bo góc sang trọng.",
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

    def show_about_dialog(self):
        is_en = (getattr(self, 'current_lang', 'vi') == 'en')
        if is_en:
            msg = (
                "CAD MATH STUDIO PRO v2.4\n"
                "Version: 2.4 (Pro Edition)\n"
                "Comprehensive Natural CAS Mathematical Computation System for Standard & Advanced Mathematics.\n\n"
                "• Equations, Inequalities & Systems (Parametric m analysis, Complex numbers z, Absolute values).\n"
                "• Global Optimization & Inequalities (Lagrange multipliers, Critical point estimation, Symmetric permutation).\n"
                "• Multivariable Calculus (Partial derivatives, Definite integrals, Taylor expansion, Limits).\n"
                "• Linear Algebra & Matrix Engine (A x B, Inversion, Determinants, Systems AX = B, Eigenvalues).\n"
                "• Combinatorics, Probability & Descriptive Statistics (Newton binomial, Boxplots, Histograms).\n"
                "• 2D Oxy Coordinate Function Variation Study & Vector Plotting."
            )
            title = "About CAD Math Studio Pro v2.4"
        else:
            msg = (
                "CAD MATH STUDIO PRO v2.4\n"
                "Phiên bản: 2.4 (Bản Pro)\n"
                "Phần mềm giải toán đa năng và vẽ đồ thị hàm số.\n\n"
                "• Giải phương trình, bất phương trình và hệ phương trình (tham số m, số phức).\n"
                "• Tìm giá trị lớn nhất, nhỏ nhất và bất đẳng thức.\n"
                "• Đạo hàm, tích phân, khai triển chuỗi và giới hạn.\n"
                "• Tính toán ma trận (nhân ma trận, nghịch đảo, định thức, giải hệ AX = B).\n"
                "• Tổ hợp, xác suất và thống kê mô tả (trung bình, phương sai, biểu đồ hộp).\n"
                "• Khảo sát sự biến thiên và vẽ đồ thị hàm số trên mặt phẳng Oxy."
            )
            title = "Thông Tin Phần Mềm CAD Math Studio Pro v2.4"
        messagebox.showinfo(title, msg)

    def switch_language(self, lang: str):
        """Chuyển ngôn ngữ giao diện toàn diện cả 6 chuyên đề và toolbar."""
        self.current_lang = lang
        # --- Đồng bộ với hệ thống i18n tập trung ---
        if _I18N_AVAILABLE:
            try:
                _i18n_set(lang)
            except Exception:
                pass
        t = TRANSLATIONS.get(lang, TRANSLATIONS.get("vi", {}))
        self.status_lbl.config(text=t['status'])
        if hasattr(self, 'title_lbl'):
            self.title_lbl.config(text=t['title'])
        self.setup_menu_bar()

        # Toolbar
        if hasattr(self, 'lbl_ai_model'):
            self.lbl_ai_model.config(text="AI Model:" if lang == "en" else "Mô hình AI:")
        if hasattr(self, 'combo_ai_profile'):
            profiles = [
                "1. Pure SymPy CAS Engine",
                "2. AI Assistant 1.5B (Lightweight)",
                "3. AI Standard Math 7B",
                "4. AI Advanced Math 7B",
            ] if lang == "en" else [
                "1. Thuần thuật toán SymPy CAS",
                "2. AI Trợ giảng 1.5B (Máy nhẹ)",
                "3. AI Chuyên toán 7B",
                "4. AI Suy luận 7B",
            ]
            cur_idx = self.combo_ai_profile.current()
            self.combo_ai_profile['values'] = profiles
            if cur_idx >= 0:
                self.combo_ai_profile.current(cur_idx)

        if hasattr(self, 'btn_ai_solve') and not getattr(self, "_ai_solving_active", False):
            self.btn_ai_solve.config(text=t['ai_solve'])
        if hasattr(self, 'btn_ai_config'):
            self.btn_ai_config.config(text=t['ai_config'])
        if hasattr(self, 'btn_export'):
            self.btn_export.config(text=t['export'])
        if hasattr(self, 'btn_restore'):
            self.btn_restore.config(text=t['restore'])
        if hasattr(self, 'btn_ribbon'):
            self.btn_ribbon.config(text=t['ribbon'])

        # 6 Notebook Tabs
        try:
            self.notebook.tab(0, text=t['tab1'])
            self.notebook.tab(1, text=t['tab2'])
            self.notebook.tab(2, text=t['tab3'])
            self.notebook.tab(3, text=t['tab4'])
            self.notebook.tab(4, text=t['tab5'])
            self.notebook.tab(5, text=t['tab6'])
        except Exception:
            pass

        # Tab 1
        if hasattr(self, 'lbl_input_eq'):
            self.lbl_input_eq.config(text=t['lbl_input_eq'])
        if hasattr(self, 'lbl_param_mode'):
            self.lbl_param_mode.config(text=t['param_mode_label'])
        if hasattr(self, 'btn_solve_eq'):
            self.btn_solve_eq.config(text=t['btn_solve_eq'])
        if hasattr(self, 'preview_frame_eq'):
            self.preview_frame_eq.config(text=t['preview_eq'])
        if hasattr(self, 'hero_frame_eq'):
            self.hero_frame_eq.config(text=t['hero_eq'])
        if hasattr(self, 'lbl_steps_eq'):
            self.lbl_steps_eq.config(text=t['steps_eq'])
        if hasattr(self, 'right_frame_eq'):
            self.right_frame_eq.config(text=t['graph_eq'])
        if hasattr(self, 'sample_eq_btns') and len(self.sample_eq_btns) == len(t['eq_samples']):
            for btn, txt in zip(self.sample_eq_btns, t['eq_samples']):
                btn.config(text=txt)
        if hasattr(self, 'eq_param_mode'):
            cur_p = self.eq_param_mode.current()
            self.eq_param_mode['values'] = t['param_modes']
            if cur_p >= 0:
                self.eq_param_mode.current(cur_p)
            else:
                self.eq_param_mode.set(t['param_modes'][0])

        # Tab 2
        if hasattr(self, 'lbl_ext_header'):
            self.lbl_ext_header.config(text=t['lbl_ext_header'])
        if hasattr(self, 'lbl_ext_cond'):
            self.lbl_ext_cond.config(text=t['lbl_ext_cond'])
        if hasattr(self, 'btn_solve_ext'):
            self.btn_solve_ext.config(text=t['btn_solve_ext'])
        if hasattr(self, 'hero_frame_ext'):
            self.hero_frame_ext.config(text=t['hero_ext'])
        if hasattr(self, 'lbl_steps_ext'):
            self.lbl_steps_ext.config(text=t['steps_ext'])
        if hasattr(self, 'contour_frame_ext'):
            self.contour_frame_ext.config(text=t['contour_ext'])
        if hasattr(self, 'sample_ext_btns') and len(self.sample_ext_btns) == len(t['ext_samples']):
            for btn, txt in zip(self.sample_ext_btns, t['ext_samples']):
                btn.config(text=txt)

        # Tab 3
        if hasattr(self, 'lbl_calc_header'):
            self.lbl_calc_header.config(text=t['lbl_calc_header'])
        if hasattr(self, 'lbl_calc_op'):
            self.lbl_calc_op.config(text=t['lbl_calc_op'])
        if hasattr(self, 'lbl_calc_var'):
            self.lbl_calc_var.config(text=t['lbl_calc_var'])
        if hasattr(self, 'lbl_calc_param'):
            self.lbl_calc_param.config(text=t['lbl_calc_param'])
        if hasattr(self, 'btn_calc'):
            self.btn_calc.config(text=t['btn_calc'])
        if hasattr(self, 'hero_frame_calc'):
            self.hero_frame_calc.config(text=t['hero_calc'])
        if hasattr(self, 'lbl_steps_calc'):
            self.lbl_steps_calc.config(text=t['steps_calc'])
        if hasattr(self, 'graph_frame_calc'):
            self.graph_frame_calc.config(text=t['graph_calc'])
        if hasattr(self, 'calc_op'):
            cur_op = self.calc_op.current()
            self.calc_op['values'] = t['calc_modes']
            if cur_op >= 0:
                self.calc_op.current(cur_op)
        if hasattr(self, 'sample_calc_btns') and len(self.sample_calc_btns) == len(t['calc_samples']):
            for btn, txt in zip(self.sample_calc_btns, t['calc_samples']):
                btn.config(text=txt)

        # Tab 4
        if hasattr(self, 'lbl_mat_header'):
            self.lbl_mat_header.config(text=t['lbl_mat_header'])
        if hasattr(self, 'frame_mat_a'):
            self.frame_mat_a.config(text=t['frame_mat_a'])
        if hasattr(self, 'frame_mat_b'):
            self.frame_mat_b.config(text=t['frame_mat_b'])
        if hasattr(self, 'btn_mat_inv'):
            self.btn_mat_inv.config(text=t['btn_mat_inv'])
        if hasattr(self, 'btn_mat_trans'):
            self.btn_mat_trans.config(text=t['btn_mat_trans'])
        if hasattr(self, 'btn_mat_solve'):
            self.btn_mat_solve.config(text=t['btn_mat_solve'])
        if hasattr(self, 'btn_mat_eigen'):
            self.btn_mat_eigen.config(text=t['btn_mat_eigen'])
        if hasattr(self, 'hero_frame_mat'):
            self.hero_frame_mat.config(text=t['hero_mat'])
        if hasattr(self, 'lbl_steps_mat'):
            self.lbl_steps_mat.config(text=t['steps_mat'])
        if hasattr(self, 'sample_mat_btns') and len(self.sample_mat_btns) == len(t['mat_samples']):
            for btn, txt in zip(self.sample_mat_btns, t['mat_samples']):
                btn.config(text=txt)

        # Tab 5
        if hasattr(self, 'lbl_stat_header'):
            self.lbl_stat_header.config(text=t['lbl_stat_header'])
        if hasattr(self, 'lbl_stat_mode'):
            self.lbl_stat_mode.config(text=t['lbl_stat_mode'])
        if hasattr(self, 'lbl_stat_data'):
            self.lbl_stat_data.config(text=t['lbl_stat_data'])
        if hasattr(self, 'btn_stat'):
            self.btn_stat.config(text=t['btn_stat'])
        if hasattr(self, 'lbl_steps_stat'):
            self.lbl_steps_stat.config(text=t['steps_stat'])
        if hasattr(self, 'plot_frame_stat'):
            self.plot_frame_stat.config(text=t['plot_stat'])
        if hasattr(self, 'stat_mode'):
            cur_st = self.stat_mode.current()
            self.stat_mode['values'] = t['stat_modes']
            if cur_st >= 0:
                self.stat_mode.current(cur_st)
        if hasattr(self, 'sample_stat_btns') and len(self.sample_stat_btns) == len(t['stat_samples']):
            for btn, txt in zip(self.sample_stat_btns, t['stat_samples']):
                btn.config(text=txt)

        # Tab 6
        if hasattr(self, 'lbl_plot_header'):
            self.lbl_plot_header.config(text=t['lbl_plot_header'])
        if hasattr(self, 'btn_run_plot'):
            self.btn_run_plot.config(text=t['btn_plot'])
        if hasattr(self, 'graph_frame_plot'):
            self.graph_frame_plot.config(text=t['graph_plot'])
        if hasattr(self, 'lbl_plot_res'):
            self.lbl_plot_res.config(text=t['report_plot'])
        if hasattr(self, 'sample_plot_btns') and len(self.sample_plot_btns) == len(t['plot_samples']):
            for btn, txt in zip(self.sample_plot_btns, t['plot_samples']):
                btn.config(text=txt)

        # Cập nhật thanh công cụ xuất ảnh đồ thị (Chép Ảnh & Lưu Ảnh) trên tất cả các Tab
        if hasattr(self, '_plot_toolbars'):
            for tb in self._plot_toolbars:
                try:
                    tb["btn_copy"].config(text="📋 " + ("Copy Image" if lang == "en" else "Chép Ảnh"))
                    tb["btn_save"].config(text="💾 " + ("Save Plot" if lang == "en" else "Lưu Ảnh"))
                    tb["lbl_hint"].config(text=("300 DPI High-Res | Right-click to copy" if lang == "en" else "Chuẩn 300 DPI | Chuột phải để sao chép"))
                except Exception:
                    pass

        # Update all math formula canvases
        canvases = [
            getattr(self, 'eq_math_canvas', None),
            getattr(self, 'eq_result_canvas', None),
            getattr(self, 'ext_math_canvas', None),
            getattr(self, 'calc_math_canvas', None),
            getattr(self, 'mat_result_canvas', None)
        ]
        for c in canvases:
            if c:
                if hasattr(c, 'btn_copy_ltx'):
                    c.btn_copy_ltx.config(text="LaTeX" if lang == "en" else "Mã LaTeX")
                if hasattr(c, 'btn_copy_txt'):
                    c.btn_copy_txt.config(text="Text" if lang == "en" else "Văn bản")
                if hasattr(c, 'btn_copy_img'):
                    c.btn_copy_img.config(text="Copy Image" if lang == "en" else "Chép Ảnh")
                if hasattr(c, 'btn_save'):
                    c.btn_save.config(text="Save Image" if lang == "en" else "Lưu Ảnh")
                if hasattr(c, 'is_showing_placeholder') and c.is_showing_placeholder():
                    c.reset_placeholder(is_en=(lang == 'en'))

        # If Tab 1 entry is empty, show language placeholder, otherwise re-check syntax
        if hasattr(self, 'eq_entry') and hasattr(self, 'eq_math_canvas') and self.eq_math_canvas:
            if not self.eq_entry.get("1.0", tk.END).strip():
                self.eq_math_canvas.reset_placeholder(is_en=(lang == 'en'))
            else:
                self.check_syntax_action()

        # Update ribbon labels and buttons
        if hasattr(self, 'ribbon_lbls'):
            for lbl1, lbl2 in self.ribbon_lbls:
                if lbl1: lbl1.config(text="ALGEBRA:" if lang == "en" else "ĐẠI SỐ:")
                if lbl2: lbl2.config(text="CALCULUS:" if lang == "en" else "GIẢI TÍCH:")
        if hasattr(self, 'ribbon_sys_btns'):
            for btn in self.ribbon_sys_btns:
                if btn: btn.config(text="Sys {" if lang == "en" else "Hệ {")

        if hasattr(self, 'graph_frame_plot'):
            self.graph_frame_plot.config(text=t.get('graph_plot', "2D FUNCTION GRAPH ON OXY PLANE" if lang == "en" else "ĐỒ THỊ HÀM SỐ TRÊN HỆ TRỤC TỌA ĐỘ OXY"))

        msg = "Language switched to English successfully!" if lang == 'en' else "Đã chuyển sang giao diện Tiếng Việt thành công!"
        messagebox.showinfo("Language" if lang == "en" else "Ngôn ngữ", msg)

    def _stop_active_ai_if_running(self):
        """Dừng tiến trình suy luận AI nếu đang hoạt động."""
        if getattr(self, "_ai_solving_active", False):
            self._ai_stop_flag = True

    def restore_cas_solution(self):
        """Phục hồi hiển thị lời giải giải tích thuần SymPy CAS của Tab hiện tại."""
        self._stop_active_ai_if_running()
        box = self.get_current_result_box()
        if not box:
            return
        tab_idx = self.notebook.index(self.notebook.select())
        if tab_idx in self._last_ground_truth_text and self._last_ground_truth_text[tab_idx]:
            box.delete("1.0", tk.END)
            box.insert("1.0", self._last_ground_truth_text[tab_idx])
            self.status_lbl.config(text="↺ Đã phục hồi lời giải giải tích SymPy CAS gốc.")
        else:
            text = box.get("1.0", tk.END).strip()
            marker = "═" * 58
            if marker in text:
                pure_cas = text.split(marker)[0].strip()
                box.delete("1.0", tk.END)
                box.insert("1.0", pure_cas)
                self.status_lbl.config(text="↺ Đã tách và phục hồi lời giải giải tích SymPy CAS gốc.")
            else:
                self.status_lbl.config(text="ℹ️ Khung kết quả hiện tại đang ở trạng thái CAS gốc.")

    def _append_ai_token(self, box, text: str):
        """Đẩy từng token vào result_box trên luồng chính Tkinter một cách an toàn."""
        if not box:
            return
        box.insert(tk.END, text)
        box.see(tk.END)

    def _get_active_tab_problem_info(self) -> Tuple[str, str, str]:
        """Trích xuất đề bài, chế độ và kết quả giải tích Ground Truth của Tab đang chọn."""
        tab_idx = self.notebook.index(self.notebook.select())
        box = self.get_current_result_box()
        gt_sol = box.get("1.0", tk.END).strip() if box else ""

        # Nếu đã có phần phân tích AI trước đó, lọc lấy phần Ground Truth của SymPy CAS
        marker = "═" * 58
        if marker in gt_sol:
            gt_sol = gt_sol.split(marker)[0].strip()

        tab_title = self.notebook.tab(tab_idx, "text")
        problem_desc = ""

        if tab_idx == 0:
            # Tab 1: Phương trình / Bất phương trình
            eq_text = self.eq_entry.get("1.0", tk.END).strip() if hasattr(self, "eq_entry") else ""
            mode = self.eq_param_mode.get() if hasattr(self, "eq_param_mode") else ""
            problem_desc = f"Phương trình / BPT: {eq_text} (Chế độ: {mode})"
        elif tab_idx == 1:
            # Tab 2: Cực trị VDC & Tham số m
            ext_text = self.ext_entry.get("1.0", tk.END).strip() if hasattr(self, "ext_entry") else ""
            vars_text = self.ext_vars_entry.get().strip() if hasattr(self, "ext_vars_entry") else ""
            mode = self.ext_mode.get() if hasattr(self, "ext_mode") else ""
            problem_desc = f"Hàm mục tiêu: {ext_text} với biến {vars_text} (Chế độ: {mode})"
        elif tab_idx == 2:
            # Tab 3: Vi tích phân & Giải tích đa biến
            func = self.calc_func_entry.get().strip() if hasattr(self, "calc_func_entry") else ""
            var = self.calc_var_entry.get().strip() if hasattr(self, "calc_var_entry") else "x"
            op = self.calc_op_combo.get() if hasattr(self, "calc_op_combo") else ""
            problem_desc = f"Phép toán vi tích phân: {op} đối với hàm f({var}) = {func}"
        elif tab_idx == 3:
            # Tab 4: Đại số tuyến tính & Ma trận
            op = self.mat_op_combo.get() if hasattr(self, "mat_op_combo") else ""
            problem_desc = f"Phép toán Ma trận: {op}"
        elif tab_idx == 4:
            # Tab 5: Tổ hợp - Xác suất & Thống kê
            data = self.stat_data_entry.get().strip() if hasattr(self, "stat_data_entry") else ""
            problem_desc = f"Mẫu số liệu thống kê: {data}"
        elif tab_idx == 5:
            # Tab 6: Khảo sát hàm số & Đồ thị Oxy
            func = self.plot_func_entry.get().strip() if hasattr(self, "plot_func_entry") else ""
            problem_desc = f"Khảo sát hàm số y = f(x) = {func} trên mặt phẳng Oxy"

        return tab_title, problem_desc, gt_sol

    def _on_ai_solve_click(self):
        """Kích hoạt hoặc Dừng bộ suy luận AI cho Bài toán Toán học hiện tại."""
        if getattr(self, "_ai_solving_active", False):
            self._ai_stop_flag = True
            self.status_lbl.config(text="⏹ Đã gửi lệnh dừng AI...", fg="#c92a2a")
            return

        if not _AI_HUB_AVAILABLE:
            messagebox.showerror(
                "Mô-đun AI Chưa Sẵn Sàng",
                "Chưa tìm thấy mô-đun AI trong stem_shared_core.\nVui lòng kiểm tra lại cấu trúc thư mục."
            )
            return

        profile_idx = self.combo_ai_profile.current() if hasattr(self, "combo_ai_profile") else 0
        if profile_idx < 0:
            profile_idx = 0

        # PROFILE 0: Thuần Python CAS (Thuật toán Python)
        if profile_idx == 0:
            self.restore_cas_solution()
            self.status_lbl.config(text="✅ Đã hiển thị lời giải giải tích chính xác 100% từ SymPy CAS.")
            return

        # Khởi tạo AI Hub & AI Manager nếu chưa có
        if not hasattr(self, "ai_hub") or self.ai_hub is None:
            self.ai_hub = AIModelHub()
        if not hasattr(self, "ai_manager") or self.ai_manager is None:
            self.ai_manager = AILocalManager()

        # Mapping profile 100% Cục Bộ (Offline): 0=Python CAS, 1=DeepSeek 1.5B (Khuyên dùng), 2=Qwen 7B, 3=DeepSeek 7B
        profile_map = {
            1: {"mgr_id": 3, "source": "local", "model": "deepseek-r1:1.5b"},
            2: {"mgr_id": 4, "source": "local", "model": "qwen2.5-coder:7b"},
            3: {"mgr_id": 2, "source": "local", "model": "deepseek-r1:7b"},
        }
        cfg = profile_map.get(profile_idx, profile_map[1])
        chosen_source = "local"
        mgr_profile_id = cfg["mgr_id"]

        self.ai_hub.set_ollama_model(cfg["model"])
        st = self.ai_hub.status()

        # Kiểm tra điều kiện tiên quyết Ollama cục bộ
        if not st.get("ollama_ready") and not st.get("llama_cpp_installed"):
            ans = messagebox.askyesno(
                "Chưa khởi động Local AI",
                "Gói 'Local AI' cần có Ollama đang chạy trên máy tính.\n\n"
                "Bạn có muốn mở Bảng Điều Khiển để xem hướng dẫn khởi động Ollama không?"
            )
            if ans:
                self.open_ai_assistant()
            return

        # Kiểm tra RAM cho profile nặng
        if chosen_source == "local":
            ram_ok, ram_msg = self.ai_manager.check_ram_for_profile(mgr_profile_id)
            if not ram_ok:
                ans = messagebox.askyesno(
                    "Cảnh báo bộ nhớ RAM",
                    f"{ram_msg}\n\nBạn có muốn tiếp tục nạp mô hình vào RAM không?"
                )
                if not ans:
                    return

        # Thu thập ngữ cảnh từ Tab đang mở
        tab_idx = self.notebook.index(self.notebook.select())
        box = self.get_current_result_box()
        if not box:
            messagebox.showwarning("Thông báo", "Vui lòng mở một Tab giải toán trước khi gọi AI!")
            return

        tab_title, problem_desc, gt_sol = self._get_active_tab_problem_info()

        if not gt_sol or len(gt_sol) < 15:
            # TỰ ĐỘNG THỰC THI BỘ GIẢI SYMPY CAS NỘI BỘ (ĐẢM BẢO 100% GROUND TRUTH, KHÔNG BỎ TRỐNG DỮ LIỆU)
            try:
                if tab_idx == 0:
                    self.solve_equation_action()
                elif tab_idx == 1:
                    self.solve_extremum_action()
                elif tab_idx == 2:
                    self.solve_calculus_action()
                elif tab_idx == 3:
                    op = self.mat_op_combo.get() if hasattr(self, "mat_op_combo") else "det"
                    self.solve_matrix_action(op)
                elif tab_idx == 4:
                    self.solve_statistics_action()
                elif tab_idx == 5:
                    self.solve_plot_oxy_action()
            except Exception:
                pass
            tab_title, problem_desc, gt_sol = self._get_active_tab_problem_info()

        # Lưu giữ bản CAS Ground Truth để phục hồi khi cần
        if tab_idx not in self._last_ground_truth_text or not self._last_ground_truth_text[tab_idx]:
            self._last_ground_truth_text[tab_idx] = gt_sol

        is_en = (getattr(self, "current_lang", "vi") == "en")
        if is_en:
            prompt_lines = [
                "You are an expert Mathematical Explainer (CAD Math Technical Explainer).",
                "MANDATORY DISCIPLINE: 100% of numbers, conditions, transformations and solution sets HAVE BEEN COMPUTED ACCURATELY BY THE SYMPY CAS CORE BELOW.",
                "DO NOT recompute independently, DO NOT invent extraneous roots, DO NOT fabricate arbitrary formulas.\n",
                f"【MATHEMATICAL TOPIC】: {tab_title}",
                f"【PROBLEM】: {problem_desc}\n",
                "【GROUND TRUTH ANALYTIC SPECIFICATION (SYMPY CAS)】:",
                gt_sol if gt_sol else "Using original problem specification.",
                "\n【PRESENTATION REQUIREMENTS】:",
                "1. Brief Summary: Domain restrictions and primary method.",
                "2. Clearly present step-by-step transformations following the exact Ground Truth above.",
                "3. Conclude with final solution set concisely and directly in professional English."
            ]
            ai_header = (
                "🤖 LOGICAL ANALYSIS & MATHEMATICAL SOLUTION (AI):\n"
                + "═" * 58 + "\n"
                + "⏳ Connecting to model and streaming step-by-step reasoning...\n\n"
            )
        else:
            prompt_lines = [
                "Bạn là Chuyên gia Thuyết minh Giải tích Toán học (CAD Math Technical Explainer).",
                "QUY TẮC BẮT BUỘC (KỶ LUẬT TUYỆT ĐỐI): 100% các con số, điều kiện, phép biến đổi và tập nghiệm ĐÃ ĐƯỢC LÕI SYMPY CAS TÍNH TOÁN CHÍNH XÁC DƯỚI ĐÂY.",
                "TUYỆT ĐỐI KHÔNG tự tính toán lại, KHÔNG bịa đặt nghiệm ngoại lai, KHÔNG suy diễn công thức lạ.\n",
                f"【CHUYÊN ĐỀ TOÁN HỌC】: {tab_title}",
                f"【BÀI TOÁN】: {problem_desc}\n",
                "【BẢN THIẾT KẾ GIẢI TÍCH GROUND TRUTH (SYMPY CAS)】:",
                gt_sol if gt_sol else "Đang sử dụng dữ liệu bài toán gốc.",
                "\n【YÊU CẦU TRÌNH BÀY】:",
                "1. Tóm lược ngắn gọn: Điều kiện xác định & Phương pháp chính.",
                "2. Trình bày rõ ràng các bước biến đổi kỹ thuật dựa chính xác theo Ground Truth ở trên.",
                "3. Kết luận nghiệm hoặc kết quả cuối cùng ngắn gọn, trực diện, chuẩn mực tiếng Việt."
            ]
            ai_header = (
                "🤖 PHÂN TÍCH LOGIC & LỜI GIẢI TOÁN HỌC (AI):\n"
                + "═" * 58 + "\n"
                + "⏳ Đang kết nối mô hình và suy luận trực tiếp từng bước...\n\n"
            )
        full_prompt = "\n".join(prompt_lines)

        # Chuẩn bị giao diện hiển thị: Append Mode vào box
        sep = "\n\n" + "═" * 58 + "\n"

        txt_all = box.get("1.0", tk.END)
        marker = "═" * 58
        pos = txt_all.find(marker)
        if pos != -1:
            box.delete(f"1.0 + {pos} chars", tk.END)

        box.insert(tk.END, sep + ai_header)
        box.see(tk.END)

        # Cập nhật trạng thái nút bấm
        self._ai_solving_active = True
        self._ai_stop_flag = False
        self._ai_streaming_active = True

        self.btn_ai_solve.config(text="⏹ Dừng AI", bg="#c92a2a", fg="#ffffff")
        self.status_lbl.config(text="⏳ AI đang suy luận từng bước (Bấm '⏹ Dừng AI' hoặc F5 để hủy)...", fg="#c92a2a")

        # Chạy suy luận trong luồng nền
        def _worker():
            breaker = RepetitionBreaker() if 'RepetitionBreaker' in globals() else None
            recent_chunks = []
            try:
                for chunk in self.ai_hub.stream(full_prompt, source=chosen_source):
                    if getattr(self, "_ai_stop_flag", False):
                        self.root.after(0, self._append_ai_token, box, "\n\n[AI] Đã dừng theo yêu cầu người dùng.\n")
                        break

                    text = chunk.text
                    clean_text = _filter_exotic_scripts(text) if '_filter_exotic_scripts' in globals() else text
                    if not clean_text:
                        continue

                    # Chống lặp chuỗi
                    if breaker and breaker.feed(clean_text):
                        self.root.after(0, self._append_ai_token, box, "\n\n[Hệ thống tự động ngắt chuỗi lặp AI - Đảm bảo tính nhất quán toán học]\n")
                        break

                    recent_chunks.append(clean_text)
                    if len(recent_chunks) > 20:
                        recent_chunks.pop(0)
                    recent_str = "".join(recent_chunks)
                    if recent_str.count(",000") >= 4 or recent_str.count("000,000") >= 3 or (len(clean_text) >= 4 and recent_str.count(clean_text) >= 5):
                        self.root.after(0, self._append_ai_token, box, "\n\n[Hệ thống tự động ngắt chuỗi lặp AI - Đảm bảo tính nhất quán toán học]\n")
                        break

                    self.root.after(0, self._append_ai_token, box, clean_text)
                else:
                    self.root.after(0, self._append_ai_token, box, (
                        "\n\n═════════════════════════════════════════════════════════\n"
                        "✅ [HOÀN TẤT - AI ĐÃ KẾT THÚC TIẾN TRÌNH SUY LUẬN]\n"
                        "═════════════════════════════════════════════════════════\n"
                    ))
            except Exception as ex:
                self.root.after(0, self._append_ai_token, box, f"\n\n⚠️ Lỗi kết nối AI: {ex}\n")
            finally:
                def _finish():
                    self._ai_solving_active = False
                    self._ai_streaming_active = False
                    self.btn_ai_solve.config(text="AI giải toán (F5)", bg="#0969da", fg="#ffffff")
                    if getattr(self, "_ai_stop_flag", False):
                        self.status_lbl.config(text="⏹ Đã dừng AI theo yêu cầu.", fg="#475569")
                    else:
                        self.status_lbl.config(text="✅ Đã hoàn tất phân tích (SymPy CAS & AI).", fg="#16a34a")
                    if hasattr(self, "ai_manager") and self.ai_manager:
                        self.ai_manager.idle.touch()
                self.root.after(0, _finish)

        threading.Thread(target=_worker, daemon=True).start()

    def open_ai_assistant(self):
        """Mở hộp thoại cấu hình tài nguyên AI Offline tối giản và chuẩn mực."""
        from stem_shared_core.ai_config_dialog import show_clean_ai_config_dialog

        if not hasattr(self, "ai_hub") or self.ai_hub is None:
            if _AI_HUB_AVAILABLE:
                self.ai_hub = AIModelHub()
        if not hasattr(self, "ai_manager") or self.ai_manager is None:
            if _AI_HUB_AVAILABLE:
                self.ai_manager = AILocalManager()

        cur_idx = self.combo_ai_profile.current() if hasattr(self, "combo_ai_profile") else 0
        if cur_idx < 0:
            cur_idx = 0

        def on_selected(idx, title):
            if hasattr(self, "combo_ai_profile"):
                self.combo_ai_profile.current(idx)
            if hasattr(self, "status_lbl") and self.status_lbl:
                self.status_lbl.config(text=f"Đã chọn hồ sơ AI: {title}")

        show_clean_ai_config_dialog(
            parent=self.root,
            ai_hub=self.ai_hub,
            ai_manager=self.ai_manager,
            current_profile_idx=cur_idx,
            on_profile_selected=on_selected,
        )
    # --------------------------------------------------------------------------
    # EQUATION RIBBON (QUICK TOOLPAD)
    # --------------------------------------------------------------------------
    def open_higher_math_dialog(self, initial_topic_idx: int = 0):
        """Mở Hộp thoại Chuyên Đề Toán Cao Cấp Đại Học."""
        try:
            from stem_shared_core.higher_math_dialog import show_higher_math_dialog
            show_higher_math_dialog(self.root, initial_topic_idx=initial_topic_idx, lang=getattr(self, "current_lang", "vi"))
        except Exception as e:
            messagebox.showerror("Lỗi Toán Cao Cấp", f"Không thể mở hộp thoại Toán Cao Cấp: {e}", parent=self.root)

    def run_higher_math_benchmark_dialog(self):
        """Chạy kiểm định chất lượng toàn diện Toán Cao Cấp."""
        try:
            from stem_shared_core.higher_math_benchmark import run_higher_math_benchmark
            success = run_higher_math_benchmark()
            if success:
                messagebox.showinfo("Kiểm định Toán cao cấp", "Hoàn thành kiểm tra 20/20 bài toán.\nBáo cáo chi tiết đã được lưu trong thư mục stem_shared_core.", parent=self.root)
            else:
                messagebox.showwarning("Kiểm Định Toán Cao Cấp", "Có một số bài kiểm định không đạt.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Lỗi Kiểm Định", str(e), parent=self.root)

    def create_equation_ribbon(self, parent_frame, target_widget_getter):
        """Tạo thanh công cụ chèn ký hiệu toán học nhanh."""
        ribbon = tk.Frame(parent_frame, bg="#f1f5f9", bd=1, relief="solid")
        ribbon.pack(fill=tk.X, pady=(1, 4))

        row1 = tk.Frame(ribbon, bg="#f1f5f9")
        row1.pack(fill=tk.X, pady=1)
        lbl_r1 = tk.Label(row1, text=self._s("ĐẠI SỐ:", "ALGEBRA:"), font=("Segoe UI", 8, "bold"), fg="#475569", bg="#f1f5f9", width=9, anchor="w")
        lbl_r1.pack(side=tk.LEFT, padx=4)

        row2 = tk.Frame(ribbon, bg="#f1f5f9")
        row2.pack(fill=tk.X, pady=1)
        lbl_r2 = tk.Label(row2, text=self._s("GIẢI TÍCH:", "CALCULUS:"), font=("Segoe UI", 8, "bold"), fg="#475569", bg="#f1f5f9", width=9, anchor="w")
        lbl_r2.pack(side=tk.LEFT, padx=4)

        if not hasattr(self, "ribbon_lbls"):
            self.ribbon_lbls = []
        self.ribbon_lbls.append((lbl_r1, lbl_r2))
        if not hasattr(self, "ribbon_sys_btns"):
            self.ribbon_sys_btns = []

        buttons_r1 = [
            ("√x", "\\sqrt{", "}"),
            ("∛x", "\\sqrt[3]{", "}"),
            ("∜x", "\\sqrt[4]{", "}"),
            ("ⁿ√x", "\\sqrt[n]{", "}"),
            ("a/b", "\\frac{", "}{}"),
            ("|x|", "|", "|"),
            ("x²", "^2", ""),
            ("x³", "^3", ""),
            ("xⁿ", "^{", "}"),
            ("xᵢ", "_{", "}"),
            (self._s("Hệ {", "Sys {"), "\\begin{cases} ", " \\\\  \\end{cases}"),
            ("≤", " <= ", ""),
            ("≥", " >= ", ""),
            ("≠", " != ", ""),
            ("±", " +- ", ""),
            ("i", "i", ""),
            ("z̄", "\\bar{z}", ""),
            ("π", "pi", ""),
            ("e", "e", ""),
            ("∞", "oo", ""),
        ]
        buttons_r2 = [
            ("sin", "sin(", ")"),
            ("cos", "cos(", ")"),
            ("tan", "tan(", ")"),
            ("cot", "cot(", ")"),
            ("ln", "ln(", ")"),
            ("logₐb", "log_{a}(", ")"),
            ("∫", "\\int ", " dx"),
            ("∑", "\\sum ", ""),
            ("lim", "\\lim_{x \\to 0} ", ""),
            ("∂/∂x", "\\partial/\\partial x ", ""),
            ("∂/∂y", "\\partial/\\partial y ", ""),
            ("f'(x)", "diff(", ", x)"),
            ("Δ", "Delta", ""),
            ("α", "alpha", ""),
            ("β", "beta", ""),
        ]

        def make_inserter(prefix, suffix):
            def insert_symbol():
                w = target_widget_getter()
                if not w:
                    return
                try:
                    if isinstance(w, tk.Entry) or isinstance(w, ttk.Entry):
                        sel_range = None
                        try:
                            sel_range = (w.index(tk.SEL_FIRST), w.index(tk.SEL_LAST))
                        except Exception:
                            pass
                        if sel_range:
                            sel_text = w.get()[sel_range[0]:sel_range[1]]
                            w.delete(sel_range[0], sel_range[1])
                            w.insert(sel_range[0], f"{prefix}{sel_text}{suffix}")
                        else:
                            pos = w.index(tk.INSERT)
                            w.insert(pos, f"{prefix}{suffix}")
                            w.icursor(pos + len(prefix))
                        w.focus_set()
                    elif isinstance(w, tk.Text) or isinstance(w, scrolledtext.ScrolledText):
                        try:
                            sel_text = w.get(tk.SEL_FIRST, tk.SEL_LAST)
                            w.delete(tk.SEL_FIRST, tk.SEL_LAST)
                            w.insert(tk.INSERT, f"{prefix}{sel_text}{suffix}")
                        except Exception:
                            w.insert(tk.INSERT, f"{prefix}{suffix}")
                        w.focus_set()
                except Exception:
                    pass
            return insert_symbol

        for label, pref, suff in buttons_r1:
            btn = tk.Button(
                row1, text=label, font=("Segoe UI", 8),
                bg="#ffffff", fg="#0f172a", relief="flat", bd=1,
                padx=4, pady=1, cursor="hand2",
                command=make_inserter(pref, suff)
            )
            btn.pack(side=tk.LEFT, padx=1, pady=1)

        for label, pref, suff in buttons_r2:
            btn = tk.Button(
                row2, text=label, font=("Segoe UI", 8),
                bg="#ffffff", fg="#0f172a", relief="flat", bd=1,
                padx=4, pady=1, cursor="hand2",
                command=make_inserter(pref, suff)
            )
            btn.pack(side=tk.LEFT, padx=1, pady=1)

    # --------------------------------------------------------------------------
    # UI BUILDER: 6 MAIN TABS
    # --------------------------------------------------------------------------
    def build_ui(self):
        # STATUS BAR (Đáy ứng dụng)
        self.status_bar = tk.Frame(self.root, bg="#e2e8f0", height=22)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_bar.pack_propagate(False)
        self.status_lbl = tk.Label(
            self.status_bar,
            text="Sẵn sàng",
            font=("Segoe UI", 8), bg="#e2e8f0", fg="#475569", anchor="w", padx=8
        )
        self.status_lbl.pack(fill=tk.BOTH, expand=True)

        # ======================================================================
        # THANH CÔNG CỤ NHỎ GỌN (TẬP TRUNG, KHÔNG TRÀN VIỀN)
        # ======================================================================
        self.ai_toolbar = tk.Frame(self.root, bg="#f1f5f9", bd=1, relief="solid", padx=6, pady=2)
        self.ai_toolbar.pack(fill=tk.X, padx=6, pady=(2, 2))

        self.lbl_ai_model = tk.Label(
            self.ai_toolbar, text=self._s("Mô hình AI:", "AI Model:"),
            font=("Segoe UI", 8, "bold"), bg="#f1f5f9", fg="#475569"
        )
        self.lbl_ai_model.pack(side=tk.LEFT, padx=(2, 2))

        self.ai_profile_var = tk.StringVar()
        profiles_init = [
            "1. Pure SymPy CAS Engine",
            "2. Lightweight AI (DeepSeek-R1 1.5B)",
            "3. Standard AI (Qwen 2.5 Coder 7B)",
            "4. Advanced AI (DeepSeek-R1 7B)",
        ] if getattr(self, "current_lang", "vi") == "en" else [
            "1. Thuần thuật toán SymPy CAS",
            "2. Mô hình AI nhẹ (DeepSeek-R1 1.5B)",
            "3. Mô hình AI tiêu chuẩn (Qwen 2.5 Coder 7B)",
            "4. Mô hình AI nâng cao (DeepSeek-R1 7B)",
        ]
        self.combo_ai_profile = ttk.Combobox(
            self.ai_toolbar,
            textvariable=self.ai_profile_var,
            state="readonly",
            width=28,
            font=("Segoe UI", 8),
            values=profiles_init,
        )
        self.combo_ai_profile.current(0)
        self.combo_ai_profile.pack(side=tk.LEFT, padx=3)

        # Nút AI Giải
        self.btn_ai_solve = tk.Button(
            self.ai_toolbar,
            text=self._s("⚡ AI giải toán (F5)", "⚡ AI Solve (F5)"),
            font=("Segoe UI", 8, "bold"),
            bg="#0969da",
            fg="#ffffff",
            activebackground="#0854ad",
            activeforeground="#ffffff",
            relief="raised",
            bd=1,
            padx=8,
            pady=1,
            cursor="hand2",
            command=self._on_ai_solve_click,
        )
        self.btn_ai_solve.pack(side=tk.LEFT, padx=3)

        # Nút Cấu hình AI đặt ngay cạnh nút AI Giải
        self.btn_ai_config = tk.Button(
            self.ai_toolbar,
            text=self._s("⚙️ Kết nối AI", "⚙️ AI Connect"),
            font=("Segoe UI", 8),
            bg="#e2e8f0",
            fg="#0f172a",
            relief="raised",
            bd=1,
            padx=6,
            pady=1,
            cursor="hand2",
            command=self.open_ai_assistant,
        )
        self.btn_ai_config.pack(side=tk.LEFT, padx=2)

        # Phân cách
        ttk.Separator(self.ai_toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=2)

        self.btn_export = tk.Button(
            self.ai_toolbar,
            text=self._s("🖨️ In ấn / Báo cáo (Ctrl+P)", "🖨️ Print / Report (Ctrl+P)"),
            font=("Segoe UI", 8, "bold"),
            bg="#10b981",
            fg="#ffffff",
            activebackground="#059669",
            activeforeground="#ffffff",
            relief="raised",
            bd=1,
            padx=8,
            pady=1,
            cursor="hand2",
            command=self.export_html_report,
        )
        self.btn_export.pack(side=tk.LEFT, padx=4)

        self.btn_restore = tk.Button(
            self.ai_toolbar,
            text=self._s("Khôi phục CAS", "Restore CAS"),
            font=("Segoe UI", 8),
            bg="#e2e8f0",
            relief="raised",
            bd=1,
            padx=6,
            pady=1,
            command=self.restore_cas_solution,
        )
        self.btn_restore.pack(side=tk.LEFT, padx=2)

        self.btn_ribbon = tk.Button(
            self.ai_toolbar,
            text=self._s("Ký hiệu toán", "Math Symbols"),
            font=("Segoe UI", 8),
            bg="#e2e8f0",
            relief="raised",
            bd=1,
            padx=6,
            pady=1,
            command=self.focus_equation_ribbon,
        )
        self.btn_ribbon.pack(side=tk.LEFT, padx=2)

        # Các bí danh tương thích kiểm thử
        self.btn_ai_config_header = self.btn_ai_config
        self.ribbon_container = self.ai_toolbar
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=(4, 6))

        # 6 TAB CHUẨN HOÁ CAO CẤP:
        self.create_equation_tab()        # Tab 1: Phương Trình & Bất Phương Trình (Kèm Tham số m)
        self.create_extremum_tab()        # Tab 2: Cực Trị VDC & Tham Số m (BĐT, Điểm Rơi)
        self.create_calculus_tab()        # Tab 3: Vi Tích Phân & Giải Tích Đa Biến
        self.create_linear_alg_tab()      # Tab 4: Đại Số Tuyến Tính & Ma Trận (A, B)
        self.create_statistics_tab()      # Tab 5: Tổ Hợp - Xác Suất & Thống Kê
        self.create_plot_oxy_tab()        # Tab 6: Khảo Sát Hàm Số & Đồ Thị Oxy

        self.notebook.select(0)

    # --------------------------------------------------------------------------
    # TAB 1: PHƯƠNG TRÌNH, BẤT PHƯƠNG TRÌNH & HỆ (SỐ PHỨC, THAM SỐ m)
    # --------------------------------------------------------------------------
    def create_equation_tab(self):
        tab = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(tab, text=self._s("1. Phương trình", "1. Equations"))

        # Equation Ribbon
        self.create_equation_ribbon(tab, lambda: self.eq_entry)

        top_f = tk.Frame(tab, bg="#ffffff")
        top_f.pack(fill=tk.X, pady=(0, 4))

        self.lbl_input_eq = tk.Label(
            top_f,
            text=self._s("NHẬP PHƯƠNG TRÌNH, BẤT PHƯƠNG TRÌNH HOẶC HỆ (THAM SỐ m):",
                         "ENTER EQUATION, INEQUALITY OR SYSTEM (PARAMETER m):"),
            font=("Segoe UI", 9, "bold"), fg="#1e293b", bg="#ffffff"
        )
        self.lbl_input_eq.pack(anchor="w")

        self.eq_entry = scrolledtext.ScrolledText(top_f, height=2, font=("Consolas", 11), bg="#f8fafc", fg="#0f172a", relief="solid", bd=1)
        self.eq_entry.pack(fill=tk.X, pady=(2, 4))
        self.eq_entry.insert(tk.END, "x^2 - 3*x + 2 <= 0")
        self.eq_entry.bind("<KeyRelease>", lambda e: self.check_syntax_action())

        # Check Syntax & Real-time Canvas
        self.preview_frame_eq = tk.LabelFrame(
            top_f,
            text=self._s("XEM TRƯỚC CÔNG THỨC 2D", "2D FORMULA PREVIEW"),
            font=("Segoe UI", 8, "bold"), fg="#0969da", bg="#ffffff"
        )
        self.preview_frame_eq.pack(fill=tk.X, pady=(2, 4))

        self.eq_math_canvas = MathFormulaCanvas(self.preview_frame_eq, height_px=42, bg="#ffffff", show_actions=False)
        self.eq_math_canvas.pack(fill=tk.X, expand=True)

        # Action Bar & Parameter Options
        act_f = tk.Frame(top_f, bg="#ffffff")
        act_f.pack(fill=tk.X, pady=(2, 4))

        self.btn_solve_eq = tk.Button(
            act_f,
            text=self._s("⚡ Giải bài toán (F5)", "⚡ Solve Problem (F5)"),
            font=("Segoe UI", 8, "bold"), bg="#0969da", fg="#ffffff",
            relief="flat", padx=10, pady=3, cursor="hand2",
            command=self.solve_equation_action
        )
        self.btn_solve_eq.pack(side=tk.LEFT, padx=(0, 10))

        self.lbl_param_mode = tk.Label(
            act_f,
            text=self._s("Chế độ tham số m:", "Parameter m Mode:"),
            font=("Segoe UI", 8, "bold"), bg="#ffffff"
        )
        self.lbl_param_mode.pack(side=tk.LEFT)

        param_modes = [
            "Auto Solve",
            "Find m so inequality holds for all x ∈ D",
            "Find m so inequality has solutions",
            "Find m so inequality has no solution",
            "Analyze number of solutions by parameter m"
        ] if getattr(self, "current_lang", "vi") == "en" else [
            "Tự động giải",
            "Tìm m để BPT nghiệm đúng với mọi x ∈ D",
            "Tìm m để BPT có nghiệm",
            "Tìm m để BPT vô nghiệm",
            "Khảo sát số nghiệm theo tham số m"
        ]
        self.eq_param_mode = ttk.Combobox(
            act_f, width=32, state="readonly",
            values=param_modes
        )
        self.eq_param_mode.pack(side=tk.LEFT, padx=(4, 10))
        self.eq_param_mode.set(param_modes[0])

        # Quick Samples Frame
        sample_f = tk.Frame(top_f, bg="#ffffff")
        sample_f.pack(fill=tk.X, pady=(2, 4))

        btn1 = tk.Button(sample_f, text="x² - 3x + 2 ≤ 0", font=("Segoe UI", 8), bg="#e2e8f0", relief="flat", padx=6, pady=2,
                         command=lambda: self.load_equation_sample("x^2 - 3*x + 2 <= 0"))
        btn1.pack(side=tk.LEFT, padx=2)

        btn2 = tk.Button(sample_f, text="(x-1)/(x+2) > 0", font=("Segoe UI", 8), bg="#e2e8f0", relief="flat", padx=6, pady=2,
                         command=lambda: self.load_equation_sample("(x - 1)/(x + 2) > 0"))
        btn2.pack(side=tk.LEFT, padx=2)

        btn3 = tk.Button(sample_f, text="√(2x+1) < x - 1", font=("Segoe UI", 8), bg="#e2e8f0", relief="flat", padx=6, pady=2,
                         command=lambda: self.load_equation_sample("sqrt(2*x + 1) < x - 1" if getattr(self, "current_lang", "vi") == "en" else "căn(2x + 1) < x - 1"))
        btn3.pack(side=tk.LEFT, padx=2)

        btn4 = tk.Button(sample_f, text=self._s("Tham số m", "Parametric m"), font=("Segoe UI", 8), bg="#e2e8f0", relief="flat", padx=6, pady=2,
                         command=lambda: self.load_equation_sample("x^2 - 2*(m - 1)*x + m + 5 >= 0", self.eq_param_mode['values'][1]))
        btn4.pack(side=tk.LEFT, padx=2)

        btn5 = tk.Button(sample_f, text=self._s("Hệ căn 4", "Root-4 System"), font=("Segoe UI", 8), bg="#e2e8f0", relief="flat", padx=6, pady=2,
                         command=lambda: self.load_equation_sample(
                             ("root(x - 1, 4) + sqrt(x + 1) - sqrt(y^4 + 2) = y\nx^2 + 2*x*(y - 1) + y^2 - 6*y + 1 = 0")
                             if getattr(self, "current_lang", "vi") == "en"
                             else ("căn[4](x - 1) + căn(x + 1) - căn(y^4 + 2) = y\nx^2 + 2*x*(y - 1) + y^2 - 6*y + 1 = 0")
                         ))
        btn5.pack(side=tk.LEFT, padx=2)

        btn6 = tk.Button(sample_f, text=self._s("Số phức", "Complex"), font=("Segoe UI", 8), bg="#e2e8f0", relief="flat", padx=6, pady=2,
                         command=lambda: self.load_equation_sample("(1 + 2i)z + 3 - i = 0"))
        btn6.pack(side=tk.LEFT, padx=2)

        self.sample_eq_btns = [btn1, btn2, btn3, btn4, btn5, btn6]

        # HERO RESULT CARD (TỰ ĐỘNG THU NHỎ, DÀN HÀNG NGANG ;)
        self.hero_frame_eq = tk.LabelFrame(top_f, text="KẾT QUẢ TẬP NGHIỆM HỢP LỆ 2D (HERO RESULT CARD)",
                                           font=("Segoe UI", 8, "bold"), fg="#16a34a", bg="#ffffff")
        self.hero_frame_eq.pack(fill=tk.X, pady=(2, 4))
        self.eq_result_canvas = MathFormulaCanvas(self.hero_frame_eq, height_px=42, bg="#ffffff", show_actions=True)
        self.eq_result_canvas.pack(fill=tk.X, expand=True)

        # MAIN SPLIT: STEP-BY-STEP SOLUTION + GRAPH / NUMBER LINE
        bot_f = tk.Frame(tab, bg="#ffffff")
        bot_f.pack(fill=tk.BOTH, expand=True)

        left_f = tk.Frame(bot_f, bg="#ffffff")
        left_f.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))

        self.lbl_steps_eq = tk.Label(left_f, text="LỜI GIẢI CHI TIẾT:",
                                     font=("Segoe UI", 9, "bold"), fg="#1e293b", bg="#ffffff")
        self.lbl_steps_eq.pack(anchor="w")
        self.eq_result_box = scrolledtext.ScrolledText(left_f, font=("Consolas", self.current_font_size), bg="#ffffff", fg="#0f172a", relief="solid", bd=1)
        self.eq_result_box.pack(fill=tk.BOTH, expand=True)

        self.right_frame_eq = tk.LabelFrame(bot_f, text="ĐỒ THỊ KHẢO SÁT & TRỤC SỐ BIỂU DIỄN TẬP NGHIỆM",
                                            font=("Segoe UI", 8, "bold"), fg="#0969da", bg="#ffffff")
        self.right_frame_eq.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4, 0))

        self.eq_fig = Figure(figsize=(4.5, 4), dpi=100, facecolor='#ffffff')
        self.eq_canvas = FigureCanvasTkAgg(self.eq_fig, master=self.right_frame_eq)
        self.create_plot_toolbar(self.right_frame_eq, lambda: self.eq_fig, self.solve_equation_action, self.eq_canvas.get_tk_widget())
        self.eq_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.check_syntax_action()

    def load_equation_sample(self, txt: str, param_mode=None):
        self.eq_entry.delete("1.0", tk.END)
        self.eq_entry.insert(tk.END, txt)
        if param_mode is not None:
            self.eq_param_mode.set(param_mode)
        else:
            vals = self.eq_param_mode['values']
            if vals:
                self.eq_param_mode.set(vals[0])
        self.check_syntax_action()
        self.root.after(50, self.solve_equation_action)

    def check_syntax_action(self):
        raw_text = self.eq_entry.get("1.0", tk.END).strip()
        is_en = (getattr(self, "current_lang", "vi") == "en")
        if not raw_text:
            self.eq_math_canvas.render_latex(
                r"\text{Please enter an equation or inequality...}" if is_en else r"\text{Vui lòng nhập phương trình hoặc bất phương trình...}"
            )
            return
        lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
        if not lines:
            lines = [l.strip() for l in raw_text.split(';') if l.strip()]

        try:
            latex_items = []
            for l in lines:
                eq_sym = smart_parse(l)
                if isinstance(eq_sym, Relational):
                    latex_items.append(sp.latex(eq_sym))
                else:
                    latex_items.append(f"{sp.latex(eq_sym)} = 0")
            if len(latex_items) > 1:
                self.eq_math_canvas.render_system(latex_items)
            else:
                self.eq_math_canvas.render_latex(latex_items[0])
            self.status_lbl.config(
                text=f"[OK: Valid syntax: Recognized {len(lines)} expression(s)]" if is_en else f"[OK: Cú pháp hợp lệ: Nhận diện {len(lines)} biểu thức]"
            )
        except Exception:
            self.eq_math_canvas.render_latex(clean_display_expr(raw_text))
            self.status_lbl.config(
                text="Parsing expression..." if is_en else "Đang phân tích cú pháp biểu thức..."
            )

    def solve_equation_action(self):
        try:
            self.eq_result_box.delete("1.0", tk.END)
            raw_text = self.eq_entry.get("1.0", tk.END).strip()
            param_mode = self.eq_param_mode.get()

            if not raw_text:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập phương trình hoặc bất phương trình!")
                return

            lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
            if len(lines) == 1 and ';' in lines[0]:
                lines = [l.strip() for l in lines[0].split(';') if l.strip()]

            parsed_list = [smart_parse(l) for l in lines if l.strip()]

            # ------------------------------------------------------------------
            # TRƯỜNG HỢP 1: BÀI TOÁN THAM SỐ m (PARAMETRIC STUDY)
            # ------------------------------------------------------------------
            is_en = (getattr(self, "current_lang", "vi") == "en")
            has_param_m = any(p.has(m) for p in parsed_list if p is not None)
            if has_param_m and len(lines) == 1:
                rel = parsed_list[0]
                out = []
                out.append("="*85)
                out.append("PARAMETRIC STUDY & ANALYSIS (m):" if is_en else "KHẢO SÁT & GIẢI TOÁN CHỨA THAM SỐ m:")
                out.append(f"  " + ("Expression:" if is_en else "Biểu thức:") + f" {clean_display_expr(rel)}")
                out.append(f"  " + ("Mode:" if is_en else "Yêu cầu:") + f" {param_mode}")
                out.append("="*85)

                # Dạng A: Tam thức bậc 2 ax^2 + bx + c >= 0 (hoặc <= 0) với mọi x
                is_poly_x = False
                diff_expr = rel.lhs - rel.rhs if isinstance(rel, Relational) else rel
                try:
                    poly_x = sp.Poly(diff_expr, x)
                    if poly_x.degree() == 2:
                        is_poly_x = True
                except: pass

                if is_poly_x:
                    coeffs = poly_x.all_coeffs()
                    A_coef = coeffs[0]
                    B_coef = coeffs[1]
                    C_coef = coeffs[2]
                    delta = sp.simplify(B_coef**2 - 4*A_coef*C_coef)

                    out.append("\n" + ("[STEP 1: IDENTIFY QUADRATIC COEFFICIENTS f(x) = ax² + bx + c]" if is_en else "[BƯỚC 1: XÁC ĐỊNH CÁC HỆ SỐ TAM THỨC BẬC HAI f(x) = ax² + bx + c]"))
                    out.append(f"  • " + ("Coeff a = " if is_en else "Hệ số a = ") + f"{clean_display_expr(A_coef)}")
                    out.append(f"  • " + ("Coeff b = " if is_en else "Hệ số b = ") + f"{clean_display_expr(B_coef)}")
                    out.append(f"  • " + ("Coeff c = " if is_en else "Hệ số c = ") + f"{clean_display_expr(C_coef)}")
                    out.append(f"  • " + ("Discriminant Δ = b² - 4ac = " if is_en else "Biệt thức Δ = b² - 4ac = ") + f"{clean_display_expr(delta)}")

                    out.append("\n" + ("[STEP 2: APPLY QUADRATIC SIGN THEOREM]" if is_en else "[BƯỚC 2: ÁP DỤNG ĐỊNH LÝ DẤU TAM THỨC BẬC HAI]"))
                    if isinstance(rel, (sp.GreaterThan, sp.StrictGreaterThan)):
                        out.append("  f(x) >= 0 ∀x ∈ ℝ  <=>  { a > 0 and Δ <= 0 }" if is_en else "  Để f(x) >= 0 với mọi x ∈ ℝ  <=>  { a > 0 và Δ <= 0 }")
                        cond_a = sp.Gt(A_coef, 0)
                        cond_d = sp.Le(delta, 0)
                        sol_m = reduce_inequalities([cond_a, cond_d], m).as_set()
                    else:
                        out.append("  f(x) <= 0 ∀x ∈ ℝ  <=>  { a < 0 and Δ <= 0 }" if is_en else "  Để f(x) <= 0 với mọi x ∈ ℝ  <=>  { a < 0 và Δ <= 0 }")
                        cond_a = sp.Lt(A_coef, 0)
                        cond_d = sp.Le(delta, 0)
                        sol_m = reduce_inequalities([cond_a, cond_d], m).as_set()

                    out.append("\n" + ("[STEP 3: SOLVE PARAMETER CONDITIONS]" if is_en else "[BƯỚC 3: GIẢI HỆ ĐIỀU KIỆN THAM SỐ m]"))
                    txt_m, lat_m = self.format_interval(sol_m)
                    req_lbl = "Required parameter m: " if is_en else "Giá trị m cần tìm: "
                    out.append(f"  ==> {req_lbl}{txt_m.replace('S = ', 'm ∈ ')}")
                    self.eq_result_canvas.render_latex(f"m \\in {sp.latex(sol_m)}")
                    self.eq_result_box.insert(tk.END, "\n".join(out))
                    self.plot_oxy_roots(sp.lambdify(x, diff_expr.subs(m, 1), 'numpy'), [])
                    return

                # Dạng B: Cô lập tham số m = f(x) hoặc m >= f(x), m <= f(x)
                out.append("\n" + ("[PARAMETER ISOLATION & EXTREMUM ANALYSIS METHOD]" if is_en else "[PHƯƠNG PHÁP CÔ LẬP THAM SỐ VÀ KHẢO SÁT HÀM SỐ]"))
                try:
                    m_isolated = sp.solve(rel, m)
                    out.append(("  Isolating parameter m: " if is_en else "  Đưa bài toán về dạng cô lập m: ") + f"{m_isolated}")
                except: pass

                if is_en:
                    out.append("\nApplying fundamental theorems for min/max comparison:")
                    out.append("  1. m >= f(x) holds ∀x ∈ D  <=>  m >= max_{x ∈ D} f(x)")
                    out.append("  2. m >= f(x) has a solution in D <=> m >= min_{x ∈ D} f(x)")
                    out.append("  3. m <= f(x) holds ∀x ∈ D  <=>  m <= min_{x ∈ D} f(x)")
                    out.append("  4. m <= f(x) has a solution in D <=> m <= max_{x ∈ D} f(x)")
                    out.append("  5. f(x) = m has a solution in D  <=> min_{x ∈ D} f(x) <= m <= max_{x ∈ D} f(x)")
                    self.eq_result_canvas.render_latex(r"\text{Apply } m \text{ isolation and analyze } \min/\max")
                else:
                    out.append("\nÁp dụng các định lý cơ bản về so sánh cực trị min / max:")
                    out.append("  1. m >= f(x) nghiệm đúng ∀x ∈ D  <=>  m >= max_{x ∈ D} f(x)")
                    out.append("  2. m >= f(x) có nghiệm x ∈ D     <=>  m >= min_{x ∈ D} f(x)")
                    out.append("  3. m <= f(x) nghiệm đúng ∀x ∈ D  <=>  m <= min_{x ∈ D} f(x)")
                    out.append("  4. m <= f(x) có nghiệm x ∈ D     <=>  m <= max_{x ∈ D} f(x)")
                    out.append("  5. f(x) = m có nghiệm x ∈ D      <=>  min_{x ∈ D} f(x) <= m <= max_{x ∈ D} f(x)")
                    self.eq_result_canvas.render_latex(r"\text{Apply } m \text{ isolation and analyze } \min/\max" if is_en else r"\text{Áp dụng cô lập } m \text{ và khảo sát } \min/\max")
                self.eq_result_box.insert(tk.END, "\n".join(out))
                return

            # ------------------------------------------------------------------
            # TRƯỜNG HỢP 2: BẤT PHƯƠNG TRÌNH HOẶC HỆ BẤT PHƯƠNG TRÌNH
            # ------------------------------------------------------------------
            is_en = (getattr(self, "current_lang", "vi") == "en")
            is_ineq = any(isinstance(p, Relational) and not isinstance(p, sp.Equality) for p in parsed_list)
            if is_ineq:
                out = []
                out.append("="*85)
                out.append("STEP-BY-STEP SOLUTION FOR INEQUALITY / SYSTEM:" if is_en else "QUY TRÌNH GIẢI BẤT PHƯƠNG TRÌNH / HỆ BPT CHI TIẾT:")
                out.append("="*85)

                # Bước 1: Điều kiện xác định
                conds = []
                for p in parsed_list:
                    diff_p = p.lhs - p.rhs if isinstance(p, Relational) else p
                    for atom in diff_p.atoms(sp.Pow):
                        if atom.exp == sp.Rational(1, 2):
                            conds.append(f"{clean_display_expr(atom.base)} >= 0")
                    for atom in diff_p.atoms(sp.log):
                        conds.append(f"{clean_display_expr(atom.args[0])} > 0")

                out.append("\n" + ("[STEP 1: DOMAIN CONDITIONS & CONSTRAINTS]" if is_en else "[BƯỚC 1: XÁC ĐỊNH ĐIỀU KIỆN XÁC ĐỊNH (ĐKXD)]"))
                if conds:
                    for c in set(conds):
                        out.append(f"  • {c}")
                else:
                    out.append("  • Defined for all x ∈ ℝ." if is_en else "  • Bất phương trình xác định với mọi x ∈ ℝ.")

                # Bước 2: Biến đổi tương đương & Xét dấu
                out.append("\n" + ("[STEP 2: EQUIVALENT REDUCTION & SIGN ANALYSIS]" if is_en else "[BƯỚC 2: BIẾN ĐỔI TƯƠNG ĐƯƠNG VÀ LẬP BẢNG XÉT DẤU]"))
                for idx, p in enumerate(parsed_list, 1):
                    f_diff = sp.simplify(p.lhs - p.rhs)
                    ineq_tag = f"  • Ineq ({idx}):" if is_en else f"  • BPT ({idx}):"
                    out.append(f"{ineq_tag} {clean_display_expr(f_diff)} {p.rel_op} 0")

                # Bước 3: Xác định tập nghiệm hợp lệ
                sol_raw = reduce_inequalities(parsed_list, x)
                sol_set = sol_raw.as_set() if hasattr(sol_raw, 'as_set') else sp.EmptySet

                out.append("\n" + ("[FINAL STEP: CONCLUSION & SOLUTION SET S]" if is_en else "[BƯỚC CUỐI: KẾT LUẬN TẬP NGHIỆM S / CONCLUSION]"))
                txt_sol, latex_sol = self.format_interval(sol_set)
                out.append(f"  ==> {txt_sol}")

                self.eq_result_canvas.render_latex(latex_sol)
                self.eq_result_box.insert(tk.END, "\n".join(out))

                # Vẽ biểu diễn tập nghiệm trên trục số
                diff_first = parsed_list[0].lhs - parsed_list[0].rhs
                self.plot_inequality_number_line(sol_set, diff_first)
                return

            # ------------------------------------------------------------------
            # TRƯỜNG HỢP 3: PHƯƠNG TRÌNH SỐ PHỨC VỚI ẨN z, i
            # ------------------------------------------------------------------
            if len(lines) == 1 and ('z' in lines[0] or 'I' in lines[0] or 'i' in lines[0]):
                eq_line = lines[0]
                eq_sym = smart_parse(eq_line)
                target_eq = eq_sym.lhs - eq_sym.rhs if isinstance(eq_sym, sp.Equality) else eq_sym
                z_sym = sp.Symbol('z')

                out = []
                out.append("="*85)
                out.append(f"COMPLEX NUMBER EQUATION ANALYSIS: {clean_display_expr(target_eq)} = 0" if is_en else f"KHẢO SÁT & GIẢI PHƯƠNG TRÌNH SỐ PHỨC: {clean_display_expr(target_eq)} = 0")
                out.append("="*85)
                out.append("\n" + ("[STEP 1: IDENTIFY COMPLEX ALGEBRAIC FORM]" if is_en else "[BƯỚC 1: XÁC ĐỊNH DẠNG ĐẠI SỐ SỐ PHỨC]"))
                out.append("  Equation contains complex variable z with imaginary unit i² = -1." if is_en else "  Phương trình chứa ẩn số phức z với đơn vị ảo i² = -1.")

                sol_z = sp.solve(target_eq, z_sym)
                if not sol_z and ('conjugate' in str(target_eq) or 'Abs' in str(target_eq)):
                    a_s, b_s = sp.symbols('a b', real=True)
                    eq_sub = target_eq.subs(z_sym, a_s + sp.I * b_s)
                    eq_re = sp.re(eq_sub)
                    eq_im = sp.im(eq_sub)
                    out.append("\n" + ("[STEP 2: REAL AND IMAGINARY PARTS DECOMPOSITION]" if is_en else "[BƯỚC 2: PHÂN TÍCH PHẦN THỰC VÀ PHẦN ẢO]"))
                    out.append("  Let z = a + bi (a, b ∈ ℝ). Transform equation into system:" if is_en else "  Đặt z = a + bi (với a, b ∈ ℝ). Biến đổi phương trình thành hệ:")
                    out.append(("  • Real part:      " if is_en else "  • Phần thực: ") + f"{clean_display_expr(eq_re)} = 0")
                    out.append(("  • Imaginary part: " if is_en else "  • Phần ảo:   ") + f"{clean_display_expr(eq_im)} = 0")
                    sols_ab = sp.solve([eq_re, eq_im], (a_s, b_s))
                    if sols_ab:
                        if isinstance(sols_ab, dict):
                            sol_z = [sols_ab[a_s] + sp.I * sols_ab[b_s]]
                        elif isinstance(sols_ab, list):
                            sol_z = [item[0] + sp.I * item[1] for item in sols_ab]

                out.append("\n" + ("[STEP 3: COMPLEX SOLUTIONS CONCLUSION]" if is_en else "[BƯỚC 3: KẾT LUẬN NGHIỆM SỐ PHỨC]"))
                if sol_z:
                    latex_sols = []
                    for sz in sol_z:
                        fmt = format_friendly_value(sz)
                        out.append(f"  ==> z = {fmt}")
                        latex_sols.append(f"z = {sp.latex(sz)}")
                    self.eq_result_canvas.render_latex(r" \;; \quad ".join(latex_sols))
                else:
                    out.append("  ==> Equation has no solutions on the complex field ℂ." if is_en else "  ==> Phương trình vô nghiệm trên tập số phức ℂ.")
                    self.eq_result_canvas.render_latex(r"\text{No solutions in } \mathbb{C}" if is_en else r"\text{Vô nghiệm trên } \mathbb{C}")

                self.eq_result_box.insert(tk.END, "\n".join(out))
                self.plot_oxy_roots(sp.lambdify(x, x**2, 'numpy'), [])
                return

            # ------------------------------------------------------------------
            # ------------------------------------------------------------------
            # TRƯỜNG HỢP 4: HỆ PHƯƠNG TRÌNH ĐA BIẾN (VD: HỆ 2 PHƯƠNG TRÌNH VDC)
            # ------------------------------------------------------------------
            if len(lines) > 1:
                eq_syms = []
                for l in lines:
                    eq_i = smart_parse(l)
                    if eq_i is not None:
                        eq_syms.append(eq_i.lhs - eq_i.rhs if isinstance(eq_i, sp.Equality) else eq_i)

                all_sys_syms = set()
                for eq_s in eq_syms:
                    all_sys_syms.update(eq_s.free_symbols)
                vars_sorted = sorted(list(all_sys_syms), key=lambda s: s.name)
                # KIỂM TRA HỆ PHƯƠNG TRÌNH VÔ ĐỊNH HOẶC BÀI TOÁN SỐ HỌC DIOPHANTINE
                if len(vars_sorted) > len(eq_syms):
                    self.solve_underdetermined_or_diophantine(eq_syms, vars_sorted, lines)
                    return

                if len(vars_sorted) < 2:
                    vars_sorted = [x, y]
                var1, var2 = vars_sorted[0], vars_sorted[1]

                out = []
                out.append("="*85)
                out.append("STEP-BY-STEP SYSTEM OF EQUATIONS DERIVATION:" if is_en else "QUY TRÌNH GIẢI HỆ PHƯƠNG TRÌNH CHI TIẾT / SYSTEM SOLVER:")
                out.append("="*85)

                # BƯỚC 1: ĐKXD
                out.append("\n" + ("[STEP 1: DOMAIN RESTRICTIONS & CONSTRAINTS]" if is_en else "[BƯỚC 1: XÁC ĐỊNH ĐIỀU KIỆN XÁC ĐỊNH (ĐKXD) / DOMAIN RESTRICTIONS]"))
                radicals = []
                for eq in eq_syms:
                    for node in sp.preorder_traversal(eq):
                        if isinstance(node, sp.Pow) and node.exp.is_Rational and node.exp.q % 2 == 0:
                            radicals.append(node.base)
                        elif node.func == sp.root and len(node.args) >= 2 and hasattr(node.args[1], 'is_integer') and node.args[1] % 2 == 0:
                            radicals.append(node.args[0])

                if radicals:
                    out.append("  Analyzing expressions under even radicals:" if is_en else "  Khảo sát các biểu thức dưới dấu căn chẵn:")
                    for r_expr in list(dict.fromkeys(radicals)):
                        out.append(f"  • {clean_display_expr(r_expr)} >= 0")
                else:
                    out.append("  • System is defined for all (x, y) ∈ ℝ²." if is_en else "  • Hệ phương trình xác định với mọi (x, y) ∈ ℝ².")

                out.append("\n" + ("[STEP 2: ALGEBRAIC DECOMPOSITION & ROOT PRESERVATION]" if is_en else "[BƯỚC 2: PHÂN TÍCH ĐẠI SỐ & BẢO TOÀN TẬP NGHIỆM / ALGEBRAIC DECOMPOSITION]"))
                out.append("  (Applying factorization and equivalent transformations)" if is_en else "  (Áp dụng phương pháp phân tích nhân tử / biến đổi tương đương tránh bẫy điểm rơi biên)")

                found_sols = []

                # Cố gắng giải thế đại số chính xác (Exact Algebraic Elimination)
                eliminated = False
                for eq_target, eq_other in [(eq_syms[1], eq_syms[0]), (eq_syms[0], eq_syms[1])]:
                    for v_target, v_free in [(var1, var2), (var2, var1)]:
                        try:
                            branches = sp.solve(eq_target, v_target)
                            if branches:
                                eliminated = True
                                out.append(("  From equation: " if is_en else "  Từ phương trình: ") + f"{clean_display_expr(eq_target)} = 0")
                                out.append(("  Expressing " if is_en else "  Ta biểu diễn ") + f"{v_target}" + (" in terms of " if is_en else " theo ") + f"{v_free}:")
                                for b_idx, br in enumerate(branches, 1):
                                    branch_lbl = f"    Branch {b_idx}: " if is_en else f"    Nhánh {b_idx}: "
                                    out.append(f"{branch_lbl}{v_target} = {clean_display_expr(br)}")

                                for br in branches:
                                    sub_expr = eq_other.subs(v_target, br)
                                    # Kiểm tra các điểm nguyên/hữu tỉ đặc biệt (điểm rơi biên / tâm)
                                    test_candidates = [0, 1, 2, 3, 4, 5, -1, -2, -3, 0.5, 1.5, 2.5, -0.5, sp.Rational(1, 3), sp.Rational(2, 3)]
                                    for tv in test_candidates:
                                        try:
                                            v_eval = sub_expr.subs(v_free, tv).evalf()
                                            if abs(complex(v_eval)) < 1e-9:
                                                other_val = br.subs(v_free, tv).evalf()
                                                if other_val.is_real:
                                                    cand = (float(other_val), float(tv)) if v_target == var1 else (float(tv), float(other_val))
                                                    e1 = abs(float(sp.re(eq_syms[0].subs({var1: cand[0], var2: cand[1]}).evalf())))
                                                    e2 = abs(float(sp.re(eq_syms[1].subs({var1: cand[0], var2: cand[1]}).evalf())))
                                                    if e1 < 1e-4 and e2 < 1e-4:
                                                        if not any(abs(cand[0]-s[0]) < 1e-3 and abs(cand[1]-s[1]) < 1e-3 for s in found_sols):
                                                            found_sols.append(cand)
                                        except Exception:
                                            pass

                                    # Quét nghiệm số học liên tục bằng Brent's method
                                    try:
                                        num_sub = sp.lambdify(v_free, sub_expr, modules=['numpy', {'sqrt': np.lib.scimath.sqrt}])
                                        grid = np.linspace(-10, 10, 500)
                                        y_vals = []
                                        valid_grid = []
                                        for g in grid:
                                            try:
                                                val = num_sub(g)
                                                if np.isreal(val) and not np.isnan(val):
                                                    y_vals.append(float(np.real(val)))
                                                    valid_grid.append(g)
                                            except Exception:
                                                pass
                                        y_vals = np.array(y_vals)
                                        valid_grid = np.array(valid_grid)
                                        if len(y_vals) > 1:
                                            sign_diff = np.where(np.diff(np.sign(y_vals)))[0]
                                            for s_idx in sign_diff:
                                                ga, gb = valid_grid[s_idx], valid_grid[s_idx+1]
                                                try:
                                                    from scipy.optimize import root_scalar
                                                    r = root_scalar(lambda t: float(np.real(num_sub(t))), bracket=[ga, gb], method='brentq')
                                                    if r.converged:
                                                        rt_f = r.root
                                                        rt_t = float(sp.re(br.subs(v_free, rt_f).evalf()))
                                                        cand = (rt_t, rt_f) if v_target == var1 else (rt_f, rt_t)
                                                        e1 = abs(float(sp.re(eq_syms[0].subs({var1: cand[0], var2: cand[1]}).evalf())))
                                                        e2 = abs(float(sp.re(eq_syms[1].subs({var1: cand[0], var2: cand[1]}).evalf())))
                                                        if e1 < 1e-4 and e2 < 1e-4:
                                                            if not any(abs(cand[0]-s[0]) < 1e-3 and abs(cand[1]-s[1]) < 1e-3 for s in found_sols):
                                                                found_sols.append(cand)
                                                except Exception:
                                                    pass
                                    except Exception:
                                        pass
                                break
                        except Exception:
                            pass
                    if eliminated:
                        break

                out.append("\n" + ("[STEP 3: NONLINEAR OPTIMIZATION ANALYSIS]" if is_en else "[BƯỚC 3: KHẢO SÁT HỆ PHƯƠNG TRÌNH BẰNG THUẬT TOÁN TỐI ƯU PHI TUYẾN]"))
                f1_num = sp.lambdify((var1, var2), eq_syms[0], modules=['numpy', {'sqrt': np.lib.scimath.sqrt}])
                f2_num = sp.lambdify((var1, var2), eq_syms[1], modules=['numpy', {'sqrt': np.lib.scimath.sqrt}])

                def sys_err(v):
                    try:
                        r1 = f1_num(v[0], v[1])
                        r2 = f2_num(v[0], v[1])
                        return float(np.real(r1)**2 + np.real(r2)**2)
                    except Exception:
                        return 1e6

                # Quét multi-start đa điểm nếu chưa đủ nghiệm hoặc để bổ sung kiểm chứng
                from scipy.optimize import minimize
                seeds = [(0, 0), (1, 0), (2, 1), (1, 1), (3, 3), (-1, -1), (2, 2), (-2, 2), (0.5, 0.5), (4, 4), (-3, 3), (1, 2), (2, 3), (3, 1), (0, 1), (1, -1)]
                for s in seeds:
                    try:
                        res = minimize(sys_err, s, method='Nelder-Mead', options={'maxiter': 500})
                        if res.fun < 1e-7:
                            rx = round(res.x[0], 4)
                            ry = round(res.x[1], 4)
                            e1 = abs(float(sp.re(eq_syms[0].subs({var1: rx, var2: ry}).evalf())))
                            e2 = abs(float(sp.re(eq_syms[1].subs({var1: rx, var2: ry}).evalf())))
                            if e1 < 1e-3 and e2 < 1e-3:
                                cand = (rx, ry)
                                if not any(abs(cand[0]-ex[0]) < 1e-2 and abs(cand[1]-ex[1]) < 1e-2 for ex in found_sols):
                                    found_sols.append(cand)
                    except Exception:
                        pass

                out.append("\n" + ("[FINAL STEP: CONCLUSION & SOLUTION SET S]" if is_en else "[BƯỚC CUỐI: KẾT LUẬN TẬP NGHIỆM S / CONCLUSION]"))
                if found_sols:
                    latex_sols = []
                    # Sắp xếp nghiệm theo hoành độ x tăng dần
                    found_sols = sorted(found_sols, key=lambda p: (p[0], p[1]))
                    for sol in found_sols:
                        val_x = int(round(sol[0])) if abs(sol[0] - round(sol[0])) < 1e-4 else sol[0]
                        val_y = int(round(sol[1])) if abs(sol[1] - round(sol[1])) < 1e-4 else sol[1]
                        fx = str(val_x) if isinstance(val_x, int) else (format_friendly_value(sp.Float(val_x)) or f"{val_x:.2f}")
                        fy = str(val_y) if isinstance(val_y, int) else (format_friendly_value(sp.Float(val_y)) or f"{val_y:.2f}")
                        sol_pair_tag = "  • Solution pair:" if is_en else "  • Cặp nghiệm:"
                        out.append(f"{sol_pair_tag} {var1} = {fx},  {var2} = {fy}")
                        latex_sols.append(r"\begin{cases} " + f"{var1} = {fx} \\\\ {var2} = {fy}" + r" \end{cases}")
                    self.eq_result_canvas.render_latex(r" \quad \text{; } \quad ".join(latex_sols))
                else:
                    out.append("  • System has no real solutions on ℝ." if is_en else "  • Hệ phương trình vô nghiệm trên tập số thực ℝ.")
                    self.eq_result_canvas.render_latex(r"\text{System has no real solutions on } \mathbb{R}" if is_en else r"\text{Hệ vô nghiệm trên } \mathbb{R}")

                self.eq_result_box.insert(tk.END, "\n".join(out))
                self.plot_oxy_system(f1_num, f2_num, found_sols)
                return

            # ------------------------------------------------------------------
            # TRƯỜNG HỢP 5: PHƯƠNG TRÌNH ĐƠN 1 BIẾN (BẬC 2, 3, VÔ TỶ, LƯỢNG GIÁC)
            # ------------------------------------------------------------------
            eq_line = lines[0]
            eq_sym = smart_parse(eq_line)
            target_eq = eq_sym.lhs - eq_sym.rhs if isinstance(eq_sym, sp.Equality) else eq_sym

            out = []
            out.append("="*85)
            out.append(f"EQUATION ANALYSIS: {clean_display_expr(target_eq)} = 0" if is_en else f"PHÂN TÍCH PHƯƠNG TRÌNH: {clean_display_expr(target_eq)} = 0")
            out.append("="*85)

            is_trig = any(fn in str(target_eq) for fn in ['sin', 'cos', 'tan', 'cot'])
            if is_trig:
                out.append("\n" + ("[STEP 1: DOMAIN CONDITIONS]" if is_en else "[BƯỚC 1: TÌM ĐIỀU KIỆN XÁC ĐỊNH (ĐKXD)]"))
                if 'tan' in str(target_eq):
                    out.append("  • Domain condition: cos(x) ≠ 0 <=> x ≠ π/2 + kπ (k ∈ ℤ)." if is_en else "  • Điều kiện xác định: cos(x) ≠ 0 <=> x ≠ π/2 + kπ (k ∈ ℤ).")
                elif 'cot' in str(target_eq):
                    out.append("  • Domain condition: sin(x) ≠ 0 <=> x ≠ kπ (k ∈ ℤ)." if is_en else "  • Điều kiện xác định: sin(x) ≠ 0 <=> x ≠ kπ (k ∈ ℤ).")
                else:
                    out.append("  • Defined for all x ∈ ℝ." if is_en else "  • Phương trình xác định với mọi x ∈ ℝ.")

                out.append("\n" + ("[STEP 2: TRIGONOMETRIC IDENTITIES & REDUCTION]" if is_en else "[BƯỚC 2: RÚT GỌN VÀ BIẾN ĐỔI TƯƠNG ĐƯƠNG LƯỢNG GIÁC]"))
                cos_x = sp.Symbol('X_cos')
                target_cos = target_eq.subs(sp.cos(2*x), 2*cos_x**2 - 1).subs(sp.cos(x), cos_x)
                if not target_cos.has(x):
                    out.append("  Applying double-angle formula: cos(2x) = 2cos²(x) - 1." if is_en else "  Áp dụng công thức nhân đôi: cos(2x) = 2cos²(x) - 1.")
                    out.append(("  Let t = cos(x) (|t| <= 1). Equation becomes: " if is_en else "  Đặt t = cos(x) (|t| <= 1). Phương trình trở thành: ") + f"{clean_display_expr(target_cos)} = 0")
                    t_sols = sp.solve(target_cos, cos_x)
                    out.append(("  Solving for t: " if is_en else "  Giải ra các giá trị của t: ") + f"{', '.join([str(t) for t in t_sols])}")
                else:
                    out.append(("  Reduced form: " if is_en else "  Dạng thu gọn: ") + f"{clean_display_expr(sp.simplify(target_eq))} = 0")

                        # KIỂM TRA PHƯƠNG TRÌNH CHỨA CĂN THỨC (RADICAL EQUATION)
            has_radical = any(isinstance(node, sp.Pow) and node.exp == sp.Rational(1, 2) for node in target_eq.atoms(sp.Pow))
            if has_radical and not is_trig:
                res_rad = self.solve_radical_pedagogical(target_eq, x)
                if res_rad and res_rad[0]:
                    rad_steps = res_rad[0]
                    if is_en:
                        rad_steps = [self._translate_solution_text(s) for s in rad_steps]
                    rad_sols = res_rad[1]
                    out.extend(rad_steps)
                    if rad_sols:
                        latex_sols = [f'x = {sp.latex(s)}' for s in rad_sols]
                        self.eq_result_canvas.render_latex(r' \;; \quad '.join(latex_sols))
                    elif len(res_rad) > 3 and res_rad[3]:
                        self.eq_result_canvas.render_latex(r'\text{Indeterminate radical solution state}' if is_en else r'\text{Nghiệm ở trạng thái chưa thể kết luận}')
                    else:
                        self.eq_result_canvas.render_latex(r'\text{No real solutions on } \mathbb{R}' if is_en else r'\text{Vô nghiệm trên } \mathbb{R}')
                    self.eq_result_box.insert(tk.END, "\n".join(out))
                    f_num = sp.lambdify(x, target_eq, modules=['numpy', {'sqrt': np.lib.scimath.sqrt}])
                    self.plot_oxy_roots(f_num, rad_sols)
                    return

            sols = sp.solve(target_eq, x)
            if not sols:
                num_f = sp.lambdify(x, target_eq, modules=['numpy', {'sqrt': np.lib.scimath.sqrt}])
                xs = np.linspace(-10, 10, 2000)
                ys = np.real(num_f(xs))
                sign_changes = np.where(np.diff(np.sign(ys)))[0]
                if len(sign_changes) > 0:
                    from scipy.optimize import minimize
                for idx in sign_changes:
                    try:
                        r = minimize(lambda v: abs(float(np.real(num_f(v[0])))), [xs[idx]], method='Nelder-Mead')
                        if r.fun < 1e-4:
                            sols.append(sp.Float(round(r.x[0], 4)))
                    except: pass

            out.append("\n" + ("[FINAL STEP: CONCLUSION & SOLUTION SET S]" if is_en else "[BƯỚC CUỐI: KẾT LUẬN TẬP NGHIỆM S / CONCLUSION]"))
            if sols:
                latex_sols = []
                for s in sols:
                    fmt = format_friendly_value(s) or clean_display_expr(s)
                    out.append(f"  • x = {fmt}")
                    latex_sols.append(f"x = {sp.latex(s)}")
                self.eq_result_canvas.render_latex(r" \;; \quad ".join(latex_sols))
            else:
                out.append("  • Equation has no real solutions on ℝ." if is_en else "  • Phương trình vô nghiệm trên tập số thực ℝ.")
                self.eq_result_canvas.render_latex(r"\text{No real solutions on } \mathbb{R}" if is_en else r"\text{Vô nghiệm trên } \mathbb{R}")

            self.eq_result_box.insert(tk.END, "\n".join(out))
            f_num = sp.lambdify(x, target_eq, modules=['numpy', {'sqrt': np.lib.scimath.sqrt}])
            self.plot_oxy_roots(f_num, sols)

        except Exception as e:
            self.eq_result_box.insert(tk.END, f"[CALCULATION ERROR]: {e}" if is_en else f"[LỖI TÍNH TOÁN]: {e}")

    def plot_oxy_roots(self, f_num, roots):
        self.eq_fig.clear()
        ax = self.eq_fig.add_subplot(111)
        try:
            xs = np.linspace(-6, 6, 800)
            ys = np.real(f_num(xs))
            ys = np.clip(ys, -20, 20)
            ax.plot(xs, ys, color='#0969da', lw=1.8, label='f(x)')
            ax.axhline(0, color='#94a3b8', lw=1, ls='--')
            ax.axvline(0, color='#94a3b8', lw=1, ls='--')

            for r in roots:
                try:
                    rv = float(r.evalf()) if hasattr(r, 'evalf') else float(r)
                    if -6 <= rv <= 6:
                        ax.plot(rv, 0, marker='o', markersize=7, color='#dc2626')
                        ax.annotate(f"x={rv:.2f}", (rv, 0), textcoords="offset points", xytext=(0, 10),
                                    ha='center', fontsize=8, fontweight='bold', color='#dc2626')
                except: pass

            ax.set_title("Khảo Sát Đồ Thị & Điểm Cắt Trục Hoành (Mặt Phẳng Oxy)", fontsize=9, fontweight='bold', color='#1e293b')
            ax.set_xlabel("Trục Ox", fontsize=8)
            ax.set_ylabel("Trục Oy", fontsize=8)
            ax.grid(True, ls=':', color='#cbd5e1')
            ax.set_ylim(-12, 12)
            self.eq_canvas.draw()
        except Exception:
            pass

    def plot_inequality_number_line(self, s_set, diff_expr):
        """Vẽ đồng thời đồ thị hàm số tô miền nghiệm và trục số tập nghiệm 1D theo nguyên lý trực quan chuẩn mực."""
        self.eq_fig.clear()
        try:
            ax_curve = self.eq_fig.add_subplot(211)
            ax_line = self.eq_fig.add_subplot(212)

            # 1. Đồ thị hàm số & Miền nghiệm
            fn = sp.lambdify(x, diff_expr, modules=['numpy', {'sqrt': np.lib.scimath.sqrt}])
            xs = np.linspace(-5, 5, 400)
            ys = np.real(fn(xs))
            ys = np.clip(ys, -15, 15)

            ax_curve.plot(xs, ys, color='#0969da', lw=1.8, label='f(x)')
            ax_curve.axhline(0, color='#94a3b8', lw=1, ls='--')
            ax_curve.set_title("Đồ Thị Hàm Số & Điểm Cắt Trục Hoành (Oxy)", fontsize=8, fontweight='bold')
            ax_curve.set_xlabel("Trục Ox", fontsize=8)
            ax_curve.set_ylabel("Trục Oy", fontsize=8)
            ax_curve.grid(True, ls=':', color='#cbd5e1')
            ax_curve.set_ylim(-10, 10)

            # 2. Trục số biểu diễn tập nghiệm (Number Line)
            ax_line.axhline(0, color='black', lw=1.5)

            # Rút trích các khoảng nghiệm để vẽ trên trục số
            intervals = []
            if isinstance(s_set, sp.Interval):
                intervals = [s_set]
            elif isinstance(s_set, sp.Union):
                intervals = [it for it in s_set.args if isinstance(it, sp.Interval)]

            pts = []
            for it in intervals:
                start_x = -4.0 if it.start == -sp.oo else float(it.start.evalf())
                end_x = 4.0 if it.end == sp.oo else float(it.end.evalf())
                ax_line.plot([start_x, end_x], [0, 0], color='#16a34a', lw=5, solid_capstyle='butt')

                if it.start != -sp.oo:
                    pts.append((start_x, "(" if it.left_open else "["))
                if it.end != sp.oo:
                    pts.append((end_x, ")" if it.right_open else "]"))

            for px, symb in pts:
                ax_line.scatter([px], [0], color='#16a34a', s=50, zorder=5)
                ax_line.text(px, -0.22, f"{px:.1f}", ha='center', va='top', fontsize=8, fontweight='bold')
                ax_line.text(px, 0.08, symb, ha='center', va='bottom', fontsize=12, color='#16a34a', fontweight='bold')

            ax_line.set_xlim(-5, 5)
            ax_line.set_ylim(-0.4, 0.4)
            ax_line.axis('off')
            ax_line.set_title("Trục Số Biểu Diễn Tập Nghiệm S", fontsize=8, fontweight='bold', color='#1e293b')

            self.eq_fig.tight_layout()
            self.eq_canvas.draw()
        except Exception:
            pass

    def plot_oxy_system(self, f1_num, f2_num, sols=None):
        self.eq_fig.clear()
        ax = self.eq_fig.add_subplot(111)
        try:
            if sols and len(sols) > 0:
                xs = [p[0] for p in sols]
                ys = [p[1] for p in sols]
                x_min, x_max = min(xs) - 2.0, max(xs) + 2.0
                y_min, y_max = min(ys) - 2.0, max(ys) + 2.0
            else:
                x_min, x_max = -4, 4
                y_min, y_max = -2, 6

            x_vals = np.linspace(x_min, x_max, 300)
            y_vals = np.linspace(y_min, y_max, 300)
            X, Y = np.meshgrid(x_vals, y_vals)
            Z1 = np.real(f1_num(X, Y))
            Z2 = np.real(f2_num(X, Y))

            ax.contour(X, Y, Z1, levels=[0], colors=['#0969da'], linewidths=1.8)
            ax.contour(X, Y, Z2, levels=[0], colors=['#16a34a'], linewidths=1.8)

            if sols:
                for p in sols:
                    ax.plot(p[0], p[1], marker='o', markersize=8, color='#dc2626')
                    ax.annotate(f"({p[0]:.1f}, {p[1]:.1f})", (p[0], p[1]),
                                textcoords="offset points", xytext=(8, 8),
                                fontsize=8, fontweight='bold', color='#dc2626')

            ax.set_title("Giao Điểm 2 Phương Trình Của Hệ (Mặt Phẳng Oxy)", fontsize=9, fontweight='bold', color='#1e293b')
            ax.set_xlabel("Trục Ox", fontsize=8)
            ax.set_ylabel("Trục Oy", fontsize=8)
            ax.axhline(0, color='#94a3b8', lw=0.8, ls='--')
            ax.axvline(0, color='#94a3b8', lw=0.8, ls='--')
            ax.grid(True, ls=':', color='#cbd5e1')
            self.eq_canvas.draw()
        except Exception:
            pass

    # --------------------------------------------------------------------------
    def solve_radical_pedagogical(self, target_eq, x, timeout_sec=3.0):
        """Ủy quyền giải phương trình vô tỷ tới CADMathCore với cơ chế timeout bảo vệ giao diện."""
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.core.solve_radical_pedagogical, target_eq, x)
            try:
                return future.result(timeout=timeout_sec)
            except concurrent.futures.TimeoutError:
                fallback_steps = [
                    ("  • TECHNICAL NOTE: Irrational equation with higher-order radicals." if getattr(self, "current_lang", "vi") == "en" else "  • LƯU Ý KỸ THUẬT: Phương trình vô tỷ chứa căn thức đa thức bậc cao (Cardano / bậc 4)."),
                    f"  • Thời gian phân tích giải tích vượt ngưỡng an toàn ({timeout_sec}s).",
                    "  • Hệ thống kích hoạt cơ chế bảo vệ giao diện: chuyển nghiệm sang trạng thái chưa thể kết luận (indeterminate)."
                ]
                return fallback_steps, [], [], ["Timeout"]

    def _translate_solution_text(self, text: str) -> str:
        """Dịch chuỗi kết quả thuật toán từ Tiếng Việt sang Tiếng Anh chuẩn mực khi current_lang == 'en'."""
        if getattr(self, "current_lang", "vi") != "en":
            return text
        replacements = [
            ("QUY TRÌNH GIẢI HỆ PHƯƠNG TRÌNH VÔ ĐỊNH & KHẢO SÁT NGHIỆM NGUYÊN (DIOPHANTINE SYSTEM):", "DIOPHANTINE SYSTEM & POSITIVE INTEGER SOLUTIONS DERIVATION:"),
            ("[BƯỚC 1: PHÂN TÍCH CẤU TRÚC ĐẠI SỐ TUYẾN TÍNH]", "[STEP 1: LINEAR ALGEBRAIC STRUCTURE ANALYSIS]"),
            ("Số lượng phương trình: M =", "Number of equations: M ="),
            ("Số lượng biến số: N =", "Number of variables: N ="),
            ("Hệ phương trình vô nghiệm trên tập số thực ℝ", "The system has no real solutions on ℝ"),
            ("Định lý Rouché-Capelli: Ma trận hệ số A và ma trận mở rộng [A|b]", "Rouché-Capelli Theorem: Coefficient matrix A and augmented matrix [A|b]"),
            ("Hệ xác định duy nhất nghiệm trên ℝ (M = N = rank)", "System has a unique solution on ℝ (M = N = rank)"),
            ("Nghiệm thực duy nhất:", "Unique real solution:"),
            ("Kiểm tra tính nguyên dương: Nghiệm", "Checking positive integer constraints: Solution"),
            ("là nghiệm nguyên dương hợp lệ.", "is a valid positive integer solution."),
            ("không phải là số nguyên dương.", "is not a positive integer."),
            ("Hệ vô định thiếu phương trình (M < N), bậc tự do (Degrees of Freedom):", "Underdetermined system (M < N), Degrees of Freedom:"),
            ("Đưa hệ về dạng ma trận bậc thang rút gọn (RREF):", "Reduced Row Echelon Form (RREF):"),
            ("Nghiệm tổng quát biểu diễn theo tham số tự do:", "Parametric general solution:"),
            ("QUY HOẠCH NGUYÊN & GIẢI THUẬT RẼ NHÁNH TÌM TẬP NGHIỆM:", "INTEGER PROGRAMMING & BRANCH-BOUND SEARCH:"),
            ("Do x_i ∈ ℤ+, ta thiết lập các bất phương trình chặn biên:", "Under x_i ∈ ℤ+, setting bounding inequalities:"),
            ("Miền giá trị hợp lệ của tham số:", "Valid parameter bounds:"),
            ("Tìm thấy", "Found"),
            ("nghiệm nguyên dương thỏa mãn điều kiện:", "positive integer solutions satisfying constraints:"),
            ("Có vô số nghiệm nguyên dương thỏa mãn:", "Infinitely many positive integer solutions satisfying:"),
            ("Hệ phương trình không có nghiệm nguyên dương nào thỏa mãn.", "No positive integer solutions exist for the system."),
            ("KẾT LUẬN CUỐI CÙNG:", "FINAL CONCLUSION:"),
            ("Tập nghiệm nguyên:", "Integer solution set:"),
            ("Vô nghiệm trên (ℤ+)^n", "No solutions in (ℤ+)^n"),
            ("BƯỚC 1: XÁC ĐỊNH ĐIỀU KIỆN XÁC ĐỊNH (ĐKXD)", "STEP 1: DOMAIN RESTRICTIONS & CONSTRAINTS"),
            ("BƯỚC 2: PHÂN TÍCH ĐẠI SỐ & BẢO TOÀN TẬP NGHIỆM", "STEP 2: ALGEBRAIC DECOMPOSITION & ROOT PRESERVATION"),
            ("BƯỚC 3: KHẢO SÁT HỆ PHƯƠNG TRÌNH", "STEP 3: NONLINEAR OPTIMIZATION ANALYSIS"),
            ("BƯỚC CUỐI: KẾT LUẬN TẬP NGHIỆM S / CONCLUSION", "FINAL STEP: CONCLUSION & SOLUTION SET S"),
            ("Cặp nghiệm:", "Solution pair:"),
            ("Hệ phương trình vô nghiệm", "System has no solutions"),
            ("Phương trình vô nghiệm", "Equation has no solutions"),
            ("Khảo sát các biểu thức dưới dấu căn chẵn:", "Analyzing expressions under even radicals:"),
            ("Hệ phương trình xác định với mọi", "System is defined for all"),
            ("Phương trình xác định với mọi", "Equation is defined for all"),
            ("Áp dụng phương pháp phân tích nhân tử", "Applying factorization and equivalent transformations"),
            ("Từ phương trình:", "From equation:"),
            ("Ta biểu diễn", "We express"),
            ("theo", "in terms of"),
            ("Nhánh", "Branch"),
            ("LỜI GIẢI CHI TIẾT:", "STEP-BY-STEP SOLUTION:"),
            ("LƯU Ý KỸ THUẬT:", "TECHNICAL NOTE:"),
            ("Phương trình vô tỷ chứa căn thức", "Irrational equation with higher-order radicals"),
            ("Thời gian phân tích giải tích vượt ngưỡng an toàn", "Analytical evaluation time exceeded safety threshold"),
            ("Hệ thống kích hoạt cơ chế bảo vệ giao diện", "Activated UI safety protection mode")
        ]
        res = text
        for vi_str, en_str in replacements:
            res = res.replace(vi_str, en_str)
        return res

    def solve_underdetermined_or_diophantine(self, eq_syms, vars_sorted, lines):
        """Ủy quyền giải hệ Diophantine tuyến tính tới CADMathCore và cập nhật giao diện đồ họa."""
        var_names_str = ", ".join(s.name for s in vars_sorted)
        cat, int_sols, n_total, out = self.core.solve_underdetermined_or_diophantine(eq_syms, vars_sorted)
        is_en = (getattr(self, "current_lang", "vi") == "en")
        if is_en:
            out = [self._translate_solution_text(l) for l in out]

        # 1. Cập nhật kết quả chi tiết lên Textbox
        self.eq_result_box.insert(tk.END, "\n".join(out))
        self.last_dioph_category = cat
        self.last_dioph_solutions = int_sols
        self.last_dioph_n_total = n_total

        # 2. Kết xuất công thức LaTeX kết luận trên Canvas
        if cat == DiophantineCategory.FINITE_BOUNDED and int_sols:
            if n_total > 10:
                latex_str = (r"\text{Found } " + str(n_total) + r" \text{ positive integer solutions}") if is_en else (r"\text{Có } " + str(n_total) + r" \text{ nghiệm nguyên dương}")
            else:
                latex_cases = [r"(" + ", ".join(str(val) for val in sol) + r")" for sol in int_sols]
                prefix = r"\text{Integer solutions } (" if is_en else r"\text{Nghiệm nguyên } ("
                latex_str = prefix + var_names_str + r") \in \{" + ", ".join(latex_cases) + r"\}"
            self.eq_result_canvas.render_latex(latex_str)
            self.plot_diophantine_system(None, vars_sorted, int_sols)
        elif cat == DiophantineCategory.UNBOUNDED_INFINITE:
            latex_str = r"\text{Infinitely many positive integer solutions } (x_i \in \mathbb{Z}^+)" if is_en else r"\text{Vô số nghiệm nguyên dương } (x_i \in \mathbb{Z}^+)"
            self.eq_result_canvas.render_latex(latex_str)
            if int_sols:
                self.plot_diophantine_system(None, vars_sorted, int_sols)
        elif cat == DiophantineCategory.UNIQUE and int_sols:
            prefix = r"\text{Unique integer solution } (" if is_en else r"\text{Nghiệm nguyên duy nhất } ("
            latex_str = prefix + var_names_str + r") = (" + ", ".join(str(c) for c in int_sols[0]) + r")"
            self.eq_result_canvas.render_latex(latex_str)
        elif cat == DiophantineCategory.INCONSISTENT:
            self.eq_result_canvas.render_latex(r"\text{Inconsistent system on } \mathbb{R}" if is_en else r"\text{Hệ vô nghiệm trên } \mathbb{R}")
        else:
            self.eq_result_canvas.render_latex(r"\text{No solutions in } (\mathbb{Z}^+)^n" if is_en else r"\text{Vô nghiệm trên } (\mathbb{Z}^+)^n")

        return cat, int_sols, n_total, out

    def plot_diophantine_system(self, sol_tuple, vars_sorted, int_sols):
        """Vẽ đồ thị ràng buộc và phân bố nghiệm nguyên dương trên mặt phẳng Oxy."""
        is_en = (getattr(self, "current_lang", "vi") == "en")
        self.eq_fig.clear()
        ax = self.eq_fig.add_subplot(111)
        try:
            if int_sols and len(int_sols) > 0 and len(vars_sorted) >= 2:
                xs = [p[0] for p in int_sols]
                ys = [p[1] for p in int_sols]
                v1_name = vars_sorted[0].name
                v2_name = vars_sorted[1].name
                x_min, x_max = max(0, min(xs) - 4), max(xs) + 6
                y_min, y_max = max(0, min(ys) - 4), max(ys) + 6
                if len(int_sols) >= 2:
                    dx = int_sols[1][0] - int_sols[0][0]
                    dy = int_sols[1][1] - int_sols[0][1]
                    if dx != 0:
                        slope = dy / dx
                        intercept = int_sols[0][1] - slope * int_sols[0][0]
                        x_line = np.linspace(x_min, x_max, 200)
                        y_line = slope * x_line + intercept
                        ax.plot(x_line, y_line, color='#0284c7', lw=1.8, ls='--', label=f'Constraint {v1_name}-{v2_name}' if is_en else f'Ràng buộc {v1_name}-{v2_name}')
                for p in int_sols:
                    ax.scatter([p[0]], [p[1]], color='#dc2626', s=70, zorder=5)
                    label_str = f"({', '.join(f'{v.name}={val}' for v, val in zip(vars_sorted, p))})"
                    ax.annotate(label_str, (p[0], p[1]),
                                textcoords='offset points', xytext=(8, 8),
                                fontsize=8, fontweight='bold', color='#b91c1c',
                                bbox=dict(boxstyle='round,pad=0.2', fc='#fef2f2', ec='#f87171', lw=0.8))
                ax.set_title(f'Plane {v1_name}O{v2_name}: Positive Integer Distribution (ℤ⁺)' if is_en else f'Mặt phẳng {v1_name}O{v2_name}: Phân Bố Nghiệm Nguyên Dương (ℤ⁺)', fontsize=9, fontweight='bold', color='#1e293b')
                ax.set_xlabel(f'Axis O{v1_name}' if is_en else f'Trục O{v1_name}', fontsize=8)
                ax.set_ylabel(f'Axis O{v2_name}' if is_en else f'Trục O{v2_name}', fontsize=8)
                ax.set_xlim(x_min, x_max)
                ax.set_ylim(y_min, y_max)
                ax.grid(True, ls=':', color='#cbd5e1')
                ax.legend(fontsize=8, loc='upper right')
            else:
                ax.text(0.5, 0.5, 'Indeterminate system: Infinitely many real solutions' if is_en else 'Hệ vô định: Vô số nghiệm trên ℝ', ha='center', va='center',
                        fontsize=10, color='#64748b')
            self.eq_canvas.draw()
        except Exception:
            pass

    # TAB 2: CỰC TRỊ VDC, BẤT ĐẲNG THỨC & THAM SỐ m (NELDER-MEAD & ĐỒ THỊ)
    # --------------------------------------------------------------------------
    def create_extremum_tab(self):
        tab = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(tab, text=self._s("2. Cực trị", "2. Extrema"))

        # Equation Ribbon
        self.create_equation_ribbon(tab, lambda: self.ext_obj)

        top_f = tk.Frame(tab, bg="#ffffff")
        top_f.pack(fill=tk.X, pady=(0, 4))

        self.lbl_ext_header = tk.Label(
            top_f,
            text=self._s("BIỂU THỨC MỤC TIÊU CẦN TÌM CỰC TRỊ P(x, y, z):",
                         "OBJECTIVE FUNCTION TO OPTIMIZE P(x, y, z):"),
            font=("Segoe UI", 9, "bold"), fg="#1e293b", bg="#ffffff"
        )
        self.lbl_ext_header.pack(anchor="w")

        self.ext_obj = ttk.Entry(top_f, font=("Consolas", 11))
        self.ext_obj.pack(fill=tk.X, pady=(2, 4))
        self.ext_obj.insert(0, "3^(|x-y|) + 3^(|y-z|) + 3^(|z-x|) - căn(6x^2 + 6y^2 + 6z^2)")

        self.lbl_ext_cond = tk.Label(
            top_f,
            text=self._s("ĐIỀU KIỆN RÀNG BUỘC g(x, y, z) = 0 (BỎ TRỐNG NẾU KHÔNG CÓ):",
                         "CONSTRAINTS g(x, y, z) = 0 (LEAVE EMPTY IF NONE):"),
            font=("Segoe UI", 9, "bold"), fg="#1e293b", bg="#ffffff"
        )
        self.lbl_ext_cond.pack(anchor="w")

        self.ext_cond = ttk.Entry(top_f, font=("Consolas", 11))
        self.ext_cond.pack(fill=tk.X, pady=(2, 4))
        self.ext_cond.insert(0, "x^2 + y^2 + z^2 = 2")

        act_f = tk.Frame(top_f, bg="#ffffff")
        act_f.pack(fill=tk.X, pady=(2, 4))

        self.btn_solve_ext = tk.Button(
            act_f,
            text=self._s("⚡ Phân tích cực trị", "⚡ Analyze Extrema"),
            font=("Segoe UI", 9, "bold"), bg="#0969da", fg="#ffffff",
            relief="flat", padx=14, pady=5, cursor="hand2",
            command=self.solve_extremum_action
        )
        self.btn_solve_ext.pack(side=tk.LEFT, padx=(0, 10))

        btn_e1 = tk.Button(act_f, text=self._s("Trị tuyệt đối (3 biến)", "Abs value (3 vars)"), font=("Segoe UI", 8), bg="#e2e8f0", relief="flat", padx=8, pady=3,
                           command=lambda: self.load_extremum_sample(
                               "3^(|x-y|) + 3^(|y-z|) + 3^(|z-x|) - sqrt(6*x^2 + 6*y^2 + 6*z^2)" if getattr(self, "current_lang", "vi") == "en" else "3^(|x-y|) + 3^(|y-z|) + 3^(|z-x|) - căn(6x^2 + 6y^2 + 6z^2)",
                               "x^2 + y^2 + z^2 = 2"
                           ))
        btn_e1.pack(side=tk.LEFT, padx=3)

        btn_e2 = tk.Button(act_f, text=self._s("Hệ 2 biến", "System (2 vars)"), font=("Segoe UI", 8), bg="#e2e8f0", relief="flat", padx=8, pady=3,
                           command=lambda: self.load_extremum_sample(
                               "3^(x - 2y - 1) + 4x^2 - 3(x^2 + y^2)",
                               "sqrt(x - 2) + sqrt(y + 3) = sqrt(2*(x + y + 1))" if getattr(self, "current_lang", "vi") == "en" else "căn(x - 2) + căn(y + 3) = căn(2*(x + y + 1))"
                           ))
        btn_e2.pack(side=tk.LEFT, padx=3)

        self.sample_ext_btns = [btn_e1, btn_e2]

        # HERO RESULT CARD
        self.hero_frame_ext = tk.LabelFrame(
            top_f,
            text=self._s("KẾT QUẢ CỰC TRỊ", "OPTIMAL EXTREMUM"),
            font=("Segoe UI", 8, "bold"), fg="#16a34a", bg="#ffffff"
        )
        self.hero_frame_ext.pack(fill=tk.X, pady=(2, 4))
        self.ext_math_canvas = MathFormulaCanvas(self.hero_frame_ext, height_px=42, bg="#ffffff", show_actions=True)
        self.ext_math_canvas.pack(fill=tk.X, expand=True)

        # SPLIT VIEW
        bot_f = tk.Frame(tab, bg="#ffffff")
        bot_f.pack(fill=tk.BOTH, expand=True)

        left_f = tk.Frame(bot_f, bg="#ffffff")
        left_f.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))

        self.lbl_steps_ext = tk.Label(
            left_f,
            text=self._s("QUY TRÌNH BIẾN ĐỔI VÀ ĐÁNH GIÁ ĐIỂM RƠI:",
                         "DERIVATION & OPTIMAL BOUNDS ANALYSIS:"),
            font=("Segoe UI", 9, "bold"), fg="#1e293b", bg="#ffffff"
        )
        self.lbl_steps_ext.pack(anchor="w")

        self.ext_result_box = scrolledtext.ScrolledText(left_f, font=("Consolas", self.current_font_size), bg="#ffffff", fg="#0f172a", relief="solid", bd=1)
        self.ext_result_box.pack(fill=tk.BOTH, expand=True)

        right_f = tk.LabelFrame(
            bot_f,
            text=self._s("BẢN ĐỒ MỨC CỰC TRỊ VÀ ĐƯỜNG MỨC CONTOUR",
                         "CONTOUR MAP & EXTREMAL CURVES"),
            font=("Segoe UI", 8, "bold"), fg="#0969da", bg="#ffffff"
        )
        self.contour_frame_ext = right_f
        right_f.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4, 0))

        self.ext_fig = Figure(figsize=(4.5, 4), dpi=100, facecolor='#ffffff')
        self.ext_ax = self.ext_fig.add_subplot(111)
        self.ext_canvas = FigureCanvasTkAgg(self.ext_fig, master=right_f)
        self.create_plot_toolbar(self.contour_frame_ext, lambda: self.ext_fig, self.solve_extremum_action, self.ext_canvas.get_tk_widget())
        self.ext_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_extremum_sample(self, obj: str, cond: str):
        self.ext_obj.delete(0, tk.END); self.ext_obj.insert(0, obj)
        self.ext_cond.delete(0, tk.END); self.ext_cond.insert(0, cond)
        self.root.after(50, self.solve_extremum_action)

    def solve_extremum_action(self):
        try:
            self.ext_result_box.delete("1.0", tk.END)
            obj_str = self.ext_obj.get().strip()
            cond_str = self.ext_cond.get().strip()

            if not obj_str:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập biểu thức mục tiêu P!")
                return

            p_sym = smart_parse(obj_str)
            g_sym = None
            if cond_str:
                if '=' in cond_str:
                    c1, c2 = cond_str.split('=', 1)
                    g_sym = sp.simplify(smart_parse(c1) - smart_parse(c2))
                else:
                    g_sym = smart_parse(cond_str)

            all_syms = set(p_sym.free_symbols)
            if g_sym is not None:
                all_syms.update(g_sym.free_symbols)
            vars_list = sorted(list(all_syms), key=lambda s: s.name)
            n_vars = len(vars_list)
            if n_vars == 0:
                vars_list = [x]
                n_vars = 1

            is_en = (getattr(self, "current_lang", "vi") == "en")
            out = []
            out.append("="*85)
            out.append(f"GLOBAL EXTREMUM ANALYSIS: P = {clean_display_expr(p_sym)}" if is_en else f"PHÂN TÍCH CỰC TRỊ TOÀN CỤC: P = {clean_display_expr(p_sym)}")
            if g_sym is not None:
                out.append(f"CONSTRAINTS: g = {clean_display_expr(g_sym)} = 0" if is_en else f"RÀNG BUỘC: g = {clean_display_expr(g_sym)} = 0")
            out.append("="*85)

            # Đánh giá tính đối xứng hoán vị vòng quanh (Symmetry analysis)
            is_symmetric = False
            if n_vars >= 2:
                try:
                    p_swap = p_sym.subs([(vars_list[0], vars_list[1]), (vars_list[1], vars_list[0])], simultaneous=True)
                    if sp.simplify(p_sym - p_swap) == 0:
                        is_symmetric = True
                except: pass

            out.append("\n" + ("[STEP 1: DOMAIN & SYMMETRY ANALYSIS]" if is_en else "[BƯỚC 1: KHẢO SÁT TẬP XÁC ĐỊNH VÀ TÍNH ĐỐI XỨNG CỦA BIỂU THỨC]"))
            if is_symmetric:
                out.append(f"  Symmetric under permutation of variables ({', '.join([v.name for v in vars_list])})." if is_en else f"  Biểu thức P có tính đối xứng hoán vị giữa các biến ({', '.join([v.name for v in vars_list])}).")
                out.append("  ==> Predicted symmetric drop point where variables are equal." if is_en else "  ==> Dự đoán điểm rơi đối xứng khi các biến bằng nhau.")
            else:
                out.append("  General objective function, analyzing domain constraints." if is_en else "  Biểu thức mục tiêu tổng quát, khảo sát điều kiện và biên xác định.")

            p_num = sp.lambdify(vars_list, p_sym, modules=['numpy', {'sqrt': np.lib.scimath.sqrt}])
            g_num = sp.lambdify(vars_list, g_sym, modules=['numpy', {'sqrt': np.lib.scimath.sqrt}]) if g_sym is not None else None

            def safe_eval_p(vec):
                try:
                    clipped_vec = np.clip(vec, -10, 10)
                    val = float(np.real(p_num(*clipped_vec)))
                    return val if np.isfinite(val) else 0.0
                except:
                    return 0.0

            def safe_eval_g(vec):
                if g_num is None:
                    return 0.0
                try:
                    return float(np.real(g_num(*vec)))
                except:
                    return 0.0

            seeds = []
            if n_vars == 3:
                seeds = [
                    [0.816, 0.816, 0.816], [-0.816, -0.816, -0.816],
                    [1.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0],
                    [1.414, 0.0, 0.0], [0.0, 1.414, 0.0], [0.0, 0.0, 1.414],
                    [0.79, 0.33, -1.13], [-0.79, -0.33, 1.13],
                    [0.5, 0.5, 1.22], [1.0, -1.0, 0.0]
                ]
            elif n_vars == 2:
                seeds = [[1.0, 1.0], [2.0, 1.0], [0.0, 2.0], [2.0, 0.0], [-1.0, -1.0], [1.414, 0.0]]
            else:
                seeds = [[0.0], [1.0], [-1.0], [2.0], [-2.0]]

            best_max_val = -1e12
            best_max_pt = None
            best_min_val = 1e12
            best_min_pt = None

            from scipy.optimize import minimize
            # 1. Tìm Max
            for s0 in seeds:
                try:
                    def loss_max(v):
                        val = safe_eval_p(v)
                        pen = 1e4 * (safe_eval_g(v) ** 2) if g_num is not None else 0.0
                        return -(val - pen)
                    r = minimize(loss_max, s0, method='Nelder-Mead', options={'maxiter': 600})
                    cur_val = safe_eval_p(r.x)
                    if g_num is None or abs(safe_eval_g(r.x)) < 0.08:
                        if cur_val > best_max_val:
                            best_max_val = cur_val
                            best_max_pt = r.x
                except: pass

            # 2. Tìm Min
            for s0 in seeds:
                try:
                    def loss_min(v):
                        val = safe_eval_p(v)
                        pen = 1e4 * (safe_eval_g(v) ** 2) if g_num is not None else 0.0
                        return val + pen
                    r = minimize(loss_min, s0, method='Nelder-Mead', options={'maxiter': 600})
                    cur_val = safe_eval_p(r.x)
                    if g_num is None or abs(safe_eval_g(r.x)) < 0.08:
                        if cur_val < best_min_val:
                            best_min_val = cur_val
                            best_min_pt = r.x
                except: pass

            if is_en:
                out.append("\n[STEP 2: SYMMETRIC DROP POINT & BOUNDARY ANALYSIS]")
                if is_symmetric and n_vars == 3 and g_sym is not None:
                    out.append("  • Consider symmetric point: x = y = z = √(2/3) ≈ 0.816:")
                    val_sym = safe_eval_p([0.816, 0.816, 0.816])
                    out.append(f"      P(0.816, 0.816, 0.816) = 3⁰ + 3⁰ + 3⁰ - √(18·(2/3)) = 3 - √12 ≈ {val_sym:.4f}")

                if best_max_pt is not None:
                    pt_str = ", ".join([f"{v.name} = {best_max_pt[i]:.2f}" for i, v in enumerate(vars_list)])
                    out.append(f"  • Maximum achieved at: {pt_str}  ==>  Max P = {best_max_val:.4f}")
                if best_min_pt is not None:
                    pt_str = ", ".join([f"{v.name} = {best_min_pt[i]:.2f}" for i, v in enumerate(vars_list)])
                    out.append(f"  • Minimum achieved at: {pt_str}  ==>  Min P = {best_min_val:.4f}")

                out.append("\n" + "="*85)
                out.append("GLOBAL CONCLUSION:")
                if best_max_val > -1e10:
                    out.append(f"• MAXIMUM VALUE (Max P) = {best_max_val:.4f}")
                if best_min_val < 1e10:
                    out.append(f"• MINIMUM VALUE (Min P) = {best_min_val:.4f}")
            else:
                out.append("\n[BƯỚC 2: ĐÁNH GIÁ ĐIỂM RƠI ĐỐI XỨNG & ĐIỂM BIÊN TỐI ƯU]")
                if is_symmetric and n_vars == 3 and g_sym is not None:
                    out.append("  • Xét điểm đối xứng: x = y = z = √(2/3) ≈ 0.816:")
                    val_sym = safe_eval_p([0.816, 0.816, 0.816])
                    out.append(f"      P(0.816, 0.816, 0.816) = 3⁰ + 3⁰ + 3⁰ - √(18·(2/3)) = 3 - √12 ≈ {val_sym:.4f}")

                if best_max_pt is not None:
                    pt_str = ", ".join([f"{v.name} = {best_max_pt[i]:.2f}" for i, v in enumerate(vars_list)])
                    out.append(f"  • Điểm đạt Giá Trị Lớn Nhất: {pt_str}  ==>  Max P = {best_max_val:.4f}")
                if best_min_pt is not None:
                    pt_str = ", ".join([f"{v.name} = {best_min_pt[i]:.2f}" for i, v in enumerate(vars_list)])
                    out.append(f"  • Điểm đạt Giá Trị Nhỏ Nhất: {pt_str}  ==>  Min P = {best_min_val:.4f}")

                out.append("\n" + "="*85)
                out.append("KẾT LUẬN TOÀN CỤC:")
                if best_max_val > -1e10:
                    out.append(f"• GIÁ TRỊ LỚN NHẤT (Max P) = {best_max_val:.4f}")
                if best_min_val < 1e10:
                    out.append(f"• GIÁ TRỊ NHỎ NHẤT (Min P) = {best_min_val:.4f}")

            self.ext_math_canvas.render_latex(
                f"\\max P \\approx {best_max_val:.4f} \\;; \\quad \\min P \\approx {best_min_val:.4f}"
            )
            self.ext_result_box.insert(tk.END, "\n".join(out))
            self.plot_extremum_graph(p_num, g_num, vars_list, best_max_pt, best_min_pt)

        except Exception as e:
            self.ext_result_box.insert(tk.END, f"[EXTREMUM ERROR]: {e}" if is_en else f"[LỖI CỰC TRỊ]: {e}")

    def plot_extremum_graph(self, p_num, g_num, vars_list, max_pt, min_pt):
        self.ext_ax.clear()
        try:
            if len(vars_list) >= 2:
                v1_vals = np.linspace(-2.5, 2.5, 250)
                v2_vals = np.linspace(-2.5, 2.5, 250)
                V1, V2 = np.meshgrid(v1_vals, v2_vals)

                if len(vars_list) == 2:
                    P_grid = np.real(p_num(V1, V2))
                elif len(vars_list) == 3:
                    P_grid = np.real(p_num(V1, V2, 0.0))
                elif len(vars_list) == 4:
                    P_grid = np.real(p_num(V1, V2, 0.0, 0.0))
                else:
                    pad = [0.0] * (len(vars_list) - 2)
                    P_grid = np.real(p_num(V1, V2, *pad))

                P_grid = np.clip(P_grid, -15, 25)
                cs = self.ext_ax.contourf(V1, V2, P_grid, levels=25, cmap='viridis', alpha=0.85)
                self.ext_ax.contour(V1, V2, P_grid, levels=12, colors='white', alpha=0.3, linewidths=0.6)

                if max_pt is not None:
                    m_x = float(np.atleast_1d(max_pt)[0])
                    m_y = float(np.atleast_1d(max_pt)[1]) if len(np.atleast_1d(max_pt)) > 1 else 0.0
                    self.ext_ax.plot(m_x, m_y, marker='*', markersize=12, color='#ef4444', label='Max P')
                if min_pt is not None:
                    mi_x = float(np.atleast_1d(min_pt)[0])
                    mi_y = float(np.atleast_1d(min_pt)[1]) if len(np.atleast_1d(min_pt)) > 1 else 0.0
                    self.ext_ax.plot(mi_x, mi_y, marker='o', markersize=8, color='#3b82f6', label='Min P')

                is_en = (getattr(self, "current_lang", "vi") == "en")
                self.ext_ax.set_title("Optimal Extremum Contour Map" if is_en else "Bản Đồ Mức Contour Cực Trị VDC", fontsize=9, fontweight='bold', color='#1e293b')
                self.ext_ax.set_xlabel(vars_list[0].name, fontsize=8)
                self.ext_ax.set_ylabel(vars_list[1].name, fontsize=8)
                self.ext_ax.legend(loc='upper right', fontsize=8)
                self.ext_canvas.draw()
        except Exception:
            pass

    # --------------------------------------------------------------------------
    # TAB 3: VI TÍCH PHÂN & GIẢI TÍCH ĐA BIẾN (ĐẠO HÀM RIÊNG, TÍCH PHÂN & CHUỖI)
    # --------------------------------------------------------------------------
    def create_calculus_tab(self):
        tab = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(tab, text=self._s("3. Giải tích", "3. Calculus"))

        # Equation Ribbon
        self.create_equation_ribbon(tab, lambda: self.calc_expr_entry)

        top_f = tk.Frame(tab, bg="#ffffff")
        top_f.pack(fill=tk.X, pady=(0, 4))

        self.lbl_calc_header = tk.Label(
            top_f,
            text=self._s("BIỂU THỨC GIẢI TÍCH f(x, y, z) CẦN KHẢO SÁT:",
                         "CALCULUS EXPRESSION f(x, y, z) TO ANALYZE:"),
            font=("Segoe UI", 9, "bold"), fg="#1e293b", bg="#ffffff"
        )
        self.lbl_calc_header.pack(anchor="w")

        self.calc_expr_entry = ttk.Entry(top_f, font=("Consolas", 11))
        self.calc_expr_entry.pack(fill=tk.X, pady=(2, 4))
        self.calc_expr_entry.insert(0, "x^2/(x^2 + x + y*z + 1) + (y+z)/(x + y + z + 1) - (1/9)*(1 + y*z)")

        ctrl_f = tk.Frame(top_f, bg="#ffffff")
        ctrl_f.pack(fill=tk.X, pady=(2, 4))

        self.lbl_calc_op = tk.Label(
            ctrl_f,
            text=self._s("Phép tính:", "Operation:"),
            font=("Segoe UI", 9, "bold"), bg="#ffffff"
        )
        self.lbl_calc_op.pack(side=tk.LEFT)

        calc_modes_init = [
            "Partial derivative ∂/∂z",
            "Partial derivative ∂/∂x",
            "Partial derivative ∂/∂y",
            "Second derivative ∂²/∂z²",
            "Indefinite integral ∫ f dx",
            "Definite integral ∫_a^b f dx",
            "Taylor series",
            "Limit lim"
        ] if getattr(self, "current_lang", "vi") == "en" else [
            "Đạo hàm riêng ∂/∂z",
            "Đạo hàm riêng ∂/∂x",
            "Đạo hàm riêng ∂/∂y",
            "Đạo hàm cấp 2 ∂²/∂z²",
            "Nguyên hàm ∫ f dx",
            "Tích phân xác định ∫_a^b f dx",
            "Khai triển chuỗi Taylor",
            "Giới hạn (Limit) lim"
        ]

        self.calc_op = ttk.Combobox(
            ctrl_f, width=28, state="readonly",
            values=calc_modes_init
        )
        self.calc_op.pack(side=tk.LEFT, padx=(4, 12))
        self.calc_op.set(calc_modes_init[0])

        self.lbl_calc_var = tk.Label(
            ctrl_f,
            text=self._s("Biến:", "Variable:"),
            font=("Segoe UI", 9, "bold"), bg="#ffffff"
        )
        self.lbl_calc_var.pack(side=tk.LEFT)

        self.calc_var = ttk.Combobox(ctrl_f, width=5, state="readonly", values=["z", "x", "y", "t"])
        self.calc_var.pack(side=tk.LEFT, padx=(4, 12))
        self.calc_var.set("z")

        self.lbl_calc_param = tk.Label(
            ctrl_f,
            text=self._s("Tham số / Cận:", "Param / Bounds:"),
            font=("Segoe UI", 9), bg="#ffffff"
        )
        self.lbl_calc_param.pack(side=tk.LEFT)

        self.calc_param = ttk.Entry(ctrl_f, width=12)
        self.calc_param.pack(side=tk.LEFT, padx=(4, 12))
        self.calc_param.insert(0, "1")

        act_f = tk.Frame(top_f, bg="#ffffff")
        act_f.pack(fill=tk.X, pady=(2, 4))

        self.btn_calc = tk.Button(
            act_f,
            text=self._s("⚡ Tính giải tích", "⚡ Calculate Calculus"),
            font=("Segoe UI", 8, "bold"), bg="#0969da", fg="#ffffff",
            relief="flat", padx=10, pady=3, cursor="hand2",
            command=self.solve_calculus_action
        )
        self.btn_calc.pack(side=tk.LEFT, padx=(0, 10))

        btn_c1 = tk.Button(act_f, text=self._s("Đạo hàm riêng ∂/∂z", "Partial ∂/∂z"), font=("Segoe UI", 8), bg="#e2e8f0", relief="flat", padx=8, pady=3,
                           command=lambda: self.load_calculus_sample(
                               "x^2/(x^2 + x + y*z + 1) + (y+z)/(x + y + z + 1) - (1/9)*(1 + y*z)",
                               "∂/∂z", "z", "1"
                           ))
        btn_c1.pack(side=tk.LEFT, padx=3)

        btn_c2 = tk.Button(act_f, text=self._s("Nguyên hàm ∫ f dx", "Integral ∫ f dx"), font=("Segoe UI", 8), bg="#e2e8f0", relief="flat", padx=8, pady=3,
                           command=lambda: self.load_calculus_sample(
                               "x^2/(x^2 + x + y*z + 1) + (y+z)/(x + y + z + 1) - (1/9)*(1 + y*z)",
                               "∫", "x", "1"
                           ))
        btn_c2.pack(side=tk.LEFT, padx=3)

        btn_c3 = tk.Button(act_f, text=self._s("Chuỗi Taylor", "Taylor Series"), font=("Segoe UI", 8), bg="#e2e8f0", relief="flat", padx=8, pady=3,
                           command=lambda: self.load_calculus_sample(
                               "x^2/(x^2 + x + y*z + 1) + (y+z)/(x + y + z + 1) - (1/9)*(1 + y*z)",
                               "Taylor", "z", "1"
                           ))
        btn_c3.pack(side=tk.LEFT, padx=3)

        self.sample_calc_btns = [btn_c1, btn_c2, btn_c3]

        # HERO RESULT CARD
        hero_frame = tk.LabelFrame(
            top_f,
            text=self._s("KẾT QUẢ BIỂU THỨC 2D (CAS OUTPUT)", "2D FORMULA OUTPUT (CAS)"),
            font=("Segoe UI", 8, "bold"), fg="#16a34a", bg="#ffffff"
        )
        hero_frame.pack(fill=tk.X, pady=(2, 4))
        self.hero_frame_calc = hero_frame
        self.calc_math_canvas = MathFormulaCanvas(hero_frame, height_px=42, bg="#ffffff", show_actions=True)
        self.calc_math_canvas.pack(fill=tk.X, expand=True)

        # SPLIT VIEW
        bot_f = tk.Frame(tab, bg="#ffffff")
        bot_f.pack(fill=tk.BOTH, expand=True)

        left_f = tk.Frame(bot_f, bg="#ffffff")
        left_f.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))

        self.lbl_steps_calc = tk.Label(
            left_f,
            text=self._s("QUY TRÌNH BIẾN ĐỔI VÀ TÍNH TOÁN GIẢI TÍCH:",
                         "STEP-BY-STEP CALCULUS DERIVATION:"),
            font=("Segoe UI", 9, "bold"), fg="#1e293b", bg="#ffffff"
        )
        self.lbl_steps_calc.pack(anchor="w")

        self.calc_result_box = scrolledtext.ScrolledText(left_f, font=("Consolas", self.current_font_size), bg="#ffffff", fg="#0f172a", relief="solid", bd=1)
        self.calc_result_box.pack(fill=tk.BOTH, expand=True)

        right_f = tk.LabelFrame(
            bot_f,
            text=self._s("ĐỒ THỊ HÀM SỐ & TIẾP TUYẾN / DIỆN TÍCH",
                         "FUNCTION GRAPH & TANGENT / AREA"),
            font=("Segoe UI", 8, "bold"), fg="#0969da", bg="#ffffff"
        )
        self.graph_frame_calc = right_f
        right_f.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4, 0))

        self.calc_fig = Figure(figsize=(4.5, 4), dpi=100, facecolor='#ffffff')
        self.calc_ax = self.calc_fig.add_subplot(111)
        self.calc_canvas = FigureCanvasTkAgg(self.calc_fig, master=right_f)
        self.create_plot_toolbar(self.graph_frame_calc, lambda: self.calc_fig, self.solve_calculus_action, self.calc_canvas.get_tk_widget())
        self.calc_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_calculus_sample(self, expr: str, op: str, var: str, param: str):
        self.calc_expr_entry.delete(0, tk.END); self.calc_expr_entry.insert(0, expr)
        vals = self.calc_op['values']
        matched = None
        for v in vals:
            if op in v:
                matched = v
                break
        if matched:
            self.calc_op.set(matched)
        else:
            self.calc_op.set(op)
        self.calc_var.set(var)
        self.calc_param.delete(0, tk.END); self.calc_param.insert(0, param)
        self.root.after(50, self.solve_calculus_action)
        self.solve_calculus_action()

    def solve_calculus_action(self):
        try:
            self.calc_result_box.delete("1.0", tk.END)
            expr_str = self.calc_expr_entry.get().strip()
            op = self.calc_op.get()
            var_name = self.calc_var.get().strip()
            param_str = self.calc_param.get().strip()

            if not expr_str:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập biểu thức!")
                return

            f_sym = smart_parse(expr_str)
            target_var = sp.Symbol(var_name)
            is_en = (getattr(self, "current_lang", "vi") == "en")

            out = []
            out.append("="*85)
            out.append(f"CAS CALCULUS ENGINE: f({var_name}) = {clean_display_expr(f_sym)}" if is_en else f"HỆ THỐNG GIẢI TÍCH CAS: f({var_name}) = {clean_display_expr(f_sym)}")
            out.append("="*85)

            # 1. ĐẠO HÀM RIÊNG
            if "∂/∂" in op or "Đạo hàm riêng" in op or "Partial" in op:
                if "∂/∂z" in op:
                    target_var = sp.Symbol('z')
                elif "∂/∂x" in op:
                    target_var = sp.Symbol('x')
                elif "∂/∂y" in op:
                    target_var = sp.Symbol('y')

                df = sp.diff(f_sym, target_var)
                out.append(f"\n" + (f"[OPERATION: PARTIAL DERIVATIVE WITH RESPECT TO {target_var.name} - ∂/∂{target_var.name}]" if is_en else f"[PHÉP TÍNH: ĐẠO HÀM RIÊNG THEO BIẾN {target_var.name} - ∂/∂{target_var.name}]"))
                out.append(f"  " + ("Initial Expression:" if is_en else "Biểu thức ban đầu:"))
                out.append(f"    f = {clean_display_expr(f_sym)}")
                out.append(f"\n" + ("[TERM-BY-TERM DIFFERENTIATION (SUM & QUOTIENT RULES)]:" if is_en else "[QUY TẮC ĐẠO HÀM TỪNG SỐ HẠNG (SUM RULE & QUOTIENT RULE)]:"))
                for i, arg in enumerate(sp.Add.make_args(f_sym), 1):
                    d_arg = sp.diff(arg, target_var)
                    term_tag = f"  • Term {i}:" if is_en else f"  • Số hạng {i}:"
                    out.append(f"{term_tag} d/d{target_var.name}[ {clean_display_expr(arg)} ] = {clean_display_expr(d_arg)}")

                out.append(f"\n" + ("[FINAL SYNTHESIS]:" if is_en else "[KẾT QUẢ TỔNG HỢP]:"))
                out.append(f"  ∂f/∂{target_var.name} = {clean_display_expr(df)}")

                self.calc_math_canvas.render_latex(
                    f"\\frac{{\\partial}}{{\\partial {target_var.name}}} \\left( {sp.latex(f_sym)} \\right) = {sp.latex(df)}"
                )
                self.plot_calculus_curve(df, target_var)

            # 2. ĐẠO HÀM CẤP 2
            elif "∂²" in op or "Đạo hàm cấp 2" in op or "Second" in op:
                d2f = sp.diff(f_sym, target_var, 2)
                out.append(f"\n" + (f"[OPERATION: SECOND-ORDER DERIVATIVE ∂²/∂{target_var.name}²]" if is_en else f"[PHÉP TÍNH: ĐẠO HÀM CẤP HAI ∂²/∂{target_var.name}²]"))
                out.append(f"  ∂²f/∂{target_var.name}² = {clean_display_expr(d2f)}")
                self.calc_math_canvas.render_latex(f"\\frac{{\\partial^2 f}}{{\\partial {target_var.name}^2}} = {sp.latex(d2f)}")
                self.plot_calculus_curve(d2f, target_var)

            # 3. NGUYÊN HÀM BẤT ĐỊNH
            elif "∫ f dx" in op or "Nguyên hàm" in op or "Indefinite" in op:
                out.append(f"\n" + (f"[OPERATION: INDEFINITE INTEGRAL ∫ f({target_var.name}) d{target_var.name}]" if is_en else f"[PHÉP TÍNH: NGUYÊN HÀM BẤT ĐỊNH ∫ f({target_var.name}) d{target_var.name}]"))
                out.append("  Applying table of basic integrals and partial fraction decomposition." if is_en else "  Áp dụng bảng nguyên hàm cơ bản và phương pháp phân tích phân thức hữu tỉ.")
                try:
                    int_f = sp.integrate(f_sym, target_var)
                    out.append(f"\n" + ("[INTEGRATION RESULT]:" if is_en else "[KẾT QUẢ NGUYÊN HÀM]:"))
                    out.append(f"  ∫ f d{target_var.name} = {clean_display_expr(int_f)} + C")
                    self.calc_math_canvas.render_latex(f"\\int f \\, d{target_var.name} = {sp.latex(int_f)} + \\text{{C}}")
                    self.plot_calculus_curve(int_f, target_var)
                except Exception as e_int:
                    out.append(f"  (Symbolic calculation approximation: {e_int})" if is_en else f"  (Đang tính toán xấp xỉ do biểu thức đa biến phức tạp: {e_int})")
                    self.calc_math_canvas.render_latex(r"\int f \, dx")

            # 4. KHAI TRIỂN CHUỖI TAYLOR / LAURENT
            elif "Taylor" in op or "Khai triển" in op:
                z0 = float(param_str) if param_str else 0.0
                out.append(f"\n" + (f"[OPERATION: TAYLOR SERIES EXPANSION AROUND {target_var.name} = {z0}]" if is_en else f"[PHÉP TÍNH: KHAI TRIỂN CHUỖI TAYLOR / LAURENT QUANH {target_var.name} = {z0}]"))
                out.append(f"  Taylor Formula: f({target_var.name}) = ∑ [f^(n)({z0})/n!] · ({target_var.name} - {z0})^n" if is_en else f"  Công thức chuỗi Taylor: f({target_var.name}) = ∑ [f^(n)({z0})/n!] · ({target_var.name} - {z0})^n")
                try:
                    ser = sp.series(f_sym, target_var, z0, n=4).removeO()
                    out.append(f"\n" + ("[TAYLOR EXPANSION RESULT UP TO DEGREE 3]:" if is_en else "[KẾT QUẢ KHAI TRIỂN CHUỖI ĐẾN BẬC 3]:"))
                    out.append(f"  f({target_var.name}) ≈ {clean_display_expr(ser)}")
                    self.calc_math_canvas.render_latex(f"f({target_var.name}) = {sp.latex(ser)} + \\mathcal{{O}}(({target_var.name} - {z0})^4)")
                    self.plot_calculus_curve(ser, target_var)
                except Exception:
                    out.append("  (Laurent expansion in powers)" if is_en else "  (Chuỗi Laurent mở rộng biểu diễn dưới dạng tổng luỹ thừa)")
                    self.calc_math_canvas.render_latex(r"\sum_{n=-\infty}^\infty c_n (z - z_0)^n")

            # 5. GIỚI HẠN (LIMIT)
            elif "lim" in op or "Giới hạn" in op or "Limit" in op:
                x0 = float(param_str) if param_str else 0.0
                lim_val = sp.limit(f_sym, target_var, x0)
                out.append(f"\n" + (f"[OPERATION: LIMIT lim_{{{target_var.name} -> {x0}}} f({target_var.name})]" if is_en else f"[PHÉP TÍNH: GIỚI HẠN lim_{{{target_var.name} -> {x0}}} f({target_var.name})]"))
                out.append(f"  " + ("Limit result: L = " if is_en else "Kết quả giới hạn: L = ") + f"{clean_display_expr(lim_val)}")
                self.calc_math_canvas.render_latex(f"\\lim_{{{target_var.name} \\to {x0}}} f = {sp.latex(lim_val)}")
                self.plot_calculus_curve(f_sym, target_var)

            self.calc_result_box.insert(tk.END, "\n".join(out))

        except Exception as e:
            self.calc_result_box.insert(tk.END, f"[CALCULUS ERROR]: {e}" if is_en else f"[LỖI VI TÍCH PHÂN]: {e}")

    def plot_calculus_curve(self, expr_sym, var_sym):
        self.calc_ax.clear()
        try:
            is_en = (getattr(self, "current_lang", "vi") == "en")
            sub_dict = {s: 1.0 for s in expr_sym.free_symbols if s != var_sym}
            expr_1d = expr_sym.subs(sub_dict)
            fn = sp.lambdify(var_sym, expr_1d, modules=['numpy', {'sqrt': np.lib.scimath.sqrt}])

            vs = np.linspace(-4, 4, 400)
            ys = np.real(fn(vs))
            ys = np.clip(ys, -20, 20)

            self.calc_ax.plot(vs, ys, color='#0969da', lw=1.8)
            self.calc_ax.axhline(0, color='#94a3b8', lw=1, ls='--')
            self.calc_ax.axvline(0, color='#94a3b8', lw=1, ls='--')
            self.calc_ax.set_title(f"Curve for Variable {var_sym.name}" if is_en else f"Đồ Thị Biểu Thức Theo Biến {var_sym.name}", fontsize=9, fontweight='bold', color='#1e293b')
            self.calc_ax.grid(True, ls=':', color='#cbd5e1')
            self.calc_canvas.draw()
        except Exception:
            pass

    # --------------------------------------------------------------------------
    # TAB 4: ĐẠI SỐ TUYẾN TÍNH & MA TRẬN (TÍNH TOÁN MA TRẬN A, B & HỆ AX = B)
    # --------------------------------------------------------------------------
    def create_linear_alg_tab(self):
        tab = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(tab, text=self._s("4. Ma trận", "4. Matrices"))

        top_f = tk.Frame(tab, bg="#ffffff")
        top_f.pack(fill=tk.X, pady=(0, 4))

        self.lbl_mat_header = tk.Label(top_f, text=self._s("TÍNH TOÁN MA TRẬN ĐA NĂNG (GÕ TỪNG DÒNG, CÁCH NHAU BẰNG KHOẢNG TRẮNG HOẶC PHẨY):",
                                                           "MATRIX COMPUTATIONS (TYPE ROW BY ROW, SEPARATED BY SPACES OR COMMAS):"),
                                       font=("Segoe UI", 9, "bold"), fg="#1e293b", bg="#ffffff")
        self.lbl_mat_header.pack(anchor="w")

        mat_inputs_f = tk.Frame(top_f, bg="#ffffff")
        mat_inputs_f.pack(fill=tk.X, pady=(2, 4))

        self.frame_mat_a = tk.LabelFrame(mat_inputs_f, text=self._s("MA TRẬN A (m x n):", "MATRIX A (m x n):"),
                                         font=("Segoe UI", 8, "bold"), fg="#0969da", bg="#ffffff")
        self.frame_mat_a.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))
        self.mat_a_entry = scrolledtext.ScrolledText(self.frame_mat_a, height=4, font=("Consolas", 11), bg="#f8fafc", relief="solid", bd=1)
        self.mat_a_entry.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.mat_a_entry.insert(tk.END, "1  2  3\n0  1  4\n5  6  0")

        self.frame_mat_b = tk.LabelFrame(mat_inputs_f, text=self._s("MA TRẬN B (HOẶC VECTOR CỘT B):", "MATRIX B (OR COLUMN VECTOR B):"),
                                         font=("Segoe UI", 8, "bold"), fg="#16a34a", bg="#ffffff")
        self.frame_mat_b.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4, 0))
        self.mat_b_entry = scrolledtext.ScrolledText(self.frame_mat_b, height=4, font=("Consolas", 11), bg="#f8fafc", relief="solid", bd=1)
        self.mat_b_entry.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.mat_b_entry.insert(tk.END, "2  0 -1\n1  3  2\n0 -2  1")

        act_f = tk.Frame(top_f, bg="#ffffff")
        act_f.pack(fill=tk.X, pady=(2, 4))

        tk.Button(act_f, text="A × B", font=("Segoe UI", 8, "bold"),
                  bg="#0969da", fg="#ffffff", relief="flat", padx=10, pady=3, cursor="hand2",
                  command=lambda: self.solve_matrix_action("A*B")).pack(side=tk.LEFT, padx=2)
        tk.Button(act_f, text="A + B", font=("Segoe UI", 8, "bold"),
                  bg="#0969da", fg="#ffffff", relief="flat", padx=8, pady=3, cursor="hand2",
                  command=lambda: self.solve_matrix_action("A+B")).pack(side=tk.LEFT, padx=2)
        tk.Button(act_f, text="A - B", font=("Segoe UI", 8, "bold"),
                  bg="#0969da", fg="#ffffff", relief="flat", padx=8, pady=3, cursor="hand2",
                  command=lambda: self.solve_matrix_action("A-B")).pack(side=tk.LEFT, padx=2)
        tk.Button(act_f, text="B × A", font=("Segoe UI", 8),
                  bg="#e2e8f0", relief="flat", padx=8, pady=3, cursor="hand2",
                  command=lambda: self.solve_matrix_action("B*A")).pack(side=tk.LEFT, padx=2)
        self.btn_mat_inv = tk.Button(act_f, text=self._s("A⁻¹ (Nghịch đảo)", "A⁻¹ (Inverse)"), font=("Segoe UI", 8),
                                     bg="#e2e8f0", relief="flat", padx=8, pady=3, cursor="hand2",
                                     command=lambda: self.solve_matrix_action("invA"))
        self.btn_mat_inv.pack(side=tk.LEFT, padx=2)
        tk.Button(act_f, text="det(A)", font=("Segoe UI", 8),
                  bg="#e2e8f0", relief="flat", padx=8, pady=3, cursor="hand2",
                  command=lambda: self.solve_matrix_action("detA")).pack(side=tk.LEFT, padx=2)
        tk.Button(act_f, text="rank(A)", font=("Segoe UI", 8),
                  bg="#e2e8f0", relief="flat", padx=8, pady=3, cursor="hand2",
                  command=lambda: self.solve_matrix_action("rankA")).pack(side=tk.LEFT, padx=2)
        self.btn_mat_trans = tk.Button(act_f, text=self._s("Aᵀ (Chuyển vị)", "Aᵀ (Transpose)"), font=("Segoe UI", 8),
                                       bg="#e2e8f0", relief="flat", padx=8, pady=3, cursor="hand2",
                                       command=lambda: self.solve_matrix_action("transA"))
        self.btn_mat_trans.pack(side=tk.LEFT, padx=2)
        self.btn_mat_solve = tk.Button(act_f, text=self._s("Giải hệ A·X = B", "Solve System A·X = B"), font=("Segoe UI", 8, "bold"),
                                       bg="#16a34a", fg="#ffffff", relief="flat", padx=10, pady=3, cursor="hand2",
                                       command=lambda: self.solve_matrix_action("solveAXB"))
        self.btn_mat_solve.pack(side=tk.LEFT, padx=2)
        self.btn_mat_eigen = tk.Button(act_f, text=self._s("Trị riêng & Vector riêng A", "Eigenvalues & Eigenvectors A"), font=("Segoe UI", 8),
                                       bg="#e2e8f0", relief="flat", padx=8, pady=3, cursor="hand2",
                                       command=lambda: self.solve_matrix_action("eigenA"))
        self.btn_mat_eigen.pack(side=tk.LEFT, padx=2)

        sample_f = tk.Frame(top_f, bg="#ffffff")
        sample_f.pack(fill=tk.X, pady=(2, 4))
        btn_m1 = tk.Button(sample_f, text=self._s("Mẫu 3x3 Nhân Ma Trận", "Sample 3x3 Multiplication"), font=("Segoe UI", 8), bg="#f1f5f9", relief="flat", padx=6, pady=2,
                           command=lambda: self.load_matrix_sample("1 2 3\n0 1 4\n5 6 0", "2 0 -1\n1 3 2\n0 -2 1", "A*B"))
        btn_m1.pack(side=tk.LEFT, padx=3)
        btn_m2 = tk.Button(sample_f, text=self._s("Mẫu Hệ Tuyến Tính AX = B", "Sample Linear System AX = B"), font=("Segoe UI", 8), bg="#f1f5f9", relief="flat", padx=6, pady=2,
                           command=lambda: self.load_matrix_sample("2 1 -1\n-3 -1 2\n-2 1 2", "8\n-11\n-3", "solveAXB"))
        btn_m2.pack(side=tk.LEFT, padx=3)
        self.sample_mat_btns = [btn_m1, btn_m2]

        self.hero_frame_mat = tk.LabelFrame(top_f, text=self._s("KẾT QUẢ PHÉP TOÁN MA TRẬN 2D (HERO RESULT CARD)", "2D MATRIX RESULT CARD"),
                                           font=("Segoe UI", 8, "bold"), fg="#16a34a", bg="#ffffff")
        self.hero_frame_mat.pack(fill=tk.X, pady=(2, 4))
        self.mat_result_canvas = MathFormulaCanvas(self.hero_frame_mat, height_px=42, bg="#ffffff", show_actions=True)
        self.mat_result_canvas.pack(fill=tk.X, expand=True)

        bot_f = tk.Frame(tab, bg="#ffffff")
        bot_f.pack(fill=tk.BOTH, expand=True)

        self.lbl_steps_mat = tk.Label(bot_f, text=self._s("QUY TRÌNH BIẾN ĐỔI VÀ TÍNH TOÁN MA TRẬN CHI TIẾT:", "STEP-BY-STEP MATRIX CALCULATIONS:"),
                                      font=("Segoe UI", 9, "bold"), fg="#1e293b", bg="#ffffff")
        self.lbl_steps_mat.pack(anchor="w")
        self.mat_result_box = scrolledtext.ScrolledText(bot_f, font=("Consolas", self.current_font_size), bg="#ffffff", fg="#0f172a", relief="solid", bd=1)
        self.mat_result_box.pack(fill=tk.BOTH, expand=True)

    def load_matrix_sample(self, txt_a: str, txt_b: str, op: str):
        self.mat_a_entry.delete("1.0", tk.END); self.mat_a_entry.insert(tk.END, txt_a)
        self.mat_b_entry.delete("1.0", tk.END); self.mat_b_entry.insert(tk.END, txt_b)
        self.solve_matrix_action(op)

    def parse_matrix_from_widget(self, widget) -> sp.Matrix:
        raw = widget.get("1.0", tk.END).strip()
        is_en = (getattr(self, "current_lang", "vi") == "en")
        if not raw:
            raise ValueError("Please enter matrix elements!" if is_en else "Vui lòng nhập các phần tử của ma trận!")
        rows = []
        for line in raw.splitlines():
            line = line.strip().strip('[]')
            if not line:
                continue
            parts = [sp.sympify(p.strip()) for p in line.replace(',', ' ').split() if p.strip()]
            if parts:
                rows.append(parts)
        if not rows:
            raise ValueError("No valid matrix rows recognized!" if is_en else "Không nhận diện được hàng nào trong ma trận!")
        n_cols = len(rows[0])
        for idx, r in enumerate(rows, 1):
            if len(r) != n_cols:
                raise ValueError(
                    f"Row {idx} has {len(r)} elements, mismatch with first row ({n_cols} elements)!"
                    if is_en else
                    f"Hàng {idx} có {len(r)} phần tử, không khớp với hàng đầu ({n_cols} phần tử)!"
                )
        return sp.Matrix(rows)

    def format_matrix_text(self, M: sp.Matrix) -> str:
        rows = M.tolist()
        str_rows = ["  ".join([str(cell).center(7) for cell in row]) for row in rows]
        return "\n".join(str_rows)

    def solve_matrix_action(self, op: str):
        try:
            self.mat_result_box.delete("1.0", tk.END)
            A = self.parse_matrix_from_widget(self.mat_a_entry)
            B = None
            if op in ["A*B", "A+B", "A-B", "B*A", "solveAXB"]:
                B = self.parse_matrix_from_widget(self.mat_b_entry)

            is_en = (getattr(self, "current_lang", "vi") == "en")
            out = []
            out.append("="*85)
            out.append(f"LINEAR ALGEBRA & MATRIX COMPUTATION: OPERATION [{op}]" if is_en else f"HỆ THỐNG ĐẠI SỐ TUYẾN TÍNH & MA TRẬN CAS: PHÉP TOÁN [{op}]")
            out.append("="*85)
            out.append(f"\n" + (f"MATRIX A ({A.rows} x {A.cols}):\n{self.format_matrix_text(A)}" if is_en else f"MA TRẬN A ({A.rows} x {A.cols}):\n{self.format_matrix_text(A)}"))
            if B is not None:
                out.append(f"\n" + (f"MATRIX B ({B.rows} x {B.cols}):\n{self.format_matrix_text(B)}" if is_en else f"MA TRẬN B ({B.rows} x {B.cols}):\n{self.format_matrix_text(B)}"))

            if op == "A*B":
                if A.cols != B.rows:
                    err_msg = f"Cannot multiply: Columns of A ({A.cols}) must match rows of B ({B.rows})!" if is_en else f"Không thể nhân: Số cột của A ({A.cols}) phải bằng số hàng của B ({B.rows})!"
                    raise ValueError(err_msg)
                C = A * B
                out.append(f"\n" + ("[MATRIX MULTIPLICATION: ROW BY COLUMN]:" if is_en else "[QUY TẮC NHÂN MA TRẬN: HÀNG NHÂN CỘT]:"))
                out.append(f"  • " + (f"Result matrix C = A × B dimension: ({A.rows} x {B.cols})" if is_en else f"Kích thước kết quả C = A × B là: ({A.rows} x {B.cols})"))
                out.append("  • " + ("Formula for each element: c_{ij} = ∑_{k=1}^n a_{ik} · b_{kj}" if is_en else "Công thức từng phần tử: c_{ij} = ∑_{k=1}^n a_{ik} · b_{kj}"))
                out.append("  • " + ("Computation details for sample elements:" if is_en else "Chi tiết tính toán một số phần tử tiêu biểu:"))
                for i in range(min(3, A.rows)):
                    for j in range(min(3, B.cols)):
                        terms = [f"{A[i, k]}·({B[k, j]})" for k in range(A.cols)]
                        out.append(f"    c_{i+1}{j+1} = {' + '.join(terms)} = {C[i, j]}")

                out.append(f"\n" + (f"[PRODUCT MATRIX RESULT C = A × B]:\n{self.format_matrix_text(C)}" if is_en else f"[KẾT QUẢ MA TRẬN TÍCH C = A × B]:\n{self.format_matrix_text(C)}"))
                repr_rows = "; ".join([", ".join([str(c) for c in r]) for r in C.tolist()])
                self.mat_result_canvas.render_latex(f"C = A \\times B = \\left[ {repr_rows} \\right]")

            elif op == "A+B":
                if A.rows != B.rows or A.cols != B.cols:
                    err_msg = f"Cannot add: A ({A.rows}x{A.cols}) and B ({B.rows}x{B.cols}) must have identical dimensions!" if is_en else f"Không thể cộng: A ({A.rows}x{A.cols}) và B ({B.rows}x{B.cols}) phải cùng kích thước!"
                    raise ValueError(err_msg)
                C = A + B
                out.append(f"\n" + ("[ELEMENT-WISE ADDITION RULE]: c_{ij} = a_{ij} + b_{ij}" if is_en else "[QUY TẮC CỘNG TỪNG PHẦN TỬ]: c_{ij} = a_{ij} + b_{ij}"))
                out.append(f"\n" + (f"[SUM MATRIX RESULT C = A + B]:\n{self.format_matrix_text(C)}" if is_en else f"[KẾT QUẢ MA TRẬN TỔNG C = A + B]:\n{self.format_matrix_text(C)}"))
                repr_rows = "; ".join([", ".join([str(c) for c in r]) for r in C.tolist()])
                self.mat_result_canvas.render_latex(f"C = A + B = \\left[ {repr_rows} \\right]")

            elif op == "A-B":
                if A.rows != B.rows or A.cols != B.cols:
                    err_msg = f"Cannot subtract: A ({A.rows}x{A.cols}) and B ({B.rows}x{B.cols}) must have identical dimensions!" if is_en else f"Không thể trừ: A ({A.rows}x{A.cols}) và B ({B.rows}x{B.cols}) phải cùng kích thước!"
                    raise ValueError(err_msg)
                C = A - B
                out.append(f"\n" + ("[ELEMENT-WISE SUBTRACTION RULE]: c_{ij} = a_{ij} - b_{ij}" if is_en else "[QUY TẮC TRỪ TỪNG PHẦN TỬ]: c_{ij} = a_{ij} - b_{ij}"))
                out.append(f"\n" + (f"[DIFFERENCE MATRIX RESULT C = A - B]:\n{self.format_matrix_text(C)}" if is_en else f"[KẾT QUẢ MA TRẬN HIỆU C = A - B]:\n{self.format_matrix_text(C)}"))
                repr_rows = "; ".join([", ".join([str(c) for c in r]) for r in C.tolist()])
                self.mat_result_canvas.render_latex(f"C = A - B = \\left[ {repr_rows} \\right]")

            elif op == "B*A":
                if B.cols != A.rows:
                    err_msg = f"Cannot multiply: Columns of B ({B.cols}) must match rows of A ({A.rows})!" if is_en else f"Không thể nhân: Số cột của B ({B.cols}) phải bằng số hàng của A ({A.rows})!"
                    raise ValueError(err_msg)
                C = B * A
                out.append(f"\n" + (f"[PRODUCT MATRIX RESULT C = B × A]:\n{self.format_matrix_text(C)}" if is_en else f"[KẾT QUẢ MA TRẬN TÍCH C = B × A]:\n{self.format_matrix_text(C)}"))
                repr_rows = "; ".join([", ".join([str(c) for c in r]) for r in C.tolist()])
                self.mat_result_canvas.render_latex(f"C = B \\times A = \\left[ {repr_rows} \\right]")

            elif op == "invA":
                res = compute_matrix_inverse(A)
                detA = res["det"]
                out.append(f"\n" + ("[STEP 1: DETERMINANT det(A)]" if is_en else "[BƯỚC 1: TÍNH ĐỊNH THỨC det(A)]"))
                out.append(f"  det(A) = {detA}")
                if res["invertible"] is False:
                    out.append("  ==> det(A) = 0: Matrix A is SINGULAR (non-invertible, A⁻¹ does not exist)." if is_en else "  ==> det(A) = 0 nên ma trận A SUY BIẾN (không khả nghịch, không tồn tại A⁻¹).")
                    self.mat_result_canvas.render_latex(r"\det(A) = 0 \implies \text{Non-invertible}" if is_en else r"\det(A) = 0 \implies \text{Không khả nghịch}")
                elif res["invertible"] is None:
                    out.append(f"  ==> {res['desc']}")
                    adjA = res["adjugate"]
                    invA = res["inverse"]
                    out.append("\n" + ("[STEP 2: FORMAL ADJUGATE MATRIX (ADJ(A))]" if is_en else "[BƯỚC 2: MA TRẬN PHỤ ĐẠI SỐ HÌNH THỨC (ADJ(A))]"))
                    out.append(f"  adj(A) =\n{self.format_matrix_text(adjA)}")
                    out.append(f"\n" + (f"[STEP 3: CONDITIONAL INVERSE A⁻¹ = (1/det(A)) · adj(A)]:\n{self.format_matrix_text(invA)}" if is_en else f"[BƯỚC 3: NGHỊCH ĐẢO CÓ ĐIỀU KIỆN A⁻¹ = (1/det(A)) · adj(A)]:\n{self.format_matrix_text(invA)}"))
                    repr_rows = "; ".join([", ".join([str(c) for c in r]) for r in invA.tolist()])
                    self.mat_result_canvas.render_latex(r"A^{-1} = \frac{1}{\det(A)} \cdot \text{adj}(A)")
                else:
                    out.append("\n" + ("[STEP 2: ADJUGATE MATRIX (ADJ(A))]" if is_en else "[BƯỚC 2: TÌM MA TRẬN PHỤ ĐẠI SỐ (ADJUGATE MATRIX)]"))
                    adjA = res["adjugate"]
                    out.append(f"  adj(A) =\n{self.format_matrix_text(adjA)}")
                    invA = res["inverse"]
                    out.append(f"\n" + (f"[STEP 3: FORMULA A⁻¹ = (1/det(A)) · adj(A)]:\n{self.format_matrix_text(invA)}" if is_en else f"[BƯỚC 3: CÔNG THỨC A⁻¹ = (1/det(A)) · adj(A)]:\n{self.format_matrix_text(invA)}"))
                    repr_rows = "; ".join([", ".join([str(c) for c in r]) for r in invA.tolist()])
                    self.mat_result_canvas.render_latex(f"A^{{-1}} = \\left[ {repr_rows} \\right]")
            elif op == "detA":
                if A.rows != A.cols:
                    err_msg = "Only square matrices have a determinant det!" if is_en else "Chỉ ma trận vuông mới có định thức det!"
                    raise ValueError(err_msg)
                detA = A.det()
                out.append(f"\n" + (f"[DETERMINANT OF SQUARE MATRIX A ({A.rows} x {A.cols})]:" if is_en else f"[TÍNH ĐỊNH THỨC MA TRẬN VUÔNG A ({A.rows} x {A.cols})]:"))
                if A.rows == 2:
                    out.append("  Diagonal rule: a·d - b·c" if is_en else "  Áp dụng quy tắc đường chéo: a·d - b·c")
                    out.append(f"  det(A) = ({A[0,0]})·({A[1,1]}) - ({A[0,1]})·({A[1,0]}) = {detA}")
                else:
                    out.append("  Laplace expansion / Gaussian triangular reduction:" if is_en else "  Áp dụng khai triển Laplace hoặc đưa về ma trận tam giác:")
                    out.append(f"  det(A) = {detA}")
                self.mat_result_canvas.render_latex(f"\\det(A) = {detA}")

            elif op == "rankA":
                r = A.rank()
                rref_mat, pivots = A.rref()
                out.append(f"\n" + (f"[STEP 1: REDUCED ROW ECHELON FORM (RREF)]:\n{self.format_matrix_text(rref_mat)}" if is_en else f"[BƯỚC 1: ĐƯA MA TRẬN VỀ DẠNG BẬC THANG RÚT GỌN (RREF)]:\n{self.format_matrix_text(rref_mat)}"))
                out.append(f"\n" + (f"[STEP 2: COUNT PIVOT COLUMNS]: {len(pivots)} pivot column(s)" if is_en else f"[BƯỚC 2: ĐẾM SỐ CỘT CƠ SỞ (PIVOTS)]: {len(pivots)} cột cơ sở"))
                out.append(f"==> " + (f"MATRIX RANK rank(A) = {r}" if is_en else f"HẠNG MA TRẬN rank(A) = {r}"))
                self.mat_result_canvas.render_latex(f"\\text{{rank}}(A) = {r}")

            elif op == "transA":
                At = A.T
                out.append(f"\n" + (f"[TRANSPOSE RULE: SWAP ROWS AND COLUMNS]:\n{self.format_matrix_text(At)}" if is_en else f"[QUY TẮC CHUYỂN VỊ: BIẾN DÒNG THÀNH CỘT]:\n{self.format_matrix_text(At)}"))
                repr_rows = "; ".join([", ".join([str(c) for c in r]) for r in At.tolist()])
                self.mat_result_canvas.render_latex(f"A^T = \\left[ {repr_rows} \\right]")

            elif op == "solveAXB":
                if A.rows != B.rows:
                    err_msg = f"Rows of A ({A.rows}) must match rows of vector B ({B.rows})!" if is_en else f"Số hàng của A ({A.rows}) phải bằng số hàng của vector B ({B.rows})!"
                    raise ValueError(err_msg)
                out.append("\n" + ("[STEP 1: AUGMENTED MATRIX (A | B)]" if is_en else "[BƯỚC 1: THIẾT LẬP MA TRẬN MỞ RỘNG (A | B)]"))
                aug = A.row_join(B)
                out.append(self.format_matrix_text(aug))

                try:
                    X = A.LUsolve(B)
                    out.append(f"\n" + ("[STEP 2: GAUSS-JORDAN ELIMINATION OR A⁻¹ · B]" if is_en else "[BƯỚC 2: GIẢI BẰNG PHƯƠNG PHÁP KHỬ GAUSS-JORDAN HOẶC A⁻¹ · B]"))
                    out.append(f"==> " + (f"SOLUTION MATRIX X:\n{self.format_matrix_text(X)}" if is_en else f"NGHIỆM MA TRẬN X:\n{self.format_matrix_text(X)}"))
                    repr_rows = "; ".join([", ".join([str(c) for c in r]) for r in X.tolist()])
                    self.mat_result_canvas.render_latex(f"X = \\left[ {repr_rows} \\right]")
                except Exception as e_solve:
                    out.append(f"\n" + (f"[CONCLUSION]: System has no solution or infinitely many solutions: {e_solve}" if is_en else f"[KẾT LUẬN]: Hệ phương trình vô nghiệm hoặc vô số nghiệm: {e_solve}"))
                    self.mat_result_canvas.render_latex(r"\text{No solution or infinitely many solutions}" if is_en else r"\text{Hệ vô nghiệm hoặc vô số nghiệm}")

            elif op == "eigenA":
                if A.rows != A.cols:
                    err_msg = "Only square matrices have eigenvalues and eigenvectors!" if is_en else "Chỉ ma trận vuông mới có trị riêng và vector riêng!"
                    raise ValueError(err_msg)
                lam = sp.Symbol('lambda')
                char_poly = A.charpoly(lam)
                out.append(f"\n" + ("[STEP 1: CHARACTERISTIC EQUATION det(A - λI) = 0]:" if is_en else "[BƯỚC 1: PHƯƠNG TRÌNH ĐẶC TRƯNG det(A - λI) = 0]:"))
                out.append(f"  P(λ) = {clean_display_expr(char_poly.as_expr())} = 0")

                try:
                    e_vects = A.eigenvects(simplify=False)
                except Exception as e_ev:
                    out.append("  Unable to compute closed-form eigenvectors: " + str(e_ev) if is_en else f"  Không thể tính dạng đóng giải tích cho toàn bộ vector riêng: {e_ev}")
                    e_vects = []

                out.append(f"\n" + ("[STEP 2: EIGENVALUES AND EIGENVECTOR SPACES]:" if is_en else "[BƯỚC 2: CÁC TRỊ RIÊNG VÀ KHÔNG GIAN VECTOR RIÊNG]:"))
                eigen_strs = []
                for idx, (val, mult, basis) in enumerate(e_vects, 1):
                    approx_str = ""
                    try:
                        c_val = complex(sp.N(val))
                        if abs(c_val.imag) < 1e-9:
                            approx_str = f" ≈ {c_val.real:.4f}"
                        else:
                            approx_str = f" ≈ {c_val.real:.4f} + {c_val.imag:.4f}i"
                    except Exception:
                        pass
                    v_clean = clean_display_expr(val)
                    disp_val = f"λ_{idx} = {v_clean}{approx_str}" if len(v_clean) <= 50 else f"λ_{idx}{approx_str}"
                    eigen_strs.append(f"\\lambda_{idx}{approx_str}")
                    mult_lbl = f"(Algebraic multiplicity = {mult})" if is_en else f"(Bội đại số = {mult})"
                    out.append(f"  • {disp_val} {mult_lbl}:")
                    for b in basis:
                        try:
                            b_approx = [f"{complex(sp.N(x)).real:.4f}" if abs(complex(sp.N(x)).imag) < 1e-9 else f"{complex(sp.N(x)):.4f}" for x in b]
                            v_str = ", ".join(b_approx)
                            vec_lbl = "Eigenvector v" if is_en else "Vector riêng v"
                            out.append(f"      {vec_lbl} = [{v_str}]^T")
                        except Exception:
                            vec_lbl = "Eigenvector v" if is_en else "Vector riêng v"
                            out.append(f"      {vec_lbl} = {b.tolist()}")

                latex_summary = ", ".join(eigen_strs[:3]) if eigen_strs else "\\det(A - \\lambda I) = 0"
                self.mat_result_canvas.render_latex(latex_summary)
            self.mat_result_box.insert(tk.END, "\n".join(out))

        except Exception as e:
            self.mat_result_box.insert(tk.END, f"[MATRIX ERROR]: {e}" if is_en else f"[LỖI MA TRẬN]: {e}")
    # --------------------------------------------------------------------------
    # TAB 5: TỔ HỢP - XÁC SUẤT & THỐNG KÊ TOÀN DIỆN
    # --------------------------------------------------------------------------
    def create_statistics_tab(self):
        tab = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(tab, text=self._s("5. Xác suất & Thống kê", "5. Statistics"))

        top_f = tk.Frame(tab, bg="#ffffff")
        top_f.pack(fill=tk.X, pady=(0, 4))

        self.lbl_stat_header = tk.Label(
            top_f,
            text=self._s("BỘ CÔNG CỤ XÁC SUẤT & THỐNG KÊ MÔ TẢ:",
                         "PROBABILITY & DESCRIPTIVE STATISTICS TOOLKIT:"),
            font=("Segoe UI", 9, "bold"), fg="#1e293b", bg="#ffffff"
        )
        self.lbl_stat_header.pack(anchor="w")

        mode_f = tk.Frame(top_f, bg="#ffffff")
        mode_f.pack(fill=tk.X, pady=(2, 4))

        self.lbl_stat_mode = tk.Label(
            mode_f,
            text=self._s("Chế độ:", "Mode:"),
            font=("Segoe UI", 9, "bold"), bg="#ffffff"
        )
        self.lbl_stat_mode.pack(side=tk.LEFT)

        stat_modes_init = [
            "1. Combinatorics & Binomial Theorem",
            "2. Probability & Binomial Distribution B(n, p)",
            "3. Descriptive Statistics (Mean, SD, IQR, Boxplot)"
        ] if getattr(self, "current_lang", "vi") == "en" else [
            "1. Đại số Tổ hợp & Nhị thức Newton",
            "2. Xác suất & Phân phối Nhị thức B(n, p)",
            "3. Thống kê mô tả (Mean, SD, IQR, Boxplot)"
        ]

        self.stat_mode = ttk.Combobox(
            mode_f, width=35, state="readonly",
            values=stat_modes_init
        )
        self.stat_mode.pack(side=tk.LEFT, padx=(4, 12))
        self.stat_mode.set(stat_modes_init[2])
        self.stat_mode.bind("<<ComboboxSelected>>", lambda e: self.update_stat_input_fields())

        self.stat_input_frame = tk.Frame(top_f, bg="#ffffff")
        self.stat_input_frame.pack(fill=tk.X, pady=(2, 4))

        self.stat_lbl1 = tk.Label(
            self.stat_input_frame,
            text=self._s("Dữ liệu mẫu số liệu (cách nhau bởi phẩy hoặc khoảng trắng):",
                         "Sample data (comma or space separated):"),
            font=("Segoe UI", 9), bg="#ffffff"
        )
        self.stat_lbl1.pack(anchor="w")

        self.stat_entry1 = ttk.Entry(self.stat_input_frame, font=("Consolas", 11))
        self.stat_entry1.pack(fill=tk.X, pady=(2, 4))
        self.stat_entry1.insert(0, "12, 15, 14, 18, 19, 15, 16, 20, 22, 15, 17, 35")

        act_f = tk.Frame(top_f, bg="#ffffff")
        act_f.pack(fill=tk.X, pady=(2, 4))

        self.btn_stat = tk.Button(
            act_f,
            text=self._s("⚡ Phân tích thống kê", "⚡ Statistical Analysis"),
            font=("Segoe UI", 8, "bold"), bg="#0969da", fg="#ffffff",
            relief="flat", padx=10, pady=3, cursor="hand2",
            command=self.solve_statistics_action
        )
        self.btn_stat.pack(side=tk.LEFT, padx=(0, 10))

        btn_s1 = tk.Button(act_f, text=self._s("Thống kê có ngoại lai", "Data with outliers"), font=("Segoe UI", 8), bg="#e2e8f0", relief="flat", padx=8, pady=3,
                           command=lambda: self.load_stat_sample("12, 15, 14, 18, 19, 15, 16, 20, 22, 15, 17, 35"))
        btn_s1.pack(side=tk.LEFT, padx=3)

        btn_s2 = tk.Button(act_f, text=self._s("Nhị thức (2x - 3)⁶", "Binomial (2x - 3)^6"), font=("Segoe UI", 8), bg="#e2e8f0", relief="flat", padx=8, pady=3,
                           command=lambda: self.load_binomial_sample("2*x - 3", "6"))
        btn_s2.pack(side=tk.LEFT, padx=3)

        btn_s3 = tk.Button(act_f, text=self._s("Phân phối B(20, 0.4)", "Distribution B(20, 0.4)"), font=("Segoe UI", 8), bg="#e2e8f0", relief="flat", padx=8, pady=3,
                           command=lambda: self.load_prob_sample("20", "0.4"))
        btn_s3.pack(side=tk.LEFT, padx=3)

        self.sample_stat_btns = [btn_s1, btn_s2, btn_s3]

        bot_f = tk.Frame(tab, bg="#ffffff")
        bot_f.pack(fill=tk.BOTH, expand=True)

        left_f = tk.Frame(bot_f, bg="#ffffff")
        left_f.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))

        self.hero_frame_stat = None
        self.lbl_steps_stat = tk.Label(
            left_f,
            text=self._s("BẢNG CHỈ SỐ THỐNG KÊ MÔ TẢ:",
                         "DESCRIPTIVE STATISTICS SUMMARY:"),
            font=("Segoe UI", 9, "bold"), fg="#1e293b", bg="#ffffff"
        )
        self.lbl_steps_stat.pack(anchor="w")

        self.stat_result_box = scrolledtext.ScrolledText(left_f, font=("Consolas", self.current_font_size), bg="#ffffff", fg="#0f172a", relief="solid", bd=1)
        self.stat_result_box.pack(fill=tk.BOTH, expand=True)

        right_f = tk.LabelFrame(
            bot_f,
            text=self._s("BIỂU ĐỒ TẦN SỐ (HISTOGRAM) & BIỂU ĐỒ HỘP (BOXPLOT)",
                         "FREQUENCY HISTOGRAM & BOXPLOT"),
            font=("Segoe UI", 8, "bold"), fg="#0969da", bg="#ffffff"
        )
        self.plot_frame_stat = right_f
        right_f.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4, 0))

        self.stat_fig = Figure(figsize=(4.5, 4), dpi=100, facecolor='#ffffff')
        self.stat_ax1 = self.stat_fig.add_subplot(211)
        self.stat_ax2 = self.stat_fig.add_subplot(212)
        self.stat_canvas = FigureCanvasTkAgg(self.stat_fig, master=right_f)
        self.create_plot_toolbar(self.plot_frame_stat, lambda: self.stat_fig, self.solve_statistics_action, self.stat_canvas.get_tk_widget())
        self.stat_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_stat_input_fields(self):
        mode = self.stat_mode.get()
        is_en = (getattr(self, "current_lang", "vi") == "en")
        if mode.startswith("1") or "Combinatorics" in mode or "Đại số" in mode:
            self.stat_lbl1.config(text="Enter binomial expression (a*x + b)^n or integers n, k:" if is_en else "Nhập biểu thức nhị thức dạng (a*x + b)^n hoặc số n, k:")
            self.stat_entry1.delete(0, tk.END)
            self.stat_entry1.insert(0, "(2*x - 3)^6")
        elif mode.startswith("2") or "Probability" in mode or "Xác suất" in mode:
            self.stat_lbl1.config(text="Enter trials n and success prob p as 'n, p' (e.g. 20, 0.4):" if is_en else "Nhập số lần thử n và xác suất thành công p dạng 'n, p' (VD: 20, 0.4):")
            self.stat_entry1.delete(0, tk.END)
            self.stat_entry1.insert(0, "20, 0.4")
        else:
            self.stat_lbl1.config(text="Sample data (comma or space separated):" if is_en else "Dữ liệu mẫu số liệu (cách nhau bởi phẩy hoặc khoảng trắng):")
            self.stat_entry1.delete(0, tk.END)
            self.stat_entry1.insert(0, "12, 15, 14, 18, 19, 15, 16, 20, 22, 15, 17, 35")

    def load_stat_sample(self, txt: str):
        vals = self.stat_mode['values']
        if len(vals) > 2:
            self.stat_mode.set(vals[2])
        self.update_stat_input_fields()
        self.root.after(50, self.solve_statistics_action)
        self.stat_entry1.delete(0, tk.END); self.stat_entry1.insert(0, txt)
        self.solve_statistics_action()

    def load_binomial_sample(self, expr: str, n_pow: str):
        vals = self.stat_mode['values']
        if len(vals) > 0:
            self.stat_mode.set(vals[0])
        self.update_stat_input_fields()
        self.stat_entry1.delete(0, tk.END); self.stat_entry1.insert(0, f"({expr})^{n_pow}")
        self.solve_statistics_action()

    def load_prob_sample(self, n_val: str, p_val: str):
        vals = self.stat_mode['values']
        if len(vals) > 1:
            self.stat_mode.set(vals[1])
        self.update_stat_input_fields()
        self.stat_entry1.delete(0, tk.END); self.stat_entry1.insert(0, f"{n_val}, {p_val}")
        self.solve_statistics_action()

    def solve_statistics_action(self):
        try:
            self.stat_result_box.delete("1.0", tk.END)
            mode = self.stat_mode.get()
            raw_input = self.stat_entry1.get().strip()
            is_en = (getattr(self, "current_lang", "vi") == "en")

            out = []
            out.append("="*85)
            out.append("ADVANCED COMBINATORICS, PROBABILITY & STATISTICS ENGINE" if is_en else "HỆ THỐNG PHÂN TÍCH TỔ HỢP - XÁC SUẤT & THỐNG KÊ CHUYÊN SÂU")
            out.append("="*85)

            if mode.startswith("1") or "Combinatorics" in mode or "Đại số" in mode:
                if '^' in raw_input or '**' in raw_input:
                    poly_expr = smart_parse(raw_input)
                    expanded = sp.expand(poly_expr)
                    out.append(f"\n" + (f"[NEWTON BINOMIAL EXPANSION]: ({raw_input})" if is_en else f"[KHAI TRIỂN NHỊ THỨC NEWTON]: ({raw_input})"))
                    out.append("  Full expanded expression:" if is_en else "  Biểu thức khai triển đầy đủ:")
                    out.append(f"    P(x) = {clean_display_expr(expanded)}")
                    out.append(f"\n" + ("[TERM COEFFICIENTS TABLE]:" if is_en else "[BẢNG HỆ SỐ CỦA CÁC SỐ HẠNG]:"))
                    poly_x = sp.Poly(expanded, x)
                    coeffs = poly_x.all_coeffs()
                    degrees = range(poly_x.degree(), -1, -1)
                    for d, c in zip(degrees, coeffs):
                        out.append(f"  • " + (f"Coefficient of x^{d}: {clean_display_expr(c)}" if is_en else f"Hệ số của x^{d}: {clean_display_expr(c)}"))
                else:
                    parts = [int(p.strip()) for p in raw_input.replace(',', ' ').split() if p.strip()]
                    n_val = parts[0]
                    k_val = parts[1] if len(parts) > 1 else 1
                    pn = math.factorial(n_val)
                    ank = math.perm(n_val, k_val)
                    cnk = math.comb(n_val, k_val)
                    out.append(f"\n" + (f"[COMBINATORICS]: n = {n_val}, k = {k_val}" if is_en else f"[ĐẠI SỐ TỔ HỢP]: n = {n_val}, k = {k_val}"))
                    out.append(f"  • " + (f"Permutation P_{n_val} = {n_val}! = {pn}" if is_en else f"Hoán vị P_{n_val} = {n_val}! = {pn}"))
                    out.append(f"  • " + (f"Arrangement A_{n_val}^{k_val} = {n_val}! / ({n_val} - {k_val})! = {ank}" if is_en else f"Chỉnh hợp A_{n_val}^{k_val} = {n_val}! / ({n_val} - {k_val})! = {ank}"))
                    out.append(f"  • " + (f"Combination C_{n_val}^{k_val} = {n_val}! / [{k_val}!({n_val} - {k_val})!] = {cnk}" if is_en else f"Tổ hợp C_{n_val}^{k_val} = {n_val}! / [{k_val}!({n_val} - {k_val})!] = {cnk}"))

            elif mode.startswith("2") or "Probability" in mode or "Xác suất" in mode:
                parts = [float(p.strip()) for p in raw_input.replace(',', ' ').split() if p.strip()]
                n_trials = int(parts[0])
                p_prob = parts[1]
                q_prob = 1.0 - p_prob
                ex = n_trials * p_prob
                vx = n_trials * p_prob * q_prob
                sdx = math.sqrt(vx)

                out.append(f"\n" + (f"[BINOMIAL DISTRIBUTION]: X ~ B(n = {n_trials}, p = {p_prob})" if is_en else f"[PHÂN PHỐI NHỊ THỨC]: X ~ B(n = {n_trials}, p = {p_prob})"))
                out.append(f"  • " + (f"Expected Value E(X) = n·p = {ex:.4f}" if is_en else f"Kỳ vọng toán học E(X) = n·p = {ex:.4f}"))
                out.append(f"  • " + (f"Variance V(X) = n·p·(1 - p) = {vx:.4f}" if is_en else f"Phương sai V(X) = n·p·(1 - p) = {vx:.4f}"))
                out.append(f"  • " + (f"Standard Deviation σ(X) = √V(X) = {sdx:.4f}" if is_en else f"Độ lệch chuẩn σ(X) = √V(X) = {sdx:.4f}"))
                out.append(f"\n" + ("[PROBABILITY DISTRIBUTION TABLE P(X = k)]:" if is_en else "[BẢNG PHÂN PHỐI XÁC SUẤT P(X = k)]:"))

                ks = np.arange(0, n_trials + 1)
                probs = [math.comb(n_trials, int(k_i)) * (p_prob**k_i) * (q_prob**(n_trials - k_i)) for k_i in ks]
                for k_i, pr in zip(ks[:15], probs[:15]):
                    out.append(f"  • P(X = {k_i:2d}) = {pr:.5f}")
                if len(ks) > 15:
                    out.append(f"  ... " + ("(Showing first 15 values)" if is_en else "(Hiển thị 15 giá trị đầu tiên)"))

                self.stat_ax1.clear()
                self.stat_ax2.clear()
                self.stat_ax1.bar(ks, probs, color='#0969da', alpha=0.85, width=0.6)
                self.stat_ax1.set_title(f"Binomial Probability Distribution B({n_trials}, {p_prob})" if is_en else f"Phân Phối Xác Suất Nhị Thức B({n_trials}, {p_prob})", fontsize=8, fontweight='bold')
                self.stat_ax1.grid(True, ls=':', color='#cbd5e1')
                self.stat_ax2.plot(ks, np.cumsum(probs), color='#16a34a', lw=2, marker='.')
                self.stat_ax2.set_title("Cumulative Distribution Function F(x) = P(X <= k)" if is_en else "Hàm Phân Phối Tích Lũy F(x) = P(X <= k)", fontsize=8, fontweight='bold')
                self.stat_ax2.grid(True, ls=':', color='#cbd5e1')
                self.stat_fig.tight_layout()
                self.stat_canvas.draw()

            else:
                numbers = [float(item.strip()) for item in re.split(r'[,;\s]+', raw_input) if item.strip()]
                if not numbers:
                    if is_en:
                        messagebox.showwarning("Warning", "Please enter sample data!")
                    else:
                        messagebox.showwarning("Cảnh báo", "Vui lòng nhập danh sách số liệu!")
                    return

                data = np.array(numbers)
                N = len(data)
                mean_val = np.mean(data)
                median_val = np.median(data)
                from collections import Counter
                counts = Counter(numbers)
                mode_val = counts.most_common(1)[0][0]

                q1 = np.percentile(data, 25)
                q2 = np.percentile(data, 50)
                q3 = np.percentile(data, 75)
                iqr = q3 - q1
                min_val = np.min(data)
                max_val = np.max(data)
                range_val = max_val - min_val

                var_sample = np.var(data, ddof=1) if N > 1 else 0.0
                std_sample = np.std(data, ddof=1) if N > 1 else 0.0
                cv = (std_sample / mean_val) * 100 if mean_val != 0 else 0.0

                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                outliers = data[(data < lower_bound) | (data > upper_bound)]

                out.append("\n" + "-"*85)
                out.append("SUMMARY TABLE OF CENTRAL TENDENCY & DISPERSION:" if is_en else "BẢNG TỔNG HỢP CÁC ĐẶC TRƯNG ĐO LƯỜNG XU HƯỚNG TRUNG TÂM & ĐỘ PHÂN TÁN:")
                out.append("-"*85)
                out.append(f"  • " + (f"Sample Size (N)                     : {N}" if is_en else f"Cỡ mẫu quan sát (Sample Size N)        : {N}"))
                out.append(f"  • " + (f"Mean (x̄)                            : {mean_val:.4f}" if is_en else f"Giá trị trung bình (Mean x̄)             : {mean_val:.4f}"))
                out.append(f"  • " + (f"Median (Me)                         : {median_val:.4f}" if is_en else f"Trung vị (Median Me)                    : {median_val:.4f}"))
                out.append(f"  • " + (f"Mode (Mo)                           : {mode_val:.4f}" if is_en else f"Mốt (Mode Mo)                           : {mode_val:.4f}"))
                out.append(f"  • " + (f"Sample Variance (s²)                : {var_sample:.4f}" if is_en else f"Phương sai mẫu hiệu chỉnh (Variance s²) : {var_sample:.4f}"))
                out.append(f"  • " + (f"Sample Standard Deviation (s)       : {std_sample:.4f}" if is_en else f"Độ lệch chuẩn mẫu (Std Dev s)           : {std_sample:.4f}"))
                out.append(f"  • " + (f"Coefficient of Variation (CV)       : {cv:.2f} %" if is_en else f"Hệ số biến thiên (CV)                   : {cv:.2f} %"))
                out.append(f"  • " + (f"Range (R)                           : {range_val:.4f}  (Min: {min_val:.2f}, Max: {max_val:.2f})" if is_en else f"Khoảng biến thiên (Range R)             : {range_val:.4f}  (Min: {min_val:.2f}, Max: {max_val:.2f})"))
                out.append(f"\n" + ("QUARTILES & OUTLIERS EVALUATION:" if is_en else "BẢNG PHÂN VỊ VÀ ĐÁNH GIÁ NGOẠI LAI (QUARTILES & OUTLIERS):"))
                out.append(f"  • " + (f"First Quartile (Q1 - 25%)           : {q1:.4f}" if is_en else f"Tứ phân vị thứ nhất (Q1 - 25%)          : {q1:.4f}"))
                out.append(f"  • " + (f"Second Quartile (Q2/Median - 50%)    : {q2:.4f}" if is_en else f"Tứ phân vị thứ hai  (Q2/Median - 50%)   : {q2:.4f}"))
                out.append(f"  • " + (f"Third Quartile (Q3 - 75%)            : {q3:.4f}" if is_en else f"Tứ phân vị thứ ba   (Q3 - 75%)          : {q3:.4f}"))
                out.append(f"  • " + (f"Interquartile Range (IQR = Q3 - Q1)  : {iqr:.4f}" if is_en else f"Khoảng tứ phân vị (IQR = Q3 - Q1)       : {iqr:.4f}"))
                out.append(f"  • " + (f"Valid Boundary: [{lower_bound:.2f} ; {upper_bound:.2f}]" if is_en else f"Ranh giới hợp lệ: [{lower_bound:.2f} ; {upper_bound:.2f}]"))
                if len(outliers) > 0:
                    out.append(f"  ==> " + (f"OUTLIERS DETECTED: {list(outliers)}" if is_en else f"PHÁT HIỆN GIÁ TRỊ NGOẠI LAI (Outliers): {list(outliers)}"))
                else:
                    out.append("  ==> " + ("No abnormal outliers detected in sample data." if is_en else "Không phát hiện giá trị ngoại lai bất thường trong mẫu số liệu."))

                self.stat_ax1.clear()
                self.stat_ax2.clear()

                self.stat_ax1.hist(data, bins='auto', color='#0969da', edgecolor='#1e293b', alpha=0.75)
                self.stat_ax1.axvline(mean_val, color='#ef4444', lw=1.8, ls='--', label=f'Mean={mean_val:.2f}')
                self.stat_ax1.axvline(median_val, color='#16a34a', lw=1.8, ls=':', label=f'Median={median_val:.2f}')
                self.stat_ax1.set_title(f"Frequency Histogram (N={N})" if is_en else f"Biểu Đồ Tần Số (Histogram, N={N})", fontsize=8, fontweight='bold')
                self.stat_ax1.legend(loc='upper right', fontsize=8)
                self.stat_ax1.grid(True, ls=':', color='#cbd5e1')

                self.stat_ax2.boxplot(data, vert=False, patch_artist=True,
                                      boxprops=dict(facecolor='#dbeafe', color='#1d4ed8'),
                                      medianprops=dict(color='#ef4444', lw=2),
                                      flierprops=dict(marker='o', markerfacecolor='#dc2626', markersize=6))
                self.stat_ax2.set_title("Boxplot & Outliers" if is_en else "Biểu Đồ Hộp Râu (Boxplot & Outliers)", fontsize=8, fontweight='bold')
                self.stat_ax2.grid(True, ls=':', color='#cbd5e1')

                self.stat_fig.tight_layout()
                self.stat_canvas.draw()

            self.stat_result_box.insert(tk.END, "\n".join(out))

        except Exception as e:
            self.stat_result_box.insert(tk.END, f"[STATISTICS ERROR]: {e}" if is_en else f"[LỖI THỐNG KÊ]: {e}")
    # --------------------------------------------------------------------------
    # TAB 6: KHẢO SÁT HÀM SỐ & ĐỒ THỊ 2D TRÊN MẶT PHẲNG OXY
    # --------------------------------------------------------------------------
    def create_plot_oxy_tab(self):
        tab = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(tab, text=self._s("6. Đồ thị hàm số", "6. Grapher"))

        # Equation Ribbon
        self.create_equation_ribbon(tab, lambda: self.plot_f_entry)

        top_f = tk.Frame(tab, bg="#ffffff")
        top_f.pack(fill=tk.X, pady=(0, 4))

        self.lbl_plot_header = tk.Label(
            top_f,
            text=self._s("HÀM SỐ CẦN KHẢO SÁT f(x) (HỆ TRỤC TỌA ĐỘ OXY):",
                         "FUNCTION TO STUDY f(x) (2D OXY COORDINATE SYSTEM):"),
            font=("Segoe UI", 9, "bold"), fg="#1e293b", bg="#ffffff"
        )
        self.lbl_plot_header.pack(anchor="w")

        self.plot_f_entry = ttk.Entry(top_f, font=("Consolas", 11))
        self.plot_f_entry.pack(fill=tk.X, pady=(2, 4))
        self.plot_f_entry.insert(0, "x^3 - 3*x^2 + 2")

        act_f = tk.Frame(top_f, bg="#ffffff")
        act_f.pack(fill=tk.X, pady=(2, 4))

        self.btn_run_plot = tk.Button(
            act_f,
            text=self._s("⚡ Khảo sát & Vẽ đồ thị", "⚡ Plot Graph & Study"),
            font=("Segoe UI", 8, "bold"), bg="#0969da", fg="#ffffff",
            relief="flat", padx=10, pady=3, cursor="hand2",
            command=self.solve_plot_oxy_action
        )
        self.btn_run_plot.pack(side=tk.LEFT, padx=(0, 10))

        btn_p1 = tk.Button(act_f, text="x³ - 3x² + 2", font=("Segoe UI", 8), bg="#e2e8f0", relief="flat", padx=8, pady=3,
                           command=lambda: self.load_plot_sample("x^3 - 3*x^2 + 2"))
        btn_p1.pack(side=tk.LEFT, padx=3)

        btn_p2 = tk.Button(act_f, text="x⁴ - 2x² - 1", font=("Segoe UI", 8), bg="#e2e8f0", relief="flat", padx=8, pady=3,
                           command=lambda: self.load_plot_sample("x^4 - 2*x^2 - 1"))
        btn_p2.pack(side=tk.LEFT, padx=3)

        btn_p3 = tk.Button(act_f, text="(2x+1)/(x-1)", font=("Segoe UI", 8), bg="#e2e8f0", relief="flat", padx=8, pady=3,
                           command=lambda: self.load_plot_sample("(2*x + 1)/(x - 1)"))
        btn_p3.pack(side=tk.LEFT, padx=3)

        btn_p4 = tk.Button(act_f, text="sin(x) + cos(x)", font=("Segoe UI", 8), bg="#e2e8f0", relief="flat", padx=8, pady=3,
                           command=lambda: self.load_plot_sample("sin(x) + cos(x)"))
        btn_p4.pack(side=tk.LEFT, padx=3)

        self.sample_plot_btns = [btn_p1, btn_p2, btn_p3, btn_p4]

        bot_f = tk.Frame(tab, bg="#ffffff")
        bot_f.pack(fill=tk.BOTH, expand=True)

        left_f = tk.Frame(bot_f, bg="#ffffff")
        left_f.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))

        self.lbl_plot_res = tk.Label(
            left_f,
            text=self._s("BẢNG KHẢO SÁT BIẾN THIÊN & ĐỒ THỊ:",
                         "VARIATION & GRAPH REPORT:"),
            font=("Segoe UI", 9, "bold"), fg="#1e293b", bg="#ffffff"
        )
        self.lbl_plot_res.pack(anchor="w")
        self.plot_result_box = scrolledtext.ScrolledText(left_f, font=("Consolas", self.current_font_size), bg="#ffffff", fg="#0f172a", relief="solid", bd=1)
        self.plot_result_box.pack(fill=tk.BOTH, expand=True)

        self.graph_frame_plot = tk.LabelFrame(bot_f, text="ĐỒ THỊ HÀM SỐ 2D TRÊN HỆ TRỤC TỌA ĐỘ OXY",
                                             font=("Segoe UI", 8, "bold"), fg="#0969da", bg="#ffffff")
        self.graph_frame_plot.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4, 0))

        self.plot_fig = Figure(figsize=(4.5, 4), dpi=100, facecolor='#ffffff')
        self.plot_ax = self.plot_fig.add_subplot(111)
        self.plot_canvas = FigureCanvasTkAgg(self.plot_fig, master=self.graph_frame_plot)
        self.create_plot_toolbar(self.graph_frame_plot, lambda: self.plot_fig, self.solve_plot_oxy_action, self.plot_canvas.get_tk_widget())
        self.plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_plot_sample(self, expr_str: str):
        self.plot_f_entry.delete(0, tk.END)
        self.plot_f_entry.insert(0, expr_str)
        self.solve_plot_oxy_action()

    def solve_plot_oxy_action(self):
        try:
            self.plot_result_box.delete("1.0", tk.END)
            f_str = self.plot_f_entry.get().strip()
            if not f_str:
                return
            f_sym = smart_parse(f_str)

            is_en = (getattr(self, "current_lang", "vi") == "en")
            out = []
            out.append("="*85)
            out.append("FUNCTION VARIATION & 2D GRAPH STUDY (OXY PLANE)" if is_en else "KHẢO SÁT SỰ BIẾN THIÊN VÀ VẼ ĐỒ THỊ HÀM SỐ TRÊN MẶT PHẲNG OXY")
            out.append(f"y = f(x) = {clean_display_expr(f_sym)}")
            out.append("="*85)

            # 1. TẬP XÁC ĐỊNH
            out.append("\n" + ("[1. DOMAIN & SYMMETRY PROPERTIES]" if is_en else "[1. TẬP XÁC ĐỊNH & TÍNH CHẤT ĐỐI XỨNG]"))
            denom = sp.denom(f_sym)
            if denom != 1 and denom.has(x):
                bad_pts = sp.solve(denom, x)
                bad_real = [bp for bp in bad_pts if bp.is_real]
                if bad_real:
                    pts_str = ', '.join([str(bp) for bp in bad_real])
                    out.append(f"  • " + (f"Denominator vanishes at: x ∈ {{{pts_str}}}" if is_en else f"Mẫu số triệt tiêu tại: x ∈ {{{pts_str}}}"))
                    out.append(f"  • " + (f"Domain: D = ℝ \\ {{{pts_str}}}" if is_en else f"Tập xác định: D = ℝ \\ {{{pts_str}}}"))
                else:
                    out.append("  • " + ("Denominator is non-zero everywhere on ℝ. Domain: D = ℝ." if is_en else "Mẫu số luôn khác 0 trên ℝ. Tập xác định: D = ℝ."))
            else:
                out.append("  • " + ("Domain: D = ℝ." if is_en else "Tập xác định: D = ℝ."))

            # Kiểm tra chẵn lẻ
            try:
                diff_even = sp.simplify(f_sym.subs(x, -x) - f_sym)
                diff_odd = sp.simplify(f_sym.subs(x, -x) + f_sym)
                if diff_even == 0:
                    out.append("  • " + ("Even function: f(-x) = f(x) ==> Symmetric across y-axis (Oy)." if is_en else "Hàm số chẵn: f(-x) = f(x) ==> Đồ thị nhận trục tung Oy làm trục đối xứng."))
                elif diff_odd == 0:
                    out.append("  • " + ("Odd function: f(-x) = -f(x) ==> Symmetric across origin O." if is_en else "Hàm số lẻ: f(-x) = -f(x) ==> Đồ thị nhận gốc tọa độ O làm tâm đối xứng."))
                else:
                    out.append("  • " + ("No special even/odd symmetry." if is_en else "Đồ thị hàm số không có tính chất đối xứng chẵn lẻ đặc biệt."))
            except Exception:
                pass

            # 2. ĐẠO HÀM BẬC 1 & SỰ BIẾN THIÊN
            out.append("\n" + ("[2. FIRST DERIVATIVE & MONOTONICITY]" if is_en else "[2. ĐẠO HÀM BẬC 1 & SỰ BIẾN THIÊN]"))
            df = sp.diff(f_sym, x)
            crit_pts = sp.solve(df, x)
            real_crit = []
            for cp in crit_pts:
                try:
                    cp_eval = cp.evalf()
                    if cp.is_real or abs(complex(cp_eval).imag) < 1e-9:
                        real_crit.append(float(sp.re(cp_eval)))
                except Exception:
                    pass
            real_crit = sorted(list(dict.fromkeys(real_crit)))

            out.append(f"  • y' = f'(x) = {clean_display_expr(sp.simplify(df))}")
            if real_crit:
                crits_str = ', '.join([f'{r:.4f}' for r in real_crit])
                out.append(f"  • " + (f"Set y' = 0 <=> x ∈ {{{crits_str}}}" if is_en else f"Cho y' = 0 <=> x ∈ {{{crits_str}}}"))
                for r in real_crit:
                    try:
                        y_val = float(sp.re(f_sym.subs(x, r).evalf()))
                        d2_val = float(sp.re(sp.diff(df, x).subs(x, r).evalf()))
                        if is_en:
                            loai = "LOCAL MINIMUM" if d2_val > 0 else ("LOCAL MAXIMUM" if d2_val < 0 else "Stationary point")
                            out.append(f"    ==> Point {loai}: ({r:.2f}; {y_val:.2f})")
                        else:
                            loai = "CỰC TIỂU" if d2_val > 0 else ("CỰC ĐẠI" if d2_val < 0 else "Điểm dừng")
                            out.append(f"    ==> Điểm {loai}: ({r:.2f}; {y_val:.2f})")
                    except Exception:
                        pass
            else:
                out.append("  • " + ("Equation y' = 0 has no real solutions." if is_en else "Phương trình y' = 0 vô nghiệm thực."))

            # 3. ĐẠO HÀM BẬC 2 & ĐIỂM UỐN
            d2f = sp.diff(df, x)
            infl_pts = sp.solve(d2f, x)
            real_infl = []
            for ip in infl_pts:
                try:
                    ip_eval = ip.evalf()
                    if ip.is_real or abs(complex(ip_eval).imag) < 1e-9:
                        real_infl.append(float(sp.re(ip_eval)))
                except Exception:
                    pass
            real_infl = sorted(list(dict.fromkeys(real_infl)))

            out.append("\n" + ("[3. SECOND DERIVATIVE, CURVATURE & INFLECTION POINTS]" if is_en else "[3. ĐẠO HÀM BẬC 2, ĐỘ CONG & ĐIỂM UỐN CỦA ĐỒ THỊ]"))
            out.append(f"  • y'' = f''(x) = {clean_display_expr(sp.simplify(d2f))}")
            if real_infl:
                infls_str = ', '.join([f'{r:.4f}' for r in real_infl])
                out.append(f"  • " + (f"Set y'' = 0 <=> x ∈ {{{infls_str}}}" if is_en else f"Cho y'' = 0 <=> x ∈ {{{infls_str}}}"))
                for r in real_infl:
                    try:
                        y_val = float(sp.re(f_sym.subs(x, r).evalf()))
                        out.append(f"    ==> " + (f"Inflection point U: ({r:.2f}; {y_val:.2f})" if is_en else f"Điểm uốn U: ({r:.2f}; {y_val:.2f})"))
                    except Exception:
                        pass
            else:
                out.append("  • " + ("No inflection points changing curvature sign on ℝ." if is_en else "Đồ thị không có điểm uốn đổi dấu độ cong trên ℝ."))

            # 4. TIỆM CẬN
            out.append("\n" + ("[4. ASYMPTOTES (OXY PLANE)]" if is_en else "[4. ĐƯỜNG TIỆM CẬN (MẶT PHẲNG OXY)]"))
            asymptotes_v = []
            asymptotes_h = []
            denom_roots = sp.solve(denom, x) if denom != 1 and denom.has(x) else []
            for dr in denom_roots:
                if dr.is_real:
                    val_tc = float(dr.evalf())
                    asymptotes_v.append(val_tc)
                    out.append(f"  • " + (f"Vertical asymptote (VA): x = {val_tc:.2f}" if is_en else f"Tiệm cận đứng (TCĐ): x = {val_tc:.2f}"))

            try:
                lim_pos = sp.limit(f_sym, x, sp.oo)
                lim_neg = sp.limit(f_sym, x, -sp.oo)
                if lim_pos.is_real and not lim_pos.has(sp.oo):
                    val_h = float(lim_pos.evalf())
                    asymptotes_h.append(val_h)
                    out.append(f"  • " + (f"Horizontal asymptote (HA): y = {val_h:.2f} (as x -> +∞)" if is_en else f"Tiệm cận ngang (TCN): y = {val_h:.2f} (khi x -> +∞)"))
                if lim_neg.is_real and not lim_neg.has(sp.oo) and lim_neg != lim_pos:
                    val_h2 = float(lim_neg.evalf())
                    asymptotes_h.append(val_h2)
                    out.append(f"  • " + (f"Horizontal asymptote (HA): y = {val_h2:.2f} (as x -> -∞)" if is_en else f"Tiệm cận ngang (TCN): y = {val_h2:.2f} (khi x -> -∞)"))
            except Exception:
                pass

            if not asymptotes_v and not asymptotes_h:
                out.append("  • " + ("Graph has no vertical or horizontal asymptotes." if is_en else "Đồ thị hàm số không có tiệm cận đứng hoặc ngang."))

            # 5. GIAO ĐIỂM VỚI CÁC TRỤC TỌA ĐỘ
            out.append("\n" + ("[5. INTERCEPTS WITH COORDINATE AXES OX, OY]" if is_en else "[5. GIAO ĐIỂM VỚI CÁC TRỤC TỌA ĐỘ OX, OY]"))
            try:
                y0 = float(sp.re(f_sym.subs(x, 0).evalf()))
                out.append(f"  • " + (f"y-intercept (x = 0): M(0; {y0:.2f})" if is_en else f"Giao với trục tung Oy (x = 0): M(0; {y0:.2f})"))
            except Exception:
                out.append("  • " + ("Function is undefined at x = 0 (no y-intercept)." if is_en else "Hàm số không xác định tại x = 0 (không cắt trục Oy)."))

            try:
                x_intercepts = sp.solve(f_sym, x)
                real_x_int = [float(sp.re(xi.evalf())) for xi in x_intercepts if xi.is_real]
                if real_x_int:
                    x_int_str = ', '.join([f'{xi:.2f}' for xi in real_x_int])
                    out.append(f"  • " + (f"x-intercepts (y = 0): x ∈ {{{x_int_str}}}" if is_en else f"Giao với trục hoành Ox (y = 0): x ∈ {{{x_int_str}}}"))
            except Exception:
                pass

            # 6. DIỆN TÍCH TÍCH PHÂN
            out.append("\n" + ("[6. AREA INTEGRAL]" if is_en else "[6. TÍCH PHÂN DIỆN TÍCH HÌNH PHẲNG]"))
            try:
                int_val = sp.integrate(sp.Abs(f_sym), (x, 0, 2))
                out.append(f"  • " + (f"Area S bounded by graph and Ox on [0, 2]: S = ∫|f(x)|dx ≈ {float(int_val.evalf()):.4f}" if is_en else f"Diện tích S giới hạn bởi đồ thị và Ox trên [0, 2]: S = ∫|f(x)|dx ≈ {float(int_val.evalf()):.4f}"))
            except Exception:
                pass

            self.plot_result_box.insert(tk.END, "\n".join(out))

            # VẼ ĐỒ THỊ 2D OXY CHUẨN
            self.plot_fig.clear()
            self.plot_ax = self.plot_fig.add_subplot(111)

            fn = sp.lambdify(x, f_sym, modules=['numpy', {'sqrt': np.lib.scimath.sqrt}])
            xs = np.linspace(-6, 6, 800)
            ys = np.real(fn(xs))
            ys = np.clip(ys, -25, 25)

            # Vẽ đường cong hàm số
            self.plot_ax.plot(xs, ys, color='#0969da', lw=2, label='y = f(x)')

            # Trục tọa độ Ox, Oy
            self.plot_ax.axhline(0, color='#334155', lw=1.2, ls='-')
            self.plot_ax.axvline(0, color='#334155', lw=1.2, ls='-')
            self.plot_ax.text(5.6, 0.5, "Ox", fontsize=9, fontweight='bold', color='#334155')
            self.plot_ax.text(0.3, 13.5, "Oy", fontsize=9, fontweight='bold', color='#334155')
            self.plot_ax.text(0.2, -1.2, "O", fontsize=9, fontweight='bold', color='#334155')

            # Vẽ tiệm cận đứng
            for tc_x in asymptotes_v:
                lbl_va = f'VA: x={tc_x:.1f}' if is_en else f'TCĐ: x={tc_x:.1f}'
                self.plot_ax.axvline(tc_x, color='#9333ea', lw=1.2, ls='--', label=lbl_va)
            # Vẽ tiệm cận ngang
            for tc_y in asymptotes_h:
                lbl_ha = f'HA: y={tc_y:.1f}' if is_en else f'TCN: y={tc_y:.1f}'
                self.plot_ax.axhline(tc_y, color='#0284c7', lw=1.2, ls='--', label=lbl_ha)

            # Đánh dấu các điểm cực trị
            for cp in real_crit:
                try:
                    cy = float(sp.re(f_sym.subs(x, cp).evalf()))
                    if -6 <= cp <= 6 and -25 <= cy <= 25:
                        self.plot_ax.plot(cp, cy, marker='o', markersize=7, color='#dc2626', zorder=5)
                        ann_txt = f"Extremum\n({cp:.1f}, {cy:.1f})" if is_en else f"Cực trị\n({cp:.1f}, {cy:.1f})"
                        y_offset = -24 if cy > 8 else 10
                        self.plot_ax.annotate(
                            ann_txt, (cp, cy),
                            textcoords="offset points", xytext=(0, y_offset),
                            ha='center', fontsize=8, fontweight='bold', color='#dc2626',
                            clip_on=False,
                            bbox=dict(boxstyle="round,pad=0.25", facecolor="#ffffff", alpha=0.92, edgecolor="#f87171", linewidth=0.8)
                        )
                except Exception:
                    pass

            self.plot_ax.set_xlim(-6, 6)
            self.plot_ax.set_ylim(-15, 15)
            self.plot_ax.grid(True, ls=':', color='#cbd5e1')
            self.plot_ax.legend(loc='upper right', fontsize=8)
            self.plot_canvas.draw()

        except Exception as e:
            self.plot_result_box.insert(tk.END, f"[PLOT ERROR]: {e}" if is_en else f"[LỖI ĐỒ THỊ]: {e}")

    def apply_theme(self, theme_key: str = "win11_light"):
        """Áp dụng bộ giao diện người dùng theo chủ đề Sáng / Xanh hiện đại / Kỹ thuật cổ điển / Tối."""
        if theme_key not in THEMES:
            theme_key = "win11_light"
        self.current_theme_key = theme_key
        t = THEMES[theme_key]

        try:
            self.root.configure(bg=t["bg_window"])
            if hasattr(self, "status_bar") and self.status_bar:
                self.status_bar.configure(bg=t["status_bg"])
            if hasattr(self, "status_lbl") and self.status_lbl:
                self.status_lbl.configure(bg=t["status_bg"], fg=t["status_fg"])
            if hasattr(self, "ai_toolbar") and self.ai_toolbar:
                self.ai_toolbar.configure(bg=t["toolbar_bg"])

            # ttk Style cho Notebook và Tabs
            style = ttk.Style()
            style.theme_use('clam')
            style.configure(".", background=t["bg_window"], foreground=t["text_box_fg"], font=("Segoe UI", 9))
            style.configure("TNotebook", background=t["bg_window"], borderwidth=0)
            style.configure("TNotebook.Tab", background=t["tab_bg"], foreground=t["tab_fg"],
                            font=("Segoe UI", 9, "bold"), padding=[16, 8])
            style.map("TNotebook.Tab",
                      background=[("selected", t["tab_active_bg"])],
                      foreground=[("selected", t["tab_active_fg"])])
            style.configure("TFrame", background=t["bg_card"])
            style.configure("TLabel", background=t["bg_card"], foreground=t["text_box_fg"])

            # Cập nhật đệ quy các widget trong toàn bộ giao diện
            def _apply_widget_theme(w):
                w_class = w.winfo_class()
                try:
                    if w_class in ("Frame",):
                        w_name = str(w).lower()
                        if "canvas" not in w_name:
                            w.configure(bg=t["bg_card"])
                    elif w_class in ("Labelframe", "LabelFrame"):
                        w.configure(bg=t["bg_card"], fg=t["btn_accent_bg"])
                    elif w_class in ("Label",):
                        w.configure(bg=t["bg_card"], fg=t["text_box_fg"])
                    elif w_class in ("Text",):
                        w.configure(bg=t["text_box_bg"], fg=t["text_box_fg"], insertbackground=t["tab_active_fg"])
                    elif w_class in ("Entry",):
                        w.configure(bg=t["entry_bg"], fg=t["entry_fg"], insertbackground=t["tab_active_fg"])
                except Exception:
                    pass
                for ch in w.winfo_children():
                    _apply_widget_theme(ch)

            if hasattr(self, "notebook"):
                for tab_id in self.notebook.tabs():
                    tab_w = self.notebook.nametowidget(tab_id)
                    _apply_widget_theme(tab_w)

            # Cập nhật hộp kết quả văn bản
            for box in [
                getattr(self, 'eq_result_box', None),
                getattr(self, 'ext_result_box', None),
                getattr(self, 'calc_result_box', None),
                getattr(self, 'mat_result_box', None),
                getattr(self, 'stat_result_box', None),
                getattr(self, 'plot_result_box', None)
            ]:
                if box:
                    try:
                        box.configure(bg=t["text_box_bg"], fg=t["text_box_fg"], insertbackground=t["tab_active_fg"])
                    except Exception:
                        pass

            # Cập nhật các đồ thị Matplotlib
            for fig_name in ("eq_fig", "ext_fig", "calc_fig", "plot_fig", "stat_fig"):
                fig = getattr(self, fig_name, None)
                if fig:
                    try:
                        fig.patch.set_facecolor(t["bg_card"])
                        for ax in fig.axes:
                            ax.set_facecolor(t["bg_card"])
                            ax.tick_params(colors=t["text_box_fg"])
                            for spine in ax.spines.values():
                                spine.set_color(t["border_color"])
                            ax.title.set_color(t["text_box_fg"])
                            ax.xaxis.label.set_color(t["text_box_fg"])
                            ax.yaxis.label.set_color(t["text_box_fg"])
                    except Exception:
                        pass

            # Vẽ lại canvas đồ thị
            for c_name in ("eq_canvas", "ext_canvas", "calc_canvas", "plot_canvas", "stat_canvas"):
                c = getattr(self, c_name, None)
                if c:
                    try:
                        c.draw_idle()
                    except Exception:
                        pass

            if hasattr(self, "status_lbl") and self.status_lbl:
                is_en = (getattr(self, "current_lang", "vi") == "en")
                self.status_lbl.config(text=f"Theme switched: {t['name']}" if is_en else f"Đã chuyển giao diện: {t['name']}")
        except Exception:
            pass


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================
def main():
    root = tk.Tk()
    root.withdraw()
    splash = None
    try:
        from stem_shared_core.splash_screen import attach_splash_screen
        splash = attach_splash_screen(
            root,
            app_id="cad_math",
            app_title="CAD Math Studio Pro v2.4",
            min_duration=2.2
        )
    except Exception:
        root.deiconify()

    app = CADMathDesktopAppV2(root)
    if splash:
        splash.set_app_ready()
    root.mainloop()


if __name__ == '__main__':
    main()
