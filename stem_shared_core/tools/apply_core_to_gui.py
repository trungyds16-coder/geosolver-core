# -*- coding: utf-8 -*-
"""
Tích hợp CADMathCore vào giao diện CADMathDesktopAppV2 (cad_math_v2/cad_math_v2.py)
- Thay thế toàn bộ mã giải thuật trùng lặp bằng việc ủy quyền (delegation) tới CADMathCore.
- Bổ sung cơ chế timeout bảo vệ (3.0s) cho radical solver trên background executor để UI không bị đơ.
- Hoàn thiện hiển thị LaTeX trên Canvas và vẽ biểu đồ 2D Oxy cho hệ Diophantine.
"""

import sys
import os

def main():
    target_path = 'cad_math_v2/cad_math_v2.py'
    with open(target_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Thay thế Enum DiophantineCategory bằng import từ cad_math_core
    old_m1 = '''class DiophantineCategory(str, Enum):
    INCONSISTENT = "INCONSISTENT"
    UNIQUE = "UNIQUE"
    EMPTY_NO_POSITIVE_INTEGER = "EMPTY_NO_POSITIVE_INTEGER"
    UNSUPPORTED_DIM_GE_2 = "UNSUPPORTED_DIM>=2"
    INFEASIBLE_BOUNDS_EMPTY = "INFEASIBLE_BOUNDS_EMPTY"
    INFEASIBLE_NO_INTEGER_POINTS = "INFEASIBLE_NO_INTEGER_POINTS"
    FINITE_BOUNDED = "FINITE_BOUNDED"
    UNBOUNDED_INFINITE = "UNBOUNDED_INFINITE"
    UNKNOWN = "UNKNOWN"'''
    
    new_m1 = '''from stem_shared_core.cad_math_core import CADMathCore, DiophantineCategory'''

    if old_m1 not in text:
        print("Lỗi: Không tìm thấy Marker 1 (DiophantineCategory enum)")
        sys.exit(1)
    text = text.replace(old_m1, new_m1, 1)

    # 2. Thay thế static methods real_status & check_sign_exact trong CADMathDesktopAppV2
    old_m2_start = '    @staticmethod\n    def real_status(r):'
    old_m2_end = "        return 'unknown'"
    idx_m2_s = text.find(old_m2_start)
    idx_m2_e = text.find(old_m2_end, idx_m2_s) + len(old_m2_end)
    if idx_m2_s == -1 or idx_m2_e <= idx_m2_s:
        print("Lỗi: Không tìm thấy Marker 2 (Static methods)")
        sys.exit(1)

    new_m2 = '''    @staticmethod
    def real_status(r):
        """Ủy quyền xác định tính thực cho CADMathCore."""
        return CADMathCore.real_status(r)

    @staticmethod
    def check_sign_exact(expr_sub):
        """Ủy quyền xác định dấu đại số/đa độ chính xác cho CADMathCore."""
        return CADMathCore.check_sign_exact(expr_sub)'''

    text = text[:idx_m2_s] + new_m2 + text[idx_m2_e:]

    # 3. Thêm self.core = CADMathCore() vào __init__
    old_m3 = '''    def __init__(self, root):
        self.root = root
        self.root.title("CAD Math Studio v2.1")'''
    
    new_m3 = '''    def __init__(self, root):
        self.root = root
        self.core = CADMathCore()
        self.root.title("CAD Math Studio v2.1")'''

    if old_m3 not in text:
        print("Lỗi: Không tìm thấy Marker 3 (__init__)")
        sys.exit(1)
    text = text.replace(old_m3, new_m3, 1)

    # 4. Cải tiến nhánh radical trong solve_single_equation
    old_m4 = '''                    if rad_sols:
                        latex_sols = [f'x = {sp.latex(s)}' for s in rad_sols]
                        self.eq_result_canvas.render_latex(r' \;; \quad '.join(latex_sols))
                    else:
                        self.eq_result_canvas.render_latex(r'\\text{Vô nghiệm trên } \\mathbb{R}')
                    self.eq_result_box.insert(tk.END, "\\n".join(out))
                    f_num = sp.lambdify(x, target_eq, modules=['numpy', {'sqrt': np.lib.scimath.sqrt}])
                    self.plot_oxy_roots(f_num, rad_sols)
                    return'''
    # Do ký tự thoát \text trong file, tìm kiếm đoạn an toàn hơn
    target_rad_sub = "self.eq_result_canvas.render_latex(r'\\text{Vô nghiệm trên } \\mathbb{R}')\n                    self.eq_result_box.insert(tk.END, \"\\n\".join(out))"
    if target_rad_sub in text:
        repl_rad_sub = "elif len(res_rad) > 3 and res_rad[3]:\n                        self.eq_result_canvas.render_latex(r'\\text{Nghiệm ở trạng thái chưa thể kết luận}')\n                    else:\n                        self.eq_result_canvas.render_latex(r'\\text{Vô nghiệm trên } \\mathbb{R}')\n                    self.eq_result_box.insert(tk.END, \"\\n\".join(out))"
        text = text.replace(target_rad_sub, repl_rad_sub, 1)

    # 5. Thay thế 359 dòng phương thức solve_radical_pedagogical & solve_underdetermined_or_diophantine
    start_kw = '    def solve_radical_pedagogical(self, target_eq, x):'
    end_kw = '    def plot_diophantine_system(self, sol_tuple, vars_sorted, int_sols):'
    idx1 = text.find(start_kw)
    idx2 = text.find(end_kw)
    if idx1 == -1 or idx2 == -1:
        print("Lỗi: Không tìm thấy Marker 5 (Phương thức solver)")
        sys.exit(1)

    new_methods = '''    def solve_radical_pedagogical(self, target_eq, x, timeout_sec=3.0):
        """Ủy quyền giải phương trình vô tỷ tới CADMathCore với cơ chế timeout bảo vệ giao diện."""
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.core.solve_radical_pedagogical, target_eq, x)
            try:
                return future.result(timeout=timeout_sec)
            except concurrent.futures.TimeoutError:
                fallback_steps = [
                    "  • CẢNH BÁO SƯ PHẠM: Phương trình vô tỷ chứa căn thức đa thức bậc cao (Cardano / bậc 4).",
                    f"  • Thời gian phân tích giải tích vượt ngưỡng an toàn ({timeout_sec}s).",
                    "  • Hệ thống kích hoạt cơ chế bảo vệ giao diện: chuyển nghiệm sang trạng thái chưa thể kết luận (indeterminate)."
                ]
                return fallback_steps, [], [], ["Timeout"]

    def solve_underdetermined_or_diophantine(self, eq_syms, vars_sorted, lines):
        """Ủy quyền giải hệ Diophantine tuyến tính tới CADMathCore và cập nhật giao diện đồ họa."""
        var_names_str = ", ".join(s.name for s in vars_sorted)
        cat, int_sols, n_total, out = self.core.solve_underdetermined_or_diophantine(eq_syms, vars_sorted)

        # 1. Cập nhật kết quả chi tiết lên Textbox
        self.eq_result_box.insert(tk.END, "\\n".join(out))
        self.last_dioph_category = cat
        self.last_dioph_solutions = int_sols
        self.last_dioph_n_total = n_total

        # 2. Kết xuất công thức LaTeX kết luận trên Canvas
        if cat == DiophantineCategory.FINITE_BOUNDED and int_sols:
            if n_total > 10:
                latex_str = r"\\text{Có } " + str(n_total) + r" \\text{ nghiệm nguyên dương}"
            else:
                latex_cases = [r"(" + ", ".join(str(val) for val in sol) + r")" for sol in int_sols]
                latex_str = r"\\text{Nghiệm nguyên } (" + var_names_str + r") \\in \\{" + ", ".join(latex_cases) + r"\\}"
            self.eq_result_canvas.render_latex(latex_str)
            self.plot_diophantine_system(None, vars_sorted, int_sols)
        elif cat == DiophantineCategory.UNBOUNDED_INFINITE:
            latex_str = r"\\text{Vô số nghiệm nguyên dương } (x_i \\in \\mathbb{Z}^+)"
            self.eq_result_canvas.render_latex(latex_str)
            if int_sols:
                self.plot_diophantine_system(None, vars_sorted, int_sols)
        elif cat == DiophantineCategory.UNIQUE and int_sols:
            latex_str = r"\\text{Nghiệm nguyên duy nhất } (" + var_names_str + r") = (" + ", ".join(str(c) for c in int_sols[0]) + r")"
            self.eq_result_canvas.render_latex(latex_str)
        elif cat == DiophantineCategory.INCONSISTENT:
            self.eq_result_canvas.render_latex(r"\\text{Hệ vô nghiệm trên } \\mathbb{R}")
        else:
            self.eq_result_canvas.render_latex(r"\\text{Vô nghiệm trên } (\\mathbb{Z}^+)^n")

        return cat, int_sols, n_total, out

'''

    text = text[:idx1] + new_methods + text[idx2:]

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Cập nhật thành công {target_path}! Độ dài mới: {len(text)} ký tự.")

if __name__ == '__main__':
    main()
