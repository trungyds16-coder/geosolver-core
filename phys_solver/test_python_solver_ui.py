# -*- coding: utf-8 -*-
"""
Unit test kiểm thử giao diện phân tích Python thuần và AI Co-Pilot trong ModularPhysicsCADStudio.
Đảm bảo nút phân tích Python thuần và Left Toolbox luôn hiện hữu, hoạt động tức thì.
"""
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import tkinter as tk
from phys_solver.app import ModularPhysicsCADStudio


class TestPhysLabPythonAndAIFeatures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = ModularPhysicsCADStudio()
        cls.app.withdraw()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.app.destroy()
        except Exception:
            pass

    def test_left_toolbox_and_buttons_exist(self):
        """Kiểm tra thanh công cụ bên trái (Left Toolbox) và các nút chủ đề / công cụ."""
        self.assertTrue(hasattr(self.app, "left_toolbox"), "Left Toolbox panel phải tồn tại.")
        self.assertTrue(hasattr(self.app, "btn_left_python"), "Nút Phân tích Python trên Left Toolbox phải có.")
        self.assertEqual(self.app.btn_left_python.cget("text"), "⚡ Phân tích Python (F4)")

    def test_dual_action_buttons_right_hud_and_bottom(self):
        """Kiểm tra sự hiện diện độc lập của nút Python thuần và nút AI trên Right HUD & Bottom Bar."""
        # Right HUD
        self.assertTrue(hasattr(self.app, "btn_python_solve"), "Nút Python trên Right HUD phải tồn tại.")
        self.assertTrue(hasattr(self.app, "btn_ai_solve"), "Nút AI trên Right HUD phải tồn tại.")
        self.assertIn("Python", self.app.btn_python_solve.cget("text"))
        self.assertIn("AI", self.app.btn_ai_solve.cget("text"))

        # Bottom Bar
        self.assertTrue(hasattr(self.app, "btn_bottom_python"), "Nút Python trên Bottom Bar phải tồn tại.")
        self.assertTrue(hasattr(self.app, "btn_bottom_ai"), "Nút AI trên Bottom Bar phải tồn tại.")

    def test_all_11_physics_topics_ground_truth(self):
        """Kiểm thử tính toán giải tích Python thuần cho toàn bộ các dạng thí nghiệm trên Blackboard."""
        test_kinds = [
            ("collision_2box", "Va chạm 2 khối hộp"),
            ("elevator_scale", "Thang máy & Cân lò xo"),
            ("inclined_plane", "Dốc nghiêng ma sát"),
            ("spring_vertical", "Con lắc lò xo treo thẳng đứng"),
            ("spring_horizontal", "Con lắc lò xo nằm ngang"),
            ("pendulum_rk4", "Con lắc đơn phi tuyến RK4"),
            ("pendulum_peg", "Con lắc vướng đinh"),
            ("fluid_venturi", "Ống Venturi Bernoulli"),
            ("fluid_torricelli", "Bình Torricelli phụt nước"),
            ("fluid_stokes", "Hạt rơi nhớt Stokes"),
            ("thermo_carnot", "Chu trình Carnot 4 kỳ"),
            ("thermo_piston", "Xilanh pít-tông khí"),
            ("circuit_rlc", "Mạch RLC nối tiếp xoay chiều"),
            ("circuit_wheatstone", "Mạch cầu Wheatstone"),
            ("meter_voltmeter_sgk", "Vôn kế kim SGK"),
            ("meter_ammeter_sgk", "Ampe kế kim SGK"),
            ("em_lorentz_helix", "Hạt Lorentz Cyclotron"),
            ("em_lenz_rod", "Thanh ray cảm ứng Lenz"),
            ("optics_prism_cauchy", "Lăng kính tán sắc Cauchy"),
            ("optics_thin_lens", "Thấu kính mỏng hội tụ"),
            ("nuclear_bohr", "Mẫu nguyên tử Bohr"),
            ("nuclear_reaction", "Cân bằng phản ứng hạt nhân"),
        ]

        for kind, title in test_kinds:
            exp_data = {"name": title, "kind": kind, "params": {}}
            gt_text = self.app._generate_ground_truth_solution(exp_data)
            self.assertIn("PYTHON THUẦN GROUND TRUTH", gt_text)
            self.assertIn("KẾT LUẬN: ĐÃ GIẢI TÍCH CHÍNH XÁC 100%", gt_text)
            self.assertGreater(len(gt_text), 100)

    def test_python_solve_click_execution(self):
        """Kiểm thử bấm nút [ ⚡ Phân tích Python (F4) ] cập nhật tức thời giao diện."""
        self.app.clear_blackboard()
        self.app.add_to_blackboard("inclined_plane", "Dốc nghiêng FBD")
        self.app._on_python_solve_click()

        sol_text = self.app.txt_solution.get("1.0", "end")
        self.assertIn("PHÂN TÍCH VECTOR LỰC", sol_text)
        self.assertIn("Gia tốc trượt dọc dốc", sol_text)
        self.assertFalse(self.app._ai_solving_active)

    def test_dynamic_profile_switching(self):
        """Kiểm tra thay đổi combobox profile cập nhật nhãn nút F5 phù hợp."""
        # Profile 0: Thuần Python
        self.app.combo_ai_profile.current(0)
        self.app._on_ai_profile_changed()
        self.assertIn("Python", self.app.btn_ai_solve.cget("text"))

        # Profile 1: AI DeepSeek / Qwen
        self.app.combo_ai_profile.current(1)
        self.app._on_ai_profile_changed()
        self.assertIn("AI", self.app.btn_ai_solve.cget("text"))


if __name__ == "__main__":
    unittest.main()
