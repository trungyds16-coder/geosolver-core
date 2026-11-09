# -*- coding: utf-8 -*-
"""
File: D:\\AI DATA\\STEM_APP\\geosolver_3d\\geometry3d_kernel.py
Mô tả: Hạt nhân Toán học Tính toán Hình học Không gian & Hệ thống Hình học Động (DGS)
Phiên bản R&D, Giải toán SGK & Toán Quốc tế SAT.

Hỗ trợ đầy đủ:
  1. Đối tượng Hình học Không gian cơ bản & Chuẩn hóa Tên Điểm:
     - validate_point_name(name: str) -> bool (Regex: ^[A-Z][0-9]*$)
     - Point3D(name, x, y, z)
     - Vector3D(x, y, z): dot_product, cross_product, length, normalize, rotate_around_axis
     - Plane3D(A, B, C, D): phương trình Ax + By + Cz + D = 0, Plane3D.from_three_points(P1, P2, P3)
  2. Khối Đa Diện Chuẩn SGK & Nâng Cao:
     - create_pyramid_sabcd, create_tetrahedron_sabc, create_prism_abc_a1b1c1,
       create_cuboid, create_truncated_pyramid, create_octahedron
     - rotate_polyhedron(polyhedron, axis_vec, angle_deg, pivot)
  3. Giải Toán Định Lượng Không Gian & Đường Vuông Góc Chung:
     - distance_point_to_plane, distance_point_to_line, distance_between_skew_lines,
       distance_between_lines, angle_between_two_lines, angle_between_planes, angle_line_and_plane
     - find_common_perpendicular(A1, u1, A2, u2) -> Tuple[Point3D, Point3D, float]
  4. Thuật Toán Thiết Diện, Phân Chia Đa Diện & Thể Tích:
     - intersect_plane_with_polyhedron, compute_polygon_area_and_perimeter,
       compute_polyhedron_volume, cut_polyhedron_by_plane
  5. Hệ Ràng Buộc Hình Học Động (Geometric Constraint Solver):
     - PointOnLineConstraint, PointOnPlaneConstraint, DistancePointToPlaneConstraint
     - GeometricConstraintSolver
  6. Hình Học Mặt Cầu & Tọa Độ Địa Lý (Spherical Geometry - SAT / Quốc tế):
     - Sphere3D(center, radius)
     - circumscribed_sphere(polyhedron_or_points) -> Sphere3D
     - geographic_to_cartesian(lat_deg, lon_deg, radius, center, name) -> Point3D
     - cartesian_to_geographic(pt, center) -> Tuple[float, float, float]
     - great_circle_distance(lat1_deg, lon1_deg, lat2_deg, lon2_deg, radius) -> float (Haversine)
     - spherical_triangle_area(P1, P2, P3, sphere) -> float (Định lý Girard)
     - intersect_sphere_with_plane(sphere, plane) -> Optional[Tuple[Point3D, float]]
"""

from __future__ import annotations
import math
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, TypedDict, Union, Sequence

EPSILON: float = 1e-9
TOL_PIVOT: float = 1e-10      # Ngưỡng suy biến pivot trong giải hệ khử Gauss 3x3
TOL_DET: float = 1e-8         # Ngưỡng tích hỗn tạp chuẩn hóa không thứ nguyên (Normalized Triple Product)
TOL_GEOM: float = 1e-7        # Ngưỡng khoảng cách kiểm tra mút đoạn thẳng nằm trên mặt phẳng
TOL_CCW: float = 1e-6         # Ngưỡng hình chiếu chọn vector tham chiếu không cộng tuyến trong sắp xếp CCW
TOL_SPHERE: float = 1e-4      # Dung sai tương đối kiểm định đồng cầu cospherical verification (|d - R| / max(R, 1e-12) <= tol)
TOL_SCALE_MIN: float = 1e-24  # Ngưỡng bảo vệ chia cho 0 cho tích độ dài vector thang đo micro (L >= 1e-8)
POINT_NAME_REGEX = re.compile(r"^[A-Z][0-9]*$")


def validate_point_name(name: str) -> bool:
    """
    Kiểm tra tính hợp lệ của tên điểm theo quy chuẩn DGS:
    Bắt buộc bắt đầu bằng 1 chữ cái in hoa [A-Z], theo sau bởi 0 hoặc nhiều chữ số [0-9]*
    (Ví dụ hợp lệ: 'A', 'S', 'A1', 'M12'; Từ chối: 'AB', 'a', 'S_1').
    """
    if not isinstance(name, str):
        return False
    return bool(POINT_NAME_REGEX.match(name.strip()))


# ==============================================================================
# 1. ĐỐI TƯỢNG HÌNH HỌC KHÔNG GIAN CƠ BẢN
# ==============================================================================

@dataclass(frozen=True)
class Vector3D:
    """Biểu diễn vector trong không gian Oxyz: v = (x, y, z)."""
    x: float
    y: float
    z: float

    def __add__(self, other: Vector3D) -> Vector3D:
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3D) -> Vector3D:
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> Vector3D:
        return Vector3D(self.x * float(scalar), self.y * float(scalar), self.z * float(scalar))

    def __rmul__(self, scalar: float) -> Vector3D:
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> Vector3D:
        if abs(scalar) < EPSILON:
            raise ZeroDivisionError("Không thể chia Vector3D cho 0.")
        return Vector3D(self.x / float(scalar), self.y / float(scalar), self.z / float(scalar))

    def __neg__(self) -> Vector3D:
        return Vector3D(-self.x, -self.y, -self.z)

    def dot_product(self, other: Vector3D) -> float:
        """Tích vô hướng (Dot Product): u . v = x1*x2 + y1*y2 + z1*z2."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross_product(self, other: Vector3D) -> Vector3D:
        """Tích có hướng (Cross Product): [u, v] = (y1*z2 - z1*y2, z1*x2 - x1*z2, x1*y2 - y1*x2)."""
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def length(self) -> float:
        """Độ dài (Chuẩn Euclid) của vector: |v| = sqrt(x^2 + y^2 + z^2)."""
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self) -> Vector3D:
        """Chuẩn hóa vector về độ dài đơn vị (Unit Vector)."""
        norm = self.length()
        if norm < EPSILON:
            raise ValueError("Không thể chuẩn hóa vector không (độ dài bằng 0).")
        return Vector3D(self.x / norm, self.y / norm, self.z / norm)

    def is_zero(self, tol: float = EPSILON) -> bool:
        """Kiểm tra vector có phải là vector-không hay không."""
        return self.length() < tol

    def rotate_around_axis(self, axis: Vector3D, angle_deg: float) -> Vector3D:
        """
        Xoay vector quanh trục axis một góc angle_deg (độ) theo công thức Rodrigues:
            v_rot = v*cos(theta) + (k x v)*sin(theta) + k*(k . v)*(1 - cos(theta))
        """
        if axis.is_zero():
            raise ValueError("Trục xoay không được bằng vector 0.")
        k = axis.normalize()
        theta = math.radians(float(angle_deg))
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        return (
            self * cos_t
            + k.cross_product(self) * sin_t
            + k * (k.dot_product(self) * (1.0 - cos_t))
        )

    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def to_sympy(self):
        import sympy as sp
        return (sp.nsimplify(self.x), sp.nsimplify(self.y), sp.nsimplify(self.z))

    def to_sympy_matrix(self):
        import sympy as sp
        return sp.Matrix([sp.nsimplify(self.x), sp.nsimplify(self.y), sp.nsimplify(self.z)])

    def __repr__(self) -> str:
        return f"Vector3D({self.x:.4f}, {self.y:.4f}, {self.z:.4f})"


@dataclass(frozen=True, init=False)
class Point3D:
    """Biểu diễn điểm trong không gian Oxyz: M(x, y, z) kèm định danh name."""
    name: str
    x: float
    y: float
    z: float

    def __init__(self, *args, **kwargs):
        if len(args) == 4 and isinstance(args[0], str):
            object.__setattr__(self, 'name', str(args[0]))
            object.__setattr__(self, 'x', float(args[1]))
            object.__setattr__(self, 'y', float(args[2]))
            object.__setattr__(self, 'z', float(args[3]))
        elif len(args) >= 3 and isinstance(args[0], (int, float)):
            object.__setattr__(self, 'x', float(args[0]))
            object.__setattr__(self, 'y', float(args[1]))
            object.__setattr__(self, 'z', float(args[2]))
            name_val = args[3] if len(args) > 3 else kwargs.get('name', 'P')
            object.__setattr__(self, 'name', str(name_val))
        else:
            object.__setattr__(self, 'name', str(kwargs.get('name', 'P')))
            object.__setattr__(self, 'x', float(kwargs.get('x', 0.0)))
            object.__setattr__(self, 'y', float(kwargs.get('y', 0.0)))
            object.__setattr__(self, 'z', float(kwargs.get('z', 0.0)))

    def vector_to(self, other: Point3D) -> Vector3D:
        """Tạo vector đi từ điểm hiện tại (self) tới điểm other: Vector(self -> other)."""
        return Vector3D(other.x - self.x, other.y - self.y, other.z - self.z)

    def translate(self, vec: Vector3D, new_name: Optional[str] = None) -> Point3D:
        """Tịnh tiến điểm theo vector vec."""
        return Point3D(
            name=new_name if new_name is not None else self.name,
            x=self.x + vec.x,
            y=self.y + vec.y,
            z=self.z + vec.z,
        )

    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def to_sympy(self):
        import sympy as sp
        return (sp.nsimplify(self.x), sp.nsimplify(self.y), sp.nsimplify(self.z))

    def to_sympy_matrix(self):
        import sympy as sp
        return sp.Matrix([sp.nsimplify(self.x), sp.nsimplify(self.y), sp.nsimplify(self.z)])

    def distance_to(self, other: Point3D) -> float:
        """Khoảng cách Euclid giữa hai điểm."""
        return self.vector_to(other).length()

    def midpoint_with(self, other: Point3D, name: str = "M") -> Point3D:
        """Trung điểm của đoạn thẳng nối self và other."""
        return Point3D(
            name=name,
            x=0.5 * (self.x + other.x),
            y=0.5 * (self.y + other.y),
            z=0.5 * (self.z + other.z),
        )

    def rotate_around_axis(
        self,
        axis: Vector3D,
        angle_deg: float,
        pivot: Optional[Point3D] = None,
    ) -> Point3D:
        """Xoay điểm quanh đường thẳng đi qua pivot có VTCP axis một góc angle_deg."""
        origin = pivot if pivot is not None else Point3D("O", 0.0, 0.0, 0.0)
        rel = origin.vector_to(self)
        rot_rel = rel.rotate_around_axis(axis, angle_deg)
        return origin.translate(rot_rel, new_name=self.name)

    def is_close(self, other: Point3D, tol: float = 1e-7) -> bool:
        """Kiểm tra hai điểm có trùng nhau trong phạm vi sai số tol hay không."""
        return self.distance_to(other) <= tol

    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def to_sympy(self):
        import sympy as sp
        return (sp.nsimplify(self.x), sp.nsimplify(self.y), sp.nsimplify(self.z))

    def to_sympy_matrix(self):
        import sympy as sp
        return sp.Matrix([sp.nsimplify(self.x), sp.nsimplify(self.y), sp.nsimplify(self.z)])

    def __repr__(self) -> str:
        return f"Point3D('{self.name}', {self.x:.4f}, {self.y:.4f}, {self.z:.4f})"


@dataclass(frozen=True)
class Plane3D:
    """
    Mặt phẳng trong không gian Oxyz có phương trình tổng quát:
        A*x + B*y + C*z + D = 0
    với vector pháp tuyến n = (A, B, C) khác vector-không.
    """
    A: float
    B: float
    C: float
    D: float
    name: str = "(P)"

    def __post_init__(self) -> None:
        norm_sq = self.A * self.A + self.B * self.B + self.C * self.C
        if norm_sq < EPSILON * EPSILON:
            raise ValueError("Vector pháp tuyến (A, B, C) của mặt phẳng không được bằng (0, 0, 0).")

    @property
    def normal(self) -> Vector3D:
        """Trả về vector pháp tuyến n = (A, B, C)."""
        return Vector3D(self.A, self.B, self.C)

    def evaluate(self, pt: Point3D) -> float:
        """Thay tọa độ điểm pt vào vế trái phương trình mặt phẳng: A*x + B*y + C*z + D."""
        return self.A * pt.x + self.B * pt.y + self.C * pt.z + self.D

    def signed_distance(self, pt: Point3D) -> float:
        """Khoảng cách đại số (có dấu) từ điểm pt đến mặt phẳng."""
        return self.evaluate(pt) / self.normal.length()

    def contains_point(self, pt: Point3D, tol: float = 1e-7) -> bool:
        """Kiểm tra điểm pt có thuộc mặt phẳng hay không."""
        return abs(self.signed_distance(pt)) <= tol

    def project_point(self, pt: Point3D, name: Optional[str] = None) -> Point3D:
        """Tìm hình chiếu vuông góc H của điểm pt lên mặt phẳng."""
        n = self.normal
        n_len_sq = n.dot_product(n)
        t = -self.evaluate(pt) / n_len_sq
        return Point3D(
            name=name if name is not None else pt.name,
            x=pt.x + self.A * t,
            y=pt.y + self.B * t,
            z=pt.z + self.C * t,
        )

    @classmethod
    def from_point_and_normal(cls, pt: Point3D, normal: Vector3D) -> Plane3D:
        """Khởi tạo mặt phẳng đi qua điểm pt và có vector pháp tuyến normal."""
        if normal.is_zero():
            raise ValueError("Vector pháp tuyến không hợp lệ (bằng vector 0).")
        d_val = -(normal.x * pt.x + normal.y * pt.y + normal.z * pt.z)
        return cls(normal.x, normal.y, normal.z, d_val)

    @classmethod
    def from_three_points(cls, P1: Point3D, P2: Point3D, P3: Point3D) -> Plane3D:
        """
        Khởi tạo mặt phẳng đi qua 3 điểm không thẳng hàng P1, P2, P3.
        Pháp tuyến n = [P1P2, P1P3].
        """
        v1 = P1.vector_to(P2)
        v2 = P1.vector_to(P3)
        normal = v1.cross_product(v2)
        if normal.is_zero():
            raise ValueError(
                f"Ba điểm {P1.name}, {P2.name}, {P3.name} thẳng hàng, không xác định duy nhất một mặt phẳng."
            )
        return cls.from_point_and_normal(P1, normal)

    def format_equation(self) -> str:
        """Trả về chuỗi phương trình mặt phẳng dạng chuẩn."""
        return f"{self.A:.4f}x + {self.B:.4f}y + {self.C:.4f}z + {self.D:.4f} = 0"

    def __repr__(self) -> str:
        return f"Plane3D(A={self.A:.4f}, B={self.B:.4f}, C={self.C:.4f}, D={self.D:.4f})"


# ==============================================================================
# 2. KHỐI ĐA DIỆN CHUẨN SGK & NÂNG CAO
# ==============================================================================

class PolyhedronDict(TypedDict):
    vertices: Dict[str, Point3D]
    edges: List[Tuple[str, str]]
    faces: List[List[str]]


def create_pyramid_sabcd(
    a: float = 4.0,
    b: float = 3.0,
    h: float = 5.0,
    sa_perp: bool = True,
) -> PolyhedronDict:
    """
    Khởi tạo hình chóp tứ giác S.ABCD có đáy ABCD là hình chữ nhật (AB = a, AD = b)
    nằm trên mặt phẳng Oxy (z = 0).
    """
    if a <= 0 or b <= 0 or h <= 0:
        raise ValueError("Các kích thước a, b, h của hình chóp S.ABCD phải dương.")

    A = Point3D("A", 0.0, 0.0, 0.0)
    B = Point3D("B", float(a), 0.0, 0.0)
    C = Point3D("C", float(a), float(b), 0.0)
    D = Point3D("D", 0.0, float(b), 0.0)

    if sa_perp:
        S = Point3D("S", 0.0, 0.0, float(h))
    else:
        S = Point3D("S", 0.5 * float(a), 0.5 * float(b), float(h))

    vertices: Dict[str, Point3D] = {"S": S, "A": A, "B": B, "C": C, "D": D}
    edges: List[Tuple[str, str]] = [
        ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
        ("S", "A"), ("S", "B"), ("S", "C"), ("S", "D"),
    ]
    faces: List[List[str]] = [
        ["A", "B", "C", "D"],
        ["S", "A", "B"],
        ["S", "B", "C"],
        ["S", "C", "D"],
        ["S", "D", "A"],
    ]
    return {"vertices": vertices, "edges": edges, "faces": faces}


def create_tetrahedron_sabc(
    a: float = 4.0,
    h: float = 4.0,
    sa_perp: bool = False,
) -> PolyhedronDict:
    """
    Khởi tạo hình chóp tam giác / tứ diện S.ABC có đáy ABC là tam giác đều cạnh a.
    """
    if a <= 0 or h <= 0:
        raise ValueError("Các kích thước a, h của tứ diện S.ABC phải dương.")

    A = Point3D("A", 0.0, 0.0, 0.0)
    B = Point3D("B", float(a), 0.0, 0.0)
    C = Point3D("C", 0.5 * float(a), float(a) * math.sqrt(3.0) / 2.0, 0.0)

    if sa_perp:
        S = Point3D("S", 0.0, 0.0, float(h))
    else:
        S = Point3D("S", 0.5 * float(a), float(a) * math.sqrt(3.0) / 6.0, float(h))

    vertices: Dict[str, Point3D] = {"S": S, "A": A, "B": B, "C": C}
    edges: List[Tuple[str, str]] = [
        ("A", "B"), ("B", "C"), ("C", "A"),
        ("S", "A"), ("S", "B"), ("S", "C"),
    ]
    faces: List[List[str]] = [
        ["A", "B", "C"],
        ["S", "A", "B"],
        ["S", "B", "C"],
        ["S", "C", "A"],
    ]
    return {"vertices": vertices, "edges": edges, "faces": faces}


def create_prism_abc_a1b1c1(a: float = 4.0, h: float = 5.0) -> PolyhedronDict:
    """
    Khởi tạo hình lăng trụ đứng tam giác đều ABC.A1B1C1.
    """
    if a <= 0 or h <= 0:
        raise ValueError("Các kích thước a, h của lăng trụ đứng ABC.A1B1C1 phải dương.")

    y_c = float(a) * math.sqrt(3.0) / 2.0
    A = Point3D("A", 0.0, 0.0, 0.0)
    B = Point3D("B", float(a), 0.0, 0.0)
    C = Point3D("C", 0.5 * float(a), y_c, 0.0)

    A1 = Point3D("A1", 0.0, 0.0, float(h))
    B1 = Point3D("B1", float(a), 0.0, float(h))
    C1 = Point3D("C1", 0.5 * float(a), y_c, float(h))

    vertices: Dict[str, Point3D] = {
        "A": A, "B": B, "C": C,
        "A1": A1, "B1": B1, "C1": C1,
    }
    edges: List[Tuple[str, str]] = [
        ("A", "B"), ("B", "C"), ("C", "A"),
        ("A1", "B1"), ("B1", "C1"), ("C1", "A1"),
        ("A", "A1"), ("B", "B1"), ("C", "C1"),
    ]
    faces: List[List[str]] = [
        ["A", "B", "C"],
        ["A1", "B1", "C1"],
        ["A", "B", "B1", "A1"],
        ["B", "C", "C1", "B1"],
        ["C", "A", "A1", "C1"],
    ]
    return {"vertices": vertices, "edges": edges, "faces": faces}


def create_cuboid(a: float = 4.0, b: float = 3.0, c: float = 5.0) -> PolyhedronDict:
    """
    Khởi tạo hình hộp chữ nhật ABCD.A1B1C1D1 (hoặc hình lập phương khi a = b = c).
    """
    if a <= 0 or b <= 0 or c <= 0:
        raise ValueError("Các kích thước a, b, c của hình hộp chữ nhật phải dương.")

    A = Point3D("A", 0.0, 0.0, 0.0)
    B = Point3D("B", float(a), 0.0, 0.0)
    C = Point3D("C", float(a), float(b), 0.0)
    D = Point3D("D", 0.0, float(b), 0.0)

    A1 = Point3D("A1", 0.0, 0.0, float(c))
    B1 = Point3D("B1", float(a), 0.0, float(c))
    C1 = Point3D("C1", float(a), float(b), float(c))
    D1 = Point3D("D1", 0.0, float(b), float(c))

    vertices: Dict[str, Point3D] = {
        "A": A, "B": B, "C": C, "D": D,
        "A1": A1, "B1": B1, "C1": C1, "D1": D1,
    }
    edges: List[Tuple[str, str]] = [
        ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
        ("A1", "B1"), ("B1", "C1"), ("C1", "D1"), ("D1", "A1"),
        ("A", "A1"), ("B", "B1"), ("C", "C1"), ("D", "D1"),
    ]
    faces: List[List[str]] = [
        ["A", "B", "C", "D"],
        ["A1", "B1", "C1", "D1"],
        ["A", "B", "B1", "A1"],
        ["B", "C", "C1", "B1"],
        ["C", "D", "D1", "C1"],
        ["D", "A", "A1", "D1"],
    ]
    return {"vertices": vertices, "edges": edges, "faces": faces}


def create_truncated_pyramid(
    a_bottom: float = 4.0,
    a_top: float = 2.0,
    h: float = 3.0,
    base_sides: int = 4,
) -> PolyhedronDict:
    """
    Khởi tạo hình chóp cụt đều (tứ giác đều khi base_sides=4 hoặc tam giác đều khi base_sides=3).
    """
    if a_bottom <= 0 or a_top <= 0 or h <= 0:
        raise ValueError("Các kích thước a_bottom, a_top, h của hình chóp cụt phải dương.")
    if base_sides not in (3, 4):
        raise ValueError("base_sides chỉ hỗ trợ 3 hoặc 4.")

    if base_sides == 4:
        a1 = float(a_bottom)
        a2 = float(a_top)
        offset = 0.5 * (a1 - a2)

        A = Point3D("A", 0.0, 0.0, 0.0)
        B = Point3D("B", a1, 0.0, 0.0)
        C = Point3D("C", a1, a1, 0.0)
        D = Point3D("D", 0.0, a1, 0.0)

        A1 = Point3D("A1", offset, offset, float(h))
        B1 = Point3D("B1", offset + a2, offset, float(h))
        C1 = Point3D("C1", offset + a2, offset + a2, float(h))
        D1 = Point3D("D1", offset, offset + a2, float(h))

        vertices: Dict[str, Point3D] = {
            "A": A, "B": B, "C": C, "D": D,
            "A1": A1, "B1": B1, "C1": C1, "D1": D1,
        }
        edges: List[Tuple[str, str]] = [
            ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
            ("A1", "B1"), ("B1", "C1"), ("C1", "D1"), ("D1", "A1"),
            ("A", "A1"), ("B", "B1"), ("C", "C1"), ("D", "D1"),
        ]
        faces: List[List[str]] = [
            ["A", "B", "C", "D"],
            ["A1", "B1", "C1", "D1"],
            ["A", "B", "B1", "A1"],
            ["B", "C", "C1", "B1"],
            ["C", "D", "D1", "C1"],
            ["D", "A", "A1", "D1"],
        ]
        return {"vertices": vertices, "edges": edges, "faces": faces}

    a1 = float(a_bottom)
    a2 = float(a_top)
    sqrt3 = math.sqrt(3.0)
    gx = 0.5 * a1
    gy = a1 * sqrt3 / 6.0

    A = Point3D("A", 0.0, 0.0, 0.0)
    B = Point3D("B", a1, 0.0, 0.0)
    C = Point3D("C", 0.5 * a1, a1 * sqrt3 / 2.0, 0.0)

    A1 = Point3D("A1", gx - 0.5 * a2, gy - a2 * sqrt3 / 6.0, float(h))
    B1 = Point3D("B1", gx + 0.5 * a2, gy - a2 * sqrt3 / 6.0, float(h))
    C1 = Point3D("C1", gx, gy + a2 * sqrt3 / 3.0, float(h))

    vertices_tri: Dict[str, Point3D] = {
        "A": A, "B": B, "C": C,
        "A1": A1, "B1": B1, "C1": C1,
    }
    edges_tri: List[Tuple[str, str]] = [
        ("A", "B"), ("B", "C"), ("C", "A"),
        ("A1", "B1"), ("B1", "C1"), ("C1", "A1"),
        ("A", "A1"), ("B", "B1"), ("C", "C1"),
    ]
    faces_tri: List[List[str]] = [
        ["A", "B", "C"],
        ["A1", "B1", "C1"],
        ["A", "B", "B1", "A1"],
        ["B", "C", "C1", "B1"],
        ["C", "A", "A1", "C1"],
    ]
    return {"vertices": vertices_tri, "edges": edges_tri, "faces": faces_tri}


def create_octahedron(a: float = 4.0) -> PolyhedronDict:
    """
    Khởi tạo hình bát diện đều (Regular Octahedron) cạnh a.
    """
    if a <= 0:
        raise ValueError("Cạnh a của hình bát diện đều phải dương.")

    edge = float(a)
    h_half = edge / math.sqrt(2.0)
    cx = 0.5 * edge
    cy = 0.5 * edge

    A = Point3D("A", 0.0, 0.0, h_half)
    B = Point3D("B", edge, 0.0, h_half)
    C = Point3D("C", edge, edge, h_half)
    D = Point3D("D", 0.0, edge, h_half)
    S = Point3D("S", cx, cy, 2.0 * h_half)
    S1 = Point3D("S1", cx, cy, 0.0)

    vertices: Dict[str, Point3D] = {
        "S": S, "A": A, "B": B, "C": C, "D": D, "S1": S1,
    }
    edges: List[Tuple[str, str]] = [
        ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
        ("S", "A"), ("S", "B"), ("S", "C"), ("S", "D"),
        ("S1", "A"), ("S1", "B"), ("S1", "C"), ("S1", "D"),
    ]
    faces: List[List[str]] = [
        ["S", "A", "B"],
        ["S", "B", "C"],
        ["S", "C", "D"],
        ["S", "D", "A"],
        ["S1", "B", "A"],
        ["S1", "C", "B"],
        ["S1", "D", "C"],
        ["S1", "A", "D"],
    ]
    return {"vertices": vertices, "edges": edges, "faces": faces}


def rotate_polyhedron(
    polyhedron: PolyhedronDict,
    axis: Vector3D,
    angle_deg: float,
    pivot: Optional[Point3D] = None,
) -> PolyhedronDict:
    """
    Xoay toàn bộ các đỉnh của khối đa diện quanh trục axis đi qua pivot một góc angle_deg (độ).
    Nếu pivot = None, xoay quanh gốc tọa độ O(0, 0, 0).
    """
    center_pivot = pivot if pivot is not None else Point3D("O", 0.0, 0.0, 0.0)
    rotated_vertices: Dict[str, Point3D] = {
        name: pt.rotate_around_axis(axis, angle_deg, center_pivot)
        for name, pt in polyhedron["vertices"].items()
    }
    return {
        "vertices": rotated_vertices,
        "edges": list(polyhedron["edges"]),
        "faces": [list(f) for f in polyhedron["faces"]],
    }


# ==============================================================================
# 3. GIẢI TOÁN ĐỊNH LƯỢNG & ĐƯỜNG VUÔNG GÓC CHUNG
# ==============================================================================

def distance_point_to_plane(pt: Point3D, plane: Plane3D) -> float:
    """Tính khoảng cách từ điểm pt đến mặt phẳng (plane)."""
    return abs(plane.evaluate(pt)) / plane.normal.length()


def distance_point_to_line(pt: Point3D, A: Point3D, u: Vector3D) -> float:
    """Tính khoảng cách từ điểm pt đến đường thẳng d(A, u)."""
    if u.is_zero():
        raise ValueError("Vector chỉ phương u của đường thẳng không được bằng vector 0.")
    return A.vector_to(pt).cross_product(u).length() / u.length()


def distance_between_lines(
    A1: Point3D,
    u1: Vector3D,
    A2: Point3D,
    u2: Vector3D,
) -> float:
    """
    Tính khoảng cách tổng quát giữa hai đường thẳng bất kỳ d1(A1, u1) và d2(A2, u2)
    (cắt nhau, trùng nhau, song song, chéo nhau).
    """
    if u1.is_zero() or u2.is_zero():
        raise ValueError("Vector chỉ phương của đường thẳng không được bằng vector 0.")

    w = A1.vector_to(A2)
    cross_u = u1.cross_product(u2)
    cross_len = cross_u.length()

    if cross_len > EPSILON:
        return abs(cross_u.dot_product(w)) / cross_len

    return w.cross_product(u1).length() / u1.length()


def distance_between_skew_lines(
    A1: Point3D,
    u1: Vector3D,
    A2: Point3D,
    u2: Vector3D,
) -> float:
    """Tính khoảng cách giữa hai đường thẳng chéo nhau."""
    return distance_between_lines(A1, u1, A2, u2)


def find_common_perpendicular(
    A1: Point3D,
    u1: Vector3D,
    A2: Point3D,
    u2: Vector3D,
) -> Tuple[Point3D, Point3D, float]:
    """
    Tìm tọa độ 2 điểm chân đường vuông góc chung (M1 thuộc d1, M2 thuộc d2)
    và độ dài đoạn vuông góc chung d(M1, M2) của hai đường thẳng chéo nhau hoặc song song.
    Phương pháp giải tích chính tắc chuẩn hóa vector đơn vị (Invariant Unit-Vector Projection):
      v1 = normalize(u1), v2 = normalize(u2)
      denom = |v1 x v2|^2 = sin^2(theta) >= 0 (chống triệt tiêu số học / Catastrophic Cancellation).
      Khi denom <= EPSILON (song song/trùng): M1 = A1, M2 = A2 + ((A1 - A2) . v2) * v2.
      Khi denom > EPSILON (chéo nhau):
        s = (b*e - d) / denom,  t = (e - b*d) / denom
        với w0 = A1 - A2, d = v1 . w0, e = v2 . w0.
    """
    if u1.is_zero():
        raise ValueError("Vector chỉ phương u1 không được bằng vector 0.")
    if u2.is_zero():
        raise ValueError("Vector chỉ phương u2 không được bằng vector 0.")

    v1 = u1.normalize()
    v2 = u2.normalize()
    w0 = A2.vector_to(A1)  # A1 - A2

    cross_v = v1.cross_product(v2)
    denom = cross_v.dot_product(cross_v)  # |v1 x v2|^2 = sin^2(theta) >= 0 (chống triệt tiêu số học)

    if denom <= EPSILON:
        # Hai đường thẳng song song hoặc trùng nhau (sin^2(theta) <= EPSILON)
        # Hình chiếu trực giao của A1 lên d2: M2 = A2 + ((A1 - A2) . v2) * v2
        t = w0.dot_product(v2)
        M1 = Point3D("M1", A1.x, A1.y, A1.z)
        M2 = A2.translate(v2 * t, new_name="M2")
    else:
        b = v1.dot_product(v2)
        d = v1.dot_product(w0)
        e = v2.dot_product(w0)
        s = (b * e - d) / denom
        t = (e - b * d) / denom
        M1 = A1.translate(v1 * s, new_name="M1")
        M2 = A2.translate(v2 * t, new_name="M2")

    dist = M1.distance_to(M2)
    return (M1, M2, dist)


def angle_between_two_lines(
    u1: Vector3D,
    u2: Vector3D,
    in_degrees: bool = True,
    return_both: bool = False,
) -> Union[float, Tuple[float, float]]:
    """
    Tính góc giữa hai đường thẳng có VTCP u1 và u2.
    Sử dụng atan2(|u1 x u2|, |u1 . u2|) để triệt tiêu hoàn toàn hiện tượng
    mất chữ số có nghĩa (catastrophic cancellation) của acos khi góc gần 0,
    đảm bảo kết quả ổn định số học trong miền [0, pi/2].
    """
    if u1.is_zero() or u2.is_zero():
        raise ValueError("Vector chỉ phương của đường thẳng không được bằng vector 0.")

    cross_len = u1.cross_product(u2).length()
    dot_abs = abs(u1.dot_product(u2))
    rad = math.atan2(cross_len, dot_abs)
    deg = math.degrees(rad)

    if return_both:
        return (deg, rad)
    return deg if in_degrees else rad


def angle_between_planes(
    plane1: Plane3D,
    plane2: Plane3D,
    in_degrees: bool = True,
    return_both: bool = False,
) -> Union[float, Tuple[float, float]]:
    """Tính góc giữa hai mặt phẳng (P1) và (P2) bằng atan2(|n1 x n2|, |n1 . n2|)."""
    n1 = plane1.normal
    n2 = plane2.normal
    cross_len = n1.cross_product(n2).length()
    dot_abs = abs(n1.dot_product(n2))
    rad = math.atan2(cross_len, dot_abs)
    deg = math.degrees(rad)

    if return_both:
        return (deg, rad)
    return deg if in_degrees else rad


def angle_line_and_plane(
    dir_vec: Vector3D,
    plane: Plane3D,
    in_degrees: bool = True,
    return_both: bool = False,
) -> Union[float, Tuple[float, float]]:
    """Tính góc giữa đường thẳng (VTCP dir_vec) và mặt phẳng (VTPT n) bằng atan2(|dir . n|, |dir x n|)."""
    if dir_vec.is_zero():
        raise ValueError("Vector chỉ phương dir_vec không được bằng vector 0.")

    n = plane.normal
    dot_abs = abs(dir_vec.dot_product(n))
    cross_len = dir_vec.cross_product(n).length()
    rad = math.atan2(dot_abs, cross_len)
    deg = math.degrees(rad)

    if return_both:
        return (deg, rad)
    return deg if in_degrees else rad


# ==============================================================================
# 4. THUẬT TOÁN THIẾT DIỆN, PHÂN CHIA ĐA DIỆN & THỂ TÍCH
# ==============================================================================

def _intersect_segment_with_plane(
    P1: Point3D,
    P2: Point3D,
    plane: Plane3D,
    tol: float = TOL_GEOM,
) -> List[Point3D]:
    """Tìm giao điểm của đoạn thẳng P1P2 với mặt phẳng plane."""
    f1 = plane.evaluate(P1)
    f2 = plane.evaluate(P2)
    norm_len = plane.normal.length()
    d1 = f1 / norm_len
    d2 = f2 / norm_len

    on_p1 = abs(d1) <= tol
    on_p2 = abs(d2) <= tol

    if on_p1 and on_p2:
        return [P1, P2]
    if on_p1:
        return [P1]
    if on_p2:
        return [P2]

    if (f1 < 0.0 and f2 > 0.0) or (f1 > 0.0 and f2 < 0.0):
        t = -f1 / (f2 - f1)
        t = max(0.0, min(1.0, t))
        ix = P1.x + t * (P2.x - P1.x)
        iy = P1.y + t * (P2.y - P1.y)
        iz = P1.z + t * (P2.z - P1.z)
        inter_name = f"I_{P1.name}{P2.name}"
        return [Point3D(inter_name, ix, iy, iz)]

    return []


def _sort_coplanar_points_ccw(
    points: List[Point3D],
    normal: Vector3D,
    tol: float = TOL_CCW,
) -> List[Point3D]:
    """
    Sắp xếp các điểm đồng phẳng theo góc cực ngược chiều kim đồng hồ quanh trọng tâm C.
    Tham số tol: ngưỡng độ dài hình chiếu để chọn vector tham chiếu không cộng tuyến.
    """
    if len(points) < 3:
        return points

    n_pts = float(len(points))
    cx = sum(p.x for p in points) / n_pts
    cy = sum(p.y for p in points) / n_pts
    cz = sum(p.z for p in points) / n_pts
    centroid = Point3D("Centroid", cx, cy, cz)

    n_unit = normal.normalize()
    ref_vec: Optional[Vector3D] = None
    for p in points:
        candidate = centroid.vector_to(p)
        candidate = candidate - n_unit * candidate.dot_product(n_unit)
        if candidate.length() > tol:
            ref_vec = candidate.normalize()
            break

    if ref_vec is None:
        return points

    e1 = ref_vec
    e2 = n_unit.cross_product(e1).normalize()

    def polar_angle(pt: Point3D) -> float:
        rel = centroid.vector_to(pt)
        return math.atan2(rel.dot_product(e2), rel.dot_product(e1))

    return sorted(points, key=polar_angle)


def intersect_plane_with_polyhedron(
    polyhedron: PolyhedronDict,
    plane: Plane3D,
    tol: float = 1e-6,
) -> List[Point3D]:
    """Tìm đa giác thiết diện tạo bởi mặt phẳng cắt (plane) và khối đa diện (polyhedron)."""
    vertices_map: Dict[str, Point3D] = polyhedron["vertices"]
    edges: List[Tuple[str, str]] = polyhedron["edges"]

    raw_points: List[Point3D] = []
    for u_name, v_name in edges:
        P1 = vertices_map[u_name]
        P2 = vertices_map[v_name]
        pts = _intersect_segment_with_plane(P1, P2, plane, tol=tol)
        raw_points.extend(pts)

    unique_points: List[Point3D] = []
    for pt in raw_points:
        duplicate_idx: Optional[int] = None
        for idx, existing in enumerate(unique_points):
            if pt.is_close(existing, tol=tol):
                duplicate_idx = idx
                break
        if duplicate_idx is None:
            unique_points.append(pt)
        else:
            if not pt.name.startswith("I_") and unique_points[duplicate_idx].name.startswith("I_"):
                unique_points[duplicate_idx] = pt

    if len(unique_points) < 3:
        return unique_points

    return _sort_coplanar_points_ccw(unique_points, plane.normal, tol=tol)


def compute_polygon_area_and_perimeter(polygon: List[Point3D]) -> Tuple[float, float]:
    """Tính diện tích (Area) và chu vi (Perimeter) của đa giác phẳng 3D."""
    n = len(polygon)
    if n < 3:
        return (0.0, 0.0)

    perimeter = 0.0
    for i in range(n):
        perimeter += polygon[i].distance_to(polygon[(i + 1) % n])

    p0 = polygon[0]
    total_cross = Vector3D(0.0, 0.0, 0.0)
    for i in range(1, n - 1):
        v1 = p0.vector_to(polygon[i])
        v2 = p0.vector_to(polygon[i + 1])
        total_cross = total_cross + v1.cross_product(v2)

    area = 0.5 * total_cross.length()
    return (area, perimeter)


def compute_polyhedron_volume(polyhedron: PolyhedronDict) -> float:
    """
    Tính thể tích khối đa diện lồi bằng phương pháp phân rã tứ diện từ tâm hình học G.
    Thực hiện kiểm tra nghiêm ngặt (Strict Validation) tính tồn tại của các đỉnh trong mặt.
    """
    vertices_map = polyhedron["vertices"]
    faces = polyhedron["faces"]
    if len(vertices_map) < 4 or len(faces) < 4:
        return 0.0

    all_pts = list(vertices_map.values())
    n_verts = float(len(all_pts))
    gx = sum(p.x for p in all_pts) / n_verts
    gy = sum(p.y for p in all_pts) / n_verts
    gz = sum(p.z for p in all_pts) / n_verts
    G = Point3D("G_vol", gx, gy, gz)

    total_volume = 0.0
    for face_names in faces:
        face_pts = []
        for name in face_names:
            if name not in vertices_map:
                raise KeyError(f"Đỉnh '{name}' trong mặt không tồn tại trong danh sách đỉnh của khối đa diện.")
            face_pts.append(vertices_map[name])

        if len(face_pts) < 3:
            raise ValueError(f"Mặt {face_names} có ít hơn 3 đỉnh hợp lệ để xác định mặt phẳng.")

        p0 = face_pts[0]
        face_normal: Optional[Vector3D] = None
        for i in range(1, len(face_pts) - 1):
            v_a = p0.vector_to(face_pts[i])
            v_b = p0.vector_to(face_pts[i + 1])
            cand_n = v_a.cross_product(v_b)
            scale_ab = v_a.length() * v_b.length()
            if scale_ab > TOL_SCALE_MIN and (cand_n.length() / scale_ab) > TOL_DET:
                face_normal = cand_n
                break
        if face_normal is None:
            raise ValueError(f"Mặt {face_names} có các đỉnh suy biến đồng tuyến, không xác định được pháp tuyến.")

        ordered_face = _sort_coplanar_points_ccw(face_pts, face_normal, tol=TOL_CCW)
        v0 = ordered_face[0]
        gv0 = G.vector_to(v0)
        for i in range(1, len(ordered_face) - 1):
            gvi = G.vector_to(ordered_face[i])
            gvi1 = G.vector_to(ordered_face[i + 1])
            tetra_vol = abs(gv0.cross_product(gvi).dot_product(gvi1)) / 6.0
            total_volume += tetra_vol

    return total_volume


def _build_half_space_polyhedron(
    polyhedron: PolyhedronDict,
    plane: Plane3D,
    keep_positive: bool,
    tol: float = 1e-6,
) -> PolyhedronDict:
    """Xây dựng khối đa diện con nằm trong nửa không gian dương hoặc âm của plane."""
    orig_vertices = polyhedron["vertices"]
    new_vertices: Dict[str, Point3D] = {}

    def register_point(pt: Point3D) -> str:
        for existing_name, existing_pt in new_vertices.items():
            if pt.is_close(existing_pt, tol=tol):
                return existing_name
        new_vertices[pt.name] = pt
        return pt.name

    def is_inside(pt: Point3D) -> bool:
        sd = plane.signed_distance(pt)
        return (sd >= -tol) if keep_positive else (sd <= tol)

    clipped_faces: List[List[str]] = []
    for face_names in polyhedron["faces"]:
        face_pts = [orig_vertices[name] for name in face_names if name in orig_vertices]
        if len(face_pts) < 3:
            continue

        face_normal: Optional[Vector3D] = None
        for i in range(1, len(face_pts) - 1):
            n_cand = face_pts[0].vector_to(face_pts[i]).cross_product(face_pts[0].vector_to(face_pts[i + 1]))
            if not n_cand.is_zero(1e-8):
                face_normal = n_cand
                break
        if face_normal is None:
            continue

        face_candidates: List[Point3D] = []
        k = len(face_pts)
        for i in range(k):
            curr_pt = face_pts[i]
            next_pt = face_pts[(i + 1) % k]
            if is_inside(curr_pt):
                face_candidates.append(curr_pt)
            inter_pts = _intersect_segment_with_plane(curr_pt, next_pt, plane, tol=tol)
            for ip in inter_pts:
                face_candidates.append(ip)

        unique_face_pts: List[Point3D] = []
        for pt in face_candidates:
            dup_idx: Optional[int] = None
            for idx, ex in enumerate(unique_face_pts):
                if pt.is_close(ex, tol=tol):
                    dup_idx = idx
                    break
            if dup_idx is None:
                unique_face_pts.append(pt)
            else:
                if not pt.name.startswith("I_") and unique_face_pts[dup_idx].name.startswith("I_"):
                    unique_face_pts[dup_idx] = pt

        if len(unique_face_pts) >= 3:
            sorted_face_pts = _sort_coplanar_points_ccw(unique_face_pts, face_normal, tol=tol)
            area, _ = compute_polygon_area_and_perimeter(sorted_face_pts)
            if area > tol * tol:
                face_vertex_names = [register_point(p) for p in sorted_face_pts]
                clipped_faces.append(face_vertex_names)

    cross_section = intersect_plane_with_polyhedron(polyhedron, plane, tol=tol)
    if len(cross_section) >= 3:
        cap_normal = (-plane.normal) if keep_positive else plane.normal
        sorted_cap = _sort_coplanar_points_ccw(cross_section, cap_normal, tol=tol)
        cap_names = [register_point(p) for p in sorted_cap]
        cap_set = set(cap_names)
        if not any(set(existing_face) == cap_set for existing_face in clipped_faces):
            clipped_faces.append(cap_names)

    edges_set: List[Tuple[str, str]] = []
    seen_pairs = set()
    for f in clipped_faces:
        m = len(f)
        for i in range(m):
            u, v = f[i], f[(i + 1) % m]
            if u == v:
                continue
            pair_key = (u, v) if u < v else (v, u)
            if pair_key not in seen_pairs:
                seen_pairs.add(pair_key)
                edges_set.append((u, v))

    return {
        "vertices": new_vertices,
        "edges": edges_set,
        "faces": clipped_faces,
    }


def cut_polyhedron_by_plane(
    polyhedron: PolyhedronDict,
    plane: Plane3D,
    tol: float = 1e-6,
) -> Tuple[PolyhedronDict, PolyhedronDict]:
    """Chia khối đa diện thành 2 phần (upper_polyhedron, lower_polyhedron) bởi mặt phẳng plane."""
    upper_poly = _build_half_space_polyhedron(polyhedron, plane, keep_positive=True, tol=tol)
    lower_poly = _build_half_space_polyhedron(polyhedron, plane, keep_positive=False, tol=tol)
    return (upper_poly, lower_poly)


# ==============================================================================
# 5. HỆ RÀNG BUỘC HÌNH HỌC ĐỘNG (GEOMETRIC CONSTRAINT SOLVER - DGS)
# ==============================================================================

@dataclass(frozen=True)
class PointOnLineConstraint:
    """
    Ràng buộc điểm trượt trên đường thẳng d đi qua line_origin với VTCP line_dir.
    Phép chiếu đại số: P_proj = A + ((AP . u) / |u|^2) * u.
    """
    point_name: str
    line_origin: Point3D
    line_dir: Vector3D

    def enforce(self, pt: Point3D) -> Point3D:
        if self.line_dir.is_zero():
            raise ValueError("Vector chỉ phương của PointOnLineConstraint không được bằng 0.")
        u = self.line_dir
        ap = self.line_origin.vector_to(pt)
        t = ap.dot_product(u) / u.dot_product(u)
        return self.line_origin.translate(u * t, new_name=pt.name)


@dataclass(frozen=True)
class PointOnPlaneConstraint:
    """
    Ràng buộc điểm trượt trên mặt phẳng plane.
    Phép chiếu đại số: P_proj = plane.project_point(pt).
    """
    point_name: str
    plane: Plane3D

    def enforce(self, pt: Point3D) -> Point3D:
        return self.plane.project_point(pt, name=pt.name)


@dataclass(frozen=True)
class DistancePointToPlaneConstraint:
    """
    Ràng buộc khoảng cách từ điểm đến mặt phẳng plane luôn không đổi và bằng distance (>= 0).
    Phép chiếu đại số:
      Gọi H là hình chiếu vuông góc của pt lên plane, n_unit là pháp tuyến đơn vị của plane.
      Giữ nguyên dấu nửa không gian hiện tại của pt (hoặc hướng +n_unit nếu pt nằm trên mặt phẳng):
      P_proj = H + sign * distance * n_unit.
    """
    point_name: str
    plane: Plane3D
    distance: float

    def __post_init__(self) -> None:
        if self.distance < 0:
            raise ValueError("Khoảng cách trong DistancePointToPlaneConstraint phải không âm.")

    def enforce(self, pt: Point3D) -> Point3D:
        sd = self.plane.signed_distance(pt)
        sign = 1.0 if sd >= 0.0 else -1.0
        h_proj = self.plane.project_point(pt, name=pt.name)
        n_unit = self.plane.normal.normalize()
        return h_proj.translate(n_unit * (sign * float(self.distance)), new_name=pt.name)


ConstraintType = Union[PointOnLineConstraint, PointOnPlaneConstraint, DistancePointToPlaneConstraint]


class GeometricConstraintSolver:
    """
    Bộ giải ràng buộc hình học động (DGS Solver):
    Quản lý danh sách các ràng buộc và tự động chiếu đại số tọa độ đỉnh khi người dùng kéo thả.
    """

    def __init__(self) -> None:
        self._constraints: Dict[str, List[ConstraintType]] = {}

    def add_constraint(self, constraint: ConstraintType) -> None:
        name = constraint.point_name
        if name not in self._constraints:
            self._constraints[name] = []
        self._constraints[name].append(constraint)

    def clear_constraints(self, point_name: Optional[str] = None) -> None:
        if point_name is None:
            self._constraints.clear()
        else:
            self._constraints.pop(point_name, None)

    def solve_point(self, pt: Point3D, iterations: int = 4) -> Point3D:
        """Áp dụng tuần tự các phép chiếu đại số cho điểm pt."""
        constraints = self._constraints.get(pt.name, [])
        if not constraints:
            return pt
        current = pt
        for _ in range(max(1, iterations)):
            for c in constraints:
                current = c.enforce(current)
        return current

    def solve_polyhedron(self, polyhedron: PolyhedronDict, iterations: int = 4) -> PolyhedronDict:
        """Hiệu chỉnh toàn bộ các đỉnh của khối đa diện theo hệ ràng buộc hiện hành."""
        updated_vertices: Dict[str, Point3D] = {
            name: self.solve_point(pt, iterations=iterations)
            for name, pt in polyhedron["vertices"].items()
        }
        return {
            "vertices": updated_vertices,
            "edges": list(polyhedron["edges"]),
            "faces": [list(f) for f in polyhedron["faces"]],
        }


# ==============================================================================
# 6. HÌNH HỌC MẶT CẦU & TỌA ĐỘ ĐỊA LÝ (SPHERICAL GEOMETRY - SAT / QUỐC TẾ)
# ==============================================================================

@dataclass(frozen=True)
class Sphere3D:
    """Biểu diễn mặt cầu tâm center(x_I, y_I, z_I) và bán kính radius > 0."""
    center: Point3D
    radius: float

    def __post_init__(self) -> None:
        if self.radius <= 0:
            raise ValueError("Bán kính mặt cầu phải lớn hơn 0.")

    @property
    def surface_area(self) -> float:
        """Diện tích mặt cầu: S = 4 * pi * R^2."""
        return 4.0 * math.pi * self.radius * self.radius

    @property
    def volume(self) -> float:
        """Thể tích khối cầu: V = (4/3) * pi * R^3."""
        return (4.0 / 3.0) * math.pi * (self.radius ** 3)

    def contains_point(self, pt: Point3D, tol: float = 1e-5) -> bool:
        """Kiểm tra điểm pt có nằm trên bề mặt cầu hay không."""
        return abs(self.center.distance_to(pt) - self.radius) <= tol

    def format_equation(self) -> str:
        c = self.center
        return f"(x - {c.x:.2f})² + (y - {c.y:.2f})² + (z - {c.z:.2f})² = {self.radius ** 2:.4f}"


def _solve_linear_3x3(A_mat: List[List[float]], b_vec: List[float]) -> Optional[Tuple[float, float, float]]:
    """Giải hệ phương trình tuyến tính 3x3 bằng khử Gauss có chọn phần tử trụ tối đa."""
    M = [row[:] + [b_vec[i]] for i, row in enumerate(A_mat)]
    for col in range(3):
        pivot_row = max(range(col, 3), key=lambda r: abs(M[r][col]))
        if abs(M[pivot_row][col]) < TOL_PIVOT:
            return None
        M[col], M[pivot_row] = M[pivot_row], M[col]
        pivot_val = M[col][col]
        for j in range(col, 4):
            M[col][j] /= pivot_val
        for r in range(3):
            if r != col:
                factor = M[r][col]
                for j in range(col, 4):
                    M[r][j] -= factor * M[col][j]
    return (M[0][3], M[1][3], M[2][3])


def circumscribed_sphere(
    polyhedron_or_points: Union[PolyhedronDict, Sequence[Point3D]],
    strict: bool = True,
    tol: float = TOL_SPHERE,
) -> Sphere3D:
    """
    Tìm tâm I và bán kính R của mặt cầu ngoại tiếp khối đa diện (hoặc tập hợp >= 4 điểm không đồng phẳng).
    Phương pháp:
      1. Chọn điểm gốc P0 và 3 điểm P1, P2, P3 sao cho tứ diện P0P1P2P3 có tích hỗn tạp chuẩn hóa
         (Dimensionless Normalized Triple Product) lớn nhất, chống sai số thang đo (Scale Invariance).
      2. Giải hệ 3 phương trình mặt phẳng trung trực bằng khử Gauss chọn phần tử trụ tối đa:
           2*(x_i - x_0)*x_I + 2*(y_i - y_0)*y_I + 2*(z_i - z_0)*z_I = (x_i^2+y_i^2+z_i^2) - (x_0^2+y_0^2+z_0^2).
      3. Nếu strict=True: Kiểm định tính đồng cầu (Cospherical Verification) của toàn bộ các đỉnh còn lại
         theo sai số tương đối so với thang bán kính: |d(I, V) - R| / max(R, 1.0) <= tol.
         Nếu vi phạm, ném ValueError (bảo vệ tuyệt đối trước đa diện không nội tiếp).
    """
    if isinstance(polyhedron_or_points, dict) and "vertices" in polyhedron_or_points:
        pts: List[Point3D] = list(polyhedron_or_points["vertices"].values())
    else:
        pts = list(polyhedron_or_points)  # type: ignore

    if len(pts) < 4:
        raise ValueError("Cần ít nhất 4 điểm không đồng phẳng để xác định mặt cầu ngoại tiếp.")

    p0 = pts[0]
    best_trio: Optional[Tuple[Point3D, Point3D, Point3D]] = None
    max_det = 0.0
    n = len(pts)
    for i in range(1, n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                v1 = p0.vector_to(pts[i])
                v2 = p0.vector_to(pts[j])
                v3 = p0.vector_to(pts[k])
                norm_scale = v1.length() * v2.length() * v3.length()
                if norm_scale > TOL_SCALE_MIN:
                    det_val = abs(v1.cross_product(v2).dot_product(v3)) / norm_scale
                    if det_val > max_det:
                        max_det = det_val
                        best_trio = (pts[i], pts[j], pts[k])

    if best_trio is None or max_det < TOL_DET:
        raise ValueError("Các đỉnh đồng phẳng hoặc suy biến thể tích, không tồn tại mặt cầu ngoại tiếp duy nhất.")

    # Dịch chuyển hệ tọa độ cục bộ về gốc p0 để chống triệt tiêu số học khi ở xa gốc O
    # Phương trình: 2 * (P_k - P_0) . (I - P_0) = |P_k - P_0|^2
    A_mat: List[List[float]] = []
    b_vec: List[float] = []
    for pk in best_trio:
        qk = p0.vector_to(pk)
        qk_sq = qk.x * qk.x + qk.y * qk.y + qk.z * qk.z
        A_mat.append([2.0 * qk.x, 2.0 * qk.y, 2.0 * qk.z])
        b_vec.append(qk_sq)

    sol = _solve_linear_3x3(A_mat, b_vec)
    if sol is None:
        raise ValueError("Không thể giải hệ phương trình tâm mặt cầu ngoại tiếp.")

    center = Point3D("I", p0.x + sol[0], p0.y + sol[1], p0.z + sol[2])
    base_pts = [p0, best_trio[0], best_trio[1], best_trio[2]]
    radius = sum(center.distance_to(p) for p in base_pts) / 4.0

    if strict:
        scale_ref = max(radius, 1e-12)
        for pt in pts:
            dist = center.distance_to(pt)
            rel_err = abs(dist - radius) / scale_ref
            if rel_err > tol:
                raise ValueError(
                    f"Khối đa diện không thể nội tiếp mặt cầu: đỉnh '{pt.name}' cách tâm d={dist:.4f} != R={radius:.4f} "
                    f"(sai số tương đối {rel_err:.2e} > tol={tol})."
                )

    return Sphere3D(center=center, radius=radius)


def geographic_to_cartesian(
    lat_deg: float,
    lon_deg: float,
    radius: float = 1.0,
    center: Optional[Point3D] = None,
    name: str = "P",
) -> Point3D:
    """
    Chuyển đổi tọa độ Địa lý (Vĩ độ lat_deg [-90, 90], Kinh độ lon_deg [-180, 180], Bán kính R)
    sang tọa độ Descartes Oxyz:
      x = x_I + R * cos(lat) * cos(lon)
      y = y_I + R * cos(lat) * sin(lon)
      z = z_I + R * sin(lat)
    """
    if radius <= 0:
        raise ValueError("Bán kính phải dương.")
    c = center if center is not None else Point3D("O", 0.0, 0.0, 0.0)
    lat_rad = math.radians(float(lat_deg))
    lon_rad = math.radians(float(lon_deg))

    x = c.x + radius * math.cos(lat_rad) * math.cos(lon_rad)
    y = c.y + radius * math.cos(lat_rad) * math.sin(lon_rad)
    z = c.z + radius * math.sin(lat_rad)
    return Point3D(name=name, x=x, y=y, z=z)


def cartesian_to_geographic(
    pt: Point3D,
    center: Optional[Point3D] = None,
) -> Tuple[float, float, float]:
    """
    Chuyển đổi tọa độ Descartes (Oxyz) sang tọa độ Địa lý (lat_deg, lon_deg, radius).
    """
    c = center if center is not None else Point3D("O", 0.0, 0.0, 0.0)
    rel = c.vector_to(pt)
    r = rel.length()
    if r < EPSILON:
        return (0.0, 0.0, 0.0)

    sin_lat = max(-1.0, min(1.0, rel.z / r))
    lat_deg = math.degrees(math.asin(sin_lat))
    lon_deg = math.degrees(math.atan2(rel.y, rel.x))
    return (lat_deg, lon_deg, r)


def great_circle_distance(
    lat1_deg: float,
    lon1_deg: float,
    lat2_deg: float,
    lon2_deg: float,
    radius: float = 6371.0,
) -> float:
    """
    Tính khoảng cách vòng lớn (Great-Circle Distance / đường chim bay) giữa 2 điểm trên mặt cầu
    bằng công thức Haversine:
      a = sin^2(dlat/2) + cos(lat1)*cos(lat2)*sin^2(dlon/2)
      c = 2 * atan2(sqrt(a), sqrt(1 - a))
      d = R * c
    """
    if radius <= 0:
        raise ValueError("Bán kính mặt cầu phải dương.")

    phi1 = math.radians(float(lat1_deg))
    phi2 = math.radians(float(lat2_deg))
    d_phi = math.radians(float(lat2_deg - lat1_deg))
    d_lam = math.radians(float(lon2_deg - lon1_deg))

    sin_dphi = math.sin(0.5 * d_phi)
    sin_dlam = math.sin(0.5 * d_lam)
    a = sin_dphi * sin_dphi + math.cos(phi1) * math.cos(phi2) * sin_dlam * sin_dlam
    a = max(0.0, min(1.0, a))
    central_angle = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return float(radius) * central_angle


def spherical_triangle_area(
    P1: Point3D,
    P2: Point3D,
    P3: Point3D,
    sphere: Sphere3D,
) -> float:
    """
    Tính diện tích tam giác cầu (Spherical Triangle Area) giới hạn bởi 3 điểm P1, P2, P3
    trên mặt cầu sphere theo Định lý Girard:
      Area = R^2 * E = R^2 * (alpha + beta + gamma - pi)
    trong đó alpha, beta, gamma là 3 góc nhị diện giữa các mặt phẳng vòng lớn (OP1P2), (OP2P3), (OP3P1).
    """
    O = sphere.center
    u1 = O.vector_to(P1).normalize()
    u2 = O.vector_to(P2).normalize()
    u3 = O.vector_to(P3).normalize()

    if abs(u1.cross_product(u2).dot_product(u3)) <= 1e-8:
        return 0.0

    def spherical_interior_angle(a: Vector3D, b: Vector3D, c: Vector3D) -> float:
        # Góc tại đỉnh a giữa hai cung tròn lớn ab và ac
        # Vector tiếp tuyến với cung ab và ac tại a:
        t_ab = b - a * a.dot_product(b)
        t_ac = c - a * a.dot_product(c)
        cos_ang = t_ab.dot_product(t_ac) / (t_ab.length() * t_ac.length())
        cos_ang = max(-1.0, min(1.0, cos_ang))
        return math.acos(cos_ang)

    alpha = spherical_interior_angle(u1, u2, u3)
    beta = spherical_interior_angle(u2, u3, u1)
    gamma = spherical_interior_angle(u3, u1, u2)

    spherical_excess = max(0.0, alpha + beta + gamma - math.pi)
    return (sphere.radius ** 2) * spherical_excess


def intersect_sphere_with_plane(
    sphere: Sphere3D,
    plane: Plane3D,
    tol: float = 1e-7,
) -> Optional[Tuple[Point3D, float]]:
    """
    Tìm giao tuyến của mặt cầu (sphere) và mặt phẳng (plane):
    - Gọi d = d(I, plane) là khoảng cách từ tâm mặt cầu I đến mặt phẳng.
    - Nếu d > R + tol: Mặt phẳng không cắt mặt cầu -> trả về None.
    - Nếu d <= R + tol: Giao tuyến là đường tròn tâm H (hình chiếu vuông góc của I lên plane)
      và bán kính r = sqrt(max(0, R^2 - d^2)).
    """
    d = distance_point_to_plane(sphere.center, plane)
    if d > sphere.radius + tol:
        return None
    H = plane.project_point(sphere.center, name="H")
    r_circle = math.sqrt(max(0.0, sphere.radius * sphere.radius - d * d))
    return (H, r_circle)


# ==============================================================================
# 7. KIỂM THỬ TỰ ĐỘNG & MINH HỌA (SELF-TEST SUITE)
# ==============================================================================

def _run_self_tests() -> None:
    print("=" * 82)
    print("GEOSOLVER 3D - KIỂM THỬ HẠT NHÂN HÌNH HỌC ĐỘNG DGS & MẶT CẦU QUỐC TẾ SAT")
    print("=" * 82)

    # 1. Kiểm thử quy tắc đặt tên điểm chuẩn DGS
    assert validate_point_name("A") is True
    assert validate_point_name("A1") is True
    assert validate_point_name("M12") is True
    assert validate_point_name("AB") is False
    assert validate_point_name("a1") is False
    print("[1] Kiểm thử Regex tên điểm DGS (^[A-Z][0-9]*$) -> ĐẠT")

    # 2. Kiểm thử hình chóp S.ABCD, đường vuông góc chung find_common_perpendicular
    sabcd = create_pyramid_sabcd(a=4.0, b=3.0, h=5.0, sa_perp=True)
    S = sabcd["vertices"]["S"]
    A = sabcd["vertices"]["A"]
    B = sabcd["vertices"]["B"]
    C = sabcd["vertices"]["C"]

    u_sa = A.vector_to(S)
    u_bc = B.vector_to(C)
    M1, M2, d_common = find_common_perpendicular(A, u_sa, B, u_bc)
    assert M1.is_close(Point3D("M1", 0.0, 0.0, 0.0), tol=1e-6)
    assert M2.is_close(Point3D("M2", 4.0, 0.0, 0.0), tol=1e-6)
    assert abs(d_common - 4.0) <= 1e-6
    print(f"[2] Chân đường vuông góc chung SA & BC: M1{M1.to_tuple()}, M2{M2.to_tuple()}, d={d_common:.4f} -> ĐẠT")

    # 3. Kiểm thử Mặt cầu ngoại tiếp hình chóp S.ABCD (SA ⊥ đáy chữ nhật ABCD)
    # Vì góc SAB = SAD = ABC = ADC = 90° nên tâm cầu ngoại tiếp I là trung điểm SC = (2, 1.5, 2.5)
    sphere_sabcd = circumscribed_sphere(sabcd)
    expected_center = S.midpoint_with(C, name="I")
    expected_R = 0.5 * S.distance_to(C)
    assert sphere_sabcd.center.is_close(expected_center, tol=1e-6)
    assert abs(sphere_sabcd.radius - expected_R) <= 1e-6
    print(f"[3] Mặt cầu ngoại tiếp S.ABCD: Tâm I{sphere_sabcd.center.to_tuple()}, R={sphere_sabcd.radius:.4f} -> ĐẠT")

    # 4. Kiểm thử Hệ Ràng buộc Hình học Động (GeometricConstraintSolver)
    plane_alpha = Plane3D(0.0, 0.0, 1.0, -2.0)  # Mặt phẳng z = 2.0
    solver = GeometricConstraintSolver()
    solver.add_constraint(DistancePointToPlaneConstraint("P", plane_alpha, distance=3.0))
    p_dragged = Point3D("P", 1.5, -2.5, 9.8)
    p_corrected = solver.solve_point(p_dragged)
    assert abs(distance_point_to_plane(p_corrected, plane_alpha) - 3.0) <= 1e-6
    assert abs(p_corrected.z - 5.0) <= 1e-6
    print(f"[4] Ràng buộc d(P, z=2) = 3.0: P_drag(1.5, -2.5, 9.8) -> P_proj{p_corrected.to_tuple()} -> ĐẠT")

    # 5. Kiểm thử Tọa độ Địa lý, Khoảng cách Haversine & Diện tích Tam giác cầu Girard
    R_earth = 6371.0
    pt_equator_0 = geographic_to_cartesian(0.0, 0.0, R_earth, name="E1")
    pt_equator_90 = geographic_to_cartesian(0.0, 90.0, R_earth, name="E2")
    pt_north_pole = geographic_to_cartesian(90.0, 0.0, R_earth, name="N")

    lat_back, lon_back, r_back = cartesian_to_geographic(pt_equator_90)
    assert abs(lat_back - 0.0) <= 1e-6 and abs(lon_back - 90.0) <= 1e-6 and abs(r_back - R_earth) <= 1e-6

    # Khoảng cách vòng lớn giữa (0°, 0°) và (0°, 90°) là 1/4 chu vi xích đạo = (pi/2) * R
    d_haversine = great_circle_distance(0.0, 0.0, 0.0, 90.0, radius=R_earth)
    assert abs(d_haversine - 0.5 * math.pi * R_earth) <= 1e-4

    # Tam giác cầu 1/8 mặt cầu (Octant: E1(0,0), E2(0,90), N(90,0)) có 3 góc vuông => E = pi/2
    earth_sphere = Sphere3D(Point3D("O", 0.0, 0.0, 0.0), R_earth)
    octant_area = spherical_triangle_area(pt_equator_0, pt_equator_90, pt_north_pole, earth_sphere)
    expected_octant_area = 0.5 * math.pi * (R_earth ** 2)
    assert abs(octant_area - expected_octant_area) / expected_octant_area <= 1e-6
    print(f"[5] Haversine d = {d_haversine:.2f} km, Diện tích tam giác cầu Girard = {octant_area:.2f} km² -> ĐẠT")

    # 6. Kiểm thử Giao tuyến Mặt cầu - Mặt phẳng
    unit_sphere = Sphere3D(Point3D("O", 0.0, 0.0, 0.0), 5.0)
    cut_plane = Plane3D(0.0, 0.0, 1.0, -3.0)  # z = 3 => d = 3, R = 5 => r_circle = 4
    inter_circle = intersect_sphere_with_plane(unit_sphere, cut_plane)
    assert inter_circle is not None
    H_circle, r_circle = inter_circle
    assert H_circle.is_close(Point3D("H", 0.0, 0.0, 3.0), tol=1e-6)
    assert abs(r_circle - 4.0) <= 1e-6
    print(f"[6] Giao tuyến Cầu(R=5) & MP(z=3): Tâm H{H_circle.to_tuple()}, bán kính r = {r_circle:.4f} -> ĐẠT")
    print("=" * 82)


if __name__ == "__main__":
    _run_self_tests()
