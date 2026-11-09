# -*- coding: utf-8 -*-
"""
geometry_validator.py
=====================
Bộ kiểm định hình học 2D nghiêm ngặt trước khi dựng hình (Fail-Fast Architecture).
Dành riêng cho hệ sinh thái GeoSolver và STEM App.

NGUYÊN TẮC BẢO CHỨNG:
1. Thiếu nút hoặc điểm không xác định được tọa độ -> Báo lỗi cụ thể (MissingGeometricNodeError).
2. Hình học suy biến (Degenerate) -> Báo lỗi (DegenerateGeometryError).
3. Va chạm nhãn điểm (Label Collision) hoặc tràn khung hình (Out-of-Bounds) -> Cảnh báo hoặc lỗi.
"""

from __future__ import annotations
import math
from typing import Dict, Tuple, List, Optional, Any

class GeometryValidationError(Exception):
    """Lớp ngoại lệ cơ sở cho mọi lỗi xác thực hình học."""
    pass

class MissingGeometricNodeError(GeometryValidationError):
    """Báo lỗi khi thiếu nút, thiếu điểm hoặc dữ kiện không đủ để dựng hình."""
    def __init__(self, node_name: str, reason: str, missing_deps: Optional[List[str]] = None):
        self.node_name = node_name
        self.reason = reason
        self.missing_deps = missing_deps or []
        msg = f"[LỖI DỰNG HÌNH - THIẾU NÚT] Không thể xác định vị trí của nút/điểm '{node_name}': {reason}."
        if self.missing_deps:
            msg += f" Dữ kiện phụ thuộc còn thiếu: {', '.join(self.missing_deps)}."
        super().__init__(msg)

class DegenerateGeometryError(GeometryValidationError):
    """Báo lỗi khi hình bị suy biến (tam giác có 3 điểm thẳng hàng, bán kính <= 0, v.v.)."""
    pass

class OutOfBoundsError(GeometryValidationError):
    """Báo lỗi khi điểm nằm ngoài viewport hoặc toạ độ bị phân kỳ (vô cực, NaN)."""
    pass

class Geometry2DValidator:
    """Trình kiểm tra chất lượng và tính toàn vẹn của mô hình hình học 2D."""

    def __init__(self, min_point_distance: float = 12.0, viewport_box: Optional[Tuple[float, float, float, float]] = None):
        """
        :param min_point_distance: Khoảng cách pixel tối thiểu để tránh đè chữ / nhãn điểm.
        :param viewport_box: (min_x, min_y, max_x, max_y) nếu cần kiểm tra giới hạn Canvas.
        """
        self.min_point_distance = min_point_distance
        self.viewport_box = viewport_box

    def validate_points(self, points: Dict[str, Tuple[float, float]], required_points: Optional[List[str]] = None) -> List[str]:
        """
        Kiểm tra tính hợp lệ của toàn bộ tập điểm.
        Báo lỗi ngay nếu thiếu điểm bắt buộc hoặc toạ độ không hợp lệ.
        Trả về danh sách các cảnh báo (warnings) nếu có.
        """
        warnings = []
        
        # 1. Kiểm tra các điểm bắt buộc phải tồn tại
        if required_points:
            for pt_name in required_points:
                if pt_name not in points:
                    raise MissingGeometricNodeError(
                        node_name=pt_name,
                        reason="Điểm bắt buộc không được khai báo hoặc solver chưa tính ra"
                    )

        # 2. Kiểm tra tính hợp lệ số học (NaN, Inf, None)
        for name, coord in points.items():
            if coord is None or len(coord) != 2:
                raise MissingGeometricNodeError(
                    node_name=name,
                    reason=f"Tọa độ không hợp lệ (nhận được: {coord})"
                )
            x, y = coord
            if x is None or y is None:
                raise MissingGeometricNodeError(
                    node_name=name,
                    reason="Tọa độ chứa giá trị rỗng (None)"
                )
            if math.isnan(x) or math.isnan(y):
                raise MissingGeometricNodeError(
                    node_name=name,
                    reason="Tọa độ là NaN (phép tính số học bị chia 0 hoặc căn số âm)"
                )
            if math.isinf(x) or math.isinf(y):
                raise OutOfBoundsError(
                    f"Điểm '{name}' có tọa độ vô hạn ({x}, {y}) - đường thẳng song song không có giao điểm hữu hạn"
                )

        # 3. Kiểm tra va chạm khoảng cách giữa các điểm (Label / Node collision)
        pt_list = list(points.items())
        for i in range(len(pt_list)):
            for j in range(i + 1, len(pt_list)):
                name1, (x1, y1) = pt_list[i]
                name2, (x2, y2) = pt_list[j]
                dist = math.hypot(x1 - x2, y1 - y2)
                if dist < 1e-5:
                    raise DegenerateGeometryError(
                        f"Hai điểm '{name1}' và '{name2}' trùng nhau tại ({x1:.3f}, {y1:.3f})"
                    )
                elif dist < self.min_point_distance:
                    warnings.append(
                        f"Cảnh báo va chạm hiển thị: '{name1}' và '{name2}' cách nhau quá gần ({dist:.1f}px < {self.min_point_distance}px), có nguy cơ đè nhãn"
                    )

        # 4. Kiểm tra viewport nếu được thiết lập
        if self.viewport_box:
            min_x, min_y, max_x, max_y = self.viewport_box
            for name, (x, y) in points.items():
                if not (min_x <= x <= max_x and min_y <= y <= max_y):
                    warnings.append(
                        f"Cảnh báo khung nhìn: Điểm '{name}' ({x:.1f}, {y:.1f}) nằm ngoài viewport ({min_x}, {min_y}, {max_x}, {max_y})"
                    )

        return warnings

    def validate_triangle(self, p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float], names: Tuple[str, str, str] = ("A", "B", "C")) -> float:
        """
        Kiểm tra tam giác hợp lệ, không suy biến (3 điểm không thẳng hàng).
        Trả về diện tích tam giác có hướng.
        """
        (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
        area_2 = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
        area = abs(area_2) / 2.0
        if area < 1e-4:
            raise DegenerateGeometryError(
                f"Tam giác {names[0]}{names[1]}{names[2]} bị suy biến (diện tích = {area:.5f} ≈ 0, ba điểm thẳng hàng)"
            )
        return area

    def validate_circle(self, center: Tuple[float, float], radius: float, name: str = "(O)") -> None:
        """Kiểm tra đường tròn hợp lệ."""
        if radius is None or math.isnan(radius) or math.isinf(radius):
            raise MissingGeometricNodeError(name, f"Bán kính đường tròn không hợp lệ: {radius}")
        if radius <= 1e-4:
            raise DegenerateGeometryError(f"Đường tròn {name} suy biến thành một điểm (bán kính R = {radius:.4f} <= 0)")
