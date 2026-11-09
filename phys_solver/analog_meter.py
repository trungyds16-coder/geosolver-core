# -*- coding: utf-8 -*-
"""
Module: analog_meter.py
Đường dẫn: D:\\AI DATA\\STEM_APP\\phys_solver\\analog_meter.py
Mô tả:
    VẼ ĐỒNG HỒ ĐO ĐIỆN KIM CHUẨN SÁCH GIÁO KHOA VIỆT NAM (ANALOG VOLTMETER & AMMETER):
    - Khung vỏ đồng hồ cơ học cổ điển phong cách thí nghiệm vật lý phòng thực hành.
    - Mặt đồng hồ hình vòng cung (Arched scale) có vạch chia độ chính xác (0 .. max).
    - Chữ in đậm nổi bật: 'V' (Vôn kế) hoặc 'A' (Ampe kế).
    - Biểu tượng chế độ in chuẩn SGK ngay dưới chữ V/A:
      * '—' hoặc 'DC' (Dòng điện một chiều)
      * '~' hoặc 'AC' (Dòng điện xoay chiều)
    - Kim chỉ thị (Deflection Needle) quay mượt mà quanh trục theo góc theta tỉ lệ với giá trị đo.
    - Cặp chốt cắm dây đỏ (+) và đen (-) chuẩn phòng thí nghiệm.
"""

from __future__ import annotations
import math
import tkinter as tk
from typing import Tuple, Optional


class AnalogMeterRenderer:
    """Trình kết xuất đồ họa đồng hồ đo kim chuẩn SGK trên Canvas Tkinter."""

    @staticmethod
    def draw_meter(
        canvas: tk.Canvas,
        cx: float,
        cy: float,
        radius: float = 85.0,
        meter_type: str = "V",         # "V" (Vôn kế) hoặc "A" (Ampe kế)
        mode: str = "DC",              # "DC" (một chiều) hoặc "AC" (xoay chiều)
        current_value: float = 0.0,    # Giá trị đo tức thời hoặc hiệu dụng
        max_scale: float = 10.0,       # Thang đo cực đại (ví dụ 10V, 3A)
        subdivisions: int = 10,        # Số vạch chia lớn
        tag_prefix: str = "analog_meter",
    ) -> None:
        """
        Vẽ toàn bộ hình ảnh chiếc đồng hồ đo kim cơ học chuẩn kỹ thuật.
        cx, cy: Tọa độ tâm đáy của kim quay trên Canvas.
        radius: Bán kính mặt cung đo.
        """
        canvas.delete(tag_prefix)

        # 1. Khung vỏ ngoài đồng hồ phong cách Technical CAD / Win32
        w_box = radius * 2.2
        h_box = radius * 2.0
        x1, y1 = cx - w_box / 2.0, cy - h_box * 0.85
        x2, y2 = cx + w_box / 2.0, cy + h_box * 0.35

        # Vỏ đồng hồ màu xám đen kỹ thuật (#2C302E) có viền vát 3D chuẩn Win32
        canvas.create_rectangle(
            x1, y1, x2, y2,
            fill="#EFEBD9", outline="#5A5D5A", width=3,
            tags=tag_prefix
        )
        canvas.create_rectangle(
            x1 + 4, y1 + 4, x2 - 4, y2 - 4,
            fill="#FAF8F0", outline="#8C908C", width=1,
            tags=tag_prefix
        )

        # 2. Vành mặt đồng hồ hình vòng cung (Arc scale background)
        arc_bbox = (cx - radius, cy - radius, cx + radius, cy + radius)
        # Góc mở từ 140 độ đến 40 độ (tổng góc quét 100 độ)
        start_deg = 40.0
        extent_deg = 100.0

        canvas.create_arc(
            arc_bbox,
            start=start_deg, extent=extent_deg,
            style="arc", outline="#1F2421", width=2,
            tags=tag_prefix
        )

        # 3. Vẽ các vạch chia độ (Graduation Ticks) và ghi số
        for i in range(subdivisions + 1):
            frac = i / float(subdivisions)
            # Góc từ trái (140 độ) sang phải (40 độ)
            angle_deg = 140.0 - frac * 100.0
            angle_rad = math.radians(angle_deg)

            # Vạch lớn và vạch nhỏ
            tick_len = 9.0 if (i % 2 == 0) else 5.0
            tick_width = 2 if (i % 2 == 0) else 1

            rx1 = cx + (radius - 2) * math.cos(angle_rad)
            ry1 = cy - (radius - 2) * math.sin(angle_rad)
            rx2 = cx + (radius - 2 - tick_len) * math.cos(angle_rad)
            ry2 = cy - (radius - 2 - tick_len) * math.sin(angle_rad)

            canvas.create_line(rx1, ry1, rx2, ry2, fill="#1F2421", width=tick_width, tags=tag_prefix)

            # Ghi số đo tại vạch chính
            if i % 2 == 0:
                val_num = (i / float(subdivisions)) * max_scale
                num_text = f"{val_num:.0f}" if val_num.is_integer() else f"{val_num:.1f}"
                lbl_r = radius - 20
                lx = cx + lbl_r * math.cos(angle_rad)
                ly = cy - lbl_r * math.sin(angle_rad)
                canvas.create_text(
                    lx, ly, text=num_text,
                    font=("Tahoma", 7, "bold"), fill="#1F2421",
                    tags=tag_prefix
                )

        # 4. CHỮ IN ĐẬM V HOẶC A VÀ KÍ HIỆU XOAY CHIỀU / MỘT CHIỀU CHUẨN SGK
        # Chữ 'V' hoặc 'A' màu xanh đậm / đen to bản ở giữa
        meter_letter = meter_type.upper()
        canvas.create_text(
            cx, cy - radius * 0.45,
            text=meter_letter,
            font=("Arial", 16, "bold"),
            fill="#003399" if meter_letter == "V" else "#8B0000",
            tags=tag_prefix
        )

        # Biểu tượng 1 chiều '—' hoặc xoay chiều '~' in ngay dưới chữ V/A
        symbol_text = "—  (DC)" if mode.upper() == "DC" else "~  (AC)"
        canvas.create_text(
            cx, cy - radius * 0.22,
            text=symbol_text,
            font=("Consolas", 10, "bold"),
            fill="#333333",
            tags=tag_prefix
        )

        # 5. KIM CHỈ THỊ (DEFLECTION NEEDLE)
        # Giới hạn giá trị trong khoảng [0, max_scale]
        clamped_val = max(0.0, min(float(current_value), float(max_scale)))
        val_ratio = clamped_val / float(max_scale) if max_scale > 0 else 0.0

        needle_deg = 140.0 - val_ratio * 100.0
        needle_rad = math.radians(needle_deg)

        needle_len = radius - 4
        nx = cx + needle_len * math.cos(needle_rad)
        ny = cy - needle_len * math.sin(needle_rad)

        # Kim vẽ màu đỏ cam kỹ thuật có bóng đổ nhẹ
        canvas.create_line(
            cx, cy, nx, ny,
            fill="#DC2626", width=2,
            arrow="last", arrowshape=(8, 10, 3),
            tags=tag_prefix
        )

        # Trục kim tròn ở tâm đáy
        canvas.create_oval(
            cx - 7, cy - 7, cx + 7, cy + 7,
            fill="#2B2D42", outline="#8D99AE", width=2,
            tags=tag_prefix
        )
        canvas.create_oval(
            cx - 2, cy - 2, cx + 2, cy + 2,
            fill="#FFFFFF", outline="",
            tags=tag_prefix
        )

        # 6. CẶP CHỐT CẮM DÂY ĐỎ (+) VÀ ĐEN (-) DƯỚI ĐÁY
        post_y = cy + h_box * 0.20
        # Chốt dương (+) màu đỏ
        canvas.create_rectangle(
            cx - 45, post_y - 8, cx - 25, post_y + 8,
            fill="#DC2626", outline="#7F1D1D", width=1, tags=tag_prefix
        )
        canvas.create_text(
            cx - 35, post_y, text="+", font=("Tahoma", 10, "bold"), fill="#FFFFFF", tags=tag_prefix
        )

        # Chốt âm (-) màu đen
        canvas.create_rectangle(
            cx + 25, post_y - 8, cx + 45, post_y + 8,
            fill="#1E293B", outline="#020617", width=1, tags=tag_prefix
        )
        canvas.create_text(
            cx + 35, post_y, text="−", font=("Tahoma", 10, "bold"), fill="#FFFFFF", tags=tag_prefix
        )

        # Nhãn đọc số LCD kỹ thuật số nhỏ phía dưới góc
        readout_str = f"{current_value:.2f} {meter_letter}"
        canvas.create_text(
            cx, cy + h_box * 0.05,
            text=readout_str,
            font=("Consolas", 8, "bold"),
            fill="#0F766E",
            tags=tag_prefix
        )
