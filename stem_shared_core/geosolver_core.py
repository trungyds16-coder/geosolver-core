# -*- coding: utf-8 -*-
"""
GeoSolver 2D - Mô-đun Giải thuật & Kiểm định Hình học Lõi (GeoSolver2DCore)
Phiên bản: 1.0 (Độc lập với Tkinter và GUI)

Bao gồm:
- Các hàm hình học giải tích chuẩn xác: khoảng cách, diện tích Gauss, kiểm tra thẳng hàng.
- Bốn điểm đặc trưng tam giác: Trọng tâm (G), Tâm ngoại tiếp (O), Tâm nội tiếp (I), Trực tâm (H).
- Đường thẳng Euler (O-G-H) và Tâm đường tròn 9 điểm Feuerbach (N9).
- Tương giao hình học: Tiếp tuyến từ một điểm, giao điểm 2 đường tròn, giao điểm đường thẳng - đường tròn.
- Kiến trúc kiểm định Fail-Fast: MissingGeometricNodeError, DegenerateGeometryError, OutOfBoundsError.
- Kiểm định va chạm nhãn hiển thị theo thuật toán hộp bao trục tọa độ (AABB Collision Detection).
"""

from __future__ import annotations
import math
from typing import Dict, Tuple, List, Optional, Any, NamedTuple
from enum import Enum

class GeoConstructionStatus(str, Enum):
    VALID = "VALID"
    DEGENERATE = "DEGENERATE"
    MISSING_NODE = "MISSING_NODE"
    OUT_OF_BOUNDS = "OUT_OF_BOUNDS"
    LABEL_COLLISION = "LABEL_COLLISION"

class GeometryValidationError(Exception):
    """Lớp ngoại lệ cơ sở cho mọi lỗi xác thực hình học."""
    pass

class MissingGeometricNodeError(GeometryValidationError):
    """Báo lỗi khi thiếu điểm hoặc dữ kiện không đủ để dựng hình."""
    def __init__(self, node_name: str, reason: str, missing_deps: Optional[List[str]] = None):
        self.node_name = node_name
        self.reason = reason
        self.missing_deps = missing_deps or []
        msg = f"[LỖI DỰNG HÌNH - THIẾU NÚT] Không thể xác định tọa độ của '{node_name}': {reason}."
        if self.missing_deps:
            msg += f" Dữ kiện phụ thuộc còn thiếu: {', '.join(self.missing_deps)}."
        super().__init__(msg)

class DegenerateGeometryError(GeometryValidationError):
    """Báo lỗi khi hình bị suy biến (tam giác thẳng hàng, bán kính <= 0)."""
    pass

class OutOfBoundsError(GeometryValidationError):
    """Báo lỗi khi điểm nằm ngoài viewport hoặc toạ độ phân kỳ (Inf, NaN)."""
    pass

class Point2D(NamedTuple):
    x: float
    y: float

class GeoSolver2DCore:
    """Mô-đun giải thuật và kiểm định hình học phẳng 2D chuẩn xác."""

    def __init__(self, min_point_distance: float = 12.0, font_size: int = 12, char_width_ratio: float = 0.65):
        self.min_point_distance = min_point_distance
        self.font_size = font_size
        self.char_width_ratio = char_width_ratio

    @staticmethod
    def distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """Khoảng cách Euclid giữa hai điểm."""
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    @staticmethod
    def triangle_area(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> float:
        """Diện tích tam giác theo công thức tọa độ Gauss (Shoelace formula)."""
        (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
        return 0.5 * abs((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1))

    @staticmethod
    def is_collinear(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float], tol: float = 1e-5) -> bool:
        """Kiểm tra 3 điểm có thẳng hàng hay không."""
        return GeoSolver2DCore.triangle_area(p1, p2, p3) < tol

    @staticmethod
    def compute_centroid(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> Tuple[float, float]:
        """Tọa độ trọng tâm tam giác: G = (A + B + C) / 3."""
        Gx = (p1[0] + p2[0] + p3[0]) / 3.0
        Gy = (p1[1] + p2[1] + p3[1]) / 3.0
        return (Gx, Gy)

    @staticmethod
    def compute_circumcenter(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> Tuple[Tuple[float, float], float]:
        """Tâm và bán kính đường tròn ngoại tiếp tam giác."""
        (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
        d = 2.0 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        if abs(d) < 1e-7:
            raise DegenerateGeometryError(f"Ba điểm thẳng hàng ({p1}, {p2}, {p3}), không tồn tại đường tròn ngoại tiếp.")

        ux = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / d
        uy = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / d
        R = math.hypot(x1 - ux, y1 - uy)
        return ((ux, uy), R)

    @staticmethod
    def compute_incenter(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> Tuple[Tuple[float, float], float]:
        """Tâm và bán kính đường tròn nội tiếp tam giác: I = (aA + bB + cC) / (a + b + c), r = S / p."""
        a = math.hypot(p2[0] - p3[0], p2[1] - p3[1])
        b = math.hypot(p1[0] - p3[0], p1[1] - p3[1])
        c = math.hypot(p1[0] - p2[0], p1[1] - p2[1])
        perimeter = a + b + c
        if perimeter < 1e-5:
            raise DegenerateGeometryError("Chu vi tam giác xấp xỉ 0, tam giác suy biến.")
        area = GeoSolver2DCore.triangle_area(p1, p2, p3)
        if area < 1e-5:
            raise DegenerateGeometryError(f"Ba điểm thẳng hàng, không tồn tại đường tròn nội tiếp (diện tích = {area:.6f}).")

        Ix = (a * p1[0] + b * p2[0] + c * p3[0]) / perimeter
        Iy = (a * p1[1] + b * p2[1] + c * p3[1]) / perimeter
        r = area / (perimeter / 2.0)
        return ((Ix, Iy), r)

    @staticmethod
    def compute_orthocenter(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> Tuple[float, float]:
        """Tọa độ trực tâm tam giác: giao điểm 2 đường cao."""
        if GeoSolver2DCore.is_collinear(p1, p2, p3):
            raise DegenerateGeometryError("Ba điểm thẳng hàng, không tồn tại trực tâm tam giác.")
        (O, R) = GeoSolver2DCore.compute_circumcenter(p1, p2, p3)
        G = GeoSolver2DCore.compute_centroid(p1, p2, p3)
        # Định lý Euler: OH = 3*OG => H = 3*G - 2*O
        Hx = 3.0 * G[0] - 2.0 * O[0]
        Hy = 3.0 * G[1] - 2.0 * O[1]
        return (Hx, Hy)

    @staticmethod
    def compute_nine_point_center(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> Tuple[Tuple[float, float], float]:
        """Tâm và bán kính đường tròn 9 điểm Euler-Feuerbach (N9, R9 = R/2)."""
        (O, R) = GeoSolver2DCore.compute_circumcenter(p1, p2, p3)
        H = GeoSolver2DCore.compute_orthocenter(p1, p2, p3)
        N9_x = (O[0] + H[0]) / 2.0
        N9_y = (O[1] + H[1]) / 2.0
        return ((N9_x, N9_y), R / 2.0)

    @staticmethod
    def intersect_lines(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float], p4: Tuple[float, float]) -> Optional[Tuple[float, float]]:
        """Giao điểm của 2 đường thẳng đi qua (p1, p2) và (p3, p4)."""
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 1e-9:
            return None  # Hai đường thẳng song song hoặc trùng nhau
        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
        return (px, py)

    @staticmethod
    def tangents_from_point_to_circle(P: Tuple[float, float], center: Tuple[float, float], radius: float) -> List[Tuple[float, float]]:
        """Tiếp điểm của các tiếp tuyến kẻ từ điểm P đến đường tròn (C(center, radius))."""
        d = math.hypot(P[0] - center[0], P[1] - center[1])
        if d < radius - 1e-7:
            return []  # Điểm nằm trong đường tròn, không có tiếp tuyến thực
        if abs(d - radius) < 1e-7:
            return [P]  # Điểm nằm trên đường tròn, có đúng 1 tiếp điểm là chính P

        # Điểm nằm ngoài đường tròn: có 2 tiếp điểm
        alpha = math.acos(radius / d)
        theta = math.atan2(P[1] - center[1], P[0] - center[0])

        t1_x = center[0] + radius * math.cos(theta + alpha)
        t1_y = center[1] + radius * math.sin(theta + alpha)

        t2_x = center[0] + radius * math.cos(theta - alpha)
        t2_y = center[1] + radius * math.sin(theta - alpha)

        return [(t1_x, t1_y), (t2_x, t2_y)]

    @staticmethod
    def intersect_circles(c1: Tuple[float, float], r1: float, c2: Tuple[float, float], r2: float) -> List[Tuple[float, float]]:
        """Giao điểm của hai đường tròn (C1(c1, r1)) và (C2(c2, r2))."""
        d = math.hypot(c2[0] - c1[0], c2[1] - c1[1])
        if d > r1 + r2 + 1e-7 or d < abs(r1 - r2) - 1e-7 or d < 1e-9:
            return []  # Không giao nhau hoặc đồng tâm
        
        a = (r1**2 - r2**2 + d**2) / (2.0 * d)
        h_sq = r1**2 - a**2
        if h_sq < 0:
            h_sq = 0.0
        h = math.sqrt(h_sq)

        # Điểm trung gian P2 trên đoạn nối tâm
        p2_x = c1[0] + a * (c2[0] - c1[0]) / d
        p2_y = c1[1] + a * (c2[1] - c1[1]) / d

        if abs(h) < 1e-7:
            return [(p2_x, p2_y)]  # Tiếp xúc nhau tại 1 điểm

        # Cắt nhau tại 2 điểm
        i1_x = p2_x + h * (c2[1] - c1[1]) / d
        i1_y = p2_y - h * (c2[0] - c1[0]) / d

        i2_x = p2_x - h * (c2[1] - c1[1]) / d
        i2_y = p2_y + h * (c2[0] - c1[0]) / d

        return [(i1_x, i1_y), (i2_x, i2_y)]

    @staticmethod
    def intersect_line_circle(p1: Tuple[float, float], p2: Tuple[float, float], center: Tuple[float, float], radius: float) -> List[Tuple[float, float]]:
        """Giao điểm giữa đường thẳng đi qua P1, P2 và đường tròn (C(center, radius)).
        - Trả về [] nếu đường thẳng không cắt đường tròn (disjoint).
        - Trả về [(x, y)] nếu đường thẳng tiếp xúc với đường tròn (tangent).
        - Trả về [(x1, y1), (x2, y2)] nếu đường thẳng là cát tuyến cắt đường tròn tại 2 điểm (secant).
        - Ném DegenerateGeometryError nếu P1 trùng P2.
        """
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        L = math.hypot(dx, dy)
        if L < 1e-9:
            raise DegenerateGeometryError("Đường thẳng xác định bởi 2 điểm trùng nhau hoặc khoảng cách quá nhỏ (< 1e-9).")

        # Hình chiếu H của tâm center lên đường thẳng
        w_x = center[0] - p1[0]
        w_y = center[1] - p1[1]
        t = (w_x * dx + w_y * dy) / (L * L)
        hx = p1[0] + t * dx
        hy = p1[1] + t * dy

        # Khoảng cách từ tâm đến đường thẳng
        d = math.hypot(hx - center[0], hy - center[1])

        if d > radius + 1e-7:
            return []  # Không cắt

        if abs(d - radius) <= 1e-7:
            return [(hx, hy)]  # Tiếp xúc tại 1 điểm

        # Cát tuyến cắt tại 2 điểm
        h_chord = math.sqrt(max(0.0, radius**2 - d**2))
        ux = dx / L
        uy = dy / L
        i1 = (hx + h_chord * ux, hy + h_chord * uy)
        i2 = (hx - h_chord * ux, hy - h_chord * uy)
        return [i1, i2]

    # --------------------------------------------------------------------------
    # KIỂM ĐỊNH TÍNH TOÀN VẸN HÌNH HỌC (FAIL-FAST CONTRACTS)
    # --------------------------------------------------------------------------
    def validate_points(self, points: Dict[str, Tuple[float, float]], required_points: Optional[List[str]] = None) -> List[str]:
        """Kiểm tra hợp lệ tập điểm, bắt lỗi thiếu điểm và kiểm tra NaN/Inf."""
        warnings = []
        if required_points:
            for pt_name in required_points:
                if pt_name not in points or points[pt_name] is None:
                    raise MissingGeometricNodeError(
                        node_name=pt_name,
                        reason="Điểm bắt buộc không có trong tập dữ kiện hoặc solver chưa tính ra"
                    )

        for name, coord in points.items():
            if coord is None or len(coord) != 2:
                raise MissingGeometricNodeError(node_name=name, reason="Tọa độ bị rỗng hoặc không đủ 2 chiều")
            x, y = coord
            if math.isnan(x) or math.isnan(y):
                raise MissingGeometricNodeError(node_name=name, reason="Tọa độ là NaN (lỗi số học chia 0 hoặc căn âm)")
            if math.isinf(x) or math.isinf(y):
                raise OutOfBoundsError(f"Điểm '{name}' có tọa độ vô cực ({x}, {y})")

        return warnings

    def validate_triangle_non_degenerate(self, p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float], names: Tuple[str, str, str] = ("A", "B", "C")) -> float:
        """Kiểm tra tam giác không suy biến. Trả về diện tích nếu hợp lệ."""
        area = self.triangle_area(p1, p2, p3)
        if area < 1e-4:
            raise DegenerateGeometryError(f"Tam giác {names[0]}{names[1]}{names[2]} bị suy biến (diện tích S = {area:.6f} ≈ 0, ba điểm thẳng hàng).")
        return area

    def validate_circle_non_degenerate(self, center: Tuple[float, float], radius: float, name: str = "(O)") -> float:
        """Kiểm tra đường tròn không suy biến. Trả về bán kính nếu hợp lệ."""
        if radius is None or math.isnan(radius) or math.isinf(radius):
            raise MissingGeometricNodeError(name, f"Bán kính đường tròn không hợp lệ: {radius}")
        if radius <= 1e-4:
            raise DegenerateGeometryError(f"Đường tròn {name} suy biến thành 1 điểm (bán kính R = {radius:.5f} <= 0).")
        return radius

    # --------------------------------------------------------------------------
    # KIỂM ĐỊNH VA CHẠM HỘP BAO NHÃN TRÊN CANVAS (AABB OVERLAP DETECTION)
    # --------------------------------------------------------------------------
    def compute_label_bbox(self, pt_coord: Tuple[float, float], label_text: str, offset: Tuple[float, float] = (5.0, -15.0), zoom_scale: float = 1.0) -> Tuple[float, float, float, float]:
        """Tính tọa độ (x1, y1, x2, y2) của hộp bao nhãn chữ trên Canvas."""
        x, y = pt_coord
        w = len(label_text) * self.font_size * self.char_width_ratio * zoom_scale
        h = self.font_size * 1.2 * zoom_scale
        box_x1 = x + offset[0] * zoom_scale
        box_y1 = y + offset[1] * zoom_scale
        box_x2 = box_x1 + w
        box_y2 = box_y1 + h
        return (box_x1, box_y1, box_x2, box_y2)

    @staticmethod
    def is_bbox_overlapping(box1: Tuple[float, float, float, float], box2: Tuple[float, float, float, float]) -> bool:
        """Kiểm tra 2 hộp chữ nhật AABB có giao nhau hay không."""
        b1_x1, b1_y1, b1_x2, b1_y2 = box1
        b2_x1, b2_y1, b2_x2, b2_y2 = box2
        if b1_x2 <= b2_x1 or b2_x2 <= b1_x1:
            return False
        if b1_y2 <= b2_y1 or b2_y2 <= b1_y1:
            return False
        return True

    def detect_canvas_label_collisions(self, points: Dict[str, Tuple[float, float]], zoom_scale: float = 1.0) -> List[str]:
        """Phát hiện toàn bộ các va chạm nhãn thực tế giữa các điểm trên Canvas."""
        bboxes = {name: self.compute_label_bbox(coord, name, zoom_scale=zoom_scale) for name, coord in points.items()}
        names = list(points.keys())
        collisions = []
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                n1, n2 = names[i], names[j]
                if self.is_bbox_overlapping(bboxes[n1], bboxes[n2]):
                    collisions.append(f"Va chạm nhãn thực tế giữa '{n1}' và '{n2}' trên Canvas (AABB Overlap)")
        return collisions

    # --------------------------------------------------------------------------
    # HỆ THỐNG BIẾN ĐỔI TỌA ĐỘ CANVAS (CARTESIAN <-> SCREEN PIXELS WITH ZOOM & PAN)
    # --------------------------------------------------------------------------
    @staticmethod
    def cartesian_to_canvas(
        pt: Tuple[float, float],
        origin_screen: Tuple[float, float] = (400.0, 300.0),
        scale_factor: float = 20.0,
        flip_y: bool = True
    ) -> Tuple[float, float]:
        """Chuyển đổi tọa độ giải tích Descartes (x, y) sang tọa độ Canvas màn hình pixel.
        flip_y=True: Trục Y của Canvas hướng xuống dưới (chuẩn Tkinter / HTML5 Canvas).
        """
        ox, oy = origin_screen
        sx = ox + pt[0] * scale_factor
        sy = (oy - pt[1] * scale_factor) if flip_y else (oy + pt[1] * scale_factor)
        return (sx, sy)

    @staticmethod
    def canvas_to_cartesian(
        screen_pt: Tuple[float, float],
        origin_screen: Tuple[float, float] = (400.0, 300.0),
        scale_factor: float = 20.0,
        flip_y: bool = True
    ) -> Tuple[float, float]:
        """Chuyển đổi ngược từ tọa độ pixel màn hình sang tọa độ Descartes giải tích."""
        if abs(scale_factor) < 1e-9:
            raise DegenerateGeometryError("Tỉ lệ phóng to thu nhỏ scale_factor không được bằng 0.")
        ox, oy = origin_screen
        cx = (screen_pt[0] - ox) / scale_factor
        cy = ((oy - screen_pt[1]) / scale_factor) if flip_y else ((screen_pt[1] - oy) / scale_factor)
        return (cx, cy)

