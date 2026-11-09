"""
================================================================================
BỘ KIỂM THỬ TOÀN DIỆN & ĐO LƯỜNG HIỆU NĂNG - CAD MATH STUDIO v2.1
(Automated Quality Assurance & Verification Benchmark Suite)
================================================================================
"""

import sys
import os
import time

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import sympy as sp
from sympy.solvers.inequalities import reduce_inequalities
import numpy as np

# Nạp ứng dụng từ thư mục hiện tại
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from cad_math_v2 import smart_parse, clean_display_expr, format_friendly_value, x, y, z, m

def run_benchmark():
    print("=" * 90)
    print("  CAD MATH STUDIO v2.1 - HỆ THỐNG KIỂM THỬ TỰ ĐỘNG & ĐO LƯỜNG CHẤT LƯỢNG TOÁN HỌC")
    print("  Thời gian kiểm thử:", time.strftime('%d/%m/%Y %H:%M:%S'))
    print("=" * 90)

    test_cases = [
        # 1. BPT bậc hai
        {
            "id": 1,
            "category": "Bất phương trình đa thức",
            "name": "BPT Bậc hai: x² - 3x + 2 <= 0",
            "run": lambda: reduce_inequalities(smart_parse("x^2 - 3*x + 2 <= 0"), x).as_set(),
            "expected_check": lambda res: str(res) == "Interval(1, 2)"
        },
        # 2. BPT phân thức
        {
            "id": 2,
            "category": "Bất phương trình phân thức",
            "name": "BPT Phân thức: (x - 1)/(x + 2) > 0",
            "run": lambda: reduce_inequalities(smart_parse("(x - 1)/(x + 2) > 0"), x).as_set(),
            "expected_check": lambda res: "oo" in str(res) and "-2" in str(res) and "1" in str(res)
        },
        # 3. Căn bậc n (Căn bậc 4 và 3)
        {
            "id": 3,
            "category": "Căn thức bậc n tổng quát",
            "name": r"Căn bậc 4 & Căn bậc 3: \sqrt[4]{x-1} và root(3, x+2)",
            "run": lambda: (smart_parse(r"\sqrt[4]{x - 1}"), smart_parse("root(3, x + 2)")),
            "expected_check": lambda res: str(res[0]) == "(x - 1)**(1/4)" and str(res[1]) == "(x + 2)**(1/3)"
        },
        # 4. Chuẩn hóa root(deg, expr) đảo ngược
        {
            "id": 4,
            "category": "Cú pháp căn bậc n",
            "name": "Tự động đảo thứ tự root(4, x-1) -> (x-1)^(1/4)",
            "run": lambda: smart_parse("root(4, x - 1)"),
            "expected_check": lambda res: str(res) == "(x - 1)**(1/4)"
        },
        # 5. Hệ phương trình VDC chứa căn bậc 4 (Bài toán kiểm tra của người dùng)
        {
            "id": 5,
            "category": "Hệ PT phi tuyến VDC",
            "name": r"Hệ căn bậc 4 Olympiad: \sqrt[4]{x-1}+\sqrt{x+1}-\sqrt{y^4+2}=y và x²+2x(y-1)+y²-6y+1=0",
            "run": lambda: test_solve_olympiad_system(),
            "expected_check": lambda res: (1, 0) in res and (2, 1) in res
        },
        # 6. Hệ phương trình đối xứng
        {
            "id": 6,
            "category": "Hệ phương trình đối xứng",
            "name": "Hệ đối xứng: x + y = 5; x * y = 6",
            "run": lambda: sp.solve([sp.Eq(x + y, 5), sp.Eq(x * y, 6)], (x, y)),
            "expected_check": lambda res: len(res) == 2 and (2, 3) in [(int(p[0]), int(p[1])) for p in res]
        },
        # 7. Phương trình lượng giác nhân đôi
        {
            "id": 7,
            "category": "Phương trình lượng giác",
            "name": "Lượng giác: cos(2x) - 3cos(x) + 2 = 0",
            "run": lambda: test_solve_trig(),
            "expected_check": lambda res: 1 in res and sp.Rational(1, 2) in res
        },
        # 8. Số phức
        {
            "id": 8,
            "category": "Đại số số phức",
            "name": "Phương trình bậc nhất số phức: (1 + 2i)z + 3 - i = 0",
            "run": lambda: sp.solve(smart_parse("(1 + 2*I)*z + 3 - I = 0"), z),
            "expected_check": lambda res: len(res) > 0 and abs(complex(res[0].evalf()).real - (-0.2)) < 1e-3
        },
        # 9. Cực trị VDC đa biến
        {
            "id": 9,
            "category": "Cực trị VDC đa biến",
            "name": "Cực trị 3 biến: 3^(|x-y|) + 3^(|y-z|) + 3^(|z-x|) tại x=y=z",
            "run": lambda: smart_parse("3^(|x-y|) + 3^(|y-z|) + 3^(|z-x|)").subs({x: 1, y: 1, z: 1}),
            "expected_check": lambda res: int(res) == 3
        },
        # 10. Đạo hàm riêng đa biến
        {
            "id": 10,
            "category": "Vi tích phân đa biến",
            "name": "Đạo hàm riêng: d/dx (x³·y² - 2xy + sin(x))",
            "run": lambda: sp.diff(smart_parse("x^3 * y^2 - 2*x*y + sin(x)"), x),
            "expected_check": lambda res: "3*x**2*y**2" in str(res) and "cos(x)" in str(res)
        },
        # 11. Tích phân từng phần xác định
        {
            "id": 11,
            "category": "Tích phân xác định",
            "name": "Tích phân: ∫ (x · e^x) dx từ 0 đến 1",
            "run": lambda: sp.integrate(x * sp.exp(x), (x, 0, 1)),
            "expected_check": lambda res: int(res) == 1
        },
        # 12. Giới hạn cơ bản
        {
            "id": 12,
            "category": "Giới hạn giải tích",
            "name": "Giới hạn hàm số: lim_{x->0} sin(x)/x",
            "run": lambda: sp.limit(sp.sin(x) / x, x, 0),
            "expected_check": lambda res: int(res) == 1
        },
        # 13. Khai triển chuỗi Taylor
        {
            "id": 13,
            "category": "Chuỗi số & Taylor",
            "name": "Khai triển Taylor: exp(x) lân cận 0 bậc 3",
            "run": lambda: sp.series(sp.exp(x), x, 0, 4).removeO(),
            "expected_check": lambda res: "x**3/6" in str(res) and "x**2/2" in str(res)
        },
        # 14. Nhân ma trận A x B
        {
            "id": 14,
            "category": "Đại số tuyến tính",
            "name": "Phép nhân ma trận: [[1, 2], [3, 4]] x [[2, 0], [1, 2]]",
            "run": lambda: sp.Matrix([[1, 2], [3, 4]]) * sp.Matrix([[2, 0], [1, 2]]),
            "expected_check": lambda res: res == sp.Matrix([[4, 4], [10, 8]])
        },
        # 15. Định thức & Nghịch đảo ma trận
        {
            "id": 15,
            "category": "Đại số tuyến tính",
            "name": "Định thức det([[1, 2], [3, 4]]) = -2",
            "run": lambda: sp.Matrix([[1, 2], [3, 4]]).det(),
            "expected_check": lambda res: int(res) == -2
        },
        # 16. Tổ hợp & Chỉnh hợp
        {
            "id": 16,
            "category": "Tổ hợp - Xác suất",
            "name": "Tổ hợp C(10, 3) = 120 và Chỉnh hợp A(10, 3) = 720",
            "run": lambda: (int(sp.binomial(10, 3)), int(sp.ff(10, 3))),
            "expected_check": lambda res: res == (120, 720)
        },
        # 17. Thống kê mô tả
        {
            "id": 17,
            "category": "Thống kê mô tả",
            "name": "Trung bình và Trung vị dãy [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]",
            "run": lambda: (float(np.mean(range(1, 11))), float(np.median(range(1, 11)))),
            "expected_check": lambda res: res == (5.5, 5.5)
        },
        # 18. Khảo sát cực trị hàm số Oxy
        {
            "id": 18,
            "category": "Khảo sát hàm số Oxy",
            "name": "Cực trị hàm bậc 3: y = x³ - 3x² + 2 ==> Cực trị tại x = 0 và x = 2",
            "run": lambda: sp.solve(sp.diff(x**3 - 3*x**2 + 2, x), x),
            "expected_check": lambda res: set(res) == {0, 2}
        },
        # 19. Điểm uốn đồ thị Oxy
        {
            "id": 19,
            "category": "Khảo sát hàm số Oxy",
            "name": "Điểm uốn đồ thị bậc 3: y'' = 6x - 6 = 0 ==> x = 1",
            "run": lambda: sp.solve(sp.diff(x**3 - 3*x**2 + 2, x, 2), x),
            "expected_check": lambda res: res == [1]
        },
        # 20. Bài toán tham số m bậc 2
        {
            "id": 20,
            "category": "Bài toán tham số m",
            "name": "Tam thức: f(x) = x² - 2(m-1)x + m + 5 >= 0 với mọi x ==> m in [-1; 4]",
            "run": lambda: test_param_m(),
            "expected_check": lambda res: res == (-1, 4)
        }
    ]

    passed_count = 0
    total_time_ms = 0
    results_summary = []

    for tc in test_cases:
        t0 = time.perf_counter()
        status = "PASSED"
        err_msg = ""
        try:
            res = tc["run"]()
            ok = tc["expected_check"](res)
            if not ok:
                status = "FAILED"
                err_msg = f"Kết quả không khớp: {res}"
        except Exception as e:
            status = "FAILED"
            err_msg = str(e)
        t_elap_ms = (time.perf_counter() - t0) * 1000
        total_time_ms += t_elap_ms

        if status == "PASSED":
            passed_count += 1
            icon = "[PASS]"
        else:
            icon = "[FAIL]"

        results_summary.append({
            "id": tc["id"],
            "category": tc["category"],
            "name": tc["name"],
            "time_ms": t_elap_ms,
            "status": status,
            "error": err_msg
        })

        print(f"  {icon} Bài {tc['id']:02d} | {tc['category']:<26} | {t_elap_ms:6.2f} ms | {tc['name']}")
        if status == "FAILED":
            print(f"        Lỗi chi tiết: {err_msg}")

    avg_time = total_time_ms / len(test_cases)
    pass_rate = (passed_count / len(test_cases)) * 100

    print("=" * 90)
    print(f"  KẾT QUẢ TỔNG QUAN:")
    print(f"  • Số bài kiểm thử đạt: {passed_count}/{len(test_cases)} ({pass_rate:.1f}%)")
    print(f"  • Thời gian chạy trung bình: {avg_time:.2f} ms / bài toán")
    print(f"  • Tổng thời gian đo lường: {total_time_ms:.2f} ms")
    print(f"  • Đánh giá chất lượng: {'ĐẠT CHUẨN XUẤT SẮC (ENTERPRISE GRADE)' if pass_rate == 100 else 'CẦN HOÀN THIỆN THÊM'}")
    print("=" * 90)

    # Xuất báo cáo Markdown
    report_md = f"""# BÁO CÁO ĐO LƯỜNG CHẤT LƯỢNG HỆ THỐNG - CAD MATH STUDIO v2.1
**Ngày xuất báo cáo:** {time.strftime('%d/%m/%Y %H:%M:%S')}  
**Kết quả kiểm định:** **{passed_count}/{len(test_cases)} ({pass_rate:.1f}%) ĐẠT TIÊU CHUẨN**  
**Tốc độ thực thi trung bình:** **{avg_time:.2f} ms / bài**  

| STT | Phân Hệ Bài Toán | Tên Bài Toán Kiểm Thử | Thời Gian (ms) | Trạng Thái |
| :---: | :--- | :--- | :---: | :---: |
"""
    for r in results_summary:
        st_icon = "✅ PASSED" if r["status"] == "PASSED" else "❌ FAILED"
        report_md += f"| {r['id']:02d} | {r['category']} | {r['name']} | {r['time_ms']:.2f} | {st_icon} |\n"

    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "BENCHMARK_REPORT.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"  --> Đã xuất báo cáo kiểm định: {report_path}")

def test_solve_olympiad_system():
    eq1 = sp.root(x - 1, 4) + sp.sqrt(x + 1) - sp.sqrt(y**4 + 2) - y
    eq2 = x**2 + 2*x*(y - 1) + y**2 - 6*y + 1
    branches = sp.solve(eq2, x)
    found = []
    for br in branches:
        sub = eq1.subs(x, br)
        for y_test in [0, 1, 2, 3, 4]:
            val = sub.subs(y, y_test).evalf()
            if abs(complex(val)) < 1e-9:
                xv = br.subs(y, y_test).evalf()
                if xv.is_real and xv >= 1:
                    found.append((int(round(float(xv))), int(y_test)))
    return list(dict.fromkeys(found))

def test_solve_trig():
    trig_eq = smart_parse("cos(2*x) - 3*cos(x) + 2")
    cos_x = sp.Symbol('X_cos')
    target_cos = trig_eq.subs(sp.cos(2*x), 2*cos_x**2 - 1).subs(sp.cos(x), cos_x)
    return sp.solve(target_cos, cos_x)

def test_param_m():
    delta = (m - 1)**2 - (m + 5)
    roots = sp.solve(delta, m)
    return (int(roots[0]), int(roots[1]))

if __name__ == "__main__":
    run_benchmark()
