# -*- coding: utf-8 -*-
"""
Kiểm thử tự động tính năng AI Co-Pilot trong CAD Math Studio v2.1
"""
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import tkinter as tk
from cad_math_v2.cad_math_v2 import CADMathDesktopAppV2, _AI_HUB_AVAILABLE


class TestCADMathAIFeatures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.root.withdraw()
        cls.app = CADMathDesktopAppV2(cls.root)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.root.destroy()
        except Exception:
            pass

    def test_ai_hub_available(self):
        self.assertTrue(_AI_HUB_AVAILABLE, "stem_shared_core AI modules should be available")

    def test_ui_ai_elements_exist(self):
        # 1. Nút cấu hình AI trên header
        self.assertTrue(hasattr(self.app, "btn_ai_config_header"))
        # 2. Thanh công cụ AI Toolbar
        self.assertTrue(hasattr(self.app, "ai_toolbar"))
        # 3. Combobox profile AI với 5 lựa chọn (bao gồm Qwen 2.5 Coder 7B)
        self.assertTrue(hasattr(self.app, "combo_ai_profile"))
        self.assertEqual(len(self.app.combo_ai_profile["values"]), 4)
        # Kiểm tra sự xuất hiện của Qwen trong danh sách profile
        qwen_profile_found = any("qwen" in v.lower() for v in self.app.combo_ai_profile["values"])
        self.assertTrue(qwen_profile_found, "Profile Qwen 2.5 Coder phải có trong combo_ai_profile")
        # 4. Nút [ 🤖 AI Phân Tích (F5) ]
        self.assertTrue(hasattr(self.app, "btn_ai_solve"))
        self.assertIn("AI giải toán", self.app.btn_ai_solve.cget("text"))

    def test_active_tab_problem_info(self):
        # Kiểm tra trích xuất thông tin tab
        self.app.notebook.select(0)
        self.app.eq_entry.delete("1.0", tk.END)
        self.app.eq_entry.insert(tk.END, "x^2 - 4 = 0")
        title, desc, gt = self.app._get_active_tab_problem_info()
        self.assertIn("phương trình", title.lower())
        self.assertIn("x^2 - 4 = 0", desc)

    def test_profile_0_restore(self):
        # Profile 0: thuần Python
        self.app.combo_ai_profile.current(0)
        self.app._on_ai_solve_click()
        self.assertFalse(self.app._ai_solving_active)


if __name__ == "__main__":
    unittest.main()
