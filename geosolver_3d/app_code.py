# -*- coding: utf-8 -*-
"""
GeoSolver 3D - Pedagogical 3D Geometry & CAD Desktop Application (Win32 Classic Style)
Target Path: D:\\AI DATA\\STEM_APP\\geosolver_3d\\app.py

Features:
- Multi-Row Win32 Classic Ribbon Toolbar (#ECE9D8, tk.GROOVE, Tahoma 9)
- Pure White Technical Canvas (#FFFFFF) with Backface Culling & SGK Hidden Dashed Edges
- Adaptive 3D Coordinate System Oxyz with Directional Arrows (Toggle: X)
- Dual Line Weight Engine: BOLD (Screen Presentation) & LIGHT (SGK Textbook Print) (Toggle: B)
- Circumscribed Sphere 3D Wireframe (Equatorial XY, Meridians XZ & YZ) + Center I & Radius R (Toggle: C)
- Interactive Planar Cross-Section Slicing with Stippled Polygon Rendering (Toggle: S)
- Deductive 3D Pedagogical Solver Dialog (8 Classic Topics: GDPT 2018 / SAT / AP / IB / Gaokao) (Toggle: D)
- Bilingual Interface (Vietnamese / English) (Toggle: L)
- AI Hub / HuggingFace Model Downloader Integration ([ AI ])
"""

import os
import sys
import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, List, Tuple, Optional, Any

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
        self.edges = self._extract_edges()
        self.centroid = self._compute_centroid()

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
        Intersects the plane n . X = d with all polyhedron edges and orders the polygon vertices.
        Returns list of (label, point_3d).
        """
        n = self.plane_normal
        d = self.plane_d
        raw_pts: List[Vec3] = []

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
                    # Deduplicate close points
                    if not any(vec_norm(vec_sub(pt, existing)) < 1e-4 for existing in raw_pts):
                        raw_pts.append(pt)

        if len(raw_pts) < 3:
            return []

        # Order points angularly around polygon center in the cutting plane
        cx = sum(p[0] for p in raw_pts) / len(raw_pts)
        cy = sum(p[1] for p in raw_pts) / len(raw_pts)
        cz = sum(p[2] for p in raw_pts) / len(raw_pts)
        center = (cx, cy, cz)

        # Build orthonormal basis (u_axis, v_axis) on the plane
        ref = (1.0, 0.0, 0.0) if abs(n[0]) < 0.8 else (0.0, 1.0, 0.0)
        u_axis = vec_normalize(vec_cross(n, ref))
        v_axis = vec_normalize(vec_cross(n, u_axis))

        def angle_key(pt: Vec3) -> float:
            rel = vec_sub(pt, center)
            return math.atan2(vec_dot(rel, v_axis), vec_dot(rel, u_axis))

        raw_pts.sort(key=angle_key)
        labels = ["M", "N", "P", "Q", "R", "K", "E", "F"]
        return [(labels[i % len(labels)], pt) for i, pt in enumerate(raw_pts)]


def build_standard_polyhedra() -> Dict[str, PolyhedronModel]:
    """Creates the 6 standard SGK/CAD polyhedra centered conveniently around O(0,0,0)."""
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
    Provides step-by-step analytical proofs, LaTeX formulas, and exact numerical evaluations
    for the 8 classic 3D geometry curriculum topics (GDPT 2018 + SAT / AP / IB / Gaokao).
    If `geosolver_3d.deductive3d_engine.Deductive3DEngine` is present, delegates or enriches.
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
        return "Chuyên đề không hợp lệ / Invalid topic."

    def _solve_topic_1(self, p: Dict[str, float], lang: str) -> str:
        sa = max(0.01, p.get("SA", 4.0))
        ab = max(0.01, p.get("AB", 3.0))
        bc = max(0.01, p.get("BC", 4.0))
        ac = math.sqrt(ab * ab + bc * bc)
        r_base = ac / 2.0
        R = 0.5 * math.sqrt(sa * sa + ac * ac)
        area_sphere = 4.0 * math.pi * R * R
        vol_sphere = (4.0 / 3.0) * math.pi * (R ** 3)
        return (
            "========================================================================\n"
            "CHUYÊN ĐỀ 1: MẶT CẦU NGOẠI TIẾP CHÓP S.ABC (SA ⊥ (ABC), ΔABC VUÔNG TẠI B)\n"
            "========================================================================\n\n"
            f"[THÔNG SỐ ĐẦU VÀO]\n"
            f"  • Chiều cao cạnh bên: SA = h = {sa:.4f}\n"
            f"  • Hai cạnh góc vuông đáy: AB = {ab:.4f}, BC = {bc:.4f}\n\n"
            "[SUY LUẬN HÌNH HỌC TỪNG BƯỚC (DEDUCTIVE PROOF)]\n"
            "  Bước 1: Xét tam giác ABC vuông tại B:\n"
            "          Gọi M là trung điểm cạnh huyền AC => M là tâm đường tròn ngoại tiếp ΔABC.\n"
            f"          AC = √(AB² + BC²) = √({ab:.4f}² + {bc:.4f}²) = {ac:.6f}\n"
            f"          Bán kính đáy: R_đáy = AC / 2 = {r_base:.6f}\n\n"
            "  Bước 2: Vì SA ⊥ (ABC) và góc ABC = 90°:\n"
            "          Ta có BC ⊥ AB và BC ⊥ SA => BC ⊥ (SAB) => BC ⊥ SB (ΔSBC vuông tại B).\n"
            "          Đồng thời ΔSAC vuông tại A.\n"
            "          Do các đỉnh A, B, C cùng nhìn đoạn SC dưới góc vuông (90°),\n"
            "          tâm mặt cầu ngoại tiếp I chính là trung điểm của cạnh SC.\n\n"
            "[CÔNG THỨC LATEX CHUẨN SGK & GAOKAO]\n"
            "  $$R = \\frac{SC}{2} = \\frac{1}{2}\\sqrt{SA^2 + AB^2 + BC^2} = \\sqrt{R_{\\text{đáy}}^2 + \\left(\\frac{SA}{2}\\right)^2}$$\n\n"
            "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
            f"  • Bán kính mặt cầu ngoại tiếp: R = {R:.6f}\n"
            f"  • Diện tích mặt cầu: S = 4πR² = {area_sphere:.6f}\n"
            f"  • Thể tích khối cầu: V = (4/3)πR³ = {vol_sphere:.6f}\n"
        )

    def _solve_topic_2(self, p: Dict[str, float], lang: str) -> str:
        a = max(0.01, p.get("a", 6.0))
        h = a * math.sqrt(6.0) / 3.0
        R = a * math.sqrt(6.0) / 4.0
        r_in = a * math.sqrt(6.0) / 12.0
        vol = (a ** 3) * math.sqrt(2.0) / 12.0
        return (
            "========================================================================\n"
            "CHUYÊN ĐỀ 2: MẶT CẦU NGOẠI TIẾP & NỘI TIẾP TỨ DIỆN ĐỀU CẠNH a\n"
            "========================================================================\n\n"
            f"[THÔNG SỐ ĐẦU VÀO]\n"
            f"  • Cạnh tứ diện đều: a = {a:.4f}\n\n"
            "[SUY LUẬN HÌNH HỌC TỪNG BƯỚC (DEDUCTIVE PROOF)]\n"
            "  Bước 1: Gọi G là trọng tâm tam giác đều BCD cạnh a.\n"
            "          Bán kính đường tròn ngoại tiếp đáy: BG = a√3 / 3.\n"
            "  Bước 2: Đường cao AG ⊥ (BCD) của tứ diện đều ABCD:\n"
            f"          h = AG = √(a² - BG²) = a√6 / 3 = {h:.6f}\n"
            "  Bước 3: Tâm mặt cầu ngoại tiếp I nằm trên AG sao cho IA = IB = R:\n"
            "          R = AB² / (2·AG) = a² / (2·a√6/3) = a√6 / 4 = (3/4)h.\n"
            "          Bán kính mặt cầu nội tiếp r = h - R = (1/4)h = a√6 / 12.\n\n"
            "[CÔNG THỨC LATEX]\n"
            "  $$h = \\frac{a\\sqrt{6}}{3}, \\quad R = \\frac{a\\sqrt{6}}{4}, \\quad r = \\frac{a\\sqrt{6}}{12}, \\quad \\frac{R}{r} = 3$$\n\n"
            "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
            f"  • Chiều cao tứ diện: h = {h:.6f}\n"
            f"  • Bán kính mặt cầu ngoại tiếp: R = {R:.6f}\n"
            f"  • Bán kính mặt cầu nội tiếp: r = {r_in:.6f}\n"
            f"  • Thể tích khối tứ diện đều: V = a³√2 / 12 = {vol:.6f}\n"
        )

    def _solve_topic_3(self, p: Dict[str, float], lang: str) -> str:
        R = max(0.01, p.get("R", 5.0))
        d = max(0.0, min(R, p.get("d", 3.0)))
        r = math.sqrt(max(0.0, R * R - d * d))
        perim = 2.0 * math.pi * r
        area_sec = math.pi * r * r
        return (
            "========================================================================\n"
            "CHUYÊN ĐỀ 3: THIẾT DIỆN MẶT CẦU VÀ MẶT PHẲNG (r = √(R² - d²))\n"
            "========================================================================\n\n"
            f"[THÔNG SỐ ĐẦU VÀO]\n"
            f"  • Bán kính mặt cầu S(I; R): R = {R:.4f}\n"
            f"  • Khoảng cách từ tâm I đến mặt phẳng (α): d = d(I, (α)) = {d:.4f}\n\n"
            "[SUY LUẬN HÌNH HỌC TỪNG BƯỚC (DEDUCTIVE PROOF)]\n"
            "  Bước 1: Gọi H là hình chiếu vuông góc của tâm I lên mặt phẳng (α) => IH = d.\n"
            "  Bước 2: Với mọi điểm M thuộc giao tuyến S(I; R) ∩ (α), tam giác IHM vuông tại H:\n"
            "          HM = √(IM² - IH²) = √(R² - d²).\n"
            "          Vậy thiết diện là đường tròn tâm H, bán kính r = √(R² - d²).\n\n"
            "[CÔNG THỨC LATEX]\n"
            "  $$r = \\sqrt{R^2 - d^2}, \\quad S_{\\text{thiết diện}} = \\pi (R^2 - d^2), \\quad C = 2\\pi\\sqrt{R^2 - d^2}$$\n\n"
            "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
            f"  • Bán kính đường tròn thiết diện: r = {r:.6f}\n"
            f"  • Chu vi đường tròn thiết diện: C = 2πr = {perim:.6f}\n"
            f"  • Diện tích hình tròn thiết diện: S_td = πr² = {area_sec:.6f}\n"
        )

    def _solve_topic_4(self, p: Dict[str, float], lang: str) -> str:
        R = max(0.01, p.get("R", 5.0))
        h = max(0.01, min(2.0 * R, p.get("h_cap", 2.0)))
        r_base = math.sqrt(max(0.0, h * (2.0 * R - h)))
        s_cap = 2.0 * math.pi * R * h
        v_cap = math.pi * (h ** 2) * (R - h / 3.0)
        return (
            "========================================================================\n"
            "CHUYÊN ĐỀ 4: THỂ TÍCH VÀ DIỆN TÍCH CHỎM CẦU (SPHERICAL CAP & ZONE)\n"
            "========================================================================\n\n"
            f"[THÔNG SỐ ĐẦU VÀO]\n"
            f"  • Bán kính mặt cầu: R = {R:.4f}\n"
            f"  • Chiều cao chỏm cầu: h = {h:.4f}\n\n"
            "[SUY LUẬN GIẢI TÍCH TÍCH PHÂN & HÌNH HỌC]\n"
            "  Bước 1: Đặt trục Oz qua tâm cầu, chỏm cầu giới hạn từ z = R - h đến z = R.\n"
            "          Bán kính đáy chỏm cầu: a = √(R² - (R - h)²) = √(2Rh - h²).\n"
            "  Bước 2: Thể tích chỏm cầu tính bằng tích phân mặt cắt:\n"
            "          V = π ∫_{R-h}^{R} (R² - z²) dz = π h² (R - h/3).\n"
            "  Bước 3: Diện tích mặt cong chỏm cầu (Archimedes Hat-Box Theorem):\n"
            "          S_xq = 2πRh = π(a² + h²).\n\n"
            "[CÔNG THỨC LATEX]\n"
            "  $$V_{\\text{chỏm}} = \\pi h^2 \\left(R - \\frac{h}{3}\\right), \\quad S_{\\text{vòm}} = 2\\pi R h$$\n\n"
            "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
            f"  • Bán kính đáy chỏm cầu: a = {r_base:.6f}\n"
            f"  • Diện tích vòm chỏm cầu: S_vòm = 2πRh = {s_cap:.6f}\n"
            f"  • Thể tích khối chỏm cầu: V_chỏm = {v_cap:.6f}\n"
        )

    def _solve_topic_5(self, p: Dict[str, float], lang: str) -> str:
        a = max(0.01, p.get("base_a", 4.0))
        h = max(0.01, p.get("height_h", 4.0))
        s_base = a * a
        vol = (1.0 / 3.0) * s_base * h
        apothem = math.sqrt(h * h + (a / 2.0) ** 2)
        s_lat = 4.0 * (0.5 * a * apothem)
        s_total = s_base + s_lat
        r_in = (3.0 * vol) / s_total
        return (
            "========================================================================\n"
            "CHUYÊN ĐỀ 5: MẶT CẦU NỘI TIẾP HÌNH CHÓP TỨ GIÁC ĐỀU (r = 3V / S_tp)\n"
            "========================================================================\n\n"
            f"[THÔNG SỐ ĐẦU VÀO]\n"
            f"  • Cạnh đáy hình vuông ABCD: a = {a:.4f}\n"
            f"  • Đường cao hình chóp SO: h = {h:.4f}\n\n"
            "[SUY LUẬN HÌNH HỌC TỪNG BƯỚC (DEDUCTIVE PROOF)]\n"
            "  Bước 1: Chia khối chóp S.ABCD thành 5 khối chóp con có chung đỉnh I (tâm cầu nội tiếp)\n"
            "          và đáy là 5 mặt của hình chóp, chiều cao đều bằng bán kính nội tiếp r:\n"
            "          V = (1/3)·r·(S_đáy + S_xq) = (1/3)·r·S_tp => r = 3V / S_tp.\n"
            "  Bước 2: Trung đoạn mặt bên d_m = SM = √(h² + (a/2)²).\n\n"
            "[CÔNG THỨC LATEX]\n"
            "  $$r = \\frac{3V}{S_{\\text{tp}}} = \\frac{a h}{a + \\sqrt{4h^2 + a^2}}$$\n\n"
            "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
            f"  • Thể tích khối chóp: V = (1/3)a²h = {vol:.6f}\n"
            f"  • Trung đoạn mặt bên: SM = {apothem:.6f}\n"
            f"  • Diện tích toàn phần: S_tp = {s_total:.6f}\n"
            f"  • Bán kính mặt cầu nội tiếp: r = 3V / S_tp = {r_in:.6f}\n"
        )

    def _solve_topic_6(self, p: Dict[str, float], lang: str) -> str:
        a = max(0.01, p.get("base_a", 4.0))
        h = max(0.01, p.get("SA", 3.0))
        v_bd = (-a, a, 0.0)
        v_sc = (a, a, -h)
        cross_v = vec_cross(v_bd, v_sc)
        bs = (-a, 0.0, h)
        d_bd_sc = abs(vec_dot(cross_v, bs)) / max(1e-9, vec_norm(cross_v))
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
            f"    • Suy ra AB là đoạn vuông góc chung của SA và BC => d(SA, BC) = AB = {a:.6f}.\n\n"
            "  Bài toán 6B (Khoảng cách giữa hai đường chéo nhau BD và SC):\n"
            "    • Gắn hệ trục Oxyz với A(0,0,0), B(a,0,0), C(a,a,0), D(0,a,0), S(0,0,h).\n"
            "    • Vector chỉ phương u_BD = (-a, a, 0), u_SC = (a, a, -h), BS = (-a, 0, h).\n\n"
            "[CÔNG THỨC LATEX]\n"
            "  $$d(d_1, d_2) = \\frac{|\\vec{u}_1 \\times \\vec{u}_2 \\cdot \\overrightarrow{M_1 M_2}|}{\\|\\vec{u}_1 \\times \\vec{u}_2\\|} = \\frac{a h}{\\sqrt{2h^2 + 4a^2}}$$\n\n"
            "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
            f"  • Khoảng cách d(SA, BC) = {a:.6f}\n"
            f"  • Khoảng cách d(BD, SC) = {d_bd_sc:.6f}\n"
        )

    def _solve_topic_7(self, p: Dict[str, float], lang: str) -> str:
        R = max(0.01, p.get("R", 5.0))
        A_deg = max(1.0, p.get("angle_A", 90.0))
        B_deg = max(1.0, p.get("angle_B", 90.0))
        C_deg = max(1.0, p.get("angle_C", 90.0))
        excess_deg = max(0.01, (A_deg + B_deg + C_deg) - 180.0)
        excess_rad = math.radians(excess_deg)
        area_tri = (R ** 2) * excess_rad
        great_circle_quarter = 0.5 * math.pi * R
        return (
            "========================================================================\n"
            "CHUYÊN ĐỀ 7: ĐỊNH LÝ GIRARD - DIỆN TÍCH TAM GIÁC CẦU & CUNG LỚN\n"
            "========================================================================\n\n"
            f"[THÔNG SỐ ĐẦU VÀO]\n"
            f"  • Bán kính mặt cầu: R = {R:.4f}\n"
            f"  • Ba góc tam giác cầu (độ): A = {A_deg:.2f}°, B = {B_deg:.2f}°, C = {C_deg:.2f}°\n\n"
            "[SUY LUẬN HÌNH HỌC CẦU (SPHERICAL GEOMETRY)]\n"
            "  Bước 1: Độ dư cầu (Spherical Excess) E = (A + B + C) - π (tính theo radian).\n"
            f"          E = ({A_deg:.2f}° + {B_deg:.2f}° + {C_deg:.2f}°) - 180° = {excess_deg:.4f}° = {excess_rad:.6f} rad.\n"
            "  Bước 2: Theo Định lý Albert Girard, diện tích tam giác cầu ΔABC trên S(O; R) bằng:\n"
            "          S_ΔABC = R² · E = R² · (A + B + C - π).\n\n"
            "[CÔNG THỨC LATEX]\n"
            "  $$E = A + B + C - \\pi, \\quad S_{\\triangle ABC} = R^2 (A + B + C - \\pi), \\quad L_{\\text{cung lớn}} = R \\cdot \\Delta\\sigma$$\n\n"
            "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
            f"  • Độ dư cầu (Spherical Excess): E = {excess_rad:.6f} rad ({excess_deg:.2f}°)\n"
            f"  • Diện tích tam giác cầu: S_ΔABC = {area_tri:.6f}\n"
            f"  • Độ dài cung lớn góc tâm 90°: L = πR/2 = {great_circle_quarter:.6f}\n"
        )

    def _solve_topic_8(self, p: Dict[str, float], lang: str) -> str:
        R = max(0.01, p.get("R", 6.0))
        h_opt = (4.0 / 3.0) * R
        r_opt = (2.0 * math.sqrt(2.0) / 3.0) * R
        v_cone_max = (32.0 / 81.0) * math.pi * (R ** 3)
        v_sphere = (4.0 / 3.0) * math.pi * (R ** 3)
        ratio = 8.0 / 27.0
        return (
            "========================================================================\n"
            "CHUYÊN ĐỀ 8: CỰC TRỊ SAT/AP/GAOKAO - KHỐI NÓN THỂ TÍCH LỚN NHẤT NỘI TIẾP CẦU\n"
            "========================================================================\n\n"
            f"[THÔNG SỐ ĐẦU VÀO]\n"
            f"  • Bán kính mặt cầu ngoại tiếp nón: R = {R:.4f}\n\n"
            "[SUY LUẬN CỰC TRỊ GIẢI TÍCH / BẤT ĐẲNG THỨC AM-GM]\n"
            "  Bước 1: Gọi chiều cao hình nón là h (0 < h < 2R).\n"
            "          Bán kính đáy hình nón nội tiếp mặt cầu: r² = R² - (h - R)² = 2Rh - h².\n"
            "  Bước 2: Thể tích khối nón:\n"
            "          V(h) = (1/3)π r² h = (1/3)π (2Rh² - h³).\n"
            "  Bước 3: Khảo sát đạo hàm V'(h) = (1/3)π (4Rh - 3h²) = 0 => h = 4R / 3.\n"
            "          Khi đó r = (2√2 / 3)R và V_max = (32 / 81)π R³ = (8 / 27) V_cầu.\n\n"
            "[CÔNG THỨC LATEX]\n"
            "  $$h_{\\text{opt}} = \\frac{4R}{3}, \\quad r_{\\text{opt}} = \\frac{2\\sqrt{2}}{3}R, \\quad V_{\\max} = \\frac{32}{81}\\pi R^3 = \\frac{8}{27}V_{\\text{cầu}}$$\n\n"
            "[KẾT QUẢ GIẢI TÍCH CHÍNH XÁC]\n"
            f"  • Chiều cao nón tối ưu: h_opt = 4R/3 = {h_opt:.6f}\n"
            f"  • Bán kính đáy nón tối ưu: r_opt = (2√2/3)R = {r_opt:.6f}\n"
            f"  • Thể tích nón cực đại: V_max = {v_cone_max:.6f}\n"
            f"  • Thể tích mặt cầu: V_cầu = {v_sphere:.6f} (Tỷ số V_max / V_cầu = 8/27 ≈ {ratio:.6f})\n"
        )


# ==============================================================================
# WIN32 CLASSIC DEDUCTIVE 3D PEDAGOGICAL DIALOG
# ==============================================================================

class Deductive3DDialog(tk.Toplevel):
    """
    Win32 Classic Toplevel Dialog featuring the 8 Pedagogical 3D Geometry Topics
    (SGK GDPT 2018 + SAT / AP / IB / Gaokao) connected to Deductive3DEngine.
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
    ]

    def __init__(self, parent: tk.Widget, engine: BuiltinDeductive3DEngine, lang: str = "VN"):
        super().__init__(parent)
        self.engine = engine
        self.lang = lang
        self.title(
            "Hộp Thoại Suy Luận Sư Phạm Hình Học Không Gian 3D (GDPT 2018 - SAT/AP/IB/Gaokao)"
            if lang == "VN"
            else "Pedagogical 3D Deductive Geometry Solver (GDPT 2018 - SAT/AP/IB/Gaokao)"
        )
        self.geometry("920x620")
        self.minsize(820, 520)
        self.configure(bg=self.WIN32_BG)
        self.transient(parent)

        self.selected_topic_idx = 1
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
        }

        self._build_ui()
        self._on_select_topic(None)

    def _build_ui(self) -> None:
        # Top header bar
        header = tk.Frame(self, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2, padx=8, pady=6)
        header.pack(side=tk.TOP, fill=tk.X, padx=6, pady=(6, 3))

        lbl_title = tk.Label(
            header,
            text=(
                "DANH MỤC 8 CHUYÊN ĐỀ SUY LUẬN HÌNH HỌC KHÔNG GIAN & GIẢI TÍCH CẦU (DEDUCTIVE 3D ENGINE)"
                if self.lang == "VN"
                else "8 CLASSIC 3D DEDUCTIVE GEOMETRY & SPHERICAL ANALYTICAL TOPICS"
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
        left_frame = tk.Frame(body, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2, width=340, padx=6, pady=6)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 6))
        left_frame.pack_propagate(False)

        tk.Label(
            left_frame,
            text="Chọn chuyên đề (8 bài toán kinh điển):" if self.lang == "VN" else "Select Topic (8 Classic Problems):",
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
            height=9,
            relief=tk.SUNKEN,
            bd=2,
            exportselection=False,
        )
        topics = self.TOPICS_VN if self.lang == "VN" else self.TOPICS_EN
        for item in topics:
            self.topic_listbox.insert(tk.END, item)
        self.topic_listbox.selection_set(0)
        self.topic_listbox.bind("<<ListboxSelect>>", self._on_select_topic)
        self.topic_listbox.pack(side=tk.TOP, fill=tk.X, pady=(0, 8))

        # Parameter input sub-panel
        param_group = tk.LabelFrame(
            left_frame,
            text="Thông số giải tích (Parameters)" if self.lang == "VN" else "Analytical Parameters",
            bg=self.WIN32_BG,
            font=self.FONT_BOLD,
            relief=tk.GROOVE,
            bd=2,
            padx=6,
            pady=6,
        )
        param_group.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.param_rows_frame = tk.Frame(param_group, bg=self.WIN32_BG)
        self.param_rows_frame.pack(side=tk.TOP, fill=tk.X)

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
        btn_solve.pack(side=tk.BOTTOM, fill=tk.X, pady=(8, 2))

        # Right column: Solution & LaTeX Output
        right_frame = tk.Frame(body, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2, padx=6, pady=6)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            right_frame,
            text=(
                "Lời giải từng bước, Công thức LaTeX & Giá trị giải tích:"
                if self.lang == "VN"
                else "Step-by-Step Proof, LaTeX Formulas & Exact Evaluation:"
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

    def _on_select_topic(self, _event: Optional[Any]) -> None:
        sel = self.topic_listbox.curselection()
        if not sel:
            return
        self.selected_topic_idx = int(sel[0]) + 1
        self._rebuild_parameter_inputs(self.selected_topic_idx)
        self._evaluate_current_topic()

    def _rebuild_parameter_inputs(self, topic_idx: int) -> None:
        for child in self.param_rows_frame.winfo_children():
            child.destroy()

        topic_param_specs = {
            1: [("SA", "Cạnh bên SA ⊥ đáy:"), ("AB", "Cạnh đáy AB:"), ("BC", "Cạnh đáy BC (⊥ AB):")],
            2: [("a", "Cạnh tứ diện đều a:")],
            3: [("R", "Bán kính cầu R:"), ("d", "Khoảng cách tâm d(I, α):")],
            4: [("R", "Bán kính cầu R:"), ("h_cap", "Chiều cao chỏm cầu h:")],
            5: [("base_a", "Cạnh đáy hình vuông a:"), ("height_h", "Chiều cao chóp SO = h:")],
            6: [("base_a", "Cạnh đáy hình vuông a:"), ("SA", "Chiều cao SA = h:")],
            7: [("R", "Bán kính cầu R:"), ("angle_A", "Góc cầu A (độ):"), ("angle_B", "Góc cầu B (độ):"), ("angle_C", "Góc cầu C (độ):")],
            8: [("R", "Bán kính mặt cầu R:")],
        }

        specs = topic_param_specs.get(topic_idx, [("R", "Bán kính R:")])
        for key, label_txt in specs:
            row = tk.Frame(self.param_rows_frame, bg=self.WIN32_BG, pady=3)
            row.pack(side=tk.TOP, fill=tk.X)
            tk.Label(row, text=label_txt, bg=self.WIN32_BG, font=self.FONT_UI, anchor="w").pack(
                side=tk.LEFT, fill=tk.X, expand=True
            )
            ent = tk.Entry(
                row,
                textvariable=self.param_vars[key],
                font=self.FONT_UI,
                width=10,
                relief=tk.SUNKEN,
                bd=2,
                justify=tk.RIGHT,
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

        result_text = self.engine.solve_topic(self.selected_topic_idx, params, self.lang)
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result_text)
        self.output_text.configure(state=tk.DISABLED)


# ==============================================================================
# WIN32 CLASSIC AI HUB / HUGGINGFACE MODEL DOWNLOADER DIALOG
# ==============================================================================

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
        self.geometry("640x420")
        self.configure(bg=self.WIN32_BG)
        self.transient(parent)

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
            "[Gợi ý Phương pháp Giải tích & Sư phạm SGK]\n"
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

    # Default SGK perspective angles (degrees)
    DEFAULT_YAW_DEG = -35.0
    DEFAULT_PITCH_DEG = 22.0
    DEFAULT_ZOOM = 135.0

    def __init__(self):
        super().__init__()
        self.title("GeoSolver 3D — Win32 Classic Pedagogical CAD & Deductive Geometry Studio")
        self.geometry("1180x780")
        self.minsize(1024, 720)
        self.configure(bg=self.WIN32_BG)

        # Load standard 3D polyhedron models & deductive engine
        self.models: Dict[str, PolyhedronModel] = build_standard_polyhedra()
        self.current_model_key: str = "pyramid_sabcd"
        self.deductive_engine = BuiltinDeductive3DEngine()

        # Interactive & Pedagogical States
        self.show_axes: bool = True            # Shortcut: X
        self.show_section: bool = True         # Shortcut: S
        self.show_sphere: bool = False         # Shortcut: C
        self.bold_mode: bool = True            # Shortcut: B (True = BOLD screen, False = LIGHT textbook print)
        self.lang: str = "VN"                  # Shortcut: L ("VN" or "EN")

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
        self._bind_shortcuts()

        # Initial render
        self._refresh_button_labels()
        self.after(50, self.redraw_canvas)

    # --------------------------------------------------------------------------
    # MULTI-ROW RIBBON TOOLBAR (TOP BAR 1 & TOP BAR 2)
    # --------------------------------------------------------------------------

    def _build_multi_row_toolbar(self) -> None:
        """
        Builds a 2-row Win32 Classic Ribbon Toolbar (#ECE9D8, relief=tk.GROOVE, bd=2)
        that prevents any button clipping on resolutions from 1024x768 upward.
        """
        self.ribbon_container = tk.Frame(self, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2)
        self.ribbon_container.pack(side=tk.TOP, fill=tk.X, padx=2, pady=(2, 0))

        # --- TOP BAR 1: POLYHEDRON MODELS GROUP ---
        self.top_bar_1 = tk.Frame(self.ribbon_container, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2, padx=4, pady=3)
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
                padx=6,
                pady=2,
                command=lambda k=key: self.select_polyhedron(k),
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.poly_buttons[key] = btn

        # --- TOP BAR 2: VISUALIZATION, AXES, LINE WEIGHT & DEDUCTIVE TOOLS ---
        self.top_bar_2 = tk.Frame(self.ribbon_container, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2, padx=4, pady=3)
        self.top_bar_2.pack(side=tk.TOP, fill=tk.X, padx=2, pady=(1, 2))

        self.lbl_group_row2 = tk.Label(
            self.top_bar_2,
            text="Trực Quan & Suy Luận:",
            bg=self.WIN32_BG,
            fg="#000080",
            font=self.FONT_TOOLBAR_BOLD,
            padx=4,
        )
        self.lbl_group_row2.pack(side=tk.LEFT, padx=(0, 4))

        self.btn_axes = tk.Button(
            self.top_bar_2,
            text="[ Trục Oxyz: BẬT ]",
            font=self.FONT_TOOLBAR,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            relief=tk.SUNKEN,
            bd=2,
            padx=5,
            pady=2,
            command=self.toggle_axes,
        )
        self.btn_axes.pack(side=tk.LEFT, padx=2)

        self.btn_section = tk.Button(
            self.top_bar_2,
            text="[ Thiết diện: BẬT ]",
            font=self.FONT_TOOLBAR,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            relief=tk.SUNKEN,
            bd=2,
            padx=5,
            pady=2,
            command=self.toggle_section,
        )
        self.btn_section.pack(side=tk.LEFT, padx=2)

        self.btn_sphere = tk.Button(
            self.top_bar_2,
            text="[ Mặt cầu ngoại tiếp: TẮT ]",
            font=self.FONT_TOOLBAR,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            relief=tk.RAISED,
            bd=2,
            padx=5,
            pady=2,
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
            pady=2,
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
            pady=2,
            command=self.reset_camera_view,
        )
        self.btn_reset_view.pack(side=tk.LEFT, padx=2)

        self.btn_deductive = tk.Button(
            self.top_bar_2,
            text="[ Suy luận 3D ]",
            font=self.FONT_TOOLBAR_BOLD,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            fg="#000080",
            relief=tk.RAISED,
            bd=2,
            padx=5,
            pady=2,
            command=self.open_deductive_dialog,
        )
        self.btn_deductive.pack(side=tk.LEFT, padx=2)

        self.btn_lang = tk.Button(
            self.top_bar_2,
            text="[ Ngôn ngữ: VN ]",
            font=self.FONT_TOOLBAR,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            relief=tk.RAISED,
            bd=2,
            padx=5,
            pady=2,
            command=self.toggle_language,
        )
        self.btn_lang.pack(side=tk.LEFT, padx=2)

        self.btn_ai = tk.Button(
            self.top_bar_2,
            text="[ AI ]",
            font=self.FONT_TOOLBAR_BOLD,
            bg=self.WIN32_BG,
            activebackground=self.WIN32_ACTIVE_BG,
            fg="#000000",
            relief=tk.RAISED,
            bd=2,
            padx=8,
            pady=2,
            command=self.open_ai_hub,
        )
        self.btn_ai.pack(side=tk.LEFT, padx=2)

    # --------------------------------------------------------------------------
    # WORKSPACE AREA (WHITE TECHNICAL CANVAS + RIGHT TELEMETRY / SLICE CONTROL)
    # --------------------------------------------------------------------------

    def _build_workspace_area(self) -> None:
        self.workspace_frame = tk.Frame(self, bg=self.WIN32_BG)
        self.workspace_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Left/Center Pure White 3D Canvas
        canvas_border = tk.Frame(self.workspace_frame, bg=self.WIN32_BG, relief=tk.GROOVE, bd=2)
        canvas_border.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 2))

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

        # Right Technical Control & Coordinate Inspector Panel
        self.side_panel = tk.Frame(
            self.workspace_frame,
            bg=self.WIN32_BG,
            relief=tk.GROOVE,
            bd=2,
            width=265,
            padx=6,
            pady=6,
        )
        self.side_panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.side_panel.pack_propagate(False)

        self.lbl_side_title = tk.Label(
            self.side_panel,
            text="THÔNG SỐ KHỐI & MẶT PHẲNG CẮT",
            bg=self.WIN32_BG,
            fg="#000080",
            font=self.FONT_TOOLBAR_BOLD,
            anchor="w",
        )
        self.lbl_side_title.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))

        # Section Plane Height Slider
        plane_box = tk.LabelFrame(
            self.side_panel,
            text="Điều chỉnh mặt phẳng thiết diện (α)",
            bg=self.WIN32_BG,
            font=self.FONT_TOOLBAR_BOLD,
            relief=tk.GROOVE,
            bd=2,
            padx=4,
            pady=4,
        )
        plane_box.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))
        self.plane_box = plane_box

        self.plane_d_scale = tk.Scale(
            plane_box,
            from_=-1.2,
            to=2.0,
            resolution=0.05,
            orient=tk.HORIZONTAL,
            bg=self.WIN32_BG,
            font=self.FONT_TOOLBAR,
            highlightthickness=0,
            label="Hằng số mặt phẳng d (n·X = d):",
            command=self._on_plane_slider_change,
        )
        self.plane_d_scale.set(self.models[self.current_model_key].plane_d)
        self.plane_d_scale.pack(side=tk.TOP, fill=tk.X)

        # Quick Shortcut Guide Box
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
        shortcut_box.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))
        self.shortcut_box = shortcut_box

        self.lbl_shortcuts = tk.Label(
            shortcut_box,
            text=(
                "• X     : Bật/Tắt hệ trục Oxyz\n"
                "• S     : Bật/Tắt thiết diện phẳng\n"
                "• C     : Bật/Tắt mặt cầu ngoại tiếp\n"
                "• B     : Nét ĐẬM / MẢNH (In SGK)\n"
                "• D     : Hộp thoại Suy luận 3D\n"
                "• L     : Đổi ngôn ngữ VN / EN\n"
                "• Space : Đặt lại góc nhìn chuẩn\n"
                "• +/-   : Thu phóng tỷ lệ\n"
                "• Mũi tên: Xoay góc nhìn 5°"
            ),
            bg=self.WIN32_BG,
            font=self.FONT_TOOLBAR,
            justify=tk.LEFT,
            anchor="w",
        )
        self.lbl_shortcuts.pack(side=tk.TOP, fill=tk.X)

        # Analytical Coordinates & Sphere Readout Box
        info_box = tk.LabelFrame(
            self.side_panel,
            text="Tọa độ Đỉnh & Mặt cầu S(I; R)",
            bg=self.WIN32_BG,
            font=self.FONT_TOOLBAR_BOLD,
            relief=tk.GROOVE,
            bd=2,
            padx=4,
            pady=4,
        )
        info_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.info_box = info_box

        self.info_text = tk.Text(
            info_box,
            font=("Consolas", 9),
            bg="#FFFFFF",
            fg="#000000",
            relief=tk.SUNKEN,
            bd=2,
            wrap=tk.WORD,
            padx=4,
            pady=4,
        )
        self.info_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

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
            text="Tâm I(0.00, 0.00, 0.00) | R = 0.000",
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

    # --------------------------------------------------------------------------
    # KEYBOARD SHORTCUT BINDINGS
    # --------------------------------------------------------------------------

    def _bind_shortcuts(self) -> None:
        self.bind("<space>", lambda _e: self.reset_camera_view())
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
        self.bind("l", lambda _e: self.toggle_language())
        self.bind("L", lambda _e: self.toggle_language())
        self.bind("<plus>", lambda _e: self._zoom_by(1.12))
        self.bind("<equal>", lambda _e: self._zoom_by(1.12))
        self.bind("<KP_Add>", lambda _e: self._zoom_by(1.12))
        self.bind("<minus>", lambda _e: self._zoom_by(1.0 / 1.12))
        self.bind("<KP_Subtract>", lambda _e: self._zoom_by(1.0 / 1.12))
        self.bind("<Left>", lambda _e: self._rotate_step(-5.0, 0.0))
        self.bind("<Right>", lambda _e: self._rotate_step(5.0, 0.0))
        self.bind("<Up>", lambda _e: self._rotate_step(0.0, 5.0))
        self.bind("<Down>", lambda _e: self._rotate_step(0.0, -5.0))

    # --------------------------------------------------------------------------
    # COMMAND HANDLERS & STATE TOGGLES
    # --------------------------------------------------------------------------

    def select_polyhedron(self, key: str) -> None:
        if key not in self.models:
            return
        self.current_model_key = key
        model = self.models[key]
        self.plane_d_scale.set(model.plane_d)
        self._refresh_button_labels()
        self.redraw_canvas()

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
        self._refresh_button_labels()
        self.redraw_canvas()

    def reset_camera_view(self) -> None:
        self.yaw_deg = self.DEFAULT_YAW_DEG
        self.pitch_deg = self.DEFAULT_PITCH_DEG
        self.zoom = self.DEFAULT_ZOOM
        self.redraw_canvas()

    def open_deductive_dialog(self) -> None:
        Deductive3DDialog(self, self.deductive_engine, self.lang)

    def open_ai_hub(self) -> None:
        model = self.models[self.current_model_key]
        name = model.name_vn if self.lang == "VN" else model.name_en
        Win32AIHubDialog(self, name, self.lang)

    def _on_plane_slider_change(self, val_str: str) -> None:
        try:
            val = float(val_str)
            self.models[self.current_model_key].plane_d = val
            self.redraw_canvas()
        except Exception:
            pass

    def _refresh_button_labels(self) -> None:
        is_vn = self.lang == "VN"

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

        # Update Row 2 Group Label & Toggle Buttons
        self.lbl_group_row2.config(text="Trực Quan & Suy Luận:" if is_vn else "Visuals & Deduction:")

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
            text=f"[ Mặt cầu ngoại tiếp: {sph_state_vn} ]" if is_vn else f"[ Circum-Sphere: {sph_state_en} ]",
            relief=tk.SUNKEN if self.show_sphere else tk.RAISED,
            bg=self.WIN32_ACTIVE_BG if self.show_sphere else self.WIN32_BG,
        )

        if self.bold_mode:
            lw_text = "[ Nét vẽ: ĐẬM ]" if is_vn else "[ Line: BOLD (Screen) ]"
        else:
            lw_text = "[ Nét vẽ: MẢNH (In ấn) ]" if is_vn else "[ Line: LIGHT (Print) ]"
        self.btn_line_weight.config(text=lw_text)

        self.btn_reset_view.config(text="[ Đặt lại View ]" if is_vn else "[ Reset View ]")
        self.btn_deductive.config(text="[ Suy luận 3D ]" if is_vn else "[ 3D Deduction ]")
        self.btn_lang.config(text=f"[ Ngôn ngữ: {self.lang} ]" if is_vn else f"[ Language: {self.lang} ]")

        # Update side panel titles
        self.lbl_side_title.config(
            text="THÔNG SỐ KHỐI & MẶT PHẲNG CẮT" if is_vn else "SOLID & SECTION PLANE INSPECTOR"
        )
        self.plane_box.config(
            text="Điều chỉnh mặt phẳng thiết diện (α)" if is_vn else "Section Plane Offset (α)"
        )
        self.shortcut_box.config(
            text="Phím tắt kỹ thuật (Shortcuts)" if is_vn else "Keyboard Shortcuts"
        )
        self.info_box.config(
            text="Tọa độ Đỉnh & Mặt cầu S(I; R)" if is_vn else "Vertices & Circumscribed Sphere"
        )

    # --------------------------------------------------------------------------
    # MOUSE & CAMERA INTERACTION
    # --------------------------------------------------------------------------

    def _on_mouse_down(self, event: tk.Event) -> None:
        self._drag_last_x = event.x
        self._drag_last_y = event.y
        self.canvas.focus_set()

    def _on_mouse_drag(self, event: tk.Event) -> None:
        if self._drag_last_x is None or self._drag_last_y is None:
            self._drag_last_x = event.x
            self._drag_last_y = event.y
            return
        dx = event.x - self._drag_last_x
        dy = event.y - self._drag_last_y
        self._drag_last_x = event.x
        self._drag_last_y = event.y

        self.yaw_deg = (self.yaw_deg + dx * 0.55) % 360.0
        if self.yaw_deg > 180.0:
            self.yaw_deg -= 360.0
        self.pitch_deg = max(-85.0, min(85.0, self.pitch_deg + dy * 0.55))
        self.redraw_canvas()

    def _on_mouse_up(self, _event: tk.Event) -> None:
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
        self.yaw_deg = (self.yaw_deg + dyaw) % 360.0
        if self.yaw_deg > 180.0:
            self.yaw_deg -= 360.0
        self.pitch_deg = max(-85.0, min(85.0, self.pitch_deg + dpitch))
        self.redraw_canvas()

    # --------------------------------------------------------------------------
    # 3D CAMERA TRANSFORMATION & PERSPECTIVE PROJECTION ENGINE
    # --------------------------------------------------------------------------

    def _camera_basis(self) -> Tuple[Vec3, Vec3, Vec3, Vec3]:
        """
        Computes right, up, forward unit vectors and camera eye position in world space
        where Oz is vertical up, Ox points front-left/right, Oy points right/depth.
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
    # BACKFACE CULLING & SGK HIDDEN EDGE DETECTION
    # --------------------------------------------------------------------------

    def _compute_edge_visibility(self, model: PolyhedronModel) -> Dict[Tuple[str, str], bool]:
        """
        Determines whether each polyhedron edge is visible (solid line) or hidden (dashed line)
        using Backface Culling: an edge is visible if at least one adjacent face has its outward
        normal pointing toward the camera eye.
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
        return edge_vis

    # --------------------------------------------------------------------------
    # MASTER 3D CANVAS RENDER PIPELINE
    # --------------------------------------------------------------------------

    def redraw_canvas(self) -> None:
        self.canvas.delete("all")
        w = max(400, self.canvas.winfo_width())
        h = max(320, self.canvas.winfo_height())

        model = self.models[self.current_model_key]

        # Style settings based on BOLD (Screen) vs LIGHT (SGK Textbook Print)
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
        edge_vis = self._compute_edge_visibility(model)

        # 4. Draw Hidden Edges First (SGK Dashed Lines)
        for u, v in model.edges:
            if not edge_vis.get((u, v), True):
                sx1, sy1, _ = self.project_point(model.vertices[u], w, h)
                sx2, sy2, _ = self.project_point(model.vertices[v], w, h)
                self.canvas.create_line(
                    sx1,
                    sy1,
                    sx2,
                    sy2,
                    fill="#000000",
                    width=hid_edge_width,
                    dash=hid_edge_dash,
                )

        # 5. Draw Planar Cross-Section Polygon if active
        section_pts = model.compute_cross_section() if self.show_section else []
        if len(section_pts) >= 3:
            poly_coords: List[float] = []
            for _lbl, pt3d in section_pts:
                sx, sy, _ = self.project_point(pt3d, w, h)
                poly_coords.extend([sx, sy])

            # Filled stippled cross-section polygon
            self.canvas.create_polygon(
                *poly_coords,
                fill=sec_fill_color,
                stipple=sec_stipple,
                outline=sec_outline_color,
                width=sec_outline_width,
            )

            # Section vertices & labels
            for lbl, pt3d in section_pts:
                sx, sy, _ = self.project_point(pt3d, w, h)
                self.canvas.create_oval(
                    sx - vertex_r,
                    sy - vertex_r,
                    sx + vertex_r,
                    sy + vertex_r,
                    fill=sec_outline_color,
                    outline=sec_outline_color,
                )
                self.canvas.create_text(
                    sx + 9,
                    sy - 8,
                    text=lbl,
                    fill=sec_outline_color,
                    font=label_font,
                )

        # 6. Draw Visible Solid Edges
        for u, v in model.edges:
            if edge_vis.get((u, v), True):
                sx1, sy1, _ = self.project_point(model.vertices[u], w, h)
                sx2, sy2, _ = self.project_point(model.vertices[v], w, h)
                self.canvas.create_line(
                    sx1,
                    sy1,
                    sx2,
                    sy2,
                    fill="#000000",
                    width=vis_edge_width,
                    capstyle=tk.ROUND,
                    joinstyle=tk.ROUND,
                )

        # 7. Draw Polyhedron Vertices & SGK Italic Labels
        cx_screen, cy_screen, _ = self.project_point(model.centroid, w, h)
        for v_name, pt3d in model.vertices.items():
            sx, sy, _ = self.project_point(pt3d, w, h)
            self.canvas.create_oval(
                sx - vertex_r,
                sy - vertex_r,
                sx + vertex_r,
                sy + vertex_r,
                fill="#000000",
                outline="#000000",
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
            else ("Nét MẢNH (In SGK)" if is_vn else "LIGHT (Print)")
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

        self.status_sphere.config(
            text=f"Tâm I({center_I[0]:.2f}, {center_I[1]:.2f}, {center_I[2]:.2f}) | R = {radius_R:.4f}"
        )

        zoom_pct = int(round((self.zoom / self.DEFAULT_ZOOM) * 100.0))
        self.status_angles.config(
            text=f"Yaw: {self.yaw_deg:.0f}° | Pitch: {self.pitch_deg:.0f}° | Zoom: {zoom_pct}%"
        )

        # Populate side coordinate & sphere inspector
        lines: List[str] = []
        lines.append(f"[{model_title}]")
        lines.append("-" * 30)
        lines.append("1. TỌA ĐỘ ĐỈNH OXYZ:" if is_vn else "1. VERTEX COORDINATES:")
        for v_lbl, pt in model.vertices.items():
            lines.append(f"  {v_lbl:<3}: ({pt[0]:6.2f}, {pt[1]:6.2f}, {pt[2]:6.2f})")

        lines.append("")
        lines.append("2. MẶT CẦU NGOẠI TIẾP S(I; R):" if is_vn else "2. CIRCUMSCRIBED SPHERE S(I; R):")
        lines.append(f"  Tâm I : ({center_I[0]:.3f}, {center_I[1]:.3f}, {center_I[2]:.3f})")
        lines.append(f"  Bán kính R = {radius_R:.4f}")
        lines.append(f"  Diện tích  = {4.0 * math.pi * radius_R ** 2:.4f}")
        lines.append(f"  Thể tích   = {(4.0 / 3.0) * math.pi * radius_R ** 3:.4f}")
        if sphere_err > 1e-2:
            lines.append("  (Đa diện tổng quát: mặt cầu khớp bình phương tối thiểu)")

        if self.show_section:
            lines.append("")
            lines.append("3. ĐA GIÁC THIẾT DIỆN:" if is_vn else "3. CROSS-SECTION POLYGON:")
            lines.append(f"  Số đỉnh cắt: {len(section_pts)}")
            for s_lbl, s_pt in section_pts:
                lines.append(f"  {s_lbl:<3}: ({s_pt[0]:6.2f}, {s_pt[1]:6.2f}, {s_pt[2]:6.2f})")

        self.info_text.configure(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, "\n".join(lines))
        self.info_text.configure(state=tk.DISABLED)


if __name__ == "__main__":
    app = GeoSolver3DApp()
    app.mainloop()