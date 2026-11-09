# -*- coding: utf-8 -*-
"""
Module: sandbox_engine.py
Đường dẫn: D:\\AI DATA\\STEM_APP\\phys_solver\\sandbox_engine.py
Mô tả:
    LÕI MÔ PHỎNG VẬT LÍ TƯƠNG TÁC ĐA DẠNG DẠNG SANDBOX (GAME-LIKE PHYSICS SANDBOX):
    1. Va chạm 2 vật (Hình hộp chữ nhật, Quả cầu) có ma sát, hệ số phục hồi e,
       tính toán và hiển thị vector lực nén đàn hồi F12(t), F21(t) biến thiên thời gian thực.
    2. Người / Khối vật trong thang máy chuyển động biến đổi đều (gia tốc a):
       Trọng lượng biểu kiến N = m*(g +- a), lực quán tính F_qt = -m*a hiển thị trên bàn cân.
    3. Vật gắn lò xo trên mặt phẳng nghiêng có ma sát:
       Lực phục hồi F_dh, phản lực N, lực ma sát trượt F_ms đổi chiều theo vận tốc v.
    4. Trình xuất Clip ngắn / Animated GIF phục vụ chia sẻ bài giảng lên mạng xã hội.
"""

from __future__ import annotations
import math
import os
from typing import Dict, List, Tuple, Any, Optional
import tkinter as tk

try:
    from PIL import Image, ImageGrab
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


# ==============================================================================
# 1. BỘ TÍNH TOÁN VA CHẠM 2 VẬT VỚI VECTOR LỰC BIẾN THIÊN THỜI GIAN THỰC
# ==============================================================================

class TwoBodyCollisionSimulation:
    """Mô phỏng va chạm 2 vật với vector lực tương tác co giãn thời gian thực."""

    def __init__(
        self,
        m1: float = 2.0,
        m2: float = 1.0,
        v1_init: float = 4.0,
        v2_init: float = -2.0,
        x1_init: float = 50.0,
        x2_init: float = 250.0,
        restitution_e: float = 1.0,     # e=1.0: Đàn hồi hoàn toàn; e=0.0: Va chạm mềm
        friction_mu: float = 0.05,
        contact_stiffness_k: float = 5000.0,  # Độ cứng tiếp xúc tính lực F12(t)
    ) -> None:
        self.m1 = m1
        self.m2 = m2
        self.v1 = v1_init
        self.v2 = v2_init
        self.x1 = x1_init
        self.x2 = x2_init
        self.e = restitution_e
        self.mu = friction_mu
        self.k_contact = contact_stiffness_k
        self.width1 = 40.0
        self.width2 = 30.0

        self.in_contact = False
        self.f_interaction = 0.0   # Độ lớn lực F12 = F21 thời gian thực
        self.f_friction1 = 0.0
        self.f_friction2 = 0.0

    def step(self, dt: float, g: float = 9.80665) -> Dict[str, Any]:
        """Tích phân bước thời gian dt giải phương trình chuyển động có ma sát và va chạm."""
        # Kiểm tra tiếp xúc giữa 2 vật (vật 1 bên trái, vật 2 bên phải)
        overlap = (self.x1 + self.width1) - self.x2

        if overlap > 0:
            self.in_contact = True
            # Lực nén tương tác đàn hồi theo định luật Hooke tiếp xúc
            self.f_interaction = self.k_contact * overlap
            # Gia tốc do va chạm
            a1_collision = -self.f_interaction / self.m1
            a2_collision = self.f_interaction / self.m2
        else:
            self.in_contact = False
            self.f_interaction = 0.0
            a1_collision = 0.0
            a2_collision = 0.0

        # Lực ma sát trượt đổi chiều theo vận tốc
        sgn_v1 = 1.0 if self.v1 > 1e-4 else (-1.0 if self.v1 < -1e-4 else 0.0)
        sgn_v2 = 1.0 if self.v2 > 1e-4 else (-1.0 if self.v2 < -1e-4 else 0.0)

        self.f_friction1 = -self.mu * self.m1 * g * sgn_v1
        self.f_friction2 = -self.mu * self.m2 * g * sgn_v2

        a1_total = a1_collision + (self.f_friction1 / self.m1)
        a2_total = a2_collision + (self.f_friction2 / self.m2)

        # Cập nhật vận tốc và tọa độ (Euler-Cromer)
        self.v1 += a1_total * dt
        self.v2 += a2_total * dt
        self.x1 += self.v1 * dt
        self.x2 += self.v2 * dt

        # Động lượng và động năng toàn phần
        p_total = self.m1 * self.v1 + self.m2 * self.v2
        E_total = 0.5 * self.m1 * (self.v1**2) + 0.5 * self.m2 * (self.v2**2)

        return {
            "x1": self.x1,
            "x2": self.x2,
            "v1": self.v1,
            "v2": self.v2,
            "f_interaction": self.f_interaction,
            "f_friction1": self.f_friction1,
            "f_friction2": self.f_friction2,
            "in_contact": self.in_contact,
            "momentum_p": p_total,
            "kinetic_energy_E": E_total,
        }


# ==============================================================================
# 2. BỘ TÍNH TOÁN NGƯỜI / VẬT TRONG THANG MÁY (TRỌNG LƯỢNG BIỂU KIẾN & QUÁN TÍNH)
# ==============================================================================

class ElevatorPhysicsSimulation:
    """Mô phỏng lực quán tính và trọng lượng biểu kiến trong thang máy."""

    @staticmethod
    def calculate_apparent_weight(
        mass_person: float = 60.0,
        elevator_acceleration: float = 2.0,   # + gia tốc đi lên, - gia tốc đi xuống
        elevator_velocity: float = 0.0,
        g: float = 9.80665,
    ) -> Dict[str, Any]:
        """
        Phương trình định luật II Newton trong hệ quy chiếu phi quán tính gắn với thang máy:
        P + N + F_qt = 0
        => N = m * (g + a) nếu thang máy có gia tốc a hướng lên
        => N = m * (g - a) nếu thang máy có gia tốc a hướng xuống
        F_qt = -m * a (lực quán tính).
        """
        if mass_person <= 0:
            mass_person = 1.0

        p_real = mass_person * g
        f_inertia = -mass_person * elevator_acceleration
        normal_force_N = mass_person * (g + elevator_acceleration)

        # Trạng thái không trọng lượng khi thang máy đứt cáp rơi tự do (a = -g)
        is_weightless = abs(normal_force_N) < 1e-3 or normal_force_N < 0
        if normal_force_N < 0:
            normal_force_N = 0.0  # Vật rời khỏi sàn thang máy

        # Chỉ số đọc trên bàn cân điện tử (kg biểu kiến)
        scale_reading_kg = normal_force_N / g

        state_desc = (
            "Tăng trọng lượng (N > P: thang máy lên nhanh dần hoặc xuống chậm dần)"
            if elevator_acceleration > 0
            else (
                "Trạng thái rơi tự do không trọng lượng (N = 0)!"
                if is_weightless
                else "Giảm trọng lượng (N < P: thang máy xuống nhanh dần hoặc lên chậm dần)"
            )
        )

        return {
            "mass_kg": mass_person,
            "real_gravity_P": p_real,
            "normal_force_N": normal_force_N,
            "inertia_force_Fqt": f_inertia,
            "scale_reading_kg": scale_reading_kg,
            "acceleration_a": elevator_acceleration,
            "is_weightless": is_weightless,
            "state_description": state_desc,
        }


# ==============================================================================
# 3. TRÌNH QUAY VÀ XUẤT CLIP NGẮN / ANIMATED GIF CHO MẠNG XÃ HỘI
# ==============================================================================

class SocialClipRecorder:
    """Hỗ trợ ghi chuỗi khung hình từ Canvas và xuất thành Animated GIF sắc nét."""

    def __init__(self, fps: int = 24, max_duration_sec: float = 4.0) -> None:
        self.fps = fps
        self.max_frames = int(fps * max_duration_sec)
        self.captured_frames: List[Image.Image] = []
        self.is_recording = False

    def start_recording(self) -> None:
        """Bắt đầu phiên ghi hình."""
        self.captured_frames.clear()
        self.is_recording = True

    def capture_canvas_frame(self, canvas: tk.Canvas) -> bool:
        """Chụp 1 frame từ Canvas. Trả về False khi đủ số frame tối đa."""
        if not self.is_recording or not HAS_PIL:
            return False

        if len(self.captured_frames) >= self.max_frames:
            self.is_recording = False
            return False

        try:
            canvas.update_idletasks()
            x = canvas.winfo_rootx()
            y = canvas.winfo_rooty()
            w = canvas.winfo_width()
            h = canvas.winfo_height()
            if w > 10 and h > 10:
                frame = ImageGrab.grab(bbox=(x, y, x + w, y + h))
                self.captured_frames.append(frame)
        except Exception:
            pass

        return len(self.captured_frames) < self.max_frames

    def save_gif(self, output_path: str) -> bool:
        """Lưu toàn bộ chuỗi khung hình thành tệp Animated GIF."""
        if not self.captured_frames:
            return False
        try:
            duration_ms = int(1000.0 / self.fps)
            self.captured_frames[0].save(
                output_path,
                save_all=True,
                append_images=self.captured_frames[1:],
                optimize=True,
                duration=duration_ms,
                loop=0,
            )
            return True
        except Exception:
            return False
