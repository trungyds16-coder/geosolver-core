# -*- coding: utf-8 -*-
"""
Bộ kiểm thử tự động chuyên sâu GeoSolver 2D v3.1 (100% gọi trực tiếp mã nguồn Production):
- test_01: Ca dương tính tam giác đều vô tỉ (gọi classify_triangle)
- test_02: Ca hồi quy lỗi gốc tam giác cân A(0,5), B(-3,0), C(3,0) (gọi classify_triangle)
- test_03: Thuộc tính bất biến tỷ lệ theo thang 10^-k (k=0..3) trên tọa độ rời rạc
- test_04: Ca số thập phân gõ tay của Claude (5, 8.7) và (0.04, 3) không bị nhận nhầm
- test_05: Ca âm tính tam giác đều với tọa độ thực tự do (gọi classify_triangle)
- test_06: Ca biên 3 điểm thẳng hàng và điểm trùng nhau (gọi classify_triangle)
- test_07: Ca tam giác vuông và vuông cân trên lưới rời rạc (gọi classify_triangle)
- test_08: Hình elip toàn diện: chuẩn, F1==F2, suy biến b=0, tiêu điểm nghiêng 53.13° và đổi F1/F2
- test_09: Chu vi Ramanujan II so với tích phân số học quy tắc trung điểm 100.000 bước
- test_10: Đo tương phản 20 cặp màu thực tế trên THEMES_GEOSOLVER theo chuẩn W3C WCAG 2.1 AA
- test_11: Kiểm tra Clean Print Mode toggle mặc định tắt và tệp cẩm nang F1
- test_12: Kiểm tra bảo mật DPAPI KeyStore (chống Use-After-Free) và hf_downloader SHA-256
"""

import math
import unittest
import sys
import os
import tempfile
import hashlib
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from geosolver.geosolver_desktop import (
    classify_triangle,
    format_radical_len,
    compute_ellipse_from_foci,
    calc_ellipse_perimeter,
    calc_ellipse_area,
    THEMES_GEOSOLVER,
)
from stem_shared_core.ai_local_manager import GeminiKeyStore
from stem_shared_core.hf_downloader import HFModelDownloader, DownloadError

class TestGeometryInvariants(unittest.TestCase):

    def test_01_true_positive_equilateral_triangle(self):
        """Ca dương tính: Tam giác đều thực sự với tọa độ vô tỉ (gọi trực tiếp classify_triangle)"""
        h = math.sqrt(3)
        res = classify_triangle((0.0, 2.0 * h), (-3.0, -h), (3.0, -h), lang="vi")
        self.assertTrue(res["is_triangle"])
        self.assertEqual(res["type"], "equilateral")
        self.assertTrue(res["is_equilateral"])
        self.assertFalse(res["all_int"])

    def test_02_regression_original_bug_isosceles_not_equilateral(self):
        """Hồi quy lỗi gốc: A(0, 5), B(-3, 0), C(3, 0) phải nhận diện là tam giác cân tại A, không báo nhầm đều."""
        res = classify_triangle((0.0, 5.0), (-3.0, 0.0), (3.0, 0.0), lang="vi")
        self.assertTrue(res["is_triangle"])
        self.assertEqual(res["type"], "isosceles")
        self.assertEqual(res["vertex"], "A")
        self.assertFalse(res["is_equilateral"])
        self.assertTrue(res["all_int"])
        self.assertEqual(res["side_labels"]["AB"], "√34 (≈ 5.83)")
        self.assertEqual(res["side_labels"]["BC"], "6")

    def test_03_scale_invariance_property(self):
        """Thuộc tính bất biến tỷ lệ theo thang 10^-k (k=0..3) trên tọa độ rời rạc"""
        # 1. Tam giác A(0,0), B(10,30), C(29,13) nhân với 1, 0.1, 0.01, 0.001 phải luôn là scalene
        base_tri = [(0.0, 0.0), (10.0, 30.0), (29.0, 13.0)]
        for k in range(4):
            factor = 10.0 ** (-k)
            scaled = [(p[0] * factor, p[1] * factor) for p in base_tri]
            r = classify_triangle(*scaled, lang="vi")
            self.assertEqual(r["type"], "scalene", f"Tam giác tại thang 10^-{k} bắt buộc phải là scalene (tam giác thường)")

        # 2. Tam giác vuông cân (0,0), (4,0), (0,4) nhân với 1, 0.1, 0.01, 0.001 phải luôn là right_isosceles
        right_base = [(0.0, 0.0), (4.0, 0.0), (0.0, 4.0)]
        for k in range(4):
            factor = 10.0 ** (-k)
            scaled = [(p[0] * factor, p[1] * factor) for p in right_base]
            r = classify_triangle(*scaled, lang="vi")
            self.assertEqual(r["type"], "right_isosceles", f"Tam giác vuông cân tại thang 10^-{k} phải luôn là right_isosceles")

    def test_04_typed_decimals_rejection_claude_cases(self):
        """Ca số thập phân gõ tay của Claude (5, 8.7) và (0.04, 3) không bị nhận nhầm"""
        # a) Tam giác A(0,0), B(10,0), C(5, 8.7): AB=10, AC=BC=sqrt(100.69) ≈ 10.034
        # Trên lưới rời rạc (s=10), d^2(AB)=10000 != 10069 == 10069 => Bắt buộc là tam giác cân tại C, KHÔNG ĐƯỢC báo đều
        r_eq = classify_triangle((0.0, 0.0), (10.0, 0.0), (5.0, 8.7), lang="vi")
        self.assertEqual(r_eq["type"], "isosceles")
        self.assertEqual(r_eq["vertex"], "C")
        self.assertFalse(r_eq["is_equilateral"])

        # b) Tam giác A(0,0), B(4,0), C(0.04, 3): Góc tại A là 89.24 độ != 90 độ
        # Tích vô hướng s=100: 400*4 = 1600 != 0 => Bắt buộc là scalene, KHÔNG ĐƯỢC báo vuông
        r_rt = classify_triangle((0.0, 0.0), (4.0, 0.0), (0.04, 3.0), lang="vi")
        self.assertEqual(r_rt["type"], "scalene")
        self.assertFalse(r_rt["is_right"])

    def test_05_negative_equilateral_pure_float_coordinates(self):
        """Ca âm tính độc lập: Dung sai 0.6% trên tọa độ thực tự do loại trừ tam giác lệch 1.8%"""
        res = classify_triangle((0.123, 5.456), (-3.123, 0.123), (3.123, 0.123), lang="vi")
        self.assertTrue(res["is_triangle"])
        self.assertFalse(res["all_int"])
        self.assertFalse(res["is_equilateral"])

    def test_06_collinear_and_coincident_points(self):
        """Ca biên: 3 điểm thẳng hàng và điểm trùng nhau không tạo thành tam giác"""
        res_col_int = classify_triangle((1.0, 2.0), (3.0, 6.0), (5.0, 10.0))
        self.assertFalse(res_col_int["is_triangle"])
        self.assertEqual(res_col_int["type"], "collinear")

        res_col_flt = classify_triangle((1.1, 2.2), (3.3, 6.6), (5.5, 11.0))
        self.assertFalse(res_col_flt["is_triangle"])
        self.assertEqual(res_col_flt["type"], "collinear")

        res_coin = classify_triangle((2.5, 3.5), (2.5, 3.5), (7.0, 9.0))
        self.assertFalse(res_coin["is_triangle"])
        self.assertEqual(res_coin["type"], "coincident")

    def test_07_right_and_right_isosceles_triangles(self):
        """Ca tam giác vuông và vuông cân trên lưới rời rạc"""
        res_iso_right = classify_triangle((0.0, 0.0), (4.0, 0.0), (0.0, 4.0))
        self.assertTrue(res_iso_right["is_triangle"])
        self.assertEqual(res_iso_right["type"], "right_isosceles")
        self.assertEqual(res_iso_right["vertex"], "A")

        res_right = classify_triangle((0.0, 0.0), (3.0, 0.0), (0.0, 4.0))
        self.assertTrue(res_right["is_triangle"])
        self.assertEqual(res_right["type"], "right")
        self.assertEqual(res_right["vertex"], "A")
        self.assertFalse(res_right["is_isosceles"])

    def test_08_ellipse_edge_cases_and_rotational_invariance(self):
        """Hình elip toàn diện: chuẩn, F1==F2, suy biến b=0, tiêu điểm nghiêng 53.13° và đổi F1/F2"""
        el_std = compute_ellipse_from_foci(-3.0, 0.0, 3.0, 0.0, 0.0, 4.0)
        self.assertAlmostEqual(el_std["a"], 5.0)
        self.assertAlmostEqual(el_std["b"], 4.0)

        el_circle = compute_ellipse_from_foci(0.0, 0.0, 0.0, 0.0, 0.0, 4.0)
        self.assertAlmostEqual(el_circle["a"], 4.0)
        self.assertAlmostEqual(el_circle["b"], 4.0)

        # F1(-2,0), F2(2,0), M(0,0) => c=2, a=2 => b=0, P=4a=8.0
        el_deg = compute_ellipse_from_foci(-2.0, 0.0, 2.0, 0.0, 0.0, 0.0)
        self.assertEqual(el_deg["b"], 0.0)
        self.assertEqual(el_deg["perimeter"], 8.0)

        # Tiêu điểm nghiêng: F1(1,1), F2(4,5) => dx=3, dy=4, theta = atan2(4,3) ≈ 53.13 độ
        el_rot1 = compute_ellipse_from_foci(1.0, 1.0, 4.0, 5.0, 0.0, 3.0)
        el_rot2 = compute_ellipse_from_foci(4.0, 5.0, 1.0, 1.0, 0.0, 3.0)
        self.assertAlmostEqual(el_rot1["a"], el_rot2["a"], places=6)
        self.assertAlmostEqual(el_rot1["b"], el_rot2["b"], places=6)
        self.assertAlmostEqual(el_rot1["area"], el_rot2["area"], places=6)
        self.assertAlmostEqual(el_rot1["perimeter"], el_rot2["perimeter"], places=6)
        angle_diff = abs(el_rot1["theta"] - el_rot2["theta"])
        self.assertAlmostEqual(math.sin(angle_diff), 0.0, places=6)

    def test_09_ramanujan_ii_exact_accuracy_table(self):
        """Chu vi Ramanujan II so với tích phân số học quy tắc trung điểm 100.000 bước"""
        def numerical_integral_perimeter(a, b, steps=100000):
            dt = (math.pi / 2.0) / steps
            s = sum(math.sqrt(a*a * math.sin((i+0.5)*dt)**2 + b*b * math.cos((i+0.5)*dt)**2) for i in range(steps))
            return 4.0 * s * dt

        test_cases = [(5.0, 5.0), (5.0, 4.0), (5.0, 2.5), (5.0, 0.5), (5.0, 0.05), (5.0, 0.0)]
        for a, b in test_cases:
            p_ram = calc_ellipse_perimeter(a, b)
            p_exact = 4.0 * a if b == 0.0 else numerical_integral_perimeter(a, b)
            rel_err = abs(p_ram - p_exact) / p_exact
            self.assertLess(rel_err, 0.00041, f"Ramanujan II tại a={a}, b={b} có sai số {rel_err*100:.6f}% < 0.041%")

    def test_10_wcag_21_aa_itemized_real_contrast(self):
        """Đo tương phản 20 cặp màu thực tế trên THEMES_GEOSOLVER theo chuẩn W3C WCAG 2.1 AA"""
        def hex_to_luminance(hex_str):
            hex_str = hex_str.lstrip('#')
            r, g, b = [int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
            def adj(c): return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
            return 0.2126 * adj(r) + 0.7152 * adj(g) + 0.0722 * adj(b)

        def contrast_ratio(c1, c2):
            l1, l2 = hex_to_luminance(c1), hex_to_luminance(c2)
            if l1 < l2: l1, l2 = l2, l1
            return (l1 + 0.05) / (l2 + 0.05)

        for theme_key, t in THEMES_GEOSOLVER.items():
            self.assertGreaterEqual(contrast_ratio(t["text"], t["bg_window"]), 4.5)
            self.assertGreaterEqual(contrast_ratio(t["text"], t["toolbar_bg"]), 4.5)
            self.assertGreaterEqual(contrast_ratio(t["btn_fg"], t["btn_bg"]), 4.5)
            self.assertGreaterEqual(contrast_ratio(t["tool_active_fg"], t["tool_active_bg"]), 4.5)
            self.assertGreaterEqual(contrast_ratio(t["status_fg"], t["status_bg"]), 4.5)

    def test_11_clean_print_mode_and_handbook_dialog(self):
        """Kiểm tra Clean Print Mode toggle mặc định tắt và tệp cẩm nang F1"""
        # 1. Tệp cẩm nang tồn tại và có nội dung đầy đủ
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        handbook_path = os.path.join(base_dir, "CAM_NANG_SU_DUNG_STEM_CAD_MATH.md")
        self.assertTrue(os.path.isfile(handbook_path))
        self.assertGreater(os.path.getsize(handbook_path), 500)

        # 2. Kiểm tra mã nguồn khởi tạo mặc định của Clean Print Mode là False
        geosolver_path = os.path.join(base_dir, "geosolver", "geosolver_desktop.py")
        with open(geosolver_path, "r", encoding="utf-8") as f:
            code = f.read()
        self.assertIn("self.var_show_dimensions = tk.BooleanVar(value=False)", code,
                      "Chế độ hiển thị kích thước cạnh var_show_dimensions bắt buộc phải mặc định là False (Clean Print)")

    def test_12_dpapi_keystore_and_downloader_sha256(self):
        """Kiểm tra bảo mật DPAPI KeyStore (chống Use-After-Free) và hf_downloader SHA-256"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 1. Kiểm tra DPAPI KeyStore roundtrip & migration
            key_path = Path(tmpdir) / "gemini_api_key.txt"
            ks = GeminiKeyStore(key_path)
            ks.save("AIzaSyTestKey_DPAPI_Verified")
            raw_text = key_path.read_text(encoding="utf-8")
            self.assertTrue(raw_text.startswith("DPAPI:"), "Tệp khóa trên Windows bắt buộc phải mã hóa có tiền tố DPAPI:")
            self.assertEqual(ks.read(), "AIzaSyTestKey_DPAPI_Verified")

            # 2. Kiểm tra hf_downloader: bắt buộc SHA-256
            dl = HFModelDownloader("https://fake.url/test.gguf", dest_dir=Path(tmpdir), expected_sha256="")
            dl.part_path.write_bytes(b"GGUF" + b"\x00" * 64)
            dl._total = 68
            with self.assertRaises(DownloadError):
                dl._verify()  # Bắt buộc raise vì thiếu SHA-256

            # 3. Kiểm tra hf_downloader: SHA-256 khớp case-insensitive
            valid_sha = hashlib.sha256(b"GGUF" + b"\x00" * 64).hexdigest()
            dl.part_path.write_bytes(b"GGUF" + b"\x00" * 64)
            dl.expected_sha256 = valid_sha.upper()
            dl._verify()  # Phải verify thành công

    def test_13_dpapi_fail_soft_on_corrupt_or_foreign_key(self):
        """Kiểm tra nguyên tắc fail-soft của GeminiKeyStore: không sập app khi file hỏng hoặc chuyển máy"""
        with tempfile.TemporaryDirectory() as tmpdir:
            key_path = Path(tmpdir) / "gemini_api_key.txt"
            ks = GeminiKeyStore(key_path)

            # a) File rác base64 không giải mã được
            key_path.write_text("DPAPI:dGhpcyBpcyBub3QgYSB2YWxpZCBkcGFwaSBibG9i", encoding="utf-8")
            orig_env = os.environ.get("GEMINI_API_KEY")
            try:
                if "GEMINI_API_KEY" in os.environ:
                    del os.environ["GEMINI_API_KEY"]
                # Bắt buộc trả về None, TUYỆT ĐỐI KHÔNG ĐƯỢC NÉM EXCEPTION làm sập app
                val = ks.read()
                self.assertIsNone(val, "Khi giải mã DPAPI thất bại, read() phải trả về None mà không làm sập ứng dụng")

                # b) Fallback về biến môi trường khi file hỏng
                os.environ["GEMINI_API_KEY"] = "AIzaSy_Env_Fallback_Key"
                self.assertEqual(ks.read(), "AIzaSy_Env_Fallback_Key")
            finally:
                if orig_env is not None:
                    os.environ["GEMINI_API_KEY"] = orig_env
                elif "GEMINI_API_KEY" in os.environ:
                    del os.environ["GEMINI_API_KEY"]

    def test_14_exact_right_triangle_float_coordinates_no_spurious_annotation(self):
        """Tam giác vuông thực sự có tọa độ vô tỉ (0,0), (√2,0), (0,√3): không được chú thích '(gần vuông, góc 0.0°)'"""
        pA = (0.0, 0.0)
        pB = (math.sqrt(2.0), 0.0)
        pC = (0.0, math.sqrt(3.0))
        res = classify_triangle(pA, pB, pC, lang="vi")
        self.assertTrue(res["is_triangle"])
        self.assertEqual(res["type"], "right")
        self.assertEqual(res["vertex"], "A")
        self.assertFalse(res["is_discrete"])
        # Kiểm tra không bị ghi chú lỗi góc 0.0°
        self.assertNotIn("gần vuông", res["description"], "Tam giác vuông chính xác góc 90° không được ghi 'gần vuông'")
        self.assertIn("AB ⊥ AC", res["description"])

    def test_15_float_near_right_and_near_right_isosceles_annotation(self):
        """Ca số thực tự do gần vuông và gần vuông cân: kiểm tra chú thích độ lệch và deviations dict"""
        # a) Gần vuông: góc 89.24 độ
        # Tọa độ có > 4 chữ số thập phân để đảm bảo rơi vào nhánh số thực tự do
        pA = (0.0, 0.0)
        pB = (4.000001, 0.0)
        pC = (0.040001, 3.0)
        res_near_rt = classify_triangle(pA, pB, pC, lang="vi")
        self.assertEqual(res_near_rt["type"], "right")
        self.assertIn("gần vuông, góc 89.2°", res_near_rt["description"])
        self.assertIn("angle_deg", res_near_rt["deviations"])
        self.assertAlmostEqual(res_near_rt["deviations"]["angle_deg"], 89.24, places=1)

        # b) Gần vuông cân: góc 90 độ, lệch 2 cạnh góc vuông nhỏ
        pA2 = (0.0, 0.0)
        pB2 = (4.010001, 0.0)
        pC2 = (0.0, 4.0)
        res_near_ri = classify_triangle(pA2, pB2, pC2, lang="vi")
        self.assertEqual(res_near_ri["type"], "right_isosceles")
        self.assertIn("gần vuông cân", res_near_ri["description"])
        self.assertIn("lệch cạnh", res_near_ri["description"])
        self.assertIn("leg_diff_pct", res_near_ri["deviations"])

    def test_16_dpapi_stress_round_trip_stability(self):
        """Kiểm tra áp lực 100 lần mã hóa/giải mã DPAPI với payload ngẫu nhiên 1KB để loại trừ rò rỉ vùng nhớ ctypes"""
        if os.name != "nt":
            self.skipTest("DPAPI chỉ khả dụng trên Windows")
        from stem_shared_core.ai_local_manager import _dpapi_encrypt, _dpapi_decrypt
        import random
        for i in range(100):
            payload = bytes([random.randint(0, 255) for _ in range(1024)])
            encrypted = _dpapi_encrypt(payload)
            decrypted = _dpapi_decrypt(encrypted)
            self.assertEqual(decrypted, payload, f"DPAPI stress failed at iteration {i}")

    def test_17_freehand_point_origin_flag_rejection(self):
        """Kiểm tra cờ nguồn gốc exact/source: vẽ chuột tự do dù toạ độ nguyên vẫn có exact=False"""
        # Điểm vẽ tự do tình cờ có tọa độ nguyên trên lưới pixel
        pA = {"x": 0.0, "y": 0.0, "source": "free"}
        pB = {"x": 3.0, "y": 0.0, "source": "free"}
        pC = {"x": 0.0, "y": 4.0, "source": "free"}
        res = classify_triangle(pA, pB, pC)
        self.assertFalse(res["is_discrete"], "Điểm vẽ tự do bị ép về nhánh liên tục dung sai (is_discrete=False)")
        self.assertFalse(res["exact"], "Khi nguồn gốc là 'free', thuộc tính exact bắt buộc là False")
        self.assertFalse(res["origin_exact"])

        # Khi chỉ định points_exact=False trực tiếp qua hàm
        res2 = classify_triangle((0, 0), (3, 0), (0, 4), points_exact=False)
        self.assertFalse(res2["exact"])

        # Khi điểm là typed hoặc grid_snap
        pA_snap = {"x": 0.0, "y": 0.0, "source": "grid_snap"}
        pB_snap = {"x": 3.0, "y": 0.0, "source": "grid_snap"}
        pC_snap = {"x": 0.0, "y": 4.0, "source": "grid_snap"}
        res3 = classify_triangle(pA_snap, pB_snap, pC_snap)
        self.assertTrue(res3["exact"])
        self.assertTrue(res3["origin_exact"])

    def test_18_format_radical_len_direct_unit_tests(self):
        """Kiểm tra trực tiếp format_radical_len với các mẫu căn thức và phân số phổ biến"""
        # Số nguyên chính phương: d_sq = 36 => 6
        self.assertEqual(format_radical_len(6.0, (0, 0), (6, 0)), "6")
        # Căn thức rút gọn: d_sq = 72 = 36 * 2 => 6√2
        self.assertEqual(format_radical_len(math.sqrt(72.0), (0, 0), (6, 6)), "6√2 (≈ 8.49)")
        # Căn thức nguyên tố: d_sq = 34 => √34
        self.assertEqual(format_radical_len(math.sqrt(34.0), (0, 5), (3, 0)), "√34 (≈ 5.83)")
        # Giá trị 0
        self.assertEqual(format_radical_len(0.0), "0")

    def test_19_ellipse_near_degenerate_a_approx_c(self):
        """Kiểm tra elip gần suy biến khi a tiệm cận c (b -> 0) không bị lỗi chia 0 hoặc căn số âm"""
        # F1(-4.999999, 0), F2(4.999999, 0), M(0, 0.0001) => c ≈ 5, a ≈ 5 => b rất nhỏ nhưng b >= 0
        el = compute_ellipse_from_foci(-4.999999, 0.0, 4.999999, 0.0, 0.0, 0.0001)
        self.assertGreaterEqual(el["b"], 0.0)
        self.assertAlmostEqual(el["a"], 5.0, places=4)
        # Chu vi phải tiệm cận đoạn thẳng 4a = 20.0
        self.assertAlmostEqual(el["perimeter"], 20.0, places=2)

    def test_20_hf_downloader_error_paths_comprehensive(self):
        """Kiểm tra các kịch bản lỗi của hf_downloader: sai magic GGUF, lệch kích thước, thiếu SHA-256"""
        with tempfile.TemporaryDirectory() as tmpdir:
            dl = HFModelDownloader("https://fake.url/test.gguf", dest_dir=Path(tmpdir), expected_sha256="abc")
            
            # 1. Sai magic bytes (không phải b'GGUF')
            dl.part_path.write_bytes(b"BAD!" + b"\x00" * 60)
            dl._total = 64
            with self.assertRaises(DownloadError) as ctx:
                dl._verify()
            self.assertEqual(ctx.exception.code, "integrity")
            self.assertIn("không phải tệp GGUF", ctx.exception.detail)

            # 2. Sai kích thước file (60 byte thay vì 64 byte)
            dl.part_path.write_bytes(b"GGUF" + b"\x00" * 56)
            dl._total = 64
            with self.assertRaises(DownloadError) as ctx2:
                dl._verify()
            self.assertEqual(ctx2.exception.code, "integrity")
            self.assertIn("kích thước", ctx2.exception.detail)

            # 3. Thiếu mã SHA-256
            dl.part_path.write_bytes(b"GGUF" + b"\x00" * 60)
            dl._total = 64
            dl.expected_sha256 = ""
            with self.assertRaises(DownloadError) as ctx3:
                dl._verify()
            self.assertEqual(ctx3.exception.code, "integrity")
            self.assertIn("thiếu mã băm SHA-256", ctx3.exception.detail)

    def test_21_mixed_point_origin_flag_behavior(self):
        """Kiểm tra logic trộn cờ nguồn gốc, thứ tự ưu tiên taint và xử lý xung đột cờ"""
        # Ca 1: A và B là typed (True), C là tuple không có metadata (None)
        pA = {"x": 0.0, "y": 0.0, "source": "typed"}
        pB = {"x": 3.0, "y": 0.0, "source": "typed"}
        pC = (0.0, 4.0)
        res_mixed = classify_triangle(pA, pB, pC)
        self.assertIsNone(res_mixed["origin_exact"], "Khi có điểm không rõ nguồn gốc (None), origin_exact bắt buộc là None")
        self.assertTrue(res_mixed["exact"], "Khi origin_exact là None, hệ thống dùng Heuristic số học is_discrete (tọa độ nguyên -> exact=True)")

        # Ca 2: A và C là typed (True), B là vẽ tự do (False)
        pA2 = {"x": 0.0, "y": 0.0, "source": "typed"}
        pB2 = {"x": 3.0, "y": 0.0, "source": "free"}
        pC2 = {"x": 0.0, "y": 4.0, "source": "typed"}
        res_free_taint = classify_triangle(pA2, pB2, pC2)
        self.assertFalse(res_free_taint["origin_exact"], "Chỉ cần 1 điểm vẽ tự do (False), origin_exact bắt buộc là False")
        self.assertFalse(res_free_taint["exact"], "Khi origin_exact là False, thuộc tính exact bắt buộc là False dù tọa độ nguyên")

        # Ca 3: Xung đột tham số - points_exact=True không được phép ghi đè điểm bị taint False
        res_taint_override = classify_triangle(pA2, pB2, pC2, points_exact=True)
        self.assertFalse(res_taint_override["origin_exact"], "points_exact=True KHÔNG ĐƯỢC PHÉP ghi đè điểm bị taint False")
        self.assertFalse(res_taint_override["exact"], "exact bắt buộc là False khi có điểm bị taint")

        # Ca 4: Xung đột trong chính dict điểm - vừa có source='free' vừa có exact=True
        p_contra = {"x": 3.0, "y": 0.0, "source": "free", "exact": True}
        res_contra = classify_triangle(pA2, p_contra, pC2)
        self.assertFalse(res_contra["origin_exact"], "Xung đột source='free' vs exact=True: Taint ưu tiên, origin_exact là False")
        self.assertFalse(res_contra["exact"], "exact bắt buộc là False khi có điểm xung đột mang thuộc tính free")

    def test_22_missing_coordinate_validation(self):
        """Kiểm tra xác thực dữ liệu điểm: thiếu x hoặc y phải ném ValueError, không được ngầm định bằng 0"""
        with self.assertRaises(ValueError):
            classify_triangle({"x": 1.0}, (2.0, 3.0), (4.0, 5.0))
        with self.assertRaises(ValueError):
            classify_triangle({"y": 1.0}, (2.0, 3.0), (4.0, 5.0))
        with self.assertRaises(ValueError):
            classify_triangle((1.0,), (2.0, 3.0), (4.0, 5.0))

    def test_23_micro_scale_invariance_scale_10_minus_5(self):
        """Kiểm tra bất biến tỷ lệ vi mô ở thang 10^-5: không trùng điểm và không nhận nhầm all_int"""
        s = 1e-5
        pA = (0.0, 0.0)
        pB = (3.0 * s, 0.0)
        pC = (0.0, 4.0 * s)
        res = classify_triangle(pA, pB, pC)
        self.assertTrue(res["is_triangle"], "Tam giác ở thang 10^-5 không được bị coi là trùng điểm")
        self.assertEqual(res["type"], "right")
        self.assertEqual(res["vertex"], "A")
        self.assertFalse(res["all_int"], "Tọa độ vi mô 10^-5 không được nhận nhầm là số nguyên (all_int=False)")
        self.assertFalse(res["is_discrete"], "Tọa độ 10^-5 vượt quá max_k=4 nên is_discrete phải là False")

    def test_24_gui_canvas_point_source_and_invariants_integration(self):
        """Kiểm tra tích hợp GUI Canvas: phát sự kiện click chuột thật để kiểm tra gán cờ source='free' và 'grid_snap'"""
        from geosolver.geosolver_desktop import GeoSolverApp
        import tkinter as tk
        app = None
        try:
            app = GeoSolverApp(with_splash=False)
            app.current_tool = "point"
            app.update()  # Map canvas lên Tkinter display pipeline

            # 1. Phát sự kiện click chuột thật khi KHÔNG bật snap_to_grid -> phải sinh ra source='free', exact=False
            app.snap_to_grid = False
            app._ask_point_name_dialog = lambda default_name: "P_free"
            app.canvas.event_generate("<ButtonPress-1>", x=150, y=150)
            app.update()

            self.assertTrue(len(app.points) >= 1, "Phát sự kiện <ButtonPress-1> phải sinh ra điểm trên Canvas")
            p_free = app.points[-1]
            self.assertEqual(p_free["source"], "free", "Click tự do không snap bắt buộc sinh ra source='free'")
            self.assertFalse(p_free["exact"], "Điểm sinh ra từ click chuột tự do bắt buộc có exact=False")

            # 2. Phát sự kiện click chuột thật khi BẬT snap_to_grid -> phải sinh ra source='grid_snap', exact=True
            app.snap_to_grid = True
            app._ask_point_name_dialog = lambda default_name: "P_snap"
            app.canvas.event_generate("<ButtonPress-1>", x=200, y=200)
            app.update()

            self.assertTrue(len(app.points) >= 2)
            p_snap = app.points[-1]
            self.assertEqual(p_snap["source"], "grid_snap", "Click khi bật snap bắt buộc sinh ra source='grid_snap'")
            self.assertTrue(p_snap["exact"], "Điểm sinh ra từ snap lưới bắt buộc có exact=True")

            # 3. Dựng tam giác từ điểm vẽ chuột tự do và quét bất biến
            app.points = [
                {"id": "A", "name": "A", "x": 0.0, "y": 0.0, "color": "#000", "fixed": False, "source": "free", "exact": False},
                {"id": "B", "name": "B", "x": 3.0, "y": 0.0, "color": "#000", "fixed": False, "source": "free", "exact": False},
                {"id": "C", "name": "C", "x": 0.0, "y": 4.0, "color": "#000", "fixed": False, "source": "free", "exact": False}
            ]
            app._scan_invariants_deep()
            invariants_text = app.txt_invariants.get("1.0", tk.END)
            self.assertIn("Tam giác vuông tại A", invariants_text)

            res = classify_triangle(app.points[0], app.points[1], app.points[2])
            self.assertFalse(res["exact"], "Điểm vẽ tự do từ Canvas GUI bắt buộc cho kết quả exact=False dù tọa độ nguyên")

            # 4. Kiểm tra kéo thả điểm (drag event): Điểm grid_snap bị kéo tự do khi tắt snap phải đổi thành source='dragged', exact=False
            app.snap_to_grid = False
            app.selected_points = [p_snap]
            app.drag_start_world = (p_snap["x"], p_snap["y"])
            app.canvas.event_generate("<B1-Motion>", x=250, y=250)
            app.update()
            self.assertEqual(p_snap["source"], "dragged", "Điểm bị kéo tự do bắt buộc đổi source='dragged'")
            self.assertFalse(p_snap["exact"], "Điểm bị kéo tự do bắt buộc có exact=False")
        finally:
            if app is not None:
                app.destroy()

    def test_25_gui_canvas_drag_typed_and_midpoint_parents_integration(self):
        """Kiểm tra Canvas GUI: Kéo điểm typed khi snap tắt thành dragged, và tạo trung điểm từ 2 điểm free lưu parents"""
        from geosolver.geosolver_desktop import GeoSolverApp, classify_triangle
        app = None
        try:
            app = GeoSolverApp(with_splash=False)
            app.update()

            # 1. Kéo điểm typed khi snap tắt -> source thành 'dragged', exact=False
            p_typed = {"id": "T1", "name": "T1", "x": 10.0, "y": 10.0, "color": "#000", "fixed": False, "source": "typed", "exact": True}
            app.points = [p_typed]
            app.snap_to_grid = False
            app.selected_points = [p_typed]
            app.drag_start_world = (10.0, 10.0)
            app.canvas.event_generate("<B1-Motion>", x=320, y=320)
            app.update()

            self.assertEqual(p_typed["source"], "dragged", "Kéo điểm typed khi snap_to_grid=False phải đổi source thành 'dragged'")
            self.assertFalse(p_typed["exact"], "Điểm typed sau khi bị kéo tự do bắt buộc có exact=False")

            # 2. Tạo trung điểm từ 2 điểm vẽ chuột tự do (free) thông qua công cụ 'midpoint' của Canvas
            p_free1 = {"id": "F1", "name": "F1", "x": 0.0, "y": 0.0, "color": "#000", "fixed": False, "source": "free", "exact": False}
            p_free2 = {"id": "F2", "name": "F2", "x": 4.0, "y": 0.0, "color": "#000", "fixed": False, "source": "free", "exact": False}
            app.points = [p_free1, p_free2]
            app.current_tool = "midpoint"
            app._ask_point_name_dialog = lambda default_name: "Mid_Free"

            sx1, sy1 = app.to_screen(p_free1["x"], p_free1["y"])
            app.canvas.event_generate("<ButtonPress-1>", x=int(sx1), y=int(sy1))
            app.update()

            sx2, sy2 = app.to_screen(p_free2["x"], p_free2["y"])
            app.canvas.event_generate("<ButtonPress-1>", x=int(sx2), y=int(sy2))
            app.update()

            self.assertEqual(len(app.points), 3, "Công cụ midpoint phải tạo thêm điểm thứ 3 trên Canvas")
            m_pt = app.points[-1]
            self.assertEqual(m_pt["source"], "midpoint")
            self.assertIn("parents", m_pt, "Điểm trung điểm bắt buộc phải lưu thuộc tính 'parents'")
            self.assertEqual(m_pt["parents"], [p_free1, p_free2], "parents phải chứa đúng 2 đối tượng điểm cha")

            # 3. Phân loại tam giác có chứa điểm trung điểm tạo từ 2 điểm free
            p_ext = {"id": "C", "name": "C", "x": 2.0, "y": 3.0, "source": "typed", "exact": True}
            res = classify_triangle(m_pt, p_free1, p_ext)
            self.assertFalse(res["exact"], "Tam giác có đỉnh là trung điểm kế thừa taint từ cha free bắt buộc exact=False")
            self.assertFalse(res["is_discrete"], "Điểm tainted bắt buộc đi vào nhánh liên tục (is_discrete=False)")
            self.assertIs(res["origin_exact"], False)
        finally:
            if app is not None:
                app.destroy()

    def test_26_nested_constructions_multi_level_taint(self):
        """Kiểm tra dựng hình lồng nhau nhiều tầng (Nested derived points): Lan truyền taint qua nhiều cấp cha-con"""
        from geosolver.geosolver_desktop import classify_triangle

        # Cấp 0 (Lá gốc)
        p_free_A = {"x": 0.0, "y": 0.0, "source": "free", "exact": False}
        p_free_B = {"x": 4.0, "y": 0.0, "source": "free", "exact": False}
        p_typed_C = {"x": 0.0, "y": 4.0, "source": "typed", "exact": True}
        p_typed_D = {"x": 4.0, "y": 4.0, "source": "typed", "exact": True}

        # Cấp 1
        m_tainted_1 = {"x": 2.0, "y": 0.0, "source": "midpoint", "parents": [p_free_A, p_free_B]}
        m_clean_1 = {"x": 2.0, "y": 4.0, "source": "midpoint", "parents": [p_typed_C, p_typed_D]}

        # Cấp 2: Trung điểm của 2 trung điểm (một bên sạch, một bên bẩn)
        m_nested_tainted = {"x": 2.0, "y": 2.0, "source": "midpoint", "parents": [m_tainted_1, m_clean_1]}
        # Cấp 2 sạch hoàn toàn: Trung điểm của 2 điểm typed
        p_typed_E = {"x": 0.0, "y": 8.0, "source": "typed", "exact": True}
        m_nested_clean = {"x": 1.0, "y": 6.0, "source": "midpoint", "parents": [m_clean_1, p_typed_E]}

        # Kiểm tra tam giác với điểm lồng bẩn cấp 2
        res_tainted = classify_triangle(m_nested_tainted, p_typed_C, p_typed_D)
        self.assertIs(res_tainted["origin_exact"], False, "Cờ False phải lan truyền qua 2 tầng trung điểm lồng nhau")
        self.assertFalse(res_tainted["exact"])
        self.assertFalse(res_tainted["is_discrete"])

        # Kiểm tra tam giác với điểm lồng sạch cấp 2
        res_clean = classify_triangle(m_nested_clean, p_typed_C, p_typed_D)
        self.assertIs(res_clean["origin_exact"], True, "Dựng hình lồng nhau nếu toàn bộ tổ tiên là typed phải giữ exact=True")
        self.assertTrue(res_clean["exact"])

    def test_27_none_and_string_and_invalid_type_rejection(self):
        """Kiểm tra xử lý ngoại lệ: Từ chối None, chuỗi '3.5', int và kiểu không hợp lệ ném ValueError chuẩn"""
        from geosolver.geosolver_desktop import classify_triangle

        # None ở tham số đầu
        with self.assertRaises(ValueError) as cm:
            classify_triangle(None, (1, 0), (0, 1))
        self.assertIn("None", str(cm.exception))

        # None ở tham số thứ 2
        with self.assertRaises(ValueError):
            classify_triangle((0, 0), None, (0, 1))

        # Chuỗi số '3.5' trong tuple
        with self.assertRaises(ValueError) as cm:
            classify_triangle(("3.5", 0), (1, 0), (0, 1))
        self.assertIn("không được là chuỗi", str(cm.exception))

        # Chuỗi số '3.5' trong dict
        with self.assertRaises(ValueError) as cm:
            classify_triangle({"x": "3.5", "y": 0}, (1, 0), (0, 1))
        self.assertIn("không được là chuỗi", str(cm.exception))

        # Số nguyên int trực tiếp không phải sequence
        with self.assertRaises(ValueError) as cm:
            classify_triangle(12345, (1, 0), (0, 1))
        self.assertIn("dict hoặc sequence", str(cm.exception))

    def test_28_drag_with_snap_on_snaps_absolute_coordinates(self):
        """Kiểm tra Canvas GUI: Kéo điểm tự do (lệch lưới) khi snap bật phải bắt tuyệt đối vào bội số của lưới"""
        from geosolver.geosolver_desktop import GeoSolverApp, classify_triangle
        app = None
        try:
            app = GeoSolverApp(with_splash=False)
            app.update()

            # Điểm tự do vốn có tọa độ lệch lưới (3.025, 4.025)
            p_free = {
                "id": "P_Free", "name": "Free1",
                "x": 3.025, "y": 4.025,
                "color": "#000", "fixed": False,
                "source": "free", "exact": False
            }
            app.points = [p_free]
            app.snap_to_grid = True
            app.grid_step = 0.5
            app.selected_points = [p_free]
            app.drag_start_world = (3.025, 4.025)

            # Mô phỏng kéo chuột dời một lượng dx = 0.5, dy = 0.5
            sx, sy = app.to_screen(3.525, 4.525)
            app.canvas.event_generate("<B1-Motion>", x=int(sx), y=int(sy))
            app.update()

            # Tọa độ sau kéo phải được làm tròn tuyệt đối vào lưới 0.5, không được giữ phần dư .025
            self.assertEqual(p_free["x"] % 0.5, 0.0, f"x={p_free['x']} phải là bội số của grid_step=0.5")
            self.assertEqual(p_free["y"] % 0.5, 0.0, f"y={p_free['y']} phải là bội số của grid_step=0.5")
            self.assertEqual(p_free["source"], "grid_snap", "Khi snap bật, kéo điểm phải gán source='grid_snap'")
            self.assertTrue(p_free["exact"], "Khi snap bật, kéo điểm phải gán exact=True")
        finally:
            if app is not None:
                app.destroy()

    def test_29_depth_limit_and_memoization_point_flag(self):
        """Kiểm tra _point_flag: Giới hạn đệ quy (_depth >= 8) trả False (không tin cậy) và memoization xử lý đồ thị DAG nhanh"""
        import time
        from geosolver.geosolver_desktop import _point_flag

        # 1. Kiểm tra chuỗi phụ thuộc sâu >= 8 trả về False
        cur = {"id": "P0", "source": "typed", "exact": True}
        for i in range(1, 10):
            cur = {"id": f"P{i}", "source": "midpoint", "parents": [cur, cur]}

        # cur có độ sâu 9 tầng, vượt quá ngưỡng 8 => bắt buộc trả về False (coi như taint)
        flag = _point_flag(cur)
        self.assertIs(flag, False, "Cây phụ thuộc vượt quá độ sâu 8 phải trả về False để chống mất dấu vết")

        # 2. Kiểm tra chuỗi ngắn < 8 toàn bộ là typed => trả về True
        cur_shallow = {"id": "S0", "source": "typed", "exact": True}
        for i in range(1, 5):
            cur_shallow = {"id": f"S{i}", "source": "midpoint", "parents": [cur_shallow, cur_shallow]}
        self.assertIs(_point_flag(cur_shallow), True, "Cây phụ thuộc sạch độ sâu < 8 phải giữ True")

        # 3. Kiểm tra bảo vệ chu trình (cycle / self-reference)
        p_cycle_a = {"id": "C_A", "source": "midpoint", "parents": []}
        p_cycle_b = {"id": "C_B", "source": "midpoint", "parents": [p_cycle_a]}
        p_cycle_a["parents"] = [p_cycle_b]
        # Không được ném RecursionError
        flag_cycle = _point_flag(p_cycle_a)
        self.assertIs(flag_cycle, False, "Chu trình đệ quy phải kết thúc an toàn và trả về False")

        # 4. Kiểm tra hiệu năng memoization trên đồ thị kim cương (DAG)
        # Tạo đồ thị kim cương nhiều nhánh hội tụ
        base = {"id": "Root", "source": "typed", "exact": True}
        layer = [base]
        for l in range(6):
            next_layer = []
            for i in range(len(layer) + 1):
                parents = []
                if i < len(layer):
                    parents.append(layer[i])
                if i > 0:
                    parents.append(layer[i - 1])
                node = {"id": f"L{l}_{i}", "source": "midpoint", "parents": parents}
                next_layer.append(node)
            layer = next_layer
        top_node = layer[len(layer) // 2]

        t0 = time.perf_counter()
        for _ in range(100):
            res = _point_flag(top_node)
        elapsed = time.perf_counter() - t0
        self.assertIs(res, True)
        self.assertLess(elapsed, 0.05, f"Memoization phải hoàn thành 100 lần duyệt DAG trong < 0.05s, thực tế: {elapsed:.4f}s")

    def test_30_undo_redo_parent_taint_propagation(self):
        """Kiểm tra Canvas GUI: Undo/Redo khôi phục liên kết cha-con và lan truyền taint chính xác khi điểm cha bị kéo"""
        from geosolver.geosolver_desktop import GeoSolverApp, classify_triangle
        app = None
        try:
            app = GeoSolverApp(with_splash=False)
            app.update()

            # Tạo 2 điểm typed ban đầu
            pA = {"id": "P_A", "name": "A", "x": 0.0, "y": 0.0, "color": "#000", "fixed": False, "source": "typed", "exact": True}
            pB = {"id": "P_B", "name": "B", "x": 4.0, "y": 0.0, "color": "#000", "fixed": False, "source": "typed", "exact": True}
            app.points = [pA, pB]
            app.current_tool = "midpoint"
            app._ask_point_name_dialog = lambda default_name: "M_AB"

            sxA, syA = app.to_screen(pA["x"], pA["y"])
            app.canvas.event_generate("<ButtonPress-1>", x=int(sxA), y=int(syA))
            app.update()

            sxB, syB = app.to_screen(pB["x"], pB["y"])
            app.canvas.event_generate("<ButtonPress-1>", x=int(sxB), y=int(syB))
            app.update()

            self.assertEqual(len(app.points), 3)
            pM = app.points[2]
            self.assertEqual(pM["name"], "M_AB")
            self.assertEqual(pM["source"], "midpoint")

            # Lưu trạng thái vào undo stack
            app._save_state()

            # Kiểm tra tam giác với điểm C typed ban đầu: cả 3 điểm đều sạch
            pC = {"id": "P_C", "name": "C", "x": 2.0, "y": 4.0, "color": "#000", "fixed": False, "source": "typed", "exact": True}
            res_before = classify_triangle(pM, pA, pC)
            self.assertIs(res_before["origin_exact"], True, "Trước khi kéo, tam giác gồm điểm dựng hình sạch phải có origin_exact=True")
            self.assertTrue(res_before["exact"])

            # Thực hiện Undo rồi Redo
            app.undo()
            app.update()
            app.redo()
            app.update()

            # Sau Redo, lấy lại tham chiếu điểm từ app.points
            pA_restored = app.points[0]
            pM_restored = app.points[2]

            # Kiểm tra parents đã được re-bind sau Redo
            self.assertIn("parents", pM_restored)
            self.assertIs(pM_restored["parents"][0], pA_restored, "parents[0] phải trỏ tới đúng đối tượng pA sống trên Canvas sau redo")

            # Giờ kéo điểm cha pA_restored khi snap tắt -> làm bẩn pA
            app.snap_to_grid = False
            app.selected_points = [pA_restored]
            app.drag_start_world = (pA_restored["x"], pA_restored["y"])
            sx_drag, sy_drag = app.to_screen(pA_restored["x"] + 1.234, pA_restored["y"] + 0.567)
            app.canvas.event_generate("<B1-Motion>", x=int(sx_drag), y=int(sy_drag))
            app.update()

            # Xác minh pA đã bị vấy bẩn (dragged, exact=False)
            self.assertEqual(pA_restored["source"], "dragged")
            self.assertFalse(pA_restored["exact"])

            # Điểm trung điểm pM_restored tự động cập nhật lại tọa độ và nhận diện vết dơ từ cha
            res_after_drag = classify_triangle(pM_restored, pB, pC)
            self.assertIs(res_after_drag["origin_exact"], False, "Sau khi điểm cha bị kéo tự do, điểm con dựng hình phải bị vấy bẩn (origin_exact=False)")
            self.assertFalse(res_after_drag["exact"], "exact phải là False khi có điểm vấy bẩn trong tam giác")
        finally:
            if app is not None:
                app.destroy()

    def test_31_permutation_invariance_all_six_orderings(self):
        """Kiểm tra bất biến hoán vị tuyệt đối: Thử cả 6 hoán vị của 3 đỉnh cho mọi loại tam giác, type và tính chất phải đồng nhất 100%"""
        import itertools
        from geosolver.geosolver_desktop import classify_triangle

        cases = [
            # 1. Tam giác vuông tại B: A(0,0), B(4,0), C(4,3)
            {
                "points": [({"name": "A", "x": 0.0, "y": 0.0}),
                           ({"name": "B", "x": 4.0, "y": 0.0}),
                           ({"name": "C", "x": 4.0, "y": 3.0})],
                "expected_type": "right",
                "apex_node": "B"
            },
            # 2. Tam giác cân tại B: A(-3,0), B(0,5), C(3,0)
            {
                "points": [({"name": "A", "x": -3.0, "y": 0.0}),
                           ({"name": "B", "x": 0.0, "y": 5.0}),
                           ({"name": "C", "x": 3.0, "y": 0.0})],
                "expected_type": "isosceles",
                "apex_node": "B"
            },
            # 3. Tam giác vuông cân tại C: A(0,4), B(4,0), C(0,0)
            {
                "points": [({"name": "A", "x": 0.0, "y": 4.0}),
                           ({"name": "B", "x": 4.0, "y": 0.0}),
                           ({"name": "C", "x": 0.0, "y": 0.0})],
                "expected_type": "right_isosceles",
                "apex_node": "C"
            },
            # 4. Tam giác đều: A(0,0), B(2,0), C(1, √3)
            {
                "points": [({"name": "A", "x": 0.0, "y": 0.0}),
                           ({"name": "B", "x": 2.0, "y": 0.0}),
                           ({"name": "C", "x": 1.0, "y": math.sqrt(3)})],
                "expected_type": "equilateral",
                "apex_node": None
            },
            # 5. Tam giác thường (Claude scale test): A(0,0), B(10,30), C(29,13)
            {
                "points": [({"name": "A", "x": 0.0, "y": 0.0}),
                           ({"name": "B", "x": 10.0, "y": 30.0}),
                           ({"name": "C", "x": 29.0, "y": 13.0})],
                "expected_type": "scalene",
                "apex_node": None
            },
            # 6. Tam giác thon dài (Needle triangle): kiểm tra collinear không phụ thuộc đỉnh góc nhọn
            {
                "points": [({"name": "A", "x": 0.0, "y": 0.0}),
                           ({"name": "B", "x": 100.0, "y": 0.0}),
                           ({"name": "C", "x": 50.0, "y": 0.5})],
                "expected_type": "isosceles",
                "apex_node": "C"
            }
        ]

        for case in cases:
            pts = case["points"]
            expected_type = case["expected_type"]
            expected_apex = case["apex_node"]

            # Thử tất cả 6 hoán vị (P1, P2, P3)
            for perm in itertools.permutations(pts):
                p1, p2, p3 = perm
                res = classify_triangle(p1, p2, p3)
                self.assertTrue(res["is_triangle"], f"Hoán vị {p1['name']},{p2['name']},{p3['name']} phải là tam giác")
                self.assertEqual(res["type"], expected_type, 
                                 f"Hoán vị {p1['name']},{p2['name']},{p3['name']} phải có type={expected_type}, thực tế={res['type']}")
                if expected_apex is not None:
                    self.assertEqual(res["vertex"], expected_apex,
                                     f"Đỉnh đặc biệt phải luôn là {expected_apex} bất kể thứ tự truyền vào")
                else:
                    self.assertIsNone(res["vertex"])

if __name__ == "__main__":
    unittest.main()
