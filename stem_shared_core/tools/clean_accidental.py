# -*- coding: utf-8 -*-
with open('cad_math_v2/cad_math_v2.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, l in enumerate(lines):
    if i + 1 < 2700:
        if 'self.last_dioph_category = category' in l or \
           'self.last_dioph_solutions = int_sols' in l or \
           'self.last_dioph_n_total = n_total' in l or \
           'return category, int_sols, n_total, out' in l:
            continue
    new_lines.append(l)

with open('cad_math_v2/cad_math_v2.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Cleaned up lines < 2700.")
