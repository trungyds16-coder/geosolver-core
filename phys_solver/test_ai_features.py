# -*- coding: utf-8 -*-
"""
Kiểm thử tự động tính năng AI Co-Pilot trong ModularPhysicsCADStudio
"""
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import tkinter as tk
from phys_solver.app import ModularPhysicsCADStudio, _AI_MODULES_AVAILABLE


class TestPhysLabAIFeatures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Tạo ứng dụng và ẩn cửa sổ khi test
        cls.app = ModularPhysicsCADStudio()
        cls.app.withdraw()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.app.destroy()
        except Exception:
            pass

    def test_ai_modules_available(self):
        self.assertTrue(_AI_MODULES_AVAILABLE, "stem_shared_core AI modules should be available")

    def test_ui_ai_elements_exist(self):
        # 1. Nút cấu hình AI trên top bar
        self.assertTrue(hasattr(self.app, "btn_ai_hub_top"))
        # 2. Combobox profile AI trên Right HUD với 5 profiles (có Qwen 2.5 Coder)
        self.assertTrue(hasattr(self.app, "combo_ai_profile"))
        self.assertEqual(len(self.app.combo_ai_profile["values"]), 4)
        qwen_found = any("qwen" in v.lower() for v in self.app.combo_ai_profile["values"])
        self.assertTrue(qwen_found, "Profile Qwen 2.5 Coder 7B phải có trong combo_ai_profile")
        # 3. Nút [ 🤖 AI Phân Tích (F5) ]
        self.assertTrue(hasattr(self.app, "btn_ai_solve"))
        # 4. Nút [ 🤖 AI Phân Tích ] trên bottom toolbar
        self.assertTrue(hasattr(self.app, "btn_bottom_ai"))

    def test_profile_0_python_ground_truth(self):
        # Profile 0: thuần Python
        self.app.combo_ai_profile.current(0)
        self.app._on_ai_solve_click()
        sol_text = self.app.txt_solution.get("1.0", "end")
        self.assertIn("1.", sol_text)
        self.assertFalse(self.app._ai_solving_active)

    def test_prompt_generation_and_guardrails(self):
        # Kiểm tra nội dung Ground Truth và thông số thí nghiệm
        exp_data = self.app._current_exp()
        self.assertIsNotNone(exp_data)
        self.assertIn("name", exp_data)
        self.assertGreater(len(self.app.latest_solution_text), 10)


if __name__ == "__main__":
    unittest.main()
