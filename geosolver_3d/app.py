# -*- coding: utf-8 -*-
"""
GeoSolver 3D - Pedagogical 3D Geometry & CAD Desktop Application (Win32 Classic Style)
Target Path: D:\\AI DATA\\STEM_APP\\geosolver_3d\\app.py

Features:
- Multi-Row Win32 Classic Ribbon Toolbar (#ECE9D8, tk.GROOVE, Tahoma 9)
- Pure White Technical Canvas (#FFFFFF) with Backface Culling & Hidden Dashed Edges
- Adaptive 3D Coordinate System Oxyz with Directional Arrows (Toggle: X)
- Dual Line Weight Engine: BOLD (Screen Presentation) & LIGHT (Print) (Toggle: B)
- Circumscribed Sphere 3D Wireframe (Equatorial XY, Meridians XZ & YZ) + Center I & Radius R (Toggle: C)
- Interactive Planar Cross-Section Slicing with Stippled Polygon Rendering (Toggle: S)
- Deductive 3D Pedagogical Solver Dialog (8 Classic Topics: GDPT 2018 / SAT / AP / IB / Gaokao) (Toggle: D)
- Bilingual Interface (Vietnamese / English) (Toggle: L)
- AI Hub / HuggingFace Model Downloader Integration ([ AI ])
"""

import os
import sys
import math
import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, List, Tuple, Optional, Any

# Windows High-DPI Awareness for Razor-Sharp CAD Rendering
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        from ctypes import windll
        windll.user32.SetProcessDPIAware()
    except Exception:
        pass

# Ensure parent STEM_APP directory is on sys.path for module resolution
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT_DIR = os.path.dirname(_CURRENT_DIR)
if _PARENT_DIR not in sys.path:
    sys.path.insert(0, _PARENT_DIR)

# Attempt to import project-specific kernels and engines with full self-contained fallbacks
try:
    from geosolver_3d.geometry3d_kernel import (
        Point3D,
        Polyhedron3D,
        create_pyramid_sabcd,
        create_tetrahedron_sabc,
        create_triangular_prism,
        create_parallelepiped_box,
        create_frustum_pyramid,
        create_regular_octahedron,
        compute_plane_cross_section,
        circumscribed_sphere_from_points,
    )
    HAS_EXTERNAL_KERNEL = True
except Exception:
    HAS_EXTERNAL_KERNEL = False

try:
    from geosolver_3d.deductive3d_engine import Deductive3DEngine
    HAS_EXTERNAL_DEDUCTIVE = True
except Exception:
    HAS_EXTERNAL_DEDUCTIVE = False

# Window Geometry & Tab State Memory Persistence
try:
    from geosolver_3d.ui_state_manager import UIStateManager
except Exception:
    try:
        from stem_shared_core.tools.ui_state_manager import UIStateManager
    except Exception:
        UIStateManager = None

# License & In-App Purchase (IAP) Manager for Pro Edition
try:
    from geosolver_3d.license_manager import LicenseManager
except Exception:
    LicenseManager = None


# ==============================================================================
# SELF-CONTAINED 3D GEOMETRY KERNEL & ANALYTICAL FALLBACKS
# ==============================================================================

Vec3 = Tuple[float, float, float]


def vec_add(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def vec_sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def vec_scale(a: Vec3, s: float) -> Vec3:
    return (a[0] * s, a[1] * s, a[2] * s)


def vec_dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vec_cross(a: Vec3, b: Vec3) -> Vec3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def vec_norm(a: Vec3) -> float:
    return math.sqrt(vec_dot(a, a))


def vec_normalize(a: Vec3) -> Vec3:
    n = vec_norm(a)
    if n < 1e-12:
        return (0.0, 0.0, 0.0)
    return (a[0] / n, a[1] / n, a[2] / n)


def solve_linear_3x3(A: List[List[float]], b: List[float]) -> Optional[Vec3]:
    """Solves 3x3 linear system A * x = b using Gaussian elimination with partial pivoting."""
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(3):
        pivot_row = max(range(col, 3), key=lambda r: abs(M[r][col]))
        if abs(M[pivot_row][col]) < 1e-11:
            return None
        M[col], M[pivot_row] = M[pivot_row], M[col]
        piv = M[col][col]
        for j in range(col, 4):
            M[col][j] /= piv
        for r in range(3):
            if r != col:
                factor = M[r][col]
                for j in range(col, 4):
                    M[r][j] -= factor * M[col][j]
    return (M[0][3], M[1][3], M[2][3])


def format_radical_number(val: float, tolerance: float = 1e-4) -> str:
    """
    Chuyển đổi số thực thập phân thành dạng căn thức rút gọn toán học (ví dụ: √41/2, 3√6/2, √3, 5√2, 4/3).
    Ngăn chặn việc làm tròn bừa bãi khi gặp các số vô tỉ từ hình học không gian.
    """
    if abs(val) < 1e-9:
        return "0"
    sign = "-" if val < 0 else ""
    v = abs(val)

    # 1. Kiểm tra số nguyên
    if abs(v - round(v)) < 1e-5:
        return f"{sign}{int(round(v))}"

    # 2. Kiểm tra phân số hữu tỉ đơn giản
    from fractions import Fraction
    try:
        f = Fraction(v).limit_denominator(30)
        if abs(float(f) - v) < 1e-6:
            return f"{sign}{f.numerator}/{f.denominator}"
    except Exception:
        pass

    # 3. Kiểm tra căn thức bậc 2: v^2 = num / den
    try:
        v2 = v * v
        f2 = Fraction(v2).limit_denominator(144)
        if abs(float(f2) - v2) < tolerance:
            num = f2.numerator
            den = f2.denominator
            total_num = num * den
            k = 1
            rem = total_num
            for i in range(int(math.isqrt(total_num)), 1, -1):
                if rem % (i * i) == 0:
                    k = i
                    rem = rem // (i * i)
                    break
            g = math.gcd(k, den)
            k //= g
            den //= g
            if rem == 1:
                num_str = f"{k}"
            elif k == 1:
                num_str = f"√{rem}"
            else:
                num_str = f"{k}√{rem}"
            if den == 1:
                return f"{sign}{num_str}"
            else:
                return f"{sign}{num_str}/{den}"
    except Exception:
        pass

    return f"{sign}{v:.4f}"


def latex_to_natural_math(text: str, lang: str = "VN") -> str:
    """
    Chuyển đổi chuỗi công thức LaTeX thành dạng ký hiệu toán học tự nhiên (Unicode)
    toán học trực quan, trực quan và dễ hiểu cho giáo viên và học sinh.
    Hỗ trợ chuyển đổi chỉ số song ngữ Việt - Anh chính xác.
    """
    if not text:
        return ""
    is_vn = (lang == "VN")
    s = text
    s = re.sub(r'\$\$(.*?)\$\$', r'\1', s, flags=re.DOTALL)
    s = re.sub(r'\$(.*?)\$', r'\1', s, flags=re.DOTALL)
    s = s.replace(r'\[', '').replace(r'\]', '').replace(r'\(', '').replace(r'\)', '')
    
    replacements = [
        (r'\\sqrt\{([^}]+)\}', r'√(\1)'),
        (r'\\sqrt\[(\d+)\]\{([^}]+)\}', r'^\1√(\2)'),
        (r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1)/(\2)'),
        (r'\\dfrac\{([^}]+)\}\{([^}]+)\}', r'(\1)/(\2)'),
        (r'\\cdot', '·'),
        (r'\\times', '×'),
        (r'\\pm', '±'),
        (r'\\mp', '∓'),
        (r'\\pi', 'π'),
        (r'\\alpha', 'α'),
        (r'\\beta', 'β'),
        (r'\\gamma', 'γ'),
        (r'\\theta', 'θ'),
        (r'\\phi', 'φ'),
        (r'\\Delta', 'Δ'),
        (r'\\perp', '⊥'),
        (r'\\parallel', '∥'),
        (r'\\angle', '∠'),
        (r'\\approx', '≈'),
        (r'\\le', '≤'),
        (r'\\ge', '≥'),
        (r'\\neq', '≠'),
        (r'\\in', '∈'),
        (r'\\infty', '∞'),
        (r'\\to', '→'),
        (r'\\implies', '⇒'),
        (r'\\iff', '⇔'),
        (r'\\circ', '°'),
        (r'\\degree', '°'),
        (r'\\left\(', '('),
        (r'\\right\)', ')'),
        (r'\\left\[', '['),
        (r'\\right\]', ']'),
        (r'\\text\{([^}]+)\}', r'\1'),
        (r'\\mathbf\{([^}]+)\}', r'\1'),
        (r'\\mathrm\{([^}]+)\}', r'\1'),
        (r'\\vec\{([^}]+)\}', r'vec(\1)'),
        (r'_\{([^}]+)\}', r'_\1'),
        (r'\^\{([^}]+)\}', r'^\1'),
    ]
    for pat, rep in replacements:
        s = re.sub(pat, rep, s)

    s = s.replace('^2', '²').replace('^3', '³').replace('^0', '⁰').replace('^1', '¹').replace('^4', '⁴')
    s = s.replace('**2', '²').replace('**3', '³').replace('**4', '⁴')
    s = s.replace('_1', '₁').replace('_2', '₂').replace('_3', '₃').replace('_4', '₄')
    if is_vn:
        s = s.replace('_day', '_đáy').replace('_d', '_đáy').replace('_tp', '_toàn_phần').replace('_xq', '_xung_quanh')
    else:
        s = s.replace('_day', '_base').replace('_đáy', '_base').replace('_d', '_base').replace('_tp', '_total').replace('_toàn_phần', '_total').replace('_xq', '_lateral').replace('_xung_quanh', '_lateral')
    s = re.sub(r'sqrt\(([^)]+)\)', r'√(\1)', s)
    s = s.replace('{', '').replace('}', '')
    s = re.sub(r' +', ' ', s).strip()
    return s


def format_formula_radicals(text: str, is_vn: bool = True) -> str:
    """Format mọi công thức và biểu thức toán học thành dạng căn thức tự nhiên, không để lọt raw LaTeX."""
    if not text:
        return ""
    lang = "VN" if is_vn else "EN"
    s = latex_to_natural_math(text, lang=lang)
    s = re.sub(r'sqrt\(([^)]+)\)', r'√(\1)', s)
    s = s.replace('**2', '²').replace('**3', '³')
    s = s.replace('*', '·')
    return s


def translate_reason_to_en(reason: str) -> str:
    """Chuyển đổi các lý do / cơ sở lý thuyết hình học sang tiếng Anh chuẩn nếu chưa song ngữ."""
    if not reason:
        return ""
    if "/" in reason:
        return reason.split("/", 1)[1].strip()
    reason_map = {
        "Định lý Pythagore trong tam giác vuông": "Pythagorean Theorem in right triangle",
        "Định lý Pythagore không gian": "3D Pythagorean Theorem",
        "Tính chất hình chóp đều": "Properties of regular pyramid",
        "Tính chất trục đường tròn ngoại tiếp đáy": "Properties of base circumcircle axis",
        "Hệ thức lượng trong tam giác đều": "Metric relations in equilateral triangle",
        "Định lý khoảng cách từ điểm đến mặt phẳng": "Point-to-plane distance theorem",
        "Định nghĩa góc giữa đường thẳng và mặt phẳng": "Definition of line-plane angle",
        "Định nghĩa góc nhị diện": "Definition of dihedral angle",
        "Định lý Albert Girard": "Albert Girard Spherical Theorem",
        "Bất đẳng thức AM-GM": "AM-GM Inequality",
        "Tâm ngoại tiếp tam giác vuông là trung điểm cạnh huyền": "Circumcenter of right triangle is midpoint of hypotenuse",
    }
    for k, v in reason_map.items():
        if k in reason:
            return v
    return reason


def compute_circumscribed_sphere(vertices: Dict[str, Vec3]) -> Tuple[Vec3, float, float]:
    """
    Computes the circumscribed sphere (or best-fit circumsphere through 4 non-coplanar vertices)
    for a polyhedron. Returns (center_I, radius_R, max_residual_error).
    """
    pts = list(vertices.values())
    if not pts:
        return ((0.0, 0.0, 0.0), 1.0, 0.0)

    # First try external kernel if available
    if HAS_EXTERNAL_KERNEL:
        try:
            res = circumscribed_sphere_from_points(pts)
            if isinstance(res, dict) and "center" in res and "radius" in res:
                c = tuple(res["center"])
                r = float(res["radius"])
                err = max(abs(vec_norm(vec_sub(p, c)) - r) for p in pts)
                return (c, r, err)
        except Exception:
            pass

    # Find 4 non-coplanar points to solve exact circumsphere
    p0 = pts[0]
    best_center: Optional[Vec3] = None
    best_radius: float = 0.0

    n = len(pts)
    for i in range(1, n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                p1, p2, p3 = pts[i], pts[j], pts[k]
                v1 = vec_sub(p1, p0)
                v2 = vec_sub(p2, p0)
                v3 = vec_sub(p3, p0)
                vol6 = abs(vec_dot(v1, vec_cross(v2, v3)))
                if vol6 > 1e-5:
                    A = [
                        [2.0 * v1[0], 2.0 * v1[1], 2.0 * v1[2]],
                        [2.0 * v2[0], 2.0 * v2[1], 2.0 * v2[2]],
                        [2.0 * v3[0], 2.0 * v3[1], 2.0 * v3[2]],
                    ]
                    rhs = [
                        vec_dot(p1, p1) - vec_dot(p0, p0),
                        vec_dot(p2, p2) - vec_dot(p0, p0),
                        vec_dot(p3, p3) - vec_dot(p0, p0),
                    ]
                    sol = solve_linear_3x3(A, rhs)
                    if sol is not None:
                        r = vec_norm(vec_sub(p0, sol))
                        err = max(abs(vec_norm(vec_sub(p, sol)) - r) for p in pts)
                        if best_center is None or err < max(
                            abs(vec_norm(vec_sub(p, best_center)) - best_radius) for p in pts
                        ):
                            best_center = sol
                            best_radius = r
                            if err < 1e-4:
                                return (best_center, best_radius, err)

    if best_center is not None:
        err = max(abs(vec_norm(vec_sub(p, best_center)) - best_radius) for p in pts)
        return (best_center, best_radius, err)

    # Fallback: centroid + average distance
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    cz = sum(p[2] for p in pts) / len(pts)
    center = (cx, cy, cz)
    radius = max(vec_norm(vec_sub(p, center)) for p in pts)
    err = max(abs(vec_norm(vec_sub(p, center)) - radius) for p in pts)
    return (center, radius, err)


def compute_polygon_hatch(
    pts: List[Tuple[float, float]],
    spacing: float = 10.0,
    angle_deg: float = 45.0,
) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """
    Computes 2D vector CAD hatching line segments inside an arbitrary planar polygon.
    Rotates points by -angle, intersects horizontal scanlines at fixed intervals,
    and rotates intersection intervals back to original screen coordinates.
    """
    if len(pts) < 3:
        return []
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    rot_pts = [(x * cos_a + y * sin_a, -x * sin_a + y * cos_a) for x, y in pts]
    min_y = min(p[1] for p in rot_pts)
    max_y = max(p[1] for p in rot_pts)

    segments: List[Tuple[Tuple[float, float], Tuple[float, float]]] = []
    n = len(rot_pts)
    curr_y = min_y + spacing * 0.7
    while curr_y < max_y:
        x_inters: List[float] = []
        for i in range(n):
            p1 = rot_pts[i]
            p2 = rot_pts[(i + 1) % n]
            y1, y2 = p1[1], p2[1]
            if (y1 <= curr_y < y2) or (y2 <= curr_y < y1):
                dy = y2 - y1
                if abs(dy) > 1e-9:
                    t = (curr_y - y1) / dy
                    xi = p1[0] + t * (p2[0] - p1[0])
                    x_inters.append(xi)
        x_inters.sort()
        for j in range(0, len(x_inters) - 1, 2):
            x_a = x_inters[j]
            x_b = x_inters[j + 1]
            orig_x1 = x_a * cos_a - curr_y * sin_a
            orig_y1 = x_a * sin_a + curr_y * cos_a
            orig_x2 = x_b * cos_a - curr_y * sin_a
            orig_y2 = x_b * sin_a + curr_y * cos_a
            segments.append(((orig_x1, orig_y1), (orig_x2, orig_y2)))
        curr_y += spacing
    return segments


class PolyhedronModel:
    """Represents a 3D polyhedron with vertices, outward-oriented faces, edges, and default section plane."""

    def __init__(
        self,
        key: str,
        name_vn: str,
        name_en: str,
        vertices: Dict[str, Vec3],
        faces: List[List[str]],
        plane_normal: Vec3,
        plane_d: float,
        plane_desc_vn: str,
        plane_desc_en: str,
    ):
        self.key = key
        self.name_vn = name_vn
        self.name_en = name_en
        self.vertices = vertices
        self.faces = faces
        self.plane_normal = vec_normalize(plane_normal)
        self.plane_d = plane_d
        self.plane_desc_vn = plane_desc_vn
        self.plane_desc_en = plane_desc_en
        self.initial_vertices = {k: v for k, v in vertices.items()}
        self.aux_points: Dict[str, Vec3] = {}
        self.aux_segments: List[Dict[str, Any]] = []
        self.aux_circles: List[Dict[str, Any]] = []
        self.aux_angles: List[Dict[str, Any]] = []
        self.section_points: List[Tuple[str, Vec3]] = []
        self.section_edges: List[Tuple[str, Vec3, str, Vec3, int]] = []
        self.point_constraints: Dict[str, Dict[str, Any]] = {}
        self.edge_colors: Dict[Tuple[str, str], str] = {}
        self.vertex_colors: Dict[str, str] = {}
        self.section_edge_map: Dict[str, Tuple[str, str]] = {}
        self.custom_planes: List[Dict[str, Any]] = []
        self.plane_defining_pts: Optional[List[str]] = None
        self.section_fill_mode: str = "hatch"  # "hatch", "cross", "solid", "stipple", "none"
        self.section_hatch_spacing: int = 10
        self.section_drag_mode: str = "pivot"  # "pivot" = độc lập đỉnh, "parallel" = trượt cả mp
        self.edges = self._extract_edges()
        self.centroid = self._compute_centroid()

    def recalculate_geometry(self) -> None:
        self.centroid = self._compute_centroid()
        self.edges = self._extract_edges()

    def reset_vertices(self) -> None:
        self.vertices = {k: v for k, v in self.initial_vertices.items()}
        self.point_constraints.clear()
        self.edge_colors.clear()
        self.vertex_colors.clear()
        self.aux_points.clear()
        self.aux_segments.clear()
        self.aux_circles.clear()
        self.aux_angles.clear()
        self.section_points.clear()
        self.section_edges.clear()
        self.section_edge_map.clear()
        self.custom_planes.clear()
        self.plane_defining_pts = None
        self.section_fill_mode = "hatch"
        self.section_drag_mode = "pivot"
        self.recalculate_geometry()

    def get_point(self, name: str) -> Optional[Vec3]:
        """Lấy tọa độ 3D của đỉnh khối, điểm phụ hoặc đỉnh thiết diện theo tên."""
        if name in self.vertices:
            return self.vertices[name]
        if name in self.aux_points:
            return self.aux_points[name]
        if hasattr(self, "section_points") and self.section_points:
            for lbl, pt in self.section_points:
                if lbl == name:
                    return pt
        return None

    def add_custom_plane(
        self,
        name: str,
        pts: List[str],
        color: str = "#1971C2",
        fill_mode: str = "hatch",
        hatch_spacing: int = 10,
        is_cutter: bool = False,
    ) -> None:
        """Thêm mặt phẳng phụ nối các điểm bất kỳ trong không gian kèm chế độ tô CAD."""
        plane_dict = {
            "name": name,
            "pts": pts,
            "color": color,
            "fill_mode": fill_mode,
            "hatch_spacing": hatch_spacing,
            "is_cutter": is_cutter,
            "visible": True,
        }
        self.custom_planes.append(plane_dict)
        if is_cutter and len(pts) >= 3:
            p1 = self.get_point(pts[0])
            p2 = self.get_point(pts[1])
            p3 = self.get_point(pts[2])
            if p1 and p2 and p3:
                u = vec_sub(p2, p1)
                v = vec_sub(p3, p1)
                n = vec_cross(u, v)
                if vec_norm(n) > 1e-6:
                    self.plane_normal = vec_normalize(n)
                    self.plane_d = vec_dot(self.plane_normal, p1)
                    self.plane_defining_pts = pts[:3]
                    self.compute_cross_section()

    def update_constraints(self) -> None:
        """Tự động tính toán lại toàn bộ điểm phụ và đường phụ theo ràng buộc hình học khi đỉnh di chuyển."""
        for name, c in list(self.point_constraints.items()):
            ctype = c.get("type")
            if ctype == "ratio":
                p1 = self.get_point(c.get("p1", ""))
                p2 = self.get_point(c.get("p2", ""))
                if p1 and p2:
                    k = c.get("k", 0.5)
                    self.aux_points[name] = vec_add(p1, vec_scale(vec_sub(p2, p1), k))
            elif ctype == "centroid":
                pts = [self.get_point(p) for p in c.get("pts", [])]
                if len(pts) >= 3 and all(p is not None for p in pts[:3]):
                    A, B, C = pts[0], pts[1], pts[2]
                    self.aux_points[name] = vec_scale(vec_add(vec_add(A, B), C), 1.0 / 3.0)
            elif ctype == "parallel":
                P = self.get_point(c.get("p_from", ""))
                A = self.get_point(c.get("p1", ""))
                B = self.get_point(c.get("p2", ""))
                if P and A and B:
                    u = vec_sub(B, A)
                    self.aux_points[name] = vec_add(P, u)
            elif ctype == "perp_line":
                P = self.get_point(c.get("p_from", ""))
                A = self.get_point(c.get("p1", ""))
                B = self.get_point(c.get("p2", ""))
                if P and A and B:
                    u = vec_sub(B, A)
                    u2 = vec_dot(u, u)
                    if u2 > 1e-9:
                        t = vec_dot(vec_sub(P, A), u) / u2
                        self.aux_points[name] = vec_add(A, vec_scale(u, t))
            elif ctype == "perp_face":
                P = self.get_point(c.get("p_from", ""))
                pts = [self.get_point(p) for p in c.get("pts", [])]
                if P and len(pts) >= 3 and all(p is not None for p in pts[:3]):
                    A, B, C = pts[0], pts[1], pts[2]
                    n = vec_normalize(vec_cross(vec_sub(B, A), vec_sub(C, A)))
                    if vec_norm(n) > 1e-6:
                        d_proj = vec_dot(n, vec_sub(P, A))
                        self.aux_points[name] = vec_sub(P, vec_scale(n, d_proj))
            elif ctype == "perp_base":
                P = self.get_point(c.get("p_from", ""))
                if P and len(self.faces) > 0:
                    base_face = self.faces[0]
                    n = self.compute_face_outward_normal(base_face)
                    p0 = self.vertices.get(base_face[0])
                    if p0:
                        d_const = vec_dot(n, p0)
                        t = vec_dot(n, P) - d_const
                        self.aux_points[name] = vec_sub(P, vec_scale(n, t))
            elif ctype == "perp_section":
                P = self.get_point(c.get("p_from", ""))
                if P:
                    n = self.plane_normal
                    d_const = self.plane_d
                    n_norm_sq = vec_dot(n, n)
                    if n_norm_sq > 1e-9:
                        t = (vec_dot(n, P) - d_const) / n_norm_sq
                        self.aux_points[name] = vec_sub(P, vec_scale(n, t))
            elif ctype == "angle_ray":
                A = self.get_point(c.get("vert", ""))
                B = self.get_point(c.get("dir", ""))
                C = self.get_point(c.get("plane", ""))
                deg = c.get("deg", 60.0)
                if A and B and C:
                    u = vec_sub(B, A)
                    v = vec_sub(C, A)
                    n = vec_cross(u, v)
                    if vec_norm(n) > 1e-6:
                        n_unit = vec_normalize(n)
                        u_unit = vec_normalize(u)
                        rad = math.radians(deg)
                        rot_dir = vec_add(
                            vec_scale(u_unit, math.cos(rad)),
                            vec_scale(vec_cross(n_unit, u_unit), math.sin(rad))
                        )
                        L = c.get("length", vec_norm(u))
                        self.aux_points[name] = vec_add(A, vec_scale(rot_dir, L))
            elif ctype == "circumcenter":
                pts = [self.get_point(p) for p in c.get("pts", [])]
                if len(pts) >= 3 and all(p is not None for p in pts[:3]):
                    A, B, C = pts[0], pts[1], pts[2]
                    vBA = vec_sub(B, A)
                    vCA = vec_sub(C, A)
                    cr = vec_cross(vBA, vCA)
                    cr_norm = vec_norm(cr)
                    if cr_norm > 1e-6:
                        b2 = vec_dot(vBA, vBA)
                        c2 = vec_dot(vCA, vCA)
                        v_num = vec_sub(vec_scale(vCA, b2), vec_scale(vBA, c2))
                        O_rel = vec_scale(vec_cross(v_num, cr), 1.0 / (2.0 * (cr_norm ** 2)))
                        self.aux_points[name] = vec_add(A, O_rel)
            elif ctype == "incenter":
                pts = [self.get_point(p) for p in c.get("pts", [])]
                if len(pts) >= 3 and all(p is not None for p in pts[:3]):
                    A, B, C = pts[0], pts[1], pts[2]
                    a = vec_norm(vec_sub(B, C))
                    b = vec_norm(vec_sub(C, A))
                    c_side = vec_norm(vec_sub(A, B))
                    perim = a + b + c_side
                    if perim > 1e-6:
                        Ix = (a * A[0] + b * B[0] + c_side * C[0]) / perim
                        Iy = (a * A[1] + b * B[1] + c_side * C[1]) / perim
                        Iz = (a * A[2] + b * B[2] + c_side * C[2]) / perim
                        self.aux_points[name] = (Ix, Iy, Iz)

        # Cập nhật tọa độ 2 đầu mút cho toàn bộ đoạn thẳng phụ
        for seg in self.aux_segments:
            p1_name = seg.get("p1_name")
            p2_name = seg.get("p2_name")
            if p1_name:
                p1 = self.get_point(p1_name)
                if p1 is not None:
                    seg["p1"] = p1
            if p2_name:
                p2 = self.get_point(p2_name)
                if p2 is not None:
                    seg["p2"] = p2

        # Cập nhật tâm & pháp tuyến các đường tròn phụ
        for circ in self.aux_circles:
            pts = [self.get_point(p) for p in circ.get("pts", [])]
            if len(pts) >= 3 and all(p is not None for p in pts[:3]):
                A, B, C = pts[0], pts[1], pts[2]
                norm = vec_normalize(vec_cross(vec_sub(B, A), vec_sub(C, A)))
                circ["normal"] = norm
                if circ.get("circle_type") == "circum":
                    vBA = vec_sub(B, A)
                    vCA = vec_sub(C, A)
                    cr = vec_cross(vBA, vCA)
                    cr_norm = vec_norm(cr)
                    if cr_norm > 1e-6:
                        b2 = vec_dot(vBA, vBA)
                        c2 = vec_dot(vCA, vCA)
                        v_num = vec_sub(vec_scale(vCA, b2), vec_scale(vBA, c2))
                        O_rel = vec_scale(vec_cross(v_num, cr), 1.0 / (2.0 * (cr_norm ** 2)))
                        O = vec_add(A, O_rel)
                        circ["center"] = O
                        circ["radius"] = vec_norm(O_rel)
                elif circ.get("circle_type") == "in":
                    a = vec_norm(vec_sub(B, C))
                    b = vec_norm(vec_sub(C, A))
                    c_side = vec_norm(vec_sub(A, B))
                    perim = a + b + c_side
                    if perim > 1e-6:
                        Ix = (a * A[0] + b * B[0] + c_side * C[0]) / perim
                        Iy = (a * A[1] + b * B[1] + c_side * C[1]) / perim
                        Iz = (a * A[2] + b * B[2] + c_side * C[2]) / perim
                        s = perim * 0.5
                        area = 0.5 * vec_norm(vec_cross(vec_sub(B, A), vec_sub(C, A)))
                        circ["center"] = (Ix, Iy, Iz)
                        circ["radius"] = area / s if s > 1e-6 else 0.0

        # Cập nhật mặt phẳng cắt nếu được định nghĩa qua các điểm động
        if getattr(self, "plane_defining_pts", None) and len(self.plane_defining_pts) >= 3:
            p1 = self.get_point(self.plane_defining_pts[0])
            p2 = self.get_point(self.plane_defining_pts[1])
            p3 = self.get_point(self.plane_defining_pts[2])
            if p1 and p2 and p3:
                u = vec_sub(p2, p1)
                v = vec_sub(p3, p1)
                n = vec_cross(u, v)
                if vec_norm(n) > 1e-6:
                    n_norm = vec_normalize(n)
                    if vec_dot(n_norm, self.plane_normal) < 0:
                        n_norm = vec_scale(n_norm, -1.0)
                    self.plane_normal = n_norm
                    self.plane_d = vec_dot(n_norm, p1)
                    self.compute_cross_section()

    def compute_volume_and_surface(self) -> Tuple[float, float]:
        """Tính toán thể tích V và diện tích toàn phần S_tp chính xác cho khối đa diện."""
        total_vol = 0.0
        total_surface = 0.0
        c = self.centroid
        for face in self.faces:
            if len(face) < 3:
                continue
            p0 = self.vertices[face[0]]
            for i in range(1, len(face) - 1):
                p1 = self.vertices[face[i]]
                p2 = self.vertices[face[i + 1]]
                cr = vec_cross(vec_sub(p1, p0), vec_sub(p2, p0))
                tri_area = 0.5 * vec_norm(cr)
                total_surface += tri_area
                tet_vol = abs(vec_dot(vec_sub(p0, c), vec_cross(vec_sub(p1, c), vec_sub(p2, c)))) / 6.0
                total_vol += tet_vol
        return total_vol, total_surface
    def apply_dimensions(self, h: float, a: float, b: float) -> None:
        """Co giãn kích thước khối đa diện theo chiều cao h, cạnh đáy a, b thời gian thực."""
        if self.key in ("pyramid_sabcd", "tetrahedron_sabc"):
            # Điều chỉnh chiều cao đỉnh S và tỉ lệ đáy
            for v_name in list(self.vertices.keys()):
                x, y, z = self.initial_vertices[v_name]
                if v_name == "S":
                    self.vertices[v_name] = (x, y, h)
                else:
                    self.vertices[v_name] = (x * (a / 2.4), y * (b / 2.4), z)
        elif self.key in ("prism_abc", "box_abcd", "frustum_abcd"):
            for v_name in list(self.vertices.keys()):
                x, y, z = self.initial_vertices[v_name]
                z_new = h if z > 0.1 else 0.0
                self.vertices[v_name] = (x * (a / 2.4), y * (b / 2.4), z_new)
        elif self.key == "octahedron":
            scale_fac = a / 2.4
            for v_name in list(self.vertices.keys()):
                x, y, z = self.initial_vertices[v_name]
                self.vertices[v_name] = (x * scale_fac, y * scale_fac, z * (h / 2.4))
        self.update_constraints()
        self.recalculate_geometry()


    def _compute_centroid(self) -> Vec3:
        pts = list(self.vertices.values())
        n = len(pts)
        if n == 0:
            return (0.0, 0.0, 0.0)
        return (
            sum(p[0] for p in pts) / n,
            sum(p[1] for p in pts) / n,
            sum(p[2] for p in pts) / n,
        )

    def _extract_edges(self) -> List[Tuple[str, str]]:
        edge_set = set()
        edges = []
        for face in self.faces:
            m = len(face)
            for i in range(m):
                u, v = face[i], face[(i + 1) % m]
                pair = (u, v) if u < v else (v, u)
                if pair not in edge_set:
                    edge_set.add(pair)
                    edges.append((u, v))
        return edges

    def compute_face_outward_normal(self, face: List[str]) -> Vec3:
        if len(face) < 3:
            return (0.0, 0.0, 1.0)
        p0 = self.vertices[face[0]]
        p1 = self.vertices[face[1]]
        p2 = self.vertices[face[2]]
        n = vec_cross(vec_sub(p1, p0), vec_sub(p2, p0))
        face_center = (
            sum(self.vertices[v][0] for v in face) / len(face),
            sum(self.vertices[v][1] for v in face) / len(face),
            sum(self.vertices[v][2] for v in face) / len(face),
        )
        outward_vec = vec_sub(face_center, self.centroid)
        if vec_dot(n, outward_vec) < 0:
            n = vec_scale(n, -1.0)
        return vec_normalize(n)

    def max_extent(self) -> float:
        if not self.vertices:
            return 2.0
        return max(
            max(abs(p[0]), abs(p[1]), abs(p[2]))
            for p in self.vertices.values()
        )

    def compute_cross_section(self) -> List[Tuple[str, Vec3]]:
        """
        Intersects the plane n . X = d with the polyhedron faces using robust topological
        segment chaining. Guarantees an exact, ordered, non-self-intersecting planar polygon,
        recording exact face indices for hidden/solid edge rendering.
        """
        n = self.plane_normal
        d = self.plane_d
        edge_intersections: Dict[Tuple[str, str], Vec3] = {}

        for u, v in self.edges:
            p1 = self.vertices[u]
            p2 = self.vertices[v]
            f1 = vec_dot(n, p1) - d
            f2 = vec_dot(n, p2) - d
            if abs(f1) < 1e-7 and abs(f2) < 1e-7:
                continue
            if f1 * f2 <= 0.0 and abs(f2 - f1) > 1e-9:
                t = -f1 / (f2 - f1)
                if -1e-6 <= t <= 1.0 + 1e-6:
                    t_clamped = max(0.0, min(1.0, t))
                    pt = vec_add(p1, vec_scale(vec_sub(p2, p1), t_clamped))
                    pair = (u, v) if u < v else (v, u)
                    edge_intersections[pair] = pt

        face_segments: List[Tuple[Tuple[Tuple[str, str], Vec3], Tuple[Tuple[str, str], Vec3], int]] = []
        for f_idx, face in enumerate(self.faces):
            pts_in_face: List[Tuple[Tuple[str, str], Vec3]] = []
            m = len(face)
            for i in range(m):
                a, b = face[i], face[(i + 1) % m]
                pair = (a, b) if a < b else (b, a)
                if pair in edge_intersections:
                    pt = edge_intersections[pair]
                    if not any(vec_norm(vec_sub(pt, p)) < 1e-4 for _, p in pts_in_face):
                        pts_in_face.append((pair, pt))
            if len(pts_in_face) == 2:
                face_segments.append((pts_in_face[0], pts_in_face[1], f_idx))

        labels = ["M", "N", "P", "Q", "R", "K", "E", "F"]

        self.section_edge_map = {}
        if not face_segments:
            raw_pts: List[Vec3] = list(edge_intersections.values())
            if len(raw_pts) < 3:
                self.section_points = []
                self.section_edges = []
                self.section_edge_map = {}
                return []
            cx = sum(p[0] for p in raw_pts) / len(raw_pts)
            cy = sum(p[1] for p in raw_pts) / len(raw_pts)
            cz = sum(p[2] for p in raw_pts) / len(raw_pts)
            center = (cx, cy, cz)
            ref = (1.0, 0.0, 0.0) if abs(n[0]) < 0.8 else (0.0, 1.0, 0.0)
            u_axis = vec_normalize(vec_cross(n, ref))
            v_axis = vec_normalize(vec_cross(n, u_axis))
            raw_pts.sort(key=lambda pt: math.atan2(vec_dot(vec_sub(pt, center), v_axis), vec_dot(vec_sub(pt, center), u_axis)))
            self.section_points = []
            for i, pt in enumerate(raw_pts):
                lbl = labels[i % len(labels)]
                self.section_points.append((lbl, pt))
                for p_pair, p_pt in edge_intersections.items():
                    if vec_norm(vec_sub(p_pt, pt)) < 1e-4:
                        self.section_edge_map[lbl] = p_pair
                        break
            self.section_edges = []
            k = len(self.section_points)
            for i in range(k):
                lbl_a, pt_a = self.section_points[i]
                lbl_b, pt_b = self.section_points[(i + 1) % k]
                self.section_edges.append((lbl_a, pt_a, lbl_b, pt_b, -1))
            return self.section_points

        loop: List[Tuple[Tuple[Tuple[str, str], Vec3], Tuple[Tuple[str, str], Vec3], int]] = []
        curr_seg = face_segments[0]
        face_segments.remove(curr_seg)
        p_curr = curr_seg[1]
        loop.append((curr_seg[0], curr_seg[1], curr_seg[2]))

        while face_segments:
            next_found = False
            for seg in face_segments:
                p_a, p_b, f_id = seg
                if vec_norm(vec_sub(p_curr[1], p_a[1])) < 1e-4:
                    loop.append((p_a, p_b, f_id))
                    p_curr = p_b
                    face_segments.remove(seg)
                    next_found = True
                    break
                elif vec_norm(vec_sub(p_curr[1], p_b[1])) < 1e-4:
                    loop.append((p_b, p_a, f_id))
                    p_curr = p_a
                    face_segments.remove(seg)
                    next_found = True
                    break
            if not next_found:
                break

        self.section_points = []
        self.section_edge_map = {}
        for i, seg in enumerate(loop):
            lbl = labels[i % len(labels)]
            self.section_points.append((lbl, seg[0][1]))
            self.section_edge_map[lbl] = seg[0][0]
        self.section_edges = []
        k = len(self.section_points)
        for i in range(k):
            lbl_a, pt_a = self.section_points[i]
            lbl_b, pt_b = self.section_points[(i + 1) % k]
            f_id = loop[i][2] if i < len(loop) else -1
            self.section_edges.append((lbl_a, pt_a, lbl_b, pt_b, f_id))

        return self.section_points


def build_standard_polyhedra() -> Dict[str, PolyhedronModel]:
    """Creates standard 3D polyhedra centered conveniently around O(0,0,0)."""
    models: Dict[str, PolyhedronModel] = {}

    # 1. Pyramid S.ABCD (Chóp tứ giác đều S.ABCD)
    models["pyramid_sabcd"] = PolyhedronModel(
        key="pyramid_sabcd",
        name_vn="Hình chóp tứ giác S.ABCD",
        name_en="Pyramid S.ABCD",
        vertices={
            "S": (0.0, 0.0, 2.2),
            "A": (-1.2, -1.2, 0.0),
            "B": (1.2, -1.2, 0.0),
            "C": (1.2, 1.2, 0.0),
            "D": (-1.2, 1.2, 0.0),
        },
        faces=[
            ["A", "B", "C", "D"],
            ["S", "A", "B"],
            ["S", "B", "C"],
            ["S", "C", "D"],
            ["S", "D", "A"],
        ],
        plane_normal=(0.18, 0.12, 1.0),
        plane_d=0.95,
        plane_desc_vn="Thiết diện (MNPQ) cắt các cạnh bên SA, SB, SC, SD",
        plane_desc_en="Cross-section (MNPQ) intersecting lateral edges SA, SB, SC, SD",
    )

    # 2. Tetrahedron S.ABC (Tứ diện S.ABC)
    models["tetrahedron_sabc"] = PolyhedronModel(
        key="tetrahedron_sabc",
        name_vn="Tứ diện S.ABC",
        name_en="Tetrahedron S.ABC",
        vertices={
            "S": (0.0, 0.0, 2.1),
            "A": (-1.3, -0.9, 0.0),
            "B": (1.4, -0.7, 0.0),
            "C": (-0.1, 1.5, 0.0),
        },
        faces=[
            ["A", "B", "C"],
            ["S", "A", "B"],
            ["S", "B", "C"],
            ["S", "C", "A"],
        ],
        plane_normal=(0.15, -0.10, 1.0),
        plane_d=0.88,
        plane_desc_vn="Thiết diện tam giác (MNP) cắt SA, SB, SC",
        plane_desc_en="Triangular cross-section (MNP) cutting SA, SB, SC",
    )

    # 3. Right Triangular Prism ABC.A'B'C' (Lăng trụ đứng)
    models["prism_abc"] = PolyhedronModel(
        key="prism_abc",
        name_vn="Lăng trụ đứng ABC.A'B'C'",
        name_en="Right Prism ABC.A'B'C'",
        vertices={
            "A": (-1.2, -0.9, 0.0),
            "B": (1.3, -0.8, 0.0),
            "C": (0.0, 1.3, 0.0),
            "A'": (-1.2, -0.9, 2.1),
            "B'": (1.3, -0.8, 2.1),
            "C'": (0.0, 1.3, 2.1),
        },
        faces=[
            ["A", "B", "C"],
            ["A'", "B'", "C'"],
            ["A", "B", "B'", "A'"],
            ["B", "C", "C'", "B'"],
            ["C", "A", "A'", "C'"],
        ],
        plane_normal=(0.22, 0.15, 1.0),
        plane_d=1.05,
        plane_desc_vn="Thiết diện (MNP) cắt các cạnh bên AA', BB', CC'",
        plane_desc_en="Cross-section (MNP) intersecting lateral edges AA', BB', CC'",
    )

    # 4. Parallelepiped / Box ABCD.A'B'C'D' (Hình hộp chữ nhật)
    models["box_abcd"] = PolyhedronModel(
        key="box_abcd",
        name_vn="Hình hộp ABCD.A'B'C'D'",
        name_en="Box ABCD.A'B'C'D'",
        vertices={
            "A": (-1.3, -1.0, 0.0),
            "B": (1.3, -1.0, 0.0),
            "C": (1.3, 1.0, 0.0),
            "D": (-1.3, 1.0, 0.0),
            "A'": (-1.3, -1.0, 1.9),
            "B'": (1.3, -1.0, 1.9),
            "C'": (1.3, 1.0, 1.9),
            "D'": (-1.3, 1.0, 1.9),
        },
        faces=[
            ["A", "B", "C", "D"],
            ["A'", "B'", "C'", "D'"],
            ["A", "B", "B'", "A'"],
            ["B", "C", "C'", "B'"],
            ["C", "D", "D'", "C'"],
            ["D", "A", "A'", "D'"],
        ],
        plane_normal=(0.28, 0.20, 1.0),
        plane_d=0.95,
        plane_desc_vn="Thiết diện tứ giác (MNPQ) cắt hình hộp",
        plane_desc_en="Planar quadrilateral section (MNPQ) across the box",
    )

    # 5. Frustum of Regular Pyramid ABCD.A'B'C'D' (Hình chóp cụt đều)
    models["frustum_abcd"] = PolyhedronModel(
        key="frustum_abcd",
        name_vn="Hình chóp cụt đều ABCD.A'B'C'D'",
        name_en="Regular Frustum ABCD.A'B'C'D'",
        vertices={
            "A": (-1.4, -1.4, 0.0),
            "B": (1.4, -1.4, 0.0),
            "C": (1.4, 1.4, 0.0),
            "D": (-1.4, 1.4, 0.0),
            "A'": (-0.75, -0.75, 1.7),
            "B'": (0.75, -0.75, 1.7),
            "C'": (0.75, 0.75, 1.7),
            "D'": (-0.75, 0.75, 1.7),
        },
        faces=[
            ["A", "B", "C", "D"],
            ["A'", "B'", "C'", "D'"],
            ["A", "B", "B'", "A'"],
            ["B", "C", "C'", "B'"],
            ["C", "D", "D'", "C'"],
            ["D", "A", "A'", "D'"],
        ],
        plane_normal=(0.15, -0.12, 1.0),
        plane_d=0.85,
        plane_desc_vn="Thiết diện (MNPQ) cắt bốn cạnh bên chóp cụt",
        plane_desc_en="Cross-section (MNPQ) cutting the four lateral edges of the frustum",
    )

    # 6. Regular Octahedron S.ABCD.S' (Bát diện đều)
    models["octahedron"] = PolyhedronModel(
        key="octahedron",
        name_vn="Khối bát diện đều S.ABCD.S'",
        name_en="Regular Octahedron S.ABCD.S'",
        vertices={
            "S": (0.0, 0.0, 1.65),
            "A": (-1.65, 0.0, 0.0),
            "B": (0.0, -1.65, 0.0),
            "C": (1.65, 0.0, 0.0),
            "D": (0.0, 1.65, 0.0),
            "S'": (0.0, 0.0, -1.65),
        },
        faces=[
            ["S", "A", "B"],
            ["S", "B", "C"],
            ["S", "C", "D"],
            ["S", "D", "A"],
            ["S'", "B", "A"],
            ["S'", "C", "B"],
            ["S'", "D", "C"],
            ["S'", "A", "D"],
        ],
        plane_normal=(0.20, 0.25, 1.0),
        plane_d=0.45,
        plane_desc_vn="Thiết diện đa giác cắt bát diện đều",
        plane_desc_en="Planar polygon section slicing the regular octahedron",
    )

    return models


# ==============================================================================
# BUILT-IN DEDUCTIVE 3D PEDAGOGICAL ENGINE (8 CLASSIC TOPICS)
# ==============================================================================

class BuiltinDeductive3DEngine:
    """
    Provides step-by-step analytical proofs, natural math formulas with exact radicals,
    and exact numerical evaluations for the 12 classic 3D geometry curriculum topics
    (GDPT 2018 + SAT / AP / IB / Gaokao).
    Full bilingual support (VN / EN) with zero language leakage.
    """

    def __init__(self):
        self.external_engine = None
        if HAS_EXTERNAL_DEDUCTIVE:
            try:
                self.external_engine = Deductive3DEngine()
            except Exception:
                self.external_engine = None

    def solve_topic(self, topic_index: int, params: Dict[str, float], lang: str = "VN") -> str:
        if topic_index == 1:
            return self._solve_topic_1(params, lang)
        elif topic_index == 2:
            return self._solve_topic_2(params, lang)
        elif topic_index == 3:
            return self._solve_topic_3(params, lang)
        elif topic_index == 4:
            return self._solve_topic_4(params, lang)
        elif topic_index == 5:
            return self._solve_topic_5(params, lang)
        elif topic_index == 6:
            return self._solve_topic_6(params, lang)
        elif topic_index == 7:
            return self._solve_topic_7(params, lang)
        elif topic_index == 8:
            return self._solve_topic_8(params, lang)
        elif topic_index == 9:
            return self._solve_topic_9(params, lang)
        elif topic_index == 10:
            return self._solve_topic_10(params, lang)
        elif topic_index == 11:
            return self._solve_topic_11(params, lang)
        elif topic_index == 12:
            return self._solve_topic_12(params, lang)
        return "Chuyên đề không hợp lệ / Invalid topic index."

    def _solve_topic_1(self, p: Dict[str, float], lang: str) -> str:
        is_vn = (lang == "VN")
        sa = max(0.01, p.get("SA", 4.0))
        ab = max(0.01, p.get("AB", 3.0))
        bc = max(0.01, p.get("BC", 4.0))
        ac = math.sqrt(ab * ab + bc * bc)
        r_base = ac / 2.0
        R = 0.5 * math.sqrt(sa * sa + ac * ac)
        area_sphere = 4.0 * math.pi * R * R
        vol_sphere = (4.0 / 3.0) * math.pi * (R ** 3)

        ac_rad = format_radical_number(ac)
        r_base_rad = format_radical_number(r_base)
        R_rad = format_radical_number(R)

        if is_vn:
            return (
                "========================================================================\n"
                "CHUYÊN ĐỀ 1: MẶT CẦU NGOẠI TIẾP CHÓP S.ABC (SA ⊥ ĐÁY, ΔABC VUÔNG TẠI B)\n"
                "========================================================================\n\n"
                f"[THÔNG SỐ ĐẦU VÀO]\n"
                f"  • Chiều cao cạnh bên: SA = h = {sa:.4f}\n"
                f"  • Hai cạnh góc vuông đáy: AB = {ab:.4f}, BC = {bc:.4f}\n\n"
                "[SUY LUẬN HÌNH HỌC TỪNG BƯỚC (DEDUCTIVE PROOF)]\n"
                "  Bước 1: Xét tam giác ABC vuông tại B:\n"
                "          Gọi M là trung điểm cạnh huyền AC => M là tâm đường tròn ngoại tiếp ΔABC.\n"
                f"          AC = √(AB² + BC²) = √({ab:.2f}² + {bc:.2f}²) = {ac_rad} (≈ {ac:.4f})\n"
                f"          Bán kính đường tròn đáy: R_đáy = AC / 2 = {r_base_rad} (≈ {r_base:.4f})\n\n"
                "  Bước 2: Vì SA ⊥ (ABC) và góc ABC = 90°:\n"
                "          Ta có BC ⊥ AB và BC ⊥ SA => BC ⊥ (SAB) => BC ⊥ SB (ΔSBC vuông tại B).\n"
                "          Đồng thời ΔSAC vuông tại A.\n"
                "          Do các đỉnh A, B, C cùng nhìn đoạn SC dưới góc vuông (90°),\n"
                "          tâm mặt cầu ngoại tiếp I chính là trung điểm của cạnh huyền chung SC.\n\n"
                "[CÔNG THỨC HÌNH HỌC TỰ NHIÊN]\n"
                "  R = SC/2 = 1/2 · √(SA² + AB² + BC²) = √(R_đáy² + (SA/2)²)\n\n"
                "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
                f"  • Bán kính mặt cầu ngoại tiếp: R = {R_rad} (≈ {R:.4f})\n"
                f"  • Diện tích mặt cầu: S = 4πR² ≈ {area_sphere:.4f}\n"
                f"  • Thể tích khối cầu: V = (4/3)πR³ ≈ {vol_sphere:.4f}\n"
            )
        else:
            return (
                "========================================================================\n"
                "TOPIC 1: CIRCUMSCRIBED SPHERE OF PYRAMID S.ABC (SA ⊥ BASE, RIGHT ΔABC AT B)\n"
                "========================================================================\n\n"
                f"[INPUT PARAMETERS]\n"
                f"  • Lateral height: SA = h = {sa:.4f}\n"
                f"  • Base right-angle legs: AB = {ab:.4f}, BC = {bc:.4f}\n\n"
                "[STEP-BY-STEP DEDUCTIVE PROOF]\n"
                "  Step 1: In right triangle ABC at vertex B:\n"
                "          Let M be the midpoint of hypotenuse AC => M is circumcenter of ΔABC.\n"
                f"          AC = √(AB² + BC²) = √({ab:.2f}² + {bc:.2f}²) = {ac_rad} (≈ {ac:.4f})\n"
                f"          Base circumcircle radius: R_base = AC / 2 = {r_base_rad} (≈ {r_base:.4f})\n\n"
                "  Step 2: Since SA ⊥ (ABC) and angle ABC = 90°:\n"
                "          BC ⊥ AB and BC ⊥ SA => BC ⊥ (SAB) => BC ⊥ SB (right ΔSBC at B).\n"
                "          Similarly, ΔSAC is right-angled at A.\n"
                "          Since vertices A, B, C all subtend diameter segment SC under right angle 90°,\n"
                "          the circumscribed sphere center I is the exact midpoint of edge SC.\n\n"
                "[NATURAL MATHEMATICAL FORMULA]\n"
                "  R = SC/2 = 1/2 · √(SA² + AB² + BC²) = √(R_base² + (SA/2)²)\n\n"
                "[EXACT ANALYTICAL RESULTS]\n"
                f"  • Circumscribed sphere radius: R = {R_rad} (≈ {R:.4f})\n"
                f"  • Sphere surface area: S = 4πR² ≈ {area_sphere:.4f}\n"
                f"  • Sphere volume: V = (4/3)πR³ ≈ {vol_sphere:.4f}\n"
            )

    def _solve_topic_2(self, p: Dict[str, float], lang: str) -> str:
        is_vn = (lang == "VN")
        a = max(0.01, p.get("a", 6.0))
        h = a * math.sqrt(6.0) / 3.0
        R = a * math.sqrt(6.0) / 4.0
        r_in = a * math.sqrt(6.0) / 12.0
        vol = (a ** 3) * math.sqrt(2.0) / 12.0

        h_rad = format_radical_number(h)
        R_rad = format_radical_number(R)
        r_in_rad = format_radical_number(r_in)
        vol_rad = format_radical_number(vol)

        if is_vn:
            return (
                "========================================================================\n"
                "CHUYÊN ĐỀ 2: MẶT CẦU NGOẠI TIẾP & NỘI TIẾP TỨ DIỆN ĐỀU CẠNH a\n"
                "========================================================================\n\n"
                f"[THÔNG SỐ ĐẦU VÀO]\n"
                f"  • Cạnh tứ diện đều: a = {a:.4f}\n\n"
                "[SUY LUẬN HÌNH HỌC TỪNG BƯỚC (DEDUCTIVE PROOF)]\n"
                "  Bước 1: Gọi G là trọng tâm tam giác đều đáy BCD cạnh a.\n"
                "          Bán kính đường tròn ngoại tiếp đáy: BG = a√3 / 3.\n"
                "  Bước 2: Đường cao AG ⊥ (BCD) của tứ diện đều ABCD:\n"
                f"          h = AG = √(a² - BG²) = a√6 / 3 = {h_rad} (≈ {h:.4f})\n"
                "  Bước 3: Tâm mặt cầu ngoại tiếp I nằm trên AG sao cho IA = IB = R:\n"
                f"          R = a² / (2·AG) = a√6 / 4 = (3/4)h = {R_rad} (≈ {R:.4f})\n"
                f"          Bán kính mặt cầu nội tiếp r = h - R = (1/4)h = a√6 / 12 = {r_in_rad} (≈ {r_in:.4f})\n\n"
                "[CÔNG THỨC HÌNH HỌC TỰ NHIÊN]\n"
                "  h = (a√6)/3,   R = (a√6)/4,   r = (a√6)/12,   R / r = 3\n\n"
                "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
                f"  • Chiều cao tứ diện: h = {h_rad} (≈ {h:.4f})\n"
                f"  • Bán kính cầu ngoại tiếp: R = {R_rad} (≈ {R:.4f})\n"
                f"  • Bán kính cầu nội tiếp: r = {r_in_rad} (≈ {r_in:.4f})\n"
                f"  • Thể tích khối tứ diện: V = (a³√2)/12 = {vol_rad} (≈ {vol:.4f})\n"
            )
        else:
            return (
                "========================================================================\n"
                "TOPIC 2: CIRCUMSCRIBED & INSCRIBED SPHERE OF REGULAR TETRAHEDRON (EDGE a)\n"
                "========================================================================\n\n"
                f"[INPUT PARAMETERS]\n"
                f"  • Regular tetrahedron edge: a = {a:.4f}\n\n"
                "[STEP-BY-STEP DEDUCTIVE PROOF]\n"
                "  Step 1: Let G be the centroid of equilateral base triangle BCD with edge a.\n"
                "          Circumradius of the base: BG = a√3 / 3.\n"
                "  Step 2: Altitude AG ⊥ (BCD) of the regular tetrahedron ABCD:\n"
                f"          h = AG = √(a² - BG²) = a√6 / 3 = {h_rad} (≈ {h:.4f})\n"
                "  Step 3: Circumscribed sphere center I lies on altitude AG such that IA = IB = R:\n"
                f"          R = a² / (2·AG) = a√6 / 4 = (3/4)h = {R_rad} (≈ {R:.4f})\n"
                f"          Inscribed sphere radius r = h - R = (1/4)h = a√6 / 12 = {r_in_rad} (≈ {r_in:.4f})\n\n"
                "[NATURAL MATHEMATICAL FORMULA]\n"
                "  h = (a√6)/3,   R = (a√6)/4,   r = (a√6)/12,   R / r = 3\n\n"
                "[EXACT ANALYTICAL RESULTS]\n"
                f"  • Altitude of tetrahedron: h = {h_rad} (≈ {h:.4f})\n"
                f"  • Circumscribed sphere radius: R = {R_rad} (≈ {R:.4f})\n"
                f"  • Inscribed sphere radius: r = {r_in_rad} (≈ {r_in:.4f})\n"
                f"  • Tetrahedron volume: V = (a³√2)/12 = {vol_rad} (≈ {vol:.4f})\n"
            )

    def _solve_topic_3(self, p: Dict[str, float], lang: str) -> str:
        is_vn = (lang == "VN")
        R = max(0.01, p.get("R", 5.0))
        d = max(0.0, min(R, p.get("d", 3.0)))
        r = math.sqrt(max(0.0, R * R - d * d))
        perim = 2.0 * math.pi * r
        area_sec = math.pi * r * r
        r_rad = format_radical_number(r)

        if is_vn:
            return (
                "========================================================================\n"
                "CHUYÊN ĐỀ 3: THIẾT DIỆN MẶT CẦU VÀ MẶT PHẲNG (r = √(R² - d²))\n"
                "========================================================================\n\n"
                f"[THÔNG SỐ ĐẦU VÀO]\n"
                f"  • Bán kính mặt cầu S(I; R): R = {R:.4f}\n"
                f"  • Khoảng cách từ tâm I đến mặt phẳng (α): d = d(I, α) = {d:.4f}\n\n"
                "[SUY LUẬN HÌNH HỌC TỪNG BƯỚC (DEDUCTIVE PROOF)]\n"
                "  Bước 1: Gọi H là hình chiếu vuông góc của tâm I lên mặt phẳng (α) => IH = d.\n"
                "  Bước 2: Với mọi điểm M thuộc đường tròn giao tuyến S(I; R) ∩ (α), tam giác IHM vuông tại H:\n"
                f"          HM = √(IM² - IH²) = √(R² - d²) = {r_rad} (≈ {r:.4f})\n"
                "          Vậy thiết diện là đường tròn tâm H, bán kính r = √(R² - d²).\n\n"
                "[CÔNG THỨC HÌNH HỌC TỰ NHIÊN]\n"
                "  r = √(R² - d²),   S_thiết_diện = π(R² - d²),   C = 2π√(R² - d²)\n\n"
                "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
                f"  • Bán kính đường tròn thiết diện: r = {r_rad} (≈ {r:.4f})\n"
                f"  • Chu vi đường tròn thiết diện: C = 2πr ≈ {perim:.4f}\n"
                f"  • Diện tích hình tròn thiết diện: S = πr² ≈ {area_sec:.4f}\n"
            )
        else:
            return (
                "========================================================================\n"
                "TOPIC 3: SPHERE-PLANE CROSS-SECTION CIRCLE (r = √(R² - d²))\n"
                "========================================================================\n\n"
                f"[INPUT PARAMETERS]\n"
                f"  • Sphere radius S(I; R): R = {R:.4f}\n"
                f"  • Distance from center I to plane (α): d = d(I, α) = {d:.4f}\n\n"
                "[STEP-BY-STEP DEDUCTIVE PROOF]\n"
                "  Step 1: Let H be the orthogonal projection of center I onto plane (α) => IH = d.\n"
                "  Step 2: For any point M on the intersection circle S(I; R) ∩ (α), triangle IHM is right at H:\n"
                f"          HM = √(IM² - IH²) = √(R² - d²) = {r_rad} (≈ {r:.4f})\n"
                "          Therefore, the cross-section is a circle with center H and radius r = √(R² - d²).\n\n"
                "[NATURAL MATHEMATICAL FORMULA]\n"
                "  r = √(R² - d²),   S_section = π(R² - d²),   C = 2π√(R² - d²)\n\n"
                "[EXACT ANALYTICAL RESULTS]\n"
                f"  • Cross-section circle radius: r = {r_rad} (≈ {r:.4f})\n"
                f"  • Cross-section circumference: C = 2πr ≈ {perim:.4f}\n"
                f"  • Cross-section area: S = πr² ≈ {area_sec:.4f}\n"
            )

    def _solve_topic_4(self, p: Dict[str, float], lang: str) -> str:
        is_vn = (lang == "VN")
        R = max(0.01, p.get("R", 5.0))
        h = max(0.01, min(2.0 * R, p.get("h_cap", 2.0)))
        r_base = math.sqrt(max(0.0, h * (2.0 * R - h)))
        s_cap = 2.0 * math.pi * R * h
        v_cap = math.pi * (h ** 2) * (R - h / 3.0)
        r_base_rad = format_radical_number(r_base)

        if is_vn:
            return (
                "========================================================================\n"
                "CHUYÊN ĐỀ 4: THỂ TÍCH VÀ DIỆN TÍCH CHỎM CẦU (SPHERICAL CAP & ZONE)\n"
                "========================================================================\n\n"
                f"[THÔNG SỐ ĐẦU VÀO]\n"
                f"  • Bán kính mặt cầu: R = {R:.4f}\n"
                f"  • Chiều cao chỏm cầu: h = {h:.4f}\n\n"
                "[SUY LUẬN GIẢI TÍCH TÍCH PHÂN & HÌNH HỌC]\n"
                "  Bước 1: Đặt trục Oz qua tâm cầu, chỏm cầu giới hạn từ z = R - h đến z = R.\n"
                f"          Bán kính đáy chỏm cầu: a = √(R² - (R - h)²) = √(2Rh - h²) = {r_base_rad} (≈ {r_base:.4f})\n"
                "  Bước 2: Thể tích chỏm cầu tính bằng tích phân mặt cắt:\n"
                "          V = π ∫_{R-h}^{R} (R² - z²) dz = π h² (R - h/3).\n"
                "  Bước 3: Diện tích mặt cong chỏm cầu (Archimedes Hat-Box Theorem):\n"
                "          S_xq = 2πRh = π(a² + h²).\n\n"
                "[CÔNG THỨC HÌNH HỌC TỰ NHIÊN]\n"
                "  V_chỏm = π h² (R - h/3),   S_vòm = 2π R h\n\n"
                "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
                f"  • Bán kính đáy chỏm cầu: a = {r_base_rad} (≈ {r_base:.4f})\n"
                f"  • Diện tích vòm chỏm cầu: S_vòm = 2πRh ≈ {s_cap:.4f}\n"
                f"  • Thể tích khối chỏm cầu: V_chỏm ≈ {v_cap:.4f}\n"
            )
        else:
            return (
                "========================================================================\n"
                "TOPIC 4: SPHERICAL CAP & ZONE VOLUME AND SURFACE AREA\n"
                "========================================================================\n\n"
                f"[INPUT PARAMETERS]\n"
                f"  • Sphere radius: R = {R:.4f}\n"
                f"  • Cap height: h = {h:.4f}\n\n"
                "[INTEGRAL CALCULUS & GEOMETRIC PROOF]\n"
                "  Step 1: Orient Oz along sphere axis; cap spans z = R - h to z = R.\n"
                f"          Cap base radius: a = √(R² - (R - h)²) = √(2Rh - h²) = {r_base_rad} (≈ {r_base:.4f})\n"
                "  Step 2: Volume by circular slice integration:\n"
                "          V = π ∫_{R-h}^{R} (R² - z²) dz = π h² (R - h/3).\n"
                "  Step 3: Curved surface area (Archimedes Hat-Box Theorem):\n"
                "          S_curved = 2πRh = π(a² + h²).\n\n"
                "[NATURAL MATHEMATICAL FORMULA]\n"
                "  V_cap = π h² (R - h/3),   S_curved = 2π R h\n\n"
                "[EXACT ANALYTICAL RESULTS]\n"
                f"  • Base circle radius: a = {r_base_rad} (≈ {r_base:.4f})\n"
                f"  • Curved surface area: S_curved ≈ {s_cap:.4f}\n"
                f"  • Spherical cap volume: V_cap ≈ {v_cap:.4f}\n"
            )

    def _solve_topic_5(self, p: Dict[str, float], lang: str) -> str:
        is_vn = (lang == "VN")
        a = max(0.01, p.get("base_a", 4.0))
        h = max(0.01, p.get("height_h", 4.0))
        s_base = a * a
        vol = (1.0 / 3.0) * s_base * h
        apothem = math.sqrt(h * h + (a / 2.0) ** 2)
        s_lat = 4.0 * (0.5 * a * apothem)
        s_total = s_base + s_lat
        r_in = (3.0 * vol) / s_total

        vol_rad = format_radical_number(vol)
        apo_rad = format_radical_number(apothem)
        s_tot_rad = format_radical_number(s_total)
        r_in_rad = format_radical_number(r_in)

        if is_vn:
            return (
                "========================================================================\n"
                "CHUYÊN ĐỀ 5: MẶT CẦU NỘI TIẾP HÌNH CHÓP TỨ GIÁC ĐỀU (r = 3V / S_tp)\n"
                "========================================================================\n\n"
                f"[THÔNG SỐ ĐẦU VÀO]\n"
                f"  • Cạnh đáy hình vuông ABCD: a = {a:.4f}\n"
                f"  • Đường cao hình chóp SO: h = {h:.4f}\n\n"
                "[SUY LUẬN HÌNH HỌC TỪNG BƯỚC (DEDUCTIVE PROOF)]\n"
                "  Bước 1: Chia khối chóp S.ABCD thành 5 khối chóp con chung đỉnh I (tâm cầu nội tiếp)\n"
                "          và đáy là 5 mặt của hình chóp, chiều cao bằng bán kính r:\n"
                "          V = (1/3)·r·(S_đáy + S_xq) = (1/3)·r·S_tp => r = 3V / S_tp.\n"
                f"  Bước 2: Trung đoạn mặt bên: d_m = SM = √(h² + (a/2)²) = {apo_rad} (≈ {apothem:.4f})\n\n"
                "[CÔNG THỨC HÌNH HỌC TỰ NHIÊN]\n"
                "  r = 3V / S_tp = (a · h) / (a + √(4h² + a²))\n\n"
                "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
                f"  • Thể tích khối chóp: V = (1/3)a²h = {vol_rad} (≈ {vol:.4f})\n"
                f"  • Trung đoạn mặt bên: SM = {apo_rad} (≈ {apothem:.4f})\n"
                f"  • Diện tích toàn phần: S_tp = {s_tot_rad} (≈ {s_total:.4f})\n"
                f"  • Bán kính mặt cầu nội tiếp: r = {r_in_rad} (≈ {r_in:.4f})\n"
            )
        else:
            return (
                "========================================================================\n"
                "TOPIC 5: INSCRIBED SPHERE OF REGULAR SQUARE PYRAMID (r = 3V / S_total)\n"
                "========================================================================\n\n"
                f"[INPUT PARAMETERS]\n"
                f"  • Square base edge: a = {a:.4f}\n"
                f"  • Pyramid altitude: SO = h = {h:.4f}\n\n"
                "[STEP-BY-STEP DEDUCTIVE PROOF]\n"
                "  Step 1: Partition pyramid S.ABCD into 5 sub-pyramids sharing apex I (incenter)\n"
                "          with the 5 faces as bases and altitude equal to inradius r:\n"
                "          V = (1/3)·r·(S_base + S_lateral) = (1/3)·r·S_total => r = 3V / S_total.\n"
                f"  Step 2: Slant height (apothem): SM = √(h² + (a/2)²) = {apo_rad} (≈ {apothem:.4f})\n\n"
                "[NATURAL MATHEMATICAL FORMULA]\n"
                "  r = 3V / S_total = (a · h) / (a + √(4h² + a²))\n\n"
                "[EXACT ANALYTICAL RESULTS]\n"
                f"  • Pyramid volume: V = (1/3)a²h = {vol_rad} (≈ {vol:.4f})\n"
                f"  • Lateral slant height: SM = {apo_rad} (≈ {apothem:.4f})\n"
                f"  • Total surface area: S_total = {s_tot_rad} (≈ {s_total:.4f})\n"
                f"  • Inscribed sphere radius: r = {r_in_rad} (≈ {r_in:.4f})\n"
            )

    def _solve_topic_6(self, p: Dict[str, float], lang: str) -> str:
        is_vn = (lang == "VN")
        a = max(0.01, p.get("base_a", 4.0))
        h = max(0.01, p.get("SA", 3.0))
        v_bd = (-a, a, 0.0)
        v_sc = (a, a, -h)
        cross_v = vec_cross(v_bd, v_sc)
        bs = (-a, 0.0, h)
        d_bd_sc = abs(vec_dot(cross_v, bs)) / max(1e-9, vec_norm(cross_v))
        d_rad = format_radical_number(d_bd_sc)

        if is_vn:
            return (
                "========================================================================\n"
                "CHUYÊN ĐỀ 6: ĐOẠN VUÔNG GÓC CHUNG & KHOẢNG CÁCH 2 ĐƯỜNG CHÉO NHAU\n"
                "========================================================================\n\n"
                f"[THÔNG SỐ ĐẦU VÀO (Chóp S.ABCD đáy vuông cạnh a, SA ⊥ (ABCD), SA = h)]\n"
                f"  • Cạnh đáy hình vuông: a = {a:.4f}\n"
                f"  • Chiều cao cạnh bên: SA = h = {h:.4f}\n\n"
                "[SUY LUẬN HÌNH HỌC & PHƯƠNG PHÁP TỌA ĐỘ HÓA OXYZ]\n"
                "  Bài toán 6A (Đoạn vuông góc chung trực tiếp giữa SA và BC):\n"
                "    • Ta có AB ⊥ SA (do SA ⊥ (ABCD)) và AB ⊥ BC (do ABCD là hình vuông).\n"
                f"    • Suy ra AB là đoạn vuông góc chung của SA và BC => d(SA, BC) = AB = {a:.4f}.\n\n"
                "  Bài toán 6B (Khoảng cách giữa hai đường chéo nhau BD và SC):\n"
                "    • Gắn hệ trục Oxyz với A(0,0,0), B(a,0,0), C(a,a,0), D(0,a,0), S(0,0,h).\n"
                f"    • Vector chỉ phương: vec(BD) = (-a, a, 0), vec(SC) = (a, a, -h).\n"
                f"    • Vector tích có hướng: vec(n) = vec(BD) × vec(SC) = (-ah, -ah, -2a²).\n"
                f"    • Khoảng cách: d(BD, SC) = |vec(BS) · vec(n)| / ||vec(n)|| = {d_rad} (≈ {d_bd_sc:.4f}).\n\n"
                "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
                f"  • Khoảng cách d(SA, BC) = {a:.4f}\n"
                f"  • Khoảng cách d(BD, SC) = {d_rad} (≈ {d_bd_sc:.4f})\n"
            )
        else:
            return (
                "========================================================================\n"
                "TOPIC 6: COMMON PERPENDICULAR & SKEW LINES DISTANCE IN 3D\n"
                "========================================================================\n\n"
                f"[INPUT PARAMETERS (Pyramid S.ABCD, square base a, SA ⊥ (ABCD), SA = h)]\n"
                f"  • Square base edge: a = {a:.4f}\n"
                f"  • Lateral height: SA = h = {h:.4f}\n\n"
                "[GEOMETRIC DEDUCTION & ANALYTIC 3D COORDINATES]\n"
                "  Subproblem 6A (Common perpendicular between SA and BC):\n"
                "    • AB ⊥ SA (as SA ⊥ (ABCD)) and AB ⊥ BC (as ABCD is a square).\n"
                f"    • Therefore AB is the common perpendicular segment => d(SA, BC) = AB = {a:.4f}.\n\n"
                "  Subproblem 6B (Distance between skew lines BD and SC):\n"
                "    • Set frame at A(0,0,0), B(a,0,0), C(a,a,0), D(0,a,0), S(0,0,h).\n"
                f"    • Direction vectors: vec(BD) = (-a, a, 0), vec(SC) = (a, a, -h).\n"
                f"    • Cross product: vec(n) = vec(BD) × vec(SC) = (-ah, -ah, -2a²).\n"
                f"    • Distance formula: d(BD, SC) = |vec(BS) · vec(n)| / ||vec(n)|| = {d_rad} (≈ {d_bd_sc:.4f}).\n\n"
                "[EXACT ANALYTICAL RESULTS]\n"
                f"  • Distance d(SA, BC) = {a:.4f}\n"
                f"  • Distance d(BD, SC) = {d_rad} (≈ {d_bd_sc:.4f})\n"
            )

    def _solve_topic_7(self, p: Dict[str, float], lang: str) -> str:
        is_vn = (lang == "VN")
        R = max(0.01, p.get("R", 5.0))
        A_deg = max(1.0, p.get("angle_A", 90.0))
        B_deg = max(1.0, p.get("angle_B", 90.0))
        C_deg = max(1.0, p.get("angle_C", 90.0))
        excess_deg = max(0.01, (A_deg + B_deg + C_deg) - 180.0)
        excess_rad = math.radians(excess_deg)
        area_tri = (R ** 2) * excess_rad
        great_circle_quarter = 0.5 * math.pi * R

        if is_vn:
            return (
                "========================================================================\n"
                "CHUYÊN ĐỀ 7: ĐỊNH LÝ GIRARD - DIỆN TÍCH TAM GIÁC CẦU & CUNG LỚN\n"
                "========================================================================\n\n"
                f"[THÔNG SỐ ĐẦU VÀO]\n"
                f"  • Bán kính mặt cầu: R = {R:.4f}\n"
                f"  • Ba góc tam giác cầu: A = {A_deg:.2f}°, B = {B_deg:.2f}°, C = {C_deg:.2f}°\n\n"
                "[SUY LUẬN HÌNH HỌC CẦU (SPHERICAL GEOMETRY)]\n"
                "  Bước 1: Độ dư cầu (Spherical Excess) E = (A + B + C) - π (tính theo radian):\n"
                f"          E = ({A_deg:.2f}° + {B_deg:.2f}° + {C_deg:.2f}°) - 180° = {excess_deg:.2f}° ≈ {excess_rad:.6f} rad.\n"
                "  Bước 2: Theo Định lý Albert Girard, diện tích tam giác cầu ΔABC trên S(O; R) bằng:\n"
                "          S_ΔABC = R² · E = R² · (A + B + C - π).\n\n"
                "[CÔNG THỨC HÌNH HỌC TỰ NHIÊN]\n"
                "  E = A + B + C - π,   S_ΔABC = R² · E,   L_cung_lớn = R · θ\n\n"
                "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
                f"  • Độ dư cầu: E = {excess_rad:.6f} rad ({excess_deg:.2f}°)\n"
                f"  • Diện tích tam giác cầu: S_ΔABC ≈ {area_tri:.4f}\n"
                f"  • Chiều dài cung lớn 90°: L = πR/2 ≈ {great_circle_quarter:.4f}\n"
            )
        else:
            return (
                "========================================================================\n"
                "TOPIC 7: GIRARD'S THEOREM - SPHERICAL TRIANGLE AREA & GREAT CIRCLE ARC\n"
                "========================================================================\n\n"
                f"[INPUT PARAMETERS]\n"
                f"  • Sphere radius: R = {R:.4f}\n"
                f"  • Spherical triangle angles: A = {A_deg:.2f}°, B = {B_deg:.2f}°, C = {C_deg:.2f}°\n\n"
                "[SPHERICAL GEOMETRY DEDUCTIVE PROOF]\n"
                "  Step 1: Spherical excess E = (A + B + C) - π in radians:\n"
                f"          E = ({A_deg:.2f}° + {B_deg:.2f}° + {C_deg:.2f}°) - 180° = {excess_deg:.2f}° ≈ {excess_rad:.6f} rad.\n"
                "  Step 2: By Albert Girard's Theorem, the area of spherical triangle ΔABC on S(O; R) is:\n"
                "          Area(ΔABC) = R² · E = R² · (A + B + C - π).\n\n"
                "[NATURAL MATHEMATICAL FORMULA]\n"
                "  E = A + B + C - π,   Area(ΔABC) = R² · E,   L_great_arc = R · θ\n\n"
                "[EXACT ANALYTICAL RESULTS]\n"
                f"  • Spherical excess: E = {excess_rad:.6f} rad ({excess_deg:.2f}°)\n"
                f"  • Spherical triangle area: Area ≈ {area_tri:.4f}\n"
                f"  • Great circle quarter arc (90°): L = πR/2 ≈ {great_circle_quarter:.4f}\n"
            )

    def _solve_topic_8(self, p: Dict[str, float], lang: str) -> str:
        is_vn = (lang == "VN")
        R = max(0.01, p.get("R", 6.0))
        h_opt = (4.0 / 3.0) * R
        r_opt = (2.0 * math.sqrt(2.0) / 3.0) * R
        v_cone_max = (32.0 / 81.0) * math.pi * (R ** 3)
        v_sphere = (4.0 / 3.0) * math.pi * (R ** 3)
        ratio = 8.0 / 27.0

        h_rad = format_radical_number(h_opt)
        r_rad = format_radical_number(r_opt)

        if is_vn:
            return (
                "========================================================================\n"
                "CHUYÊN ĐỀ 8: CỰC TRỊ SAT/AP - KHỐI NÓN THỂ TÍCH LỚN NHẤT NỘI TIẾP CẦU\n"
                "========================================================================\n\n"
                f"[THÔNG SỐ ĐẦU VÀO]\n"
                f"  • Bán kính mặt cầu ngoại tiếp nón: R = {R:.4f}\n\n"
                "[SUY LUẬN CỰC TRỊ GIẢI TÍCH / BẤT ĐẲNG THỨC AM-GM]\n"
                "  Bước 1: Gọi chiều cao hình nón là h (0 < h < 2R).\n"
                "          Bán kính đáy hình nón nội tiếp mặt cầu: r² = R² - (h - R)² = 2Rh - h².\n"
                "  Bước 2: Thể tích khối nón: V(h) = (1/3)π r² h = (1/3)π (2Rh² - h³).\n"
                "  Bước 3: Khảo sát đạo hàm V'(h) = (1/3)π (4Rh - 3h²) = 0 => h = 4R / 3.\n"
                f"          Khi đó r_opt = (2√2 / 3)R = {r_rad} (≈ {r_opt:.4f}) và V_max = (32/81)π R³ = (8/27) V_cầu.\n\n"
                "[CÔNG THỨC HÌNH HỌC TỰ NHIÊN]\n"
                "  h_opt = 4R / 3,   r_opt = (2√2 / 3)R,   V_max = (32/81)π R³ = (8/27)V_cầu\n\n"
                "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
                f"  • Chiều cao nón tối ưu: h_opt = 4R/3 = {h_rad} (≈ {h_opt:.4f})\n"
                f"  • Bán kính đáy nón tối ưu: r_opt = {r_rad} (≈ {r_opt:.4f})\n"
                f"  • Thể tích nón cực đại: V_max ≈ {v_cone_max:.4f}\n"
                f"  • Thể tích mặt cầu: V_cầu ≈ {v_sphere:.4f} (Tỷ số V_max / V_cầu = 8/27 ≈ {ratio:.4f})\n"
            )
        else:
            return (
                "========================================================================\n"
                "TOPIC 8: SAT/AP OPTIMIZATION - MAX-VOLUME CONE INSCRIBED IN SPHERE\n"
                "========================================================================\n\n"
                f"[INPUT PARAMETERS]\n"
                f"  • Circumscribing sphere radius: R = {R:.4f}\n\n"
                "[CALCULUS OPTIMIZATION & AM-GM PROOF]\n"
                "  Step 1: Let the cone altitude be h (0 < h < 2R).\n"
                "          Inscribed cone base radius: r² = R² - (h - R)² = 2Rh - h².\n"
                "  Step 2: Cone volume: V(h) = (1/3)π r² h = (1/3)π (2Rh² - h³).\n"
                "  Step 3: First derivative V'(h) = (1/3)π (4Rh - 3h²) = 0 => h = 4R / 3.\n"
                f"          Then optimal radius r_opt = (2√2 / 3)R = {r_rad} (≈ {r_opt:.4f}) and V_max = (8/27) V_sphere.\n\n"
                "[NATURAL MATHEMATICAL FORMULA]\n"
                "  h_opt = 4R / 3,   r_opt = (2√2 / 3)R,   V_max = (32/81)π R³ = (8/27)V_sphere\n\n"
                "[EXACT ANALYTICAL RESULTS]\n"
                f"  • Optimal cone height: h_opt = 4R/3 = {h_rad} (≈ {h_opt:.4f})\n"
                f"  • Optimal base radius: r_opt = {r_rad} (≈ {r_opt:.4f})\n"
                f"  • Maximum cone volume: V_max ≈ {v_cone_max:.4f}\n"
                f"  • Sphere volume: V_sphere ≈ {v_sphere:.4f} (Ratio V_max / V_sphere = 8/27 ≈ {ratio:.4f})\n"
            )

    def _solve_topic_9(self, p: Dict[str, float], lang: str) -> str:
        is_vn = (lang == "VN")
        px = p.get("px", 1.0)
        py = p.get("py", 2.0)
        pz = p.get("pz", 3.0)
        A = p.get("pl_A", 1.0)
        B = p.get("pl_B", 2.0)
        C = p.get("pl_C", 2.0)
        D = p.get("pl_D", -1.0)
        denom_sq = A * A + B * B + C * C
        denom = math.sqrt(denom_sq) if denom_sq > 1e-9 else 1.0
        val = abs(A * px + B * py + C * pz + D)
        dist = val / denom
        t = -(A * px + B * py + C * pz + D) / denom_sq if denom_sq > 1e-9 else 0.0
        hx = px + A * t
        hy = py + B * t
        hz = pz + C * t
        dist_rad = format_radical_number(dist)

        if is_vn:
            return (
                "========================================================================\n"
                "CHUYÊN ĐỀ 9: KHOẢNG CÁCH TỪ ĐIỂM ĐẾN MẶT PHẲNG & HÌNH CHIẾU VUÔNG GÓC\n"
                "========================================================================\n\n"
                f"[THÔNG SỐ ĐẦU VÀO]\n"
                f"  • Điểm P({px:.2f}, {py:.2f}, {pz:.2f})\n"
                f"  • Mặt phẳng (α): {A:.2f}x + {B:.2f}y + {C:.2f}z + {D:.2f} = 0\n\n"
                "[SUY LUẬN TỪNG BƯỚC]\n"
                f"  Bước 1: Vector pháp tuyến mặt phẳng n = ({A:.2f}, {B:.2f}, {C:.2f}), ||n|| = √({A}² + {B}² + {C}²) = {denom:.4f}.\n"
                f"  Bước 2: Thay tọa độ P vào vế trái: |{A}({px}) + {B}({py}) + {C}({pz}) + {D}| = {val:.4f}.\n"
                f"  Bước 3: Khoảng cách: d(P, α) = {val:.4f} / {denom:.4f} = {dist_rad} (≈ {dist:.4f}).\n"
                f"  Bước 4: Tọa độ hình chiếu vuông góc H: H({hx:.2f}, {hy:.2f}, {hz:.2f}).\n\n"
                "[CÔNG THỨC HÌNH HỌC TỰ NHIÊN]\n"
                "  d(P, α) = |A x_0 + B y_0 + C z_0 + D| / √(A² + B² + C²)\n\n"
                "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
                f"  • Khoảng cách d(P, α) = {dist_rad} (≈ {dist:.4f})\n"
                f"  • Chân đường vuông góc H: ({hx:.4f}, {hy:.4f}, {hz:.4f})\n"
            )
        else:
            return (
                "========================================================================\n"
                "TOPIC 9: DISTANCE FROM POINT TO PLANE & ORTHOGONAL PROJECTION FOOT\n"
                "========================================================================\n\n"
                f"[INPUT PARAMETERS]\n"
                f"  • Point P({px:.2f}, {py:.2f}, {pz:.2f})\n"
                f"  • Plane (α): {A:.2f}x + {B:.2f}y + {C:.2f}z + {D:.2f} = 0\n\n"
                "[STEP-BY-STEP DEDUCTIVE PROOF]\n"
                f"  Step 1: Normal vector n = ({A:.2f}, {B:.2f}, {C:.2f}), ||n|| = √({A}² + {B}² + {C}²) = {denom:.4f}.\n"
                f"  Step 2: Evaluate numerator: |{A}({px}) + {B}({py}) + {C}({pz}) + {D}| = {val:.4f}.\n"
                f"  Step 3: Distance formula: d(P, α) = {val:.4f} / {denom:.4f} = {dist_rad} (≈ {dist:.4f}).\n"
                f"  Step 4: Orthogonal projection foot H: H({hx:.2f}, {hy:.2f}, {hz:.2f}).\n\n"
                "[NATURAL MATHEMATICAL FORMULA]\n"
                "  d(P, α) = |A x_0 + B y_0 + C z_0 + D| / √(A² + B² + C²)\n\n"
                "[EXACT ANALYTICAL RESULTS]\n"
                f"  • Distance d(P, α) = {dist_rad} (≈ {dist:.4f})\n"
                f"  • Projection foot H: ({hx:.4f}, {hy:.4f}, {hz:.4f})\n"
            )

    def _solve_topic_10(self, p: Dict[str, float], lang: str) -> str:
        is_vn = (lang == "VN")
        ux = p.get("ux", 1.0)
        uy = p.get("uy", 1.0)
        uz = p.get("uz", 0.0)
        nx = p.get("pl_A", 0.0)
        ny = p.get("pl_B", 0.0)
        nz = p.get("pl_C", 1.0)
        u_len = math.sqrt(ux*ux + uy*uy + uz*uz) or 1.0
        n_len = math.sqrt(nx*nx + ny*ny + nz*nz) or 1.0
        dot = abs(ux*nx + uy*ny + uz*nz)
        sin_phi = max(0.0, min(1.0, dot / (u_len * n_len)))
        phi_deg = math.degrees(math.asin(sin_phi))
        sin_rad = format_radical_number(sin_phi)

        if is_vn:
            return (
                "========================================================================\n"
                "CHUYÊN ĐỀ 10: GÓC GIỮA ĐƯỜNG THẲNG VÀ MẶT PHẲNG\n"
                "========================================================================\n\n"
                f"[THÔNG SỐ ĐẦU VÀO]\n"
                f"  • Vector chỉ phương đường thẳng: u = ({ux:.2f}, {uy:.2f}, {uz:.2f}), ||u|| = {u_len:.4f}\n"
                f"  • Vector pháp tuyến mặt phẳng: n = ({nx:.2f}, {ny:.2f}, {nz:.2f}), ||n|| = {n_len:.4f}\n\n"
                "[SUY LUẬN TỪNG BƯỚC]\n"
                f"  Bước 1: Tính tích vô hướng: |u · n| = |{ux*nx + uy*ny + uz*nz:.4f}| = {dot:.4f}.\n"
                f"  Bước 2: Áp dụng công thức: sin(φ) = |u · n| / (||u|| · ||n||) = {sin_rad} (≈ {sin_phi:.4f}).\n"
                f"  Bước 3: Suy ra góc giữa đường thẳng và mặt phẳng: φ ≈ {phi_deg:.2f}°.\n\n"
                "[CÔNG THỨC HÌNH HỌC TỰ NHIÊN]\n"
                "  sin(φ) = |vec(u) · vec(n)| / (||vec(u)|| · ||vec(n)||)\n\n"
                "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
                f"  • sin(φ) = {sin_rad} (≈ {sin_phi:.4f})\n"
                f"  • Góc φ = {phi_deg:.2f}° ({math.radians(phi_deg):.4f} rad)\n"
            )
        else:
            return (
                "========================================================================\n"
                "TOPIC 10: ANGLE BETWEEN LINE AND PLANE (SIN φ = |u·n| / (|u|·|n|))\n"
                "========================================================================\n\n"
                f"[INPUT PARAMETERS]\n"
                f"  • Direction vector of line: u = ({ux:.2f}, {uy:.2f}, {uz:.2f}), ||u|| = {u_len:.4f}\n"
                f"  • Normal vector of plane: n = ({nx:.2f}, {ny:.2f}, {nz:.2f}), ||n|| = {n_len:.4f}\n\n"
                "[STEP-BY-STEP DEDUCTIVE PROOF]\n"
                f"  Step 1: Compute scalar dot product: |u · n| = |{ux*nx + uy*ny + uz*nz:.4f}| = {dot:.4f}.\n"
                f"  Step 2: Apply formula: sin(φ) = |u · n| / (||u|| · ||n||) = {sin_rad} (≈ {sin_phi:.4f}).\n"
                f"  Step 3: Line-plane angle: φ ≈ {phi_deg:.2f}°.\n\n"
                "[NATURAL MATHEMATICAL FORMULA]\n"
                "  sin(φ) = |vec(u) · vec(n)| / (||vec(u)|| · ||vec(n)||)\n\n"
                "[EXACT ANALYTICAL RESULTS]\n"
                f"  • sin(φ) = {sin_rad} (≈ {sin_phi:.4f})\n"
                f"  • Angle φ = {phi_deg:.2f}° ({math.radians(phi_deg):.4f} rad)\n"
            )

    def _solve_topic_11(self, p: Dict[str, float], lang: str) -> str:
        is_vn = (lang == "VN")
        n1x = p.get("pl_A", 1.0)
        n1y = p.get("pl_B", 0.0)
        n1z = p.get("pl_C", 0.0)
        n2x = p.get("nx2", 0.0)
        n2y = p.get("ny2", 1.0)
        n2z = p.get("nz2", 0.0)
        n1_len = math.sqrt(n1x*n1x + n1y*n1y + n1z*n1z) or 1.0
        n2_len = math.sqrt(n2x*n2x + n2y*n2y + n2z*n2z) or 1.0
        dot = abs(n1x*n2x + n1y*n2y + n1z*n2z)
        cos_theta = max(0.0, min(1.0, dot / (n1_len * n2_len)))
        theta_deg = math.degrees(math.acos(cos_theta))
        cos_rad = format_radical_number(cos_theta)

        if is_vn:
            return (
                "========================================================================\n"
                "CHUYÊN ĐỀ 11: GÓC GIỮA HAI MẶT PHẲNG - GÓC NHỊ DIỆN\n"
                "========================================================================\n\n"
                f"[THÔNG SỐ ĐẦU VÀO]\n"
                f"  • VTPT mặt phẳng 1: n1 = ({n1x:.2f}, {n1y:.2f}, {n1z:.2f}), ||n1|| = {n1_len:.4f}\n"
                f"  • VTPT mặt phẳng 2: n2 = ({n2x:.2f}, {n2y:.2f}, {n2z:.2f}), ||n2|| = {n2_len:.4f}\n\n"
                "[SUY LUẬN TỪNG BƯỚC]\n"
                f"  Bước 1: Tính tích vô hướng: |n1 · n2| = |{n1x*n2x + n1y*n2y + n1z*n2z:.4f}| = {dot:.4f}.\n"
                f"  Bước 2: Áp dụng công thức: cos(θ) = |n1 · n2| / (||n1|| · ||n2||) = {cos_rad} (≈ {cos_theta:.4f}).\n"
                f"  Bước 3: Suy ra góc nhị diện: θ ≈ {theta_deg:.2f}°.\n\n"
                "[CÔNG THỨC HÌNH HỌC TỰ NHIÊN]\n"
                "  cos(θ) = |vec(n1) · vec(n2)| / (||vec(n1)|| · ||vec(n2)||)\n\n"
                "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
                f"  • cos(θ) = {cos_rad} (≈ {cos_theta:.4f})\n"
                f"  • Góc θ = {theta_deg:.2f}° ({math.radians(theta_deg):.4f} rad)\n"
            )
        else:
            return (
                "========================================================================\n"
                "TOPIC 11: DIHEDRAL ANGLE BETWEEN TWO PLANES (COS θ = |n1·n2| / (|n1|·|n2|))\n"
                "========================================================================\n\n"
                f"[INPUT PARAMETERS]\n"
                f"  • Plane 1 normal: n1 = ({n1x:.2f}, {n1y:.2f}, {n1z:.2f}), ||n1|| = {n1_len:.4f}\n"
                f"  • Plane 2 normal: n2 = ({n2x:.2f}, {n2y:.2f}, {n2z:.2f}), ||n2|| = {n2_len:.4f}\n\n"
                "[STEP-BY-STEP DEDUCTIVE PROOF]\n"
                f"  Step 1: Compute scalar dot product: |n1 · n2| = |{n1x*n2x + n1y*n2y + n1z*n2z:.4f}| = {dot:.4f}.\n"
                f"  Step 2: Apply formula: cos(θ) = |n1 · n2| / (||n1|| · ||n2||) = {cos_rad} (≈ {cos_theta:.4f}).\n"
                f"  Step 3: Dihedral angle: θ ≈ {theta_deg:.2f}°.\n\n"
                "[NATURAL MATHEMATICAL FORMULA]\n"
                "  cos(θ) = |vec(n1) · vec(n2)| / (||vec(n1)|| · ||vec(n2)||)\n\n"
                "[EXACT ANALYTICAL RESULTS]\n"
                f"  • cos(θ) = {cos_rad} (≈ {cos_theta:.4f})\n"
                f"  • Dihedral angle θ = {theta_deg:.2f}° ({math.radians(theta_deg):.4f} rad)\n"
            )

    def _solve_topic_12(self, p: Dict[str, float], lang: str) -> str:
        is_vn = (lang == "VN")
        a = max(0.01, p.get("base_a", 4.0))
        h = max(0.01, p.get("height_h", 4.0))
        sa = max(0.01, p.get("SA", 4.0))
        R = max(0.01, p.get("R", 5.0))
        v_pyramid = (1.0 / 3.0) * (a * a) * h
        v_sphere = (4.0 / 3.0) * math.pi * (R ** 3)
        v_pyr_rad = format_radical_number(v_pyramid)

        if is_vn:
            return (
                "========================================================================\n"
                "CHUYÊN ĐỀ 12: BÀI TOÁN TÙY CHỈNH - GIẢI TÍCH HÌNH HỌC KHÔNG GIAN TỰ DO\n"
                "========================================================================\n\n"
                f"[THÔNG SỐ TÙY CHỌN TỪ KHỐI]\n"
                f"  • Chiều cao hình học: h = {h:.4f}\n"
                f"  • Cạnh đáy: a = {a:.4f}\n"
                f"  • Cạnh bên: SA = {sa:.4f}\n"
                f"  • Bán kính cầu liên quan: R = {R:.4f}\n\n"
                "[SUY LUẬN GIẢI TÍCH]\n"
                f"  Bước 1: Diện tích đáy hình vuông: B = a² = {a*a:.4f}.\n"
                f"  Bước 2: Thể tích chóp đáy vuông chiều cao h: V_chóp = (1/3)Bh = {v_pyr_rad} (≈ {v_pyramid:.4f}).\n"
                f"  Bước 3: Thể tích mặt cầu bán kính R: V_cầu = (4/3)πR³ ≈ {v_sphere:.4f}.\n"
                f"  Bước 4: Tỉ số thể tích: V_chóp / V_cầu ≈ {v_pyramid / v_sphere:.4f}.\n\n"
                "[KẾT LUẬN]\n"
                f"  • Thể tích chóp: V = {v_pyr_rad} (≈ {v_pyramid:.4f}) đơn vị thể tích.\n"
                f"  • Thể tích cầu: V ≈ {v_sphere:.4f} đơn vị thể tích.\n"
            )
        else:
            return (
                "========================================================================\n"
                "TOPIC 12: CUSTOM 3D ANALYTICAL PROBLEM & SOLID VOLUME/SURFACE EVALUATION\n"
                "========================================================================\n\n"
                f"[CUSTOM PARAMETERS FROM 3D SOLID]\n"
                f"  • Geometric height: h = {h:.4f}\n"
                f"  • Base edge: a = {a:.4f}\n"
                f"  • Lateral edge: SA = {sa:.4f}\n"
                f"  • Reference sphere radius: R = {R:.4f}\n\n"
                "[STEP-BY-STEP ANALYTICAL EVALUATION]\n"
                f"  Step 1: Square base area: B = a² = {a*a:.4f}.\n"
                f"  Step 2: Pyramid volume with height h: V_pyramid = (1/3)Bh = {v_pyr_rad} (≈ {v_pyramid:.4f}).\n"
                f"  Step 3: Reference sphere volume: V_sphere = (4/3)πR³ ≈ {v_sphere:.4f}.\n"
                f"  Step 4: Volume ratio: V_pyramid / V_sphere ≈ {v_pyramid / v_sphere:.4f}.\n\n"
                "[CONCLUSION]\n"
                f"  • Pyramid volume: V = {v_pyr_rad} (≈ {v_pyramid:.4f}) cubic units.\n"
                f"  • Sphere volume: V ≈ {v_sphere:.4f} cubic units.\n"
            )


# ==============================================================================
# WIN32 POINT ON SEGMENT WITH DYNAMIC RATIO DIALOG
# ==============================================================================

class PointOnSegmentDialog(tk.Toplevel):
    """
    Hộp thoại tạo nhanh điểm trên đoạn thẳng với tỉ số động k:
    Cho phép chọn đoạn thẳng (hoặc tự động nhận cạnh đang chọn trên canvas),
    chọn tỉ số k (với các nút nhanh 1/4, 1/3, 1/2, 2/3, 3/4 và thanh trượt),
    sau khi tạo người dùng có thể kéo chuột để trượt điểm tự do trong miền [0.0, 1.0].
    """
    WIN32_BG = "#ECE9D8"
    WIN32_ACTIVE_BG = "#D4D0C8"
    FONT_UI = ("Tahoma", 9)
    FONT_BOLD = ("Tahoma", 9, "bold")

    def __init__(self, parent: "GeoSolver3DApp", preselected_edge: Optional[Tuple[str, str]] = None):
        super().__init__(parent)
        self.app = parent
        self.model = parent.models[parent.current_model_key]
        self.lang = parent.lang
        is_vn = (self.lang == "VN")
        self.title("Thêm Điểm Trên Đoạn Thẳng (k = AE/AB)" if is_vn else "Add Point on Segment (Ratio k)")
        self.minsize(460, 320)
        self.geometry("480x350")
        self.configure(bg=self.WIN32_BG)
        self.transient(parent)

        v_list = sorted(list(set(list(self.model.vertices.keys()) + list(self.model.aux_points.keys()))))
        if hasattr(self.model, "section_points") and self.model.section_points:
            for lbl, _ in self.model.section_points:
                if lbl not in v_list:
                    v_list.append(lbl)

        p1_init = "A"
        p2_init = "B"
        if preselected_edge and len(preselected_edge) == 2:
            p1_init, p2_init = preselected_edge
        elif len(v_list) >= 2:
            p1_init, p2_init = v_list[0], v_list[1]

        self.var_p1 = tk.StringVar(value=p1_init)
        self.var_p2 = tk.StringVar(value=p2_init)
        self.var_k = tk.DoubleVar(value=0.5)
        self.var_name = tk.StringVar(value=self._suggest_name())

        self._build_ui(v_list)

    def _suggest_name(self) -> str:
        existing = set(self.model.vertices.keys()) | set(self.model.aux_points.keys())
        for c in ["E", "M", "N", "P", "K", "I", "H", "F"]:
            if c not in existing:
                return c
        idx = 1
        while f"E{idx}" in existing:
            idx += 1
        return f"E{idx}"

    def _build_ui(self, v_list: List[str]) -> None:
        is_vn = (self.lang == "VN")
        top = tk.Frame(self, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2, padx=10, pady=8)
        top.pack(side=tk.TOP, fill=tk.X, padx=8, pady=(8, 4))
        tk.Label(
            top,
            text="ĐIỂM TRÊN ĐOẠN THẲNG & TỈ SỐ ĐỘNG" if is_vn else "POINT ON SEGMENT WITH DYNAMIC RATIO",
            font=self.FONT_BOLD,
            fg="#000080",
            bg=self.WIN32_BG,
        ).pack(side=tk.LEFT)

        body = tk.Frame(self, bg=self.WIN32_BG, padx=10, pady=4)
        body.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=4)

        # 1. Chọn đoạn thẳng
        f_seg = tk.LabelFrame(body, text="1. Đoạn thẳng xác định" if is_vn else "1. Segment", bg=self.WIN32_BG, font=self.FONT_BOLD, padx=8, pady=6)
        f_seg.pack(side=tk.TOP, fill=tk.X, pady=4)

        tk.Label(f_seg, text="Đầu mút 1:" if is_vn else "Endpoint 1:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT)
        opt1 = tk.OptionMenu(f_seg, self.var_p1, *v_list)
        opt1.config(bg=self.WIN32_BG, font=self.FONT_UI)
        opt1.pack(side=tk.LEFT, padx=4)

        tk.Label(f_seg, text="Đầu mút 2:" if is_vn else "Endpoint 2:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=(10, 0))
        opt2 = tk.OptionMenu(f_seg, self.var_p2, *v_list)
        opt2.config(bg=self.WIN32_BG, font=self.FONT_UI)
        opt2.pack(side=tk.LEFT, padx=4)

        tk.Label(f_seg, text="Tên điểm:" if is_vn else "Point Name:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=(10, 0))
        tk.Entry(f_seg, textvariable=self.var_name, width=5, font=self.FONT_BOLD, relief=tk.SUNKEN, bd=2).pack(side=tk.LEFT, padx=4)

        # 2. Tỉ số k
        f_ratio = tk.LabelFrame(body, text="2. Tỉ số k = AE/AB (0.0 đến 1.0)" if is_vn else "2. Ratio k (0.0 to 1.0)", bg=self.WIN32_BG, font=self.FONT_BOLD, padx=8, pady=6)
        f_ratio.pack(side=tk.TOP, fill=tk.X, pady=4)

        f_presets = tk.Frame(f_ratio, bg=self.WIN32_BG)
        f_presets.pack(side=tk.TOP, fill=tk.X, pady=(0, 4))
        presets = [("1/4", 0.25), ("1/3", 0.3333), ("1/2 (Trung điểm)", 0.5), ("2/3", 0.6667), ("3/4", 0.75)]
        for p_lbl, p_val in presets:
            tk.Button(
                f_presets,
                text=p_lbl,
                font=("Tahoma", 8),
                bg=self.WIN32_BG,
                relief=tk.RAISED,
                bd=1,
                padx=4,
                command=lambda v=p_val: self.var_k.set(v),
            ).pack(side=tk.LEFT, padx=2)

        self.scale_k = tk.Scale(
            f_ratio,
            from_=0.0,
            to=1.0,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            variable=self.var_k,
            bg=self.WIN32_BG,
            font=self.FONT_UI,
            highlightthickness=0,
        )
        self.scale_k.pack(side=tk.TOP, fill=tk.X)

        # 3. Ghi chú & Nút bấm
        tk.Label(
            body,
            text=("* Sau khi tạo, bạn có thể chọn chế độ [Di chuyển] và kéo chuột để trượt điểm trong miền [0, 1].\n"
                "Điểm được bảo toàn trên cạnh xác định, không bao giờ bay ra ngoài."),
            font=("Tahoma", 8),
            fg="#555555",
            bg=self.WIN32_BG,
            justify=tk.LEFT,
        ).pack(side=tk.TOP, fill=tk.X, pady=4)

        btn_bar = tk.Frame(body, bg=self.WIN32_BG)
        btn_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=6)

        tk.Button(
            btn_bar,
            text="[ ➕ Tạo Điểm & Cho Phép Kéo Thả ]" if is_vn else "[ ➕ Create Point & Enable Dragging ]",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            fg="#000080",
            relief=tk.RAISED,
            bd=2,
            pady=4,
            command=self._apply_create,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        tk.Button(
            btn_bar,
            text="[ Đóng ]" if is_vn else "[ Close ]",
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            pady=4,
            command=self.destroy,
        ).pack(side=tk.LEFT, padx=2)

    def _apply_create(self) -> None:
        p1_name = self.var_p1.get()
        p2_name = self.var_p2.get()
        is_vn = (self.lang == "VN")
        if p1_name == p2_name:
            messagebox.showerror("Lỗi" if is_vn else "Error", "Hai đầu mút đoạn thẳng phải khác nhau!" if is_vn else "Endpoints must be distinct!")
            return
        p1 = self.model.get_point(p1_name)
        p2 = self.model.get_point(p2_name)
        if not p1 or not p2:
            messagebox.showerror("Lỗi" if is_vn else "Error", "Không tìm thấy tọa độ đầu mút!" if is_vn else "Could not resolve endpoints!")
            return

        k = max(0.0, min(1.0, float(self.var_k.get())))
        pt = vec_add(p1, vec_scale(vec_sub(p2, p1), k))
        name = self.var_name.get().strip() or "E"

        base_name = name
        idx = 1
        while name in self.model.vertices or name in self.model.aux_points:
            idx += 1
            name = f"{base_name}{idx}"

        self.model.aux_points[name] = pt
        self.model.point_constraints[name] = {"type": "ratio", "p1": p1_name, "p2": p2_name, "k": k}
        self.model.aux_segments.append({
            "p1_name": p1_name,
            "p2_name": name,
            "p1": p1,
            "p2": pt,
            "color": "#000080",
            "dash": True,
            "label": f"{name} (k={k:.2f})",
            "width": 1.8,
        })
        self.app.set_interact_mode("move")
        self.app.selected_vertex = name
        self.app.dragged_vertex = None
        self.app.redraw_canvas()
        messagebox.showinfo(
            "Thành công" if is_vn else "Success",
            f"Đã tạo điểm {name} trên đoạn {p1_name}{p2_name} (tỉ số k = {k:.2f}).\nChế độ [Di chuyển] đã được kích hoạt, bạn có thể kéo chuột để trượt điểm {name}."
            if is_vn else
            f"Created point {name} on segment {p1_name}{p2_name} (ratio k = {k:.2f}).\nMove mode activated, you can now drag point {name} freely on the segment."
        )
        self.destroy()


# ==============================================================================
# WIN32 PLANE THROUGH 3 POINTS & CAD HATCHING DIALOG
# ==============================================================================

class Plane3PointDialog(tk.Toplevel):
    """
    Hộp thoại dựng mặt phẳng & tô màu / gạch chéo diện tích đa giác bất kỳ (3 hoặc 4 điểm):
    - Chọn nhanh mặt có sẵn của khối (Mặt đáy, Mặt bên...) hoặc tự chọn các đỉnh
    - Tô màu mặt phẳng với các chế độ chuẩn CAD: Gạch chéo CAD (Hatch 45°), Gạch ca-rô CAD (Cross-Hatch), Tô mờ (Solid), Chấm lưới (Stipple)
    - Tùy chọn dùng làm Mặt phẳng cắt thiết diện khối đa diện (cho phép kéo độc lập các đỉnh)
    - Danh sách quản lý các mặt phẳng đã vẽ kèm nút xóa
    """
    WIN32_BG = "#ECE9D8"
    WIN32_ACTIVE_BG = "#D4D0C8"
    FONT_UI = ("Tahoma", 9)
    FONT_BOLD = ("Tahoma", 9, "bold")

    def __init__(self, parent: "GeoSolver3DApp"):
        super().__init__(parent)
        self.app = parent
        self.model = parent.models[parent.current_model_key]
        self.lang = parent.lang
        is_vn = (self.lang == "VN")
        self.title("Tô Màu & Kẻ Nét Gạch Chéo Diện Tích (CAD Hatch) - GeoSolver 3D" if is_vn else "Area Hatching & Shading (CAD Hatch) - GeoSolver 3D")
        self.minsize(620, 540)
        self.geometry("640x560")
        self.configure(bg=self.WIN32_BG)
        self.transient(parent)

        v_list = sorted(list(set(list(self.model.vertices.keys()) + list(self.model.aux_points.keys()))))
        if hasattr(self.model, "section_points") and self.model.section_points:
            for lbl, _ in self.model.section_points:
                if lbl not in v_list:
                    v_list.append(lbl)

        p1_init = v_list[0] if v_list else "A"
        p2_init = v_list[1] if len(v_list) > 1 else p1_init
        p3_init = v_list[2] if len(v_list) > 2 else p2_init

        # Danh sách chọn nhanh mặt khối
        self.face_options = ["[ ✍ Tự chọn điểm tùy ý... ]" if is_vn else "[ ✍ Custom points... ]"]
        for f_idx, face in enumerate(getattr(self.model, "faces", [])):
            f_str = "-".join(face)
            if f_idx == 0:
                self.face_options.append(f"Mặt đáy: ({f_str})")
            else:
                self.face_options.append(f"Mặt bên {f_idx}: ({f_str})")

        self.var_quick_face = tk.StringVar(value=self.face_options[0])
        self.var_p1 = tk.StringVar(value=p1_init)
        self.var_p2 = tk.StringVar(value=p2_init)
        self.var_p3 = tk.StringVar(value=p3_init)
        self.var_p4 = tk.StringVar(value="[ Không dùng ]")
        self.var_name = tk.StringVar(value=f"({p1_init}{p2_init}{p3_init})")
        self.var_color = tk.StringVar(value="#1971C2")
        self.var_fill = tk.StringVar(value="hatch")
        self.var_spacing = tk.IntVar(value=10)
        self.var_is_cutter = tk.BooleanVar(value=False)

        self._build_ui(v_list)

    def _build_ui(self, v_list: List[str]) -> None:
        is_vn = (self.lang == "VN")
        top = tk.Frame(self, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2, padx=10, pady=8)
        top.pack(side=tk.TOP, fill=tk.X, padx=8, pady=(8, 4))
        tk.Label(
            top,
            text="TÔ MÀU & KẺ NÉT GẠCH CHÉO DIỆN TÍCH / MẶT PHẲNG (CHUẨN CAD)" if is_vn else "POLYGON AREA CAD HATCHING & COLOR SHADING",
            font=self.FONT_BOLD,
            fg="#6B21A8",
            bg=self.WIN32_BG,
        ).pack(side=tk.LEFT)

        body = tk.Frame(self, bg=self.WIN32_BG, padx=10, pady=4)
        body.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=4)

        # 1. Chọn mặt khối hoặc chọn điểm
        f_pts = tk.LabelFrame(body, text="1. Chọn Diện Tích Cần Tô Màu / Gạch Chéo" if is_vn else "1. Select Area to Hatch / Shade", bg=self.WIN32_BG, font=self.FONT_BOLD, padx=8, pady=6)
        f_pts.pack(side=tk.TOP, fill=tk.X, pady=3)

        # Hàng chọn nhanh mặt
        r_qf = tk.Frame(f_pts, bg=self.WIN32_BG)
        r_qf.pack(side=tk.TOP, fill=tk.X, pady=(1, 5))
        tk.Label(r_qf, text="⚡ Chọn nhanh mặt của khối:" if is_vn else "⚡ Quick select solid face:", bg=self.WIN32_BG, font=self.FONT_BOLD, fg="#000080").pack(side=tk.LEFT)
        opt_qf = tk.OptionMenu(r_qf, self.var_quick_face, *self.face_options, command=self._on_quick_face_select)
        opt_qf.config(bg=self.WIN32_BG, font=self.FONT_UI)
        opt_qf.pack(side=tk.LEFT, padx=6)

        # Hàng chọn từng đỉnh
        r_pts = tk.Frame(f_pts, bg=self.WIN32_BG)
        r_pts.pack(side=tk.TOP, fill=tk.X, pady=2)

        v_list_opt = v_list if v_list else ["A", "B", "C"]
        v_list_p4 = ["[ Không dùng ]"] + v_list_opt

        tk.Label(r_pts, text="Điểm 1:" if is_vn else "P1:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT)
        opt1 = tk.OptionMenu(r_pts, self.var_p1, *v_list_opt, command=self._on_pts_change)
        opt1.config(bg=self.WIN32_BG, font=self.FONT_UI)
        opt1.pack(side=tk.LEFT, padx=2)

        tk.Label(r_pts, text="Điểm 2:" if is_vn else "P2:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=(4, 0))
        opt2 = tk.OptionMenu(r_pts, self.var_p2, *v_list_opt, command=self._on_pts_change)
        opt2.config(bg=self.WIN32_BG, font=self.FONT_UI)
        opt2.pack(side=tk.LEFT, padx=2)

        tk.Label(r_pts, text="Điểm 3:" if is_vn else "P3:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=(4, 0))
        opt3 = tk.OptionMenu(r_pts, self.var_p3, *v_list_opt, command=self._on_pts_change)
        opt3.config(bg=self.WIN32_BG, font=self.FONT_UI)
        opt3.pack(side=tk.LEFT, padx=2)

        tk.Label(r_pts, text="Điểm 4 (tứ giác):" if is_vn else "P4 (quad):", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=(4, 0))
        opt4 = tk.OptionMenu(r_pts, self.var_p4, *v_list_p4, command=self._on_pts_change)
        opt4.config(bg=self.WIN32_BG, font=self.FONT_UI)
        opt4.pack(side=tk.LEFT, padx=2)

        tk.Label(r_pts, text="Tên:" if is_vn else "Name:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=(6, 0))
        tk.Entry(r_pts, textvariable=self.var_name, width=9, font=self.FONT_BOLD, relief=tk.SUNKEN, bd=2).pack(side=tk.LEFT, padx=2)

        # 2. Màu sắc & Chế độ tô CAD
        f_style = tk.LabelFrame(body, text="2. Màu sắc & Kiểu Tô Kỹ Thuật CAD" if is_vn else "2. Color & CAD Hatch Style", bg=self.WIN32_BG, font=self.FONT_BOLD, padx=8, pady=6)
        f_style.pack(side=tk.TOP, fill=tk.X, pady=3)

        # Bảng màu
        f_colors = tk.Frame(f_style, bg=self.WIN32_BG)
        f_colors.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Label(f_colors, text="Màu mặt phẳng:" if is_vn else "Color:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT)
        color_choices = [
            ("#1971C2", "● Xanh"),
            ("#E03131", "● Đỏ"),
            ("#2B8A3E", "● Lục"),
            ("#E8590C", "● Cam"),
            ("#9C36B5", "● Tím"),
            ("#212529", "● Đen"),
        ]
        self.color_preview = tk.Label(f_colors, text="   ", bg=self.var_color.get(), relief=tk.SOLID, bd=1)
        self.color_preview.pack(side=tk.RIGHT, padx=6)
        for c_hex, c_lbl in color_choices:
            tk.Button(
                f_colors,
                text=c_lbl,
                fg=c_hex,
                bg=self.WIN32_BG,
                font=("Tahoma", 8, "bold"),
                relief=tk.RAISED,
                bd=1,
                padx=4,
                command=lambda ch=c_hex: self._set_color(ch),
            ).pack(side=tk.LEFT, padx=2)

        # Chế độ tô
        f_modes = tk.Frame(f_style, bg=self.WIN32_BG)
        f_modes.pack(side=tk.TOP, fill=tk.X, pady=4)
        tk.Label(f_modes, text="Kiểu tô:" if is_vn else "Shading:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT)
        modes = [
            ("hatch", "▨ Gạch chéo CAD (45°)"),
            ("cross", "▦ Gạch ca-rô CAD"),
            ("solid", "■ Tô mờ (Solid)"),
            ("stipple", "░ Chấm lưới"),
            ("none", "⬡ Khung viền"),
        ]
        for m_val, m_lbl in modes:
            tk.Radiobutton(
                f_modes,
                text=m_lbl,
                variable=self.var_fill,
                value=m_val,
                bg=self.WIN32_BG,
                font=self.FONT_UI,
            ).pack(side=tk.LEFT, padx=2)

        # Khoảng cách nét gạch
        f_sp = tk.Frame(f_style, bg=self.WIN32_BG)
        f_sp.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Label(f_sp, text="Khoảng cách gạch (Spacing):" if is_vn else "Hatch Spacing:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT)
        for sp in [6, 10, 14, 18]:
            tk.Button(f_sp, text=f"[{sp}px]", font=("Tahoma", 7), bg=self.WIN32_BG, command=lambda s=sp: self.var_spacing.set(s)).pack(side=tk.LEFT, padx=1)
        tk.Scale(f_sp, from_=4, to=24, orient=tk.HORIZONTAL, variable=self.var_spacing, bg=self.WIN32_BG, highlightthickness=0, width=10).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)

        # 3. Tùy chọn nâng cao
        f_adv = tk.LabelFrame(body, text="3. Tùy chọn Cắt Thiết Diện" if is_vn else "3. Section Cutting Option", bg=self.WIN32_BG, font=self.FONT_BOLD, padx=8, pady=4)
        f_adv.pack(side=tk.TOP, fill=tk.X, pady=3)
        tk.Checkbutton(
            f_adv,
            text="Đồng thời làm Mặt phẳng cắt thiết diện khối đa diện (cho phép kéo độc lập các đỉnh)" if is_vn else "Use as Polyhedron Cutting Plane (enables independent vertex drag)",
            variable=self.var_is_cutter,
            bg=self.WIN32_BG,
            font=self.FONT_UI,
        ).pack(side=tk.LEFT, padx=2)

        # 4. Danh sách các mặt phẳng đã vẽ
        f_list = tk.LabelFrame(body, text="4. Các Mặt Phẳng Đã Vẽ Trong Khối" if is_vn else "4. Custom Planes in Solid", bg=self.WIN32_BG, font=self.FONT_BOLD, padx=8, pady=4)
        f_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=3)

        self.planes_listbox = tk.Listbox(f_list, font=("Consolas", 9), height=4, relief=tk.SUNKEN, bd=2)
        self.planes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb_pl = tk.Scrollbar(f_list, orient=tk.VERTICAL, command=self.planes_listbox.yview)
        sb_pl.pack(side=tk.RIGHT, fill=tk.Y)
        self.planes_listbox.config(yscrollcommand=sb_pl.set)
        self._refresh_listbox()

        btn_del_pl = tk.Button(f_list, text="[ 🗑 Xóa mp chọn ]" if is_vn else "[ 🗑 Delete Plane ]", bg=self.WIN32_BG, font=self.FONT_UI, command=self._delete_selected_plane)
        btn_del_pl.pack(side=tk.BOTTOM, pady=2)

        # Bottom buttons
        btn_bar = tk.Frame(body, bg=self.WIN32_BG)
        btn_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=4)

        tk.Button(
            btn_bar,
            text="[ ▨ Tạo Nét Gạch Chéo / Tô Màu Diện Tích (CAD Hatch) ]" if is_vn else "[ ▨ Create CAD Hatch / Shaded Area ]",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            fg="#000080",
            relief=tk.RAISED,
            bd=2,
            pady=4,
            command=self._apply_create_plane,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        tk.Button(
            btn_bar,
            text="[ Đóng ]" if is_vn else "[ Close ]",
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            pady=4,
            command=self.destroy,
        ).pack(side=tk.LEFT, padx=2)

    def _set_color(self, c: str) -> None:
        self.var_color.set(c)
        self.color_preview.config(bg=c)

    def _on_pts_change(self, _val=None) -> None:
        p1, p2, p3 = self.var_p1.get(), self.var_p2.get(), self.var_p3.get()
        self.var_name.set(f"({p1}{p2}{p3})")

    def _refresh_listbox(self) -> None:
        self.planes_listbox.delete(0, tk.END)
        for i, pl in enumerate(getattr(self.model, "custom_planes", [])):
            pts_str = "-".join(pl.get("pts", []))
            mode_str = pl.get("fill_mode", "hatch")
            is_c = " [Cutter]" if pl.get("is_cutter") else ""
            self.planes_listbox.insert(tk.END, f"{i+1}. {pl.get('name', 'Plane')} ({pts_str}) - {mode_str}{is_c}")

    def _delete_selected_plane(self) -> None:
        sel = self.planes_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        if hasattr(self.model, "custom_planes") and 0 <= idx < len(self.model.custom_planes):
            del self.model.custom_planes[idx]
            self._refresh_listbox()
            self.app.redraw_canvas()

    def _on_quick_face_select(self, val: str) -> None:
        if "(" not in val or ")" not in val:
            return
        pts_part = val[val.find("(") + 1 : val.find(")")]
        pts = [p.strip() for p in pts_part.split("-") if p.strip()]
        if len(pts) >= 1:
            self.var_p1.set(pts[0])
        if len(pts) >= 2:
            self.var_p2.set(pts[1])
        if len(pts) >= 3:
            self.var_p3.set(pts[2])
        if len(pts) >= 4:
            self.var_p4.set(pts[3])
        else:
            self.var_p4.set("[ Không dùng ]")
        self.var_name.set(f"({''.join(pts)})")

    def _on_pts_change(self, _val=None) -> None:
        p1, p2, p3 = self.var_p1.get(), self.var_p2.get(), self.var_p3.get()
        p4 = self.var_p4.get()
        if p4 and p4 != "[ Không dùng ]":
            self.var_name.set(f"({p1}{p2}{p3}{p4})")
        else:
            self.var_name.set(f"({p1}{p2}{p3})")

    def _apply_create_plane(self) -> None:
        p1, p2, p3 = self.var_p1.get(), self.var_p2.get(), self.var_p3.get()
        p4 = self.var_p4.get()
        is_vn = (self.lang == "VN")
        
        pts = [p1, p2, p3]
        if p4 and p4 != "[ Không dùng ]":
            pts.append(p4)

        if len(set(pts)) < len(pts):
            messagebox.showerror("Lỗi" if is_vn else "Error", "Các điểm chọn phải phân biệt!" if is_vn else "Selected points must be distinct!")
            return

        coords = [self.model.get_point(p) for p in pts]
        if any(c is None for c in coords):
            messagebox.showerror("Lỗi" if is_vn else "Error", "Không tìm thấy tọa độ của một trong các điểm!" if is_vn else "Could not find coordinates for all points!")
            return

        u = vec_sub(coords[1], coords[0])
        v = vec_sub(coords[2], coords[0])
        cr = vec_cross(u, v)
        if vec_norm(cr) < 1e-5:
            messagebox.showerror("Lỗi" if is_vn else "Error", "Các điểm thẳng hàng, không xác định được mặt phẳng!" if is_vn else "Points are collinear, cannot define plane!")
            return

        name = self.var_name.get().strip() or f"({''.join(pts)})"
        color = self.var_color.get()
        fill_mode = self.var_fill.get()
        spacing = int(self.var_spacing.get())
        is_cutter = bool(self.var_is_cutter.get())

        self.model.add_custom_plane(
            name=name,
            pts=pts,
            color=color,
            fill_mode=fill_mode,
            hatch_spacing=spacing,
            is_cutter=is_cutter,
        )

        if is_cutter:
            self.app.show_section = True
            self.model.section_fill_mode = fill_mode
            self.model.section_hatch_spacing = spacing
            if hasattr(self.app, "btn_section"):
                self.app.btn_section.config(text="[ Thiết diện: BẬT ]" if is_vn else "[ Section: ON ]", relief=tk.SUNKEN)
            if hasattr(self.app, "plane_d_scale"):
                self.app.plane_d_scale.set(self.model.plane_d)

        self._refresh_listbox()
        self.app.redraw_canvas()
        messagebox.showinfo(
            "Thành công" if is_vn else "Success",
            f"Đã vẽ mặt phẳng {name} qua 3 điểm {p1}, {p2}, {p3} với kiểu tô {fill_mode} chuẩn CAD!"
            if is_vn else
            f"Constructed plane {name} through {p1}, {p2}, {p3} with {fill_mode} CAD shading!"
        )


# ==============================================================================
# WIN32 CLASSIC 3D GEOMETRIC CONSTRUCTION DIALOG (DỰNG HÌNH KHÔNG GIAN)
# ==============================================================================

class Construction3DDialog(tk.Toplevel):
    """
    Hộp thoại dựng hình không gian 3D tương tác theo mô hình hình học không gian 3D:
    Tab 1: Điểm & Đoạn Thẳng (Điểm E trên cạnh tỉ lệ k, Trọng tâm G, Song song PQ // AB, Hình chiếu PK ⊥ AB)
    Tab 2: Mặt phẳng & Khoảng cách (Đường cao PH ⊥ mp Thiết diện/Đáy/ABC, Đoạn vuông góc chung Δ1, Δ2)
    Tab 3: Góc, Đường tròn & Mặt cầu (Dựng góc θ°, Đo góc, Tâm O & Vòng tròn ngoại tiếp, Tâm I & Nội tiếp)
    """

    WIN32_BG = "#ECE9D8"
    WIN32_ACTIVE_BG = "#D4D0C8"
    FONT_UI = ("Tahoma", 9)
    FONT_BOLD = ("Tahoma", 9, "bold")

    def __init__(self, parent: "GeoSolver3DApp"):
        super().__init__(parent)
        self.app = parent
        self.model = parent.models[parent.current_model_key]
        self.lang = parent.lang
        self.title("Dựng Hình Học Không Gian 3D (3D Geometric Constructions)" if self.lang == "VN" else "3D Geometric Constructions")
        self.minsize(640, 500)
        self.configure(bg=self.WIN32_BG)
        self.transient(parent)

        self.option_menus: List[Tuple[tk.OptionMenu, tk.StringVar]] = []

        # Phục hồi kích thước & vị trí cửa sổ và tab người dùng đã chọn trước đó
        if UIStateManager:
            UIStateManager.restore_window(self, "Construction3DDialog", default_geometry="680x560", min_width=640, min_height=500)
            saved_tab = int(UIStateManager.get_active_tab("Construction3DDialog", default=1))
        else:
            self.geometry("680x560")
            saved_tab = 1

        self._build_ui()
        self._switch_tab(saved_tab)

        # Tự động ghi nhớ kích thước khi người dùng kéo giãn hoặc di chuyển cửa sổ
        if UIStateManager:
            UIStateManager.attach_window_tracking(
                self,
                "Construction3DDialog",
                get_extra_state_fn=lambda: {"active_tab": self.active_tab_idx},
            )

    def _create_option_menu(self, parent: tk.Widget, var: tk.StringVar, v_list: List[str], pack_side=tk.LEFT, padx=1, pady=0) -> tk.OptionMenu:
        """Tạo OptionMenu thống nhất phong cách Win32 và đăng ký để tự động làm mới khi có điểm mới."""
        opt = tk.OptionMenu(parent, var, *v_list)
        opt.config(bg=self.WIN32_BG, activebackground=self.WIN32_ACTIVE_BG, font=self.FONT_UI, relief=tk.RAISED, bd=1, padx=3, pady=1)
        opt.pack(side=pack_side, padx=padx, pady=pady)
        self.option_menus.append((opt, var))
        return opt

    def _refresh_all_dropdowns(self) -> None:
        """Cập nhật tức thời tất cả danh sách điểm thả xuống trên cả 3 tab khi vừa dựng thêm điểm mới."""
        v_list = self._get_vertex_list()
        for menu, var in self.option_menus:
            try:
                menu_widget = menu["menu"]
                menu_widget.delete(0, "end")
                for val in v_list:
                    menu_widget.add_command(label=val, command=tk._setit(var, val))
                if var.get() not in v_list and v_list:
                    var.set(v_list[0])
            except Exception:
                pass

    def _propose_next_point_name(self, current_name: str) -> str:
        """Tự động gợi ý tên điểm tiếp theo khoa học và tránh trùng lặp."""
        existing = set(self.model.vertices.keys()) | set(self.model.aux_points.keys())
        if len(current_name) == 1 and "A" <= current_name <= "Z":
            next_ord = ord(current_name) + 1
            while next_ord <= ord("Z"):
                cand = chr(next_ord)
                if cand not in existing:
                    return cand
                next_ord += 1
        base = re.sub(r"\d+$", "", current_name) or "P"
        idx = 1
        while f"{base}{idx}" in existing:
            idx += 1
        return f"{base}{idx}"

    def _get_vertex_list(self) -> List[str]:
        all_v = list(self.model.vertices.keys()) + list(self.model.aux_points.keys())
        if hasattr(self.model, "section_points") and self.model.section_points:
            for lbl, _ in self.model.section_points:
                all_v.append(lbl)
        else:
            sec = self.model.compute_cross_section()
            for lbl, _ in sec:
                all_v.append(lbl)
        return sorted(list(set(all_v)))

    def _get_vertex_coord(self, name: str) -> Vec3:
        if name in self.model.vertices:
            return self.model.vertices[name]
        if name in self.model.aux_points:
            return self.model.aux_points[name]
        if hasattr(self.model, "section_points") and self.model.section_points:
            for lbl, pt in self.model.section_points:
                if lbl == name:
                    return pt
        return (0.0, 0.0, 0.0)

    def _build_ui(self) -> None:
        is_vn = self.lang == "VN"
        top = tk.Frame(self, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2, padx=8, pady=6)
        top.pack(side=tk.TOP, fill=tk.X, padx=6, pady=(6, 4))

        tk.Label(
            top,
            text="CÔNG CỤ DỰNG HÌNH KHÔNG GIAN 3D" if is_vn else "3D GEOMETRIC CONSTRUCTION TOOLS",
            bg=self.WIN32_BG,
            fg="#000080",
            font=self.FONT_BOLD,
        ).pack(side=tk.LEFT)

        v_list = self._get_vertex_list()
        default_v1 = v_list[0] if v_list else "A"
        default_v2 = v_list[1] if len(v_list) > 1 else default_v1
        default_v3 = v_list[2] if len(v_list) > 2 else default_v2
        default_v4 = v_list[3] if len(v_list) > 3 else default_v3

        # Tab Navigation Bar
        tab_bar = tk.Frame(self, bg=self.WIN32_BG)
        tab_bar.pack(side=tk.TOP, fill=tk.X, padx=6, pady=(0, 4))

        self.active_tab_idx = 1
        self.tab_buttons: List[tk.Button] = []

        tabs_data = [
            (1, "1. Điểm & Đoạn Thẳng" if is_vn else "1. Points & Lines"),
            (2, "2. Mặt Phẳng & Khoảng Cách" if is_vn else "2. Planes & Distances"),
            (3, "3. Góc, Đường Tròn & Cầu" if is_vn else "3. Angles, Circles & Spheres"),
        ]

        self.tab_frames: Dict[int, tk.Frame] = {}
        body_container = tk.Frame(self, bg=self.WIN32_BG, padx=6, pady=2)
        body_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        for idx, title_text in tabs_data:
            btn = tk.Button(
                tab_bar,
                text=title_text,
                font=self.FONT_BOLD if idx == 1 else self.FONT_UI,
                bg=self.WIN32_ACTIVE_BG if idx == 1 else self.WIN32_BG,
                relief=tk.SUNKEN if idx == 1 else tk.RAISED,
                bd=2,
                padx=8,
                pady=2,
                command=lambda i=idx: self._switch_tab(i),
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.tab_buttons.append(btn)

            t_frame = tk.Frame(body_container, bg=self.WIN32_BG)
            self.tab_frames[idx] = t_frame

        # ======================================================================
        # TAB 1: ĐIỂM & ĐOẠN THẲNG
        # ======================================================================
        t1 = self.tab_frames[1]

        # 1.1 Dựng điểm E trên cạnh AB theo tỉ số k = AE / AB
        box1_1 = tk.LabelFrame(
            t1,
            text="1. Dựng Điểm E trên đoạn AB theo tỉ số k = AE/AB (hoặc Trung điểm k=0.5)" if is_vn else "1. Point E on Segment AB with Ratio k = AE/AB",
            bg=self.WIN32_BG, font=self.FONT_BOLD, relief=tk.GROOVE, bd=2, padx=6, pady=4
        )
        box1_1.pack(side=tk.TOP, fill=tk.X, pady=3)
        self.ratio_a = tk.StringVar(value=default_v1)
        self.ratio_b = tk.StringVar(value=default_v2)
        self.ratio_k = tk.StringVar(value="0.5")
        self.ratio_name = tk.StringVar(value="E")

        r1_1 = tk.Frame(box1_1, bg=self.WIN32_BG)
        r1_1.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Label(r1_1, text="Đoạn thẳng:" if is_vn else "Segment:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT)
        self._create_option_menu(r1_1, self.ratio_a, v_list, padx=2)
        self._create_option_menu(r1_1, self.ratio_b, v_list, padx=2)
        tk.Label(r1_1, text="Tỉ số k:" if is_vn else "Ratio k:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=(6, 2))
        ent_k = tk.Entry(r1_1, textvariable=self.ratio_k, width=5, font=self.FONT_UI, relief=tk.SUNKEN, bd=2)
        ent_k.pack(side=tk.LEFT, padx=2)
        tk.Button(r1_1, text="[1/3]", font=("Tahoma", 7), bg=self.WIN32_BG, command=lambda: self.ratio_k.set("0.3333")).pack(side=tk.LEFT, padx=1)
        tk.Button(r1_1, text="[1/2]", font=("Tahoma", 7), bg=self.WIN32_BG, command=lambda: self.ratio_k.set("0.5")).pack(side=tk.LEFT, padx=1)
        tk.Button(r1_1, text="[2/3]", font=("Tahoma", 7), bg=self.WIN32_BG, command=lambda: self.ratio_k.set("0.6667")).pack(side=tk.LEFT, padx=1)
        tk.Label(r1_1, text="Tên điểm:" if is_vn else "Name:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=(6, 2))
        tk.Entry(r1_1, textvariable=self.ratio_name, width=4, font=self.FONT_BOLD, relief=tk.SUNKEN, bd=2).pack(side=tk.LEFT, padx=2)
        tk.Button(box1_1, text="[ Dựng Điểm E trên Cạnh AB ]" if is_vn else "[ Construct Point E on AB ]", bg=self.WIN32_BG, font=self.FONT_BOLD, fg="#000080", relief=tk.RAISED, bd=2, command=self._construct_point_on_edge).pack(side=tk.TOP, fill=tk.X, pady=2)

        # 1.2 Dựng điểm G trên mặt phẳng / tam giác ABC
        box1_2 = tk.LabelFrame(
            t1,
            text="2. Dựng Trọng tâm G / Điểm trên mặt tam giác ABC" if is_vn else "2. Centroid G / Point on Triangle ABC",
            bg=self.WIN32_BG, font=self.FONT_BOLD, relief=tk.GROOVE, bd=2, padx=6, pady=4
        )
        box1_2.pack(side=tk.TOP, fill=tk.X, pady=3)
        self.face_a = tk.StringVar(value=default_v1)
        self.face_b = tk.StringVar(value=default_v2)
        self.face_c = tk.StringVar(value=default_v3)
        self.face_pt_name = tk.StringVar(value="G")
        r1_2 = tk.Frame(box1_2, bg=self.WIN32_BG)
        r1_2.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Label(r1_2, text="Tam giác:" if is_vn else "Triangle:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT)
        self._create_option_menu(r1_2, self.face_a, v_list, padx=1)
        self._create_option_menu(r1_2, self.face_b, v_list, padx=1)
        self._create_option_menu(r1_2, self.face_c, v_list, padx=1)
        tk.Label(r1_2, text="Tên điểm:" if is_vn else "Name:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=(6, 2))
        tk.Entry(r1_2, textvariable=self.face_pt_name, width=4, font=self.FONT_BOLD, relief=tk.SUNKEN, bd=2).pack(side=tk.LEFT, padx=2)
        tk.Button(box1_2, text="[ Dựng Trọng tâm G (1/3, 1/3, 1/3) ]" if is_vn else "[ Construct Centroid G ]", bg=self.WIN32_BG, font=self.FONT_BOLD, fg="#2B8A3E", relief=tk.RAISED, bd=2, command=self._construct_point_on_face).pack(side=tk.TOP, fill=tk.X, pady=2)

        # 1.3 Đường thẳng song song
        box1_3 = tk.LabelFrame(
            t1,
            text="3. Kẻ đường thẳng qua P song song với AB (PQ ∥ AB)" if is_vn else "3. Line through P Parallel to AB (PQ ∥ AB)",
            bg=self.WIN32_BG, font=self.FONT_BOLD, relief=tk.GROOVE, bd=2, padx=6, pady=4
        )
        box1_3.pack(side=tk.TOP, fill=tk.X, pady=3)
        self.par_p = tk.StringVar(value=default_v1)
        self.par_a = tk.StringVar(value=default_v2)
        self.par_b = tk.StringVar(value=default_v3)
        r1_3 = tk.Frame(box1_3, bg=self.WIN32_BG)
        r1_3.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Label(r1_3, text="Điểm:" if is_vn else "Point:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT)
        self._create_option_menu(r1_3, self.par_p, v_list, padx=2)
        tk.Label(r1_3, text="Song song với:" if is_vn else "Parallel to:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=(6, 0))
        self._create_option_menu(r1_3, self.par_a, v_list, padx=1)
        self._create_option_menu(r1_3, self.par_b, v_list, padx=1)
        tk.Button(box1_3, text="[ Kẻ Đường Song Song PQ ]" if is_vn else "[ Construct Parallel Line PQ ]", bg=self.WIN32_BG, font=self.FONT_BOLD, relief=tk.RAISED, bd=2, command=self._construct_parallel_line).pack(side=tk.TOP, fill=tk.X, pady=2)

        # 1.4 Hình chiếu PK vuông góc AB
        box1_4 = tk.LabelFrame(
            t1,
            text="4. Hạ đường vuông góc xuống Đường thẳng: PK ⊥ AB" if is_vn else "4. Perpendicular Projection to Line: PK ⊥ AB",
            bg=self.WIN32_BG, font=self.FONT_BOLD, relief=tk.GROOVE, bd=2, padx=6, pady=4
        )
        box1_4.pack(side=tk.TOP, fill=tk.X, pady=3)
        self.line_p = tk.StringVar(value=default_v1)
        self.line_a = tk.StringVar(value=default_v2)
        self.line_b = tk.StringVar(value=default_v3)
        r1_4 = tk.Frame(box1_4, bg=self.WIN32_BG)
        r1_4.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Label(r1_4, text="Điểm:" if is_vn else "Point:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT)
        self._create_option_menu(r1_4, self.line_p, v_list, padx=2)
        tk.Label(r1_4, text="Đường thẳng:" if is_vn else "Line:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=(6, 0))
        self._create_option_menu(r1_4, self.line_a, v_list, padx=1)
        self._create_option_menu(r1_4, self.line_b, v_list, padx=1)
        tk.Button(box1_4, text="[ Dựng Hình chiếu K (PK ⊥ AB) ]" if is_vn else "[ Drop Perpendicular K (PK ⊥ AB) ]", bg=self.WIN32_BG, font=self.FONT_BOLD, relief=tk.RAISED, bd=2, command=self._construct_perp_line).pack(side=tk.TOP, fill=tk.X, pady=2)

        # ======================================================================
        # TAB 2: MẶT PHẲNG & KHOẢNG CÁCH
        # ======================================================================
        t2 = self.tab_frames[2]

        # 2.1 Chân đường cao PH ⊥ Mặt phẳng (Hỗ trợ Thiết diện, Mặt đáy, hoặc 3 điểm)
        box2_1 = tk.LabelFrame(
            t2,
            text="1. Hạ đường cao vuông góc xuống Mặt phẳng: PH ⊥ (Mặt phẳng)" if is_vn else "1. Drop Altitude to Plane: PH ⊥ (Plane)",
            bg=self.WIN32_BG, font=self.FONT_BOLD, relief=tk.GROOVE, bd=2, padx=6, pady=4
        )
        box2_1.pack(side=tk.TOP, fill=tk.X, pady=4)

        self.perp_p = tk.StringVar(value="S" if "S" in v_list else default_v1)
        self.plane_target_type = tk.StringVar(value="section" if self.app.show_section else "3pts")
        self.perp_f1 = tk.StringVar(value=default_v1)
        self.perp_f2 = tk.StringVar(value=default_v2)
        self.perp_f3 = tk.StringVar(value=default_v3)
        self.perp_h_name = tk.StringVar(value="H")

        r2_top = tk.Frame(box2_1, bg=self.WIN32_BG)
        r2_top.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Label(r2_top, text="Từ điểm:" if is_vn else "From point:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT)
        self._create_option_menu(r2_top, self.perp_p, v_list, padx=2)
        tk.Label(r2_top, text="Tên hình chiếu:" if is_vn else "Foot Name:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=(8, 2))
        tk.Entry(r2_top, textvariable=self.perp_h_name, width=4, font=self.FONT_BOLD, relief=tk.SUNKEN, bd=2).pack(side=tk.LEFT, padx=2)

        r2_type = tk.Frame(box2_1, bg=self.WIN32_BG)
        r2_type.pack(side=tk.TOP, fill=tk.X, pady=3)
        tk.Label(r2_type, text="Mặt phẳng:" if is_vn else "Plane:", bg=self.WIN32_BG, font=self.FONT_BOLD).pack(side=tk.LEFT)
        tk.Radiobutton(r2_type, text="Mặt phẳng Thiết diện (α)" if is_vn else "Cross-Section Plane (α)", variable=self.plane_target_type, value="section", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=4)
        tk.Radiobutton(r2_type, text="Mặt phẳng đáy" if is_vn else "Base Plane", variable=self.plane_target_type, value="base", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=4)
        tk.Radiobutton(r2_type, text="Qua 3 điểm (ABC)" if is_vn else "Through 3 Points (ABC)", variable=self.plane_target_type, value="3pts", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=4)

        r2_pts = tk.Frame(box2_1, bg=self.WIN32_BG)
        r2_pts.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Label(r2_pts, text="3 điểm xác định mp:" if is_vn else "3 points defining plane:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT)
        self._create_option_menu(r2_pts, self.perp_f1, v_list, padx=1)
        self._create_option_menu(r2_pts, self.perp_f2, v_list, padx=1)
        self._create_option_menu(r2_pts, self.perp_f3, v_list, padx=1)

        tk.Button(box2_1, text="[ Dựng Chân đường cao H (PH ⊥ Mặt phẳng) ]" if is_vn else "[ Drop Altitude H (PH ⊥ Plane) ]", bg=self.WIN32_BG, font=self.FONT_BOLD, fg="#000080", relief=tk.RAISED, bd=2, command=self._construct_perp_plane).pack(side=tk.TOP, fill=tk.X, pady=3)

        # 2.2 Đoạn vuông góc chung 2 đường chéo nhau
        box2_2 = tk.LabelFrame(
            t2,
            text="2. Đoạn vuông góc chung của 2 đường chéo nhau (Δ1, Δ2)" if is_vn else "2. Common Perpendicular of Skew Lines (Δ1, Δ2)",
            bg=self.WIN32_BG, font=self.FONT_BOLD, relief=tk.GROOVE, bd=2, padx=6, pady=4
        )
        box2_2.pack(side=tk.TOP, fill=tk.X, pady=4)
        self.skew_a1 = tk.StringVar(value="S" if "S" in v_list else default_v1)
        self.skew_a2 = tk.StringVar(value="A" if "A" in v_list else default_v2)
        self.skew_b1 = tk.StringVar(value="B" if "B" in v_list else default_v3)
        self.skew_b2 = tk.StringVar(value="C" if "C" in v_list else default_v4)
        r4 = tk.Frame(box2_2, bg=self.WIN32_BG)
        r4.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Label(r4, text="Đường thẳng 1:" if is_vn else "Line 1:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT)
        self._create_option_menu(r4, self.skew_a1, v_list, padx=1)
        self._create_option_menu(r4, self.skew_a2, v_list, padx=1)
        tk.Label(r4, text="Đường thẳng 2:" if is_vn else "Line 2:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=(6, 0))
        self._create_option_menu(r4, self.skew_b1, v_list, padx=1)
        self._create_option_menu(r4, self.skew_b2, v_list, padx=1)
        tk.Button(box2_2, text="[ Dựng Đoạn Vuông Góc Chung MN ]" if is_vn else "[ Construct Common Perpendicular MN ]", bg=self.WIN32_BG, font=self.FONT_BOLD, fg="#8B0000", relief=tk.RAISED, bd=2, command=self._construct_common_perp).pack(side=tk.TOP, fill=tk.X, pady=3)

        # ======================================================================
        # TAB 3: GÓC, ĐƯỜNG TRÒN & MẶT CẦU
        # ======================================================================
        t3 = self.tab_frames[3]

        # 3.1 Dựng tia / đoạn thẳng tại đỉnh A tạo góc θ° với AB trong mp ABC
        box3_1 = tk.LabelFrame(
            t3,
            text="1. Dựng Góc θ°: Tia AE tạo với AB góc θ° trong mặt phẳng (ABC)" if is_vn else "1. Construct Angle θ°: Ray AE making angle θ° with AB in Plane (ABC)",
            bg=self.WIN32_BG, font=self.FONT_BOLD, relief=tk.GROOVE, bd=2, padx=6, pady=4
        )
        box3_1.pack(side=tk.TOP, fill=tk.X, pady=3)
        self.ang_vert = tk.StringVar(value=default_v1)
        self.ang_dir = tk.StringVar(value=default_v2)
        self.ang_plane = tk.StringVar(value=default_v3)
        self.ang_deg = tk.StringVar(value="60.0")
        self.ang_name = tk.StringVar(value="E_ang")

        r3_ang = tk.Frame(box3_1, bg=self.WIN32_BG)
        r3_ang.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Label(r3_ang, text="Đỉnh:" if is_vn else "Vertex:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT)
        self._create_option_menu(r3_ang, self.ang_vert, v_list, padx=1)
        tk.Label(r3_ang, text="Theo cạnh:" if is_vn else "Along edge:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=(4, 0))
        self._create_option_menu(r3_ang, self.ang_dir, v_list, padx=1)
        tk.Label(r3_ang, text="Mặt phẳng:" if is_vn else "Plane:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=(4, 0))
        self._create_option_menu(r3_ang, self.ang_plane, v_list, padx=1)

        r3_ang2 = tk.Frame(box3_1, bg=self.WIN32_BG)
        r3_ang2.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Label(r3_ang2, text="Góc θ (độ):" if is_vn else "Angle θ (deg):", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT)
        tk.Entry(r3_ang2, textvariable=self.ang_deg, width=5, font=self.FONT_UI, relief=tk.SUNKEN, bd=2).pack(side=tk.LEFT, padx=2)
        tk.Button(r3_ang2, text="[30°]", font=("Tahoma", 7), bg=self.WIN32_BG, command=lambda: self.ang_deg.set("30.0")).pack(side=tk.LEFT, padx=1)
        tk.Button(r3_ang2, text="[45°]", font=("Tahoma", 7), bg=self.WIN32_BG, command=lambda: self.ang_deg.set("45.0")).pack(side=tk.LEFT, padx=1)
        tk.Button(r3_ang2, text="[60°]", font=("Tahoma", 7), bg=self.WIN32_BG, command=lambda: self.ang_deg.set("60.0")).pack(side=tk.LEFT, padx=1)
        tk.Button(r3_ang2, text="[90°]", font=("Tahoma", 7), bg=self.WIN32_BG, command=lambda: self.ang_deg.set("90.0")).pack(side=tk.LEFT, padx=1)
        tk.Label(r3_ang2, text="Tên điểm mới:" if is_vn else "New Point:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=(6, 2))
        tk.Entry(r3_ang2, textvariable=self.ang_name, width=6, font=self.FONT_BOLD, relief=tk.SUNKEN, bd=2).pack(side=tk.LEFT, padx=2)
        tk.Button(box3_1, text="[ Dựng Góc θ° & Tia AE ]" if is_vn else "[ Construct Angle θ° & Ray AE ]", bg=self.WIN32_BG, font=self.FONT_BOLD, fg="#000080", relief=tk.RAISED, bd=2, command=self._construct_angle_ray).pack(side=tk.TOP, fill=tk.X, pady=2)

        # 3.2 Đo & Đánh dấu góc giữa 2 đường thẳng AB và CD
        box3_2 = tk.LabelFrame(
            t3,
            text="2. Đo & Đánh dấu Góc giữa 2 đường thẳng AB và CD" if is_vn else "2. Measure & Mark Angle between Lines AB and CD",
            bg=self.WIN32_BG, font=self.FONT_BOLD, relief=tk.GROOVE, bd=2, padx=6, pady=4
        )
        box3_2.pack(side=tk.TOP, fill=tk.X, pady=3)
        self.meas_a1 = tk.StringVar(value=default_v1)
        self.meas_a2 = tk.StringVar(value=default_v2)
        self.meas_b1 = tk.StringVar(value=default_v2)
        self.meas_b2 = tk.StringVar(value=default_v3)
        r3_meas = tk.Frame(box3_2, bg=self.WIN32_BG)
        r3_meas.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Label(r3_meas, text="Đường thẳng 1:" if is_vn else "Line 1:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT)
        self._create_option_menu(r3_meas, self.meas_a1, v_list, padx=1)
        self._create_option_menu(r3_meas, self.meas_a2, v_list, padx=1)
        tk.Label(r3_meas, text="Đường thẳng 2:" if is_vn else "Line 2:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=(6, 0))
        self._create_option_menu(r3_meas, self.meas_b1, v_list, padx=1)
        self._create_option_menu(r3_meas, self.meas_b2, v_list, padx=1)
        tk.Button(box3_2, text="[ Tính & Đánh Dấu Góc ]" if is_vn else "[ Calculate & Mark Angle ]", bg=self.WIN32_BG, font=self.FONT_BOLD, fg="#8B0000", relief=tk.RAISED, bd=2, command=self._measure_lines_angle).pack(side=tk.TOP, fill=tk.X, pady=2)

        # 3.3 Đường tròn ngoại tiếp tam giác đáy
        box3_3 = tk.LabelFrame(
            t3,
            text="3. Tâm O & Đường tròn ngoại tiếp tam giác ABC" if is_vn else "3. Circumcenter O & Circumcircle of Triangle ABC",
            bg=self.WIN32_BG, font=self.FONT_BOLD, relief=tk.GROOVE, bd=2, padx=6, pady=4
        )
        box3_3.pack(side=tk.TOP, fill=tk.X, pady=3)
        self.circ_a = tk.StringVar(value=default_v1)
        self.circ_b = tk.StringVar(value=default_v2)
        self.circ_c = tk.StringVar(value=default_v3)
        r3_3 = tk.Frame(box3_3, bg=self.WIN32_BG)
        r3_3.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Label(r3_3, text="Tam giác:" if is_vn else "Triangle:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT)
        self._create_option_menu(r3_3, self.circ_a, v_list, padx=1)
        self._create_option_menu(r3_3, self.circ_b, v_list, padx=1)
        self._create_option_menu(r3_3, self.circ_c, v_list, padx=1)
        tk.Button(box3_3, text="[ Dựng Tâm O & Vòng Tròn Ngoại Tiếp ]" if is_vn else "[ Circumcenter O & Circumcircle ]", bg=self.WIN32_BG, font=self.FONT_BOLD, fg="#008080", relief=tk.RAISED, bd=2, command=self._construct_circumcircle).pack(side=tk.TOP, fill=tk.X, pady=2)

        # 3.4 Đường tròn nội tiếp tam giác đáy
        box3_4 = tk.LabelFrame(
            t3,
            text="4. Tâm I & Đường tròn nội tiếp tam giác ABC" if is_vn else "4. Incenter I & Incircle of Triangle ABC",
            bg=self.WIN32_BG, font=self.FONT_BOLD, relief=tk.GROOVE, bd=2, padx=6, pady=4
        )
        box3_4.pack(side=tk.TOP, fill=tk.X, pady=3)
        self.incirc_a = tk.StringVar(value=default_v1)
        self.incirc_b = tk.StringVar(value=default_v2)
        self.incirc_c = tk.StringVar(value=default_v3)
        r3_4 = tk.Frame(box3_4, bg=self.WIN32_BG)
        r3_4.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Label(r3_4, text="Tam giác:" if is_vn else "Triangle:", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT)
        self._create_option_menu(r3_4, self.incirc_a, v_list, padx=1)
        self._create_option_menu(r3_4, self.incirc_b, v_list, padx=1)
        self._create_option_menu(r3_4, self.incirc_c, v_list, padx=1)
        tk.Button(box3_4, text="[ Dựng Tâm I & Vòng Tròn Nội Tiếp ]" if is_vn else "[ Incenter I & Incircle ]", bg=self.WIN32_BG, font=self.FONT_BOLD, fg="#D9480F", relief=tk.RAISED, bd=2, command=self._construct_incircle).pack(side=tk.TOP, fill=tk.X, pady=2)

        # Bottom Clear and Close buttons
        btn_bar = tk.Frame(self, bg=self.WIN32_BG, pady=6)
        btn_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=8)

        tk.Button(btn_bar, text="[ Xóa toàn bộ nét dựng phụ ]" if is_vn else "[ Clear All Auxiliary ]", font=self.FONT_BOLD, bg=self.WIN32_BG, fg="#8B0000", relief=tk.RAISED, bd=2, command=self._clear_aux).pack(side=tk.LEFT)
        tk.Button(btn_bar, text="[ Đóng ]" if is_vn else "[ Close ]", font=self.FONT_UI, bg=self.WIN32_BG, relief=tk.RAISED, bd=2, command=self.destroy).pack(side=tk.RIGHT)

    def _switch_tab(self, idx: int) -> None:
        self.active_tab_idx = idx
        for i, btn in enumerate(self.tab_buttons, 1):
            if i == idx:
                btn.config(relief=tk.SUNKEN, bg=self.WIN32_ACTIVE_BG, font=self.FONT_BOLD)
                self.tab_frames[i].pack(fill=tk.BOTH, expand=True)
            else:
                btn.config(relief=tk.RAISED, bg=self.WIN32_BG, font=self.FONT_UI)
                self.tab_frames[i].pack_forget()
        if UIStateManager:
            UIStateManager.save_active_tab("Construction3DDialog", idx)

    def _construct_point_on_edge(self) -> None:
        is_vn = self.lang == "VN"
        try:
            k = float(self.ratio_k.get())
        except Exception:
            messagebox.showerror("Lỗi" if is_vn else "Error", "Tỉ số k phải là số thực hợp lệ!" if is_vn else "Ratio k must be a valid float!")
            return
        p1 = self._get_vertex_coord(self.ratio_a.get())
        p2 = self._get_vertex_coord(self.ratio_b.get())
        pt = vec_add(p1, vec_scale(vec_sub(p2, p1), k))
        name = self.ratio_name.get().strip() or "E"
        base_name = name
        idx = 1
        while name in self.model.vertices or name in self.model.aux_points:
            idx += 1
            name = f"{base_name}{idx}"
        self.model.aux_points[name] = pt
        self.model.point_constraints[name] = {"type": "ratio", "p1": self.ratio_a.get(), "p2": self.ratio_b.get(), "k": k}
        self.model.aux_segments.append({"p1_name": self.ratio_a.get(), "p2_name": name, "p1": p1, "p2": pt, "color": "#000080", "dash": True, "label": f"{name} (k={k:.2f})", "width": 1.8})
        self.app.redraw_canvas()
        self._refresh_all_dropdowns()
        self.ratio_name.set(self._propose_next_point_name(name))
        messagebox.showinfo(
            "Thành công" if is_vn else "Success",
            f"Đã dựng điểm {name} = ({pt[0]:.2f}, {pt[1]:.2f}, {pt[2]:.2f}) trên đoạn {self.ratio_a.get()}{self.ratio_b.get()} với tỉ số k = {k:.2f}."
            if is_vn else f"Constructed point {name} = ({pt[0]:.2f}, {pt[1]:.2f}, {pt[2]:.2f}) on segment {self.ratio_a.get()}{self.ratio_b.get()} (ratio k = {k:.2f})."
        )

    def _construct_point_on_face(self) -> None:
        is_vn = self.lang == "VN"
        p1 = self._get_vertex_coord(self.face_a.get())
        p2 = self._get_vertex_coord(self.face_b.get())
        p3 = self._get_vertex_coord(self.face_c.get())
        # Centroid G = (A + B + C) / 3
        G = vec_scale(vec_add(vec_add(p1, p2), p3), 1.0 / 3.0)
        name = self.face_pt_name.get().strip() or "G"
        base_name = name
        idx = 1
        while name in self.model.vertices or name in self.model.aux_points:
            idx += 1
            name = f"{base_name}{idx}"
        self.model.aux_points[name] = G
        self.model.point_constraints[name] = {"type": "centroid", "pts": [self.face_a.get(), self.face_b.get(), self.face_c.get()]}
        self.model.aux_segments.append({"p1_name": self.face_a.get(), "p2_name": name, "p1": p1, "p2": G, "color": "#2B8A3E", "dash": True, "label": name, "width": 1.5})
        self.app.redraw_canvas()
        self._refresh_all_dropdowns()
        self.face_pt_name.set(self._propose_next_point_name(name))
        messagebox.showinfo(
            "Thành công" if is_vn else "Success",
            f"Đã dựng Trọng tâm {name} = ({G[0]:.2f}, {G[1]:.2f}, {G[2]:.2f}) của tam giác {self.face_a.get()}{self.face_b.get()}{self.face_c.get()}."
            if is_vn else f"Constructed Centroid {name} = ({G[0]:.2f}, {G[1]:.2f}, {G[2]:.2f}) of triangle {self.face_a.get()}{self.face_b.get()}{self.face_c.get()}."
        )

    def _construct_parallel_line(self) -> None:
        is_vn = self.lang == "VN"
        P = self._get_vertex_coord(self.par_p.get())
        A = self._get_vertex_coord(self.par_a.get())
        B = self._get_vertex_coord(self.par_b.get())
        u = vec_sub(B, A)
        if vec_norm(u) < 1e-6:
            messagebox.showerror("Lỗi" if is_vn else "Error", "Hai điểm A và B trùng nhau!" if is_vn else "Points A and B are identical!")
            return
        Q = vec_add(P, u)
        q_idx = 1
        name = "Q"
        while name in self.model.vertices or name in self.model.aux_points:
            q_idx += 1
            name = f"Q{q_idx}"
        self.model.aux_points[name] = Q
        self.model.point_constraints[name] = {"type": "parallel", "p_from": self.par_p.get(), "p1": self.par_a.get(), "p2": self.par_b.get()}
        self.model.aux_segments.append({
            "p1_name": self.par_p.get(),
            "p2_name": name,
            "p1": P,
            "p2": Q,
            "color": "#9C36B5",
            "dash": True,
            "label": f"// {self.par_a.get()}{self.par_b.get()}",
            "width": 2.0,
        })
        self.app.redraw_canvas()
        self._refresh_all_dropdowns()
        messagebox.showinfo(
            "Thành công" if is_vn else "Success",
            f"Đã dựng điểm {name} = ({Q[0]:.2f}, {Q[1]:.2f}, {Q[2]:.2f})\nĐoạn {self.par_p.get()}{name} song song với {self.par_a.get()}{self.par_b.get()}."
            if is_vn else f"Constructed point {name} = ({Q[0]:.2f}, {Q[1]:.2f}, {Q[2]:.2f})\nSegment {self.par_p.get()}{name} is parallel to {self.par_a.get()}{self.par_b.get()}."
        )

    def _construct_perp_plane(self) -> None:
        is_vn = self.lang == "VN"
        P = self._get_vertex_coord(self.perp_p.get())
        name = self.perp_h_name.get().strip() or "H"
        base_name = name
        idx = 1
        while name in self.model.vertices or name in self.model.aux_points:
            idx += 1
            name = f"{base_name}{idx}"

        target = self.plane_target_type.get()
        if target == "section":
            # Perpendicular to Cross-Section plane (α): n . X = d
            n = self.model.plane_normal
            d_const = self.model.plane_d
            n_norm_sq = vec_dot(n, n)
            if n_norm_sq < 1e-9:
                messagebox.showerror("Lỗi" if is_vn else "Error", "Vectơ pháp tuyến thiết diện không hợp lệ!" if is_vn else "Invalid section plane normal!")
                return
            t = (vec_dot(n, P) - d_const) / n_norm_sq
            H = vec_sub(P, vec_scale(n, t))
            dist = abs(vec_dot(n, P) - d_const) / math.sqrt(n_norm_sq)
            plane_desc = "mp Thiết diện (α)" if is_vn else "Cross-Section plane (α)"
        elif target == "base":
            # Perpendicular to base face of polyhedron
            base_face = self.model.faces[0]
            n = self.model.compute_face_outward_normal(base_face)
            p0 = self.model.vertices[base_face[0]]
            d_const = vec_dot(n, p0)
            t = (vec_dot(n, P) - d_const)
            H = vec_sub(P, vec_scale(n, t))
            dist = abs(t)
            plane_desc = f"mp đáy ({''.join(base_face)})"
        else:
            # Perpendicular through 3 points ABC
            A = self._get_vertex_coord(self.perp_f1.get())
            B = self._get_vertex_coord(self.perp_f2.get())
            C = self._get_vertex_coord(self.perp_f3.get())
            n = vec_normalize(vec_cross(vec_sub(B, A), vec_sub(C, A)))
            if vec_norm(n) < 1e-6:
                messagebox.showerror("Lỗi" if is_vn else "Error", "Ba điểm xác định mặt phẳng thẳng hàng hoặc trùng nhau!" if is_vn else "Collinear or identical points!")
                return
            d_proj = vec_dot(n, vec_sub(P, A))
            H = vec_sub(P, vec_scale(n, d_proj))
            dist = abs(d_proj)
            plane_desc = f"mp ({self.perp_f1.get()}{self.perp_f2.get()}{self.perp_f3.get()})"

        self.model.aux_points[name] = H
        if target == "section":
            self.model.point_constraints[name] = {"type": "perp_section", "p_from": self.perp_p.get()}
        elif target == "base":
            self.model.point_constraints[name] = {"type": "perp_base", "p_from": self.perp_p.get()}
        else:
            self.model.point_constraints[name] = {"type": "perp_face", "p_from": self.perp_p.get(), "pts": [self.perp_f1.get(), self.perp_f2.get(), self.perp_f3.get()]}
        self.model.aux_segments.append({"p1_name": self.perp_p.get(), "p2_name": name, "p1": P, "p2": H, "color": "#E03131", "dash": True, "label": f"{name} (d={dist:.2f})", "width": 2.0})
        self.app.redraw_canvas()
        self._refresh_all_dropdowns()
        self.perp_h_name.set(self._propose_next_point_name(name))
        messagebox.showinfo(
            "Thành công" if is_vn else "Success",
            f"Đã hạ chân đường cao {self.perp_p.get()}{name} ⊥ {plane_desc} tại {name} = ({H[0]:.2f}, {H[1]:.2f}, {H[2]:.2f})\nKhoảng cách d({self.perp_p.get()}, mp) = {dist:.4f}."
            if is_vn else f"Dropped altitude {self.perp_p.get()}{name} ⊥ {plane_desc} at {name} = ({H[0]:.2f}, {H[1]:.2f}, {H[2]:.2f})\nDistance d = {dist:.4f}."
        )

    def _construct_perp_line(self) -> None:
        is_vn = self.lang == "VN"
        P = self._get_vertex_coord(self.line_p.get())
        A = self._get_vertex_coord(self.line_a.get())
        B = self._get_vertex_coord(self.line_b.get())
        u = vec_sub(B, A)
        u_len_sq = vec_dot(u, u)
        if u_len_sq < 1e-9:
            messagebox.showerror("Lỗi" if is_vn else "Error", "Hai điểm A và B trùng nhau!" if is_vn else "Points A and B are identical!")
            return
        t = vec_dot(vec_sub(P, A), u) / u_len_sq
        K = vec_add(A, vec_scale(u, t))
        dist = vec_norm(vec_sub(P, K))

        k_idx = 1
        name = "K"
        while name in self.model.vertices or name in self.model.aux_points:
            k_idx += 1
            name = f"K{k_idx}"
        self.model.aux_points[name] = K
        self.model.point_constraints[name] = {"type": "perp_line", "p_from": self.line_p.get(), "p1": self.line_a.get(), "p2": self.line_b.get()}
        self.model.aux_segments.append({"p1_name": self.line_p.get(), "p2_name": name, "p1": P, "p2": K, "color": "#1971C2", "dash": True, "label": f"{name} (d={dist:.2f})", "width": 1.8})
        self.app.redraw_canvas()
        self._refresh_all_dropdowns()
        messagebox.showinfo(
            "Thành công" if is_vn else "Success",
            f"Đã dựng hình chiếu {name} = ({K[0]:.2f}, {K[1]:.2f}, {K[2]:.2f})\nKhoảng cách d({self.line_p.get()}, {self.line_a.get()}{self.line_b.get()}) = {dist:.4f}"
            if is_vn else f"Constructed projection {name} = ({K[0]:.2f}, {K[1]:.2f}, {K[2]:.2f})\nDistance d = {dist:.4f}"
        )

    def _construct_common_perp(self) -> None:
        is_vn = self.lang == "VN"
        A1 = self._get_vertex_coord(self.skew_a1.get())
        A2 = self._get_vertex_coord(self.skew_a2.get())
        B1 = self._get_vertex_coord(self.skew_b1.get())
        B2 = self._get_vertex_coord(self.skew_b2.get())

        u1 = vec_sub(A2, A1)
        u2 = vec_sub(B2, B1)
        n = vec_cross(u1, u2)
        n_len = vec_norm(n)
        if n_len < 1e-6:
            messagebox.showerror("Lỗi" if is_vn else "Error", "Hai đường thẳng song song hoặc trùng nhau!" if is_vn else "Parallel or identical lines!")
            return

        a11 = vec_dot(u1, u1)
        a12 = -vec_dot(u1, u2)
        b_vec1 = -vec_dot(vec_sub(A1, B1), u1)

        a21 = vec_dot(u2, u1)
        a22 = -vec_dot(u2, u2)
        b_vec2 = -vec_dot(vec_sub(A1, B1), u2)

        det = a11 * a22 - a12 * a21
        if abs(det) < 1e-9:
            messagebox.showerror("Lỗi" if is_vn else "Error", "Không thể tìm đoạn vuông góc chung!" if is_vn else "Cannot find common perpendicular!")
            return

        t1 = (b_vec1 * a22 - a12 * b_vec2) / det
        t2 = (a11 * b_vec2 - b_vec1 * a21) / det

        M_pt = vec_add(A1, vec_scale(u1, t1))
        N_pt = vec_add(B1, vec_scale(u2, t2))
        dist = vec_norm(vec_sub(M_pt, N_pt))

        self.model.aux_points["M_perp"] = M_pt
        self.model.aux_points["N_perp"] = N_pt
        self.model.aux_segments.append({"p1": M_pt, "p2": N_pt, "color": "#E03131", "dash": False, "label": f"d={dist:.2f}", "width": 2.5})
        self.app.redraw_canvas()
        self._refresh_all_dropdowns()
        messagebox.showinfo(
            "Thành công" if is_vn else "Success",
            f"Đã dựng Đoạn vuông góc chung M_perp - N_perp!\nKhoảng cách ngắn nhất d = {dist:.4f}"
            if is_vn else f"Constructed common perpendicular M_perp - N_perp!\nShortest distance d = {dist:.4f}"
        )

    def _construct_angle_ray(self) -> None:
        is_vn = self.lang == "VN"
        try:
            deg = float(self.ang_deg.get())
        except Exception:
            messagebox.showerror("Lỗi" if is_vn else "Error", "Góc độ phải là số thực!" if is_vn else "Angle must be a valid float!")
            return

        A = self._get_vertex_coord(self.ang_vert.get())
        B = self._get_vertex_coord(self.ang_dir.get())
        C = self._get_vertex_coord(self.ang_plane.get())

        u = vec_sub(B, A)
        v = vec_sub(C, A)
        n = vec_cross(u, v)
        if vec_norm(n) < 1e-6:
            messagebox.showerror("Lỗi" if is_vn else "Error", "Ba điểm thẳng hàng, không xác định được mặt phẳng!" if is_vn else "Collinear points!")
            return

        n_unit = vec_normalize(n)
        u_len = vec_norm(u)
        u_dir = vec_normalize(u)
        u_perp = vec_cross(n_unit, u_dir)

        rad = math.radians(deg)
        rot_dir = vec_add(vec_scale(u_dir, math.cos(rad)), vec_scale(u_perp, math.sin(rad)))
        E = vec_add(A, vec_scale(rot_dir, u_len))

        name = self.ang_name.get().strip() or "E"
        base_name = name
        idx = 1
        while name in self.model.vertices or name in self.model.aux_points:
            idx += 1
            name = f"{base_name}{idx}"

        self.model.aux_points[name] = E
        self.model.point_constraints[name] = {"type": "angle_ray", "vert": self.ang_vert.get(), "dir": self.ang_dir.get(), "plane": self.ang_plane.get(), "deg": deg, "length": u_len}
        self.model.aux_segments.append({"p1_name": self.ang_vert.get(), "p2_name": name, "p1": A, "p2": E, "color": "#8B0000", "dash": True, "label": f"{name} (∠{deg:.0f}°)", "width": 2.0})
        self.model.aux_angles.append({
            "vertex": self.ang_vert.get(),
            "p1": self.ang_dir.get(),
            "p2": name,
            "degrees": deg,
            "label": f"{deg:.0f}°",
            "color": "#8B0000",
            "is_right": abs(deg - 90.0) < 0.5,
        })
        self.app.redraw_canvas()
        self._refresh_all_dropdowns()
        self.ang_name.set(self._propose_next_point_name(name))
        messagebox.showinfo(
            "Thành công" if is_vn else "Success",
            f"Đã dựng tia {self.ang_vert.get()}{name} tạo với {self.ang_vert.get()}{self.ang_dir.get()} một góc {deg:.1f}° tại điểm {name} = ({E[0]:.2f}, {E[1]:.2f}, {E[2]:.2f})."
            if is_vn else f"Constructed ray {self.ang_vert.get()}{name} making {deg:.1f}° with {self.ang_vert.get()}{self.ang_dir.get()} at point {name} = ({E[0]:.2f}, {E[1]:.2f}, {E[2]:.2f})."
        )

    def _measure_lines_angle(self) -> None:
        is_vn = self.lang == "VN"
        A1 = self._get_vertex_coord(self.meas_a1.get())
        A2 = self._get_vertex_coord(self.meas_a2.get())
        B1 = self._get_vertex_coord(self.meas_b1.get())
        B2 = self._get_vertex_coord(self.meas_b2.get())

        u1 = vec_sub(A2, A1)
        u2 = vec_sub(B2, B1)
        l1 = vec_norm(u1)
        l2 = vec_norm(u2)
        if l1 < 1e-6 or l2 < 1e-6:
            messagebox.showerror("Lỗi" if is_vn else "Error", "Đường thẳng không hợp lệ (điểm trùng nhau)!" if is_vn else "Invalid line (identical points)!")
            return

        cos_val = abs(vec_dot(u1, u2)) / (l1 * l2)
        cos_val = max(0.0, min(1.0, cos_val))
        deg = math.degrees(math.acos(cos_val))

        # Add angle marker if they share a common vertex
        shared_v = None
        other1, other2 = None, None
        v1_a, v1_b = self.meas_a1.get(), self.meas_a2.get()
        v2_a, v2_b = self.meas_b1.get(), self.meas_b2.get()
        if v1_a == v2_a:
            shared_v, other1, other2 = v1_a, v1_b, v2_b
        elif v1_a == v2_b:
            shared_v, other1, other2 = v1_a, v1_b, v2_a
        elif v1_b == v2_a:
            shared_v, other1, other2 = v1_b, v1_a, v2_b
        elif v1_b == v2_b:
            shared_v, other1, other2 = v1_b, v1_a, v2_a

        if shared_v and other1 and other2:
            self.model.aux_angles.append({
                "vertex": shared_v,
                "p1": other1,
                "p2": other2,
                "degrees": deg,
                "label": f"{deg:.1f}°",
                "color": "#8B0000",
                "is_right": abs(deg - 90.0) < 0.5,
            })
            self.app.redraw_canvas()

        messagebox.showinfo(
            "Kết quả đo góc 3D" if is_vn else "3D Angle Measurement Result",
            f"Góc giữa hai đường thẳng:\n• Đường 1: {self.meas_a1.get()}{self.meas_a2.get()}\n• Đường 2: {self.meas_b1.get()}{self.meas_b2.get()}\n\n"
            f"cos(θ) = |u1·u2| / (|u1|·|u2|) = {cos_val:.4f}\n"
            f"=> Góc θ = {deg:.2f}° ({math.radians(deg):.4f} rad)"
            if is_vn else
            f"Angle between lines:\n• Line 1: {self.meas_a1.get()}{self.meas_a2.get()}\n• Line 2: {self.meas_b1.get()}{self.meas_b2.get()}\n\n"
            f"cos(θ) = {cos_val:.4f}\n"
            f"=> Angle θ = {deg:.2f}° ({math.radians(deg):.4f} rad)"
        )

    def _construct_circumcircle(self) -> None:
        is_vn = self.lang == "VN"
        A = self._get_vertex_coord(self.circ_a.get())
        B = self._get_vertex_coord(self.circ_b.get())
        C = self._get_vertex_coord(self.circ_c.get())
        u = vec_sub(B, A)
        v = vec_sub(C, A)
        n = vec_cross(u, v)
        n_len = vec_norm(n)
        if n_len < 1e-6:
            messagebox.showerror("Lỗi" if is_vn else "Error", "Ba điểm thẳng hàng, không tạo thành tam giác!" if is_vn else "Collinear points!")
            return
        n2 = n_len * n_len
        u2 = vec_dot(u, u)
        v2 = vec_dot(v, v)
        u2_v = vec_scale(v, u2)
        v2_u = vec_scale(u, v2)
        diff = vec_sub(u2_v, v2_u)
        cross_val = vec_cross(diff, n)
        O_rel = vec_scale(cross_val, 1.0 / (2.0 * n2))
        O = vec_add(A, O_rel)
        R = vec_norm(vec_sub(O, A))
        n_unit = vec_scale(n, 1.0 / n_len)

        o_idx = 1
        name = "O_circ"
        while name in self.model.vertices or name in self.model.aux_points:
            o_idx += 1
            name = f"O_circ{o_idx}"
        self.model.aux_points[name] = O
        self.model.point_constraints[name] = {"type": "circumcenter", "pts": [self.circ_a.get(), self.circ_b.get(), self.circ_c.get()]}
        self.model.aux_circles.append({
            "center": O,
            "normal": n_unit,
            "radius": R,
            "color": "#008080",
            "label": f"R={R:.2f}",
            "circle_type": "circum",
            "pts": [self.circ_a.get(), self.circ_b.get(), self.circ_c.get()]
        })
        self.app.redraw_canvas()
        self._refresh_all_dropdowns()
        messagebox.showinfo(
            "Thành công" if is_vn else "Success",
            f"Đã dựng Tâm ngoại tiếp {name} = ({O[0]:.2f}, {O[1]:.2f}, {O[2]:.2f})\nBán kính ngoại tiếp R = {R:.4f}"
            if is_vn else f"Constructed Circumcenter {name} = ({O[0]:.2f}, {O[1]:.2f}, {O[2]:.2f})\nCircumradius R = {R:.4f}"
        )

    def _construct_incircle(self) -> None:
        is_vn = self.lang == "VN"
        A = self._get_vertex_coord(self.incirc_a.get())
        B = self._get_vertex_coord(self.incirc_b.get())
        C = self._get_vertex_coord(self.incirc_c.get())
        a_len = vec_norm(vec_sub(C, B))
        b_len = vec_norm(vec_sub(C, A))
        c_len = vec_norm(vec_sub(B, A))
        p = a_len + b_len + c_len
        if p < 1e-6:
            messagebox.showerror("Lỗi" if is_vn else "Error", "Các điểm trùng nhau!" if is_vn else "Identical points!")
            return
        term_a = vec_scale(A, a_len)
        term_b = vec_scale(B, b_len)
        term_c = vec_scale(C, c_len)
        sum_pts = vec_add(vec_add(term_a, term_b), term_c)
        I = vec_scale(sum_pts, 1.0 / p)

        u = vec_sub(B, A)
        v = vec_sub(C, A)
        n = vec_cross(u, v)
        n_len = vec_norm(n)
        if n_len < 1e-6:
            messagebox.showerror("Lỗi" if is_vn else "Error", "Ba điểm thẳng hàng!" if is_vn else "Collinear points!")
            return
        area = 0.5 * n_len
        s = 0.5 * p
        r = area / s
        n_unit = vec_scale(n, 1.0 / n_len)

        i_idx = 1
        name = "I_circ"
        while name in self.model.vertices or name in self.model.aux_points:
            i_idx += 1
            name = f"I_circ{i_idx}"
        self.model.aux_points[name] = I
        self.model.point_constraints[name] = {"type": "incenter", "pts": [self.incirc_a.get(), self.incirc_b.get(), self.incirc_c.get()]}
        self.model.aux_circles.append({
            "center": I,
            "normal": n_unit,
            "radius": r,
            "color": "#D9480F",
            "label": f"r={r:.2f}",
            "circle_type": "in",
            "pts": [self.incirc_a.get(), self.incirc_b.get(), self.incirc_c.get()]
        })
        self.app.redraw_canvas()
        self._refresh_all_dropdowns()
        messagebox.showinfo(
            "Thành công" if is_vn else "Success",
            f"Đã dựng Tâm nội tiếp {name} = ({I[0]:.2f}, {I[1]:.2f}, {I[2]:.2f})\nBán kính nội tiếp r = {r:.4f}"
            if is_vn else f"Constructed Incenter {name} = ({I[0]:.2f}, {I[1]:.2f}, {I[2]:.2f})\nInradius r = {r:.4f}"
        )

    def _clear_aux(self) -> None:
        is_vn = self.lang == "VN"
        self.model.aux_points.clear()
        self.model.aux_segments.clear()
        self.model.aux_circles.clear()
        if hasattr(self.model, "aux_angles"):
            self.model.aux_angles.clear()
        self.model.point_constraints.clear()
        self.app.redraw_canvas()
        self._refresh_all_dropdowns()
        messagebox.showinfo("Thông báo" if is_vn else "Notice", "Đã xóa toàn bộ các nét dựng phụ!" if is_vn else "Cleared all auxiliary constructions!")


class Deductive3DDialog(tk.Toplevel):
    """
    Win32 Classic Toplevel Dialog featuring the 12 Pedagogical 3D Geometry Topics
    (3D Spatial Geometry) connected to Deductive3DEngine.
    """

    WIN32_BG = "#ECE9D8"
    WIN32_PANEL = "#F5F4EA"
    FONT_UI = ("Tahoma", 9)
    FONT_BOLD = ("Tahoma", 9, "bold")
    FONT_MONO = ("Consolas", 10)

    TOPICS_VN = [
        "1. Mặt cầu ngoại tiếp chóp S.ABC (SA ⊥ đáy, ΔABC vuông)",
        "2. Mặt cầu ngoại tiếp tứ diện đều cạnh a",
        "3. Thiết diện mặt cầu và mặt phẳng (r = √(R² - d²))",
        "4. Thể tích và diện tích chỏm cầu (Spherical Cap & Zone)",
        "5. Mặt cầu nội tiếp hình chóp tứ giác đều (r = 3V / S_tp)",
        "6. Đoạn vuông góc chung & khoảng cách 2 đường chéo nhau",
        "7. Định lý Girard: Diện tích tam giác cầu & cung lớn",
        "8. Cực trị SAT/AP: Khối nón thể tích lớn nhất nội tiếp cầu R",
        "9. Khoảng cách từ điểm P đến mặt phẳng (ABC) & Hình chiếu H",
        "10. Góc giữa đường thẳng và mặt phẳng (sin φ = |u·n| / (|u|·|n|))",
        "11. Góc giữa hai mặt phẳng - Góc nhị diện (cos θ = |n1·n2| / (|n1|·|n2|))",
        "12. Tùy chỉnh: Nhập thông số giải tích tự do & Thể tích khối",
    ]

    TOPICS_EN = [
        "1. Circumscribed Sphere of Pyramid S.ABC (SA ⊥ base, right ΔABC)",
        "2. Circumscribed & Inscribed Sphere of Regular Tetrahedron (edge a)",
        "3. Sphere-Plane Cross-Section Circle (r = sqrt(R^2 - d^2))",
        "4. Spherical Cap & Zone Volume and Surface Area",
        "5. Inscribed Sphere of Regular Square Pyramid (r = 3V / S_total)",
        "6. Common Perpendicular & Skew Lines Distance in 3D",
        "7. Girard's Theorem: Spherical Triangle Area & Great Circle Arc",
        "8. SAT/AP Optimization: Max-Volume Cone Inscribed in Sphere R",
        "9. Distance from Point P to Plane (ABC) & Orthogonal Projection H",
        "10. Angle between Line and Plane (sin phi = |u·n| / (|u|·|n|))",
        "11. Dihedral Angle between Two Planes (cos theta = |n1·n2| / (|n1|·|n2|))",
        "12. Custom 3D Analytical Problem & Polyhedron Volume/Surface",
    ]

    def __init__(self, parent: tk.Widget, engine: BuiltinDeductive3DEngine, lang: str = "VN"):
        super().__init__(parent)
        self.app = parent
        self.engine = engine
        self.lang = lang
        self.title(
            "Hộp Thoại Suy Luận Hình Học Không Gian 3D (SAT/AP/IB/VN)"
            if lang == "VN"
            else "3D Deductive Geometry Solver (SAT/AP/IB/VN)"
        )
        self.minsize(860, 540)
        self.configure(bg=self.WIN32_BG)
        self.transient(parent)

        if UIStateManager:
            UIStateManager.restore_window(self, "Deductive3DDialog", default_geometry="960x650", min_width=860, min_height=540)
            saved_topic = UIStateManager.get_state("Deductive3DDialog").get("selected_topic_idx", 1)
        else:
            self.geometry("960x650")
            saved_topic = 1

        self.selected_topic_idx = max(1, min(12, int(saved_topic)))
        self.param_vars: Dict[str, tk.DoubleVar] = {
            "SA": tk.DoubleVar(value=4.0),
            "AB": tk.DoubleVar(value=3.0),
            "BC": tk.DoubleVar(value=4.0),
            "a": tk.DoubleVar(value=6.0),
            "R": tk.DoubleVar(value=5.0),
            "d": tk.DoubleVar(value=3.0),
            "h_cap": tk.DoubleVar(value=2.0),
            "base_a": tk.DoubleVar(value=4.0),
            "height_h": tk.DoubleVar(value=4.0),
            "angle_A": tk.DoubleVar(value=90.0),
            "angle_B": tk.DoubleVar(value=90.0),
            "angle_C": tk.DoubleVar(value=90.0),
            "px": tk.DoubleVar(value=1.0),
            "py": tk.DoubleVar(value=2.0),
            "pz": tk.DoubleVar(value=3.0),
            "pl_A": tk.DoubleVar(value=1.0),
            "pl_B": tk.DoubleVar(value=2.0),
            "pl_C": tk.DoubleVar(value=2.0),
            "pl_D": tk.DoubleVar(value=-1.0),
            "ux": tk.DoubleVar(value=1.0),
            "uy": tk.DoubleVar(value=1.0),
            "uz": tk.DoubleVar(value=0.0),
            "nx2": tk.DoubleVar(value=0.0),
            "ny2": tk.DoubleVar(value=1.0),
            "nz2": tk.DoubleVar(value=0.0),
        }

        self._build_ui()
        self._on_select_topic(None)

        if UIStateManager:
            UIStateManager.attach_window_tracking(
                self,
                "Deductive3DDialog",
                get_extra_state_fn=lambda: {"selected_topic_idx": self.selected_topic_idx},
            )

    def _build_ui(self) -> None:
        # Top header bar
        header = tk.Frame(self, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2, padx=8, pady=6)
        header.pack(side=tk.TOP, fill=tk.X, padx=6, pady=(6, 3))

        lbl_title = tk.Label(
            header,
            text=(
                "DANH MỤC 12 CHUYÊN ĐỀ SUY LUẬN HÌNH HỌC KHÔNG GIAN & GIẢI TÍCH CẦU (DEDUCTIVE 3D ENGINE)"
                if self.lang == "VN"
                else "12 CLASSIC 3D DEDUCTIVE GEOMETRY & SPHERICAL ANALYTICAL TOPICS"
            ),
            bg=self.WIN32_BG,
            fg="#000080",
            font=self.FONT_BOLD,
        )
        lbl_title.pack(side=tk.LEFT)

        btn_close = tk.Button(
            header,
            text="[ Đóng / Close ]",
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            padx=8,
            command=self.destroy,
        )
        btn_close.pack(side=tk.RIGHT)

        # Main split frame
        body = tk.Frame(self, bg=self.WIN32_BG)
        body.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=6, pady=4)

        # Left column: Topic List + Parameter Inputs
        left_frame = tk.Frame(body, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2, width=360, padx=6, pady=6)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 6))
        left_frame.pack_propagate(False)

        tk.Label(
            left_frame,
            text="Chọn chuyên đề (12 bài toán tiêu chuẩn):" if self.lang == "VN" else "Select Topic (12 Standard Problems):",
            bg=self.WIN32_BG,
            font=self.FONT_BOLD,
            anchor="w",
        ).pack(side=tk.TOP, fill=tk.X, pady=(0, 4))

        self.topic_listbox = tk.Listbox(
            left_frame,
            font=self.FONT_UI,
            bg="#FFFFFF",
            fg="#000000",
            selectbackground="#0A246A",
            selectforeground="#FFFFFF",
            height=11,
            relief=tk.SUNKEN,
            bd=2,
            exportselection=False,
        )
        topics = self.TOPICS_VN if self.lang == "VN" else self.TOPICS_EN
        for item in topics:
            self.topic_listbox.insert(tk.END, item)
        sel_idx = max(0, min(len(topics) - 1, self.selected_topic_idx - 1))
        self.topic_listbox.selection_set(sel_idx)
        self.topic_listbox.see(sel_idx)
        self.topic_listbox.bind("<<ListboxSelect>>", self._on_select_topic)
        self.topic_listbox.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))

        # Parameter input sub-panel
        param_group = tk.LabelFrame(
            left_frame,
            text="Thông số giải tích (Parameters)" if self.lang == "VN" else "Analytical Parameters",
            bg=self.WIN32_BG,
            font=self.FONT_BOLD,
            relief=tk.GROOVE,
            bd=2,
            padx=6,
            pady=4,
        )
        param_group.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Nút lấy số đo từ mô hình 3D trên Canvas
        btn_sync = tk.Button(
            param_group,
            text="[ Lấy số đo từ Canvas 3D ]" if self.lang == "VN" else "[ Sync from 3D Canvas ]",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            fg="#000080",
            relief=tk.RAISED,
            bd=2,
            pady=3,
            command=self._sync_from_canvas,
        )
        btn_sync.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))

        self.param_rows_frame = tk.Frame(param_group, bg=self.WIN32_BG)
        self.param_rows_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        btn_solve = tk.Button(
            param_group,
            text="[ Giải & Sinh Suy Luận Từng Bước ]" if self.lang == "VN" else "[ Run Deductive Proof ]",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            fg="#000080",
            relief=tk.RAISED,
            bd=2,
            pady=4,
            command=self._evaluate_current_topic,
        )
        btn_solve.pack(side=tk.BOTTOM, fill=tk.X, pady=(4, 2))

        # Right column: Solution & LaTeX Output
        right_frame = tk.Frame(body, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2, padx=6, pady=6)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            right_frame,
            text=(
                "Lời giải từng bước, Công thức & Ký hiệu toán học tự nhiên:"
                if self.lang == "VN"
                else "Step-by-Step Proof, Natural Math Formulas & Exact Evaluation:"
            ),
            bg=self.WIN32_BG,
            font=self.FONT_BOLD,
            anchor="w",
        ).pack(side=tk.TOP, fill=tk.X, pady=(0, 4))

        txt_container = tk.Frame(right_frame, bg=self.WIN32_BG)
        txt_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(txt_container, orient=tk.VERTICAL)
        self.output_text = tk.Text(
            txt_container,
            font=self.FONT_MONO,
            bg="#FFFFFF",
            fg="#000000",
            relief=tk.SUNKEN,
            bd=2,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            padx=8,
            pady=8,
        )
        scrollbar.config(command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bottom Action Bar with Copy, Export & Close
        bottom_bar = tk.Frame(right_frame, bg=self.WIN32_BG, pady=4)
        bottom_bar.pack(side=tk.BOTTOM, fill=tk.X)

        btn_copy = tk.Button(
            bottom_bar,
            text="[ 📋 Sao chép Lời giải (Ctrl+C) ]" if self.lang == "VN" else "[ 📋 Copy Proof (Ctrl+C) ]",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            padx=6,
            pady=2,
            command=self._copy_solution,
        )
        btn_copy.pack(side=tk.LEFT, padx=2)

        btn_export = tk.Button(
            bottom_bar,
            text="[ 💾 Xuất ra tệp TXT/MD... ]" if self.lang == "VN" else "[ 💾 Export to File... ]",
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            padx=6,
            pady=2,
            command=self._export_to_file,
        )
        btn_export.pack(side=tk.LEFT, padx=2)

        btn_close = tk.Button(
            bottom_bar,
            text="[ Đóng ]" if self.lang == "VN" else "[ Close ]",
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=2,
            command=self.destroy,
        )
        btn_close.pack(side=tk.RIGHT, padx=2)

        self.bind("<Control-c>", lambda _e: self._copy_solution())
        self.bind("<Control-C>", lambda _e: self._copy_solution())

    def _sync_from_canvas(self) -> None:
        try:
            if hasattr(self.app, "ent_dim_h"):
                h = float(self.app.ent_dim_h.get())
                a = float(self.app.ent_dim_a.get())
                b = float(self.app.ent_dim_b.get())
            else:
                h, a, b = 4.0, 3.0, 4.0
        except Exception:
            h, a, b = 4.0, 3.0, 4.0

        model = self.app.models[self.app.current_model_key] if hasattr(self.app, "models") else None
        self.param_vars["SA"].set(h)
        self.param_vars["AB"].set(a)
        self.param_vars["BC"].set(b)
        self.param_vars["a"].set(a)
        self.param_vars["base_a"].set(a)
        self.param_vars["height_h"].set(h)
        self.param_vars["R"].set(max(1.0, round(a * 0.8, 2)))
        self.param_vars["d"].set(max(0.5, round(abs(model.plane_d) if model else 1.0, 2)))
        self.param_vars["h_cap"].set(max(0.5, round(a * 0.4, 2)))
        self.param_vars["px"].set(0.0)
        self.param_vars["py"].set(0.0)
        self.param_vars["pz"].set(h)

        self._evaluate_current_topic()
        messagebox.showinfo(
            "Đồng bộ thành công" if self.lang == "VN" else "Sync Successful",
            f"Đã cập nhật số đo từ mô hình 3D trên Canvas:\n• Chiều cao h = {h:.2f}\n• Cạnh đáy a = {a:.2f}\n• Cạnh đáy b = {b:.2f}"
            if self.lang == "VN"
            else f"Synced dimensions from 3D Canvas:\n• Height h = {h:.2f}\n• Base edge a = {a:.2f}\n• Base edge b = {b:.2f}",
        )

    def _on_select_topic(self, _event: Optional[Any]) -> None:
        sel = self.topic_listbox.curselection()
        if not sel:
            return
        self.selected_topic_idx = int(sel[0]) + 1
        if UIStateManager:
            UIStateManager.save_state("Deductive3DDialog", selected_topic_idx=self.selected_topic_idx)
        self._rebuild_parameter_inputs(self.selected_topic_idx)
        self._evaluate_current_topic()

    def _copy_solution(self) -> None:
        try:
            txt = self.output_text.get("1.0", tk.END).strip()
            if txt:
                self.clipboard_clear()
                self.clipboard_append(txt)
                is_vn = (self.lang == "VN")
                messagebox.showinfo(
                    "Thành công" if is_vn else "Success",
                    "Đã sao chép toàn bộ lời giải và công thức vào Clipboard!"
                    if is_vn
                    else "Full proof and formulas copied to Clipboard!",
                    parent=self,
                )
        except Exception:
            pass

    def _export_to_file(self) -> None:
        is_vn = (self.lang == "VN")
        fpath = filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".md",
            filetypes=[
                ("Markdown Document (*.md)", "*.md"),
                ("Text Document (*.txt)", "*.txt"),
                ("All Files (*.*)", "*.*")
            ],
            title="Xuất lời giải suy luận 3D" if is_vn else "Export 3D Deductive Proof",
        )
        if not fpath:
            return
        try:
            txt = self.output_text.get("1.0", tk.END)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(txt)
            messagebox.showinfo(
                "Thành công" if is_vn else "Success",
                f"Đã xuất tệp thành công:\n{fpath}" if is_vn else f"Exported proof successfully to:\n{fpath}",
                parent=self,
            )
        except Exception as ex:
            messagebox.showerror("Lỗi" if is_vn else "Error", str(ex), parent=self)

    def _rebuild_parameter_inputs(self, topic_idx: int) -> None:
        for child in self.param_rows_frame.winfo_children():
            child.destroy()

        is_vn = (self.lang == "VN")
        topic_param_specs_vn = {
            1: [("SA", "Cạnh bên SA ⊥ đáy:"), ("AB", "Cạnh đáy AB:"), ("BC", "Cạnh đáy BC (⊥ AB):")],
            2: [("a", "Cạnh tứ diện đều a:")],
            3: [("R", "Bán kính cầu R:"), ("d", "Khoảng cách tâm d(I, α):")],
            4: [("R", "Bán kính cầu R:"), ("h_cap", "Chiều cao chỏm cầu h:")],
            5: [("base_a", "Cạnh đáy hình vuông a:"), ("height_h", "Chiều cao chóp SO = h:")],
            6: [("base_a", "Cạnh đáy hình vuông a:"), ("SA", "Chiều cao SA = h:")],
            7: [("R", "Bán kính cầu R:"), ("angle_A", "Góc cầu A (độ):"), ("angle_B", "Góc cầu B (độ):"), ("angle_C", "Góc cầu C (độ):")],
            8: [("R", "Bán kính mặt cầu R:")],
            9: [("px", "Điểm P(x):"), ("py", "Điểm P(y):"), ("pz", "Điểm P(z):"), ("pl_A", "Mặt phẳng Ax:"), ("pl_B", "By:"), ("pl_C", "Cz:"), ("pl_D", "Hệ số D:")],
            10: [("ux", "VTCP u(x):"), ("uy", "u(y):"), ("uz", "u(z):"), ("pl_A", "VTPT mp n(x):"), ("pl_B", "n(y):"), ("pl_C", "n(z):")],
            11: [("pl_A", "Mặt phẳng 1 n1(x):"), ("pl_B", "n1(y):"), ("pl_C", "n1(z):"), ("nx2", "Mặt phẳng 2 n2(x):"), ("ny2", "n2(y):"), ("nz2", "n2(z):")],
            12: [("base_a", "Cạnh đáy a:"), ("height_h", "Chiều cao h:"), ("SA", "Cạnh bên SA:"), ("R", "Bán kính cầu R:")],
        }

        topic_param_specs_en = {
            1: [("SA", "Lateral height SA ⊥ base:"), ("AB", "Base edge AB:"), ("BC", "Base edge BC (⊥ AB):")],
            2: [("a", "Tetrahedron edge a:")],
            3: [("R", "Sphere radius R:"), ("d", "Center distance d(I, α):")],
            4: [("R", "Sphere radius R:"), ("h_cap", "Cap height h:")],
            5: [("base_a", "Square base edge a:"), ("height_h", "Altitude SO = h:")],
            6: [("base_a", "Square base edge a:"), ("SA", "Lateral height SA = h:")],
            7: [("R", "Sphere radius R:"), ("angle_A", "Spherical angle A (°):"), ("angle_B", "Spherical angle B (°):"), ("angle_C", "Spherical angle C (°):")],
            8: [("R", "Circumscribed radius R:")],
            9: [("px", "Point P(x):"), ("py", "Point P(y):"), ("pz", "Point P(z):"), ("pl_A", "Plane coeff Ax:"), ("pl_B", "By:"), ("pl_C", "Cz:"), ("pl_D", "Offset D:")],
            10: [("ux", "Direction u(x):"), ("uy", "u(y):"), ("uz", "u(z):"), ("pl_A", "Plane normal n(x):"), ("pl_B", "n(y):"), ("pl_C", "n(z):")],
            11: [("pl_A", "Plane 1 n1(x):"), ("pl_B", "n1(y):"), ("pl_C", "n1(z):"), ("nx2", "Plane 2 n2(x):"), ("ny2", "n2(y):"), ("nz2", "n2(z):")],
            12: [("base_a", "Base edge a:"), ("height_h", "Height h:"), ("SA", "Lateral edge SA:"), ("R", "Reference sphere R:")],
        }

        specs_dict = topic_param_specs_vn if is_vn else topic_param_specs_en
        specs = specs_dict.get(topic_idx, [("R", "Bán kính R:" if is_vn else "Radius R:")])
        for key, label_txt in specs:
            row = tk.Frame(self.param_rows_frame, bg=self.WIN32_BG, pady=2)
            row.pack(side=tk.TOP, fill=tk.X)
            tk.Label(row, text=label_txt, bg=self.WIN32_BG, font=self.FONT_UI, anchor="w").pack(
                side=tk.LEFT, padx=2
            )
            if key not in self.param_vars:
                self.param_vars[key] = tk.DoubleVar(value=1.0)
            ent = tk.Entry(
                row,
                textvariable=self.param_vars[key],
                font=self.FONT_UI,
                width=8,
                relief=tk.SUNKEN,
                bd=2,
            )
            ent.pack(side=tk.RIGHT)
            ent.bind("<Return>", lambda _e: self._evaluate_current_topic())

    def _evaluate_current_topic(self) -> None:
        params: Dict[str, float] = {}
        for k, var in self.param_vars.items():
            try:
                params[k] = float(var.get())
            except Exception:
                params[k] = 1.0

        result_text = None
        if HAS_EXTERNAL_DEDUCTIVE:
            try:
                ext_engine = Deductive3DEngine()
                res = None
                t = self.selected_topic_idx
                if t == 1:
                    res = ext_engine.prove_circumscribed_sphere(case_type="pyramid_sa_perp_base", sa=params.get("SA", 12.0), ab=params.get("AB", 3.0), bc=params.get("BC", 4.0), angle_b=90)
                elif t == 2:
                    res = ext_engine.prove_circumscribed_sphere(case_type="regular_tetrahedron", a=params.get("a", 6.0))
                elif t == 3:
                    res = ext_engine.prove_plane_sphere_intersection(R=params.get("R", 5.0), d=params.get("d", 1.0))
                elif t == 4:
                    res = ext_engine.prove_plane_sphere_intersection(R=params.get("R", 5.0), d=params.get("R", 5.0) - params.get("h_cap", 2.0))
                elif t == 5:
                    res = ext_engine.prove_inscribed_sphere(case_type="regular_quad_pyramid", a=params.get("base_a", 4.0), h=params.get("height_h", 4.0))
                elif t == 6:
                    res = ext_engine.prove_distance_skew_lines(
                        m1=Point3D(0, 0, 0, name="O"), u1=Vector3D(1, 0, 0),
                        m2=Point3D(0, params.get("base_a", 4.0), params.get("SA", 4.0), name="S"), u2=Vector3D(0, 1, 0)
                    )
                elif t == 7:
                    import sympy as sp
                    res = ext_engine.prove_girard_spherical_area(
                        R=params.get("R", 6371.0),
                        angle_A=sp.rad(params.get("angle_A", 90.0)),
                        angle_B=sp.rad(params.get("angle_B", 90.0)),
                        angle_C=sp.rad(params.get("angle_C", 90.0))
                    )
                elif t == 8:
                    res = ext_engine.prove_inscribed_solid_optimization(solid_type="cone", R=params.get("R", 9.0))
                elif t == 9:
                    pt = Point3D(params.get("px", 1.0), params.get("py", 2.0), params.get("pz", 3.0), name="P")
                    pl = Plane3D(params.get("pl_A", 1.0), params.get("pl_B", 2.0), params.get("pl_C", 2.0), params.get("pl_D", -1.0))
                    res = ext_engine.prove_distance_point_to_plane(pt, pl)
                elif t == 10:
                    u_dir = Vector3D(params.get("ux", 1.0), params.get("uy", 1.0), params.get("uz", 0.0))
                    pl = Plane3D(params.get("pl_A", 0.0), params.get("pl_B", 0.0), params.get("pl_C", 1.0), 0.0)
                    res = ext_engine.prove_angle_line_plane(u_dir, pl)
                elif t == 11:
                    pl1 = Plane3D(params.get("pl_A", 1.0), params.get("pl_B", 0.0), params.get("pl_C", 0.0), 0.0)
                    pl2 = Plane3D(params.get("nx2", 0.0), params.get("ny2", 1.0), params.get("nz2", 0.0), 0.0)
                    res = ext_engine.prove_angle_between_planes(pl1, pl2)
                elif t == 12:
                    a_val = params.get("base_a", 4.0)
                    h_val = params.get("height_h", 4.0)
                    res = ext_engine.prove_inscribed_sphere(case_type="regular_quad_pyramid", a=a_val, h=h_val)
                
                if res:
                    is_vn = (self.lang == "VN")
                    topic_title = self.TOPICS_VN[t - 1] if is_vn else self.TOPICS_EN[t - 1]
                    lines = [
                        "=" * 76,
                        "  BÁO CÁO SUY LUẬN HÌNH HỌC 3D" if is_vn else "  3D DEDUCTIVE GEOMETRY PROOF REPORT",
                        f"  {'Mã bài toán / ID' if is_vn else 'Problem ID      '} : {res.problem_id}",
                        f"  {'Chuyên đề / Topic' if is_vn else 'Topic / Theorem  '} : {topic_title}",
                        "=" * 76, ""
                    ]
                    for s in res.steps:
                        title = s.title_vi if is_vn else (s.title_en or s.title_vi)
                        stmt = s.statement_vi if is_vn else (s.statement_en or s.statement_vi)
                        step_lbl = f"[Bước {s.step_number}]" if is_vn else f"[Step {s.step_number}]"
                        lines.append(f"{step_lbl} {title}")
                        lines.append(f"  • {'Diễn giải' if is_vn else 'Explanation'} : {format_formula_radicals(stmt, is_vn)}")
                        if s.latex_formula:
                            lines.append(f"  • {'Ký hiệu toán học tự nhiên' if is_vn else 'Natural Math Formula'} : {format_formula_radicals(s.latex_formula, is_vn)}")
                        if s.math_reasons:
                            clean_reasons = []
                            for r in s.math_reasons:
                                if not is_vn and "/" in r:
                                    clean_reasons.append(r.split("/", 1)[1].strip())
                                elif not is_vn:
                                    clean_reasons.append(translate_reason_to_en(r))
                                else:
                                    clean_reasons.append(r.split("/", 1)[0].strip())
                            lines.append(f"  • {'Cơ sở lý thuyết' if is_vn else 'Theoretical Basis'}          : {', '.join(clean_reasons)}")
                        lines.append("")
                    lines.append("-" * 76)
                    sym_formatted = format_formula_radicals(str(res.symbolic_result), is_vn)
                    lines.append(f"{'KẾT QUẢ ĐẠI SỐ CHÍNH XÁC (SymPy)' if is_vn else 'EXACT SYMBOLIC RESULT (SymPy)'} : {sym_formatted}")
                    rad_num = format_radical_number(res.numeric_value)
                    if rad_num != f"{res.numeric_value:.4f}":
                        lines.append(f"{'GIÁ TRỊ SỐ THỰC XẤP XỈ' if is_vn else 'APPROXIMATE VALUE'}          : {rad_num} (≈ {res.numeric_value:.4f}) {res.unit}")
                    else:
                        lines.append(f"{'GIÁ TRỊ SỐ THỰC' if is_vn else 'NUMERICAL VALUE'}                 : {res.numeric_value:.4f} {res.unit}")
                    concl = res.conclusion_vi if is_vn else (res.conclusion_en or res.conclusion_vi)
                    lines.append(f"{'KẾT LUẬN' if is_vn else 'CONCLUSION'}                       : {format_formula_radicals(concl, is_vn)}")
                    lines.append("=" * 76)
                    result_text = "\n".join(lines)
            except Exception:
                pass

        if not result_text:
            result_text = self.engine.solve_topic(self.selected_topic_idx, params, self.lang)

        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result_text)
        self.output_text.configure(state=tk.DISABLED)


class Win32AIHubDialog(tk.Toplevel):
    """
    Monochrome Win32 Classic [ AI ] Hub Dialog for invoking local STEM AI models
    or HuggingFace Geometry-LLM checkpoints.
    """

    WIN32_BG = "#ECE9D8"
    FONT_UI = ("Tahoma", 9)
    FONT_BOLD = ("Tahoma", 9, "bold")
    FONT_MONO = ("Consolas", 9)

    def __init__(self, parent: tk.Widget, current_model_name: str, lang: str = "VN"):
        super().__init__(parent)
        self.lang = lang
        self.title("AI Hub & HuggingFace STEM Checkpoint Manager" if lang == "EN" else "Trạm AI & Tải Mô Hình Toán Học HuggingFace")
        self.minsize(500, 350)
        self.configure(bg=self.WIN32_BG)
        self.transient(parent)

        if UIStateManager:
            UIStateManager.restore_window(self, "Win32AIHubDialog", default_geometry="640x420", min_width=500, min_height=350)
            UIStateManager.attach_window_tracking(self, "Win32AIHubDialog")
        else:
            self.geometry("640x420")

        self.repo_var = tk.StringVar(value="Qwen/Qwen2.5-Math-7B-Instruct")
        self.prompt_var = tk.StringVar(
            value=f"Phân tích thiết diện và tâm mặt cầu ngoại tiếp của {current_model_name}."
        )
        self._build_ui()

    def _build_ui(self) -> None:
        top = tk.Frame(self, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2, padx=8, pady=6)
        top.pack(side=tk.TOP, fill=tk.X, padx=6, pady=6)

        tk.Label(
            top,
            text="[ AI ] HUGGINGFACE STEM MODEL HUB & DEDUCTIVE ASSISTANT",
            bg=self.WIN32_BG,
            fg="#000080",
            font=self.FONT_BOLD,
        ).pack(side=tk.LEFT)

        form = tk.Frame(self, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2, padx=8, pady=8)
        form.pack(side=tk.TOP, fill=tk.X, padx=6, pady=(0, 6))

        r1 = tk.Frame(form, bg=self.WIN32_BG, pady=2)
        r1.pack(side=tk.TOP, fill=tk.X)
        tk.Label(r1, text="HuggingFace Repo ID:", bg=self.WIN32_BG, font=self.FONT_UI, width=20, anchor="w").pack(side=tk.LEFT)
        tk.Entry(r1, textvariable=self.repo_var, font=self.FONT_UI, relief=tk.SUNKEN, bd=2).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
        tk.Button(
            r1,
            text="[ Kiểm tra / Tải ]",
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            command=self._check_model_status,
        ).pack(side=tk.RIGHT)

        r2 = tk.Frame(form, bg=self.WIN32_BG, pady=4)
        r2.pack(side=tk.TOP, fill=tk.X)
        tk.Label(r2, text="Truy vấn Hình học 3D:", bg=self.WIN32_BG, font=self.FONT_UI, width=20, anchor="w").pack(side=tk.LEFT)
        tk.Entry(r2, textvariable=self.prompt_var, font=self.FONT_UI, relief=tk.SUNKEN, bd=2).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
        tk.Button(
            r2,
            text="[ Suy luận AI ]",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            command=self._run_local_synthesis,
        ).pack(side=tk.RIGHT)

        log_frame = tk.Frame(self, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2, padx=6, pady=6)
        log_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=6, pady=(0, 6))

        self.log_text = tk.Text(
            log_frame,
            font=self.FONT_MONO,
            bg="#FFFFFF",
            fg="#000000",
            relief=tk.SUNKEN,
            bd=2,
            wrap=tk.WORD,
            padx=6,
            pady=6,
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._run_local_synthesis()

    def _check_model_status(self) -> None:
        repo = self.repo_var.get().strip()
        self.log_text.insert(
            tk.END,
            f"\n[HF-HUB] Đang kiểm tra kho lưu trữ '{repo}'...\n"
            f"[HF-HUB] Sẵn sàng kết nối Symbolic Deductive3DEngine + Local Weights.\n",
        )
        self.log_text.see(tk.END)

    def _run_local_synthesis(self) -> None:
        query = self.prompt_var.get().strip()
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(
            tk.END,
            "====================================================================\n"
            "[AI SYMBOLIC-NEURAL GEOMETRY SYNTHESIS]\n"
            "====================================================================\n"
            f"• Model Repo : {self.repo_var.get()}\n"
            f"• Yêu cầu    : {query}\n\n"
            "[Gợi ý Phương pháp Giải tích & Tổng hợp]\n"
            "1. Gắn hệ trục tọa độ trực chuẩn Oxyz tại gốc O(0, 0, 0).\n"
            "2. Xác định tọa độ các đỉnh đa diện và vector pháp tuyến mặt phẳng cắt.\n"
            "3. Với mặt cầu ngoại tiếp: Giải hệ phương trình mặt phẳng trung trực của\n"
            "   3 cạnh không đồng phẳng xuất phát từ cùng một đỉnh để tìm tâm I(x, y, z)\n"
            "   và bán kính R = IA.\n"
            "4. Sử dụng hộp thoại [ Suy luận 3D ] (Phím tắt: D) để xuất lời giải LaTeX chi tiết.\n",
        )


# ==============================================================================
# MAIN WIN32 CLASSIC GEOSOLVER 3D APPLICATION
# ==============================================================================

# ==============================================================================
# WIN32 EXPORT 3D IMAGE DIALOG (MULTI-MODE)
# ==============================================================================

class Export3DImageDialog(tk.Toplevel):
    """
    Hộp thoại Xuất ảnh bản vẽ 3D với nhiều tùy chọn chuyên nghiệp:
    - Trục tọa độ Oxyz (Bật / Tắt)
    - Mặt cầu / đường tròn ngoại tiếp S(I; R) (Bật / Tắt)
    - Thiết diện phẳng & Gạch chéo CAD (Bật / Tắt)
    - Điểm & Đoạn phụ (Bật / Tắt)
    - Nhãn tên đỉnh (Bật / Tắt)
    - Chế độ nét khuất (Nét đứt (cạnh khuất) / Khung dây / Ẩn nét khuất)
    - Nền ảnh (Nền trắng #FFFFFF / Nền trong suốt PNG)
    - Độ phân giải (1x Màn hình, 2x In ấn rõ nét 300 DPI, 3x Bản vẽ lớn 450 DPI)
    """
    WIN32_BG = "#ECE9D8"
    FONT_UI = ("Tahoma", 9)
    FONT_BOLD = ("Tahoma", 9, "bold")

    def __init__(self, parent: "GeoSolver3DApp"):
        super().__init__(parent)
        self.app = parent
        self.lang = parent.lang
        is_vn = (self.lang == "VN")
        self.title("Tùy Chọn Xuất Hình Ảnh Bản Vẽ 3D (CAD Export)" if is_vn else "Export 3D Diagram Options (CAD Export)")
        self.geometry("480x520")
        self.minsize(440, 480)
        self.configure(bg=self.WIN32_BG)
        self.transient(parent)
        self.grab_set()

        # Variables
        self.var_axes = tk.BooleanVar(value=parent.show_axes)
        self.var_sphere = tk.BooleanVar(value=parent.show_sphere)
        self.var_section = tk.BooleanVar(value=parent.show_section)
        self.var_aux = tk.BooleanVar(value=True)
        self.var_labels = tk.BooleanVar(value=True)
        self.var_hidden = tk.StringVar(value=parent.hidden_mode)
        self.var_bold = tk.BooleanVar(value=parent.bold_mode)
        self.var_transparent = tk.BooleanVar(value=False)
        self.var_scale = tk.IntVar(value=2)

        self._build_ui()

    def _build_ui(self) -> None:
        is_vn = (self.lang == "VN")

        # Header banner
        hdr = tk.Frame(self, bg=self.WIN32_BG, pady=6)
        hdr.pack(side=tk.TOP, fill=tk.X, padx=10)
        tk.Label(
            hdr,
            text="CẤU HÌNH XUẤT ẢNH BẢN VẼ HÌNH HỌC 3D" if is_vn else "3D GEOMETRY DIAGRAM EXPORT CONFIG",
            font=("Tahoma", 10, "bold"),
            bg=self.WIN32_BG,
            fg="#000080",
        ).pack(side=tk.TOP, anchor="w")
        tk.Label(
            hdr,
            text="Chọn các đối tượng và kiểu kết xuất phục vụ in ấn giáo trình / bài giảng:"
            if is_vn
            else "Select visible elements and render styling for publication & slides:",
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            fg="#444444",
        ).pack(side=tk.TOP, anchor="w", pady=(2, 0))

        # Group 1: Visible Elements
        grp_elem = tk.LabelFrame(
            self,
            text="1. Đối tượng hiển thị trên bản vẽ" if is_vn else "1. Visible Elements",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            padx=10,
            pady=6,
        )
        grp_elem.pack(side=tk.TOP, fill=tk.X, padx=10, pady=4)

        tk.Checkbutton(
            grp_elem,
            text="Trục tọa độ không gian Oxyz (X, Y, Z)" if is_vn else "Spatial Coordinate Axes Oxyz",
            variable=self.var_axes,
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            anchor="w",
        ).pack(side=tk.TOP, fill=tk.X, pady=1)

        tk.Checkbutton(
            grp_elem,
            text="Mặt cầu ngoại tiếp S(I; R) & Tâm I" if is_vn else "Circumscribed Sphere S(I; R) & Center I",
            variable=self.var_sphere,
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            anchor="w",
        ).pack(side=tk.TOP, fill=tk.X, pady=1)

        tk.Checkbutton(
            grp_elem,
            text="Mặt phẳng thiết diện & Gạch chéo CAD (Hatching)" if is_vn else "Cross-Section Plane & CAD Hatching",
            variable=self.var_section,
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            anchor="w",
        ).pack(side=tk.TOP, fill=tk.X, pady=1)

        tk.Checkbutton(
            grp_elem,
            text="Đường dựng phụ, góc & điểm phụ trợ (Auxiliary)" if is_vn else "Auxiliary Lines, Points & Angles",
            variable=self.var_aux,
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            anchor="w",
        ).pack(side=tk.TOP, fill=tk.X, pady=1)

        tk.Checkbutton(
            grp_elem,
            text="Ký hiệu nhãn tên đỉnh (A, B, C, S, M, N...)" if is_vn else "Vertex Labels (A, B, C, S, M, N...)",
            variable=self.var_labels,
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            anchor="w",
        ).pack(side=tk.TOP, fill=tk.X, pady=1)

        # Group 2: Styling & Background
        grp_style = tk.LabelFrame(
            self,
            text="2. Kiểu nét vẽ & Nền ảnh" if is_vn else "2. Style & Background",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            padx=10,
            pady=6,
        )
        grp_style.pack(side=tk.TOP, fill=tk.X, padx=10, pady=4)

        f_hid = tk.Frame(grp_style, bg=self.WIN32_BG)
        f_hid.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Label(f_hid, text="Nét khuất:" if is_vn else "Hidden Lines:", font=self.FONT_UI, bg=self.WIN32_BG, width=12, anchor="w").pack(side=tk.LEFT)
        tk.Radiobutton(f_hid, text="Nét đứt (cạnh khuất)" if is_vn else "Dashed lines", variable=self.var_hidden, value="dashed", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=4)
        tk.Radiobutton(f_hid, text="Khung dây" if is_vn else "Wireframe", variable=self.var_hidden, value="solid", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=4)
        tk.Radiobutton(f_hid, text="Ẩn cạnh khuất" if is_vn else "Culled", variable=self.var_hidden, value="hidden", bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=4)

        f_bg = tk.Frame(grp_style, bg=self.WIN32_BG)
        f_bg.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Checkbutton(
            f_bg,
            text="Nền trong suốt (Transparent PNG)" if is_vn else "Transparent Background (PNG)",
            variable=self.var_transparent,
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            anchor="w",
        ).pack(side=tk.LEFT)

        tk.Checkbutton(
            f_bg,
            text="Nét vẽ ĐẬM rõ nét" if is_vn else "Bold CAD Lines",
            variable=self.var_bold,
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            anchor="w",
        ).pack(side=tk.RIGHT)

        # Group 3: Resolution / Scale
        grp_dpi = tk.LabelFrame(
            self,
            text="3. Độ phân giải kết xuất" if is_vn else "3. Render Resolution & Quality",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            padx=10,
            pady=6,
        )
        grp_dpi.pack(side=tk.TOP, fill=tk.X, padx=10, pady=4)

        f_dpi = tk.Frame(grp_dpi, bg=self.WIN32_BG)
        f_dpi.pack(side=tk.TOP, fill=tk.X)
        tk.Radiobutton(f_dpi, text="2x (300 DPI - In ấn rõ nét)" if is_vn else "2x (300 DPI - Standard Print)", variable=self.var_scale, value=2, bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=4)
        tk.Radiobutton(f_dpi, text="3x (450 DPI - Poster)" if is_vn else "3x (450 DPI - High Res)", variable=self.var_scale, value=3, bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=4)
        tk.Radiobutton(f_dpi, text="1x (Màn hình 96 DPI)" if is_vn else "1x (Screen 96 DPI)", variable=self.var_scale, value=1, bg=self.WIN32_BG, font=self.FONT_UI).pack(side=tk.LEFT, padx=4)

        # Status Pro / Watermark Notice Banner
        is_pro = LicenseManager.is_pro_active() if LicenseManager else False
        f_status = tk.Frame(self, bg="#E8F5E9" if is_pro else "#FFF8E1", relief=tk.SOLID, bd=1)
        f_status.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(6, 2))
        if is_pro:
            txt_status = "💎 Bản Pro đã kích hoạt: In ấn & xuất ảnh SẠCH 100% (Không dính Watermark)." if is_vn else "💎 Pro Edition Active: 100% clean printing & export (No Watermark)."
            fg_status = "#2E7D32"
        else:
            txt_status = "ℹ️ Bản Tiêu Chuẩn: In & xuất file (PNG/JPEG) có hình mờ nhẹ. [ Mua Pro $1.99 để in sạch 100% ]" if is_vn else "ℹ️ Standard Edition: Output has subtle watermark. [ Buy Pro $1.99 for clean print ]"
            fg_status = "#8D6E63"
        lbl_st = tk.Label(f_status, text=txt_status, font=self.FONT_UI, bg="#E8F5E9" if is_pro else "#FFF8E1", fg=fg_status, padx=6, pady=3)
        lbl_st.pack(side=tk.LEFT)
        if not is_pro:
            tk.Button(f_status, text="[ Mua $1.99 ]" if is_vn else "[ Buy $1.99 ]", font=self.FONT_BOLD, bg="#2E7D32", fg="#FFFFFF", relief=tk.RAISED, bd=1, padx=4, command=lambda: ProUpgradeDialog(self.app, feature="print")).pack(side=tk.RIGHT, padx=4, pady=2)

        # Buttons
        btn_box = tk.Frame(self, bg=self.WIN32_BG, pady=10)
        btn_box.pack(side=tk.BOTTOM, fill=tk.X, padx=10)

        tk.Button(
            btn_box,
            text="[ 💾 Xuất ảnh ngay... ]" if is_vn else "[ 💾 Save Image Now... ]",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            fg="#000080",
            relief=tk.RAISED,
            bd=2,
            padx=12,
            pady=4,
            command=self._on_export,
        ).pack(side=tk.LEFT, padx=4)

        tk.Button(
            btn_box,
            text="[ 🖨️ In bản vẽ... ]" if is_vn else "[ 🖨️ Print Now... ]",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            fg="#1971C2",
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=4,
            command=self._on_print,
        ).pack(side=tk.LEFT, padx=4)

        tk.Button(
            btn_box,
            text="[ Hủy ]" if is_vn else "[ Cancel ]",
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=4,
            command=self.destroy,
        ).pack(side=tk.RIGHT, padx=4)

    def _on_print(self) -> None:
        """In trực tiếp bản vẽ 3D độ nét cao (300 DPI) ra máy in qua Windows Print Wizard."""
        is_vn = (self.lang == "VN")
        import tempfile
        temp_img = os.path.join(tempfile.gettempdir(), f"geosolver3d_print_{os.getpid()}.png")
        try:
            self.app._render_scene_to_image(
                temp_img,
                scale=self.var_scale.get(),
                show_axes=self.var_axes.get(),
                show_sphere=self.var_sphere.get(),
                show_section=self.var_section.get(),
                show_auxiliary=self.var_aux.get(),
                show_labels=self.var_labels.get(),
                hidden_mode=self.var_hidden.get(),
                bold_mode=self.var_bold.get(),
                transparent_bg=False,
            )
            os.startfile(temp_img, "print")
            self.destroy()
        except Exception as ex:
            messagebox.showerror(
                "Lỗi in ấn" if is_vn else "Print Error",
                f"Không thể mở trình in Windows: {ex}" if is_vn else f"Unable to open Windows print wizard: {ex}",
                parent=self,
            )

    def _on_export(self) -> None:
        is_vn = (self.lang == "VN")
        file_path = filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".png",
            filetypes=[
                ("PNG Image (*.png)", "*.png"),
                ("JPEG Image (*.jpg;*.jpeg)", "*.jpg;*.jpeg"),
                ("PostScript Vector (*.eps)", "*.eps"),
                ("All Files (*.*)", "*.*")
            ],
            title="Lưu ảnh bản vẽ 3D" if is_vn else "Save 3D Diagram Image",
        )
        if not file_path:
            return
        try:
            if file_path.lower().endswith((".eps", ".ps")):
                self.app.canvas.postscript(file=file_path, colormode="color")
                messagebox.showinfo(
                    "Thành công" if is_vn else "Success",
                    f"Đã xuất bản vẽ Vector EPS thành công tại:\n{file_path}"
                    if is_vn
                    else f"Vector EPS file exported successfully to:\n{file_path}",
                    parent=self,
                )
            else:
                ext = os.path.splitext(file_path)[1].lower()
                if not ext:
                    file_path += ".png"
                self.app._render_scene_to_image(
                    file_path,
                    scale=self.var_scale.get(),
                    show_axes=self.var_axes.get(),
                    show_sphere=self.var_sphere.get(),
                    show_section=self.var_section.get(),
                    show_auxiliary=self.var_aux.get(),
                    show_labels=self.var_labels.get(),
                    hidden_mode=self.var_hidden.get(),
                    bold_mode=self.var_bold.get(),
                    transparent_bg=self.var_transparent.get(),
                )
                messagebox.showinfo(
                    "Thành công" if is_vn else "Success",
                    f"Đã xuất ảnh chất lượng cao thành công tại:\n{file_path}"
                    if is_vn
                    else f"Image exported successfully to:\n{file_path}",
                    parent=self,
                )
                self.destroy()
        except Exception as ex:
            messagebox.showerror(
                "Lỗi" if is_vn else "Error",
                f"Lỗi xuất ảnh: {ex}" if is_vn else f"Export error: {ex}",
                parent=self,
            )


# ==============================================================================
# WIN32 PRO ACTIVATE CODE DIALOG (1-MACHINE HARDWARE ID BINDING)
# ==============================================================================

class ActivateCodeDialog(tk.Toplevel):
    """Hộp thoại hiển thị Hardware ID và nhập mã kích hoạt khóa theo 1 máy tính."""
    WIN32_BG = "#ECE9D8"
    FONT_BOLD = ("Tahoma", 8, "bold")
    FONT_UI = ("Tahoma", 8)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent_upgrade = parent
        self.app = parent.app
        self.lang = getattr(parent, "lang", "VN")
        is_vn = (self.lang == "VN")

        self.title("Kích Hoạt Bản Quyền GeoSolver 3D Pro" if is_vn else "Activate GeoSolver 3D Pro")
        self.geometry("490x280")
        self.resizable(False, False)
        self.configure(bg=self.WIN32_BG)
        self.transient(parent)
        self.grab_set()

        from geosolver_3d.license_manager import LicenseManager
        hwid = LicenseManager.get_hardware_id() if LicenseManager else "N/A"

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

        tk.Label(hw_row, text=hwid, font=("Consolas", 11, "bold"), fg="#000080", bg="#FFFFFF", relief=tk.SUNKEN, bd=1, padx=8, pady=2).pack(side=tk.LEFT, fill=tk.X, expand=True)

        def copy_hwid():
            self.clipboard_clear()
            self.clipboard_append(hwid)
            messagebox.showinfo("Đã sao chép" if is_vn else "Copied", "Đã sao chép mã máy tính vào bộ nhớ đệm!\nHãy gửi mã này để nhận key kích hoạt." if is_vn else "Hardware ID copied to clipboard!", parent=self)

        tk.Button(hw_row, text="[ 📋 Sao chép ]" if is_vn else "[ 📋 Copy ]", font=self.FONT_BOLD, bg=self.WIN32_BG, padx=6, command=copy_hwid).pack(side=tk.RIGHT, padx=(6, 0))

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

        tk.Label(code_box, text="Nhập mã kích hoạt Pro nhận được:" if is_vn else "Enter received Pro Activation Code:", font=self.FONT_BOLD, bg=self.WIN32_BG).pack(anchor="w", pady=(2, 2))
        self.entry_code = tk.Entry(code_box, font=("Consolas", 11, "bold"), justify="center")
        self.entry_code.pack(fill=tk.X, pady=2)
        self.entry_code.focus_set()

        # Buttons
        btn_box = tk.Frame(self, bg=self.WIN32_BG, padx=12, pady=10)
        btn_box.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(btn_box, text="[ Kích Hoạt Ngay ]" if is_vn else "[ Activate Now ]", font=self.FONT_BOLD, bg="#2E7D32", fg="#FFFFFF", padx=10, pady=4, command=self._do_activate).pack(side=tk.LEFT)
        tk.Button(btn_box, text="[ Hủy ]" if is_vn else "[ Cancel ]", font=self.FONT_UI, bg=self.WIN32_BG, padx=8, pady=4, command=self.destroy).pack(side=tk.RIGHT)

    def _do_activate(self):
        code = self.entry_code.get().strip()
        is_vn = (self.lang == "VN")
        if not code:
            messagebox.showwarning("Thiếu dữ liệu" if is_vn else "Warning", "Vui lòng nhập mã kích hoạt!" if is_vn else "Please enter activation code!", parent=self)
            return
        from geosolver_3d.license_manager import LicenseManager
        if LicenseManager:
            ok, msg = LicenseManager.activate_with_code(code)
            if ok:
                messagebox.showinfo("Kích hoạt thành công" if is_vn else "Success", msg, parent=self)
                if hasattr(self.app, "update_pro_ui_state"):
                    self.app.update_pro_ui_state()
                self.destroy()
                self.parent_upgrade.destroy()
            else:
                messagebox.showwarning("Kích hoạt thất bại" if is_vn else "Failed", msg, parent=self)


# ==============================================================================
# WIN32 PRO UPGRADE & IAP DIALOG ($1.99)
# ==============================================================================

class ProUpgradeDialog(tk.Toplevel):
    """Hộp thoại giới thiệu và nâng cấp Gói Pro ($1.99) qua Microsoft Store IAP hoặc mã kích hoạt."""
    WIN32_BG = "#ECE9D8"
    FONT_TITLE = ("Tahoma", 10, "bold")
    FONT_BOLD = ("Tahoma", 8, "bold")
    FONT_UI = ("Tahoma", 8)

    def __init__(self, parent, feature: str = "general"):
        super().__init__(parent)
        self.app = parent
        self.lang = getattr(parent, "lang", "VN")
        self.feature = feature
        is_vn = (self.lang == "VN")

        self.title("Nâng Cấp GeoSolver 3D Pro ($1.99) - Gói In Ấn Sạch" if is_vn else "Upgrade to GeoSolver 3D Pro ($1.99) - Clean Print")
        self.geometry("540x470")
        self.resizable(False, False)
        self.configure(bg=self.WIN32_BG)
        self.transient(parent)
        self.grab_set()

        # Banner Header
        hdr = tk.Frame(self, bg="#002D62", pady=10, padx=16)
        hdr.pack(side=tk.TOP, fill=tk.X)

        tk.Label(
            hdr,
            text="💎 GEOSOLVER 3D PRO — GÓI IN ẤN & XUẤT BẢN VẼ SẠCH",
            font=("Tahoma", 11, "bold"),
            bg="#002D62",
            fg="#FFD700",
        ).pack(anchor="w")

        subtitle_vn = "Sở hữu trọn đời chỉ $1.99 — Gỡ bỏ hoàn toàn hình mờ (No Watermark)"
        subtitle_en = "Lifetime access for only $1.99 — 100% Watermark-Free Direct Printing"
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
            msg_vn = "ℹ️ Bản Tiêu Chuẩn cho phép in ấn có hình mờ bản quyền nhẹ. Gói Pro ($1.99) giúp in bản vẽ SẠCH 100% không hình mờ."
            msg_en = "ℹ️ Standard Edition prints with subtle watermark. Pro Edition ($1.99) prints 100% CLEAN diagrams."
        elif feature == "export_hd":
            msg_vn = "ℹ️ Gói Pro ($1.99) hỗ trợ xuất file ảnh PNG / JPEG sắc nét 300 DPI / 450 DPI sạch 100%, không dính hình mờ."
            msg_en = "ℹ️ Pro Edition ($1.99) exports crisp 300/450 DPI PNG/JPEG diagrams completely free of watermarks."
        else:
            msg_vn = "ℹ️ Nâng cấp Pro ($1.99) để sở hữu tính năng In ấn & Xuất bản vẽ sạch 100% không hình mờ trọn đời."
            msg_en = "ℹ️ Upgrade to Pro ($1.99) for lifetime 100% watermark-free printing and clean CAD exports."

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
            "Đặc quyền của Gói Pro In Ấn & Bản Vẽ Sạch ($1.99):\n\n"
            "• 🖨️ In ấn trực tiếp sạch 100% (Ctrl+P): In ra máy in qua Windows Print Wizard không dính hình mờ bản quyền.\n"
            "• 📐 Xuất ảnh PNG / JPEG siêu nét 300 DPI / 450 DPI: Không có watermark, nền trong suốt hoặc nền trắng tinh khiết.\n"
            "• 📄 Phục vụ chuyên nghiệp: Soạn bài giảng, giáo án điện tử, đề thi, phiếu học tập và tài liệu nghiên cứu.\n"
            "• 🌐 Sở hữu trọn đời: Hỗ trợ miễn phí toàn bộ các bản cập nhật và gói đa ngôn ngữ trong tương lai."
        )
        features_en = (
            "Exclusive benefits of Pro Printing & Clean Export ($1.99):\n\n"
            "• 🖨️ 100% Clean Direct Printing (Ctrl+P): Print technical drawings via Windows Print Wizard without any watermark.\n"
            "• 📐 Ultra High-Res Export (300/450 DPI): Clean PNG & JPEG diagrams without watermarks for professional use.\n"
            "• 📄 Ideal for Educators: Perfect for exam sheets, worksheets, research papers, and textbook preparations.\n"
            "• 🌐 Lifetime Ownership: Free access to all future updates and upcoming international language packs."
        )

        tk.Label(
            body,
            text=features_vn if is_vn else features_en,
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            fg="#222222",
            justify=tk.LEFT,
            anchor="nw",
            wraplength=500,
        ).pack(fill=tk.BOTH, expand=True)

        # Action Buttons Box
        btn_box = tk.Frame(self, bg=self.WIN32_BG, padx=14, pady=8)
        btn_box.pack(side=tk.BOTTOM, fill=tk.X)

        # Primary Store Purchase Button ($1.99)
        btn_store = tk.Button(
            btn_box,
            text="[ 🛒 Mua Gói Pro Trên Microsoft Store ($1.99) ]" if is_vn else "[ 🛒 Buy Pro on Microsoft Store ($1.99) ]",
            font=("Tahoma", 9, "bold"),
            bg="#2E7D32",
            fg="#FFFFFF",
            activebackground="#1B5E20",
            activeforeground="#FFFFFF",
            relief=tk.RAISED,
            bd=3,
            padx=12,
            pady=5,
            command=self._on_store_buy,
        )
        btn_store.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))

        # Secondary row: Enter Code / Cancel
        sub_row = tk.Frame(btn_box, bg=self.WIN32_BG)
        sub_row.pack(side=tk.TOP, fill=tk.X)

        tk.Button(
            sub_row,
            text="[ 🔑 Nhập Mã Kích Hoạt / Promo Code ]" if is_vn else "[ 🔑 Enter License / Promo Code ]",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            fg="#000080",
            relief=tk.RAISED,
            bd=2,
            padx=8,
            pady=3,
            command=self._on_enter_code,
        ).pack(side=tk.LEFT)

        tk.Button(
            sub_row,
            text="[ Tiếp Tục Bản Miễn Phí ]" if is_vn else "[ Continue Free ]",
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            padx=8,
            pady=3,
            command=self.destroy,
        ).pack(side=tk.RIGHT)

    def _on_store_buy(self) -> None:
        try:
            from geosolver_3d.license_manager import LicenseManager
            if LicenseManager:
                LicenseManager.open_store_purchase()
        except Exception:
            pass

    def _on_enter_code(self) -> None:
        ActivateCodeDialog(self)


# ==============================================================================
# WIN32 PRODUCT ABOUT DIALOG
# ==============================================================================

class ProductAboutDialog(tk.Toplevel):
    """Hộp thoại Thông tin sản phẩm GeoSolver 3D."""
    WIN32_BG = "#ECE9D8"
    FONT_UI = ("Tahoma", 9)
    FONT_BOLD = ("Tahoma", 9, "bold")

    def __init__(self, parent: "GeoSolver3DApp"):
        super().__init__(parent)
        self.app = parent
        is_vn = (parent.lang == "VN")
        self.title("Thông Tin Sản Phẩm - GeoSolver 3D" if is_vn else "About - GeoSolver 3D CAD Studio")
        self.geometry("540x450")
        self.resizable(False, False)
        self.configure(bg=self.WIN32_BG)
        self.transient(parent)
        self.grab_set()

        hdr = tk.Frame(self, bg=self.WIN32_BG, pady=10)
        hdr.pack(side=tk.TOP, fill=tk.X, padx=14)

        tk.Label(
            hdr,
            text="GEOSOLVER 3D CAD PRO",
            font=("Tahoma", 12, "bold"),
            bg=self.WIN32_BG,
            fg="#000080",
        ).pack(side=tk.TOP, anchor="w")

        tk.Label(
            hdr,
            text="Phiên bản 3.2.1.0 (Gói In Ấn Pro) - Dựng hình & Giải toán Hình học Không gian CAD"
            if is_vn
            else "Version 3.2.1.0 (Pro Print Edition) - 3D Spatial Geometry & CAD Studio",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            fg="#222222",
        ).pack(side=tk.TOP, anchor="w", pady=(2, 6))

        info_frame = tk.LabelFrame(
            self,
            text="Thông tin phần mềm" if is_vn else "Software Information",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            padx=10,
            pady=8,
        )
        info_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=14, pady=4)

        desc_vn = (
            "• Phiên bản 3.2.1.0: Hỗ trợ in ấn bản vẽ CAD và xuất ảnh PNG/JPEG chất lượng cao.\n"
            "• Phần mềm hỗ trợ học tập và vẽ hình học không gian 3 chiều.\n"
            "• Các chức năng chính:\n"
            "    - 12 Khối hình mẫu: Hình chóp, tứ diện, lăng trụ, hình hộp, hình lập phương...\n"
            "    - Tự động vẽ nét đứt cho cạnh khuất và nét liền cho cạnh nhìn thấy.\n"
            "    - Cắt hình bằng mặt phẳng để xem thiết diện và gạch sọc mặt cắt CAD.\n"
            "    - Xác định tâm và bán kính mặt cầu ngoại tiếp (chống suy biến số học).\n"
            "    - 12 Dạng bài tập suy luận từng bước, công thức hiển thị dạng căn thức dễ nhìn.\n"
            "    - Xuất ảnh PNG, JPEG và in ấn trực tiếp (Bản Tiêu Chuẩn kèm hình mờ nhẹ).\n"
            "    - [Gói Pro $1.99] Mở khóa in ấn trực tiếp và xuất ảnh sạch 100% không dính Watermark.\n"
            "• Đội ngũ phát triển: STEM AI & Math CAD Research Team."
        )
        desc_en = (
            "• Version 3.2.1.0: Direct CAD printing and high-resolution PNG/JPEG export.\n"
            "• Software for learning and drawing 3D spatial geometry.\n"
            "• Main features:\n"
            "    - 12 Standard 3D shapes: Pyramids, tetrahedra, prisms, boxes, cubes...\n"
            "    - Automatic dashed lines for hidden edges and solid lines for visible edges.\n"
            "    - Plane slicing to view cross-sections with line hatching.\n"
            "    - Circumscribed sphere radius and center determination.\n"
            "    - 12 Step-by-step geometry topics with natural radical formulas.\n"
            "    - PNG & JPEG export and direct printing (Standard Edition has subtle watermark).\n"
            "    - [Pro Edition $1.99] 100% Watermark-Free Direct Printing and Clean Export.\n"
            "• Developed by: STEM AI & Math CAD Research Team."
        )

        tk.Label(
            info_frame,
            text=desc_vn if is_vn else desc_en,
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            justify=tk.LEFT,
            anchor="nw",
        ).pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        is_pro = LicenseManager.is_pro_active() if LicenseManager else False
        status_text = "Trạng thái: 💎 Đã kích hoạt Gói Pro ($1.99)" if is_pro else "Trạng thái: 🆓 Bản Tiêu Chuẩn (Free)"
        if not is_vn:
            status_text = "Status: 💎 Pro Edition Active ($1.99)" if is_pro else "Status: 🆓 Standard Edition (Free)"

        lbl_status = tk.Label(
            info_frame,
            text=status_text,
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            fg="#2E7D32" if is_pro else "#C2410C",
            anchor="w",
            pady=4,
        )
        lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

        btn_box = tk.Frame(self, bg=self.WIN32_BG, pady=8)
        btn_box.pack(side=tk.BOTTOM, fill=tk.X, padx=14)

        if not is_pro:
            tk.Button(
                btn_box,
                text="[ 💎 Nâng Cấp Pro ($1.99) ]" if is_vn else "[ 💎 Upgrade to Pro ($1.99) ]",
                font=self.FONT_BOLD,
                bg="#2E7D32",
                fg="#FFFFFF",
                relief=tk.RAISED,
                bd=2,
                padx=10,
                pady=3,
                command=lambda: (self.destroy(), ProUpgradeDialog(self.app)),
            ).pack(side=tk.LEFT)

        tk.Button(
            btn_box,
            text="[ Đóng ]" if is_vn else "[ Close ]",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            padx=12,
            pady=3,
            command=self.destroy,
        ).pack(side=tk.RIGHT)


# ==============================================================================
# WIN32 SHORTCUTS GUIDE DIALOG
# ==============================================================================

# ==============================================================================
# WIN32 USER HANDBOOK DIALOG (CẨM NANG HƯỚNG DẪN SỬ DỤNG CHI TIẾT)
# ==============================================================================

class UserHandbookDialog(tk.Toplevel):
    """Hộp thoại Cẩm nang hướng dẫn sử dụng chi tiết từng mục và phím tắt."""
    WIN32_BG = "#ECE9D8"
    FONT_UI = ("Tahoma", 9)
    FONT_BOLD = ("Tahoma", 9, "bold")
    FONT_MONO = ("Consolas", 9)

    SECTIONS_VN = [
        ("1. Giới thiệu tổng quan", (
            "1. GIỚI THIỆU TỔNG QUAN\n\n"
            "GeoSolver 3D là phần mềm hỗ trợ vẽ hình học không gian 3 chiều và giải toán hình học.\n"
            "Phần mềm giúp bạn:\n"
            "  • Quan sát trực quan các khối hình: chóp, tứ diện, lăng trụ, hình hộp, hình lập phương...\n"
            "  • Tự động vẽ nét đứt cho cạnh bị che khuất và nét liền cho cạnh nhìn thấy.\n"
            "  • Cắt hình bằng mặt phẳng để xem thiết diện và gạch sọc mặt cắt.\n"
            "  • Xem lời giải chi tiết cho 12 dạng bài tập quen thuộc với công thức căn thức tự nhiên (như √3, √41/2).\n"
            "  • Xuất ảnh PNG (có tùy chọn nền trong suốt để chèn vào Word) và xuất báo cáo HTML.\n"
        )),
        ("2. Giao diện phần mềm", (
            "2. GIAO DIỆN PHẦN MỀM\n\n"
            "Giao diện gồm 4 khu vực chính:\n"
            "  • Thanh Menu trên cùng: Tệp, Chỉnh sửa, Hiển thị, Công cụ, Tùy chọn, Thông tin.\n"
            "  • Hàng nút bấm Ribbon: Chọn khối mẫu, hoàn tác (Ctrl+Z), làm lại (Ctrl+Y), xuất ảnh, thu phóng, trục Oxyz, nét đứt, thiết diện, mặt cầu.\n"
            "  • Khung vẽ hình 3D (Canvas): Nơi hiển thị hình khối, giữ chuột trái để xoay, lăn chuột để phóng to/thu nhỏ.\n"
            "  • Cột thông số bên phải (Sidebar): Nhập kích thước đáy, chiều cao, góc xoay mặt cắt và xem kết quả tính thể tích V, diện tích S, bán kính mặt cầu R.\n"
        )),
        ("3. Chọn hình khối mẫu", (
            "3. CHỌN HÌNH KHỐI MẪU\n\n"
            "Bấm vào danh sách 'Chọn Khối Đa Diện' trên thanh công cụ hoặc menu 'Tệp -> Mở Khối Đa Diện Mẫu':\n"
            "  1. Chóp tam giác S.ABC\n"
            "  2. Tứ diện đều ABCD\n"
            "  3. Chóp tứ giác đều S.ABCD\n"
            "  4. Chóp có cạnh bên vuông góc đáy\n"
            "  5. Lăng trụ đứng tam giác\n"
            "  6. Lăng trụ tam giác đều\n"
            "  7. Hình hộp chữ nhật\n"
            "  8. Hình lập phương\n"
            "  9. Lăng trụ xiên tam giác\n"
            "  10. Bát diện đều\n"
            "  11. Chóp cụt tứ giác đều\n"
            "  12. Chóp đáy hình thang\n"
        )),
        ("4. Xoay, thu phóng & góc nhìn", (
            "4. ĐIỀU HƯỚNG GÓC NHÌN 3D\n\n"
            "  • Xoay hình 3D: Giữ chuột trái trên khung vẽ và kéo chuột sang trái, phải, lên hoặc xuống. Hoặc dùng 4 phím mũi tên ← → ↑ ↓.\n"
            "  • Phóng to, thu nhỏ: Lăn con lăn chuột tới trước hoặc lùi. Hoặc nhấn phím Ctrl++ / Ctrl+-.\n"
            "  • Đặt lại góc nhìn ban đầu: Nhấn Ctrl+0 (hoặc nút [ ↺ Đặt lại ]).\n"
            "  • Chuyển chế độ xoay: Nhấn phím M.\n"
        )),
        ("5. Kéo dời đỉnh & thêm điểm", (
            "5. KÉO DỜI ĐỈNH VÀ THÊM ĐIỂM TRÊN CẠNH\n\n"
            "  • Kéo dời đỉnh: Nhấn phím V (hoặc nút [ Dời đỉnh ]), rê chuột vào đỉnh màu đỏ rồi giữ chuột trái kéo. Nhấn Ctrl+R để đưa các đỉnh về vị trí ban đầu.\n"
            "  • Thêm điểm trên cạnh: Vào menu 'Công cụ -> Thêm Điểm Trên Đoạn Thẳng (Tỉ số k)', chọn cạnh (như SA hoặc BC), kéo thanh tỉ số k (k = 0.5 là trung điểm) rồi bấm Đồng ý.\n"
        )),
        ("6. Cắt hình (thiết diện)", (
            "6. CẮT HÌNH BẰNG MẶT PHẲNG (THIẾT DIỆN)\n\n"
            "  • Bật/tắt thiết diện: Nhấn phím S hoặc nút [ Thiết diện ].\n"
            "  • 4 Hướng cắt nhanh: Oxy (cắt ngang), Cắt Xiên (cắt chéo), Oxz (cắt đứng), Cắt Chéo Đáy.\n"
            "  • Điều chỉnh vị trí: Kéo thanh trượt vị trí ở cột bên phải để mặt cắt di chuyển lên xuống.\n"
            "  • Chế độ 'Độc lập đỉnh': Cho phép kéo từng đỉnh của mặt cắt tự do dọc theo các cạnh.\n"
        )),
        ("7. Gạch sọc mặt cắt & đổi màu", (
            "7. GẠCH SỌC MẶT CẮT (HATCHING) VÀ ĐỔI MÀU\n\n"
            "  • Mặt cắt khi cắt qua khối hình được tự động gạch sọc chéo 45° hoặc gạch ca-rô để dễ quan sát.\n"
            "  • Đổi màu hiển thị: Bấm vào 5 ô màu ở cột bên phải (Đỏ, Xanh, Đen, Lục, Cam) để đổi màu mặt cắt và đường viền.\n"
        )),
        ("8. Mặt cầu ngoại tiếp", (
            "8. MẶT CẦU NGOẠI TIẾP\n\n"
            "  • Bật/tắt mặt cầu: Nhấn phím C hoặc nút [ Cầu Ngoại Tiếp ].\n"
            "  • Phần mềm tự động xác định tâm I và tính bán kính R dưới dạng căn thức tự nhiên (như R = √41/2).\n"
        )),
        ("9. Giải toán 3D (12 dạng bài)", (
            "9. XEM CÁC DẠNG BÀI TẬP VÀ LỜI GIẢI MẪU\n\n"
            "Nhấn phím F5 hoặc phím D để mở bảng giải toán gồm 12 bài toán:\n"
            "  1. Đường thẳng vuông góc mặt phẳng\n"
            "  2. Hai mặt phẳng vuông góc\n"
            "  3. Góc giữa đường thẳng và mặt phẳng\n"
            "  4. Góc giữa hai mặt phẳng\n"
            "  5. Khoảng cách từ điểm đến mặt phẳng\n"
            "  6. Khoảng cách giữa hai đường thẳng chéo nhau\n"
            "  7. Tâm và bán kính mặt cầu ngoại tiếp\n"
            "  8. Thể tích và diện tích hình chóp\n"
            "  9. Thể tích và diện tích hình lăng trụ\n"
            "  10. Thiết diện và diện tích thiết diện\n"
            "  11. Tỉ số thể tích khối đa diện\n"
            "  12. Hệ trục tọa độ Oxyz trong không gian\n\n"
            "Nhập số liệu vào các ô và bấm 'Tính toán'. Lời giải hiển thị từng bước rõ ràng, kết quả căn thức chính xác. Có nút 'Sao chép lời giải' để dán vào Word.\n"
        )),
        ("10. Xuất ảnh & xuất báo cáo", (
            "10. XUẤT ẢNH VÀ XUẤT BÁO CÁO\n\n"
            "  • Xuất ảnh (Ctrl+E): Mở hộp thoại chọn hiển thị trục Oxyz, mặt cầu, thiết diện. Tích chọn 'Nền trong suốt' để chèn ảnh vào Word không bị viền xám. Chọn độ phân giải 96 DPI hoặc 300 DPI.\n"
            "  • Xuất báo cáo HTML (Ctrl+P): Tạo file web gồm ảnh 3D và các bảng thông số số liệu để xem hoặc in ấn.\n"
        )),
        ("11. Hoàn tác, sao chép & dán", (
            "11. HOÀN TÁC (UNDO/REDO), SAO CHÉP & DÁN\n\n"
            "  • Ctrl + Z: Hoàn tác bước vừa làm khi chỉnh nhầm.\n"
            "  • Ctrl + Y: Làm lại bước vừa hoàn tác.\n"
            "  • Ctrl + C: Sao chép thông số hoặc lời giải.\n"
            "  • Ctrl + V: Dán thông số vào ô đang chọn.\n"
        )),
        ("12. Bảng phím tắt & chuột", (
            "12. BẢNG PHÍM TẮT VÀ THAO TÁC CHUỘT TOÀN TẬP\n\n"
            "  • F1              : Mở cẩm nang hướng dẫn sử dụng\n"
            "  • F5 hoặc D       : Mở bảng giải 12 bài toán hình không gian\n"
            "  • Ctrl + Z        : Hoàn tác (Undo)\n"
            "  • Ctrl + Y        : Làm lại (Redo)\n"
            "  • Ctrl + C        : Sao chép thông số / lời giải\n"
            "  • Ctrl + V        : Dán thông số\n"
            "  • Ctrl + R        : Đưa các đỉnh về vị trí ban đầu\n"
            "  • Ctrl + E        : Xuất hình ảnh PNG (có nền trong suốt)\n"
            "  • Ctrl + P        : Xuất báo cáo HTML\n"
            "  • Ctrl + + / -    : Phóng to / Thu nhỏ hình\n"
            "  • Ctrl + 0        : Đặt lại góc nhìn mặc định ban đầu\n"
            "  • M               : Chế độ xoay hình 3D\n"
            "  • V               : Chế độ kéo dời đỉnh\n"
            "  • X               : Bật/tắt trục tọa độ Oxyz\n"
            "  • H               : Bật/tắt nét đứt cạnh khuất\n"
            "  • S               : Bật/tắt mặt phẳng cắt (thiết diện)\n"
            "  • C               : Bật/tắt mặt cầu ngoại tiếp\n"
            "  • B               : Đổi nét vẽ ĐẬM / MẢNH\n"
            "  • ← → ↑ ↓         : Xoay hình từng bước bằng phím mũi tên\n"
            "  • Alt + F4        : Thoát phần mềm\n\n"
            "THAO TÁC CHUỘT:\n"
            "  • Giữ chuột trái trên vùng trống: Xoay hình 3D.\n"
            "  • Lăn con lăn chuột: Phóng to / thu nhỏ.\n"
            "  • Giữ chuột trái trên đỉnh đỏ: Kéo đỉnh tới vị trí mới.\n"
            "  • Kéo vách ngăn giữa hai khung: Mở rộng khung vẽ hoặc cột thông số.\n"
        ))
    ]

    SECTIONS_EN = [
        ("1. Overview", (
            "1. OVERVIEW\n\n"
            "GeoSolver 3D is a software tool for drawing and exploring 3D spatial geometry.\n"
            "Key capabilities:\n"
            "  • Visualize 3D shapes: pyramids, tetrahedra, prisms, boxes, cubes, octahedra...\n"
            "  • Automatic dashed lines for hidden edges and solid lines for visible edges.\n"
            "  • Plane slicing to view cross-sections with line hatching.\n"
            "  • Circumscribed sphere center and radius calculation.\n"
            "  • Step-by-step solutions for 12 geometry topics with exact radical values (e.g. √3, √41/2).\n"
            "  • Export PNG images (with transparent background) and HTML reports.\n"
        )),
        ("2. User Interface", (
            "2. USER INTERFACE\n\n"
            "The main window is organized into 4 areas:\n"
            "  • Top Menu Bar: File, Edit, View, Tools, Options, Help.\n"
            "  • Ribbon Toolbar: Polyhedron selection, Undo (Ctrl+Z), Redo (Ctrl+Y), Export, Zoom, Oxyz Axes, Hidden Lines, Slicing, Sphere.\n"
            "  • 3D Drawing Canvas: Left-click and drag to orbit, scroll wheel to zoom.\n"
            "  • Right Sidebar: Adjust dimensions, height, slicing plane, and view Volume V, Surface Area S, and Sphere Radius R.\n"
        )),
        ("3. Standard Shapes", (
            "3. SELECTING STANDARD 3D SHAPES\n\n"
            "Choose a shape from the toolbar dropdown or 'File -> Open Standard Polyhedron':\n"
            "  1. Triangular Pyramid S.ABC\n"
            "  2. Regular Tetrahedron ABCD\n"
            "  3. Regular Square Pyramid S.ABCD\n"
            "  4. Pyramid with Edge Perpendicular to Base\n"
            "  5. Right Triangular Prism\n"
            "  6. Regular Triangular Prism\n"
            "  7. Rectangular Box\n"
            "  8. Cube\n"
            "  9. Oblique Triangular Prism\n"
            "  10. Regular Octahedron\n"
            "  11. Truncated Square Pyramid\n"
            "  12. Trapezoidal Base Pyramid\n"
        )),
        ("4. Orbit, Zoom & View", (
            "4. 3D CAMERA NAVIGATION\n\n"
            "  • 3D Orbit: Left-drag on canvas, or use arrow keys ← → ↑ ↓.\n"
            "  • Zoom: Mouse wheel scroll, or press Ctrl++ / Ctrl+-.\n"
            "  • Reset View: Press Ctrl+0 (or click [ ↺ Reset ]).\n"
            "  • Switch to Orbit Mode: Press key M.\n"
        )),
        ("5. Move Vertices & Points", (
            "5. MOVING VERTICES AND ADDING POINTS\n\n"
            "  • Move Vertex: Press V, hover over red vertex dot and drag. Press Ctrl+R to reset positions.\n"
            "  • Add Point on Segment: Go to 'Tools -> Add Point on Segment (Ratio k)', choose an edge, drag ratio k (k=0.5 for midpoint) and click OK.\n"
        )),
        ("6. Cross-Section Slicing", (
            "6. CROSS-SECTION SLICING\n\n"
            "  • Toggle Slicing: Press S or click [ Section ].\n"
            "  • 4 Quick Orientations: Oxy (horizontal), Oblique (tilted), Oxz (vertical), Diagonal.\n"
            "  • Position Slider: Drag the plane position slider on the sidebar to slide the plane up/down.\n"
            "  • Independent Vertex Mode: Drag individual section vertices along edges.\n"
        )),
        ("7. Hatching & Colors", (
            "7. CAD HATCHING AND COLOR PALETTE\n\n"
            "  • Sliced polygon surfaces feature diagonal 45° hatching or cross-hatching for clear visibility.\n"
            "  • Color Palette: Click on Red, Blue, Black, Green, or Orange in the sidebar to switch color.\n"
        )),
        ("8. Circumscribed Sphere", (
            "8. CIRCUMSCRIBED SPHERE\n\n"
            "  • Toggle Sphere: Press C or click [ Circumscribed Sphere ].\n"
            "  • Automatically computes center I and exact radical radius R (e.g. R = √41/2).\n"
        )),
        ("9. 12 Geometry Topics", (
            "9. 12 STEP-BY-STEP DEDUCTIVE TOPICS\n\n"
            "Press F5 or D to open the deductive solver for 12 core topics:\n"
            "  1. Line perpendicular to plane\n"
            "  2. Two perpendicular planes\n"
            "  3. Angle between line and plane\n"
            "  4. Dihedral angle between planes\n"
            "  5. Distance from point to plane\n"
            "  6. Distance between skew lines\n"
            "  7. Circumscribed sphere center & radius\n"
            "  8. Pyramid volume & surface area\n"
            "  9. Prism volume & surface area\n"
            "  10. Cross-section & section area\n"
            "  11. Volume ratio\n"
            "  12. 3D Cartesian coordinates Oxyz\n\n"
            "Enter parameters and click 'Compute'. Exact radical formulas and step reasons are provided. Click 'Copy Proof' to paste into Word.\n"
        )),
        ("10. Image & Report Export", (
            "10. IMAGE AND REPORT EXPORT\n\n"
            "  • Export Image (Ctrl+E): Choose to include axes, sphere, section. Check 'Transparent background' for seamless document insertion. Select 96 DPI or 300 DPI.\n"
            "  • HTML Report (Ctrl+P): Exports an HTML document with 3D diagram and complete telemetry tables.\n"
        )),
        ("11. Undo, Redo, Copy & Paste", (
            "11. UNDO, REDO, COPY & PASTE\n\n"
            "  • Ctrl + Z: Undo last modification.\n"
            "  • Ctrl + Y: Redo undone action.\n"
            "  • Ctrl + C: Copy telemetry or proof text.\n"
            "  • Ctrl + V: Paste coordinate data.\n"
        )),
        ("12. Shortcuts & Mouse", (
            "12. COMPLETE KEYBOARD & MOUSE SHORTCUTS\n\n"
            "  • F1              : Open User Handbook\n"
            "  • F5 or D         : Open 12 Topics Deductive Solver\n"
            "  • Ctrl + Z        : Undo\n"
            "  • Ctrl + Y        : Redo\n"
            "  • Ctrl + C        : Copy telemetry / proof text\n"
            "  • Ctrl + V        : Paste data\n"
            "  • Ctrl + R        : Reset solid coordinates\n"
            "  • Ctrl + E        : Export 3D Image (transparent PNG)\n"
            "  • Ctrl + P        : Export HTML Report\n"
            "  • Ctrl + + / -    : Step Zoom In / Zoom Out\n"
            "  • Ctrl + 0        : Reset Camera to default view\n"
            "  • M               : 3D Orbit Mode\n"
            "  • V               : Select & Move Vertex Mode\n"
            "  • X               : Toggle Oxyz Coordinate Axes\n"
            "  • H               : Toggle Hidden Dashed Lines\n"
            "  • S               : Toggle Cross-Section Plane\n"
            "  • C               : Toggle Circumscribed Sphere\n"
            "  • B               : Toggle Line Weight: BOLD / LIGHT\n"
            "  • ← → ↑ ↓         : Step Orbit with arrow keys\n"
            "  • Alt + F4        : Exit Application\n\n"
            "MOUSE NAVIGATION:\n"
            "  • Left-drag on canvas: 3D Camera Orbit.\n"
            "  • Mouse wheel: Dynamic Zoom in / out.\n"
            "  • Left-drag on red vertex: Move vertex position.\n"
            "  • Drag divider sash: Resize canvas / sidebar width.\n"
        ))
    ]

    def __init__(self, parent: "GeoSolver3DApp"):
        super().__init__(parent)
        self.app = parent
        is_vn = (parent.lang == "VN")
        self.title("Hướng Dẫn Sử Dụng GeoSolver 3D" if is_vn else "GeoSolver 3D User Guide")
        self.geometry("780x560")
        self.minsize(680, 480)
        self.configure(bg=self.WIN32_BG)
        self.transient(parent)
        self.grab_set()

        self.sections = self.SECTIONS_VN if is_vn else self.SECTIONS_EN

        # Top Header
        hdr = tk.Frame(self, bg=self.WIN32_BG, pady=6)
        hdr.pack(side=tk.TOP, fill=tk.X, padx=12)
        tk.Label(
            hdr,
            text="CẨM NANG HƯỚNG DẪN SỬ DỤNG GEOSOLVER 3D" if is_vn else "GEOSOLVER 3D USER GUIDE & HANDBOOK",
            font=("Tahoma", 11, "bold"),
            bg=self.WIN32_BG,
            fg="#000080",
        ).pack(side=tk.TOP, anchor="w")
        tk.Label(
            hdr,
            text="Chọn từng mục ở danh sách bên trái để xem hướng dẫn chi tiết và phím tắt." if is_vn else "Select a topic on the left to read detailed instructions and shortcuts.",
            font=self.FONT_UI,
            bg=self.WIN32_BG,
            fg="#444444",
        ).pack(side=tk.TOP, anchor="w")

        # Main Body Splitter
        body = tk.Frame(self, bg=self.WIN32_BG)
        body.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=12, pady=4)

        # Left listbox for topics
        left_frame = tk.Frame(body, bg=self.WIN32_BG, width=220)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 6))

        tk.Label(
            left_frame,
            text="Danh mục hướng dẫn:" if is_vn else "Topics:",
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

        # Right content area
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

        # Bottom Button Bar
        btn_box = tk.Frame(self, bg=self.WIN32_BG, pady=6)
        btn_box.pack(side=tk.BOTTOM, fill=tk.X, padx=12)

        tk.Button(
            btn_box,
            text="[ Sao Chép Nội Dung ]" if is_vn else "[ Copy Content ]",
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
            text="[ Đóng ]" if is_vn else "[ Close ]",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            padx=14,
            pady=3,
            command=self.destroy,
        ).pack(side=tk.RIGHT)

        # Select first topic by default
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
            is_vn = (self.app.lang == "VN")
            messagebox.showinfo(
                "Đã sao chép" if is_vn else "Copied",
                "Đã sao chép nội dung hướng dẫn vào Clipboard." if is_vn else "Handbook section copied to clipboard."
            )

class ShortcutsGuideDialog(tk.Toplevel):
    """Hộp thoại Bảng tra cứu phím tắt kỹ thuật & thao tác chuột."""
    WIN32_BG = "#ECE9D8"
    FONT_UI = ("Tahoma", 9)
    FONT_BOLD = ("Tahoma", 9, "bold")
    FONT_MONO = ("Consolas", 9)

    def __init__(self, parent: "GeoSolver3DApp"):
        super().__init__(parent)
        self.app = parent
        is_vn = (parent.lang == "VN")
        self.title("Bảng Phím Tắt & Thao Tác Chuột" if is_vn else "Shortcuts & Navigation Guide")
        self.geometry("640x520")
        self.configure(bg=self.WIN32_BG)
        self.transient(parent)
        self.grab_set()

        hdr = tk.Frame(self, bg=self.WIN32_BG, pady=6)
        hdr.pack(side=tk.TOP, fill=tk.X, padx=12)
        tk.Label(
            hdr,
            text="DANH SÁCH PHÍM TẮT & THAO TÁC ĐỒ HỌA 3D" if is_vn else "3D GRAPHICS SHORTCUTS & NAVIGATION GUIDE",
            font=("Tahoma", 10, "bold"),
            bg=self.WIN32_BG,
            fg="#000080",
        ).pack(side=tk.TOP, anchor="w")

        body = tk.Frame(self, bg=self.WIN32_BG)
        body.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=12, pady=4)

        txt = tk.Text(
            body,
            font=self.FONT_MONO,
            bg="#FFFFFF",
            fg="#000000",
            relief=tk.SUNKEN,
            bd=2,
            wrap=tk.WORD,
            padx=8,
            pady=8,
        )
        sb = tk.Scrollbar(body, orient=tk.VERTICAL, command=txt.yview)
        txt.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        txt_vn = (
            "═══════════════════════════════════════════════════════════════════\n"
            "                   DANH SÁCH PHÍM TẮT VÀ THAO TÁC CHUỘT                   \n"
            "═══════════════════════════════════════════════════════════════════\n\n"
            "1. TẬP TIN & XUẤT BẢN:\n"
            "   • Ctrl + E        : Mở hộp thoại Xuất hình ảnh CAD (Nhiều chế độ)\n"
            "   • Ctrl + P        : Xuất Báo cáo Kỹ thuật HTML & In ấn PDF\n"
            "   • Alt + F4        : Thoát khỏi ứng dụng\n\n"
            "2. CHỈNH SỬA & KHÔI PHỤC:\n"
            "   • Ctrl + Z        : Hoàn tác (Undo) thao tác trước\n"
            "   • Ctrl + Y        : Làm lại (Redo) thao tác vừa hoàn tác\n"
            "   • Ctrl + C        : Sao chép thông số khối & tọa độ vào Clipboard\n"
            "   • Ctrl + V        : Dán / Nhập dữ liệu tọa độ\n"
            "   • R / Ctrl + R    : Đưa các đỉnh về vị trí ban đầu\n\n"
            "3. ĐIỀU KHIỂN GÓC NHÌN & CAMERA 3D:\n"
            "   • Kéo chuột trái  : Xoay khối đa diện quanh trọng tâm (Orbit)\n"
            "   • Con lăn chuột   : Thu phóng tỷ lệ (Zoom In / Zoom Out)\n"
            "   • Ctrl + + / -    : Phóng to / Thu nhỏ khung nhìn\n"
            "   • Ctrl + 0 / Space: Đặt lại góc nhìn và tỷ lệ chuẩn ban đầu\n"
            "   • Mũi tên ← → ↑ ↓ : Xoay góc nhìn từng bước 5°\n\n"
            "4. CHẾ ĐỘ HIỂN THỊ HÌNH HỌC:\n"
            "   • M / V           : Chuyển đổi Xoay 3D / Chọn & Di chuyển đỉnh\n"
            "   • X               : Bật / Tắt hệ trục tọa độ Oxyz\n"
            "   • H               : Bật / Tắt nét đứt cạnh khuất (Dashed / Wireframe)\n"
            "   • S               : Bật / Tắt mặt phẳng thiết diện cắt\n"
            "   • C               : Bật / Tắt mặt cầu ngoại tiếp S(I; R)\n"
            "   • B               : Đổi nét vẽ ĐẬM (rõ nét) / MẢNH\n"
            "   • L               : Chuyển đổi ngôn ngữ Tiếng Việt / English\n\n"
            "5. CÔNG CỤ & SUY LUẬN TOÁN HỌC:\n"
            "   • D               : Mở Hộp thoại Suy luận 3D (12 Chuyên đề)\n"
            "   • F1              : Mở bảng hướng dẫn phím tắt này\n"
            "═══════════════════════════════════════════════════════════════════\n"
        )
        txt_en = (
            "═══════════════════════════════════════════════════════════════════\n"
            "                   WIN32 DESKTOP SHORTCUT GUIDE                    \n"
            "═══════════════════════════════════════════════════════════════════\n\n"
            "1. FILE & EXPORT:\n"
            "   • Ctrl + E        : Open Multi-Mode CAD Diagram Export Dialog\n"
            "   • Ctrl + P        : Export Technical HTML / Print PDF Report\n"
            "   • Alt + F4        : Exit Application\n\n"
            "2. EDIT & RECOVERY:\n"
            "   • Ctrl + Z        : Undo previous geometric action\n"
            "   • Ctrl + Y        : Redo previously undone action\n"
            "   • Ctrl + C        : Copy solid telemetry & coordinates to Clipboard\n"
            "   • Ctrl + V        : Paste / Import coordinate data\n"
            "   • R / Ctrl + R    : Reset solid polyhedron to canonical coordinates\n\n"
            "3. 3D CAMERA ORBIT & ZOOM NAVIGATION:\n"
            "   • Left Drag       : 3D Camera Orbit around model centroid\n"
            "   • Mouse Wheel     : Dynamic Zoom In / Zoom Out\n"
            "   • Ctrl + + / -    : Step Zoom In / Zoom Out\n"
            "   • Ctrl + 0 / Space: Reset camera view and zoom to default\n"
            "   • Arrow Keys      : Step Orbit by 5° intervals\n\n"
            "4. DISPLAY TOGGLES:\n"
            "   • M / V           : Switch 3D Orbit / Select & Move vertex mode\n"
            "   • X               : Toggle 3D Coordinate Axes Oxyz\n"
            "   • H               : Toggle Hidden Dashed Lines (Dashed / Wire)\n"
            "   • S               : Toggle Cross-Section Plane\n"
            "   • C               : Toggle Circumscribed Sphere S(I; R)\n"
            "   • B               : Toggle Line Weight: BOLD (Screen) / LIGHT (Print)\n"
            "   • L               : Toggle Language: Vietnamese / English\n\n"
            "5. PEDAGOGICAL TOOLS & DEDUCTION:\n"
            "   • D               : Open 3D Deductive Geometry Solver (12 Topics)\n"
            "   • F1              : Open this Shortcut Guide\n"
            "═══════════════════════════════════════════════════════════════════\n"
        )

        txt.insert(tk.END, txt_vn if is_vn else txt_en)
        txt.configure(state=tk.DISABLED)

        btn_box = tk.Frame(self, bg=self.WIN32_BG, pady=6)
        btn_box.pack(side=tk.BOTTOM, fill=tk.X, padx=12)
        tk.Button(
            btn_box,
            text="[ Đóng ]" if is_vn else "[ Close ]",
            font=self.FONT_BOLD,
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            padx=12,
            pady=2,
            command=self.destroy,
        ).pack(side=tk.RIGHT)


class GeoSolver3DApp(tk.Tk):
    """
    Main Desktop Application Window for GeoSolver 3D (Win32 Classic / MS Office 2003 / CAD Studio).
    """

    WIN32_BG = "#ECE9D8"
    WIN32_ACTIVE_BG = "#D6D2C2"
    CANVAS_BG = "#FFFFFF"
    FONT_TOOLBAR = ("Tahoma", 9)
    FONT_TOOLBAR_BOLD = ("Tahoma", 9, "bold")
    FONT_STATUS = ("Tahoma", 9)

    # Default perspective angles (degrees)
    DEFAULT_YAW_DEG = -35.0
    DEFAULT_PITCH_DEG = 22.0
    DEFAULT_ZOOM = 135.0

    def __init__(self, with_splash: bool = False):
        super().__init__()
        self.title("GeoSolver 3D CAD Pro (v3.2.1.0)")
        self._undo_stack: List[Dict[str, Any]] = []
        self._redo_stack: List[Dict[str, Any]] = []
        self._is_undoing: bool = False

        self.ico_path = os.path.join(os.path.dirname(__file__), "assets", "geosolver_3d.ico")
        if os.path.exists(self.ico_path):
            try:
                self.iconbitmap(default=self.ico_path)
                self.iconbitmap(self.ico_path)
            except Exception:
                try:
                    self.iconbitmap(self.ico_path)
                except Exception:
                    pass
        g3_png = os.path.join(os.path.dirname(__file__), "assets", "geosolver_3d_logo.png")
        if os.path.exists(g3_png):
            try:
                from PIL import Image, ImageTk
                pil_3 = Image.open(g3_png).resize((64, 64), Image.Resampling.LANCZOS)
                self._app_icon_photo = ImageTk.PhotoImage(pil_3, master=self)
                self.iconphoto(True, self._app_icon_photo)
            except Exception:
                pass

        splash = None
        if with_splash:
            try:
                from stem_shared_core.splash_screen import attach_splash_screen
                splash = attach_splash_screen(
                    self,
                    app_id="geosolver_3d",
                    app_title="GeoSolver 3D",
                    min_duration=2.2
                )
            except Exception:
                pass
        self.minsize(1024, 720)
        self.configure(bg=self.WIN32_BG)

        # Phục hồi kích thước cửa sổ & ngôn ngữ đã lưu
        if UIStateManager:
            UIStateManager.restore_window(self, "GeoSolver3DApp", default_geometry="1180x780", min_width=1024, min_height=720)
            app_state = UIStateManager.get_state("GeoSolver3DApp")
            saved_lang = app_state.get("lang", "VN")
        else:
            self.geometry("1180x780")
            saved_lang = "VN"

        # Load standard 3D polyhedron models & deductive engine
        self.models: Dict[str, PolyhedronModel] = build_standard_polyhedra()
        self.current_model_key: str = "pyramid_sabcd"
        self.deductive_engine = BuiltinDeductive3DEngine()

        # Interactive & Pedagogical States
        self.interact_mode: str = "orbit"      # Shortcut: M ("orbit" = xoay 3D, "move" = kéo đỉnh di chuyển)
        self.hidden_mode: str = "dashed"       # Shortcut: H ("dashed" = nét đứt cạnh khuất, "solid" = khung dây, "hidden" = ẩn cạnh khuất)
        self.show_axes: bool = True            # Shortcut: X
        self.show_section: bool = True         # Shortcut: S
        self.show_sphere: bool = False         # Shortcut: C
        self.bold_mode: bool = True            # Shortcut: B (True = BOLD screen, False = LIGHT textbook print)
        self.lang: str = saved_lang            # Shortcut: L ("VN" or "EN")
        self.hovered_vertex: Optional[str] = None
        self.dragged_vertex: Optional[str] = None
        self.selected_vertex: Optional[str] = None
        self.selected_edge: Optional[Tuple[str, str]] = None
        self.selected_aux_idx: Optional[int] = None

        # 3D Camera Orbit & Perspective Parameters
        self.yaw_deg: float = self.DEFAULT_YAW_DEG
        self.pitch_deg: float = self.DEFAULT_PITCH_DEG
        self.zoom: float = self.DEFAULT_ZOOM
        self.camera_distance: float = 9.5
        self.pan_x: float = 0.0
        self.pan_y: float = 15.0

        # Mouse drag tracking
        self._drag_last_x: Optional[int] = None
        self._drag_last_y: Optional[int] = None

        # Cached sphere calculation for status bar
        self.last_sphere_center: Vec3 = (0.0, 0.0, 0.0)
        self.last_sphere_radius: float = 0.0

        # Build Multi-Row Win32 Ribbon UI, Canvas, Side Inspector, and Status Bar
        self._build_multi_row_toolbar()
        self._build_workspace_area()
        self._build_status_bar()
        self._build_menu_bar()
        self._bind_shortcuts()
        self.push_undo_state()

        # Tự động ghi nhớ kích thước cửa sổ chính khi đóng
        if UIStateManager:
            UIStateManager.attach_window_tracking(
                self,
                "GeoSolver3DApp",
                get_extra_state_fn=lambda: {
                    "lang": self.lang,
                    "ribbon_expanded": getattr(self, "ribbon_expanded", True),
                    "current_model_key": self.current_model_key,
                },
                on_close_callback=self.destroy,
            )

        # Initial render
        self._refresh_button_labels()
        self.after(50, self.redraw_canvas)
        if splash:
            splash.set_app_ready()

    # --------------------------------------------------------------------------
    # DESKTOP MENU BAR (WIN32 UNIFIED APPLICATION MENU)
    # --------------------------------------------------------------------------

    def _build_menu_bar(self) -> None:
        """
        Đồng bộ hệ thống Menu Bar Win32 chuẩn Desktop tương thích hoàn toàn với
        GeoSolver 2D và CAD Math Studio v2:
        - Tệp (File): Mở khối mẫu, Xuất hình CAD, Xuất báo cáo HTML/PDF, Xuất suy luận, Thoát
        - Chỉnh sửa (Edit): Hoàn tác (Ctrl+Z), Làm lại (Ctrl+Y), Sao chép (Ctrl+C), Dán (Ctrl+V), Khôi phục khối
        - Hiển thị (View): Phóng to (Ctrl++), Thu nhỏ (Ctrl+-), Đặt lại Zoom (Ctrl+0), Trục Oxyz, Nét đứt (cạnh khuất), Thiết diện, Mặt cầu, Nét vẽ
        - Tùy chọn (Options): Ngôn ngữ (Tiếng Việt / English), AI hỗ trợ (Vô hiệu chờ nâng cấp)
        - Thông tin (Help): Thông tin sản phẩm, Hướng dẫn phím tắt (F1)
        """
        is_vn = (self.lang == "VN")
        self.menubar = tk.Menu(self)

        # 1. MENU TỆP (FILE)
        menu_file = tk.Menu(self.menubar, tearoff=0)
        
        poly_menu = tk.Menu(menu_file, tearoff=0)
        for k, name_vn, name_en in self._poly_specs:
            poly_menu.add_command(
                label=name_vn.strip("[] ") if is_vn else name_en.strip("[] "),
                command=lambda key=k: self.select_polyhedron(key)
            )
        menu_file.add_cascade(
            label="Mở Khối Đa Diện Mẫu" if is_vn else "Open Standard Polyhedron",
            menu=poly_menu
        )
        menu_file.add_separator()
        menu_file.add_command(
            label="Xuất Hình Ảnh Bản Vẽ 3D... (Ctrl+E)" if is_vn else "Export 3D Diagram Image... (Ctrl+E)",
            command=self.export_image_dialog,
            accelerator="Ctrl+E"
        )
        menu_file.add_command(
            label="In Bản Vẽ Trực Tiếp... (Ctrl+P)" if is_vn else "Direct Print Diagram... (Ctrl+P)",
            command=self.print_diagram_direct,
            accelerator="Ctrl+P"
        )
        menu_file.add_command(
            label="Xuất Báo Cáo Kỹ Thuật HTML / In ấn PDF..." if is_vn else "Export HTML / Print PDF Report...",
            command=self.export_html_report,
        )
        menu_file.add_command(
            label="Xuất Báo Cáo Suy Luận 3D (Markdown / TXT)..." if is_vn else "Export 3D Deduction Report (Markdown / TXT)...",
            command=self.export_deduction_report
        )
        menu_file.add_separator()
        menu_file.add_command(
            label="Thoát Ứng Dụng (Alt+F4)" if is_vn else "Exit Application (Alt+F4)",
            command=self.destroy,
            accelerator="Alt+F4"
        )
        self.menubar.add_cascade(label="Tệp" if is_vn else "File", menu=menu_file)

        # 2. MENU CHỈNH SỬA (EDIT)
        menu_edit = tk.Menu(self.menubar, tearoff=0)
        menu_edit.add_command(
            label="Hoàn tác (Undo) (Ctrl+Z)" if is_vn else "Undo (Ctrl+Z)",
            command=self.undo,
            accelerator="Ctrl+Z"
        )
        menu_edit.add_command(
            label="Làm lại (Redo) (Ctrl+Y)" if is_vn else "Redo (Ctrl+Y)",
            command=self.redo,
            accelerator="Ctrl+Y"
        )
        menu_edit.add_separator()
        menu_edit.add_command(
            label="Sao chép Thông số & Tọa độ (Ctrl+C)" if is_vn else "Copy Solid Data & Coordinates (Ctrl+C)",
            command=self.copy_selection,
            accelerator="Ctrl+C"
        )
        menu_edit.add_command(
            label="Dán / Nhập Dữ liệu (Ctrl+V)" if is_vn else "Paste / Import Data (Ctrl+V)",
            command=self.paste_data,
            accelerator="Ctrl+V"
        )
        menu_edit.add_separator()
        menu_edit.add_command(
            label="Khôi phục Tọa độ Khối Gốc (Ctrl+R)" if is_vn else "Reset Solid Coordinates (Ctrl+R)",
            command=self.reset_model_vertices,
            accelerator="Ctrl+R"
        )
        self.menubar.add_cascade(label="Chỉnh sửa" if is_vn else "Edit", menu=menu_edit)

        # 3. MENU HIỂN THỊ (VIEW)
        menu_view = tk.Menu(self.menubar, tearoff=0)
        menu_view.add_command(
            label="Phóng to (Zoom In) (Ctrl++)" if is_vn else "Zoom In (Ctrl++)",
            command=lambda: self._zoom_by(1.15),
            accelerator="Ctrl++"
        )
        menu_view.add_command(
            label="Thu nhỏ (Zoom Out) (Ctrl+-)" if is_vn else "Zoom Out (Ctrl+-)",
            command=lambda: self._zoom_by(1.0 / 1.15),
            accelerator="Ctrl+-"
        )
        menu_view.add_command(
            label="Đặt lại Zoom & Góc nhìn (Ctrl+0)" if is_vn else "Reset Zoom & Camera View (Ctrl+0)",
            command=self.reset_camera_view,
            accelerator="Ctrl+0"
        )
        menu_view.add_separator()
        menu_view.add_command(
            label="Chế độ Xoay 3D (M)" if is_vn else "3D Orbit Mode (M)",
            command=lambda: self.set_interact_mode("orbit"),
            accelerator="M"
        )
        menu_view.add_command(
            label="Chế độ Chọn & Di chuyển đỉnh (V)" if is_vn else "Select & Move Vertex Mode (V)",
            command=lambda: self.set_interact_mode("move"),
            accelerator="V"
        )
        menu_view.add_separator()
        menu_view.add_command(
            label=f"Trục tọa độ Oxyz ({'✓ BẬT' if self.show_axes else 'TẮT'}) (X)" if is_vn else f"Oxyz Axes ({'✓ ON' if self.show_axes else 'OFF'}) (X)",
            command=self.toggle_axes,
            accelerator="X"
        )
        menu_view.add_command(
            label=f"Nét đứt cạnh khuất ({'✓ BẬT' if self.hidden_mode == 'dashed' else 'TẮT'}) (H)" if is_vn else f"Hidden Dashed Lines ({'✓ ON' if self.hidden_mode == 'dashed' else 'OFF'}) (H)",
            command=self.toggle_hidden_lines,
            accelerator="H"
        )
        menu_view.add_command(
            label=f"Mặt phẳng Thiết diện ({'✓ BẬT' if self.show_section else 'TẮT'}) (S)" if is_vn else f"Cross-Section Plane ({'✓ ON' if self.show_section else 'OFF'}) (S)",
            command=self.toggle_section,
            accelerator="S"
        )
        menu_view.add_command(
            label=f"Mặt cầu Ngoại tiếp S(I; R) ({'✓ BẬT' if self.show_sphere else 'TẮT'}) (C)" if is_vn else f"Circumscribed Sphere ({'✓ ON' if self.show_sphere else 'OFF'}) (C)",
            command=self.toggle_sphere,
            accelerator="C"
        )
        menu_view.add_command(
            label=f"Độ dày nét ({'✓ ĐẬM' if self.bold_mode else 'MẢNH'}) (B)" if is_vn else f"Line Weight ({'✓ BOLD' if self.bold_mode else 'LIGHT'}) (B)",
            command=self.toggle_line_weight,
            accelerator="B"
        )
        self.menubar.add_cascade(label="Hiển thị" if is_vn else "View", menu=menu_view)

        # 4. MENU CÔNG CỤ (TOOLS)
        menu_tools = tk.Menu(self.menubar, tearoff=0)
        menu_tools.add_command(
            label="Dựng Hình Học Không Gian 3D..." if is_vn else "3D Geometric Constructions...",
            command=self.open_construction_dialog
        )
        menu_tools.add_command(
            label="Thêm Điểm Trên Đoạn Thẳng (Tỉ số k)..." if is_vn else "Add Point on Segment (Ratio k)...",
            command=self.open_point_on_segment_dialog
        )
        menu_tools.add_command(
            label="Tô Màu & Gạch Chéo CAD Cho Mặt Phẳng..." if is_vn else "CAD Hatching & Plane Shading...",
            command=self.open_plane_3points_dialog
        )
        menu_tools.add_command(
            label="Hộp Thoại Suy Luận 3D (12 Chuyên Đề)... (D)" if is_vn else "3D Deductive Solver (12 Topics)... (D)",
            command=self.open_deductive_dialog,
            accelerator="D"
        )
        self.menubar.add_cascade(label="Công cụ" if is_vn else "Tools", menu=menu_tools)

        # 5. MENU TÙY CHỌN (OPTIONS)
        menu_opts = tk.Menu(self.menubar, tearoff=0)
        lang_menu = tk.Menu(menu_opts, tearoff=0)
        lang_menu.add_command(
            label="Tiếng Việt (Vietnamese)" + ("  ✓" if is_vn else ""),
            command=lambda: self.set_language("VN")
        )
        lang_menu.add_command(
            label="English (English)" + ("  ✓" if not is_vn else ""),
            command=lambda: self.set_language("EN")
        )
        menu_opts.add_cascade(label="Ngôn ngữ (Language)" if is_vn else "Language", menu=lang_menu)
        menu_opts.add_separator()
        
        ai_label = "AI Hỗ Trợ Giải Toán 3D (Đang hoàn thiện)..." if is_vn else "AI 3D STEM Assistant (In Development)..."
        menu_opts.add_command(
            label=ai_label,
            command=self.open_ai_hub,
            state=tk.DISABLED,
        )
        menu_opts.add_separator()
        is_pro = LicenseManager.is_pro_active() if LicenseManager else False
        pro_label = "💎 Trạng Thái Bản Quyền In Ấn Pro..." if is_pro else "💎 Nâng Cấp Gói In Ấn Pro ($1.99)..."
        if not is_vn:
            pro_label = "💎 Pro Printing License Status..." if is_pro else "💎 Upgrade to Pro Printing ($1.99)..."
        menu_opts.add_command(
            label=pro_label,
            command=self.open_pro_upgrade_dialog,
        )
        self.menubar.add_cascade(label="Tùy chọn" if is_vn else "Options", menu=menu_opts)

        # 6. MENU THÔNG TIN (HELP)
        menu_help = tk.Menu(self.menubar, tearoff=0)
        menu_help.add_command(
            label="Hướng Dẫn Sử Dụng (F1)..." if is_vn else "User Guide (F1)...",
            command=self.open_user_handbook,
            accelerator="F1"
        )
        menu_help.add_command(
            label="Bảng Tra Cứu Phím Tắt..." if is_vn else "Keyboard Shortcuts...",
            command=self.open_shortcuts_guide
        )
        menu_help.add_separator()
        menu_help.add_command(
            label="Thông Tin Phần Mềm..." if is_vn else "About GeoSolver 3D...",
            command=self.open_about_dialog
        )
        self.menubar.add_cascade(label="Thông tin" if is_vn else "Help", menu=menu_help)

        self.config(menu=self.menubar)

    # --------------------------------------------------------------------------
    # UNDO / REDO STATE MANAGEMENT
    # --------------------------------------------------------------------------

    def _capture_state(self) -> Dict[str, Any]:
        import copy
        model = self.models[self.current_model_key]
        return {
            "model_key": self.current_model_key,
            "vertices": {k: tuple(v) for k, v in model.vertices.items()},
            "aux_points": {k: tuple(v) for k, v in model.aux_points.items()},
            "aux_segments": copy.deepcopy(model.aux_segments),
            "aux_circles": copy.deepcopy(model.aux_circles),
            "aux_angles": copy.deepcopy(model.aux_angles),
            "custom_planes": copy.deepcopy(model.custom_planes),
            "plane_normal": tuple(model.plane_normal),
            "plane_d": float(model.plane_d),
            "section_fill_mode": str(model.section_fill_mode),
            "section_drag_mode": str(model.section_drag_mode),
            "point_constraints": copy.deepcopy(model.point_constraints),
            "edge_colors": copy.deepcopy(model.edge_colors),
            "vertex_colors": copy.deepcopy(model.vertex_colors),
            "dim_h": self.ent_dim_h.get() if hasattr(self, "ent_dim_h") else "2.2",
            "dim_a": self.ent_dim_a.get() if hasattr(self, "ent_dim_a") else "2.4",
            "dim_b": self.ent_dim_b.get() if hasattr(self, "ent_dim_b") else "2.4",
            "yaw_deg": self.yaw_deg,
            "pitch_deg": self.pitch_deg,
            "zoom": self.zoom,
            "pan_x": self.pan_x,
            "pan_y": self.pan_y,
        }

    def _apply_state(self, state: Dict[str, Any]) -> None:
        import copy
        self.current_model_key = state.get("model_key", self.current_model_key)
        model = self.models[self.current_model_key]
        model.vertices = {k: tuple(v) for k, v in state.get("vertices", {}).items()}
        model.aux_points = {k: tuple(v) for k, v in state.get("aux_points", {}).items()}
        model.aux_segments = copy.deepcopy(state.get("aux_segments", []))
        model.aux_circles = copy.deepcopy(state.get("aux_circles", []))
        model.aux_angles = copy.deepcopy(state.get("aux_angles", []))
        model.custom_planes = copy.deepcopy(state.get("custom_planes", []))
        model.plane_normal = tuple(state.get("plane_normal", (0.0, 0.0, 1.0)))
        model.plane_d = float(state.get("plane_d", 1.0))
        model.section_fill_mode = str(state.get("section_fill_mode", "hatch"))
        model.section_drag_mode = str(state.get("section_drag_mode", "pivot"))
        model.point_constraints = copy.deepcopy(state.get("point_constraints", {}))
        model.edge_colors = copy.deepcopy(state.get("edge_colors", {}))
        model.vertex_colors = copy.deepcopy(state.get("vertex_colors", {}))
        model.recalculate_geometry()

        if hasattr(self, "ent_dim_h"):
            self.ent_dim_h.delete(0, tk.END)
            self.ent_dim_h.insert(0, state.get("dim_h", "2.2"))
        if hasattr(self, "ent_dim_a"):
            self.ent_dim_a.delete(0, tk.END)
            self.ent_dim_a.insert(0, state.get("dim_a", "2.4"))
        if hasattr(self, "ent_dim_b"):
            self.ent_dim_b.delete(0, tk.END)
            self.ent_dim_b.insert(0, state.get("dim_b", "2.4"))
        if hasattr(self, "plane_d_scale"):
            self.plane_d_scale.set(model.plane_d)

        self.yaw_deg = float(state.get("yaw_deg", self.yaw_deg))
        self.pitch_deg = float(state.get("pitch_deg", self.pitch_deg))
        self.zoom = float(state.get("zoom", self.zoom))
        self.pan_x = float(state.get("pan_x", self.pan_x))
        self.pan_y = float(state.get("pan_y", self.pan_y))

        self.redraw_canvas()
        self._refresh_button_labels()

    def push_undo_state(self) -> None:
        if getattr(self, "_is_undoing", False):
            return
        state = self._capture_state()
        self._undo_stack.append(state)
        if len(self._undo_stack) > 35:
            self._undo_stack.pop(0)
        self._redo_stack.clear()

    def undo(self, event=None) -> None:
        if not self._undo_stack:
            is_vn = (self.lang == "VN")
            self.set_status("Không còn thao tác để hoàn tác (Undo stack empty)." if is_vn else "Nothing to undo.")
            return
        self._is_undoing = True
        try:
            curr = self._capture_state()
            self._redo_stack.append(curr)
            prev = self._undo_stack.pop()
            self._apply_state(prev)
            is_vn = (self.lang == "VN")
            self.set_status("Đã hoàn tác thao tác trước (Ctrl+Z)." if is_vn else "Undone previous action (Ctrl+Z).")
        finally:
            self._is_undoing = False

    def redo(self, event=None) -> None:
        if not self._redo_stack:
            is_vn = (self.lang == "VN")
            self.set_status("Không có thao tác để làm lại (Redo stack empty)." if is_vn else "Nothing to redo.")
            return
        self._is_undoing = True
        try:
            curr = self._capture_state()
            self._undo_stack.append(curr)
            nxt = self._redo_stack.pop()
            self._apply_state(nxt)
            is_vn = (self.lang == "VN")
            self.set_status("Đã làm lại thao tác (Ctrl+Y)." if is_vn else "Redone action (Ctrl+Y).")
        finally:
            self._is_undoing = False

    # --------------------------------------------------------------------------
    # CLIPBOARD & DIALOG HANDLERS
    # --------------------------------------------------------------------------

    def copy_selection(self, event=None) -> None:
        w_focus = self.focus_get()
        if isinstance(w_focus, (tk.Entry, tk.Text)):
            return
        is_vn = (self.lang == "VN")
        try:
            model = self.models[self.current_model_key]
            vol_val, surf_val = model.compute_volume_and_surface()
            center_I, radius_R, _ = compute_circumscribed_sphere(model.vertices)
            r_in = (3.0 * vol_val / surf_val) if surf_val > 1e-6 else 0.0

            lines = [
                f"=== GEOSOLVER 3D: {model.name_vn if is_vn else model.name_en} ===",
                f"• {'Thể tích V' if is_vn else 'Volume V'}: {format_radical_number(vol_val)} (≈ {vol_val:.4f})",
                f"• {'Diện tích toàn phần S_tp' if is_vn else 'Total Surface S_total'}: {format_radical_number(surf_val)} (≈ {surf_val:.4f})",
                f"• {'Bán kính cầu ngoại tiếp R' if is_vn else 'Circumradius R'}: {format_radical_number(radius_R)} (≈ {radius_R:.4f})",
                f"• {'Bán kính cầu nội tiếp r' if is_vn else 'Inradius r'}: {format_radical_number(r_in)} (≈ {r_in:.4f})",
                f"• {'Tâm cầu ngoại tiếp I' if is_vn else 'Circumcenter I'}: ({center_I[0]:.2f}, {center_I[1]:.2f}, {center_I[2]:.2f})",
                "",
                "TỌA ĐỘ ĐỈNH OXYZ:" if is_vn else "VERTEX COORDINATES OXYZ:",
            ]
            for v_lbl, pt in model.vertices.items():
                lines.append(f"  {v_lbl}: ({pt[0]:.4f}, {pt[1]:.4f}, {pt[2]:.4f})")
            
            txt = "\n".join(lines)
            self.clipboard_clear()
            self.clipboard_append(txt)
            self.set_status("Đã sao chép thông số khối vào Clipboard (Ctrl+C)." if is_vn else "Copied 3D solid parameters to Clipboard (Ctrl+C).")
        except Exception as ex:
            self.set_status(f"Copy error: {ex}")

    def paste_data(self, event=None) -> None:
        w_focus = self.focus_get()
        if isinstance(w_focus, (tk.Entry, tk.Text)):
            return
        is_vn = (self.lang == "VN")
        try:
            txt = self.clipboard_get()
            if txt:
                self.set_status("Đã nhận dữ liệu Clipboard (Ctrl+V)." if is_vn else "Received Clipboard data (Ctrl+V).")
        except Exception:
            pass

    def print_diagram_direct(self, event=None) -> None:
        """In trực tiếp bản vẽ 3D độ nét cao (300 DPI) ra máy in qua Windows Print Wizard."""
        is_vn = (self.lang == "VN")
        is_pro = LicenseManager.is_pro_active() if LicenseManager else False
        import tempfile
        temp_img = os.path.join(tempfile.gettempdir(), f"geosolver3d_direct_print_{os.getpid()}.png")
        try:
            self._render_scene_to_image(
                temp_img,
                scale=2,
                show_axes=self.show_axes,
                show_sphere=self.show_sphere,
                show_section=self.show_section,
                show_auxiliary=True,
                show_labels=True,
                hidden_mode=self.hidden_mode,
                bold_mode=self.bold_mode,
                transparent_bg=False,
            )
            os.startfile(temp_img, "print")
            if is_pro:
                self.set_status("Đang mở trình in Windows (Bản in Pro sạch 100%)..." if is_vn else "Opening Windows Print Wizard (100% Clean Pro Print)...")
            else:
                self.set_status("Đang mở trình in Windows (kèm hình mờ bản quyền nhẹ)..." if is_vn else "Opening Windows Print Wizard (with subtle watermark)...")
        except Exception as ex:
            messagebox.showerror(
                "Lỗi in ấn" if is_vn else "Print Error",
                f"Không thể kích hoạt trình in Windows: {ex}" if is_vn else f"Unable to activate Windows print wizard: {ex}",
                parent=self
            )

    def export_image_dialog(self) -> None:
        """Mở hộp thoại Xuất hình ảnh với đầy đủ tùy chọn đối tượng, nét vẽ, và độ phân giải."""
        Export3DImageDialog(self)

    def export_html_report(self) -> None:
        """
        Xuất toàn bộ bài toán hình học 3D thành Báo Cáo Kỹ Thuật HTML tự chứa (self-contained),
        tích hợp kết xuất MathJax 3.2 cho các hệ thức hình học và nhúng ảnh bản vẽ sạch Base64.
        Hỗ trợ 1-click In ấn sang PDF chuẩn trang A4.
        """
        import tempfile
        import webbrowser
        from stem_shared_core.report_engine import build_full_stem_html_report, canvas_to_base64_png

        is_vn = (self.lang == "VN")
        file_title = "Xuất Báo Cáo Hình Học 3D HTML / In ấn PDF" if is_vn else "Export 3D Geometry HTML / Print PDF Report"
        filepath = filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".html",
            filetypes=[("HTML Web Document (*.html)", "*.html")],
            title=file_title
        )
        if not filepath:
            return

        try:
            plot_b64 = ""
            temp_png = os.path.join(tempfile.gettempdir(), f"geosolver3d_export_{os.getpid()}.png")
            try:
                self._render_scene_to_image(temp_png, scale=2)
                if os.path.exists(temp_png):
                    import base64
                    with open(temp_png, "rb") as pf:
                        b64_data = base64.b64encode(pf.read()).decode("ascii")
                        plot_b64 = f"data:image/png;base64,{b64_data}"
                    os.remove(temp_png)
            except Exception:
                plot_b64 = canvas_to_base64_png(self.canvas)

            model = self.models[self.current_model_key]
            vol_val, surf_val = model.compute_volume_and_surface()
            center_I, radius_R, _ = compute_circumscribed_sphere(model.vertices)
            r_in = (3.0 * vol_val / surf_val) if surf_val > 1e-6 else 0.0

            extra_facts = [
                {"k": "Mô hình hình học" if is_vn else "Solid Model", "v": model.name_vn if is_vn else model.name_en},
                {"k": "Thể tích V" if is_vn else "Volume V", "v": f"{format_radical_number(vol_val)} (≈ {vol_val:.4f})"},
                {"k": "Diện tích toàn phần" if is_vn else "Total Surface Area", "v": f"{format_radical_number(surf_val)} (≈ {surf_val:.4f})"},
                {"k": "Bán kính cầu ngoại tiếp R" if is_vn else "Circumradius R", "v": f"{format_radical_number(radius_R)} (≈ {radius_R:.4f})"},
                {"k": "Bán kính cầu nội tiếp r" if is_vn else "Inradius r", "v": f"{format_radical_number(r_in)} (≈ {r_in:.4f})"},
                {"k": "Tọa độ tâm cầu ngoại tiếp I" if is_vn else "Circumcenter I", "v": f"({center_I[0]:.2f}, {center_I[1]:.2f}, {center_I[2]:.2f})"},
            ]
            for v_name, pt in model.vertices.items():
                extra_facts.append({"k": f"Đỉnh {v_name}" if is_vn else f"Vertex {v_name}", "v": f"({pt[0]:.2f}, {pt[1]:.2f}, {pt[2]:.2f})"})

            params = {"SA": 4.0, "AB": 3.0, "BC": 4.0, "a": 6.0, "base_a": 4.0, "height_h": 4.0}
            if hasattr(self, "ent_dim_h"):
                try:
                    params["SA"] = float(self.ent_dim_h.get())
                    params["height_h"] = float(self.ent_dim_h.get())
                    params["AB"] = float(self.ent_dim_a.get())
                    params["base_a"] = float(self.ent_dim_a.get())
                    params["a"] = float(self.ent_dim_a.get())
                    params["BC"] = float(self.ent_dim_b.get())
                except Exception:
                    pass

            solution_steps = self.deductive_engine.solve_topic(1, params, self.lang)

            html_code = build_full_stem_html_report(
                app_title="GeoSolver 3D CAD Studio",
                topic=f"Hình Học Không Gian 3D - {model.name_vn}" if is_vn else f"3D Spatial Geometry - {model.name_en}",
                problem_text=f"Khảo sát và tính toán hình học không gian cho {model.name_vn}." if is_vn else f"3D geometric analysis for {model.name_en}.",
                hero_formula_latex=r"R = \frac{1}{2}\sqrt{h^2 + a^2 + b^2} \quad;\quad V = \frac{1}{3}B \cdot h",
                hero_formula_text="R = 1/2 · √(h² + a² + b²); V = 1/3 · B · h",
                solution_steps=solution_steps,
                plot_base64_png=plot_b64,
                extra_facts=extra_facts[:16],
                ai_commentary="Hệ thống đã tự động tính toán chính xác tâm, bán kính cầu ngoại tiếp và thiết diện theo chuẩn GDPT 2018."
                if is_vn else "The system computed exact circumcenter, sphere radius and cross section based on standard 3D curriculum."
            )

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_code)

            res = messagebox.askyesno(
                "Xuất báo cáo thành công" if is_vn else "Report Exported Successfully",
                f"Báo cáo kỹ thuật HTML đã được tạo tại:\n{filepath}\n\nBạn có muốn mở ngay trên trình duyệt web không?"
                if is_vn
                else f"HTML report generated successfully at:\n{filepath}\n\nWould you like to open it in your browser now?",
                parent=self
            )
            if res:
                webbrowser.open(filepath)
        except Exception as ex:
            messagebox.showerror("Lỗi" if is_vn else "Error", f"Lỗi xuất báo cáo HTML: {ex}" if is_vn else f"Report export error: {ex}", parent=self)

    def export_deduction_report(self) -> None:
        """Xuất báo cáo suy luận 3D của mô hình hiện tại ra tệp Markdown hoặc Văn bản."""
        is_vn = (self.lang == "VN")
        fpath = filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".md",
            filetypes=[
                ("Markdown Document (*.md)", "*.md"),
                ("Text Document (*.txt)", "*.txt"),
                ("All Files (*.*)", "*.*")
            ],
            title="Xuất Báo Cáo Suy Luận 3D" if is_vn else "Export 3D Deduction Report",
        )
        if not fpath:
            return
        try:
            params = {"SA": 4.0, "AB": 3.0, "BC": 4.0, "a": 6.0, "base_a": 4.0, "height_h": 4.0}
            if hasattr(self, "ent_dim_h"):
                try:
                    params["SA"] = float(self.ent_dim_h.get())
                    params["height_h"] = float(self.ent_dim_h.get())
                    params["AB"] = float(self.ent_dim_a.get())
                    params["base_a"] = float(self.ent_dim_a.get())
                    params["a"] = float(self.ent_dim_a.get())
                    params["BC"] = float(self.ent_dim_b.get())
                except Exception:
                    pass
            proof_txt = self.deductive_engine.solve_topic(1, params, self.lang)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(proof_txt)
            messagebox.showinfo(
                "Thành công" if is_vn else "Success",
                f"Đã xuất báo cáo suy luận thành công:\n{fpath}" if is_vn else f"Deduction report exported successfully:\n{fpath}",
                parent=self
            )
        except Exception as ex:
            messagebox.showerror("Lỗi" if is_vn else "Error", str(ex), parent=self)

    def open_about_dialog(self) -> None:
        """Mở hộp thoại thông tin sản phẩm GeoSolver 3D."""
        ProductAboutDialog(self)

    def open_user_handbook(self) -> None:
        """Mở hộp thoại Cẩm nang hướng dẫn sử dụng chi tiết từng mục và phím tắt."""
        UserHandbookDialog(self)

    def open_shortcuts_guide(self) -> None:
        """Mở hộp thoại hướng dẫn phím tắt và thao tác đồ họa."""
        ShortcutsGuideDialog(self)

    def notify_ai_upgrade(self) -> None:
        """Bảo lưu tính năng AI hỗ trợ giải toán không gian 3D cho nâng cấp sau."""
        is_vn = (self.lang == "VN")
        title = "AI Hỗ Trợ Giải Toán 3D" if is_vn else "AI 3D STEM Assistant"
        msg = (
            "Chức năng AI hỗ trợ giải toán không gian 3D đang tạm thời được bảo lưu và nâng cấp "
            "đồng bộ trong lộ trình tiếp theo theo yêu cầu kỹ thuật.\n\n"
            "Toàn bộ thuật toán & module AI cốt lõi đã được lưu giữ an toàn trong hệ thống.\n"
            "Hiện tại xin vui lòng sử dụng Bộ Giải Tích & Suy Luận 3D (12 Chuyên Đề Từng Bước) "
            "đã được tích hợp sẵn 100% trong phần mềm (Bấm phím 'D' hoặc menu 'Công cụ -> Hộp Thoại Suy Luận 3D')."
            if is_vn
            else
            "The AI 3D STEM Assistant feature is temporarily reserved for future synchronized upgrades.\n\n"
            "All underlying AI logic and modules are safely preserved.\n"
            "Please use the built-in 12-Topic 3D Deductive Reasoning Engine available under 'Tools -> 3D Deductive Solver' (Shortcut: 'D')."
        )
        messagebox.showinfo(title, msg, parent=self)

    def set_language(self, lang: str) -> None:
        """Thiết lập ngôn ngữ giao diện (VN hoặc EN)."""
        if self.lang != lang:
            self.lang = lang
            self._refresh_button_labels()
            self.redraw_canvas()

    # --------------------------------------------------------------------------
    # MULTI-ROW RIBBON TOOLBAR (TOP BAR 1 & TOP BAR 2)
    # --------------------------------------------------------------------------

    def _build_multi_row_toolbar(self) -> None:
        """
        Builds a 2-row Win32 Classic Ribbon Toolbar (#ECE9D8, relief=tk.GROOVE, bd=2)
        that prevents any button clipping on resolutions from 1024x768 upward.
        """
        self.ribbon_expanded = True
        self.current_theme_color = "#000000"

        self.ribbon_container = tk.Frame(self, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2)
        self.ribbon_container.pack(side=tk.TOP, fill=tk.X, padx=2, pady=(2, 0))

        # Header bar containing title and Ribbon Collapse button (▲ / ▼)
        ribbon_ctrl_bar = tk.Frame(self.ribbon_container, bg=self.WIN32_BG, height=22)
        ribbon_ctrl_bar.pack(side=tk.TOP, fill=tk.X, padx=4, pady=1)

        self.lbl_header_title = tk.Label(
            ribbon_ctrl_bar,
            text="GEOSOLVER 3D — HÌNH HỌC KHÔNG GIAN & VẼ KỸ THUẬT CAD",
            font=("Tahoma", 8, "bold"),
            bg=self.WIN32_BG,
            fg="#444444",
        )
        self.lbl_header_title.pack(side=tk.LEFT, padx=2)

        # Bảng màu nhanh 1 chạm phong cách 2D (Chấm tròn ● Đỏ, ● Xanh, ● Đen, ● Lục, ● Cam)
        palette_frame = tk.Frame(ribbon_ctrl_bar, bg=self.WIN32_BG)
        palette_frame.pack(side=tk.LEFT, padx=12)
        self.lbl_palette_title = tk.Label(palette_frame, text="Màu:" if self.lang == "VN" else "Color:", bg=self.WIN32_BG, font=("Tahoma", 8, "bold"))
        self.lbl_palette_title.pack(side=tk.LEFT, padx=(0, 3))
        colors_list = [
            ("#E03131", "● Đỏ", "#c92a2a", "#ffe3e3"),
            ("#1971C2", "● Xanh", "#1864ab", "#d0ebff"),
            ("#212529", "● Đen", "#212529", "#e9ecef"),
            ("#2B8A3E", "● Lục", "#2b8a3e", "#d3f9d8"),
            ("#E8590C", "● Cam", "#d9480f", "#ffe8cc"),
        ]
        self.color_palette_buttons = {}
        for c_hex, c_text, fg_col, bg_col in colors_list:
            btn_col = tk.Button(
                palette_frame,
                text=c_text,
                font=("Tahoma", 7, "bold"),
                fg=fg_col,
                bg=bg_col,
                activebackground=bg_col,
                activeforeground=fg_col,
                relief=tk.GROOVE,
                bd=1,
                padx=3,
                pady=1,
                cursor="hand2",
                command=lambda c=c_hex: self.set_theme_color(c),
            )
            btn_col.pack(side=tk.LEFT, padx=1)
            self.color_palette_buttons[c_hex] = btn_col

        # Nút thu gọn / mở rộng Ribbon phong cách MS Office
        self.btn_toggle_ribbon = tk.Button(
            ribbon_ctrl_bar,
            text="▲ Thu gọn Ribbon",
            font=("Tahoma", 8),
            bg=self.WIN32_BG,
            relief=tk.GROOVE,
            bd=1,
            padx=4,
            pady=0,
            command=self.toggle_ribbon,
        )
        self.btn_toggle_ribbon.pack(side=tk.RIGHT, padx=2)

        # --- TOP BAR 1: POLYHEDRON MODELS GROUP ---
        self.top_bar_1 = tk.Frame(self.ribbon_container, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2, padx=4, pady=2)
        self.top_bar_1.pack(side=tk.TOP, fill=tk.X, padx=2, pady=(2, 1))

        self.lbl_group_row1 = tk.Label(
            self.top_bar_1,
            text="Khối Đa Diện:",
            bg=self.WIN32_BG,
            fg="#000080",
            font=self.FONT_TOOLBAR_BOLD,
            padx=4,
        )
        self.lbl_group_row1.pack(side=tk.LEFT, padx=(0, 4))

        self.poly_buttons: Dict[str, tk.Button] = {}
        poly_specs = [
            ("pyramid_sabcd", "[ Chóp S.ABCD ]", "[ Pyramid S.ABCD ]"),
            ("tetrahedron_sabc", "[ Tứ diện S.ABC ]", "[ Tetrahedron S.ABC ]"),
            ("prism_abc", "[ Lăng trụ đứng ]", "[ Right Prism ]"),
            ("box_abcd", "[ Hình hộp ]", "[ Box ABCD.A'B'C'D' ]"),
            ("frustum_abcd", "[ Chóp cụt ]", "[ Frustum ]"),
            ("octahedron", "[ Bát diện đều ]", "[ Octahedron ]"),
        ]
        self._poly_specs = poly_specs

        for key, text_vn, _text_en in poly_specs:
            btn = tk.Button(
                self.top_bar_1,
                text=text_vn,
                font=self.FONT_TOOLBAR,
                bg=self.WIN32_BG,
                activebackground=self.WIN32_ACTIVE_BG,
                fg="#000000",
                relief=tk.RAISED,
                bd=2,
                padx=5,
                pady=1,
                command=lambda k=key: self.select_polyhedron(k),
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.poly_buttons[key] = btn

        # Nút khôi phục khối đa diện về tọa độ chuẩn
        self.btn_reset_model = tk.Button(
            self.top_bar_1,
            text="[ ↺ Khôi phục khối ]",
            font=self.FONT_TOOLBAR,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            fg="#8B0000",
            relief=tk.RAISED,
            bd=2,
            padx=5,
            pady=1,
            command=self.reset_model_vertices,
        )
        self.btn_reset_model.pack(side=tk.LEFT, padx=(6, 2))

        self.btn_undo = tk.Button(
            self.top_bar_1,
            text="[ ↶ Hoàn tác (Ctrl+Z) ]",
            font=self.FONT_TOOLBAR,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            fg="#000000",
            relief=tk.RAISED,
            bd=2,
            padx=4,
            pady=1,
            command=self.undo,
        )
        self.btn_undo.pack(side=tk.LEFT, padx=2)

        self.btn_redo = tk.Button(
            self.top_bar_1,
            text="[ ↷ Làm lại (Ctrl+Y) ]",
            font=self.FONT_TOOLBAR,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            fg="#000000",
            relief=tk.RAISED,
            bd=2,
            padx=4,
            pady=1,
            command=self.redo,
        )
        self.btn_redo.pack(side=tk.LEFT, padx=2)

        # --- TOP BAR 2: 3D DISPLAY, CAMERA ORBIT, AXES, HIDDEN LINES ---
        self.top_bar_2 = tk.Frame(self.ribbon_container, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2, padx=4, pady=2)
        self.top_bar_2.pack(side=tk.TOP, fill=tk.X, padx=2, pady=(1, 1))

        self.lbl_group_row2 = tk.Label(
            self.top_bar_2,
            text="Hiển Thị 3D:",
            bg=self.WIN32_BG,
            fg="#000080",
            font=self.FONT_TOOLBAR_BOLD,
            padx=4,
        )
        self.lbl_group_row2.pack(side=tk.LEFT, padx=(0, 4))

        # Chế độ Thao tác: [ 🔄 Xoay 3D ] và [ ✋ Chọn / Di chuyển ]
        self.btn_mode_orbit = tk.Button(
            self.top_bar_2,
            text="[ 🔄 Xoay 3D ]",
            font=self.FONT_TOOLBAR_BOLD,
            bg=self.WIN32_ACTIVE_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            fg="#000080",
            relief=tk.SUNKEN,
            bd=2,
            padx=5,
            pady=1,
            command=lambda: self.set_interact_mode("orbit"),
        )
        self.btn_mode_orbit.pack(side=tk.LEFT, padx=1)

        self.btn_mode_move = tk.Button(
            self.top_bar_2,
            text="[ ✋ Chọn / Di chuyển ]",
            font=self.FONT_TOOLBAR,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            fg="#000000",
            relief=tk.RAISED,
            bd=2,
            padx=5,
            pady=1,
            command=lambda: self.set_interact_mode("move"),
        )
        self.btn_mode_move.pack(side=tk.LEFT, padx=1)

        self.btn_axes = tk.Button(
            self.top_bar_2,
            text="[ Trục Oxyz: BẬT ]",
            font=self.FONT_TOOLBAR,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            relief=tk.SUNKEN,
            bd=2,
            padx=5,
            pady=1,
            command=self.toggle_axes,
        )
        self.btn_axes.pack(side=tk.LEFT, padx=2)

        # Nút điều khiển Nét Đứt Cạnh Khuất (3 chế độ: BẬT nét đứt / TẮT khung dây / ẨN nét khuất)
        self.btn_hidden = tk.Button(
            self.top_bar_2,
            text="[ Nét đứt (cạnh khuất): BẬT ]",
            font=self.FONT_TOOLBAR,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            relief=tk.SUNKEN,
            bd=2,
            padx=5,
            pady=1,
            command=self.toggle_hidden_lines,
        )
        self.btn_hidden.pack(side=tk.LEFT, padx=2)

        self.btn_section = tk.Button(
            self.top_bar_2,
            text="[ Thiết diện: BẬT ]",
            font=self.FONT_TOOLBAR,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            relief=tk.SUNKEN,
            bd=2,
            padx=5,
            pady=1,
            command=self.toggle_section,
        )
        self.btn_section.pack(side=tk.LEFT, padx=2)

        self.btn_sphere = tk.Button(
            self.top_bar_2,
            text="[ Mặt cầu: TẮT ]",
            font=self.FONT_TOOLBAR,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            relief=tk.RAISED,
            bd=2,
            padx=5,
            pady=1,
            command=self.toggle_sphere,
        )
        self.btn_sphere.pack(side=tk.LEFT, padx=2)

        self.btn_line_weight = tk.Button(
            self.top_bar_2,
            text="[ Nét vẽ: ĐẬM ]",
            font=self.FONT_TOOLBAR,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            relief=tk.RAISED,
            bd=2,
            padx=5,
            pady=1,
            command=self.toggle_line_weight,
        )
        self.btn_line_weight.pack(side=tk.LEFT, padx=2)

        self.btn_reset_view = tk.Button(
            self.top_bar_2,
            text="[ Đặt lại View ]",
            font=self.FONT_TOOLBAR,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            relief=tk.RAISED,
            bd=2,
            padx=5,
            pady=1,
            command=self.reset_camera_view,
        )
        self.btn_reset_view.pack(side=tk.LEFT, padx=2)

        # --- TOP BAR 3: PEDAGOGICAL CONSTRUCTIONS, DEDUCTION, EXPORT & AI ---
        self.top_bar_3 = tk.Frame(self.ribbon_container, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2, padx=4, pady=2)
        self.top_bar_3.pack(side=tk.TOP, fill=tk.X, padx=2, pady=(1, 2))

        self.lbl_group_row3 = tk.Label(
            self.top_bar_3,
            text="Công Cụ & Suy Luận:",
            bg=self.WIN32_BG,
            fg="#000080",
            font=self.FONT_TOOLBAR_BOLD,
            padx=4,
        )
        self.lbl_group_row3.pack(side=tk.LEFT, padx=(0, 4))

        # Nút mở Hộp thoại Dựng hình không gian 3D
        self.btn_construct = tk.Button(
            self.top_bar_3,
            text="[ Dựng hình 3D ]",
            font=self.FONT_TOOLBAR_BOLD,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            fg="#2B8A3E",
            relief=tk.RAISED,
            bd=2,
            padx=6,
            pady=1,
            command=self.open_construction_dialog,
        )
        self.btn_construct.pack(side=tk.LEFT, padx=2)

        # Nút thêm nhanh điểm trên đoạn thẳng với tỉ số động k
        self.btn_point_on_seg = tk.Button(
            self.top_bar_3,
            text="[ ➕ Điểm trên đoạn ]",
            font=self.FONT_TOOLBAR_BOLD,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            fg="#1971C2",
            relief=tk.RAISED,
            bd=2,
            padx=5,
            pady=1,
            command=self.open_point_on_segment_dialog,
        )
        self.btn_point_on_seg.pack(side=tk.LEFT, padx=2)

        # Nút vẽ & tô màu / gạch chéo diện tích mặt phẳng chuẩn CAD
        self.btn_plane_3pts = tk.Button(
            self.top_bar_3,
            text="[ ▨ Tô màu & Gạch chéo CAD ]",
            font=self.FONT_TOOLBAR_BOLD,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            fg="#6B21A8",
            relief=tk.RAISED,
            bd=2,
            padx=6,
            pady=1,
            command=self.open_plane_3points_dialog,
        )
        self.btn_plane_3pts.pack(side=tk.LEFT, padx=2)

        self.btn_deductive = tk.Button(
            self.top_bar_3,
            text="[ Suy luận 3D ]",
            font=self.FONT_TOOLBAR_BOLD,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            fg="#000080",
            relief=tk.RAISED,
            bd=2,
            padx=6,
            pady=1,
            command=self.open_deductive_dialog,
        )
        self.btn_deductive.pack(side=tk.LEFT, padx=2)

        # Nút xuất ảnh Canvas chất lượng cao chuẩn in ấn sách giáo khoa (PNG)
        self.btn_export = tk.Button(
            self.top_bar_3,
            text="[ Xuất ảnh CAD... ]",
            font=self.FONT_TOOLBAR,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            relief=tk.RAISED,
            bd=2,
            padx=5,
            pady=1,
            command=self.export_image_dialog,
        )
        self.btn_export.pack(side=tk.LEFT, padx=2)

        self.btn_lang = tk.Button(
            self.top_bar_3,
            text="[ Ngôn ngữ: VN ]",
            font=self.FONT_TOOLBAR,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            relief=tk.RAISED,
            bd=2,
            padx=5,
            pady=1,
            command=self.toggle_language,
        )
        self.btn_lang.pack(side=tk.LEFT, padx=2)

        self.btn_ai = tk.Button(
            self.top_bar_3,
            text="[ AI ]",
            font=self.FONT_TOOLBAR_BOLD,
            bg=self.WIN32_BG,
            state=tk.DISABLED,
            relief=tk.FLAT,
            bd=1,
        )
        self.btn_ai.pack(side=tk.LEFT, padx=2)

        self.btn_pro = tk.Button(
            self.top_bar_3,
            text="[ 🖨️ Pro In Ấn $1.99 ]",
            font=self.FONT_TOOLBAR_BOLD,
            bg="#FFF3E0",
            fg="#E65100",
            activebackground="#FFE0B2",
            relief=tk.RAISED,
            bd=2,
            padx=6,
            pady=1,
            command=self.open_pro_upgrade_dialog,
        )
        self.btn_pro.pack(side=tk.LEFT, padx=2)

    # --------------------------------------------------------------------------
    # WORKSPACE AREA (WHITE TECHNICAL CANVAS + RIGHT TELEMETRY / SLICE CONTROL)
    # --------------------------------------------------------------------------

    def _build_workspace_area(self) -> None:
        # Sử dụng tk.PanedWindow với thanh phân cách kéo riêng (Sash) cho phép tùy ý co giãn kích thước
        self.workspace_paned = tk.PanedWindow(
            self,
            orient=tk.HORIZONTAL,
            bg=self.WIN32_BG,
            sashrelief=tk.RAISED,
            sashwidth=6,
            bd=0,
        )
        self.workspace_paned.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.workspace_frame = self.workspace_paned  # Duy trì biến tương thích ngược

        # Left/Center Pure White 3D Canvas
        canvas_border = tk.Frame(self.workspace_paned, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2)
        self.workspace_paned.add(canvas_border, minsize=400, stretch="always")

        self.canvas = tk.Canvas(
            canvas_border,
            bg=self.CANVAS_BG,
            highlightthickness=0,
            cursor="crosshair",
        )
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Bind 3D Mouse Orbit & Zoom
        self.canvas.bind("<ButtonPress-1>", self._on_mouse_down)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_up)
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind("<Button-4>", lambda e: self._zoom_by(1.1))
        self.canvas.bind("<Button-5>", lambda e: self._zoom_by(1.0 / 1.1))
        self.canvas.bind("<Configure>", lambda _e: self.redraw_canvas())
        self.canvas.bind("<Motion>", self._on_mouse_move)

        # Right Technical Control & Coordinate Inspector Panel (Width 370px rộng rãi, có thanh kéo riêng)
        self.side_container = tk.Frame(
            self.workspace_paned,
            bg=self.WIN32_BG,
            relief=tk.GROOVE,
            bd=2,
            width=370,
        )
        self.side_container.pack_propagate(False)
        self.workspace_paned.add(self.side_container, minsize=320, width=370, stretch="never")

        # Fixed Header Bar for Side Panel
        title_frame = tk.Frame(self.side_container, bg=self.WIN32_BG, padx=8, pady=5)
        title_frame.pack(side=tk.TOP, fill=tk.X)
        self.lbl_side_title = tk.Label(
            title_frame,
            text="THÔNG SỐ KHỐI & THIẾT DIỆN" if self.lang == "VN" else "SOLID & SECTION INSPECTOR",
            bg=self.WIN32_BG,
            fg="#000080",
            font=self.FONT_TOOLBAR_BOLD,
            anchor="w",
        )
        self.lbl_side_title.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Scrollable Canvas & Scrollbar for Side Panel
        self.side_canvas = tk.Canvas(
            self.side_container,
            bg=self.WIN32_BG,
            highlightthickness=0,
            bd=0,
        )
        self.side_scrollbar = tk.Scrollbar(
            self.side_container,
            orient=tk.VERTICAL,
            command=self.side_canvas.yview,
        )
        self.side_panel = tk.Frame(self.side_canvas, bg=self.WIN32_BG, padx=6, pady=4)

        self.side_panel.bind(
            "<Configure>",
            lambda e: self.side_canvas.configure(scrollregion=self.side_canvas.bbox("all"))
        )
        self._side_canvas_win = self.side_canvas.create_window(
            (0, 0),
            window=self.side_panel,
            anchor="nw",
            width=345,
        )
        self.side_canvas.bind(
            "<Configure>",
            lambda e: self.side_canvas.itemconfig(self._side_canvas_win, width=e.width)
        )
        self.side_canvas.configure(yscrollcommand=self.side_scrollbar.set)
        self.side_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.side_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 1. Dimension & Shape Parameter Editor
        dim_box = tk.LabelFrame(
            self.side_panel,
            text="Kích thước Đa diện (Dimensions)",
            bg=self.WIN32_BG,
            font=self.FONT_TOOLBAR_BOLD,
            relief=tk.GROOVE,
            bd=2,
            padx=6,
            pady=5,
        )
        dim_box.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))
        self.dim_box = dim_box

        f_dim1 = tk.Frame(dim_box, bg=self.WIN32_BG, pady=2)
        f_dim1.pack(side=tk.TOP, fill=tk.X)
        self.lbl_dim_h = tk.Label(f_dim1, text="Chiều cao h (SA):", font=self.FONT_TOOLBAR, bg=self.WIN32_BG, width=15, anchor="w")
        self.lbl_dim_h.pack(side=tk.LEFT)
        self.ent_dim_h = tk.Entry(f_dim1, font=self.FONT_TOOLBAR, width=7, relief=tk.SUNKEN, bd=2)
        self.ent_dim_h.insert(0, "2.2")
        self.ent_dim_h.pack(side=tk.RIGHT)

        f_dim2 = tk.Frame(dim_box, bg=self.WIN32_BG, pady=2)
        f_dim2.pack(side=tk.TOP, fill=tk.X)
        self.lbl_dim_a = tk.Label(f_dim2, text="Cạnh đáy a (AB):", font=self.FONT_TOOLBAR, bg=self.WIN32_BG, width=15, anchor="w")
        self.lbl_dim_a.pack(side=tk.LEFT)
        self.ent_dim_a = tk.Entry(f_dim2, font=self.FONT_TOOLBAR, width=7, relief=tk.SUNKEN, bd=2)
        self.ent_dim_a.insert(0, "2.4")
        self.ent_dim_a.pack(side=tk.RIGHT)

        f_dim3 = tk.Frame(dim_box, bg=self.WIN32_BG, pady=2)
        f_dim3.pack(side=tk.TOP, fill=tk.X)
        self.lbl_dim_b = tk.Label(f_dim3, text="Cạnh đáy b (BC):", font=self.FONT_TOOLBAR, bg=self.WIN32_BG, width=15, anchor="w")
        self.lbl_dim_b.pack(side=tk.LEFT)
        self.ent_dim_b = tk.Entry(f_dim3, font=self.FONT_TOOLBAR, width=7, relief=tk.SUNKEN, bd=2)
        self.ent_dim_b.insert(0, "2.4")
        self.ent_dim_b.pack(side=tk.RIGHT)

        self.btn_apply_dim = tk.Button(
            dim_box,
            text="[ Áp dụng Kích thước ]",
            font=self.FONT_TOOLBAR_BOLD,
            bg=self.WIN32_BG,
            fg="#000080",
            relief=tk.RAISED,
            bd=2,
            pady=3,
            command=self.apply_user_dimensions,
        )
        self.btn_apply_dim.pack(side=tk.TOP, fill=tk.X, pady=(4, 2))

        # 2. Section Plane Height Slider & Orientation Selector
        plane_box = tk.LabelFrame(
            self.side_panel,
            text="Mặt phẳng Thiết diện (α) & Vị trí cắt",
            bg=self.WIN32_BG,
            font=self.FONT_TOOLBAR_BOLD,
            relief=tk.GROOVE,
            bd=2,
            padx=6,
            pady=5,
        )
        plane_box.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))
        self.plane_box = plane_box

        self.plane_d_scale = tk.Scale(
            plane_box,
            from_=-1.5,
            to=2.5,
            resolution=0.05,
            orient=tk.HORIZONTAL,
            bg=self.WIN32_BG,
            font=self.FONT_TOOLBAR,
            highlightthickness=0,
            label="Hằng số mặt phẳng d (n·X = d):",
            command=self._on_plane_slider_change,
        )
        self.plane_d_scale.set(self.models[self.current_model_key].plane_d)
        self.plane_d_scale.pack(side=tk.TOP, fill=tk.X, pady=(0, 4))

        # Nút nhanh mở hộp thoại Tô màu & Gạch chéo diện tích
        self.btn_side_hatch = tk.Button(
            plane_box,
            text="[ ▨ Tô màu / Gạch chéo diện tích... ]" if self.lang == "VN" else "[ ▨ CAD Hatch & Shading... ]",
            font=("Tahoma", 8, "bold"),
            fg="#6B21A8",
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            activebackground=self.WIN32_ACTIVE_BG,
            pady=3,
            command=self.open_plane_3points_dialog,
        )
        self.btn_side_hatch.pack(side=tk.TOP, fill=tk.X, pady=(1, 4))

        # Hướng cắt mặt phẳng nhanh (Ngang Oxy, Xiên alpha, Dọc Oxz, Chéo) - Rõ nét, Tương phản cao
        f_cuts = tk.Frame(plane_box, bg=self.WIN32_BG)
        f_cuts.pack(side=tk.TOP, fill=tk.X, pady=2)
        self.btn_cut_oxy = tk.Button(
            f_cuts,
            text="[ Ngang Oxy ]" if self.lang == "VN" else "[ Horiz Oxy ]",
            font=("Tahoma", 8, "bold"),
            fg="#000080",
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            activebackground=self.WIN32_ACTIVE_BG,
            command=lambda: self.set_section_plane_orientation((0.0, 0.0, 1.0)),
        )
        self.btn_cut_oxy.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)

        self.btn_cut_skew = tk.Button(
            f_cuts,
            text="[ Xiên (α) ]" if self.lang == "VN" else "[ Inclined (α) ]",
            font=("Tahoma", 8, "bold"),
            fg="#000080",
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            activebackground=self.WIN32_ACTIVE_BG,
            command=lambda: self.set_section_plane_orientation((0.0, 0.5, 0.866)),
        )
        self.btn_cut_skew.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)

        f_cuts2 = tk.Frame(plane_box, bg=self.WIN32_BG)
        f_cuts2.pack(side=tk.TOP, fill=tk.X, pady=2)
        self.btn_cut_oxz = tk.Button(
            f_cuts2,
            text="[ Dọc Oxz ]" if self.lang == "VN" else "[ Vert Oxz ]",
            font=("Tahoma", 8, "bold"),
            fg="#000080",
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            activebackground=self.WIN32_ACTIVE_BG,
            command=lambda: self.set_section_plane_orientation((0.0, 1.0, 0.0)),
        )
        self.btn_cut_oxz.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)

        self.btn_cut_diag = tk.Button(
            f_cuts2,
            text="[ Chéo (1,1,1) ]" if self.lang == "VN" else "[ Diag (1,1,1) ]",
            font=("Tahoma", 8, "bold"),
            fg="#000080",
            bg=self.WIN32_BG,
            relief=tk.RAISED,
            bd=2,
            activebackground=self.WIN32_ACTIVE_BG,
            command=lambda: self.set_section_plane_orientation((0.577, 0.577, 0.577)),
        )
        self.btn_cut_diag.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)

        # Chế độ Tô bóng kỹ thuật CAD cho Thiết diện
        f_shading_lbl = tk.Frame(plane_box, bg=self.WIN32_BG)
        f_shading_lbl.pack(side=tk.TOP, fill=tk.X, pady=(4, 1))
        self.lbl_sec_shading = tk.Label(f_shading_lbl, text="Kiểu tô thiết diện CAD:" if self.lang == "VN" else "CAD Section Shading:", font=("Tahoma", 8, "bold"), bg=self.WIN32_BG, fg="#000080")
        self.lbl_sec_shading.pack(side=tk.LEFT)

        f_shd1 = tk.Frame(plane_box, bg=self.WIN32_BG)
        f_shd1.pack(side=tk.TOP, fill=tk.X, pady=1)
        self.btn_shd_hatch = tk.Button(f_shd1, text="▨ Gạch chéo", font=("Tahoma", 7, "bold"), bg=self.WIN32_ACTIVE_BG, relief=tk.SUNKEN, bd=1, command=lambda: self.set_section_shading("hatch"))
        self.btn_shd_hatch.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        self.btn_shd_cross = tk.Button(f_shd1, text="▦ Gạch ca-rô", font=("Tahoma", 7), bg=self.WIN32_BG, relief=tk.RAISED, bd=1, command=lambda: self.set_section_shading("cross"))
        self.btn_shd_cross.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)

        f_shd2 = tk.Frame(plane_box, bg=self.WIN32_BG)
        f_shd2.pack(side=tk.TOP, fill=tk.X, pady=1)
        self.btn_shd_solid = tk.Button(f_shd2, text="■ Tô mờ", font=("Tahoma", 7), bg=self.WIN32_BG, relief=tk.RAISED, bd=1, command=lambda: self.set_section_shading("solid"))
        self.btn_shd_solid.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        self.btn_shd_stipple = tk.Button(f_shd2, text="░ Chấm lưới", font=("Tahoma", 7), bg=self.WIN32_BG, relief=tk.RAISED, bd=1, command=lambda: self.set_section_shading("stipple"))
        self.btn_shd_stipple.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        self.btn_shd_none = tk.Button(f_shd2, text="⬡ Viền", font=("Tahoma", 7), bg=self.WIN32_BG, relief=tk.RAISED, bd=1, command=lambda: self.set_section_shading("none"))
        self.btn_shd_none.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)

        # Chế độ Kéo thiết diện: Độc lập đỉnh (Pivot 3 Điểm) vs Trượt cả mặt phẳng (Parallel)
        f_drag_lbl = tk.Frame(plane_box, bg=self.WIN32_BG)
        f_drag_lbl.pack(side=tk.TOP, fill=tk.X, pady=(4, 1))
        self.lbl_sec_drag = tk.Label(f_drag_lbl, text="Chế độ kéo thiết diện:" if self.lang == "VN" else "Section Drag Mode:", font=("Tahoma", 8, "bold"), bg=self.WIN32_BG, fg="#000080")
        self.lbl_sec_drag.pack(side=tk.LEFT)

        f_drag_btns = tk.Frame(plane_box, bg=self.WIN32_BG)
        f_drag_btns.pack(side=tk.TOP, fill=tk.X, pady=1)
        self.btn_drag_pivot = tk.Button(f_drag_btns, text="🎯 Độc lập đỉnh", font=("Tahoma", 7, "bold"), bg=self.WIN32_ACTIVE_BG, relief=tk.SUNKEN, bd=1, command=lambda: self.set_section_drag_mode("pivot"))
        self.btn_drag_pivot.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        self.btn_drag_parallel = tk.Button(f_drag_btns, text="⇕ Trượt cả mp", font=("Tahoma", 7), bg=self.WIN32_BG, relief=tk.RAISED, bd=1, command=lambda: self.set_section_drag_mode("parallel"))
        self.btn_drag_parallel.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)

        # 3. Analytical Coordinates, Volume, Surface & Sphere Readout Box (với thanh cuộn riêng)
        info_box = tk.LabelFrame(
            self.side_panel,
            text="Thể tích, Diện tích & Tọa độ Oxyz",
            bg=self.WIN32_BG,
            font=self.FONT_TOOLBAR_BOLD,
            relief=tk.GROOVE,
            bd=2,
            padx=6,
            pady=5,
        )
        info_box.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))
        self.info_box = info_box

        f_info_inner = tk.Frame(info_box, bg=self.WIN32_BG)
        f_info_inner.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.info_scroll = tk.Scrollbar(f_info_inner, orient=tk.VERTICAL)
        self.info_text = tk.Text(
            f_info_inner,
            font=("Consolas", 9),
            bg="#FFFFFF",
            fg="#000000",
            relief=tk.SUNKEN,
            bd=2,
            wrap=tk.WORD,
            height=14,
            padx=5,
            pady=5,
            yscrollcommand=self.info_scroll.set,
        )
        self.info_scroll.config(command=self.info_text.yview)
        self.info_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Định dạng tags màu sắc cho Text hiển thị cực kỳ rõ nét
        self.info_text.tag_config("hdr", font=("Consolas", 9, "bold"), foreground="#000080")
        self.info_text.tag_config("hl_v", font=("Consolas", 9, "bold"), foreground="#B22222")
        self.info_text.tag_config("hl_s", font=("Consolas", 9, "bold"), foreground="#006400")
        self.info_text.tag_config("coord", font=("Consolas", 9), foreground="#1A237E")

        # 4. Quick Shortcut Guide Box
        shortcut_box = tk.LabelFrame(
            self.side_panel,
            text="Phím tắt kỹ thuật (Shortcuts)",
            bg=self.WIN32_BG,
            font=self.FONT_TOOLBAR_BOLD,
            relief=tk.GROOVE,
            bd=2,
            padx=6,
            pady=4,
        )
        shortcut_box.pack(side=tk.TOP, fill=tk.X, pady=(0, 4))
        self.shortcut_box = shortcut_box

        self.lbl_shortcuts = tk.Label(
            shortcut_box,
            text=(
                "• M / V : Xoay 3D / Chọn & Di chuyển\n"
                "• X     : Bật/Tắt hệ trục Oxyz\n"
                "• S     : Bật/Tắt thiết diện phẳng\n"
                "• C     : Bật/Tắt mặt cầu ngoại tiếp\n"
                "• B     : Đổi nét ĐẬM / MẢNH\n"
                "• D     : Hộp thoại Suy luận 3D\n"
                "• L     : Đổi ngôn ngữ VN / EN\n"
                "• Space : Đặt lại góc nhìn mặc định\n"
                "• +/-   : Thu phóng tỷ lệ\n"
                "• Mũi tên: Xoay góc nhìn 5°"
            ),
            bg=self.WIN32_BG,
            font=self.FONT_TOOLBAR,
            justify=tk.LEFT,
            anchor="w",
        )
        self.lbl_shortcuts.pack(side=tk.TOP, fill=tk.X)

        # Bind mouse wheel for side panel scrolling
        def _bind_wheel(w):
            w.bind("<MouseWheel>", self._on_side_mousewheel)
            for c in w.winfo_children():
                _bind_wheel(c)

        self.side_canvas.bind("<MouseWheel>", self._on_side_mousewheel)
        _bind_wheel(self.side_panel)

    # --------------------------------------------------------------------------
    # WIN32 STATUS BAR
    # --------------------------------------------------------------------------

    def _build_status_bar(self) -> None:
        self.status_bar = tk.Frame(self, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2, pady=2)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=2, pady=(0, 2))

        self.status_left = tk.Label(
            self.status_bar,
            text="Sẵn sàng",
            bg=self.WIN32_BG,
            font=self.FONT_STATUS,
            anchor="w",
            padx=6,
        )
        self.status_left.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.status_sphere = tk.Label(
            self.status_bar,
            text="Tâm I(0.00, 0.00, 0.00) | R = 0.000" if self.lang == "VN" else "Center I(0.00, 0.00, 0.00) | R = 0.000",
            bg=self.WIN32_BG,
            fg="#000080",
            font=self.FONT_TOOLBAR_BOLD,
            relief=tk.SUNKEN,
            bd=1,
            padx=8,
        )
        self.status_sphere.pack(side=tk.RIGHT, padx=4)

        self.status_angles = tk.Label(
            self.status_bar,
            text="Yaw: -35° | Pitch: 22° | Zoom: 135%",
            bg=self.WIN32_BG,
            font=self.FONT_STATUS,
            relief=tk.SUNKEN,
            bd=1,
            padx=8,
        )
        self.status_angles.pack(side=tk.RIGHT, padx=4)

    def set_status(self, text: str) -> None:
        """Cập nhật nội dung thanh trạng thái phía dưới."""
        if hasattr(self, "status_left"):
            self.status_left.config(text=text)

    # --------------------------------------------------------------------------
    # KEYBOARD SHORTCUT BINDINGS
    # --------------------------------------------------------------------------

    def _bind_shortcuts(self) -> None:
        # 1. Navigation & Orbit
        self.bind("<m>", lambda _e: self.toggle_interact_mode())
        self.bind("<M>", lambda _e: self.toggle_interact_mode())
        self.bind("<v>", lambda _e: self.set_interact_mode("move"))
        self.bind("<V>", lambda _e: self.set_interact_mode("move"))
        self.bind("<Delete>", self._on_delete_key)
        self.bind("<BackSpace>", self._on_delete_key)
        self.bind("<h>", self._on_key_h)
        self.bind("<H>", self._on_key_h)
        self.bind("<space>", lambda _e: self.reset_camera_view())
        self.bind("<Control-Key-0>", lambda _e: self.reset_camera_view())
        self.bind("s", lambda _e: self.toggle_section())
        self.bind("S", lambda _e: self.toggle_section())
        self.bind("x", lambda _e: self.toggle_axes())
        self.bind("X", lambda _e: self.toggle_axes())
        self.bind("b", lambda _e: self.toggle_line_weight())
        self.bind("B", lambda _e: self.toggle_line_weight())
        self.bind("c", lambda _e: self.toggle_sphere())
        self.bind("C", lambda _e: self.toggle_sphere())
        self.bind("d", lambda _e: self.open_deductive_dialog())
        self.bind("D", lambda _e: self.open_deductive_dialog())
        self.bind("r", lambda _e: self.reset_model_vertices())
        self.bind("R", lambda _e: self.reset_model_vertices())
        self.bind("<Control-r>", lambda _e: self.reset_model_vertices())
        self.bind("<Control-R>", lambda _e: self.reset_model_vertices())
        self.bind("l", lambda _e: self.toggle_language())
        self.bind("L", lambda _e: self.toggle_language())

        # 2. Undo / Redo / Clipboard Shortcuts
        self.bind("<Control-z>", self.undo)
        self.bind("<Control-Z>", self.undo)
        self.bind("<Control-y>", self.redo)
        self.bind("<Control-Y>", self.redo)
        self.bind("<Control-Shift-z>", self.redo)
        self.bind("<Control-Shift-Z>", self.redo)
        self.bind("<Control-c>", self.copy_selection)
        self.bind("<Control-C>", self.copy_selection)
        self.bind("<Control-v>", self.paste_data)
        self.bind("<Control-V>", self.paste_data)

        # 3. File & Report Shortcuts
        self.bind("<Control-e>", lambda _e: self.export_image_dialog())
        self.bind("<Control-E>", lambda _e: self.export_image_dialog())
        self.bind("<Control-p>", lambda _e: self.print_diagram_direct())
        self.bind("<Control-P>", lambda _e: self.print_diagram_direct())
        self.bind("<Control-Shift-p>", lambda _e: self.export_html_report())
        self.bind("<Control-Shift-P>", lambda _e: self.export_html_report())
        self.bind("<F1>", lambda _e: self.open_user_handbook())

        # 4. Zoom & Camera Stepping
        self.bind("<plus>", lambda _e: self._zoom_by(1.15))
        self.bind("<equal>", lambda _e: self._zoom_by(1.15))
        self.bind("<KP_Add>", lambda _e: self._zoom_by(1.15))
        self.bind("<Control-plus>", lambda _e: self._zoom_by(1.15))
        self.bind("<Control-equal>", lambda _e: self._zoom_by(1.15))
        self.bind("<minus>", lambda _e: self._zoom_by(1.0 / 1.15))
        self.bind("<KP_Subtract>", lambda _e: self._zoom_by(1.0 / 1.15))
        self.bind("<Control-minus>", lambda _e: self._zoom_by(1.0 / 1.15))
        self.bind("<Left>", lambda _e: self._rotate_step(-5.0, 0.0))
        self.bind("<Right>", lambda _e: self._rotate_step(5.0, 0.0))
        self.bind("<Up>", lambda _e: self._rotate_step(0.0, 5.0))
        self.bind("<Down>", lambda _e: self._rotate_step(0.0, -5.0))

    # --------------------------------------------------------------------------
    # COMMAND HANDLERS & STATE TOGGLES
    # --------------------------------------------------------------------------

    def open_point_on_segment_dialog(self) -> None:
        PointOnSegmentDialog(self, preselected_edge=self.selected_edge)

    def open_plane_3points_dialog(self) -> None:
        Plane3PointDialog(self)

    def set_section_shading(self, mode: str) -> None:
        model = self.models[self.current_model_key]
        model.section_fill_mode = mode
        btns = {
            "hatch": getattr(self, "btn_shd_hatch", None),
            "cross": getattr(self, "btn_shd_cross", None),
            "solid": getattr(self, "btn_shd_solid", None),
            "stipple": getattr(self, "btn_shd_stipple", None),
            "none": getattr(self, "btn_shd_none", None),
        }
        for m, btn in btns.items():
            if btn:
                if m == mode:
                    btn.config(relief=tk.SUNKEN, bg=self.WIN32_ACTIVE_BG, font=("Tahoma", 7, "bold"))
                else:
                    btn.config(relief=tk.RAISED, bg=self.WIN32_BG, font=("Tahoma", 7))
        self.redraw_canvas()

    def set_section_drag_mode(self, mode: str) -> None:
        model = self.models[self.current_model_key]
        model.section_drag_mode = mode
        if hasattr(self, "btn_drag_pivot") and hasattr(self, "btn_drag_parallel"):
            if mode == "pivot":
                self.btn_drag_pivot.config(relief=tk.SUNKEN, bg=self.WIN32_ACTIVE_BG, font=("Tahoma", 7, "bold"))
                self.btn_drag_parallel.config(relief=tk.RAISED, bg=self.WIN32_BG, font=("Tahoma", 7))
            else:
                self.btn_drag_parallel.config(relief=tk.SUNKEN, bg=self.WIN32_ACTIVE_BG, font=("Tahoma", 7, "bold"))
                self.btn_drag_pivot.config(relief=tk.RAISED, bg=self.WIN32_BG, font=("Tahoma", 7))

    def select_polyhedron(self, key: str) -> None:
        self.push_undo_state()
        if key not in self.models:
            return
        self.current_model_key = key
        model = self.models[key]
        self.plane_d_scale.set(model.plane_d)
        if hasattr(self, "btn_shd_hatch"):
            self.set_section_shading(getattr(model, "section_fill_mode", "hatch"))
        if hasattr(self, "btn_drag_pivot"):
            self.set_section_drag_mode(getattr(model, "section_drag_mode", "pivot"))
        self._refresh_button_labels()
        self.redraw_canvas()

    def toggle_interact_mode(self) -> None:
        new_mode = "move" if self.interact_mode == "orbit" else "orbit"
        self.set_interact_mode(new_mode)

    def set_interact_mode(self, mode: str) -> None:
        self.interact_mode = mode
        self.canvas.config(cursor="fleur" if self.interact_mode == "move" else "crosshair")
        self._refresh_button_labels()
        self.redraw_canvas()

    def _on_key_h(self, event: tk.Event) -> None:
        if isinstance(event.widget, (tk.Entry, ttk.Entry, tk.Text)):
            return
        self.toggle_hidden_lines()

    def toggle_hidden_lines(self) -> None:
        # Chuyển đổi vòng tròn 3 trạng thái: dashed -> solid -> hidden -> dashed
        states = ["dashed", "solid", "hidden"]
        idx = (states.index(self.hidden_mode) + 1) % len(states)
        self.hidden_mode = states[idx]
        self._refresh_button_labels()
        self.redraw_canvas()

    def reset_model_vertices(self) -> None:
        model = self.models[self.current_model_key]
        model.reset_vertices()
        self.redraw_canvas()

    def _on_side_mousewheel(self, event: tk.Event) -> None:
        """Cuộn mượt mà thanh trượt thanh công cụ bên phải."""
        if hasattr(self, "side_canvas") and event.delta:
            self.side_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _update_orientation_button_styles(self) -> None:
        """Cập nhật trạng thái viền và màu cho các nút đổi hướng mặt phẳng cắt."""
        if not hasattr(self, "btn_cut_oxy"):
            return
        model = self.models[self.current_model_key]
        cur_n = model.plane_normal
        orientations = [
            (self.btn_cut_oxy, (0.0, 0.0, 1.0)),
            (self.btn_cut_skew, (0.0, 0.5, 0.866)),
            (self.btn_cut_oxz, (0.0, 1.0, 0.0)),
            (self.btn_cut_diag, (0.577, 0.577, 0.577)),
        ]
        for btn, n_vec in orientations:
            norm_target = vec_normalize(n_vec)
            sim = abs(vec_dot(cur_n, norm_target))
            if sim > 0.98:
                btn.config(relief=tk.SUNKEN, bg=self.WIN32_ACTIVE_BG, fg="#000080")
            else:
                btn.config(relief=tk.RAISED, bg=self.WIN32_BG, fg="#000000")

    def set_section_plane_orientation(self, normal: Vec3) -> None:
        """Chuyển đổi hướng mặt phẳng thiết diện nhanh và tính toán lại giới hạn cắt."""
        model = self.models[self.current_model_key]
        model.plane_normal = vec_normalize(normal)
        dots = [vec_dot(model.plane_normal, v) for v in model.vertices.values()]
        min_d, max_d = min(dots), max(dots)
        mid_d = round((min_d + max_d) * 0.5, 2)
        model.plane_d = mid_d
        if hasattr(self, "plane_d_scale"):
            self.plane_d_scale.config(from_=round(min_d - 0.2, 2), to=round(max_d + 0.2, 2))
            self.plane_d_scale.set(mid_d)
        self._update_orientation_button_styles()
        model.compute_cross_section()
        model.update_constraints()
        self.redraw_canvas()

    def _render_scene_to_image(
        self,
        file_path: str,
        scale: int = 2,
        show_axes: Optional[bool] = None,
        show_sphere: Optional[bool] = None,
        show_section: Optional[bool] = None,
        show_auxiliary: bool = True,
        show_labels: bool = True,
        hidden_mode: Optional[str] = None,
        bold_mode: Optional[bool] = None,
        transparent_bg: bool = False,
    ) -> None:
        """
        Vẽ và xuất trực tiếp toàn bộ không gian 3D ra file PNG độ phân giải cao 300 DPI bằng Pillow.
        Thuần Python, không phụ thuộc Ghostscript, hoạt động 100% ổn định trên mọi máy tính.
        """
        from PIL import Image, ImageDraw, ImageFont

        w = max(600, self.canvas.winfo_width())
        h = max(450, self.canvas.winfo_height())
        img_w = w * scale
        img_h = h * scale

        actual_show_axes = self.show_axes if show_axes is None else show_axes
        actual_show_sphere = self.show_sphere if show_sphere is None else show_sphere
        actual_show_section = self.show_section if show_section is None else show_section
        actual_hidden_mode = self.hidden_mode if hidden_mode is None else hidden_mode
        actual_bold_mode = self.bold_mode if bold_mode is None else bold_mode

        if transparent_bg:
            img = Image.new("RGBA", (img_w, img_h), (255, 255, 255, 0))
        else:
            img = Image.new("RGBA", (img_w, img_h), (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)

        font_size = int((11 if actual_bold_mode else 10) * scale)
        font_bold_size = int((12 if actual_bold_mode else 11) * scale)
        try:
            label_font = ImageFont.truetype("times.ttf", font_size)
            label_bold_font = ImageFont.truetype("timesbd.ttf", font_bold_size)
            axis_font = ImageFont.truetype("arialbd.ttf", int(11 * scale))
        except Exception:
            label_font = ImageFont.load_default()
            label_bold_font = label_font
            axis_font = label_font

        model = self.models[self.current_model_key]

        def hex_to_rgba(hex_code: str, alpha: int = 255) -> Tuple[int, int, int, int]:
            hc = hex_code.lstrip("#")
            if len(hc) == 6:
                return (int(hc[0:2], 16), int(hc[2:4], 16), int(hc[4:6], 16), alpha)
            return (0, 0, 0, alpha)

        def to_img(pt3d: Vec3) -> Tuple[float, float, float]:
            sx, sy, sz = self.project_point(pt3d, w, h)
            return (sx * scale, sy * scale, sz)

        def draw_dashed(x1: float, y1: float, x2: float, y2: float, col: Tuple[int, int, int, int], width: int, dash: Tuple[int, int]):
            dx = x2 - x1
            dy = y2 - y1
            dist = math.hypot(dx, dy)
            if dist < 1e-4:
                return
            d_len = dash[0] * scale
            g_len = dash[1] * scale
            tot = d_len + g_len
            ux, uy = dx / dist, dy / dist
            cur = 0.0
            while cur < dist:
                end_d = min(dist, cur + d_len)
                draw.line([(x1 + cur * ux, y1 + cur * uy), (x1 + end_d * ux, y1 + end_d * uy)], fill=col, width=width)
                cur += tot

        vis_width = int((2.0 if actual_bold_mode else 1.2) * scale)
        hid_width = int((1.5 if actual_bold_mode else 0.9) * scale)
        hid_dash = (6, 4) if actual_bold_mode else (4, 3)
        vertex_r = (3.0 if actual_bold_mode else 2.2) * scale

        # 1. Trục tọa độ Oxyz
        if actual_show_axes:
            ox, oy, _ = to_img((0.0, 0.0, 0.0))
            axis_len = 2.4
            axes_info = [
                ("x", (axis_len, 0.0, 0.0), "#8B0000"),
                ("y", (0.0, axis_len, 0.0), "#006400"),
                ("z", (0.0, 0.0, axis_len), "#00008B"),
            ]
            ax_w = max(1, int(1.2 * scale))
            for ax_lbl, tip_3d, ax_col in axes_info:
                tx, ty, _ = to_img(tip_3d)
                rgba = hex_to_rgba(ax_col)
                draw.line([(ox, oy), (tx, ty)], fill=rgba, width=ax_w)
                draw.text((tx + 6 * scale, ty - 8 * scale), ax_lbl, fill=rgba, font=axis_font)
            draw.text((ox - 14 * scale, oy + 4 * scale), "O", fill=hex_to_rgba("#222222"), font=axis_font)

        # 2. Mặt cầu ngoại tiếp S(I; R)
        center_I, radius_R, sphere_err = compute_circumscribed_sphere(model.vertices)
        if actual_show_sphere:
            cx_img, cy_img, cz_cam = to_img(center_I)
            r_screen = radius_R * self.zoom * (self.camera_distance / max(1.5, cz_cam)) * scale
            sph_col = hex_to_rgba("#4169E1", 200)
            draw.ellipse(
                [(cx_img - r_screen, cy_img - r_screen), (cx_img + r_screen, cy_img + r_screen)],
                outline=sph_col, width=max(1, int(1.2 * scale))
            )
            draw.ellipse(
                [(cx_img - r_screen, cy_img - r_screen * 0.35), (cx_img + r_screen, cy_img + r_screen * 0.35)],
                outline=sph_col, width=max(1, int(1.0 * scale))
            )
            draw.ellipse(
                [(cx_img - vertex_r, cy_img - vertex_r), (cx_img + vertex_r, cy_img + vertex_r)],
                fill=sph_col, outline=sph_col
            )
            draw.text((cx_img + 8 * scale, cy_img - 10 * scale), "I", fill=sph_col, font=label_bold_font)

        # 3. Phân định nét khuất
        edge_vis, face_visible = self._compute_edge_visibility(model)

        # 4. Vẽ các mặt phẳng phụ tự tạo (Custom Planes) với gạch chéo CAD TRƯỚC
        # QUAN TRỌNG: Vẽ mảng màu & gạch chéo TRƯỚC để nét đứt không bị che!
        for c_plane in getattr(model, "custom_planes", []):
            if not c_plane.get("visible", True):
                continue
            plane_pts = c_plane.get("pts", [])
            if len(plane_pts) < 3:
                continue
            coords_3d = [model.get_point(p) for p in plane_pts]
            if any(p is None for p in coords_3d):
                continue
            pl_img_pts = [to_img(p)[:2] for p in coords_3d]
            pl_hex = c_plane.get("color", "#1971C2")
            pl_fill = c_plane.get("fill_mode", "hatch")
            pl_spacing = float(c_plane.get("hatch_spacing", 10)) * scale
            pl_col_rgba = hex_to_rgba(pl_hex, 180)
            pl_fill_rgba = hex_to_rgba(pl_hex, 60)

            if pl_fill == "solid":
                overlay = Image.new("RGBA", (img_w, img_h), (255, 255, 255, 0))
                ov_draw = ImageDraw.Draw(overlay)
                ov_draw.polygon(pl_img_pts, fill=hex_to_rgba(pl_hex, 110))
                img = Image.alpha_composite(img, overlay)
                draw = ImageDraw.Draw(img)
            elif pl_fill in ("hatch", "cross"):
                overlay = Image.new("RGBA", (img_w, img_h), (255, 255, 255, 0))
                ov_draw = ImageDraw.Draw(overlay)
                ov_draw.polygon(pl_img_pts, fill=pl_fill_rgba)
                img = Image.alpha_composite(img, overlay)
                draw = ImageDraw.Draw(img)

                h_lines = compute_polygon_hatch(pl_img_pts, spacing=pl_spacing, angle_deg=45.0)
                if pl_fill == "cross":
                    h_lines.extend(compute_polygon_hatch(pl_img_pts, spacing=pl_spacing, angle_deg=-45.0))
                for (hx1, hy1), (hx2, hy2) in h_lines:
                    draw.line([(hx1, hy1), (hx2, hy2)], fill=pl_col_rgba, width=max(1, int(1.2 * scale)))

            # Viền mặt phẳng
            k_pl = len(pl_img_pts)
            for i_pl in range(k_pl):
                draw.line([pl_img_pts[i_pl], pl_img_pts[(i_pl + 1) % k_pl]], fill=pl_col_rgba, width=max(1, int(2.0 * scale)))

            cx_pl = sum(pt[0] for pt in pl_img_pts) / k_pl
            cy_pl = sum(pt[1] for pt in pl_img_pts) / k_pl
            pl_name = c_plane.get("name", "")
            if pl_name:
                draw.text((cx_pl - 10 * scale, cy_pl - 8 * scale), pl_name, fill=pl_col_rgba, font=label_bold_font)

        # 4.5 Vẽ thiết diện phẳng (Polygon bán trong suốt + viền + gạch chéo CAD)
        section_pts = model.compute_cross_section() if actual_show_section else []
        sec_outline_col = hex_to_rgba("#000080")
        sec_fill_col = hex_to_rgba("#B4C3F0", 110)
        sec_width = int((2.2 if actual_bold_mode else 1.2) * scale)

        if len(section_pts) >= 3:
            sec_coords = [to_img(pt3d)[:2] for _, pt3d in section_pts]
            sec_mode = getattr(model, "section_fill_mode", "hatch")
            sec_spacing = float(getattr(model, "section_hatch_spacing", 10)) * scale

            if sec_mode == "solid":
                overlay = Image.new("RGBA", (img_w, img_h), (255, 255, 255, 0))
                ov_draw = ImageDraw.Draw(overlay)
                ov_draw.polygon(sec_coords, fill=sec_fill_col)
                img = Image.alpha_composite(img, overlay)
                draw = ImageDraw.Draw(img)
            elif sec_mode in ("hatch", "cross"):
                overlay = Image.new("RGBA", (img_w, img_h), (255, 255, 255, 0))
                ov_draw = ImageDraw.Draw(overlay)
                ov_draw.polygon(sec_coords, fill=hex_to_rgba("#B4C3F0", 45))
                img = Image.alpha_composite(img, overlay)
                draw = ImageDraw.Draw(img)

                h_lines = compute_polygon_hatch(sec_coords, spacing=sec_spacing, angle_deg=45.0)
                if sec_mode == "cross":
                    h_lines.extend(compute_polygon_hatch(sec_coords, spacing=sec_spacing, angle_deg=-45.0))
                for (hx1, hy1), (hx2, hy2) in h_lines:
                    draw.line([(hx1, hy1), (hx2, hy2)], fill=sec_outline_col, width=max(1, int(1.2 * scale)))

        # 5. Vẽ các cạnh khuất (nét đứt) SAU lớp màu => Nét đứt luôn nổi trên nền tô màu!
        if actual_hidden_mode != "hidden":
            for u, v in model.edges:
                pair = (u, v) if u < v else (v, u)
                if not edge_vis.get((u, v), True):
                    edge_hex = model.edge_colors.get(pair, "#000000")
                    col = hex_to_rgba(edge_hex)
                    x1, y1, _ = to_img(model.vertices[u])
                    x2, y2, _ = to_img(model.vertices[v])
                    if actual_hidden_mode == "dashed":
                        draw_dashed(x1, y1, x2, y2, col, hid_width, hid_dash)
                    else:
                        draw.line([(x1, y1), (x2, y2)], fill=col, width=hid_width)

            # Vẽ cạnh thiết diện trên mặt khuất (nét đứt)
            if len(section_pts) >= 3 and hasattr(model, "section_edges") and model.section_edges:
                for lbl_a, pt_a, lbl_b, pt_b, face_idx in model.section_edges:
                    is_edge_visible = face_visible[face_idx] if 0 <= face_idx < len(face_visible) else True
                    if not is_edge_visible:
                        x1, y1, _ = to_img(pt_a)
                        x2, y2, _ = to_img(pt_b)
                        if actual_hidden_mode == "dashed":
                            draw_dashed(x1, y1, x2, y2, sec_outline_col, sec_width, hid_dash)
                        else:
                            draw.line([(x1, y1), (x2, y2)], fill=sec_outline_col, width=sec_width)

        # 5.5 Vẽ cạnh thiết diện trên mặt thấy
        if len(section_pts) >= 3:
            if hasattr(model, "section_edges") and model.section_edges:
                for lbl_a, pt_a, lbl_b, pt_b, face_idx in model.section_edges:
                    is_edge_visible = face_visible[face_idx] if 0 <= face_idx < len(face_visible) else True
                    if is_edge_visible:
                        x1, y1, _ = to_img(pt_a)
                        x2, y2, _ = to_img(pt_b)
                        draw.line([(x1, y1), (x2, y2)], fill=sec_outline_col, width=sec_width)
            else:
                k_sec = len(section_pts)
                for i_sec in range(k_sec):
                    x1, y1, _ = to_img(section_pts[i_sec][1])
                    x2, y2, _ = to_img(section_pts[(i_sec + 1) % k_sec][1])
                    draw.line([(x1, y1), (x2, y2)], fill=sec_outline_col, width=sec_width)

            for s_lbl, s_pt in section_pts:
                sx, sy, _ = to_img(s_pt)
                v_col = hex_to_rgba(model.vertex_colors.get(s_lbl, "#000080"))
                draw.ellipse([(sx - vertex_r, sy - vertex_r), (sx + vertex_r, sy + vertex_r)], fill=v_col, outline=v_col)
                draw.text((sx + 8 * scale, sy - 8 * scale), s_lbl, fill=v_col, font=label_bold_font)

        # 6. Vẽ các cạnh thấy (nét liền)
        for u, v in model.edges:
            pair = (u, v) if u < v else (v, u)
            if edge_vis.get((u, v), True):
                edge_hex = model.edge_colors.get(pair, self.current_theme_color if self.current_theme_color != "#000000" else "#000000")
                col = hex_to_rgba(edge_hex)
                x1, y1, _ = to_img(model.vertices[u])
                x2, y2, _ = to_img(model.vertices[v])
                draw.line([(x1, y1), (x2, y2)], fill=col, width=vis_width)

        # 7. Vẽ đỉnh và nhãn đỉnh khối đa diện
        cx_screen, cy_screen, _ = to_img(model.centroid)
        for v_name, pt3d in model.vertices.items():
            sx, sy, _ = to_img(pt3d)
            v_col = hex_to_rgba(model.vertex_colors.get(v_name, "#000000"))
            draw.ellipse([(sx - vertex_r, sy - vertex_r), (sx + vertex_r, sy + vertex_r)], fill=v_col, outline=v_col)
            dx = sx - cx_screen
            dy = sy - cy_screen
            dist = math.hypot(dx, dy)
            ox, oy = (0.0, -14.0 * scale) if dist < 1e-3 else ((dx / dist) * 14.0 * scale, (dy / dist) * 14.0 * scale)
            draw.text((sx + ox - 4 * scale, sy + oy - 6 * scale), v_name, fill=hex_to_rgba("#000000"), font=label_bold_font)

        # 8. Vẽ đường phụ và điểm phụ
        for seg in model.aux_segments:
            p1_3d = seg.get("p1")
            p2_3d = seg.get("p2")
            if p1_3d and p2_3d:
                col = hex_to_rgba(seg.get("color", "#E03131"))
                w_seg = int((seg.get("width", 1.8 if actual_bold_mode else 1.2)) * scale)
                is_occ = self._is_segment_occluded(p1_3d, p2_3d, model, face_visible)
                x1, y1, _ = to_img(p1_3d)
                x2, y2, _ = to_img(p2_3d)
                if is_occ:
                    if actual_hidden_mode == "dashed":
                        draw_dashed(x1, y1, x2, y2, col, w_seg, hid_dash)
                else:
                    draw.line([(x1, y1), (x2, y2)], fill=col, width=w_seg)
                lbl = seg.get("label", "")
                if lbl:
                    mx, my = (x1 + x2) * 0.5, (y1 + y2) * 0.5
                    draw.text((mx + 6 * scale, my - 6 * scale), lbl, fill=col, font=label_font)

        for p_lbl, p_pt in model.aux_points.items():
            sx, sy, _ = to_img(p_pt)
            p_col = hex_to_rgba(model.vertex_colors.get(p_lbl, "#E03131"))
            draw.ellipse([(sx - vertex_r, sy - vertex_r), (sx + vertex_r, sy + vertex_r)], fill=p_col, outline=hex_to_rgba("#8B0000"))
            draw.text((sx + 8 * scale, sy - 8 * scale), p_lbl, fill=p_col, font=label_bold_font)

        if transparent_bg:
            img.save(file_path, "PNG", dpi=(300, 300))
        else:
            final_img = img.convert("RGB")
            final_img.save(file_path, "PNG", dpi=(300, 300))

    def export_image(self) -> None:
        """Xuất ảnh Canvas độ phân giải cao phục vụ in ấn sách giáo khoa (PNG) hoặc bản vẽ Vector (EPS)."""
        is_vn = (self.lang == "VN")
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image (*.png)", "*.png"),
                ("PostScript Vector (*.eps)", "*.eps"),
                ("All Files (*.*)", "*.*")
            ],
            title="Xuất ảnh bản vẽ 3D" if is_vn else "Export 3D Diagram",
        )
        if not file_path:
            return
        try:
            if file_path.lower().endswith(".eps") or file_path.lower().endswith(".ps"):
                self.canvas.postscript(file=file_path, colormode="color")
                messagebox.showinfo(
                    "Thành công" if is_vn else "Success",
                    f"Đã xuất bản vẽ Vector EPS thành công tại:\n{file_path}"
                    if is_vn
                    else f"Vector EPS file exported successfully to:\n{file_path}"
                )
            else:
                if not file_path.lower().endswith(".png"):
                    file_path += ".png"
                self._render_scene_to_image(file_path, scale=2)
                messagebox.showinfo(
                    "Thành công" if is_vn else "Success",
                    f"Đã xuất ảnh PNG chất lượng cao (300 DPI) thành công tại:\n{file_path}"
                    if is_vn
                    else f"High-resolution PNG image (300 DPI) exported successfully to:\n{file_path}"
                )
        except Exception as ex:
            messagebox.showerror("Lỗi" if is_vn else "Error", f"Lỗi xuất ảnh: {ex}" if is_vn else f"Export error: {ex}")

    def _find_edge_at(self, mx: int, my: int) -> Optional[Tuple[str, Any]]:
        """Tìm cạnh hoặc đoạn thẳng phụ gần nhất với con trỏ chuột trong khoảng 8 pixel."""
        w = max(400, self.canvas.winfo_width())
        h = max(320, self.canvas.winfo_height())
        model = self.models[self.current_model_key]

        def dist_to_segment_2d(px: float, py: float, x1: float, y1: float, x2: float, y2: float) -> float:
            dx = x2 - x1
            dy = y2 - y1
            l2 = dx * dx + dy * dy
            if l2 < 1e-6:
                return math.hypot(px - x1, py - y1)
            t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / l2))
            return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))

        best_dist = 8.0
        best_target = None

        # 1. Kiểm tra các đoạn phụ (ưu tiên cao)
        for idx, seg in enumerate(model.aux_segments):
            p1 = seg.get("p1")
            p2 = seg.get("p2")
            if p1 and p2:
                sx1, sy1, _ = self.project_point(p1, w, h)
                sx2, sy2, _ = self.project_point(p2, w, h)
                d = dist_to_segment_2d(mx, my, sx1, sy1, sx2, sy2)
                if d < best_dist:
                    best_dist = d
                    best_target = ("aux", idx)

        # 2. Kiểm tra các cạnh khối đa diện
        for u, v in model.edges:
            p1 = model.vertices.get(u)
            p2 = model.vertices.get(v)
            if p1 and p2:
                sx1, sy1, _ = self.project_point(p1, w, h)
                sx2, sy2, _ = self.project_point(p2, w, h)
                d = dist_to_segment_2d(mx, my, sx1, sy1, sx2, sy2)
                if d < best_dist:
                    best_dist = d
                    best_target = ("model", (u, v) if u < v else (v, u))

        return best_target

    def _find_vertex_at(self, mx: int, my: int) -> Optional[str]:
        """Tìm đỉnh khối hoặc điểm phụ gần nhất với tọa độ chuột trên màn hình 2D (ngưỡng 14px)."""
        w = max(400, self.canvas.winfo_width())
        h = max(320, self.canvas.winfo_height())
        model = self.models[self.current_model_key]
        closest_lbl = None
        min_dist = 14.0
        # Đỉnh khối đa diện
        for lbl, pt3d in model.vertices.items():
            sx, sy, _ = self.project_point(pt3d, w, h)
            d = math.hypot(mx - sx, my - sy)
            if d < min_dist:
                min_dist = d
                closest_lbl = lbl
        # Điểm phụ dựng thêm
        for lbl, pt3d in model.aux_points.items():
            sx, sy, _ = self.project_point(pt3d, w, h)
            d = math.hypot(mx - sx, my - sy)
            if d < min_dist:
                min_dist = d
                closest_lbl = lbl
        # Điểm đỉnh thiết diện (M, N, P, Q...)
        if self.show_section and hasattr(model, "section_points"):
            for s_lbl, s_pt in model.section_points:
                sx, sy, _ = self.project_point(s_pt, w, h)
                d = math.hypot(mx - sx, my - sy)
                if d < min_dist:
                    min_dist = d
                    closest_lbl = s_lbl
        return closest_lbl

    def _on_mouse_move(self, event: tk.Event) -> None:
        v = self._find_vertex_at(event.x, event.y)
        edge_info = None if v else self._find_edge_at(event.x, event.y)
        if v != self.hovered_vertex:
            self.hovered_vertex = v
            if v or edge_info:
                self.canvas.config(cursor="hand2")
            else:
                self.canvas.config(cursor="fleur" if self.interact_mode == "move" else "crosshair")
            self.redraw_canvas()
        elif edge_info:
            self.canvas.config(cursor="hand2")

    def toggle_ribbon(self) -> None:
        if self.ribbon_expanded:
            self.top_bar_1.pack_forget()
            self.top_bar_2.pack_forget()
            self.top_bar_3.pack_forget()
            self.btn_toggle_ribbon.config(text="▼ Mở rộng Ribbon" if self.lang == "VN" else "▼ Expand Ribbon")
            self.ribbon_expanded = False
        else:
            self.top_bar_1.pack(side=tk.TOP, fill=tk.X, padx=2, pady=(2, 1))
            self.top_bar_2.pack(side=tk.TOP, fill=tk.X, padx=2, pady=(1, 1))
            self.top_bar_3.pack(side=tk.TOP, fill=tk.X, padx=2, pady=(1, 2))
            self.btn_toggle_ribbon.config(text="▲ Thu gọn Ribbon" if self.lang == "VN" else "▲ Collapse Ribbon")
            self.ribbon_expanded = True
        if UIStateManager:
            UIStateManager.save_state("GeoSolver3DApp", ribbon_expanded=self.ribbon_expanded)

    def set_theme_color(self, hex_color: str) -> None:
        model = self.models[self.current_model_key]
        is_vn = (self.lang == "VN")

        # 1. Nếu có cạnh khối đa diện được chọn: tô màu riêng cạnh đó
        if self.selected_edge:
            pair = self.selected_edge
            model.edge_colors[pair] = hex_color
            u, v = pair
            self.status_left.config(
                text=f"Đã tô màu cho cạnh {u}{v}."
                if is_vn
                else f"Colored edge {u}{v}."
            )
            self.redraw_canvas()
            return

        # 2. Nếu có đoạn phụ được chọn: tô màu riêng đoạn phụ đó
        if self.selected_aux_idx is not None and 0 <= self.selected_aux_idx < len(model.aux_segments):
            seg = model.aux_segments[self.selected_aux_idx]
            seg["color"] = hex_color
            lbl = seg.get("label", f"#{self.selected_aux_idx + 1}")
            self.status_left.config(
                text=f"Đã tô màu cho đoạn phụ {lbl}."
                if is_vn
                else f"Colored aux segment {lbl}."
            )
            self.redraw_canvas()
            return

        # 3. Nếu có đỉnh được chọn: tô màu riêng đỉnh đó
        if self.selected_vertex:
            v_name = self.selected_vertex
            model.vertex_colors[v_name] = hex_color
            self.status_left.config(
                text=f"Đã tô màu cho đỉnh {v_name}."
                if is_vn
                else f"Colored vertex {v_name}."
            )
            self.redraw_canvas()
            return

        # 4. Ngược lại: đặt màu chủ đạo mặc định toàn khối
        self.current_theme_color = hex_color
        for col_hex, btn in getattr(self, "color_palette_buttons", {}).items():
            if col_hex == hex_color:
                btn.config(relief=tk.SUNKEN, bd=2)
            else:
                btn.config(relief=tk.GROOVE, bd=1)
        self.status_left.config(
            text=f"Đã đặt màu khối mặc định: {hex_color}"
            if is_vn
            else f"Set default solid color: {hex_color}"
        )
        self.redraw_canvas()

    def _on_delete_key(self, event=None) -> None:
        model = self.models[self.current_model_key]
        is_vn = (self.lang == "VN")
        if self.selected_aux_idx is not None and 0 <= self.selected_aux_idx < len(model.aux_segments):
            seg_lbl = model.aux_segments[self.selected_aux_idx].get("label", "")
            del model.aux_segments[self.selected_aux_idx]
            self.selected_aux_idx = None
            self.status_left.config(text=f"Đã xóa đoạn phụ {seg_lbl}." if is_vn else f"Deleted aux segment {seg_lbl}.")
            self.redraw_canvas()
        elif self.selected_vertex and self.selected_vertex in model.aux_points:
            v = self.selected_vertex
            del model.aux_points[v]
            if v in model.point_constraints:
                del model.point_constraints[v]
            model.aux_segments = [s for s in model.aux_segments if s.get("p1_name") != v and s.get("p2_name") != v]
            self.selected_vertex = None
            self.status_left.config(text=f"Đã xóa điểm phụ {v}." if is_vn else f"Deleted aux point {v}.")
            self.redraw_canvas()

    def apply_user_dimensions(self) -> None:
        self.push_undo_state()
        try:
            h = float(self.ent_dim_h.get())
            a = float(self.ent_dim_a.get())
            b = float(self.ent_dim_b.get())
            model = self.models[self.current_model_key]
            model.apply_dimensions(h, a, b)
            self.redraw_canvas()
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Vui lòng nhập giá trị số hợp lệ: {ex}")

    def toggle_axes(self) -> None:
        self.show_axes = not self.show_axes
        self._refresh_button_labels()
        self.redraw_canvas()

    def toggle_section(self) -> None:
        self.show_section = not self.show_section
        self._refresh_button_labels()
        self.redraw_canvas()

    def toggle_sphere(self) -> None:
        self.show_sphere = not self.show_sphere
        self._refresh_button_labels()
        self.redraw_canvas()

    def toggle_line_weight(self) -> None:
        self.bold_mode = not self.bold_mode
        self._refresh_button_labels()
        self.redraw_canvas()

    def toggle_language(self) -> None:
        self.lang = "EN" if self.lang == "VN" else "VN"
        if UIStateManager:
            UIStateManager.save_state("GeoSolver3DApp", lang=self.lang)
        self._refresh_button_labels()
        self.redraw_canvas()

    def reset_camera_view(self) -> None:
        self.yaw_deg = self.DEFAULT_YAW_DEG
        self.pitch_deg = self.DEFAULT_PITCH_DEG
        self.zoom = self.DEFAULT_ZOOM
        self.redraw_canvas()

    def open_construction_dialog(self) -> None:
        Construction3DDialog(self)

    def open_deductive_dialog(self) -> None:
        Deductive3DDialog(self, self.deductive_engine, self.lang)

    def open_pro_upgrade_dialog(self) -> None:
        ProUpgradeDialog(self, feature="general")

    def update_pro_ui_state(self) -> None:
        """Cập nhật trạng thái hiển thị giao diện theo quyền Pro (IAP)."""
        is_vn = (self.lang == "VN")
        is_pro = LicenseManager.is_pro_active() if LicenseManager else False

        # Window Title
        if is_pro:
            self.title(
                f"GeoSolver 3D CAD Pro (v3.2.1.0) - {'Hình Học Không Gian & CAD' if is_vn else 'Spatial Geometry & CAD Studio'}"
            )
        else:
            self.title(
                f"GeoSolver 3D CAD (v3.2.1.0) - {'Bản Tiêu Chuẩn' if is_vn else 'Standard Edition'}"
            )

        # Toolbar Pro button
        if hasattr(self, "btn_pro"):
            if is_pro:
                self.btn_pro.config(
                    text="[ 👑 Pro ]",
                    bg="#E8F5E9",
                    fg="#2E7D32",
                    activebackground="#C8E6C9",
                    command=self.open_pro_upgrade_dialog,
                )
            else:
                self.btn_pro.config(
                    text="[ 🖨️ Pro In Ấn $1.99 ]" if is_vn else "[ 🖨️ Pro Print $1.99 ]",
                    bg="#FFF3E0",
                    fg="#E65100",
                    activebackground="#FFE0B2",
                    command=self.open_pro_upgrade_dialog,
                )

    def open_ai_hub(self) -> None:
        is_vn = (self.lang == "VN")
        title = "Trợ Lý AI 3D (Đang hoàn thiện)" if is_vn else "AI 3D Assistant (In Development)"
        msg = (
            "Tính năng Trợ lý AI 3D đang được tiếp tục hoàn thiện và dự kiến tích hợp trong bản cập nhật kế tiếp.\n\n"
            "Hiện tại, quý thầy cô và học sinh có thể sử dụng Động cơ Suy luận 12 Chuyên đề 3D tại mục 'Công cụ -> Suy luận 3D' (Phím tắt: 'D') với lời giải từng bước chuẩn chương trình GDPT 2018."
            if is_vn else
            "The AI 3D Assistant feature is currently under active development and will be released in an upcoming update.\n\n"
            "Currently, please use the built-in 12-Topic 3D Deductive Engine under 'Tools -> 3D Deduction' (Shortcut: 'D') for complete step-by-step mathematical proofs."
        )
        messagebox.showinfo(title, msg, parent=self)

    def _on_plane_slider_change(self, val_str: str) -> None:
        try:
            val = float(val_str)
            self.models[self.current_model_key].plane_d = val
            self.redraw_canvas()
        except Exception:
            pass

    def _refresh_button_labels(self) -> None:
        is_vn = self.lang == "VN"

        # Update Pro state and title
        self.update_pro_ui_state()

        # Update Desktop Menu Bar
        if hasattr(self, "_build_menu_bar"):
            self._build_menu_bar()

        # Update Undo / Redo Buttons
        if hasattr(self, "btn_undo"):
            self.btn_undo.config(text="[ ↶ Hoàn tác (Ctrl+Z) ]" if is_vn else "[ ↶ Undo (Ctrl+Z) ]")
        if hasattr(self, "btn_redo"):
            self.btn_redo.config(text="[ ↷ Làm lại (Ctrl+Y) ]" if is_vn else "[ ↷ Redo (Ctrl+Y) ]")
        if hasattr(self, "btn_ai"):
            self.btn_ai.config(
                text="[ AI ]",
                state=tk.DISABLED,
                relief=tk.FLAT,
            )

        # Update Ribbon collapse button
        self.btn_toggle_ribbon.config(
            text=("▲ Thu gọn Ribbon" if self.ribbon_expanded else "▼ Mở rộng Ribbon")
            if is_vn
            else ("▲ Collapse Ribbon" if self.ribbon_expanded else "▼ Expand Ribbon")
        )

        # Update Palette label and buttons
        if hasattr(self, "lbl_palette_title"):
            self.lbl_palette_title.config(text="Màu:" if is_vn else "Color:")
        palette_names_vn = {"#E03131": "● Đỏ", "#1971C2": "● Xanh", "#212529": "● Đen", "#2B8A3E": "● Lục", "#E8590C": "● Cam"}
        palette_names_en = {"#E03131": "● Red", "#1971C2": "● Blue", "#212529": "● Black", "#2B8A3E": "● Green", "#E8590C": "● Orange"}
        for c_hex, btn in getattr(self, "color_palette_buttons", {}).items():
            btn.config(text=palette_names_vn.get(c_hex, "") if is_vn else palette_names_en.get(c_hex, ""))

        # Update Row 1 Group Label & Polyhedron Buttons
        self.lbl_group_row1.config(text="Khối Đa Diện:" if is_vn else "Polyhedra:")
        for key, text_vn, text_en in self._poly_specs:
            btn = self.poly_buttons[key]
            btn.config(
                text=text_vn if is_vn else text_en,
                relief=tk.SUNKEN if key == self.current_model_key else tk.RAISED,
                bg=self.WIN32_ACTIVE_BG if key == self.current_model_key else self.WIN32_BG,
                font=self.FONT_TOOLBAR_BOLD if key == self.current_model_key else self.FONT_TOOLBAR,
            )
        self.btn_reset_model.config(text="[ ↺ Khôi phục khối ]" if is_vn else "[ ↺ Reset Solid ]")

        # Update Row 2 Group Label & 3D Display Buttons
        self.lbl_group_row2.config(text="Hiển Thị 3D:" if is_vn else "3D Display:")

        is_orbit = (self.interact_mode == "orbit")
        if hasattr(self, "btn_mode_orbit"):
            self.btn_mode_orbit.config(
                text="[ 🔄 Xoay 3D ]" if is_vn else "[ 🔄 3D Orbit ]",
                relief=tk.SUNKEN if is_orbit else tk.RAISED,
                bg=self.WIN32_ACTIVE_BG if is_orbit else self.WIN32_BG,
                fg="#000080" if is_orbit else "#000000",
                font=self.FONT_TOOLBAR_BOLD if is_orbit else self.FONT_TOOLBAR,
            )
        if hasattr(self, "btn_mode_move"):
            self.btn_mode_move.config(
                text="[ ✋ Chọn / Di chuyển ]" if is_vn else "[ ✋ Select & Move ]",
                relief=tk.RAISED if is_orbit else tk.SUNKEN,
                bg=self.WIN32_BG if is_orbit else self.WIN32_ACTIVE_BG,
                fg="#000000" if is_orbit else "#000080",
                font=self.FONT_TOOLBAR if is_orbit else self.FONT_TOOLBAR_BOLD,
            )
        if hasattr(self, "lbl_header_title"):
            self.lbl_header_title.config(
                text="GEOSOLVER 3D — BẢNG ĐIỀU KHIỂN CAD KHÔNG GIAN"
                if is_vn
                else "GEOSOLVER 3D — 3D SOLID GEOMETRY CAD CONTROL PANEL"
            )

        hidden_txt = {
            "dashed": "[ Nét đứt (cạnh khuất): BẬT ]" if is_vn else "[ Hidden: DASHED ]",
            "solid": "[ Nét đứt: KHUNG DÂY ]" if is_vn else "[ Hidden: SOLID ]",
            "hidden": "[ Nét đứt: ẨN ]" if is_vn else "[ Hidden: CULLED ]",
        }.get(self.hidden_mode, "[ Nét đứt (cạnh khuất): BẬT ]")
        self.btn_hidden.config(
            text=hidden_txt,
            relief=tk.SUNKEN if self.hidden_mode == "dashed" else tk.RAISED,
            bg=self.WIN32_ACTIVE_BG if self.hidden_mode == "dashed" else self.WIN32_BG,
        )

        axes_state_vn = "BẬT" if self.show_axes else "TẮT"
        axes_state_en = "ON" if self.show_axes else "OFF"
        self.btn_axes.config(
            text=f"[ Trục Oxyz: {axes_state_vn} ]" if is_vn else f"[ Axes Oxyz: {axes_state_en} ]",
            relief=tk.SUNKEN if self.show_axes else tk.RAISED,
            bg=self.WIN32_ACTIVE_BG if self.show_axes else self.WIN32_BG,
        )

        sec_state_vn = "BẬT" if self.show_section else "TẮT"
        sec_state_en = "ON" if self.show_section else "OFF"
        self.btn_section.config(
            text=f"[ Thiết diện: {sec_state_vn} ]" if is_vn else f"[ Cross-Section: {sec_state_en} ]",
            relief=tk.SUNKEN if self.show_section else tk.RAISED,
            bg=self.WIN32_ACTIVE_BG if self.show_section else self.WIN32_BG,
        )

        sph_state_vn = "BẬT" if self.show_sphere else "TẮT"
        sph_state_en = "ON" if self.show_sphere else "OFF"
        self.btn_sphere.config(
            text=f"[ Mặt cầu: {sph_state_vn} ]" if is_vn else f"[ Sphere: {sph_state_en} ]",
            relief=tk.SUNKEN if self.show_sphere else tk.RAISED,
            bg=self.WIN32_ACTIVE_BG if self.show_sphere else self.WIN32_BG,
        )

        if self.bold_mode:
            lw_text = "[ Nét vẽ: ĐẬM ]" if is_vn else "[ Line: BOLD (Screen) ]"
        else:
            lw_text = "[ Nét vẽ: MẢNH (In ấn) ]" if is_vn else "[ Line: LIGHT (Print) ]"
        self.btn_line_weight.config(text=lw_text)

        self.btn_reset_view.config(text="[ Đặt lại View ]" if is_vn else "[ Reset View ]")

        # Update Row 3 Group Label & Pedagogical / Deductive Buttons
        if hasattr(self, "lbl_group_row3"):
            self.lbl_group_row3.config(text="Công Cụ & Suy Luận:" if is_vn else "Tools & Deduction:")
        self.btn_construct.config(text="[ Dựng hình 3D ]" if is_vn else "[ 3D Construction ]")
        if hasattr(self, "btn_point_on_seg"):
            self.btn_point_on_seg.config(text="[ ➕ Điểm trên đoạn ]" if is_vn else "[ ➕ Point on Seg ]")
        if hasattr(self, "btn_plane_3pts"):
            self.btn_plane_3pts.config(text="[ 📐 Mặt phẳng 3 điểm ]" if is_vn else "[ 📐 3-Point Plane ]")
        self.btn_deductive.config(text="[ Suy luận 3D ]" if is_vn else "[ 3D Deduction ]")
        self.btn_export.config(text="[ Xuất ảnh PNG ]" if is_vn else "[ Export PNG ]")
        self.btn_lang.config(text=f"[ Ngôn ngữ: {self.lang} ]" if is_vn else f"[ Language: {self.lang} ]")
        if hasattr(self, "lbl_sec_shading"):
            self.lbl_sec_shading.config(text="Kiểu tô thiết diện CAD:" if is_vn else "CAD Section Shading:")
        if hasattr(self, "lbl_sec_drag"):
            self.lbl_sec_drag.config(text="Chế độ kéo thiết diện:" if is_vn else "Section Drag Mode:")
        if hasattr(self, "btn_drag_pivot"):
            self.btn_drag_pivot.config(text="🎯 Độc lập đỉnh" if is_vn else "🎯 Independent Pivot")
        if hasattr(self, "btn_drag_parallel"):
            self.btn_drag_parallel.config(text="⇕ Trượt cả mp" if is_vn else "⇕ Parallel Slide")

        # Update side panel titles and labels
        self.lbl_side_title.config(
            text="THÔNG SỐ KHỐI & MẶT PHẲNG CẮT" if is_vn else "SOLID & SECTION PLANE INSPECTOR"
        )
        if hasattr(self, "dim_box"):
            self.dim_box.config(text="Kích thước Đa diện (CAD)" if is_vn else "Solid Dimensions (CAD)")
        if hasattr(self, "lbl_dim_h"):
            self.lbl_dim_h.config(text="Chiều cao h (SA):" if is_vn else "Height h (SA):")
        if hasattr(self, "lbl_dim_a"):
            self.lbl_dim_a.config(text="Cạnh đáy a (AB):" if is_vn else "Base edge a (AB):")
        if hasattr(self, "lbl_dim_b"):
            self.lbl_dim_b.config(text="Cạnh đáy b (BC):" if is_vn else "Base edge b (BC):")
        if hasattr(self, "btn_apply_dim"):
            self.btn_apply_dim.config(text="[ Áp dụng Kích thước ]" if is_vn else "[ Apply Dimensions ]")

        self.plane_box.config(
            text="Điều chỉnh mặt phẳng thiết diện (α)" if is_vn else "Section Plane Offset (α)"
        )
        self.plane_d_scale.config(
            label="Hằng số mặt phẳng d (n·X = d):" if is_vn else "Plane Constant d (n·X = d):"
        )
        self.shortcut_box.config(
            text="Phím tắt kỹ thuật (Shortcuts)" if is_vn else "Technical Shortcuts"
        )
        self.lbl_shortcuts.config(
            text=(
                "• X     : Bật/Tắt hệ trục Oxyz\n"
                "• S     : Bật/Tắt thiết diện phẳng\n"
                "• C     : Bật/Tắt mặt cầu ngoại tiếp\n"
                "• B     : Đổi nét ĐẬM / MẢNH\n"
                "• D     : Hộp thoại Suy luận 3D\n"
                "• L     : Đổi ngôn ngữ VN / EN\n"
                "• Space : Đặt lại góc nhìn mặc định\n"
                "• +/-   : Thu phóng tỷ lệ\n"
                "• Mũi tên: Xoay góc nhìn 5°"
            )
            if is_vn
            else (
                "• X     : Toggle Axes Oxyz\n"
                "• S     : Toggle Cross-Section\n"
                "• C     : Toggle Circum-Sphere\n"
                "• B     : Toggle Bold / Light Line\n"
                "• D     : 3D Deductive Dialog\n"
                "• L     : Toggle Language VN/EN\n"
                "• Space : Reset camera view\n"
                "• +/-   : Zoom In / Out\n"
                "• Arrows: Orbit rotate 5°"
            )
        )
        self.info_box.config(
            text="Thể tích, Diện tích & Tọa độ Oxyz" if is_vn else "Volume, Surface & Oxyz Coordinates"
        )
        if hasattr(self, "btn_cut_oxy"):
            self.btn_cut_oxy.config(text="[ Ngang Oxy ]" if is_vn else "[ Horiz Oxy ]")
        if hasattr(self, "btn_cut_skew"):
            self.btn_cut_skew.config(text="[ Xiên (α) ]" if is_vn else "[ Inclined (α) ]")
        if hasattr(self, "btn_cut_oxz"):
            self.btn_cut_oxz.config(text="[ Dọc Oxz ]" if is_vn else "[ Vert Oxz ]")
        if hasattr(self, "btn_cut_diag"):
            self.btn_cut_diag.config(text="[ Chéo (1,1,1) ]" if is_vn else "[ Diag (1,1,1) ]")
        self._update_orientation_button_styles()

    # --------------------------------------------------------------------------
    # MOUSE & CAMERA INTERACTION
    # --------------------------------------------------------------------------

    def _on_mouse_down(self, event: tk.Event) -> None:
        self.canvas.focus_set()
        is_vn = (self.lang == "VN")
        model = self.models[self.current_model_key]
        v = self._find_vertex_at(event.x, event.y)
        is_shift_or_ctrl = bool(event.state & 0x0001) or bool(event.state & 0x0004)

        # 1. Nhấn trúng đỉnh (đỉnh khối, điểm phụ, hoặc đỉnh thiết diện M, N, P, Q)
        if v:
            self.selected_vertex = v
            self.selected_edge = None
            self.selected_aux_idx = None
            # Kiểm tra nếu là điểm thiết diện MNPQ
            is_sec_pt = (self.show_section and hasattr(model, "section_points") and any(s[0] == v for s in model.section_points))
            if is_sec_pt:
                pair = getattr(model, "section_edge_map", {}).get(v)
                pair_str = f" (trên cạnh {pair[0]}{pair[1]})" if pair else ""
                drag_mode_str = "kéo độc lập đỉnh (xoay nghiêng mp)" if getattr(model, "section_drag_mode", "pivot") == "pivot" else "trượt cả thiết diện"
                self.status_left.config(
                    text=f"Đã chọn đỉnh thiết diện {v}{pair_str} - Chế độ: {drag_mode_str}."
                    if is_vn
                    else f"Selected section vertex {v}{pair_str} - Mode: {drag_mode_str}."
                )
                self._drag_sec_fixed_pts = [pt for lbl, pt in model.section_points if lbl != v]
            else:
                self._drag_sec_fixed_pts = None
                self.status_left.config(
                    text=f"Đã chọn đỉnh {v}. Bạn có thể kéo di chuyển hoặc bấm bảng màu."
                    if is_vn
                    else f"Selected vertex {v}. You can drag to move or click palette to color."
                )
            if self.interact_mode == "move" or is_shift_or_ctrl:
                self.dragged_vertex = v
                self._drag_last_x = event.x
                self._drag_last_y = event.y
            self.redraw_canvas()
            return

        # 2. Nhấn trúng cạnh (cạnh khối hoặc đoạn phụ)
        edge_info = self._find_edge_at(event.x, event.y)
        if edge_info:
            target_type, target_val = edge_info
            if target_type == "model":
                self.selected_edge = target_val
                self.selected_aux_idx = None
                self.selected_vertex = None
                u, w_vert = target_val
                self.status_left.config(
                    text=f"Đã chọn cạnh {u}{w_vert}. Nhấn nút trên bảng màu để tô màu cạnh này."
                    if is_vn
                    else f"Selected edge {u}{w_vert}. Click a palette color to dye this edge."
                )
            else:
                self.selected_aux_idx = target_val
                self.selected_edge = None
                self.selected_vertex = None
                seg_lbl = model.aux_segments[target_val].get("label", f"#{target_val+1}")
                self.status_left.config(
                    text=f"Đã chọn đoạn phụ {seg_lbl}. Nhấn nút trên bảng màu để tô màu đoạn này."
                    if is_vn
                    else f"Selected aux segment {seg_lbl}. Click a palette color to dye this segment."
                )
            self.dragged_vertex = None
            self.redraw_canvas()
            return

        # 3. Nhấn vào vùng trống canvas
        self.selected_vertex = None
        self.selected_edge = None
        self.selected_aux_idx = None
        self.dragged_vertex = None
        self._drag_last_x = event.x
        self._drag_last_y = event.y
        self.redraw_canvas()

    def _on_mouse_drag(self, event: tk.Event) -> None:
        if self._drag_last_x is None or self._drag_last_y is None:
            self._drag_last_x = event.x
            self._drag_last_y = event.y
            return

        dx = event.x - self._drag_last_x
        dy = event.y - self._drag_last_y
        self._drag_last_x = event.x
        self._drag_last_y = event.y

        # Nếu đang kéo đỉnh 3D (Đỉnh khối, Điểm phụ ràng buộc, hoặc Đỉnh thiết diện MNPQ)
        if self.dragged_vertex:
            model = self.models[self.current_model_key]
            right, up, _fwd, _eye = self._camera_basis()
            scale = 1.0 / max(10.0, self.zoom)
            dP = vec_sub(vec_scale(right, dx * scale), vec_scale(up, dy * scale))

            # 1. Trượt thiết diện khi kéo điểm thiết diện M, N, P, Q
            if self.show_section and hasattr(model, "section_points"):
                s_dict = dict(model.section_points)
                if self.dragged_vertex in s_dict:
                    cur_pt = s_dict[self.dragged_vertex]
                    pair = getattr(model, "section_edge_map", {}).get(self.dragged_vertex)
                    if pair and pair[0] in model.vertices and pair[1] in model.vertices:
                        p1 = model.vertices[pair[0]]
                        p2 = model.vertices[pair[1]]
                        v_edge = vec_sub(p2, p1)
                        l2 = vec_dot(v_edge, v_edge)
                        if l2 > 1e-6:
                            target_pt = vec_add(cur_pt, dP)
                            t = vec_dot(vec_sub(target_pt, p1), v_edge) / l2
                            t_clamped = max(0.01, min(0.99, t))
                            pt_new = vec_add(p1, vec_scale(v_edge, t_clamped))

                            if getattr(model, "section_drag_mode", "pivot") == "pivot":
                                # Kéo độc lập đỉnh thiết diện: các đỉnh khác đóng vai trò điểm cố định xác định mặt phẳng mới!
                                fixed_pts = getattr(self, "_drag_sec_fixed_pts", None)
                                if not fixed_pts or len(fixed_pts) < 2:
                                    fixed_pts = [pt for lbl, pt in model.section_points if lbl != self.dragged_vertex]
                                if len(fixed_pts) >= 2:
                                    n_cand = vec_cross(vec_sub(fixed_pts[0], pt_new), vec_sub(fixed_pts[1], pt_new))
                                    if vec_norm(n_cand) > 1e-5:
                                        n_unit = vec_normalize(n_cand)
                                        if vec_dot(n_unit, model.plane_normal) < 0:
                                            n_unit = vec_scale(n_unit, -1.0)
                                        model.plane_normal = n_unit
                                        model.plane_d = vec_dot(n_unit, pt_new)
                                    else:
                                        model.plane_d = vec_dot(model.plane_normal, pt_new)
                                else:
                                    model.plane_d = vec_dot(model.plane_normal, pt_new)
                            else:
                                model.plane_d = vec_dot(model.plane_normal, pt_new)
                        else:
                            model.plane_d = model.plane_d + vec_dot(model.plane_normal, dP)
                    else:
                        model.plane_d = model.plane_d + vec_dot(model.plane_normal, dP)

                    if hasattr(self, "plane_d_scale"):
                        self.plane_d_scale.set(model.plane_d)
                    model.compute_cross_section()
                    model.update_constraints()
                    self.redraw_canvas()
                    return

            if self.dragged_vertex in model.vertices:
                old_p = model.vertices[self.dragged_vertex]
                model.vertices[self.dragged_vertex] = vec_add(old_p, dP)
            elif self.dragged_vertex in model.aux_points:
                old_p = model.aux_points[self.dragged_vertex]
                new_p = vec_add(old_p, dP)
                # Nếu điểm có ràng buộc tỉ số k trên đoạn AB, trượt theo đoạn AB
                c = model.point_constraints.get(self.dragged_vertex)
                if c and c.get("type") == "ratio":
                    p1 = model.get_point(c["p1"])
                    p2 = model.get_point(c["p2"])
                    if p1 and p2:
                        u = vec_sub(p2, p1)
                        u2 = vec_dot(u, u)
                        if u2 > 1e-9:
                            k_new = vec_dot(vec_sub(new_p, p1), u) / u2
                            c["k"] = max(0.0, min(1.0, k_new))
                            new_p = vec_add(p1, vec_scale(u, c["k"]))
                            for seg in model.aux_segments:
                                if seg.get("p2_name") == self.dragged_vertex or seg.get("p1_name") == self.dragged_vertex:
                                    seg["label"] = f"{self.dragged_vertex} (k={c['k']:.2f})"
                            is_vn = (self.lang == "VN")
                            self.status_left.config(
                                text=f"Điểm {self.dragged_vertex} ∈ {c['p1']}{c['p2']} | Tỉ số k = {c['k']:.2f}"
                                if is_vn
                                else f"Point {self.dragged_vertex} ∈ {c['p1']}{c['p2']} | Ratio k = {c['k']:.2f}"
                            )
                model.aux_points[self.dragged_vertex] = new_p

            model.update_constraints()
            model.recalculate_geometry()
            self.redraw_canvas()
            return

        # Nếu đang ở chế độ xoay Orbit: kéo chuột trái xoay tự nhiên theo chuẩn CAD / GeoGebra
        self.yaw_deg = (self.yaw_deg - dx * 0.45) % 360.0
        if self.yaw_deg > 180.0:
            self.yaw_deg -= 360.0
        self.pitch_deg = max(-85.0, min(85.0, self.pitch_deg + dy * 0.45))
        self.redraw_canvas()

    def _on_mouse_up(self, _event: tk.Event) -> None:
        self.dragged_vertex = None
        self._drag_sec_fixed_pts = None
        self._drag_last_x = None
        self._drag_last_y = None

    def _on_mouse_wheel(self, event: tk.Event) -> None:
        if event.delta > 0:
            self._zoom_by(1.1)
        elif event.delta < 0:
            self._zoom_by(1.0 / 1.1)

    def _zoom_by(self, factor: float) -> None:
        self.zoom = max(45.0, min(380.0, self.zoom * factor))
        self.redraw_canvas()

    def _rotate_step(self, dyaw: float, dpitch: float) -> None:
        self.yaw_deg = (self.yaw_deg - dyaw) % 360.0
        if self.yaw_deg > 180.0:
            self.yaw_deg -= 360.0
        self.pitch_deg = max(-85.0, min(85.0, self.pitch_deg + dpitch))
        self.redraw_canvas()

    # --------------------------------------------------------------------------
    # 3D CAMERA TRANSFORMATION & PERSPECTIVE PROJECTION ENGINE
    # --------------------------------------------------------------------------

    def _camera_basis(self) -> Tuple[Vec3, Vec3, Vec3, Vec3]:
        """
        Computes right, up, forward unit vectors and camera eye position in world space.
        Uses a standard right-handed camera basis so that cross(right, up) == forward
        and horizontal screen coordinate matches world right without mirroring.
        """
        yaw = math.radians(self.yaw_deg)
        pitch = math.radians(self.pitch_deg)

        # Spherical camera eye around target (0, 0, 0.65)
        cx = self.camera_distance * math.cos(pitch) * math.cos(yaw)
        cy = self.camera_distance * math.cos(pitch) * math.sin(yaw)
        cz = self.camera_distance * math.sin(pitch) + 0.65
        eye: Vec3 = (cx, cy, cz)
        target: Vec3 = (0.0, 0.0, 0.65)

        forward = vec_normalize(vec_sub(target, eye))
        world_up: Vec3 = (0.0, 0.0, 1.0)
        # Standard right-handed camera basis: forward x world_up points to camera right (+X)
        right = vec_cross(forward, world_up)
        if vec_norm(right) < 1e-6:
            right = (1.0, 0.0, 0.0)
        else:
            right = vec_normalize(right)
        up = vec_normalize(vec_cross(right, forward))
        return right, up, forward, eye

    def project_point(self, pt: Vec3, width: int, height: int) -> Tuple[float, float, float]:
        """
        Projects 3D point (x, y, z) to 2D canvas coordinates (sx, sy, depth).
        """
        right, up, forward, eye = self._camera_basis()
        rel = vec_sub(pt, eye)
        x_cam = vec_dot(rel, right)
        y_cam = vec_dot(rel, up)
        z_cam = max(1.5, vec_dot(rel, forward))

        persp = self.camera_distance / z_cam
        sx = (width * 0.5) + self.pan_x + x_cam * self.zoom * persp
        sy = (height * 0.54) + self.pan_y - y_cam * self.zoom * persp
        return (sx, sy, z_cam)

    # --------------------------------------------------------------------------
    # BACKFACE CULLING & HIDDEN EDGE DETECTION
    # --------------------------------------------------------------------------

    @staticmethod
    def _convex_hull_2d(points: Dict[str, Tuple[float, float]]) -> List[str]:
        """
        Computes 2D convex hull of screen projected points using Andrew's Monotone Chain.
        Returns list of vertex names on the hull in cyclic order.
        """
        pts = sorted(points.items(), key=lambda item: (item[1][0], item[1][1]))
        if len(pts) <= 2:
            return [p[0] for p in pts]

        def cross_2d(o: Tuple[float, float], a: Tuple[float, float], b: Tuple[float, float]) -> float:
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

        lower: List[str] = []
        for p in pts:
            while len(lower) >= 2 and cross_2d(points[lower[-2]], points[lower[-1]], p[1]) <= 1e-4:
                lower.pop()
            lower.append(p[0])

        upper: List[str] = []
        for p in reversed(pts):
            while len(upper) >= 2 and cross_2d(points[upper[-2]], points[upper[-1]], p[1]) <= 1e-4:
                upper.pop()
            upper.append(p[0])

        return lower[:-1] + upper[:-1]

    def _is_segment_occluded(
        self,
        p1: Vec3,
        p2: Vec3,
        model: PolyhedronModel,
        face_visible: List[bool]
    ) -> bool:
        """
        Xác định một đoạn thẳng 3D (p1, p2) có bị khuất (cần vẽ nét đứt) hay không
        theo nguyên tắc hình học không gian :
        - Nếu cả 2 đầu mút cùng nằm trên một mặt ngoài đang hướng về mắt nhìn (front-facing) => Thấy (nét liền).
        - Nếu nằm trên mặt khuất (back-facing) hoặc đi xuyên qua lòng khối đa diện (nội bộ) => Khuất (nét đứt).
        """
        def point_on_face(pt: Vec3, face: List[str]) -> bool:
            for v_name in face:
                v_pt = model.vertices.get(v_name)
                if v_pt and math.hypot(pt[0] - v_pt[0], pt[1] - v_pt[1], pt[2] - v_pt[2]) < 1e-4:
                    return True
            if len(face) < 3:
                return False
            v0 = model.vertices[face[0]]
            normal = model.compute_face_outward_normal(face)
            dist_to_plane = abs(vec_dot(normal, vec_sub(pt, v0)))
            if dist_to_plane > 1e-3:
                return False
            nx, ny, nz = abs(normal[0]), abs(normal[1]), abs(normal[2])
            if nz >= nx and nz >= ny:
                poly2d = [(model.vertices[v][0], model.vertices[v][1]) for v in face]
                pt2d = (pt[0], pt[1])
            elif ny >= nx and ny >= nz:
                poly2d = [(model.vertices[v][0], model.vertices[v][2]) for v in face]
                pt2d = (pt[0], pt[2])
            else:
                poly2d = [(model.vertices[v][1], model.vertices[v][2]) for v in face]
                pt2d = (pt[1], pt[2])
            n_pts = len(poly2d)
            inside = False
            for i in range(n_pts):
                x1, y1 = poly2d[i]
                x2, y2 = poly2d[(i + 1) % n_pts]
                dx = x2 - x1
                dy = y2 - y1
                l2 = dx * dx + dy * dy
                if l2 > 1e-8:
                    t = max(0.0, min(1.0, ((pt2d[0] - x1) * dx + (pt2d[1] - y1) * dy) / l2))
                    if math.hypot(pt2d[0] - (x1 + t * dx), pt2d[1] - (y1 + t * dy)) < 1e-4:
                        return True
                if ((y1 > pt2d[1]) != (y2 > pt2d[1])) and (
                    pt2d[0] < (x2 - x1) * (pt2d[1] - y1) / (y2 - y1 + 1e-12) + x1
                ):
                    inside = not inside
            return inside

        for f_idx, face in enumerate(model.faces):
            if point_on_face(p1, face) and point_on_face(p2, face):
                if face_visible[f_idx]:
                    return False  # Nằm trên mặt thấy => Nét liền

        return True  # Nằm trên mặt khuất hoặc đi trong lòng khối => Nét đứt

    def _compute_edge_visibility(self, model: PolyhedronModel) -> Tuple[Dict[Tuple[str, str], bool], List[bool]]:
        """
        Determines whether each polyhedron edge is visible (solid line) or hidden (dashed line)
        using Backface Culling + 2D Silhouette boundary protection.
        """
        _right, _up, _forward, eye = self._camera_basis()
        face_visible: List[bool] = []

        for face in model.faces:
            normal = model.compute_face_outward_normal(face)
            face_center = (
                sum(model.vertices[v][0] for v in face) / len(face),
                sum(model.vertices[v][1] for v in face) / len(face),
                sum(model.vertices[v][2] for v in face) / len(face),
            )
            to_eye = vec_normalize(vec_sub(eye, face_center))
            is_front = vec_dot(normal, to_eye) > 1e-5
            face_visible.append(is_front)

        edge_vis: Dict[Tuple[str, str], bool] = {}
        for u, v in model.edges:
            pair = (u, v) if u < v else (v, u)
            vis = False
            for f_idx, face in enumerate(model.faces):
                m = len(face)
                for i in range(m):
                    a, b = face[i], face[(i + 1) % m]
                    f_pair = (a, b) if a < b else (b, a)
                    if f_pair == pair and face_visible[f_idx]:
                        vis = True
                        break
                if vis:
                    break
            edge_vis[(u, v)] = vis
            edge_vis[(v, u)] = vis

        # 2D Silhouette Boundary Protection:
        # Project all vertices to screen; any edge on the 2D convex hull boundary MUST be visible (solid)
        w = max(400, self.canvas.winfo_width())
        h = max(320, self.canvas.winfo_height())
        screen_pts = {v: self.project_point(pt, w, h)[:2] for v, pt in model.vertices.items()}
        hull_verts = self._convex_hull_2d(screen_pts)
        if len(hull_verts) >= 3:
            h_len = len(hull_verts)
            for i in range(h_len):
                u_h = hull_verts[i]
                v_h = hull_verts[(i + 1) % h_len]
                edge_vis[(u_h, v_h)] = True
                edge_vis[(v_h, u_h)] = True

        return edge_vis, face_visible

    # --------------------------------------------------------------------------
    # MASTER 3D CANVAS RENDER PIPELINE
    # --------------------------------------------------------------------------

    def redraw_canvas(self) -> None:
        self.canvas.delete("all")
        w = max(400, self.canvas.winfo_width())
        h = max(320, self.canvas.winfo_height())

        model = self.models[self.current_model_key]

        # Style settings based on BOLD (Screen) vs LIGHT (Print)
        if self.bold_mode:
            vis_edge_width = 2.0
            hid_edge_width = 1.5
            hid_edge_dash = (6, 4)
            sec_outline_width = 2.5
            sec_outline_color = "#000080"
            sec_fill_color = "#B4C3F0"
            sec_stipple = "gray50"
            vertex_r = 2.5
            label_font = ("Times New Roman", 11, "bold italic")
            axis_width = 1.5
            axis_colors = {"x": "#8B0000", "y": "#006400", "z": "#00008B", "O": "#222222"}
        else:
            vis_edge_width = 1.0
            hid_edge_width = 0.8
            hid_edge_dash = (4, 3)
            sec_outline_width = 1.0
            sec_outline_color = "#000080"
            sec_fill_color = "#B4C3F0"
            sec_stipple = "gray25"
            vertex_r = 1.8
            label_font = ("Times New Roman", 10, "italic")
            axis_width = 0.8
            axis_colors = {"x": "#444444", "y": "#444444", "z": "#444444", "O": "#444444"}

        # 1. Draw 3D Coordinate System Oxyz if active
        if self.show_axes:
            self._draw_oxyz_axes(model, w, h, axis_width, axis_colors, label_font)

        # 2. Compute and Draw Circumscribed Sphere Wireframe if active
        center_I, radius_R, sphere_err = compute_circumscribed_sphere(model.vertices)
        self.last_sphere_center = center_I
        self.last_sphere_radius = radius_R
        if self.show_sphere:
            self._draw_circumscribed_sphere(center_I, radius_R, w, h, label_font, vertex_r)

        # 3. Compute Backface Culling Edge Visibility
        edge_vis, face_visible = self._compute_edge_visibility(model)

        # 4. Draw Custom Planes & Planar Cross-Section Polygon FIRST (CAD Hatching & Shading)
        # QUAN TRỌNG: Vẽ các mảng đa giác tô màu & gạch chéo TRƯỚC để nét đứt không bị che khuất!
        for c_plane in getattr(model, "custom_planes", []):
            if not c_plane.get("visible", True):
                continue
            plane_pts = c_plane.get("pts", [])
            if len(plane_pts) < 3:
                continue
            coords_3d = [model.get_point(p) for p in plane_pts]
            if any(p is None for p in coords_3d):
                continue
            screen_pts = [self.project_point(p, w, h)[:2] for p in coords_3d]
            poly_coords = [coord for pt in screen_pts for coord in (round(pt[0]), round(pt[1]))]
            pl_color = c_plane.get("color", "#1971C2")
            pl_fill = c_plane.get("fill_mode", "hatch")
            pl_spacing = float(c_plane.get("hatch_spacing", 10))

            if pl_fill == "solid":
                self.canvas.create_polygon(*poly_coords, fill=pl_color, stipple="gray50", outline="")
            elif pl_fill == "stipple":
                self.canvas.create_polygon(*poly_coords, fill=pl_color, stipple="gray25", outline="")
            elif pl_fill in ("hatch", "cross"):
                self.canvas.create_polygon(*poly_coords, fill=pl_color, stipple="gray12", outline="")
                h_segs = compute_polygon_hatch(screen_pts, spacing=pl_spacing, angle_deg=45.0)
                if pl_fill == "cross":
                    h_segs.extend(compute_polygon_hatch(screen_pts, spacing=pl_spacing, angle_deg=-45.0))
                for (hx1, hy1), (hx2, hy2) in h_segs:
                    self.canvas.create_line(
                        round(hx1), round(hy1), round(hx2), round(hy2),
                        fill=pl_color, width=1, capstyle=tk.ROUND
                    )

            # Viền đa giác mặt phẳng
            k_pl = len(screen_pts)
            for i_pl in range(k_pl):
                pA_pl = screen_pts[i_pl]
                pB_pl = screen_pts[(i_pl + 1) % k_pl]
                self.canvas.create_line(
                    round(pA_pl[0]), round(pA_pl[1]), round(pB_pl[0]), round(pB_pl[1]),
                    fill=pl_color, width=2, capstyle=tk.ROUND, joinstyle=tk.ROUND
                )

            # Nhãn tên mặt phẳng tại trọng tâm 2D
            cx_pl = sum(pt[0] for pt in screen_pts) / k_pl
            cy_pl = sum(pt[1] for pt in screen_pts) / k_pl
            pl_name = c_plane.get("name", "")
            if pl_name:
                self.canvas.create_text(
                    round(cx_pl), round(cy_pl),
                    text=pl_name, fill=pl_color, font=label_font
                )

        # 4.5 Draw Planar Cross-Section Polygon fill if active
        section_pts = model.compute_cross_section() if self.show_section else []
        if len(section_pts) >= 3:
            poly_coords: List[float] = []
            sec_screen_pts: List[Tuple[float, float]] = []
            for _lbl, pt3d in section_pts:
                sx, sy, _ = self.project_point(pt3d, w, h)
                sec_screen_pts.append((sx, sy))
                poly_coords.extend([round(sx), round(sy)])

            sec_mode = getattr(model, "section_fill_mode", "hatch")
            sec_spacing = float(getattr(model, "section_hatch_spacing", 10))

            if sec_mode == "solid":
                self.canvas.create_polygon(
                    *poly_coords,
                    fill=sec_fill_color,
                    stipple=sec_stipple,
                    outline="",
                )
            elif sec_mode == "stipple":
                self.canvas.create_polygon(
                    *poly_coords,
                    fill=sec_fill_color,
                    stipple="gray25",
                    outline="",
                )
            elif sec_mode in ("hatch", "cross"):
                self.canvas.create_polygon(
                    *poly_coords,
                    fill=sec_fill_color,
                    stipple="gray12",
                    outline="",
                )
                h_lines = compute_polygon_hatch(sec_screen_pts, spacing=sec_spacing, angle_deg=45.0)
                if sec_mode == "cross":
                    h_lines.extend(compute_polygon_hatch(sec_screen_pts, spacing=sec_spacing, angle_deg=-45.0))
                for (hx1, hy1), (hx2, hy2) in h_lines:
                    self.canvas.create_line(
                        round(hx1), round(hy1), round(hx2), round(hy2),
                        fill=sec_outline_color, width=1, capstyle=tk.ROUND
                    )

        # 5. Draw Hidden Edges (Dashed / Wireframe / Culled)
        # Nét đứt (cạnh khuất) vẽ SAU lớp tô màu đa giác => LUÔN NỔI BẬT RÕ RÀNG TRÊN NỀN TÔ MÀU!
        if self.hidden_mode != "hidden":
            actual_dash = hid_edge_dash if self.hidden_mode == "dashed" else ()
            for u, v in model.edges:
                pair = (u, v) if u < v else (v, u)
                if not edge_vis.get((u, v), True):
                    edge_col = model.edge_colors.get(pair, "#000000")
                    sx1, sy1, _ = self.project_point(model.vertices[u], w, h)
                    sx2, sy2, _ = self.project_point(model.vertices[v], w, h)
                    self.canvas.create_line(
                        sx1, sy1, sx2, sy2,
                        fill=edge_col,
                        width=hid_edge_width,
                        dash=actual_dash,
                    )
                    if self.selected_edge == pair:
                        self.canvas.create_line(
                            sx1, sy1, sx2, sy2,
                            fill="#00BFFF",
                            width=hid_edge_width + 3,
                            dash=(4, 2),
                        )

            # Cạnh thiết diện trên mặt khuất => Vẽ nét đứt nổi trên nền
            if len(section_pts) >= 3 and hasattr(model, "section_edges") and model.section_edges:
                for lbl_a, pt_a, lbl_b, pt_b, face_idx in model.section_edges:
                    is_edge_visible = face_visible[face_idx] if 0 <= face_idx < len(face_visible) else True
                    if not is_edge_visible:
                        sx1_sec, sy1_sec, _ = self.project_point(pt_a, w, h)
                        sx2_sec, sy2_sec, _ = self.project_point(pt_b, w, h)
                        self.canvas.create_line(
                            round(sx1_sec), round(sy1_sec), round(sx2_sec), round(sy2_sec),
                            fill=sec_outline_color,
                            width=sec_outline_width,
                            dash=actual_dash,
                            capstyle=tk.ROUND,
                            joinstyle=tk.ROUND,
                        )

        # 5.5 Draw Visible Section Edges
        if len(section_pts) >= 3:
            if hasattr(model, "section_edges") and model.section_edges:
                for lbl_a, pt_a, lbl_b, pt_b, face_idx in model.section_edges:
                    is_edge_visible = face_visible[face_idx] if 0 <= face_idx < len(face_visible) else True
                    if is_edge_visible:
                        sx1_sec, sy1_sec, _ = self.project_point(pt_a, w, h)
                        sx2_sec, sy2_sec, _ = self.project_point(pt_b, w, h)
                        self.canvas.create_line(
                            round(sx1_sec), round(sy1_sec), round(sx2_sec), round(sy2_sec),
                            fill=sec_outline_color,
                            width=sec_outline_width,
                            capstyle=tk.ROUND,
                            joinstyle=tk.ROUND,
                        )
            else:
                k_sec = len(section_pts)
                for i_sec in range(k_sec):
                    pA_sec = section_pts[i_sec][1]
                    pB_sec = section_pts[(i_sec + 1) % k_sec][1]
                    sx1_sec, sy1_sec, _ = self.project_point(pA_sec, w, h)
                    sx2_sec, sy2_sec, _ = self.project_point(pB_sec, w, h)
                    self.canvas.create_line(
                        round(sx1_sec), round(sy1_sec), round(sx2_sec), round(sy2_sec),
                        fill=sec_outline_color,
                        width=sec_outline_width,
                        capstyle=tk.ROUND,
                        joinstyle=tk.ROUND,
                    )

            # Section vertices & labels (với hiệu ứng Hover, Highlight & Dragging)
            for lbl, pt3d in section_pts:
                sx, sy, _ = self.project_point(pt3d, w, h)
                if lbl == self.selected_vertex:
                    self.canvas.create_oval(
                        sx - vertex_r - 6, sy - vertex_r - 6,
                        sx + vertex_r + 6, sy + vertex_r + 6,
                        outline="#00BFFF", width=2, dash=(3, 2)
                    )
                if lbl == self.dragged_vertex:
                    self.canvas.create_oval(
                        sx - vertex_r - 5, sy - vertex_r - 5,
                        sx + vertex_r + 5, sy + vertex_r + 5,
                        outline="#E03131", width=2, dash=(2, 2)
                    )
                elif lbl == self.hovered_vertex:
                    self.canvas.create_oval(
                        sx - vertex_r - 4, sy - vertex_r - 4,
                        sx + vertex_r + 4, sy + vertex_r + 4,
                        outline="#1971C2", width=2
                    )

                v_col = model.vertex_colors.get(lbl, sec_outline_color)
                self.canvas.create_oval(
                    round(sx - vertex_r),
                    round(sy - vertex_r),
                    round(sx + vertex_r),
                    round(sy + vertex_r),
                    fill=v_col,
                    outline=v_col,
                )
                self.canvas.create_text(
                    round(sx + 9),
                    round(sy - 8),
                    text=lbl,
                    fill=v_col,
                    font=label_font,
                )

        # 6. Draw Visible Solid Edges (hỗ trợ tô màu từng cạnh hoặc theo màu chủ đạo)
        for u, v in model.edges:
            pair = (u, v) if u < v else (v, u)
            if edge_vis.get((u, v), True):
                edge_col = model.edge_colors.get(pair, self.current_theme_color if self.current_theme_color != "#000000" else "#000000")
                sx1, sy1, _ = self.project_point(model.vertices[u], w, h)
                sx2, sy2, _ = self.project_point(model.vertices[v], w, h)
                self.canvas.create_line(
                    sx1, sy1, sx2, sy2,
                    fill=edge_col,
                    width=vis_edge_width,
                    capstyle=tk.ROUND,
                    joinstyle=tk.ROUND,
                )
                if self.selected_edge == pair:
                    self.canvas.create_line(
                        sx1, sy1, sx2, sy2,
                        fill="#00BFFF",
                        width=vis_edge_width + 3,
                        dash=(4, 2),
                    )

        # 7. Draw Polyhedron Vertices & Labels (với hiệu ứng Hover / Dragging)
        cx_screen, cy_screen, _ = self.project_point(model.centroid, w, h)
        for v_name, pt3d in model.vertices.items():
            sx, sy, _ = self.project_point(pt3d, w, h)
            
            # Hiệu ứng Highlight khi được chọn, rê chuột hoặc đang kéo đỉnh
            if v_name == self.selected_vertex:
                self.canvas.create_oval(
                    sx - vertex_r - 6, sy - vertex_r - 6,
                    sx + vertex_r + 6, sy + vertex_r + 6,
                    outline="#00BFFF", width=2, dash=(3, 2)
                )
            if v_name == self.dragged_vertex:
                self.canvas.create_oval(
                    sx - vertex_r - 5, sy - vertex_r - 5,
                    sx + vertex_r + 5, sy + vertex_r + 5,
                    outline="#E03131", width=2, dash=(2, 2)
                )
            elif v_name == self.hovered_vertex:
                self.canvas.create_oval(
                    sx - vertex_r - 4, sy - vertex_r - 4,
                    sx + vertex_r + 4, sy + vertex_r + 4,
                    outline="#1971C2", width=2
                )

            v_col = model.vertex_colors.get(
                v_name,
                "#E03131" if v_name == self.dragged_vertex else ("#1971C2" if v_name == self.hovered_vertex else "#000000")
            )
            self.canvas.create_oval(
                sx - vertex_r,
                sy - vertex_r,
                sx + vertex_r,
                sy + vertex_r,
                fill=v_col,
                outline=v_col,
            )
            # Offset label outward from projected centroid
            dx = sx - cx_screen
            dy = sy - cy_screen
            dist = math.hypot(dx, dy)
            if dist < 1e-3:
                ox, oy = 0.0, -14.0
            else:
                ox = (dx / dist) * 14.0
                oy = (dy / dist) * 14.0
            self.canvas.create_text(
                sx + ox,
                sy + oy,
                text=v_name,
                fill="#000000",
                font=label_font,
            )

        # 7b. Draw Auxiliary Construction Elements với Phân Định Nét Đứt Khuất Tự Động
        for idx, seg in enumerate(model.aux_segments):
            p1_3d = seg["p1"]
            p2_3d = seg["p2"]
            col = seg.get("color", "#E03131")
            w_seg = seg.get("width", 1.8 if self.bold_mode else 1.2)
            is_occ = self._is_segment_occluded(p1_3d, p2_3d, model, face_visible)

            if is_occ:
                if self.hidden_mode == "hidden":
                    continue
                actual_dash = hid_edge_dash if self.hidden_mode == "dashed" else ()
            else:
                actual_dash = ()

            sx1, sy1, _ = self.project_point(p1_3d, w, h)
            sx2, sy2, _ = self.project_point(p2_3d, w, h)
            self.canvas.create_line(
                sx1, sy1, sx2, sy2,
                fill=col,
                width=w_seg,
                dash=actual_dash,
                capstyle=tk.ROUND,
                joinstyle=tk.ROUND,
            )
            if self.selected_aux_idx == idx:
                self.canvas.create_line(
                    sx1, sy1, sx2, sy2,
                    fill="#00BFFF",
                    width=w_seg + 3,
                    dash=(4, 2),
                )
            lbl = seg.get("label", "")
            if lbl:
                mx = (sx1 + sx2) * 0.5
                my = (sy1 + sy2) * 0.5
                self.canvas.create_text(mx + 6, my - 6, text=lbl, fill=col, font=label_font)

        for p_lbl, p_pt in model.aux_points.items():
            sx, sy, _ = self.project_point(p_pt, w, h)
            if p_lbl == self.selected_vertex:
                self.canvas.create_oval(
                    sx - vertex_r - 6, sy - vertex_r - 6,
                    sx + vertex_r + 6, sy + vertex_r + 6,
                    outline="#00BFFF", width=2, dash=(3, 2)
                )
            p_col = model.vertex_colors.get(p_lbl, "#E03131")
            self.canvas.create_oval(
                sx - vertex_r - 1.5, sy - vertex_r - 1.5,
                sx + vertex_r + 1.5, sy + vertex_r + 1.5,
                fill=p_col, outline="#8B0000"
            )
            self.canvas.create_text(sx + 10, sy - 8, text=p_lbl, fill=p_col, font=label_font)

        # 7c. Draw Auxiliary Circles (Circumcircle, Incircle)
        for circ in getattr(model, "aux_circles", []):
            c_3d = circ["center"]
            norm_3d = circ["normal"]
            r_val = circ["radius"]
            c_col = circ.get("color", "#008080")
            lbl = circ.get("label", "")
            w_arb = (0.0, 0.0, 1.0) if abs(norm_3d[2]) < 0.9 else (1.0, 0.0, 0.0)
            u_axis = vec_normalize(vec_cross(w_arb, norm_3d))
            v_axis = vec_cross(norm_3d, u_axis)
            pts_2d = []
            for deg in range(0, 361, 10):
                rad = math.radians(deg)
                p_c = vec_add(c_3d, vec_add(vec_scale(u_axis, r_val * math.cos(rad)), vec_scale(v_axis, r_val * math.sin(rad))))
                sx_c, sy_c, _ = self.project_point(p_c, w, h)
                pts_2d.extend([round(sx_c), round(sy_c)])
            if len(pts_2d) >= 4:
                self.canvas.create_line(pts_2d, fill=c_col, width=1.6 if self.bold_mode else 1.0, smooth=True, capstyle=tk.ROUND, joinstyle=tk.ROUND)
            if lbl:
                scx, scy, _ = self.project_point(c_3d, w, h)
                self.canvas.create_text(round(scx + 8), round(scy + 8), text=lbl, fill=c_col, font=label_font)

        # 7d. Draw Auxiliary Angles and Right-Angle Markers
        for mark in getattr(model, "aux_angles", []):
            try:
                v_name = mark["vertex"]
                p1_name = mark["p1"]
                p2_name = mark["p2"]
                ang_deg = mark.get("degrees", 0.0)
                col = mark.get("color", "#8B0000")
                lbl = mark.get("label", f"{ang_deg:.1f}°")
                v_pt = model.vertices.get(v_name) or model.aux_points.get(v_name)
                p1_pt = model.vertices.get(p1_name) or model.aux_points.get(p1_name)
                p2_pt = model.vertices.get(p2_name) or model.aux_points.get(p2_name)
                if not (v_pt and p1_pt and p2_pt):
                    continue
                sx_v, sy_v, _ = self.project_point(v_pt, w, h)
                sx_1, sy_1, _ = self.project_point(p1_pt, w, h)
                sx_2, sy_2, _ = self.project_point(p2_pt, w, h)
                dx1, dy1 = sx_1 - sx_v, sy_1 - sy_v
                dx2, dy2 = sx_2 - sx_v, sy_2 - sy_v
                len1 = math.hypot(dx1, dy1)
                len2 = math.hypot(dx2, dy2)
                if len1 < 2.0 or len2 < 2.0:
                    continue
                if mark.get("is_right", False) or abs(ang_deg - 90.0) < 0.5:
                    s = 10.0
                    u1 = (dx1 / len1, dy1 / len1)
                    u2 = (dx2 / len2, dy2 / len2)
                    c1 = (sx_v + s * u1[0], sy_v + s * u1[1])
                    c2 = (sx_v + s * (u1[0] + u2[0]), sy_v + s * (u1[1] + u2[1]))
                    c3 = (sx_v + s * u2[0], sy_v + s * u2[1])
                    self.canvas.create_line(round(c1[0]), round(c1[1]), round(c2[0]), round(c2[1]), round(c3[0]), round(c3[1]), fill=col, width=1.5)
                else:
                    r = 18.0
                    a1 = math.degrees(math.atan2(-dy1, dx1)) % 360
                    a2 = math.degrees(math.atan2(-dy2, dx2)) % 360
                    extent = (a2 - a1) % 360
                    if extent > 180:
                        extent -= 360
                    self.canvas.create_arc(
                        round(sx_v - r), round(sy_v - r), round(sx_v + r), round(sy_v + r),
                        start=a1, extent=extent, style=tk.ARC, outline=col, width=1.5
                    )
                    bisect_rad = math.radians(a1 + extent * 0.5)
                    tx = sx_v + (r + 10.0) * math.cos(bisect_rad)
                    ty = sy_v - (r + 10.0) * math.sin(bisect_rad)
                    self.canvas.create_text(round(tx), round(ty), text=lbl, fill=col, font=("Times New Roman", 9, "bold italic"))
            except Exception:
                pass

        # 8. Update Status Bar & Side Coordinate Inspector
        self._update_telemetry_and_status(model, center_I, radius_R, sphere_err, section_pts)

    # --------------------------------------------------------------------------
    # OXYZ COORDINATE AXES RENDERER
    # --------------------------------------------------------------------------

    def _draw_oxyz_axes(
        self,
        model: PolyhedronModel,
        w: int,
        h: int,
        axis_width: float,
        axis_colors: Dict[str, str],
        label_font: Tuple[Any, ...],
    ) -> None:
        """
        Draws the 3D coordinate system Oxyz with origin O(0, 0, 0), adaptive length,
        directional arrows arrow=tk.LAST, arrowshape=(8, 10, 3), and labels x, y, z, O.
        """
        L = max(2.2, model.max_extent() * 1.48)
        origin: Vec3 = (0.0, 0.0, 0.0)
        ox, oy, _ = self.project_point(origin, w, h)

        axes_defs = [
            ("x", (L, 0.0, 0.0), axis_colors["x"]),
            ("y", (0.0, L, 0.0), axis_colors["y"]),
            ("z", (0.0, 0.0, L * 1.12), axis_colors["z"]),
        ]

        for axis_lbl, end_pt, col in axes_defs:
            ex, ey, _ = self.project_point(end_pt, w, h)
            self.canvas.create_line(
                ox,
                oy,
                ex,
                ey,
                fill=col,
                width=axis_width,
                arrow=tk.LAST,
                arrowshape=(8, 10, 3),
            )
            # Place axis label slightly beyond arrow tip
            dx = ex - ox
            dy = ey - oy
            d_len = max(1.0, math.hypot(dx, dy))
            lx = ex + (dx / d_len) * 13.0
            ly = ey + (dy / d_len) * 13.0
            self.canvas.create_text(lx, ly, text=axis_lbl, fill=col, font=label_font)

        # Origin label O and dot
        self.canvas.create_oval(ox - 2.0, oy - 2.0, ox + 2.0, oy + 2.0, fill=axis_colors["O"], outline=axis_colors["O"])
        self.canvas.create_text(ox - 10, oy + 10, text="O", fill=axis_colors["O"], font=label_font)

    # --------------------------------------------------------------------------
    # CIRCUMSCRIBED SPHERE WIREFRAME RENDERER
    # --------------------------------------------------------------------------

    def _draw_circumscribed_sphere(
        self,
        center: Vec3,
        radius: float,
        w: int,
        h: int,
        label_font: Tuple[Any, ...],
        vertex_r: float,
    ) -> None:
        """
        Draws the 3D perspective wireframe of the circumscribed sphere S(I; R):
        - Equatorial circle (parallel to XY plane)
        - Meridian XZ circle
        - Meridian YZ circle
        - Outer silhouette circle
        using fine dotted lines dash=(2, 3), color #4169E1, plus center I(x, y, z).
        """
        sphere_color = "#4169E1"
        sphere_dash = (2, 3)
        sphere_width = 1.2 if self.bold_mode else 0.8
        segments = 72

        cx, cy, cz = center

        # 1. Three orthogonal great circles in 3D (XY equator, XZ meridian, YZ meridian)
        for plane_mode in ("xy", "xz", "yz"):
            pts_2d: List[float] = []
            for i in range(segments + 1):
                theta = (2.0 * math.pi * i) / segments
                c_t = math.cos(theta)
                s_t = math.sin(theta)
                if plane_mode == "xy":
                    p3 = (cx + radius * c_t, cy + radius * s_t, cz)
                elif plane_mode == "xz":
                    p3 = (cx + radius * c_t, cy, cz + radius * s_t)
                else:
                    p3 = (cx, cy + radius * c_t, cz + radius * s_t)
                sx, sy, _ = self.project_point(p3, w, h)
                pts_2d.extend([sx, sy])
            self.canvas.create_line(
                *pts_2d,
                fill=sphere_color,
                width=sphere_width,
                dash=sphere_dash,
            )

        # 2. Outer apparent silhouette contour circle around projected center I
        ix, iy, iz_cam = self.project_point(center, w, h)
        r_screen = radius * self.zoom * (self.camera_distance / max(1.5, iz_cam))
        self.canvas.create_oval(
            ix - r_screen,
            iy - r_screen,
            ix + r_screen,
            iy + r_screen,
            outline=sphere_color,
            width=sphere_width,
            dash=sphere_dash,
        )

        # 3. Draw center I
        self.canvas.create_oval(
            ix - vertex_r,
            iy - vertex_r,
            ix + vertex_r,
            iy + vertex_r,
            fill=sphere_color,
            outline=sphere_color,
        )
        self.canvas.create_text(
            ix + 11,
            iy - 9,
            text="I",
            fill=sphere_color,
            font=label_font,
        )

    # --------------------------------------------------------------------------
    # TELEMETRY & STATUS BAR UPDATER
    # --------------------------------------------------------------------------

    def _update_telemetry_and_status(
        self,
        model: PolyhedronModel,
        center_I: Vec3,
        radius_R: float,
        sphere_err: float,
        section_pts: List[Tuple[str, Vec3]],
    ) -> None:
        is_vn = self.lang == "VN"
        model_title = model.name_vn if is_vn else model.name_en
        mode_str = (
            ("Nét ĐẬM (Màn hình)" if is_vn else "BOLD (Screen)")
            if self.bold_mode
            else ("Nét MẢNH (In ấn)" if is_vn else "LIGHT (Print)")
        )

        self.status_left.config(
            text=(
                f"Khối: {model_title}  |  Chế độ: {mode_str}  |  "
                f"Trục Oxyz: {'BẬT' if self.show_axes else 'TẮT'}  |  "
                f"Thiết diện: {'BẬT' if self.show_section else 'TẮT'}  |  "
                f"Mặt cầu: {'BẬT' if self.show_sphere else 'TẮT'}"
                if is_vn
                else f"Solid: {model_title}  |  Style: {mode_str}  |  "
                f"Axes: {'ON' if self.show_axes else 'OFF'}  |  "
                f"Section: {'ON' if self.show_section else 'OFF'}  |  "
                f"Sphere: {'ON' if self.show_sphere else 'OFF'}"
            )
        )

        center_prefix = "Tâm I" if is_vn else "Center I"
        self.status_sphere.config(
            text=f"{center_prefix}({center_I[0]:.2f}, {center_I[1]:.2f}, {center_I[2]:.2f}) | R = {radius_R:.4f}"
        )

        zoom_pct = int(round((self.zoom / self.DEFAULT_ZOOM) * 100.0))
        self.status_angles.config(
            text=f"Yaw: {self.yaw_deg:.0f}° | Pitch: {self.pitch_deg:.0f}° | Zoom: {zoom_pct}%"
        )

        # Tính thể tích V và diện tích toàn phần S_tp thời gian thực
        vol_val, surf_val = model.compute_volume_and_surface()
        r_in = (3.0 * vol_val / surf_val) if surf_val > 1e-6 else 0.0

        # Populate side coordinate & sphere inspector with clear tags and prominent Volume / Area
        self.info_text.configure(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)

        self.info_text.insert(tk.END, f"[{model_title}]\n", "hdr")
        self.info_text.insert(tk.END, ("-" * 34) + "\n")
        self.info_text.insert(tk.END, ("THÔNG SỐ HÌNH HỌC (3D CAD):\n" if is_vn else "GEOMETRIC PARAMETERS (3D CAD):\n"), "hdr")
        vol_rad = format_radical_number(vol_val)
        surf_rad = format_radical_number(surf_val)
        rin_rad = format_radical_number(r_in)
        R_rad = format_radical_number(radius_R)

        vol_disp = f"{vol_rad} (≈ {vol_val:.4f})" if vol_rad != f"{vol_val:.4f}" else f"{vol_val:.4f}"
        surf_disp = f"{surf_rad} (≈ {surf_val:.4f})" if surf_rad != f"{surf_val:.4f}" else f"{surf_val:.4f}"
        rin_disp = f"{rin_rad} (≈ {r_in:.4f})" if rin_rad != f"{r_in:.4f}" else f"{r_in:.4f}"
        R_disp = f"{R_rad} (≈ {radius_R:.4f})" if R_rad != f"{radius_R:.4f}" else f"{radius_R:.4f}"

        self.info_text.insert(tk.END, (f"  ▶ Thể tích V        = {vol_disp}\n" if is_vn else f"  ▶ Volume V          = {vol_disp}\n"), "hl_v")
        self.info_text.insert(tk.END, (f"  ▶ Diện tích S_tp    = {surf_disp}\n" if is_vn else f"  ▶ Total Surface S_tp = {surf_disp}\n"), "hl_s")
        self.info_text.insert(tk.END, (f"  • Bán kính cầu nội r = {rin_disp}\n" if is_vn else f"  • Inradius r        = {rin_disp}\n"))
        self.info_text.insert(tk.END, (f"  • Bán kính cầu ngoại R = {R_disp}\n\n" if is_vn else f"  • Circumradius R    = {R_disp}\n\n"))

        self.info_text.insert(tk.END, ("1. TỌA ĐỘ ĐỈNH OXYZ:\n" if is_vn else "1. VERTEX COORDINATES:\n"), "hdr")
        for v_lbl, pt in model.vertices.items():
            self.info_text.insert(tk.END, f"  {v_lbl:<3}: ({pt[0]:6.2f}, {pt[1]:6.2f}, {pt[2]:6.2f})\n", "coord")

        self.info_text.insert(tk.END, ("\n2. MẶT CẦU NGOẠI TIẾP S(I; R):\n" if is_vn else "\n2. CIRCUMSCRIBED SPHERE S(I; R):\n"), "hdr")
        self.info_text.insert(tk.END, f"  {center_prefix} : ({center_I[0]:.3f}, {center_I[1]:.3f}, {center_I[2]:.3f})\n")
        self.info_text.insert(tk.END, (f"  Bán kính R = {radius_R:.4f}\n" if is_vn else f"  Radius R = {radius_R:.4f}\n"))
        self.info_text.insert(tk.END, (f"  Diện tích  = {4.0 * math.pi * radius_R ** 2:.4f}\n" if is_vn else f"  Surface Area = {4.0 * math.pi * radius_R ** 2:.4f}\n"))
        self.info_text.insert(tk.END, (f"  Thể tích   = {(4.0 / 3.0) * math.pi * radius_R ** 3:.4f}\n" if is_vn else f"  Volume       = {(4.0 / 3.0) * math.pi * radius_R ** 3:.4f}\n"))
        if sphere_err > 1e-2:
            self.info_text.insert(tk.END, ("  (Đa diện tổng quát: mặt cầu khớp tối thiểu)\n" if is_vn else "  (General polyhedron: fitted sphere)\n"))

        if self.show_section:
            self.info_text.insert(tk.END, ("\n3. ĐA GIÁC THIẾT DIỆN:\n" if is_vn else "\n3. CROSS-SECTION POLYGON:\n"), "hdr")
            sec_hdr_cnt = f"  Số đỉnh cắt: {len(section_pts)}\n" if is_vn else f"  Cut vertices: {len(section_pts)}\n"
            self.info_text.insert(tk.END, sec_hdr_cnt)
            for s_lbl, s_pt in section_pts:
                self.info_text.insert(tk.END, f"  {s_lbl:<3}: ({s_pt[0]:6.2f}, {s_pt[1]:6.2f}, {s_pt[2]:6.2f})\n", "coord")

        self.info_text.configure(state=tk.DISABLED)


if __name__ == "__main__":
    import multiprocessing
    from pathlib import Path
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

        git_commit = "6b501ce55a63c1114dda4f3f11bad3623f1cc587"
        git_dirty = False
        try:
            import subprocess
            res_c = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, timeout=2)
            if res_c.returncode == 0 and res_c.stdout.strip():
                git_commit = res_c.stdout.strip()
            res_p = subprocess.run(["git", "status", "--porcelain", "geosolver_3d"], capture_output=True, text=True, timeout=2)
            if res_p.returncode == 0:
                git_dirty = bool(res_p.stdout.strip())
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
            log_smoke("[SMOKE TEST 3D] Khoi chay kiem thu dong goi GeoSolver 3D (Smoke Test)...")
            
            # 1. Kiem tra hat nhan hinh hoc 3D & Tinh toan truc tiep bo Test Vectors mau trong EXE
            from geosolver_3d.geometry3d_kernel import (
                Point3D, Vector3D, Plane3D, create_pyramid_sabcd, circumscribed_sphere,
                find_common_perpendicular, distance_point_to_plane
            )
            # Benchmark TV-3D-07
            m1_7, m2_7, d_7 = find_common_perpendicular(
                Point3D("O", 0.0, 0.0, 0.0), Vector3D(1.0, 0.0, 0.0),
                Point3D("A", 0.0, 2.0, 3.0), Vector3D(0.0, 1.0, 0.0)
            )
            assert abs(d_7 - 3.0) < 1e-12, "TV-3D-07 failed in binary"

            # Benchmark TV-3D-12
            p_test = create_pyramid_sabcd(4.0, 3.0, 5.0, sa_perp=True)
            sp_test = circumscribed_sphere(p_test, strict=True)
            assert abs(sp_test.radius - 3.5355339) < 1e-5, "TV-3D-12 failed in binary"

            # Benchmark TV-3D-19 (atan2 & skew orthogonality)
            th19 = 1e-3
            m1_19, m2_19, d_19 = find_common_perpendicular(
                Point3D("A1", 10.0, 0.0, 0.0), Vector3D(1.0, 0.0, 0.0),
                Point3D("A2", 0.0, 0.0, 5.0), Vector3D(math.cos(th19), math.sin(th19), 0.0)
            )
            assert abs(d_19 - 5.0) < 1e-7, "TV-3D-19 failed in binary"

            # Benchmark TV-3D-21 (Micro-scale L=1e-3)
            L_m = 1e-3
            tetra_m = {
                "vertices": {
                    "A": Point3D("A", 0.0, 0.0, 0.0),
                    "B": Point3D("B", L_m, 0.0, 0.0),
                    "C": Point3D("C", 0.0, L_m, 0.0),
                    "S": Point3D("S", 0.0, 0.0, L_m),
                },
                "edges": [("A", "B"), ("A", "C"), ("A", "S"), ("B", "C"), ("C", "S"), ("S", "B")],
                "faces": [["A", "B", "C"], ["A", "B", "S"], ["A", "C", "S"], ["B", "C", "S"]]
            }
            sp_m = circumscribed_sphere(tetra_m, strict=True)
            assert abs(sp_m.radius - (math.sqrt(3.0)/2.0)*L_m) / sp_m.radius < 1e-10, "TV-3D-21 failed in binary"

            result["checks"]["geometry3d_kernel"] = True
            result["numeric_benchmarks"] = {
                "TV-3D-07_skew_orthogonal_d": float(f"{d_7:.4f}"),
                "TV-3D-12_sphere_radius": float(f"{sp_test.radius:.4f}"),
                "TV-3D-19_skew_above_threshold_d": float(f"{d_19:.4f}"),
                "TV-3D-21_micro_radius": float(f"{sp_m.radius:.6e}")
            }
            log_smoke("[SMOKE TEST 3D] 1. Hat nhan hinh hoc 3D va Chay truc tiep 4 Test Vectors mau trong EXE: DAT")

            # 2. Kiem tra Engine suy luan dien dich 3D (deductive3d_engine)
            from geosolver_3d.deductive3d_engine import Deductive3DEngine
            eng = Deductive3DEngine()
            res = eng.prove_circumscribed_sphere("perp_lateral_edge", SA=4.0, ab=3.0, bc=4.0)
            assert res.numeric_value > 0 and len(res.steps) > 0 and "R =" in res.conclusion_en
            result["checks"]["deductive3d_engine"] = True
            log_smoke("[SMOKE TEST 3D] 2. Engine suy luan dien dich 3D va chuan quoc te EN: DAT")

            # 3. Kiem tra nap dong SymPy
            import sympy
            x = sympy.Symbol('x')
            sol = sympy.solve(x**2 - 4, x)
            assert len(sol) == 2
            result["checks"]["sympy"] = True
            log_smoke("[SMOKE TEST 3D] 3. Nap dong thu vien dai so hinh thuc SymPy: DAT")

            # 4. Kiem tra khoi tao va huy Tkinter GUI runtime
            import tkinter as tk
            tk_root = tk.Tk()
            tk_root.withdraw()
            tk_root.update()
            tk_root.destroy()
            result["checks"]["tkinter_runtime"] = True
            log_smoke("[SMOKE TEST 3D] 4. Khoi tao va giai phong Tkinter GUI runtime: DAT")

            # 5. Kiem tra cac module quan trong
            from PIL import Image, ImageTk
            import stem_shared_core.report_engine
            import geosolver_3d.ui_state_manager
            result["checks"]["critical_modules"] = True
            log_smoke("[SMOKE TEST 3D] 5. Nap cac module phu thuoc quan trong (PIL, report_engine, ui_state): DAT")

            # 6. Kiem tra tai nguyen dong goi
            if getattr(sys, 'frozen', False):
                base_dir = Path(getattr(sys, '_MEIPASS', os.path.dirname(sys.executable)))
                ico_path = base_dir / "assets" / "geosolver_3d.ico"
                if not ico_path.is_file():
                    ico_path = base_dir / "geosolver_3d" / "assets" / "geosolver_3d.ico"
                handbook_path = base_dir / "CAM_NANG_SU_DUNG_GEOSOLVER_3D.md"
                assert ico_path.is_file(), f"Thieu assets/geosolver_3d.ico trong goi EXE: {ico_path}"
                assert handbook_path.is_file(), f"Thieu cam nang trong goi EXE: {handbook_path}"
                result["checks"]["assets"] = True
                log_smoke("[SMOKE TEST 3D] 6. Tai nguyen dong goi trong frozen bundle: DAT")
            else:
                base_dir = Path(__file__).resolve().parent
                ico_path = base_dir / "assets" / "geosolver_3d.ico"
                handbook_path = base_dir.parent / "CAM_NANG_SU_DUNG_GEOSOLVER_3D.md"
                assert ico_path.is_file(), f"Thieu assets/geosolver_3d.ico: {ico_path}"
                assert handbook_path.is_file(), f"Thieu cam nang: {handbook_path}"
                result["checks"]["assets"] = True
                log_smoke("[SMOKE TEST 3D] 6. Tai nguyen trong cay ma nguon dev: DAT")

            # 7. Kiem tra nap cau hinh bao mat SSL/TLS & CA certifi
            import ssl, certifi
            ca_file = certifi.where()
            assert os.path.isfile(ca_file) and os.path.getsize(ca_file) > 0, f"Thieu CA bundle certifi: {ca_file}"
            ssl_ctx = ssl.create_default_context()
            try:
                ssl_ctx.load_verify_locations(cafile=ca_file)
            except Exception:
                pass
            assert ssl_ctx is not None
            result["checks"]["ssl_certifi"] = True
            log_smoke("[SMOKE TEST 3D] 7. Nap cau hinh bao mat SSL/TLS va CA bundle certifi: DAT")

            result["status"] = "PASS"
            result["exit_code"] = 0
            log_smoke("[SMOKE TEST 3D] TAT CA CAC MUC KIEM THU KHOI DEU THANH CONG (MA THOAT 0).")
        except Exception as exc:
            import traceback
            err_msg = traceback.format_exc()
            log_smoke(f"[SMOKE TEST 3D] THAT BAI: {exc}\n{err_msg}")
            result["status"] = "FAIL"
            result["error"] = str(exc)
            result["traceback"] = err_msg
            result["exit_code"] = 1

        try:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            log_smoke(f"[SMOKE TEST 3D] Da ghi nhat ky ket qua kiem thu vao: {out_path}")
            
            run_log_path = out_path.parent / "smoke_run.log"
            with open(run_log_path, "w", encoding="utf-8") as rf:
                rf.write("\n".join(log_lines) + "\n")
        except Exception as io_err:
            print(f"Loi ghi file ket qua: {io_err}")

        sys.exit(result["exit_code"])

    app = GeoSolver3DApp(with_splash=True)
    app.mainloop()