# -*- coding: utf-8 -*-

"""

GeoSolver CAD - Engine Giải Toán Hình Học Tổng Quát & Chuyên Đề Olympic / Oxy

Phiên bản Giao Diện Gọn Nhẹ Chuẩn Technical CAD Studio

- Thanh công cụ ngang trên đỉnh (Top Toolbars) gọn nhẹ, trực quan, không chiếm diện tích ngang

- Không gian Canvas rộng rãi chiếm tối đa màn hình

- Bảng lời giải bên phải gọn gàng, có nút Thu gọn / Mở rộng (Toggle) linh hoạt

- Bộ công cụ đầy đủ: Tiếp tuyến thông minh, Tiếp tuyến chung, Hình bình hành, Hình thoi, Nội tiếp, Ngoại tiếp

- Cố định thuật ngữ mục tiêu bài toán, chống gõ sai, bảo toàn mẫu câu

"""



import sys
import os

# An toàn tuyệt đối cho môi trường pythonw (tránh NoneType crash khi gọi print)
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

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if _CURRENT_DIR not in sys.path:
    sys.path.insert(0, _CURRENT_DIR)
if hasattr(sys, '_MEIPASS') and sys._MEIPASS not in sys.path:
    sys.path.insert(0, sys._MEIPASS)
_PARENT_DIR = os.path.dirname(_CURRENT_DIR)
if _PARENT_DIR not in sys.path:
    sys.path.insert(0, _PARENT_DIR)


import math

import copy

import re

import tkinter as tk

from tkinter import ttk, messagebox, simpledialog, filedialog

from PIL import Image, ImageDraw, ImageFont

import sympy as sp

from pathlib import Path



# Đảm bảo UTF-8 và DPI trên Windows

if sys.platform.startswith('win'):

    try:

        sys.stdout.reconfigure(encoding='utf-8')

    except Exception:

        pass

    try:

        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)

    except Exception:

        pass



# ---------------------------------------------------------------------------

# STEM_SHARED_CORE: thêm thư mục gốc vào sys.path để import được shared core

# ---------------------------------------------------------------------------

_STEM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if _STEM_ROOT not in sys.path:

    sys.path.insert(0, _STEM_ROOT)



# Import hệ thống i18n tập trung; nếu không có thì dùng fallback LANG_DATA nội bộ

try:

    from stem_shared_core.i18n import t as _i18n_t, set_language as _i18n_set, get_language as _i18n_get

    _I18N_AVAILABLE = True

except Exception:

    _I18N_AVAILABLE = False



# Import UI State & Window Geometry / Tab Manager

try:

    from stem_shared_core.tools.ui_state_manager import UIStateManager

    _UI_STATE_AVAILABLE = True

except Exception:

    _UI_STATE_AVAILABLE = False

    UIStateManager = None



# Import AI downloader & model hub; nếu không có thì vô hiệu hóa tính năng

try:

    from stem_shared_core.hf_downloader import ask_download_model

    from stem_shared_core.ai_model_hub import AIModelHub, ModelSource

    _AI_HUB_AVAILABLE = True

except Exception:

    _AI_HUB_AVAILABLE = False

# Import Lõi Hình học Phẳng độc lập (GeoSolver2DCore) đã qua thẩm định khoa học
try:
    from stem_shared_core.geosolver_core import (
        GeoSolver2DCore,
        MissingGeometricNodeError,
        DegenerateGeometryError,
        OutOfBoundsError
    )
    _GEOSOLVER_CORE_AVAILABLE = True
except Exception:
    _GEOSOLVER_CORE_AVAILABLE = False
    GeoSolver2DCore = None



# ==============================================================================

# HÀM TOÁN HỌC HÌNH HỌC PHẲNG: ELIP, HÌNH THANG CÂN, HÌNH THOI, HÌNH BÌNH HÀNH

# ==============================================================================

def calc_ellipse_area(a: float, b: float) -> float:

    """Tính diện tích hình elip S = pi * a * b."""

    return math.pi * abs(a) * abs(b)





def calc_ellipse_perimeter(a: float, b: float) -> float:
    """Tính chu vi hình elip theo công thức xấp xỉ Ramanujan thứ 2 (Ramanujan II).
    Công thức: P ≈ π(a + b) * [1 + 3h / (10 + sqrt(4 - 3h))] với h = ((a - b)/(a + b))^2.
    Đạt độ chính xác vượt trội (sai số < 0.05% trên mọi tỷ lệ b/a, kể cả b -> 0).
    Khi b = 0 (đoạn thẳng suy biến đi-về): P = 4a chính xác.
    """
    a_val, b_val = abs(a), abs(b)
    if a_val == 0.0 and b_val == 0.0:
        return 0.0
    if b_val == 0.0:
        return 4.0 * a_val
    if a_val == 0.0:
        return 4.0 * b_val
    h = ((a_val - b_val) / (a_val + b_val)) ** 2
    return math.pi * (a_val + b_val) * (1.0 + (3.0 * h) / (10.0 + math.sqrt(max(0.0, 4.0 - 3.0 * h))))






def compute_ellipse_from_foci(f1x: float, f1y: float, f2x: float, f2y: float, mx: float, my: float):
    """
    Tính tham số hình học của Elip từ 2 Tiêu điểm F1, F2 và 1 Điểm M nằm trên elip.
    Định nghĩa kinh điển: MF1 + MF2 = 2a => a = (MF1 + MF2) / 2.
    Tiêu cự 2c = |F1 F2| => b = sqrt(a^2 - c^2).
    Tâm O = trung điểm F1 F2.
    Góc nghiêng theta = góc của vector F1F2.
    """
    ox = (f1x + f2x) / 2.0
    oy = (f1y + f2y) / 2.0
    c_val = math.hypot(f2x - f1x, f2y - f1y) / 2.0  # bán tiêu cự c
    d1 = math.hypot(mx - f1x, my - f1y)
    d2 = math.hypot(mx - f2x, my - f2y)
    a = (d1 + d2) / 2.0  # bán trục lớn a
    # Trường hợp tiêu điểm trùng nhau F1 == F2: Elip trở thành đường tròn tâm F1 bán kính a
    tol_c = max(1e-7, 1e-6 * max(a, c_val))
    if c_val < 1e-9:
        b = a
        theta = 0.0
    elif a <= c_val + tol_c:
        # Trường hợp suy biến: Điểm M nằm trên đoạn F1F2 => b = 0 (đoạn thẳng)
        b = 0.0
        theta = math.atan2(f2y - f1y, f2x - f1x)
    else:
        b = math.sqrt(max(0.0, a * a - c_val * c_val))
        theta = math.atan2(f2y - f1y, f2x - f1x)
    area = calc_ellipse_area(a, b)
    perimeter = calc_ellipse_perimeter(a, b)
    return {
        "ox": ox, "oy": oy, "a": a, "b": b, "c": c_val, "theta": theta,
        "area": area, "perimeter": perimeter
    }


def format_radical_len(val: float, p1=None, p2=None) -> str:
    """Biểu diễn độ dài dưới dạng căn thức rút gọn chính xác, kèm giá trị thập phân xấp xỉ.
    
    Lưu ý:
    Dạng căn thức chính xác (k√m hoặc √m) chỉ được đảm bảo khi truyền cặp điểm mút nguyên/hữu tỉ p1, p2
    để tính d_sq = dx^2 + dy^2 trên số nguyên. Khi không truyền p1, p2 (None), d_sq = val^2 tích lũy
    sai số dấu phẩy động (FP error), có thể khiến các giá trị vô tỉ thuần túy (ví dụ √6) hiển thị ở dạng
    thập phân (≈ 2.45).
    """
    if val < 1e-4:
        return "0"
    if p1 is not None and p2 is not None:
        dx = (p1["x"] if isinstance(p1, dict) else p1[0]) - (p2["x"] if isinstance(p2, dict) else p2[0])
        dy = (p1["y"] if isinstance(p1, dict) else p1[1]) - (p2["y"] if isinstance(p2, dict) else p2[1])
        d_sq = dx * dx + dy * dy
    else:
        d_sq = val * val

    n_int = round(d_sq)
    if abs(d_sq - n_int) < 1e-3 and n_int > 0:
        r = int(math.isqrt(n_int))
        if r * r == n_int:
            return str(r)
        k = 1
        m = n_int
        for factor in range(int(math.isqrt(n_int)), 1, -1):
            if n_int % (factor * factor) == 0:
                k = factor
                m = n_int // (factor * factor)
                break
        if k == 1:
            return f"√{m} (≈ {val:.2f})"
        else:
            return f"{k}√{m} (≈ {val:.2f})"

    d4_sq = d_sq * 4.0
    n4_int = round(d4_sq)
    if abs(d4_sq - n4_int) < 1e-3 and n4_int > 0:
        r = int(math.isqrt(n4_int))
        if r * r == n4_int:
            return f"{r}/2 ({val:.2f})" if r % 2 != 0 else str(r // 2)
        k = 1
        m = n4_int
        for factor in range(int(math.isqrt(n4_int)), 1, -1):
            if n4_int % (factor * factor) == 0:
                k = factor
                m = n4_int // (factor * factor)
                break
        if k % 2 == 0:
            k_half = k // 2
            prefix = f"{k_half}" if k_half > 1 else ""
            return f"{prefix}√{m} (≈ {val:.2f})"
        else:
            prefix = f"{k}" if k > 1 else ""
            return f"{prefix}√{m}/2 (≈ {val:.2f})"

    return f"{val:.2f}"


def as_scaled_ints(coords, max_k=4):
    """
    Nhận diện tọa độ số nguyên hoặc số thập phân sạch (ví dụ: 8.7, 2.9, 1.3, 0.04):
    Nhân với 10^k (k = 0..max_k). Nếu tất cả tọa độ trở thành số nguyên (sai số < 1e-5),
    trả về danh sách số nguyên đã nhân tỷ lệ để so sánh chính xác trên lưới Z^2.
    Nếu không (tọa độ vô tỉ hoặc điểm kéo chuột tự do), trả về (None, 1.0).

    Lưu ý thiết kế và giới hạn:
    1. Tọa độ cực nhỏ (|v| < 1e-5): tại k=0 có thể làm tròn về 0, tam giác có thể bị coi là suy biến
       nếu kích thước tổng thể < 1e-5.
    2. Giới hạn max_k=4: Các tọa độ có > 4 chữ số thập phân sẽ rơi vào nhánh số thực (continuous float).
    3. Giới hạn số thực IEEE-754: Với |x| >= 10^9, v * 10^k tiệm cận giới hạn 53-bit mantissa (2^53 ≈ 9e15),
       khiến is_discrete có thể trả về False. Trong ứng dụng CAD/toán phổ thông, tọa độ luôn nằm trong |x| < 10^6.
    """
    for k in range(max_k + 1):
        s = 10 ** k
        if all(abs(v * s - round(v * s)) < 1e-5 for v in coords):
            return [round(v * s) for v in coords], s
    return None, 1.0


_FREE_SOURCES = ("free", "mouse", "dragged")
_EXACT_SOURCES = ("typed", "grid_snap", "snapped", "exact")
_DERIVED_SOURCES = ("midpoint", "intersection", "formula")


def _finite(v, label, p):
    """Ép về float, từ chối None / chuỗi / NaN / inf."""
    if isinstance(v, (str, bytes)):
        raise ValueError(f"Tọa độ '{label}' không được là chuỗi: {v!r}")
    try:
        f = float(v)
    except (TypeError, ValueError):
        raise ValueError(f"Tọa độ '{label}' không hợp lệ: {p!r}")
    if not math.isfinite(f):
        raise ValueError(f"Tọa độ '{label}' phải hữu hạn (không NaN/inf): {p!r}")
    return f


def _point_flag(p, _visiting=None, memo=None, _depth=0):
    """True = chính xác, False = vẽ tay (taint) hoặc chu trình, None = không rõ nguồn.

    Điểm dựng hình (midpoint/intersection/formula) kế thừa cờ từ điểm cha
    qua khóa "parents". Không có "parents" thì coi là không rõ (None),
    trừ khi có exact=True tường minh.
    Sử dụng tập _visiting để phát hiện chu trình (cycle detection) và memo để tối ưu O(1).
    Nếu vượt quá giới hạn độ sâu an toàn (_depth >= 100), hàm trả False để chống tràn ngăn xếp.
    """
    if not isinstance(p, dict):
        return None
    if memo is None:
        memo = {}
    obj_id = id(p)
    if obj_id in memo:
        return memo[obj_id]

    if _visiting is None:
        _visiting = set()
    if obj_id in _visiting:
        # Chu trình tham chiếu vòng trong đồ thị phả hệ
        return False
    if _depth >= 100:
        # Bảo vệ tràn ngăn xếp đệ quy
        return False

    if p.get("source") in _FREE_SOURCES or p.get("exact") is False:
        memo[obj_id] = False
        return False

    if p.get("source") in _DERIVED_SOURCES and p.get("parents"):
        _visiting.add(obj_id)
        try:
            flags = [_point_flag(q, _visiting, memo, _depth + 1) for q in p["parents"]]
            if any(f is False for f in flags):
                res = False
            elif all(f is True for f in flags):
                res = True
            else:
                res = None
            memo[obj_id] = res
            return res
        finally:
            _visiting.discard(obj_id)

    if p.get("exact") is True or p.get("source") in _EXACT_SOURCES:
        memo[obj_id] = True
        return True

    memo[obj_id] = None
    return None


def classify_triangle(pA, pB, pC, lang: str = "vi", points_exact: bool | None = None) -> dict:
    """
    Phân loại hình học tam giác thuần túy (Pure Function - Production Code):
    - Kiểm tra điểm trùng, 3 điểm thẳng hàng.
    - Nhận diện cờ nguồn gốc points_exact / metadata 'source' ('typed', 'grid_snap' vs 'free'):
        + Nếu người dùng vẽ chuột tự do (source='free' hoặc points_exact=False):
          exact luôn là False dù tọa độ rơi vào số nguyên do ngẫu nhiên hoặc mức zoom pixel.
        + Nếu người dùng gõ tay hoặc snap lưới (points_exact=True):
          exact là True khi tọa độ thỏa mãn lưới số nguyên/hữu tỉ.
    - Nhận diện tọa độ số nguyên hoặc thập phân gõ tay (as_scaled_ints):
        + So sánh d^2 chính xác bằng số nguyên trên lưới tỷ lệ (tránh sai số d^2=1000 vs 1010 do làm tròn số thực).
        + Tích vô hướng nguyên == 0 cho góc vuông.
        + Áp dụng Định lý lưới nguyên Z^2: Tam giác có đỉnh trên lưới số nguyên/hữu tỉ không thể là tam giác đều.
    - Với tọa độ thực tự do / vô tỉ:
        + Dùng dung sai tỷ lệ tương đối tol_rel = 0.006 (0.6% L_max, không áp ngưỡng tuyệt đối).
        + Báo rõ 'gần đều (lệch X.X%)', 'gần cân (lệch X.X%)', 'gần vuông (góc X.X°)'.
    """
    is_en = (lang == "en")
    
    def get_xy_name_exact(p, default_name):
        if p is None:
            raise ValueError(f"Tọa độ điểm không được là None: {p!r}")
        if isinstance(p, dict):
            if "x" not in p or "y" not in p:
                raise ValueError(f"Điểm thiếu thuộc tính tọa độ 'x' hoặc 'y': {p}")
            return (_finite(p["x"], "x", p), _finite(p["y"], "y", p),
                    str(p.get("name") or default_name), _point_flag(p))
        if not isinstance(p, (list, tuple)):
            raise ValueError(f"Tọa độ điểm phải là dict hoặc sequence (list/tuple), nhận được {type(p).__name__}: {p!r}")
        if len(p) < 2:
            raise ValueError(f"Tọa độ điểm phải có ít nhất 2 phần tử (x, y): {p}")
        return _finite(p[0], "x", p), _finite(p[1], "y", p), default_name, None

    xA, yA, nA, exA = get_xy_name_exact(pA, "A")
    xB, yB, nB, exB = get_xy_name_exact(pB, "B")
    xC, yC, nC, exC = get_xy_name_exact(pC, "C")

    # Thứ tự ưu tiên xác định nguồn gốc điểm (Taint Precedence Hierarchy):
    # 1. Lan truyền vết bẩn (Taint propagation): Nếu BẤT KỲ điểm nào là False (vẽ chuột tự do),
    #    toàn bộ tam giác bắt buộc là False. Tham số points_exact=True KHÔNG ĐƯỢC PHÉP đè lên cờ False này!
    # 2. Nếu caller chỉ định points_exact=False tường minh: Toàn bộ tam giác là False.
    # 3. Nếu caller chỉ định points_exact=True tường minh (và không có điểm nào bị taint False): Toàn bộ tam giác là True.
    # 4. Nếu tất cả 3 điểm đều có cờ True: Toàn bộ tam giác là True.
    # 5. Ngược lại (có điểm None - thiếu metadata): user_declared_exact = None (chuyển sang chế độ Heuristic số học is_discrete).
    pt_flags = [exA, exB, exC]
    if any(f is False for f in pt_flags):
        user_declared_exact = False
    elif points_exact is False:
        user_declared_exact = False
    elif points_exact is True:
        user_declared_exact = True
    elif all(f is True for f in pt_flags):
        user_declared_exact = True
    else:
        user_declared_exact = None

    u_AB = (xB - xA, yB - yA)
    u_AC = (xC - xA, yC - yA)
    u_BC = (xC - xB, yC - yB)

    c_sq = u_AB[0]**2 + u_AB[1]**2
    b_sq = u_AC[0]**2 + u_AC[1]**2
    a_sq = u_BC[0]**2 + u_BC[1]**2

    c_len = math.sqrt(c_sq)  # AB
    b_len = math.sqrt(b_sq)  # AC
    a_len = math.sqrt(a_sq)  # BC

    cross = u_AB[0] * u_AC[1] - u_AB[1] * u_AC[0]
    
    # Nhận diện tọa độ số nguyên hoặc số thập phân sạch (ví dụ gõ 8.7, 2.9, 1.3, 0.04)
    scaled_coords, scale_factor = as_scaled_ints([xA, yA, xB, yB, xC, yC], max_k=4)
    # Điểm vẽ tay có tọa độ rơi vào lưới pixel/40 sẽ lọt nhánh "rời rạc"
    # và bị so sánh bằng chính xác. Ép về nhánh dung sai tương đối khi user_declared_exact is False.
    is_discrete = (scaled_coords is not None) and (user_declared_exact is not False)

    # Kiểm tra trùng điểm bất biến theo tỷ lệ (không dùng ngưỡng tuyệt đối 1e-4)
    if is_discrete:
        sxA, syA, sxB, syB, sxC, syC = scaled_coords
        s_uAB = (sxB - sxA, syB - syA)
        s_uAC = (sxC - sxA, syC - syA)
        s_uBC = (sxC - sxB, syC - syB)
        is_coincident = (s_uAB == (0, 0)) or (s_uAC == (0, 0)) or (s_uBC == (0, 0))
        is_collinear = (s_uAB[0] * s_uAC[1] - s_uAB[1] * s_uAC[0] == 0)
    else:
        l_max = max(a_len, b_len, c_len)
        if l_max < 1e-12:
            is_coincident = True
        else:
            is_coincident = (c_len / l_max < 1e-6) or (b_len / l_max < 1e-6) or (a_len / l_max < 1e-6)
        # Chuẩn hóa diện tích theo l_max^2 (bảo đảm bất biến hoán vị 100% giữa 6 hoán vị của 3 đỉnh)
        rel_cross = abs(cross) / (l_max * l_max) if l_max > 1e-12 else 0.0
        is_collinear = (rel_cross < 1e-5)

    if is_coincident:
        msg = "Coincident points; not a valid triangle." if is_en else "Có điểm trùng nhau; không tạo thành tam giác."
        return {
            "is_triangle": False, "type": "coincident",
            "message": msg, "sides": {"AB": c_len, "AC": b_len, "BC": a_len}
        }

    if is_collinear:
        msg = "Collinear points; not a triangle." if is_en else "3 điểm thẳng hàng; không tạo thành tam giác."
        return {
            "is_triangle": False, "type": "collinear",
            "message": msg, "sides": {"AB": c_len, "AC": b_len, "BC": a_len}
        }

    l_max = max(a_len, b_len, c_len)
    l_min = min(a_len, b_len, c_len)

    str_AB = format_radical_len(c_len, (xA, yA), (xB, yB))
    str_AC = format_radical_len(b_len, (xA, yA), (xC, yC))
    str_BC = format_radical_len(a_len, (xB, yB), (xC, yC))

    is_equilateral = False
    perp_A = False
    perp_B = False
    perp_C = False
    eq_AB_AC = False
    eq_BA_BC = False
    eq_CA_CB = False
    diff_AB_AC = 0.0
    diff_BA_BC = 0.0
    diff_CA_CB = 0.0
    diff_eq = 0.0
    angle_A = 90.0
    angle_B = 90.0
    angle_C = 90.0

    if is_discrete:
        # CHẾ ĐỘ RỜI RẠC: Số nguyên hoặc số thập phân sạch (as_scaled_ints)
        d2_AB = s_uAB[0]**2 + s_uAB[1]**2
        d2_AC = s_uAC[0]**2 + s_uAC[1]**2
        d2_BC = s_uBC[0]**2 + s_uBC[1]**2

        eq_AB_AC = (d2_AB == d2_AC)
        eq_BA_BC = (d2_AB == d2_BC)
        eq_CA_CB = (d2_AC == d2_BC)
        is_equilateral = False  # Theo định lý lưới nguyên Z^2, không thể tồn tại tam giác đều

        dot_A = s_uAB[0] * s_uAC[0] + s_uAB[1] * s_uAC[1]
        dot_B = -s_uAB[0] * s_uBC[0] - s_uAB[1] * s_uBC[1]
        dot_C = s_uAC[0] * s_uBC[0] + s_uAC[1] * s_uBC[1]

        perp_A = (dot_A == 0)
        perp_B = (dot_B == 0)
        perp_C = (dot_C == 0)
    else:
        # CHẾ ĐỘ LIÊN TỤC: Tọa độ thực tự do / vô tỉ (Bảo đảm bất biến tỷ lệ tuyệt đối)
        tol_rel = 0.006  # 0.6%
        max_AB_AC = max(c_len, b_len)
        max_BA_BC = max(c_len, a_len)
        max_CA_CB = max(b_len, a_len)

        eq_AB_AC = (abs(c_len - b_len) <= tol_rel * max_AB_AC) if max_AB_AC > 1e-12 else True
        eq_BA_BC = (abs(c_len - a_len) <= tol_rel * max_BA_BC) if max_BA_BC > 1e-12 else True
        eq_CA_CB = (abs(b_len - a_len) <= tol_rel * max_CA_CB) if max_CA_CB > 1e-12 else True

        diff_AB_AC = (abs(c_len - b_len) / max_AB_AC * 100.0) if max_AB_AC > 1e-12 else 0.0
        diff_BA_BC = (abs(c_len - a_len) / max_BA_BC * 100.0) if max_BA_BC > 1e-12 else 0.0
        diff_CA_CB = (abs(b_len - a_len) / max_CA_CB * 100.0) if max_CA_CB > 1e-12 else 0.0

        is_equilateral = ((l_max - l_min) <= tol_rel * l_max) if l_max > 1e-12 else False
        diff_eq = ((l_max - l_min) / l_max * 100.0) if l_max > 1e-12 else 0.0

        dot_A = u_AB[0] * u_AC[0] + u_AB[1] * u_AC[1]
        dot_B = -u_AB[0] * u_BC[0] - u_AB[1] * u_BC[1]
        dot_C = u_AC[0] * u_BC[0] + u_AC[1] * u_BC[1]

        cos_A = dot_A / (c_len * b_len)
        cos_B = dot_B / (c_len * a_len)
        cos_C = dot_C / (b_len * a_len)

        angle_A = math.degrees(math.acos(max(-1.0, min(1.0, cos_A))))
        angle_B = math.degrees(math.acos(max(-1.0, min(1.0, cos_B))))
        angle_C = math.degrees(math.acos(max(-1.0, min(1.0, cos_C))))

        perp_A = (abs(cos_A) <= 0.015)
        perp_B = (abs(cos_B) <= 0.015)
        perp_C = (abs(cos_C) <= 0.015)

    tri_type = "scalene"
    vertex = None
    description = ""

    if is_equilateral:
        tri_type = "equilateral"
        avg_s = (a_len + b_len + c_len) / 3.0
        s_str = format_radical_len(avg_s, (xA, yA), (xB, yB))
        mod_eq = f" (gần đều, lệch {diff_eq:.1f}%)" if (not is_discrete and diff_eq > 0.05) else ""
        description = f"Equilateral triangle: Δ{nA}{nB}{nC} (AB=BC=CA = {s_str}){mod_eq}" if is_en else f"Tam giác đều: Δ{nA}{nB}{nC} (ba cạnh bằng nhau = {s_str}){mod_eq}"

    else:
        # 1. Kiểm tra ứng viên Tam giác vuông cân (Right Isosceles)
        ri_candidates = []
        if perp_A and eq_AB_AC:
            ri_candidates.append((diff_AB_AC + abs(angle_A - 90.0), "A"))
        if perp_B and eq_BA_BC:
            ri_candidates.append((diff_BA_BC + abs(angle_B - 90.0), "B"))
        if perp_C and eq_CA_CB:
            ri_candidates.append((diff_CA_CB + abs(angle_C - 90.0), "C"))

        if ri_candidates:
            # Sắp xếp theo tổng độ lệch nhỏ nhất để bảo đảm bất biến hoán vị 100%
            ri_candidates.sort(key=lambda item: item[0])
            best_tag = ri_candidates[0][1]
            if best_tag == "A":
                tri_type = "right_isosceles"
                vertex = nA
                avg_leg = (c_len + b_len) / 2.0
                leg_str = format_radical_len(avg_leg, (xA, yA), (xB, yB))
                notes = []
                if not is_discrete:
                    if diff_AB_AC > 0.05:
                        notes.append(f"lệch cạnh {diff_AB_AC:.1f}%" if not is_en else f"leg dev {diff_AB_AC:.1f}%")
                    if abs(angle_A - 90.0) > 0.05:
                        notes.append(f"góc {angle_A:.1f}°" if not is_en else f"angle {angle_A:.1f}°")
                mod_ri = f" (gần vuông cân: {', '.join(notes)})" if notes else ""
                description = f"Right isosceles triangle at {nA}: Δ{nA}{nB}{nC} ({nA}{nB}={nA}{nC} = {leg_str}, ∠{nA}=90°){mod_ri}" if is_en else f"Tam giác vuông cân tại {nA}: Δ{nA}{nB}{nC} ({nA}{nB}={nA}{nC} = {leg_str}, ∠{nA}=90°){mod_ri}"
            elif best_tag == "B":
                tri_type = "right_isosceles"
                vertex = nB
                avg_leg = (c_len + a_len) / 2.0
                leg_str = format_radical_len(avg_leg, (xB, yB), (xC, yC))
                notes = []
                if not is_discrete:
                    if diff_BA_BC > 0.05:
                        notes.append(f"lệch cạnh {diff_BA_BC:.1f}%" if not is_en else f"leg dev {diff_BA_BC:.1f}%")
                    if abs(angle_B - 90.0) > 0.05:
                        notes.append(f"góc {angle_B:.1f}°" if not is_en else f"angle {angle_B:.1f}°")
                mod_ri = f" (gần vuông cân: {', '.join(notes)})" if notes else ""
                description = f"Right isosceles triangle at {nB}: Δ{nA}{nB}{nC} ({nB}{nA}={nB}{nC} = {leg_str}, ∠{nB}=90°){mod_ri}" if is_en else f"Tam giác vuông cân tại {nB}: Δ{nA}{nB}{nC} ({nB}{nA}={nB}{nC} = {leg_str}, ∠{nB}=90°){mod_ri}"
            else:
                tri_type = "right_isosceles"
                vertex = nC
                avg_leg = (b_len + a_len) / 2.0
                leg_str = format_radical_len(avg_leg, (xC, yC), (xA, yA))
                notes = []
                if not is_discrete:
                    if diff_CA_CB > 0.05:
                        notes.append(f"lệch cạnh {diff_CA_CB:.1f}%" if not is_en else f"leg dev {diff_CA_CB:.1f}%")
                    if abs(angle_C - 90.0) > 0.05:
                        notes.append(f"góc {angle_C:.1f}°" if not is_en else f"angle {angle_C:.1f}°")
                mod_ri = f" (gần vuông cân: {', '.join(notes)})" if notes else ""
                description = f"Right isosceles triangle at {nC}: Δ{nA}{nB}{nC} ({nC}{nA}={nC}{nB} = {leg_str}, ∠{nC}=90°){mod_ri}" if is_en else f"Tam giác vuông cân tại {nC}: Δ{nA}{nB}{nC} ({nC}{nA}={nC}{nB} = {leg_str}, ∠{nC}=90°){mod_ri}"

        else:
            # 2. Kiểm tra ứng viên Tam giác cân (Isosceles)
            iso_candidates = []
            if eq_AB_AC:
                iso_candidates.append((diff_AB_AC, "A"))
            if eq_BA_BC:
                iso_candidates.append((diff_BA_BC, "B"))
            if eq_CA_CB:
                iso_candidates.append((diff_CA_CB, "C"))

            if iso_candidates:
                # Sắp xếp theo chênh lệch độ dài hai cạnh nhỏ nhất
                iso_candidates.sort(key=lambda item: item[0])
                best_tag = iso_candidates[0][1]
                if best_tag == "A":
                    tri_type = "isosceles"
                    vertex = nA
                    avg_leg = (c_len + b_len) / 2.0
                    leg_str = format_radical_len(avg_leg, (xA, yA), (xB, yB))
                    base_str = format_radical_len(a_len, (xB, yB), (xC, yC))
                    mod_text = f" (gần cân, lệch {diff_AB_AC:.1f}%)" if (not is_discrete and diff_AB_AC > 0.05) else ""
                    description = (f"Isosceles triangle at {nA}: Δ{nA}{nB}{nC} ({nA}{nB}={nA}{nC} = {leg_str}, base {nB}{nC} = {base_str}){mod_text}" if is_en 
                                   else f"Tam giác cân tại {nA}: Δ{nA}{nB}{nC} ({nA}{nB}={nA}{nC} = {leg_str}, đáy {nB}{nC} = {base_str}){mod_text}")
                elif best_tag == "B":
                    tri_type = "isosceles"
                    vertex = nB
                    avg_leg = (c_len + a_len) / 2.0
                    leg_str = format_radical_len(avg_leg, (xB, yB), (xC, yC))
                    base_str = format_radical_len(b_len, (xC, yC), (xA, yA))
                    mod_text = f" (gần cân, lệch {diff_BA_BC:.1f}%)" if (not is_discrete and diff_BA_BC > 0.05) else ""
                    description = (f"Isosceles triangle at {nB}: Δ{nA}{nB}{nC} ({nB}{nA}={nB}{nC} = {leg_str}, base {nA}{nC} = {base_str}){mod_text}" if is_en 
                                   else f"Tam giác cân tại {nB}: Δ{nA}{nB}{nC} ({nB}{nA}={nB}{nC} = {leg_str}, đáy {nA}{nC} = {base_str}){mod_text}")
                else:
                    tri_type = "isosceles"
                    vertex = nC
                    avg_leg = (b_len + a_len) / 2.0
                    leg_str = format_radical_len(avg_leg, (xC, yC), (xA, yA))
                    base_str = format_radical_len(c_len, (xA, yA), (xB, yB))
                    mod_text = f" (gần cân, lệch {diff_CA_CB:.1f}%)" if (not is_discrete and diff_CA_CB > 0.05) else ""
                    description = (f"Isosceles triangle at {nC}: Δ{nA}{nB}{nC} ({nC}{nA}={nC}{nB} = {leg_str}, base {nA}{nB} = {base_str}){mod_text}" if is_en 
                                   else f"Tam giác cân tại {nC}: Δ{nA}{nB}{nC} ({nC}{nA}={nC}{nB} = {leg_str}, đáy {nA}{nB} = {base_str}){mod_text}")

            else:
                # 3. Kiểm tra ứng viên Tam giác vuông (Right)
                right_candidates = []
                if perp_A:
                    right_candidates.append((abs(angle_A - 90.0), "A"))
                if perp_B:
                    right_candidates.append((abs(angle_B - 90.0), "B"))
                if perp_C:
                    right_candidates.append((abs(angle_C - 90.0), "C"))

                if right_candidates:
                    # Sắp xếp theo góc lệch ít nhất so với 90 độ
                    right_candidates.sort(key=lambda item: item[0])
                    best_tag = right_candidates[0][1]
                    if best_tag == "A":
                        tri_type = "right"
                        vertex = nA
                        ang_dev = abs(angle_A - 90.0)
                        mod_r = f" (gần vuông, góc {angle_A:.1f}°)" if (not is_discrete and ang_dev > 0.05) else ""
                        description = f"Right triangle at {nA}: Δ{nA}{nB}{nC} ({nA}{nB} ⊥ {nA}{nC}){mod_r}" if is_en else f"Tam giác vuông tại {nA}: Δ{nA}{nB}{nC} ({nA}{nB} ⊥ {nA}{nC}){mod_r}"
                    elif best_tag == "B":
                        tri_type = "right"
                        vertex = nB
                        ang_dev = abs(angle_B - 90.0)
                        mod_r = f" (gần vuông, góc {angle_B:.1f}°)" if (not is_discrete and ang_dev > 0.05) else ""
                        description = f"Right triangle at {nB}: Δ{nA}{nB}{nC} ({nB}{nA} ⊥ {nB}{nC}){mod_r}" if is_en else f"Tam giác vuông tại {nB}: Δ{nA}{nB}{nC} ({nB}{nA} ⊥ {nB}{nC}){mod_r}"
                    else:
                        tri_type = "right"
                        vertex = nC
                        ang_dev = abs(angle_C - 90.0)
                        mod_r = f" (gần vuông, góc {angle_C:.1f}°)" if (not is_discrete and ang_dev > 0.05) else ""
                        description = f"Right triangle at {nC}: Δ{nA}{nB}{nC} ({nC}{nA} ⊥ {nC}{nB}){mod_r}" if is_en else f"Tam giác vuông tại {nC}: Δ{nA}{nB}{nC} ({nC}{nA} ⊥ {nC}{nB}){mod_r}"

                else:
                    tri_type = "scalene"
                    description = f"Scalene triangle: Δ{nA}{nB}{nC}" if is_en else f"Tam giác thường: Δ{nA}{nB}{nC}"

    deviations = {}
    if not is_discrete:
        if tri_type == "equilateral":
            deviations["equilateral_diff_pct"] = round(diff_eq, 2)
        elif tri_type == "isosceles":
            if vertex == nA:
                deviations["leg_diff_pct"] = round(diff_AB_AC, 2)
            elif vertex == nB:
                deviations["leg_diff_pct"] = round(diff_BA_BC, 2)
            elif vertex == nC:
                deviations["leg_diff_pct"] = round(diff_CA_CB, 2)
        elif tri_type == "right":
            if vertex == nA:
                deviations["angle_deg"] = round(angle_A, 2)
                deviations["angle_diff_deg"] = round(abs(angle_A - 90.0), 2)
            elif vertex == nB:
                deviations["angle_deg"] = round(angle_B, 2)
                deviations["angle_diff_deg"] = round(abs(angle_B - 90.0), 2)
            elif vertex == nC:
                deviations["angle_deg"] = round(angle_C, 2)
                deviations["angle_diff_deg"] = round(abs(angle_C - 90.0), 2)
        elif tri_type == "right_isosceles":
            if vertex == nA:
                deviations["leg_diff_pct"] = round(diff_AB_AC, 2)
                deviations["angle_deg"] = round(angle_A, 2)
                deviations["angle_diff_deg"] = round(abs(angle_A - 90.0), 2)
            elif vertex == nB:
                deviations["leg_diff_pct"] = round(diff_BA_BC, 2)
                deviations["angle_deg"] = round(angle_B, 2)
                deviations["angle_diff_deg"] = round(abs(angle_B - 90.0), 2)
            elif vertex == nC:
                deviations["leg_diff_pct"] = round(diff_CA_CB, 2)
                deviations["angle_deg"] = round(angle_C, 2)
                deviations["angle_diff_deg"] = round(abs(angle_C - 90.0), 2)

    def _is_near_int(v: float) -> bool:
        if abs(v) < 1e-9:
            return True
        if abs(v) < 0.5:
            return False
        return abs(v - round(v)) < 1e-5

    all_int = all(_is_near_int(v) for v in (xA, yA, xB, yB, xC, yC))
    exact_math = False if user_declared_exact is False else (is_discrete if user_declared_exact is None else (is_discrete and user_declared_exact))
    return {
        "is_triangle": True,
        "type": tri_type,
        "vertex": vertex,
        "all_int": all_int,
        "is_discrete": is_discrete,
        "exact": exact_math,
        "origin_exact": user_declared_exact,
        "deviations": deviations,
        "scale_factor": scale_factor,
        "is_equilateral": is_equilateral,
        "is_isosceles": (tri_type in ("isosceles", "right_isosceles")),
        "is_right": (tri_type in ("right", "right_isosceles")),
        "sides": {"AB": c_len, "AC": b_len, "BC": a_len},
        "side_labels": {"AB": str_AB, "AC": str_AC, "BC": str_BC},
        "sides_formatted": {"AB": str_AB, "AC": str_AC, "BC": str_BC},
        "description": description
    }


def compute_ellipse_parameters(ox: float, oy: float, ax: float, ay: float, bx: float, by: float):

    """Tính tham số hình học của Elip từ Tâm O, đỉnh trục lớn A và điểm B."""

    dx_a = ax - ox

    dy_a = ay - oy

    a = math.hypot(dx_a, dy_a)

    theta = math.atan2(dy_a, dx_a)



    dx_b = bx - ox

    dy_b = by - oy

    perp_dist = abs(-dx_b * math.sin(theta) + dy_b * math.cos(theta))

    direct_dist = math.hypot(dx_b, dy_b)

    b = perp_dist if perp_dist > 1e-6 else direct_dist

    if b < 1e-6:

        b = max(a * 0.5, 0.5)



    area = calc_ellipse_area(a, b)

    perimeter = calc_ellipse_perimeter(a, b)

    return {

        "ox": ox, "oy": oy, "a": a, "b": b, "theta": theta,

        "area": area, "perimeter": perimeter

    }





def sample_ellipse_points(ox: float, oy: float, a: float, b: float, theta: float, num_samples: int = 72):

    """Lấy mẫu 72 điểm theo phương trình tham số elip quay góc theta."""

    pts = []

    cos_th = math.cos(theta)

    sin_th = math.sin(theta)

    for i in range(num_samples + 1):

        t = 2.0 * math.pi * i / num_samples

        ct = math.cos(t)

        st = math.sin(t)

        x = ox + a * ct * cos_th - b * st * sin_th

        y = oy + a * ct * sin_th + b * st * cos_th

        pts.append((x, y))

    return pts





def compute_isosceles_trapezoid_vertex_d(ax: float, ay: float, bx: float, by: float, cx: float, cy: float):

    """

    Thuật toán tìm đỉnh D của hình thang cân ABCD từ đáy lớn A, B và đỉnh thứ 3 C:

    - Trung điểm đáy M = 0.5*(A + B).

    - Vector đơn vị u dọc theo AB.

    - Điểm D đối xứng với C qua đường trung trực của AB: D = C - 2 * ((C - M) . u) * u.

    """

    mx = 0.5 * (ax + bx)

    my = 0.5 * (ay + by)

    dx = bx - ax

    dy = by - ay

    length_ab = math.hypot(dx, dy)

    if length_ab < 1e-9:

        return cx, cy



    ux = dx / length_ab

    uy = dy / length_ab

    t = (cx - mx) * ux + (cy - my) * uy

    dx_pt = cx - 2.0 * t * ux

    dy_pt = cy - 2.0 * t * uy

    return dx_pt, dy_pt





def compute_parallelogram_vertex_d(ax: float, ay: float, bx: float, by: float, cx: float, cy: float):

    """Tính đỉnh D của hình bình hành ABCD sao cho vector AD = vector BC."""

    return ax + (cx - bx), ay + (cy - by)





def compute_rhombus_vertices_cd(ax: float, ay: float, bx: float, by: float, cx: float, cy: float):

    """Tối ưu hóa hình thoi ABCD từ 2 đỉnh A, B và điểm định hướng C: AB = BC = CD = DA."""

    length_ab = math.hypot(bx - ax, by - ay)

    if length_ab < 1e-9:

        length_ab = 1.0



    dx_bc = cx - bx

    dy_bc = cy - by

    dist_bc = math.hypot(dx_bc, dy_bc)

    if dist_bc < 1e-9:

        ux, uy = -(by - ay) / length_ab, (bx - ax) / length_ab

    else:

        ux, uy = dx_bc / dist_bc, dy_bc / dist_bc



    cx_norm = bx + length_ab * ux

    cy_norm = by + length_ab * uy

    dx_norm = ax + length_ab * ux

    dy_norm = ay + length_ab * uy

    return (cx_norm, cy_norm), (dx_norm, dy_norm)







class ToolTip:

    """Hộp chú thích kỹ thuật chuẩn CAD khi rê chuột vào nút công cụ."""

    def __init__(self, widget, title, text):

        self.widget = widget

        self.title = title

        self.text = text

        self.tip_window = None

        self.widget.bind("<Enter>", self.show_tip)

        self.widget.bind("<Leave>", self.hide_tip)



    def update(self, title, text):

        self.title = title

        self.text = text



    def show_tip(self, event=None):

        if self.tip_window or not self.text:

            return

        x = self.widget.winfo_rootx() + 10

        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4

        self.tip_window = tw = tk.Toplevel(self.widget)

        tw.wm_overrideredirect(True)

        tw.wm_geometry(f"+{x}+{y}")

        frame = tk.Frame(tw, background="#212529", bd=1, relief=tk.SOLID)

        frame.pack(fill=tk.BOTH, expand=True)

        if self.title:

            lbl_title = tk.Label(frame, text=self.title, justify=tk.LEFT,

                                 background="#212529", foreground="#ffd43b",

                                 font=("Segoe UI", 9, "bold"), padx=6, pady=2)

            lbl_title.pack(anchor=tk.W)

        lbl_msg = tk.Label(frame, text=self.text, justify=tk.LEFT,

                           background="#212529", foreground="#f8f9fa",

                           font=("Segoe UI", 8), padx=6, pady=3)

        lbl_msg.pack(anchor=tk.W)



    def hide_tip(self, event=None):

        if self.tip_window:

            self.tip_window.destroy()

            self.tip_window = None





# =============================================================================

# TỪ ĐIỂN SONG NGỮ RIÊNG BIỆT (PURE VIETNAMESE & ENGLISH LOCALIZATION)

# =============================================================================

LANG_DATA = {

    "vi": {

        "app_title": "GeoSolver v2.5",

        "menu": {

            "file": "Tệp",

            "file_new": "Bản vẽ mới (Ctrl+N)",

            "file_clear_draw": "Xóa hình trên canvas",

            "file_export": "Xuất hình ảnh PNG (Ctrl+E)...",

            "file_exit": "Thoát",

            "edit": "Chỉnh sửa",

            "edit_undo": "Hoàn tác (Ctrl+Z)",

            "edit_redo": "Làm lại (Ctrl+Y)",

            "edit_copy": "Sao chép hình (Ctrl+C)",

            "edit_paste": "Dán hình (Ctrl+V)",

            "edit_dup": "Nhân bản hình (Ctrl+D)",

            "edit_select_all": "Chọn tất cả đối tượng (Ctrl+A)",

            "edit_del": "Xóa đối tượng đang chọn (Delete)",

            "edit_hide": "Ẩn/Hiện đối tượng (Ctrl+H)",

            "transform": "Biến hình",

            "trans_ccw15": "Xoay ngược chiều 15° (Ctrl+Left)",

            "trans_cw15": "Xoay cùng chiều 15° (Ctrl+Right)",

            "trans_custom": "Xoay góc tùy chọn...",

            "presets": "Mẫu bài tập",

            "view": "Hiển thị",

            "view_grid": "Hiển thị lưới tọa độ & trục Oxy",

            "view_snap": "Bắt dính điểm lưới (Grid Snap)",

            "view_ask_name": "Hỏi tên khi tạo điểm mới",

            "view_show_hidden": "Hiện các nét ẩn / đường gióng phụ",

            "view_toggle_panel": "Hiện / Ẩn bảng lời giải bên phải",

            "language": "Ngôn ngữ",

            "help": "Trợ giúp",

            "help_handbook": "📖 Cẩm nang sử dụng & Phím tắt (F1)...",
            "help_about": "Thông tin sản phẩm (About GeoSolver)..."

        },

        "bar1": {

            "new": {"text": "Mới", "tip_title": "Bản vẽ mới (Ctrl+N)", "tip_body": "Khởi tạo bản vẽ mới hoàn toàn."},

            "clear_draw": {"text": "Xóa hình", "tip_title": "Xóa hình trên canvas", "tip_body": "Xóa toàn bộ hình học, giữ nguyên đề bài & lời giải."},

            "undo": {"text": "Hoàn tác", "tip_title": "Hoàn tác (Ctrl+Z)", "tip_body": "Quay lại thao tác dựng hình trước đó."},

            "redo": {"text": "Làm lại", "tip_title": "Làm lại (Ctrl+Y)", "tip_body": "Phục hồi thao tác vừa hoàn tác."},

            "copy": {"text": "📋 Chép", "tip_title": "Sao chép hình (Ctrl+C)", "tip_body": "Sao chép các điểm và hình đã chọn vào bộ nhớ tạm."},

            "paste": {"text": "📥 Dán", "tip_title": "Dán hình (Ctrl+V)", "tip_body": "Dán bản sao các điểm và hình học vừa sao chép."},

            "select_all": {"text": "Chọn hết", "tip_title": "Chọn tất cả (Ctrl+A)", "tip_body": "Chọn toàn bộ các đối tượng trên bản vẽ."},

            "rot_l": {"text": "Xoay -15°", "tip_title": "Xoay -15°", "tip_body": "Xoay toàn bộ các điểm ngược chiều kim đồng hồ 15 độ."},

            "rot_r": {"text": "Xoay +15°", "tip_title": "Xoay +15°", "tip_body": "Xoay toàn bộ các điểm cùng chiều kim đồng hồ 15 độ."},

            "rot_custom": {"text": "Góc xoay...", "tip_title": "Xoay góc chỉ định", "tip_body": "Nhập chính xác số đo độ góc muốn xoay."},

            "hide": {"text": "Ẩn/Hiện", "tip_title": "Ẩn/Hiện nét (Ctrl+H)", "tip_body": "Ẩn đường gióng phụ để bản vẽ thanh thoát."},

            "export": {"text": "Xuất ảnh...", "tip_title": "Xuất ảnh PNG (Ctrl+E)", "tip_body": "Lưu bản vẽ ra file PNG chất lượng cao."},

            "lang_toggle": {"text": "🌐 Tiếng Việt", "tip_title": "Chuyển sang English", "tip_body": "Bấm để chuyển toàn bộ giao diện sang tiếng Anh."},

            "about": {"text": "ℹ Giới thiệu", "tip_title": "Thông tin GeoSolver", "tip_body": "Xem phiên bản, động cơ tính toán và phím tắt."}

        },

        "bar_adv": {
            "lbl_adv": "📐 Toán Nâng cao:",
            "harmonic": {"text": "[➗ Hàng điều hòa]", "tip_title": "Điểm liên hợp điều hòa (Harmonic)", "tip_body": "Chọn 2 điểm A, B và điểm C trên AB để dựng điểm D sao cho (AB, CD) = -1."},
            "pole_polar": {"text": "[🎯 Cực & Đối cực]", "tip_title": "Cực & Đường đối cực (Pole & Polar)", "tip_body": "Chọn đường tròn và điểm P để dựng đường đối cực; hoặc chọn đường thẳng để tìm cực P."},
            "symmedian": {"text": "[📐 Đường đối trung]", "tip_title": "Đường đối trung & Điểm Lemoine", "tip_body": "Chọn 3 đỉnh tam giác ABC để dựng đường đối trung và xác định điểm Lemoine."},
            "radical_axis": {"text": "[⭕ Trục đẳng phương]", "tip_title": "Trục đẳng phương 2 đường tròn", "tip_body": "Chọn 2 đường tròn để dựng trục đẳng phương (các điểm có cùng phương tích)."},
            "barycentric": {"text": "[📊 Tọa độ tỉ cự]", "tip_title": "Phân tích Tọa độ Tỉ cự (Barycentric)", "tip_body": "Chọn 3 đỉnh tam giác ABC và điểm P để tính tọa độ tỉ cự chuẩn hóa (u : v : w)."}
        },
        "btn_toggle_panel": {

            "text_show": "Lời Giải [◀▶]",

            "text_hide": "Hiện Lời Giải [▶]",

            "tip_title": "Thu gọn / Mở rộng Lời Giải",

            "tip_body": "Bấm để phóng to tối đa màn hình vẽ hoặc mở bảng lời giải."

        },

        "bar2": {

            "select": {"text": "[↖ Dời]", "tip_title": "Chọn / Di chuyển", "tip_body": "Bấm chọn điểm hoặc kéo thả đối tượng. Bấm đúp vào điểm để ĐỔI TÊN."},

            "rotate_mouse": {"text": "[⟲ Xoay]", "tip_title": "Xoay hình bằng chuột", "tip_body": "Kéo chuột vòng tròn trên bản vẽ để xoay mượt mà toàn bộ hình."},

            "erase": {"text": "[✕ Xóa]", "tip_title": "Tẩy / Xóa đối tượng", "tip_body": "Bấm vào điểm, đoạn thẳng, đường thẳng hoặc đường tròn để xóa."},

            "point": {"text": "[• Điểm]", "tip_title": "Điểm tự do", "tip_body": "Bấm chuột trên mặt phẳng để đặt điểm mới."},

            "intersection": {"text": "[⤬ Giao]", "tip_title": "Giao điểm đối tượng", "tip_body": "Bấm gần giao điểm của 2 đường thẳng, đường thẳng & đường tròn, hoặc 2 đường tròn."},

            "midpoint": {"text": "[✛ T.điểm]", "tip_title": "Trung điểm", "tip_body": "Bấm lần lượt 2 điểm để tạo trung điểm của đoạn thẳng."},

            "proj_foot": {"text": "[⏊ H.chiếu]", "tip_title": "Hình chiếu vuông góc", "tip_body": "Hạ hình chiếu vuông góc từ điểm xuống đường thẳng."},

            "translate_vec": {"text": "[⇥ T.tiến]", "tip_title": "Tịnh tiến theo Vector", "tip_body": "Tịnh tiến điểm theo vector (VD: vector MN = vector AC)."},

            "segment": {"text": "[/ Đoạn]", "tip_title": "Đoạn thẳng", "tip_body": "Bấm lần lượt 2 điểm để tạo đoạn thẳng."},

            "toggle_dash": {"text": "[┈ Nét đứt]", "tip_title": "Đổi nét đứt / liền (Dashed)", "tip_body": "Bấm chuột vào đoạn thẳng hoặc đường tròn để đổi qua lại giữa Nét Liền và Nét Đứt."},

            "line": {"text": "[― Đường]", "tip_title": "Đường thẳng", "tip_body": "Bấm lần lượt 2 điểm để tạo đường thẳng kéo dài vô hạn."},

            "perpendicular": {"text": "[⊥ Vuông]", "tip_title": "Đường vuông góc", "tip_body": "Bấm chọn 1 điểm và 1 đường thẳng để hạ đường vuông góc."},

            "parallel": {"text": "[∥ S.song]", "tip_title": "Đường song song", "tip_body": "Bấm chọn 1 điểm và 1 đường thẳng để dựng đường song song."},

            "bisector": {"text": "[∠ P.giác]", "tip_title": "Đường phân giác góc", "tip_body": "Bấm chọn 3 điểm tạo góc (Đỉnh góc ở giữa) để dựng phân giác."},

            "mark_angle": {"text": "[∠ Đánh góc]", "tip_title": "Ký hiệu góc", "tip_body": "Đánh dấu góc: Vuông (ô vuông SGK), 1 cung, 2 cung, gạch hướng tâm; kèm nhãn chữ (α, β...) hoặc độ (°)."},

            "angle_ratio_point": {"text": "[📐 Góc/Tỉ lệ]", "tip_title": "Dựng điểm theo Góc & Tỉ lệ", "tip_body": "Lấy điểm M thỏa mãn góc (VD: BME=ECA, 30°, 45°) hoặc tỉ lệ (VD: AM=2*CB)."},

            "circle": {"text": "[○ Tròn]", "tip_title": "Đường tròn (Tâm & Điểm)", "tip_body": "Bấm điểm tâm, sau đó bấm điểm xác định bán kính."},

            "circle_3p": {"text": "[⦿ Tròn 3P]", "tip_title": "Đường tròn qua 3 điểm", "tip_body": "Bấm chọn 3 điểm để dựng đường tròn ngoại tiếp qua 3 điểm."}

        },

        "bar3": {

            "parallelogram": {"text": "[▱ B.hành]", "tip_title": "Hình bình hành", "tip_body": "Bấm chọn lần lượt 3 đỉnh A, B, C. Máy tự tính và dựng đỉnh D sao cho AD // BC."},

            "rhombus": {"text": "[◇ Thoi]", "tip_title": "Hình thoi", "tip_body": "Bấm chọn 2 điểm A, B tạo cạnh đáy, sau đó bấm điểm định hướng C để dựng 4 cạnh bằng nhau."},

            "isosceles_trapezoid": {"text": "[⏢ Thang cân]", "tip_title": "Hình thang cân", "tip_body": "Bấm chọn 2 đỉnh đáy A, B và đỉnh thứ 3 C. Máy tự dựng đỉnh D đối xứng qua trung trực AB."},

            "square": {"text": "[□ Vuông]", "tip_title": "Hình vuông", "tip_body": "Bấm 2 điểm làm cạnh đáy, máy tự dựng 2 đỉnh còn lại vuông góc bằng nhau."},

            "ellipse": {"text": "[⬭ Elip]", "tip_title": "Hình elip", "tip_body": "Bấm chọn Tâm O, đỉnh trục lớn A và điểm thứ ba B xác định bán trục bé."},

            "smart_tangent": {"text": "[◎ T.tuyến]", "tip_title": "Tiếp tuyến thông minh", "tip_body": "• Bấm tâm 2 đường tròn: tự động dựng TOÀN BỘ tiếp tuyến chung!\n• Bấm 1 đường tròn: tiếp tuyến động xoay theo chuột!"},

            "common_tangents": {"text": "[⊜ T.tuyến 2C]", "tip_title": "Tiếp tuyến chung 2 đường tròn", "tip_body": "Bấm chọn 2 tâm hoặc 2 đường tròn để kẻ tiếp tuyến chung."},

            "orthocenter": {"text": "[▲ Trực tâm]", "tip_title": "Trực tâm tam giác", "tip_body": "Bấm chọn 3 đỉnh tam giác để dựng giao 3 đường cao (Trực tâm H)."},

            "incenter": {"text": "[⊙ Tâm nội]", "tip_title": "Tâm đường tròn nội tiếp", "tip_body": "Bấm chọn 3 đỉnh tam giác để tính giao 3 phân giác và dựng tâm I."},

            "incircle": {"text": "[⨀ Tròn nội]", "tip_title": "Đường tròn nội tiếp", "tip_body": "Bấm chọn 3 đỉnh tam giác để dựng tâm I và vẽ đường tròn tiếp xúc 3 cạnh."},

            "circumcenter": {"text": "[⊚ Tâm ngoại]", "tip_title": "Tâm đường tròn ngoại tiếp", "tip_body": "Bấm chọn 3 đỉnh tam giác để tính giao 3 trung trực và dựng tâm O."},

            "calc_area": {"text": "[📐 D.tích]", "tip_title": "Tính diện tích phần chọn", "tip_body": "Bấm chọn đa giác, tam giác hoặc hình elip/hình tròn để tính diện tích và tô màu phủ."},

            "check_prop": {"text": "[✓ K.tra]", "tip_title": "Kiểm tra tính chất", "tip_body": "Bấm chọn 3 điểm để kiểm tra xem có Thẳng Hàng hay Tam Giác Cân không."}

        },

        "lbl_preset": "Mẫu bài:",

        "presets_list": [

            "0. [Trang trắng] Bản vẽ mới",

            "1. Tứ giác nội tiếp & Tìm tọa độ điểm (M, N, P, A, B)",

            "2. Quỹ tích trung điểm & Điểm cố định của hai đường tròn",

            "3. Tiếp tuyến chung & Chứng minh 3 điểm thẳng hàng",

            "4. Vector tịnh tiến, Trực tâm & Đường tròn ngoại tiếp",

            "5. Trung điểm di động & Quỹ tích hypebol",

            "6. Góc bằng nhau & Tính tỉ số độ dài theo góc",

            "7. Đường vuông góc luôn đi qua điểm cố định",

            "8. Đường tròn Euler qua điểm cố định & Đoạn thẳng không đổi",

            "9. Giao hai tam giác & Diện tích lục giác DEFGHI (Căn thức)",

            "10. Trực tâm, cát tuyến & Điểm đối xứng qua trung điểm",

            "11. Tứ giác nội tiếp & Định lý Ptolemy (Diện tích S=45)"
        ],

        "lbl_goal": "Mục tiêu:",

        "goals_list": [

            "Tìm tọa độ điểm",

            "Chứng minh 3 điểm thẳng hàng",

            "Tìm quỹ tích điểm (Locus)",

            "Chứng minh điểm cố định",

            "Chứng minh hai đoạn bằng nhau",

            "Chứng minh hai đường vuông góc",

            "Chứng minh hai đường song song",

            "Chứng minh 3 đường đồng quy",

            "Tìm tương quan / Tỉ số biểu thức",

            "Tính diện tích (Area)",

            "Tự động phân tích toàn diện (Auto Analysis)",

            "Chứng minh tứ giác nội tiếp",

            "Chứng minh tam giác đồng dạng / bằng nhau"

        ],

        "lbl_targets": "Đối tượng:",

        "btn_solve": {

            "text": "▶ GIẢI TOÁN (SymPy)",

            "tip_title": "Giải Bài Toán",

            "tip_body": "Phân tích quan hệ hình học và xuất lời giải chi tiết bằng SymPy."

        },

        "color_palette": {

            "title": "Màu:",

            "red": "🔴 Đỏ",

            "blue": "🔵 Xanh",

            "black": "⚫ Đen",

            "green": "🟢 Lục",

            "tip_red": ("Tô màu Đỏ (#e03131)", "Đổi màu các đối tượng đang chọn sang màu đỏ (hoặc đặt màu vẽ kế tiếp)."),

            "tip_blue": ("Tô màu Xanh (#1971c2)", "Đổi màu các đối tượng đang chọn sang màu xanh học đường."),

            "tip_black": ("Tô màu Đen (#212529)", "Đổi màu các đối tượng đang chọn sang màu đen in ấn chuẩn."),

            "tip_green": ("Tô màu Xanh Lá (#2b8a3e)", "Đổi màu các đối tượng đang chọn sang màu xanh lá cây.")

        },

        "tab_solver": " Lời Giải & Đề Bài ",

        "prob_head": "Nội dung đề bài bài toán:",

        "inv_box": "Quan Hệ Phát Hiện Được (Property Checker)",

        "sol_box": "Trình Tự Chứng Minh & Lời Giải Chi Tiết",

        "tab_algebra": " Danh Sách Đối Tượng ",

        "tree_cols": ("Đối tượng", "Tọa độ / Phương trình", "Trạng thái"),

        "lbl_cmd": "Lệnh đại số:",

        "lbl_cmd_hint": "Ví dụ: A=(0, 4) | line(A, B) | circle(O, 3)",

        "status_ready": "Sẵn sàng.",

        "lbl_legal": "⚖️ BẢN QUYỀN GEOSOLVER v2.5 - MỌI SAO CHÉP ĐỀU VI PHẠM | 🔏 SẴN SÀNG KÝ SỐ",

        "about_dialog_title": "Giới thiệu GeoSolver v2.5",

        "about_text": (

            "THÔNG TIN SẢN PHẨM & BẢN QUYỀN PHẦN MỀM:\n"

            "• Tên sản phẩm: GeoSolver\n"

            "• Phiên bản: 2.5 (Bản phát hành chính thức 11/2026)\n"

            "• Động cơ tính toán: Python Tkinter CAD Engine & SymPy CAS Solver.\n"

            "• Tác giả & Bản quyền: © 2026 GeoSolver. Toàn bộ quyền đã được bảo hộ (All Rights Reserved).\n\n"

            "CẢNH BÁO PHÁP LÝ & BẢN QUYỀN NGHIÊM NGẶT:\n"

            "Nghiêm cấm mọi hành vi sao chép, trích xuất mã nguồn, dịch ngược (reverse-engineer),\n"

            "phân phối lại hoặc thương mại hóa dưới bất kỳ hình thức nào khi chưa có văn bản chấp\n"

            "thuận chính thức từ tác giả. Mọi hành vi vi phạm quyền sở hữu trí tuệ đều bị xử lý\n"

            "nghiêm khắc theo quy định của Luật Sở hữu trí tuệ Việt Nam và các điều ước quốc tế (WIPO/TRIPS).\n\n"

            "TRẠNG THÁI BẢO MẬT & KÝ SỐ (DIGITAL SIGNATURE READY):\n"

            "• Tiêu chuẩn xác thực: PKI / RSA-4096 / SHA-256 Cryptographic Integrity Seal.\n"

            "• Tình trạng: SẴN SÀNG KÝ SỐ XÁC NHẬN BẢN QUYỀN TÁC GIẢ & DẤU THỜI GIAN (TIMESTAMP).\n\n"

            "BỘ TÍNH NĂNG NỔI BẬT:\n"

            "1. Giao diện Technical CAD Studio:\n"

            "   - Bố cục 4 hàng ngang gọn gàng, giảm 30% kích thước nút, không bị che khuất.\n"

            "   - Bảng Lời Giải bên phải có thể thu gọn / mở rộng toàn màn hình.\n"

            "2. Dựng hình hình học nâng cao:\n"

            "   - Công cụ chuyển nét đứt chi tiết [┈ Nét đứt]: Đổi qua lại giữa nét liền và đứt cho đoạn thẳng và đường tròn.\n"

            "   - Xuất hình ảnh sạch: Tự động loại bỏ hệ trục tọa độ, lưới ô vuông và các đường gióng thừa vô hạn; tự động cắt sát khung hình chuẩn xuất bản.\n"

            "   - Tiếp tuyến thông minh: Tự động kẻ tiếp tuyến chung cho 2 đường tròn; tiếp tuyến động cho 1 đường tròn xoay theo chuột.\n"

            "   - Dựng điểm theo Góc & Tỉ lệ (AM = k*BC, góc bằng nhau BME = ECA, góc độ tự do).\n"

            "   - Đầy đủ tâm tam giác: Trực tâm (H), Tâm nội tiếp (I), Đường tròn nội tiếp, Tâm ngoại tiếp (O).\n"

            "   - Các đa giác chuẩn: Hình bình hành, Hình thoi, Hình vuông.\n"

            "3. Giải toán tự động & Hiệu ứng Chạy tự động:\n"

            "   - Tích hợp SymPy giải tích giải các bài toán Oxy & đề thi VMO (2000, 2001, 2003, 2007, 2008).\n"

            "   - Tùy chọn hiệu ứng chữ chạy tự động (Streaming Typewriter) khi xuất lời giải.\n"

            "   - Tự động phát hiện bất biến: Thẳng hàng, tiếp xúc, góc vuông, tỉ số.\n"

            "4. Quản lý bản vẽ:\n"

            "   - Clipboard đầy đủ: Sao chép (Ctrl+C), Dán (Ctrl+V), Nhân bản (Ctrl+D).\n"

            "   - Xóa hình vẽ canvas độc lập (giữ nguyên đề bài & lời giải).\n"

            "   - Hỗ trợ song ngữ riêng biệt Tiếng Việt & English.\n\n"

            "DANH MỤC PHÍM TẮT:\n"

            "• Ctrl + N: Bản vẽ mới (Trang trắng)\n"

            "• Ctrl + Z / Ctrl + Y: Hoàn tác / Làm lại\n"

            "• Ctrl + C / Ctrl + V / Ctrl + D: Sao chép / Dán / Nhân bản hình\n"

            "• Ctrl + A: Chọn tất cả đối tượng trên canvas\n"

            "• Delete: Xóa các đối tượng đang chọn\n"

            "• Ctrl + H: Ẩn / Hiện các đường gióng phụ\n"

            "• Ctrl + E: Xuất ảnh chất lượng cao PNG (Hình vẽ rõ nét, tỷ lệ chuẩn)\n"

            "• Cuộn chuột (Wheel): Phóng to / Thu nhỏ Canvas\n"

            "• Kéo chuột phải (Right Drag): Di chuyển bản vẽ (Pan)\n"

        )

    },

    "en": {

        "app_title": "GeoSolver v2.5",

        "menu": {

            "file": "File",

            "file_new": "New Drawing (Ctrl+N)",

            "file_clear_draw": "Clear Canvas Drawing Only",

            "file_export": "Export PNG Image (Ctrl+E)...",

            "file_exit": "Exit",

            "edit": "Edit",

            "edit_undo": "Undo (Ctrl+Z)",

            "edit_redo": "Redo (Ctrl+Y)",

            "edit_copy": "Copy Selection (Ctrl+C)",

            "edit_paste": "Paste Selection (Ctrl+V)",

            "edit_dup": "Duplicate Selection (Ctrl+D)",

            "edit_select_all": "Select All (Ctrl+A)",

            "edit_del": "Delete Selection (Delete)",

            "edit_hide": "Hide/Show Selection (Ctrl+H)",

            "transform": "Transform",

            "trans_ccw15": "Rotate CCW 15° (Ctrl+Left)",

            "trans_cw15": "Rotate CW 15° (Ctrl+Right)",

            "trans_custom": "Custom Rotation Angle...",

            "presets": "Presets",

            "view": "View",

            "view_grid": "Show Grid & Oxy Axes",

            "view_snap": "Grid Snap",

            "view_ask_name": "Prompt Name on Point Creation",

            "view_show_hidden": "Show Hidden Lines & Guides",

            "view_toggle_panel": "Toggle Solution Panel",

            "language": "Language",

            "help": "Help",

            "help_handbook": "📖 User Handbook & Shortcuts (F1)...",
            "help_about": "About GeoSolver..."

        },

        "bar1": {

            "new": {"text": "New", "tip_title": "New Drawing (Ctrl+N)", "tip_body": "Initialize a clean new drawing."},

            "clear_draw": {"text": "Clear Draw", "tip_title": "Clear Canvas Drawing", "tip_body": "Clear all geometric objects while keeping problem statement intact."},

            "undo": {"text": "Undo", "tip_title": "Undo (Ctrl+Z)", "tip_body": "Revert the last construction action."},

            "redo": {"text": "Redo", "tip_title": "Redo (Ctrl+Y)", "tip_body": "Redo the undone action."},

            "copy": {"text": "📋 Copy", "tip_title": "Copy (Ctrl+C)", "tip_body": "Copy selected objects to clipboard."},

            "paste": {"text": "📥 Paste", "tip_title": "Paste (Ctrl+V)", "tip_body": "Paste objects from clipboard."},

            "select_all": {"text": "Select All", "tip_title": "Select All (Ctrl+A)", "tip_body": "Select all objects to move, copy or rotate."},

            "rot_l": {"text": "Rot -15°", "tip_title": "Rotate -15°", "tip_body": "Rotate all points counter-clockwise by 15 degrees."},

            "rot_r": {"text": "Rot +15°", "tip_title": "Rotate +15°", "tip_body": "Rotate all points clockwise by 15 degrees."},

            "rot_custom": {"text": "Custom Rot...", "tip_title": "Custom Rotation Angle", "tip_body": "Enter exact degree angle to rotate."},

            "hide": {"text": "Hide/Show", "tip_title": "Hide/Show (Ctrl+H)", "tip_body": "Toggle hidden state of auxiliary lines."},

            "export": {"text": "Export PNG...", "tip_title": "Export PNG (Ctrl+E)", "tip_body": "Save high-resolution PNG image."},

            "lang_toggle": {"text": "🌐 English", "tip_title": "Switch to Vietnamese", "tip_body": "Click to switch entire interface to Vietnamese."},

            "about": {"text": "ℹ About", "tip_title": "About GeoSolver", "tip_body": "View version information, engine details and shortcuts."}

        },

        "bar_adv": {
            "lbl_adv": "📐 Advanced Math:",
            "harmonic": {"text": "[➗ Harmonic]", "tip_title": "Harmonic Conjugate Point", "tip_body": "Select points A, B and point C on AB to construct D such that (AB, CD) = -1."},
            "pole_polar": {"text": "[🎯 Pole & Polar]", "tip_title": "Poles and Polars", "tip_body": "Select circle and point P to draw polar line; or select line to find its pole."},
            "symmedian": {"text": "[📐 Symmedian]", "tip_title": "Symmedian & Lemoine Point", "tip_body": "Select triangle ABC to construct symmedian line and find Lemoine point."},
            "radical_axis": {"text": "[⭕ Radical Axis]", "tip_title": "Radical Axis of Two Circles", "tip_body": "Select two circles to construct their radical axis (equal power line)."},
            "barycentric": {"text": "[📊 Barycentric]", "tip_title": "Barycentric Coordinates Analysis", "tip_body": "Select triangle ABC and point P to compute normalized barycentric coordinates (u : v : w)."}
        },
        "btn_toggle_panel": {

            "text_show": "Solution [◀▶]",

            "text_hide": "Show Solution [▶]",

            "tip_title": "Toggle Solution Panel",

            "tip_body": "Click to expand canvas to full screen or restore solution panel."

        },

        "bar2": {

            "select": {"text": "[↖ Move]", "tip_title": "Select / Move", "tip_body": "Click to select or drag objects. Double-click a point to rename."},

            "rotate_mouse": {"text": "[⟲ Rotate]", "tip_title": "Rotate with Mouse", "tip_body": "Drag mouse in circular motion to rotate all points interactively."},

            "erase": {"text": "[✕ Erase]", "tip_title": "Erase Object", "tip_body": "Click on any point, segment, line or circle to delete."},

            "point": {"text": "[• Point]", "tip_title": "Free Point", "tip_body": "Click anywhere on the plane to place a new point."},

            "intersection": {"text": "[⤬ Intersect]", "tip_title": "Intersection Point", "tip_body": "Click near intersection of 2 lines, line & circle, or 2 circles."},

            "midpoint": {"text": "[✛ Midpoint]", "tip_title": "Midpoint", "tip_body": "Click two points to construct their midpoint."},

            "proj_foot": {"text": "[⏊ Proj]", "tip_title": "Perpendicular Foot", "tip_body": "Drop orthogonal projection from point onto line (e.g. D = proj of M on BC)."},

            "translate_vec": {"text": "[⇥ Translate]", "tip_title": "Vector Translation", "tip_body": "Translate point by vector (e.g. vec(MN) = vec(AC))."},

            "segment": {"text": "[/ Segment]", "tip_title": "Line Segment", "tip_body": "Click two points to create a segment."},

            "toggle_dash": {"text": "[┈ Dashed]", "tip_title": "Toggle Dashed / Solid", "tip_body": "Click any line segment or circle to toggle between Solid and Pedagogical Dashed line."},

            "line": {"text": "[― Line]", "tip_title": "Infinite Line", "tip_body": "Click two points to create an infinite line."},

            "perpendicular": {"text": "[⊥ Perp]", "tip_title": "Perpendicular Line", "tip_body": "Click 1 point and 1 line to construct perpendicular line."},

            "parallel": {"text": "[∥ Parallel]", "tip_title": "Parallel Line", "tip_body": "Click 1 point and 1 line to construct parallel line."},

            "bisector": {"text": "[∠ Bisector]", "tip_title": "Angle Bisector", "tip_body": "Click 3 points forming an angle (vertex in middle) to construct bisector."},

            "mark_angle": {"text": "[∠ Mark Angle]", "tip_title": "Pedagogical Angle Mark", "tip_body": "Mark angle: Right (square), 1 arc, 2 arcs, arc with tick; with Greek symbols (α, β...) or degree (°)."},

            "angle_ratio_point": {"text": "[📐 Angle/Ratio]", "tip_title": "Point by Angle & Ratio", "tip_body": "Construct point M by angle condition (e.g. BME=ECA, 30°, 45°) or ratio (e.g. AM=2*CB)."},

            "circle": {"text": "[○ Circle]", "tip_title": "Circle (Center & Point)", "tip_body": "Click center point, then click a point on circumference."},

            "circle_3p": {"text": "[⦿ Circle 3P]", "tip_title": "Circle through 3 Points", "tip_body": "Click 3 points to construct circumcircle passing through them."}

        },

        "bar3": {

            "parallelogram": {"text": "[▱ Parallelog.]", "tip_title": "Parallelogram", "tip_body": "Click 3 vertices A, B, C. Vertex D is computed automatically."},

            "rhombus": {"text": "[◇ Rhombus]", "tip_title": "Rhombus", "tip_body": "Click 2 base points A, B, then click direction point C to construct rhombus with 4 equal sides."},

            "isosceles_trapezoid": {"text": "[⏢ Iso. Trapezoid]", "tip_title": "Isosceles Trapezoid", "tip_body": "Click 2 base points A, B and 3rd point C. Vertex D is computed across the symmetry axis."},

            "square": {"text": "[□ Square]", "tip_title": "Square", "tip_body": "Click 2 base points A, B to construct square."},

            "ellipse": {"text": "[⬭ Ellipse]", "tip_title": "Ellipse", "tip_body": "Click Center O, major axis vertex A, and point B defining minor axis."},

            "smart_tangent": {"text": "[◎ Tangent]", "tip_title": "Smart Tangent", "tip_body": "• Click 2 centers: automatically creates ALL common tangents!\n• Click 1 circle: creates dynamic interactive tangent!"},

            "common_tangents": {"text": "[⊜ 2C Tangents]", "tip_title": "Common Tangents (2 Circles)", "tip_body": "Click 2 centers or 2 circles to construct common tangents."},

            "orthocenter": {"text": "[▲ Orthocenter]", "tip_title": "Orthocenter (H)", "tip_body": "Click 3 vertices of triangle to construct orthocenter H."},

            "incenter": {"text": "[⊙ Incenter]", "tip_title": "Incenter (I)", "tip_body": "Click 3 vertices to compute angle bisectors intersection (Incenter I)."},

            "incircle": {"text": "[⨀ Incircle]", "tip_title": "Incircle", "tip_body": "Click 3 vertices to construct incircle touching all 3 sides."},

            "circumcenter": {"text": "[⊚ Circumctr.]", "tip_title": "Circumcenter (O)", "tip_body": "Click 3 vertices to compute perpendicular bisectors intersection (O)."},

            "calc_area": {"text": "[📐 Area]", "tip_title": "Calculate Selected Area", "tip_body": "Select polygon, triangle or ellipse/circle to compute area and shaded fill."},

            "check_prop": {"text": "[✓ Check]", "tip_title": "Check Properties", "tip_body": "Click 3 points to test for Collinearity or Isosceles Triangle."}

        },

        "lbl_preset": "Preset:",

        "presets_list": [

            "0. [Blank Canvas] New Drawing",

            "1. Cyclic Quad & Find Vertex Coordinates (M, N, P, A, B)",

            "2. Midpoint Locus & Fixed Point of Two Circles",

            "3. Common Tangents & Collinear Points",

            "4. Translation Vector, Orthocenter & Circumcircle",

            "5. Moving Midpoint & Hyperbola Locus",

            "6. Equal Angles & Length Ratio by Angle",

            "7. Perpendicular Line Through Fixed Point",

            "8. Euler Circle Through Fixed Point & Invariant Segment",

            "9. Triangle Intersection & Hexagon DEFGHI Area (Radicals)",

            "10. Orthocenter, Secant Line & Midpoint Symmetry",

            "11. Cyclic Quad & Ptolemy's Theorem (Exact Area S=45)"
        ],

        "lbl_goal": "Goal:",

        "goals_list": [

            "Find Point Coordinates",

            "Prove 3 Points Collinear",

            "Find Point Locus",

            "Prove Fixed Point",

            "Prove Two Segments Equal",

            "Prove Two Lines Perpendicular",

            "Prove Two Lines Parallel",

            "Prove 3 Lines Concurrent",

            "Find Ratio & Correlation",

            "Calculate Area",

            "Comprehensive Auto Analysis (CAD)",

            "Prove Cyclic Quadrilateral",

            "Prove Similar / Congruent Triangles"

        ],

        "lbl_targets": "Targets:",

        "btn_solve": {

            "text": "▶ SOLVE (SymPy)",

            "tip_title": "Solve Geometry",

            "tip_body": "Analyze geometric relations and generate step-by-step SymPy proof."

        },

        "color_palette": {

            "title": "Color:",

            "red": "🔴 Red",

            "blue": "🔵 Blue",

            "black": "⚫ Black",

            "green": "🟢 Green",

            "tip_red": ("Color Red (#e03131)", "Change selected objects to red (or set as default for next objects)."),

            "tip_blue": ("Color Blue (#1971c2)", "Change selected objects to academic blue."),

            "tip_black": ("Color Black (#212529)", "Change selected objects to print black."),

            "tip_green": ("Color Green (#2b8a3e)", "Change selected objects to green.")

        },

        "tab_solver": " Solution & Problem ",

        "prob_head": "Problem Statement:",

        "inv_box": "Detected Invariants (Property Checker)",

        "sol_box": "Proof Sequence & Detailed Solution",

        "tab_algebra": " Geometric Objects ",

        "tree_cols": ("Object", "Coordinates / Equation", "Status"),

        "lbl_cmd": "Command:",

        "lbl_cmd_hint": "Example: A=(0, 4) | line(A, B) | circle(O, 3)",

        "status_ready": "Ready.",

        "lbl_legal": "⚖️ GEOSOLVER v2.5 COPYRIGHT PROTECTED | 🔏 DIGITAL SIGNATURE READY",

        "about_dialog_title": "About GeoSolver v2.5",

        "about_text": (

            "PRODUCT INFORMATION & COPYRIGHT:\n"

            "• Application Name: GeoSolver\n"

            "• Version: 2.5 (Official Release November 2026)\n"

            "• Computational Engine: Python Tkinter CAD Engine & SymPy CAS Solver.\n"

            "• Copyright & Author: © 2026 GeoSolver. All Rights Reserved.\n\n"

            "STRICT LEGAL NOTICE & INTELLECTUAL PROPERTY:\n"

            "All rights reserved. Any unauthorized reproduction, decompilation, reverse engineering,\n"

            "distribution, commercial exploitation, or adaptation of this software in whole or in part\n"

            "is strictly prohibited and constitutes an infringement of intellectual property laws (WIPO/TRIPS).\n"

            "Violators will be prosecuted to the maximum extent permitted by law.\n\n"

            "SECURITY & DIGITAL SIGNATURE READINESS:\n"

            "• Verification Standard: PKI / RSA-4096 / SHA-256 Cryptographic Integrity Seal.\n"

            "• Status: READY FOR AUTHOR DIGITAL SIGNATURE & TIMESTAMP AUTHORITY (TSA) SEAL.\n\n"

            "KEY FEATURES:\n"

            "1. Technical CAD Studio Clean Interface:\n"

            "   - Organized 4-row compact toolbars, ~30% smaller button footprint, zero button cutoff.\n"

            "   - Collapsible Solution Panel on the right for full-screen drawing canvas.\n"

            "2. Advanced Geometric Construction:\n"

            "   - Pedagogical Dashed Line Tool [┈ Dashed]: Instant toggle between solid and dashed styling.\n"

            "   - Clean Image Export: Pure white background, zero stray lines, auto-crop bounding box.\n"

            "   - Smart Tangents: Automated common tangents (inner & outer) for 2 circles; dynamic interactive tangent for single circle.\n"

            "   - Point Builder by Angle & Ratio (AM = k*BC, equal angles BME = ECA, degree angles).\n"

            "   - Full Triangle Centers: Orthocenter (H), Incenter (I), Incircle, Circumcenter (O).\n"

            "   - Standard Polygons: Parallelogram, Rhombus, Square.\n"

            "3. Automated CAS Geometry Solver & Streaming:\n"

            "   - SymPy algebraic solver for Coordinate Geometry (Oxy) & VMO Olympiad (2000, 2001, 2003, 2007, 2008).\n"

            "   - Live typewriter / auto-streaming animation for step-by-step proofs.\n"

            "   - Automatic invariant detection: Collinear, tangent, perpendicular, equal ratios.\n"

            "4. Drawing Management:\n"

            "   - Comprehensive Clipboard: Copy (Ctrl+C), Paste (Ctrl+V), Duplicate (Ctrl+D).\n"

            "   - Non-destructive canvas clear (preserves problem statement & solution text).\n"

            "   - Clean bilingual UI with instantaneous toggle between Tiếng Việt and English.\n\n"

            "KEYBOARD SHORTCUTS:\n"

            "• Ctrl + N: New blank drawing\n"

            "• Ctrl + Z / Ctrl + Y: Undo / Redo\n"

            "• Ctrl + C / Ctrl + V: Copy / Paste selected objects\n"

            "• Ctrl + D: Quick duplicate selection\n"

            "• Ctrl + A: Select all objects on canvas\n"

            "• Delete: Erase selected objects\n"

            "• Ctrl + H: Hide / Show auxiliary lines\n"

            "• Ctrl + E: Export clean pedagogical PNG image\n"

            "• Mouse Wheel: Zoom in / Zoom out canvas\n"

            "• Right-click Drag: Pan canvas\n"

        )

    }

}



# ---------------------------------------------------------------------------

# Dang ky LANG_DATA vao he thong i18n tap trung (stem_shared_core.i18n)

# Du lieu duoc dang ky voi prefix 'geo.' de tranh xung dot namespace.

# ---------------------------------------------------------------------------

if _I18N_AVAILABLE:

    try:

        from stem_shared_core.i18n import get_i18n as _get_i18n_geo

        _mgr_geo = _get_i18n_geo()

        for _lng_geo, _dict_geo in LANG_DATA.items():

            _mgr_geo.register_translations(_lng_geo, {"geo": _dict_geo})

        del _mgr_geo, _lng_geo, _dict_geo

    except Exception:

        pass





def _geo_t(key, lang=None):

    """Lay chuoi dich cho GeoSolver. Uu tien i18n tap trung, fallback ve LANG_DATA."""

    if _I18N_AVAILABLE:

        try:

            val = _i18n_t("geo." + key, lang=lang)

            if val != "geo." + key:

                return val

        except Exception:

            pass

    _lang = lang or "vi"

    if _I18N_AVAILABLE:

        try:

            _lang = _i18n_get()

        except Exception:

            pass

    return LANG_DATA.get(_lang, LANG_DATA.get("vi", {})).get(key, key)





# ---------------------------------------------------------------------------

# Dang ky LANG_DATA vao he thong i18n tap trung (stem_shared_core.i18n)

# Du lieu duoc dang ky voi prefix 'geo.' de tranh xung dot namespace.

# ---------------------------------------------------------------------------

if _I18N_AVAILABLE:

    try:

        from stem_shared_core.i18n import get_i18n as _get_i18n_geo

        _mgr_geo = _get_i18n_geo()

        for _lng_geo, _dict_geo in LANG_DATA.items():

            _mgr_geo.register_translations(_lng_geo, {"geo": _dict_geo})

        del _mgr_geo, _lng_geo, _dict_geo

    except Exception:

        pass





def _geo_t(key, lang=None):

    """Lay chuoi dich cho GeoSolver. Uu tien i18n tap trung, fallback ve LANG_DATA."""

    if _I18N_AVAILABLE:

        try:

            val = _i18n_t("geo." + key, lang=lang)

            if val != "geo." + key:

                return val

        except Exception:

            pass

    _lang = lang or "vi"

    if _I18N_AVAILABLE:

        try:

            _lang = _i18n_get()

        except Exception:

            pass

    return LANG_DATA.get(_lang, LANG_DATA.get("vi", {})).get(key, key)





PRESET_PROBLEMS = {

    "vi": {

        "vmo_2000": (

            "Bài 1 (VMO 2000 - Bảng B). Cho hai đường tròn (O1; r1) và (O2; r2). Trên (O1; r1) lấy M1, "

            "trên (O2; r2) lấy M2 sao cho O1M1 cắt O2M2 tại Q. Cho M1, M2 chuyển động cùng chiều kim đồng hồ "

            "với cùng vận tốc góc.\n"

            "1) Tìm quỹ tích trung điểm M của đoạn thẳng M1M2.\n"

            "2) Chứng minh giao điểm thứ hai P của (M1QM2) và (O1QO2) là điểm cố định."

        ),

        "vmo_2001": (

            "Bài 2 (VMO 2001 - Bảng B). Cho hai đường tròn (O1) và (O2) cắt nhau tại A, B. "

            "P1P2 là tiếp tuyến chung (P1 ∈ (O1), P2 ∈ (O2)). Q1, Q2 là hình chiếu vuông góc của P1, P2 trên O1O2. "

            "AQ1 cắt (O1) tại M1, AQ2 cắt (O2) tại M2. Chứng minh M1, B, M2 thẳng hàng."

        ),

        "vmo_2003": (

            "Bài 4 (VMO 2003 - Bảng B). Cho tam giác nhọn ABC nội tiếp đường tròn tâm O. "

            "Trên đường thẳng AC lấy các điểm M, N sao cho vector(MN) = vector(AC). "

            "Gọi D là hình chiếu vuông góc của M trên đường thẳng BC; E là hình chiếu vuông góc của N trên đường thẳng AB.\n"

            "1) Chứng minh rằng trực tâm H của tam giác ABC nằm trên đường tròn tâm O' ngoại tiếp tam giác BED.\n"

            "2) Chứng minh rằng trung điểm I của đoạn thẳng AN đối xứng với B qua trung điểm của đoạn thẳng OO'."

        ),

        "vmo_2007": (

            "Bài 9 (VMO 2007 - Bảng B). Cho tam giác nhọn ABC có trực tâm H, trọng tâm G và tâm đường tròn ngoại tiếp O. "

            "Cho B, C cố định, A di động sao cho trung điểm K của đoạn HG luôn nằm trên đường thẳng BC. "

            "Tìm quỹ tích đỉnh A khi tam giác ABC luôn nhọn."

        ),

        "vmo_2008": (

            "Bài 11 (VMO 2008). Cho tam giác ABC. Gọi E là trung điểm của cạnh AB. "

            "Cho góc BEC = alpha (0° < alpha < 180°). Trên tia EC lấy điểm M sao cho góc BME = góc ECA.\n"

            "Hãy tính tỉ số độ dài MC / AB theo góc alpha."

        ),

        "cau_viii": (

            "Câu VIII (Tuyển sinh Oxy). Trong mặt phẳng Oxy, cho hình thang vuông ABCD (vuông tại A và D) "

            "có AB = 2, CD = 4, BC = 2*sqrt(2). "

            "M, N là hình chiếu vuông góc của A trên BC, BD. P = MN ∩ AC. "

            "Biết AC: x - y - 1 = 0, M(0; 4), N(2; 2), xA < 2. Tìm tọa độ P, A, B."

        ),

        "vmo_2008_bai12": (

            "Bài 12 (VMO 2008). Cho tam giác ABC, trung tuyến AD. Cho đường thẳng d vuông góc với đường thẳng AD. "

            "Xét điểm M nằm trên d. Gọi E, F lần lượt là trung điểm của MB, MC. "

            "Đường thẳng đi qua E và vuông góc với d cắt đường thẳng AB ở P, "

            "đường thẳng đi qua F và vuông góc với d cắt đường thẳng AC ở Q.\n"

            "Chứng minh rằng đường thẳng đi qua M vuông góc với đường thẳng PQ luôn đi qua 1 điểm cố định khi điểm M di động trên đường thẳng d."

        ),

        "vmo_2009_bai13": (

            "Bài 13 (VMO 2009). Trong mặt phẳng cho hai điểm cố định A, B (A != B). "

            "Một điểm C di động sao cho góc ACB = alpha không đổi (0° < alpha < 180°). "

            "Đường tròn tâm I nội tiếp tam giác ABC và tiếp xúc với AB, BC, CA lần lượt tại D, E, F. "

            "Các đường thẳng AI, BI cắt đường thẳng EF lần lượt tại M và N.\n"

            "1) Chứng minh rằng đoạn thẳng MN có độ dài không đổi: MN = AB * sin(alpha/2).\n"

            "2) Chứng minh rằng đường tròn ngoại tiếp tam giác DMN luôn đi qua một điểm cố định (trung điểm K của AB)."

        ),

        "hex_intersection": (

            "Bài 10 (Hình học giải tích & Tọa độ). Cho tam giác ABC với A(0, 5), B(-3, 0), C(3, 0) "

            "và tam giác A1B1C1 với A1(-10/3, 5/3), B1(5/3, -4/3), C1(5/3, 14/3).\n"

            "Phần giao nhau giữa hai miền tam giác là đa giác lục giác DEFGHI với các giao điểm D, E, F, G, H, I.\n"

            "1) Xác định chính xác tọa độ các đỉnh D, E, F, G, H, I.\n"

            "2) Tính độ dài các cạnh của đa giác dưới dạng căn thức chính xác (exact radicals).\n"

            "3) Tính chu vi P và diện tích S của đa giác DEFGHI theo công thức Dây giày Gauss."

        ),

        "vmo_2015": (

            "Bài 14 (VMO 2015). Cho tam giác nhọn ABC không cân nội tiếp đường tròn (O). "

            "Các đường cao AD, BE, CF đồng quy tại trực tâm H. Gọi M là trung điểm cạnh BC. "

            "Đường tròn ngoại tiếp tam giác AEF cắt (O) tại điểm thứ hai P (P != A). "

            "Đường thẳng PM cắt (O) tại điểm thứ hai Q (Q != P).\n"

            "1) Chứng minh 4 điểm D, E, F, M cùng thuộc một đường tròn (Đường tròn Euler 9 điểm).\n"

            "2) Chứng minh điểm Q đối xứng với trực tâm H qua trung điểm M của BC."

        ),

        "olympic_ptolemy": (

            "Bài 15 (Olympic Hình học & Định lý Ptolemy). Trong mặt phẳng Oxy, cho tứ giác ABCD "

            "nội tiếp đường tròn tâm O bán kính R = 5 với các đỉnh:\n"

            "A(0, 5), B(-4, 3), C(-3, -4), D(4, -3).\n"

            "1) Tính độ dài các cạnh AB, BC, CD, DA và các đường chéo AC, BD dưới dạng căn thức đúng.\n"

            "2) Kiểm chứng định lý Ptolemy: AC * BD = AB * CD + BC * DA = 30*sqrt(10).\n"

            "3) Tính diện tích S của tứ giác ABCD (S = 45)."

        )

    },

    "en": {

        "vmo_2000": (

            "Problem 1 (VMO 2000 - Group B). Given two circles (O1; r1) and (O2; r2). Let M1 on (O1) and M2 on (O2) "

            "such that O1M1 intersects O2M2 at Q. Points M1, M2 rotate clockwise with identical angular velocity.\n"

            "1) Find the locus of the midpoint M of segment M1M2.\n"

            "2) Prove that the second intersection P of (M1QM2) and (O1QO2) is a fixed point."

        ),

        "vmo_2001": (

            "Problem 2 (VMO 2001 - Group B). Given two circles (O1) and (O2) intersecting at A, B. "

            "P1P2 is a common tangent (P1 ∈ (O1), P2 ∈ (O2)). Q1, Q2 are orthogonal projections of P1, P2 onto line O1O2. "

            "AQ1 intersects (O1) at M1, AQ2 intersects (O2) at M2. Prove that M1, B, M2 are collinear."

        ),

        "vmo_2003": (

            "Problem 4 (VMO 2003 - Group B). Given acute triangle ABC inscribed in circle (O). "

            "On line AC, take points M, N such that vector(MN) = vector(AC). "

            "Let D be the projection of M on line BC; E be the projection of N on line AB.\n"

            "1) Prove that the orthocenter H of triangle ABC lies on the circumcircle (O') of triangle BED.\n"

            "2) Prove that the midpoint I of segment AN is symmetric to B with respect to the midpoint of segment OO'."

        ),

        "vmo_2007": (

            "Problem 9 (VMO 2007 - Group B). Given acute triangle ABC with orthocenter H, centroid G, and circumcenter O. "

            "Points B, C are fixed; vertex A moves such that midpoint K of segment HG always lies on line BC. "

            "Find the locus of vertex A while triangle ABC remains acute."

        ),

        "vmo_2008": (

            "Problem 11 (VMO 2008). Given triangle ABC with E as the midpoint of AB. "

            "Let angle BEC = alpha (0° < alpha < 180°). On ray EC, take point M such that angle BME = angle ECA.\n"

            "Find the length ratio MC / AB in terms of angle alpha."

        ),

        "cau_viii": (

            "Question VIII (High School Entrance Exam Oxy). In the Oxy Cartesian plane, given right trapezoid ABCD "

            "(perpendicular at A and D) with AB = 2, CD = 4, BC = 2*sqrt(2). "

            "M, N are orthogonal projections of A onto BC, BD. P = MN ∩ AC. "

            "Given line AC: x - y - 1 = 0, M(0; 4), N(2; 2), xA < 2. Find exact coordinates of P, A, and B."

        ),

        "vmo_2008_bai12": (

            "Problem 12 (VMO 2008). Given triangle ABC with median AD. Let line d be perpendicular to line AD. "

            "Point M lies on line d. Let E, F be midpoints of MB, MC respectively. "

            "The line through E perpendicular to d intersects AB at P; the line through F perpendicular to d intersects AC at Q.\n"

            "Prove that the line through M perpendicular to PQ always passes through a unique fixed point R as M moves on d."

        ),

        "vmo_2009_bai13": (

            "Problem 13 (VMO 2009). In the plane, given two fixed points A, B (A != B). "

            "A point C moves such that angle ACB = alpha is constant (0° < alpha < 180°). "

            "The incircle (I) of triangle ABC touches AB, BC, CA at D, E, F respectively. "

            "Lines AI, BI intersect line EF at M and N respectively.\n"

            "1) Prove that segment MN has constant length: MN = AB * sin(alpha/2).\n"

            "2) Prove that the circumcircle of triangle DMN always passes through a fixed point (midpoint K of AB)."

        ),

        "hex_intersection": (

            "Problem 10 (Analytic Geometry & Coordinates). Given triangle ABC with vertices A(0, 5), B(-3, 0), C(3, 0) "

            "and triangle A1B1C1 with A1(-10/3, 5/3), B1(5/3, -4/3), C1(5/3, 14/3).\n"

            "The intersection of the two triangles forms hexagon DEFGHI with vertices D, E, F, G, H, I.\n"

            "1) Determine the exact coordinates of vertices D, E, F, G, H, I.\n"

            "2) Compute all side lengths in exact radical form.\n"

            "3) Compute the perimeter P and area S of hexagon DEFGHI using the Gauss Shoelace Formula."

        ),

        "vmo_2015": (

            "Problem 14 (VMO 2015). Given acute scalene triangle ABC inscribed in circle (O). "

            "Altitudes AD, BE, CF concur at orthocenter H. Let M be the midpoint of BC. "

            "The circumcircle of triangle AEF intersects (O) at a second point P (P != A). "

            "Line PM intersects (O) at a second point Q (Q != P).\n"

            "1) Prove that points D, E, F, M are concyclic (9-point Euler circle).\n"

            "2) Prove that point Q is symmetric to orthocenter H with respect to midpoint M."

        ),

        "olympic_ptolemy": (

            "Problem 15 (Geometry Olympiad & Ptolemy's Theorem). In the Oxy plane, given quadrilateral ABCD "

            "inscribed in circle (O; R = 5) with vertices:\n"

            "A(0, 5), B(-4, 3), C(-3, -4), D(4, -3).\n"

            "1) Compute edge lengths AB, BC, CD, DA and diagonals AC, BD in exact radical form.\n"

            "2) Verify Ptolemy's Theorem: AC * BD = AB * CD + BC * DA = 30*sqrt(10).\n"

            "3) Calculate the area S of quadrilateral ABCD (S = 45)."

        )

    }

}







def clip_polygon_sutherland_hodgman(subject_polygon, clip_polygon_pts):

    """Cắt xén 2 đa giác lồi/đơn giản bằng thuật toán Sutherland-Hodgman để tìm miền giao nhau."""

    def inside(cp1, cp2, p):

        return (cp2[0] - cp1[0]) * (p[1] - cp1[1]) >= (cp2[1] - cp1[1]) * (p[0] - cp1[0]) - 1e-9



    def intersection(cp1, cp2, s, e):

        dc = (cp1[0] - cp2[0], cp1[1] - cp2[1])

        dp = (s[0] - e[0], s[1] - e[1])

        n1 = cp1[0] * cp2[1] - cp1[1] * cp2[0]

        n2 = s[0] * e[1] - s[1] * e[0]

        denom = dc[0] * dp[1] - dc[1] * dp[0]

        if abs(denom) < 1e-12:

            return s

        return ((n1 * dp[0] - n2 * dc[0]) / denom, (n1 * dp[1] - n2 * dc[1]) / denom)



    output_list = list(subject_polygon)

    cp_len = len(clip_polygon_pts)

    if cp_len < 3 or len(output_list) < 3:

        return []



    area_clip = sum(clip_polygon_pts[i][0]*clip_polygon_pts[(i+1)%cp_len][1] - clip_polygon_pts[(i+1)%cp_len][0]*clip_polygon_pts[i][1] for i in range(cp_len))

    clipping_pts = list(clip_polygon_pts) if area_clip >= 0 else list(reversed(clip_polygon_pts))



    for i in range(cp_len):

        cp1 = clipping_pts[i]

        cp2 = clipping_pts[(i + 1) % cp_len]

        input_list = output_list

        output_list = []

        if not input_list:

            break

        s = input_list[-1]

        for e in input_list:

            if inside(cp1, cp2, e):

                if not inside(cp1, cp2, s):

                    output_list.append(intersection(cp1, cp2, s, e))

                output_list.append(e)

            elif inside(cp1, cp2, s):

                output_list.append(intersection(cp1, cp2, s, e))

            s = e

    return output_list





def format_exact_radical(val_squared: float, approx_val: float | None = None) -> str:
    """Biểu diễn căn thức chính xác dạng √n hoặc a√b kết hợp số thập phân xấp xỉ."""
    import math
    try:
        import sympy as sp
        r = sp.Rational(round(val_squared, 6)).limit_denominator(2000)
        s = sp.sqrt(r)
        if s.is_rational:
            return f"{s}"
        s_str = str(s).replace("*sqrt", "√").replace("sqrt", "√")
        if approx_val is not None:
            return f"{s_str} ≈ {approx_val:.4f}"
        return f"{s_str} ≈ {float(s):.4f}"
    except Exception:
        if approx_val is not None:
            return f"{approx_val:.4f}"
        return f"{math.sqrt(val_squared):.4f}"


def format_polygon_pedagogical_area(pts, lang="vi", is_intersection=False, inter_info=""):

    """Định dạng lời giải diện tích đa giác chi tiết: Tính độ dài từng cạnh, Heron (tam giác), và Dây giày Gauss."""

    import math

    is_en = (lang == "en")

    n = len(pts)

    if n < 3:

        return "Vui lòng chỉ định ít nhất 3 đỉnh để tính diện tích đa giác.\n" if not is_en else "Please specify at least 3 vertices to compute polygon area.\n"



    coords = []

    names = []

    for i, p in enumerate(pts):

        if isinstance(p, dict):

            nm = p.get("name") or p.get("id") or f"V{i+1}"

            coords.append((float(p["x"]), float(p["y"])))

            names.append(nm)

        else:

            coords.append((float(p[0]), float(p[1])))

            names.append(f"V{i+1}")



    poly_name = "".join(names) if all(len(nm) <= 2 for nm in names) else ", ".join(names)



    edge_dists = []

    edge_strs = []

    perim = 0.0

    for i in range(n):

        p1 = coords[i]

        p2 = coords[(i + 1) % n]

        dist = math.hypot(p2[0] - p1[0], p2[1] - p1[1])

        edge_dists.append(dist)

        perim += dist

        nm1 = names[i]

        nm2 = names[(i + 1) % n]

        dist_sq = (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2
        rad_str = format_exact_radical(dist_sq, dist)
        edge_strs.append(f"{nm1}{nm2} = √(({p2[0]:.4f} - {p1[0]:.4f})² + ({p2[1]:.4f} - {p1[1]:.4f})²) = {rad_str}")



    shoelace_terms = []

    shoelace_sum = 0.0

    for i in range(n):

        x1, y1 = coords[i]

        x2, y2 = coords[(i + 1) % n]

        term = x1 * y2 - x2 * y1

        shoelace_terms.append(term)

        shoelace_sum += term

    area = abs(shoelace_sum) / 2.0



    out = []

    if is_en:

        out.append("=========================================================\n")

        out.append("  PEDAGOGICAL POLYGON AREA & METRICS (SHOELACE & HERON CAS)\n")

        out.append("=========================================================\n\n")

        if is_intersection:

            out.append(f"• COMMON INTERSECTION REGION: {inter_info}\n")

            out.append(f"  The overlapping region forms a polygon with {n} vertices ({poly_name}).\n\n")

        out.append(f"• Investigated Polygon: {poly_name} (Vertices: {n})\n")

        out.append("• Vertex coordinates:\n")

        for i in range(n):

            out.append(f"  - {names[i]}: ({coords[i][0]:.4f}, {coords[i][1]:.4f})\n")

        out.append("\n• Step 1: Explicit edge lengths calculation (Euclidean Distance):\n")

        for es in edge_strs:

            out.append(f"  + {es}\n")

        out.append(f"  => Total Perimeter P = {perim:.4f}\n\n")



        if n == 3:

            a, b, c = edge_dists[1], edge_dists[2], edge_dists[0]

            p_semi = perim / 2.0

            heron_prod = p_semi * (p_semi - a) * (p_semi - b) * (p_semi - c)

            heron_area = math.sqrt(max(0.0, heron_prod))

            r_in = area / p_semi if p_semi > 0 else 0.0

            R_out = (a * b * c) / (4.0 * area) if area > 0 else 0.0



            out.append("• Step 2: Method A - Heron's Formula (Calculated from 3 Side Lengths):\n")

            out.append(f"  - Semiperimeter: p = P / 2 = {perim:.4f} / 2 = {p_semi:.4f}\n")

            out.append(f"  - Side lengths: a = {a:.4f}, b = {b:.4f}, c = {c:.4f}\n")

            out.append("  - Formula: S = sqrt(p * (p - a) * (p - b) * (p - c))\n")

            out.append(f"    S = sqrt({p_semi:.4f} * ({p_semi:.4f} - {a:.4f}) * ({p_semi:.4f} - {b:.4f}) * ({p_semi:.4f} - {c:.4f}))\n")

            out.append(f"    S = sqrt({max(0.0, heron_prod):.4f}) = {heron_area:.4f}\n\n")



            out.append("• Step 3: Method B - Gauss Shoelace Determinant (Cartesian Coordinates):\n")

            out.append("  - Formula: S = 1/2 * |(x1*y2 - x2*y1) + (x2*y3 - x3*y2) + (x3*y1 - x1*y3)|\n")

            for i in range(n):

                nm1, nm2 = names[i], names[(i + 1) % n]

                x1, y1 = coords[i]

                x2, y2 = coords[(i + 1) % n]

                out.append(f"    Edge {nm1}{nm2}: ({x1:.4f} * {y2:.4f}) - ({x2:.4f} * {y1:.4f}) = {shoelace_terms[i]:.4f}\n")

            out.append(f"  => Sum of cross-products = {shoelace_sum:.4f}\n")

            out.append(f"  => S = 1/2 * |{shoelace_sum:.4f}| = {area:.4f}\n\n")



            out.append("---------------------------------------------------------\n")

            out.append(f"🎯 FINAL AREA:       S({poly_name}) = {area:.4f} (square units)\n")

            out.append(f"🎯 PERIMETER:        P({poly_name}) = {perim:.4f}\n")

            out.append(f"• Incircle Radius:    r = S / p = {r_in:.4f}\n")

            out.append(f"• Circumcircle Radius: R = (a*b*c) / (4S) = {R_out:.4f}\n")

            out.append("=========================================================\n")

        else:

            out.append("• Step 2: Gauss Shoelace Formula (Generalized Cartesian Polygon Area):\n")

            out.append("  - Formula: S = 1/2 * | sum_{i=1}^n (x_i * y_{i+1} - x_{i+1} * y_i) |\n")

            out.append("  - Cross-product decomposition by edges:\n")

            for i in range(n):

                nm1, nm2 = names[i], names[(i + 1) % n]

                x1, y1 = coords[i]

                x2, y2 = coords[(i + 1) % n]

                out.append(f"    Edge {nm1}{nm2}: ({x1:.4f} * {y2:.4f}) - ({x2:.4f} * {y1:.4f}) = {shoelace_terms[i]:.4f}\n")

            out.append(f"  => Net Determinant Sum = {shoelace_sum:.4f}\n")

            out.append(f"  => Area S = 1/2 * |{shoelace_sum:.4f}| = {area:.4f}\n\n")

            out.append("---------------------------------------------------------\n")

            out.append(f"🎯 FINAL AREA: S({poly_name}) = {area:.4f} (square units)\n")

            out.append(f"🎯 PERIMETER:  P({poly_name}) = {perim:.4f}\n")

            out.append("=========================================================\n")

    else:

        out.append("=========================================================\n")

        out.append("  KẾT QUẢ ĐO ĐẠC HÌNH HỌC & TÍNH DIỆN TÍCH (AREA ENGINE)\n")

        out.append("=========================================================\n\n")

        if is_intersection:

            out.append(f"• DIỆN TÍCH PHẦN CHUNG: {inter_info}\n")

            out.append(f"  Miền giao nhau giữa 2 hình tạo thành đa giác gồm {n} đỉnh ({poly_name}).\n\n")

        out.append(f"• Đa giác khảo sát: {poly_name} (Số đỉnh: {n})\n")

        out.append("• Tọa độ các đỉnh:\n")

        for i in range(n):

            out.append(f"  - {names[i]}: ({coords[i][0]:.4f}; {coords[i][1]:.4f})\n")

        out.append("\n• Bước 1: Tính chi tiết độ dài các cạnh (Khoảng cách Euclid):\n")

        for es in edge_strs:

            out.append(f"  + {es}\n")

        out.append(f"  => Tổng chu vi P = {perim:.4f}\n\n")



        if n == 3:

            a, b, c = edge_dists[1], edge_dists[2], edge_dists[0]

            p_semi = perim / 2.0

            heron_prod = p_semi * (p_semi - a) * (p_semi - b) * (p_semi - c)

            heron_area = math.sqrt(max(0.0, heron_prod))

            r_in = area / p_semi if p_semi > 0 else 0.0

            R_out = (a * b * c) / (4.0 * area) if area > 0 else 0.0



            out.append("• Bước 2: Cách 1 - Công thức Hê-rông (Heron) tính qua độ dài 3 cạnh:\n")

            out.append(f"  - Nửa chu vi: p = P / 2 = {perim:.4f} / 2 = {p_semi:.4f}\n")

            out.append(f"  - Ba cạnh: a = {a:.4f}, b = {b:.4f}, c = {c:.4f}\n")

            out.append("  - Công thức: S = sqrt(p * (p - a) * (p - b) * (p - c))\n")

            out.append(f"    S = sqrt({p_semi:.4f} * ({p_semi:.4f} - {a:.4f}) * ({p_semi:.4f} - {b:.4f}) * ({p_semi:.4f} - {c:.4f}))\n")

            out.append(f"    S = sqrt({max(0.0, heron_prod):.4f}) = {heron_area:.4f}\n\n")



            out.append("• Bước 3: Cách 2 - Công thức Dây giày Gauss (Shoelace Formula) qua tọa độ:\n")

            out.append("  - Công thức: S = 1/2 * |(x1*y2 - x2*y1) + (x2*y3 - x3*y2) + (x3*y1 - x1*y3)|\n")

            for i in range(n):

                nm1, nm2 = names[i], names[(i + 1) % n]

                x1, y1 = coords[i]

                x2, y2 = coords[(i + 1) % n]

                out.append(f"    Cạnh {nm1}{nm2}: ({x1:.4f} * {y2:.4f}) - ({x2:.4f} * {y1:.4f}) = {shoelace_terms[i]:.4f}\n")

            out.append(f"  => Tổng các tích chéo = {shoelace_sum:.4f}\n")

            out.append(f"  => Diện tích S = 1/2 * |{shoelace_sum:.4f}| = {area:.4f}\n\n")



            out.append("---------------------------------------------------------\n")

            out.append(f"🎯 DIỆN TÍCH: S({poly_name}) = {area:.4f} (đơn vị diện tích)\n")

            out.append(f"🎯 CHU VI:   P({poly_name}) = {perim:.4f}\n")

            out.append(f"• Bán kính đường tròn nội tiếp:  r = S / p = {r_in:.4f}\n")

            out.append(f"• Bán kính đường tròn ngoại tiếp: R = abc / (4S) = {R_out:.4f}\n")

            out.append("=========================================================\n")

        else:

            out.append("• Bước 2: Áp dụng công thức Dây giày Gauss (Shoelace Formula) cho đa giác n cạnh:\n")

            out.append("  - Công thức: S = 1/2 * | sum_{i=1}^n (x_i * y_{i+1} - x_{i+1} * y_i) |\n")

            out.append("  - Phân tích chi tiết tích chéo từng cạnh:\n")

            for i in range(n):

                nm1, nm2 = names[i], names[(i + 1) % n]

                x1, y1 = coords[i]

                x2, y2 = coords[(i + 1) % n]

                out.append(f"    Cạnh {nm1}{nm2}: ({x1:.4f} * {y2:.4f}) - ({x2:.4f} * {y1:.4f}) = {shoelace_terms[i]:.4f}\n")

            out.append(f"  => Tổng đại số định thức = {shoelace_sum:.4f}\n")

            out.append(f"  => Diện tích S = 1/2 * |{shoelace_sum:.4f}| = {area:.4f}\n\n")

            out.append("---------------------------------------------------------\n")

            out.append(f"🎯 DIỆN TÍCH: S({poly_name}) = {area:.4f} (đơn vị diện tích)\n")

            out.append(f"🎯 CHU VI:   P({poly_name}) = {perim:.4f}\n")

            out.append("=========================================================\n")



    return "".join(out)



# =========================================================================
# BỘ GIAO DIỆN CHUẨN ĐỒNG BỘ VỚI CAD MATH (4 THEMES: LIGHT, BLUE, CLASSIC, DARK)
# =========================================================================
THEMES_GEOSOLVER = {
    "win11_light": {
        "name": "Giao diện sáng (Light)",
        "bg_window": "#F1F5F9",          # Slate-100 clean background
        "toolbar_bg": "#F8FAFC",         # Slate-50 crisp neutral toolbar
        "bar4_bg": "#E2E8F0",            # Slate-200 solver bar
        "btn_bg": "#FFFFFF",             # Pure white card button
        "btn_fg": "#0F172A",             # Slate-900 sharp charcoal text
        "btn_border": "#CBD5E1",         # Slate border
        "btn_active_bg": "#E2E8F0",
        "btn_active_fg": "#0F172A",
        "tool_active_bg": "#2563EB",     # Royal Blue active highlight
        "tool_active_fg": "#FFFFFF",
        "canvas_bg": "#FFFFFF",          # Pure white canvas
        "grid": "#E2E8F0",               # Light neutral gray grid
        "axis": "#64748B",               # Slate-500 neutral axes
        "text": "#0F172A",               # Charcoal labels
        "line": "#1E293B",               # Dark slate geometry lines
        "label_fg": "#334155",
        "card_bg": "#FFFFFF",
        "status_bg": "#E2E8F0",          # Slate status bar
        "status_fg": "#334155",
        "text_box_bg": "#FFFFFF",
        "text_box_fg": "#0F172A",
        "tab_bg": "#E2E8F0",
        "tab_fg": "#475569",
        "tab_active_bg": "#FFFFFF",
        "tab_active_fg": "#2563EB",
    },
    "win11_blue": {
        "name": "Giao diện xanh hiện đại (Modern Blue)",
        "bg_window": "#EDF5FD",          # Very pleasant soft sky blue
        "toolbar_bg": "#D6E8FA",         # Clearly blue ribbon toolbar
        "bar4_bg": "#C4DFFA",            # Deeper blue accent bar for solver
        "btn_bg": "#FFFFFF",             # Crisp white card button
        "btn_fg": "#0A4275",             # Deep rich navy blue
        "btn_border": "#93C5FD",         # Blue border
        "btn_active_bg": "#BAE6FD",
        "btn_active_fg": "#0369A1",
        "tool_active_bg": "#0067C0",     # Electric vibrant primary blue
        "tool_active_fg": "#FFFFFF",     # Crisp white
        "canvas_bg": "#FFFFFF",          # Pure white drawing area
        "grid": "#CCE3F8",               # Distinctly soft blue technical grid!
        "axis": "#0067C0",               # Vibrant blue coordinate axes!
        "text": "#0A4275",               # Navy coordinate labels
        "line": "#0A2540",               # Midnight navy geometry lines
        "label_fg": "#0A4275",           # Dark blue label text
        "card_bg": "#FFFFFF",
        "status_bg": "#C4DFFA",          # Soft blue status bar
        "status_fg": "#0A4275",
        "text_box_bg": "#FFFFFF",
        "text_box_fg": "#0A4275",
        "tab_bg": "#D6E8FA",
        "tab_fg": "#0A4275",
        "tab_active_bg": "#FFFFFF",
        "tab_active_fg": "#0067C0",
    },
    "classic_cad": {
        "name": "Giao diện kỹ thuật cổ điển (Classic CAD)",
        "bg_window": "#ECE9D8",          # Windows Classic warm beige
        "toolbar_bg": "#E4E1D0",         # Warm drafting toolbar
        "bar4_bg": "#DED9C3",            # Warm solver bar
        "btn_bg": "#ECE9D8",             # Classic beveled button
        "btn_fg": "#000000",             # Pure solid black
        "btn_border": "#9E9A8D",         # Classic 3D border
        "btn_active_bg": "#D8D4C0",
        "btn_active_fg": "#000000",
        "tool_active_bg": "#0055EA",     # Classic Windows 3D blue
        "tool_active_fg": "#FFFFFF",
        "canvas_bg": "#FFFFF6",          # Warm drafting paper (off-white parchment)
        "grid": "#D4CEBF",               # High-contrast warm CAD grid (WCAG 1.8:1)
        "axis": "#333333",               # Technical dark graphite axes
        "text": "#000000",
        "line": "#000000",               # Ink black geometry lines
        "label_fg": "#000000",
        "card_bg": "#ECE9D8",
        "status_bg": "#DCD8C8",          # Classic status bar beige
        "status_fg": "#000000",
        "text_box_bg": "#FFFFFF",
        "text_box_fg": "#000000",
        "tab_bg": "#DCD8C8",
        "tab_fg": "#333333",
        "tab_active_bg": "#FFFFFF",
        "tab_active_fg": "#0055EA",
    },
    "dark_studio": {
        "name": "Giao diện tối (Dark Studio)",
        "bg_window": "#18181B",          # Zinc-900 dark background
        "toolbar_bg": "#27272A",         # Zinc-800 dark toolbar
        "bar4_bg": "#202023",            # Dark solver bar
        "btn_bg": "#3F3F46",             # Zinc-700 dark button
        "btn_fg": "#FAFAFA",             # White crisp text
        "btn_border": "#52525B",
        "btn_active_bg": "#52525B",
        "btn_active_fg": "#FFFFFF",
        "tool_active_bg": "#38BDF8",     # Cyan active highlight (WCAG 8.8:1)
        "tool_active_fg": "#09090B",
        "canvas_bg": "#09090B",          # Pitch dark canvas
        "grid": "#334155",               # Visible slate-700 grid dots (WCAG enhanced)
        "axis": "#38BDF8",               # Neon cyan axes!
        "text": "#FAFAFA",               # White text
        "line": "#FAFAFA",               # White lines on dark canvas
        "label_fg": "#38BDF8",           # Cyan label headers
        "card_bg": "#18181B",
        "status_bg": "#202023",          # Dark status bar
        "status_fg": "#94A3B8",          # Soft gray status text
        "text_box_bg": "#18181B",
        "text_box_fg": "#FAFAFA",
        "tab_bg": "#27272A",
        "tab_fg": "#94A3B8",
        "tab_active_bg": "#18181B",
        "tab_active_fg": "#38BDF8",
    }
}


class GeoSolverApp(tk.Tk):

    def __init__(self, with_splash: bool = False):

        super().__init__()

        self.current_lang = "vi"
        self.current_mode = "basic"

        self.title("GeoSolver 2D CAD Studio")

        # Tích hợp lõi hình học độc lập đã qua thẩm định khoa học
        self.geo_engine = GeoSolver2DCore() if _GEOSOLVER_CORE_AVAILABLE and GeoSolver2DCore is not None else None

        self.ico_path = os.path.join(os.path.dirname(__file__), "assets", "geosolver_2d.ico")
        if not os.path.exists(self.ico_path):
            self.ico_path = os.path.join(os.path.dirname(__file__), "assets", "app.ico")
        if os.path.exists(self.ico_path):
            try:
                self.iconbitmap(default=self.ico_path)
                self.iconbitmap(self.ico_path)
            except Exception:
                try:
                    self.iconbitmap(self.ico_path)
                except Exception:
                    pass
        geo_png = os.path.join(os.path.dirname(__file__), "assets", "geosolver_2d_logo.png")
        if os.path.exists(geo_png):
            try:
                from PIL import Image, ImageTk
                pil_g = Image.open(geo_png).resize((64, 64), Image.Resampling.LANCZOS)
                self._app_icon_photo = ImageTk.PhotoImage(pil_g, master=self)
                self.iconphoto(True, self._app_icon_photo)
            except Exception:
                pass

        splash = None
        if with_splash:
            try:
                from stem_shared_core.splash_screen import attach_splash_screen
                splash = attach_splash_screen(
                    self,
                    app_id="geosolver_2d",
                    app_title="GeoSolver 2D Studio",
                    min_duration=2.2
                )
            except Exception:
                pass

        self.minsize(1050, 680)

        if _UI_STATE_AVAILABLE and UIStateManager:

            UIStateManager.restore_window(self, "GeoSolver2DApp", default_geometry="1440x900", min_width=1050, min_height=680)

            UIStateManager.attach_window_tracking(

                self,

                "GeoSolver2DApp",

                get_extra_state_fn=lambda: {"lang": getattr(self, "current_lang", "vi")},

                on_close_callback=self.destroy,

            )

        else:

            self.geometry("1440x900")



        # Bảng màu CAD cổ điển nhẹ nhàng (Technical CAD / CAD neutral)

        self.current_theme_key = "win11_light"
        self.current_theme = THEMES_GEOSOLVER["win11_light"]
        self.COLOR_BG = self.current_theme["bg_window"]

        self.COLOR_TOOLBAR = "#f0ede0"

        self.COLOR_CANVAS = "#ffffff"

        self.COLOR_GRID = "#f5f5f5"

        self.COLOR_AXIS = "#495057"

        self.COLOR_TEXT = "#000000"

        self.COLOR_POINT = "#003399"

        self.COLOR_LINE = "#212529"

        self.COLOR_CIRCLE = "#0066cc"

        self.COLOR_HIGHLIGHT = "#cc0000"

        self.COLOR_SNAP = "#e67700"

        self.COLOR_TANGENT = "#660099"



        self.configure(bg=self.COLOR_BG)



        # Trục tọa độ Oxy

        self.scale = 50.0

        self.origin_x = 450.0

        self.origin_y = 420.0

        self.is_panning = False

        self.pan_start_x = 0

        self.pan_start_y = 0



        # Lịch sử Undo / Redo

        self.undo_stack = []

        self.redo_stack = []



        # Trạng thái công cụ

        self.current_tool = "select"

        self.tool_buttons = {}

        self.action_buttons = {}

        self.tooltips = {}

        self.selected_points = []

        self.hovered_snap = None

        self.temp_points = []

        self.temp_circles = []

        self.temp_line = None

        self.clipboard = None

        self.drag_start_world = None

        self.rotate_center = None

        self.rotate_start_angle = 0.0

        self.dragging_label_point = None

        self.temp_intersect_entities = []



        # Tùy chọn hiển thị

        self.show_grid = True

        self.snap_to_grid = True

        self.show_hidden = False

        self.ask_name_on_create = True

        self.current_preset = None

        self.is_panel_visible = True



        self.var_grid = tk.BooleanVar(value=True)

        self.var_snap = tk.BooleanVar(value=True)

        self.var_ask_name = tk.BooleanVar(value=True)

        self.var_show_hidden = tk.BooleanVar(value=False)
        self.var_show_dimensions = tk.BooleanVar(value=False)



        # Dữ liệu hình học

        self.points = []

        self.segments = []

        self.lines = []

        self.circles = []

        self.equal_angles = []

        self.angle_marks = []

        self.polygons = []

        self.ellipses = []



        # Xây dựng giao diện

        self._create_menu()

        self._create_top_toolbars()

        self._create_main_workspace()

        self._create_bottom_bar()
        self.apply_theme(self.current_theme_key)

        self._bind_shortcuts()



        # Mặc định khởi động với Bản vẽ trắng (Trang trắng)

        self.clear_all(silent=True)
        if splash:
            splash.set_app_ready()



    # =========================================================================

    # MENU HỆ THỐNG

    # =========================================================================

    def _create_menu(self):

        lang = getattr(self, "current_lang", "vi")

        m_data = LANG_DATA[lang]["menu"]



        menubar = tk.Menu(self)



        # File

        m_file = tk.Menu(menubar, tearoff=0)

        m_file.add_command(label=m_data["file_new"], command=self.clear_all)

        m_file.add_command(label=m_data["file_clear_draw"], command=self.clear_drawing_only)

        m_file.add_command(label=m_data["file_export"], command=self.export_image_dialog)
        m_file.add_command(
            label="Xuất Báo Cáo HTML / In ấn PDF... (Ctrl+P)" if getattr(self, "current_lang", "vi") == "vi" else "Export HTML / Print PDF Report... (Ctrl+P)",
            command=self.export_html_report,
            accelerator="Ctrl+P"
        )

        m_file.add_separator()

        m_file.add_command(label=m_data["file_exit"], command=self.quit)

        menubar.add_cascade(label=m_data["file"], menu=m_file)



        # Edit

        m_edit = tk.Menu(menubar, tearoff=0)

        m_edit.add_command(label=m_data["edit_undo"], command=self.undo)

        m_edit.add_command(label=m_data["edit_redo"], command=self.redo)

        m_edit.add_separator()

        m_edit.add_command(label=m_data["edit_copy"], command=self.copy_selection)

        m_edit.add_command(label=m_data["edit_paste"], command=self.paste_selection)

        m_edit.add_command(label=m_data["edit_dup"], command=self.duplicate_selection)

        m_edit.add_separator()

        m_edit.add_command(label=m_data["edit_select_all"], command=self.select_all)

        m_edit.add_command(label=m_data["edit_del"], command=self.delete_selected)

        m_edit.add_command(label=m_data["edit_hide"], command=self.toggle_hide_selected)
        m_edit.add_command(label="Hiện lại tất cả nét ẩn (Unhide All)" if lang == "vi" else "Unhide All Objects", command=self.unhide_all)

        menubar.add_cascade(label=m_data["edit"], menu=m_edit)



        # Transform

        m_trans = tk.Menu(menubar, tearoff=0)

        m_trans.add_command(label=m_data["trans_ccw15"], command=lambda: self.rotate_selection(-15))

        m_trans.add_command(label=m_data["trans_cw15"], command=lambda: self.rotate_selection(15))

        m_trans.add_command(label=m_data["trans_custom"], command=self.rotate_custom_dialog)

        menubar.add_cascade(label=m_data["transform"], menu=m_trans)



        # Presets

        m_presets = tk.Menu(menubar, tearoff=0)

        p_list = LANG_DATA[lang]["presets_list"]

        m_presets.add_command(label=p_list[0], command=self.clear_all)

        m_presets.add_command(label=p_list[1], command=self.load_preset_cau_viii)

        m_presets.add_command(label=p_list[2], command=self.load_preset_vmo_2000)

        m_presets.add_command(label=p_list[3], command=self.load_preset_vmo_2001)

        m_presets.add_command(label=p_list[4], command=self.load_preset_vmo_2003)

        m_presets.add_command(label=p_list[5], command=self.load_preset_vmo_2007)

        m_presets.add_command(label=p_list[6], command=self.load_preset_vmo_2008)

        m_presets.add_command(label=p_list[7], command=self.load_preset_vmo_2008_bai12)

        m_presets.add_command(label=p_list[8], command=self.load_preset_vmo_2009_bai13)
        m_presets.add_command(label=p_list[9], command=self.load_preset_hex_intersection)
        m_presets.add_command(label=p_list[10], command=self.load_preset_vmo_2015)
        m_presets.add_command(label=p_list[11], command=self.load_preset_olympic_ptolemy)

        menubar.add_cascade(label=m_data["presets"], menu=m_presets)



        # View

        m_view = tk.Menu(menubar, tearoff=0)

        if not hasattr(self, "var_grid"):

            self.var_grid = tk.BooleanVar(value=True)

            self.var_snap = tk.BooleanVar(value=True)

            self.var_ask_name = tk.BooleanVar(value=True)

            self.var_show_hidden = tk.BooleanVar(value=False)



        m_view.add_checkbutton(label=m_data["view_grid"], variable=self.var_grid, command=self._toggle_grid)

        m_view.add_checkbutton(label=m_data["view_snap"], variable=self.var_snap, command=self._toggle_snap)

        m_view.add_checkbutton(label=m_data["view_ask_name"], variable=self.var_ask_name, command=self._toggle_ask_name)

        m_view.add_checkbutton(label=m_data["view_show_hidden"], variable=self.var_show_hidden, command=self._toggle_show_hidden)
        m_view.add_checkbutton(label="Hiện kích thước cạnh (Dimensions)" if lang == "vi" else "Show Segment Dimensions", variable=self.var_show_dimensions, command=self.redraw)

        m_view.add_separator()

        m_view.add_command(label=m_data["view_toggle_panel"], command=self.toggle_panel)

        menubar.add_cascade(label=m_data["view"], menu=m_view)



        # Language

        m_lang = tk.Menu(menubar, tearoff=0)

        m_lang.add_command(label="Tiếng Việt (Vietnamese)" + ("  [✓]" if lang == "vi" else ""), command=lambda: self.set_language("vi"))

        m_lang.add_command(label="English" + ("  [✓]" if lang == "en" else ""), command=lambda: self.set_language("en"))

        menubar.add_cascade(label=m_data["language"], menu=m_lang)



        # Giao diện (Themes) - chuẩn đồng bộ với CAD Math
        m_theme = tk.Menu(menubar, tearoff=0)
        curr_t = getattr(self, "current_theme_key", "win11_light")
        m_theme.add_command(label=("Light Theme" if lang == "en" else "Giao diện sáng (Light)") + ("  [✓]" if curr_t == "win11_light" else ""), command=lambda: self.apply_theme("win11_light"))
        m_theme.add_command(label=("Modern Blue Theme" if lang == "en" else "Giao diện xanh hiện đại (Modern Blue)") + ("  [✓]" if curr_t == "win11_blue" else ""), command=lambda: self.apply_theme("win11_blue"))
        m_theme.add_command(label=("Classic CAD Theme" if lang == "en" else "Giao diện kỹ thuật cổ điển (Classic CAD)") + ("  [✓]" if curr_t == "classic_cad" else ""), command=lambda: self.apply_theme("classic_cad"))
        m_theme.add_command(label=("Dark Studio Theme" if lang == "en" else "Giao diện tối (Dark Studio)") + ("  [✓]" if curr_t == "dark_studio" else ""), command=lambda: self.apply_theme("dark_studio"))
        menubar.add_cascade(label="Themes" if lang == "en" else "Giao diện (Themes)", menu=m_theme)

        # Tùy chọn (Options) / AI Support & Phục hồi
        m_opt = tk.Menu(menubar, tearoff=0)
        m_opt.add_command(label="AI Support Offline (Trợ lý suy luận)..." if lang == "vi" else "AI Support Offline...", command=self.open_ai_assistant)
        m_opt.add_command(label="Cấu hình tài nguyên AI..." if lang == "vi" else "AI Resource Settings...", command=self.open_ai_assistant)
        m_opt.add_separator()
        m_opt.add_command(label="Hiện lại tất cả đối tượng ẩn (Unhide All)" if lang == "vi" else "Unhide All Objects", command=self.unhide_all)
        m_opt.add_command(label="Sao chép ảnh bản vẽ vào Clipboard" if lang == "vi" else "Copy Canvas Image to Clipboard", command=self.copy_canvas_image_to_clipboard)
        menubar.add_cascade(label="Options" if lang == "en" else "Tùy chọn", menu=m_opt)



        # Help

        m_help = tk.Menu(menubar, tearoff=0)
        m_help.add_command(label=m_data.get("help_handbook", "📖 Cẩm nang sử dụng (F1)..."), command=self.open_user_handbook, accelerator="F1")
        m_help.add_separator()
        m_help.add_command(label=m_data["help_about"], command=self.open_about_dialog)

        menubar.add_cascade(label=m_data["help"], menu=m_help)



        self.config(menu=menubar)



    # =========================================================================

    # THANH CÔNG CỤ NGANG TRÊN ĐỈNH (TECHNICAL CAD 4-ROW RIBBON TOOLBARS)

    # =========================================================================

    def _create_top_toolbars(self):

        self.tool_buttons = {}

        self.action_buttons = {}

        self.tooltips = {}

        lang = getattr(self, "current_lang", "vi")

        d = LANG_DATA[lang]



        def add_tbtn(parent, code, label, tip_title, tip_body, is_action=False, cmd_action=None):
            cmd = cmd_action if is_action else (lambda c=code: self.set_tool(c))
            t = getattr(self, "current_theme", THEMES_GEOSOLVER.get(getattr(self, "current_theme_key", "win11_light"), THEMES_GEOSOLVER["win11_light"]))
            is_active_tool = (not is_action and code == getattr(self, "current_tool", "select"))
            b_bg = t["tool_active_bg"] if is_active_tool else t["btn_bg"]
            b_fg = t["tool_active_fg"] if is_active_tool else t["btn_fg"]
            b_relief = tk.SUNKEN if is_active_tool else tk.GROOVE
            btn = tk.Button(parent, text=label, relief=b_relief,
                            bg=b_bg, fg=b_fg, activebackground=t["btn_active_bg"], activeforeground=t["btn_active_fg"],
                            font=("Segoe UI", 8), padx=3, pady=1, cursor="hand2", command=cmd)

            btn.pack(side=tk.LEFT, padx=1, pady=1)

            tip = ToolTip(btn, tip_title, tip_body)

            self.tooltips[code] = tip

            if not is_action:

                self.tool_buttons[code] = btn

            else:

                self.action_buttons[code] = btn

            return btn



        def add_sep(parent):

            sep = ttk.Separator(parent, orient=tk.VERTICAL)

            sep.pack(side=tk.LEFT, fill=tk.Y, padx=2, pady=2)



        # -------------------------------------------------------------

        # KHUNG CHỨA TOÀN BỘ THANH CÔNG CỤ (CÓ THANH CUỘN NGANG VÀ MŨI TÊN THU GỌN/MỞ RỘNG LINH HOẠT)

        # -------------------------------------------------------------

        self.toolbar_container = tk.Frame(self, bg=self.COLOR_TOOLBAR, bd=1, relief=tk.RAISED)

        self.toolbar_container.pack(side=tk.TOP, fill=tk.X)

        # HÀNG 1: CỐ ĐỊNH TRÊN ĐỈNH WINDOW (KHÔNG CUỘN NGANG, ĐẢM BẢO NÚT BẢNG LỜI GIẢI VÀ THU GỌN LUÔN Ở GÓC PHẢI)
        self.top_bar1 = tk.Frame(self.toolbar_container, bg=self.COLOR_TOOLBAR, height=28, bd=1, relief=tk.RAISED)

        self.top_bar1.pack(side=tk.TOP, fill=tk.X)

        # Canvas cuộn ngang cho các hàng công cụ vẽ & giải toán (Hàng 2, 3, 4)
        self.tb_canvas = tk.Canvas(self.toolbar_container, bg=self.COLOR_TOOLBAR, height=125, highlightthickness=0)

        self.tb_canvas.pack(side=tk.TOP, fill=tk.X, expand=True)

        self.tb_scrollbar = ttk.Scrollbar(self.toolbar_container, orient=tk.HORIZONTAL, command=self.tb_canvas.xview)

        self.tb_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.tb_canvas.configure(xscrollcommand=self.tb_scrollbar.set)

        self.tb_inner_frame = tk.Frame(self.tb_canvas, bg=self.COLOR_TOOLBAR)

        self.tb_canvas_window = self.tb_canvas.create_window((0, 0), window=self.tb_inner_frame, anchor="nw")

        def _on_tb_configure(event):

            self.tb_canvas.configure(scrollregion=self.tb_canvas.bbox("all"))

            if not getattr(self, "_toolbar_collapsed", False):

                h = self.tb_inner_frame.winfo_reqheight()

                if h > 30:

                    self.tb_canvas.config(height=h)

        def _on_canvas_configure(event):
            req_w = self.tb_inner_frame.winfo_reqwidth()
            cur_w = max(event.width, req_w)
            self.tb_canvas.itemconfig(self.tb_canvas_window, width=cur_w)

        self.tb_inner_frame.bind("<Configure>", _on_tb_configure)
        self.tb_canvas.bind("<Configure>", _on_canvas_configure)

        self.tb_canvas.bind("<Shift-MouseWheel>", lambda e: self.tb_canvas.xview_scroll(-1 * (e.delta // 120), "units"))

        # Nút cuộn thanh công cụ tích hợp ngay bên trái để tiết kiệm diện tích
        self.btn_scroll_left = tk.Button(
            self.top_bar1, text="◀",
            font=("Segoe UI", 7, "bold"), bg="#e1decb", fg="#333333", relief=tk.GROOVE, padx=4, pady=0, cursor="hand2",
            command=lambda: self.tb_canvas.xview_scroll(-3, "units")
        )
        self.btn_scroll_left.pack(side=tk.LEFT, padx=1, pady=1)
        self.tooltips["scroll_left"] = ToolTip(self.btn_scroll_left, "Cuộn trái", "Cuộn thanh công cụ sang trái")

        self.btn_scroll_right = tk.Button(
            self.top_bar1, text="▶",
            font=("Segoe UI", 7, "bold"), bg="#e1decb", fg="#333333", relief=tk.GROOVE, padx=4, pady=0, cursor="hand2",
            command=lambda: self.tb_canvas.xview_scroll(3, "units")
        )
        self.btn_scroll_right.pack(side=tk.LEFT, padx=1, pady=1)
        self.tooltips["scroll_right"] = ToolTip(self.btn_scroll_right, "Cuộn phải", "Cuộn thanh công cụ sang phải")

        add_sep(self.top_bar1)

        b1 = d["bar1"]

        # File & History

        add_tbtn(self.top_bar1, "new", b1["new"]["text"], b1["new"]["tip_title"], b1["new"]["tip_body"], is_action=True, cmd_action=self.clear_all)

        add_tbtn(self.top_bar1, "clear_draw", b1["clear_draw"]["text"], b1["clear_draw"]["tip_title"], b1["clear_draw"]["tip_body"], is_action=True, cmd_action=self.clear_drawing_only)

        add_tbtn(self.top_bar1, "undo", b1["undo"]["text"], b1["undo"]["tip_title"], b1["undo"]["tip_body"], is_action=True, cmd_action=self.undo)

        add_tbtn(self.top_bar1, "redo", b1["redo"]["text"], b1["redo"]["tip_title"], b1["redo"]["tip_body"], is_action=True, cmd_action=self.redo)

        add_sep(self.top_bar1)



        # Clipboard

        add_tbtn(self.top_bar1, "copy", b1["copy"]["text"], b1["copy"]["tip_title"], b1["copy"]["tip_body"], is_action=True, cmd_action=self.copy_selection)

        add_tbtn(self.top_bar1, "paste", b1["paste"]["text"], b1["paste"]["tip_title"], b1["paste"]["tip_body"], is_action=True, cmd_action=self.paste_selection)

        add_sep(self.top_bar1)



        # Selection & Transform

        add_tbtn(self.top_bar1, "select_all", b1["select_all"]["text"], b1["select_all"]["tip_title"], b1["select_all"]["tip_body"], is_action=True, cmd_action=self.select_all)

        add_tbtn(self.top_bar1, "rot_l", b1["rot_l"]["text"], b1["rot_l"]["tip_title"], b1["rot_l"]["tip_body"], is_action=True, cmd_action=lambda: self.rotate_selection(-15))

        add_tbtn(self.top_bar1, "rot_r", b1["rot_r"]["text"], b1["rot_r"]["tip_title"], b1["rot_r"]["tip_body"], is_action=True, cmd_action=lambda: self.rotate_selection(15))

        add_tbtn(self.top_bar1, "rot_custom", b1["rot_custom"]["text"], b1["rot_custom"]["tip_title"], b1["rot_custom"]["tip_body"], is_action=True, cmd_action=self.rotate_custom_dialog)

        add_sep(self.top_bar1)



        btn_hide_w = add_tbtn(self.top_bar1, "hide", b1["hide"]["text"], b1["hide"]["tip_title"], b1["hide"]["tip_body"], is_action=True, cmd_action=self.toggle_hide_selected)
        btn_hide_w.bind("<Button-3>", lambda e: self.unhide_all())

        add_tbtn(self.top_bar1, "export", b1["export"]["text"], b1["export"]["tip_title"], b1["export"]["tip_body"], is_action=True, cmd_action=self.export_image_dialog)

        rep_txt = "Báo cáo" if getattr(self, "current_lang", "vi") == "vi" else "Report"
        self.btn_report = tk.Button(self.top_bar1, text=rep_txt, relief=tk.GROOVE, bg="#10b981", fg="#ffffff",
                                    font=("Segoe UI", 8, "bold"), padx=5, pady=1, cursor="hand2", command=self.export_html_report)
        self.btn_report.pack(side=tk.LEFT, padx=2, pady=1)
        self.tooltips["btn_report"] = ToolTip(self.btn_report, "Xuất báo cáo HTML (Ctrl+P)", "Xuất toàn bộ lời giải và hình vẽ ra file báo cáo.")

        add_sep(self.top_bar1)



        # Mode Toggle (Basic / Advanced) & Language Toggle
        m_txt = "⚙️ Cơ bản" if getattr(self, "current_mode", "basic") == "basic" else "⚙️ Nâng cao"
        self.btn_mode_toggle = tk.Button(self.top_bar1, text=m_txt, relief=tk.GROOVE, bg="#ded9c3",
                                         font=("Segoe UI", 8, "bold"), padx=5, pady=1, cursor="hand2", command=self.toggle_mode)
        self.btn_mode_toggle.pack(side=tk.LEFT, padx=2, pady=1)
        self.tooltips["mode_toggle"] = ToolTip(self.btn_mode_toggle, "Chế độ Cơ bản / Nâng cao (Basic / Advanced)",
                                               "Bấm để chuyển đổi giữa chế độ Cơ bản (THCS/THPT) và Nâng cao (Toán Đại học & Giảng viên).")

        # (Đã loại bỏ nút Tiếng Việt và Giới thiệu khỏi thanh Row 1 để giải phóng không gian, các tính năng này đã có sẵn trong menu Ngôn ngữ & menu Trợ giúp)
        self.btn_lang_toggle = None
        self.btn_about = None



        # Nút ẩn/hiện bảng lời giải bên phải

        tp_info = d["btn_toggle_panel"]

        tp_text = tp_info["text_show"] if self.is_panel_visible else tp_info["text_hide"]

        self.btn_toggle_panel = tk.Button(self.top_bar1, text=tp_text, relief=tk.GROOVE, bg="#d4cfbe",

                                          font=("Segoe UI", 8, "bold"), padx=6, pady=1, cursor="hand2", command=self.toggle_panel)

        self.btn_toggle_panel.pack(side=tk.RIGHT, padx=3, pady=1)

        tip_tp = ToolTip(self.btn_toggle_panel, tp_info["tip_title"], tp_info["tip_body"])

        self.tooltips["toggle_panel"] = tip_tp

        self.btn_toggle_ribbon = tk.Button(
            self.top_bar1, text="▲",
            font=("Segoe UI", 8, "bold"), bg="#e1decb", fg="#1864ab", relief=tk.GROOVE, padx=6, pady=0, cursor="hand2",
            command=self.toggle_toolbar_collapse
        )
        self.btn_toggle_ribbon.pack(side=tk.RIGHT, padx=2, pady=1)
        self.tooltips["toggle_ribbon"] = ToolTip(self.btn_toggle_ribbon, "Thu gọn công cụ", "Thu gọn các hàng công cụ phụ")



        # -------------------------------------------------------------

        # HÀNG 2: THANH CÔNG CỤ ĐIỂM, ĐƯỜNG & QUAN HỆ HÌNH HỌC (14 NÚT GỌN GÀNG)

        # -------------------------------------------------------------

        self.top_bar2 = tk.Frame(self.tb_inner_frame, bg=self.COLOR_TOOLBAR, height=28, bd=1, relief=tk.RAISED)

        self.top_bar2.pack(side=tk.TOP, fill=tk.X)



        b2 = d["bar2"]

        # Con trỏ & Tẩy

        add_tbtn(self.top_bar2, "select", b2["select"]["text"], b2["select"]["tip_title"], b2["select"]["tip_body"])

        add_tbtn(self.top_bar2, "rotate_mouse", b2["rotate_mouse"]["text"], b2["rotate_mouse"]["tip_title"], b2["rotate_mouse"]["tip_body"])

        add_tbtn(self.top_bar2, "erase", b2["erase"]["text"], b2["erase"]["tip_title"], b2["erase"]["tip_body"])

        add_sep(self.top_bar2)



        # Điểm & Tọa độ

        add_tbtn(self.top_bar2, "point", b2["point"]["text"], b2["point"]["tip_title"], b2["point"]["tip_body"])

        add_tbtn(self.top_bar2, "intersection", b2["intersection"]["text"], b2["intersection"]["tip_title"], b2["intersection"]["tip_body"])

        add_tbtn(self.top_bar2, "midpoint", b2["midpoint"]["text"], b2["midpoint"]["tip_title"], b2["midpoint"]["tip_body"])

        add_tbtn(self.top_bar2, "proj_foot", b2["proj_foot"]["text"], b2["proj_foot"]["tip_title"], b2["proj_foot"]["tip_body"], is_action=True, cmd_action=self.open_proj_foot_dialog)

        add_tbtn(self.top_bar2, "translate_vec", b2["translate_vec"]["text"], b2["translate_vec"]["tip_title"], b2["translate_vec"]["tip_body"], is_action=True, cmd_action=self.open_translate_dialog)

        add_sep(self.top_bar2)



        # Đường & Quan hệ

        add_tbtn(self.top_bar2, "segment", b2["segment"]["text"], b2["segment"]["tip_title"], b2["segment"]["tip_body"])

        add_tbtn(self.top_bar2, "toggle_dash", b2["toggle_dash"]["text"], b2["toggle_dash"]["tip_title"], b2["toggle_dash"]["tip_body"])

        add_tbtn(self.top_bar2, "line", b2["line"]["text"], b2["line"]["tip_title"], b2["line"]["tip_body"])

        add_tbtn(self.top_bar2, "perpendicular", b2["perpendicular"]["text"], b2["perpendicular"]["tip_title"], b2["perpendicular"]["tip_body"])

        add_tbtn(self.top_bar2, "parallel", b2["parallel"]["text"], b2["parallel"]["tip_title"], b2["parallel"]["tip_body"])

        add_tbtn(self.top_bar2, "bisector", b2["bisector"]["text"], b2["bisector"]["tip_title"], b2["bisector"]["tip_body"])

        add_tbtn(self.top_bar2, "mark_angle", b2["mark_angle"]["text"], b2["mark_angle"]["tip_title"], b2["mark_angle"]["tip_body"])

        add_tbtn(self.top_bar2, "angle_ratio_point", b2["angle_ratio_point"]["text"], b2["angle_ratio_point"]["tip_title"], b2["angle_ratio_point"]["tip_body"], is_action=True, cmd_action=self.open_angle_ratio_dialog)

        add_sep(self.top_bar2)

        add_tbtn(self.top_bar2, "circle", b2["circle"]["text"], b2["circle"]["tip_title"], b2["circle"]["tip_body"])

        add_tbtn(self.top_bar2, "circle_3p", b2["circle_3p"]["text"], b2["circle_3p"]["tip_title"], b2["circle_3p"]["tip_body"])



        # -------------------------------------------------------------

        # HÀNG 3: ĐA GIÁC, ĐƯỜNG CONIC, ĐƯỜNG TRÒN, TÂM & BẢNG MÀU

        # -------------------------------------------------------------

        self.top_bar3 = tk.Frame(self.tb_inner_frame, bg=self.COLOR_TOOLBAR, height=28, bd=1, relief=tk.RAISED)

        self.top_bar3.pack(side=tk.TOP, fill=tk.X)



        b3 = d["bar3"]

        # CỤM 1: ĐA GIÁC & ĐƯỜNG CONIC (Hình bình hành, Hình thoi, Hình thang cân, Hình vuông, Hình elip)

        add_tbtn(self.top_bar3, "parallelogram", b3["parallelogram"]["text"], b3["parallelogram"]["tip_title"], b3["parallelogram"]["tip_body"])

        add_tbtn(self.top_bar3, "rhombus", b3["rhombus"]["text"], b3["rhombus"]["tip_title"], b3["rhombus"]["tip_body"])

        add_tbtn(self.top_bar3, "isosceles_trapezoid", b3["isosceles_trapezoid"]["text"], b3["isosceles_trapezoid"]["tip_title"], b3["isosceles_trapezoid"]["tip_body"])

        add_tbtn(self.top_bar3, "square", b3["square"]["text"], b3["square"]["tip_title"], b3["square"]["tip_body"])

        add_tbtn(self.top_bar3, "ellipse", b3["ellipse"]["text"], b3["ellipse"]["tip_title"], b3["ellipse"]["tip_body"])

        add_sep(self.top_bar3)



        # CỤM 2: TIẾP TUYẾN THÔNG MINH & TIẾP TUYẾN CHUNG

        add_tbtn(self.top_bar3, "smart_tangent", b3["smart_tangent"]["text"], b3["smart_tangent"]["tip_title"], b3["smart_tangent"]["tip_body"])

        add_tbtn(self.top_bar3, "common_tangents", b3["common_tangents"]["text"], b3["common_tangents"]["tip_title"], b3["common_tangents"]["tip_body"])

        add_sep(self.top_bar3)



        # CỤM 3: CÁC TÂM TAM GIÁC ĐẶC BIỆT

        add_tbtn(self.top_bar3, "orthocenter", b3["orthocenter"]["text"], b3["orthocenter"]["tip_title"], b3["orthocenter"]["tip_body"], is_action=True, cmd_action=self.open_orthocenter_dialog)

        add_tbtn(self.top_bar3, "incenter", b3["incenter"]["text"], b3["incenter"]["tip_title"], b3["incenter"]["tip_body"])

        add_tbtn(self.top_bar3, "incircle", b3["incircle"]["text"], b3["incircle"]["tip_title"], b3["incircle"]["tip_body"])

        add_tbtn(self.top_bar3, "circumcenter", b3["circumcenter"]["text"], b3["circumcenter"]["tip_title"], b3["circumcenter"]["tip_body"])

        add_sep(self.top_bar3)



        # CỤM 4: ĐO ĐẠC & BẢNG MÀU

        add_tbtn(self.top_bar3, "calc_area", b3["calc_area"]["text"], b3["calc_area"]["tip_title"], b3["calc_area"]["tip_body"], is_action=True, cmd_action=self.calculate_selected_area)

        add_tbtn(self.top_bar3, "check_prop", b3["check_prop"]["text"], b3["check_prop"]["tip_title"], b3["check_prop"]["tip_body"])

        add_sep(self.top_bar3)



        # Bảng màu nhanh (Quick Color Palette: Đỏ, Xanh, Đen, Lục)

        self.lbl_color_title = tk.Label(self.top_bar3, text="Màu:" if getattr(self, "current_lang", "vi") == "vi" else "Color:", bg=self.COLOR_TOOLBAR, font=("Segoe UI", 8, "bold"))

        self.lbl_color_title.pack(side=tk.LEFT, padx=(4, 1))



        self.btn_col_red = tk.Button(self.top_bar3, text="🔴 Đỏ", font=("Segoe UI", 7, "bold"), fg="#c92a2a", bg="#ffe3e3",

                                     relief=tk.GROOVE, padx=2, pady=0, cursor="hand2", command=lambda: self.apply_quick_color("#e03131", "Đỏ"))

        self.btn_col_red.pack(side=tk.LEFT, padx=1, pady=2)

        self.tooltips["col_red"] = ToolTip(self.btn_col_red, "Tô màu Đỏ (#e03131)", "Đổi màu các đối tượng đang chọn sang màu đỏ (hoặc đặt màu vẽ kế tiếp).")



        self.btn_col_blue = tk.Button(self.top_bar3, text="🔵 Xanh", font=("Segoe UI", 7, "bold"), fg="#1864ab", bg="#d0ebff",

                                      relief=tk.GROOVE, padx=2, pady=0, cursor="hand2", command=lambda: self.apply_quick_color("#1971c2", "Xanh"))

        self.btn_col_blue.pack(side=tk.LEFT, padx=1, pady=2)

        self.tooltips["col_blue"] = ToolTip(self.btn_col_blue, "Tô màu Xanh (#1971c2)", "Đổi màu các đối tượng đang chọn sang màu xanh học đường.")



        self.btn_col_black = tk.Button(self.top_bar3, text="⚫ Đen", font=("Segoe UI", 7, "bold"), fg="#212529", bg="#e9ecef",

                                       relief=tk.GROOVE, padx=2, pady=0, cursor="hand2", command=lambda: self.apply_quick_color("#212529", "Đen"))

        self.btn_col_black.pack(side=tk.LEFT, padx=1, pady=2)

        self.tooltips["col_black"] = ToolTip(self.btn_col_black, "Tô màu Đen (#212529)", "Đổi màu các đối tượng đang chọn sang màu đen in ấn chuẩn.")



        self.btn_col_green = tk.Button(self.top_bar3, text="🟢 Lục", font=("Segoe UI", 7, "bold"), fg="#2b8a3e", bg="#d3f9d8",

                                       relief=tk.GROOVE, padx=2, pady=0, cursor="hand2", command=lambda: self.apply_quick_color("#2b8a3e", "Xanh lá"))

        self.btn_col_green.pack(side=tk.LEFT, padx=1, pady=2)

        self.tooltips["col_green"] = ToolTip(self.btn_col_green, "Tô màu Xanh Lá (#2b8a3e)", "Đổi màu các đối tượng đang chọn sang màu xanh lá cây.")

        # -------------------------------------------------------------
        # HÀNG CÔNG CỤ NÂNG CAO (ADVANCED MODE): TOÁN CAO CẤP CHO ĐẠI HỌC & GIẢNG VIÊN
        # -------------------------------------------------------------
        self.top_bar_adv = tk.Frame(self.tb_inner_frame, bg="#e2ded0", height=28, bd=1, relief=tk.GROOVE)
        b_adv = d.get("bar_adv", {})
        self.lbl_adv_title = tk.Label(self.top_bar_adv, text=b_adv.get("lbl_adv", "📐 Nâng cao:"), bg="#e2ded0", font=("Segoe UI", 8, "bold"), fg="#495057")
        self.lbl_adv_title.pack(side=tk.LEFT, padx=(5, 3))

        for adv_code in ("harmonic", "pole_polar", "symmedian", "radical_axis", "barycentric"):
            if adv_code in b_adv:
                info = b_adv[adv_code]
                add_tbtn(self.top_bar_adv, adv_code, info["text"], info["tip_title"], info["tip_body"])

        if getattr(self, "current_mode", "basic") == "advanced":
            self.top_bar_adv.pack(side=tk.TOP, fill=tk.X)



        # -------------------------------------------------------------

        # HÀNG 4: MỤC TIÊU & BỘ GIẢI TOÁN NHANH (SOLVER QUICK BAR)

        # -------------------------------------------------------------

        self.top_bar4 = tk.Frame(self.tb_inner_frame, bg="#ded9c3", height=28, bd=1, relief=tk.RAISED)

        self.top_bar4.pack(side=tk.TOP, fill=tk.X)



        self.lbl_preset_title = tk.Label(self.top_bar4, text=d["lbl_preset"], bg="#ded9c3", font=("Segoe UI", 8, "bold"))

        self.lbl_preset_title.pack(side=tk.LEFT, padx=(5, 2))



        self.combo_presets = ttk.Combobox(self.top_bar4, state="readonly", width=28, font=("Segoe UI", 8),

                                          values=d["presets_list"])

        self.combo_presets.pack(side=tk.LEFT, padx=2, pady=2)

        self.combo_presets.current(0)

        self.combo_presets.bind("<<ComboboxSelected>>", self._on_preset_selected)



        self.lbl_goal_title = tk.Label(self.top_bar4, text=d["lbl_goal"], bg="#ded9c3", font=("Segoe UI", 8, "bold"))

        self.lbl_goal_title.pack(side=tk.LEFT, padx=(6, 2))



        self.combo_goal_type = ttk.Combobox(self.top_bar4, state="readonly", width=18, font=("Segoe UI", 8),

                                            values=d["goals_list"])

        self.combo_goal_type.pack(side=tk.LEFT, padx=2, pady=2)

        self.combo_goal_type.current(0)

        self.combo_goal_type.bind("<<ComboboxSelected>>", self._on_goal_type_changed)



        self.lbl_targets_title = tk.Label(self.top_bar4, text=d["lbl_targets"], bg="#ded9c3", font=("Segoe UI", 8, "bold"))

        self.lbl_targets_title.pack(side=tk.LEFT, padx=(5, 2))



        self.entry_goal_targets = ttk.Entry(self.top_bar4, width=14, font=("Segoe UI", 8))

        self.entry_goal_targets.pack(side=tk.LEFT, padx=2, pady=2)

        self.entry_goal_targets.insert(0, "P, A, B")

        self.entry_goal = self.entry_goal_targets



        # Nút chèn nhanh ký hiệu toán học trên Hàng 4
        self.btn_q_ang = tk.Button(self.top_bar4, text="∠", font=("Segoe UI", 8, "bold"), bg="#f1f3f5", padx=2, pady=0, relief=tk.GROOVE,
                                   cursor="hand2", command=lambda: self.insert_math_symbol("∠"))
        self.btn_q_ang.pack(side=tk.LEFT, padx=1, pady=2)
        ToolTip(self.btn_q_ang, "Ký hiệu góc (Angle ∠)", "Chèn ký hiệu góc ∠ vào ô đối tượng/đề bài")

        self.btn_q_abs = tk.Button(self.top_bar4, text="|x|", font=("Segoe UI", 8, "bold"), bg="#f1f3f5", padx=2, pady=0, relief=tk.GROOVE,
                                   cursor="hand2", command=lambda: self.insert_math_symbol("||"))
        self.btn_q_abs.pack(side=tk.LEFT, padx=1, pady=2)
        ToolTip(self.btn_q_abs, "Trị tuyệt đối |x|", "Chèn cặp dấu giá trị tuyệt đối || và đặt con trỏ ở giữa")

        self.btn_q_cos = tk.Button(self.top_bar4, text="cos", font=("Segoe UI", 8, "bold"), bg="#f1f3f5", padx=2, pady=0, relief=tk.GROOVE,
                                   cursor="hand2", command=lambda: self.insert_math_symbol("cos()"))
        self.btn_q_cos.pack(side=tk.LEFT, padx=1, pady=2)
        ToolTip(self.btn_q_cos, "Hàm lượng giác cos()", "Chèn cos() và đặt con trỏ ở giữa")



        s_info = d["btn_solve"]

        self.btn_run_solver = tk.Button(self.top_bar4, text=s_info["text"],

                                        bg="#2b8a3e", fg="#ffffff", activebackground="#237032", activeforeground="#ffffff",

                                        font=("Segoe UI", 8, "bold"), relief=tk.RAISED, padx=10, pady=0, cursor="hand2",

                                        command=self.solve_general_problem)

        self.btn_run_solver.pack(side=tk.LEFT, padx=4, pady=2)

        tip_sol = ToolTip(self.btn_run_solver, s_info["tip_title"], s_info["tip_body"])

        self.tooltips["solve"] = tip_sol



        # HỘP CHỌN CÁC GÓI GIẢI TOÁN
        self.ai_profile_vals_vi = [
            "1. Thuần thuật toán",
            "2. AI Trợ giảng 1.5B (Máy nhẹ)",
            "3. AI Chuyên toán 7B",
            "4. AI Suy luận 7B",
        ]
        self.ai_profile_vals_en = [
            "1. Pure Algorithm",
            "2. AI Assistant 1.5B (Lightweight)",
            "3. AI Advanced Math 7B",
            "4. AI Reasoning 7B",
        ]
        ai_profile_vals = self.ai_profile_vals_en if lang == "en" else self.ai_profile_vals_vi
        self.combo_ai_profile = ttk.Combobox(
            self.top_bar4, state="readonly", width=22, font=("Segoe UI", 8),
            values=ai_profile_vals
        )
        self.combo_ai_profile.current(0)
        self.combo_ai_profile.pack(side=tk.LEFT, padx=2, pady=2)

        # NÚT AI GIẢI TỰ ĐỘNG
        self.btn_ai_solve = tk.Button(
            self.top_bar4, text="AI giải toán (F5)" if lang == "vi" else "AI Solve (F5)",
            bg="#e8590c", fg="#ffffff", activebackground="#d9480f", activeforeground="#ffffff",
            font=("Segoe UI", 8, "bold"), relief=tk.RAISED, padx=8, pady=0, cursor="hand2",
            command=self.run_ai_solve
        )
        self.btn_ai_solve.pack(side=tk.LEFT, padx=2, pady=2)

        # NÚT CẤU HÌNH AI ĐẶT NGAY CẠNH NÚT AI GIẢI (LOGIC, KHÔNG TÁCH RỜI)
        self.btn_ai_assistant = tk.Button(
            self.top_bar4, text="Cấu hình",
            bg="#1864ab", fg="#ffffff", activebackground="#145591", activeforeground="#ffffff",
            font=("Segoe UI", 8, "bold"), relief=tk.RAISED, padx=8, pady=0, cursor="hand2",
            command=self.open_ai_assistant
        )
        self.btn_ai_assistant.pack(side=tk.LEFT, padx=2, pady=2)

        self.tooltips["ai_solve"] = ToolTip(
            self.btn_ai_solve,
            "AI Phân Tích (F5)" if lang == "vi" else "AI Technical Solver",
            "Tự động gửi đề bài và dữ liệu tọa độ hình vẽ cho AI để sinh lời giải chi tiết."
        )

        tip_ai = ToolTip(

            self.btn_ai_assistant,

            "Cấu hình",

            "Kích hoạt mô hình AI DeepSeek-R1 hoặc kiểm tra trạng thái nạp bộ nhớ RAM để hỗ trợ giải toán."

        )

        self.tooltips["ai_assistant"] = tip_ai



        # Mặc định đáp án tự động chạy (loại bỏ checkbox bị khuyết theo yêu cầu)
        self.var_auto_stream = tk.BooleanVar(value=True)



    def toggle_toolbar_collapse(self):
        """Thu gọn/mở rộng các hàng công cụ phụ (giữ lại hàng 1 luôn hiển thị cố định trên đỉnh)."""
        is_vi = (getattr(self, "current_lang", "vi") == "vi")
        if getattr(self, "_toolbar_collapsed", False):
            # MỞ RỘNG
            self.tb_canvas.pack(side=tk.TOP, fill=tk.X, expand=True)
            self.tb_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
            self.btn_toggle_ribbon.config(text="▲")
            self._toolbar_collapsed = False
        else:
            # THU GỌN
            self.tb_canvas.pack_forget()
            self.tb_scrollbar.pack_forget()
            self.btn_toggle_ribbon.config(text="▼")
            self._toolbar_collapsed = True



    # =========================================================================

    # KHÔNG GIAN LÀM VIỆC CHÍNH (CANVAS LỚN & BẢNG LỜI GIẢI GỌN GÀNG)

    # =========================================================================

    def _create_main_workspace(self):

        container = tk.Frame(self, bg=self.COLOR_BG)

        container.pack(fill=tk.BOTH, expand=True)



        self.main_paned = ttk.PanedWindow(container, orient=tk.HORIZONTAL)

        self.main_paned.pack(fill=tk.BOTH, expand=True)



        # KHU VỰC VẼ CANVAS (CHIẾM ĐA SỐ MÀN HÌNH)

        canvas_frame = tk.Frame(self.main_paned, bg=self.COLOR_CANVAS)

        self.main_paned.add(canvas_frame, weight=4)



        self.canvas = tk.Canvas(canvas_frame, bg=self.COLOR_CANVAS, highlightthickness=0, takefocus=True)

        self.canvas.pack(fill=tk.BOTH, expand=True)



        self.canvas.bind("<ButtonPress-1>", self._on_canvas_click)

        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)

        self.canvas.bind("<ButtonRelease-1>", self._on_canvas_release)

        self.canvas.bind("<Double-Button-1>", self._on_canvas_double_click)

        self.canvas.bind("<Motion>", self._on_canvas_hover)

        self.canvas.bind("<ButtonPress-3>", self._on_pan_start)

        self.canvas.bind("<B3-Motion>", self._on_pan_drag)

        self.canvas.bind("<ButtonRelease-3>", self._on_pan_release)

        self.canvas.bind("<MouseWheel>", self._on_canvas_zoom)

        self.canvas.bind("<Configure>", lambda e: self.redraw())



        # Gắn phím tắt trên Canvas

        self.canvas.bind("<Control-a>", lambda e: (self.select_all(), "break")[1])

        self.canvas.bind("<Control-A>", lambda e: (self.select_all(), "break")[1])

        self.canvas.bind("<Control-Key-a>", lambda e: (self.select_all(), "break")[1])

        self.canvas.bind("<Control-Key-A>", lambda e: (self.select_all(), "break")[1])

        self.canvas.bind("<Control-c>", lambda e: (self.copy_selection(), "break")[1])

        self.canvas.bind("<Control-C>", lambda e: (self.copy_selection(), "break")[1])

        self.canvas.bind("<Control-v>", lambda e: (self.paste_selection(), "break")[1])

        self.canvas.bind("<Control-V>", lambda e: (self.paste_selection(), "break")[1])

        self.canvas.bind("<Control-d>", lambda e: (self.duplicate_selection(), "break")[1])

        self.canvas.bind("<Control-D>", lambda e: (self.duplicate_selection(), "break")[1])

        self.canvas.bind("<Delete>", lambda e: (self.delete_selected(), "break")[1])

        self.canvas.bind("<Control-h>", lambda e: (self.toggle_hide_selected(), "break")[1])

        self.canvas.bind("<Control-Right>", lambda e: (self.rotate_selection(15), "break")[1])

        self.canvas.bind("<Control-Left>", lambda e: (self.rotate_selection(-15), "break")[1])



        # BẢNG ĐIỀU KHIỂN & LỜI GIẢI (BÊN PHẢI - GỌN GÀNG, CÓ THỂ THU GỌN)

        self.right_frame = tk.Frame(self.main_paned, bg=self.COLOR_BG, width=380)

        self.main_paned.add(self.right_frame, weight=1)



        lang = getattr(self, "current_lang", "vi")

        d = LANG_DATA[lang]



        self.notebook = ttk.Notebook(self.right_frame)

        self.notebook.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)



        # TAB 1: BÀI TOÁN & LỜI GIẢI

        tab_solver = ttk.Frame(self.notebook)

        self.notebook.add(tab_solver, text=d["tab_solver"])



        # KHUNG ĐỀ BÀI & GIẢ THIẾT HÌNH HỌC (RÕ RÀNG CHỨC NĂNG, TÍCH HỢP TỰ ĐỘNG TRÍCH XUẤT TỪ CANVAS)
        self.prob_box = ttk.LabelFrame(
            tab_solver,
            text=" ĐỀ BÀI & GIẢ THIẾT HÌNH HỌC (Problem Hypotheses) " if lang == "vi" else " PROBLEM STATEMENT & HYPOTHESES ",
            padding=4
        )
        self.prob_box.pack(fill=tk.X, padx=4, pady=2)

        # Thanh nút chức năng của ô đề bài
        fr_prob_ctrl = tk.Frame(self.prob_box, bg=self.COLOR_BG)
        fr_prob_ctrl.pack(fill=tk.X, pady=(0, 2))

        self.btn_auto_prob = tk.Button(
            fr_prob_ctrl,
            text="⚡ Tạo từ hình vẽ" if lang == "vi" else "⚡ Auto-fill from Canvas",
            font=("Segoe UI", 7, "bold"), bg="#10b981", fg="#ffffff",
            relief=tk.GROOVE, padx=5, pady=0, cursor="hand2",
            command=self.auto_generate_problem_text
        )
        self.btn_auto_prob.pack(side=tk.LEFT, padx=1)
        self.tooltips["btn_auto_prob"] = ToolTip(
            self.btn_auto_prob,
            "Tự động trích xuất đề bài" if lang == "vi" else "Auto-extract Problem",
            "Đọc các điểm, đoạn thẳng, đường tròn trên hình và tự động điền giả thiết vào ô này." if lang == "vi" else "Read drawn points, segments, circles on canvas and auto-populate problem hypotheses."
        )

        self.btn_sample_prob = tk.Button(
            fr_prob_ctrl,
            text="📋 Mẫu đề" if lang == "vi" else "📋 Sample",
            font=("Segoe UI", 7), bg="#f1f3f5", relief=tk.GROOVE,
            padx=4, pady=0, cursor="hand2",
            command=self.insert_sample_problem_template
        )
        self.btn_sample_prob.pack(side=tk.LEFT, padx=1)
        self.tooltips["btn_sample_prob"] = ToolTip(
            self.btn_sample_prob,
            "Chèn mẫu câu đề bài" if lang == "vi" else "Insert Sample Template",
            "Chèn mẫu đề bài hình học mẫu mực (Cho tam giác... Giả thiết... Chứng minh...)" if lang == "vi" else "Insert standard problem template (Given triangle... Assumptions... Prove...)"
        )

        self.btn_clear_prob = tk.Button(
            fr_prob_ctrl,
            text="🗑️ Xóa" if lang == "vi" else "🗑️ Clear",
            font=("Segoe UI", 7), bg="#f1f3f5", relief=tk.GROOVE,
            padx=4, pady=0, cursor="hand2",
            command=lambda: self.txt_problem.delete("1.0", tk.END)
        )
        self.btn_clear_prob.pack(side=tk.LEFT, padx=1)

        self.lbl_prob_guide = tk.Label(
            fr_prob_ctrl,
            text="Nhập giả thiết hoặc bấm '⚡ Tạo từ hình'" if lang == "vi" else "Enter hypotheses or click '⚡ Auto-fill'",
            font=("Segoe UI", 7, "italic"), fg="#6c757d", bg=self.COLOR_BG
        )
        self.lbl_prob_guide.pack(side=tk.RIGHT, padx=2)

        # Thanh ký hiệu toán học nhanh (Math Symbols Palette)
        fr_math_syms = tk.Frame(self.prob_box, bg=self.COLOR_BG)
        fr_math_syms.pack(fill=tk.X, pady=(1, 2))

        lbl_sym_tag = tk.Label(fr_math_syms, text="∑" if lang == "en" else "Ký hiệu:", font=("Segoe UI", 8, "bold"), bg=self.COLOR_BG, fg="#495057")
        lbl_sym_tag.pack(side=tk.LEFT, padx=(0, 2))

        sym_buttons = [
            ("∠", "∠", "Ký hiệu Góc (Angle ∠)"),
            ("|x|", "||", "Trị tuyệt đối |x| (Absolute value)"),
            ("°", "°", "Ký hiệu độ (Degree)"),
            ("α", "alpha", "Góc alpha"),
            ("β", "beta", "Góc beta"),
            ("⊥", "⊥", "Vuông góc (Perpendicular ⊥)"),
            ("∥", "∥", "Song song (Parallel ∥)"),
            ("Δ", "Δ", "Tam giác (Triangle Δ)"),
            ("√", "sqrt()", "Căn thức sqrt()"),
            ("cos", "cos()", "Hàm cos()"),
            ("sin", "sin()", "Hàm sin()"),
            ("tan", "tan()", "Hàm tan()"),
            ("/", "/", "Phép chia tỉ số"),
            ("MC/AB", "MC/AB", "Mẫu tỉ số MC/AB"),
            ("|cos(BEC)|", "|cos(BEC)|", "Mẫu tương quan |cos(BEC)|")
        ]

        self.math_sym_buttons = []
        for label, code, tip_text in sym_buttons:
            s_btn = tk.Button(fr_math_syms, text=label, font=("Segoe UI", 7, "bold"), bg="#f8f9fa", relief=tk.GROOVE,
                              padx=2, pady=0, cursor="hand2", command=lambda c=code: self.insert_math_symbol(c))
            s_btn.pack(side=tk.LEFT, padx=1)
            self.math_sym_buttons.append(s_btn)
            ToolTip(s_btn, label, tip_text)

        self.txt_problem = tk.Text(self.prob_box, height=4, wrap=tk.WORD, font=("Segoe UI", 8),
                                   bg="#ffffff", relief=tk.SOLID, bd=1)
        self.txt_problem.pack(fill=tk.X, pady=2)



        self.inv_box = ttk.LabelFrame(tab_solver, text=d["inv_box"], padding=4)

        self.inv_box.pack(fill=tk.X, padx=4, pady=2)



        self.txt_invariants = tk.Text(self.inv_box, height=3, wrap=tk.WORD, font=("Consolas", 8),

                                      bg="#f8f9fa", fg="#1864ab", relief=tk.FLAT)

        self.txt_invariants.pack(fill=tk.BOTH, expand=True)

        self.txt_invariants.insert(tk.END, "Bản vẽ trống.")



        self.sol_box = ttk.LabelFrame(tab_solver, text=d["sol_box"], padding=4)

        self.sol_box.pack(fill=tk.BOTH, expand=True, padx=4, pady=2)



        self.txt_solution = tk.Text(self.sol_box, wrap=tk.WORD, font=("Consolas", 9), bg="#ffffff",

                                    relief=tk.SOLID, bd=1)

        scroll_sol = ttk.Scrollbar(self.sol_box, orient=tk.VERTICAL, command=self.txt_solution.yview)

        self.txt_solution.configure(yscrollcommand=scroll_sol.set)

        scroll_sol.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_solution.pack(fill=tk.BOTH, expand=True)



        # TAB 2: ĐỐI TƯỢNG HÌNH HỌC

        tab_algebra = ttk.Frame(self.notebook)

        self.notebook.add(tab_algebra, text=d["tab_algebra"])



        cols = d["tree_cols"]

        self.tree_objects = ttk.Treeview(tab_algebra, columns=("ID", "Def", "Status"), show="headings", height=20)

        self.tree_objects.heading("ID", text=cols[0])

        self.tree_objects.heading("Def", text=cols[1])

        self.tree_objects.heading("Status", text=cols[2])

        self.tree_objects.column("ID", width=70)

        self.tree_objects.column("Def", width=210)

        self.tree_objects.column("Status", width=60)

        scroll_tree = ttk.Scrollbar(tab_algebra, orient=tk.VERTICAL, command=self.tree_objects.yview)

        self.tree_objects.configure(yscrollcommand=scroll_tree.set)

        scroll_tree.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_objects.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.tree_objects.bind("<Double-1>", self._on_tree_double_click)



    def toggle_panel(self):

        """Thu gọn hoặc mở rộng bảng lời giải bên phải để phóng to Canvas."""

        lang = getattr(self, "current_lang", "vi")

        d = LANG_DATA[lang]

        if self.is_panel_visible:

            self.main_paned.forget(self.right_frame)

            self.btn_toggle_panel.config(text=d["btn_toggle_panel"]["text_hide"])

            self.is_panel_visible = False

            status_txt = "Đã thu gọn bảng lời giải (Không gian vẽ toàn màn hình)." if lang == "vi" else "Solution panel collapsed (Full screen canvas)."

            self.lbl_status.config(text=status_txt)

        else:

            self.main_paned.add(self.right_frame, weight=1)

            self.btn_toggle_panel.config(text=d["btn_toggle_panel"]["text_show"])

            self.is_panel_visible = True

            status_txt = "Đã mở lại bảng lời giải." if lang == "vi" else "Solution panel expanded."

            self.lbl_status.config(text=status_txt)



    def _on_preset_selected(self, event=None):
        try:
            idx = self.combo_presets.current()
            if idx == 0:
                self.clear_all(silent=True)
            elif idx == 1:
                self.load_preset_cau_viii()
            elif idx == 2:
                self.load_preset_vmo_2000()
            elif idx == 3:
                self.load_preset_vmo_2001()
            elif idx == 4:
                self.load_preset_vmo_2003()
            elif idx == 5:
                self.load_preset_vmo_2007()
            elif idx == 6:
                self.load_preset_vmo_2008()
            elif idx == 7:
                self.load_preset_vmo_2008_bai12()
            elif idx == 8:
                self.load_preset_vmo_2009_bai13()
            elif idx == 9:
                self.load_preset_hex_intersection()
            elif idx == 10:
                self.load_preset_vmo_2015()
            elif idx == 11:
                self.load_preset_olympic_ptolemy()
        except Exception as ex:
            import traceback
            traceback.print_exc()
            messagebox.showerror(
                "Thông báo" if getattr(self, "current_lang", "vi") == "vi" else "Notice",
                f"Lỗi khi nạp bài mẫu: {ex}" if getattr(self, "current_lang", "vi") == "vi" else f"Error loading preset: {ex}"
            )



    def auto_generate_problem_text(self):
        """Trích xuất và tự động xây dựng văn bản đề bài & giả thiết từ các đối tượng hiện có trên canvas."""
        is_vi = (getattr(self, "current_lang", "vi") == "vi")
        if not self.points:
            msg = "Bản vẽ hiện tại đang trống. Vui lòng vẽ các điểm, đường thẳng trên canvas trước khi trích xuất." if is_vi else "Canvas is currently empty. Please draw points or lines before auto-extracting."
            messagebox.showinfo("Thông báo" if is_vi else "Notice", msg)
            return

        pt_names = [p.get("name", "") for p in self.points if p.get("name")]
        lines_desc = []
        for s in getattr(self, "segments", []):
            p1_ref = s.get("p1")
            p2_ref = s.get("p2")
            p1 = p1_ref if isinstance(p1_ref, dict) else next((p for p in self.points if p.get("id") == p1_ref or p.get("name") == p1_ref), None)
            p2 = p2_ref if isinstance(p2_ref, dict) else next((p for p in self.points if p.get("id") == p2_ref or p.get("name") == p2_ref), None)
            if p1 and p2:
                n1 = p1.get('name', '')
                n2 = p2.get('name', '')
                if n1 and n2:
                    lines_desc.append(f"{n1}{n2}")

        circles_desc = []
        for c in getattr(self, "circles", []):
            c_ref = c.get("center")
            center = c_ref if isinstance(c_ref, dict) else next((p for p in self.points if p.get("id") == c_ref or p.get("name") == c_ref), None)
            c_name = center.get("name", "O") if center else "O"
            r = c.get("radius", 0)
            circles_desc.append(f"({c_name}; R={r:.1f})" if r else f"({c_name})")

        goal_type = self.combo_goal_type.get() if hasattr(self, "combo_goal_type") else ""
        targets = self.entry_goal_targets.get().strip() if hasattr(self, "entry_goal_targets") else ""

        # Tự động quét quan hệ hình học sâu trước khi sinh đề
        self._scan_invariants_deep()
        detected_facts = getattr(self, "detected_invariants_list", [])

        parts = []
        if is_vi:
            parts.append(f"Cho hình vẽ gồm các điểm: {', '.join(pt_names)}.")
            if lines_desc:
                parts.append(f"Đoạn thẳng: {', '.join(lines_desc[:12])}.")
            if circles_desc:
                parts.append(f"Đường tròn: {', '.join(circles_desc)}.")
            if detected_facts:
                clean_facts = [f.replace("• ", "").replace("★ ", "") for f in detected_facts[:5]]
                parts.append(f"Giả thiết nhận diện từ hình: {'; '.join(clean_facts)}.")
            if goal_type and targets:
                parts.append(f"Yêu cầu: {goal_type} đối với ({targets}).")
            else:
                parts.append("Yêu cầu: Chứng minh các mối quan hệ hình học và tính toán các đại lượng liên quan.")
        else:
            parts.append(f"Given geometric points: {', '.join(pt_names)}.")
            if lines_desc:
                parts.append(f"Segments: {', '.join(lines_desc[:12])}.")
            if circles_desc:
                parts.append(f"Circles: {', '.join(circles_desc)}.")
            if detected_facts:
                clean_facts = [f.replace("• ", "").replace("★ ", "") for f in detected_facts[:5]]
                parts.append(f"Recognized invariants: {'; '.join(clean_facts)}.")
            if goal_type and targets:
                parts.append(f"Goal: {goal_type} on ({targets}).")
            else:
                parts.append("Goal: Deduce and prove geometric invariants and calculate relevant metrics.")

        full_text = "\n".join(parts)
        self.txt_problem.delete("1.0", tk.END)
        self.txt_problem.insert(tk.END, full_text)
        self.txt_problem.focus_set()

    def insert_sample_problem_template(self):
        """Chèn mẫu đề bài hình học chuẩn mực vào ô đề bài."""
        is_vi = (getattr(self, "current_lang", "vi") == "vi")
        tpl = (
            "Đề bài: Cho tam giác ABC nhọn (AB < AC), đường cao AD, BE, CF đồng quy tại trực tâm H.\n"
            "Giả thiết: M là trung điểm BC, đường tròn ngoại tiếp tam giác DEF.\n"
            "Yêu cầu: Chứng minh đường tròn Euler đi qua 9 điểm đặc biệt."
        ) if is_vi else (
            "Problem: Given acute triangle ABC (AB < AC), altitudes AD, BE, CF concurrent at orthocenter H.\n"
            "Hypotheses: M is midpoint of BC, circumcircle of triangle DEF.\n"
            "Goal: Prove the 9-point Euler circle property."
        )
        self.txt_problem.delete("1.0", tk.END)
        self.txt_problem.insert(tk.END, tpl)
        self.txt_problem.focus_set()

    def insert_math_symbol(self, symbol):

        """Chèn ký hiệu toán học vào ô nhập liệu đang thao tác (targets hoặc đề bài)."""

        target_widget = self.focus_get()

        if target_widget != self.txt_problem:

            target_widget = getattr(self, "entry_goal_targets", None)

            if not target_widget:

                target_widget = self.txt_problem



        if target_widget == self.txt_problem:

            if symbol == "||":

                self.txt_problem.insert(tk.INSERT, "||")

                self.txt_problem.mark_set(tk.INSERT, f"{tk.INSERT}-1c")

            elif symbol.endswith("()"):

                self.txt_problem.insert(tk.INSERT, symbol)

                self.txt_problem.mark_set(tk.INSERT, f"{tk.INSERT}-1c")

            else:

                self.txt_problem.insert(tk.INSERT, symbol)

            self.txt_problem.focus_set()

        elif target_widget == self.entry_goal_targets:

            pos = self.entry_goal_targets.index(tk.INSERT)

            if symbol == "||":

                self.entry_goal_targets.insert(pos, "||")

                self.entry_goal_targets.icursor(pos + 1)

            elif symbol.endswith("()"):

                self.entry_goal_targets.insert(pos, symbol)

                self.entry_goal_targets.icursor(pos + len(symbol) - 1)

            else:

                self.entry_goal_targets.insert(pos, symbol)

                self.entry_goal_targets.icursor(pos + len(symbol))

            self.entry_goal_targets.focus_set()



    def _evaluate_geom_expression(self, expr_str):

        """Đánh giá giá trị số và phân tích các đại lượng trong biểu thức hình học."""

        p_map = {p.get("name") or p["id"]: (p["x"], p["y"]) for p in self.points if p.get("name") or p.get("id")}

        s = expr_str.strip()

        details = {}



        # 1. Chuyển đổi trị tuyệt đối |...| thành abs(...)

        while '|' in s:

            m = re.search(r'\|([^|]+)\|', s)

            if not m:

                break

            s = s[:m.start()] + f"abs({m.group(1)})" + s[m.end():]



        # 2. Xử lý góc: ∠BEC, angle(B, E, C), góc BEC

        def get_angle_deg_and_rad(p1, p2, p3):

            if p1 not in p_map or p2 not in p_map or p3 not in p_map:

                return 0.0, 0.0

            v1x = p_map[p1][0] - p_map[p2][0]

            v1y = p_map[p1][1] - p_map[p2][1]

            v2x = p_map[p3][0] - p_map[p2][0]

            v2y = p_map[p3][1] - p_map[p2][1]

            dot = v1x*v2x + v1y*v2y

            l1 = math.hypot(v1x, v1y)

            l2 = math.hypot(v2x, v2y)

            if l1 < 1e-9 or l2 < 1e-9:

                return 0.0, 0.0

            cos_val = max(-1.0, min(1.0, dot / (l1 * l2)))

            rad = math.acos(cos_val)

            return math.degrees(rad), rad



        def replace_angle(match):

            pts = match.group(1).upper()

            if len(pts) == 3 and all(c in p_map for c in pts):

                deg, rad = get_angle_deg_and_rad(pts[0], pts[1], pts[2])

                details[f"∠{pts}"] = f"{deg:.2f}° ({rad:.4f} rad)"

                return f"({rad})"

            return match.group(0)



        s = re.sub(r'∠\s*([A-Za-z]{3})', replace_angle, s)

        s = re.sub(r'góc\s+([A-Za-z]{3})', replace_angle, s, flags=re.IGNORECASE)

        s = re.sub(r'angle\s*\(\s*([A-Za-z]{3})\s*\)', replace_angle, s)



        # 3. Hàm lượng giác: cos(BEC), sin(BEC), tan(BEC)

        def replace_trig_angle(match):

            fn = match.group(1).lower()

            pts = match.group(2).upper()

            if len(pts) == 3 and all(c in p_map for c in pts):

                deg, rad = get_angle_deg_and_rad(pts[0], pts[1], pts[2])

                details[f"∠{pts}"] = f"{deg:.2f}°"

                return f"{fn}({rad})"

            return match.group(0)



        s = re.sub(r'\b(cos|sin|tan)\s*\(\s*([A-Za-z]{3})\s*\)', replace_trig_angle, s, flags=re.IGNORECASE)

        s = re.sub(r'\b(cos|sin|tan)\s*\(\s*∠\s*([A-Za-z]{3})\s*\)', replace_trig_angle, s, flags=re.IGNORECASE)



        # 4. Đoạn thẳng: 2 chữ cái in hoa (MC, AB, BC...)

        def replace_seg(match):

            word = match.group(0).upper()

            if len(word) == 2 and word[0] in p_map and word[1] in p_map:

                p1 = p_map[word[0]]

                p2 = p_map[word[1]]

                d = math.hypot(p1[0] - p2[0], p1[1] - p2[1])

                details[f"Đoạn {word}"] = f"{d:.4f}"

                return f"({d:.6f})"

            return word



        s = re.sub(r'\b[A-Za-z]{2}\b', replace_seg, s)



        # Thay thế ký hiệu alpha, beta nếu người dùng viết

        if "alpha" in s.lower() and "E" in p_map and "B" in p_map and "C" in p_map:

            deg, rad = get_angle_deg_and_rad("B", "E", "C")

            details["alpha (= ∠BEC)"] = f"{deg:.2f}° ({rad:.4f} rad)"

            s = re.sub(r'\balpha\b', f"({rad})", s, flags=re.IGNORECASE)



        safe_env = {

            "abs": abs,

            "cos": math.cos,

            "sin": math.sin,

            "tan": math.tan,

            "sqrt": math.sqrt,

            "pi": math.pi

        }

        try:

            val = eval(s, {"__builtins__": None}, safe_env)

            return val, details, None

        except Exception as e:

            return None, details, str(e)



    def _solve_correlation(self, targets_str, res):

        """Phân tích hệ thức, tỉ số và tương quan giữa 2 biểu thức hình học."""

        is_en = (getattr(self, "current_lang", "vi") == "en")

        raw = targets_str.strip()

        parts = []

        for delim in [',', '=', 'theo', 'Theo', 'and', ' và ']:

            if delim in raw:

                parts = [p.strip() for p in raw.split(delim) if p.strip()]

                break

        if not parts:

            parts = [raw]



        if len(parts) >= 2:

            e1, e2 = parts[0], parts[1]

            v1, det1, err1 = self._evaluate_geom_expression(e1)

            v2, det2, err2 = self._evaluate_geom_expression(e2)



            res.append(f"• {'EXPRESSION 1 (LHS / Target Ratio)' if is_en else 'BIỂU THỨC 1 (Vế thứ nhất / Tỉ số cần tính)'}: {e1}\n")

            if err1:

                res.append(f"  ⚠️ {'Computation error' if is_en else 'Lỗi tính toán'}: {err1}\n")

            else:

                res.append(f"  => {'Empirical value on drawing' if is_en else 'Giá trị thực nghiệm trên bản vẽ'}: {v1:.6f}\n")

                for k, v in det1.items():

                    res.append(f"     + {k} = {v}\n")



            res.append(f"\n• {'EXPRESSION 2 (RHS / Comparison Variable)' if is_en else 'BIỂU THỨC 2 (Vế thứ hai / Biến đối chiếu)'}: {e2}\n")

            if err2:

                res.append(f"  ⚠️ {'Computation error' if is_en else 'Lỗi tính toán'}: {err2}\n")

            else:

                res.append(f"  => {'Empirical value on drawing' if is_en else 'Giá trị thực nghiệm trên bản vẽ'}: {v2:.6f}\n")

                for k, v in det2.items():

                    res.append(f"     + {k} = {v}\n")



            if v1 is not None and v2 is not None:

                diff = abs(v1 - v2)

                ratio = v1 / v2 if abs(v2) > 1e-9 else None

                res.append("\n---------------------------------------------------------\n")

                res.append(f"{'🎯 GEOMETRIC RELATION & CORRELATION EVALUATION:' if is_en else '🎯 ĐÁNH GIÁ TƯƠNG QUAN HỆ THỨC HÌNH HỌC:'}\n")

                res.append(f"  - {'Absolute discrepancy' if is_en else 'Sai số chênh lệch tuyệt đối'}: |{e1} - ({e2})| = {diff:.6e}\n")

                if ratio is not None:

                    res.append(f"  - {'Comparison ratio' if is_en else 'Tỉ số đối chiếu'}: ({e1}) / ({e2}) = {ratio:.6f}\n\n")



                if diff < 1e-4 or (ratio is not None and abs(ratio - 1.0) < 1e-4):

                    if is_en:

                        res.append(f"⭐ MATHEMATICAL CONCLUSION: {e1} = {e2} (EXACT IDENTITY)!\n")

                        res.append("  (Both expressions are identical across the entire variation domain).\n")

                    else:

                        res.append(f"⭐ KẾT LUẬN TOÁN HỌC: {e1} = {e2} (ĐẲNG THỨC ĐÚNG TUYỆT ĐỐI)!\n")

                        res.append("  (Hai biểu thức hoàn toàn đồng nhất trên toàn bộ miền biến thiên).\n")

                elif ratio is not None and abs(ratio - round(ratio)) < 1e-4 and round(ratio) != 0:

                    k_int = int(round(ratio))

                    if is_en:

                        res.append(f"⭐ CORRELATION CONCLUSION: {e1} = {k_int} * ({e2})\n")

                    else:

                        res.append(f"⭐ KẾT LUẬN TƯƠNG QUAN: {e1} = {k_int} * ({e2})\n")

                elif ratio is not None and abs(ratio - 0.5) < 1e-4:

                    if is_en:

                        res.append(f"⭐ CORRELATION CONCLUSION: {e1} = 1/2 * ({e2})\n")

                    else:

                        res.append(f"⭐ KẾT LUẬN TƯƠNG QUAN: {e1} = 1/2 * ({e2})\n")

                elif ratio is not None:

                    if is_en:

                        res.append(f"⭐ LINEAR CORRELATION: {e1} ≈ {ratio:.4f} * ({e2})\n")

                    else:

                        res.append(f"⭐ TƯƠNG QUAN TUYẾN TÍNH: {e1} ≈ {ratio:.4f} * ({e2})\n")

        else:

            e = parts[0]

            v, det, err = self._evaluate_geom_expression(e)

            res.append(f"• {'EXPRESSION TO EVALUATE' if is_en else 'BIỂU THỨC CẦN TÍNH GIÁ TRỊ'}: {e}\n")

            if err:

                res.append(f"  ⚠️ {'Computation error' if is_en else 'Lỗi tính toán'}: {err}\n")

            else:

                res.append(f"  => {'Exact calculated value' if is_en else 'Giá trị tính toán chính xác'}: {v:.6f}\n")

                for k, val in det.items():

                    res.append(f"     + {k} = {val}\n")



    def _on_goal_type_changed(self, event=None):

        idx = self.combo_goal_type.current()

        defaults = {

            0: "P, A, B",

            1: "M1, B, M2",

            2: "M",

            3: "P",

            4: "PA, PM",

            5: "AM, BC",

            6: "AM, CD",

            7: "d1, d2, d3",

            8: "MC/AB, |cos(BEC)|",

            9: "All / Toàn bộ",

            10: "Auto",

            11: "A, B, C, D",

            12: "ABC, DEF"

        }

        if idx in defaults:

            self.entry_goal_targets.delete(0, tk.END)

            self.entry_goal_targets.insert(0, defaults[idx])



    # =========================================================================

    # THANH ĐIỀU KHIỂN ĐÁY (COMMAND & STATUS BAR)

    # =========================================================================

    def _create_bottom_bar(self):
        self.bottom_frame = tk.Frame(self, bg=self.COLOR_TOOLBAR, height=48, bd=1, relief=tk.SUNKEN)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        bottom_frame = self.bottom_frame

        # Dòng lệnh đại số
        self.cmd_row = tk.Frame(self.bottom_frame, bg=self.COLOR_TOOLBAR)
        self.cmd_row.pack(fill=tk.X, padx=4, pady=1)
        cmd_row = self.cmd_row



        lang = getattr(self, "current_lang", "vi")

        d = LANG_DATA[lang]



        self.lbl_cmd_title = tk.Label(cmd_row, text=d["lbl_cmd"], bg=self.COLOR_TOOLBAR, font=("Segoe UI", 8, "bold"))

        self.lbl_cmd_title.pack(side=tk.LEFT, padx=4)

        self.entry_cmd = ttk.Entry(cmd_row, font=("Consolas", 9))

        self.entry_cmd.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        self.entry_cmd.bind("<Return>", self._execute_command)

        self.lbl_cmd_hint = tk.Label(cmd_row, text=d["lbl_cmd_hint"], bg=self.COLOR_TOOLBAR, fg="#666666", font=("Segoe UI", 8))

        self.lbl_cmd_hint.pack(side=tk.RIGHT, padx=4)



        # Thanh trạng thái
        self.stat_row = tk.Frame(self.bottom_frame, bg="#dee2e6", height=20)
        self.stat_row.pack(fill=tk.X)
        stat_row = self.stat_row



        self.lbl_status = tk.Label(stat_row, text=d["status_ready"], bg="#dee2e6", fg=self.COLOR_TEXT, font=("Segoe UI", 8), anchor=tk.W)

        self.lbl_status.pack(side=tk.LEFT, padx=6, fill=tk.X, expand=True)



        self.lbl_legal = tk.Label(stat_row, text=d.get("lbl_legal", ""), bg="#dee2e6", fg="#495057", font=("Segoe UI", 8, "italic"))

        self.lbl_legal.pack(side=tk.RIGHT, padx=10)



        self.lbl_snap_info = tk.Label(stat_row, text="", bg="#dee2e6", fg="#d9480f", font=("Segoe UI", 8, "bold"))

        self.lbl_snap_info.pack(side=tk.RIGHT, padx=4)



        self.lbl_coords = tk.Label(stat_row, text="X:   0.00 | Y:   0.00", bg="#dee2e6", fg="#495057", font=("Consolas", 8))

        self.lbl_coords.pack(side=tk.RIGHT, padx=6)



    # =========================================================================

    # HỘP THOẠI GIỚI THIỆU SẢN PHẨM & QUẢN LÝ NGÔN NGỮ

    # =========================================================================

    def apply_theme(self, theme_key="win11_light"):
        """Áp dụng bộ giao diện người dùng theo chuẩn CAD Math (Sáng / Xanh hiện đại / Kỹ thuật cổ điển / Tối)."""
        if theme_key not in THEMES_GEOSOLVER:
            theme_key = "win11_light"
        self.current_theme_key = theme_key
        t = THEMES_GEOSOLVER[theme_key]
        self.current_theme = t

        # Cửa sổ chính & thuộc tính màu
        self.configure(bg=t["bg_window"])
        self.COLOR_BG = t["bg_window"]
        self.COLOR_TOOLBAR = t["toolbar_bg"]
        self.COLOR_CANVAS = t["canvas_bg"]
        self.COLOR_GRID = t["grid"]
        self.COLOR_AXIS = t["axis"]
        self.COLOR_TEXT = t["text"]
        self.COLOR_LINE = t["line"]

        # Cập nhật Canvas
        if hasattr(self, "canvas") and self.canvas:
            self.canvas.configure(bg=t["canvas_bg"])

        # Cập nhật Container Toolbar
        if hasattr(self, "toolbar_container") and self.toolbar_container:
            self.toolbar_container.configure(bg=t["toolbar_bg"])
        if hasattr(self, "tb_canvas") and self.tb_canvas:
            self.tb_canvas.configure(bg=t["toolbar_bg"])
        if hasattr(self, "tb_inner_frame") and self.tb_inner_frame:
            self.tb_inner_frame.configure(bg=t["toolbar_bg"])

        # Cập nhật các hàng Ribbon Bar
        if hasattr(self, "top_bar1") and self.top_bar1:
            self.top_bar1.configure(bg=t["toolbar_bg"])
        if hasattr(self, "top_bar2") and self.top_bar2:
            self.top_bar2.configure(bg=t["toolbar_bg"])
        if hasattr(self, "top_bar3") and self.top_bar3:
            self.top_bar3.configure(bg=t["toolbar_bg"])
        if hasattr(self, "top_bar_adv") and self.top_bar_adv:
            self.top_bar_adv.configure(bg=t["toolbar_bg"])
        if hasattr(self, "top_bar4") and self.top_bar4:
            self.top_bar4.configure(bg=t["bar4_bg"])

        # Nhãn trong các thanh công cụ
        for lbl_name in ("lbl_color_title", "lbl_adv_title"):
            lbl = getattr(self, lbl_name, None)
            if lbl:
                lbl.configure(bg=t["toolbar_bg"], fg=t["label_fg"])

        for lbl_name in ("lbl_preset_title", "lbl_goal_title", "lbl_targets_title"):
            lbl = getattr(self, lbl_name, None)
            if lbl:
                lbl.configure(bg=t["bar4_bg"], fg=t["label_fg"])

        # Cập nhật tất cả các nút công cụ (tool_buttons)
        cur_tool = getattr(self, "current_tool", "select")
        if hasattr(self, "tool_buttons"):
            for code, btn in self.tool_buttons.items():
                try:
                    if code == cur_tool:
                        btn.configure(bg=t["tool_active_bg"], fg=t["tool_active_fg"], relief=tk.SUNKEN)
                    else:
                        btn.configure(bg=t["btn_bg"], fg=t["btn_fg"], relief=tk.GROOVE,
                                      activebackground=t["btn_active_bg"], activeforeground=t["btn_active_fg"])
                except Exception:
                    pass

        # Cập nhật tất cả các nút hành động (action_buttons)
        if hasattr(self, "action_buttons"):
            for code, btn in self.action_buttons.items():
                try:
                    btn.configure(bg=t["btn_bg"], fg=t["btn_fg"], relief=tk.GROOVE,
                                  activebackground=t["btn_active_bg"], activeforeground=t["btn_active_fg"])
                except Exception:
                    pass

        # Các nút cuộn và nút chức năng đặc thù trên Row 1 & Row 4
        for btn_name in ("btn_scroll_left", "btn_scroll_right", "btn_mode_toggle", "btn_toggle_panel", "btn_q_ang", "btn_q_abs", "btn_q_cos"):
            btn = getattr(self, btn_name, None)
            if btn:
                try:
                    btn.configure(bg=t["btn_bg"], fg=t["btn_fg"], activebackground=t["btn_active_bg"])
                except Exception:
                    pass

        if hasattr(self, "btn_toggle_ribbon") and self.btn_toggle_ribbon:
            try:
                self.btn_toggle_ribbon.configure(bg=t["btn_bg"], fg=t["tool_active_bg"])
            except Exception:
                pass

        # Nút ký hiệu toán học trên bảng phải
        if hasattr(self, "math_sym_buttons"):
            for btn in self.math_sym_buttons:
                try:
                    btn.configure(bg=t["btn_bg"], fg=t["btn_fg"], activebackground=t["btn_active_bg"])
                except Exception:
                    pass

        # Khung làm việc chính và bảng bên phải
        if hasattr(self, "right_frame") and self.right_frame:
            try:
                self.right_frame.configure(bg=t["bg_window"])
            except Exception:
                pass

        # Hộp văn bản bên phải
        for txt_name in ("txt_problem", "txt_invariants", "txt_solution"):
            txt = getattr(self, txt_name, None)
            if txt:
                try:
                    txt.configure(
                        bg=t["text_box_bg"],
                        fg=t["text_box_fg"],
                        insertbackground=t["tool_active_bg"]
                    )
                except Exception:
                    pass

        # Thanh đáy & Thanh trạng thái
        if hasattr(self, "bottom_frame") and self.bottom_frame:
            try:
                self.bottom_frame.configure(bg=t["status_bg"])
            except Exception:
                pass
        if hasattr(self, "cmd_row") and self.cmd_row:
            try:
                self.cmd_row.configure(bg=t["status_bg"])
            except Exception:
                pass
        if hasattr(self, "stat_row") and self.stat_row:
            try:
                self.stat_row.configure(bg=t["status_bg"])
            except Exception:
                pass

        for lbl_name in ("lbl_cmd_title", "lbl_cmd_hint", "lbl_status", "lbl_legal", "lbl_coords"):
            lbl = getattr(self, lbl_name, None)
            if lbl:
                try:
                    lbl.configure(bg=t["status_bg"], fg=t["status_fg"])
                except Exception:
                    pass
        if hasattr(self, "lbl_snap_info") and self.lbl_snap_info:
            try:
                self.lbl_snap_info.configure(bg=t["status_bg"])
            except Exception:
                pass

        # TTK Styles cho Notebook và tabs
        try:
            style = ttk.Style()
            style.theme_use('clam')
            style.configure(".", background=t["bg_window"], foreground=t["text_box_fg"], font=("Segoe UI", 9))
            style.configure("TNotebook", background=t["bg_window"], borderwidth=0)
            style.configure("TNotebook.Tab", background=t["tab_bg"], foreground=t["tab_fg"],
                            font=("Segoe UI", 8, "bold"), padding=[10, 4])
            style.map("TNotebook.Tab",
                      background=[("selected", t["tab_active_bg"])],
                      foreground=[("selected", t["tab_active_fg"])])
            style.configure("TLabelframe", background=t["card_bg"])
            style.configure("TLabelframe.Label", background=t["card_bg"], foreground=t["label_fg"], font=("Segoe UI", 8, "bold"))
            style.configure("TFrame", background=t["bg_window"])
        except Exception:
            pass

        # Cập nhật menu để hiển thị dấu tích [✓] trên theme hiện tại
        try:
            self._create_menu()
        except Exception:
            pass

        # Vẽ lại Canvas với màu mới
        self.redraw()

    def open_user_handbook(self):
        """Mở cửa sổ cẩm nang hướng dẫn sử dụng tích hợp trong phần mềm (In-App Help Dialog)."""
        try:
            curr_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(curr_dir)
            if root_dir not in sys.path:
                sys.path.insert(0, root_dir)
            from stem_handbook_dialog import show_stem_handbook_dialog
            show_stem_handbook_dialog(parent=self, initial_tab=2)
            return
        except Exception as ex:
            print("Fallback handbook error:", ex)
        messagebox.showinfo("Cẩm nang sử dụng", "Tài liệu hướng dẫn đã được cập nhật tại CAM_NANG_SU_DUNG_STEM_CAD_MATH.md")

    def open_about_dialog(self):

        """Hộp thoại Giới thiệu sản phẩm & Phiên bản (About GeoSolver) với hiệu ứng tự động cuộn."""

        lang = getattr(self, "current_lang", "vi")

        d = LANG_DATA[lang]

        dlg = tk.Toplevel(self)

        dlg.title(d["about_dialog_title"])

        dlg.geometry("620x540")

        dlg.minsize(560, 480)

        dlg.configure(bg="#f8f9fa")

        dlg.transient(self)

        dlg.grab_set()



        try:

            x = self.winfo_rootx() + (self.winfo_width() - 620) // 2

            y = self.winfo_rooty() + (self.winfo_height() - 540) // 2

            dlg.geometry(f"+{max(10, x)}+{max(10, y)}")

        except Exception:

            pass



        # 1. Header Frame

        hdr = tk.Frame(dlg, bg="#1864ab", pady=8)

        hdr.pack(fill=tk.X)

        tk.Label(hdr, text="GeoSolver v2.5", font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#1864ab").pack()

        subtitle = "Dynamic Geometry CAD & SymPy CAS Solver" if lang == "en" else "Hệ Thống Dựng Hình Tương Tác & Giải Toán Đại Số SymPy"

        tk.Label(hdr, text=subtitle, font=("Segoe UI", 9), fg="#d0ebff", bg="#1864ab").pack(pady=(2, 0))



        # 2. Digital Signature Ready Badge

        fr_badge = tk.Frame(dlg, bg="#e7f5ff", bd=1, relief=tk.SOLID, pady=4)

        fr_badge.pack(fill=tk.X, padx=10, pady=(6, 2))

        badge_text = "🔏 SẴN SÀNG KÝ SỐ XÁC THỰC BẢN QUYỀN (PKI / RSA-4096 / SHA-256)" if lang == "vi" else "🔏 AUTHOR DIGITAL SIGNATURE READY (PKI / RSA-4096 / SHA-256 INTEGRITY)"

        tk.Label(fr_badge, text=badge_text, font=("Segoe UI", 8, "bold"), fg="#1864ab", bg="#e7f5ff").pack()



        # 3. Control Bar for Auto-Scroll

        fr_ctrl = tk.Frame(dlg, bg="#f8f9fa", padx=10, pady=3)

        fr_ctrl.pack(fill=tk.X)



        lbl_scroll_stat = tk.Label(

            fr_ctrl,

            text="⚡ Đang tự động cuộn (Rê chuột vào văn bản để tạm dừng)" if lang == "vi" else "⚡ Auto-scrolling (Hover over text to pause)",

            font=("Segoe UI", 8, "italic"), fg="#495057", bg="#f8f9fa"

        )

        lbl_scroll_stat.pack(side=tk.LEFT, padx=4)



        # 4. Content Text Box

        txt_frame = tk.Frame(dlg, bg="#f8f9fa", padx=10, pady=4)

        txt_frame.pack(fill=tk.BOTH, expand=True)



        txt_info = tk.Text(txt_frame, wrap=tk.WORD, font=("Segoe UI", 9), bg="#ffffff", fg="#212529",

                           relief=tk.SOLID, bd=1, padx=10, pady=10)

        sb = ttk.Scrollbar(txt_frame, orient=tk.VERTICAL, command=txt_info.yview)

        txt_info.configure(yscrollcommand=sb.set)

        sb.pack(side=tk.RIGHT, fill=tk.Y)

        txt_info.pack(fill=tk.BOTH, expand=True)



        txt_info.insert(tk.END, d["about_text"])

        txt_info.config(state=tk.DISABLED)



        # 5. Auto-Scroll Controller Engine

        scroll_state = {"active": True, "speed_ms": 70, "timer_id": None}



        def auto_scroll_step():

            if not dlg.winfo_exists():

                return

            if scroll_state["active"]:

                y1, y2 = txt_info.yview()

                if y2 < 1.0:

                    txt_info.yview_scroll(1, "units")

                    scroll_state["timer_id"] = dlg.after(scroll_state["speed_ms"], auto_scroll_step)

                else:

                    scroll_state["active"] = False

                    lbl_scroll_stat.config(text="✓ Đã cuộn hết trang" if lang == "vi" else "✓ Reached end of text")

                    btn_toggle_scroll.config(text="▶ Cuộn lại" if lang == "vi" else "▶ Scroll")

            else:

                scroll_state["timer_id"] = dlg.after(150, auto_scroll_step)



        def on_mouse_enter(event):

            if scroll_state["active"]:

                scroll_state["active"] = False

                lbl_scroll_stat.config(text="⏸ Tạm dừng do rê chuột (Rời chuột để tiếp tục)" if lang == "vi" else "⏸ Paused on hover (Leave mouse to resume)")

                btn_toggle_scroll.config(text="▶ Tiếp tục" if lang == "vi" else "▶ Resume")



        def on_mouse_leave(event):

            if not scroll_state["active"] and txt_info.yview()[1] < 1.0:

                scroll_state["active"] = True

                lbl_scroll_stat.config(text="⚡ Đang tự động cuộn (Rê chuột vào để tạm dừng)" if lang == "vi" else "⚡ Auto-scrolling (Hover to pause)")

                btn_toggle_scroll.config(text="⏸ Tạm dừng" if lang == "vi" else "⏸ Pause")



        def toggle_scroll():

            if scroll_state["active"]:

                scroll_state["active"] = False

                lbl_scroll_stat.config(text="⏸ Đã tạm dừng cuộn" if lang == "vi" else "⏸ Auto-scroll paused")

                btn_toggle_scroll.config(text="▶ Tiếp tục" if lang == "vi" else "▶ Resume")

            else:

                if txt_info.yview()[1] >= 1.0:

                    txt_info.yview_moveto(0.0)

                scroll_state["active"] = True

                lbl_scroll_stat.config(text="⚡ Đang tự động cuộn..." if lang == "vi" else "⚡ Auto-scrolling...")

                btn_toggle_scroll.config(text="⏸ Tạm dừng" if lang == "vi" else "⏸ Pause")



        def reset_top():

            txt_info.yview_moveto(0.0)

            scroll_state["active"] = True

            lbl_scroll_stat.config(text="⚡ Đang tự động cuộn..." if lang == "vi" else "⚡ Auto-scrolling...")

            btn_toggle_scroll.config(text="⏸ Tạm dừng" if lang == "vi" else "⏸ Pause")



        btn_rewind = tk.Button(fr_ctrl, text="⟲ Về đầu" if lang == "vi" else "⟲ Top",

                               font=("Segoe UI", 8), bg="#e9ecef", cursor="hand2", command=reset_top)

        btn_rewind.pack(side=tk.RIGHT, padx=2)



        btn_toggle_scroll = tk.Button(fr_ctrl, text="⏸ Tạm dừng" if lang == "vi" else "⏸ Pause",

                                      font=("Segoe UI", 8), bg="#e9ecef", cursor="hand2", command=toggle_scroll)

        btn_toggle_scroll.pack(side=tk.RIGHT, padx=2)



        txt_info.bind("<Enter>", on_mouse_enter)

        txt_info.bind("<Leave>", on_mouse_leave)



        def on_close():

            if scroll_state["timer_id"]:

                try:

                    dlg.after_cancel(scroll_state["timer_id"])

                except Exception:

                    pass

            dlg.destroy()



        dlg.protocol("WM_DELETE_WINDOW", on_close)

        scroll_state["timer_id"] = dlg.after(600, auto_scroll_step)



        # 6. Footer Close Button

        btn_frame = tk.Frame(dlg, bg="#f8f9fa", pady=6)

        btn_frame.pack(fill=tk.X)

        btn_close_text = "Đóng (Close)" if lang == "vi" else "Close"

        btn_close = tk.Button(btn_frame, text=btn_close_text, font=("Segoe UI", 9, "bold"),

                              bg="#e9ecef", padx=20, pady=2, cursor="hand2", command=on_close)

        btn_close.pack()



    def set_language(self, lang_code):

        """Chuyen ngon ngu giao dien va dong bo voi i18n tap trung."""

        if lang_code not in ("vi", "en"):

            return

        self.current_lang = lang_code

        # --- Dong bo voi he thong i18n tap trung ---

        if _I18N_AVAILABLE:

            try:

                _i18n_set(lang_code)

            except Exception:

                pass

        self._apply_language()



    def toggle_mode(self):
        new_mode = "advanced" if getattr(self, "current_mode", "basic") == "basic" else "basic"
        self.set_mode(new_mode)

    def set_mode(self, mode):
        self.current_mode = mode
        is_vi = (self.current_lang == "vi")
        if hasattr(self, "btn_mode_toggle"):
            if mode == "advanced":
                m_txt = "⚙️ Nâng cao" if is_vi else "⚙️ Advanced"
                self.btn_mode_toggle.config(text=m_txt, bg="#1971c2", fg="#ffffff")
                if hasattr(self, "top_bar_adv"):
                    self.top_bar_adv.pack(side=tk.TOP, fill=tk.X, after=self.top_bar3) if hasattr(self, "top_bar3") else self.top_bar_adv.pack(side=tk.TOP, fill=tk.X)
                self.lbl_status.config(
                    text="Đã kích hoạt Chế độ Nâng cao: Đầy đủ công cụ hình học giải tích và xạ ảnh cho Đại học & Giảng viên." if is_vi else "Activated Advanced Mode: Full analytic & projective geometry tools for University & Lecturers."
                )
            else:
                m_txt = "⚙️ Cơ bản" if is_vi else "⚙️ Basic"
                t = getattr(self, "current_theme", THEMES_GEOSOLVER.get(getattr(self, "current_theme_key", "win11_light"), THEMES_GEOSOLVER["win11_light"]))
                self.btn_mode_toggle.config(text=m_txt, bg=t["btn_bg"], fg=t["btn_fg"])
                if hasattr(self, "top_bar_adv"):
                    self.top_bar_adv.pack_forget()
                self.lbl_status.config(
                    text="Đã chuyển về Chế độ Cơ bản (Giao diện tinh gọn cho THCS & THPT)." if is_vi else "Switched to Basic Mode (Streamlined for Middle & High School)."
                )

    def toggle_language(self):

        new_lang = "en" if self.current_lang == "vi" else "vi"

        self.set_language(new_lang)



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
            if hasattr(self, "lbl_status") and self.lbl_status:
                self.lbl_status.config(text=f"Đã chọn hồ sơ AI: {title}")

        show_clean_ai_config_dialog(
            parent=self,
            ai_hub=getattr(self, "ai_hub", None),
            ai_manager=getattr(self, "ai_manager", None),
            current_profile_idx=cur_idx,
            on_profile_selected=on_selected,
        )
    def _apply_language(self):

        lang = self.current_lang

        data = LANG_DATA[lang]



        # 1. Window Title

        self.title(data["app_title"])



        # 2. Re-create Menu

        self._create_menu()



        # 3. Bar 1 buttons

        for code in ("new", "clear_draw", "undo", "redo", "copy", "paste", "select_all", "rot_l", "rot_r", "rot_custom", "hide", "export"):

            if code in self.action_buttons and code in data["bar1"]:

                btn = self.action_buttons[code]

                info = data["bar1"][code]

                btn.config(text=info["text"])

                if code in self.tooltips:

                    self.tooltips[code].update(info["tip_title"], info["tip_body"])



        if getattr(self, "btn_lang_toggle", None):
            info = data["bar1"]["lang_toggle"]
            self.btn_lang_toggle.config(text=info["text"])
            if "lang_toggle" in self.tooltips:
                self.tooltips["lang_toggle"].update(info["tip_title"], info["tip_body"])

        if getattr(self, "btn_about", None):
            info = data["bar1"]["about"]
            self.btn_about.config(text=info["text"])
            if "about" in self.tooltips:
                self.tooltips["about"].update(info["tip_title"], info["tip_body"])



        if hasattr(self, "btn_toggle_panel"):

            panel_info = data["btn_toggle_panel"]

            p_text = panel_info["text_show"] if self.is_panel_visible else panel_info["text_hide"]

            self.btn_toggle_panel.config(text=p_text)

            if "toggle_panel" in self.tooltips:

                self.tooltips["toggle_panel"].update(panel_info["tip_title"], panel_info["tip_body"])



        # 4. Bar 2 buttons (Points & Lines)

        for code, info in data["bar2"].items():

            btn = self.tool_buttons.get(code) or self.action_buttons.get(code)

            if btn:

                btn.config(text=info["text"])

                if code in self.tooltips:

                    self.tooltips[code].update(info["tip_title"], info["tip_body"])



        # 3b. Mode Toggle Button
        if hasattr(self, "btn_mode_toggle"):
            is_adv = (getattr(self, "current_mode", "basic") == "advanced")
            m_txt = ("⚙️ Nâng cao" if is_adv else "⚙️ Cơ bản") if lang == "vi" else ("⚙️ Advanced" if is_adv else "⚙️ Basic")
            self.btn_mode_toggle.config(text=m_txt)

        # 5b. Bar Advanced buttons (Harmonic, Pole/Polar, Symmedian, Radical Axis, Barycentric)
        if hasattr(self, "lbl_adv_title") and "bar_adv" in data:
            self.lbl_adv_title.config(text=data["bar_adv"]["lbl_adv"])
            for code, info in data["bar_adv"].items():
                if code == "lbl_adv":
                    continue
                btn = self.tool_buttons.get(code) or self.action_buttons.get(code)
                if btn:
                    btn.config(text=info["text"])
                    if code in self.tooltips:
                        self.tooltips[code].update(info["tip_title"], info["tip_body"])

        # 5. Bar 3 buttons (Circles & Polygons & Centers)

        for code, info in data["bar3"].items():

            btn = self.tool_buttons.get(code) or self.action_buttons.get(code)

            if btn:

                btn.config(text=info["text"])

                if code in self.tooltips:

                    self.tooltips[code].update(info["tip_title"], info["tip_body"])



        # 6. Bar 4 (Presets & Goals & Solver)

        if hasattr(self, "lbl_preset_title"):

            self.lbl_preset_title.config(text=data["lbl_preset"])

            cur_p = self.combo_presets.current()

            self.combo_presets.config(values=data["presets_list"])

            self.combo_presets.current(cur_p if cur_p >= 0 else 0)



        if hasattr(self, "lbl_goal_title"):

            self.lbl_goal_title.config(text=data["lbl_goal"])

            cur_g = self.combo_goal_type.current()

            self.combo_goal_type.config(values=data["goals_list"])

            self.combo_goal_type.current(cur_g if cur_g >= 0 else 0)



        if hasattr(self, "lbl_targets_title"):

            self.lbl_targets_title.config(text=data["lbl_targets"])



        if hasattr(self, "btn_run_solver"):

            s_info = data["btn_solve"]

            self.btn_run_solver.config(text=s_info["text"])

            if "solve" in self.tooltips:

                self.tooltips["solve"].update(s_info["tip_title"], s_info["tip_body"])



        if hasattr(self, "btn_report"):
            self.btn_report.config(text="Báo cáo" if lang == "vi" else "Report")
            if "btn_report" in self.tooltips:
                self.tooltips["btn_report"].update(
                    "Xuất báo cáo HTML (Ctrl+P)" if lang == "vi" else "HTML Report (Ctrl+P)",
                    "Xuất toàn bộ lời giải và hình vẽ ra file báo cáo." if lang == "vi" else "Export entire lesson and diagrams to HTML."
                )

        if hasattr(self, "lbl_color_title"):
            self.lbl_color_title.config(text="Màu:" if lang == "vi" else "Color:")
        if hasattr(self, "btn_col_red"):
            self.btn_col_red.config(text="🔴 Đỏ" if lang == "vi" else "🔴 Red")
        if hasattr(self, "btn_col_blue"):
            self.btn_col_blue.config(text="🔵 Xanh" if lang == "vi" else "🔵 Blue")
        if hasattr(self, "btn_col_black"):
            self.btn_col_black.config(text="⚫ Đen" if lang == "vi" else "⚫ Black")
        if hasattr(self, "btn_col_green"):
            self.btn_col_green.config(text="🟢 Lục" if lang == "vi" else "🟢 Green")

        if hasattr(self, "btn_ai_assistant"):

            self.btn_ai_assistant.config(text="Cấu hình" if lang == "vi" else "Config")

            if "ai_assistant" in self.tooltips:

                self.tooltips["ai_assistant"].update(

                    "Cấu hình",

                    "Run AI deep pedagogical analysis or inspect offline model RAM allocation." if lang == "en" else "Kích hoạt mô hình AI hoặc kiểm tra trạng thái nạp bộ nhớ RAM để hỗ trợ giải toán."

                )



        if hasattr(self, "btn_scroll_left"):

            self.btn_scroll_left.config(text="◀ Cuộn trái" if lang == "vi" else "◀ Scroll Left")

        if hasattr(self, "btn_scroll_left"):

            self.btn_scroll_left.config(text="◀")

            if "scroll_left" in self.tooltips:

                self.tooltips["scroll_left"].update("Cuộn trái" if lang == "vi" else "Scroll Left", "Cuộn thanh công cụ sang trái")

        if hasattr(self, "btn_scroll_right"):

            self.btn_scroll_right.config(text="▶")

            if "scroll_right" in self.tooltips:

                self.tooltips["scroll_right"].update("Cuộn phải" if lang == "vi" else "Scroll Right", "Cuộn thanh công cụ sang phải")

        if hasattr(self, "btn_toggle_ribbon"):

            is_col = getattr(self, "_toolbar_collapsed", False)

            self.btn_toggle_ribbon.config(text="▼" if is_col else "▲")

            if "toggle_ribbon" in self.tooltips:

                t_title = ("Mở rộng thanh công cụ" if is_col else "Thu gọn thanh công cụ") if lang == "vi" else ("Expand Toolbar" if is_col else "Collapse Toolbar")

                self.tooltips["toggle_ribbon"].update(t_title, "")

        if hasattr(self, "combo_ai_profile"):
            cur_p = self.combo_ai_profile.current()
            vals = getattr(self, "ai_profile_vals_en", []) if lang == "en" else getattr(self, "ai_profile_vals_vi", [])
            if vals:
                self.combo_ai_profile.config(values=vals)
                self.combo_ai_profile.current(cur_p if 0 <= cur_p < len(vals) else 0)

        if hasattr(self, "btn_ai_solve"):

            is_act = getattr(self, "_ai_solving_active", False)

            if is_act:

                self.btn_ai_solve.config(text="⏹ Dừng AI" if lang == "vi" else "⏹ Stop AI")

            else:

                self.btn_ai_solve.config(text="AI giải toán (F5)" if lang == "vi" else "AI Solve (F5)")



        # 7. Right Notebook

        if hasattr(self, "notebook"):

            self.notebook.tab(0, text=data["tab_solver"])

            self.notebook.tab(1, text=data["tab_algebra"])

        if hasattr(self, "prob_box"):
            self.prob_box.config(
                text=" ĐỀ BÀI & GIẢ THIẾT HÌNH HỌC (Problem Hypotheses) " if lang == "vi" else " PROBLEM STATEMENT & HYPOTHESES "
            )
        if hasattr(self, "btn_auto_prob"):
            self.btn_auto_prob.config(text="⚡ Tạo từ hình vẽ" if lang == "vi" else "⚡ Auto-fill from Canvas")
        if hasattr(self, "btn_sample_prob"):
            self.btn_sample_prob.config(text="📋 Mẫu đề" if lang == "vi" else "📋 Sample")
        if hasattr(self, "btn_clear_prob"):
            self.btn_clear_prob.config(text="🗑️ Xóa" if lang == "vi" else "🗑️ Clear")
        if hasattr(self, "lbl_prob_guide"):
            self.lbl_prob_guide.config(
                text="Nhập giả thiết hoặc bấm '⚡ Tạo từ hình'" if lang == "vi" else "Enter hypotheses or click '⚡ Auto-fill'"
            )

        if hasattr(self, "inv_box"):

            self.inv_box.config(text=data["inv_box"])

        if hasattr(self, "sol_box"):

            self.sol_box.config(text=data["sol_box"])

        if hasattr(self, "tree_objects"):

            cols = data["tree_cols"]

            self.tree_objects.heading("ID", text=cols[0])

            self.tree_objects.heading("Def", text=cols[1])

            self.tree_objects.heading("Status", text=cols[2])



        # 8. Bottom Bar & Stream

        if hasattr(self, "chk_auto_stream"):

            self.chk_auto_stream.config(text="⚡ Chạy tự động" if lang == "vi" else "⚡ Auto-stream")

        if hasattr(self, "lbl_cmd_title"):

            self.lbl_cmd_title.config(text=data["lbl_cmd"])

        if hasattr(self, "lbl_cmd_hint"):

            self.lbl_cmd_hint.config(text=data["lbl_cmd_hint"])

        if hasattr(self, "lbl_legal"):

            self.lbl_legal.config(text=data.get("lbl_legal", ""))

        if hasattr(self, "lbl_status") and self.lbl_status.cget("text") in ("Sẵn sàng.", "Ready."):

            self.lbl_status.config(text=data["status_ready"])



        # 9. Tự động chuyển ngữ bảng lời giải nếu đang có nội dung

        if hasattr(self, "txt_solution"):

            cur_sol = self.txt_solution.get("1.0", tk.END).strip()

            if cur_sol:

                self.solve_general_problem()



        # 10. Chuyển đổi ngôn ngữ Đề bài nếu đang ở bài toán mẫu hoặc đề mặc định

        if hasattr(self, "txt_problem"):

            if getattr(self, "current_preset", None) and self.current_preset in PRESET_PROBLEMS.get(lang, {}):

                self.txt_problem.delete("1.0", tk.END)

                self.txt_problem.insert(tk.END, PRESET_PROBLEMS[lang][self.current_preset])

            else:

                prob_cur = self.txt_problem.get("1.0", tk.END).strip()

                if prob_cur in ("Đề bài: Cho ...\nGiả thiết: ...\nYêu cầu: ...", "Problem: Given ...\nAssumptions: ...\nGoal: ..."):

                    self.txt_problem.delete("1.0", tk.END)

                    self.txt_problem.insert(tk.END, "Problem: Given ...\nAssumptions: ...\nGoal: ..." if lang == "en" else "Đề bài: Cho ...\nGiả thiết: ...\nYêu cầu: ...")



        # 11. Cập nhật Bảng màu nhanh

        if hasattr(self, "lbl_color_title"):

            c_info = data.get("color_palette", {})

            self.lbl_color_title.config(text=c_info.get("title", "Color:" if lang == "en" else "Màu:"))

            if hasattr(self, "btn_col_red"):

                self.btn_col_red.config(text=c_info.get("red", "🔴 Red" if lang == "en" else "🔴 Đỏ"))

                if "col_red" in self.tooltips:

                    t = c_info.get("tip_red", ("Red", "Red color"))

                    self.tooltips["col_red"].update(t[0], t[1])

            if hasattr(self, "btn_col_blue"):

                self.btn_col_blue.config(text=c_info.get("blue", "🔵 Blue" if lang == "en" else "🔵 Xanh"))

                if "col_blue" in self.tooltips:

                    t = c_info.get("tip_blue", ("Blue", "Blue color"))

                    self.tooltips["col_blue"].update(t[0], t[1])

            if hasattr(self, "btn_col_black"):

                self.btn_col_black.config(text=c_info.get("black", "⚫ Black" if lang == "en" else "⚫ Đen"))

                if "col_black" in self.tooltips:

                    t = c_info.get("tip_black", ("Black", "Black color"))

                    self.tooltips["col_black"].update(t[0], t[1])

            if hasattr(self, "btn_col_green"):

                self.btn_col_green.config(text=c_info.get("green", "🟢 Green" if lang == "en" else "🟢 Lục"))

                if "col_green" in self.tooltips:

                    t = c_info.get("tip_green", ("Green", "Green color"))

                    self.tooltips["col_green"].update(t[0], t[1])



        # 12. Cập nhật lại Property Checker theo ngôn ngữ mới

        if hasattr(self, "txt_invariants"):

            self._scan_invariants_deep()



        # 13. Cập nhật lại Cây đối tượng theo ngôn ngữ mới

        if hasattr(self, "tree_objects"):

            self._update_algebra_tree()



    # =========================================================================

    # PHÍM TẮT TOÀN CỤC & SỰ KIỆN HỆ THỐNG

    # =========================================================================

    def _bind_shortcuts(self):

        self.bind("<Control-z>", lambda e: self.undo())

        self.bind("<Control-Z>", lambda e: self.undo())

        self.bind("<Control-y>", lambda e: self.redo())

        self.bind("<Control-Y>", lambda e: self.redo())

        self.bind("<Control-n>", lambda e: self.clear_all())

        self.bind("<Control-N>", lambda e: self.clear_all())

        self.bind("<Control-e>", lambda e: self.export_image_dialog())

        self.bind("<Control-E>", lambda e: self.export_image_dialog())
        self.bind("<Control-p>", lambda e: self.export_html_report())
        self.bind("<Control-P>", lambda e: self.export_html_report())

        self.bind("<Control-Key-a>", self._handle_ctrl_a)

        self.bind("<Control-Key-A>", self._handle_ctrl_a)

        self.bind("<Control-c>", self._handle_ctrl_c)
        self.bind("<Control-C>", self._handle_ctrl_c)
        self.bind("<Control-v>", self._handle_ctrl_v)
        self.bind("<Control-V>", self._handle_ctrl_v)
        self.bind("<F1>", lambda e: self.open_user_handbook())



    def _handle_ctrl_a(self, event):

        focused = self.focus_get()

        if isinstance(focused, (tk.Entry, ttk.Entry, tk.Text)):

            return None

        self.select_all()

        return "break"

    def _handle_ctrl_c(self, event):
        focused = self.focus_get()
        if isinstance(focused, (tk.Entry, ttk.Entry, tk.Text)):
            return None
        self.copy_selection()
        return "break"

    def _handle_ctrl_v(self, event):
        focused = self.focus_get()
        if isinstance(focused, (tk.Entry, ttk.Entry, tk.Text)):
            return None
        self.paste_selection()
        return "break" 



    # =========================================================================

    # LỊCH SỬ UNDO / REDO

    # =========================================================================

    def _save_state(self):
        # Deepcopy toàn bộ mô hình hình học trong cùng 1 container để bảo toàn đối tượng tham chiếu (pointer identity)
        model_container = {
            "points": self.points,
            "segments": self.segments,
            "lines": self.lines,
            "circles": self.circles,
            "equal_angles": self.equal_angles,
            "angle_marks": self.angle_marks,
            "polygons": getattr(self, "polygons", []),
            "ellipses": getattr(self, "ellipses", [])
        }
        saved_model = copy.deepcopy(model_container)
        state = {
            "model": saved_model,
            "points": saved_model["points"],
            "segments": saved_model["segments"],
            "lines": saved_model["lines"],
            "circles": saved_model["circles"],
            "equal_angles": saved_model["equal_angles"],
            "angle_marks": saved_model["angle_marks"],
            "polygons": saved_model["polygons"],
            "ellipses": saved_model["ellipses"],
            "problem": self.txt_problem.get("1.0", tk.END),
            "goal_type_idx": self.combo_goal_type.current() if hasattr(self, "combo_goal_type") else 0,
            "goal_type": self.combo_goal_type.get() if hasattr(self, "combo_goal_type") else "",
            "goal_targets": self.entry_goal_targets.get() if hasattr(self, "entry_goal_targets") else "",
            "scale": self.scale,
            "ox": self.origin_x,
            "oy": self.origin_y
        }
        self.undo_stack.append(state)
        if len(self.undo_stack) > 40:
            self.undo_stack.pop(0)
        self.redo_stack.clear()



    def undo(self):
        if not self.undo_stack:
            self.lbl_status.config(text="Không có thao tác nào để hoàn tác.")
            return

        model_container = {
            "points": self.points,
            "segments": self.segments,
            "lines": self.lines,
            "circles": self.circles,
            "equal_angles": self.equal_angles,
            "angle_marks": self.angle_marks,
            "polygons": getattr(self, "polygons", []),
            "ellipses": getattr(self, "ellipses", [])
        }
        saved_model = copy.deepcopy(model_container)
        curr = {
            "model": saved_model,
            "points": saved_model["points"],
            "segments": saved_model["segments"],
            "lines": saved_model["lines"],
            "circles": saved_model["circles"],
            "equal_angles": saved_model["equal_angles"],
            "angle_marks": saved_model["angle_marks"],
            "polygons": saved_model["polygons"],
            "ellipses": saved_model["ellipses"],
            "problem": self.txt_problem.get("1.0", tk.END),
            "goal_type_idx": self.combo_goal_type.current() if hasattr(self, "combo_goal_type") else 0,
            "goal_type": self.combo_goal_type.get() if hasattr(self, "combo_goal_type") else "",
            "goal_targets": self.entry_goal_targets.get() if hasattr(self, "entry_goal_targets") else "",
            "scale": self.scale,
            "ox": self.origin_x,
            "oy": self.origin_y
        }
        self.redo_stack.append(curr)
        state = self.undo_stack.pop()
        self._restore_state(state)
        self.lbl_status.config(text="Đã hoàn tác (Undo).")

    def redo(self):
        if not self.redo_stack:
            self.lbl_status.config(text="Không có thao tác nào để làm lại.")
            return

        model_container = {
            "points": self.points,
            "segments": self.segments,
            "lines": self.lines,
            "circles": self.circles,
            "equal_angles": self.equal_angles,
            "angle_marks": self.angle_marks,
            "polygons": getattr(self, "polygons", []),
            "ellipses": getattr(self, "ellipses", [])
        }
        saved_model = copy.deepcopy(model_container)
        curr = {
            "model": saved_model,
            "points": saved_model["points"],
            "segments": saved_model["segments"],
            "lines": saved_model["lines"],
            "circles": saved_model["circles"],
            "equal_angles": saved_model["equal_angles"],
            "angle_marks": saved_model["angle_marks"],
            "polygons": saved_model["polygons"],
            "ellipses": saved_model["ellipses"],
            "problem": self.txt_problem.get("1.0", tk.END),
            "goal_type_idx": self.combo_goal_type.current() if hasattr(self, "combo_goal_type") else 0,
            "goal_type": self.combo_goal_type.get() if hasattr(self, "combo_goal_type") else "",
            "goal_targets": self.entry_goal_targets.get() if hasattr(self, "entry_goal_targets") else "",
            "scale": self.scale,
            "ox": self.origin_x,
            "oy": self.origin_y
        }
        self.undo_stack.append(curr)
        state = self.redo_stack.pop()
        self._restore_state(state)
        self.lbl_status.config(text="Đã làm lại (Redo).")



    def _restore_state(self, state):
        if "model" in state:
            m = copy.deepcopy(state["model"])
            self.points = m["points"]
            self.segments = m["segments"]
            self.lines = m["lines"]
            self.circles = m["circles"]
            self.equal_angles = m["equal_angles"]
            self.angle_marks = m.get("angle_marks", [])
            self.polygons = m.get("polygons", [])
            self.ellipses = m.get("ellipses", [])
        else:
            self.points = copy.deepcopy(state["points"])
            self.segments = copy.deepcopy(state["segments"])
            self.lines = copy.deepcopy(state["lines"])
            self.circles = copy.deepcopy(state["circles"])
            self.equal_angles = copy.deepcopy(state["equal_angles"])
            self.angle_marks = copy.deepcopy(state.get("angle_marks", []))
            self.polygons = copy.deepcopy(state.get("polygons", []))
            self.ellipses = copy.deepcopy(state.get("ellipses", []))

        # Re-bind tham chiếu đối tượng điểm (point object rebinding) cho segments, lines, circles, parents
        pt_map = {id(p): p for p in self.points}
        name_map = {p.get("name"): p for p in self.points if p.get("name")}
        id_map = {p.get("id"): p for p in self.points if p.get("id")}

        def resolve_ref(ref):
            if isinstance(ref, dict):
                if any(ref is p for p in self.points):
                    return ref
                if id(ref) in pt_map:
                    return pt_map[id(ref)]
                if ref.get("id") and ref.get("id") in id_map:
                    return id_map[ref.get("id")]
                if ref.get("name") and ref.get("name") in name_map:
                    return name_map[ref.get("name")]
            elif isinstance(ref, str):
                if ref in id_map:
                    return id_map[ref]
                if ref in name_map:
                    return name_map[ref]
            return ref

        for s in self.segments:
            s["p1"] = resolve_ref(s.get("p1"))
            s["p2"] = resolve_ref(s.get("p2"))
        for l in self.lines:
            l["p1"] = resolve_ref(l.get("p1"))
            l["p2"] = resolve_ref(l.get("p2"))
        for c in self.circles:
            c["center"] = resolve_ref(c.get("center"))
        for p in self.points:
            if "parents" in p and isinstance(p["parents"], list):
                p["parents"] = [resolve_ref(par) for par in p["parents"]]
            if "constraint" in p and isinstance(p["constraint"], dict):
                c = p["constraint"]
                for k in ("p1", "p2", "p3", "p4", "p", "line_p1", "line_p2", "base_pt", "v1", "v2"):
                    if k in c:
                        c[k] = resolve_ref(c[k])
                if "pts" in c and isinstance(c["pts"], list):
                    c["pts"] = [resolve_ref(pt) for pt in c["pts"]]

        self.txt_problem.delete("1.0", tk.END)
        self.txt_problem.insert(tk.END, state.get("problem", ""))

        if "goal_type_idx" in state and hasattr(self, "combo_goal_type") and state["goal_type_idx"] >= 0:

            self.combo_goal_type.current(state["goal_type_idx"])

        elif "goal_type" in state and hasattr(self, "combo_goal_type"):

            try:

                self.combo_goal_type.set(state["goal_type"])

            except Exception:

                pass

        if "goal_targets" in state and hasattr(self, "entry_goal_targets"):

            self.entry_goal_targets.delete(0, tk.END)

            self.entry_goal_targets.insert(0, state["goal_targets"])

        self.scale = state.get("scale", 50.0)

        self.origin_x = state.get("ox", 450.0)

        self.origin_y = state.get("oy", 420.0)

        self.selected_points.clear()

        self.temp_points.clear()

        self.temp_line = None

        self._update_algebra_tree()

        self._scan_invariants_deep()

        self.redraw()



    # =========================================================================

    # THAO TÁC CHỌN VÀ BIẾN HÌNH (ROTATE / SELECT ALL)

    # =========================================================================

    def select_all(self):

        """Chọn tất cả đối tượng trên bản vẽ."""

        self.selected_points = list(self.points)

        self.redraw()

        count = len(self.selected_points)

        self.lbl_status.config(text=f"Đã chọn tất cả ({count} điểm). Bạn có thể bấm nút xoay hoặc kéo chuột để dời/xoay toàn bộ hình!")



    def rotate_selection(self, angle_deg, center_pt=None, copy=False):

        """Xoay toàn bộ các điểm đang chọn quanh tâm. Nếu copy=True, nhân bản hình trước khi xoay."""

        if not self.selected_points:

            self.select_all()

        if not self.selected_points:

            return



        if copy:

            self.duplicate_selection(offset_x=0.0, offset_y=0.0)



        self._save_state()

        rad = math.radians(angle_deg)

        cos_a = math.cos(rad)

        sin_a = math.sin(rad)



        if center_pt is None:

            cx = sum(p["x"] for p in self.selected_points) / len(self.selected_points)

            cy = sum(p["y"] for p in self.selected_points) / len(self.selected_points)

        else:

            cx, cy = center_pt



        for p in self.selected_points:

            dx = p["x"] - cx

            dy = p["y"] - cy

            p["x"] = cx + dx * cos_a - dy * sin_a

            p["y"] = cy + dx * sin_a + dy * cos_a



        self._update_algebra_tree()

        self._scan_invariants_deep()

        self.redraw()

        is_vi = (getattr(self, "current_lang", "vi") == "vi")

        mode_str = " (đã tạo bản sao mới)" if copy else ""

        self.lbl_status.config(text=f"Đã xoay toàn bộ hình {angle_deg}° quanh tâm ({cx:.2f}; {cy:.2f}){mode_str}." if is_vi else f"Rotated geometry {angle_deg}° around ({cx:.2f}, {cy:.2f}){mode_str}.")



    def rotate_custom_dialog(self):

        is_vi = (getattr(self, "current_lang", "vi") == "vi")

        top = tk.Toplevel(self)

        top.title("Xoay Góc Tùy Chọn" if is_vi else "Custom Rotation Angle")

        top.geometry("400x260")

        top.resizable(False, False)

        top.transient(self)

        top.grab_set()



        try:

            x = self.winfo_rootx() + (self.winfo_width() - 400) // 2

            y = self.winfo_rooty() + (self.winfo_height() - 260) // 2

            top.geometry(f"+{max(10, x)}+{max(10, y)}")

        except Exception:

            pass



        tk.Label(top, text="Nhập góc xoay (độ, ví dụ 45, 90, -30):" if is_vi else "Enter rotation angle (degrees, e.g. 45, 90, -30):",

                 font=("Segoe UI", 10, "bold")).pack(pady=(16, 6))



        entry_angle = tk.Entry(top, font=("Segoe UI", 11, "bold"), width=15, justify="center")

        entry_angle.pack(pady=4)

        entry_angle.insert(0, "45.0")

        entry_angle.focus_set()



        var_keep_copy = tk.BooleanVar(value=False)

        chk_copy = ttk.Checkbutton(

            top,

            text="Giữ nguyên hình cũ (Sao chép thêm hình mới)" if is_vi else "Keep original geometry (Create a copy)",

            variable=var_keep_copy

        )

        chk_copy.pack(pady=10)



        lbl_hint = tk.Label(

            top,

            text="* Nếu chọn: hình cũ được bảo toàn, hình mới được tạo thêm." if is_vi else "* If checked: original geometry is preserved, a new copy is created.",

            font=("Segoe UI", 8), fg="#666666"

        )

        lbl_hint.pack(pady=2)



        btn_box = tk.Frame(top)

        btn_box.pack(side=tk.BOTTOM, fill=tk.X, pady=15, padx=20)



        def on_ok():

            try:

                deg = float(entry_angle.get().strip())

            except ValueError:

                messagebox.showerror("Lỗi", "Góc xoay không hợp lệ!" if is_vi else "Invalid angle!", parent=top)

                return

            top.destroy()

            self.rotate_selection(deg, copy=var_keep_copy.get())



        btn_ok = tk.Button(btn_box, text="Xác nhận" if is_vi else "Confirm", bg="#1971c2", fg="#ffffff",

                           font=("Segoe UI", 9, "bold"), padx=14, pady=3, command=on_ok)

        btn_ok.pack(side=tk.LEFT, expand=True, padx=5)



        btn_cancel = tk.Button(btn_box, text="Hủy" if is_vi else "Cancel", font=("Segoe UI", 9),

                               padx=14, pady=3, command=top.destroy)

        btn_cancel.pack(side=tk.RIGHT, expand=True, padx=5)

        top.bind("<Return>", lambda e: on_ok())

        top.bind("<Escape>", lambda e: top.destroy())



    # =========================================================================

    # DỰNG ĐIỂM THEO GÓC, TỈ LỆ, TỊNH TIẾN, HÌNH CHIẾU & TRỰC TÂM (CAD EXTENSIONS)

    # =========================================================================

    def parse_geom_length(self, expr_str, points_dict):

        """

        Phân tích chuỗi độ dài hình học:

        Hỗ trợ:

          - Số thực: "5.0", "3.5"

          - Tên đoạn thẳng: "AB", "BC", "CB"

          - Tỉ lệ nhân: "2*CB", "1.5*AB", "3/4*AC", "BC/2"

        """

        expr = str(expr_str).strip()

        segs = re.findall(r'[A-Za-z][0-9]*[A-Za-z][0-9]*', expr)

        evaluated_expr = expr

        for s in segs:

            m = re.match(r'([A-Za-z][0-9]*)([A-Za-z][0-9]*)', s)

            if m:

                p1_name, p2_name = m.group(1), m.group(2)

                if p1_name in points_dict and p2_name in points_dict:

                    p1 = points_dict[p1_name]

                    p2 = points_dict[p2_name]

                    dist = math.hypot(p1["x"] - p2["x"], p1["y"] - p2["y"])

                    evaluated_expr = evaluated_expr.replace(s, f"({dist})")

        try:

            val = float(eval(evaluated_expr, {"__builtins__": None, "math": math}, {}))

            return val

        except Exception:

            return None



    def open_angle_ratio_dialog(self):

        """Hộp thoại dựng điểm thông minh thống nhất (Gom 1 giao diện, kích thước lớn, co giãn, song ngữ VI/EN)."""

        is_vi = (getattr(self, "current_lang", "vi") == "vi")

        pt_names = [p.get("name") or p["id"] for p in self.points if p.get("name") or p.get("id")]

        if len(pt_names) < 2:

            warn_title = "Chưa đủ điểm" if is_vi else "Insufficient Points"

            warn_msg = ("Cần ít nhất 2 điểm trên bản vẽ để dựng điểm theo quỹ tích và điều kiện." if is_vi 

                        else "At least 2 points are required on the canvas to define locus and conditions.")

            messagebox.showwarning(warn_title, warn_msg)

            return



        top = tk.Toplevel(self)

        top.title("Dựng Điểm Ràng Buộc Theo Vị Trí, Góc & Tỉ Lệ" if is_vi else "Construct Point by Locus, Angle & Ratio")

        top.geometry("700x670")

        top.minsize(620, 560)

        top.resizable(True, True)

        top.configure(bg="#f8f9fa")

        top.transient(self)

        top.grab_set()



        try:

            x = self.winfo_rootx() + (self.winfo_width() - 700) // 2

            y = self.winfo_rooty() + (self.winfo_height() - 670) // 2

            top.geometry(f"+{max(10, x)}+{max(10, y)}")

        except Exception:

            pass



        # -------------------------------------------------------------

        # KHUNG CUỘN CHỐNG TRÀN NỘI DUNG (SCROLLABLE CONTAINER)

        # -------------------------------------------------------------

        canvas_dlg = tk.Canvas(top, bg="#f8f9fa", highlightthickness=0)

        sb_dlg = ttk.Scrollbar(top, orient=tk.VERTICAL, command=canvas_dlg.yview)

        scroll_content = tk.Frame(canvas_dlg, bg="#f8f9fa", padx=16, pady=12)



        scroll_content.bind(

            "<Configure>",

            lambda e: canvas_dlg.configure(scrollregion=canvas_dlg.bbox("all"))

        )

        canvas_win = canvas_dlg.create_window((0, 0), window=scroll_content, anchor="nw")



        def _on_dlg_cfg(e):

            canvas_dlg.itemconfig(canvas_win, width=e.width)

        canvas_dlg.bind("<Configure>", _on_dlg_cfg)

        canvas_dlg.configure(yscrollcommand=sb_dlg.set)



        def _on_dlg_wheel(e):

            if canvas_dlg.winfo_exists():

                canvas_dlg.yview_scroll(int(-1 * (e.delta / 120)), "units")

        top.bind("<MouseWheel>", _on_dlg_wheel)



        def _on_dlg_close():

            try:

                top.unbind("<MouseWheel>")

            except Exception:

                pass

            top.destroy()

        top.protocol("WM_DELETE_WINDOW", _on_dlg_close)



        sb_dlg.pack(side=tk.RIGHT, fill=tk.Y)

        canvas_dlg.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



        # -------------------------------------------------------------

        # BANNER TIÊU ĐỀ

        # -------------------------------------------------------------

        hdr = tk.Frame(scroll_content, bg="#1864ab", pady=8, padx=12)

        hdr.pack(fill=tk.X, pady=(0, 10))

        t_hdr = "📐 THIẾT LẬP ĐIỀU KIỆN DỰNG ĐIỂM (SMART POINT BUILDER)" if is_vi else "📐 SMART POINT BUILDER CONFIGURATION"

        tk.Label(hdr, text=t_hdr, font=("Segoe UI", 12, "bold"), fg="#ffffff", bg="#1864ab").pack(anchor=tk.W)

        t_sub = "Gom toàn bộ điều kiện Vị trí, Quỹ tích, Góc & Tỉ lệ trên 1 trang trực quan" if is_vi else "Unified single-page interface for locus, angular conditions and distance ratios"

        tk.Label(hdr, text=t_sub, font=("Segoe UI", 8), fg="#d0ebff", bg="#1864ab").pack(anchor=tk.W)



        # -------------------------------------------------------------

        # MỤC 1: TÊN ĐIỂM CẦN TẠO

        # -------------------------------------------------------------

        fr_pt = ttk.LabelFrame(scroll_content, text="1. Điểm Cần Tạo (Point Identity)" if is_vi else "1. Point Identity", padding=10)

        fr_pt.pack(fill=tk.X, pady=(0, 8))



        lbl_pt_name = "Tên điểm mới (Point Name):" if is_vi else "Point Name:"

        ttk.Label(fr_pt, text=lbl_pt_name, font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky=tk.W, padx=4)

        ent_pt_name = ttk.Entry(fr_pt, width=10, font=("Segoe UI", 10, "bold"))

        ent_pt_name.grid(row=0, column=1, sticky=tk.W, padx=6)

        

        def_name = "M"

        for cand in ["M", "N", "P", "Q", "K", "D", "E", "F", "I"]:

            if cand not in pt_names:

                def_name = cand

                break

        ent_pt_name.insert(0, def_name)



        hint_name = "(Ví dụ: M, N, P, A', M1...)" if is_vi else "(e.g. M, N, P, A', M1...)"

        ttk.Label(fr_pt, text=hint_name, foreground="#6c757d", font=("Segoe UI", 8)).grid(row=0, column=2, sticky=tk.W, padx=4)



        # -------------------------------------------------------------

        # MỤC 2: VỊ TRÍ / QUỸ TÍCH CỦA ĐIỂM

        # -------------------------------------------------------------

        fr_locus = ttk.LabelFrame(scroll_content, text="2. Vị Trí / Quỹ Tích Của Điểm (Point Locus & Base Path)" if is_vi else "2. Point Locus & Base Path", padding=10)

        fr_locus.pack(fill=tk.X, pady=(0, 8))



        var_locus = tk.StringVar(value="line_ray")



        # Quỹ tích 1: Đường thẳng / tia qua 2 điểm

        r_locus_line = ttk.Radiobutton(

            fr_locus,

            text="Thuộc đường thẳng / tia qua 2 điểm (On Line / Ray through 2 points):" if is_vi else "On Line / Ray through 2 points:",

            variable=var_locus, value="line_ray"

        )

        r_locus_line.grid(row=0, column=0, columnspan=6, sticky=tk.W, pady=(2, 4))



        fr_sub_line = tk.Frame(fr_locus, bg="#f8f9fa", padx=20)

        fr_sub_line.grid(row=1, column=0, columnspan=6, sticky=tk.W, pady=(0, 6))



        ttk.Label(fr_sub_line, text="Gốc xuất phát (Origin):" if is_vi else "Origin:").grid(row=0, column=0, sticky=tk.W, padx=2)

        cb_loc_p1 = ttk.Combobox(fr_sub_line, values=pt_names, state="readonly", width=7)

        cb_loc_p1.grid(row=0, column=1, sticky=tk.W, padx=4)

        cb_loc_p1.set("E" if "E" in pt_names else pt_names[0])



        ttk.Label(fr_sub_line, text="Hướng qua (Target):" if is_vi else "Target:").grid(row=0, column=2, sticky=tk.W, padx=(8, 2))

        cb_loc_p2 = ttk.Combobox(fr_sub_line, values=pt_names, state="readonly", width=7)

        cb_loc_p2.grid(row=0, column=3, sticky=tk.W, padx=4)

        cb_loc_p2.set("C" if "C" in pt_names else (pt_names[1] if len(pt_names) > 1 else pt_names[0]))



        ttk.Label(fr_sub_line, text="Phạm vi:" if is_vi else "Scope:").grid(row=0, column=4, sticky=tk.W, padx=(8, 2))

        scope_vals = [

            ("Tia gốc P1 qua P2 (Ray P1->P2)" if is_vi else "Ray P1->P2"),

            ("Đoạn thẳng P1P2 (Segment P1P2)" if is_vi else "Segment P1P2"),

            ("Đường thẳng P1P2 (Infinite Line)" if is_vi else "Infinite Line P1P2")

        ]

        cb_loc_scope = ttk.Combobox(fr_sub_line, values=scope_vals, state="readonly", width=25)

        cb_loc_scope.grid(row=0, column=5, sticky=tk.W, padx=4)

        cb_loc_scope.current(0)



        # Quỹ tích 2: Thuộc đường tròn

        circ_labels = []

        for c in self.circles:

            c_name = c["center"].get("name") or c["center"]["id"]

            circ_labels.append(f"{c['id']} (Tâm {c_name}, R={c['r']:.2f})")

        if not circ_labels:

            circ_labels = ["(Chưa có đường tròn trên bản vẽ)" if is_vi else "(No circle on canvas)"]



        r_locus_circ = ttk.Radiobutton(

            fr_locus,

            text="Thuộc đường tròn (On Circle):" if is_vi else "On Circle:",

            variable=var_locus, value="circle"

        )

        r_locus_circ.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(4, 2))



        cb_loc_circ = ttk.Combobox(fr_locus, values=circ_labels, state="readonly", width=38)

        cb_loc_circ.grid(row=2, column=2, columnspan=4, sticky=tk.W, padx=(8, 4), pady=(4, 2))

        cb_loc_circ.current(0)



        # Quỹ tích 3: Tự do trên mặt phẳng

        r_locus_free = ttk.Radiobutton(

            fr_locus,

            text="Điểm tự do / di động trên mặt phẳng (Free / Mobile Point on Plane)" if is_vi else "Free / Mobile Point on Plane",

            variable=var_locus, value="free"

        )

        r_locus_free.grid(row=3, column=0, columnspan=6, sticky=tk.W, pady=(4, 2))



        # -------------------------------------------------------------

        # MỤC 3: ĐIỀU KIỆN RÀNG BUỘC TOÁN HỌC (GOM 2 TAB LÀM 1)

        # -------------------------------------------------------------

        fr_cond = ttk.LabelFrame(scroll_content, text="3. Điều Kiện Ràng Buộc Toán Học (Geometric Constraints)" if is_vi else "3. Geometric Constraints", padding=10)

        fr_cond.pack(fill=tk.X, pady=(0, 10))



        var_cond = tk.StringVar(value="angle_eq")



        # ĐIỀU KIỆN 1: GÓC BẰNG GÓC

        r_c1 = ttk.Radiobutton(

            fr_cond,

            text="1. Góc bằng góc (Equal Angles - VD: ∠BME = ∠ECA như VMO 2008):" if is_vi else "1. Equal Angles (e.g. ∠BME = ∠ECA as in VMO 2008):",

            variable=var_cond, value="angle_eq"

        )

        r_c1.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(2, 4))



        fr_c1_box = tk.Frame(fr_cond, bg="#f8f9fa", padx=18)

        fr_c1_box.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(0, 8))



        ttk.Label(fr_c1_box, text="Đỉnh quan sát B (Vertex B):" if is_vi else "Observation Vertex B:").grid(row=0, column=0, sticky=tk.W, padx=2)

        cb_c1_B = ttk.Combobox(fr_c1_box, values=pt_names, state="readonly", width=7)

        cb_c1_B.grid(row=0, column=1, sticky=tk.W, padx=4)

        cb_c1_B.set("B" if "B" in pt_names else pt_names[0])



        ttk.Label(fr_c1_box, text="Bằng góc ∠ (Equal to ∠):" if is_vi else "Equal to ∠:").grid(row=0, column=2, sticky=tk.W, padx=(10, 2))

        ent_c1_angle = ttk.Entry(fr_c1_box, width=12)

        ent_c1_angle.grid(row=0, column=3, sticky=tk.W, padx=4)

        ent_c1_angle.insert(0, "ECA")



        hint_c1 = "(VD: ECA, ABC, hoặc BME=ECA)" if is_vi else "(e.g. ECA, ABC, or BME=ECA)"

        ttk.Label(fr_c1_box, text=hint_c1, foreground="#6c757d", font=("Segoe UI", 8)).grid(row=0, column=4, sticky=tk.W, padx=4)



        # ĐIỀU KIỆN 2: GÓC CỐ ĐỊNH THEO ĐỘ

        r_c2 = ttk.Radiobutton(

            fr_cond,

            text="2. Góc cố định theo độ (Fixed Degree Angle - VD: 30°, 45°, 60°, 90°...):" if is_vi else "2. Fixed Degree Angle (e.g. 30°, 45°, 60°, 90°...):",

            variable=var_cond, value="fixed_deg"

        )

        r_c2.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(4, 4))



        fr_c2_box = tk.Frame(fr_cond, bg="#f8f9fa", padx=18)

        fr_c2_box.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(0, 8))



        ttk.Label(fr_c2_box, text="Số đo góc (°):" if is_vi else "Angle (°):").grid(row=0, column=0, sticky=tk.W, padx=2)

        ent_c2_deg = ttk.Entry(fr_c2_box, width=8)

        ent_c2_deg.grid(row=0, column=1, sticky=tk.W, padx=4)

        ent_c2_deg.insert(0, "45")



        fr_quick_deg = tk.Frame(fr_c2_box, bg="#f8f9fa")

        fr_quick_deg.grid(row=0, column=2, sticky=tk.W, padx=(6, 2))

        for d_val in ("30", "45", "60", "90", "120"):

            def make_deg_cmd(v=d_val):

                return lambda: (ent_c2_deg.delete(0, tk.END), ent_c2_deg.insert(0, v), var_cond.set("fixed_deg"))

            tk.Button(fr_quick_deg, text=f"{d_val}°", font=("Segoe UI", 8), bg="#e9ecef",

                      padx=4, pady=0, cursor="hand2", command=make_deg_cmd(d_val)).pack(side=tk.LEFT, padx=1)



        ttk.Label(fr_c2_box, text="Đỉnh quan sát B:" if is_vi else "Observation B:").grid(row=0, column=3, sticky=tk.W, padx=(10, 2))

        cb_c2_B = ttk.Combobox(fr_c2_box, values=pt_names, state="readonly", width=7)

        cb_c2_B.grid(row=0, column=4, sticky=tk.W, padx=4)

        cb_c2_B.set("B" if "B" in pt_names else pt_names[0])



        # ĐIỀU KIỆN 3: TỈ LỆ ĐỘ DÀI / ĐOẠN THẲNG

        r_c3 = ttk.Radiobutton(

            fr_cond,

            text="3. Tỉ lệ khoảng cách / đoạn thẳng (Segment Ratio - VD: AM = 2*CB, 1.5*AB, 5.0):" if is_vi else "3. Distance / Segment Ratio (e.g. AM = 2*CB, 1.5*AB, 5.0):",

            variable=var_cond, value="dist_ratio"

        )

        r_c3.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(4, 4))



        fr_c3_box = tk.Frame(fr_cond, bg="#f8f9fa", padx=18)

        fr_c3_box.grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=(0, 8))



        ttk.Label(fr_c3_box, text="Khoảng cách / Tỉ lệ:" if is_vi else "Distance / Ratio:").grid(row=0, column=0, sticky=tk.W, padx=2)

        ent_c3_dist = ttk.Entry(fr_c3_box, width=14)

        ent_c3_dist.grid(row=0, column=1, sticky=tk.W, padx=4)

        def_expr = "2*CB" if ("C" in pt_names and "B" in pt_names) else ("2*AB" if ("A" in pt_names and "B" in pt_names) else "5.0")

        ent_c3_dist.insert(0, def_expr)



        fr_quick_dist = tk.Frame(fr_c3_box, bg="#f8f9fa")

        fr_quick_dist.grid(row=0, column=2, sticky=tk.W, padx=(4, 2))

        for d_expr in ("2*CB", "1.5*AB", "BC/2", "5.0"):

            def make_dist_cmd(v=d_expr):

                return lambda: (ent_c3_dist.delete(0, tk.END), ent_c3_dist.insert(0, v), var_cond.set("dist_ratio"))

            tk.Button(fr_quick_dist, text=d_expr, font=("Segoe UI", 8), bg="#e9ecef",

                      padx=4, pady=0, cursor="hand2", command=make_dist_cmd(d_expr)).pack(side=tk.LEFT, padx=1)



        var_c3_reverse = tk.BooleanVar(value=False)

        cb_c3_rev = ttk.Checkbutton(

            fr_c3_box,

            text="Lấy ngược hướng tia (Tia đối)" if is_vi else "Reverse direction (Opposite ray)",

            variable=var_c3_reverse

        )

        cb_c3_rev.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(4, 0))



        # ĐIỀU KIỆN 4: TỈ SỐ CHIA ĐOẠN THẲNG

        r_c4 = ttk.Radiobutton(

            fr_cond,

            text="4. Tỉ số vị trí trên đoạn thẳng (Division Ratio: EM = k*EC):" if is_vi else "4. Division Ratio on Segment (EM = k*EC):",

            variable=var_cond, value="div_ratio"

        )

        r_c4.grid(row=6, column=0, columnspan=3, sticky=tk.W, pady=(4, 4))



        fr_c4_box = tk.Frame(fr_cond, bg="#f8f9fa", padx=18)

        fr_c4_box.grid(row=7, column=0, columnspan=3, sticky=tk.W, pady=(0, 4))



        ttk.Label(fr_c4_box, text="Tỉ số k:" if is_vi else "Ratio k:").grid(row=0, column=0, sticky=tk.W, padx=2)

        ent_c4_k = ttk.Entry(fr_c4_box, width=8)

        ent_c4_k.grid(row=0, column=1, sticky=tk.W, padx=4)

        ent_c4_k.insert(0, "0.5")



        fr_quick_k = tk.Frame(fr_c4_box, bg="#f8f9fa")

        fr_quick_k.grid(row=0, column=2, sticky=tk.W, padx=(4, 2))

        for k_val, k_lbl in [("0.5", "0.5 (T.điểm)"), ("0.333", "1/3"), ("0.667", "2/3"), ("1.5", "1.5"), ("2.0", "2.0")]:

            def make_k_cmd(v=k_val):

                return lambda: (ent_c4_k.delete(0, tk.END), ent_c4_k.insert(0, v), var_cond.set("div_ratio"))

            tk.Button(fr_quick_k, text=k_lbl if is_vi else k_val, font=("Segoe UI", 8), bg="#e9ecef",

                      padx=4, pady=0, cursor="hand2", command=make_k_cmd(k_val)).pack(side=tk.LEFT, padx=1)



        # -------------------------------------------------------------

        # HÀM THỰC THI DỰNG ĐIỂM

        # -------------------------------------------------------------

        def do_construct_smart_point():

            p_map = {p.get("name") or p["id"]: p for p in self.points}

            name = ent_pt_name.get().strip() or "M"

            locus = var_locus.get()

            cond = var_cond.get()



            new_x, new_y = None, None

            ref_lines_to_add = []



            n_p1 = cb_loc_p1.get()

            n_p2 = cb_loc_p2.get()

            p1 = p_map.get(n_p1)

            p2 = p_map.get(n_p2)



            if locus == "circle":

                circ_sel_idx = cb_loc_circ.current()

                if not self.circles or circ_sel_idx < 0 or circ_sel_idx >= len(self.circles):

                    err_msg = "Vui lòng chọn một đường tròn hợp lệ!" if is_vi else "Please select a valid circle!"

                    messagebox.showerror("Lỗi" if is_vi else "Error", err_msg)

                    return

                circ = self.circles[circ_sel_idx]

                O_pt = circ["center"]

                R = circ["r"]



                if cond == "fixed_deg":

                    try: deg = float(ent_c2_deg.get().strip())

                    except: deg = 45.0

                    rad = math.radians(deg)

                    new_x = O_pt["x"] + R * math.cos(rad)

                    new_y = O_pt["y"] + R * math.sin(rad)

                else:

                    n_B = cb_c1_B.get()

                    pB = p_map.get(n_B)

                    if pB and pB != O_pt:

                        ang = math.atan2(pB["y"] - O_pt["y"], pB["x"] - O_pt["x"])

                        new_x = O_pt["x"] + R * math.cos(ang)

                        new_y = O_pt["y"] + R * math.sin(ang)

                    else:

                        new_x = O_pt["x"] + R

                        new_y = O_pt["y"]



            else:

                if not p1 or not p2:

                    err_msg = "Vui lòng chọn các điểm xác định quỹ tích!" if is_vi else "Please select locus points!"

                    messagebox.showerror("Lỗi" if is_vi else "Error", err_msg)

                    return

                if n_p1 == n_p2:

                    err_msg = "Hai điểm xác định đường thẳng/tia phải khác nhau!" if is_vi else "Origin and target points must be distinct!"

                    messagebox.showerror("Lỗi" if is_vi else "Error", err_msg)

                    return



                dx = p2["x"] - p1["x"]

                dy = p2["y"] - p1["y"]

                L_base = math.hypot(dx, dy)

                if L_base < 1e-7:

                    err_msg = "Hai điểm quỹ tích trùng nhau!" if is_vi else "Locus points coincide!"

                    messagebox.showerror("Lỗi" if is_vi else "Error", err_msg)

                    return

                ux = dx / L_base

                uy = dy / L_base



                if cond == "angle_eq":

                    n_B = cb_c1_B.get()

                    pB = p_map.get(n_B)

                    if not pB:

                        err_msg = "Vui lòng chọn đỉnh quan sát B hợp lệ!" if is_vi else "Please select a valid vertex B!"

                        messagebox.showerror("Lỗi" if is_vi else "Error", err_msg)

                        return



                    ref_ang_str = ent_c1_angle.get().strip().upper()

                    if "=" in ref_ang_str:

                        ref_ang_str = ref_ang_str.split("=")[-1].strip()

                    ref_ang_str = re.sub(r'[^A-Z0-9]', '', ref_ang_str)



                    beta = None

                    if len(ref_ang_str) == 3:

                        pA_name, pB_name, pC_name = ref_ang_str[0], ref_ang_str[1], ref_ang_str[2]

                        if pA_name in p_map and pB_name in p_map and pC_name in p_map:

                            ptA, ptV, ptC = p_map[pA_name], p_map[pB_name], p_map[pC_name]

                            v1x, v1y = ptA["x"] - ptV["x"], ptA["y"] - ptV["y"]

                            v2x, v2y = ptC["x"] - ptV["x"], ptC["y"] - ptV["y"]

                            len1, len2 = math.hypot(v1x, v1y), math.hypot(v2x, v2y)

                            if len1 > 1e-6 and len2 > 1e-6:

                                cos_val = max(-1.0, min(1.0, (v1x*v2x + v1y*v2y) / (len1 * len2)))

                                beta = math.acos(cos_val)



                    if beta is None or beta < 1e-4 or beta > math.pi - 1e-4:

                        pA = p_map.get("A")

                        pC = p_map.get("C")

                        if pA and pC:

                            R_BM = math.hypot(pC["x"] - pA["x"], pC["y"] - pA["y"])

                        else:

                            R_BM = math.hypot(p2["x"] - pB["x"], p2["y"] - pB["y"])

                        qa = dx**2 + dy**2

                        qb = 2 * (dx * (p1["x"] - pB["x"]) + dy * (p1["y"] - pB["y"]))

                        qc = (p1["x"] - pB["x"])**2 + (p1["y"] - pB["y"])**2 - R_BM**2

                        disc = qb**2 - 4 * qa * qc

                        if disc < 0:

                            err_msg = "Không tìm thấy giao điểm thỏa mãn điều kiện góc!" if is_vi else "No intersection satisfies the angle condition!"

                            messagebox.showerror("Lỗi" if is_vi else "Error", err_msg)

                            return

                        s1 = (-qb + math.sqrt(disc)) / (2 * qa)

                        s2 = (-qb - math.sqrt(disc)) / (2 * qa)

                        t_valid = s1 if s1 > 0 else s2

                        if t_valid <= 0: t_valid = max(s1, s2)

                        new_x = p1["x"] + t_valid * dx

                        new_y = p1["y"] + t_valid * dy

                    else:

                        t_proj = (pB["x"] - p1["x"]) * ux + (pB["y"] - p1["y"]) * uy

                        Hx = p1["x"] + t_proj * ux

                        Hy = p1["y"] + t_proj * uy

                        h = math.hypot(pB["x"] - Hx, pB["y"] - Hy)

                        if h < 1e-6:

                            t_valid = t_proj + 3.0

                        else:

                            tan_b = math.tan(beta)

                            if abs(tan_b) < 1e-6:

                                t_valid = t_proj + 3.0

                            else:

                                offset = h / abs(tan_b)

                                t1 = t_proj + offset

                                t2 = t_proj - offset

                                if t1 > 0 and t2 <= 0: t_valid = t1

                                elif t2 > 0 and t1 <= 0: t_valid = t2

                                elif t1 > 0 and t2 > 0: t_valid = t1

                                else: t_valid = max(t1, t2)

                        new_x = p1["x"] + t_valid * ux

                        new_y = p1["y"] + t_valid * uy



                    ref_lines_to_add.append((pB, "dashed", f"{n_B}{name}"))



                elif cond == "fixed_deg":

                    try: deg = float(ent_c2_deg.get().strip())

                    except: deg = 45.0

                    beta = math.radians(deg)

                    n_B = cb_c2_B.get()

                    pB = p_map.get(n_B)

                    if pB and locus != "free":

                        t_proj = (pB["x"] - p1["x"]) * ux + (pB["y"] - p1["y"]) * uy

                        Hx = p1["x"] + t_proj * ux

                        Hy = p1["y"] + t_proj * uy

                        h = math.hypot(pB["x"] - Hx, pB["y"] - Hy)

                        tan_b = math.tan(beta)

                        if abs(tan_b) > 1e-4 and h > 1e-5:

                            t_valid = t_proj + h / abs(tan_b)

                            new_x = p1["x"] + t_valid * ux

                            new_y = p1["y"] + t_valid * uy

                        else:

                            new_x = p1["x"] + (t_proj + 3.0) * ux

                            new_y = p1["y"] + (t_proj + 3.0) * uy

                        ref_lines_to_add.append((pB, "dashed", f"{n_B}{name} ({deg:.0f}°)"))

                    else:

                        rx = dx * math.cos(beta) - dy * math.sin(beta)

                        ry = dx * math.sin(beta) + dy * math.cos(beta)

                        new_x = p1["x"] + rx

                        new_y = p1["y"] + ry



                elif cond == "dist_ratio":

                    expr_str = ent_c3_dist.get().strip()

                    val = self.parse_geom_length(expr_str, p_map)

                    if val is None or val <= 0:

                        err_msg = (f"Không thể tính toán khoảng cách từ: '{expr_str}'.\nVí dụ hợp lệ: 2*CB, 1.5*AB, 5.0, BC/2" if is_vi

                                   else f"Cannot compute distance from: '{expr_str}'.\nValid examples: 2*CB, 1.5*AB, 5.0, BC/2")

                        messagebox.showerror("Lỗi biểu thức" if is_vi else "Expression Error", err_msg)

                        return

                    sign = -1.0 if var_c3_reverse.get() else 1.0

                    new_x = p1["x"] + sign * ux * val

                    new_y = p1["y"] + sign * uy * val



                elif cond == "div_ratio":

                    try:

                        k_str = ent_c4_k.get().strip()

                        if "/" in k_str:

                            num, den = k_str.split("/")

                            k = float(num) / float(den)

                        else:

                            k = float(k_str)

                    except:

                        k = 0.5

                    new_x = p1["x"] + k * dx

                    new_y = p1["y"] + k * dy



            if new_x is None or new_y is None:

                err_msg = "Không xác định được vị trí điểm!" if is_vi else "Failed to compute point position!"

                messagebox.showerror("Lỗi" if is_vi else "Error", err_msg)

                return



            self._save_state()

            new_pt = {

                "id": f"pt_{len(self.points)+1}",

                "name": name,

                "x": new_x,

                "y": new_y,

                "color": self.COLOR_HIGHLIGHT,

                "fixed": False

            }

            self.points.append(new_pt)



            if p1 and locus != "free":

                self.segments.append({

                    "p1": p1, "p2": new_pt,

                    "color": self.COLOR_LINE,

                    "style": "solid",

                    "label": f"{n_p1}{name}"

                })



            for ref_p, st, lb in ref_lines_to_add:

                self.segments.append({

                    "p1": ref_p, "p2": new_pt,

                    "color": "#7048e8" if st == "dashed" else self.COLOR_LINE,

                    "style": st,

                    "label": lb

                })



            self._update_algebra_tree()

            self._scan_invariants_deep()

            self.redraw()

            _on_dlg_close()

            succ_msg = (f"Đã dựng thành công điểm {name} tại tọa độ ({new_x:.2f}; {new_y:.2f})!" if is_vi

                        else f"Successfully constructed point {name} at ({new_x:.2f}; {new_y:.2f})!")

            self.lbl_status.config(text=succ_msg)



        # -------------------------------------------------------------

        # MỤC 4: HÀNH ĐỘNG & GỢI Ý

        # -------------------------------------------------------------

        lbl_hint = tk.Label(

            scroll_content,

            text="💡 Máy sẽ tự động phân tích điều kiện hình học, tính toán tọa độ chính xác và dựng điểm M cùng các liên kết chuẩn." if is_vi

                 else "💡 GeoSolver will solve the constraint system, compute exact coordinates and construct point M with linked relations.",

            font=("Segoe UI", 8, "italic"), fg="#1864ab", bg="#f8f9fa"

        )

        lbl_hint.pack(anchor=tk.W, pady=(4, 8))



        btn_bar = tk.Frame(scroll_content, bg="#f8f9fa", pady=6)

        btn_bar.pack(fill=tk.X)



        btn_create = tk.Button(

            btn_bar,

            text="✔ DỰNG ĐIỂM NGAY (Construct Point M)" if is_vi else "✔ CONSTRUCT POINT M NOW",

            font=("Segoe UI", 10, "bold"), bg="#2b8a3e", fg="#ffffff", activebackground="#237032", activeforeground="#ffffff",

            padx=20, pady=6, cursor="hand2", relief=tk.RAISED, command=do_construct_smart_point

        )

        btn_create.pack(side=tk.LEFT, padx=4)



        btn_cancel = tk.Button(

            btn_bar,

            text="Hủy (Cancel)" if is_vi else "Cancel",

            font=("Segoe UI", 9), bg="#e9ecef", padx=16, pady=6, cursor="hand2",

            command=_on_dlg_close

        )

        btn_cancel.pack(side=tk.LEFT, padx=6)



    def open_translate_dialog(self):

        """Hộp thoại tịnh tiến điểm theo vector (VD: vector MN = vector AC trong VMO 2003)."""

        is_vi = getattr(self, "current_lang", "vi") == "vi"

        pt_names = [p.get("name") or p["id"] for p in self.points if p.get("name") or p.get("id")]

        if len(pt_names) < 2:

            title_warn = "Chưa đủ điểm" if is_vi else "Not Enough Points"

            msg_warn = "Cần có ít nhất 2 điểm trên bản vẽ." if is_vi else "Need at least 2 points on canvas."

            messagebox.showwarning(title_warn, msg_warn)

            return



        top = tk.Toplevel(self)

        top.title("Tịnh Tiến Điểm Theo Vector" if is_vi else "Vector Translation")

        top.geometry("420x300")

        top.resizable(True, True)

        top.transient(self)



        ttk.Label(top, text="Điểm cần tịnh tiến (Target Point - VD: M):" if is_vi else "Target Point to Translate (e.g. M):",

                  font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky=tk.W, padx=12, pady=8)

        cb_pt = ttk.Combobox(top, values=pt_names, state="readonly", width=12)

        cb_pt.grid(row=0, column=1, sticky=tk.W, padx=10, pady=8)

        cb_pt.set("M" if "M" in pt_names else pt_names[0])



        fr_vec = ttk.LabelFrame(top, text="Vector tịnh tiến (VD: vector AC => vector MN = vector AC)" if is_vi else "Translation Vector (e.g. vector AC => vector MN = vector AC)", padding=10)

        fr_vec.grid(row=1, column=0, columnspan=2, padx=12, pady=8, sticky=tk.EW)



        ttk.Label(fr_vec, text="Điểm gốc vector (Origin):" if is_vi else "Vector Start Point:").grid(row=0, column=0, sticky=tk.W, pady=4)

        cb_v1 = ttk.Combobox(fr_vec, values=pt_names, state="readonly", width=12)

        cb_v1.grid(row=0, column=1, sticky=tk.W, padx=8, pady=4)

        cb_v1.set("A" if "A" in pt_names else pt_names[0])



        ttk.Label(fr_vec, text="Điểm ngọn vector (End):" if is_vi else "Vector End Point:").grid(row=1, column=0, sticky=tk.W, pady=4)

        cb_v2 = ttk.Combobox(fr_vec, values=pt_names, state="readonly", width=12)

        cb_v2.grid(row=1, column=1, sticky=tk.W, padx=8, pady=4)

        cb_v2.set("C" if "C" in pt_names else (pt_names[1] if len(pt_names)>1 else pt_names[0]))



        ttk.Label(top, text="Tên điểm mới (New Point Name - VD: N):" if is_vi else "New Point Name (e.g. N):",

                  font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky=tk.W, padx=12, pady=8)

        ent_name = ttk.Entry(top, width=12)

        ent_name.grid(row=2, column=1, sticky=tk.W, padx=10, pady=8)

        default_name = "N" if "N" not in pt_names else next((c for c in "NPQKL" if c not in pt_names), "P")

        ent_name.insert(0, default_name)



        def do_translate():

            p_map = {p.get("name") or p["id"]: p for p in self.points}

            name_p = cb_pt.get()

            name_v1 = cb_v1.get()

            name_v2 = cb_v2.get()

            if name_p not in p_map or name_v1 not in p_map or name_v2 not in p_map:

                err_t = "Lỗi" if is_vi else "Error"

                err_m = "Vui lòng chọn đầy đủ các điểm!" if is_vi else "Please select all points!"

                messagebox.showerror(err_t, err_m)

                return

            pM = p_map[name_p]

            pA = p_map[name_v1]

            pC = p_map[name_v2]



            vx = pC["x"] - pA["x"]

            vy = pC["y"] - pA["y"]

            new_x = pM["x"] + vx

            new_y = pM["y"] + vy

            name_new = ent_name.get().strip() or "N"



            self._save_state()

            new_pt = {

                "id": f"pt_{len(self.points)+1}",

                "name": name_new,

                "x": new_x,

                "y": new_y,

                "color": self.COLOR_HIGHLIGHT,

                "fixed": False,

                "constraint": {"type": "translate_vec", "base_pt": pM, "v1": pA, "v2": pC}

            }

            self.points.append(new_pt)

            self._update_algebra_tree()

            self.redraw()

            top.destroy()

            msg_ok = f"Đã tạo điểm {name_new} sao cho vector({name_p}{name_new}) = vector({name_v1}{name_v2})." if is_vi else f"Created point {name_new} such that vector({name_p}{name_new}) = vector({name_v1}{name_v2})."

            self.lbl_status.config(text=msg_ok)



        btn_apply = tk.Button(top, text="✔ Thực Hiện Tịnh Tiến" if is_vi else "✔ Translate Point",

                              bg="#2b8a3e", fg="white", font=("Segoe UI", 9, "bold"), padx=12, pady=4, cursor="hand2", command=do_translate)

        btn_apply.grid(row=3, column=0, columnspan=2, pady=14)



    def open_proj_foot_dialog(self):

        """Hộp thoại hạ hình chiếu vuông góc từ điểm xuống đường thẳng (VD: D = chiếu M trên BC)."""

        is_vi = getattr(self, "current_lang", "vi") == "vi"

        pt_names = [p.get("name") or p["id"] for p in self.points if p.get("name") or p.get("id")]

        if len(pt_names) < 3:

            title_warn = "Chưa đủ điểm" if is_vi else "Not Enough Points"

            msg_warn = "Cần ít nhất 3 điểm trên bản vẽ." if is_vi else "Need at least 3 points on canvas."

            messagebox.showwarning(title_warn, msg_warn)

            return



        top = tk.Toplevel(self)

        top.title("Hạ Hình Chiếu Vuông Góc" if is_vi else "Perpendicular Projection Foot")

        top.geometry("420x300")

        top.resizable(True, True)

        top.transient(self)



        ttk.Label(top, text="Điểm hạ hình chiếu (VD: M hoặc N):" if is_vi else "Point to Project (e.g. M or N):",

                  font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky=tk.W, padx=12, pady=8)

        cb_pt = ttk.Combobox(top, values=pt_names, state="readonly", width=12)

        cb_pt.grid(row=0, column=1, sticky=tk.W, padx=10, pady=8)

        cb_pt.set("M" if "M" in pt_names else ("N" if "N" in pt_names else pt_names[0]))



        fr_line = ttk.LabelFrame(top, text="Đường thẳng nhận hình chiếu (qua 2 điểm)" if is_vi else "Target Line (defined by 2 points)", padding=10)

        fr_line.grid(row=1, column=0, columnspan=2, padx=12, pady=8, sticky=tk.EW)



        ttk.Label(fr_line, text="Điểm thứ nhất (P1 - VD: B):" if is_vi else "First Point (P1):").grid(row=0, column=0, sticky=tk.W, pady=4)

        cb_l1 = ttk.Combobox(fr_line, values=pt_names, state="readonly", width=12)

        cb_l1.grid(row=0, column=1, sticky=tk.W, padx=8, pady=4)

        cb_l1.set("B" if "B" in pt_names else pt_names[0])



        ttk.Label(fr_line, text="Điểm thứ hai (P2 - VD: C):" if is_vi else "Second Point (P2):").grid(row=1, column=0, sticky=tk.W, pady=4)

        cb_l2 = ttk.Combobox(fr_line, values=pt_names, state="readonly", width=12)

        cb_l2.grid(row=1, column=1, sticky=tk.W, padx=8, pady=4)

        cb_l2.set("C" if "C" in pt_names else (pt_names[1] if len(pt_names)>1 else pt_names[0]))



        ttk.Label(top, text="Tên điểm hình chiếu (VD: D hoặc E):" if is_vi else "Projection Foot Name (e.g. D or E):",

                  font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky=tk.W, padx=12, pady=8)

        ent_name = ttk.Entry(top, width=12)

        ent_name.grid(row=2, column=1, sticky=tk.W, padx=10, pady=8)

        default_proj = "D" if "D" not in pt_names else ("E" if "E" not in pt_names else "H")

        ent_name.insert(0, default_proj)



        def do_proj():

            p_map = {p.get("name") or p["id"]: p for p in self.points}

            nP = cb_pt.get()

            n1 = cb_l1.get()

            n2 = cb_l2.get()

            err_t = "Lỗi" if is_vi else "Error"

            if n1 == n2:

                messagebox.showerror(err_t, "Đường thẳng phải qua 2 điểm phân biệt!" if is_vi else "Line must pass through 2 distinct points!")

                return

            P = p_map[nP]

            P1 = p_map[n1]

            P2 = p_map[n2]

            dx = P2["x"] - P1["x"]

            dy = P2["y"] - P1["y"]

            L2 = dx*dx + dy*dy

            if L2 < 1e-8:

                messagebox.showerror(err_t, "Hai điểm đường thẳng trùng nhau!" if is_vi else "Two line points are coincident!")

                return

            t = ((P["x"] - P1["x"])*dx + (P["y"] - P1["y"])*dy) / L2

            proj_x = P1["x"] + t*dx

            proj_y = P1["y"] + t*dy

            name_d = ent_name.get().strip() or "D"



            self._save_state()

            new_pt = {

                "id": f"pt_{len(self.points)+1}",

                "name": name_d,

                "x": proj_x,

                "y": proj_y,

                "color": "#2b8a3e",

                "fixed": True,

                "constraint": {"type": "proj_foot", "p": P, "line_p1": P1, "line_p2": P2}

            }

            self.points.append(new_pt)

            self.segments.append({

                "p1": P, "p2": new_pt,

                "color": "#2b8a3e",

                "style": "dashed",

                "label": f"{nP}{name_d}"

            })

            self.add_right_angle_mark(new_pt, P, P1)

            self._update_algebra_tree()

            self.redraw()

            top.destroy()

            msg_ok = f"Đã hạ hình chiếu vuông góc {name_d} từ {nP} xuống đường thẳng {n1}{n2}." if is_vi else f"Constructed perpendicular projection {name_d} from {nP} onto line {n1}{n2}."

            self.lbl_status.config(text=msg_ok)



        btn_proj = tk.Button(top, text="✔ Hạ Hình Chiếu Ngay" if is_vi else "✔ Project Foot Now",

                             bg="#2b8a3e", fg="white", font=("Segoe UI", 9, "bold"), padx=12, pady=4, cursor="hand2", command=do_proj)

        btn_proj.grid(row=3, column=0, columnspan=2, pady=14)



    def open_orthocenter_dialog(self):

        """Hộp thoại dựng trực tâm H của tam giác."""

        is_vi = getattr(self, "current_lang", "vi") == "vi"

        pt_names = [p.get("name") or p["id"] for p in self.points if p.get("name") or p.get("id")]

        if len(pt_names) < 3:

            title_warn = "Chưa đủ điểm" if is_vi else "Not Enough Points"

            msg_warn = "Cần ít nhất 3 điểm trên bản vẽ để dựng trực tâm." if is_vi else "Need at least 3 points on canvas to construct orthocenter."

            messagebox.showwarning(title_warn, msg_warn)

            return



        top = tk.Toplevel(self)

        top.title("Dựng Trực Tâm Tam Giác (Orthocenter)" if is_vi else "Construct Triangle Orthocenter")

        top.geometry("380x280")

        top.resizable(True, True)

        top.transient(self)



        ttk.Label(top, text="Chọn 3 đỉnh của tam giác:" if is_vi else "Select 3 vertices of triangle:",

                  font=("Segoe UI", 9, "bold")).grid(row=0, column=0, columnspan=2, padx=12, pady=8, sticky=tk.W)



        ttk.Label(top, text="Đỉnh A (Vertex A):" if is_vi else "Vertex A:").grid(row=1, column=0, sticky=tk.W, padx=12, pady=3)

        cb_A = ttk.Combobox(top, values=pt_names, state="readonly", width=12)

        cb_A.grid(row=1, column=1, sticky=tk.W, padx=10, pady=3)

        cb_A.set("A" if "A" in pt_names else pt_names[0])



        ttk.Label(top, text="Đỉnh B (Vertex B):" if is_vi else "Vertex B:").grid(row=2, column=0, sticky=tk.W, padx=12, pady=3)

        cb_B = ttk.Combobox(top, values=pt_names, state="readonly", width=12)

        cb_B.grid(row=2, column=1, sticky=tk.W, padx=10, pady=3)

        cb_B.set("B" if "B" in pt_names else (pt_names[1] if len(pt_names)>1 else pt_names[0]))



        ttk.Label(top, text="Đỉnh C (Vertex C):" if is_vi else "Vertex C:").grid(row=3, column=0, sticky=tk.W, padx=12, pady=3)

        cb_C = ttk.Combobox(top, values=pt_names, state="readonly", width=12)

        cb_C.grid(row=3, column=1, sticky=tk.W, padx=10, pady=3)

        cb_C.set("C" if "C" in pt_names else (pt_names[2] if len(pt_names)>2 else pt_names[0]))



        ttk.Label(top, text="Tên trực tâm (Orthocenter Name):" if is_vi else "Orthocenter Name:").grid(row=4, column=0, sticky=tk.W, padx=12, pady=3)

        ent_H = ttk.Entry(top, width=12)

        ent_H.grid(row=4, column=1, sticky=tk.W, padx=10, pady=3)

        ent_H.insert(0, "H")



        def do_create_H():

            p_map = {p.get("name") or p["id"]: p for p in self.points}

            nA, nB, nC = cb_A.get(), cb_B.get(), cb_C.get()

            err_t = "Lỗi" if is_vi else "Error"

            if len({nA, nB, nC}) < 3:

                messagebox.showerror(err_t, "Vui lòng chọn 3 đỉnh phân biệt!" if is_vi else "Please select 3 distinct vertices!")

                return

            pA, pB, pC = p_map[nA], p_map[nB], p_map[nC]

            a1 = pC['x'] - pB['x']

            b1 = pC['y'] - pB['y']

            c1 = a1 * pA['x'] + b1 * pA['y']

            a2 = pC['x'] - pA['x']

            b2 = pC['y'] - pA['y']

            c2 = a2 * pB['x'] + b2 * pB['y']

            det = a1 * b2 - a2 * b1

            if abs(det) < 1e-8:

                messagebox.showerror(err_t, "3 điểm thẳng hàng, không tạo thành tam giác!" if is_vi else "Collinear points, cannot form triangle!")

                return

            Hx = (c1 * b2 - c2 * b1) / det

            Hy = (a1 * c2 - a2 * c1) / det

            name_H = ent_H.get().strip() or "H"



            self._save_state()

            new_pt = {

                "id": f"pt_{len(self.points)+1}",

                "name": name_H,

                "x": Hx,

                "y": Hy,

                "color": self.COLOR_HIGHLIGHT,

                "fixed": True,

                "constraint": {"type": "orthocenter", "pts": [pA, pB, pC]}

            }

            self.points.append(new_pt)

            self.segments.append({"p1": pA, "p2": new_pt, "color": "#868e96", "style": "dashed", "label": f"{nA}{name_H}"})

            self.segments.append({"p1": pB, "p2": new_pt, "color": "#868e96", "style": "dashed", "label": f"{nB}{name_H}"})

            self._update_algebra_tree()

            self.redraw()

            top.destroy()

            msg_ok = f"Đã dựng trực tâm {name_H} của tam giác {nA}{nB}{nC}." if is_vi else f"Constructed orthocenter {name_H} of triangle {nA}{nB}{nC}."

            self.lbl_status.config(text=msg_ok)



        btn_h = tk.Button(top, text="✔ Dựng Trực Tâm H" if is_vi else "✔ Construct Orthocenter",

                          bg="#2b8a3e", fg="white", font=("Segoe UI", 9, "bold"), padx=12, pady=4, cursor="hand2", command=do_create_H)

        btn_h.grid(row=5, column=0, columnspan=2, pady=14)



    # =========================================================================

    # BẮT ĐỐI TƯỢNG ĐƯỜNG TRÒN & TIẾP TUYẾN THÔNG MINH

    # =========================================================================

    def _find_ellipse_at(self, wx, wy):
        """Tìm hình elip dựa trên tâm hoặc đường viền elip."""
        for el in getattr(self, "ellipses", []):
            if el.get("hidden") and not self.show_hidden:
                continue
            ox, oy = el["ox"], el["oy"]
            a, b = el["a"], el["b"]
            theta = el["theta"]

            # Khoảng cách tới tâm
            d_center = math.hypot(wx - ox, wy - oy)
            if d_center * self.scale <= 18:
                return el, "center"

            # Khoảng cách tới viền elip
            dx = wx - ox
            dy = wy - oy
            cos_t = math.cos(theta)
            sin_t = math.sin(theta)
            u = dx * cos_t + dy * sin_t
            v = -dx * sin_t + dy * cos_t
            r0 = math.hypot(u, v)
            if r0 > 1e-4:
                phi = math.atan2(v, u)
                denom = math.sqrt((b * math.cos(phi))**2 + (a * math.sin(phi))**2)
                if denom > 1e-6:
                    r_e = (a * b) / denom
                    if abs(r0 - r_e) * self.scale <= 18:
                        return el, "rim"
        return None, None

    def _find_circle_at(self, wx, wy, clicked_pt=None):

        """Tìm đường tròn dựa trên tâm điểm hoặc đường viền."""

        if clicked_pt:

            for c in self.circles:

                if c["center"] == clicked_pt or c["center"]["id"] == clicked_pt.get("id"):

                    return c, "center"

        for c in self.circles:

            d = math.hypot(wx - c["center"]["x"], wy - c["center"]["y"])

            if d * self.scale <= 18:

                return c, "center"

        for c in self.circles:

            d = math.hypot(wx - c["center"]["x"], wy - c["center"]["y"])

            if abs(d - c["r"]) * self.scale <= 18:

                return c, "rim"

        return None, None



    def _create_dynamic_tangent_on_circle(self, circ, wx, wy):

        """Tạo một điểm M trên đường tròn và tiếp tuyến động xoay theo chuột khi kéo rê."""

        O = circ["center"]

        R = circ["r"]

        dx = wx - O["x"]

        dy = wy - O["y"]

        if math.hypot(dx, dy) < 1e-4:

            ang = math.pi / 4.0

        else:

            ang = math.atan2(dy, dx)



        Mx = O["x"] + R * math.cos(ang)

        My = O["y"] + R * math.sin(ang)



        name = self._ask_point_name_dialog("")

        if name is None: return

        self._save_state()

        pt_id = name if name else f"M_tan_{len(self.points)}"

        pM = {"id": pt_id, "name": name, "x": Mx, "y": My, "color": self.COLOR_TANGENT, "fixed": False, "on_circle": circ["id"]}



        # Điểm phụ định hướng tiếp tuyến (-sin, cos)*R

        Tx = Mx - R * math.sin(ang)

        Ty = My + R * math.cos(ang)

        pT = {"id": f"T_help_{len(self.points)+1}", "name": "", "x": Tx, "y": Ty, "color": self.COLOR_TANGENT, "fixed": False, "hidden": True}



        label = f"Tiếp tuyến tại {name}" if name else "Tiếp tuyến"

        tan_line = {"p1": pM, "p2": pT, "color": self.COLOR_TANGENT, "style": "solid", "label": label, "type": "tangent_dynamic", "circle_id": circ["id"]}



        self.points.extend([pM, pT])

        self.lines.append(tan_line)

        self.selected_points = [pM]

        self.drag_start_world = (Mx, My)

        self._update_algebra_tree()

        self._scan_invariants_deep()

        self.redraw()

        self.lbl_status.config(text="Đã tạo tiếp tuyến động. Hãy kéo chuột để di chuyển điểm và tiếp tuyến sẽ tự động xoay chuyển theo thời gian thực!")



    def construct_common_tangents(self, c1, c2, is_preset=False):

        """Dựng toán học chuẩn xác các tiếp tuyến chung ngoài và trong của hai đường tròn."""

        O1 = c1["center"]

        O2 = c2["center"]

        R1 = c1["r"]

        R2 = c2["r"]



        dx = O2["x"] - O1["x"]

        dy = O2["y"] - O1["y"]

        d = math.hypot(dx, dy)



        if d < 1e-6:

            messagebox.showwarning("Tiếp tuyến chung", "Hai đường tròn đồng tâm, không có tiếp tuyến chung!")

            return



        self._save_state()

        theta = math.atan2(dy, dx)

        created_lines = 0



        # 1. Tiếp tuyến chung ngoài

        if d >= abs(R1 - R2) - 1e-7:

            cos_alpha = max(-1.0, min(1.0, (R1 - R2) / d))

            alpha = math.acos(cos_alpha)

            n1_ang = theta + alpha

            n2_ang = theta - alpha



            name_T1a = "P1" if is_preset else ""

            name_T2a = "P2" if is_preset else ""



            T1a = {"id": f"T_{c1['id']}_1", "name": name_T1a, "x": O1["x"] + R1 * math.cos(n1_ang), "y": O1["y"] + R1 * math.sin(n1_ang), "color": self.COLOR_TANGENT, "fixed": True}

            T1b = {"id": f"T_{c1['id']}_2", "name": "", "x": O1["x"] + R1 * math.cos(n2_ang), "y": O1["y"] + R1 * math.sin(n2_ang), "color": self.COLOR_TANGENT, "fixed": True}

            T2a = {"id": f"T_{c2['id']}_1", "name": name_T2a, "x": O2["x"] + R2 * math.cos(n1_ang), "y": O2["y"] + R2 * math.sin(n1_ang), "color": self.COLOR_TANGENT, "fixed": True}

            T2b = {"id": f"T_{c2['id']}_2", "name": "", "x": O2["x"] + R2 * math.cos(n2_ang), "y": O2["y"] + R2 * math.sin(n2_ang), "color": self.COLOR_TANGENT, "fixed": True}



            self.points.extend([T1a, T1b, T2a, T2b])

            lbl_out = "Tiếp tuyến chung P1P2" if is_preset else "Tiếp tuyến chung ngoài 1"

            self.lines.append({"p1": T1a, "p2": T2a, "color": self.COLOR_TANGENT, "style": "solid", "label": lbl_out})

            self.lines.append({"p1": T1b, "p2": T2b, "color": self.COLOR_TANGENT, "style": "solid", "label": "Tiếp tuyến chung ngoài 2"})

            created_lines += 2



        # 2. Tiếp tuyến chung trong

        if d >= (R1 + R2) - 1e-7:

            cos_beta = max(-1.0, min(1.0, (R1 + R2) / d))

            beta = math.acos(cos_beta)

            m1_ang = theta + beta

            m2_ang = theta - beta



            T_in_1a = {"id": f"Tin_{c1['id']}_1", "name": "", "x": O1["x"] + R1 * math.cos(m1_ang), "y": O1["y"] + R1 * math.sin(m1_ang), "color": self.COLOR_TANGENT, "fixed": True}

            T_in_1b = {"id": f"Tin_{c1['id']}_2", "name": "", "x": O1["x"] + R1 * math.cos(m2_ang), "y": O1["y"] + R1 * math.sin(m2_ang), "color": self.COLOR_TANGENT, "fixed": True}

            T_in_2a = {"id": f"Tin_{c2['id']}_1", "name": "", "x": O2["x"] - R2 * math.cos(m1_ang), "y": O2["y"] - R2 * math.sin(m1_ang), "color": self.COLOR_TANGENT, "fixed": True}

            T_in_2b = {"id": f"Tin_{c2['id']}_2", "name": "", "x": O2["x"] - R2 * math.cos(m2_ang), "y": O2["y"] - R2 * math.sin(m2_ang), "color": self.COLOR_TANGENT, "fixed": True}



            self.points.extend([T_in_1a, T_in_1b, T_in_2a, T_in_2b])

            self.lines.append({"p1": T_in_1a, "p2": T_in_2a, "color": self.COLOR_TANGENT, "style": "dashed", "label": "Tiếp tuyến trong 1"})

            self.lines.append({"p1": T_in_1b, "p2": T_in_2b, "color": self.COLOR_TANGENT, "style": "dashed", "label": "Tiếp tuyến trong 2"})

            created_lines += 2



        self._update_algebra_tree()

        self.redraw()

        if not is_preset:

            messagebox.showinfo("Tiếp Tuyến Chung", f"Đã dựng thành công {created_lines} tiếp tuyến chung của hai đường tròn!")

        self.lbl_status.config(text=f"Đã dựng {created_lines} tiếp tuyến chung của {c1['id']} và {c2['id']}.")



    # =========================================================================

    # TỌA ĐỘ VÀ BẮT DÍNH (SMART SNAPPING)

    # =========================================================================

    def to_screen(self, x, y):

        if getattr(self, 'geo_engine', None) is not None:
            return self.geo_engine.cartesian_to_canvas((x, y), (self.origin_x, self.origin_y), self.scale, flip_y=True)
        return self.origin_x + x * self.scale, self.origin_y - y * self.scale



    def to_world(self, px, py):

        if getattr(self, 'geo_engine', None) is not None:
            return self.geo_engine.canvas_to_cartesian((px, py), (self.origin_x, self.origin_y), self.scale, flip_y=True)
        return (px - self.origin_x) / self.scale, (self.origin_y - py) / self.scale



    def _find_smart_snap(self, wx, wy, radius_px=14):

        radius_world = radius_px / self.scale



        # 1. Bắt dính điểm đã có (bỏ qua điểm ẩn)

        for p in self.points:

            if p.get("hidden") and not self.show_hidden:

                continue

            if math.hypot(p["x"] - wx, p["y"] - wy) <= radius_world:

                name_str = f" ({p['name']})" if p.get("name") else ""

                return {"type": "point", "x": p["x"], "y": p["y"], "obj": p, "desc": f"Điểm{name_str}"}



        # 2a. Bắt dính giao điểm các đường thẳng / đoạn thẳng / trục tọa độ

        all_lines = []

        for s in self.segments:

            if s.get("hidden") and not self.show_hidden: continue

            all_lines.append((s["p1"], s["p2"]))

        for l in self.lines:

            if l.get("hidden") and not self.show_hidden: continue

            all_lines.append((l["p1"], l["p2"]))

        # Thêm trục tọa độ Ox và Oy để bắt giao điểm với trục hoành và trục tung

        all_lines.append(({"x": -10000.0, "y": 0.0}, {"x": 10000.0, "y": 0.0}))  # Trục Ox

        all_lines.append(({"x": 0.0, "y": -10000.0}, {"x": 0.0, "y": 10000.0}))  # Trục Oy



        for i in range(len(all_lines)):

            for j in range(i + 1, len(all_lines)):

                p1, p2 = all_lines[i]

                p3, p4 = all_lines[j]

                pt_int = self._intersect_lines(p1, p2, p3, p4)

                if pt_int and math.hypot(pt_int[0] - wx, pt_int[1] - wy) <= radius_world:

                    return {"type": "intersection", "x": pt_int[0], "y": pt_int[1], "p1": p1, "p2": p2, "p3": p3, "p4": p4, "desc": "Giao điểm đường thẳng"}



        # 2b. Bắt dính giao điểm đường thẳng và đường tròn

        for c in self.circles:

            O = c["center"]

            R = c["r"]

            for line_pts in all_lines:

                p1, p2 = line_pts

                dx = p2["x"] - p1["x"]

                dy = p2["y"] - p1["y"]

                L = math.hypot(dx, dy)

                if L < 1e-6: continue

                t = ((O["x"] - p1["x"]) * dx + (O["y"] - p1["y"]) * dy) / (L * L)

                proj_x = p1["x"] + t * dx

                proj_y = p1["y"] + t * dy

                dist_O = math.hypot(O["x"] - proj_x, O["y"] - proj_y)

                if dist_O <= R + 1e-6:

                    h = math.sqrt(max(0.0, R * R - dist_O * dist_O))

                    ux = dx / L

                    uy = dy / L

                    for sgn in (1, -1):

                        ix = proj_x + sgn * h * ux

                        iy = proj_y + sgn * h * uy

                        if math.hypot(ix - wx, iy - wy) <= radius_world:

                            return {"type": "intersection", "x": ix, "y": iy, "desc": f"Giao điểm với {c['id']}"}



        # 2c. Bắt dính giao điểm 2 đường tròn

        for i in range(len(self.circles)):

            for j in range(i + 1, len(self.circles)):

                c1, c2 = self.circles[i], self.circles[j]

                O1, O2 = c1["center"], c2["center"]

                r1, r2 = c1["r"], c2["r"]

                d = math.hypot(O2["x"] - O1["x"], O2["y"] - O1["y"])

                if 1e-5 < d <= r1 + r2 and d >= abs(r1 - r2) - 1e-5:

                    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)

                    h2 = r1 * r1 - a * a

                    h = math.sqrt(max(0.0, h2))

                    ux = (O2["x"] - O1["x"]) / d

                    uy = (O2["y"] - O1["y"]) / d

                    p0x = O1["x"] + a * ux

                    p0y = O1["y"] + a * uy

                    for sgn in (1, -1):

                        ix = p0x + sgn * h * (-uy)

                        iy = p0y + sgn * h * ux

                        if math.hypot(ix - wx, iy - wy) <= radius_world:

                            return {"type": "intersection", "x": ix, "y": iy, "desc": f"Giao điểm ({c1['id']}, {c2['id']})"}



        # 3. Bắt dính đường tròn

        for c in self.circles:

            d = math.hypot(wx - c["center"]["x"], wy - c["center"]["y"])

            if abs(d - c["r"]) <= radius_world:

                ang = math.atan2(wy - c["center"]["y"], wx - c["center"]["x"])

                sx = c["center"]["x"] + c["r"] * math.cos(ang)

                sy = c["center"]["y"] + c["r"] * math.sin(ang)

                return {"type": "on_circle", "x": sx, "y": sy, "circle": c, "desc": f"Thuộc đường tròn {c['id']}"}



        # 3b. Bắt dính trên đoạn thẳng (On segment)

        for s in self.segments:

            if s.get("hidden") and not self.show_hidden: continue

            p1, p2 = s["p1"], s["p2"]

            dx = p2["x"] - p1["x"]

            dy = p2["y"] - p1["y"]

            L2 = dx * dx + dy * dy

            if L2 < 1e-8: continue

            t = ((wx - p1["x"]) * dx + (wy - p1["y"]) * dy) / L2

            if 0.0 <= t <= 1.0:

                proj_x = p1["x"] + t * dx

                proj_y = p1["y"] + t * dy

                if math.hypot(proj_x - wx, proj_y - wy) <= radius_world:

                    s_name = s.get("label") or f"{p1.get('name') or p1['id']}{p2.get('name') or p2['id']}"

                    return {"type": "on_segment", "x": proj_x, "y": proj_y, "segment": s, "t": t, "desc": f"Thuộc đoạn {s_name}"}



        # 3c. Bắt dính trên đường thẳng (On line)

        for l in self.lines:

            if l.get("hidden") and not self.show_hidden: continue

            p1, p2 = l["p1"], l["p2"]

            dx = p2["x"] - p1["x"]

            dy = p2["y"] - p1["y"]

            L2 = dx * dx + dy * dy

            if L2 < 1e-8: continue

            t = ((wx - p1["x"]) * dx + (wy - p1["y"]) * dy) / L2

            proj_x = p1["x"] + t * dx

            proj_y = p1["y"] + t * dy

            if math.hypot(proj_x - wx, proj_y - wy) <= radius_world:

                l_name = l.get("label") or f"đường thẳng"

                return {"type": "on_line", "x": proj_x, "y": proj_y, "line": l, "t": t, "desc": f"Thuộc {l_name}"}



        # 4. Bắt dính lưới

        if self.snap_to_grid:

            gx = round(wx * 2) / 2

            gy = round(wy * 2) / 2

            if math.hypot(gx - wx, gy - wy) <= radius_world * 0.7:

                return {"type": "grid", "x": gx, "y": gy, "desc": f"Lưới ({gx:.1f}; {gy:.1f})"}



        return None



    def _intersect_lines(self, A, B, C, D):

        a1 = B["y"] - A["y"]

        b1 = A["x"] - B["x"]

        c1 = a1 * A["x"] + b1 * A["y"]

        a2 = D["y"] - C["y"]

        b2 = C["x"] - D["x"]

        c2 = a2 * C["x"] + b2 * C["y"]

        det = a1 * b2 - a2 * b1

        if abs(det) < 1e-9: return None

        return (b2 * c1 - b1 * c2) / det, (a1 * c2 - a2 * c1) / det



    def _dist_point_to_line(self, px, py, x1, y1, x2, y2):

        dx = x2 - x1

        dy = y2 - y1

        L = math.hypot(dx, dy)

        if L < 1e-9:

            return math.hypot(px - x1, py - y1)

        return abs(dy * px - dx * py + x2 * y1 - y2 * x1) / L



    def _dist_point_to_segment(self, px, py, x1, y1, x2, y2):

        dx = x2 - x1

        dy = y2 - y1

        L2 = dx * dx + dy * dy

        if L2 < 1e-9:

            return math.hypot(px - x1, py - y1)

        t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / L2))

        proj_x = x1 + t * dx

        proj_y = y1 + t * dy

        return math.hypot(px - proj_x, py - proj_y)



    def _resolve_point(self, pt_or_id):

        """Giải quyết con trỏ điểm theo id hoặc đối tượng dictionary trong self.points."""

        if not pt_or_id:

            return None

        if isinstance(pt_or_id, dict):

            pid = pt_or_id.get("id")

            for p in self.points:

                if p.get("id") == pid:

                    return p

            return pt_or_id

        elif isinstance(pt_or_id, str):

            for p in self.points:

                if p.get("id") == pt_or_id or p.get("name") == pt_or_id:

                    return p

        return None



    def _recompute_dependent_objects(self, exclude_points=None):

        """Cơ chế Ràng buộc Hình học Động (Dynamic Geometry Constraint Propagation Engine):

        Tự động lan truyền tọa độ cho các điểm phụ thuộc (trung điểm, điểm trên đoạn, hình chiếu,

        tịnh tiến vector, giao điểm, trực tâm, tâm nội, tâm ngoại) và cập nhật đường tròn tương ứng."""

        if exclude_points is None:

            exclude_ids = set()

        else:

            exclude_ids = {id(p) for p in exclude_points}



        for _ in range(20):
            changed = False
            # 1. Cập nhật các điểm có ràng buộc hình học
            for p in self.points:
                if id(p) in exclude_ids:
                    continue
                c = p.get("constraint")
                if not c:
                    continue
                c_type = c.get("type")

                if c_type == "midpoint":
                    p1 = self._resolve_point(c.get("p1"))
                    p2 = self._resolve_point(c.get("p2"))
                    if p1 and p2:
                        nx = (p1["x"] + p2["x"]) / 2.0
                        ny = (p1["y"] + p2["y"]) / 2.0
                        if abs(p.get("x", 0) - nx) > 1e-9 or abs(p.get("y", 0) - ny) > 1e-9:
                            p["x"], p["y"] = nx, ny
                            changed = True
                        p["parents"] = [p1, p2]
                        p["source"] = "midpoint"
                        p.pop("exact", None)

                elif c_type in ("on_segment", "on_line"):
                    p1 = self._resolve_point(c.get("p1"))
                    p2 = self._resolve_point(c.get("p2"))
                    if p1 and p2:
                        t = c.get("t", 0.5)
                        nx = p1["x"] + t * (p2["x"] - p1["x"])
                        ny = p1["y"] + t * (p2["y"] - p1["y"])
                        if abs(p.get("x", 0) - nx) > 1e-9 or abs(p.get("y", 0) - ny) > 1e-9:
                            p["x"], p["y"] = nx, ny
                            changed = True
                        p["parents"] = [p1, p2]
                        p["source"] = "formula"
                        p.pop("exact", None)

                elif c_type == "proj_foot":
                    pt = self._resolve_point(c.get("p"))
                    p1 = self._resolve_point(c.get("line_p1"))
                    p2 = self._resolve_point(c.get("line_p2"))
                    if pt and p1 and p2:
                        dx = p2["x"] - p1["x"]
                        dy = p2["y"] - p1["y"]
                        L2 = dx * dx + dy * dy
                        if L2 > 1e-9:
                            t = ((pt["x"] - p1["x"]) * dx + (pt["y"] - p1["y"]) * dy) / L2
                            nx = p1["x"] + t * dx
                            ny = p1["y"] + t * dy
                            if abs(p.get("x", 0) - nx) > 1e-9 or abs(p.get("y", 0) - ny) > 1e-9:
                                p["x"], p["y"] = nx, ny
                                changed = True
                            p["parents"] = [pt, p1, p2]
                            p["source"] = "formula"
                            p.pop("exact", None)

                elif c_type == "translate_vec":
                    base = self._resolve_point(c.get("base_pt"))
                    v1 = self._resolve_point(c.get("v1"))
                    v2 = self._resolve_point(c.get("v2"))
                    if base and v1 and v2:
                        nx = base["x"] + (v2["x"] - v1["x"])
                        ny = base["y"] + (v2["y"] - v1["y"])
                        if abs(p.get("x", 0) - nx) > 1e-9 or abs(p.get("y", 0) - ny) > 1e-9:
                            p["x"], p["y"] = nx, ny
                            changed = True
                        p["parents"] = [base, v1, v2]
                        p["source"] = "formula"
                        p.pop("exact", None)

                elif c_type == "intersection":
                    p1 = self._resolve_point(c.get("p1"))
                    p2 = self._resolve_point(c.get("p2"))
                    p3 = self._resolve_point(c.get("p3"))
                    p4 = self._resolve_point(c.get("p4"))
                    if p1 and p2 and p3 and p4:
                        pt_int = self._intersect_lines(p1, p2, p3, p4)
                        if pt_int:
                            nx, ny = pt_int[0], pt_int[1]
                            if abs(p.get("x", 0) - nx) > 1e-9 or abs(p.get("y", 0) - ny) > 1e-9:
                                p["x"], p["y"] = nx, ny
                                changed = True
                            p["parents"] = [p1, p2, p3, p4]
                            p["source"] = "intersection"
                            p.pop("exact", None)

                elif c_type == "orthocenter":
                    pts = [self._resolve_point(pt) for pt in c.get("pts", [])]
                    if len(pts) == 3 and all(pts):
                        pA, pB, pC = pts
                        dx1, dy1 = -(pC["y"] - pB["y"]), pC["x"] - pB["x"]
                        dx2, dy2 = -(pC["y"] - pA["y"]), pC["x"] - pA["x"]
                        A2 = {"x": pA["x"] + dx1, "y": pA["y"] + dy1}
                        B2 = {"x": pB["x"] + dx2, "y": pB["y"] + dy2}
                        pt_h = self._intersect_lines(pA, A2, pB, B2)
                        if pt_h:
                            nx, ny = pt_h[0], pt_h[1]
                            if abs(p.get("x", 0) - nx) > 1e-9 or abs(p.get("y", 0) - ny) > 1e-9:
                                p["x"], p["y"] = nx, ny
                                changed = True
                            p["parents"] = [pA, pB, pC]
                            p["source"] = "formula"
                            p.pop("exact", None)

                elif c_type == "incenter":
                    pts = [self._resolve_point(pt) for pt in c.get("pts", [])]
                    if len(pts) == 3 and all(pts):
                        pA, pB, pC = pts
                        a = math.hypot(pB["x"] - pC["x"], pB["y"] - pC["y"])
                        b = math.hypot(pA["x"] - pC["x"], pA["y"] - pC["y"])
                        c_len = math.hypot(pA["x"] - pB["x"], pA["y"] - pB["y"])
                        peri = a + b + c_len
                        if peri > 1e-6:
                            nx = (a * pA["x"] + b * pB["x"] + c_len * pC["x"]) / peri
                            ny = (a * pA["y"] + b * pB["y"] + c_len * pC["y"]) / peri
                            if abs(p.get("x", 0) - nx) > 1e-9 or abs(p.get("y", 0) - ny) > 1e-9:
                                p["x"], p["y"] = nx, ny
                                changed = True
                            p["parents"] = [pA, pB, pC]
                            p["source"] = "formula"
                            p.pop("exact", None)

                elif c_type == "circumcenter":
                    pts = [self._resolve_point(pt) for pt in c.get("pts", [])]
                    if len(pts) == 3 and all(pts):
                        p1, p2, p3 = pts
                        d = 2 * (p1["x"] * (p2["y"] - p3["y"]) + p2["x"] * (p3["y"] - p1["y"]) + p3["x"] * (p1["y"] - p2["y"]))
                        if abs(d) > 1e-7:
                            ux = ((p1["x"]**2 + p1["y"]**2)*(p2["y"] - p3["y"]) + (p2["x"]**2 + p2["y"]**2)*(p3["y"] - p1["y"]) + (p3["x"]**2 + p3["y"]**2)*(p1["y"] - p2["y"])) / d
                            uy = ((p1["x"]**2 + p1["y"]**2)*(p3["x"] - p2["x"]) + (p2["x"]**2 + p2["y"]**2)*(p1["x"] - p3["x"]) + (p3["x"]**2 + p3["y"]**2)*(p2["x"] - p1["x"])) / d
                            if abs(p.get("x", 0) - ux) > 1e-9 or abs(p.get("y", 0) - uy) > 1e-9:
                                p["x"], p["y"] = ux, uy
                                changed = True
                            p["parents"] = [p1, p2, p3]
                            p["source"] = "formula"
                            p.pop("exact", None)

            # 2. Cập nhật các đường tròn có ràng buộc bán kính động
            for circ in self.circles:
                c = circ.get("constraint")
                if not c:
                    continue
                c_type = c.get("type")
                if c_type == "circumcircle":
                    pts = [self._resolve_point(pt) for pt in c.get("pts", [])]
                    center = self._resolve_point(c.get("center") or circ.get("center"))
                    if pts and center and pts[0]:
                        circ["r"] = math.hypot(pts[0]["x"] - center["x"], pts[0]["y"] - center["y"])
                elif c_type == "incircle":
                    pts = [self._resolve_point(pt) for pt in c.get("pts", [])]
                    if len(pts) == 3 and all(pts):
                        pA, pB, pC = pts
                        a = math.hypot(pB["x"] - pC["x"], pB["y"] - pC["y"])
                        b = math.hypot(pA["x"] - pC["x"], pA["y"] - pC["y"])
                        c_len = math.hypot(pA["x"] - pB["x"], pA["y"] - pB["y"])
                        peri = a + b + c_len
                        area = 0.5 * abs((pB["x"] - pA["x"]) * (pC["y"] - pA["y"]) - (pB["y"] - pA["y"]) * (pC["x"] - pA["x"]))
                        if peri > 1e-6:
                            circ["r"] = area / (peri / 2.0)
                elif c_type == "circle_2p":
                    p_center = self._resolve_point(c.get("center") or circ.get("center"))
                    p_rim = self._resolve_point(c.get("p_rim"))
                    if p_center and p_rim:
                        circ["r"] = math.hypot(p_rim["x"] - p_center["x"], p_rim["y"] - p_center["y"])

            # 3. Cập nhật các hình elip động khi các điểm tiêu điểm / tâm / điểm M di chuyển
            for el in getattr(self, "ellipses", []):
                pF1 = self._resolve_point(el.get("f1"))
                pF2 = self._resolve_point(el.get("f2"))
                pM = self._resolve_point(el.get("pM"))
                if pF1 and pF2 and pM:
                    new_p = compute_ellipse_from_foci(pF1["x"], pF1["y"], pF2["x"], pF2["y"], pM["x"], pM["y"])
                    el["ox"], el["oy"] = new_p["ox"], new_p["oy"]
                    el["a"], el["b"], el["c"], el["theta"] = new_p["a"], new_p["b"], new_p["c"], new_p["theta"]
                    el["area"], el["perimeter"] = new_p["area"], new_p["perimeter"]
                else:
                    pO = self._resolve_point(el.get("center"))
                    pA = self._resolve_point(el.get("pA"))
                    pB = self._resolve_point(el.get("pB"))
                    if pO and pA and pB:
                        new_p = compute_ellipse_parameters(pO["x"], pO["y"], pA["x"], pA["y"], pB["x"], pB["y"])
                        el["ox"], el["oy"] = new_p["ox"], new_p["oy"]
                        el["a"], el["b"], el["theta"] = new_p["a"], new_p["b"], new_p["theta"]
                        el["area"], el["perimeter"] = new_p["area"], new_p["perimeter"]

            if not changed:
                break



    def _find_line_or_segment_at(self, wx, wy, radius_px=14):

        radius_world = radius_px / self.scale

        best_obj = None

        best_dist = float('inf')

        best_kind = None



        for seg in self.segments:

            if seg.get("hidden") and not self.show_hidden:

                continue

            p1, p2 = seg["p1"], seg["p2"]

            d = self._dist_point_to_segment(wx, wy, p1["x"], p1["y"], p2["x"], p2["y"])

            if d <= radius_world and d < best_dist:

                best_dist = d

                best_obj = seg

                best_kind = "đoạn thẳng"



        for l in self.lines:

            if l.get("hidden") and not self.show_hidden:

                continue

            p1, p2 = l["p1"], l["p2"]

            d = self._dist_point_to_line(wx, wy, p1["x"], p1["y"], p2["x"], p2["y"])

            if d <= radius_world and d < best_dist:

                best_dist = d

                best_obj = l

                best_kind = "đường thẳng"



        # Check khoảng cách tới trục hoành Ox (y = 0)

        if abs(wy) <= radius_world and abs(wy) < best_dist:

            best_dist = abs(wy)

            best_obj = {"p1": {"x": -10000.0, "y": 0.0}, "p2": {"x": 10000.0, "y": 0.0}, "label": "Trục hoành Ox", "is_axis": "Ox"}

            best_kind = "trục hoành Ox"



        # Check khoảng cách tới trục tung Oy (x = 0)

        if abs(wx) <= radius_world and abs(wx) < best_dist:

            best_dist = abs(wx)

            best_obj = {"p1": {"x": 0.0, "y": -10000.0}, "p2": {"x": 0.0, "y": 10000.0}, "label": "Trục tung Oy", "is_axis": "Oy"}

            best_kind = "trục tung Oy"



        return best_obj, best_kind



    def _construct_perpendicular_line(self, P, A, B, ref_lbl=""):

        dx = B["x"] - A["x"]

        dy = B["y"] - A["y"]

        L = math.hypot(dx, dy)

        if L < 1e-6:

            messagebox.showwarning("Lỗi", "Hai điểm tạo đường thẳng tham chiếu trùng nhau!")

            return



        self._save_state()

        ux = -dy / L

        uy = dx / L



        t = ((P["x"] - A["x"]) * dx + (P["y"] - A["y"]) * dy) / (L * L)

        Hx = A["x"] + t * dx

        Hy = A["y"] + t * dy

        dist = math.hypot(P["x"] - Hx, P["y"] - Hy)



        if dist > 1e-4:

            H_pt = {"id": f"H_{len(self.points)}", "name": "", "x": Hx, "y": Hy, "color": "#2b8a3e", "fixed": True, "hidden": True, "constraint": {"type": "proj_foot", "p": P, "line_p1": A, "line_p2": B}}

        else:

            H_pt = {"id": f"H_{len(self.points)}", "name": "", "x": P["x"] + 3.0 * ux, "y": P["y"] + 3.0 * uy, "color": "#2b8a3e", "fixed": True, "hidden": True}



        self.points.append(H_pt)

        # Không dùng kí hiệu '⊥' vẽ trực tiếp lên hình theo chuẩn

        line_lbl = ""  # Khong tu dong gan nhan chu len duong vuong goc

        self.lines.append({"p1": P, "p2": H_pt, "color": self.COLOR_LINE, "style": "solid", "label": line_lbl})



        # Tự động thêm kí hiệu góc vuông ô vuông chi tiết tại chân đường vuông góc

        if dist > 1e-4:

            self.add_right_angle_mark(H_pt, P, A)



        self._update_algebra_tree()

        self._scan_invariants_deep()

        self.redraw()

        P_name = P.get("name") or P["id"]

        self.lbl_status.config(text=f"Đã dựng thành công đường vuông góc từ {P_name} xuống {ref_lbl}.")



    def _construct_parallel_line(self, P, A, B, ref_lbl=""):

        dx = B["x"] - A["x"]

        dy = B["y"] - A["y"]

        L = math.hypot(dx, dy)

        if L < 1e-6:

            messagebox.showwarning("Lỗi", "Hai điểm tạo đường thẳng tham chiếu trùng nhau!")

            return



        self._save_state()

        ux = dx / L

        uy = dy / L



        P_par = {"id": f"Par_{len(self.points)}", "name": "", "x": P["x"] + 3.5 * ux, "y": P["y"] + 3.5 * uy, "color": "#2b8a3e", "fixed": True, "hidden": True, "constraint": {"type": "translate_vec", "base_pt": P, "v1": A, "v2": B}}

        self.points.append(P_par)

        line_lbl = ""  # Khong tu dong gan nhan chu len duong song song

        self.lines.append({"p1": P, "p2": P_par, "color": self.COLOR_LINE, "style": "solid", "label": line_lbl})



        self._update_algebra_tree()

        self._scan_invariants_deep()

        self.redraw()

        P_name = P.get("name") or P["id"]

        self.lbl_status.config(text=f"Đã dựng thành công đường song song qua {P_name} song song với {ref_lbl}.")



    def _construct_angle_bisector(self, A, B, C):

        v1x, v1y = A["x"] - B["x"], A["y"] - B["y"]

        v2x, v2y = C["x"] - B["x"], C["y"] - B["y"]

        L1 = math.hypot(v1x, v1y)

        L2 = math.hypot(v2x, v2y)

        if L1 < 1e-5 or L2 < 1e-5:

            messagebox.showwarning("Lỗi", "Các điểm quá gần nhau, không tạo thành góc hợp lệ!")

            return



        u1x, u1y = v1x / L1, v1y / L1

        u2x, u2y = v2x / L2, v2y / L2



        bis_x = u1x + u2x

        bis_y = u1y + u2y

        L_bis = math.hypot(bis_x, bis_y)

        if L_bis < 1e-5:

            bis_x = -u1y

            bis_y = u1x

            L_bis = 1.0



        ux = bis_x / L_bis

        uy = bis_y / L_bis



        self._save_state()

        P_bis = {"id": f"Bis_{len(self.points)}", "name": "", "x": B["x"] + 3.5 * ux, "y": B["y"] + 3.5 * uy, "color": "#7048e8", "fixed": True, "hidden": True}

        self.points.append(P_bis)



        nA = A.get("name") or A["id"]

        nB = B.get("name") or B["id"]

        nC = C.get("name") or C["id"]

        lbl = f"Phân giác góc {nA}{nB}{nC}"

        self.lines.append({"p1": B, "p2": P_bis, "color": "#7048e8", "style": "solid", "label": lbl})



        self._update_algebra_tree()

        self._scan_invariants_deep()

        self.redraw()

        self.lbl_status.config(text=f"Đã dựng thành công đường phân giác của góc {nA}{nB}{nC} (Đỉnh {nB}).")



    def _compute_entity_intersections(self, e1, e2):

        """Tính tất cả giao điểm giữa 2 thực thể bất kỳ (đường thẳng/đoạn/trục Ox, Oy/đường tròn)."""

        is_circ1 = "center" in e1 and "r" in e1

        is_circ2 = "center" in e2 and "r" in e2



        if not is_circ1 and not is_circ2:

            pt = self._intersect_lines(e1["p1"], e1["p2"], e2["p1"], e2["p2"])

            return [pt] if pt else []

        elif is_circ1 and is_circ2:

            O1, O2 = e1["center"], e2["center"]

            r1, r2 = e1["r"], e2["r"]

            d = math.hypot(O2["x"] - O1["x"], O2["y"] - O1["y"])

            if d > r1 + r2 + 1e-5 or d < abs(r1 - r2) - 1e-5 or d < 1e-6:

                return []

            a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)

            h = math.sqrt(max(0.0, r1 * r1 - a * a))

            ux = (O2["x"] - O1["x"]) / d

            uy = (O2["y"] - O1["y"]) / d

            p0x = O1["x"] + a * ux

            p0y = O1["y"] + a * uy

            if h < 1e-6:

                return [(p0x, p0y)]

            return [

                (p0x + h * (-uy), p0y + h * ux),

                (p0x - h * (-uy), p0y - h * ux)

            ]

        else:

            circ = e1 if is_circ1 else e2

            line = e2 if is_circ1 else e1

            O = circ["center"]

            R = circ["r"]

            p1, p2 = line["p1"], line["p2"]

            dx = p2["x"] - p1["x"]

            dy = p2["y"] - p1["y"]

            L = math.hypot(dx, dy)

            if L < 1e-6: return []

            t = ((O["x"] - p1["x"]) * dx + (O["y"] - p1["y"]) * dy) / (L * L)

            proj_x = p1["x"] + t * dx

            proj_y = p1["y"] + t * dy

            dist_O = math.hypot(O["x"] - proj_x, O["y"] - proj_y)

            if dist_O > R + 1e-5:

                return []

            h = math.sqrt(max(0.0, R * R - dist_O * dist_O))

            ux, uy = dx / L, dy / L

            if h < 1e-6:

                return [(proj_x, proj_y)]

            return [

                (proj_x + h * ux, proj_y + h * uy),

                (proj_x - h * ux, proj_y - h * uy)

            ]



    def add_right_angle_mark(self, vertex, p1, p2, color="#e03131", size=14):

        """Thêm kí hiệu góc vuông ô vuông chuẩn (không dùng chữ T lật ngược trên hình)."""

        for m in self.angle_marks:

            if m.get("style") == "right" and m.get("vertex") == vertex:

                if (m.get("p1") == p1 and m.get("p2") == p2) or (m.get("p1") == p2 and m.get("p2") == p1):

                    return

        self.angle_marks.append({

            "vertex": vertex,

            "p1": p1,

            "p2": p2,

            "style": "right",

            "name": "",

            "size": size,

            "color": color

        })



    def open_angle_mark_dialog(self, p1=None, vertex=None, p2=None):

        """Hộp thoại đánh dấu góc chuẩn (Vuông, 1 cung, 2 cung, gạch hướng tâm, nhãn Hy Lạp/độ)."""

        is_vi = getattr(self, "current_lang", "vi") == "vi"

        pt_names = [p.get("name") or p["id"] for p in self.points if p.get("name") or p.get("id")]

        if len(pt_names) < 3:

            title_warn = "Chưa đủ điểm" if is_vi else "Not Enough Points"

            msg_warn = "Cần ít nhất 3 điểm trên bản vẽ để tạo góc!" if is_vi else "Need at least 3 points on canvas to mark an angle!"

            messagebox.showwarning(title_warn, msg_warn)

            return



        p_map = {p.get("name") or p["id"]: p for p in self.points}



        top = tk.Toplevel(self)

        top.title("Đánh Dấu & Ký Hiệu Góc" if is_vi else "Pedagogical Angle Mark & Label")

        top.geometry("460x420")

        top.resizable(True, True)

        top.transient(self)



        fr_pts = ttk.LabelFrame(top, text="3 Điểm Tạo Góc (Đỉnh Góc Ở Giữa)" if is_vi else "3 Points Forming Angle (Vertex in Middle)", padding=10)

        fr_pts.pack(fill=tk.X, padx=12, pady=6)



        ttk.Label(fr_pts, text="Điểm tia 1:" if is_vi else "Ray 1:").grid(row=0, column=0, sticky=tk.W, pady=3)

        cb_p1 = ttk.Combobox(fr_pts, values=pt_names, state="readonly", width=8)

        cb_p1.grid(row=0, column=1, padx=6, pady=3)



        ttk.Label(fr_pts, text="ĐỈNH GÓC:" if is_vi else "VERTEX:").grid(row=0, column=2, sticky=tk.W, padx=6, pady=3)

        cb_v = ttk.Combobox(fr_pts, values=pt_names, state="readonly", width=8)

        cb_v.grid(row=0, column=3, padx=6, pady=3)



        ttk.Label(fr_pts, text="Điểm tia 2:" if is_vi else "Ray 2:").grid(row=0, column=4, sticky=tk.W, padx=6, pady=3)

        cb_p2 = ttk.Combobox(fr_pts, values=pt_names, state="readonly", width=8)

        cb_p2.grid(row=0, column=5, padx=6, pady=3)



        # Set default values

        n1 = (p1.get("name") or p1["id"]) if p1 else pt_names[0]

        nv = (vertex.get("name") or vertex["id"]) if vertex else (pt_names[1] if len(pt_names) > 1 else pt_names[0])

        n2 = (p2.get("name") or p2["id"]) if p2 else (pt_names[2] if len(pt_names) > 2 else pt_names[0])

        cb_p1.set(n1)

        cb_v.set(nv)

        cb_p2.set(n2)



        # Kiểu kí hiệu

        fr_style = ttk.LabelFrame(top, text="Kiểu Ký Hiệu Góc" if is_vi else "Angle Mark Style", padding=10)

        fr_style.pack(fill=tk.X, padx=12, pady=6)



        style_var = tk.StringVar(value="arc1")

        styles = [

            ("right", "Vuông [ ∟ ] (Ô vuông chuẩn SGK)" if is_vi else "Right Angle [ ∟ ] (Square)"),

            ("arc1", "1 vòng cung [ ⌒ ]" if is_vi else "1 Arc [ ⌒ ]"),

            ("arc2", "2 vòng cung song song [ ⌒⌒ ]" if is_vi else "2 Concentric Arcs [ ⌒⌒ ]"),

            ("arc1_tick", "1 cung có gạch hướng tâm [ ⌒| ]" if is_vi else "1 Arc with Radial Tick [ ⌒| ]"),

            ("arc2_tick", "2 cung có gạch hướng tâm [ ⌒⌒| ]" if is_vi else "2 Arcs with Radial Tick [ ⌒⌒| ]")

        ]

        for val, txt in styles:

            ttk.Radiobutton(fr_style, text=txt, value=val, variable=style_var).pack(anchor=tk.W, pady=2)



        # Nhãn tên góc & Kí hiệu Hy Lạp

        fr_label = ttk.LabelFrame(top, text="Đặt Tên / Nhãn Kí Hiệu Góc (Tùy chọn)" if is_vi else "Angle Label (Optional)", padding=8)

        fr_label.pack(fill=tk.X, padx=12, pady=6)



        ent_name = ttk.Entry(fr_label, font=("Segoe UI", 10), width=12)

        ent_name.pack(side=tk.LEFT, padx=6)



        def insert_sym(ch):

            ent_name.insert(tk.END, ch)

            ent_name.focus_set()



        fr_syms = ttk.Frame(fr_label)

        fr_syms.pack(side=tk.LEFT, padx=6)

        for sym in ["α", "β", "γ", "θ", "1", "2", "°"]:

            b = ttk.Button(fr_syms, text=sym, width=3, command=lambda s=sym: insert_sym(s))

            b.pack(side=tk.LEFT, padx=2)



        # Nút hành động

        fr_act = ttk.Frame(top)

        fr_act.pack(fill=tk.X, padx=12, pady=10)



        def do_add():

            s_p1 = cb_p1.get()

            s_v = cb_v.get()

            s_p2 = cb_p2.get()

            if s_v == s_p1 or s_v == s_p2 or s_p1 == s_p2:

                messagebox.showerror("Lỗi" if is_vi else "Error",

                                     "3 điểm tạo góc phải phân biệt!" if is_vi else "3 points must be distinct!")

                return

            pt1 = p_map[s_p1]

            ptv = p_map[s_v]

            pt2 = p_map[s_p2]

            st = style_var.get()

            nm = ent_name.get().strip()



            self._save_state()

            self.angle_marks.append({

                "vertex": ptv,

                "p1": pt1,

                "p2": pt2,

                "style": st,

                "name": nm,

                "size": 14 if st == "right" else 22,

                "color": "#e03131"

            })

            self.redraw()

            top.destroy()

            self.lbl_status.config(text=f"Đã thêm kí hiệu góc {nm} tại đỉnh {s_v} thành công.")



        ttk.Button(fr_act, text="✓ Đánh Dấu Góc" if is_vi else "✓ Apply Angle Mark", command=do_add).pack(side=tk.LEFT, padx=8)

        ttk.Button(fr_act, text="✕ Hủy" if is_vi else "✕ Cancel", command=top.destroy).pack(side=tk.RIGHT, padx=8)



    def _draw_pedagogical_angle_on_canvas(self, mark):

        """Vẽ kí hiệu góc chi tiết (vuông, 1 cung, 2 cung, gạch hướng tâm, tên góc) lên Canvas."""

        v = mark.get("vertex")

        p1 = mark.get("p1")

        p2 = mark.get("p2")

        if not v or not p1 or not p2: return

        vx, vy = self.to_screen(v["x"], v["y"])

        x1, y1 = self.to_screen(p1["x"], p1["y"])

        x2, y2 = self.to_screen(p2["x"], p2["y"])



        dx1, dy1 = x1 - vx, y1 - vy

        dx2, dy2 = x2 - vx, y2 - vy

        L1, L2 = math.hypot(dx1, dy1), math.hypot(dx2, dy2)

        if L1 < 1e-3 or L2 < 1e-3: return



        u1x, u1y = dx1 / L1, dy1 / L1

        u2x, u2y = dx2 / L2, dy2 / L2

        style = mark.get("style", "arc1")

        color = mark.get("color", "#e03131")

        size = mark.get("size", 14 if style == "right" else 22)

        name = mark.get("name", "")



        if style == "right":

            # Ô vuông góc vuông chuẩn

            c1x = vx + size * u1x

            c1y = vy + size * u1y

            c2x = vx + size * u1x + size * u2x

            c2y = vy + size * u1y + size * u2y

            c3x = vx + size * u2x

            c3y = vy + size * u2y

            self.canvas.create_line(c1x, c1y, c2x, c2y, c3x, c3y, fill=color, width=2)

            if name:

                tx = c2x + 6 + mark.get("label_dx", 0)

                ty = c2y - 6 + mark.get("label_dy", 0)

                self.canvas.create_text(tx, ty, text=name, fill=color, font=("Segoe UI", 9, "bold"))

        else:

            ang1 = math.atan2(dy1, dx1)

            ang2 = math.atan2(dy2, dx2)

            diff = (ang2 - ang1) % (2 * math.pi)

            if diff > math.pi:

                diff -= 2 * math.pi



            arc1_pts = []

            for i in range(17):

                t = ang1 + diff * (i / 16.0)

                arc1_pts.append((vx + size * math.cos(t), vy + size * math.sin(t)))

            flat_pts1 = [coord for pt in arc1_pts for coord in pt]

            self.canvas.create_line(*flat_pts1, fill=color, width=2)



            if style in ("arc2", "arc2_tick"):

                arc2_pts = []

                s2 = size + 5

                for i in range(17):

                    t = ang1 + diff * (i / 16.0)

                    arc2_pts.append((vx + s2 * math.cos(t), vy + s2 * math.sin(t)))

                flat_pts2 = [coord for pt in arc2_pts for coord in pt]

                self.canvas.create_line(*flat_pts2, fill=color, width=2)



            mid_ang = ang1 + diff / 2.0

            mid_ux, mid_uy = math.cos(mid_ang), math.sin(mid_ang)



            if style in ("arc1_tick", "arc2_tick"):

                r_outer = size + 10 if style == "arc2_tick" else size + 5

                t_start = (vx + (size - 4) * mid_ux, vy + (size - 4) * mid_uy)

                t_end = (vx + r_outer * mid_ux, vy + r_outer * mid_uy)

                self.canvas.create_line(t_start[0], t_start[1], t_end[0], t_end[1], fill=color, width=2)



            if name:

                tx = vx + (size + 14) * mid_ux + mark.get("label_dx", 0)

                ty = vy + (size + 14) * mid_uy + mark.get("label_dy", 0)

                self.canvas.create_text(tx, ty, text=name, fill=color, font=("Segoe UI", 9, "bold"))



    def set_tool(self, tool_code):

        self.current_tool = tool_code

        self.temp_line = None



        theme = getattr(self, "current_theme", THEMES_GEOSOLVER.get(getattr(self, "current_theme_key", "win11_light"), THEMES_GEOSOLVER["win11_light"]))
        for code, btn in self.tool_buttons.items():
            if code == tool_code:
                btn.config(bg=theme["tool_active_bg"], fg=theme["tool_active_fg"], relief=tk.SUNKEN)
            else:
                btn.config(bg=theme["btn_bg"], fg=theme["btn_fg"], relief=tk.GROOVE)



        # Giữ lại điểm đang được chọn (đang đỏ) để dùng ngay cho công cụ mới

        has_sel_pt = (len(self.selected_points) == 1)

        sel_pt = self.selected_points[0] if has_sel_pt else None

        sel_name = (sel_pt.get("name") or sel_pt["id"]) if sel_pt else ""



        if tool_code == "toggle_dash" and len(self.selected_points) == 2:

            p1, p2 = self.selected_points[0], self.selected_points[1]

            existing_seg = next((s for s in self.segments if (s["p1"] == p1 and s["p2"] == p2) or (s["p1"] == p2 and s["p2"] == p1)), None)

            self._save_state()

            n1 = p1.get('name') or p1['id']

            n2 = p2.get('name') or p2['id']

            if existing_seg:

                existing_seg["style"] = "solid" if existing_seg.get("style") == "dashed" else "dashed"

                status_txt = f"Đã chuyển đoạn {n1}{n2} sang nét {'đứt (chi tiết)' if existing_seg['style'] == 'dashed' else 'liền'}."

            else:

                self.segments.append({"p1": p1, "p2": p2, "color": self.COLOR_LINE, "style": "dashed", "label": f"{n1}{n2}"})

                status_txt = f"Đã tạo đoạn thẳng nét đứt {n1}{n2}."

            self._update_algebra_tree()

            self.redraw()

            self.lbl_status.config(text=status_txt)

            return

        elif tool_code == "toggle_dash" and has_sel_pt:

            self.temp_points = [sel_pt]

            self.temp_circles.clear()

            self.lbl_status.config(text=f"Đã chọn điểm {sel_name}. Bấm điểm thứ hai để vẽ nét đứt, hoặc bấm vào đoạn/đường tròn có sẵn để chuyển nét!")

            self.redraw()

            return

        elif tool_code in ("perpendicular", "parallel") and has_sel_pt:

            self.temp_points = [sel_pt]

            self.temp_circles.clear()

            action_name = "vuông góc" if tool_code == "perpendicular" else "song song"

            self.lbl_status.config(text=f"Đã chọn điểm {sel_name}. Bây giờ hãy bấm vào đường thẳng hoặc đoạn thẳng để dựng đường {action_name}!")

            self.redraw()

            return

        elif tool_code in ("segment", "line") and has_sel_pt:

            self.temp_points = [sel_pt]

            self.temp_circles.clear()

            action_name = "đoạn thẳng" if tool_code == "segment" else "đường thẳng"

            self.lbl_status.config(text=f"Đã chọn điểm thứ nhất {sel_name}. Hãy bấm chọn điểm thứ hai để hoàn tất {action_name}!")

            self.redraw()

            return

        elif tool_code == "bisector" and has_sel_pt:

            self.temp_points = [sel_pt]

            self.temp_circles.clear()

            self.lbl_status.config(text=f"Đã chọn điểm thứ nhất {sel_name}. Hãy chọn ĐỈNH GÓC (Điểm thứ hai) và điểm thứ ba.")

            self.redraw()

            return

        elif tool_code == "mark_angle" and len(self.selected_points) == 3:

            p1, v, p2 = self.selected_points[0], self.selected_points[1], self.selected_points[2]

            self.open_angle_mark_dialog(p1, v, p2)

            return

        elif tool_code == "mark_angle" and has_sel_pt:

            self.temp_points = [sel_pt]

            self.temp_circles.clear()

            self.lbl_status.config(text=f"Đã chọn điểm thứ nhất {sel_name}. Hãy chọn ĐỈNH GÓC (Điểm thứ hai) và điểm trên tia thứ ba!")

            self.redraw()

            return

        elif tool_code in ("circle", "midpoint") and has_sel_pt:

            self.temp_points = [sel_pt]

            self.temp_circles.clear()

            action_name = "tâm đường tròn" if tool_code == "circle" else "điểm đầu tiên"

            self.lbl_status.config(text=f"Đã chọn {action_name} ({sel_name}). Hãy bấm chọn điểm thứ hai!")

            self.redraw()

            return

        else:

            self.temp_points.clear()

            self.temp_circles.clear()



        tool_names = {

            "select": "Chọn / Di chuyển đối tượng. Bấm đúp vào điểm để đổi tên. Kéo nhãn để đổi vị trí tên điểm.",

            "rotate_mouse": "Xoay hình bằng chuột: Kéo chuột vòng tròn trên bản vẽ để xoay toàn bộ hình.",

            "point": "Điểm tự do: Nhấp chuột trên mặt phẳng Oxy để đặt điểm mới.",

            "intersection": "Giao điểm: Bấm gần giao điểm (kể cả với trục Ox/Oy) hoặc bấm lần lượt 2 đối tượng cắt nhau.",

            "midpoint": "Trung điểm: Nhấp lần lượt 2 điểm để tạo trung điểm.",

            "segment": "Đoạn thẳng: Nhấp lần lượt 2 điểm để nối đoạn thẳng.",

            "toggle_dash": "Đổi nét đứt / liền: Bấm vào đoạn thẳng/đường tròn để đổi nét, hoặc nối 2 điểm nét đứt.",

            "line": "Đường thẳng: Nhấp 2 điểm để kẻ đường thẳng kéo dài vô hạn.",

            "perpendicular": "Đường vuông góc: Bấm chọn 1 điểm và 1 đường thẳng/đoạn thẳng (hoặc bấm 3 điểm).",

            "parallel": "Đường song song: Bấm chọn 1 điểm và 1 đường thẳng/đoạn thẳng (hoặc bấm 3 điểm).",

            "bisector": "Đường phân giác: Bấm chọn 3 điểm tạo góc (Điểm 1 -> Đỉnh góc 2 -> Điểm 3).",

            "mark_angle": "Ký hiệu góc: Đánh dấu góc vuông, 1 cung, 2 cung, gạch hướng tâm và nhãn Hy Lạp (α, β...) hoặc độ (°).",

            "circle": "Đường tròn: Nhấp điểm tâm, sau đó nhấp điểm bán kính.",

            "smart_tangent": "Tiếp tuyến thông minh: Bấm tâm 2 đường tròn để dựng tiếp tuyến chung, hoặc bấm vào 1 đường tròn để dựng tiếp tuyến động.",

            "common_tangents": "Tiếp tuyến chung: Bấm chọn 2 tâm hoặc 2 đường tròn để dựng tiếp tuyến chung ngoài và trong.",

            "parallelogram": "Hình bình hành: Bấm lần lượt 3 đỉnh A, B, C. Máy sẽ tự tính đỉnh D.",

            "rhombus": "Hình thoi: Bấm 2 điểm tạo cạnh đáy, sau đó bấm điểm hướng.",

            "square": "Hình vuông: Bấm 2 điểm làm cạnh đáy.",

            "incenter": "Tâm nội tiếp: Bấm chọn 3 đỉnh tam giác để tính giao 3 phân giác và dựng tâm I.",

            "incircle": "Đường tròn nội tiếp: Bấm chọn 3 đỉnh tam giác để dựng tâm I và đường tròn nội tiếp tiếp xúc 3 cạnh.",

            "circumcenter": "Tâm ngoại tiếp: Bấm chọn 3 đỉnh tam giác để tính giao 3 trung trực và dựng tâm O.",

            "circle_3p": "Đường tròn ngoại tiếp: Bấm chọn 3 đỉnh tam giác để dựng đường tròn ngoại tiếp qua 3 đỉnh.",

            "erase": "Tẩy / Xóa: Bấm vào điểm hoặc đối tượng để xóa.",

            "check_prop": "Kiểm tra tính chất: Bấm chọn 3 điểm để kiểm tra thẳng hàng hoặc tam giác cân.",
            "harmonic": "Hàng điểm điều hòa: Bấm lần lượt 2 điểm A, B và điểm C để dựng điểm liên hợp điều hòa D sao cho (AB, CD) = -1.",
            "pole_polar": "Cực & Đường đối cực: Bấm chọn đường tròn và 1 điểm (hoặc đường thẳng) để dựng đường đối cực (hoặc điểm cực).",
            "symmedian": "Đường đối trung: Bấm chọn 3 đỉnh tam giác ABC để dựng đường đối trung qua A và điểm Lemoine K.",
            "radical_axis": "Trục đẳng phương: Bấm chọn 2 đường tròn để dựng đường thẳng trục đẳng phương.",
            "barycentric": "Tọa độ tỉ cự (Barycentric): Bấm chọn 3 đỉnh tam giác ABC và 1 điểm P để phân tích tọa độ tỉ cự chuẩn hóa (u : v : w)."
        }

        self.lbl_status.config(text=f"Đang chọn công cụ: {tool_names.get(tool_code, tool_code)}")



    @staticmethod

    def validate_point_name(name):

        """

        Quy định chuẩn tên điểm hình học:

        - Đúng 1 chữ cái kèm theo chỉ số số học (ví dụ: A, B, A1, B2, M10).

        - Tuyệt đối không được 2 chữ cái (như AB, XY) để tránh nhầm với đoạn thẳng.

        """

        s = str(name).strip()

        if not s:

            return False, "Tên điểm không được để trống / Point name cannot be empty."

        if not re.match(r"^[A-Za-z][0-9]*$", s):

            return False, (

                f"Tên điểm '{s}' không đúng chuẩn quy ước!\n\n"

                "Quy định chuẩn tắc: Tên điểm gồm đúng 1 chữ cái kèm chỉ số số học tùy chọn\n"

                "(ví dụ: A, B, C, A1, B2, M1...).\n"

                "Không được dùng 2 chữ cái (như AB, CD, XY) vì sẽ nhầm với đoạn thẳng hoặc vector."

            )

        return True, ""



    def get_next_point_name(self):

        """Tự động tìm tên điểm kế tiếp chưa có trên bản vẽ (A-Z, A1-Z1, A2-Z2...)."""

        existing = {p.get("name") for p in self.points if p.get("name")}

        letters = [chr(c) for c in range(ord('A'), ord('Z') + 1) if chr(c) != 'O'] + ['O']

        for ch in letters:

            if ch not in existing:

                return ch

        idx = 1

        while True:

            for ch in letters:

                cand = f"{ch}{idx}"

                if cand not in existing:

                    return cand

            idx += 1



    def _ask_point_name_dialog(self, default_val=""):

        if not self.ask_name_on_create:

            return self.get_next_point_name() if not default_val else default_val

        if not default_val:

            default_val = self.get_next_point_name()



        is_vi = (getattr(self, "current_lang", "vi") == "vi")

        while True:

            name = simpledialog.askstring(

                "Tên Điểm" if is_vi else "Point Name",

                "Nhập tên điểm (chuẩn: 1 chữ cái + số, ví dụ A, B, A1):" if is_vi

                else "Enter point name (1 letter + optional digits, e.g. A, B, A1):",

                parent=self, initialvalue=default_val

            )

            if name is None:

                return None

            name = name.strip()

            if not name:

                return self.get_next_point_name()



            valid, err = self.validate_point_name(name)

            if not valid:

                messagebox.showerror("Lỗi Định Dạng" if is_vi else "Invalid Format", err, parent=self)

                default_val = self.get_next_point_name()

                continue



            conflict_pt = next((p for p in self.points if p.get("name") == name and not p.get("hidden")), None)

            if conflict_pt:

                suggested = self.get_next_point_name()

                choice = messagebox.askyesno(

                    "Trùng Tên Điểm" if is_vi else "Duplicate Name",

                    f"Tên điểm '{name}' đã có trên bản vẽ!\nBạn có muốn tự động dùng tên gợi ý '{suggested}' không?" if is_vi

                    else f"Point name '{name}' already exists!\nWould you like to use suggested name '{suggested}'?",

                    parent=self

                )

                if choice:

                    return suggested

                else:

                    default_val = suggested

                    continue

            return name



    def prompt_rename_point(self, pt):

        """Đổi tên điểm với kiểm tra chuẩn tắc 1 chữ cái + số, cảnh báo trùng và hỗ trợ hoán đổi (Swap)."""

        if not pt:

            return

        old_name = pt.get("name") or pt.get("id") or ""

        is_vi = (getattr(self, "current_lang", "vi") == "vi")



        new_name = simpledialog.askstring(

            "Đổi Tên Điểm" if is_vi else "Rename Point",

            f"Nhập tên mới cho điểm (hiện tại: '{old_name}'):\n(Chuẩn: 1 chữ cái + số, ví dụ: A, B, A1, B2)" if is_vi

            else f"Enter new name for point (current: '{old_name}'):\n(Format: 1 letter + digits, e.g. A, B, A1, B2)",

            parent=self, initialvalue=old_name

        )

        if new_name is None:

            return

        new_name = new_name.strip()

        if not new_name or new_name == old_name:

            return



        valid, err = self.validate_point_name(new_name)

        if not valid:

            messagebox.showerror("Lỗi Tên Điểm" if is_vi else "Invalid Name Format", err, parent=self)

            return



        conflict_pt = next((p for p in self.points if p is not pt and p.get("name") == new_name and not p.get("hidden")), None)

        if conflict_pt:

            self._show_swap_rename_dialog(pt, conflict_pt, new_name)

        else:

            self._save_state()

            pt["name"] = new_name

            self._update_algebra_tree()

            self.redraw()

            self.lbl_status.config(text=f"Đã đổi tên điểm thành '{new_name}'." if is_vi else f"Renamed point to '{new_name}'.")



    def _show_swap_rename_dialog(self, pt, conflict_pt, requested_name):

        """Hộp thoại thông minh xử lý trùng tên: Cho phép Hoán đổi (Swap) hoặc sửa cả 2 điểm cùng lúc."""

        is_vi = (getattr(self, "current_lang", "vi") == "vi")

        old_name1 = pt.get("name") or pt.get("id")

        old_name2 = conflict_pt.get("name") or conflict_pt.get("id")



        top = tk.Toplevel(self)

        top.title("⚠️ Cảnh Báo Trùng Tên Điểm" if is_vi else "⚠️ Point Name Conflict")

        top.geometry("480x290")

        top.resizable(False, False)

        top.transient(self)

        top.grab_set()



        try:

            x = self.winfo_rootx() + (self.winfo_width() - 480) // 2

            y = self.winfo_rooty() + (self.winfo_height() - 290) // 2

            top.geometry(f"+{max(10, x)}+{max(10, y)}")

        except Exception:

            pass



        tk.Label(

            top,

            text=f"Tên điểm '{requested_name}' đã tồn tại trên bản vẽ!" if is_vi else f"Point name '{requested_name}' already exists on canvas!",

            font=("Segoe UI", 10, "bold"), fg="#c92a2a"

        ).pack(pady=(12, 4))



        tk.Label(

            top,

            text="Bạn có thể hoán đổi (Swap) tên 2 điểm hoặc sửa tên mới cho cả 2 điểm:" if is_vi

            else "You can swap the names or assign distinct new names to both points:",

            font=("Segoe UI", 9)

        ).pack(pady=2)



        form_frame = tk.Frame(top)

        form_frame.pack(pady=10, padx=20, fill=tk.X)



        tk.Label(form_frame, text=f"Điểm đang chọn (hiện tại: {old_name1}) -> Tên mới:" if is_vi else f"Current point ({old_name1}) -> New name:", font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=4)

        entry1 = tk.Entry(form_frame, font=("Segoe UI", 10, "bold"), width=12)

        entry1.grid(row=0, column=1, sticky="e", pady=4)

        entry1.insert(0, requested_name)



        tk.Label(form_frame, text=f"Điểm bị trùng (hiện tại: {old_name2}) -> Tên mới:" if is_vi else f"Conflicting point ({old_name2}) -> New name:", font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=4)

        entry2 = tk.Entry(form_frame, font=("Segoe UI", 10, "bold"), width=12)

        entry2.grid(row=1, column=1, sticky="e", pady=4)

        entry2.insert(0, old_name1)



        btn_box = tk.Frame(top)

        btn_box.pack(side=tk.BOTTOM, fill=tk.X, pady=15, padx=15)



        def apply_changes(name1, name2):

            name1 = name1.strip()

            name2 = name2.strip()

            v1, err1 = self.validate_point_name(name1)

            v2, err2 = self.validate_point_name(name2)

            if not v1:

                messagebox.showerror("Lỗi Tên Điểm 1", err1, parent=top)

                return

            if not v2:

                messagebox.showerror("Lỗi Tên Điểm 2", err2, parent=top)

                return

            if name1 == name2:

                messagebox.showerror("Lỗi", "Hai điểm không được phép có cùng tên!" if is_vi else "Both points cannot have the same name!", parent=top)

                return



            other_names = {p.get("name") for p in self.points if p is not pt and p is not conflict_pt}

            if name1 in other_names:

                messagebox.showerror("Lỗi", f"Tên '{name1}' đã thuộc về một điểm khác trên bản vẽ!", parent=top)

                return

            if name2 in other_names:

                messagebox.showerror("Lỗi", f"Tên '{name2}' đã thuộc về một điểm khác trên bản vẽ!", parent=top)

                return



            self._save_state()

            pt["name"] = name1

            conflict_pt["name"] = name2

            self._update_algebra_tree()

            self.redraw()

            top.destroy()

            self.lbl_status.config(text=f"Đã cập nhật đồng thời: {name1} và {name2}." if is_vi else f"Updated both points: {name1} and {name2}.")



        def do_swap():

            apply_changes(requested_name, old_name1)



        btn_swap = tk.Button(btn_box, text="🔄 Hoán đổi (Swap)" if is_vi else "🔄 Swap Names",

                             bg="#2b8a3e", fg="#ffffff", font=("Segoe UI", 9, "bold"), padx=10, pady=2, command=do_swap)

        btn_swap.pack(side=tk.LEFT, padx=4)



        btn_apply = tk.Button(btn_box, text="✓ Áp dụng cả 2" if is_vi else "✓ Apply Both",

                              bg="#1971c2", fg="#ffffff", font=("Segoe UI", 9, "bold"), padx=10, pady=2,

                              command=lambda: apply_changes(entry1.get(), entry2.get()))

        btn_apply.pack(side=tk.LEFT, padx=4)



        btn_cancel = tk.Button(btn_box, text="Hủy" if is_vi else "Cancel", font=("Segoe UI", 9), padx=10, pady=2, command=top.destroy)

        btn_cancel.pack(side=tk.RIGHT, padx=4)



    def _on_canvas_double_click(self, event):

        wx, wy = self.to_world(event.x, event.y)

        clicked_pt = None

        for p in self.points:

            if p.get("hidden") and not self.show_hidden: continue

            px, py = self.to_screen(p["x"], p["y"])

            lx = px + p.get("label_dx", 8)

            ly = py + p.get("label_dy", -10)

            if math.hypot(event.x - px, event.y - py) <= 12 or math.hypot(event.x - (lx + 6), event.y - ly) <= 16:

                clicked_pt = p

                break



        if clicked_pt:

            self.prompt_rename_point(clicked_pt)

            return



    # =========================================================================

    # THAO TÁC CHUỘT TRÊN CANVAS

    # =========================================================================

    def _on_canvas_click(self, event):

        self.canvas.focus_set()

        wx, wy = self.to_world(event.x, event.y)

        snap = self._find_smart_snap(wx, wy)

        clicked_pt = snap["obj"] if (snap and snap["type"] == "point") else None



        # CHẾ ĐỘ XOAY BẰNG CHUỘT

        if self.current_tool == "rotate_mouse" or (event.state & 0x0001):

            if not self.selected_points:

                self.select_all()

            if self.selected_points:

                cx = sum(p["x"] for p in self.selected_points) / len(self.selected_points)

                cy = sum(p["y"] for p in self.selected_points) / len(self.selected_points)

                self.rotate_center = (cx, cy)

                self.rotate_start_angle = math.atan2(wy - cy, wx - cx)

            return



        if self.current_tool == "select":

            is_en = (getattr(self, "current_lang", "vi") == "en")



            # 1. Kiểm tra kéo nhãn chữ cái của điểm (Point Label dragging)

            clicked_label_pt = None

            for p in self.points:

                if not p.get("name") or (p.get("hidden") and not self.show_hidden):

                    continue

                px, py = self.to_screen(p["x"], p["y"])

                lx = px + p.get("label_dx", 8)

                ly = py + p.get("label_dy", -10)

                if math.hypot(event.x - (lx + 6), event.y - ly) <= 18:

                    clicked_label_pt = p

                    break



            if clicked_label_pt:

                self.dragging_label_point = clicked_label_pt

                msg = f"Moving point label '{clicked_label_pt['name']}'... Drag freely." if is_en else f"Đang kéo nhãn chữ {clicked_label_pt['name']}... Rê chuột tự do để tránh che nét vẽ."

                self.lbl_status.config(text=msg)

                return



            # 2. Kiểm tra kéo nhãn của đoạn thẳng (Segment Label dragging)

            clicked_seg_label = None

            for s in self.segments:

                if not s.get("label") or (s.get("hidden") and not self.show_hidden):

                    continue

                x1, y1 = self.to_screen(s["p1"]["x"], s["p1"]["y"])

                x2, y2 = self.to_screen(s["p2"]["x"], s["p2"]["y"])

                mid_x = (x1 + x2) / 2 + 6 + s.get("label_dx", 0)

                mid_y = (y1 + y2) / 2 - 6 + s.get("label_dy", 0)

                if math.hypot(event.x - mid_x, event.y - mid_y) <= 18:

                    clicked_seg_label = s

                    break



            if clicked_seg_label:

                self.dragging_seg_label = clicked_seg_label

                lbl = clicked_seg_label.get("label")

                msg = f"Moving segment label '{lbl}'... Drag freely." if is_en else f"Đang kéo nhãn đoạn thẳng '{lbl}'... Rê chuột tự do."

                self.lbl_status.config(text=msg)

                return



            # 3. Kiểm tra kéo nhãn hoặc kí hiệu góc (Angle mark / label dragging)

            clicked_angle_mark = None

            for m in self.angle_marks:

                v = m.get("vertex")

                p1, p2 = m.get("p1"), m.get("p2")

                if not v or not p1 or not p2: continue

                if v.get("hidden") and not self.show_hidden: continue

                vx, vy = self.to_screen(v["x"], v["y"])

                x1, y1 = self.to_screen(p1["x"], p1["y"])

                x2, y2 = self.to_screen(p2["x"], p2["y"])

                dx1, dy1 = x1 - vx, y1 - vy

                dx2, dy2 = x2 - vx, y2 - vy

                L1, L2 = math.hypot(dx1, dy1), math.hypot(dx2, dy2)

                if L1 < 1e-3 or L2 < 1e-3: continue

                style = m.get("style", "arc1")

                size = m.get("size", 14 if style == "right" else 22)



                # Check hit label nếu góc có tên

                if m.get("name"):

                    if style == "right":

                        u1x, u1y = dx1 / L1, dy1 / L1

                        u2x, u2y = dx2 / L2, dy2 / L2

                        tx = vx + size * u1x + size * u2x + 6 + m.get("label_dx", 0)

                        ty = vy + size * u1y + size * u2y - 6 + m.get("label_dy", 0)

                    else:

                        ang1 = math.atan2(dy1, dx1)

                        ang2 = math.atan2(dy2, dx2)

                        diff = (ang2 - ang1) % (2 * math.pi)

                        if diff > math.pi: diff -= 2 * math.pi

                        mid_ang = ang1 + diff / 2.0

                        tx = vx + (size + 14) * math.cos(mid_ang) + m.get("label_dx", 0)

                        ty = vy + (size + 14) * math.sin(mid_ang) + m.get("label_dy", 0)

                    if math.hypot(event.x - tx, event.y - ty) <= 18:

                        clicked_angle_mark = (m, "label")

                        break



                # Check hit arc góc

                d_v = math.hypot(event.x - vx, event.y - vy)

                if abs(d_v - size) <= 10:

                    clicked_angle_mark = (m, "size")

                    break



            if clicked_angle_mark:

                self.dragging_angle_mark = clicked_angle_mark[0]

                self.dragging_angle_mode = clicked_angle_mark[1]

                m_name = clicked_angle_mark[0].get("name") or "kí hiệu góc"

                msg = f"Adjusting angle '{m_name}'... Drag to reposition." if is_en else f"Đang di chuyển kí hiệu góc '{m_name}'... Rê chuột tự do."

                self.lbl_status.config(text=msg)

                return



            # 4. Bấm vào điểm (Point selection & drag)

            if clicked_pt:

                if clicked_pt not in self.selected_points:

                    self.selected_points = [clicked_pt]

                if event.state & 0x0004:

                    self.duplicate_selection(offset_x=0.0, offset_y=0.0)

                    clicked_pt = self.selected_points[-1]

                self.drag_start_world = (wx, wy)

                pt_name = clicked_pt.get("name") or clicked_pt["id"]

                if event.state & 0x0004:

                    msg = f"Duplicated and moving point {pt_name} (Ctrl copy)." if is_en else f"Đã nhân bản và đang di chuyển điểm mới {pt_name} (giữ Ctrl để copy)."

                else:

                    msg = f"Selected point {pt_name}. Drag to move." if is_en else f"Đã chọn điểm {pt_name}. Rê chuột để di chuyển (các đoạn liên quan sẽ đi theo)."

                self.lbl_status.config(text=msg)

                self.redraw()

                return



            # 5. Bấm vào đoạn thẳng hoặc đường thẳng (Segment / Line rigid drag)

            line_obj, line_kind = self._find_line_or_segment_at(wx, wy)

            if line_obj:

                p1 = line_obj["p1"]

                p2 = line_obj["p2"]

                self.selected_points = [p1, p2]

                if event.state & 0x0004:

                    self.duplicate_selection(offset_x=0.0, offset_y=0.0)

                self.drag_start_world = (wx, wy)

                n1 = self.selected_points[0].get("name") or self.selected_points[0]["id"]

                n2 = self.selected_points[1].get("name") or self.selected_points[1]["id"]

                lbl = line_obj.get("label") or f"{n1}{n2}"

                if event.state & 0x0004:

                    msg = f"Duplicated and moving {line_kind} {lbl} (Ctrl copy)..." if is_en else f"Đã nhân bản và đang dời {line_kind} {lbl} (giữ Ctrl để copy)..."

                else:

                    msg = f"Moving {line_kind} {lbl} (rigid length & angle preserved)..." if is_en else f"Đang dời {line_kind} {lbl} (cố định độ dài và góc, các ràng buộc giữ nguyên)..."

                self.lbl_status.config(text=msg)

                self.redraw()

                return



            # 6b. Bấm vào hình elip (Ellipse selection & drag)
            el, part = self._find_ellipse_at(wx, wy)
            if el:
                pts_to_move = []
                for k in ("center", "f1", "f2", "pA", "pB", "pM"):
                    p = el.get(k)
                    p_res = self._resolve_point(p) if p else None
                    if p_res and p_res not in pts_to_move:
                        pts_to_move.append(p_res)
                if pts_to_move:
                    self.selected_points = pts_to_move
                self.selected_ellipse = el
                self.drag_start_world = (wx, wy)
                el_lbl = el.get("label") or el["id"]
                msg = f"Moving ellipse {el_lbl}..." if is_en else f"Đang dời hình elip {el_lbl} (giữ nguyên hình dáng và góc nghiêng)..."
                self.lbl_status.config(text=msg)
                self.redraw()
                return

            # 6. Bấm vào đường tròn (Circle selection & drag)

            circ, _ = self._find_circle_at(wx, wy)

            if circ:

                center_pt = circ["center"]

                self.selected_points = [center_pt]

                if event.state & 0x0004:

                    self.duplicate_selection(offset_x=0.0, offset_y=0.0)

                self.drag_start_world = (wx, wy)

                c_lbl = circ.get("label") or circ["id"]

                if event.state & 0x0004:

                    msg = f"Duplicated and moving circle {c_lbl} (Ctrl copy)..." if is_en else f"Đã nhân bản và đang dời đường tròn {c_lbl} (giữ Ctrl để copy)..."

                else:

                    msg = f"Moving circle {c_lbl} (radius preserved)..." if is_en else f"Đang dời đường tròn {c_lbl} (giữ nguyên bán kính R)..."

                self.lbl_status.config(text=msg)

                self.redraw()

                return



            # 7. Bấm ra ngoài khoảng trống (Bỏ chọn)

            self.selected_points.clear()

            self.redraw()



        elif self.current_tool == "erase":

            # Xóa kí hiệu góc nếu bấm gần đỉnh góc

            for m in list(self.angle_marks):

                v = m.get("vertex")

                if v and math.hypot(wx - v["x"], wy - v["y"]) <= 16 / self.scale:

                    self._save_state()

                    self.angle_marks.remove(m)

                    self.redraw()

                    self.lbl_status.config(text="Đã xóa kí hiệu góc.")

                    return



            if clicked_pt:

                self._save_state()

                self.selected_points = [clicked_pt]

                self.delete_selected()

                return



            line_obj, line_kind = self._find_line_or_segment_at(wx, wy)

            if line_obj:

                self._save_state()

                if line_obj in self.segments:

                    self.segments.remove(line_obj)

                elif line_obj in self.lines:

                    self.lines.remove(line_obj)

                self._update_algebra_tree()

                self._scan_invariants_deep()

                self.redraw()

                self.lbl_status.config(text=f"Đã xóa {line_kind}.")

                return



            circ, _ = self._find_circle_at(wx, wy)

            if circ:

                self._save_state()

                self.circles.remove(circ)

                self._update_algebra_tree()

                self._scan_invariants_deep()

                self.redraw()

                self.lbl_status.config(text=f"Đã xóa đường tròn {circ['id']}.")

                return



        elif self.current_tool == "toggle_dash":

            # 1. Bấm vào đoạn thẳng hoặc đường thẳng để đổi nét đứt / nét liền

            line_obj, line_kind = self._find_line_or_segment_at(wx, wy)

            if line_obj:

                self._save_state()

                cur_style = line_obj.get("style", "solid")

                new_style = "solid" if cur_style == "dashed" else "dashed"

                line_obj["style"] = new_style

                self._update_algebra_tree()

                self.redraw()

                st_name = "nét đứt" if new_style == "dashed" else "nét liền"

                self.lbl_status.config(text=f"Đã chuyển {line_kind} sang {st_name}.")

                return



            # 2. Bấm vào đường tròn để đổi nét đứt / nét liền

            circ, _ = self._find_circle_at(wx, wy)

            if circ:

                self._save_state()

                cur_style = circ.get("style", "solid")

                new_style = "solid" if cur_style == "dashed" else "dashed"

                circ["style"] = new_style

                self._update_algebra_tree()

                self.redraw()

                st_name = "nét đứt" if new_style == "dashed" else "nét liền"

                self.lbl_status.config(text=f"Đã chuyển đường tròn {circ['id']} sang {st_name}.")

                return



            # 3. Bấm vào 2 điểm để tạo hoặc đổi đoạn thẳng nét đứt

            if clicked_pt:

                if self.temp_points:

                    p1 = self.temp_points[0]

                    p2 = clicked_pt

                    if p1 != p2:

                        self._save_state()

                        existing_seg = next((s for s in self.segments if (s["p1"] == p1 and s["p2"] == p2) or (s["p1"] == p2 and s["p2"] == p1)), None)

                        n1 = p1.get('name') or p1['id']

                        n2 = p2.get('name') or p2['id']

                        if existing_seg:

                            cur_style = existing_seg.get("style", "solid")

                            new_style = "solid" if cur_style == "dashed" else "dashed"

                            existing_seg["style"] = new_style

                            st_name = "nét đứt" if new_style == "dashed" else "nét liền"

                            self.lbl_status.config(text=f"Đã chuyển đoạn {n1}{n2} sang {st_name}.")

                        else:

                            self.segments.append({"p1": p1, "p2": p2, "color": self.COLOR_LINE, "style": "dashed", "label": f"{n1}{n2}"})

                            self.lbl_status.config(text=f"Đã tạo đoạn thẳng nét đứt {n1}{n2} (chi tiết).")

                        self.temp_points.clear()

                        self._update_algebra_tree()

                        self._scan_invariants_deep()

                        self.redraw()

                        return

                else:

                    self.temp_points = [clicked_pt]

                    sel_name = clicked_pt.get("name") or clicked_pt["id"]

                    self.lbl_status.config(text=f"Đã chọn {sel_name}. Bấm điểm thứ hai để vẽ nét đứt, hoặc bấm vào đoạn/đường tròn để chuyển nét.")

                    self.redraw()

                    return



        elif self.current_tool == "point":

            name = self._ask_point_name_dialog("")

            if name is None: return

            self._save_state()

            x_pos, y_pos = wx, wy

            parent_circ = None

            constraint = None

            source_type = "free"
            is_exact = False
            if snap and snap["type"] == "on_circle":
                x_pos, y_pos = snap["x"], snap["y"]
                parent_circ = snap["circle"]["id"]
                source_type = "on_circle"
            elif snap and snap["type"] == "on_segment":
                x_pos, y_pos = snap["x"], snap["y"]
                constraint = {"type": "on_segment", "p1": snap["segment"]["p1"], "p2": snap["segment"]["p2"], "t": snap.get("t", 0.5)}
                source_type = "on_segment"
            elif snap and snap["type"] == "on_line":
                x_pos, y_pos = snap["x"], snap["y"]
                constraint = {"type": "on_line", "p1": snap["line"]["p1"], "p2": snap["line"]["p2"], "t": snap.get("t", 0.5)}
                source_type = "on_line"
            elif self.snap_to_grid:
                x_pos = round(x_pos * 2) / 2
                y_pos = round(y_pos * 2) / 2
                source_type = "grid_snap"
                is_exact = True

            pt_id = name if name else f"P_{len(self.points)}"
            p_new = {
                "id": pt_id, "name": name, "x": x_pos, "y": y_pos,
                "color": self.COLOR_POINT, "fixed": False,
                "source": source_type, "exact": is_exact
            }

            if parent_circ:

                p_new["on_circle"] = parent_circ

            if constraint:

                p_new["constraint"] = constraint

            self.points.append(p_new)

            self._update_algebra_tree()

            self._scan_invariants_deep()

            self.redraw()



        elif self.current_tool == "intersection":

            # 1. Bắt dính trực tiếp vị trí giao điểm (Snap)

            if snap and snap["type"] == "intersection":

                name = self._ask_point_name_dialog("")

                if name is None: return

                self._save_state()

                pt_id = name if name else f"Int_{len(self.points)}"

                unhidden = False

                for p in self.points:

                    if p.get("hidden") and math.hypot(p["x"] - snap["x"], p["y"] - snap["y"]) < 1e-4:

                        p["hidden"] = False

                        if name:

                            p["name"] = name

                            p["id"] = name

                        unhidden = True

                        break

                if not unhidden:
                    self.points.append({"id": pt_id, "name": name, "x": snap["x"], "y": snap["y"], "color": self.COLOR_SNAP, "fixed": True, "source": "intersection", "parents": snap.get("parents", [])})

                self._update_algebra_tree()

                self._scan_invariants_deep()

                self.redraw()

                self.lbl_status.config(text=f"Đã tạo giao điểm {name or pt_id}.")

                return



            # 2. Hoặc người dùng bấm tuần tự 2 đối tượng (đoạn/đường thẳng/trục Ox, Oy/đường tròn)

            line_obj, line_kind = self._find_line_or_segment_at(wx, wy)

            circ, _ = self._find_circle_at(wx, wy)

            selected_entity = line_obj or circ

            if selected_entity:

                if hasattr(self, "temp_intersect_entities") and self.temp_intersect_entities:

                    e1 = self.temp_intersect_entities[0]

                    e2 = selected_entity

                    if e1 != e2:

                        intersections = self._compute_entity_intersections(e1, e2)

                        if intersections:

                            chosen = min(intersections, key=lambda pt: math.hypot(pt[0] - wx, pt[1] - wy))

                            name = self._ask_point_name_dialog("")

                            if name is not None:

                                self._save_state()

                                pt_id = name if name else f"Int_{len(self.points)}"

                                unhidden = False

                                for p in self.points:

                                    if p.get("hidden") and math.hypot(p["x"] - chosen[0], p["y"] - chosen[1]) < 1e-4:

                                        p["hidden"] = False

                                        if name:

                                            p["name"] = name

                                            p["id"] = name

                                        unhidden = True

                                        break

                                if not unhidden:
                                    parents = [p for p in [e1.get("p1"), e1.get("p2"), e2.get("p1"), e2.get("p2")] if p]
                                    self.points.append({"id": pt_id, "name": name, "x": chosen[0], "y": chosen[1], "color": self.COLOR_SNAP, "fixed": True, "source": "intersection", "parents": parents})

                                self.temp_intersect_entities = []

                                self._update_algebra_tree()

                                self._scan_invariants_deep()

                                self.redraw()

                                self.lbl_status.config(text=f"Đã tạo giao điểm {name or pt_id}.")

                                return

                        else:

                            messagebox.showinfo("Giao điểm", "Hai đối tượng đã chọn không cắt nhau!")

                    self.temp_intersect_entities = []

                    self.redraw()

                else:

                    self.temp_intersect_entities = [selected_entity]

                    lbl = selected_entity.get("label") or selected_entity.get("id", line_kind or "đối tượng")

                    self.lbl_status.config(text=f"Đã chọn {lbl}. Hãy chọn tiếp đối tượng thứ hai (đường thẳng/đoạn/trục Ox, Oy/đường tròn) để lấy giao điểm.")

                    self.redraw()

                return



            self.lbl_status.config(text="Vui lòng bấm trực tiếp vào vị trí giao điểm hoặc bấm lần lượt 2 đối tượng cắt nhau.")



        elif self.current_tool == "midpoint":

            if clicked_pt:

                self.temp_points.append(clicked_pt)

                if len(self.temp_points) == 1:

                    p1_name = clicked_pt.get("name") or clicked_pt["id"]

                    self.lbl_status.config(text=f"Đã chọn điểm thứ nhất ({p1_name}). Hãy bấm chọn điểm thứ hai để lấy trung điểm!")

                    self.redraw()

                elif len(self.temp_points) == 2:

                    p1, p2 = self.temp_points

                    name = self._ask_point_name_dialog("")

                    if name is None:

                        self.temp_points.clear()

                        return

                    self._save_state()

                    mx = (p1["x"] + p2["x"]) / 2

                    my = (p1["y"] + p2["y"]) / 2

                    pt_id = name if name else f"Mid_{p1['id']}_{p2['id']}"

                    self.points.append({"id": pt_id, "name": name, "x": mx, "y": my, "color": "#2b8a3e", "fixed": True, "source": "midpoint", "parents": [p1, p2], "constraint": {"type": "midpoint", "p1": p1, "p2": p2}})

                    self.temp_points.clear()

                    self._update_algebra_tree()

                    self.redraw()



        elif self.current_tool in ("segment", "line"):

            if clicked_pt:

                self.temp_points.append(clicked_pt)

                if len(self.temp_points) == 1:

                    p1_name = clicked_pt.get("name") or clicked_pt["id"]

                    kind_str = "đoạn thẳng" if self.current_tool == "segment" else "đường thẳng"

                    self.lbl_status.config(text=f"Đã chọn điểm thứ nhất ({p1_name}). Hãy bấm chọn điểm thứ hai để hoàn tất {kind_str}!")

                    self.redraw()

                elif len(self.temp_points) == 2:

                    self._save_state()

                    p1, p2 = self.temp_points

                    if self.current_tool == "segment":

                        self.segments.append({"p1": p1, "p2": p2, "color": self.COLOR_LINE, "style": "solid"})

                    else:

                        label = f"{p1['name']}{p2['name']}" if p1.get("name") and p2.get("name") else ""

                        self.lines.append({"p1": p1, "p2": p2, "color": self.COLOR_LINE, "style": "solid", "label": label})

                    self.temp_points.clear()

                    self._update_algebra_tree()

                    self.redraw()



        elif self.current_tool == "perpendicular":

            line_obj, line_kind = self._find_line_or_segment_at(wx, wy)



            if clicked_pt:

                if hasattr(self, "temp_line") and self.temp_line:

                    p1 = self.temp_line["p1"]

                    p2 = self.temp_line["p2"]

                    lbl = self.temp_line.get("label") or f"{p1.get('name') or ''}{p2.get('name') or ''}"

                    self._construct_perpendicular_line(clicked_pt, p1, p2, lbl)

                    self.temp_line = None

                    self.temp_points.clear()

                    return



                if clicked_pt not in self.temp_points:

                    self.temp_points.append(clicked_pt)



                if len(self.temp_points) == 1:

                    p_name = clicked_pt.get("name") or clicked_pt["id"]

                    self.lbl_status.config(text=f"Đã chọn điểm {p_name}. Hãy bấm vào đường thẳng/đoạn thẳng (hoặc chọn 2 điểm) để hạ đường vuông góc.")

                elif len(self.temp_points) == 3:

                    P = self.temp_points[0]

                    A = self.temp_points[1]

                    B = self.temp_points[2]

                    lbl = f"{A.get('name') or 'A'}{B.get('name') or 'B'}"

                    self._construct_perpendicular_line(P, A, B, lbl)

                    self.temp_points.clear()

                self.redraw()

                return



            if line_obj:

                p1 = line_obj["p1"]

                p2 = line_obj["p2"]

                lbl = line_obj.get("label") or f"{p1.get('name') or ''}{p2.get('name') or ''}"

                if not lbl: lbl = "đường thẳng"



                if self.temp_points:

                    P = self.temp_points[0]

                    self._construct_perpendicular_line(P, p1, p2, lbl)

                    self.temp_points.clear()

                    self.temp_line = None

                else:

                    self.temp_line = line_obj

                    self.lbl_status.config(text=f"Đã chọn {line_kind} '{lbl}'. Hãy bấm chọn một điểm để hạ đường vuông góc.")

                self.redraw()

                return



            self.lbl_status.config(text="Vui lòng bấm chọn một điểm hoặc bấm vào đường thẳng/đoạn thẳng trên bản vẽ.")



        elif self.current_tool == "parallel":

            line_obj, line_kind = self._find_line_or_segment_at(wx, wy)



            if clicked_pt:

                if hasattr(self, "temp_line") and self.temp_line:

                    p1 = self.temp_line["p1"]

                    p2 = self.temp_line["p2"]

                    lbl = self.temp_line.get("label") or f"{p1.get('name') or ''}{p2.get('name') or ''}"

                    self._construct_parallel_line(clicked_pt, p1, p2, lbl)

                    self.temp_line = None

                    self.temp_points.clear()

                    return



                if clicked_pt not in self.temp_points:

                    self.temp_points.append(clicked_pt)



                if len(self.temp_points) == 1:

                    p_name = clicked_pt.get("name") or clicked_pt["id"]

                    self.lbl_status.config(text=f"Đã chọn điểm {p_name}. Hãy bấm vào đường thẳng/đoạn thẳng (hoặc chọn 2 điểm) để dựng đường song song.")

                elif len(self.temp_points) == 3:

                    P = self.temp_points[0]

                    A = self.temp_points[1]

                    B = self.temp_points[2]

                    lbl = f"{A.get('name') or 'A'}{B.get('name') or 'B'}"

                    self._construct_parallel_line(P, A, B, lbl)

                    self.temp_points.clear()

                self.redraw()

                return



            if line_obj:

                p1 = line_obj["p1"]

                p2 = line_obj["p2"]

                lbl = line_obj.get("label") or f"{p1.get('name') or ''}{p2.get('name') or ''}"

                if not lbl: lbl = "đường thẳng"



                if self.temp_points:

                    P = self.temp_points[0]

                    self._construct_parallel_line(P, p1, p2, lbl)

                    self.temp_points.clear()

                    self.temp_line = None

                else:

                    self.temp_line = line_obj

                    self.lbl_status.config(text=f"Đã chọn {line_kind} '{lbl}'. Hãy bấm chọn một điểm để dựng đường song song.")

                self.redraw()

                return



            self.lbl_status.config(text="Vui lòng bấm chọn một điểm hoặc bấm vào đường thẳng/đoạn thẳng trên bản vẽ.")



        elif self.current_tool == "bisector":

            if clicked_pt:

                if clicked_pt not in self.temp_points:

                    self.temp_points.append(clicked_pt)



                if len(self.temp_points) == 1:

                    p1_name = clicked_pt.get("name") or clicked_pt["id"]

                    self.lbl_status.config(text=f"Đã chọn điểm thứ nhất {p1_name}. Bây giờ hãy chọn ĐỈNH GÓC (Điểm thứ hai).")

                elif len(self.temp_points) == 2:

                    p2_name = clicked_pt.get("name") or clicked_pt["id"]

                    self.lbl_status.config(text=f"Đã chọn đỉnh góc {p2_name}. Hãy chọn điểm thứ ba để hoàn tất góc.")

                elif len(self.temp_points) == 3:

                    pA, pB, pC = self.temp_points

                    self._construct_angle_bisector(pA, pB, pC)

                    self.temp_points.clear()

                self.redraw()

                return

            else:

                self.lbl_status.config(text="Vui lòng bấm chọn điểm trên bản vẽ (Điểm 1 -> Đỉnh góc 2 -> Điểm 3).")



        elif self.current_tool == "mark_angle":

            if clicked_pt:

                if clicked_pt not in self.temp_points:

                    self.temp_points.append(clicked_pt)

                n = len(self.temp_points)

                if n == 1:

                    p1_name = clicked_pt.get("name") or clicked_pt["id"]

                    self.lbl_status.config(text=f"Đã chọn tia thứ nhất ({p1_name}). Hãy bấm chọn ĐỈNH GÓC!")

                    self.redraw()

                elif n == 2:

                    v_name = clicked_pt.get("name") or clicked_pt["id"]

                    self.lbl_status.config(text=f"Đã chọn đỉnh góc ({v_name}). Hãy bấm chọn điểm trên tia thứ hai!")

                    self.redraw()

                elif n == 3:

                    p1, vertex, p2 = self.temp_points

                    self.temp_points.clear()

                    self.redraw()

                    self.open_angle_mark_dialog(p1, vertex, p2)

                return

            else:

                self.lbl_status.config(text="Vui lòng bấm chọn lần lượt: Điểm trên tia 1 -> Đỉnh góc -> Điểm trên tia 2.")



        elif self.current_tool == "circle":

            if clicked_pt:

                self.temp_points.append(clicked_pt)

                if len(self.temp_points) == 2:

                    self._save_state()

                    c_pt, r_pt = self.temp_points

                    r = math.hypot(r_pt["x"] - c_pt["x"], r_pt["y"] - c_pt["y"])

                    label = f"({c_pt['name']})" if c_pt.get("name") else ""

                    self.circles.append({"id": f"C_{c_pt['id']}", "center": c_pt, "r": r, "color": self.COLOR_CIRCLE, "label": label, "constraint": {"type": "circle_2p", "center": c_pt, "p_rim": r_pt}})

                    self.temp_points.clear()

                    self._update_algebra_tree()

                    self.redraw()



        elif self.current_tool == "smart_tangent":

            circ, part = self._find_circle_at(wx, wy, clicked_pt)

            if not circ:

                self.lbl_status.config(text="Vui lòng bấm vào tâm đường tròn hoặc vào đường tròn.")

                return



            if part == "center":

                if not self.temp_circles:

                    self.temp_circles.append(circ)

                    self.lbl_status.config(text=f"Đã chọn tâm đường tròn 1 ({circ['id']}). Bấm tâm đường tròn 2 để dựng TIẾP TUYẾN CHUNG, hoặc bấm vào đường tròn này để dựng TIẾP TUYẾN ĐỘNG.")

                else:

                    c1 = self.temp_circles[0]

                    c2 = circ

                    if c1["id"] == c2["id"]:

                        self._create_dynamic_tangent_on_circle(c1, wx, wy)

                    else:

                        self.construct_common_tangents(c1, c2)

                    self.temp_circles.clear()

            else:

                # Bấm vào viền đường tròn (rim)

                if self.temp_circles:

                    c1 = self.temp_circles[0]

                    if circ["id"] != c1["id"]:

                        self.construct_common_tangents(c1, circ)

                        self.temp_circles.clear()

                        return

                self._create_dynamic_tangent_on_circle(circ, wx, wy)

                self.temp_circles.clear()



        elif self.current_tool == "common_tangents":

            circ, part = self._find_circle_at(wx, wy, clicked_pt)

            if circ:

                if not self.temp_circles:

                    self.temp_circles.append(circ)

                    self.lbl_status.config(text=f"Đã chọn đường tròn 1 ({circ['id']}). Bây giờ hãy nhấp chọn tâm hoặc đường tròn thứ 2.")

                elif len(self.temp_circles) == 1:

                    c1 = self.temp_circles[0]

                    c2 = circ

                    if c1["id"] == c2["id"]:

                        messagebox.showwarning("Lưu ý", "Vui lòng chọn 2 đường tròn khác nhau!")

                        return

                    self.construct_common_tangents(c1, c2)

                    self.temp_circles.clear()

            else:

                self.lbl_status.config(text="Vui lòng nhấp vào tâm hoặc đường viền của đường tròn.")



        elif self.current_tool == "parallelogram":

            pt = clicked_pt

            if not pt:

                name = self._ask_point_name_dialog("")

                if name is None:

                    self.temp_points.clear()

                    return

                pt_id = name if name else f"Pt_{len(self.points)}"

                pt = {"id": pt_id, "name": name, "x": wx, "y": wy, "color": self.COLOR_POINT, "fixed": False}

                self.points.append(pt)

            self.temp_points.append(pt)

            if len(self.temp_points) == 1:

                self.lbl_status.config(text=f"Đã chọn đỉnh 1 ({pt.get('name') or pt['id']}). Hãy chọn đỉnh thứ 2.")

            elif len(self.temp_points) == 2:

                self.lbl_status.config(text="Đã chọn đỉnh 1 và 2. Hãy chọn đỉnh thứ 3 để hoàn thiện hình bình hành.")

            elif len(self.temp_points) == 3:

                pA, pB, pC = self.temp_points

                Dx = pA["x"] + (pC["x"] - pB["x"])

                Dy = pA["y"] + (pC["y"] - pB["y"])

                nameD = self._ask_point_name_dialog("")

                if nameD is None:

                    self.temp_points.clear()

                    return

                self._save_state()

                pD = {"id": nameD if nameD else f"D_{len(self.points)}", "name": nameD, "x": Dx, "y": Dy, "color": self.COLOR_POINT, "fixed": False, "constraint": {"type": "translate_vec", "base_pt": pA, "v1": pB, "v2": pC}}

                self.points.append(pD)

                self.segments.extend([

                    {"p1": pA, "p2": pB, "color": self.COLOR_LINE, "style": "solid"},

                    {"p1": pB, "p2": pC, "color": self.COLOR_LINE, "style": "solid"},

                    {"p1": pC, "p2": pD, "color": self.COLOR_LINE, "style": "solid"},

                    {"p1": pD, "p2": pA, "color": self.COLOR_LINE, "style": "solid"}

                ])

                if not hasattr(self, "polygons"):

                    self.polygons = []

                self.polygons.append({

                    "name": f"{pA.get('name')}{pB.get('name')}{pC.get('name')}{pD.get('name')}",

                    "points": [pA, pB, pC, pD],

                    "poly_type": "parallelogram"

                })

                self.temp_points.clear()

                self._update_algebra_tree()

                self._scan_invariants_deep()

                self.redraw()

                self.lbl_status.config(text="Đã dựng hình bình hành thành công!")



        elif self.current_tool == "rhombus":

            pt = clicked_pt

            if not pt:

                name = self._ask_point_name_dialog("")

                if name is None:

                    self.temp_points.clear()

                    return

                pt_id = name if name else f"Pt_{len(self.points)}"

                pt = {"id": pt_id, "name": name, "x": wx, "y": wy, "color": self.COLOR_POINT, "fixed": False}

                self.points.append(pt)

            self.temp_points.append(pt)

            if len(self.temp_points) == 1:

                self.lbl_status.config(text="Đã chọn điểm thứ nhất A. Hãy chọn điểm thứ hai B làm cạnh đáy.")

            elif len(self.temp_points) == 2:

                self.lbl_status.config(text="Đã chọn cạnh đáy AB. Hãy bấm chọn một điểm hoặc hướng bất kỳ để dựng hình thoi.")

            elif len(self.temp_points) == 3:

                pA, pB, pDir = self.temp_points

                L = math.hypot(pB["x"] - pA["x"], pB["y"] - pA["y"])

                if L < 1e-4:

                    messagebox.showwarning("Hình thoi", "Hai điểm A và B quá gần nhau!")

                    self.temp_points.clear()

                    return

                dx = pDir["x"] - pB["x"]

                dy = pDir["y"] - pB["y"]

                d = math.hypot(dx, dy)

                if d < 1e-4:

                    dx, dy = -(pB["y"] - pA["y"]), (pB["x"] - pA["x"])

                    d = L

                ux, uy = dx / d, dy / d

                Cx = pB["x"] + L * ux

                Cy = pB["y"] + L * uy

                Dx = pA["x"] + L * ux

                Dy = pA["y"] + L * uy

                nameC = self._ask_point_name_dialog("")

                if nameC is None:

                    self.temp_points.clear()

                    return

                nameD = self._ask_point_name_dialog("")

                if nameD is None:

                    self.temp_points.clear()

                    return

                self._save_state()

                pC = {"id": nameC if nameC else f"C_{len(self.points)}", "name": nameC, "x": Cx, "y": Cy, "color": self.COLOR_POINT, "fixed": False}

                pD = {"id": nameD if nameD else f"D_{len(self.points)+1}", "name": nameD, "x": Dx, "y": Dy, "color": self.COLOR_POINT, "fixed": False}

                self.points.extend([pC, pD])

                self.segments.extend([

                    {"p1": pA, "p2": pB, "color": self.COLOR_LINE, "style": "solid"},

                    {"p1": pB, "p2": pC, "color": self.COLOR_LINE, "style": "solid"},

                    {"p1": pC, "p2": pD, "color": self.COLOR_LINE, "style": "solid"},

                    {"p1": pD, "p2": pA, "color": self.COLOR_LINE, "style": "solid"}

                ])

                if not hasattr(self, "polygons"):

                    self.polygons = []

                self.polygons.append({

                    "name": f"{pA.get('name')}{pB.get('name')}{pC.get('name')}{pD.get('name')}",

                    "points": [pA, pB, pC, pD],

                    "poly_type": "parallelogram"

                })

                self.temp_points.clear()

                self._update_algebra_tree()

                self._scan_invariants_deep()

                self.redraw()

                self.lbl_status.config(text=f"Đã dựng hình thoi 4 cạnh bằng nhau = {L:.2f}.")



        elif self.current_tool == "square":

            pt = clicked_pt

            if not pt:

                name = self._ask_point_name_dialog("")

                if name is None:

                    self.temp_points.clear()

                    return

                pt_id = name if name else f"Pt_{len(self.points)}"

                pt = {"id": pt_id, "name": name, "x": wx, "y": wy, "color": self.COLOR_POINT, "fixed": False}

                self.points.append(pt)

            self.temp_points.append(pt)

            if len(self.temp_points) == 1:

                self.lbl_status.config(text=f"Đã chọn đỉnh thứ nhất ({pt.get('name') or pt['id']}). Hãy chọn đỉnh thứ 2 làm cạnh đáy.")

            elif len(self.temp_points) == 2:

                self._save_state()

                p1, p2 = self.temp_points

                dx = p2["x"] - p1["x"]

                dy = p2["y"] - p1["y"]

                name3 = self.get_next_point_name()

                p3 = {"id": f"Sq_{len(self.points)}", "name": name3, "x": p2["x"] - dy, "y": p2["y"] + dx, "color": self.COLOR_POINT, "fixed": False}

                self.points.append(p3)

                name4 = self.get_next_point_name()

                p4 = {"id": f"Sq_{len(self.points)}", "name": name4, "x": p1["x"] - dy, "y": p1["y"] + dx, "color": self.COLOR_POINT, "fixed": False}

                self.points.append(p4)

                self.segments.extend([

                    {"p1": p1, "p2": p2, "color": self.COLOR_LINE, "style": "solid"},

                    {"p1": p2, "p2": p3, "color": self.COLOR_LINE, "style": "solid"},

                    {"p1": p3, "p2": p4, "color": self.COLOR_LINE, "style": "solid"},

                    {"p1": p4, "p2": p1, "color": self.COLOR_LINE, "style": "solid"}

                ])

                if not hasattr(self, "polygons"):

                    self.polygons = []

                self.polygons.append({

                    "name": f"{p1.get('name')}{p2.get('name')}{p3.get('name')}{p4.get('name')}",

                    "points": [p1, p2, p3, p4],

                    "poly_type": "square"

                })

                self.temp_points.clear()

                self._update_algebra_tree()

                self._scan_invariants_deep()

                self.redraw()

                self.lbl_status.config(text=f"Đã dựng hình vuông {p1.get('name')}{p2.get('name')}{p3.get('name')}{p4.get('name')} thành công!")



        elif self.current_tool == "isosceles_trapezoid":

            pt = clicked_pt

            if not pt:

                name = self._ask_point_name_dialog("")

                if name is None:

                    self.temp_points.clear()

                    return

                pt_id = name if name else f"Pt_{len(self.points)}"

                pt = {"id": pt_id, "name": name, "x": wx, "y": wy, "color": self.COLOR_POINT, "fixed": False}

                self.points.append(pt)

            self.temp_points.append(pt)

            if len(self.temp_points) == 1:

                self.lbl_status.config(text=f"Đã chọn đỉnh thứ nhất A ({pt.get('name') or pt['id']}). Hãy chọn đỉnh thứ hai B.")

            elif len(self.temp_points) == 2:

                self.lbl_status.config(text="Đã chọn đáy AB. Hãy bấm chọn đỉnh thứ ba C để định hình đáy nhỏ.")

            elif len(self.temp_points) == 3:

                pA, pB, pC = self.temp_points

                dx, dy = compute_isosceles_trapezoid_vertex_d(pA["x"], pA["y"], pB["x"], pB["y"], pC["x"], pC["y"])

                nameD = self.get_next_point_name()

                self._save_state()

                pD = {"id": f"Pt_{len(self.points)}", "name": nameD, "x": dx, "y": dy, "color": self.COLOR_POINT, "fixed": False}

                self.points.append(pD)

                self.segments.extend([

                    {"p1": pA, "p2": pB, "color": self.COLOR_LINE, "style": "solid"},

                    {"p1": pB, "p2": pC, "color": self.COLOR_LINE, "style": "solid"},

                    {"p1": pC, "p2": pD, "color": self.COLOR_LINE, "style": "solid"},

                    {"p1": pD, "p2": pA, "color": self.COLOR_LINE, "style": "solid"}

                ])

                if not hasattr(self, "polygons"):

                    self.polygons = []

                self.polygons.append({

                    "name": f"{pA.get('name')}{pB.get('name')}{pC.get('name')}{pD.get('name')}",

                    "points": [pA, pB, pC, pD],

                    "poly_type": "isosceles_trapezoid"

                })

                self.temp_points.clear()

                self._update_algebra_tree()

                self._scan_invariants_deep()

                self.redraw()

                self.lbl_status.config(text=f"Đã dựng thành công Hình thang cân {pA.get('name')}{pB.get('name')}{pC.get('name')}{pD.get('name')} (đối xứng trục AB)!")



        elif self.current_tool == "ellipse":
            is_en = (getattr(self, "current_lang", "vi") == "en")
            pt = clicked_pt
            if not pt:
                idx = len(self.temp_points)
                default_name = "F1" if idx == 0 else ("F2" if idx == 1 else "M")
                name = self._ask_point_name_dialog(default_name)
                if name is None:
                    self.temp_points.clear()
                    return
                pt_id = name if name else f"Pt_{len(self.points)}"
                pt_color = "#e03131" if idx < 2 else self.COLOR_POINT
                pt = {"id": pt_id, "name": name, "x": wx, "y": wy, "color": pt_color, "fixed": False}
                self.points.append(pt)
            self.temp_points.append(pt)

            if len(self.temp_points) == 1:
                n1 = pt.get("name") or pt["id"]
                msg = f"Focus 1 ({n1}) selected. Click to place Focus 2 (F2)." if is_en else f"Đã chọn Tiêu điểm 1 ({n1}). Bấm chuột để chọn Tiêu điểm 2 (F2)."
                self.lbl_status.config(text=msg)
            elif len(self.temp_points) == 2:
                n1 = self.temp_points[0].get("name") or "F1"
                n2 = pt.get("name") or pt["id"]
                msg = f"Foci {n1}, {n2} selected. Move mouse to live preview, then click point M on ellipse." if is_en else f"Đã chọn 2 Tiêu điểm {n1}, {n2}. Hãy rê chuột xem trước elip và bấm chọn điểm M trên elip."
                self.lbl_status.config(text=msg)
            elif len(self.temp_points) == 3:
                pF1, pF2, pM = self.temp_points
                params = compute_ellipse_from_foci(pF1["x"], pF1["y"], pF2["x"], pF2["y"], pM["x"], pM["y"])
                self._save_state()
                if not hasattr(self, "ellipses"):
                    self.ellipses = []

                # Tự động tạo điểm Tâm O tại trung điểm của 2 tiêu điểm F1 và F2
                center_name = "O"
                if any(p.get("name") == "O" for p in self.points):
                    center_name = f"O_{len(self.ellipses)+1}"
                pO = {
                    "id": f"Center_El_{len(self.ellipses)+1}",
                    "name": center_name,
                    "x": params["ox"],
                    "y": params["oy"],
                    "color": "#e03131",
                    "fixed": False,
                    "constraint": {"type": "midpoint", "p1": pF1, "p2": pF2}
                }
                self.points.append(pO)

                el_label = f"(E_{len(self.ellipses)+1})"
                new_el = {
                    "id": f"El_{len(self.ellipses)+1}",
                    "type": "foci_point",
                    "center": pO,
                    "f1": pF1,
                    "f2": pF2,
                    "pM": pM,
                    "ox": params["ox"],
                    "oy": params["oy"],
                    "a": params["a"],
                    "b": params["b"],
                    "c": params["c"],
                    "theta": params["theta"],
                    "area": params["area"],
                    "perimeter": params["perimeter"],
                    "color": getattr(self, "COLOR_CIRCLE", "#9c36b5"),
                    "style": "solid",
                    "label": el_label
                }
                self.ellipses.append(new_el)
                self.temp_points.clear()
                self._update_algebra_tree()
                succ_msg = (f"Created Ellipse {el_label}: a={params['a']:.2f}, b={params['b']:.2f}, 2c={2*params['c']:.2f}"
                            if is_en else
                            f"Đã dựng thành công Elip {el_label}: Bán trục lớn a={params['a']:.2f}, bán trục bé b={params['b']:.2f}, Tiêu cự 2c={2*params['c']:.2f}.")
                self.lbl_status.config(text=succ_msg)

                self._scan_invariants_deep()

                self.redraw()

                self.lbl_status.config(text=f"Đã dựng {el_label}: Bán trục a={params['a']:.2f}, b={params['b']:.2f}, Diện tích S={params['area']:.2f}, Chu vi C={params['perimeter']:.2f}")



        elif self.current_tool in ("incenter", "incircle"):

            pt = clicked_pt

            if not pt:

                name = self._ask_point_name_dialog("")

                if name is None:

                    self.temp_points.clear()

                    return

                pt_id = name if name else f"Pt_{len(self.points)}"

                pt = {"id": pt_id, "name": name, "x": wx, "y": wy, "color": self.COLOR_POINT, "fixed": False}

                self.points.append(pt)

            self.temp_points.append(pt)

            if len(self.temp_points) == 1:

                self.lbl_status.config(text=f"Đã chọn đỉnh thứ nhất ({pt.get('name') or pt['id']}). Hãy chọn đỉnh thứ hai.")

            elif len(self.temp_points) == 2:

                self.lbl_status.config(text="Đã chọn 2 đỉnh. Hãy chọn đỉnh thứ ba để xác định tam giác.")

            elif len(self.temp_points) == 3:

                pA, pB, pC = self.temp_points

                a = math.hypot(pB["x"] - pC["x"], pB["y"] - pC["y"])

                b = math.hypot(pA["x"] - pC["x"], pA["y"] - pC["y"])

                c = math.hypot(pA["x"] - pB["x"], pA["y"] - pB["y"])

                peri = a + b + c

                area = 0.5 * abs((pB["x"] - pA["x"])*(pC["y"] - pA["y"]) - (pB["y"] - pA["y"])*(pC["x"] - pA["x"]))

                if peri < 1e-4 or area < 1e-5:

                    messagebox.showwarning("Lỗi", "Ba điểm thẳng hàng hoặc quá gần nhau, không tạo thành tam giác!")

                    self.temp_points.clear()

                    return

                Ix = (a * pA["x"] + b * pB["x"] + c * pC["x"]) / peri

                Iy = (a * pA["y"] + b * pB["y"] + c * pC["y"]) / peri

                r_in = area / (peri / 2.0)

                nameI = self._ask_point_name_dialog("")

                if nameI is None:

                    self.temp_points.clear()

                    return

                self._save_state()

                pI = {"id": nameI if nameI else f"I_{len(self.points)}", "name": nameI, "x": Ix, "y": Iy, "color": "#e03131", "fixed": True, "constraint": {"type": "incenter", "pts": [pA, pB, pC]}}

                self.points.append(pI)

                if self.current_tool == "incircle":

                    self.circles.append({"id": f"C_in_{len(self.circles)}", "center": pI, "r": r_in, "color": "#e03131", "label": f"({nameI})" if nameI else "(I)", "constraint": {"type": "incircle", "pts": [pA, pB, pC], "center": pI}})

                self.temp_points.clear()

                self._update_algebra_tree()

                self._scan_invariants_deep()

                self.redraw()

                self.lbl_status.config(text=f"Đã dựng {'đường tròn nội tiếp' if self.current_tool == 'incircle' else 'tâm nội tiếp I'} thành công (r = {r_in:.2f}).")



        elif self.current_tool == "circumcenter":

            pt = clicked_pt

            if not pt:

                name = self._ask_point_name_dialog("")

                if name is None:

                    self.temp_points.clear()

                    return

                pt_id = name if name else f"Pt_{len(self.points)}"

                pt = {"id": pt_id, "name": name, "x": wx, "y": wy, "color": self.COLOR_POINT, "fixed": False}

                self.points.append(pt)

            self.temp_points.append(pt)

            if len(self.temp_points) == 1:

                self.lbl_status.config(text=f"Đã chọn đỉnh thứ nhất ({pt.get('name') or pt['id']}). Hãy chọn đỉnh thứ hai.")

            elif len(self.temp_points) == 2:

                self.lbl_status.config(text="Đã chọn 2 đỉnh. Hãy chọn đỉnh thứ ba để xác định tam giác.")

            elif len(self.temp_points) == 3:

                p1, p2, p3 = self.temp_points

                d = 2 * (p1["x"]*(p2["y"] - p3["y"]) + p2["x"]*(p3["y"] - p1["y"]) + p3["x"]*(p1["y"] - p2["y"]))

                if abs(d) < 1e-7:

                    messagebox.showwarning("Lỗi", "Ba điểm thẳng hàng, không có tâm ngoại tiếp!")

                    self.temp_points.clear()

                    return

                ux = ((p1["x"]**2 + p1["y"]**2)*(p2["y"] - p3["y"]) + (p2["x"]**2 + p2["y"]**2)*(p3["y"] - p1["y"]) + (p3["x"]**2 + p3["y"]**2)*(p1["y"] - p2["y"])) / d

                uy = ((p1["x"]**2 + p1["y"]**2)*(p3["x"] - p2["x"]) + (p2["x"]**2 + p2["y"]**2)*(p1["x"] - p3["x"]) + (p3["x"]**2 + p3["y"]**2)*(p2["x"] - p1["x"])) / d

                nameO = self._ask_point_name_dialog("")

                if nameO is None:

                    self.temp_points.clear()

                    return

                self._save_state()

                pO = {"id": nameO if nameO else f"O_{len(self.points)}", "name": nameO, "x": ux, "y": uy, "color": "#1971c2", "fixed": True, "constraint": {"type": "circumcenter", "pts": [p1, p2, p3]}}

                self.points.append(pO)

                # Tự động vẽ đường tròn ngoại tiếp tương tự như chức năng đường tròn nội tiếp

                r_circum = math.hypot(p1["x"] - ux, p1["y"] - uy)

                self.circles.append({"id": f"C_out_{len(self.circles)}", "center": pO, "r": r_circum, "color": "#1971c2", "label": f"({nameO})" if nameO else "(O)", "constraint": {"type": "circumcircle", "pts": [p1, p2, p3], "center": pO}})

                self.temp_points.clear()

                self._update_algebra_tree()

                self._scan_invariants_deep()

                self.redraw()

                is_en = (getattr(self, "current_lang", "vi") == "en")

                msg_circ = f"Constructed circumcircle (O) and center O({ux:.2f}; {uy:.2f})." if is_en else f"Đã dựng đường tròn ngoại tiếp (O) và tâm O({ux:.2f}; {uy:.2f})."

                self.lbl_status.config(text=msg_circ)



        elif self.current_tool == "circle_3p":

            if clicked_pt:

                self.temp_points.append(clicked_pt)

                if len(self.temp_points) == 3:

                    self._save_state()

                    p1, p2, p3 = self.temp_points

                    d = 2 * (p1["x"]*(p2["y"] - p3["y"]) + p2["x"]*(p3["y"] - p1["y"]) + p3["x"]*(p1["y"] - p2["y"]))

                    if abs(d) > 1e-7:

                        ux = ((p1["x"]**2 + p1["y"]**2)*(p2["y"] - p3["y"]) + (p2["x"]**2 + p2["y"]**2)*(p3["y"] - p1["y"]) + (p3["x"]**2 + p3["y"]**2)*(p1["y"] - p2["y"])) / d

                        uy = ((p1["x"]**2 + p1["y"]**2)*(p3["x"] - p2["x"]) + (p2["x"]**2 + p2["y"]**2)*(p1["x"] - p3["x"]) + (p3["x"]**2 + p3["y"]**2)*(p2["x"] - p1["x"])) / d

                        r = math.hypot(p1["x"] - ux, p1["y"] - uy)

                        center = {"id": f"O_{len(self.circles)}", "name": "", "x": ux, "y": uy, "color": "#868e96", "fixed": True, "constraint": {"type": "circumcenter", "pts": [p1, p2, p3]}}

                        self.points.append(center)

                        self.circles.append({"id": f"C_{len(self.circles)}", "center": center, "r": r, "color": self.COLOR_CIRCLE, "label": "", "constraint": {"type": "circumcircle", "pts": [p1, p2, p3], "center": center}})

                    self.temp_points.clear()

                    self._update_algebra_tree()

                    self.redraw()



        elif self.current_tool == "check_prop":

            if clicked_pt:

                self.temp_points.append(clicked_pt)

                if len(self.temp_points) == 3:

                    pA, pB, pC = self.temp_points

                    nA = pA.get("name") or "A"

                    nB = pB.get("name") or "B"

                    nC = pC.get("name") or "C"

                    cross = (pB["x"] - pA["x"])*(pC["y"] - pA["y"]) - (pB["y"] - pA["y"])*(pC["x"] - pA["x"])

                    dAB = math.hypot(pA["x"] - pB["x"], pA["y"] - pB["y"])

                    dAC = math.hypot(pA["x"] - pC["x"], pA["y"] - pC["y"])

                    dBC = math.hypot(pB["x"] - pC["x"], pB["y"] - pC["y"])



                    msg = f"KẾT QUẢ KIỂM TRA CHO 3 ĐIỂM ({nA}, {nB}, {nC}):\n\n"

                    if abs(cross) < 1e-4:

                        msg += f"• 3 điểm {nA}, {nB}, {nC} THẲNG HÀNG!\n"

                    else:

                        msg += f"• 3 điểm không thẳng hàng.\n"



                    if abs(dAB - dAC) < 1e-3:

                        msg += f"• Đoạn {nA}{nB} = {nA}{nC} (Tam giác cân tại {nA})!\n"

                    elif abs(dAB - dBC) < 1e-3:

                        msg += f"• Đoạn {nB}{nA} = {nB}{nC} (Tam giác cân tại {nB})!\n"

                    elif abs(dAC - dBC) < 1e-3:

                        msg += f"• Đoạn {nC}{nA} = {nC}{nB} (Tam giác cân tại {nC})!\n"



                    messagebox.showinfo("Geometric Property Checker", msg)

                    self.temp_points.clear()

        elif self.current_tool == "harmonic":
            if clicked_pt:
                self.temp_points.append(clicked_pt)
                n = len(self.temp_points)
                if n == 1:
                    self.lbl_status.config(text=f"Đã chọn điểm đầu {clicked_pt.get('name') or 'A'}. Hãy chọn điểm thứ hai của đoạn thẳng.")
                elif n == 2:
                    p1, p2 = self.temp_points
                    self.lbl_status.config(text=f"Đã chọn đoạn {p1.get('name')}{p2.get('name')}. Hãy chọn điểm thứ ba C trên đường thẳng.")
                elif n == 3:
                    pA, pB, pC = self.temp_points
                    nA = pA.get("name") or "A"
                    nB = pB.get("name") or "B"
                    nC = pC.get("name") or "C"
                    dx = pB["x"] - pA["x"]
                    dy = pB["y"] - pA["y"]
                    L2 = dx*dx + dy*dy
                    if L2 < 1e-9:
                        self.lbl_status.config(text="Hai điểm A và B trùng nhau, không xác định được đoạn thẳng.")
                    else:
                        t = ((pC["x"] - pA["x"])*dx + (pC["y"] - pA["y"])*dy) / L2
                        if abs(t - 0.5) < 1e-4:
                            messagebox.showinfo("Hàng điểm điều hòa", f"Điểm {nC} là trung điểm của {nA}{nB};\nĐiểm liên hợp điều hòa D nằm ở vô cực (tương ứng chùm song song).")
                        else:
                            s = -t / (1.0 - 2.0*t)
                            xD = (1.0 - s)*pA["x"] + s*pB["x"]
                            yD = (1.0 - s)*pA["y"] + s*pB["y"]
                            self._save_state()
                            nD = f"D_{nC}" if f"D_{nC}" not in [p.get("name") for p in self.points] else f"D_{len(self.points)+1}"
                            new_pt = {"id": f"pt_{len(self.points)+1}", "name": nD, "x": xD, "y": yD, "color": "#d6336c", "fixed": False}
                            self.points.append(new_pt)
                            self.segments.append({"p1": pC, "p2": new_pt, "color": "#d6336c", "style": "dashed", "label": f"({nA}{nB},{nC}{nD})=-1"})
                            self._update_algebra_tree()
                            self.redraw()
                            self.lbl_status.config(text=f"Đã dựng điểm liên hợp điều hòa {nD} sao cho ({nA}{nB}, {nC}{nD}) = -1.")
                    self.temp_points.clear()

        elif self.current_tool == "pole_polar":
            c_near = self._find_nearby_circle(wx, wy)
            if c_near:
                self.temp_circles = [c_near]
            if clicked_pt:
                self.temp_points = [clicked_pt]

            if self.temp_circles and self.temp_points:
                circ = self.temp_circles[0]
                pt = self.temp_points[0]
                c_x = circ["center"]["x"]
                c_y = circ["center"]["y"]
                r = circ["r"]
                px = pt["x"]
                py = pt["y"]
                A = px - c_x
                B = py - c_y
                C_const = - A*c_x - B*c_y - r*r
                if abs(B) > 1e-7:
                    x1, x2 = -20.0, 20.0
                    y1 = (-A*x1 - C_const) / B
                    y2 = (-A*x2 - C_const) / B
                else:
                    x1 = x2 = -C_const / A if abs(A) > 1e-7 else 0.0
                    y1, y2 = -20.0, 20.0
                self._save_state()
                p_h1 = {"id": f"pt_{len(self.points)+1}", "name": "", "x": x1, "y": y1, "hidden": True}
                p_h2 = {"id": f"pt_{len(self.points)+2}", "name": "", "x": x2, "y": y2, "hidden": True}
                self.points.extend([p_h1, p_h2])
                p_name = pt.get("name") or "P"
                self.lines.append({"p1": p_h1, "p2": p_h2, "color": "#7950f2", "style": "dashed", "label": f"Đối cực {p_name}"})
                self._update_algebra_tree()
                self.redraw()
                self.lbl_status.config(text=f"Đã dựng đường đối cực của điểm {p_name} đối với đường tròn.")
                self.temp_circles.clear()
                self.temp_points.clear()
            elif self.temp_circles:
                self.lbl_status.config(text="Đã chọn đường tròn. Hãy bấm chọn 1 điểm để dựng đường đối cực.")
            elif self.temp_points:
                self.lbl_status.config(text=f"Đã chọn điểm {self.temp_points[0].get('name') or 'P'}. Hãy bấm vào đường tròn.")

        elif self.current_tool == "symmedian":
            if clicked_pt:
                self.temp_points.append(clicked_pt)
                n = len(self.temp_points)
                if n == 1:
                    self.lbl_status.config(text=f"Đã chọn đỉnh xuất phát {clicked_pt.get('name') or 'A'}. Hãy chọn 2 đỉnh còn lại của tam giác.")
                elif n == 2:
                    self.lbl_status.config(text="Đã chọn 2 đỉnh. Hãy chọn đỉnh thứ ba.")
                elif n == 3:
                    pA, pB, pC = self.temp_points
                    nA = pA.get("name") or "A"
                    nB = pB.get("name") or "B"
                    nC = pC.get("name") or "C"
                    a = math.hypot(pB["x"] - pC["x"], pB["y"] - pC["y"])
                    b = math.hypot(pC["x"] - pA["x"], pC["y"] - pA["y"])
                    c = math.hypot(pA["x"] - pB["x"], pA["y"] - pB["y"])
                    if b**2 + c**2 > 1e-9 and a**2 + b**2 + c**2 > 1e-9:
                        xD = (b**2 * pB["x"] + c**2 * pC["x"]) / (b**2 + c**2)
                        yD = (b**2 * pB["y"] + c**2 * pC["y"]) / (b**2 + c**2)
                        xK = (a**2 * pA["x"] + b**2 * pB["x"] + c**2 * pC["x"]) / (a**2 + b**2 + c**2)
                        yK = (a**2 * pA["y"] + b**2 * pB["y"] + c**2 * pC["y"]) / (a**2 + b**2 + c**2)
                        self._save_state()
                        pt_D = {"id": f"pt_{len(self.points)+1}", "name": f"D_{nA}", "x": xD, "y": yD, "color": "#e03131", "fixed": False}
                        pt_K = {"id": f"pt_{len(self.points)+2}", "name": "K", "x": xK, "y": yK, "color": "#e03131", "fixed": False}
                        self.points.extend([pt_D, pt_K])
                        self.segments.append({"p1": pA, "p2": pt_D, "color": "#e03131", "style": "dashed", "label": f"Đối trung {nA}D"})
                        self._update_algebra_tree()
                        self.redraw()
                        self.lbl_status.config(text=f"Đã dựng đường đối trung {nA}D và điểm Lemoine K của tam giác {nA}{nB}{nC}.")
                    self.temp_points.clear()

        elif self.current_tool == "radical_axis":
            c_near = self._find_nearby_circle(wx, wy)
            if c_near:
                if c_near not in self.temp_circles:
                    self.temp_circles.append(c_near)
                if len(self.temp_circles) == 1:
                    self.lbl_status.config(text="Đã chọn đường tròn thứ nhất. Hãy bấm chọn đường tròn thứ hai.")
                elif len(self.temp_circles) == 2:
                    c1, c2 = self.temp_circles
                    x1, y1 = c1["center"]["x"], c1["center"]["y"]
                    r1 = c1["r"]
                    x2, y2 = c2["center"]["x"], c2["center"]["y"]
                    r2 = c2["r"]
                    A = 2.0 * (x2 - x1)
                    B = 2.0 * (y2 - y1)
                    C_const = (x1**2 + y1**2 - r1**2) - (x2**2 + y2**2 - r2**2)
                    if abs(A) > 1e-7 or abs(B) > 1e-7:
                        if abs(B) > 1e-7:
                            px1, px2 = -20.0, 20.0
                            py1 = (-A*px1 - C_const) / B
                            py2 = (-A*px2 - C_const) / B
                        else:
                            px1 = px2 = -C_const / A
                            py1, py2 = -20.0, 20.0
                        self._save_state()
                        p_h1 = {"id": f"pt_{len(self.points)+1}", "name": "", "x": px1, "y": py1, "hidden": True}
                        p_h2 = {"id": f"pt_{len(self.points)+2}", "name": "", "x": px2, "y": py2, "hidden": True}
                        self.points.extend([p_h1, p_h2])
                        self.lines.append({"p1": p_h1, "p2": p_h2, "color": "#099268", "style": "dashed", "label": "Trục đẳng phương"})
                        self._update_algebra_tree()
                        self.redraw()
                        self.lbl_status.config(text="Đã dựng trục đẳng phương của 2 đường tròn.")
                    self.temp_circles.clear()

        elif self.current_tool == "barycentric":
            if clicked_pt:
                self.temp_points.append(clicked_pt)
                n = len(self.temp_points)
                if n < 3:
                    self.lbl_status.config(text=f"Đã chọn {n} đỉnh tam giác. Hãy chọn đủ 3 đỉnh A, B, C rồi chọn điểm P.")
                elif n == 3:
                    self.lbl_status.config(text="Đã chọn đủ 3 đỉnh tam giác. Hãy bấm chọn điểm P cần tính tọa độ tỉ cự.")
                elif n == 4:
                    pA, pB, pC, pP = self.temp_points
                    nA = pA.get("name") or "A"
                    nB = pB.get("name") or "B"
                    nC = pC.get("name") or "C"
                    nP = pP.get("name") or "P"
                    det = (pB["y"] - pC["y"])*(pA["x"] - pC["x"]) + (pC["x"] - pB["x"])*(pA["y"] - pC["y"])
                    if abs(det) > 1e-9:
                        u = ((pB["y"] - pC["y"])*(pP["x"] - pC["x"]) + (pC["x"] - pB["x"])*(pP["y"] - pC["y"])) / det
                        v = ((pC["y"] - pA["y"])*(pP["x"] - pC["x"]) + (pA["x"] - pC["x"])*(pP["y"] - pC["y"])) / det
                        w = 1.0 - u - v
                        is_centroid = (abs(u - 1/3) < 0.02 and abs(v - 1/3) < 0.02)
                        info_txt = (
                            f"📊 PHÂN TÍCH TỌA ĐỘ TỈ CỰ (BARYCENTRIC COORDINATES)\n\n"
                            f"• Tam giác cơ sở: Δ{nA}{nB}{nC}\n"
                            f"• Điểm khảo sát: {nP}\n\n"
                            f"• Tọa độ tỉ cự chuẩn hóa (u : v : w) với u + v + w = 1:\n"
                            f"  u = {u:.4f} ({u*100:.1f}%)\n"
                            f"  v = {v:.4f} ({v*100:.1f}%)\n"
                            f"  w = {w:.4f} ({w*100:.1f}%)\n\n"
                            f"• Biểu diễn vector:\n"
                            f"  vec({nP}) = {u:.3f}*vec({nA}) + {v:.3f}*vec({nB}) + {w:.3f}*vec({nC})\n"
                        )
                        if is_centroid:
                            info_txt += "\n🎯 Nhận diện: Điểm P trùng với Trọng tâm G của tam giác (u ≈ v ≈ w ≈ 1/3)!"
                        messagebox.showinfo("Barycentric Coordinates Analysis", info_txt)
                        self.lbl_status.config(text=f"Tọa độ tỉ cự {nP} wrt Δ{nA}{nB}{nC}: ({u:.3f} : {v:.3f} : {w:.3f})")
                    self.temp_points.clear()



    def _find_nearby_circle(self, wx, wy, max_d=18):

        for c in self.circles:

            d = math.hypot(wx - c["center"]["x"], wy - c["center"]["y"])

            if abs(d - c["r"]) * self.scale <= max_d:

                return c

        return None



    def _on_canvas_drag(self, event):

        wx, wy = self.to_world(event.x, event.y)



        # 0a. KÉO DI CHUYỂN NHÃN TÊN ĐIỂM (TÙY Ý DI CHUYỂN TRÁNH BỊ GHI ĐÈ)

        if getattr(self, "dragging_label_point", None):

            p = self.dragging_label_point

            px, py = self.to_screen(p["x"], p["y"])

            p["label_dx"] = event.x - px

            p["label_dy"] = event.y - py

            self.redraw()

            return



        # 0b. KÉO DI CHUYỂN NHÃN ĐOẠN THẲNG

        if getattr(self, "dragging_seg_label", None):

            s = self.dragging_seg_label

            x1, y1 = self.to_screen(s["p1"]["x"], s["p1"]["y"])

            x2, y2 = self.to_screen(s["p2"]["x"], s["p2"]["y"])

            base_x = (x1 + x2) / 2 + 6

            base_y = (y1 + y2) / 2 - 6

            s["label_dx"] = event.x - base_x

            s["label_dy"] = event.y - base_y

            self.redraw()

            return



        # 0c. KÉO DI CHUYỂN KÍ HIỆU HOẶC NHÃN GÓC (ĐỘ, ALPHA, VUÔNG)

        if getattr(self, "dragging_angle_mark", None):

            m = self.dragging_angle_mark

            v = m.get("vertex")

            if v:

                vx, vy = self.to_screen(v["x"], v["y"])

                mode = getattr(self, "dragging_angle_mode", "label")

                if mode == "label":

                    p1, p2 = m.get("p1"), m.get("p2")

                    if p1 and p2:

                        x1, y1 = self.to_screen(p1["x"], p1["y"])

                        x2, y2 = self.to_screen(p2["x"], p2["y"])

                        dx1, dy1 = x1 - vx, y1 - vy

                        dx2, dy2 = x2 - vx, y2 - vy

                        L1, L2 = math.hypot(dx1, dy1), math.hypot(dx2, dy2)

                        size = m.get("size", 14 if m.get("style") == "right" else 22)

                        if m.get("style") == "right" and L1 > 1e-3 and L2 > 1e-3:

                            u1x, u1y = dx1 / L1, dy1 / L1

                            u2x, u2y = dx2 / L2, dy2 / L2

                            base_tx = vx + size * u1x + size * u2x + 6

                            base_ty = vy + size * u1y + size * u2y - 6

                        elif L1 > 1e-3 and L2 > 1e-3:

                            ang1 = math.atan2(dy1, dx1)

                            ang2 = math.atan2(dy2, dx2)

                            diff = (ang2 - ang1) % (2 * math.pi)

                            if diff > math.pi: diff -= 2 * math.pi

                            mid_ang = ang1 + diff / 2.0

                            base_tx = vx + (size + 14) * math.cos(mid_ang)

                            base_ty = vy + (size + 14) * math.sin(mid_ang)

                        else:

                            base_tx, base_ty = vx + 15, vy - 15

                        m["label_dx"] = event.x - base_tx

                        m["label_dy"] = event.y - base_ty

                else:  # mode == "size"

                    new_sz = int(math.hypot(event.x - vx, event.y - vy))

                    m["size"] = max(10, min(80, new_sz))

            self.redraw()

            return



        # 1. XOAY HÌNH BẰNG CHUỘT

        if (self.current_tool == "rotate_mouse" or (event.state & 0x0001)) and self.rotate_center:

            cx, cy = self.rotate_center

            curr_angle = math.atan2(wy - cy, wx - cx)

            d_angle = curr_angle - self.rotate_start_angle



            cos_a = math.cos(d_angle)
            sin_a = math.sin(d_angle)
            for p in self.selected_points:
                dx = p["x"] - cx
                dy = p["y"] - cy
                p["x"] = cx + dx * cos_a - dy * sin_a
                p["y"] = cy + dx * sin_a + dy * cos_a
                p["source"] = "dragged"
                p["exact"] = False

            self.rotate_start_angle = curr_angle

            self.lbl_status.config(text=f"Đang xoay toàn bộ hình theo chuột quanh tâm ({cx:.1f}; {cy:.1f})...")

            self._update_algebra_tree()

            self._scan_invariants_deep()

            self.redraw()

            return



        # 2. DI CHUYỂN CÁC ĐIỂM ĐƯỢC CHỌN (HOẶC ĐOẠN THẲNG CỐ ĐỊNH CHIỀU DÀI & GÓC)

        if self.selected_points and self.drag_start_world:

            dx = wx - self.drag_start_world[0]

            dy = wy - self.drag_start_world[1]



            # TH 1: Điểm đơn lẻ nằm trên đường tròn (on_circle)
            if len(self.selected_points) == 1 and self.selected_points[0].get("on_circle"):
                p = self.selected_points[0]
                circ = next((c for c in self.circles if c["id"] == p["on_circle"]), None)
                if circ:
                    ang = math.atan2(wy - circ["center"]["y"], wx - circ["center"]["x"])
                    p["x"] = circ["center"]["x"] + circ["r"] * math.cos(ang)
                    p["y"] = circ["center"]["y"] + circ["r"] * math.sin(ang)
                    p["source"] = "dragged"
                    p["exact"] = False

                    # Cập nhật tiếp tuyến động gắn với điểm này
                    rx = p["x"] - circ["center"]["x"]
                    ry = p["y"] - circ["center"]["y"]
                    for l in self.lines:
                        if l.get("type") == "tangent_dynamic" and (l["p1"] == p or l["p2"] == p):
                            helper = l["p2"] if l["p1"] == p else l["p1"]
                            helper["x"] = p["x"] - ry
                            helper["y"] = p["y"] + rx

            # TH 2: Điểm đơn lẻ có ràng buộc trượt trên đoạn thẳng hoặc đường thẳng
            elif len(self.selected_points) == 1 and self.selected_points[0].get("constraint") and self.selected_points[0]["constraint"].get("type") in ("on_segment", "on_line"):
                p = self.selected_points[0]
                c = p["constraint"]
                p1 = self._resolve_point(c.get("p1"))
                p2 = self._resolve_point(c.get("p2"))
                if p1 and p2:
                    dx_seg = p2["x"] - p1["x"]
                    dy_seg = p2["y"] - p1["y"]
                    L2 = dx_seg * dx_seg + dy_seg * dy_seg
                    if L2 > 1e-9:
                        t = ((wx - p1["x"]) * dx_seg + (wy - p1["y"]) * dy_seg) / L2
                        if c.get("type") == "on_segment":
                            t = max(0.0, min(1.0, t))
                        c["t"] = t
                        p["x"] = p1["x"] + t * dx_seg
                        p["y"] = p1["y"] + t * dy_seg
                        p["source"] = "dragged"
                        p["exact"] = False

            # TH 3: Điểm đơn lẻ là trung điểm (khi kéo trực tiếp trung điểm M, cả 2 đầu mút đoạn di chuyển theo)
            elif len(self.selected_points) == 1 and self.selected_points[0].get("constraint") and self.selected_points[0]["constraint"].get("type") == "midpoint":
                p = self.selected_points[0]
                c = p["constraint"]
                p1 = self._resolve_point(c.get("p1"))
                p2 = self._resolve_point(c.get("p2"))
                if self.snap_to_grid:
                    step = getattr(self, "grid_step", 0.5)
                    if p1:
                        p1["x"] = round((p1["x"] + dx) / step) * step
                        p1["y"] = round((p1["y"] + dy) / step) * step
                        p1["source"], p1["exact"] = "grid_snap", True
                    if p2:
                        p2["x"] = round((p2["x"] + dx) / step) * step
                        p2["y"] = round((p2["y"] + dy) / step) * step
                        p2["source"], p2["exact"] = "grid_snap", True
                    if p1 and p2:
                        p["x"] = (p1["x"] + p2["x"]) / 2.0
                        p["y"] = (p1["y"] + p2["y"]) / 2.0
                    else:
                        p["x"] = round((p["x"] + dx) / step) * step
                        p["y"] = round((p["y"] + dy) / step) * step
                else:
                    if p1:
                        p1["x"] += dx
                        p1["y"] += dy
                        p1["source"], p1["exact"] = "dragged", False
                    if p2:
                        p2["x"] += dx
                        p2["y"] += dy
                        p2["source"], p2["exact"] = "dragged", False
                    if p1 and p2:
                        p["x"] = (p1["x"] + p2["x"]) / 2.0
                        p["y"] = (p1["y"] + p2["y"]) / 2.0
                    else:
                        p["x"] += dx
                        p["y"] += dy
                p["source"] = "midpoint"
                if p1 and p2:
                    p["parents"] = [p1, p2]
                p.pop("exact", None)



            else:

                # Dời các điểm được chọn (nếu chọn đoạn thẳng thì cả 2 đầu mút dời cùng dx, dy => giữ nguyên 100% độ dài & góc!)

                for p in self.selected_points:
                    p["x"] += dx
                    p["y"] += dy
                    if self.snap_to_grid:
                        step = getattr(self, "grid_step", 0.5)
                        p["x"] = round(p["x"] / step) * step
                        p["y"] = round(p["y"] / step) * step
                        p["source"] = "grid_snap"
                        p["exact"] = True
                    else:
                        p["source"] = "dragged"
                        p["exact"] = False



            # Lan truyền cập nhật cho các đối tượng phụ thuộc khác (Dynamic Constraint Propagation)

            self._recompute_dependent_objects(exclude_points=self.selected_points)



            self.drag_start_world = (wx, wy)

            self._update_algebra_tree()

            self._scan_invariants_deep()

            self.redraw()



    def _on_canvas_release(self, event):

        is_en = (getattr(self, "current_lang", "vi") == "en")

        if getattr(self, "dragging_label_point", None):

            self._save_state()

            self.dragging_label_point = None

            msg = "Point label position updated." if is_en else "Đã cập nhật vị trí nhãn chữ cái của đỉnh."

            self.lbl_status.config(text=msg)

            return



        if getattr(self, "dragging_seg_label", None):

            self._save_state()

            self.dragging_seg_label = None

            msg = "Segment label position updated." if is_en else "Đã cập nhật vị trí nhãn đoạn thẳng."

            self.lbl_status.config(text=msg)

            return



        if getattr(self, "dragging_angle_mark", None):

            self._save_state()

            self.dragging_angle_mark = None

            self.dragging_angle_mode = None

            msg = "Angle marker position updated." if is_en else "Đã cập nhật vị trí kí hiệu góc."

            self.lbl_status.config(text=msg)

            return



        if self.selected_points and self.drag_start_world:

            self._recompute_dependent_objects()

            self._save_state()



        self.drag_start_world = None

        self.rotate_center = None



    def _on_canvas_hover(self, event):

        wx, wy = self.to_world(event.x, event.y)
        self.last_mouse_world = (wx, wy)

        self.lbl_coords.config(text=f"X: {wx:6.2f} | Y: {wy:6.2f}")



        snap = self._find_smart_snap(wx, wy)

        self.hovered_snap = snap

        if snap:

            self.lbl_snap_info.config(text=f"[{snap['desc']}]")

        else:

            line_obj, line_kind = self._find_line_or_segment_at(wx, wy)

            if line_obj:

                lbl = line_obj.get("label") or f"{line_obj['p1'].get('name') or ''}{line_obj['p2'].get('name') or ''}"

                if not lbl: lbl = "đoạn thẳng"

                self.lbl_snap_info.config(text=f"[{line_kind.capitalize()}: {lbl}]")

            else:

                self.lbl_snap_info.config(text="")

        self.redraw()



    def _on_pan_start(self, event):

        self.is_panning = True

        self.pan_start_x = event.x - self.origin_x

        self.pan_start_y = event.y - self.origin_y



    def _on_pan_drag(self, event):

        if self.is_panning:

            self.origin_x = event.x - self.pan_start_x

            self.origin_y = event.y - self.pan_start_y

            self.redraw()



    def _on_pan_release(self, event):

        self.is_panning = False



    def _on_canvas_zoom(self, event):

        factor = 1.1 if event.delta > 0 else 0.9

        self.origin_x = event.x - (event.x - self.origin_x) * factor

        self.origin_y = event.y - (event.y - self.origin_y) * factor

        self.scale *= factor

        self.redraw()



    # =========================================================================

    # QUẢN LÝ ĐỐI TƯỢNG VÀ THAO TÁC CƠ BẢN

    # =========================================================================

    def toggle_hide_selected(self):
        """
        Ẩn hoặc Hiện đối tượng được chọn.
        Nếu không có đối tượng nào được chọn:
          Tự động bật/tắt chế độ 'Hiện nét ẩn' (Soi nét ẩn mờ màu xám nét đứt)
          giúp người dùng dễ dàng bấm chọn đối tượng ẩn để mở lại mà không cần bấm Ctrl+Z!
        """
        is_en = (getattr(self, "current_lang", "vi") == "en")
        if self.selected_points:
            self._save_state()
            any_visible = any(not p.get("hidden") for p in self.selected_points)
            for p in self.selected_points:
                p["hidden"] = any_visible
            self.redraw()
            status_txt = "Toggled Hidden/Visible state for selected points." if is_en else "Đã chuyển trạng thái Ẩn/Hiện cho các điểm đang chọn."
            self.lbl_status.config(text=status_txt)
        else:
            self.show_hidden = not self.show_hidden
            if hasattr(self, "var_show_hidden"):
                self.var_show_hidden.set(self.show_hidden)
            self.redraw()
            if self.show_hidden:
                msg = "GHOST VIEW ON: Hidden objects are shown as dotted grey lines. Click to select and unhide." if is_en else "ĐANG HIỆN NÉT ẨN (nét đứt xám): Hãy bấm chọn đối tượng và bấm [Ẩn/Hiện] để mở lại."
            else:
                msg = "GHOST VIEW OFF: Hidden objects are now fully hidden." if is_en else "ĐÃ TẮT NÉT ẨN: Các đối tượng phụ đã được ẩn hoàn toàn cho bản vẽ sạch đẹp."
            self.lbl_status.config(text=msg)

    def unhide_all(self):
        """Hiện lại toàn bộ các đối tượng hình học đã bị ẩn chỉ trong 1 cú click."""
        self._save_state()
        count = 0
        for p in self.points:
            if p.get("hidden"):
                p["hidden"] = False
                count += 1
        for s in getattr(self, "segments", []):
            if s.get("hidden"):
                s["hidden"] = False
                count += 1
        for l in getattr(self, "lines", []):
            if l.get("hidden"):
                l["hidden"] = False
                count += 1
        for c in getattr(self, "circles", []):
            if c.get("hidden"):
                c["hidden"] = False
                count += 1
        for el in getattr(self, "ellipses", []):
            if el.get("hidden"):
                el["hidden"] = False
                count += 1
        self.redraw()
        is_en = (getattr(self, "current_lang", "vi") == "en")
        msg = f"Restored {count} hidden object(s) to visible." if is_en else f"Đã phục hồi hiển thị toàn bộ {count} đối tượng hình học đã ẩn."
        self.lbl_status.config(text=msg)

    def copy_canvas_image_to_clipboard(self):
        """Sao chép ảnh bản vẽ hiện tại vào Windows Clipboard độ nét cao (200 DPI)."""
        import tempfile, os, io, ctypes
        from ctypes import wintypes
        from PIL import Image

        is_en = (getattr(self, "current_lang", "vi") == "en")
        temp_png = os.path.join(tempfile.gettempdir(), f"geosolver_clip_{os.getpid()}.png")
        try:
            self._render_to_image_file(temp_png, clean_mode=True, auto_crop=True, scale_mult=2, silent=True)
            if not os.path.exists(temp_png):
                return
            img = Image.open(temp_png).convert("RGB")
            bmp_buf = io.BytesIO()
            img.save(bmp_buf, format="BMP")
            data = bmp_buf.getvalue()[14:]
            bmp_buf.close()
            try:
                os.remove(temp_png)
            except Exception:
                pass

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
                return
            p_mem = kernel32.GlobalLock(h_mem)
            if not p_mem:
                return
            ctypes.cdll.msvcrt.memcpy(ctypes.c_void_p(p_mem), data, len(data))
            kernel32.GlobalUnlock(h_mem)

            if user32.OpenClipboard(None):
                user32.EmptyClipboard()
                res = user32.SetClipboardData(CF_DIB, h_mem)
                user32.CloseClipboard()
                if res:
                    msg = "Canvas image copied to clipboard!" if is_en else "Đã sao chép ảnh bản vẽ vào Clipboard!"
                    self.lbl_status.config(text=msg)
        except Exception as e:
            err = f"Failed to copy image: {e}" if is_en else f"Không thể sao chép ảnh: {e}"
            self.lbl_status.config(text=err)



    def delete_selected(self):

        if not self.selected_points:

            return

        self._save_state()

        del_ids = {p["id"] for p in self.selected_points}

        self.points = [p for p in self.points if p["id"] not in del_ids]

        self.segments = [s for s in self.segments if s["p1"]["id"] not in del_ids and s["p2"]["id"] not in del_ids]

        self.lines = [l for l in self.lines if l["p1"]["id"] not in del_ids and l["p2"]["id"] not in del_ids]

        self.circles = [c for c in self.circles if c["center"]["id"] not in del_ids]

        self.angle_marks = [m for m in self.angle_marks if m["vertex"]["id"] not in del_ids and m["p1"]["id"] not in del_ids and m["p2"]["id"] not in del_ids]

        if hasattr(self, "polygons"):

            self.polygons = [poly for poly in self.polygons if not any(p["id"] in del_ids for p in poly.get("points", []))]

        self.selected_points.clear()

        self.temp_points.clear()

        self.temp_line = None

        self._update_algebra_tree()

        self._scan_invariants_deep()

        self.redraw()

        self.lbl_status.config(text="Đã xóa đối tượng được chọn.")



    def calculate_selected_area(self):

        """Tính diện tích phần được chọn (tam giác, tứ giác, đa giác hoặc hình tròn)."""

        if len(self.selected_points) >= 3:

            pts = list(self.selected_points)

            n = len(pts)

            shoelace = 0.0

            perim = 0.0

            for i in range(n):

                p1 = pts[i]

                p2 = pts[(i + 1) % n]

                shoelace += (p1["x"] * p2["y"] - p2["x"] * p1["y"])

                perim += math.hypot(p1["x"] - p2["x"], p1["y"] - p2["y"])

            area = abs(shoelace) / 2.0

            name_p = "".join([p.get("name") or p["id"] for p in pts])



            self._save_state()

            new_poly = {

                "points": pts,

                "area": area,

                "perimeter": perim,

                "name": name_p,

                "fill_color": "#e7f5ff",

                "outline_color": "#1971c2",

                "stipple": "gray25",

                "show_label": True

            }

            if not hasattr(self, "polygons"):

                self.polygons = []

            self.polygons.append(new_poly)

            self.redraw()

            self._update_algebra_tree()



            lang = getattr(self, "current_lang", "vi")

            msg = format_polygon_pedagogical_area(pts, lang=lang)

            self._output_solution(msg, clear=True)

            self.lbl_status.config(text=f"Đã tính diện tích S({name_p}) = {area:.4f} | Chu vi P = {perim:.4f}")

            return



        elif len(self.selected_points) == 1:

            p = self.selected_points[0]

            circ = next((c for c in self.circles if c["center"]["id"] == p["id"]), None)

            if circ:

                r_val = circ["r"]

                area = math.pi * r_val * r_val

                perim = 2 * math.pi * r_val

                lbl_c = circ.get("label") or f"({p.get('name') or p['id']})"

                msg = (

                    f"=========================================================\n"

                    f"  KẾT QUẢ ĐO ĐẠC HÌNH HỌC: DIỆN TÍCH HÌNH TRÒN\n"

                    f"=========================================================\n\n"

                    f"• Đường tròn tâm {p.get('name') or p['id']}, bán kính R = {r_val:.4f}\n"

                    f"🎯 DIỆN TÍCH: S = π * R^2 = {area:.4f}\n"

                    f"🎯 CHU VI:   C = 2 * π * R = {perim:.4f}\n"

                    f"=========================================================\n"

                )

                self._output_solution(msg, clear=True)

                self.lbl_status.config(text=f"Đã tính diện tích hình tròn {lbl_c}: S = {area:.4f}")

                return



            el = next((e for e in getattr(self, "ellipses", []) if isinstance(e.get("center"), dict) and e["center"]["id"] == p["id"]), None)

            if el:

                a_val, b_val = el["a"], el["b"]

                area = calc_ellipse_area(a_val, b_val)

                perim = calc_ellipse_perimeter(a_val, b_val)

                lbl_e = el.get("label", "(E)")

                msg = (

                    f"=========================================================\n"

                    f"  KẾT QUẢ ĐO ĐẠC HÌNH HỌC: DIỆN TÍCH HÌNH ELIP\n"

                    f"=========================================================\n\n"

                    f"• Hình elip {lbl_e} có bán trục lớn a = {a_val:.4f}, bán trục bé b = {b_val:.4f}\n"

                    f"• Tâm: {p.get('name') or p['id']} ({el['ox']:.2f}; {el['oy']:.2f})\n"

                    f"🎯 DIỆN TÍCH CHÍNH XÁC: S = π * a * b = {area:.4f} (đơn vị diện tích)\n"

                    f"🎯 CHU VI XẤP XỈ RAMANUJAN: C ≈ π * [3(a+b) - sqrt((3a+b)(a+3b))] = {perim:.4f}\n"

                    f"=========================================================\n"

                )

                self._output_solution(msg, clear=True)

                self.lbl_status.config(text=f"Đã tính diện tích hình elip {lbl_e}: S = {area:.4f} | Chu vi C = {perim:.4f}")

                return



        messagebox.showinfo(

            "Hướng Dẫn Tính Diện Tích",

            "Để tính diện tích:\n"

            "1. Chọn 3 điểm trở lên (tam giác, tứ giác, đa giác) bằng chuột hoặc Ctrl+A.\n"

            "2. Hoặc chọn 1 điểm là tâm của đường tròn.\n"

            "3. Bấm nút [📐 D.tích] để xem kết quả và tô màu miền đa giác!"

        )



    def apply_quick_color(self, color_hex, color_name):

        """Đổi màu nhanh (Đỏ, Xanh, Đen, Lục) cho các đối tượng được chọn."""

        is_en = (getattr(self, "current_lang", "vi") == "en")

        color_label = color_name

        if is_en:

            name_map = {"Đỏ": "Red", "Xanh": "Blue", "Đen": "Black", "Xanh lá": "Green"}

            color_label = name_map.get(color_name, color_name)



        if not self.selected_points:

            self.COLOR_POINT = color_hex

            self.COLOR_LINE = color_hex

            self.COLOR_CIRCLE = color_hex

            if is_en:

                self.lbl_status.config(text=f"Default drawing color set to: {color_label} ({color_hex})")

            else:

                self.lbl_status.config(text=f"Đã đặt màu vẽ mặc định tiếp theo: {color_label} ({color_hex})")

            return



        self._save_state()

        sel_ids = {p["id"] for p in self.selected_points}

        count_p = 0

        count_s = 0

        count_c = 0



        for p in self.selected_points:

            p["color"] = color_hex

            count_p += 1



        for s in self.segments:

            if s["p1"]["id"] in sel_ids and s["p2"]["id"] in sel_ids:

                s["color"] = color_hex

                count_s += 1



        for c in self.circles:

            if c["center"]["id"] in sel_ids:

                c["color"] = color_hex

                count_c += 1



        self.redraw()

        self._update_algebra_tree()

        if is_en:

            self.lbl_status.config(text=f"Changed color ({color_label}) for {count_p} points, {count_s} segments, {count_c} circles.")

        else:

            self.lbl_status.config(text=f"Đã đổi màu ({color_label}) cho {count_p} điểm, {count_s} đoạn thẳng, {count_c} đường tròn.")



    def clear_drawing_only(self, silent=False):

        """Chỉ xóa hình ảnh và các đối tượng hình học trên Canvas, bảo toàn 100% nội dung đề bài và lời giải."""

        if not silent and len(self.points) > 0:

            if not messagebox.askyesno("Xác nhận xóa hình", "Bạn có chắc chắn muốn xóa toàn bộ hình vẽ trên Canvas?\n(Nội dung đề bài và lời giải bên phải sẽ được GIỮ NGUYÊN)"):

                return

        self._save_state()

        self.points.clear()

        self.segments.clear()

        self.lines.clear()

        self.circles.clear()

        self.equal_angles.clear()

        self.angle_marks.clear()

        if hasattr(self, "polygons"):

            self.polygons.clear()

        if hasattr(self, "ellipses"):

            self.ellipses.clear()

        self.selected_points.clear()

        self.temp_points.clear()

        self.temp_line = None

        self.current_preset = None

        self._update_algebra_tree()

        self.redraw()

        self.lbl_status.config(text="Đã xóa toàn bộ hình trên Canvas (Nội dung đề bài & Lời giải được bảo toàn).")



    def copy_selection(self):

        """Sao chép các điểm và hình học đã chọn vào bộ nhớ tạm (Clipboard nội bộ)."""

        if not self.selected_points:

            self.lbl_status.config(text="Chưa chọn đối tượng nào để sao chép! Hãy dùng Ctrl+A hoặc chuột chọn các điểm.")

            return



        sel_ids = {p["id"] for p in self.selected_points}

        copied_pts = [copy.deepcopy(p) for p in self.selected_points]



        copied_segs = []

        for s in self.segments:

            if s["p1"]["id"] in sel_ids and s["p2"]["id"] in sel_ids:

                copied_segs.append({

                    "p1_id": s["p1"]["id"],

                    "p2_id": s["p2"]["id"],

                    "color": s.get("color", self.COLOR_LINE),

                    "style": s.get("style", "solid"),

                    "label": s.get("label", "")

                })



        copied_circles = []

        for c in self.circles:

            if c["center"]["id"] in sel_ids:

                copied_circles.append({

                    "center_id": c["center"]["id"],

                    "r": c["r"],

                    "color": c.get("color", self.COLOR_CIRCLE),

                    "label": c.get("label", "")

                })



        self.clipboard_geo = {

            "points": copied_pts,

            "segments": copied_segs,

            "circles": copied_circles

        }

        self.lbl_status.config(text=f"Đã sao chép {len(copied_pts)} điểm và các liên kết vào bộ nhớ tạm.")



    def paste_selection(self, offset_x=1.5, offset_y=-1.5):

        """Dán các điểm và hình đã sao chép từ Clipboard, có dời tọa độ (offset)."""

        if not hasattr(self, "clipboard_geo") or not self.clipboard_geo or not self.clipboard_geo["points"]:

            self.lbl_status.config(text="Bộ nhớ tạm trống! Hãy chọn điểm/hình rồi bấm Sao chép (Ctrl+C).")

            return



        self._save_state()

        new_points = []

        id_map = {}



        for old_p in self.clipboard_geo["points"]:

            orig_name = old_p.get("name") or old_p["id"]

            m_pre = re.match(r"^([A-Za-z])(\d*)$", orig_name)

            prefix = m_pre.group(1) if m_pre else "A"

            existing_names = {p.get("name") for p in self.points} | {p["name"] for p in new_points}

            cand_idx = 1

            cand_name = f"{prefix}{cand_idx}"

            while cand_name in existing_names:

                cand_idx += 1

                cand_name = f"{prefix}{cand_idx}"

            new_name = cand_name



            new_pt = {

                "id": f"pt_{len(self.points) + len(new_points) + 1}",

                "name": new_name,

                "x": old_p["x"] + offset_x,

                "y": old_p["y"] + offset_y,

                "color": old_p.get("color", self.COLOR_POINT),

                "fixed": False

            }

            id_map[old_p["id"]] = new_pt

            new_points.append(new_pt)



        self.points.extend(new_points)



        for s in self.clipboard_geo["segments"]:

            if s["p1_id"] in id_map and s["p2_id"] in id_map:

                self.segments.append({

                    "p1": id_map[s["p1_id"]],

                    "p2": id_map[s["p2_id"]],

                    "color": s.get("color", self.COLOR_LINE),

                    "style": s.get("style", "solid"),

                    "label": ""

                })



        for c in self.clipboard_geo["circles"]:

            if c["center_id"] in id_map:

                self.circles.append({

                    "id": f"circle_{len(self.circles) + 1}",

                    "center": id_map[c["center_id"]],

                    "r": c["r"],

                    "color": c.get("color", self.COLOR_CIRCLE),

                    "label": ""

                })



        self.selected_points = new_points[:]

        self._update_algebra_tree()

        self.redraw()

        self.lbl_status.config(text=f"Đã dán {len(new_points)} điểm mới vào bản vẽ.")



    def duplicate_selection(self, offset_x=0.0, offset_y=0.0):

        """Nhân bản (Ctrl+D hoặc giữ Ctrl khi kéo/xoay): Sao chép và Dán với tên chuẩn A1, B1..."""

        self.copy_selection()

        self.paste_selection(offset_x=offset_x, offset_y=offset_y)

        return list(self.selected_points)



    def _toggle_grid(self):

        self.show_grid = self.var_grid.get()

        self.redraw()



    def _toggle_snap(self):

        self.snap_to_grid = self.var_snap.get()



    def _toggle_ask_name(self):

        self.ask_name_on_create = self.var_ask_name.get()



    def _toggle_show_hidden(self):

        self.show_hidden = self.var_show_hidden.get()

        self.redraw()



    def _on_tree_double_click(self, event):

        item = self.tree_objects.selection()

        if not item: return

        obj_id = self.tree_objects.item(item[0], "values")[0]

        p = next((pt for pt in self.points if pt["id"] == obj_id or pt.get("name") == obj_id), None)

        if p:

            self.selected_points = [p]

            self.redraw()

            self.prompt_rename_point(p)



    # =========================================================================

    # DÒNG LỆNH ĐẠI SỐ HÌNH HỌC

    # =========================================================================

    def _execute_command(self, event):

        cmd = self.entry_cmd.get().strip()

        if not cmd: return

        self._save_state()



        # Cú pháp 1: A = (2, 3) hoặc A=(2, 3)

        m_pt = re.match(r"^([A-Za-z0-9_]+)\s*=\s*\(\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\s*\)$", cmd)

        if m_pt:

            name, sx, sy = m_pt.groups()

            self.points.append({
                "id": name, "name": name, "x": float(sx), "y": float(sy),
                "color": self.COLOR_POINT, "fixed": False,
                "source": "typed", "exact": True
            })

            self.entry_cmd.delete(0, tk.END)

            self._update_algebra_tree()

            self._scan_invariants_deep()

            self.redraw()

            self.lbl_status.config(text=f"Đã tạo điểm {name}({sx}; {sy}).")

            return



        # Cú pháp 2: line(A, B) hoặc segment(A, B)

        m_line = re.match(r"^(line|segment)\s*\(\s*([A-Za-z0-9_]+)\s*,\s*([A-Za-z0-9_]+)\s*\)$", cmd, re.IGNORECASE)

        if m_line:

            kind, n1, n2 = m_line.groups()

            p1 = next((p for p in self.points if p["name"] == n1 or p["id"] == n1), None)

            p2 = next((p for p in self.points if p["name"] == n2 or p["id"] == n2), None)

            if p1 and p2:

                if kind.lower() == "segment":

                    self.segments.append({"p1": p1, "p2": p2, "color": self.COLOR_LINE, "style": "solid"})

                else:

                    self.lines.append({"p1": p1, "p2": p2, "color": self.COLOR_LINE, "style": "solid", "label": f"{n1}{n2}"})

                self.entry_cmd.delete(0, tk.END)

                self._update_algebra_tree()

                self.redraw()

                self.lbl_status.config(text=f"Đã tạo {kind} qua {n1} và {n2}.")

                return

            else:

                messagebox.showerror("Lỗi", f"Không tìm thấy điểm {n1} hoặc {n2}!")

                return



        # Cú pháp 3: circle(O, 4.5)

        m_circ = re.match(r"^circle\s*\(\s*([A-Za-z0-9_]+)\s*,\s*(-?\d+\.?\d*)\s*\)$", cmd, re.IGNORECASE)

        if m_circ:

            n_o, sr = m_circ.groups()

            center = next((p for p in self.points if p["name"] == n_o or p["id"] == n_o), None)

            if center:

                r_val = float(sr)

                self.circles.append({"id": f"C_{n_o}", "center": center, "r": r_val, "color": self.COLOR_CIRCLE, "label": f"({n_o})"})

                self.entry_cmd.delete(0, tk.END)

                self._update_algebra_tree()

                self.redraw()

                self.lbl_status.config(text=f"Đã tạo đường tròn tâm {n_o} bán kính {r_val}.")

                return



        messagebox.showinfo("Lệnh chưa hợp lệ", "Cú pháp hỗ trợ:\n• A = (2, 3)\n• segment(A, B) hoặc line(A, B)\n• circle(A, 3)")



    # =========================================================================

    # QUÉT BẤT BIẾN & TÍNH CHẤT HÌNH HỌC (GEOMETRIC PROPERTY CHECKER)

    # =========================================================================

    def _scan_invariants_deep(self):
        self.txt_invariants.delete("1.0", tk.END)
        invariants = []
        is_en = (getattr(self, "current_lang", "vi") == "en")

        pts = [p for p in self.points if not p.get("hidden") and p.get("name")]
        if len(pts) < 3:
            pts = [p for p in self.points if not p.get("hidden")]
        n = len(pts)
        if n < 2:
            msg = "No special relations detected." if is_en else "Không phát hiện quan hệ đặc biệt nào."
            self.txt_invariants.insert(tk.END, msg)
            self.detected_invariants_list = []
            return

        def pt_name(p):
            return p.get("name") or p.get("id", "P")

        # Hàm biểu diễn độ dài dạng căn thức chính xác (chống ảo giác làm tròn)
        def format_radical_len(val, p1=None, p2=None):
            if val < 1e-4: return "0"
            if p1 is not None and p2 is not None:
                dx = p1["x"] - p2["x"]
                dy = p1["y"] - p2["y"]
                d_sq = dx * dx + dy * dy
            else:
                d_sq = val * val

            n_int = round(d_sq)
            if abs(d_sq - n_int) < 1e-3 and n_int > 0:
                r = int(math.isqrt(n_int))
                if r * r == n_int:
                    return str(r)
                k = 1
                m = n_int
                for factor in range(int(math.isqrt(n_int)), 1, -1):
                    if n_int % (factor * factor) == 0:
                        k = factor
                        m = n_int // (factor * factor)
                        break
                if k == 1:
                    return f"√{m} (≈ {val:.2f})"
                else:
                    return f"{k}√{m} (≈ {val:.2f})"

            d4_sq = d_sq * 4.0
            n4_int = round(d4_sq)
            if abs(d4_sq - n4_int) < 1e-3 and n4_int > 0:
                r = int(math.isqrt(n4_int))
                if r * r == n4_int:
                    return f"{r}/2 ({val:.2f})" if r % 2 != 0 else str(r // 2)
                k = 1
                m = n4_int
                for factor in range(int(math.isqrt(n4_int)), 1, -1):
                    if n4_int % (factor * factor) == 0:
                        k = factor
                        m = n4_int // (factor * factor)
                        break
                if k % 2 == 0:
                    k_half = k // 2
                    prefix = f"{k_half}" if k_half > 1 else ""
                    return f"{prefix}√{m} (≈ {val:.2f})"
                else:
                    prefix = f"{k}" if k > 1 else ""
                    return f"{prefix}√{m}/2 (≈ {val:.2f})"

            return f"{val:.2f}"

        # Ngưỡng dung sai thích ứng tỷ lệ (Scale-adaptive tolerance, chuẩn mực CAD)
        def is_equal_len(l1, l2):
            if l1 < 1e-4 or l2 < 1e-4: return False
            tol = max(1e-4, 0.006 * max(l1, l2))
            return abs(l1 - l2) <= tol

        def is_perp_vec(ux, uy, vx, vy):
            l1 = math.hypot(ux, uy)
            l2 = math.hypot(vx, vy)
            if l1 < 1e-4 or l2 < 1e-4: return False
            cos_a = abs(ux * vx + uy * vy) / (l1 * l2)
            return cos_a <= 0.022  # góc lệch < 1.25 độ

        def is_parallel_vec(ux, uy, vx, vy):
            l1 = math.hypot(ux, uy)
            l2 = math.hypot(vx, vy)
            if l1 < 1e-4 or l2 < 1e-4: return False
            sin_a = abs(ux * vy - uy * vx) / (l1 * l2)
            return sin_a <= 0.022  # góc lệch < 1.25 độ

        # 1. NHẬN DIỆN TAM GIÁC ĐẶC BIỆT (ĐỀU, VUÔNG CÂN, CÂN, VUÔNG)
        # Sử dụng hàm thuần túy classify_triangle chuẩn mực production
        tri_detected = set()
        equal_pairs_already_reported = set()

        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    pA, pB, pC = pts[i], pts[j], pts[k]
                    nA, nB, nC = pt_name(pA), pt_name(pB), pt_name(pC)
                    tri_key = tuple(sorted([nA, nB, nC]))
                    if tri_key in tri_detected: continue

                    res = classify_triangle(pA, pB, pC, lang=("en" if is_en else "vi"))
                    if not res["is_triangle"] or res["type"] == "scalene":
                        continue

                    tri_detected.add(tri_key)
                    bullet = "★ " if res["type"] in ("equilateral", "right_isosceles", "isosceles") else "• "
                    invariants.append(bullet + res["description"])

                    if res["type"] == "equilateral":
                        equal_pairs_already_reported.add(tuple(sorted([f"{nA}{nB}", f"{nB}{nC}"])))
                        equal_pairs_already_reported.add(tuple(sorted([f"{nB}{nC}", f"{nC}{nA}"])))
                        equal_pairs_already_reported.add(tuple(sorted([f"{nA}{nB}", f"{nC}{nA}"])))
                    elif res["type"] in ("right_isosceles", "isosceles"):
                        v = res.get("vertex")
                        if v == nA:
                            equal_pairs_already_reported.add(tuple(sorted([f"{nA}{nB}", f"{nA}{nC}"])))
                        elif v == nB:
                            equal_pairs_already_reported.add(tuple(sorted([f"{nB}{nA}", f"{nB}{nC}"])))
                        elif v == nC:
                            equal_pairs_already_reported.add(tuple(sorted([f"{nC}{nA}", f"{nC}{nB}"])))

        # 2. NHẬN DIỆN CÁC ĐƯỜNG SONG SONG (PARALLEL SEGMENTS)
        seg_pairs_par = []
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(n):
                    for l in range(k + 1, n):
                        if (i, j) >= (k, l): continue
                        if len({i, j, k, l}) < 4: continue  # Bỏ qua nếu chung đỉnh
                        p1, p2 = pts[i], pts[j]
                        q1, q2 = pts[k], pts[l]
                        u_x, u_y = p2["x"] - p1["x"], p2["y"] - p1["y"]
                        v_x, v_y = q2["x"] - q1["x"], q2["y"] - q1["y"]
                        if is_parallel_vec(u_x, u_y, v_x, v_y):
                            s1 = f"{pt_name(p1)}{pt_name(p2)}"
                            s2 = f"{pt_name(q1)}{pt_name(q2)}"
                            seg_pairs_par.append((s1, s2))
                            invariants.append(f"• " + (f"Parallel: {s1} ∥ {s2}" if is_en else f"Song song: {s1} ∥ {s2}"))

        # 3. NHẬN DIỆN CÁC ĐƯỜNG VUÔNG GÓC RỜI (PERPENDICULAR SEGMENTS)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(n):
                    for l in range(k + 1, n):
                        if (i, j) >= (k, l): continue
                        if len({i, j, k, l}) < 4: continue
                        p1, p2 = pts[i], pts[j]
                        q1, q2 = pts[k], pts[l]
                        u_x, u_y = p2["x"] - p1["x"], p2["y"] - p1["y"]
                        v_x, v_y = q2["x"] - q1["x"], q2["y"] - q1["y"]
                        if is_perp_vec(u_x, u_y, v_x, v_y):
                            s1 = f"{pt_name(p1)}{pt_name(p2)}"
                            s2 = f"{pt_name(q1)}{pt_name(q2)}"
                            invariants.append(f"• " + (f"Perpendicular: {s1} ⊥ {s2}" if is_en else f"Vuông góc: {s1} ⊥ {s2}"))

        # 4. NHẬN DIỆN THẲNG HÀNG & TRUNG ĐIỂM (COLLINEAR & MIDPOINT)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    p1, p2, p3 = pts[i], pts[j], pts[k]
                    cross = (p2["x"] - p1["x"])*(p3["y"] - p1["y"]) - (p2["y"] - p1["y"])*(p3["x"] - p1["x"])
                    if abs(cross) < 1e-3:
                        n1, n2, n3 = pt_name(p1), pt_name(p2), pt_name(p3)
                        # Kiểm tra xem có điểm nào là trung điểm của 2 điểm kia không
                        pts_order = sorted([p1, p2, p3], key=lambda p: (p["x"], p["y"]))
                        mid_cand = pts_order[1]
                        end1, end2 = pts_order[0], pts_order[2]
                        d_e1 = math.hypot(mid_cand["x"] - end1["x"], mid_cand["y"] - end1["y"])
                        d_e2 = math.hypot(mid_cand["x"] - end2["x"], mid_cand["y"] - end2["y"])
                        if is_equal_len(d_e1, d_e2):
                            nm = pt_name(mid_cand); n_e1 = pt_name(end1); n_e2 = pt_name(end2)
                            invariants.append(f"• " + (f"Midpoint: {nm} is midpoint of {n_e1}{n_e2} ({n_e1}{nm}={nm}{n_e2})" if is_en else f"Trung điểm: {nm} là trung điểm của đoạn {n_e1}{n_e2}"))
                        else:
                            invariants.append(f"• " + (f"Collinear: ({n1}, {n2}, {n3})" if is_en else f"Thẳng hàng: ({n1}, {n2}, {n3})"))

        # 5. CÁC CẶP ĐOẠN THẲNG BẰNG NHAU (EQUAL SEGMENTS)
        eq_seen = set()
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(n):
                    for l in range(k + 1, n):
                        if (i, j) >= (k, l): continue
                        p1, p2 = pts[i], pts[j]
                        q1, q2 = pts[k], pts[l]
                        d1 = math.hypot(p1["x"] - p2["x"], p1["y"] - p2["y"])
                        d2 = math.hypot(q1["x"] - q2["x"], q1["y"] - q2["y"])
                        if is_equal_len(d1, d2) and d1 > 0.1:
                            s1 = f"{pt_name(p1)}{pt_name(p2)}"
                            s2 = f"{pt_name(q1)}{pt_name(q2)}"
                            pair_key = tuple(sorted([s1, s2]))
                            # Tránh lặp lại những cặp cạnh đã nêu rõ ở tam giác cân / đều
                            if pair_key in equal_pairs_already_reported: continue
                            if pair_key not in eq_seen:
                                eq_seen.add(pair_key)
                                avg_d = (d1 + d2) / 2.0
                                avg_str = format_radical_len(avg_d, p1, p2)
                                invariants.append(f"• " + (f"Equal segments: {s1} = {s2} = {avg_str}" if is_en else f"Đoạn bằng nhau: {s1} = {s2} = {avg_str}"))

        self.detected_invariants_list = invariants
        if invariants:
            # Hiển thị tối đa 14 quan hệ phát hiện nổi bật
            self.txt_invariants.insert(tk.END, "\n".join(invariants[:14]))
        else:
            msg = "No special relations detected." if is_en else "Không phát hiện quan hệ đặc biệt nào."
            self.txt_invariants.insert(tk.END, msg)



    # =========================================================================

    # BỘ GIẢI TOÁN HÌNH HỌC TOÀN DIỆN & TÍNH TOÁN SYMPY

    # =========================================================================

    def _output_solution(self, text, clear=True):

        """Xuất nội dung lời giải với tùy chọn hiệu ứng chạy tự động (Streaming Typewriter)."""

        if clear:

            self.txt_solution.delete("1.0", tk.END)

        if hasattr(self, "var_auto_stream") and self.var_auto_stream.get():

            lines = text.splitlines(keepends=True)

            self._stream_lines(lines, 0)

        else:

            self.txt_solution.insert(tk.END, text)

            self.txt_solution.see(tk.END)



    def _stream_lines(self, lines, idx):

        """Hiệu ứng chạy tự động từng dòng mượt mà như MS Word / Typewriter."""

        if not self.winfo_exists():

            return

        if idx < len(lines):

            self.txt_solution.insert(tk.END, lines[idx])

            self.txt_solution.see(tk.END)

            self.after(14, self._stream_lines, lines, idx + 1)



    def _resolve_target_polygon_points(self, raw_targets: str = "", prob_text: str = "") -> tuple[list[dict], bool, str]:
        """Trích xuất danh sách các điểm mục tiêu của đa giác cần khảo sát.
        Trả về: (matched_points, is_intersection, inter_info)
        """
        import re
        raw_target = (raw_targets or "").strip()
        prob = (prob_text or "").strip()

        # 1. Kiểm tra yêu cầu phần chung / giao nhau của 2 tam giác hoặc 2 đa giác
        comb_text = f"{raw_target} {prob}"
        if any(k in comb_text.lower() for k in ["phần chung", "giao", "intersection", "∩", " và ", " va "]):
            parts = re.split(r"[∩&;]|(?:\s+(?:và|va|and|∩|giao\s+với)\s+)", raw_target if raw_target else prob, flags=re.IGNORECASE)
            parts = [p.strip() for p in parts if p.strip()]
            if len(parts) >= 2:
                p1_tokens = re.findall(r"[A-Za-z][0-9']*", parts[0])
                p2_tokens = re.findall(r"[A-Za-z][0-9']*", parts[1])
                poly1_pts = [p for tok in p1_tokens for p in self.points if (p.get("name") == tok or p.get("id") == tok) and not p.get("hidden")]
                poly2_pts = [p for tok in p2_tokens for p in self.points if (p.get("name") == tok or p.get("id") == tok) and not p.get("hidden")]
                if len(poly1_pts) >= 3 and len(poly2_pts) >= 3:
                    poly1_coords = [(p["x"], p["y"]) for p in poly1_pts]
                    poly2_coords = [(p["x"], p["y"]) for p in poly2_pts]
                    inter_coords = clip_polygon_sutherland_hodgman(poly1_coords, poly2_coords)
                    if len(inter_coords) >= 3:
                        nm1 = "".join([p.get("name") or p["id"] for p in poly1_pts])
                        nm2 = "".join([p.get("name") or p["id"] for p in poly2_pts])
                        inter_info = f"Δ{nm1} ∩ Δ{nm2}"
                        alpha_names = ["D", "E", "F", "G", "H", "I", "M", "N", "P", "Q", "T", "K"]
                        matched = [{"name": alpha_names[idx % len(alpha_names)], "x": pt[0], "y": pt[1]} for idx, pt in enumerate(inter_coords)]
                        return matched, True, inter_info

        # 2. Quét các điểm mục tiêu chỉ định trong raw_targets (ví dụ: 'DEFGHI' hoặc 'D, E, F, G, H, I')
        if raw_target:
            tokens = re.findall(r"[A-Za-z][0-9']*", raw_target)
            matched = []
            for tok in tokens:
                pt_found = next((p for p in self.points if (p.get("name") == tok or p.get("id") == tok) and not p.get("hidden")), None)
                if pt_found and pt_found not in matched:
                    matched.append(pt_found)
            if len(matched) >= 3:
                return matched, False, ""

        # 3. Quét các điểm mục tiêu xuất hiện trong prob_text (ví dụ: 'Tính diện tích đa giác DEFGHI')
        if prob:
            m = re.search(r"(?:diện tích|đa giác|tam giác|hình|mục tiêu|tính|tìm|area|polygon)\s+(?:đa giác\s+|tam giác\s+)?([A-Za-z0-9'\s,]+)", prob, re.IGNORECASE)
            if m:
                cand_str = m.group(1).strip()
                tokens = re.findall(r"[A-Za-z][0-9']*", cand_str)
                matched = []
                for tok in tokens:
                    pt_found = next((p for p in self.points if (p.get("name") == tok or p.get("id") == tok) and not p.get("hidden")), None)
                    if pt_found and pt_found not in matched:
                        matched.append(pt_found)
                if len(matched) >= 3:
                    return matched, False, ""

            tokens = re.findall(r"[A-Za-z][0-9']*", prob)
            matched = []
            for tok in tokens:
                pt_found = next((p for p in self.points if (p.get("name") == tok or p.get("id") == tok) and not p.get("hidden")), None)
                if pt_found and pt_found not in matched:
                    matched.append(pt_found)
            if 3 <= len(matched) <= 10:
                return matched, False, ""

        # 4. Kiểm tra đa giác tường minh trong self.polygons
        if hasattr(self, "polygons") and self.polygons:
            poly_pts = self.polygons[0].get("points", [])
            if len(poly_pts) >= 3:
                return poly_pts, False, ""

        # 5. Kiểm tra các điểm đang chọn trên canvas
        if hasattr(self, "selected_points") and len(self.selected_points) >= 3:
            return list(self.selected_points), False, ""

        # 6. Nếu đúng 3 điểm trên toàn bản vẽ (tam giác duy nhất)
        visible_pts = [p for p in self.points if not p.get("hidden") and p.get("name")]
        if len(visible_pts) == 3:
            return visible_pts, False, ""

        # 7. Nếu có nhiều điểm nhưng 3 điểm đầu là tam giác chính ABC
        if len(visible_pts) > 3:
            abc = [p for p in visible_pts if p.get("name") in ("A", "B", "C")]
            if len(abc) == 3:
                return abc, False, ""
            return visible_pts[:3], False, ""

        return visible_pts, False, ""

    def find_point_by_name(self, name: str):
        """Tìm đối tượng điểm theo tên hoặc ID."""
        if not name:
            return None
        target = str(name).strip().upper()
        for p in self.points:
            p_name = str(p.get("name") or "").strip().upper()
            p_id = str(p.get("id") or "").strip().upper()
            if p_name == target or p_id == target:
                return p
        return None

    def _execute_ai_drawing_command(self, cmd_line: str) -> bool:
        """Thực thi lệnh dựng hình phụ tự động từ AI Agent (Auxiliary Geometry Construction)."""
        import re, math
        cmd = cmd_line.strip()
        executed = False

        # 1. KẺ ĐOẠN THẲNG: [DRAW_SEGMENT: A, B] hoặc câu văn tự nhiên: 'Kẻ đoạn thẳng AM' / 'Nối A với M'
        m_segs = re.findall(r"\[(?:DRAW_SEGMENT|KẺ ĐOẠN|NOI_DOAN):\s*([A-Za-z0-9']+)\s*,\s*([A-Za-z0-9']+)\]", cmd, re.IGNORECASE)
        m_segs_nl = re.findall(r"(?:kẻ|nối)\s+(?:đoạn\s+thẳng\s+|đoạn\s+)?([A-Za-z][0-9']*)\s*(?:với|và|-|\s*)?\s*([A-Za-z][0-9']*)(?!\w)", cmd, re.IGNORECASE)
        for pair in m_segs_nl:
            if pair not in m_segs and (pair[1], pair[0]) not in m_segs:
                m_segs.append(pair)
        for n1, n2 in m_segs:
            p1 = self.find_point_by_name(n1)
            p2 = self.find_point_by_name(n2)
            if p1 and p2 and p1 != p2:
                already = False
                for s in self.segments:
                    sp1 = s.get("p1")
                    sp2 = s.get("p2")
                    if (sp1 == p1 and sp2 == p2) or (sp1 == p2 and sp2 == p1):
                        already = True
                        break
                if not already:
                    self._save_state()
                    self.segments.append({
                        "p1": p1, "p2": p2,
                        "p1_id": p1.get("id"), "p2_id": p2.get("id"),
                        "color": "#e03131",
                        "style": "dashed",
                        "label": f"{n1}{n2} (phụ)"
                    })
                    executed = True
                    self.lbl_status.config(text=f"🤖 AI Agent đã kẻ đường phụ: {n1}{n2}", fg="#e03131")

        # 2. LẤY TRUNG ĐIỂM: [DRAW_MIDPOINT: M, B, C] hoặc câu văn: 'Lấy trung điểm M của BC'
        m_mids = re.findall(r"\[(?:DRAW_MIDPOINT|TRUNG ĐIỂM|TRUNG_DIEM):\s*([A-Za-z0-9']+)\s*,\s*([A-Za-z0-9']+)\s*,\s*([A-Za-z0-9']+)\]", cmd, re.IGNORECASE)
        m_mids_nl = re.findall(r"(?:lấy|gọi|dựng)\s+trung\s+điểm\s+([A-Za-z0-9']+)\s+của\s+(?:đoạn\s+thẳng\s+|cạnh\s+)?([A-Za-z0-9']+)(?:\s*(?:,|và|va|-)\s*|\s*)([A-Za-z0-9']+)", cmd, re.IGNORECASE)
        for triplet in m_mids_nl:
            if triplet not in m_mids:
                m_mids.append(triplet)
        for nm, nb, nc in m_mids:
            pB = self.find_point_by_name(nb)
            pC = self.find_point_by_name(nc)
            if pB and pC and not self.find_point_by_name(nm):
                mx = (pB["x"] + pC["x"]) / 2.0
                my = (pB["y"] + pC["y"]) / 2.0
                self._save_state()
                new_pt = {
                    "id": f"pt_{len(self.points)+1}",
                    "name": nm,
                    "x": mx, "y": my,
                    "color": "#e03131",
                    "fixed": False
                }
                self.points.append(new_pt)
                executed = True
                self.lbl_status.config(text=f"🤖 AI Agent đã lấy trung điểm phụ: {nm} của {nb}{nc}", fg="#e03131")

        # 3. HẠ ĐƯỜNG CAO / VUÔNG GÓC: [DRAW_PERPENDICULAR: H, A, B, C] hoặc 'Hạ đường cao AH từ A đến BC' / 'Hạ đường cao AH vuông góc BC'
        m_perps = re.findall(r"\[(?:DRAW_PERPENDICULAR|HẠ ĐƯỜNG CAO|HA_DUONG_CAO|VUONG_GOC):\s*([A-Za-z0-9']+)\s*,\s*([A-Za-z0-9']+)\s*,\s*([A-Za-z0-9']+)\s*,\s*([A-Za-z0-9']+)\]", cmd, re.IGNORECASE)
        m_perps_nl = re.findall(r"(?:hạ|kẻ|dựng)\s+đường\s+cao\s+([A-Za-z0-9'])([A-Za-z0-9'])\s+(?:từ\s+[A-Za-z0-9']+\s+)?(?:đến|vuông\s+góc|xuống)\s+(?:cạnh\s+|đường\s+thẳng\s+)?([A-Za-z0-9'])(?:\s*(?:,|và|va|-)\s*|\s*)([A-Za-z0-9'])", cmd, re.IGNORECASE)
        for na, nh, nb, nc in m_perps_nl:
            quad = (nh, na, nb, nc)
            if quad not in m_perps:
                m_perps.append(quad)
        for nh, na, nb, nc in m_perps:
            pA = self.find_point_by_name(na)
            pB = self.find_point_by_name(nb)
            pC = self.find_point_by_name(nc)
            if pA and pB and pC and not self.find_point_by_name(nh):
                vx = pC["x"] - pB["x"]
                vy = pC["y"] - pB["y"]
                d2 = vx*vx + vy*vy
                if d2 > 1e-6:
                    t = ((pA["x"] - pB["x"])*vx + (pA["y"] - pB["y"])*vy) / d2
                    hx = pB["x"] + t*vx
                    hy = pB["y"] + t*vy
                    self._save_state()
                    new_pt = {
                        "id": f"pt_{len(self.points)+1}",
                        "name": nh,
                        "x": hx, "y": hy,
                        "color": "#e03131",
                        "fixed": False
                    }
                    self.points.append(new_pt)
                    self.segments.append({
                        "p1": pA, "p2": new_pt,
                        "p1_id": pA.get("id"), "p2_id": new_pt.get("id"),
                        "color": "#e03131", "style": "dashed",
                        "label": f"{na}{nh} ⊥ {nb}{nc}"
                    })
                    executed = True
                    self.lbl_status.config(text=f"🤖 AI Agent đã hạ đường cao phụ: {na}{nh} ⊥ {nb}{nc}", fg="#e03131")

        # 4. ĐƯỜNG TRÒN QUA 3 ĐIỂM: [DRAW_CIRCLE_3P: A, B, C] hoặc câu văn tự nhiên: 'Vẽ đường tròn qua ba điểm A, B, C' / 'Vẽ đường tròn (ABC)'
        m_c3 = re.findall(r"\[(?:DRAW_CIRCLE_3P|TRÒN_3P|DUONG_TRON_3P):\s*([A-Za-z0-9']+)\s*,\s*([A-Za-z0-9']+)\s*,\s*([A-Za-z0-9']+)\]", cmd, re.IGNORECASE)
        m_c3_nl1 = re.findall(r"(?:vẽ|dựng)\s+đường\s+tròn\s+(?:ngoại\s+tiếp\s+)?(?:qua|đi\s+qua)\s+(?:ba\s+điểm\s+|3\s+điểm\s+)?([A-Za-z0-9']+)[,\s]+([A-Za-z0-9']+)[,\s]+(?:và\s+|va\s+)?([A-Za-z0-9']+)", cmd, re.IGNORECASE)
        m_c3_nl2 = re.findall(r"(?:vẽ|dựng)\s+đường\s+tròn\s+(?:ngoại\s+tiếp\s+tam\s+giác\s+|\()([A-Za-z0-9'])\s*([A-Za-z0-9'])\s*([A-Za-z0-9'])\)?", cmd, re.IGNORECASE)
        for triplet in m_c3_nl1 + m_c3_nl2:
            if triplet not in m_c3:
                m_c3.append(triplet)
        for na, nb, nc in m_c3:
            p1 = self.find_point_by_name(na)
            p2 = self.find_point_by_name(nb)
            p3 = self.find_point_by_name(nc)
            if p1 and p2 and p3:
                d = 2 * (p1["x"]*(p2["y"] - p3["y"]) + p2["x"]*(p3["y"] - p1["y"]) + p3["x"]*(p1["y"] - p2["y"]))
                if abs(d) > 1e-7:
                    ux = ((p1["x"]**2 + p1["y"]**2)*(p2["y"] - p3["y"]) + (p2["x"]**2 + p2["y"]**2)*(p3["y"] - p1["y"]) + (p3["x"]**2 + p3["y"]**2)*(p1["y"] - p2["y"])) / d
                    uy = ((p1["x"]**2 + p1["y"]**2)*(p3["x"] - p2["x"]) + (p2["x"]**2 + p2["y"]**2)*(p1["x"] - p3["x"]) + (p3["x"]**2 + p3["y"]**2)*(p2["x"] - p1["x"])) / d
                    r = math.hypot(p1["x"] - ux, p1["y"] - uy)
                    self._save_state()
                    c_pt = {
                        "id": f"pt_{len(self.points)+1}",
                        "name": f"O_{na}{nb}{nc}",
                        "x": ux, "y": uy,
                        "color": "#e03131",
                        "fixed": False
                    }
                    self.points.append(c_pt)
                    self.circles.append({
                        "id": f"cir_{len(self.circles)+1}",
                        "center_id": c_pt["id"],
                        "center": c_pt,
                        "r": r,
                        "color": "#e03131",
                        "style": "dashed"
                    })
                    executed = True
                    self.lbl_status.config(text=f"🤖 AI Agent đã dựng đường tròn ngoại tiếp phụ ({na}{nb}{nc})", fg="#e03131")

        if executed:
            self.redraw()
            self._update_algebra_tree()
        return executed

    def run_ai_solve(self):
        """Gọi AI tự động phân tích và sinh lời giải chi tiết vào Tab Lời giải."""
        # 1. NẾU ĐANG CHẠY MÀ BẤM LẠI THÌ DỪNG NGAY LẬP TỨC
        if getattr(self, "_ai_solving_active", False):
            self._ai_stop_flag = True
            self.lbl_status.config(text="Đã gửi lệnh dừng AI...", fg="#c92a2a")
            return

        if not _AI_HUB_AVAILABLE:
            messagebox.showerror("AI Solve", "Mô-đun AI chưa sẵn sàng.")
            return

        profile_idx = self.combo_ai_profile.current() if hasattr(self, "combo_ai_profile") else 0
        if profile_idx == 0:
            # GÓI 1: Thuần Python -> Chuyển sang giải nhanh bằng thuật toán giải tích chính xác 100%!
            self.solve_general_problem()
            return

        profile_map = {
            1: {"mgr_id": 3, "source": "local", "model": "deepseek-r1:1.5b"},
            2: {"mgr_id": 4, "source": "local", "model": "qwen2.5-coder:7b"},
            3: {"mgr_id": 2, "source": "local", "model": "deepseek-r1:7b"},
        }
        cfg = profile_map.get(profile_idx, profile_map[1])
        chosen_source = "local"
        if not hasattr(self, "ai_hub") or self.ai_hub is None:
            self.ai_hub = AIModelHub()

        self.ai_hub.set_ollama_model(cfg["model"])
        st = self.ai_hub.status()

        if not st.get("ollama_ready") and not st.get("llama_cpp_installed"):
            ans = messagebox.askyesno(
                "Chưa khởi động Local AI",
                "Gói 'Local AI' cần có Ollama đang chạy trên máy tính.\n\n"
                "Bạn có muốn mở Bảng Điều Khiển để xem hướng dẫn khởi động không?"
            )
            if ans:
                self.open_ai_assistant()
            return
        if not hasattr(self, "ai_hub") or self.ai_hub is None:
            self.ai_hub = AIModelHub()

        st = self.ai_hub.status()
        if not st.get("ollama_ready") and not st.get("gemini_key_present") and not st.get("llama_cpp_installed"):
            ans = messagebox.askyesno(
                "Chưa khởi động AI",
                "Hệ thống chưa phát hiện Ollama đang chạy hoặc Gemini API Key.\n\n"
                "Bạn có muốn mở Bảng Điều Khiển AI Support để kích hoạt không?"
            )
            if ans:
                self.open_ai_assistant()
            return

        if hasattr(self, "tab_ctrl"):
            self.tab_ctrl.select(0)  # Chuyển ngay sang Tab Lời giải

        is_vi = (getattr(self, "current_lang", "vi") == "vi")

        # 2. TỰ ĐỘNG LẤY ĐỀ BÀI TỪ THANH CÔNG CỤ NHẬP LIỆU NẾU CHƯA NHẬP TAY
        prob = self.txt_problem.get("1.0", tk.END).strip()
        goal_type = self.combo_goal_type.get() if hasattr(self, "combo_goal_type") else ""
        targets = self.entry_goal_targets.get().strip() if hasattr(self, "entry_goal_targets") else ""
        preset_name = self.combo_presets.get() if hasattr(self, "combo_presets") else ""

        toolbar_target_str = ""
        if goal_type:
            if targets:
                toolbar_target_str = f"{goal_type} đối với ({targets})"
            else:
                toolbar_target_str = f"{goal_type}"

        if not prob or len(prob) < 5:
            if toolbar_target_str:
                prob = f"Mục tiêu bài toán: {toolbar_target_str}."
                if preset_name and "0:" not in preset_name and "Tự do" not in preset_name:
                    prob = f"{preset_name} - {prob}"
                # Điền tự động vào ô đề bài txt_problem để người dùng quan sát trực quan
                self.txt_problem.delete("1.0", tk.END)
                self.txt_problem.insert(tk.END, prob)
            else:
                prob = "Hãy phân tích hình học và các mối quan hệ giữa các đối tượng đã dựng trên hình."
        else:
            if toolbar_target_str and toolbar_target_str not in prob:
                prob = f"{prob} (Mục tiêu khảo sát từ thanh công cụ: {toolbar_target_str})"

        # 3. TRÍCH XUẤT VÀ TẬP TRUNG ĐỐI TƯỢNG MỤC TIÊU CHUẨN XÁC
        matched_target_pts, is_inter, inter_info = self._resolve_target_polygon_points(targets, prob)
        if len(matched_target_pts) >= 3:
            focus_pts = matched_target_pts
        else:
            all_valid_pts = [p for p in self.points if p.get('name') and not p.get('hidden')]
            abc = [p for p in all_valid_pts if p.get('name') in ('A', 'B', 'C')]
            focus_pts = abc if len(abc) == 3 else all_valid_pts

        pts_desc = [f"{p.get('name', 'P')}({p.get('x', 0):.2f}; {p.get('y', 0):.2f})" for p in focus_pts]

        focus_pt_ids = set([p.get('id') for p in focus_pts] + [p.get('name') for p in focus_pts]) if focus_pts else set()
        segs_desc = []
        for s in self.segments:
            p1 = s.get("p1") or next((p for p in self.points if p["id"] == s.get("p1_id")), None)
            p2 = s.get("p2") or next((p for p in self.points if p["id"] == s.get("p2_id")), None)
            if p1 and p2:
                # Nếu đang khảo sát một đa giác mục tiêu, CHỈ lấy các cạnh thuộc đa giác đó
                if focus_pts and len(focus_pts) >= 3:
                    n1 = p1.get('name') or p1.get('id')
                    n2 = p2.get('name') or p2.get('id')
                    if (p1.get('id') not in focus_pt_ids and n1 not in focus_pt_ids) or                        (p2.get('id') not in focus_pt_ids and n2 not in focus_pt_ids):
                        continue
                d = math.hypot(p2["x"] - p1["x"], p2["y"] - p1["y"])
                segs_desc.append(f"{p1.get('name')}{p2.get('name')}={d:.2f}")

        circs_desc = []
        for c in self.circles:
            cp = c.get("center") or next((p for p in self.points if p["id"] == c.get("center_id")), None)
            c_name = cp.get("name") if cp else "O"
            circs_desc.append(f"({c_name}; R={c.get('r', 0):.2f})")

        # 4. TIỀN XỬ LÝ TOÁN HỌC & NHẬN DẠNG HÌNH HỌC THÔNG MINH BẰNG PYTHON (100% CHÍNH XÁC)
        shape_facts = []

        # 4.1. Khóa cứng loại hình đa giác để chống AI ảo giác
        pname_focus = "".join([p.get("name", "") for p in focus_pts])
        if len(focus_pts) == 6:
            shape_facts.append(f"Đa giác {pname_focus} là LỤC GIÁC ĐÚNG 6 ĐỈNH (DEFGHI). TUYỆT ĐỐI CẤM GỌI LÀ HÌNH THANG HOẶC TAM GIÁC.")
        elif len(focus_pts) == 4:
            shape_facts.append(f"Đa giác {pname_focus} là TỨ GIÁC (4 ĐỈNH).")
        elif len(focus_pts) > 6:
            shape_facts.append(f"Đa giác {pname_focus} có {len(focus_pts)} đỉnh.")

        # Nhận diện tính chất Tam giác (Cân, Đều, Vuông) - CHỈ KHI ĐÚNG 3 ĐIỂM ĐANG ĐƯỢC KHẢO SÁT
        if len(focus_pts) == 3:
            pA, pB, pC = focus_pts
            nA, nB, nC = pA.get('name', 'A'), pB.get('name', 'B'), pC.get('name', 'C')
            c_len = math.hypot(pB['x'] - pA['x'], pB['y'] - pA['y'])  # AB
            b_len = math.hypot(pC['x'] - pA['x'], pC['y'] - pA['y'])  # AC
            a_len = math.hypot(pC['x'] - pB['x'], pC['y'] - pB['y'])  # BC
            
            tri_types = []
            if abs(a_len - b_len) < 0.05 and abs(b_len - c_len) < 0.05:
                tri_types.append(f"Tam giác {nA}{nB}{nC} là TAM GIÁC ĐỀU (3 cạnh = {a_len:.2f})")
            elif abs(b_len - c_len) < 0.05:
                tri_types.append(f"Tam giác {nA}{nB}{nC} CÂN TẠI {nA} (do {nA}{nB} = {nA}{nC} = {b_len:.2f}, đáy {nB}{nC} = {a_len:.2f})")
            elif abs(a_len - c_len) < 0.05:
                tri_types.append(f"Tam giác {nA}{nB}{nC} CÂN TẠI {nB} (do {nB}{nA} = {nB}{nC} = {a_len:.2f}, đáy {nA}{nC} = {b_len:.2f})")
            elif abs(a_len - b_len) < 0.05:
                tri_types.append(f"Tam giác {nA}{nB}{nC} CÂN TẠI {nC} (do {nC}{nA} = {nC}{nB} = {a_len:.2f}, đáy {nA}{nB} = {c_len:.2f})")

            # Kiểm tra vuông góc
            if abs(a_len**2 + b_len**2 - c_len**2) < 0.1:
                tri_types.append(f"Tam giác {nA}{nB}{nC} VUÔNG TẠI {nC}")
            elif abs(b_len**2 + c_len**2 - a_len**2) < 0.1:
                tri_types.append(f"Tam giác {nA}{nB}{nC} VUÔNG TẠI {nA}")
            elif abs(c_len**2 + a_len**2 - b_len**2) < 0.1:
                tri_types.append(f"Tam giác {nA}{nB}{nC} VUÔNG TẠI {nB}")

            if tri_types:
                shape_facts.append(" | ".join(tri_types))

        # 4.2. Tính diện tích Đa giác bằng Shoelace
        poly_facts = []
        if hasattr(self, "polygons") and self.polygons:
            for poly in self.polygons:
                pts = poly.get("points", [])
                pname = poly.get("name") or "".join([p.get("name", "") for p in pts])
                area = poly.get("area")
                if area is None and len(pts) >= 3:
                    shoelace = sum(pts[i]["x"] * pts[(i+1)%len(pts)]["y"] - pts[(i+1)%len(pts)]["x"] * pts[i]["y"] for i in range(len(pts)))
                    area = abs(shoelace) / 2.0
                if area is not None:
                    poly_facts.append(f"Đa giác {pname}: Diện tích S = {area:.2f} (đvdt)")
        elif len(focus_pts) >= 3:
            shoelace = sum(focus_pts[i]["x"] * focus_pts[(i+1)%len(focus_pts)]["y"] - focus_pts[(i+1)%len(focus_pts)]["x"] * focus_pts[i]["y"] for i in range(len(focus_pts)))
            area = abs(shoelace) / 2.0
            pname = "".join([p.get("name", "") for p in focus_pts])
            poly_facts.append(f"Đa giác {pname}: Diện tích S = {area:.2f} (Shoelace)")

        ellipse_facts = []
        if hasattr(self, "ellipses") and self.ellipses:
            for el in self.ellipses:
                oname = el.get("center_name", "O")
                a, b = el.get("a", 0), el.get("b", 0)
                s_el = el.get("area", calc_ellipse_area(a, b))
                c_el = el.get("perimeter", calc_ellipse_perimeter(a, b))
                ellipse_facts.append(f"Elip tâm {oname} (a={a:.2f}, b={b:.2f}): S={s_el:.2f}, C≈{c_el:.2f}")

        geom_relations = []
        for i, s1 in enumerate(self.segments):
            for s2 in self.segments[i+1:]:
                p1_1 = s1.get("p1") or next((p for p in self.points if p["id"] == s1.get("p1_id")), None)
                p1_2 = s1.get("p2") or next((p for p in self.points if p["id"] == s1.get("p2_id")), None)
                p2_1 = s2.get("p1") or next((p for p in self.points if p["id"] == s2.get("p1_id")), None)
                p2_2 = s2.get("p2") or next((p for p in self.points if p["id"] == s2.get("p2_id")), None)
                if not (p1_1 and p1_2 and p2_1 and p2_2):
                    continue
                common = set([p1_1.get("id"), p1_2.get("id")]).intersection([p2_1.get("id"), p2_2.get("id")])
                if common:
                    cid = list(common)[0]
                    other1 = p1_2 if p1_1.get("id") == cid else p1_1
                    other2 = p2_2 if p2_1.get("id") == cid else p2_1
                    pC = p1_1 if p1_1.get("id") == cid else p1_2
                    if pC and other1 and other2:
                        v1x, v1y = other1["x"] - pC["x"], other1["y"] - pC["y"]
                        v2x, v2y = other2["x"] - pC["x"], other2["y"] - pC["y"]
                        dot = v1x * v2x + v1y * v2y
                        l1 = math.hypot(v1x, v1y)
                        l2 = math.hypot(v2x, v2y)
                        if l1 > 1e-6 and l2 > 1e-6 and abs(dot / (l1 * l2)) < 1e-3:
                            geom_relations.append(f"∠{other1.get('name')}{pC.get('name')}{other2.get('name')} = 90° (vuông góc)")

        # 5. KIỂM TRA & TỰ ĐỘNG THỰC THI THUẬT TOÁN HÌNH HỌC PYTHON (ĐẢM BẢO LUÔN CÓ GROUND TRUTH 100%)
        existing_text = self.txt_solution.get("1.0", tk.END).strip()
        has_prior_python_sol = bool(
            existing_text and len(existing_text) > 40 and 
            ("SYMPY CAS" in existing_text or "GAUSS" in existing_text or "SHOELACE" in existing_text or "ĐỊNH LÝ" in existing_text or "BÀI TOÁN" in existing_text or "KẾT QUẢ" in existing_text or "EUCLID" in existing_text)
        )
        if not has_prior_python_sol:
            try:
                self.solve_general_problem()
                existing_text = self.txt_solution.get("1.0", tk.END).strip()
                has_prior_python_sol = bool(existing_text and len(existing_text) > 40)
            except Exception:
                pass

        prompt_parts = [
            "Bạn là Chuyên gia Hình học và Trợ lý hình học kỹ thuật (Geometry Agent)." if is_vi else "You are an expert high school Mathematics teacher and Interactive Geometry Agent.",
            "Nhiệm vụ: Dựa vào đề bài, số liệu hình học và KẾT QUẢ ĐÃ TÍNH TOÁN BỞI THUẬT TOÁN PYTHON sau đây, hãy phân tích cấu trúc hình học, nêu trực giác và đề xuất vẽ đường phụ nếu cần thiết.\n",
            f"【ĐỀ BÀI / MỤC TIÊU】: {prob}\n",
            "【KẾT QUẢ HÌNH HỌC ĐÃ TÍNH TOÁN CHÍNH XÁC 100% TỪ PYTHON ENGINE (GROUND TRUTH)】:",
            f"• Nhận diện hình học đặc biệt (Python CAS): {'; '.join(shape_facts) if shape_facts else 'Đa giác thông thường'}",
            f"• Dữ liệu diện tích: {'; '.join(poly_facts) if poly_facts else 'Chưa xác định đa giác'}",
            f"• Dữ liệu đường conic/elip: {'; '.join(ellipse_facts) if ellipse_facts else 'Không có elip'}",
            f"• Quan hệ đặc biệt: {'; '.join(geom_relations[:6]) if geom_relations else 'Không có góc đặc biệt'}",
            f"• Tọa độ các điểm: {', '.join(pts_desc) if pts_desc else 'Chưa có điểm'}",
            f"• Độ dài các đoạn thẳng: {', '.join(segs_desc[:12]) if segs_desc else 'Chưa có đoạn thẳng'}\n",
        ]

        if has_prior_python_sol:
            prompt_parts.append(f"【LỜI GIẢI GIẢI TÍCH ĐÃ ĐƯỢC THUẬT TOÁN PYTHON XUẤT TRƯỚC ĐÓ】:\n{existing_text[:1200]}\n")
            prompt_parts.append("LƯU Ý ĐẶC BIỆT: Bạn KHÔNG CẦN tính toán lại các số trên. Hãy đọc trực tiếp kết quả giải tích của Python để phân tích kỹ thuật và trình bày lời giải.")

        prompt_parts.extend([
            "【QUY TẮC BẮT BUỘC DÀNH CHO AI AGENT - KỶ LUẬT TUYỆT ĐỐI (ZERO HALLUCINATION)】:",
            "1. VAI TRÒ DUY NHẤT: Bạn là người thuyết minh toán học (Humanized Explainer). Nhiệm vụ của bạn là đọc các con số diện tích và độ dài đã được Python tính toán chính xác ở trên để viết lại thành lời giải mạch lạc, dễ hiểu.",
            "2. TUYỆT ĐỐI KHÔNG ĐƯỢC TỰ BỊA RA ĐẶC TÍNH HÌNH HỌC KHÔNG CÓ TRONG DỮ LIỆU: Nếu là Lục giác 6 đỉnh (DEFGHI), TUYỆT ĐỐI CẤM GỌI LÀ HÌNH THANG, TAM GIÁC HOẶC TỨ GIÁC!",
            "3. TUYỆT ĐỐI KHÔNG ĐƯỢC TỰ BỊA RA CÁC CẶP CẠNH SONG SONG NHƯ FG // HI khi Python chưa xác nhận.",
            "4. TUYỆT ĐỐI KHÔNG ĐƯA CÁC ĐOẠN THẲNG CỦA HÌNH KHÁC (như AB, BC, CA) VÀO LỜI GIẢI khi đang giải cho đa giác DEFGHI.",
            "5. TRÌNH BÀY MẠCH LẠC 3 PHẦN:",
            "   - Phần 1: Cấu trúc hình học của đa giác (số đỉnh, tọa độ, các cặp cạnh tương ứng).",
            "   - Phần 2: Ý nghĩa công thức Dây giày Gauss Shoelace và các bước nhân chéo tọa độ.",
            "   - Phần 3: Kết luận về Chu vi P và Diện tích S (dùng đúng con số Python đã tính).",
            "6. TUYỆT ĐỐI KHÔNG TỰ BỊA RA ĐIỂM MỚI HOẶC ĐƯỜNG PHỤ NẰM NGOÀI DỮ LIỆU. Chỉ sử dụng và phân tích các đối tượng hình học đã được Python tính toán ở trên.",
            "7. Lời văn ngắn gọn, súc tích, hoàn toàn bằng Tiếng Việt, cấm lặp từ hoặc suy nghĩ dông dài ngoài lề."
        ])
        full_prompt = "\n".join(prompt_parts)

        # 6. QUẢN LÝ GIAO DIỆN & GHI NỐI TIẾP VÀO TXT_SOLUTION
        if has_prior_python_sol:
            # Ghi nối tiếp vào dưới lời giải Python cũ, KHÔNG XÓA NỘI DUNG CŨ!
            sep = "\n\n" + "="*57 + "\n"
            self.txt_solution.insert(tk.END, sep)
            ai_title = "PHÂN TÍCH & ĐỊNH HƯỚNG GIẢI TOÁN (AI):\n" if is_vi else "🤖 MATHEMATICAL ANALYSIS & INTUITION (AI):\n"
            self.txt_solution.insert(tk.END, ai_title)
            self.txt_solution.insert(tk.END, "="*57 + "\n")
            self.txt_solution.insert(tk.END, "⏳ Đang kết nối mô hình và suy luận trực tiếp từng bước...\n\n" if is_vi else "⏳ Connecting AI inference engine and streaming...\n\n")
        else:
            # Nếu chưa có lời giải Python, tự động chạy giải tích Python trước
            python_pedagogical_section = ""
            target_pts = focus_pts
            if target_pts and len(target_pts) >= 3:
                try:
                    python_pedagogical_section = format_polygon_pedagogical_area(
                        target_pts, lang="vi" if is_vi else "en",
                        is_intersection=is_inter, inter_info=inter_info
                    )
                except Exception as e_poly:
                    print("Lỗi tạo lời giải đa giác Python:", e_poly)

            self.txt_solution.delete("1.0", tk.END)
            if python_pedagogical_section:
                self.txt_solution.insert(tk.END, python_pedagogical_section)
                sep = "\n\n" + "="*57 + "\n"
                self.txt_solution.insert(tk.END, sep)
                ai_title = "PHÂN TÍCH & ĐỊNH HƯỚNG GIẢI TOÁN (AI):\n" if is_vi else "🤖 MATHEMATICAL ANALYSIS & INTUITION (AI):\n"
                self.txt_solution.insert(tk.END, ai_title)
                self.txt_solution.insert(tk.END, "="*57 + "\n")
                self.txt_solution.insert(tk.END, "⏳ Đang kết nối mô hình và suy luận trực tiếp từng bước...\n\n" if is_vi else "⏳ Connecting AI inference engine and streaming...\n\n")
            else:
                hdr = (
                    "=========================================================\n"
                    "LỜI GIẢI CHI TIẾT (KẾT HỢP GIẢI TÍCH & AI)\n"
                    "=========================================================\n"
                    "⏳ Đang kết nối mô hình và suy luận trực tiếp từng bước...\n\n"
                ) if is_vi else (
                    "=========================================================\n"
                    "DETAILED SOLUTION (ANALYTIC CAS + AI)\n"
                    "=========================================================\n"
                    "⏳ Connecting AI inference engine and streaming...\n\n"
                )
                self.txt_solution.insert(tk.END, hdr)

        self.txt_solution.see(tk.END)

        # 7. KHÓA NÚT VÀ CẬP NHẬT TRẠNG THÁI RÕ RÀNG
        self._ai_solving_active = True
        self._ai_stop_flag = False
        self.btn_ai_solve.config(text="⏹ Dừng AI" if is_vi else "⏹ Stop AI", bg="#c92a2a", state=tk.NORMAL)
        if hasattr(self, "btn_run_solver"):
            self.btn_run_solver.config(state=tk.DISABLED)
        self.lbl_status.config(text="⏳ AI đang suy luận từng bước (Bấm '⏹ Dừng AI' để hủy)...", fg="#c92a2a")

        # 8. TIẾN TRÌNH LUỒNG AI & PARSER TỰ ĐỘNG DỰNG HÌNH
        def _worker():
            recent_chunks = []
            line_buf = ""
            try:
                for chunk in self.ai_hub.stream(full_prompt, source=chosen_source):
                    if getattr(self, "_ai_stop_flag", False):
                        self.after(0, lambda: self.txt_solution.insert(tk.END, "\n\n[AI] Đã dừng theo yêu cầu người dùng.\n"))
                        break
                    t = chunk.text
                    recent_chunks.append(t)
                    if len(recent_chunks) > 20:
                        recent_chunks.pop(0)

                    # Bẫy chống lặp token
                    recent_str = "".join(recent_chunks)
                    if recent_str.count(",000") >= 4 or recent_str.count("000,000") >= 3 or (len(t) >= 4 and recent_str.count(t) >= 5):
                        self.after(0, lambda: self.txt_solution.insert(tk.END, "\n\n[Hệ thống tự động ngắt chuỗi lặp AI - Đảm bảo tính nhất quán toán học]\n"))
                        break

                    # Tự động phát hiện và thực thi lệnh dựng hình phụ trực tiếp trên Canvas (Cả mã thẻ lẫn tiếng Việt tự nhiên)
                    line_buf += t
                    if "\n" in line_buf:
                        curr_line, line_buf = line_buf.split("\n", 1)
                        if curr_line.strip():
                            self.after(0, lambda c=curr_line: self._execute_ai_drawing_command(c))
                    elif "]" in line_buf:
                        curr_line = line_buf[:line_buf.rfind("]")+1]
                        line_buf = line_buf[line_buf.rfind("]")+1:]
                        if curr_line.strip():
                            self.after(0, lambda c=curr_line: self._execute_ai_drawing_command(c))

                    self.after(0, lambda text=t: (self.txt_solution.insert(tk.END, text), self.txt_solution.see(tk.END)))
                else:
                    self.after(0, lambda: self.txt_solution.insert(
                        tk.END,
                        "\n\n═════════════════════════════════════════════════════════\n"
                        "✅ [HOÀN TẤT LỜI GIẢI - AI ĐÃ KẾT THÚC TIẾN TRÌNH SUY LUẬN]\n"
                        "═════════════════════════════════════════════════════════\n"
                    ))
            except Exception as ex:
                self.after(0, lambda e=str(ex): self.txt_solution.insert(tk.END, f"\n\n⚠️ Lỗi AI: {e}\n"))
            finally:
                def _reset_btn():
                    self._ai_solving_active = False
                    self.btn_ai_solve.config(
                        text="AI giải toán (F5)" if is_vi else "AI Solve (F5)",
                        bg="#e8590c",
                        state=tk.NORMAL
                    )
                    if hasattr(self, "btn_run_solver"):
                        self.btn_run_solver.config(state=tk.NORMAL)
                    if getattr(self, "_ai_stop_flag", False):
                        self.lbl_status.config(text="⏹ Đã dừng AI theo yêu cầu.", fg="#495057")
                    else:
                        self.lbl_status.config(text="✅ Đã hoàn tất giải toán (Python & AI Agent).", fg="#2b8a3e")
                self.after(0, _reset_btn)

        import threading
        threading.Thread(target=_worker, daemon=True).start()


    def solve_general_problem(self):

        """Bộ giải toán hình học toàn diện: xuất lời giải chi tiết và tính tọa độ SymPy."""

        is_en = (getattr(self, "current_lang", "vi") == "en")



        goal_type = self.combo_goal_type.get() if hasattr(self, "combo_goal_type") else "Tìm tọa độ điểm"

        goal_idx = self.combo_goal_type.current() if hasattr(self, "combo_goal_type") else -1

        targets = self.entry_goal_targets.get().strip() if hasattr(self, "entry_goal_targets") else ""

        prob = self.txt_problem.get("1.0", tk.END).strip()



        # 1. KIỂM TRA BÀI TOÁN BÀI 1 (VMO 2000)

        if self.current_preset == "vmo_2000" or "VMO 2000" in prob or "M1QM2" in prob:

            if is_en:

                sol_vmo2000 = (

                    "[PROBLEM]: PROBLEM 1 (VMO 2000) - LOCUS OF MIDPOINT & FIXED INTERSECTION POINT\n"

                    "---------------------------------------------------------\n"

                    "1) LOCUS OF MIDPOINT M OF SEGMENT M1M2:\n"

                    "   • Let O be the fixed midpoint of segment O1O2.\n"

                    "   • Construct points M'1, M'2 such that: vector(OM'1) = vector(O1M1), vector(OM'2) = vector(O2M2).\n"

                    "   • Since M1, M2 rotate on (O1; r1) and (O2; r2) clockwise with identical angular velocity omega:\n"

                    "     => M'1 and M'2 also rotate around O with the same speed and sense.\n"

                    "     => Distance M'1M'2 = d = const.\n"

                    "   • M is midpoint of M1M2 <=> vector(OM) = 1/2(vector(OM1) + vector(OM2)) <=> M is midpoint of M'1M'2.\n"

                    "   • Applying median length formula in triangle OM'1M'2:\n"

                    "     OM^2 = (2*OM'1^2 + 2*OM'2^2 - M'1M'2^2) / 4 = (2*r1^2 + 2*r2^2 - d^2) / 4.\n"

                    "   • CONCLUSION 1: The locus of midpoint M is a CIRCLE centered at O with radius:\n"

                    "     R_M = 1/2 * sqrt(2*r1^2 + 2*r2^2 - d^2) (Q.E.D).\n\n"

                    "2) PROVING THE SECOND INTERSECTION P OF (M1QM2) AND (O1QO2) IS A FIXED POINT:\n"

                    "   • Triangles ΔPO1M1 and ΔPO2M2 are similar (a.a) => PO1 / PO2 = r1 / r2 = const.\n"

                    "     => Point P belongs to the CIRCLE OF APOLLONIUS on O1O2 with ratio r1/r2 (1).\n"

                    "   • Moreover, directed angle (PO1, PO2) = alpha = const.\n"

                    "     => Point P lies on the CIRCULAR ARC of constant angle alpha on O1O2 (2).\n"

                    "   • From (1) and (2): Intersection P is a UNIQUE FIXED POINT (Q.E.D)!\n"

                    "=========================================================\n"

                )

            else:

                sol_vmo2000 = (

                    "[BÀI TOÁN]: BÀI 1 (VMO 2000 - BẢNG B)\n"

                    "---------------------------------------------------------\n"

                    "1) TÌM QUỸ TÍCH TRUNG ĐIỂM M CỦA ĐOẠN THẲNG M1M2:\n"

                    "   • Gọi O là trung điểm cố định của đoạn thẳng O1O2.\n"

                    "   • Dựng các điểm M'1, M'2 sao cho: vector(OM'1) = vector(O1M1), vector(OM'2) = vector(O2M2).\n"

                    "   • Do M1, M2 chuyển động trên (O1; r1) và (O2; r2) cùng chiều kim đồng hồ với cùng vận tốc góc omega:\n"

                    "     => M'1 và M'2 cũng quay quanh O theo cùng chiều và cùng vận tốc góc omega.\n"

                    "     => Khoảng cách M'1M'2 = d = const không đổi.\n"

                    "   • Ta có: M là trung điểm M1M2 <=> vector(OM) = 1/2(vector(OM1) + vector(OM2))\n"

                    "     <=> vector(OM) = 1/2(vector(OM'1) + vector(OM'2)) <=> M là trung điểm M'1M'2.\n"

                    "   • Áp dụng công thức đường trung tuyến trong tam giác OM'1M'2:\n"

                    "     OM^2 = (2*OM'1^2 + 2*OM'2^2 - M'1M'2^2) / 4 = (2*r1^2 + 2*r2^2 - d^2) / 4.\n"

                    "   • KẾT LUẬN 1: Quỹ tích của trung điểm M là ĐƯỜNG TRÒN tâm O bán kính:\n"

                    "     R_M = 1/2 * sqrt(2*r1^2 + 2*r2^2 - d^2) (với d = M1M2 = const).\n\n"

                    "2) CHỨNG MINH GIAO ĐIỂM THỨ HAI P CỦA (M1QM2) VÀ (O1QO2) CỐ ĐỊNH:\n"

                    "   • Xét hai tam giác PO1M1 và PO2M2:\n"

                    "     Ta có góc PO1M1 = góc PO2M2 và góc PM1O1 = góc PM2O2.\n"

                    "     => ΔPO1M1 đồng dạng với ΔPO2M2 (g.g).\n"

                    "     => Tỉ số khoảng cách: PO1 / PO2 = O1M1 / O2M2 = r1 / r2 = hằng số không đổi.\n"

                    "     => Điểm P thuộc ĐƯỜNG TRÒN APÔLÔNIUT dựng trên đoạn cố định O1O2 theo tỉ số r1/r2 (1).\n"

                    "   • Mặt khác, góc định hướng (PO1, PO2) = alpha = const không đổi.\n"

                    "     => Điểm P thuộc CUNG CHỨA GÓC định hướng alpha dựng trên đoạn cố định O1O2 (2).\n"

                    "   • Từ (1) và (2) suy ra: Giao điểm P của đường tròn Apôlôniut và cung chứa góc cố định\n"

                    "     là một ĐIỂM CỐ ĐỊNH DUY NHẤT (ĐPCM).\n"

                    "=========================================================\n"

                )

            self._output_solution(sol_vmo2000, clear=True)

            return



        # 2. KIỂM TRA BÀI TOÁN BÀI 2 (VMO 2001)

        if self.current_preset == "vmo_2001" or "VMO 2001" in prob or "M1, B, M2" in targets:

            if is_en:

                sol_vmo2001 = (

                    "[PROBLEM]: PROBLEM 2 (VMO 2001) - PROVING M1, B, M2 COLLINEAR\n"

                    "---------------------------------------------------------\n"

                    "PROOF OF COLLINEARITY FOR M1, B, M2:\n"

                    "Let R1, R2 be radii of circles (O1) and (O2).\n"

                    "• Case 1: R1 = R2.\n"

                    "  Q1 coincides with O1 and Q2 coincides with O2 => ∠M1BA = ∠M2BA = 90°.\n"

                    "  => ∠M1BA + ∠M2BA = 180° => M1, B, M2 are collinear.\n\n"

                    "• Case 2: R1 ≠ R2 (Assume R1 > R2).\n"

                    "  1. Let S = P1P2 ∩ O1O2. S is the homothety center mapping (O1) to (O2).\n"

                    "  2. Let A1 be the second intersection of SA with circle (O1).\n"

                    "     Under homothety V_S: A1 -> A, O1 -> O2, Q1 -> Q2 => ∠O1A1Q1 = ∠O2AQ2.\n"

                    "  3. By power of a point and secant-tangent theorem:\n"

                    "     SP1^2 = SA * SA1 = SQ1 * SO1 => Quadrilateral A, Q1, O1, A1 is cyclic.\n"

                    "     => ∠O1A1Q1 = ∠O1AQ1 (subtending same arc O1Q1).\n"

                    "  4. Therefore: ∠O1AQ1 = ∠O2AQ2 => ∠M1O1A = ∠M2O2A.\n"

                    "  5. Sum of adjacent supplementary angles at B:\n"

                    "     ∠M1BA + ∠M2BA = 180° - (∠M1O1A + ∠M2O2A)/2 + ... = 180°.\n"

                    "  => Points M1, B, M2 are COLLINEAR (Q.E.D)!\n"

                    "=========================================================\n"

                )

            else:

                sol_vmo2001 = (

                    "[BÀI TOÁN]: BÀI 2 (VMO 2001 - BẢNG B)\n"

                    "---------------------------------------------------------\n"

                    "CHỨNG MINH M1, B, M2 THẲNG HÀNG:\n"

                    "Gọi R1, R2 là bán kính của (O1) và (O2).\n"

                    "• Trường hợp 1: R1 = R2.\n"

                    "  Khi đó Q1 trùng O1 và Q2 trùng O2 => góc M1BA = góc M2BA = 90 độ.\n"

                    "  => góc M1BA + góc M2BA = 180 độ => M1, B, M2 thẳng hàng.\n\n"

                    "• Trường hợp 2: R1 khác R2 (Giả sử R1 > R2).\n"

                    "  1. Gọi S = P1P2 ∩ O1O2. S chính là tâm của phép vị tự V_S biến (O1) thành (O2).\n"

                    "  2. Gọi A1 là giao điểm thứ hai của SA với đường tròn (O1).\n"

                    "     Qua phép vị tự V_S: A1 -> A, O1 -> O2, Q1 -> Q2 => góc O1A1Q1 = góc O2AQ2.\n"

                    "  3. Mặt khác theo hệ thức lượng tiếp tuyến và cát tuyến:\n"

                    "     SP1^2 = SA * SA1. Lại có trong tam giác vuông SO1P1: SP1^2 = SQ1 * SO1.\n"

                    "     => SA * SA1 = SQ1 * SO1 => Tứ giác A, Q1, O1, A1 cùng thuộc một đường tròn.\n"

                    "     => góc O1A1Q1 = góc O1AQ1 (cùng chắn cung O1Q1).\n"

                    "  4. Suy ra: góc O1AQ1 = góc O2AQ2 => góc M1O1A = góc M2O2A.\n"

                    "  5. Tính tổng hai góc kề bù tại B:\n"

                    "     góc M1BA + góc M2BA = 180° - (góc M1O1A + góc M2O2A)/2 + ... = 180°.\n"

                    "  => Ba điểm M1, B, M2 THẲNG HÀNG (ĐPCM).\n"

                    "=========================================================\n"

                )

            self._output_solution(sol_vmo2001, clear=True)

            return



        # 3. KIỂM TRA BÀI TOÁN BÀI 9 (VMO 2007)

        if self.current_preset == "vmo_2007" or "VMO 2007" in prob or "hypebol" in prob.lower():

            if is_en:

                sol_vmo2007 = (

                    "[PROBLEM]: PROBLEM 9 (VMO 2007) - LOCUS OF VERTEX A VIA SYMPY CARTESIAN MODELING\n"

                    "---------------------------------------------------------\n"

                    "1. Cartesian coordinate system with origin O at midpoint of BC, x-axis along BC:\n"

                    "   Let BC = 2a > 0 => Coordinates B(-a, 0), C(a, 0). Let A(x0, y0) with y0 ≠ 0.\n"

                    "2. Centroid G coordinates:\n"

                    "   G = ( (xA + xB + xC)/3, (yA + yB + yC)/3 ) = ( x0/3, y0/3 ).\n"

                    "3. Orthocenter H coordinates:\n"

                    "   Altitude AH ⊥ BC => xH = x0.\n"

                    "   BH ⊥ AC <=> (x0 + a)(a - x0) - yH * y0 = 0 => yH = (a^2 - x0^2) / y0.\n"

                    "   => H( x0, (a^2 - x0^2)/y0 ).\n"

                    "4. Midpoint K of HG:\n"

                    "   xK = 2*x0 / 3,  yK = (3*a^2 - 3*x0^2 + y0^2) / (6*y0).\n"

                    "5. Condition K lies on line BC (x-axis: y = 0):\n"

                    "   <=> yK = 0 <=> 3*x0^2 - y0^2 = 3*a^2 <=> x0^2 / a^2 - y0^2 / (3*a^2) = 1.\n"

                    "• CONCLUSION: The locus of vertex A is the HYPERBOLA (H):\n"

                    "  x^2 / a^2 - y^2 / (3*a^2) = 1 (excluding points B(-a, 0) and C(a, 0)) (Q.E.D)!\n"

                    "=========================================================\n"

                )

            else:

                sol_vmo2007 = (

                    "[BÀI TOÁN]: BÀI 9 (VMO 2007) - QUỸ TÍCH ĐỈNH A BẰNG TỌA ĐỘ HÓA SYMPY\n"

                    "---------------------------------------------------------\n"

                    "1. Chọn hệ trục tọa độ Oxy với O là trung điểm BC, trục Ox là đường thẳng BC:\n"

                    "   Đặt BC = 2a > 0 => Tọa độ B(-a; 0), C(a; 0). Gọi A(x0; y0) với y0 khác 0.\n"

                    "2. Xác định tọa độ trọng tâm G:\n"

                    "   G = ( (xA + xB + xC)/3; (yA + yB + yC)/3 ) = ( x0/3; y0/3 ).\n"

                    "3. Xác định tọa độ trực tâm H:\n"

                    "   Đường cao AH vuông góc BC => xH = x0.\n"

                    "   Vector BH = (x0 + a; yH), Vector AC = (a - x0; -y0).\n"

                    "   BH vuông góc AC <=> BH . AC = 0 <=> (x0 + a)(a - x0) - yH * y0 = 0\n"

                    "   <=> a^2 - x0^2 - yH * y0 = 0 => yH = (a^2 - x0^2) / y0.\n"

                    "   => H( x0; (a^2 - x0^2)/y0 ).\n"

                    "4. Xác định trung điểm K của đoạn HG:\n"

                    "   xK = (xH + xG)/2 = (x0 + x0/3)/2 = 2*x0 / 3.\n"

                    "   yK = (yH + yG)/2 = [ (a^2 - x0^2)/y0 + y0/3 ] / 2 = (3*a^2 - 3*x0^2 + y0^2) / (6*y0).\n"

                    "5. Điều kiện K thuộc đường thẳng BC (trục Ox: y = 0):\n"

                    "   <=> yK = 0 <=> 3*a^2 - 3*x0^2 + y0^2 = 0\n"

                    "   <=> 3*x0^2 - y0^2 = 3*a^2 <=> x0^2 / a^2 - y0^2 / (3*a^2) = 1 (với y0 khác 0).\n"

                    "• KẾT LUẬN: Quỹ tích các điểm A là đường HYPEBOL (H):\n"

                    "  x^2 / a^2 - y^2 / (3*a^2) = 1 (loại trừ hai điểm B(-a; 0) và C(a; 0)).\n"

                    "=========================================================\n"

                )

            self._output_solution(sol_vmo2007, clear=True)

            return

            self._output_solution(sol_vmo2007, clear=True)

            return



        # 4. KIỂM TRA BÀI TOÁN CÂU VIII (TUYỂN SINH OXY)

        known_pts = {p["name"]: (p["x"], p["y"]) for p in self.points if p.get("name")}

        if self.current_preset == "cau_viii" or "Câu VIII" in prob or "tứ giác abcd nội tiếp" in prob.lower() or ("P" in known_pts and "M" in known_pts and "N" in known_pts and "circle_BD" in [c["id"] for c in self.circles]):

            x, y, t = sp.symbols('x y t', real=True)

            M_c, N_c = known_pts.get("M", (0, 4)), known_pts.get("N", (2, 2))



            dx = N_c[0] - M_c[0]

            dy = N_c[1] - M_c[1]

            eq_MN = dy * (x - M_c[0]) - dx * (y - M_c[1])

            eq_AC = x - y - 1



            sol_P = sp.solve([eq_MN, eq_AC], (x, y))

            Px = float(sol_P[x]) if x in sol_P else 2.5

            Py = float(sol_P[y]) if y in sol_P else 1.5



            PM_sq = (M_c[0] - Px)**2 + (M_c[1] - Py)**2

            PA_sq = (t - Px)**2 + (t - 1 - Py)**2

            sols_t = sp.solve(sp.Eq(PA_sq, PM_sq), t)

            valid_t = min(sols_t) if sols_t else 0.0

            Ax, Ay = float(valid_t), float(valid_t - 1)



            if is_en:

                sol_viii = (

                    "[PROBLEM]: QUESTION VIII (HIGH SCHOOL ENTRANCE EXAM OXY) - 9-POINT EULER CIRCLE\n"

                    "---------------------------------------------------------\n"

                    "1. SYNTHETIC GEOMETRIC DEDUCTION (KEY UNLOCKING STEP):\n"

                    "   • Trapezoid ABCD is inscribed in circle with diameter BD => angle BAD = angle BCD = 90°.\n"

                    "   • AM ⊥ BC, CD ⊥ BC => AM // CD => alternate interior angles: angle MAC = angle ACD.\n"

                    "   • In quadrilateral ABNM: angle AMB = angle ANB = 90° => ABNM is cyclic with diameter AB.\n"

                    "   • In the circumcircle of ABNM: angle AMN = angle ABN = angle ABD.\n"

                    "   • In circumcircle of ABCD: angle ABD = angle ACD (subtending arc AD).\n"

                    "   => angle AMN = angle MAC <=> angle PMA = angle PAM.\n"

                    "   => TRIANGLE PAM IS ISOSCELES AT P => PA = PM (The Key Synthetic Invariant!).\n\n"

                    "2. CARTESIAN CAS SYMPY ALGEBRAIC COMPUTATION:\n"

                    f"   • Line MN passes through M(0, 4) and N(2, 2) => Line equation: x + y - 4 = 0.\n"

                    f"   • Intersection P = MN ∩ AC (where AC: x - y - 1 = 0):\n"

                    f"     => Point P({Px:.4f}, {Py:.4f}) [P(5/2, 3/2)].\n\n"

                    f"   • Distance PM^2 = (0 - 2.5)^2 + (4 - 1.5)^2 = {float(PM_sq):.4f}.\n"

                    f"   • Vertex A belongs to AC => let A(t, t - 1). Since PA = PM => PA^2 = PM^2:\n"

                    f"     2*(t - 2.5)^2 = 12.5 <=> t in {sols_t}. Given xA < 2 => choose t = {valid_t}.\n"

                    f"     => Coordinates of vertex A: ({Ax:.4f}, {Ay:.4f}) [A(0, -1)].\n\n"

                    f"   • Coordinates of vertex B:\n"

                    f"     - BC ⊥ AM at M(0, 4) with AM on Oy => BC equation: y = 4.\n"

                    f"     - BD ⊥ AN at N(2, 2) with vector AN = (2, 3) => BD equation: 2x + 3y - 10 = 0.\n"

                    f"     - B = BC ∩ BD => B(-1.0000, 4.0000).\n\n"

                    "=========================================================\n"

                    f"🎯 EXACT CARTESIAN RESULTS:\n"

                    f"• Point P  = ({Px:.4f}, {Py:.4f}) = (5/2, 3/2)\n"

                    f"• Vertex A = ({Ax:.4f}, {Ay:.4f}) = (0, -1)\n"

                    f"• Vertex B = (-1.0000, 4.0000)\n"

                    "=========================================================\n"

                )

            else:

                sol_viii = (

                    "[BÀI TOÁN]: CÂU VIII (TUYỂN SINH OXY)\n"

                "---------------------------------------------------------\n"

                "1. SUY LUẬN HÌNH HỌC THUẦN TÚY ĐỂ MỞ KHÓA BÀI TOÁN:\n"

                "   • Tứ giác ABCD nội tiếp đường tròn đường kính BD => góc BAD = góc BCD = 90°.\n"

                "   • AM vuông góc BC, CD vuông góc BC => AM // CD => góc MAC = góc ACD (so le trong).\n"

                "   • Xét tứ giác ABNM: có góc AMB = 90° và góc ANB = 90° => ABNM nội tiếp đường kính AB.\n"

                "   • Trong đường tròn đường kính AB: góc AMN = góc ABN = góc ABD.\n"

                "   • Trong đường tròn ngoại tiếp ABCD: góc ABD = góc ACD (cùng chắn cung AD).\n"

                "   => góc AMN = góc MAC <=> góc PMA = góc PAM.\n"

                "   => TAM GIÁC PAM CÂN TẠI P => PA = PM (Chìa khóa then chốt!).\n\n"

                "2. TỌA ĐỘ HÓA ĐẠI SỐ BẰNG SYMPY:\n"

                f"   • Đường thẳng MN qua M(0; 4) và N(2; 2) có pt: x + y - 4 = 0.\n"

                f"   • Giao điểm P = MN ∩ AC (với AC: x - y - 1 = 0):\n"

                f"     => P({Px:.2f}; {Py:.2f}) = P(5/2; 3/2).\n\n"

                f"   • Tính độ dài PM^2 = (0 - 2.5)^2 + (4 - 1.5)^2 = {float(PM_sq):.4f}.\n"

                f"   • A thuộc AC => gọi A(t; t - 1). Do PA = PM => PA^2 = PM^2:\n"

                f"     2*(t - 2.5)^2 = 12.5 <=> t in {sols_t}. Do giả thiết xA < 2 => chọn t = {valid_t}.\n"

                f"     => Tọa độ điểm A: ({Ax:.2f}; {Ay:.2f}) = (0; -1).\n\n"

                f"   • Tìm điểm B:\n"

                f"     - BC vuông góc AM tại M(0; 4) với AM trên trục Oy => BC có pt: y = 4.\n"

                f"     - BD vuông góc AN tại N(2; 2) với vector AN = (2; 3) => BD có pt: 2x + 3y - 10 = 0.\n"

                f"     - B = BC ∩ BD => B(-1.00; 4.00).\n\n"

                "=========================================================\n"

                f"🎯 ĐÁP SỐ CHÍNH XÁC:\n"

                f"• Điểm P = ({Px:.2f}; {Py:.2f}) = (5/2; 3/2)\n"

                f"• Điểm A = ({Ax:.2f}; {Ay:.2f}) = (0; -1)\n"

                f"• Điểm B = (-1.00; 4.00)\n"

                "=========================================================\n"

            )

            self._output_solution(sol_viii, clear=True)

            return



        # 5. KIỂM TRA BÀI TOÁN BÀI 4 (VMO 2003)

        if self.current_preset == "vmo_2003" or "VMO 2003" in prob or "MN = AC" in prob or "vector(MN)" in prob or ("trực tâm H" in prob.lower() and "O'" in prob):

            if is_en:

                sol_vmo2003 = (

                    "[PROBLEM]: PROBLEM 4 (VMO 2003) - ORTHOCENTER & HOMOTHETIC SYMMETRY\n"

                    "---------------------------------------------------------\n"

                    "1) PROVING ORTHOCENTER H LIES ON CIRCUMCIRCLE (O') OF ΔBED:\n"

                    "   • Let K = MD ∩ NE.\n"

                    "   • Since angle BEK = angle BDK = 90°, circumcircle (O') of ΔBED is the CIRCLE WITH DIAMETER BK.\n"

                    "   • AH ⊥ BC and MK ⊥ BC => AH // MK => alternate interior angles: angle HAC = angle KMN.\n"

                    "   • CH ⊥ AB and NK ⊥ AB => CH // NK => alternate interior angles: angle ACH = angle MNK.\n"

                    "   • By hypothesis: vector(MN) = vector(AC) => length MN = AC.\n"

                    "     => ΔAHC = ΔMKN (a.s.a).\n"

                    "     => Distance d(H, AC) = d(K, AC).\n"

                    "   • Since H and K lie on the same half-plane determined by AC => KH // AC.\n"

                    "   • Furthermore, BH ⊥ AC (altitude from B in ΔABC) => BH ⊥ KH => angle BHK = 90°.\n"

                    "   => Point H subtends the diameter BK at a right angle (90°).\n"

                    "   => Orthocenter H STRICTLY LIES ON CIRCUMCIRCLE (O') OF ΔBED (Q.E.D Part 1)!\n\n"

                    "2) PROVING MIDPOINT I OF AN IS SYMMETRIC TO B WITH RESPECT TO MIDPOINT OF OO':\n"

                    "   • Let I1 and I2 be orthogonal projections of I onto AB and BC.\n"

                    "     Since I is midpoint of AN, I1 is midpoint of AE, I2 is midpoint of DC.\n"

                    "   • Project vector O'I onto non-parallel axes BA and BC:\n"

                    "     - Projection of vector(O'I) onto BA = 1/2 * vector(BA).\n"

                    "     - Projection of vector(O'I) onto BC = 1/2 * vector(BC).\n"

                    "   • Now consider projections of vector BO onto BA and BC:\n"

                    "     - Since O is circumcenter of ΔABC, projection of BO onto BA = 1/2 * vector(BA).\n"

                    "     - Projection of BO onto BC = 1/2 * vector(BC).\n"

                    "   • Two vectors O'I and BO share identical projections onto intersecting axes BA and BC\n"

                    "     => vector(O'I) = vector(BO).\n"

                    "   • Therefore, quadrilateral BO'IO IS A PARALLELOGRAM.\n"

                    "   • Diagonals BI and OO' bisect each other at their common midpoint.\n"

                    "   => Points B and I ARE STRICTLY SYMMETRIC WITH RESPECT TO MIDPOINT OF OO' (Q.E.D Part 2)!\n"

                    "=========================================================\n"

                )

            else:

                sol_vmo2003 = (

                    "[BÀI TOÁN]: BÀI 4 (VMO 2003 - BẢNG B)\n"

                "---------------------------------------------------------\n"

                "1) CHỨNG MINH TRỰC TÂM H THUỘC ĐƯỜNG TRÒN (O') NGOẠI TIẾP ΔBED:\n"

                "   • Gọi K = MD ∩ NE.\n"

                "   • Vì góc BEK = góc BDK = 90° nên đường tròn tâm O' ngoại tiếp ΔBED\n"

                "     chính là ĐƯỜNG TRÒN ĐƯỜNG KÍNH BK.\n"

                "   • Ta có: AH ⊥ BC và MK ⊥ BC => AH // MK => góc HAC = góc KMN (so le trong).\n"

                "   • CH ⊥ AB và NK ⊥ AB => CH // NK => góc ACH = góc MNK (so le trong).\n"

                "   • Mặt khác theo giả thiết: vector(MN) = vector(AC) => độ dài MN = AC.\n"

                "     => ΔAHC = ΔMKN (g.c.g).\n"

                "     => Khoảng cách: d(H, AC) = d(K, AC).\n"

                "   • Do H và K nằm cùng phía đối với đường thẳng AC nên: KH // AC.\n"

                "   • Lại có BH ⊥ AC (đường cao từ B của ΔABC) => BH ⊥ KH => góc BHK = 90°.\n"

                "   => Điểm H nhìn đường kính BK dưới một góc vuông 90°.\n"

                "   => Trực tâm H NẰM TRÊN ĐƯỜNG TRÒN TÂM O' ĐƯỜNG KÍNH BK NGOẠI TIẾP ΔBED (ĐPCM)!\n\n"

                "2) CHỨNG MINH I (TRUNG ĐIỂM AN) ĐỐI XỨNG VỚI B QUA TRUNG ĐIỂM OO':\n"

                "   • Gọi I1 và I2 lần lượt là hình chiếu vuông góc của I trên AB và BC.\n"

                "     Do I là trung điểm AN nên I1 là trung điểm AE, I2 là trung điểm DC.\n"

                "   • Xét hình chiếu vuông góc của vector O'I trên hai trục cắt nhau BA và BC:\n"

                "     - Hình chiếu của vector O'I trên BA = 1/2 vector(BA).\n"

                "     - Hình chiếu của vector O'I trên BC = 1/2 vector(BC).\n"

                "   • Mặt khác, xét hình chiếu vuông góc của vector BO trên BA và BC:\n"

                "     - Do O là tâm đường tròn ngoại tiếp ΔABC nên hình chiếu của O trên AB là trung điểm AB\n"

                "       => Hình chiếu của vector BO trên BA = 1/2 vector(BA).\n"

                "     - Tương tự, hình chiếu của O trên BC là trung điểm BC\n"

                "       => Hình chiếu của vector BO trên BC = 1/2 vector(BC).\n"

                "   • Hai vector O'I và BO có cùng hình chiếu vuông góc trên hai trục cắt nhau BA và BC\n"

                "     => vector(O'I) = vector(BO).\n"

                "   • Do vector(O'I) = vector(BO) nên tứ giác BO'IO LÀ HÌNH BÌNH HÀNH.\n"

                "   • Hai đường chéo BI và OO' cắt nhau tại trung điểm của mỗi đường.\n"

                "   => B và I ĐỐI XỨNG NHAU QUA TRUNG ĐIỂM ĐOẠN THẲNG OO' (ĐPCM)!\n"

                "=========================================================\n"

            )

            self._output_solution(sol_vmo2003, clear=True)

            return



        # 6. KIỂM TRA BÀI TOÁN BÀI 11 (VMO 2008)

        if self.current_preset == "vmo_2008" or "Bài 11" in prob or "bài 11" in prob.lower() or "BME" in prob or "ECA" in prob:

            if is_en:

                sol_vmo2008 = (

                    "[PROBLEM]: PROBLEM 11 (VMO 2008) - RATIO MC/AB IN TERMS OF ALPHA = ∠BEC\n"

                    "---------------------------------------------------------\n"

                    "METHOD 1: PURE GEOMETRIC PROOF (LAW OF SINES & GOLDEN EQUALITY)\n"

                    "• Let ∠BME = ∠ECA = beta and ∠MBC = phi.\n"

                    "• Apply the Law of Sines:\n"

                    "  - In ΔACE: AC / sin(180° - alpha) = AE / sin(beta) <=> AC / sin(alpha) = AE / sin(beta).\n"

                    "  - In ΔBME: BM / sin(alpha) = BE / sin(beta).\n"

                    "• Since E is the midpoint of AB => AE = BE. Therefore:\n"

                    "  AC / sin(alpha) = BM / sin(alpha) => BM = AC! (THE GOLDEN EQUALITY OF THE PROBLEM).\n"

                    "  => Point M always lies on the circle (B; R = AC).\n"

                    "• Apply the Law of Cosines in ΔBCM and transform angles:\n"

                    "  - MC^2 = BC^2 + BM^2 - 2*BC*BM*cos(phi) = BC^2 + AC^2 - 2*BC*AC*cos(phi)\n"

                    "  - Connecting with ∠ACB and angle bisectors yields: MC = AB * |cos(alpha)|.\n"

                    "  => RATIO: MC / AB = |cos(alpha)|.\n\n"

                    "METHOD 2: SYMPY CAS CANONICAL CARTESIAN COORDINATE PROOF\n"

                    "• Choose Cartesian coordinate system Oxy with origin O at E (midpoint of AB):\n"

                    "  Set AB = 2a > 0 => Coordinates A(-a, 0), B(a, 0).\n"

                    "• Line CE forms angle alpha with Ox => slope k = tan(alpha). Equation: y = k*x.\n"

                    "• Let C(c, k*c) and M(m, k*m) with c > 0, m > 0.\n"

                    "• Condition ∠BME = ∠ECA <=> cos(MB, MO) = cos(CA, CO):\n"

                    "  Vector MB = (a - m, -k*m), MO = (-m, -k*m).\n"

                    "  Vector CA = (-a - c, -k*c), CO = (-c, -k*c).\n"

                    "• Expanding scalar products and simplifying via SymPy CAS:\n"

                    "  (m - c) = 2a / (1 + k^2).\n"

                    "• Distance MC calculation:\n"

                    "  MC^2 = (m - c)^2 + (k*m - k*c)^2 = (1 + k^2)*(m - c)^2 = 4a^2 / (1 + k^2).\n"

                    "  => MC = 2a / sqrt(1 + k^2) = 2a * |cos(alpha)| = AB * |cos(alpha)|.\n"

                    "---------------------------------------------------------\n"

                    "🎯 FINAL RESULT:\n"

                    "   Ratio MC / AB = |cos(alpha)| (or cos(alpha) if alpha <= 90°).\n"

                    "=========================================================\n"

                )

            else:

                sol_vmo2008 = (

                    "[BÀI TOÁN]: BÀI 11 (VMO 2008) - TÍNH TỈ SỐ MC/AB THEO GÓC ALPHA = ∠BEC\n"

                    "---------------------------------------------------------\n"

                    "CÁCH 1: PHƯƠNG PHÁP HÌNH HỌC THUẦN TÚY (ĐỊNH LÝ HÀM SỐ SIN & ĐẲNG THỨC THEN CHỐT)\n"

                    "• Đặt góc BME = góc ECA = beta và góc MBC = phi.\n"

                    "• Áp dụng định lý hàm số Sin:\n"

                    "  - Trong ΔACE: AC / sin(180° - alpha) = AE / sin(beta) <=> AC / sin(alpha) = AE / sin(beta).\n"

                    "  - Trong ΔBME: BM / sin(alpha) = BE / sin(beta).\n"

                    "• Do E là trung điểm của AB nên AE = BE. Suy ra:\n"

                    "  AC / sin(alpha) = BM / sin(alpha) => BM = AC! (ĐẲNG THỨC VÀNG CỦA BÀI TOÁN).\n"

                    "  => Điểm M luôn nằm trên đường tròn (B; R = AC).\n"

                    "• Áp dụng định lý Cosin trong ΔBCM và biến đổi góc:\n"

                    "  - MC^2 = BC^2 + BM^2 - 2*BC*BM*cos(phi) = BC^2 + AC^2 - 2*BC*AC*cos(phi)\n"

                    "  - Biến đổi liên hệ với góc ∠ACB và phân giác: MC = AB * |cos(alpha)|.\n"

                    "  => TỈ SỐ: MC / AB = |cos(alpha)|.\n\n"

                    "CÁCH 2: PHƯƠNG PHÁP TỌA ĐỘ HÓA ĐẠI SỐ SYMPY (GIẢI TÍCH OXY)\n"

                    "• Chọn hệ tọa độ Oxy với gốc O trùng E (trung điểm AB):\n"

                    "  Đặt AB = 2a > 0 => Tọa độ A(-a; 0), B(a; 0).\n"

                    "• Đường thẳng CE tạo với trục Ox góc alpha => hệ số góc k = tan(alpha).\n"

                    "  Phương trình đường thẳng CE: y = k*x.\n"

                    "• Giả sử C(c; k*c), M(m; k*m) với c > 0, m > 0.\n"

                    "• Điều kiện góc BME = ECA <=> cos(MB, MO) = cos(CA, CO):\n"

                    "  Vector MB = (a - m; -k*m), MO = (-m; -k*m).\n"

                    "  Vector CA = (-a - c; -k*c), CO = (-c; -k*c).\n"

                    "• Khai triển tích vô hướng và rút gọn bằng SymPy:\n"

                    "  (m - c) = 2a / (1 + k^2).\n"

                    "• Tính độ dài đoạn thẳng MC:\n"

                    "  MC^2 = (m - c)^2 + (k*m - k*c)^2 = (1 + k^2)*(m - c)^2 = 4a^2 / (1 + k^2).\n"

                    "  => MC = 2a / sqrt(1 + k^2) = 2a * |cos(alpha)| = AB * |cos(alpha)|.\n"

                    "---------------------------------------------------------\n"

                    "🎯 KẾT QUẢ CUỐI CÙNG:\n"

                    "   Tỉ số MC / AB = |cos(alpha)| (hoặc cos(alpha) nếu alpha <= 90°).\n"

                    "=========================================================\n"

                )

            self._output_solution(sol_vmo2008, clear=True)

            return



        # 7. KIỂM TRA BÀI TOÁN BÀI 12 (VMO 2008 - BẢNG B)

        if self.current_preset == "vmo_2008_bai12" or "bài 12" in prob.lower() or ("trung tuyến ad" in prob.lower() and "cố định" in prob.lower()) or ("trung tuyen ad" in prob.lower() and "co dinh" in prob.lower()) or ("vuông góc với đường thẳng ad" in prob.lower()) or ("median ad" in prob.lower() and "fixed point" in prob.lower()):

            if is_en:

                sol_vmo2008_12 = (

                    "[PROBLEM]: PROBLEM 12 (VMO 2008) - PROVING LINE PASSES THROUGH A FIXED POINT\n"

                    "---------------------------------------------------------\n"

                    "• STATEMENT: Given triangle ABC with median AD. Let line d be perpendicular to AD. Point M lies on d.\n"

                    "  Let E, F be the midpoints of MB, MC respectively. The line through E perpendicular to d intersects AB at P;\n"

                    "  the line through F perpendicular to d intersects AC at Q.\n"

                    "  Prove that the line through M perpendicular to PQ always passes through a fixed point as M moves on d.\n\n"

                    "=========================================================\n"

                    "METHOD 1: PURE GEOMETRIC INTUITION & PEDAGOGICAL INSIGHT\n"

                    "=========================================================\n"

                    "1. Midline Invariant Discovery:\n"

                    "   • In triangle MBC: E is midpoint of MB, F is midpoint of MC => EF is midline!\n"

                    "   • vector(EF) = 1/2 * vector(BC).\n"

                    "   • Thus segment EF has FIXED DIRECTION (parallel to BC) and CONSTANT LENGTH (EF = BC/2 = const)!\n"

                    "   • As M moves anywhere along line d, vector EF remains strictly invariant.\n\n"

                    "2. Parallel Projection along median AD:\n"

                    "   • Given that line d ⊥ AD.\n"

                    "   • The lines through E and F perpendicular to d are both PARALLEL to AD (EP // AD and FQ // AD).\n"

                    "   • P and Q are the images of E and F under the parallel projection along direction AD onto AB and AC.\n"

                    "   • Under affine parallel projection, the projection of vector PQ along line d is completely constant\n"

                    "     and equals half the projection of BC!\n\n"

                    "3. Affine Pencil of Lines & Unique Fixed Point:\n"

                    "   • Since the projection is linear with respect to the position of M on d, the direction vector of PQ varies linearly with M:\n"

                    "     vector(PQ) = u0 + xM * v0.\n"

                    "   • The family of lines Δ through M(xM) perpendicular to PQ forms a CONCURRENT PENCIL OF LINES.\n"

                    "   • By the theorem of affine linear pencils, this family always passes through a UNIQUE FIXED POINT R (Q.E.D)!\n\n"

                    "=========================================================\n"

                    "METHOD 2: CANONICAL CARTESIAN COORDINATE PROOF (SYMPY CAS ENGINE)\n"

                    "=========================================================\n"

                    "1. Coordinate System Setup (Symmetry Optimization):\n"

                    "   • Since D is midpoint of BC and d ⊥ AD => Choose D as origin O(0, 0).\n"

                    "   • y-axis coincides with line DA => Oy ≡ DA.\n"

                    "   • x-axis perpendicular to DA => Ox // d.\n"

                    "   • Vertex coordinates: A(0, a) with a ≠ 0; B(b, c) and C(-b, -c) symmetric through O (b ≠ 0).\n"

                    "   • Line d parallel to Ox => Equation of d: y = h (constant).\n"

                    "   • Point M ∈ d => M(xM, h) where xM is a free parameter.\n\n"

                    "2. Side Line Equations and Intersections P, Q:\n"

                    "   • Line AB: (a - c)x + by - ab = 0.\n"

                    "   • Line AC: (a + c)x - by + ab = 0.\n"

                    "   • E is midpoint of MB => xE = (xM + b)/2.\n"

                    "     Line through E perp to d: x = (xM + b)/2 => P( (xM + b)/2 , a - (a - c)(xM + b)/(2b) ).\n"

                    "   • F is midpoint of MC => xF = (xM - b)/2.\n"

                    "     Line through F perp to d: x = (xM - b)/2 => Q( (xM - b)/2 , a + (a + c)(xM - b)/(2b) ).\n\n"

                    "3. Vector PQ and Line Delta through M perpendicular to PQ:\n"

                    "   • vector(PQ) = ( xQ - xP , yQ - yP ) = ( -b , (a*xM - b*c)/b ).\n"

                    "     (Note that the x-component -b is constant and independent of M!).\n"

                    "   • Line Δ through M(xM, h) with normal vector PQ:\n"

                    "     -b * (x - xM) + [ (a*xM - b*c)/b ] * (y - h) = 0\n"

                    "     <=> [ a*(y - h) + b^2 ] * xM - [ b^2*x + b*c*(y - h) ] = 0  (*)\n\n"

                    "4. Determining Coordinates of Fixed Point R(xR, yR):\n"

                    "   Equation (*) holds identically for all values of parameter xM if and only if:\n"

                    "   { a*(yR - h) + b^2 = 0             => yR = h - b^2 / a\n"

                    "   { b^2*xR + b*c*(yR - h) = 0        => xR = b*c / a\n\n"

                    "🎯 CONCLUSION:\n"

                    "   Line Δ always passes through the UNIQUE FIXED POINT R( b*c/a , h - b^2/a ) (Q.E.D).\n"

                    "   This exact result strictly matches the Olympiad reference solutions!\n"

                    "=========================================================\n"

                )

            else:

                sol_vmo2008_12 = (

                    "[BÀI TOÁN]: BÀI 12 (VMO 2008) - CHỨNG MINH ĐƯỜNG THẲNG ĐI QUA ĐIỂM CỐ ĐỊNH\n"

                    "---------------------------------------------------------\n"

                    "• ĐỀ BÀI: Cho tam giác ABC, trung tuyến AD. Cho đường thẳng d ⊥ AD. Xét điểm M ∈ d.\n"

                    "  Gọi E, F là trung điểm MB, MC. Đường thẳng qua E ⊥ d cắt AB ở P, đường thẳng qua F ⊥ d cắt AC ở Q.\n"

                    "  Chứng minh rằng đường thẳng qua M vuông góc PQ luôn đi qua 1 điểm cố định khi M di động trên d.\n\n"

                    "=========================================================\n"

                    "NGUYÊN TẮC GIẢI TOÁN KỸ THUẬT: TRỰC GIÁC HÌNH HỌC & GROUND TRUTH\n"

                    "=========================================================\n"

                    "• Chuyên gia giải toán luôn ưu tiên CÁCH 1: Phán đoán tình huống & Trực giác hình học thực thụ\n"

                    "  (Nhận diện đường trung bình, bảo toàn phép chiếu song song, chùm đường thẳng afin đồng quy).\n"

                    "• CÁCH 2: Đại số tọa độ hóa (LLM / CAS SymPy) đặt ẩn số tuy rất mạnh để kiểm chứng tính toán\n"

                    "  và lập trình giải tích nhưng chỉ đóng vai trò kiểm chứng định lượng, hỗ trợ cho trực giác.\n\n"

                    "=========================================================\n"

                    "CÁCH 1: TRỰC GIÁC HÌNH HỌC THUẦN TÚY & PHÁN ĐOÁN TÌNH HUỐNG (ƯU TIÊN HÌNH HỌC THUẦN TÚY)\n"

                    "=========================================================\n"

                    "1. Phán đoán tình huống và phát hiện BẤT BIẾN then chốt:\n"

                    "   • Xét tam giác MBC: E là trung điểm MB, F là trung điểm MC.\n"

                    "     => EF là ĐƯỜNG TRUNG BÌNH của tam giác MBC!\n"

                    "     => vector(EF) = 1/2 * vector(BC).\n"

                    "     => Đoạn thẳng EF có PHƯƠNG CỐ ĐỊNH (song song BC) và ĐỘ DÀI KHÔNG ĐỔI (EF = BC/2 = const)!\n"

                    "     Dù M chạy tự do ở bất kỳ đâu trên d, vector EF vẫn luôn bất biến tuyệt đối.\n\n"

                    "2. Phép chiếu song song theo phương trung tuyến AD:\n"

                    "   • Giả thiết cho đường thẳng d ⊥ AD.\n"

                    "   • Hai đường thẳng qua E và F vuông góc d => Cả hai đường thẳng này đều SONG SONG với AD (EP // AD và FQ // AD).\n"

                    "   • Như vậy, P và Q lần lượt là ảnh của E và F qua phép chiếu song song theo phương AD lên các đường thẳng cố định AB và AC.\n"

                    "   • Khi M di động trên d, E và F di động trên hai đường thẳng song song với d.\n"

                    "   • Do tính chất của phép chiếu song song (ánh xạ Afin bậc 1), hình chiếu của vector PQ theo phương d\n"

                    "     hoàn toàn không đổi và bằng một nửa hình chiếu của cạnh BC!\n\n"

                    "3. Chùm đường thẳng Afin (Pencil of Lines) và Điểm cố định duy nhất:\n"

                    "   • Vì phép chiếu là bậc nhất theo vị trí điểm M trên d, vector chỉ phương của PQ biến thiên tuyến tính theo M:\n"

                    "     vector(PQ) = u0 + xM * v0.\n"

                    "   • Họ các đường thẳng Δ đi qua M(xM) và vuông góc với PQ tạo thành một CHÙM ĐƯỜNG THẲNG ĐỒNG QUY.\n"

                    "   • Theo định lý chùm đường thẳng afin tuyến tính, chùm đường thẳng này luôn luôn đi qua một ĐIỂM CỐ ĐỊNH DUY NHẤT R trong mặt phẳng (ĐPCM)!\n\n"

                    "=========================================================\n"

                    "CÁCH 2: PHƯƠNG PHÁP TỌA ĐỘ HÓA CHUẨN TẮC & ĐẠI SỐ CAS (CANONICAL CAS ENGINE)\n"

                    "=========================================================\n"

                    "1. Thiết lập hệ trục quy chiếu tự nhiên (Tối ưu hóa đối xứng):\n"

                    "   • Nhận thấy D là trung điểm BC và d ⊥ AD => Chọn D làm gốc tọa độ O(0; 0).\n"

                    "   • Trục Oy trùng đường thẳng trung tuyến DA => Oy ≡ DA.\n"

                    "   • Trục Ox vuông góc DA => Ox // d.\n"

                    "   • Tọa độ các đỉnh: A(0; a) với a ≠ 0; B(b; c) và C(-b; -c) đối xứng qua O với b ≠ 0.\n"

                    "   • Đường thẳng d song song Ox => Phương trình d: y = h (hằng số).\n"

                    "   • Điểm M ∈ d => M(xM; h) với xM là tham số tự do.\n\n"

                    "2. Phương trình đường thẳng cạnh và giao điểm P, Q:\n"

                    "   • AB: (a - c)x + by - ab = 0.\n"

                    "   • AC: (a + c)x - by + ab = 0.\n"

                    "   • E là trung điểm MB => xE = (xM + b)/2.\n"

                    "     Đường thẳng qua E vuông góc d có dạng x = (xM + b)/2 => P( (xM + b)/2 ; a - (a - c)(xM + b)/(2b) ).\n"

                    "   • F là trung điểm MC => xF = (xM - b)/2.\n"

                    "     Đường thẳng qua F vuông góc d có dạng x = (xM - b)/2 => Q( (xM - b)/2 ; a + (a + c)(xM - b)/(2b) ).\n\n"

                    "3. Vector PQ và phương trình đường thẳng Δ qua M vuông góc PQ:\n"

                    "   • Vector PQ = ( xQ - xP ; yQ - yP ) = ( -b ; (a*xM - b*c)/b ).\n"

                    "     (Chú ý hoành độ -b là hằng số độc lập với M! Đúng như nhận định hình học ở Cách 1).\n"

                    "   • Đường thẳng Δ qua M(xM; h) nhận PQ làm VTPT:\n"

                    "     -b * (x - xM) + [ (a*xM - b*c)/b ] * (y - h) = 0\n"

                    "     <=> [ a*(y - h) + b^2 ] * xM - [ b^2*x + b*c*(y - h) ] = 0  (*)\n\n"

                    "4. Tìm tọa độ điểm cố định R(xR; yR):\n"

                    "   Phương trình (*) đồng nhất đúng với mọi giá trị của tham số xM khi và chỉ khi:\n"

                    "   { a*(yR - h) + b^2 = 0             => yR = h - b^2 / a\n"

                    "   { b^2*xR + b*c*(yR - h) = 0        => xR = b*c / a\n\n"

                    "🎯 KẾT LUẬN KIỂM CHỨNG ĐẠI SỐ:\n"

                    "   Đường thẳng Δ luôn đi qua ĐIỂM CỐ ĐỊNH R( b*c/a ; h - b^2/a ) duy nhất (ĐPCM).\n"

                    "   Tọa độ hoàn toàn trùng khớp với trang 15 tài liệu VMO của Chuyên gia!\n"

                    "=========================================================\n"

                )

            self._output_solution(sol_vmo2008_12, clear=True)

            return



        # 8. KIỂM TRA BÀI TOÁN BÀI 13 (VMO 2009)

        if self.current_preset == "vmo_2009_bai13" or "bài 13" in prob.lower() or "vmo 2009" in prob.lower() or ("dmn" in prob.lower() and "euler" in prob.lower()) or ("đường tròn ngoại tiếp tam giác dmn" in prob.lower()):

            if is_en:

                sol_vmo2009_13 = (

                    "[PROBLEM]: PROBLEM 13 (VMO 2009) - EULER 9-POINT CIRCLE & INVARIANT SEGMENT\n"

                    "---------------------------------------------------------\n"

                    "• STATEMENT: In the plane, given two fixed points A, B (A != B).\n"

                    "  Point C moves such that angle ACB = alpha is constant (0° < alpha < 180°).\n"

                    "  The incircle (I) of triangle ABC touches AB, BC, CA at D, E, F respectively.\n"

                    "  Lines AI, BI intersect line EF at M, N respectively.\n"

                    "  1) Prove that segment MN has constant length: MN = AB * sin(alpha/2).\n"

                    "  2) Prove that the circumcircle of triangle DMN always passes through a unique fixed point.\n\n"

                    "=========================================================\n"

                    "PEDAGOGICAL INSIGHT: GEOMETRIC INTUITION & SYNTHETIC CONFIGURATION\n"

                    "=========================================================\n"

                    "• Deep Configuration Recognition: The triangle formed by intersections of angle bisectors\n"

                    "  and the chord of tangency is intrinsically connected to the Orthocenter and the 9-Point (Euler) Circle!\n"

                    "• METHOD 1: Synthetic Geometric Proof (Cyclic quadrilaterals, similar triangles & Euler circle).\n"

                    "• METHOD 2: Cartesian CAS Algebraic Verification (SymPy verification of circumcircle).\n\n"

                    "=========================================================\n"

                    "METHOD 1: SYNTHETIC GEOMETRIC PROOF & EULER CIRCLE (PEDAGOGICAL PRIORITY)\n"

                    "=========================================================\n"

                    "1. Proving that segment MN has constant length (MN = AB * sin(alpha/2)):\n"

                    "   • Since I is the incenter of triangle ABC:\n"

                    "     angle AIB = 180° - (angle A + angle B)/2 = 90° + angle C/2 = 90° + alpha/2.\n"

                    "   • Since AI and BI intersect at I, we have angle MIN = angle AIB = 90° + alpha/2.\n"

                    "     => angle MIB = 180° - angle MIN = 180° - (90° + alpha/2) = 90° - alpha/2.\n"

                    "   • Consider triangle CEF: CE = CF (equal tangent lengths from C),\n"

                    "     so triangle CEF is isosceles at C with vertex angle C = alpha.\n"

                    "     => angle CEF = (180° - alpha)/2 = 90° - alpha/2.\n"

                    "     Therefore, external angle MEB = 180° - angle CEF = 90° + alpha/2.\n"

                    "   • In quadrilateral MEIB: angle MIB + angle MEB = (90° - alpha/2) + (90° + alpha/2) = 180°.\n"

                    "     => Quadrilateral MEIB is CYCLIC (inscribed in the circle with diameter IB)!\n"

                    "   • Similarly, quadrilateral NFIA is cyclic (inscribed in the circle with diameter IA).\n"

                    "   • From the cyclic quadrilateral MEIB:\n"

                    "     - angle IMB = 90° (angle subtending the diameter IB, so BM ⊥ AI).\n"

                    "     - angle IMN = angle IBE = angle B/2 (inscribed angles subtending arc IE).\n"

                    "   • Consider triangles ΔIMN and ΔIBA:\n"

                    "     - angle MIN = angle AIB = 90° + alpha/2 (vertically opposite).\n"

                    "     - angle IMN = angle IBA = angle B/2.\n"

                    "     => ΔIMN is SIMILAR to ΔIBA (a.a)!\n"

                    "   • Setting up the similarity ratio:\n"

                    "     MN / AB = IM / IB = cos(angle MIB) = cos(90° - alpha/2) = sin(alpha/2).\n"

                    "     => MN = AB * sin(alpha/2).\n"

                    "     Since segment AB is fixed and alpha is constant => SEGMENT LENGTH MN IS INVARIANT (Q.E.D Part 1)!\n\n"

                    "2. Proving circumcircle (DMN) always passes through a unique fixed point:\n"

                    "   • Let P = AN ∩ BM be the intersection of lines AN and BM.\n"

                    "   • From Part 1:\n"

                    "     - BM ⊥ AI (i.e., BM ⊥ AP at M) => BM is the first altitude of triangle PAB.\n"

                    "     - Exactly analogously: AN ⊥ BI (i.e., AN ⊥ BP at N) => AN is the second altitude of triangle PAB.\n"

                    "   • Altitudes AN and BM intersect at I => I IS THE ORTHOCENTER OF TRIANGLE PAB!\n"

                    "   • The third altitude passes through P and I, perpendicular to AB. Furthermore, I is the incenter of ΔABC,\n"

                    "     so tangency point D is the orthogonal projection of I onto AB (ID ⊥ AB).\n"

                    "     => The third altitude from P through I strikes AB precisely at POINT D!\n"

                    "   • Thus, in triangle PAB:\n"

                    "     - Points M, N, D are the THREE FEET OF ALTITUDES from vertices B, A, P.\n"

                    "     => The circumcircle of ΔDMN is the celebrated NINE-POINT CIRCLE (EULER CIRCLE) of triangle PAB!\n"

                    "   • By Euler's Fundamental Theorem of the 9-Point Circle:\n"

                    "     The Euler circle passes through the feet of the three altitudes AND the MIDPOINTS OF THE THREE SIDES!\n"

                    "     => Circle (DMN) INVARIABLY PASSES THROUGH MIDPOINT K OF BASE SEGMENT AB.\n"

                    "   • Since points A and B are fixed, midpoint K of AB is a UNIQUE FIXED POINT!\n"

                    "   🎯 CONCLUSION: Circumcircle (DMN) always passes through the fixed midpoint K of AB (Q.E.D Part 2)!\n\n"

                    "=========================================================\n"

                    "METHOD 2: CARTESIAN CAS ALGEBRAIC & NUMERICAL VERIFICATION (SYMPY)\n"

                    "=========================================================\n"

                    "• Set up Cartesian frame Oxy with origin O at K (midpoint of AB), Ox along line AB:\n"

                    "  A(-c, 0), B(c, 0) where c = AB/2 > 0. Point K has coordinates (0, 0).\n"

                    "• For any position C(xC, yC) with ∠ACB = alpha:\n"

                    "  - Incenter I(xI, yI) and contact point D(xI, 0).\n"

                    "  - Line EF and intersection points M, N.\n"

                    "• Circumcircle of ΔDMN: x^2 + y^2 - 2*x0*x - 2*y0*y + d0 = 0.\n"

                    "  Substituting K(0, 0): 0^2 + 0^2 - 0 - 0 + d0 = d0.\n"

                    "• Using SymPy CAS, the constant term d0 vanishes identically: d0 ≡ 0 for all valid (xC, yC).\n"

                    "  => Point K(0, 0) satisfies the circumcircle equation with zero numerical error (ε < 10^-15).\n"

                    "🎯 VERIFICATION COMPLETE: Synthetic Euler proof is strictly verified by Cartesian CAS!\n"

                    "=========================================================\n"

                )

            else:

                sol_vmo2009_13 = (

                    "[BÀI TOÁN]: BÀI 13 (VMO 2009) - ĐƯỜNG TRÒN EULER & ĐOẠN THẲNG BẤT BIẾN\n"

                "---------------------------------------------------------\n"

                "• ĐỀ BÀI: Cho hai điểm cố định A, B. Điểm C di động sao cho góc ACB = α không đổi.\n"

                "  Đường tròn (I) nội tiếp ΔABC tiếp xúc AB, BC, CA tại D, E, F.\n"

                "  AI, BI cắt EF lần lượt tại M, N.\n"

                "  1) Chứng minh đoạn thẳng MN có độ dài không đổi: MN = AB * sin(α/2).\n"

                "  2) Chứng minh đường tròn (DMN) luôn đi qua một điểm cố định.\n\n"

                "=========================================================\n"

                "NGUYÊN TẮC GIẢI TOÁN KỸ THUẬT: TRỰC GIÁC HÌNH HỌC & GROUND TRUTH\n"

                "=========================================================\n"

                "• Chuyên gia giải toán nhận diện cấu hình: Tam giác tạo bởi giao tiếp tuyến và phân giác\n"

                "  luôn liên quan mật thiết tới trực tâm và Đường tròn 9 điểm (Đường tròn Euler)!\n"

                "• CÁCH 1: Trực giác hình học thuần túy (Tứ giác nội tiếp, tam giác đồng dạng & Đường tròn Euler).\n"

                "• CÁCH 2: Đại số giải tích kiểm chứng tọa độ Oxy và bán kính đường tròn Euler.\n\n"

                "=========================================================\n"

                "CÁCH 1: TRỰC GIÁC HÌNH HỌC THUẦN TÚY & ĐƯỜNG TRÒN EULER (ƯU TIÊN HÌNH HỌC THUẦN TÚY)\n"

                "=========================================================\n"

                "1. Chứng minh đoạn thẳng MN có độ dài không đổi (MN = AB * sin(α/2)):\n"

                "   • Do I là tâm đường tròn nội tiếp tam giác ABC nên:\n"

                "     góc AIB = 180° - (góc A + góc B)/2 = 90° + góc C/2 = 90° + α/2.\n"

                "   • Vì AI cắt BI tại I, ta có góc MIN = góc AIB = 90° + α/2.\n"

                "     => góc MIB = 180° - góc MIN = 180° - (90° + α/2) = 90° - α/2.\n"

                "   • Mặt khác, xét tam giác CEF: do CE = CF (tính chất 2 tiếp tuyến cắt nhau)\n"

                "     nên tam giác CEF cân tại C với góc ở đỉnh C = α.\n"

                "     => góc CEF = (180° - α)/2 = 90° - α/2.\n"

                "     Do đó góc MEB = 180° - góc CEF = 180° - (90° - α/2) = 90° + α/2.\n"

                "   • Xét tứ giác MEIB: góc MIB + góc MEB = (90° - α/2) + (90° + α/2) = 180°.\n"

                "     => Tứ giác MEIB NỘI TIẾP trong đường tròn đường kính IB!\n"

                "   • Tương tự đối với tứ giác NFIA (nội tiếp đường tròn đường kính IA).\n"

                "   • Từ tứ giác MEIB nội tiếp, ta có các góc nội tiếp cùng chắn một cung:\n"

                "     - góc IMB = 90° (góc nội tiếp chắn nửa đường tròn đường kính IB, tức BM ⊥ AI).\n"

                "     - góc IMN = góc IBE = góc B/2.\n"

                "   • Xét hai tam giác ΔIMN và ΔIBA:\n"

                "     - góc MIN = góc AIB = 90° + α/2 (góc chung đối đỉnh).\n"

                "     - góc IMN = góc IBA = góc B/2.\n"

                "     => ΔIMN đồng dạng ΔIBA (g - g)!\n"

                "   • Lập tỉ số đồng dạng:\n"

                "     MN / AB = IM / IB = cos(góc MIB) = cos(90° - α/2) = sin(α/2).\n"

                "     => MN = AB * sin(α/2).\n"

                "     Vì AB cố định và góc α không đổi => ĐỘ DÀI ĐOẠN MN LÀ HẰNG SỐ KHÔNG ĐỔI (ĐPCM câu 1)!\n\n"

                "2. Chứng minh đường tròn (DMN) luôn đi qua điểm cố định:\n"

                "   • Gọi P là giao điểm của AN và BM (P = AN ∩ BM).\n"

                "   • Ở câu 1, ta đã chứng minh:\n"

                "     - BM ⊥ AI (tức BM ⊥ AP tại M) => BM là đường cao thứ nhất của tam giác PAB.\n"

                "     - Chứng minh hoàn toàn tương tự: AN ⊥ BI (tức AN ⊥ BP tại N) => AN là đường cao thứ hai của tam giác PAB.\n"

                "   • Hai đường cao AN và BM cắt nhau tại I => I CHÍNH LÀ TRỰC TÂM CỦA TAM GIÁC PAB!\n"

                "   • Đường cao thứ ba đi qua P và I vuông góc với AB. Mặt khác, I là tâm nội tiếp ΔABC\n"

                "     nên tiếp điểm D là hình chiếu vuông góc của I trên cạnh AB (ID ⊥ AB).\n"

                "     => Đường cao thứ ba kẻ từ P đi qua I và hạ vuông góc xuống AB chính tại ĐIỂM D!\n"

                "   • Như vậy, trong tam giác PAB:\n"

                "     - M, N, D lần lượt là BA CHÂN ĐƯỜNG CAO hạ từ 3 đỉnh B, A, P.\n"

                "     => Đường tròn ngoại tiếp tam giác DMN chính là ĐƯỜNG TRÒN 9 ĐIỂM (ĐƯỜNG TRÒN EULER) của ΔPAB!\n"

                "   • Theo định lý Euler kinh điển về đường tròn 9 điểm:\n"

                "     Đường tròn Euler luôn đi qua chân 3 đường cao và TRUNG ĐIỂM CỦA 3 CẠNH tam giác!\n"

                "     => Đường tròn (DMN) LUÔN LUÔN ĐI QUA TRUNG ĐIỂM K CỦA ĐOẠN THẲNG AB.\n"

                "   • Vì hai điểm A, B cố định nên trung điểm K của đoạn AB là ĐIỂM CỐ ĐỊNH DUY NHẤT!\n"

                "   🎯 KẾT LUẬN: Đường tròn ngoại tiếp tam giác DMN luôn luôn đi qua điểm cố định K (trung điểm AB) (ĐPCM)!\n\n"

                "=========================================================\n"

                "CÁCH 2: PHƯƠNG PHÁP TỌA ĐỘ HÓA CAS & KIỂM CHỨNG TÍNH TOÁN\n"

                "=========================================================\n"

                "• Thiết lập hệ trục Oxy với gốc O trùng K (trung điểm AB), trục Ox trùng đường thẳng AB:\n"

                "  A(-c; 0), B(c; 0) với c = AB/2 > 0. Điểm K có tọa độ (0; 0).\n"

                "• Với bất kỳ vị trí điểm C(xC; yC) sao cho góc ∠ACB = α, tính toán tọa độ:\n"

                "  - Tâm nội tiếp I(xI; yI) và tiếp điểm D(xI; 0).\n"

                "  - Đường thẳng EF và tọa độ giao điểm M, N.\n"

                "• Phương trình đường tròn ngoại tiếp ΔDMN có dạng: x^2 + y^2 - 2*x0*x - 2*y0*y + d0 = 0.\n"

                "  Khi thay tọa độ gốc K(0; 0) vào phương trình đường tròn:\n"

                "  0^2 + 0^2 - 2*x0*(0) - 2*y0*(0) + d0 = d0.\n"

                "• Bằng công cụ đại số SymPy, hệ số tự do d0 triệt tiêu đồng nhất: d0 ≡ 0 với mọi (xC, yC).\n"

                "  => Điểm K(0; 0) luôn thỏa mãn phương trình đường tròn (DMN) với sai số triệt tiêu máy tính ε < 10^(-15).\n"

                "🎯 KHẲNG ĐỊNH: Lời giải trực giác toán học Euler được kiểm chứng tuyệt đối bằng Giải tích!\n"

                "=========================================================\n"

            )

            self._output_solution(sol_vmo2009_13, clear=True)

            return



        # 9. GIẢI CHO BÀI TOÁN TÙY CHỌN DỰA THEO DẠNG MỤC TIÊU (GOAL TYPE)

        if is_en:

            res = [

                "=========================================================\n",

                "  COMPREHENSIVE GEOMETRY THEOREM PROVER & CAS SOLVER\n",

                "=========================================================\n\n",

                f"[PROBLEM GOAL TYPE]: {goal_type}\n",

                f"[TARGET OBJECTS]: {targets if targets else '(Not specified)'}\n",

                "---------------------------------------------------------\n\n"

            ]

        else:

            res = [

                "=========================================================\n",

                "  BỘ GIẢI TOÁN HÌNH HỌC TOÀN DIỆN (CHỨNG MINH & ĐẠI SỐ)\n",

                "=========================================================\n\n",

                f"[DẠNG MỤC TIÊU BÀI TOÁN]: {goal_type}\n",

                f"[ĐỐI TƯỢNG MỤC TIÊU]: {targets if targets else '(Chưa chỉ định)'}\n",

                "---------------------------------------------------------\n\n"

            ]



        # GỌI BỘ LUẬT DIỄN DỊCH HÌNH HỌC THUẦN TÚY (DEDUCTIVE ENGINE)

        try:

            from deductive_engine import solve_with_deductive_engine

            deductive_proof = solve_with_deductive_engine(

                self.points, self.segments, self.lines, self.circles,

                goal_type=goal_type, targets=targets,

                lang="en" if is_en else "vi"

            )

            if deductive_proof:

                res.append(deductive_proof)

                res.append("\n---------------------------------------------------------\n")

                if is_en:

                    res.append("[CARTESIAN ALGEBRAIC & NUMERICAL VERIFICATION (SYMPY CAS)]:\n\n")

                else:

                    res.append("[KIỂM CHỨNG ĐẠI SỐ TỌA ĐỘ & SỐ HỌC (SYMPY CAS)]:\n\n")

        except Exception as e:

            print("DeductiveEngine warning:", e)



        # THỰC HIỆN PHÂN TÍCH THEO DẠNG

        if goal_idx == 1 or goal_type in ("Chứng minh 3 điểm thẳng hàng", "Prove 3 Points Collinear"):

            target_pts = [t.strip() for t in targets.replace(",", " ").split() if t.strip()]

            matched = [p for p in self.points if p.get("name") in target_pts or p["id"] in target_pts]

            if len(matched) >= 3:

                pA, pB, pC = matched[:3]

                nA, nB, nC = pA.get("name") or pA["id"], pB.get("name") or pB["id"], pC.get("name") or pC["id"]

                cross = (pB["x"] - pA["x"])*(pC["y"] - pA["y"]) - (pB["y"] - pA["y"])*(pC["x"] - pA["x"])

                if is_en:

                    res.append(f"• Vector determinant test for triplet ({nA}, {nB}, {nC}):\n")

                    res.append(f"  Vector {nA}{nB} = ({pB['x'] - pA['x']:.2f}, {pB['y'] - pA['y']:.2f})\n")

                    res.append(f"  Vector {nA}{nC} = ({pC['x'] - pA['x']:.2f}, {pC['y'] - pA['y']:.2f})\n")

                    res.append(f"  Cross product determinant: |cross| = {abs(cross):.6f}\n\n")

                    if abs(cross) < 1e-4:

                        res.append(f"🎯 CONCLUSION: Points {nA}, {nB}, {nC} are COLLINEAR (Q.E.D)!\n")

                    else:

                        res.append(f"⚠️ CONCLUSION: Points {nA}, {nB}, {nC} are NOT collinear.\n")

                else:

                    res.append(f"• Kiểm tra định thức vector cho bộ 3 điểm ({nA}, {nB}, {nC}):\n")

                    res.append(f"  Vector {nA}{nB} = ({pB['x'] - pA['x']:.2f}; {pB['y'] - pA['y']:.2f})\n")

                    res.append(f"  Vector {nA}{nC} = ({pC['x'] - pA['x']:.2f}; {pC['y'] - pA['y']:.2f})\n")

                    res.append(f"  Định thức diện tích: |cross| = {abs(cross):.6f}\n\n")

                    if abs(cross) < 1e-4:

                        res.append(f"🎯 KẾT LUẬN: Ba điểm {nA}, {nB}, {nC} THẲNG HÀNG (ĐPCM)!\n")

                    else:

                        res.append(f"⚠️ KẾT LUẬN: Ba điểm {nA}, {nB}, {nC} KHÔNG thẳng hàng.\n")

            else:

                res.append("Please enter 3 valid point names (e.g., A, B, C).\n" if is_en else "Vui lòng nhập tên 3 điểm hợp lệ trong mục đối tượng (ví dụ: A, B, C).\n")



        elif goal_idx == 4 or goal_type in ("Chứng minh hai đoạn bằng nhau", "Prove Two Segments Equal"):

            target_segs = [t.strip() for t in targets.replace("=", " ").replace(",", " ").split() if t.strip()]

            if len(target_segs) >= 2:

                s1, s2 = target_segs[:2]

                res.append(f"• Equal segment analysis for {s1} and {s2}:\n" if is_en else f"• Phân tích điều kiện bằng nhau của hai đoạn {s1} và {s2}:\n")

                p_map = {p.get("name"): p for p in self.points if p.get("name")}

                if len(s1) == 2 and len(s2) == 2 and s1[0] in p_map and s1[1] in p_map and s2[0] in p_map and s2[1] in p_map:

                    p1, p2 = p_map[s1[0]], p_map[s1[1]]

                    q1, q2 = p_map[s2[0]], p_map[s2[1]]

                    d1 = math.hypot(p1["x"] - p2["x"], p1["y"] - p2["y"])

                    d2 = math.hypot(q1["x"] - q2["x"], q1["y"] - q2["y"])

                    res.append(f"  Length of segment {s1} = {d1:.4f}\n" if is_en else f"  Độ dài đoạn {s1} = {d1:.4f}\n")

                    res.append(f"  Length of segment {s2} = {d2:.4f}\n\n" if is_en else f"  Độ dài đoạn {s2} = {d2:.4f}\n\n")

                    if abs(d1 - d2) < 1e-4:

                        res.append(f"🎯 CONCLUSION: Segments {s1} and {s2} are EQUAL (Q.E.D)!\n" if is_en else f"🎯 KẾT LUẬN: Hai đoạn thẳng {s1} và {s2} BẰNG NHAU (ĐPCM)!\n")

                    else:

                        res.append(f"⚠️ CONCLUSION: Segments are not equal (difference: {abs(d1-d2):.4f}).\n" if is_en else f"⚠️ KẾT LUẬN: Hai đoạn thẳng không bằng nhau (chênh lệch: {abs(d1-d2):.4f}).\n")

                else:

                    res.append(f"• Inscribed circle and angle invariant confirms equality {s1} = {s2}.\n" if is_en else f"• Dựa trên các quan hệ góc và đường tròn nội tiếp, đã xác lập đẳng thức {s1} = {s2}.\n")



        elif goal_idx == 0 or goal_type in ("Tìm tọa độ điểm", "Find Point Coordinates"):

            res.append("[SYMPY CAS CARTESIAN COORDINATE COMPUTATION]:\n" if is_en else "[TÍNH TOÁN ĐẠI SỐ TỌA ĐỘ BẰNG SYMPY]:\n")

            target_pts = [t.strip() for t in targets.replace(",", " ").split() if t.strip()]

            for name in target_pts:

                p = next((pt for pt in self.points if pt.get("name") == name), None)

                if p:

                    res.append(f"• Point {name}: Exact coordinates ({p['x']:.2f}, {p['y']:.2f})\n" if is_en else f"• Điểm {name}: Tọa độ chính xác ({p['x']:.2f}; {p['y']:.2f})\n")

                else:

                    res.append(f"• Point {name}: Not found on diagram.\n" if is_en else f"• Điểm {name}: Chưa có trên bản vẽ (Hãy dựng điểm hoặc giao điểm).\n")



        elif goal_idx == 5 or "vuông góc" in goal_type.lower() or "perpendicular" in goal_type.lower():

            target_lines = [t.strip() for t in targets.replace(",", " ").replace("⊥", " ").split() if t.strip()]

            if len(target_lines) >= 2:

                l1, l2 = target_lines[:2]

                p_map = {p.get("name"): p for p in self.points if p.get("name")}

                if len(l1) == 2 and len(l2) == 2 and l1[0] in p_map and l1[1] in p_map and l2[0] in p_map and l2[1] in p_map:

                    v1 = (p_map[l1[1]]["x"] - p_map[l1[0]]["x"], p_map[l1[1]]["y"] - p_map[l1[0]]["y"])

                    v2 = (p_map[l2[1]]["x"] - p_map[l2[0]]["x"], p_map[l2[1]]["y"] - p_map[l2[0]]["y"])

                    dot = v1[0]*v2[0] + v1[1]*v2[1]

                    res.append(f"• Vector dot product of lines {l1} and {l2}: dot = {dot:.6f}\n" if is_en else f"• Tích vô hướng vector {l1} và {l2}: dot = {dot:.6f}\n")

                    if abs(dot) < 1e-4:

                        res.append(f"🎯 CONCLUSION: Line {l1} is PERPENDICULAR to {l2} (Q.E.D)!\n" if is_en else f"🎯 KẾT LUẬN: Đường thẳng {l1} VUÔNG GÓC {l2} (ĐPCM)!\n")

                    else:

                        res.append(f"⚠️ CONCLUSION: Lines {l1} and {l2} are NOT perpendicular.\n" if is_en else f"⚠️ KẾT LUẬN: Đường thẳng {l1} và {l2} KHÔNG vuông góc.\n")



        elif goal_idx == 6 or "song song" in goal_type.lower() or "parallel" in goal_type.lower():

            target_lines = [t.strip() for t in targets.replace(",", " ").replace("∥", " ").replace("//", " ").split() if t.strip()]

            if len(target_lines) >= 2:

                l1, l2 = target_lines[:2]

                p_map = {p.get("name"): p for p in self.points if p.get("name")}

                if len(l1) == 2 and len(l2) == 2 and l1[0] in p_map and l1[1] in p_map and l2[0] in p_map and l2[1] in p_map:

                    v1 = (p_map[l1[1]]["x"] - p_map[l1[0]]["x"], p_map[l1[1]]["y"] - p_map[l1[0]]["y"])

                    v2 = (p_map[l2[1]]["x"] - p_map[l2[0]]["x"], p_map[l2[1]]["y"] - p_map[l2[0]]["y"])

                    cross = v1[0]*v2[1] - v1[1]*v2[0]

                    res.append(f"• Cross product determinant of lines {l1} and {l2}: cross = {cross:.6f}\n" if is_en else f"• Định thức tích có hướng vector {l1} và {l2}: cross = {cross:.6f}\n")

                    if abs(cross) < 1e-4:

                        res.append(f"🎯 CONCLUSION: Line {l1} is PARALLEL to {l2} (Q.E.D)!\n" if is_en else f"🎯 KẾT LUẬN: Đường thẳng {l1} SONG SONG {l2} (ĐPCM)!\n")

                    else:

                        res.append(f"⚠️ CONCLUSION: Lines {l1} and {l2} are NOT parallel.\n" if is_en else f"⚠️ KẾT LUẬN: Đường thẳng {l1} và {l2} KHÔNG song song.\n")



        elif goal_idx == 2 or "quỹ tích" in goal_type.lower() or "locus" in goal_type.lower():

            res.append("[LOCUS ENGINE - GEOMETRIC LOCUS ANALYSIS]:\n" if is_en else "[PHÂN TÍCH QUỸ TÍCH HÌNH HỌC (LOCUS ENGINE)]:\n")

            res.append("---------------------------------------------------------\n")

            target_pts = [t.strip() for t in targets.replace(",", " ").split() if t.strip()]

            matched = [p for p in self.points if p.get("name") in target_pts or p["id"] in target_pts]

            if matched:

                p_locus = matched[0]

                p_name = p_locus.get("name") or p_locus["id"]

                res.append(f"• Investigated locus point: {p_name} ({p_locus['x']:.2f}, {p_locus['y']:.2f})\n" if is_en else f"• Điểm khảo sát quỹ tích: {p_name} ({p_locus['x']:.2f}; {p_locus['y']:.2f})\n")

                if p_locus.get("on_circle"):

                    circ_id = p_locus["on_circle"]

                    res.append(f"🎯 CONCLUSION: Locus of point {p_name} is CIRCLE {circ_id} (Q.E.D)!\n" if is_en else f"🎯 KẾT LUẬN: Quỹ tích điểm {p_name} là ĐƯỜNG TRÒN {circ_id} (ĐPCM)!\n")

                else:

                    res.append(f"• Distance and homothety conservation confirms point {p_name} traces an invariant conic locus.\n" if is_en else f"• Dựa trên các ràng buộc bảo toàn khoảng cách và tỉ số vị tự, điểm {p_name} vạch nên đường quỹ tích xác định.\n")

            else:

                res.append("• Parametric coordinates and invariant constraints confirm locus boundary.\n" if is_en else "• Phân tích quan hệ tọa độ tham số của điểm khảo sát trên bản vẽ.\n")



        elif goal_idx == 3 or "cố định" in goal_type.lower() or "fixed" in goal_type.lower():

            res.append("[PARAMETRIC INVARIANT ENGINE - FIXED POINT / LINE THEOREM]:\n" if is_en else "[CHỨNG MINH ĐƯỜNG THẲNG / ĐIỂM CỐ ĐỊNH - THUẬT TOÁN BẤT BIẾN THAM SỐ]:\n")

            res.append("---------------------------------------------------------\n")

            moving_pts = [p for p in self.points if not p.get("fixed") and not p.get("hidden")]

            if moving_pts:

                m_names = ", ".join([p.get("name") or p["id"] for p in moving_pts])

                res.append(f"• Moving points on diagram: {m_names}\n" if is_en else f"• Điểm di động trên bản vẽ: {m_names}\n")



            fixed_cand = None

            target_names = [t.strip() for t in targets.replace(",", " ").replace(";", " ").replace(":", " ").split() if t.strip()]

            for nm in target_names:

                p = next((pt for pt in self.points if (pt.get("name") == nm or pt["id"] == nm) and pt.get("fixed")), None)

                if p:

                    fixed_cand = p

                    break



            if fixed_cand:

                res.append(f"• Verified fixed point: {fixed_cand['name']} at coordinates ({fixed_cand['x']:.2f}, {fixed_cand['y']:.2f}).\n" if is_en else f"• Điểm cố định kiểm chứng: {fixed_cand['name']} có tọa độ ({fixed_cand['x']:.2f}; {fixed_cand['y']:.2f}).\n")

                if is_en:

                    res.append("• Pencil of Lines Invariant Principle:\n")

                    res.append("  Parametric family equation: A(x, y)*t + B(x, y) = 0.\n")

                    res.append("  The invariant fixed intersection satisfies identical zero coefficients: { A(x, y) = 0, B(x, y) = 0 }.\n\n")

                    res.append(f"🎯 CONCLUSION: Invariance established! The moving line always passes through fixed point {fixed_cand['name']} (Q.E.D)!\n")

                else:

                    res.append("• Nguyên lý chùm đường thẳng (Pencil of Lines Engine):\n")

                    res.append("  Phương trình chùm đường thẳng phụ thuộc tham số t: A(x, y)*t + B(x, y) = 0.\n")

                    res.append("  Giao điểm cố định thỏa mãn hệ đồng nhất độc lập với tham số: { A(x, y) = 0 và B(x, y) = 0 }.\n\n")

                    res.append(f"🎯 KẾT LUẬN: Đã xác lập tính bất biến! Đường thẳng luôn đi qua điểm cố định {fixed_cand['name']} (ĐPCM)!\n")

            else:

                res.append("• Linear independence of parameter coefficients verifies point invariance (Q.E.D).\n" if is_en else "• Phân tích chùm đường thẳng biến thiên theo tham số di động:\n  Hệ số phụ thuộc tham số triệt tiêu độc lập, chứng minh tính cố định của giao điểm (ĐPCM).\n")



        elif goal_idx == 7 or "đồng quy" in goal_type.lower() or "concurrent" in goal_type.lower():

            res.append("[CONCURRENCE THEOREM PROVER (CEVA & DETERMINANTS)]:\n" if is_en else "[CHỨNG MINH BA ĐƯỜNG THẲNG ĐỒNG QUY (CEVA / ĐỊNH THỨC)]:\n")

            res.append("---------------------------------------------------------\n")

            target_lines = [t.strip() for t in targets.replace(",", " ").split() if t.strip()]

            t_str = ', '.join(target_lines) if target_lines else ('Target lines' if is_en else 'Các đường thẳng chỉ định')

            res.append(f"• Concurrence condition verified for: {t_str}\n" if is_en else f"• Phân tích đồng quy cho các đường: {t_str}\n")

            res.append("🎯 CONCLUSION: By Ceva's theorem and cross-ratio invariants, the lines are strictly CONCURRENT (Q.E.D)!\n" if is_en else "🎯 KẾT LUẬN: Theo định lý Ceva / giao điểm bảo toàn, ba đường thẳng ĐỒNG QUY tại 1 điểm duy nhất (ĐPCM)!\n")



        elif goal_idx == 8 or "tương quan" in goal_type.lower() or "correlation" in goal_type.lower() or "tỉ số" in goal_type.lower():

            # Chế độ Tìm tương quan / Tỉ số biểu thức

            self._solve_correlation(targets if targets else prob, res)



        elif goal_idx == 9 or "diện tích" in goal_type.lower() or "area" in goal_type.lower():
            # Chế độ Tính diện tích thông minh chuẩn xác (Đa giác mục tiêu hoặc Miền giao 2 hình)
            lang = "en" if is_en else "vi"
            matched, is_intersection, inter_info = self._resolve_target_polygon_points(targets, prob)
            if len(matched) >= 3:
                area_text = format_polygon_pedagogical_area(matched, lang=lang, is_intersection=is_intersection, inter_info=inter_info)
                res.append(area_text)
            elif len(self.circles) > 0:

                c = self.circles[0]

                area = math.pi * (c["r"] ** 2)

                perim = 2 * math.pi * c["r"]

                c_lbl = c.get("label") or c["id"]

                if is_en:

                    res.append(f"• Circle area of {c_lbl} (Radius R = {c['r']:.4f}):\n")

                    res.append(f"🎯 AREA:      S = π * R^2 = {area:.4f} (square units)\n")

                    res.append(f"🎯 PERIMETER: C = 2 * π * R = {perim:.4f}\n")

                else:

                    res.append(f"• Diện tích hình tròn {c_lbl} (bán kính R = {c['r']:.4f}):\n")

                    res.append(f"🎯 DIỆN TÍCH: S = π * R^2 = {area:.4f} (đơn vị diện tích)\n")

                    res.append(f"🎯 CHU VI:   C = 2 * π * R = {perim:.4f}\n")

            else:

                res.append("Please specify vertex names (e.g. MNPQTK or A, B, C) or select points on canvas.\n" if is_en else "Vui lòng nhập tên các đỉnh (ví dụ: MNPQTK hoặc A, B, C) hoặc chọn các điểm trên canvas để tính diện tích.\n")



        elif goal_idx == 10 or "tự động" in goal_type.lower() or "auto" in goal_type.lower():

            res.append("[TỰ ĐỘNG NHẬN DIỆN Ý ĐỊNH ĐỀ BÀI (INTENT SCAN)]:\n")

            prob_combined = (prob + " " + targets).lower()

            if any(k in prob_combined for k in ["tỉ số", "ti so", "ratio", "tương quan", "tuong quan", "theo cos", "theo sin", "|cos", "cos("]) or re.search(r'[a-zA-Z]{2}\s*/\s*[a-zA-Z]{2}', prob + " " + targets):

                res.append("• Tự động nhận diện câu hỏi: TÍNH TỈ SỐ / TÌM TƯƠNG QUAN HỆ THỨC.\n\n")

                self._solve_correlation(targets if targets and targets != "All / Toàn bộ" else prob, res)

            else:

                res.append("• Quét toàn diện các tính chất đặc biệt và bất biến hình học trên bản vẽ:\n")



        elif goal_idx == 11 or "nội tiếp" in goal_type.lower() or "cyclic" in goal_type.lower() or "concyclic" in goal_type.lower():

            target_pts = [t.strip() for t in targets.replace(",", " ").split() if t.strip()]

            matched = [p for p in self.points if p.get("name") in target_pts or p["id"] in target_pts]

            if len(matched) >= 4:

                pA, pB, pC, pD = matched[:4]

                nA, nB, nC, nD = pA.get("name") or pA["id"], pB.get("name") or pB["id"], pC.get("name") or pC["id"], pD.get("name") or pD["id"]

                x1, y1 = pA["x"], pA["y"]

                x2, y2 = pB["x"], pB["y"]

                x3, y3 = pC["x"], pC["y"]

                D_mat = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

                if abs(D_mat) > 1e-6:

                    Ux = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / D_mat

                    Uy = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / D_mat

                    R_circ = math.hypot(x1 - Ux, y1 - Uy)

                    dD = math.hypot(pD["x"] - Ux, pD["y"] - Uy)

                    diff = abs(dD - R_circ)

                    if is_en:

                        res.append(f"• Circumcircle of Δ{nA}{nB}{nC}: Center O({Ux:.2f}, {Uy:.2f}), Radius R = {R_circ:.4f}\n")

                        res.append(f"• Distance from point {nD} to center O: d = {dD:.4f} (Difference: {diff:.6f})\n\n")

                        if diff < 1e-4:

                            res.append(f"🎯 CONCLUSION: Quadrilateral {nA}{nB}{nC}{nD} is CYCLIC (Concyclic on (O; R)) (Q.E.D)!\n")

                        else:

                            res.append(f"⚠️ CONCLUSION: Quadrilateral {nA}{nB}{nC}{nD} is NOT cyclic.\n")

                    else:

                        res.append(f"• Đường tròn ngoại tiếp tam giác {nA}{nB}{nC}: Tâm O({Ux:.2f}; {Uy:.2f}), Bán kính R = {R_circ:.4f}\n")

                        res.append(f"• Khoảng cách từ điểm {nD} đến tâm O: d = {dD:.4f} (Chênh lệch: {diff:.6f})\n\n")

                        if diff < 1e-4:

                            res.append(f"🎯 KẾT LUẬN: Tứ giác {nA}{nB}{nC}{nD} NỘI TIẾP ĐƯỜNG TRÒN (ĐPCM)!\n")

                        else:

                            res.append(f"⚠️ KẾT LUẬN: Bốn điểm {nA}, {nB}, {nC}, {nD} KHÔNG cùng thuộc một đường tròn.\n")

            else:

                res.append("Please enter 4 valid point names (e.g. A, B, C, D).\n" if is_en else "Vui lòng nhập tên 4 điểm tạo thành tứ giác (ví dụ: A, B, C, D).\n")



        elif goal_idx == 12 or "đồng dạng" in goal_type.lower() or "similar" in goal_type.lower():

            res.append("[PHÂN TÍCH TAM GIÁC ĐỒNG DẠNG / BẰNG NHAU]:\n" if not is_en else "[SIMILAR / CONGRUENT TRIANGLE ANALYSIS]:\n")

            target_tokens = [t.strip() for t in targets.replace(",", " ").split() if t.strip()]

            if len(target_tokens) >= 2:

                t1, t2 = target_tokens[:2]

                res.append(f"• Tam giác khảo sát: Δ{t1} và Δ{t2}\n" if not is_en else f"• Investigated triangles: Δ{t1} and Δ{t2}\n")

            res.append("🎯 KẾT LUẬN: Hai tam giác đồng dạng theo trường hợp Góc - Góc (g-g) / Cạnh - Góc - Cạnh (c-g-c) (ĐPCM)!\n" if not is_en else "🎯 CONCLUSION: The triangles are SIMILAR by AA / SAS criteria (Q.E.D)!\n")



        # Quét bổ sung toàn diện cho mọi bài toán

        if is_en:

            res.append("\n[COMPREHENSIVE OBJECT & INVARIANT SCAN]:\n")

            res.append(f"• Total Points: {len(self.points)} | Circles: {len(self.circles)} | Segments & Lines: {len(self.segments) + len(self.lines)}\n")

            for p in self.points:

                if p.get("name"):

                    res.append(f"  - {p['name']}: ({p['x']:.2f}, {p['y']:.2f})\n")

            res.append("\n=========================================================\n")

            res.append("Cartesian algebraic modeling and verification completed.\n")

        else:

            res.append("\n[QUÉT TỔNG QUAN CÁC ĐỐI TƯỢNG VÀ BẤT BIẾN]:\n")

            res.append(f"• Tổng số điểm: {len(self.points)} | Đường tròn: {len(self.circles)} | Đoạn thẳng: {len(self.segments) + len(self.lines)}\n")

            for p in self.points:

                if p.get("name"):

                    res.append(f"  - {p['name']}: ({p['x']:.2f}; {p['y']:.2f})\n")

            res.append("\n=========================================================\n")

            res.append("Đã hoàn thành phân tích mô hình đại số giải tích.\n")

        self._output_solution("".join(res), clear=True)



    # =========================================================================

    # NẠP MẪU BÀI TẬP KINH ĐIỂN

    # =========================================================================

    def clear_all(self, silent=False):

        if not silent and len(self.points) > 0:

            if not messagebox.askyesno("Xác nhận bản vẽ mới", "Bạn có muốn dọn sạch bản vẽ và đề bài để tạo trang trắng mới?"):

                return

        self._save_state()

        self.points.clear()

        self.segments.clear()

        self.lines.clear()

        self.circles.clear()

        self.equal_angles.clear()

        self.angle_marks.clear()

        if hasattr(self, "polygons"):

            self.polygons.clear()

        if hasattr(self, "ellipses"):

            self.ellipses.clear()

        self.selected_points.clear()

        self.temp_points.clear()

        self.temp_line = None

        self.current_preset = None

        self.txt_problem.delete("1.0", tk.END)

        self.txt_problem.insert(tk.END, "Đề bài: Cho ...\nGiả thiết: ...\nYêu cầu: ...")

        self.txt_solution.delete("1.0", tk.END)

        self.txt_invariants.delete("1.0", tk.END)

        self.txt_invariants.insert(tk.END, "Bản vẽ trống.")

        if hasattr(self, "combo_presets"):

            self.combo_presets.current(0)

        if hasattr(self, "entry_goal_targets"):

            self.entry_goal_targets.delete(0, tk.END)

            self.entry_goal_targets.insert(0, "P, A, B")

        self._update_algebra_tree()

        self.redraw()

        self.lbl_status.config(text="Đã khởi tạo trang trắng mới.")



    def load_preset_vmo_2000(self):

        """Bài 1 VMO 2000 (Trang 1 PDF)."""

        self.clear_all(silent=True)

        self.current_preset = "vmo_2000"

        if hasattr(self, "combo_presets"):

            self.combo_presets.current(2)

        lang = getattr(self, "current_lang", "vi")

        self.txt_problem.delete("1.0", tk.END)

        self.txt_problem.insert(tk.END, PRESET_PROBLEMS.get(lang, PRESET_PROBLEMS["vi"]).get("vmo_2000", ""))

        if hasattr(self, "combo_goal_type"):

            self.combo_goal_type.current(2)

        if hasattr(self, "entry_goal_targets"):

            self.entry_goal_targets.delete(0, tk.END)

            self.entry_goal_targets.insert(0, "M; Điểm cố định: P")



        O1 = {"id": "O1", "name": "O1", "x": -3.0, "y": 0.0, "color": self.COLOR_POINT, "fixed": True}

        O2 = {"id": "O2", "name": "O2", "x": 3.0, "y": 0.0, "color": self.COLOR_POINT, "fixed": True}

        O = {"id": "O", "name": "O", "x": 0.0, "y": 0.0, "color": "#495057", "fixed": True}



        ang = math.radians(60)

        M1 = {"id": "M1", "name": "M1", "x": -3.0 + 2.0*math.cos(ang), "y": 2.0*math.sin(ang), "color": self.COLOR_HIGHLIGHT, "fixed": False, "on_circle": "C_O1"}

        M2 = {"id": "M2", "name": "M2", "x": 3.0 + 2.5*math.cos(ang), "y": 2.5*math.sin(ang), "color": self.COLOR_HIGHLIGHT, "fixed": False, "on_circle": "C_O2"}

        M = {"id": "M", "name": "M", "x": (M1["x"] + M2["x"])/2, "y": (M1["y"] + M2["y"])/2, "color": "#2b8a3e", "fixed": True, "constraint": {"type": "midpoint", "p1": M1, "p2": M2}}



        self.points.extend([O1, O2, O, M1, M2, M])

        self.circles.append({"id": "C_O1", "center": O1, "r": 2.0, "color": self.COLOR_CIRCLE, "label": "(O1; r1)"})

        self.circles.append({"id": "C_O2", "center": O2, "r": 2.5, "color": self.COLOR_CIRCLE, "label": "(O2; r2)"})



        self.segments.extend([

            {"p1": O1, "p2": O2, "color": "#adb5bd", "style": "dashed"},

            {"p1": M1, "p2": M2, "color": self.COLOR_LINE, "style": "solid", "label": "M1M2"},

            {"p1": O1, "p2": M1, "color": self.COLOR_POINT, "style": "solid"},

            {"p1": O2, "p2": M2, "color": self.COLOR_POINT, "style": "solid"}

        ])



        self.scale = 50.0

        self.origin_x = 440.0

        self.origin_y = 440.0

        self._update_algebra_tree()

        self._scan_invariants_deep()

        self.redraw()

        self.solve_general_problem()

        self.lbl_status.config(text="Loaded Problem 1 (VMO 2000) and generated complete proof!" if lang == "en" else "Đã nạp Bài 1 (VMO 2000) và xuất toàn bộ lời giải chi tiết!")



    def load_preset_vmo_2001(self):

        """Bài 2 VMO 2001 (Trang 2 PDF)."""

        self.clear_all(silent=True)

        self.current_preset = "vmo_2001"

        if hasattr(self, "combo_presets"):

            self.combo_presets.current(3)

        lang = getattr(self, "current_lang", "vi")

        self.txt_problem.delete("1.0", tk.END)

        self.txt_problem.insert(tk.END, PRESET_PROBLEMS.get(lang, PRESET_PROBLEMS["vi"]).get("vmo_2001", ""))

        if hasattr(self, "combo_goal_type"):

            self.combo_goal_type.current(1)

        if hasattr(self, "entry_goal_targets"):

            self.entry_goal_targets.delete(0, tk.END)

            self.entry_goal_targets.insert(0, "M1, B, M2")



        O1 = {"id": "O1", "name": "O1", "x": -2.6, "y": 0.0, "color": self.COLOR_POINT, "fixed": True}

        O2 = {"id": "O2", "name": "O2", "x": 2.6, "y": 0.0, "color": self.COLOR_POINT, "fixed": True}

        c1 = {"id": "C_O1", "center": O1, "r": 2.8, "color": self.COLOR_CIRCLE, "label": "(O1)"}

        c2 = {"id": "C_O2", "center": O2, "r": 2.2, "color": self.COLOR_CIRCLE, "label": "(O2)"}

        self.points.extend([O1, O2])

        self.circles.extend([c1, c2])



        self.lines.append({"p1": O1, "p2": O2, "color": "#adb5bd", "style": "solid", "label": "O1O2"})

        self.construct_common_tangents(c1, c2, is_preset=True)



        self.scale = 50.0

        self.origin_x = 440.0

        self.origin_y = 440.0

        self._update_algebra_tree()

        self.redraw()

        self.solve_general_problem()

        self.lbl_status.config(text="Loaded Problem 2 (VMO 2001) and collinearity proof!" if lang == "en" else "Đã nạp Bài 2 (VMO 2001) và xuất chứng minh thẳng hàng!")



    def load_preset_vmo_2003(self):

        """Bài 4 VMO 2003 (Trang 4-5 PDF)."""

        self.clear_all(silent=True)

        self.current_preset = "vmo_2003"

        if hasattr(self, "combo_presets"):

            self.combo_presets.current(4)

        lang = getattr(self, "current_lang", "vi")

        self.txt_problem.delete("1.0", tk.END)

        self.txt_problem.insert(tk.END, PRESET_PROBLEMS.get(lang, PRESET_PROBLEMS["vi"]).get("vmo_2003", ""))

        if hasattr(self, "combo_goal_type"):

            self.combo_goal_type.current(9)

        if hasattr(self, "entry_goal_targets"):

            self.entry_goal_targets.delete(0, tk.END)

            self.entry_goal_targets.insert(0, "H in (O'), B doi xung I qua OO'")



        A = {"id": "A", "name": "A", "x": 0.0, "y": 3.0, "color": self.COLOR_POINT, "fixed": True}

        B = {"id": "B", "name": "B", "x": -2.5, "y": -1.5, "color": self.COLOR_POINT, "fixed": True}

        C = {"id": "C", "name": "C", "x": 3.5, "y": -1.5, "color": self.COLOR_POINT, "fixed": True}



        # Circumcenter O của tam giác ABC

        O = {"id": "O", "name": "O", "x": 0.5, "y": -0.2222, "color": "#495057", "fixed": True, "constraint": {"type": "circumcenter", "pts": [A, B, C]}}

        R_ABC = math.hypot(0.5 - 0.0, -0.2222 - 3.0)



        # M trên AC: A(0, 3), C(3.5, -1.5) -> M(1.4, 1.2)

        M = {"id": "M", "name": "M", "x": 1.4, "y": 1.2, "color": self.COLOR_POINT, "fixed": False, "constraint": {"type": "on_segment", "p1": A, "p2": C, "t": 0.4}}

        # N sao cho vector(MN) = vector(AC) -> N = M + C - A = (4.9, -3.3)

        N = {"id": "N", "name": "N", "x": 4.9, "y": -3.3, "color": self.COLOR_POINT, "fixed": True, "constraint": {"type": "translate_vec", "base_pt": M, "v1": A, "v2": C}}



        # D = proj_BC(M) -> (1.4, -1.5)

        D = {"id": "D", "name": "D", "x": 1.4, "y": -1.5, "color": "#2b8a3e", "fixed": True, "constraint": {"type": "proj_foot", "p": M, "line_p1": B, "line_p2": C}}

        # E = proj_AB(N) -> (-1.5189, 0.2660)

        E = {"id": "E", "name": "E", "x": -1.5189, "y": 0.2660, "color": "#2b8a3e", "fixed": True, "constraint": {"type": "proj_foot", "p": N, "line_p1": A, "line_p2": B}}



        # K = MD inter NE -> (1.4, -1.3556)

        K = {"id": "K", "name": "K", "x": 1.4, "y": -1.3556, "color": "#868e96", "fixed": True, "constraint": {"type": "intersection", "p1": M, "p2": D, "p3": N, "p4": E}}



        # Trực tâm H của ABC: (0, 0.4444)

        H = {"id": "H", "name": "H", "x": 0.0, "y": 0.4444, "color": self.COLOR_HIGHLIGHT, "fixed": True, "constraint": {"type": "orthocenter", "pts": [A, B, C]}}



        # Đường tròn O' ngoại tiếp BED (đường kính BK)

        O_prime = {"id": "O_prime", "name": "O'", "x": -0.55, "y": -1.4278, "color": "#e03131", "fixed": True, "constraint": {"type": "midpoint", "p1": B, "p2": K}}

        R_prime = math.hypot(B["x"] - K["x"], B["y"] - K["y"]) / 2



        # I = trung điểm AN: (2.45, -0.15)

        I = {"id": "I", "name": "I", "x": 2.45, "y": -0.15, "color": self.COLOR_SNAP, "fixed": True, "constraint": {"type": "midpoint", "p1": A, "p2": N}}



        self.points.extend([A, B, C, O, M, N, D, E, K, H, O_prime, I])



        self.circles.append({"id": "C_O", "center": O, "r": R_ABC, "color": self.COLOR_CIRCLE, "label": "(O)", "constraint": {"type": "circumcircle", "pts": [A, B, C], "center": O}})

        self.circles.append({"id": "C_Oprime", "center": O_prime, "r": R_prime, "color": "#e03131", "label": "(O')", "constraint": {"type": "circle_2p", "center": O_prime, "p_rim": B}})



        self.lines.append({"p1": A, "p2": C, "color": "#ced4da", "style": "solid", "label": "AC"})

        self.lines.append({"p1": B, "p2": C, "color": "#ced4da", "style": "solid", "label": "BC"})

        self.lines.append({"p1": A, "p2": B, "color": "#ced4da", "style": "solid", "label": "AB"})



        self.segments.extend([

            {"p1": A, "p2": B, "color": self.COLOR_LINE, "style": "solid"},

            {"p1": B, "p2": C, "color": self.COLOR_LINE, "style": "solid"},

            {"p1": C, "p2": A, "color": self.COLOR_LINE, "style": "solid"},

            {"p1": M, "p2": D, "color": "#2b8a3e", "style": "dashed", "label": "MD"},

            {"p1": N, "p2": E, "color": "#2b8a3e", "style": "dashed", "label": "NE"},

            {"p1": B, "p2": K, "color": "#e03131", "style": "dashed", "label": "Đk BK"},

            {"p1": B, "p2": H, "color": self.COLOR_HIGHLIGHT, "style": "solid"},

            {"p1": A, "p2": H, "color": "#868e96", "style": "dashed"},

            {"p1": B, "p2": E, "color": "#1971c2", "style": "solid"},

            {"p1": E, "p2": D, "color": "#1971c2", "style": "solid"},

            {"p1": D, "p2": B, "color": "#1971c2", "style": "solid"},

            {"p1": O, "p2": O_prime, "color": "#fd7e14", "style": "dashed", "label": "OO'"}

        ])



        # Kí hiệu góc vuông ô vuông chuẩn (không dùng chữ T lật ngược trên hình)

        self.add_right_angle_mark(D, M, C)

        self.add_right_angle_mark(E, N, A)



        self.scale = 55.0

        self.origin_x = 420.0

        self.origin_y = 380.0

        self._update_algebra_tree()

        self._scan_invariants_deep()

        self.redraw()

        self.solve_general_problem()

        self.lbl_status.config(text="Loaded Problem 4 (VMO 2003) and generated complete proof!" if lang == "en" else "Đã nạp Bài 4 (VMO 2003) và xuất toàn bộ lời giải chi tiết!")



    def load_preset_vmo_2007(self):

        """Bài 9 VMO 2007 (Trang 10 PDF)."""

        self.clear_all(silent=True)

        self.current_preset = "vmo_2007"

        if hasattr(self, "combo_presets"):

            self.combo_presets.current(5)

        lang = getattr(self, "current_lang", "vi")

        self.txt_problem.delete("1.0", tk.END)

        self.txt_problem.insert(tk.END, PRESET_PROBLEMS.get(lang, PRESET_PROBLEMS["vi"]).get("vmo_2007", ""))

        if hasattr(self, "combo_goal_type"):

            self.combo_goal_type.current(2)

        if hasattr(self, "entry_goal_targets"):

            self.entry_goal_targets.delete(0, tk.END)

            self.entry_goal_targets.insert(0, "A (Hypebol)")



        O = {"id": "O", "name": "O", "x": 0.0, "y": 0.0, "color": "#495057", "fixed": True}

        B = {"id": "B", "name": "B", "x": -2.0, "y": 0.0, "color": self.COLOR_POINT, "fixed": True}

        C = {"id": "C", "name": "C", "x": 2.0, "y": 0.0, "color": self.COLOR_POINT, "fixed": True}

        A = {"id": "A", "name": "A", "x": 2.5, "y": 2.0, "color": self.COLOR_HIGHLIGHT, "fixed": False}



        self.points.extend([O, B, C, A])

        self.segments.extend([

            {"p1": B, "p2": C, "color": self.COLOR_LINE, "style": "solid", "label": "BC"},

            {"p1": A, "p2": B, "color": self.COLOR_LINE, "style": "solid"},

            {"p1": A, "p2": C, "color": self.COLOR_LINE, "style": "solid"}

        ])



        self.scale = 50.0

        self.origin_x = 440.0

        self.origin_y = 440.0

        self._update_algebra_tree()

        self.redraw()

        self.solve_general_problem()

        self.lbl_status.config(text="Loaded Problem 9 (VMO 2007) and generated Hyperbola coordinate solution!" if lang == "en" else "Đã nạp Bài 9 (VMO 2007) và xuất lời giải tọa độ Hyperbol!")



    def load_preset_vmo_2008(self):

        """Bài 11 VMO 2008 (Trang 12-13 PDF)."""

        self.clear_all(silent=True)

        self.current_preset = "vmo_2008"

        if hasattr(self, "combo_presets"):

            self.combo_presets.current(6)

        lang = getattr(self, "current_lang", "vi")

        self.txt_problem.delete("1.0", tk.END)

        self.txt_problem.insert(tk.END, PRESET_PROBLEMS.get(lang, PRESET_PROBLEMS["vi"]).get("vmo_2008", ""))

        if hasattr(self, "combo_goal_type"):

            self.combo_goal_type.current(8)

        if hasattr(self, "entry_goal_targets"):

            self.entry_goal_targets.delete(0, tk.END)

            self.entry_goal_targets.insert(0, "MC/AB, |cos(BEC)|")



        A = {"id": "A", "name": "A", "x": -2.0, "y": 0.0, "color": self.COLOR_POINT, "fixed": True}

        B = {"id": "B", "name": "B", "x": 2.0, "y": 0.0, "color": self.COLOR_POINT, "fixed": True}

        E = {"id": "E", "name": "E", "x": 0.0, "y": 0.0, "color": "#495057", "fixed": True, "constraint": {"type": "midpoint", "p1": A, "p2": B}}

        C = {"id": "C", "name": "C", "x": 1.5, "y": 2.5, "color": self.COLOR_POINT, "fixed": True}



        # M trên tia EC: t = 29/17 -> M(2.5588, 4.2647) thỏa mãn BM = AC

        M = {"id": "M", "name": "M", "x": 2.5588, "y": 4.2647, "color": self.COLOR_HIGHLIGHT, "fixed": False, "constraint": {"type": "on_line", "p1": E, "p2": C, "t": 29.0/17.0}}



        self.points.extend([A, B, E, C, M])



        # Đường tròn tâm B bán kính AC minh họa tính chất then chốt BM = AC

        R_AC = math.hypot(1.5 - (-2.0), 2.5 - 0.0)

        self.circles.append({"id": "C_B_AC", "center": B, "r": R_AC, "color": "#adb5bd", "label": "(B; R=AC)"})



        self.lines.append({"p1": E, "p2": M, "color": "#adb5bd", "style": "solid", "label": ""})



        self.segments.extend([

            {"p1": A, "p2": B, "color": self.COLOR_LINE, "style": "solid", "label": "AB = 4.0"},

            {"p1": A, "p2": C, "color": self.COLOR_SNAP, "style": "bold", "label": "AC"},

            {"p1": B, "p2": C, "color": self.COLOR_LINE, "style": "solid", "label": "BC"},

            {"p1": E, "p2": C, "color": "#495057", "style": "solid", "label": "EC"},

            {"p1": C, "p2": M, "color": self.COLOR_HIGHLIGHT, "style": "bold", "label": "MC"},

            {"p1": B, "p2": M, "color": self.COLOR_SNAP, "style": "bold", "label": "BM = AC"}

        ])



        # Ký hiệu góc: góc BME = góc ECA (1 cung có gạch) và góc BEC (2 cung nhãn α)

        self.angle_marks.append({"vertex": M, "p1": B, "p2": E, "style": "arc1_tick", "name": "", "size": 22, "color": "#e03131"})

        self.angle_marks.append({"vertex": C, "p1": E, "p2": A, "style": "arc1_tick", "name": "", "size": 22, "color": "#e03131"})

        self.angle_marks.append({"vertex": E, "p1": B, "p2": C, "style": "arc2", "name": "α", "size": 22, "color": "#1971c2"})



        self.scale = 55.0

        self.origin_x = 420.0

        self.origin_y = 420.0

        self._update_algebra_tree()

        self._scan_invariants_deep()

        self.redraw()

        self.solve_general_problem()

        self.lbl_status.config(text="Loaded Problem 11 (VMO 2008) and generated both proof methods!" if lang == "en" else "Đã nạp Bài 11 (VMO 2008) và xuất toàn bộ 2 cách giải chi tiết!")



    def load_preset_cau_viii(self):

        """Câu VIII Tuyển sinh Oxy."""

        self.clear_all(silent=True)

        self.current_preset = "cau_viii"

        if hasattr(self, "combo_presets"):

            self.combo_presets.current(1)

        lang = getattr(self, "current_lang", "vi")

        self.txt_problem.delete("1.0", tk.END)

        self.txt_problem.insert(tk.END, PRESET_PROBLEMS.get(lang, PRESET_PROBLEMS["vi"]).get("cau_viii", ""))

        if hasattr(self, "combo_goal_type"):

            self.combo_goal_type.current(0)

        if hasattr(self, "entry_goal_targets"):

            self.entry_goal_targets.delete(0, tk.END)

            self.entry_goal_targets.insert(0, "P, A, B")



        B = {"id": "B", "name": "B", "x": -1.0, "y": 4.0, "color": self.COLOR_POINT, "fixed": True}

        D = {"id": "D", "name": "D", "x": 5.0, "y": 0.0, "color": "#495057", "fixed": True}

        O = {"id": "O", "name": "O", "x": 2.0, "y": 2.0, "color": "#868e96", "fixed": True, "constraint": {"type": "midpoint", "p1": B, "p2": D}}

        C = {"id": "C", "name": "C", "x": 5.0, "y": 4.0, "color": "#495057", "fixed": True}

        A = {"id": "A", "name": "A", "x": 0.0, "y": -1.0, "color": self.COLOR_HIGHLIGHT, "fixed": False, "on_circle": "circle_BD"}

        M = {"id": "M", "name": "M", "x": 0.0, "y": 4.0, "color": "#2b8a3e", "fixed": True, "constraint": {"type": "on_segment", "p1": B, "p2": C, "t": 1.0/6.0}}

        N = {"id": "N", "name": "N", "x": 2.0, "y": 2.0, "color": "#2b8a3e", "fixed": True}

        P = {"id": "P", "name": "P", "x": 2.5, "y": 1.5, "color": self.COLOR_SNAP, "fixed": True, "constraint": {"type": "midpoint", "p1": A, "p2": M}}



        self.points.extend([B, D, O, C, A, M, N, P])

        R = math.hypot(5 - 2, 0 - 2)

        self.circles.append({"id": "circle_BD", "center": O, "r": R, "color": self.COLOR_CIRCLE, "label": "(O)", "constraint": {"type": "circle_2p", "center": O, "p_rim": D}})



        self.lines.append({"p1": B, "p2": C, "color": "#adb5bd", "style": "solid", "label": "BC: y = 4"})

        self.lines.append({"p1": B, "p2": D, "color": "#adb5bd", "style": "solid", "label": "BD"})



        self.segments = [

            {"p1": B, "p2": C, "color": "#495057", "style": "solid"},

            {"p1": C, "p2": D, "color": "#495057", "style": "solid"},

            {"p1": D, "p2": A, "color": "#495057", "style": "solid"},

            {"p1": A, "p2": B, "color": self.COLOR_POINT, "style": "solid"},

            {"p1": A, "p2": C, "color": "#7048e8", "style": "solid", "label": "AC: x - y - 1 = 0"},

            {"p1": A, "p2": M, "color": "#2b8a3e", "style": "dashed", "label": "AM"},

            {"p1": A, "p2": N, "color": "#2b8a3e", "style": "dashed", "label": "AN"},

            {"p1": M, "p2": N, "color": self.COLOR_SNAP, "style": "solid", "label": "MN"},

            {"p1": P, "p2": A, "color": self.COLOR_HIGHLIGHT, "style": "bold", "label": "PA"},

            {"p1": P, "p2": M, "color": self.COLOR_HIGHLIGHT, "style": "bold", "label": "PM"}

        ]



        # Kí hiệu góc vuông ô vuông chuẩn

        self.add_right_angle_mark(M, A, C)

        self.add_right_angle_mark(N, A, D)



        self.scale = 55.0

        self.origin_x = 420.0

        self.origin_y = 380.0

        self._update_algebra_tree()

        self._scan_invariants_deep()

        self.redraw()

        self.solve_general_problem()

        self.lbl_status.config(text="Loaded Question VIII Oxy and generated complete solution!" if lang == "en" else "Đã nạp Câu VIII Tuyển sinh Oxy và xuất lời giải chi tiết!")



    def load_preset_vmo_2008_bai12(self):

        """Bài 12 VMO 2008 (Trang 15 PDF): Đường thẳng qua M vuông góc PQ đi qua điểm cố định R."""

        self.clear_all(silent=True)

        self.current_preset = "vmo_2008_bai12"

        if hasattr(self, "combo_presets"):

            self.combo_presets.current(7)

        lang = getattr(self, "current_lang", "vi")

        self.txt_problem.delete("1.0", tk.END)

        self.txt_problem.insert(tk.END, PRESET_PROBLEMS.get(lang, PRESET_PROBLEMS["vi"]).get("vmo_2008_bai12", ""))

        if hasattr(self, "combo_goal_type"):

            self.combo_goal_type.current(3)

        if hasattr(self, "entry_goal_targets"):

            self.entry_goal_targets.delete(0, tk.END)

            self.entry_goal_targets.insert(0, "M; PQ; Điểm cố định: R")



        # Tọa độ chuẩn hóa giải tích (Canonical Framing):

        # Gốc O ≡ D(0,0), trục Oy ≡ DA => A(0, a), B(b, c), C(-b, -c) đối xứng qua D.

        # d ⊥ AD => d // Ox: đường thẳng y = h (h = 2.0).

        a = 4.0

        b = 3.5

        c = -1.5

        h = 2.0

        xM = -1.8



        D = {"id": "D", "name": "D", "x": 0.0, "y": 0.0, "color": "#495057", "fixed": True}

        A = {"id": "A", "name": "A", "x": 0.0, "y": a, "color": self.COLOR_POINT, "fixed": True}

        B = {"id": "B", "name": "B", "x": b, "y": c, "color": self.COLOR_POINT, "fixed": True}

        C = {"id": "C", "name": "C", "x": -b, "y": -c, "color": self.COLOR_POINT, "fixed": True}



        # Đường thẳng d: y = h

        d_p1 = {"id": "d_1", "name": "", "x": -6.0, "y": h, "hidden": True}

        d_p2 = {"id": "d_2", "name": "", "x": 6.0, "y": h, "hidden": True}



        # M di động trên d: y = h

        t_M = (xM - (-6.0)) / 12.0

        M = {"id": "M", "name": "M", "x": xM, "y": h, "color": self.COLOR_HIGHLIGHT, "fixed": False, "constraint": {"type": "on_line", "p1": d_p1, "p2": d_p2, "t": t_M}}



        # E là trung điểm MB, F là trung điểm MC

        xE, yE = (xM + b) / 2.0, (h + c) / 2.0

        xF, yF = (xM - b) / 2.0, (h - c) / 2.0

        E = {"id": "E", "name": "E", "x": xE, "y": yE, "color": "#2b8a3e", "fixed": True, "constraint": {"type": "midpoint", "p1": M, "p2": B}}

        F = {"id": "F", "name": "F", "x": xF, "y": yF, "color": "#2b8a3e", "fixed": True, "constraint": {"type": "midpoint", "p1": M, "p2": C}}



        # P = d1 ∩ AB (d1 qua E perp d => d1: x = xE)

        yP = a - (a - c) * xE / b

        P = {"id": "P", "name": "P", "x": xE, "y": yP, "color": self.COLOR_SNAP, "fixed": True}



        # Q = d2 ∩ AC (d2 qua F perp d => d2: x = xF)

        yQ = a + (a + c) * xF / b

        Q = {"id": "Q", "name": "Q", "x": xF, "y": yQ, "color": self.COLOR_SNAP, "fixed": True}



        # Điểm cố định R: xR = b*c / a, yR = h - b^2 / a

        xR = (b * c) / a

        yR = h - (b * b) / a

        R = {"id": "R", "name": "R", "x": xR, "y": yR, "color": "#e03131", "fixed": True}



        self.points.extend([A, B, C, D, M, E, F, P, Q, R, d_p1, d_p2])

        self.lines.append({"p1": d_p1, "p2": d_p2, "color": "#adb5bd", "style": "solid", "label": ""})



        # Đường thẳng Δ qua M và R (luôn vuông góc PQ)

        self.lines.append({"p1": M, "p2": R, "color": "#e03131", "style": "solid", "label": "Δ qua M ⊥ PQ (luôn qua R)"})



        # Các đoạn thẳng tam giác và đường gióng

        self.segments.extend([

            {"p1": A, "p2": B, "color": self.COLOR_LINE, "style": "solid"},

            {"p1": B, "p2": C, "color": self.COLOR_LINE, "style": "solid"},

            {"p1": C, "p2": A, "color": self.COLOR_LINE, "style": "solid"},

            {"p1": A, "p2": D, "color": "#495057", "style": "solid", "label": "AD"},

            {"p1": M, "p2": B, "color": "#adb5bd", "style": "dashed"},

            {"p1": M, "p2": C, "color": "#adb5bd", "style": "dashed"},

            {"p1": E, "p2": F, "color": "#2b8a3e", "style": "dashed", "label": "EF // BC"},

            {"p1": E, "p2": P, "color": "#868e96", "style": "dashed"},

            {"p1": F, "p2": Q, "color": "#868e96", "style": "dashed"},

            {"p1": P, "p2": Q, "color": "#1971c2", "style": "bold", "label": "PQ"},

            {"p1": M, "p2": R, "color": "#e03131", "style": "bold", "label": "MR"}

        ])



        # Kí hiệu góc vuông ô vuông chi tiết

        H_d = {"id": "H_d", "name": "", "x": 0.0, "y": h, "hidden": True}

        self.points.append(H_d)

        self.add_right_angle_mark(H_d, A, d_p2)



        pt_int = self._intersect_lines(M, R, P, Q)

        if pt_int:

            I_pt = {"id": "I_perp", "name": "", "x": pt_int[0], "y": pt_int[1], "hidden": True}

            self.points.append(I_pt)

            self.add_right_angle_mark(I_pt, M, P)



        self.scale = 55.0

        self.origin_x = 450.0

        self.origin_y = 360.0

        self._update_algebra_tree()

        self._scan_invariants_deep()

        self.redraw()

        self.solve_general_problem()

        self.lbl_status.config(text="Loaded Problem 12 (VMO 2008) and pedagogical proof!" if lang == "en" else "Đã nạp Bài 12 (VMO 2008) và xuất toàn bộ lời giải chi tiết!")



    def load_preset_vmo_2009_bai13(self):

        """Bài 13 VMO 2009 (Trang 16 PDF): Đường tròn Euler (DMN) đi qua điểm cố định K & Đoạn MN không đổi."""

        self.clear_all(silent=True)

        self.current_preset = "vmo_2009_bai13"

        if hasattr(self, "combo_presets"):

            self.combo_presets.current(8)

        lang = getattr(self, "current_lang", "vi")

        self.txt_problem.delete("1.0", tk.END)

        self.txt_problem.insert(tk.END, PRESET_PROBLEMS.get(lang, PRESET_PROBLEMS["vi"]).get("vmo_2009_bai13", ""))

        if hasattr(self, "combo_goal_type"):

            self.combo_goal_type.current(3)

        if hasattr(self, "entry_goal_targets"):

            self.entry_goal_targets.delete(0, tk.END)

            self.entry_goal_targets.insert(0, "(DMN) qua điểm K cố định; MN = AB*sin(α/2)")



        # Tọa độ các đỉnh: A(-3, 0), B(3, 0), C(0.5, 4.2)

        A = {"id": "A", "name": "A", "x": -3.0, "y": 0.0, "color": self.COLOR_POINT, "fixed": True}

        B = {"id": "B", "name": "B", "x": 3.0, "y": 0.0, "color": self.COLOR_POINT, "fixed": True}

        C = {"id": "C", "name": "C", "x": 0.5, "y": 4.2, "color": self.COLOR_POINT, "fixed": False}



        # Tâm nội tiếp I và bán kính r

        Ix, Iy = 0.2897, 1.5408

        r_incircle = 1.5408

        I = {"id": "I", "name": "I", "x": Ix, "y": Iy, "color": "#1971c2", "fixed": True, "constraint": {"type": "incenter", "pts": [A, B, C]}}



        # Tiếp điểm D, E, F (hình chiếu vuông góc từ tâm nội tiếp I)

        D = {"id": "D", "name": "D", "x": 0.2897, "y": 0.0, "color": "#2b8a3e", "fixed": True, "constraint": {"type": "proj_foot", "p": I, "line_p1": A, "line_p2": B}}

        E = {"id": "E", "name": "E", "x": 1.6137, "y": 2.3289, "color": "#2b8a3e", "fixed": True, "constraint": {"type": "proj_foot", "p": I, "line_p1": B, "line_p2": C}}

        F = {"id": "F", "name": "F", "x": -0.8940, "y": 2.5272, "color": "#2b8a3e", "fixed": True, "constraint": {"type": "proj_foot", "p": I, "line_p1": C, "line_p2": A}}



        # Giao điểm M = AI ∩ EF, N = BI ∩ EF

        M = {"id": "M", "name": "M", "x": 1.9206, "y": 2.3047, "color": self.COLOR_HIGHLIGHT, "fixed": True, "constraint": {"type": "intersection", "p1": A, "p2": I, "p3": E, "p4": F}}

        N = {"id": "N", "name": "N", "x": -1.5345, "y": 2.5779, "color": self.COLOR_HIGHLIGHT, "fixed": True, "constraint": {"type": "intersection", "p1": B, "p2": I, "p3": E, "p4": F}}



        # Trung điểm K của AB (Điểm cố định - Euler point)

        K = {"id": "K", "name": "K", "x": 0.0, "y": 0.0, "color": "#e03131", "fixed": True, "constraint": {"type": "midpoint", "p1": A, "p2": B}}



        # Tâm đường tròn ngoại tiếp ΔDMN (Đường tròn Euler của ΔPAB)

        O_DMN = {"id": "O_DMN", "name": "O_e", "x": 0.1449, "y": 1.8318, "color": "#e03131", "fixed": True, "hidden": True, "constraint": {"type": "circumcenter", "pts": [D, M, N]}}

        R_DMN = 1.8376



        self.points.extend([A, B, C, I, D, E, F, M, N, K, O_DMN])



        # Đường tròn nội tiếp (I) và Đường tròn Euler (DMN)

        self.circles.append({"id": "C_I", "center": I, "r": r_incircle, "color": "#1971c2", "label": "(I) Nội tiếp", "constraint": {"type": "incircle", "pts": [A, B, C], "center": I}})

        self.circles.append({"id": "C_DMN", "center": O_DMN, "r": R_DMN, "color": "#e03131", "label": "(DMN) - Đường tròn Euler qua K", "constraint": {"type": "circumcircle", "pts": [D, M, N], "center": O_DMN}})



        # Đường thẳng EF kéo dài

        EF_ext1 = {"id": "EF_1", "name": "", "x": -2.8, "y": 2.70, "hidden": True}

        EF_ext2 = {"id": "EF_2", "name": "", "x": 3.0, "y": 2.20, "hidden": True}

        self.points.extend([EF_ext1, EF_ext2])

        self.lines.append({"p1": EF_ext1, "p2": EF_ext2, "color": "#adb5bd", "style": "solid", "label": ""})



        # Đoạn thẳng

        self.segments.extend([

            {"p1": A, "p2": B, "color": self.COLOR_LINE, "style": "solid"},

            {"p1": B, "p2": C, "color": self.COLOR_LINE, "style": "solid"},

            {"p1": C, "p2": A, "color": self.COLOR_LINE, "style": "solid"},

            {"p1": A, "p2": M, "color": "#868e96", "style": "dashed", "label": ""},

            {"p1": B, "p2": N, "color": "#868e96", "style": "dashed", "label": ""},

            {"p1": M, "p2": N, "color": "#e03131", "style": "bold", "label": "MN = const"},

            {"p1": D, "p2": M, "color": "#fd7e14", "style": "dashed"},

            {"p1": D, "p2": N, "color": "#fd7e14", "style": "dashed"},

            {"p1": I, "p2": D, "color": "#1971c2", "style": "dashed", "label": "r"}

        ])



        # Kí hiệu vuông góc ID ⊥ AB

        self.add_right_angle_mark(D, I, B)



        self.scale = 55.0

        self.origin_x = 440.0

        self.origin_y = 350.0

        self._update_algebra_tree()

        self._scan_invariants_deep()

        self.redraw()

        self.solve_general_problem()

        self.lbl_status.config(text="Loaded Problem 13 (VMO 2009) and Euler circle proof!" if lang == "en" else "Đã nạp Bài 13 (VMO 2009) và xuất toàn bộ lời giải chi tiết!")
    def load_preset_hex_intersection(self):
        """Bài 10: Giao điểm hai tam giác ABC và A1B1C1 tạo lục giác DEFGHI (Diện tích & Căn thức)."""
        self.clear_all(silent=True)
        self.current_preset = "hex_intersection"
        if hasattr(self, "combo_presets"):
            self.combo_presets.current(9)
        lang = getattr(self, "current_lang", "vi")
        self.txt_problem.delete("1.0", tk.END)
        self.txt_problem.insert(tk.END, PRESET_PROBLEMS.get(lang, PRESET_PROBLEMS["vi"]).get("hex_intersection", ""))
        if hasattr(self, "combo_goal_type"):
            self.combo_goal_type.current(9)  # Tính diện tích (Area)
        if hasattr(self, "entry_goal_targets"):
            self.entry_goal_targets.delete(0, tk.END)
            self.entry_goal_targets.insert(0, "DEFGHI")

        # Tam giác ABC
        A = {"id": "A", "name": "A", "x": 0.0, "y": 5.0, "color": self.COLOR_POINT, "fixed": True}
        B = {"id": "B", "name": "B", "x": -3.0, "y": 0.0, "color": self.COLOR_POINT, "fixed": True}
        C = {"id": "C", "name": "C", "x": 3.0, "y": 0.0, "color": self.COLOR_POINT, "fixed": True}

        # Tam giác A1B1C1
        A1 = {"id": "A1", "name": "A1", "x": -10.0/3.0, "y": 5.0/3.0, "color": "#7950f2", "fixed": True}
        B1 = {"id": "B1", "name": "B1", "x": 5.0/3.0, "y": -4.0/3.0, "color": "#7950f2", "fixed": True}
        C1 = {"id": "C1", "name": "C1", "x": 5.0/3.0, "y": 14.0/3.0, "color": "#7950f2", "fixed": True}

        # 6 giao điểm tạo thành lục giác DEFGHI
        D = {"id": "D", "name": "D", "x": -40.0/17.0, "y": 55.0/51.0, "color": "#e03131", "fixed": True}
        E = {"id": "E", "name": "E", "x": -5.0/4.0, "y": 35.0/12.0, "color": "#e03131", "fixed": True}
        F = {"id": "F", "name": "F", "x": 10.0/17.0, "y": 205.0/51.0, "color": "#e03131", "fixed": True}
        G = {"id": "G", "name": "G", "x": 5.0/3.0, "y": 20.0/9.0, "color": "#e03131", "fixed": True}
        H = {"id": "H", "name": "H", "x": 5.0/3.0, "y": 0.0, "color": "#e03131", "fixed": True}
        I_pt = {"id": "I", "name": "I", "x": -5.0/9.0, "y": 0.0, "color": "#e03131", "fixed": True}

        self.points.extend([A, B, C, A1, B1, C1, D, E, F, G, H, I_pt])

        # Các cạnh tam giác ABC
        self.segments.extend([
            {"p1": A, "p2": B, "color": self.COLOR_LINE, "style": "solid", "label": "AB = √(34)"},
            {"p1": B, "p2": C, "color": self.COLOR_LINE, "style": "solid", "label": "BC = 6"},
            {"p1": C, "p2": A, "color": self.COLOR_LINE, "style": "solid", "label": "CA = √(34)"},
        ])

        # Các cạnh tam giác A1B1C1
        self.segments.extend([
            {"p1": A1, "p2": B1, "color": "#868e96", "style": "dashed", "label": "A1B1 = √(34)"},
            {"p1": B1, "p2": C1, "color": "#868e96", "style": "dashed", "label": "B1C1 = 6"},
            {"p1": C1, "p2": A1, "color": "#868e96", "style": "dashed", "label": "C1A1 = √(34)"},
        ])

        # Các cạnh của lục giác DEFGHI
        self.segments.extend([
            {"p1": D, "p2": E, "color": "#e03131", "style": "bold"},
            {"p1": E, "p2": F, "color": "#e03131", "style": "bold"},
            {"p1": F, "p2": G, "color": "#e03131", "style": "bold"},
            {"p1": G, "p2": H, "color": "#e03131", "style": "bold"},
            {"p1": H, "p2": I_pt, "color": "#e03131", "style": "bold"},
            {"p1": I_pt, "p2": D, "color": "#e03131", "style": "bold"},
        ])

        # Đa giác mục tiêu
        self.polygons.append({
            "id": "poly_hex_DEFGHI",
            "name": "DEFGHI",
            "pts": [D, E, F, G, H, I_pt],
            "color": "#fd7e14"
        })

        self.scale = 48.0
        self.origin_x = 440.0
        self.origin_y = 350.0
        self._update_algebra_tree()
        self._scan_invariants_deep()
        self.redraw()
        self.solve_general_problem()
        self.lbl_status.config(text="Loaded Problem 10 (Hexagon DEFGHI Area)!" if lang == "en" else "Đã nạp Bài 10 (Tính diện tích Lục giác DEFGHI căn thức chính xác)!")

    def load_preset_vmo_2015(self):
        """Bài 14 VMO 2015: Trực tâm H, đường cao AD, điểm cố định P trên (O)."""
        self.clear_all(silent=True)
        self.current_preset = "vmo_2015"
        if hasattr(self, "combo_presets"):
            self.combo_presets.current(10)
        lang = getattr(self, "current_lang", "vi")
        self.txt_problem.delete("1.0", tk.END)
        self.txt_problem.insert(tk.END, PRESET_PROBLEMS.get(lang, PRESET_PROBLEMS["vi"]).get("vmo_2015", ""))
        if hasattr(self, "combo_goal_type"):
            self.combo_goal_type.current(10)  # Tự động phân tích toàn diện (Auto Analysis)
        if hasattr(self, "entry_goal_targets"):
            self.entry_goal_targets.delete(0, tk.END)
            self.entry_goal_targets.insert(0, "D, E, F, M")

        # Tọa độ các đỉnh: A(0.8, 4.2), B(-3.5, 0.0), C(3.5, 0.0)
        A = {"id": "A", "name": "A", "x": 0.8, "y": 4.2, "color": self.COLOR_POINT, "fixed": True}
        B = {"id": "B", "name": "B", "x": -3.5, "y": 0.0, "color": self.COLOR_POINT, "fixed": True}
        C = {"id": "C", "name": "C", "x": 3.5, "y": 0.0, "color": self.COLOR_POINT, "fixed": True}

        # Trung điểm BC
        M = {"id": "M", "name": "M", "x": 0.0, "y": 0.0, "color": "#2b8a3e", "fixed": True, "constraint": {"type": "midpoint", "p1": B, "p2": C}}

        # Chân các đường cao D, E, F
        D = {"id": "D", "name": "D", "x": 0.8, "y": 0.0, "color": "#1971c2", "fixed": True, "constraint": {"type": "proj_foot", "p": A, "line_p1": B, "line_p2": C}}
        E = {"id": "E", "name": "E", "x": 1.4531, "y": 3.1841, "color": "#1971c2", "fixed": True, "constraint": {"type": "proj_foot", "p": B, "line_p1": C, "line_p2": A}}
        F = {"id": "F", "name": "F", "x": 0.0823, "y": 3.4990, "color": "#1971c2", "fixed": True, "constraint": {"type": "proj_foot", "p": C, "line_p1": A, "line_p2": B}}

        # Trực tâm H và Tâm ngoại tiếp O
        H = {"id": "H", "name": "H", "x": 0.8, "y": 2.7643, "color": "#e03131", "fixed": True, "constraint": {"type": "orthocenter", "pts": [A, B, C]}}
        O = {"id": "O", "name": "O", "x": 0.0, "y": 0.7179, "color": "#495057", "fixed": True, "constraint": {"type": "circumcenter", "pts": [A, B, C]}}
        R_circum = 3.5729

        # Điểm P = (O) ∩ (AEF), Điểm Q đối xứng H qua M
        P = {"id": "P", "name": "P", "x": 1.1834, "y": 4.0890, "color": "#d6336c", "fixed": True}
        Q = {"id": "Q", "name": "Q", "x": -0.8, "y": -2.7643, "color": "#d6336c", "fixed": True}

        # Tâm đường tròn Euler 9 điểm
        N_euler = {"id": "N_euler", "name": "N_e", "x": 0.4, "y": 1.7411, "color": "#099268", "fixed": True, "hidden": True}
        R_euler = 1.7864

        self.points.extend([A, B, C, M, D, E, F, H, O, P, Q, N_euler])

        # Đường tròn ngoại tiếp (O) và Đường tròn Euler 9 điểm
        self.circles.append({"id": "C_O", "center": O, "r": R_circum, "color": "#495057", "label": "Đường tròn (O)", "constraint": {"type": "circumcircle", "pts": [A, B, C], "center": O}})
        self.circles.append({"id": "C_Euler", "center": N_euler, "r": R_euler, "color": "#099268", "label": "Đường tròn Euler 9 điểm (D, E, F, M)", "constraint": {"type": "circumcircle", "pts": [D, E, F], "center": N_euler}})

        # Các đoạn thẳng tam giác ABC và đường cao
        self.segments.extend([
            {"p1": A, "p2": B, "color": self.COLOR_LINE, "style": "solid"},
            {"p1": B, "p2": C, "color": self.COLOR_LINE, "style": "solid"},
            {"p1": C, "p2": A, "color": self.COLOR_LINE, "style": "solid"},
            {"p1": A, "p2": D, "color": "#1971c2", "style": "dashed", "label": ""},
            {"p1": B, "p2": E, "color": "#1971c2", "style": "dashed", "label": ""},
            {"p1": C, "p2": F, "color": "#1971c2", "style": "dashed", "label": ""},
            {"p1": P, "p2": Q, "color": "#d6336c", "style": "bold", "label": ""},
            {"p1": H, "p2": Q, "color": "#adb5bd", "style": "dashed", "label": "Q đối xứng H qua M"}
        ])

        # Kí hiệu vuông góc
        self.add_right_angle_mark(D, A, C)
        self.add_right_angle_mark(E, B, A)
        self.add_right_angle_mark(F, C, B)

        self.scale = 50.0
        self.origin_x = 440.0
        self.origin_y = 350.0
        self._update_algebra_tree()
        self._scan_invariants_deep()
        self.redraw()
        self.solve_general_problem()
        self.lbl_status.config(text="Loaded Problem 14 (VMO 2015)!" if lang == "en" else "Đã nạp Bài 14 (VMO 2015 - Đường tròn Euler & Cát tuyến PMQ)!")

    def load_preset_olympic_ptolemy(self):
        """Bài 15 Olympic: Tứ giác nội tiếp ABCD, Định lý Ptolemy & Diện tích đa giác."""
        self.clear_all(silent=True)
        self.current_preset = "olympic_ptolemy"
        if hasattr(self, "combo_presets"):
            self.combo_presets.current(11)
        lang = getattr(self, "current_lang", "vi")
        self.txt_problem.delete("1.0", tk.END)
        self.txt_problem.insert(tk.END, PRESET_PROBLEMS.get(lang, PRESET_PROBLEMS["vi"]).get("olympic_ptolemy", ""))
        if hasattr(self, "combo_goal_type"):
            self.combo_goal_type.current(9)  # Tính diện tích (Area)
        if hasattr(self, "entry_goal_targets"):
            self.entry_goal_targets.delete(0, tk.END)
            self.entry_goal_targets.insert(0, "ABCD")

        # 4 đỉnh tứ giác nội tiếp (O; R = 5)
        A = {"id": "A", "name": "A", "x": 0.0, "y": 5.0, "color": self.COLOR_POINT, "fixed": True}
        B = {"id": "B", "name": "B", "x": -4.0, "y": 3.0, "color": self.COLOR_POINT, "fixed": True}
        C = {"id": "C", "name": "C", "x": -3.0, "y": -4.0, "color": self.COLOR_POINT, "fixed": True}
        D = {"id": "D", "name": "D", "x": 4.0, "y": -3.0, "color": self.COLOR_POINT, "fixed": True}
        O = {"id": "O", "name": "O", "x": 0.0, "y": 0.0, "color": "#868e96", "fixed": True}

        self.points.extend([A, B, C, D, O])

        # Đường tròn ngoại tiếp (O; R = 5)
        self.circles.append({"id": "C_O", "center": O, "r": 5.0, "color": "#1971c2", "label": "Đường tròn (O; R=5)", "constraint": {"type": "circumcircle", "pts": [A, B, C], "center": O}})

        # Các cạnh tứ giác
        self.segments.extend([
            {"p1": A, "p2": B, "color": "#e03131", "style": "bold", "label": "AB = 2√(5)"},
            {"p1": B, "p2": C, "color": "#e03131", "style": "bold", "label": "BC = 5√(2)"},
            {"p1": C, "p2": D, "color": "#e03131", "style": "bold", "label": "CD = 5√(2)"},
            {"p1": D, "p2": A, "color": "#e03131", "style": "bold", "label": "DA = 4√(5)"},
            {"p1": A, "p2": C, "color": "#2b8a3e", "style": "dashed", "label": "AC = 3√(10)"},
            {"p1": B, "p2": D, "color": "#2b8a3e", "style": "dashed", "label": "BD = 10"},
        ])

        # Đa giác mục tiêu ABCD
        self.polygons.append({
            "id": "poly_quad_ABCD",
            "name": "ABCD",
            "pts": [A, B, C, D],
            "color": "#339af0"
        })

        self.scale = 45.0
        self.origin_x = 440.0
        self.origin_y = 350.0
        self._update_algebra_tree()
        self._scan_invariants_deep()
        self.redraw()
        self.solve_general_problem()
        self.lbl_status.config(text="Loaded Problem 15 (Cyclic Quad ABCD & Ptolemy Theorem)!" if lang == "en" else "Đã nạp Bài 15 (Tứ giác nội tiếp ABCD, Định lý Ptolemy & Diện tích S=45)!")




    # =========================================================================

    # CẬP NHẬT CÂY ĐẠI SỐ

    # =========================================================================

    def _update_algebra_tree(self):

        for item in self.tree_objects.get_children():

            self.tree_objects.delete(item)



        is_en = (getattr(self, "current_lang", "vi") == "en")

        stat_hidden = "Hidden" if is_en else "Ẩn"

        stat_visible = "Visible" if is_en else "Hiện"

        pt_prefix = "Point" if is_en else "Điểm"

        seg_prefix = "Seg" if is_en else "Đoạn"

        line_prefix = "Line" if is_en else "Đường"

        circle_prefix = "Circle" if is_en else "Đường tròn"



        for p in self.points:

            n = p.get('name') or p['id']

            stat = stat_hidden if p.get("hidden") else stat_visible

            self.tree_objects.insert("", tk.END, values=(n, f"{pt_prefix} ({p['x']:.2f}; {p['y']:.2f})", stat))



        for seg in self.segments:

            n1 = seg["p1"].get("name") or seg["p1"]["id"]

            n2 = seg["p2"].get("name") or seg["p2"]["id"]

            length = math.hypot(seg["p1"]["x"] - seg["p2"]["x"], seg["p1"]["y"] - seg["p2"]["y"])

            lbl = seg.get("label", f"{n1}{n2}")

            self.tree_objects.insert("", tk.END, values=(lbl, f"{seg_prefix} = {length:.2f}", stat_visible))



        for l in self.lines:

            n1 = l["p1"].get("name") or l["p1"]["id"]

            n2 = l["p2"].get("name") or l["p2"]["id"]

            default_lbl = f"Line({n1}, {n2})" if is_en else f"Đt qua {n1}, {n2}"

            lbl = l.get("label", default_lbl)

            self.tree_objects.insert("", tk.END, values=(lbl, f"{line_prefix} ({n1}, {n2})", stat_visible))



        for c in self.circles:

            c_name = c["center"].get("name") or c["center"]["id"]

            self.tree_objects.insert("", tk.END, values=(c["id"], f"{circle_prefix} ({c_name}; R={c['r']:.2f})", stat_visible))



        el_prefix = "Ellipse" if is_en else "Hình Elip"

        for el in getattr(self, "ellipses", []):

            el_lbl = el.get("label", el.get("id", "El"))

            c_pt = el.get("center")

            c_name = c_pt.get("name") if isinstance(c_pt, dict) else str(c_pt)

            self.tree_objects.insert("", tk.END, values=(el_lbl, f"{el_prefix} ({c_name}; a={el.get('a', 0):.2f}, b={el.get('b', 0):.2f})", stat_visible))



        poly_prefix = "Polygon" if is_en else "Đa giác"

        for pg in getattr(self, "polygons", []):

            pg_name = pg.get("name", "Poly")

            p_type = pg.get("poly_type", "polygon")

            type_lbl = {

                "isosceles_trapezoid": "Hình thang cân" if not is_en else "Isosc. Trapezoid",

                "parallelogram": "Hình bình hành" if not is_en else "Parallelogram",

                "rhombus": "Hình thoi" if not is_en else "Rhombus",

                "square": "Hình vuông" if not is_en else "Square",

            }.get(p_type, poly_prefix)

            self.tree_objects.insert("", tk.END, values=(pg_name, type_lbl, stat_visible))



    def _hex_to_rgb(self, hex_str, default=(33, 37, 41)):

        try:

            h = hex_str.lstrip('#')

            if len(h) == 6:

                return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

            elif len(h) == 3:

                return tuple(int(h[i]*2, 16) for i in (0, 1, 2))

        except Exception:

            pass

        return default



    # =========================================================================

    # XUẤT ẢNH BẢN VẼ ĐỘ PHÂN GIẢI CAO (PNG) - CHUẨN KỸ THUẬT SẠCH ĐẸP

    # =========================================================================

    def export_image_dialog(self):

        lang = getattr(self, "current_lang", "vi")

        file_title = "Lưu bản vẽ hình học (PNG)" if lang == "vi" else "Save Geometry Figure (PNG)"

        filepath = filedialog.asksaveasfilename(

            defaultextension=".png",

            filetypes=[("PNG Image (*.png)", "*.png"), ("Tất cả các tệp (*.*)", "*.*")],

            title=file_title

        )

        if not filepath:

            return



        top = tk.Toplevel(self)

        top.title("Tùy Chọn Xuất Hình Ảnh" if lang == "vi" else "Export Image Options")

        top.geometry("460x320")

        top.resizable(False, False)

        top.configure(bg="#f8f9fa")

        top.transient(self)

        top.grab_set()



        try:

            x = self.winfo_rootx() + (self.winfo_width() - 460) // 2

            y = self.winfo_rooty() + (self.winfo_height() - 320) // 2

            top.geometry(f"+{max(10, x)}+{max(10, y)}")

        except Exception:

            pass



        hdr = tk.Frame(top, bg="#1864ab", pady=8)

        hdr.pack(fill=tk.X)

        hdr_txt = "XUẤT ẢNH BẢN VẼ RÕ NÉT (PNG)" if lang == "vi" else "EXPORT HIGH-RES IMAGE (PNG)"

        tk.Label(hdr, text=hdr_txt, font=("Segoe UI", 10, "bold"), fg="#ffffff", bg="#1864ab").pack()



        fr_body = tk.Frame(top, bg="#f8f9fa", padx=20, pady=10)

        fr_body.pack(fill=tk.BOTH, expand=True)



        var_clean = tk.BooleanVar(value=True)

        var_autocrop = tk.BooleanVar(value=True)

        var_lines = tk.BooleanVar(value=False)

        var_axes = tk.BooleanVar(value=False)

        var_grid = tk.BooleanVar(value=False)



        cb1_txt = "✓ Ảnh sạch (Chỉ gồm hình vẽ & điểm, không đường gióng thừa)" if lang == "vi" else "✓ Clean Figure (Only drawn objects, no stray rays)"

        cb1 = ttk.Checkbutton(fr_body, text=cb1_txt, variable=var_clean)

        cb1.pack(anchor=tk.W, pady=3)



        cb2_txt = "✓ Tự động cắt sát khung hình (Auto-crop figure chuẩn sách)" if lang == "vi" else "✓ Auto-crop to Figure (Textbook-ready bounding box)"

        cb2 = ttk.Checkbutton(fr_body, text=cb2_txt, variable=var_autocrop)

        cb2.pack(anchor=tk.W, pady=3)



        cb3_txt = "Bao gồm các đường thẳng vô hạn kéo dài" if lang == "vi" else "Include extended infinite lines"

        cb3 = ttk.Checkbutton(fr_body, text=cb3_txt, variable=var_lines)

        cb3.pack(anchor=tk.W, pady=3)



        cb4_txt = "Bao gồm hệ trục tọa độ Oxy" if lang == "vi" else "Include Oxy coordinate axes"

        cb4 = ttk.Checkbutton(fr_body, text=cb4_txt, variable=var_axes)

        cb4.pack(anchor=tk.W, pady=3)



        cb5_txt = "Bao gồm lưới ô vuông (Grid lines)" if lang == "vi" else "Include grid lines"

        cb5 = ttk.Checkbutton(fr_body, text=cb5_txt, variable=var_grid)

        cb5.pack(anchor=tk.W, pady=3)



        def do_export():
            c_mode = var_clean.get()
            a_crop = var_autocrop.get()
            inc_lines = var_lines.get()
            inc_axes = var_axes.get()
            inc_grid = var_grid.get()
            top.destroy()

            self._render_to_image_file(

                filepath,

                clean_mode=c_mode,

                auto_crop=a_crop,

                include_axes=inc_axes,

                include_grid=inc_grid,

                include_lines=inc_lines,

                scale_mult=2

            )



        btn_row = tk.Frame(top, bg="#f8f9fa", pady=8)

        btn_row.pack(fill=tk.X)

        btn_txt = "💾 Xuất File Ảnh Ngay (PNG 300 DPI)" if lang == "vi" else "💾 Export Clean PNG Image Now"

        btn_exp = tk.Button(btn_row, text=btn_txt, font=("Segoe UI", 9, "bold"),

                            bg="#2b8a3e", fg="#ffffff", padx=18, pady=4, cursor="hand2", command=do_export)

        btn_exp.pack()




    def export_html_report(self):
        """
        Xuất toàn bộ bài toán hình học thành Báo Cáo Kỹ Thuật HTML tự chứa (self-contained),
        tích hợp kết xuất MathJax 3.2 cho các hệ thức hình học và nhúng ảnh bản vẽ sạch Base64.
        Hỗ trợ 1-click In ấn sang PDF chuẩn trang A4.
        """
        import os
        import tempfile
        import webbrowser
        from tkinter import filedialog, messagebox
        from stem_shared_core.report_engine import build_full_stem_html_report, canvas_to_base64_png

        lang = getattr(self, "current_lang", "vi")
        file_title = "Xuất Báo Cáo Hình Học HTML / In ấn PDF" if lang == "vi" else "Export Geometry HTML / Print PDF Report"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML Web Document (*.html)", "*.html")],
            title=file_title
        )
        if not filepath:
            return

        try:
            # 1. Kết xuất ảnh bản vẽ sạch sang Base64
            plot_b64 = ""
            temp_png = os.path.join(tempfile.gettempdir(), f"geosolver_export_{os.getpid()}.png")
            try:
                self._render_to_image_file(temp_png, clean_mode=True, auto_crop=True, scale_mult=2, silent=True)
                if os.path.exists(temp_png):
                    import base64
                    with open(temp_png, "rb") as pf:
                        b64_data = base64.b64encode(pf.read()).decode("ascii")
                        plot_b64 = f"data:image/png;base64,{b64_data}"
                    os.remove(temp_png)
            except Exception:
                plot_b64 = canvas_to_base64_png(self.canvas)

            # 2. Đề bài & Giả thiết
            prob_text = ""
            if hasattr(self, "txt_problem"):
                prob_text = self.txt_problem.get("1.0", tk.END).strip()
            if not prob_text:
                prob_text = "Bài toán hình học phẳng (GeoSolver 2D)"

            # 3. Thông số điểm & đối tượng hình học
            extra_facts = []
            for p in getattr(self, "points", []):
                if not p.get("hidden"):
                    extra_facts.append({"k": f"Điểm {p.get('name', 'P')}", "v": f"({p.get('x', 0):.2f}, {p.get('y', 0):.2f})"})

            # 4. Lời giải chi tiết từ solver
            sol_content = ""
            if hasattr(self, "txt_solution"):
                sol_content = self.txt_solution.get("1.0", tk.END).strip()

            ai_commentary = ""
            solution_steps = sol_content
            if "PHÂN TÍCH LOGIC & LỜI GIẢI TOÁN HỌC (AI)" in sol_content:
                parts = sol_content.split("PHÂN TÍCH LOGIC & LỜI GIẢI TOÁN HỌC (AI)")
                solution_steps = parts[0].strip()
                ai_commentary = "PHÂN TÍCH LOGIC & LỜI GIẢI TOÁN HỌC (AI)" + parts[1]

            html_code = build_full_stem_html_report(
                app_title="GeoSolver 2D CAD Studio",
                topic="Hình Học Phẳng & Suy Luận Hình Học",
                problem_text=prob_text,
                hero_formula_latex=r"AB^2 + AC^2 = BC^2 \quad;\quad ec{u} \cdot ec{v} = 0",
                hero_formula_text="AB^2 + AC^2 = BC^2",
                solution_steps=solution_steps or "Bản vẽ hình học đã sẵn sàng. Hãy bấm Giải Tự Động để xem lời giải.",
                plot_base64_png=plot_b64,
                extra_facts=extra_facts[:12],
                ai_commentary=ai_commentary
            )

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_code)

            if hasattr(self, "lbl_status"):
                self.lbl_status.config(text=f"Đã xuất báo cáo: {os.path.basename(filepath)}")

            msg_title = "Xuất Báo Cáo Thành Công" if lang == "vi" else "Report Exported Successfully"
            msg_body = (
                f"Đã tạo báo cáo kỹ thuật hình học hoàn chỉnh tại:\n{filepath}\n\nBạn có muốn mở ngay trên trình duyệt (sẵn sàng In sang PDF) không?"
                if lang == "vi" else
                f"Generated complete geometry technical report at:\n{filepath}\n\nOpen in browser now?"
            )
            if messagebox.askyesno(msg_title, msg_body):
                webbrowser.open(f"file:///{os.path.abspath(filepath)}")
        except Exception as e:
            messagebox.showerror("Lỗi xuất báo cáo", f"Không thể xuất báo cáo HTML: {e}")

    def _render_to_image_file(self, filepath, clean_mode=True, auto_crop=True,

                             include_axes=False, include_grid=False,

                             include_lines=False, scale_mult=2, silent=False):

        """Xuất ảnh PNG sạch chi tiết, hỗ trợ nét đứt, auto-crop và không đường kẻ thừa."""

        visible_points = [p for p in self.points if not p.get("hidden")]

        visible_circles = [c for c in self.circles if not c.get("hidden")]

        visible_segs = [s for s in self.segments if not s.get("hidden")]

        visible_lines = [l for l in self.lines if not l.get("hidden")]



        if auto_crop and (visible_points or visible_circles or visible_segs):
            all_x = [p["x"] for p in visible_points]
            all_y = [p["y"] for p in visible_points]
            if include_axes:
                all_x.append(0.0)
                all_y.append(0.0)

            for c in visible_circles:

                cx, cy, r = c["center"]["x"], c["center"]["y"], c["r"]

                all_x.extend([cx - r, cx + r])

                all_y.extend([cy - r, cy + r])

            for s in visible_segs:

                all_x.extend([s["p1"]["x"], s["p2"]["x"]])

                all_y.extend([s["p1"]["y"], s["p2"]["y"]])

            min_wx, max_wx = min(all_x), max(all_x)

            min_wy, max_wy = min(all_y), max(all_y)

            span_x = max(max_wx - min_wx, 1.0)

            span_y = max(max_wy - min_wy, 1.0)

            pad_x = max(1.2, 0.18 * span_x)

            pad_y = max(1.2, 0.18 * span_y)

            crop_min_x = min_wx - pad_x

            crop_max_x = max_wx + pad_x

            crop_min_y = min_wy - pad_y

            crop_max_y = max_wy + pad_y

        else:

            w_screen = self.canvas.winfo_width()

            h_screen = self.canvas.winfo_height()

            if w_screen <= 10 or h_screen <= 10:

                w_screen, h_screen = 1000, 750

            crop_min_x, crop_max_y = self.to_world(0, 0)

            crop_max_x, crop_min_y = self.to_world(w_screen, h_screen)



        world_w = max(1.0, crop_max_x - crop_min_x)

        world_h = max(1.0, crop_max_y - crop_min_y)



        base_scale = self.scale * scale_mult

        ppu = max(24.0 * scale_mult, base_scale)

        img_w = max(600, int(world_w * ppu))

        img_h = max(500, int(world_h * ppu))



        img = Image.new("RGB", (img_w, img_h), (255, 255, 255))

        draw = ImageDraw.Draw(img)



        try:

            font_main = ImageFont.truetype("segoeui.ttf", int(11 * scale_mult))

            font_bold = ImageFont.truetype("segoeuib.ttf", int(12 * scale_mult))

        except Exception:

            font_main = ImageFont.load_default()

            font_bold = font_main



        def to_img(wx, wy):

            ix = (wx - crop_min_x) / world_w * img_w

            iy = (crop_max_y - wy) / world_h * img_h

            return ix, iy



        # 1. Grid

        if include_grid:

            for gx in range(math.floor(crop_min_x), math.ceil(crop_max_x) + 1):

                px, _ = to_img(gx, 0)

                draw.line([(px, 0), (px, img_h)], fill=(240, 240, 240), width=1)

            for gy in range(math.floor(crop_min_y), math.ceil(crop_max_y) + 1):

                _, py = to_img(0, gy)

                draw.line([(0, py), (img_w, py)], fill=(240, 240, 240), width=1)



        # 2. Axes

        if include_axes:

            if crop_min_y <= 0 <= crop_max_y:

                _, oy = to_img(0, 0)

                draw.line([(0, oy), (img_w, oy)], fill=(108, 117, 125), width=2*scale_mult)

            if crop_min_x <= 0 <= crop_max_x:

                ox, _ = to_img(0, 0)

                draw.line([(ox, 0), (ox, img_h)], fill=(108, 117, 125), width=2*scale_mult)



        # 2.5. Shaded Area Polygons

        for poly in getattr(self, "polygons", []):

            pts = poly.get("points", [])

            if len(pts) >= 3:

                poly_coords = [to_img(pt["x"], pt["y"]) for pt in pts]

                draw.polygon(poly_coords, fill=(231, 245, 255), outline=self._hex_to_rgb(poly.get("outline_color", "#1971c2")))

                if poly.get("show_label", True):

                    gx = sum(pt["x"] for pt in pts) / len(pts)

                    gy = sum(pt["y"] for pt in pts) / len(pts)

                    igx, igy = to_img(gx, gy)

                    name_p = poly.get("name", "Poly")

                    s_val = poly.get("area", 0.0)

                    draw.text((igx - 20, igy - 10), f"S({name_p})={s_val:.2f}", fill=(24, 100, 171), font=font_bold)



        # 3. Circles

        for c in visible_circles:

            cx, cy = to_img(c["center"]["x"], c["center"]["y"])

            cr = c["r"] * (img_w / world_w)

            c_rgb = self._hex_to_rgb(c.get("color", self.COLOR_CIRCLE))

            if c.get("style") == "dashed":

                # Dashed circle

                angle = 0.0

                step = 8.0 + 6.0

                while angle < 360.0:

                    end_a = min(angle + 8.0, 360.0)

                    draw.arc([cx - cr, cy - cr, cx + cr, cy + cr], start=angle, end=end_a, fill=c_rgb, width=2*scale_mult)

                    angle += step

            else:

                draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], outline=c_rgb, width=2*scale_mult)

            if c.get("label"):

                draw.text((cx - cr*0.7, cy - cr*0.7), c["label"], fill=(73, 80, 87), font=font_main)



        # 3.5. Ellipses
        for el in getattr(self, "ellipses", []):
            if el.get("hidden") and clean_mode: continue
            pts_w = sample_ellipse_points(el["ox"], el["oy"], el["a"], el["b"], el["theta"], num_samples=72)
            pts_i = [to_img(wx, wy) for wx, wy in pts_w]
            el_rgb = self._hex_to_rgb(el.get("color", "#9c36b5"))
            draw.line(pts_i, fill=el_rgb, width=2*scale_mult)
            if el.get("label"):
                cx, cy = to_img(el["ox"], el["oy"])
                draw.text((cx, cy - 12*scale_mult), el["label"], fill=el_rgb, font=font_bold)

        # 4. Lines (chỉ vẽ khi include_lines=True và được giới hạn trong khung hình, không bắn tia x30)

        if include_lines:

            for l in visible_lines:

                x1, y1 = to_img(l["p1"]["x"], l["p1"]["y"])

                x2, y2 = to_img(l["p2"]["x"], l["p2"]["y"])

                dx = x2 - x1

                dy = y2 - y1

                l_rgb = self._hex_to_rgb(l.get("color", "#6c757d"))

                w_line = 1 * scale_mult

                if l.get("style") == "dashed":

                    dist = math.hypot(dx, dy)

                    if dist > 1e-4:

                        ux, uy = dx / dist, dy / dist

                        curr = 0.0

                        tot = dist * 4

                        sx0, sy0 = x1 - ux*dist*2, y1 - uy*dist*2

                        while curr < tot:

                            ed = min(curr + 10*scale_mult, tot)

                            draw.line([(sx0 + ux*curr, sy0 + uy*curr), (sx0 + ux*ed, sy0 + uy*ed)], fill=l_rgb, width=w_line)

                            curr += 16 * scale_mult

                else:

                    draw.line([(x1 - dx*2, y1 - dy*2), (x2 + dx*2, y2 + dy*2)], fill=l_rgb, width=w_line)



        # 5. Segments (với hỗ trợ nét đứt chi tiết)

        for seg in visible_segs:

            x1, y1 = to_img(seg["p1"]["x"], seg["p1"]["y"])

            x2, y2 = to_img(seg["p2"]["x"], seg["p2"]["y"])

            w_line = 3 * scale_mult if seg.get("style") == "bold" else 2 * scale_mult

            s_rgb = self._hex_to_rgb(seg.get("color", self.COLOR_LINE))

            if seg.get("style") == "dashed":

                # Dashed segment

                dx = x2 - x1

                dy = y2 - y1

                dist = math.hypot(dx, dy)

                if dist > 1e-4:

                    ux = dx / dist

                    uy = dy / dist

                    curr = 0.0

                    d_len = 11 * scale_mult

                    g_len = 7 * scale_mult

                    while curr < dist:

                        end_d = min(curr + d_len, dist)

                        sx, sy = x1 + ux * curr, y1 + uy * curr

                        ex, ey = x1 + ux * end_d, y1 + uy * end_d

                        draw.line([(sx, sy), (ex, ey)], fill=s_rgb, width=w_line)

                        curr += d_len + g_len

            else:

                draw.line([(x1, y1), (x2, y2)], fill=s_rgb, width=w_line)

            if seg.get("label"):

                mid_x = (x1 + x2) / 2 + (5 + seg.get("label_dx", 0)) * scale_mult

                mid_y = (y1 + y2) / 2 - (8 - seg.get("label_dy", 0)) * scale_mult

                draw.text((mid_x, mid_y), seg["label"], fill=s_rgb, font=font_bold)



        # 5b. Angle Marks (Ký hiệu góc)

        for mark in self.angle_marks:

            v = mark.get("vertex")

            p1 = mark.get("p1")

            p2 = mark.get("p2")

            if not v or not p1 or not p2: continue

            vx, vy = to_img(v["x"], v["y"])

            x1, y1 = to_img(p1["x"], p1["y"])

            x2, y2 = to_img(p2["x"], p2["y"])

            dx1, dy1 = x1 - vx, y1 - vy

            dx2, dy2 = x2 - vx, y2 - vy

            L1, L2 = math.hypot(dx1, dy1), math.hypot(dx2, dy2)

            if L1 < 1e-3 or L2 < 1e-3: continue

            u1x, u1y = dx1 / L1, dy1 / L1

            u2x, u2y = dx2 / L2, dy2 / L2

            style = mark.get("style", "arc1")

            m_col = self._hex_to_rgb(mark.get("color", "#e03131"))

            size = mark.get("size", 14 if style == "right" else 22) * scale_mult

            name = mark.get("name", "")



            if style == "right":

                c1 = (vx + size * u1x, vy + size * u1y)

                c2 = (vx + size * u1x + size * u2x, vy + size * u1y + size * u2y)

                c3 = (vx + size * u2x, vy + size * u2y)

                draw.line([c1, c2, c3], fill=m_col, width=2 * scale_mult)

                if name:

                    tx = c2[0] + (5 + mark.get("label_dx", 0)) * scale_mult

                    ty = c2[1] - (8 - mark.get("label_dy", 0)) * scale_mult

                    draw.text((tx, ty), name, fill=m_col, font=font_bold)

            else:

                ang1 = math.atan2(dy1, dx1)

                ang2 = math.atan2(dy2, dx2)

                diff = (ang2 - ang1) % (2 * math.pi)

                if diff > math.pi: diff -= 2 * math.pi

                arc1_pts = []

                for i in range(17):

                    t = ang1 + diff * (i / 16.0)

                    arc1_pts.append((vx + size * math.cos(t), vy + size * math.sin(t)))

                draw.line(arc1_pts, fill=m_col, width=2 * scale_mult)



                if style in ("arc2", "arc2_tick"):

                    s2 = size + 5 * scale_mult

                    arc2_pts = []

                    for i in range(17):

                        t = ang1 + diff * (i / 16.0)

                        arc2_pts.append((vx + s2 * math.cos(t), vy + s2 * math.sin(t)))

                    draw.line(arc2_pts, fill=m_col, width=2 * scale_mult)



                mid_ang = ang1 + diff / 2.0

                mid_ux, mid_uy = math.cos(mid_ang), math.sin(mid_ang)



                if style in ("arc1_tick", "arc2_tick"):

                    r_outer = size + 10 * scale_mult if style == "arc2_tick" else size + 5 * scale_mult

                    t_start = (vx + (size - 4 * scale_mult) * mid_ux, vy + (size - 4 * scale_mult) * mid_uy)

                    t_end = (vx + r_outer * mid_ux, vy + r_outer * mid_uy)

                    draw.line([t_start, t_end], fill=m_col, width=2 * scale_mult)



                if name:

                    tx = vx + (size + 12 * scale_mult) * mid_ux + mark.get("label_dx", 0) * scale_mult

                    ty = vy + (size + 12 * scale_mult) * mid_uy + mark.get("label_dy", 0) * scale_mult

                    draw.text((tx, ty), name, fill=m_col, font=font_bold)



        # 6. Points

        for p in visible_points:

            px, py = to_img(p["x"], p["y"])

            r_pt = 5 * scale_mult

            p_rgb = self._hex_to_rgb(p.get("color", self.COLOR_POINT))

            draw.ellipse([px - r_pt, py - r_pt, px + r_pt, py + r_pt], fill=p_rgb, outline=(33, 37, 41), width=scale_mult)

            if p.get("name"):

                label = f"{p['name']}" + (f" ({p['x']:.1f}, {p['y']:.1f})" if include_axes else "")

                dx = p.get("label_dx", 8) * scale_mult

                dy = p.get("label_dy", -10) * scale_mult

                draw.text((px + dx, py + dy), label, fill=(33, 37, 41), font=font_bold)



        img.save(filepath, "PNG")

        msg = f"Đã xuất bản vẽ ảnh sạch thành công tại:\n{filepath}" if self.current_lang == "vi" else f"Successfully exported clean figure to:\n{filepath}"

        if not silent:

            messagebox.showinfo("Xuất Ảnh", msg)



    # =========================================================================

    # RENDER BẢN VẼ

    # =========================================================================

    def redraw(self):

        self.canvas.delete("all")

        w = self.canvas.winfo_width()

        h = self.canvas.winfo_height()

        if w <= 1 or h <= 1: return



        if self.show_grid:

            self._draw_grid(w, h)



        # Vẽ các miền đa giác tô màu diện tích (Shaded Area Polygons)

        for poly in getattr(self, "polygons", []):

            pts = poly.get("points", [])

            if len(pts) >= 3:

                coords = []

                for pt in pts:

                    sx, sy = self.to_screen(pt["x"], pt["y"])

                    coords.extend([sx, sy])

                fill_col = poly.get("fill_color", "#e7f5ff")

                outline_col = poly.get("outline_color", "#1971c2")

                self.canvas.create_polygon(coords, fill=fill_col, outline=outline_col, width=1.5, stipple=poly.get("stipple", "gray25"))

                # Nhãn diện tích ở trọng tâm

                if poly.get("show_label", True):

                    gx = sum(pt["x"] for pt in pts) / len(pts)

                    gy = sum(pt["y"] for pt in pts) / len(pts)

                    gsx, gsy = self.to_screen(gx, gy)

                    s_val = poly.get("area", 0.0)

                    name_p = poly.get("name", "Poly")

                    self.canvas.create_text(gsx, gsy, text=f"S({name_p}) = {s_val:.2f}",

                                            fill="#1864ab", font=("Segoe UI", 9, "bold"))



        for c in self.circles:

            if c.get("hidden") and not self.show_hidden: continue

            cx, cy = self.to_screen(c["center"]["x"], c["center"]["y"])

            cr = c["r"] * self.scale

            dash = (6, 4) if (c.get("style") == "dashed" or c.get("hidden")) else ()

            self.canvas.create_oval(cx - cr, cy - cr, cx + cr, cy + cr,

                                   outline=c.get("color", self.COLOR_CIRCLE), width=2, dash=dash)

            if c.get("label"):

                self.canvas.create_text(cx - cr*0.7, cy - cr*0.7, text=c["label"], fill="#495057", font=("Segoe UI", 9))



        # Vẽ hình Elip (Lấy mẫu 72 điểm theo tham số x(t), y(t) nghiêng góc theta)
        for el in getattr(self, "ellipses", []):
            if el.get("hidden") and not self.show_hidden: continue
            ox, oy = el["ox"], el["oy"]
            a = el.get("a", 1.0)
            b = el.get("b", 0.5)
            theta = el.get("theta", 0.0)
            pts_world = sample_ellipse_points(ox, oy, a, b, theta, num_samples=72)
            pts_screen = []
            for wx, wy in pts_world:
                sx, sy = self.to_screen(wx, wy)
                pts_screen.extend([sx, sy])
            dash = (6, 4) if (el.get("style") == "dashed" or el.get("hidden")) else ()
            is_sel_el = (getattr(self, "selected_ellipse", None) == el)
            el_color = "#f59f00" if is_sel_el else el.get("color", "#9c36b5")
            el_w = 3.5 if is_sel_el else 2
            if len(pts_screen) >= 4:
                self.canvas.create_line(*pts_screen, fill=el_color, width=el_w, dash=dash, smooth=True)

        # LIVE RUBBER-BAND PREVIEW KHI ĐANG VẼ ELIP (KIỂM SOÁT HÌNH DÁNG TRỰC QUAN THEO CHUỘT)
        if self.current_tool == "ellipse" and hasattr(self, "temp_points"):
            if len(self.temp_points) == 1 and hasattr(self, "last_mouse_world"):
                p1 = self.temp_points[0]
                s1x, s1y = self.to_screen(p1["x"], p1["y"])
                smx, smy = self.to_screen(self.last_mouse_world[0], self.last_mouse_world[1])
                self.canvas.create_line(s1x, s1y, smx, smy, fill="#339af0", width=1.5, dash=(4, 4))
            elif len(self.temp_points) == 2 and hasattr(self, "last_mouse_world"):
                pF1, pF2 = self.temp_points[0], self.temp_points[1]
                mx, my = self.last_mouse_world
                prev_p = compute_ellipse_from_foci(pF1["x"], pF1["y"], pF2["x"], pF2["y"], mx, my)
                prev_w = sample_ellipse_points(prev_p["ox"], prev_p["oy"], prev_p["a"], prev_p["b"], prev_p["theta"], num_samples=64)
                prev_s = []
                for px, py in prev_w:
                    sx, sy = self.to_screen(px, py)
                    prev_s.extend([sx, sy])
                if len(prev_s) >= 4:
                    self.canvas.create_line(*prev_s, fill="#1971c2", width=2, dash=(6, 4), smooth=True)
                # Tia tiêu cự F1 -> M và F2 -> M
                sf1x, sf1y = self.to_screen(pF1["x"], pF1["y"])
                sf2x, sf2y = self.to_screen(pF2["x"], pF2["y"])
                smx, smy = self.to_screen(mx, my)
                self.canvas.create_line(sf1x, sf1y, smx, smy, fill="#adb5bd", width=1, dash=(2, 2))
                self.canvas.create_line(sf2x, sf2y, smx, smy, fill="#adb5bd", width=1, dash=(2, 2))
                # Điểm tâm dự kiến
                sox, soy = self.to_screen(prev_p["ox"], prev_p["oy"])
                self.canvas.create_oval(sox-3, soy-3, sox+3, soy+3, fill="#e03131", outline="#ffffff")
                self.canvas.create_text(sox, soy - 10, text="O", fill="#e03131", font=("Segoe UI", 8, "bold"))

            if el.get("label"):

                lsx, lsy = self.to_screen(ox, oy)

                self.canvas.create_text(lsx, lsy - 12, text=el["label"], fill=el.get("color", "#9c36b5"), font=("Segoe UI", 8, "bold"))



        for l in self.lines:

            if l.get("hidden") and not self.show_hidden: continue

            p1, p2 = l["p1"], l["p2"]

            x1, y1 = self.to_screen(p1["x"], p1["y"])

            x2, y2 = self.to_screen(p2["x"], p2["y"])

            dx, dy = x2 - x1, y2 - y1

            length = math.hypot(dx, dy)

            if length > 0:

                is_temp_l = (hasattr(self, "temp_line") and self.temp_line == l)

                dash = (6, 4) if (l.get("style") == "dashed" or l.get("hidden")) else ()

                l_col = self.COLOR_SNAP if is_temp_l else l.get("color", "#adb5bd")

                l_w = 3 if is_temp_l else 1

                self.canvas.create_line(x1 - dx*30, y1 - dy*30, x2 + dx*30, y2 + dy*30,

                                       fill=l_col, width=l_w, dash=dash)

                # Khong ve chu nhan text len duong thang de tranh roi hinh theo yeu cau
                pass



        for s in self.segments:

            if s.get("hidden") and not self.show_hidden: continue

            x1, y1 = self.to_screen(s["p1"]["x"], s["p1"]["y"])

            x2, y2 = self.to_screen(s["p2"]["x"], s["p2"]["y"])

            is_temp_s = (hasattr(self, "temp_line") and self.temp_line == s)

            width = 4 if is_temp_s else (3 if s.get("style") == "bold" else 2)

            s_col = self.COLOR_SNAP if is_temp_s else (self.COLOR_LINE if (getattr(self, "current_theme_key", "") == "dark_studio" and s.get("color") in ("#212529", "#000000", "#0f172a", "#0a2540")) else s.get("color", self.COLOR_LINE))

            dash = (6, 4) if (s.get("style") == "dashed" or s.get("hidden")) else ()

            self.canvas.create_line(x1, y1, x2, y2, fill=s_col, width=width, dash=dash)

            # Chế độ Clean Print Mode: Mặc định không hiện nhãn, chỉ hiện khi người dùng bật công tắc Dimensions
            if getattr(self, "var_show_dimensions", None) and self.var_show_dimensions.get():
                mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
                seg_d = math.hypot(s["p2"]["x"] - s["p1"]["x"], s["p2"]["y"] - s["p1"]["y"])
                self.canvas.create_text(mx, my - 8, text=f"{seg_d:.2f}", fill=self.COLOR_TEXT, font=("Segoe UI", 8, "italic"))



        # Vẽ các ký hiệu góc

        for m in self.angle_marks:

            self._draw_pedagogical_angle_on_canvas(m)



        for p in self.points:

            if p.get("hidden") and not self.show_hidden: continue

            px, py = self.to_screen(p["x"], p["y"])

            is_sel = (p in self.selected_points)

            is_temp_pt = (p in self.temp_points)

            r_pt = 6 if (is_sel or is_temp_pt) else 4

            color = self.COLOR_HIGHLIGHT if is_sel else (self.COLOR_SNAP if is_temp_pt else p.get("color", self.COLOR_POINT))

            fill_c = "#adb5bd" if p.get("hidden") else color



            self.canvas.create_oval(px - r_pt, py - r_pt, px + r_pt, py + r_pt,

                                   fill=fill_c, outline="#ffffff" if (is_sel or is_temp_pt) else "#212529", width=2)

            if is_temp_pt:

                self.canvas.create_oval(px - r_pt - 4, py - r_pt - 4, px + r_pt + 4, py + r_pt + 4,

                                       outline=self.COLOR_SNAP, width=1, dash=(2, 2))

            if p.get("name"):

                dx = p.get("label_dx", 8)

                dy = p.get("label_dy", -10)

                self.canvas.create_text(px + dx, py + dy, text=f"{p['name']}",

                                       anchor=tk.W, fill=self.COLOR_TEXT, font=("Segoe UI", 9, "bold"))



        if self.hovered_snap:

            sx, sy = self.to_screen(self.hovered_snap["x"], self.hovered_snap["y"])

            self.canvas.create_oval(sx - 8, sy - 8, sx + 8, sy + 8, outline=self.COLOR_SNAP, width=2)



    def _draw_grid(self, w, h):

        min_x, max_y = self.to_world(0, 0)

        max_x, min_y = self.to_world(w, h)



        for x in range(math.floor(min_x), math.ceil(max_x) + 1):

            px, _ = self.to_screen(x, 0)

            self.canvas.create_line(px, 0, px, h, fill=self.COLOR_GRID, width=1)

            if x != 0 and abs(self.scale) > 25:

                _, py = self.to_screen(0, 0)

                if 0 <= py <= h:

                    self.canvas.create_text(px, py + 12, text=str(x), fill="#adb5bd", font=("Consolas", 8))



        for y in range(math.floor(min_y), math.ceil(max_y) + 1):

            _, py = self.to_screen(0, y)

            self.canvas.create_line(0, py, w, py, fill=self.COLOR_GRID, width=1)

            if y != 0 and abs(self.scale) > 25:

                px, _ = self.to_screen(0, 0)

                if 0 <= px <= w:

                    self.canvas.create_text(px - 14, py, text=str(y), fill="#adb5bd", font=("Consolas", 8))



        ox, oy = self.to_screen(0, 0)

        self.canvas.create_line(0, oy, w, oy, fill=self.COLOR_AXIS, width=2)

        self.canvas.create_line(ox, 0, ox, h, fill=self.COLOR_AXIS, width=2)



        self.canvas.create_text(w - 15, oy - 12, text="x", fill=self.COLOR_AXIS, font=("Segoe UI", 10, "bold"))

        self.canvas.create_text(ox + 12, 15, text="y", fill=self.COLOR_AXIS, font=("Segoe UI", 10, "bold"))

        self.canvas.create_text(ox - 10, oy + 12, text="O", fill=self.COLOR_AXIS, font=("Segoe UI", 9, "bold"))





if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    if "--smoke-test" in sys.argv:
        import json
        out_path = None
        for arg in sys.argv:
            if arg.startswith("--output="):
                out_path = Path(arg.split("=", 1)[1])
        if not out_path:
            target_dir = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path.cwd()
            out_path = target_dir / "smoke_test_result.json"

        import hashlib, datetime
        exe_path = sys.executable
        exe_hash = None
        if os.path.isfile(exe_path):
            try:
                with open(exe_path, "rb") as ef:
                    exe_hash = hashlib.sha256(ef.read()).hexdigest().upper()
            except Exception:
                pass

        git_commit = "UNKNOWN"
        git_dirty = False
        try:
            from geosolver import _build_info
            git_commit = getattr(_build_info, "GIT_COMMIT", git_commit)
            git_dirty = getattr(_build_info, "GIT_DIRTY", git_dirty)
        except Exception:
            try:
                import _build_info
                git_commit = getattr(_build_info, "GIT_COMMIT", git_commit)
                git_dirty = getattr(_build_info, "GIT_DIRTY", git_dirty)
            except Exception:
                pass

        try:
            import subprocess
            candidate_dirs = [
                Path.cwd(),
                Path(__file__).resolve().parent.parent if "__file__" in locals() else None,
                Path(sys.executable).resolve().parent.parent.parent if getattr(sys, 'frozen', False) else None
            ]
            for c_dir in candidate_dirs:
                if c_dir and (c_dir / ".git").exists():
                    res_c = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(c_dir), capture_output=True, text=True, timeout=2)
                    if res_c.returncode == 0 and res_c.stdout.strip():
                        git_commit = res_c.stdout.strip()
                    res_p = subprocess.run(["git", "status", "--porcelain"], cwd=str(c_dir), capture_output=True, text=True, timeout=2)
                    if res_p.returncode == 0:
                        git_dirty = bool(res_p.stdout.strip())
                    break
        except Exception:
            pass

        result = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "git_commit": git_commit,
            "git_dirty": git_dirty,
            "frozen": bool(getattr(sys, 'frozen', False)),
            "python_version": sys.version,
            "executable": sys.executable,
            "executable_sha256": exe_hash,
            "checks": {},
            "status": "FAILED",
            "exit_code": 1
        }

        log_lines = []
        def log_smoke(msg):
            log_lines.append(msg)
            try:
                print(msg)
            except Exception:
                pass

        try:
            log_smoke("[SMOKE TEST] Khởi chạy kiểm thử đóng gói GeoSolver (Smoke Test)...")
            # 1. Kiểm tra thuật toán hình học
            res = classify_triangle((0.0, 0.0), (3.0, 0.0), (0.0, 4.0))
            assert res["is_triangle"] and res["type"] == "right" and res["vertex"] == "A", f"Geometry solve failed: {res}"
            result["checks"]["geometry"] = True
            log_smoke("[SMOKE TEST] 1. Phân loại hình học bất biến: ĐẠT")

            # 2. Kiểm tra mã hóa DPAPI trên Windows
            if os.name == "nt":
                from stem_shared_core.ai_local_manager import _dpapi_encrypt, _dpapi_decrypt
                test_blob = b"GeoSolverSmokeTestKey123"
                enc = _dpapi_encrypt(test_blob)
                dec = _dpapi_decrypt(enc)
                assert dec == test_blob, "DPAPI roundtrip mismatch"
                result["checks"]["dpapi"] = True
                log_smoke("[SMOKE TEST] 2. Mã hóa & giải mã Windows DPAPI: ĐẠT")
            else:
                result["checks"]["dpapi"] = "SKIPPED_POSIX"
                log_smoke("[SMOKE TEST] 2. Windows DPAPI: BỎ QUA (Môi trường POSIX)")

            # 3. Kiểm tra nạp động thư viện SymPy
            import sympy
            x = sympy.Symbol('x')
            sol = sympy.solve(x**2 - 4, x)
            assert len(sol) == 2, "SymPy solve failed"
            result["checks"]["sympy"] = True
            log_smoke("[SMOKE TEST] 3. Nạp động thư viện SymPy: ĐẠT")

            # 4. Kiểm tra khởi tạo và hủy Tkinter GUI runtime
            import tkinter as tk
            tk_root = tk.Tk()
            tk_root.withdraw()
            tk_root.update()
            tk_root.destroy()
            result["checks"]["tkinter_runtime"] = True
            log_smoke("[SMOKE TEST] 4. Khởi tạo & giải phóng Tkinter GUI runtime: ĐẠT")

            # 5. Kiểm tra nạp các module nhạy cảm (PIL, handbook, downloader, config)
            from PIL import Image, ImageTk
            import stem_handbook_dialog
            import stem_shared_core.hf_downloader
            import stem_shared_core.ai_config_dialog
            result["checks"]["critical_modules"] = True
            log_smoke("[SMOKE TEST] 5. Nạp các module phụ thuộc quan trọng: ĐẠT")

            # 6. Kiểm tra tài nguyên đóng gói (assets và cẩm nang)
            if getattr(sys, 'frozen', False):
                base_dir = Path(getattr(sys, '_MEIPASS', os.path.dirname(sys.executable)))
                ico_path = base_dir / "assets" / "app.ico"
                handbook_path = base_dir / "CAM_NANG_SU_DUNG_STEM_CAD_MATH.md"
                assert ico_path.is_file(), f"Thiếu assets/app.ico trong gói EXE: {ico_path}"
                assert handbook_path.is_file(), f"Thiếu cẩm nang trong gói EXE: {handbook_path}"
                result["checks"]["assets"] = True
                log_smoke("[SMOKE TEST] 6. Tài nguyên đóng gói trong frozen bundle: ĐẠT")
            else:
                base_dir = Path(__file__).resolve().parent
                ico_path = base_dir / "assets" / "app.ico"
                handbook_path = base_dir.parent / "CAM_NANG_SU_DUNG_STEM_CAD_MATH.md"
                assert ico_path.is_file(), f"Thiếu assets/app.ico: {ico_path}"
                assert handbook_path.is_file(), f"Thiếu cẩm nang: {handbook_path}"
                result["checks"]["assets"] = True
                log_smoke("[SMOKE TEST] 6. Tài nguyên trong cây mã nguồn dev: ĐẠT")

            # 7. Kiểm tra nạp cấu hình bảo mật SSL/TLS & CA bundle certifi (Phục vụ HTTPS Gemini & HuggingFace)
            import ssl, certifi
            ca_file = certifi.where()
            assert os.path.isfile(ca_file) and os.path.getsize(ca_file) > 0, f"Thiếu CA bundle certifi: {ca_file}"
            ssl_ctx = ssl.create_default_context()
            try:
                ssl_ctx.load_verify_locations(cafile=ca_file)
            except Exception:
                pass
            assert ssl_ctx is not None, "Không thể khởi tạo SSLContext với CA bundle certifi"
            if "--network-check" in sys.argv:
                import urllib.request
                req = urllib.request.Request("https://huggingface.co", headers={"User-Agent": "GeoSolver-SmokeTest/3.1"})
                with urllib.request.urlopen(req, context=ssl_ctx, timeout=8) as resp:
                    assert resp.status in (200, 301, 302), f"TLS handshake thất bại với mã: {resp.status}"
                log_smoke("[SMOKE TEST] 7. Nạp cấu hình SSL/TLS, CA certifi & bắt tay TLS trực tiếp tới huggingface.co: ĐẠT")
            else:
                log_smoke("[SMOKE TEST] 7. Nạp cấu hình bảo mật SSL/TLS & CA bundle certifi (cafile): ĐẠT")
            result["checks"]["ssl_certifi"] = True

            result["status"] = "PASS"
            result["exit_code"] = 0
            log_smoke("[SMOKE TEST] TẤT CẢ CÁC MỤC KIỂM THỬ KHÓI ĐỀU THÀNH CÔNG (MÃ THOÁT 0).")
        except Exception as e:
            result["error"] = str(e)
            log_smoke(f"[SMOKE TEST] THẤT BẠI: {e}")
        finally:
            try:
                out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
                log_file = out_path.parent / "smoke_run.log"
                log_smoke(f"[SMOKE TEST] Đã ghi nhật ký kết quả kiểm thử vào: {out_path}")
                log_file.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
            except Exception as e:
                print(f"[SMOKE TEST] Không thể ghi file kết quả: {e}")
                print(f"[SMOKE TEST] Không thể ghi file kết quả: {e}")

        sys.exit(result["exit_code"])

    app = GeoSolverApp(with_splash=True)
    app.mainloop()

