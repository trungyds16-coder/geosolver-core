# -*- coding: utf-8 -*-
with open('stem_shared_core/tools/run_batch_auto_test.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'inv_ok = all(abs(float(sp.N(test["target"].subs(test["var"], r)))) < 1e-7 for r in valid)'
replacement = 'inv_ok = all(abs(complex(sp.N(test["target"].subs(test["var"], r)))) < 1e-7 for r in valid)'

if target in text:
    text = text.replace(target, replacement)
    with open('stem_shared_core/tools/run_batch_auto_test.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed invariant check successfully.")
else:
    print("Target not found.")
