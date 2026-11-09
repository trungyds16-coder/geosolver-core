# -*- coding: utf-8 -*-
"""
Patch cad_math_v2/cad_math_v2.py for Round 9 refinements:
1. solve_radical_pedagogical:
   - Change 'tiệm cận ngưỡng bất định' to 'chưa xác định được bằng phương pháp đại số hay số học độ chính xác cao'.
   - Change 'Tập nghiệm chính thức: S =' to 'Tập nghiệm: S ='.
2. solve_underdetermined_or_diophantine:
   - Returns (category, int_sols, n_total, out) for unambiguous machine verification.
   - Sets self.last_dioph_category, self.last_dioph_solutions, self.last_dioph_n_total.
"""

def patch_v2_9():
    path = "cad_math_v2/cad_math_v2.py"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # 1. Radical text changes
    old_tiem_can = "CHƯA XÁC ĐỊNH (Dấu biểu thức tiệm cận ngưỡng bất định, không tự động nhận nghiệm)."
    new_tiem_can = "CHƯA XÁC ĐỊNH (Dấu biểu thức chưa xác định được bằng phương pháp đại số hay số học độ chính xác cao, không tự động nhận nghiệm)."
    if old_tiem_can in text:
        text = text.replace(old_tiem_can, new_tiem_can)
        print("Replaced 'tiem can' phrase.")

    old_s_chinh_thuc = "steps.append(f\"  ==> Tập nghiệm chính thức: S = {{{s_str}}}\")"
    new_s_chinh_thuc = "steps.append(f\"  ==> Tập nghiệm: S = {{{s_str}}}\")"
    if old_s_chinh_thuc in text:
        text = text.replace(old_s_chinh_thuc, new_s_chinh_thuc)
        print("Replaced 'chinh thuc' in S.")

    old_s_approx = "steps.append(f\"  ==> Tập nghiệm chính thức: S gồm {len(valid_sols)} nghiệm thực, giá trị gần đúng: S ≈ {{{', '.join(approx_vals)}}}\")"
    new_s_approx = "steps.append(f\"  ==> Tập nghiệm: S gồm {len(valid_sols)} nghiệm thực, giá trị gần đúng: S ≈ {{{', '.join(approx_vals)}}}\")"
    if old_s_approx in text:
        text = text.replace(old_s_approx, new_s_approx)
        print("Replaced 'chinh thuc' in approx S.")

    # 2. Return structured data from solve_underdetermined_or_diophantine
    old_dio_end = '''        self.eq_result_box.insert(tk.END, "\\n".join(out))'''
    new_dio_end = '''        self.eq_result_box.insert(tk.END, "\\n".join(out))
        self.last_dioph_category = category
        self.last_dioph_solutions = int_sols
        self.last_dioph_n_total = n_total
        return category, int_sols, n_total, out'''

    # Ensure early returns also return structured tuple
    old_inconsistent = '''        if not linsols:
            out.append("  • Hệ phương trình vô nghiệm trên tập số thực ℝ (rank(A) != rank(A|b)).")
            self.eq_result_canvas.render_latex(r"\\text{Hệ vô nghiệm trên } \\mathbb{R}")
            self.eq_result_box.insert(tk.END, "\\n".join(out))
            return'''

    new_inconsistent = '''        if not linsols:
            out.append("  • Hệ phương trình vô nghiệm trên tập số thực ℝ (rank(A) != rank(A|b)).")
            self.eq_result_canvas.render_latex(r"\\text{Hệ vô nghiệm trên } \\mathbb{R}")
            self.eq_result_box.insert(tk.END, "\\n".join(out))
            return "INCONSISTENT", [], 0, out'''

    old_d0 = '''            if is_pos_int:
                out.append(f"  ==> Hệ có nghiệm nguyên dương duy nhất: ({sol_str})")
                self.eq_result_canvas.render_latex(r"\\text{Nghiệm nguyên duy nhất } (" + var_names_str + r") = (" + ", ".join(str(c) for c in sol_tuple) + r")")
            else:
                out.append(f"  ==> Hệ có nghiệm thực duy nhất ({sol_str}) nhưng không thuộc tập số nguyên dương (ℤ⁺)ⁿ.")
                self.eq_result_canvas.render_latex(r"\\text{Vô nghiệm trên } (\\mathbb{Z}^+)^n")
            self.eq_result_box.insert(tk.END, "\\n".join(out))
            return'''

    new_d0 = '''            if is_pos_int:
                out.append(f"  ==> Hệ có nghiệm nguyên dương duy nhất: ({sol_str})")
                self.eq_result_canvas.render_latex(r"\\text{Nghiệm nguyên duy nhất } (" + var_names_str + r") = (" + ", ".join(str(c) for c in sol_tuple) + r")")
                self.eq_result_box.insert(tk.END, "\\n".join(out))
                return "UNIQUE", [tuple(int(c) for c in sol_tuple)], 1, out
            else:
                out.append(f"  ==> Hệ có nghiệm thực duy nhất ({sol_str}) nhưng không thuộc tập số nguyên dương (ℤ⁺)ⁿ.")
                self.eq_result_canvas.render_latex(r"\\text{Vô nghiệm trên } (\\mathbb{Z}^+)^n")
                self.eq_result_box.insert(tk.END, "\\n".join(out))
                return "EMPTY_NO_POSITIVE_INTEGER", [], 0, out'''

    old_dge2 = '''            out.append("  • Lưu ý sư phạm: Lớp bài toán Diophantine đa tham số (d >= 2) hiện chưa quét tự động trên tập số nguyên dương (ℤ⁺)ⁿ.")
            self.eq_result_canvas.render_latex(r"\\text{Họ nghiệm trên } \\mathbb{R} \\text{ phụ thuộc } " + str(d) + r" \\text{ tham số (chưa xét trên } \\mathbb{Z}^+ \\text{)}")
            self.eq_result_box.insert(tk.END, "\\n".join(out))
            return'''

    new_dge2 = '''            out.append("  • Lưu ý sư phạm: Lớp bài toán Diophantine đa tham số (d >= 2) hiện chưa quét tự động trên tập số nguyên dương (ℤ⁺)ⁿ.")
            self.eq_result_canvas.render_latex(r"\\text{Họ nghiệm trên } \\mathbb{R} \\text{ phụ thuộc } " + str(d) + r" \\text{ tham số (chưa xét trên } \\mathbb{Z}^+ \\text{)}")
            self.eq_result_box.insert(tk.END, "\\n".join(out))
            return "UNSUPPORTED_DIM>=2", [], 0, out'''

    if old_inconsistent in text: text = text.replace(old_inconsistent, new_inconsistent)
    if old_d0 in text: text = text.replace(old_d0, new_d0)
    if old_dge2 in text: text = text.replace(old_dge2, new_dge2)
    if old_dio_end in text: text = text.replace(old_dio_end, new_dio_end)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("cad_math_v2.py updated with Round 9 refinements.")

if __name__ == "__main__":
    patch_v2_9()
