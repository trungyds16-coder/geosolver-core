# -*- coding: utf-8 -*-
"""
apply_v2_5_integration.py
=========================
Tích hợp mã nguồn chuẩn hóa Version 2.5 vào cad_math_v2/cad_math_v2.py:
- Tích hợp sign_status và solve_radical_fixed (chuẩn hóa tự động, bắt nghiệm phức, nghiệm bất định).
- Tích hợp solve_dioph_fixed (sử dụng solve_congruence CRT, phân biệt vô nghiệm nguyên và vô hạn nghiệm).
- Cập nhật văn phong sư phạm và hiển thị giá trị g(r).
"""

import sys

def apply_patch():
    target_path = r'd:\AI DATA\STEM_APP\cad_math_v2\cad_math_v2.py'
    with open(target_path, 'r', encoding='utf-8') as f:
        content = f.read()

    old_radical_start = "    def solve_radical_pedagogical(self, target_eq, x):"
    plot_diophantine_start = "    def plot_diophantine_system(self, sol_tuple, vars_sorted, int_sols):"

    start_idx = content.find(old_radical_start)
    end_idx = content.find(plot_diophantine_start)
    assert start_idx != -1 and end_idx != -1, "Method boundaries not found in cad_math_v2.py"

    replacement = '''    def solve_radical_pedagogical(self, target_eq, x):
        """Giải phương trình vô tỷ dạng √(f(x)) = g(x) với kiểm tra dấu đại số chính xác v2.5."""
        steps = []
        rads = [t for t in target_eq.atoms(sp.Pow) if t.exp == sp.Rational(1, 2)]
        if len(rads) != 1:
            return ["  • Ngoài phạm vi hỗ trợ: Cần phương trình chứa đúng một căn thức bậc hai."], []

        rad = rads[0]
        expanded = sp.expand(target_eq)
        c = expanded.coeff(rad)
        rest = sp.expand(expanded - c * rad)

        if c == 0 or c.free_symbols or any(t.exp == sp.Rational(1, 2) for t in rest.atoms(sp.Pow)):
            return ["  • Ngoài phạm vi hỗ trợ: Dạng căn thức không chuẩn hoặc không cô lập được."], []

        fx = rad.base
        gx = sp.simplify(-rest / c)

        steps.append("\\n[BƯỚC 1: XÁC ĐỊNH ĐIỀU KIỆN CÓ NGHĨA & ĐIỀU KIỆN VẾ PHẢI]")
        steps.append(f"  • Đưa phương trình về dạng chuẩn tắc: √({clean_display_expr(fx)}) = {clean_display_expr(gx)}")
        steps.append(f"  • Điều kiện xác định căn thức: {clean_display_expr(fx)} >= 0")
        try:
            cond_fx = sp.solve(fx >= 0, x)
            steps.append(f"    ==> Miền D_rad: {cond_fx}")
        except: pass
        steps.append(f"  • Điều kiện vế phải (Vì căn bậc hai số học √({clean_display_expr(fx)}) >= 0 nên vế phải bắt buộc g(x) >= 0): {clean_display_expr(gx)} >= 0")
        try:
            cond_gx = sp.solve(gx >= 0, x)
            steps.append(f"    ==> Miền D_sign: {cond_gx}")
        except: pass

        steps.append("\\n[BƯỚC 2: BÌNH PHƯƠNG HAI VẾ TÌM TẬP NGHIỆM ĐẠI SỐ SƠ BỘ]")
        steps.append(f"  • ({clean_display_expr(rad)})² = ({clean_display_expr(gx)})²")
        poly_eq = sp.simplify(fx - gx**2)
        steps.append(f"  <=> {clean_display_expr(poly_eq)} = 0")

        raw_sols = sp.solve(poly_eq, x)
        steps.append(f"  • Nghiệm đại số sơ bộ từ phương trình hệ quả: {raw_sols}")

        steps.append("\\n[BƯỚC 3: XÁC ĐỊNH DẤU ĐẠI SỐ CHÍNH XÁC & LOẠI BỎ NGHIỆM NGOẠI LAI]")
        valid_sols = []
        rejected_sols = []
        unknown_sols = []

        def sign_status(v):
            v = sp.simplify(v)
            if v.is_real is False: return 'nonreal'
            if v.is_zero: return 'zero'
            if v.is_positive: return 'pos'
            if v.is_negative: return 'neg'
            try:
                a = sp.N(v, 60)
                if abs(sp.im(a)) > sp.Float('1e-40'): return 'nonreal'
                a = sp.re(a)
                if abs(a) > sp.Float('1e-40'): return 'pos' if a > 0 else 'neg'
            except Exception:
                pass
            return 'unknown'

        for r in raw_sols:
            if r.is_real is False or abs(sp.N(r, 30).as_real_imag()[1]) > sp.Float('1e-25'):
                rejected_sols.append(r)
                steps.append(f"  • x = {clean_display_expr(r)}: LOẠI (Nghiệm phức không thuộc tập số thực ℝ).")
                continue

            g_val = gx.subs(x, r)
            f_val = fx.subs(x, r)
            sg = sign_status(g_val)
            sf = sign_status(f_val)

            g_disp = f"g({clean_display_expr(r)}) = {clean_display_expr(g_val)}"
            try:
                g_disp += f" ≈ {float(g_val.evalf()):.4f}"
            except: pass

            if sg in ['pos', 'zero'] and sf in ['pos', 'zero']:
                valid_sols.append(r)
                steps.append(f"  • x = {clean_display_expr(r)}: NHẬN (Thỏa mãn {g_disp} >= 0).")
            elif sg == 'neg':
                rejected_sols.append(r)
                steps.append(f"  • x = {clean_display_expr(r)}: LOẠI (Nghiệm ngoại lai do vi phạm điều kiện vế phải {g_disp} < 0).")
            elif sf == 'neg':
                rejected_sols.append(r)
                steps.append(f"  • x = {clean_display_expr(r)}: LOẠI (Nghiệm ngoại lai do vi phạm điều kiện căn thức f(r) < 0).")
            else:
                unknown_sols.append(r)
                steps.append(f"  • x = {clean_display_expr(r)}: CHƯA XÁC ĐỊNH (Dấu tiệm cận ngưỡng bất định, không tự động nhận nghiệm).")

        return steps, valid_sols

    def solve_underdetermined_or_diophantine(self, eq_syms, vars_sorted, lines):
        """Bộ giải Diophantine tuyến tính v2.5 sử dụng giải đồng dư CRT và trần số nghiệm."""
        from sympy.ntheory.modular import solve_congruence
        out = []
        out.append("=" * 85)
        out.append("QUY TRÌNH GIẢI HỆ PHƯƠNG TRÌNH VÔ ĐỊNH & KHẢO SÁT NGHIỆM NGUYÊN (DIOPHANTINE v2.5):")
        out.append("=" * 85)

        m = len(eq_syms)
        n = len(vars_sorted)
        var_names_str = ", ".join(s.name for s in vars_sorted)

        # BƯỚC 1: PHÂN TÍCH CẤU TRÚC
        out.append("\\n[BƯỚC 1: PHÂN TÍCH CẤU TRÚC ĐẠI SỐ TUYẾN TÍNH]")
        out.append(f"  • Số lượng phương trình: M = {m}")
        out.append(f"  • Số lượng biến số: N = {n} ({var_names_str})")

        linsols = sp.linsolve(eq_syms, vars_sorted)
        if not linsols:
            out.append("  • Hệ phương trình vô nghiệm trên tập số thực ℝ (rank(A) != rank(A|b)).")
            self.eq_result_canvas.render_latex(r"\\text{Hệ vô nghiệm trên } \\mathbb{R}")
            self.eq_result_box.insert(tk.END, "\\n".join(out))
            return

        sol_tuple = list(linsols)[0]
        free_syms = sorted(set().union(*[sp.sympify(e).free_symbols for e in sol_tuple]), key=lambda s: s.name)
        d = len(free_syms)
        out.append(f"  • Bậc tự do của hệ: d = N - rank(A) = {d} tham số tự do.")

        # Xử lý d = 0 (Hệ xác định, nghiệm duy nhất)
        if d == 0:
            out.append("\\n[BƯỚC 2: KHẢO SÁT NGHIỆM DUY NHẤT (d = 0)]")
            is_pos_int = all(sp.sympify(e).is_integer and e > 0 for e in sol_tuple)
            sol_str = ", ".join(f"{v.name} = {c}" for v, c in zip(vars_sorted, sol_tuple))
            if is_pos_int:
                out.append(f"  ==> Hệ có nghiệm nguyên dương duy nhất: ({sol_str})")
                self.eq_result_canvas.render_latex(r"\\text{Nghiệm nguyên duy nhất } (" + var_names_str + r") = (" + ", ".join(str(c) for c in sol_tuple) + r")")
            else:
                out.append(f"  ==> Hệ có nghiệm thực duy nhất ({sol_str}) nhưng không thuộc tập số nguyên dương (ℤ⁺)ⁿ.")
                self.eq_result_canvas.render_latex(r"\\text{Vô nghiệm trên } (\\mathbb{Z}^+)^n")
            self.eq_result_box.insert(tk.END, "\\n".join(out))
            return

        # Xử lý d >= 2 (Đa tham số)
        if d >= 2:
            out.append(f"\\n[BƯỚC 2: HỌ NGHIỆM TỔNG QUÁT ĐA THAM SỐ (d = {d} >= 2)]")
            out.append(f"  • Hệ có {d} tham số tự do ({', '.join(s.name for s in free_syms)}).")
            out.append("  • Biểu diễn affine nghiệm tổng quát trên ℝ:")
            for v, expr in zip(vars_sorted, sol_tuple):
                out.append(f"    {v} = {clean_display_expr(expr)}")
            out.append("  • Thông báo sư phạm: Lớp bài toán Diophantine đa tham số (d >= 2) hiện nằm ngoài phạm vi quét tự động.")
            self.eq_result_canvas.render_latex(r"\\text{Vô số nghiệm phụ thuộc } " + str(d) + r" \\text{ tham số}")
            self.eq_result_box.insert(tk.END, "\\n".join(out))
            return

        # TRƯỜNG HỢP d = 1: Phân tích đồng dư CRT chuẩn hóa
        p = free_syms[0]
        out.append(f"\\n[BƯỚC 2: BIỂU DIỄN THAM SỐ AFFINE THEO ẨN TỰ DO {p}]")
        for v, expr in zip(vars_sorted, sol_tuple):
            if expr == v:
                out.append(f"  • Tham số tự do: {v} ∈ ℝ")
            else:
                out.append(f"  • Biến phụ thuộc {v}: {v} = {clean_display_expr(expr)}")

        out.append("\\n[BƯỚC 3: PHÂN TÍCH ĐỒNG DƯ CRT VÀ RÀNG BUỘC BIÊN (ℤ⁺)]")
        lo = hi = None
        cong = []
        cap = 1000

        for e in sol_tuple:
            e_exp = sp.expand(e)
            a = sp.Rational(e_exp.coeff(p))
            b = sp.Rational(e_exp.subs(p, 0))
            D = sp.ilcm(a.q, b.q)
            A = int(a * D)
            B = int(b * D)
            g = sp.igcd(A, D)

            if (-B) % g != 0:
                out.append(f"  • Phát hiện mâu thuẫn đồng dư: {A}·{p} + {B} = 0 (mod {D}) không có nghiệm nguyên.")
                out.append("\\n  ==> KẾT QUẢ: Hệ đồng dư vô nghiệm trên ℤ (Hệ có nghiệm thực dương nhưng không có điểm nguyên).")
                self.eq_result_canvas.render_latex(r"\\text{Vô nghiệm trên } (\\mathbb{Z}^+)^n")
                self.eq_result_box.insert(tk.END, "\\n".join(out))
                return

            if A != 0:
                Ag, Dg = A // g, D // g
                cong.append(((-(B // g) * pow(Ag, -1, Dg)) % Dg if Dg > 1 else 0, Dg))

            if a > 0:
                bd = sp.floor(-b / a) + 1
                lo = bd if lo is None else max(lo, bd)
            elif a < 0:
                bd = sp.ceiling(-b / a) - 1
                hi = bd if hi is None else min(hi, bd)
            elif b <= 0:
                out.append(f"  • Biến hằng {clean_display_expr(b)} <= 0 vi phạm ràng buộc nguyên dương.")
                out.append("\\n  ==> KẾT QUẢ: Miền ràng buộc rỗng (Hệ vô nghiệm nguyên dương).")
                self.eq_result_canvas.render_latex(r"\\text{Vô nghiệm trên } (\\mathbb{Z}^+)^n")
                self.eq_result_box.insert(tk.END, "\\n".join(out))
                return

        sc = solve_congruence(*cong) if cong else (0, 1)
        if sc is None:
            out.append("\\n  ==> KẾT QUẢ: Hệ đồng dư vô nghiệm trên ℤ (Hệ không có nghiệm nguyên).")
            self.eq_result_canvas.render_latex(r"\\text{Vô nghiệm trên } (\\mathbb{Z}^+)^n")
            self.eq_result_box.insert(tk.END, "\\n".join(out))
            return

        r, M = int(sc[0]), int(sc[1])
        if lo is None: lo = 1
        lo = max(1, int(lo))
        start = int(lo) + ((r - int(lo)) % M)

        int_sols = []
        if hi is not None:
            hi = int(hi)
            if start > hi:
                out.append("\\n  ==> KẾT QUẢ: Miền ràng buộc rỗng (start > hi).")
                self.eq_result_canvas.render_latex(r"\\text{Vô nghiệm trên } (\\mathbb{Z}^+)^n")
                self.eq_result_box.insert(tk.END, "\\n".join(out))
                return

            n_count = (hi - start) // M + 1
            out.append(f"  • Miền nghiệm hữu hạn bị chặn ({p} ∈ [{lo}, {hi}]). Bước nhảy modulo M = {M}.")
            out.append(f"  ==> Tìm được {n_count} bộ nghiệm nguyên dương (hiển thị tối đa {cap} bộ):")

            for k in range(min(n_count, cap)):
                cand = [item.subs(p, start + M * k) for item in sol_tuple]
                int_sols.append(tuple(int(c) for c in cand))

            for idx, sol in enumerate(int_sols[:20], 1):
                sol_str = ", ".join(f"{v.name} = {val}" for v, val in zip(vars_sorted, sol))
                out.append(f"    • Bộ nghiệm {idx}: {sol_str}")
            if len(int_sols) > 20:
                out.append(f"    ... và {len(int_sols) - 20} bộ nghiệm khác.")

            latex_cases = [r"(" + ", ".join(str(val) for val in sol) + r")" for sol in int_sols[:10]]
            self.eq_result_canvas.render_latex(r"\\text{Nghiệm nguyên } (" + var_names_str + r") \\in \\{" + ", ".join(latex_cases) + (r", \\dots" if len(int_sols) > 10 else "") + r"\\}")
        else:
            out.append(f"  • Miền nghiệm vô hạn không bị chặn trên ({p} >= {lo}). Bước nhảy modulo M = {M}.")
            k_sym = sp.Symbol('k', integer=True, nonnegative=True)
            family = tuple(sp.expand(item.subs(p, start + M * k_sym)) for item in sol_tuple)
            family_str = ", ".join(f"{v.name} = {clean_display_expr(f)}" for v, f in zip(vars_sorted, family))
            out.append(f"  • Họ nghiệm tham số tổng quát: ({family_str}) với k ∈ ℤ, k >= 0.")
            out.append(f"  ==> Hệ có VÔ SỐ BỘ NGHIỆM NGUYÊN DƯƠNG. Ba bộ nghiệm nhỏ nhất đại diện:")

            for j in range(3):
                cand = [item.subs(p, start + M * j) for item in sol_tuple]
                int_sols.append(tuple(int(c) for c in cand))
                sol_str = ", ".join(f"{v.name} = {val}" for v, val in zip(vars_sorted, cand))
                out.append(f"    • Bộ nghiệm {j+1}: {sol_str}")

            self.eq_result_canvas.render_latex(r"\\text{Vô số nghiệm nguyên dương } (x_i \\in \\mathbb{Z}^+)")

        out.append("\\n[BƯỚC 4: KẾT LUẬN]")
        out.append(f"  ==> Hoàn tất khảo sát cấu trúc nghiệm trên (ℤ⁺)ⁿ.")
        self.eq_result_box.insert(tk.END, "\\n".join(out))
        self.plot_diophantine_system(sol_tuple, vars_sorted, int_sols)
'''

    content = content[:start_idx] + replacement + content[end_idx:]
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Version 2.5 successfully integrated into cad_math_v2.py!")

if __name__ == '__main__':
    apply_patch()
