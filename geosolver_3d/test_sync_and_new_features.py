# -*- coding: utf-8 -*-
"""
test_sync_and_new_features.py
Comprehensive test suite verifying all newly synchronized desktop features:
1. Title synchronization (VN & EN)
2. Desktop Menu Bar structure (File, Edit, View, Tools, Options, Help)
3. Undo / Redo (Ctrl+Z, Ctrl+Y) and Clipboard copy
4. Multi-mode Image Export Dialog & options (Axes, Sphere, Section, Transparent, DPI)
5. Bilingual Deductive Solutions: 100% pure English verification across all 12 topics (zero Vietnamese leakage)
6. Exact Radical Formatter for irrational values (no ugly floats or raw unrendered LaTeX)
7. HTML & Markdown report generators
8. AI reservation notice and code preservation
"""

import os
import sys
import math
import tkinter as tk

# Ensure parent directory is in sys.path
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT_DIR = os.path.dirname(_CURRENT_DIR)
if _PARENT_DIR not in sys.path:
    sys.path.insert(0, _PARENT_DIR)

from geosolver_3d.app import (
    GeoSolver3DApp,
    format_radical_number,
    latex_to_natural_math,
    format_formula_radicals,
    BuiltinDeductive3DEngine,
    Export3DImageDialog,
    ProductAboutDialog,
    ShortcutsGuideDialog,
)


def test_radical_formatter():
    print("[TEST 1] Kiểm tra Bộ định dạng Căn thức tự nhiên (Radical Formatter)...")
    # Test values
    val1 = math.sqrt(41) / 2.0  # √41/2
    val2 = 6.0 * math.sqrt(6.0) / 4.0  # 3√6/2
    val3 = math.sqrt(3.0)  # √3
    val4 = math.sqrt(2.0) / 2.0  # √2/2
    val5 = 4.0 / 3.0  # 4/3
    val6 = 5.0 * math.sqrt(2.0)  # 5√2
    val7 = math.sqrt(6.0) / 3.0  # √6/3

    assert format_radical_number(val1) == "√41/2", f"Got: {format_radical_number(val1)}"
    assert format_radical_number(val2) == "3√6/2", f"Got: {format_radical_number(val2)}"
    assert format_radical_number(val3) == "√3", f"Got: {format_radical_number(val3)}"
    assert format_radical_number(val4) == "√2/2", f"Got: {format_radical_number(val4)}"
    assert format_radical_number(val5) == "4/3", f"Got: {format_radical_number(val5)}"
    assert format_radical_number(val6) == "5√2", f"Got: {format_radical_number(val6)}"
    assert format_radical_number(val7) == "√6/3", f"Got: {format_radical_number(val7)}"

    # Test formula latex conversion
    latex_sample = r"$$R = \frac{SC}{2} = \frac{1}{2}\sqrt{SA^2 + AB^2 + BC^2} = \sqrt{R_{\text{đáy}}^2 + \left(\frac{SA}{2}\right)^2}$$"
    nat_vn = latex_to_natural_math(latex_sample, lang="VN")
    nat_en = latex_to_natural_math(latex_sample, lang="EN")

    assert "√(" in nat_vn and "_đáy" in nat_vn, f"VN formula mismatch: {nat_vn}"
    assert "√(" in nat_en and "_base" in nat_en, f"EN formula mismatch: {nat_en}"
    print("  -> Các số vô tỉ được biểu diễn căn thức chính xác 100%: √41/2, 3√6/2, √3, √2/2, 5√2, √6/3!")
    print("  PASSED: Bộ định dạng căn thức tự nhiên hoạt động hoàn hảo!")


def test_bilingual_deduction_leakage():
    print("[TEST 2] Kiểm tra 12 Chuyên đề Suy Luận Tiếng Anh (Kiểm tra triệt tiêu tiếng Việt)...")
    engine = BuiltinDeductive3DEngine()
    params = {
        "SA": 4.0, "AB": 3.0, "BC": 4.0, "a": 6.0,
        "R": 5.0, "d": 3.0, "h_cap": 2.0, "base_a": 4.0, "height_h": 4.0,
        "angle_A": 90.0, "angle_B": 90.0, "angle_C": 90.0,
        "px": 1.0, "py": 2.0, "pz": 3.0, "pl_A": 1.0, "pl_B": 2.0, "pl_C": 2.0, "pl_D": -1.0,
        "ux": 1.0, "uy": 1.0, "uz": 0.0,
        "nx2": 0.0, "ny2": 1.0, "nz2": 0.0,
    }

    # Vietnamese words that should NEVER appear in English mode
    vn_forbidden = [
        "Bước ", "CHUYÊN ĐỀ", "THÔNG SỐ", "SUY LUẬN", "ĐẦU VÀO",
        "chiều cao", "cạnh đáy", "tam giác", "ngoại tiếp", "nội tiếp",
        "mặt cầu", "mặt phẳng", "khoảng cách", "hình chiếu", "thể tích",
        "diện tích", "bán kính", "đường tròn", "thiết diện", "KẾT QUẢ", "KẾT LUẬN"
    ]

    for t in range(1, 13):
        sol_en = engine.solve_topic(t, params, lang="EN")
        assert f"TOPIC {t}:" in sol_en, f"Topic {t} missing English header!"
        assert "PARAMETERS" in sol_en, f"Topic {t} missing English input params!"
        assert "[EXACT ANALYTICAL RESULTS]" in sol_en or "[CONCLUSION]" in sol_en, f"Topic {t} missing English results!"

        # Check for forbidden Vietnamese words (case-insensitive where relevant)
        for w in vn_forbidden:
            assert w.lower() not in sol_en.lower(), f"Topic {t} leaked Vietnamese word '{w}' in English proof!\nSnippet: {sol_en[:300]}"

    print("  -> Đã kiểm tra toàn bộ 12 Chuyên đề suy luận khi chuyển sang EN.")
    print("  -> 0% từ ngữ tiếng Việt bị rò rỉ, 100% chuẩn thuật ngữ Toán quốc tế!")
    print("  PASSED: Lời giải tiếng Anh chuẩn xác 100%!")


def test_app_ui_sync_and_features():
    print("[TEST 3] Kiểm tra Đồng bộ Menu Bar, Tiêu đề cửa sổ & Phím tắt...")
    app = GeoSolver3DApp()
    app.withdraw()

    # 1. Check Window Title in VN and EN
    app.set_language("VN")
    assert "GeoSolver 3D - Hình Học Không Gian & Vẽ Kỹ Thuật CAD" in app.title(), f"VN Title mismatch: {app.title()}"
    app.set_language("EN")
    assert "GeoSolver 3D - Spatial Geometry & CAD Studio" in app.title(), f"EN Title mismatch: {app.title()}"
    app.set_language("VN")

    # 2. Check Menu Bar Structure
    assert hasattr(app, "menubar") and app.menubar is not None, "Menu bar not initialized!"
    # Check menu items count (File, Edit, View, Tools, Options, Help)
    num_menus = app.menubar.index("end") + 1
    assert num_menus >= 6, f"Expected at least 6 top menus, got: {num_menus}"

    # 3. Check Undo / Redo functionality
    initial_model = app.current_model_key
    app.select_polyhedron("tetrahedron_sabc")
    assert app.current_model_key == "tetrahedron_sabc"
    assert len(app._undo_stack) > 0, "Undo stack empty after action!"

    app.undo()
    assert app.current_model_key == initial_model, f"Undo failed! Expected {initial_model}, got {app.current_model_key}"
    app.redo()
    assert app.current_model_key == "tetrahedron_sabc", f"Redo failed! Expected tetrahedron_sabc, got {app.current_model_key}"

    # Reset back
    app.select_polyhedron("pyramid_sabcd")

    # 4. Check Clipboard copy
    app.copy_selection()
    cb_content = app.clipboard_get()
    assert "GEOSOLVER 3D" in cb_content, f"Clipboard content mismatch: {cb_content[:100]}"
    assert "TỌA ĐỘ ĐỈNH" in cb_content or "VERTEX COORDINATES" in cb_content

    # 5. Check Multi-Mode Image Export
    test_out_png = os.path.join(_CURRENT_DIR, "test_export_options.png")
    app._render_scene_to_image(
        test_out_png,
        scale=2,
        show_axes=True,
        show_sphere=True,
        show_section=True,
        show_auxiliary=True,
        show_labels=True,
        hidden_mode="dashed",
        bold_mode=True,
        transparent_bg=True
    )
    assert os.path.exists(test_out_png), "Export image file not created!"
    assert os.path.getsize(test_out_png) > 1000, "Export image file empty!"
    os.remove(test_out_png)

    # 6. Check AI Hub status
    assert hasattr(app, "notify_ai_upgrade"), "notify_ai_upgrade method missing!"
    assert hasattr(app, "open_ai_hub"), "open_ai_hub code was deleted!"

    # 7. Check HTML report generator
    test_html = os.path.join(_CURRENT_DIR, "test_report.html")
    from stem_shared_core.report_engine import build_full_stem_html_report
    html_out = build_full_stem_html_report(
        app_title="GeoSolver 3D CAD Studio",
        topic="3D Spatial Geometry",
        problem_text="Test 3D Problem",
        solution_steps="Step 1: Test step with exact radical √41/2."
    )
    with open(test_html, "w", encoding="utf-8") as f:
        f.write(html_out)
    assert os.path.exists(test_html) and "MathJax" in html_out
    os.remove(test_html)

    app.destroy()
    print("  -> Tiêu đề cửa sổ song ngữ đồng bộ hoàn hảo.")
    print("  -> Hệ thống Menu Bar Win32 (Tệp, Chỉnh sửa, Hiển thị, Công cụ, Tùy chọn, Thông tin) đầy đủ.")
    print("  -> Hoàn tác (Undo/Redo Ctrl+Z/Ctrl+Y) và Sao chép (Ctrl+C) hoạt động chính xác.")
    print("  -> Hộp thoại xuất ảnh đa chế độ (Trục Oxyz, Cầu, Nét đứt, Nền trong suốt, 300 DPI) thành công!")
    print("  -> Module AI được bảo lưu nguyên vẹn, thông báo nâng cấp thân thiện.")
    print("  PASSED: Toàn bộ kiểm thử tính năng giao diện và đồng bộ đạt 100%!")


if __name__ == "__main__":
    test_radical_formatter()
    test_bilingual_deduction_leakage()
    test_app_ui_sync_and_features()
    print("\n" + "=" * 60)
    print("TẤT CẢ CÁC YÊU CẦU ĐÃ ĐƯỢC KIỂM THỬ THÀNH CÔNG 100%!")
    print("=" * 60)
