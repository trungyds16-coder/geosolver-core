# -*- coding: utf-8 -*-
with open('cad_math_v2/cad_math_v2.py', 'r', encoding='utf-8') as f:
    text = f.read()

bad = """                    self.eq_result_box.insert(tk.END, "\\n".join(out))
        self.last_dioph_category = category
        self.last_dioph_solutions = int_sols
        self.last_dioph_n_total = n_total
        return category, int_sols, n_total, out"""

good = """                    self.eq_result_box.insert(tk.END, "\\n".join(out))"""

if bad in text:
    text = text.replace(bad, good)
    print("Found bad at 2029 and replaced.")

# Now find the true end of solve_underdetermined_or_diophantine right before plot_diophantine_system
p_end_marker = "        self.eq_result_box.insert(tk.END, \"\\n\".join(out))\n    def plot_diophantine_system"
p_end_replacement = """        self.eq_result_box.insert(tk.END, "\\n".join(out))
        self.last_dioph_category = category
        self.last_dioph_solutions = int_sols
        self.last_dioph_n_total = n_total
        return category, int_sols, n_total, out
    def plot_diophantine_system"""

if p_end_marker in text:
    text = text.replace(p_end_marker, p_end_replacement)
    print("Added return at end of solve_underdetermined_or_diophantine.")
else:
    print("Marker not found, inspecting context...")

with open('cad_math_v2/cad_math_v2.py', 'w', encoding='utf-8') as f:
    f.write(text)
