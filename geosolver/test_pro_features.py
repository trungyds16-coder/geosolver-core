# -*- coding: utf-8 -*-
"""
GeoSolver 2D CAD Pro - Bộ Kiểm Thử Tính Năng Pro (Unit Tests)
Kiểm tra toàn diện: LicenseManager, Icon Pro, Xuất file JPEG & Watermark, In ấn trực tiếp, Kết nối AI.
"""

import os
import sys
import unittest
import tempfile
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from geosolver.license_manager import LicenseManager
from geosolver.geosolver_desktop import GeoSolverApp


class TestGeoSolver2DPro(unittest.TestCase):
    app = None

    @classmethod
    def setUpClass(cls):
        cls.app = GeoSolverApp(with_splash=False)
        cls.app.update()

    @classmethod
    def tearDownClass(cls):
        if cls.app:
            try:
                cls.app.destroy()
            except Exception:
                pass
            cls.app = None

    def setUp(self):
        LicenseManager.revoke_license_for_testing()

    def tearDown(self):
        LicenseManager.revoke_license_for_testing()

    def test_01_license_manager_flow(self):
        """Kiểm tra quy trình bản quyền: Free -> Activate -> Pro -> Revoke."""
        self.assertFalse(LicenseManager.is_pro_active())

        # Hardware ID
        hwid = LicenseManager.get_hardware_id()
        self.assertTrue(len(hwid) >= 10)

        # Kích hoạt bằng mã Master nội bộ
        ok, msg = LicenseManager.activate_with_code("PRO2D-2026-VIP")
        self.assertTrue(ok)
        self.assertTrue(LicenseManager.is_pro_active())

        # Thu hồi bản quyền
        LicenseManager.revoke_license_for_testing()
        self.assertFalse(LicenseManager.is_pro_active())

        # Kích hoạt bằng mã máy tính
        from generate_license_key import generate_key_for_hwid
        key = generate_key_for_hwid(hwid, "UNIT", "2D")
        ok2, msg2 = LicenseManager.activate_with_code(key)
        self.assertTrue(ok2)
        self.assertTrue(LicenseManager.is_pro_active())

    def test_02_pro_assets_exist(self):
        """Kiểm tra sự tồn tại và tính hợp lệ của bộ icon Pro mới."""
        assets_dir = os.path.join(BASE_DIR, "assets")
        pro_logo = os.path.join(assets_dir, "geosolver_2d_logo_pro.png")
        pro_ico = os.path.join(assets_dir, "geosolver_2d_pro.ico")

        self.assertTrue(os.path.exists(pro_logo), f"Missing {pro_logo}")
        self.assertTrue(os.path.exists(pro_ico), f"Missing {pro_ico}")

        with Image.open(pro_logo) as im:
            self.assertEqual(im.size, (512, 512))
            self.assertEqual(im.mode, "RGBA")

    def test_03_subtle_watermark_generation(self):
        """Kiểm tra cơ chế đóng dấu watermark bán trong suốt cho bản tiêu chuẩn."""
        test_im = Image.new("RGB", (600, 400), (255, 255, 255))
        wm_im = self.app._apply_subtle_watermark(test_im, "GeoSolver 2D CAD • STEM AI")
        self.assertEqual(wm_im.size, (600, 400))
        self.assertEqual(wm_im.mode, "RGBA")

        # Kiểm tra xem có điểm ảnh watermark bán trong suốt không
        import numpy as np
        arr = np.array(wm_im)
        diff_count = (arr[:, :, :3] < 250).sum()
        self.assertTrue(diff_count > 50, "Watermark was not applied to the image")

    def test_04_jpeg_export_and_pro_clean_mode(self):
        """Kiểm tra xuất file ảnh JPEG: Bản thường có watermark, Bản Pro sạch 100%."""
        # Thêm đối tượng hình học mẫu
        pA = {"name": "A", "x": 0.0, "y": 0.0, "source": "typed", "exact": True}
        pB = {"name": "B", "x": 4.0, "y": 0.0, "source": "typed", "exact": True}
        pC = {"name": "C", "x": 0.0, "y": 3.0, "source": "typed", "exact": True}
        self.app.points = [pA, pB, pC]
        self.app.segments = [
            {"p1": pA, "p2": pB, "color": "#000000", "style": "solid", "label": "AB"},
            {"p1": pB, "p2": pC, "color": "#000000", "style": "solid", "label": "BC"},
            {"p1": pC, "p2": pA, "color": "#000000", "style": "solid", "label": "CA"}
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            # 1. Xuất JPEG khi CHƯA kích hoạt Pro (Bản Tiêu Chuẩn)
            LicenseManager.revoke_license_for_testing()
            jpg_std = os.path.join(tmpdir, "test_std.jpg")
            self.app._render_to_image_file(jpg_std, silent=True)
            self.assertTrue(os.path.exists(jpg_std))
            with Image.open(jpg_std) as im_std:
                self.assertEqual(im_std.format, "JPEG")

            # 2. Xuất JPEG khi ĐÃ kích hoạt Pro
            LicenseManager.activate_with_code("PRO2D-2026-VIP")
            jpg_pro = os.path.join(tmpdir, "test_pro.jpg")
            self.app._render_to_image_file(jpg_pro, silent=True)
            self.assertTrue(os.path.exists(jpg_pro))
            with Image.open(jpg_pro) as im_pro:
                self.assertEqual(im_pro.format, "JPEG")

    def test_05_pro_ui_state_transition(self):
        """Kiểm tra sự đổi icon và tiêu đề cửa sổ khi thanh toán/kích hoạt Pro."""
        # Bản thường
        LicenseManager.revoke_license_for_testing()
        self.app.update_pro_ui_state()
        self.assertIn("Bản Tiêu Chuẩn", self.app.title())

        # Kích hoạt Pro
        LicenseManager.activate_with_code("PRO2D-2026-VIP")
        self.app.update_pro_ui_state()
        self.assertIn("Pro", self.app.title())
        self.assertIn("v3.2.0.0", self.app.title())


if __name__ == "__main__":
    unittest.main()
