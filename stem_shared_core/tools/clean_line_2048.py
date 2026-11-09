# -*- coding: utf-8 -*-
with open('cad_math_v2/cad_math_v2.py', 'r', encoding='utf-8') as f:
    text = f.read()

bad2 = """                self.eq_result_canvas.render_latex(r"\\text{Áp dụng cô lập } m \\text{ và khảo sát } \\min/\\max")
                self.eq_result_box.insert(tk.END, "\\n".join(out))
        self.last_dioph_category = category
        self.last_dioph_solutions = int_sols
        self.last_dioph_n_total = n_total
        return category, int_sols, n_total, out
                return"""

good2 = """                self.eq_result_canvas.render_latex(r"\\text{Áp dụng cô lập } m \\text{ và khảo sát } \\min/\\max")
                self.eq_result_box.insert(tk.END, "\\n".join(out))
                return"""

if bad2 in text:
    text = text.replace(bad2, good2)
    print("Fixed bad2 at line 2048.")
else:
    print("bad2 not found.")

with open('cad_math_v2/cad_math_v2.py', 'w', encoding='utf-8') as f:
    f.write(text)
