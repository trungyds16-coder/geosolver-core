# -*- coding: utf-8 -*-
import math
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from geosolver.geosolver_desktop import THEMES_GEOSOLVER, calc_ellipse_perimeter

def hex_to_luminance(hex_str):
    hex_str = hex_str.lstrip('#')
    r, g, b = [int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    def adj(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * adj(r) + 0.7152 * adj(g) + 0.0722 * adj(b)

def contrast_ratio(c1, c2):
    l1, l2 = hex_to_luminance(c1), hex_to_luminance(c2)
    if l1 < l2: l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)

print("=== WCAG CONTRAST RATIOS (EXACT MEASUREMENTS) ===")
wcag_rows = []
for k, t in THEMES_GEOSOLVER.items():
    name = t['name']
    pairs = [
        ("Văn bản cửa sổ", t['text'], t['bg_window']),
        ("Văn bản Ribbon", t['text'], t['toolbar_bg']),
        ("Nút thường (btn_fg/btn_bg)", t['btn_fg'], t['btn_bg']),
        ("Nút đang chọn (tool_active_fg/tool_active_bg)", t['tool_active_fg'], t['tool_active_bg']),
        ("Thanh trạng thái (status_fg/status_bg)", t['status_fg'], t['status_bg']),
    ]
    for role, fg, bg in pairs:
        cr = contrast_ratio(fg, bg)
        grade = "AAA" if cr >= 7.0 else ("AA" if cr >= 4.5 else "FAIL")
        wcag_rows.append((k, name, role, fg, bg, cr, grade))
        print(f"[{k}] {role}: {fg} on {bg} => {cr:.2f}:1 ({grade})")

print("\n=== RAMANUJAN PERIMETER ERROR (EXACT SIMPSON INTEGRAL) ===")
def numerical_integral_perimeter(a, b, steps=100000):
    dt = (math.pi / 2.0) / steps
    s = sum(math.sqrt(a*a * math.sin((i+0.5)*dt)**2 + b*b * math.cos((i+0.5)*dt)**2) for i in range(steps))
    return 4.0 * s * dt

def ramanujan_1(a, b):
    return math.pi * (3.0 * (a + b) - math.sqrt((3.0 * a + b) * (a + 3.0 * b)))

def ramanujan_2(a, b):
    if b == 0.0: return 4.0 * a
    h = ((a - b) / (a + b)) ** 2
    return math.pi * (a + b) * (1.0 + (3.0 * h) / (10.0 + math.sqrt(max(0.0, 4.0 - 3.0 * h))))

test_cases = [
    (5.0, 5.0, "Đường tròn (b/a = 1.0)"),
    (5.0, 4.0, "Elip chuẩn (b/a = 0.8)"),
    (5.0, 2.5, "Elip trung bình (b/a = 0.5)"),
    (5.0, 0.5, "Elip dẹt (b/a = 0.1)"),
    (5.0, 0.05, "Elip rất dẹt (b/a = 0.01)"),
    (5.0, 0.0, "Suy biến đoạn thẳng (b/a = 0.0)"),
]

ram_rows = []
for a, b, desc in test_cases:
    p_exact = 4.0 * a if b == 0.0 else numerical_integral_perimeter(a, b)
    p_r1 = ramanujan_1(a, b)
    p_r2 = ramanujan_2(a, b)
    err_r1 = abs(p_r1 - p_exact) / p_exact * 100.0
    err_r2 = abs(p_r2 - p_exact) / p_exact * 100.0
    # Also calculate pure Ramanujan 2 without the shortcut at b=0
    if b == 0.0:
        h0 = 1.0
        p_r2_pure = math.pi * a * (1.0 + 3.0 / (10.0 + 1.0)) # pi * a * (1 + 3/11) = pi * a * 14/11 ≈ 3.9984...
        err_r2_pure = abs(p_r2_pure - p_exact) / p_exact * 100.0
        print(f"At b=0: continuous Ramanujan 2 gives P={p_r2_pure:.8f}, error={err_r2_pure:.6f}%")
    ram_rows.append((desc, a, b, p_exact, p_r1, err_r1, p_r2, err_r2))
    print(f"{desc}: P_exact={p_exact:.8f}, R1={p_r1:.8f} (err={err_r1:.6f}%), R2={p_r2:.8f} (err={err_r2:.6f}%)")
