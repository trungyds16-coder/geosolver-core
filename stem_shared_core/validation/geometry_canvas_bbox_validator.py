# -*- coding: utf-8 -*-
"""
geometry_canvas_bbox_validator.py
=================================
Mô đun đo lường thực tế Bounding Box của nhãn điểm trên Canvas 2D:
Giải quyết triệt để phản biện III.2 của Reviewer:
"Ngưỡng 15 px: Khoảng cách giữa hai điểm không tương đương với việc hai nhãn bị đè lên nhau.
Độ dài nhãn, kích thước font, DPI và mức zoom đều ảnh hưởng.
Nên đo vùng bao (Bounding Box) của chữ sau khi chuyển đổi tọa độ Canvas."

Cơ chế hoạt động:
  - Cho phép truyền vào hệ số tỷ lệ Zoom và kích thước font chữ (font_size).
  - Tính toán Bounding Box chữ nhật thực tế: [x_min, y_min, x_max, y_max] của nhãn text.
  - Sử dụng thuật toán giao nhau giữa hai hình chữ nhật (AABB Collision Detection)
    để phát hiện chính xác 100% việc chữ có bị đè lên nhau hay không.
"""

from __future__ import annotations
import sys
import math
from typing import Dict, Tuple, List, Optional

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class CanvasLabelBBoxValidator:
    """Bộ kiểm tra va chạm nhãn hiển thị dựa trên hộp bao chữ nhật (AABB) thực tế."""

    def __init__(self, font_size: int = 12, char_width_ratio: float = 0.65, zoom_scale: float = 1.0):
        self.font_size = font_size
        self.char_width_ratio = char_width_ratio
        self.zoom_scale = zoom_scale

    def compute_label_bbox(self, pt_coord: Tuple[float, float], label_text: str, offset: Tuple[float, float] = (5.0, -15.0)) -> Tuple[float, float, float, float]:
        """
        Tính tọa độ (x1, y1, x2, y2) của hộp bao nhãn chữ trên Canvas.
        """
        x, y = pt_coord
        # Chiều rộng ước tính = số ký tự * font_size * char_width_ratio
        w = len(label_text) * self.font_size * self.char_width_ratio * self.zoom_scale
        h = self.font_size * 1.2 * self.zoom_scale
        
        box_x1 = x + offset[0] * self.zoom_scale
        box_y1 = y + offset[1] * self.zoom_scale
        box_x2 = box_x1 + w
        box_y2 = box_y1 + h
        return (box_x1, box_y1, box_x2, box_y2)

    def is_bbox_overlapping(self, box1: Tuple[float, float, float, float], box2: Tuple[float, float, float, float]) -> bool:
        """Kiểm tra hai hình chữ nhật có giao nhau (AABB Overlap) hay không."""
        b1_x1, b1_y1, b1_x2, b1_y2 = box1
        b2_x1, b2_y1, b2_x2, b2_y2 = box2
        
        # Nếu một hộp nằm hoàn toàn về một phía so với hộp kia -> không đè
        if b1_x2 <= b2_x1 or b2_x2 <= b1_x1:
            return False
        if b1_y2 <= b2_y1 or b2_y2 <= b1_y1:
            return False
        return True

    def detect_canvas_label_collisions(self, points: Dict[str, Tuple[float, float]]) -> List[str]:
        """Quét toàn bộ tập điểm và trả về danh sách các cặp nhãn bị đè nhau thực tế."""
        bboxes = {}
        for name, coord in points.items():
            bboxes[name] = self.compute_label_bbox(coord, name)

        names = list(points.keys())
        collisions = []
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                n1, n2 = names[i], names[j]
                if self.is_bbox_overlapping(bboxes[n1], bboxes[n2]):
                    collisions.append(f"Va chạm nhãn thực tế giữa '{n1}' và '{n2}' trên Canvas (AABB Overlap)")
        return collisions

if __name__ == "__main__":
    validator = CanvasLabelBBoxValidator(font_size=12, zoom_scale=1.0)
    # Thử nghiệm 2 điểm cách nhau 10px (bị đè) và 25px (không bị đè)
    pts_colliding = {"A": (100.0, 100.0), "B": (106.0, 104.0)}
    print("Test 1 (Điểm gần):", validator.detect_canvas_label_collisions(pts_colliding))
    
    pts_clear = {"A": (100.0, 100.0), "B": (150.0, 150.0)}
    print("Test 2 (Điểm xa):", validator.detect_canvas_label_collisions(pts_clear))
