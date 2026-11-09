import os, sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
test_samples_localization.py
Comprehensive automated test suite to verify 100% English localization
when clicking sample buttons and generating step-by-step solutions.
"""
import sys
import tkinter as tk
from tkinter import messagebox

# Mock messageboxes
messagebox.showinfo = lambda *args, **kwargs: None
messagebox.showwarning = lambda *args, **kwargs: None
messagebox.showerror = lambda *args, **kwargs: None

from cad_math_v2.cad_math_v2 import CADMathDesktopAppV2

def test_all_samples():
    print("Initializing CADMathDesktopAppV2...")
    root = tk.Tk()
    root.withdraw()  # Hide UI window

    app = CADMathDesktopAppV2(root)
    print("Switching language to English ('en')...")
    app.switch_language("en")

    failures = []

    def assert_no_vietnamese(tab_name, action_desc, text, forbidden_words):
        found = []
        for w in forbidden_words:
            if w in text:
                found.append(w)
        if found:
            failures.append(f"[{tab_name}] {action_desc} contains Vietnamese: {found}")
            print(f"  [FAIL] FAIL: [{tab_name}] {action_desc} -> Found {found}")
        else:
            print(f"  [PASS]: [{tab_name}] {action_desc}")

    # ---------------------------------------------------------
    # TAB 1: EQUATIONS
    # ---------------------------------------------------------
    print("\n--- Testing Tab 1: Equations ---")
    app.sample_eq_btns[0].invoke()
    app.solve_equation_action()
    res1 = app.eq_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 1", "Sample 1 (x^2-3x+2 <= 0)", res1, ["BƯỚC 1", "BƯỚC 2", "KẾT LUẬN TẬP NGHIỆM", "Tập nghiệm"])

    app.sample_eq_btns[2].invoke()  # sqrt
    entry_txt = app.eq_entry.get("1.0", tk.END)
    assert_no_vietnamese("Tab 1", "Sample 3 Input Box", entry_txt, ["căn"])
    app.solve_equation_action()
    res3 = app.eq_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 1", "Sample 3 Solution", res3, ["BƯỚC 1", "ĐIỀU KIỆN XÁC ĐỊNH", "KẾT LUẬN"])

    app.sample_eq_btns[3].invoke()  # Param m
    app.solve_equation_action()
    res4 = app.eq_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 1", "Sample 4 Solution (m)", res4, ["KHẢO SÁT & GIẢI TOÁN", "Hệ số a", "Biệt thức Δ", "BƯỚC 1", "BƯỚC 2"])

    app.sample_eq_btns[4].invoke()  # Root 4 system
    entry_txt5 = app.eq_entry.get("1.0", tk.END)
    assert_no_vietnamese("Tab 1", "Sample 5 Input Box", entry_txt5, ["căn"])
    app.solve_equation_action()
    res5 = app.eq_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 1", "Sample 5 Solution", res5, ["QUY TRÌNH GIẢI", "BƯỚC 1", "BƯỚC 2", "Cặp nghiệm"])

    app.sample_eq_btns[5].invoke()  # Complex
    app.solve_equation_action()
    res6 = app.eq_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 1", "Sample 6 Solution (Complex)", res6, ["GIẢI PHƯƠNG TRÌNH SỐ PHỨC", "BƯỚC 1", "Phần thực", "Phần ảo"])

    # ---------------------------------------------------------
    # TAB 2: EXTREMUM
    # ---------------------------------------------------------
    print("\n--- Testing Tab 2: Extremum ---")
    app.sample_ext_btns[0].invoke()
    obj1 = app.ext_obj.get()
    assert_no_vietnamese("Tab 2", "Sample 1 Input Box", obj1, ["căn"])
    app.solve_extremum_action()
    res_ext1 = app.ext_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 2", "Sample 1 Solution", res_ext1, ["BƯỚC 2", "KẾT LUẬN TOÀN CỤC", "GIÁ TRỊ LỚN NHẤT", "Điểm đạt"])

    app.sample_ext_btns[1].invoke()
    cond2 = app.ext_cond.get()
    assert_no_vietnamese("Tab 2", "Sample 2 Input Box", cond2, ["căn"])
    app.solve_extremum_action()
    res_ext2 = app.ext_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 2", "Sample 2 Solution", res_ext2, ["BƯỚC 2", "KẾT LUẬN TOÀN CỤC", "GIÁ TRỊ LỚN NHẤT", "Điểm đạt"])

    # ---------------------------------------------------------
    # TAB 3: CALCULUS
    # ---------------------------------------------------------
    print("\n--- Testing Tab 3: Calculus ---")
    app.sample_calc_btns[0].invoke()
    res_c1 = app.calc_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 3", "Sample 1 (∂/∂z)", res_c1, ["PHÉP TÍNH: ĐẠO HÀM RIÊNG", "Biểu thức ban đầu", "QUY TẮC ĐẠO HÀM", "Số hạng", "KẾT QUẢ TỔNG HỢP"])

    app.sample_calc_btns[1].invoke()
    res_c2 = app.calc_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 3", "Sample 2 (∫)", res_c2, ["PHÉP TÍNH: NGUYÊN HÀM", "Áp dụng bảng nguyên hàm", "KẾT QUẢ NGUYÊN HÀM"])

    app.sample_calc_btns[2].invoke()
    res_c3 = app.calc_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 3", "Sample 3 (Taylor)", res_c3, ["PHÉP TÍNH: KHAI TRIỂN", "Công thức chuỗi", "KẾT QUẢ KHAI TRIỂN"])

    # ---------------------------------------------------------
    # TAB 4: LINEAR ALGEBRA
    # ---------------------------------------------------------
    print("\n--- Testing Tab 4: Linear Algebra ---")
    app.sample_mat_btns[0].invoke()
    res_m1 = app.mat_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 4", "Sample 1 (A * B)", res_m1, ["QUY TẮC NHÂN MA TRẬN", "Kích thước kết quả", "Công thức từng phần tử", "Chi tiết tính toán", "KẾT QUẢ MA TRẬN TÍCH"])

    app.sample_mat_btns[1].invoke()
    res_m2 = app.mat_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 4", "Sample 2 (AX = B)", res_m2, ["BƯỚC 1: THIẾT LẬP", "BƯỚC 2: GIẢI BẰNG", "NGHIỆM MA TRẬN"])

    app.solve_matrix_action("invA")
    res_inv = app.mat_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 4", "Operation invA", res_inv, ["BƯỚC 1: TÍNH ĐỊNH THỨC", "BƯỚC 2: TÌM MA TRẬN PHỤ", "BƯỚC 3: CÔNG THỨC"])

    app.solve_matrix_action("detA")
    res_det = app.mat_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 4", "Operation detA", res_det, ["TÍNH ĐỊNH THỨC", "Áp dụng khai triển"])

    app.solve_matrix_action("rankA")
    res_rank = app.mat_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 4", "Operation rankA", res_rank, ["BƯỚC 1: ĐƯA MA TRẬN", "BƯỚC 2: ĐẾM SỐ CỘT", "HẠNG MA TRẬN"])

    app.solve_matrix_action("transA")
    res_trans = app.mat_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 4", "Operation transA", res_trans, ["QUY TẮC CHUYỂN VỊ"])

    app.solve_matrix_action("eigenA")
    res_eigen = app.mat_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 4", "Operation eigenA", res_eigen, ["BƯỚC 1: PHƯƠNG TRÌNH", "BƯỚC 2: CÁC TRỊ RIÊNG", "Bội đại số", "Vector riêng"])

    # ---------------------------------------------------------
    # TAB 5: STATISTICS
    # ---------------------------------------------------------
    print("\n--- Testing Tab 5: Statistics ---")
    app.sample_stat_btns[0].invoke()
    cur_stat_mode = app.stat_mode.get()
    assert_no_vietnamese("Tab 5", "Sample 1 Stat Mode Combobox", cur_stat_mode, ["Thống kê", "toàn diện", "mô tả"])
    res_s1 = app.stat_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 5", "Sample 1 Solution", res_s1, [
        "BẢNG TỔNG HỢP", "Cỡ mẫu quan sát", "Giá trị trung bình", "Trung vị",
        "Phương sai mẫu", "Độ lệch chuẩn", "BẢNG PHÂN VỊ", "Tứ phân vị",
        "Ranh giới hợp lệ", "PHÁT HIỆN GIÁ TRỊ NGOẠI LAI"
    ])

    app.sample_stat_btns[1].invoke()
    cur_stat_mode = app.stat_mode.get()
    assert_no_vietnamese("Tab 5", "Sample 2 Stat Mode Combobox", cur_stat_mode, ["Đại số Tổ hợp", "Nhị thức"])
    res_s2 = app.stat_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 5", "Sample 2 Solution", res_s2, ["KHAI TRIỂN NHỊ THỨC", "Biểu thức khai triển", "BẢNG HỆ SỐ", "Hệ số của"])

    app.sample_stat_btns[2].invoke()
    cur_stat_mode = app.stat_mode.get()
    assert_no_vietnamese("Tab 5", "Sample 3 Stat Mode Combobox", cur_stat_mode, ["Xác suất", "Phân phối"])
    res_s3 = app.stat_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 5", "Sample 3 Solution", res_s3, ["PHÂN PHỐI NHỊ THỨC", "Kỳ vọng", "Phương sai", "Độ lệch chuẩn", "BẢNG PHÂN PHỐI"])

    # ---------------------------------------------------------
    # TAB 6: PLOT OXY
    # ---------------------------------------------------------
    print("\n--- Testing Tab 6: Plot Oxy ---")
    app.sample_plot_btns[0].invoke()
    res_p1 = app.plot_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 6", "Sample 1 Solution", res_p1, [
        "KHẢO SÁT SỰ BIẾN THIÊN", "TẬP XÁC ĐỊNH", "ĐẠO HÀM BẬC 1",
        "Điểm CỰC ĐẠI", "Điểm CỰC TIỂU", "ĐẠO HÀM BẬC 2", "Điểm uốn",
        "ĐƯỜNG TIỆM CẬN", "GIAO ĐIỂM", "DIỆN TÍCH"
    ])

    app.sample_plot_btns[2].invoke()
    res_p3 = app.plot_result_box.get("1.0", tk.END)
    assert_no_vietnamese("Tab 6", "Sample 3 Solution", res_p3, ["Tiệm cận đứng", "Tiệm cận ngang", "Mẫu số triệt tiêu"])

    root.destroy()

    if failures:
        print(f"\n[FAIL] FAILED with {len(failures)} errors:")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    else:
        print("\n[SUCCESS] ALL 20+ SAMPLE VERIFICATION TESTS PASSED 100% IN ENGLISH MODE!")

if __name__ == "__main__":
    test_all_samples()
