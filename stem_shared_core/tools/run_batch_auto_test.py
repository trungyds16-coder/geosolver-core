"""
Benchmark Harness tự động kiểm định thuật toán giải phương trình & hệ Diophantine (CADMathCore)
Phiên bản: 2.13 (Nghiên cứu khoa học & Kiểm định độc lập)
Đặc điểm:
- Kiểm tra Bất biến Toán học:
  + Phân hệ Radical: R1 (Triệt tiêu phần dư & vế phải không âm), R2 (Vi phạm vế phải độc lập),
    R3 (Bất biến phân hoạch), R4 (Tập nghiệm đối chuẩn chuyên gia).
  + Phân hệ Diophantine: D1 (Tính khả thi nguyên dương độc lập), D2 (Hợp đồng hiển thị đại diện),
    D3 (Tính khớp số lượng nghiệm giải tích).
- Oracle kiểm tra tính khả thi nguyên trên tham số hóa affine từ sp.linsolve:
  + Vét cạn trực tiếp tham số tự do p in [1, 3000] bằng math.lcm và số học nguyên C thuần túy.
  + Kiểm thử trên 100 hệ Diophantine ngẫu nhiên phân tầng cân bằng (25 hệ/loại).
- Kiểm thử đột biến thật trên Bytecode (Real Mutation Testing) trên 6 toán tử đại diện.
- Đo đạc thời gian qua 5 vòng thực nghiệm: báo cáo trung vị, within-task IQR và cross-task IQR.
- Truy vấn môi trường thực thi động (dynamic environment querying).
"""

import os
import sys
import time
import math
import random
import statistics
import inspect
import types
import textwrap
import unittest.mock
import platform
import sympy as sp

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from stem_shared_core.cad_math_core import CADMathCore, DiophantineCategory

def get_test_cases(x, y, z):
    return [
        # NHÓM 1: PHƯƠNG TRÌNH VÔ TỶ (8 CA ĐẶC TRƯNG)
        {
            "id": "RAD_01_CANONICAL",
            "name": "Phương trình vô tỷ chính tắc sqrt(2x-1) = x - 1 (c = 1)",
            "type": "radical",
            "target": sp.sqrt(2*x - 1) - (x - 1),
            "var": x,
            "expected_valid": [2 + sp.sqrt(2)],
            "expected_rejected_count": 1
        },
        {
            "id": "RAD_02_NEGATIVE_COEFF",
            "name": "Phương trình vô tỷ hệ số căn âm: (x - 1) - sqrt(2x-1) = 0 (c = -1)",
            "type": "radical",
            "target": (x - 1) - sp.sqrt(2*x - 1),
            "var": x,
            "expected_valid": [2 + sp.sqrt(2)],
            "expected_rejected_count": 1
        },
        {
            "id": "RAD_03_COEFF_NOT_ONE",
            "name": "Phương trình vô tỷ hệ số căn c != 1: 2*sqrt(x+2) - (x+1) = 0",
            "type": "radical",
            "target": 2*sp.sqrt(x + 2) - (x + 1),
            "var": x,
            "expected_valid": [1 + 2*sp.sqrt(2)],
            "expected_rejected_count": 1
        },
        {
            "id": "RAD_04_CARDANO_CUBIC",
            "name": "Phương trình vô tỷ bậc 3 sinh nghiệm Cardano thực: sqrt(x^3-3x+1) = 1/2",
            "type": "radical",
            "target": sp.sqrt(x**3 - 3*x + 1) - sp.Rational(1, 2),
            "var": x,
            "expected_valid_count": 3,
            "expected_rejected_count": 0
        },
        {
            "id": "RAD_05_COMPLEX_QUARTIC",
            "name": "Bẫy bình phương sinh nghiệm phức: sqrt(x) = x^2 + 1",
            "type": "radical",
            "target": sp.sqrt(x) - (x**2 + 1),
            "var": x,
            "expected_valid": [],
            "expected_rejected_count": 4
        },
        {
            "id": "RAD_06_OUT_OF_SCOPE",
            "name": "Phương trình nhiều căn thức (ngoài phạm vi): sqrt(x+1) + sqrt(x-1) = 2",
            "type": "radical_out_of_scope",
            "target": sp.sqrt(x + 1) + sp.sqrt(x - 1) - 2,
            "var": x,
            "expected_error": True
        },
        {
            "id": "RAD_07_SYNTHETIC_UNKNOWN",
            "name": "Kiểm thử đường dẫn an toàn qua mock.patch: Nhánh bất định (indeterminate)",
            "type": "radical_mock_unknown",
            "target": sp.sqrt(2*x - 1) - (x - 1),
            "var": x,
            "expected_indet_count": 2
        },
        {
            "id": "RAD_08_ZERO_BRANCH",
            "name": "Phương trình vô tỷ nghiệm tại biên vế phải: sqrt(x) - x = 0 (g(0)=0)",
            "type": "radical",
            "target": sp.sqrt(x) - x,
            "var": x,
            "expected_valid": [0, 1],
            "expected_rejected_count": 0
        },

        # NHÓM 2: HỆ DIOPHANTINE & PHÂN LOẠI CẤU TRÚC (16 CA BAO PHỦ CÁC TRẠNG THÁI & BIÊN SUY BIẾN)
        {
            "id": "DIO_01_TRAM_TRAU",
            "name": "Bài toán Trăm trâu cổ điển",
            "type": "diophantine",
            "eqs": [x + y + z - 100, 5*x + 3*y + sp.Rational(1, 3)*z - 100],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.FINITE_BOUNDED,
            "expected_count": 3,
            "expected_sample": (4, 18, 78)
        },
        {
            "id": "DIO_02_SYSTEM_2",
            "name": "Hệ Diophantine hai phương trình hữu hạn",
            "type": "diophantine",
            "eqs": [3*x - 7*z + 500, 3*y + 10*z - 800],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.FINITE_BOUNDED,
            "expected_count": 2,
            "expected_sample": (6, 20, 74)
        },
        {
            "id": "DIO_03_COUNTER_A",
            "name": "Phản ví dụ A bước nhảy 251 (Vô hạn nghiệm)",
            "type": "diophantine",
            "eqs": [251*x - z + 5, y - 2],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.UNBOUNDED_INFINITE,
            "expected_sample": (1, 2, 256)
        },
        {
            "id": "DIO_04_COUNTER_B",
            "name": "Phản ví dụ B vô nghiệm nguyên gcd: 2x - 2z = 1",
            "type": "diophantine",
            "eqs": [2*x - 2*z - 1, y - 5],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS
        },
        {
            "id": "DIO_05_HUGE_CAP",
            "name": "Hệ có số lượng nghiệm lớn N = 10^9, kiểm tra giải tích",
            "type": "diophantine",
            "eqs": [x + z - 1000000001, y - 2],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.FINITE_BOUNDED,
            "expected_count": 1000000000
        },
        {
            "id": "DIO_06_MULTI_PARAM",
            "name": "Hệ đa tham số tự do d=2: x + y + z = 10",
            "type": "diophantine",
            "eqs": [x + y + z - 10],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.UNSUPPORTED_DIM_GE_2
        },
        {
            "id": "DIO_07_INCONSISTENT",
            "name": "Hệ vô nghiệm thực: x + y = 1, x + y = 2",
            "type": "diophantine",
            "eqs": [x + y - 1, x + y - 2],
            "vars": [x, y],
            "expected_category": DiophantineCategory.INCONSISTENT
        },
        {
            "id": "DIO_08_BOUNDS_EMPTY",
            "name": "Hệ vô nghiệm do hằng số không dương: y = 0",
            "type": "diophantine",
            "eqs": [x - z - 5, y],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.INFEASIBLE_BOUNDS_EMPTY
        },
        {
            "id": "DIO_09_UNIQUE_D0",
            "name": "Hệ d=0 xác định nghiệm nguyên dương duy nhất",
            "type": "diophantine",
            "eqs": [x + y - 5, x - y - 1],
            "vars": [x, y],
            "expected_category": DiophantineCategory.UNIQUE,
            "expected_count": 1,
            "expected_sample": (3, 2)
        },
        {
            "id": "DIO_10_NON_COPRIME_CRT",
            "name": "Hệ đồng dư modulo không nguyên tố cùng nhau: gcd(m1, m2) > 1",
            "type": "diophantine",
            "eqs": [6*x - z - 1, 4*y - z - 1],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.UNBOUNDED_INFINITE,
            "expected_sample": (2, 3, 11)
        },
        {
            "id": "DIO_11_UNIQUE_NON_POSITIVE",
            "name": "Hệ d=0 có nghiệm thực duy nhất nhưng không thuộc (Z+)^n",
            "type": "diophantine",
            "eqs": [x + y - 1, x - y - 3],
            "vars": [x, y],
            "expected_category": DiophantineCategory.EMPTY_NO_POSITIVE_INTEGER,
            "expected_count": 0
        },
        {
            "id": "DIO_12_CRT_INCOMPATIBLE",
            "name": "Hệ đồng dư CRT xung đột vô nghiệm (sc is None)",
            "type": "diophantine",
            "eqs": [2*x - z, 2*y - z + 1],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS,
            "expected_count": 0
        },
        {
            "id": "DIO_13_BOUNDARY_SENSITIVE_LO",
            "name": "Ca biên nhạy cận dưới: x - z + 3 = 0, y - 2 = 0 (z >= 4, diệt Mutant 1)",
            "type": "diophantine",
            "eqs": [x - z + 3, y - 2],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.UNBOUNDED_INFINITE,
            "expected_sample": (1, 2, 4)
        },
        {
            "id": "DIO_14_BOUNDARY_SENSITIVE_HI",
            "name": "Ca biên nhạy cận trên: x + z - 4 = 0, y - 2 = 0 (z <= 3, diệt Mutant 2 & 3)",
            "type": "diophantine",
            "eqs": [x + z - 4, y - 2],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.FINITE_BOUNDED,
            "expected_count": 3,
            "expected_sample": (3, 2, 1)
        },
        {
            "id": "DIO_15_BOUNDARY_DEGENERATE_START",
            "name": "Ca biên suy biến bước nhảy start_val == hi: 2x - z + 1 = 0, y + z - 4 = 0",
            "type": "diophantine",
            "eqs": [2*x - z + 1, y + z - 4],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.FINITE_BOUNDED,
            "expected_count": 1,
            "expected_sample": (1, 1, 3)
        },
        {
            "id": "DIO_16_BOUNDARY_DEGENERATE_INTERVAL",
            "name": "Ca biên khoảng cận co cụm 1 điểm [1, 1]: x + z - 2 = 0, y - 2 = 0",
            "type": "diophantine",
            "eqs": [x + z - 2, y - 2],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.FINITE_BOUNDED,
            "expected_count": 1,
            "expected_sample": (1, 2, 1)
        }
    ]

def execute_single_run(app, test_cases, is_warmup=False):
    passed_count = 0
    times = []
    results = []

    for idx, test in enumerate(test_cases, 1):
        t0 = time.perf_counter()
        t_type = test["type"]
        is_pass = False
        detail = ""

        try:
            if t_type == "radical":
                steps, valid, rejected, indet = app.solve_radical_pedagogical(test["target"], test["var"])
                dt = (time.perf_counter() - t0) * 1000
                times.append(dt)

                rads = [t for t in test["target"].atoms(sp.Pow) if t.exp == sp.Rational(1, 2)]
                rad = rads[0]
                expanded = sp.expand(test["target"])
                c_val = expanded.coeff(rad)
                rest = sp.expand(expanded - c_val * rad)
                gx = sp.simplify(-rest / c_val)
                fx = rad.base

                # BẤT BIẾN R1: Triệt tiêu phần dư phương trình gốc < 1e-7 và vế phải g(r) >= -1e-12
                r1_ok = True
                for r in valid:
                    val_sub = abs(complex(sp.N(test["target"].subs(test["var"], r))))
                    g_val = float(sp.N(gx.subs(test["var"], r)))
                    if val_sub >= 1e-7 or g_val < -1e-12:
                        r1_ok = False
                        break

                # BẤT BIẾN R2: Nghiệm rejected vi phạm độc lập điều kiện xác định/vế phải/nghiệm phức
                r2_ok = True
                for r_info in rejected:
                    r = r_info[0]
                    r_im = abs(complex(sp.N(r)).imag)
                    if r_im > 1e-5:
                        continue
                    g_val = float(sp.N(gx.subs(test["var"], r)))
                    f_val = float(sp.N(fx.subs(test["var"], r)))
                    residue = abs(complex(sp.N(test["target"].subs(test["var"], r))))
                    if g_val < -1e-12 or f_val < -1e-12 or residue > 1e-5:
                        continue
                    r2_ok = False
                    break

                # BẤT BIẾN R3 (PHÂN HOẠCH): len(valid) + len(rejected) + len(indet) == len(raw_sols)
                poly_eq = sp.simplify(fx - gx**2)
                raw_sols = sp.solve(poly_eq, test["var"])
                r3_ok = (len(valid) + len(rejected) + len(indet) == len(raw_sols))

                # BẤT BIẾN R4 (ĐỐI CHIẾU TẬP CHUẨN ĐÃ DUYỆT): Curated Reference Set Matching
                if "expected_valid" in test:
                    r4_ok = (len(valid) == len(test["expected_valid"]))
                    if r4_ok and len(valid) > 0:
                        r4_ok = all(any(sp.simplify(v - ev) == 0 for ev in test["expected_valid"]) for v in valid)
                elif "expected_valid_count" in test:
                    r4_ok = (len(valid) == test["expected_valid_count"])
                else:
                    r4_ok = True

                rej_count_ok = (len(rejected) == test["expected_rejected_count"])

                if r1_ok and r2_ok and r3_ok and r4_ok and rej_count_ok:
                    is_pass = True
                    detail = f"Nhận {len(valid)}, loại {len(rejected)} (Thỏa mãn Bất biến R1-R4)"
                else:
                    detail = f"Thất bại: R1={r1_ok}, R2={r2_ok}, R3={r3_ok}, R4={r4_ok}, Rej={rej_count_ok}"

            elif t_type == "radical_out_of_scope":
                steps, valid, rejected, indet = app.solve_radical_pedagogical(test["target"], test["var"])
                dt = (time.perf_counter() - t0) * 1000
                times.append(dt)
                if len(steps) > 0 and "Ngoài phạm vi hỗ trợ" in steps[0]:
                    is_pass = True
                    detail = "Từ chối an toàn dạng bài ngoài phạm vi hỗ trợ"

            elif t_type == "radical_mock_unknown":
                with unittest.mock.patch.object(app, 'check_sign_exact', return_value='unknown'):
                    steps, valid, rejected, indet = app.solve_radical_pedagogical(test["target"], test["var"])
                dt = (time.perf_counter() - t0) * 1000
                times.append(dt)
                warning_ok = any("CHƯA THỂ KẾT LUẬN" in s for s in steps)
                if len(indet) == test["expected_indet_count"] and len(valid) == 0 and warning_ok:
                    is_pass = True
                    detail = f"Mã sản phẩm nhận diện {len(indet)} nghiệm bất định, cảnh báo bước 4 kích hoạt"

            elif t_type == "diophantine":
                cat, sols, n_tot, out_lines = app.solve_underdetermined_or_diophantine(test["eqs"], test["vars"])
                dt = (time.perf_counter() - t0) * 1000
                times.append(dt)

                exp_cat = test["expected_category"]
                cat_ok = (cat == exp_cat)

                # BẤT BIẾN D1: Tính khả thi nguyên dương độc lập và thỏa mãn hệ phương trình gốc
                d1_ok = True
                if sols:
                    for s_tuple in sols:
                        if not all(isinstance(val, int) and val > 0 for val in s_tuple):
                            d1_ok = False
                            break
                        sub_d = {v: val for v, val in zip(test["vars"], s_tuple)}
                        if not all(sp.simplify(eq.subs(sub_d)) == 0 for eq in test["eqs"]):
                            d1_ok = False
                            break
                else:
                    d1_ok = (n_tot == 0)

                # BẤT BIẾN D2: Hợp đồng độ dài tập nghiệm hiển thị đại diện (Display length contract)
                d2_ok = True
                if cat == DiophantineCategory.FINITE_BOUNDED:
                    d2_ok = (len(sols) == min(n_tot, 10))
                elif cat == DiophantineCategory.UNBOUNDED_INFINITE:
                    d2_ok = (len(sols) == 3)

                # BẤT BIẾN D3: Tính khớp số lượng nghiệm giải tích
                d3_ok = True
                if "expected_count" in test:
                    d3_ok = (n_tot == test["expected_count"])

                sample_ok = True
                if "expected_sample" in test:
                    sample_ok = (test["expected_sample"] in sols)

                if cat_ok and d1_ok and d2_ok and d3_ok and sample_ok:
                    is_pass = True
                    if sols:
                        detail = f"Category={cat} khớp, D1-D3 thỏa mãn ({len(sols)} nghiệm đại diện, n_tot={n_tot})"
                    else:
                        detail = f"Category={cat} khớp, D1-D3 thỏa mãn (0 nghiệm, n_tot=0)"
                else:
                    detail = f"Thất bại: cat_ok={cat_ok} (got {cat}), D1={d1_ok}, D2={d2_ok}, D3={d3_ok}, sample={sample_ok}"

        except Exception as e:
            dt = (time.perf_counter() - t0) * 1000
            times.append(dt)
            detail = f"Lỗi ngoại lệ: {e}"

        if is_pass: passed_count += 1
        results.append((test['id'], is_pass, dt, detail))

    return passed_count, times, results

def run_suite():
    py_ver = sys.version.split()[0]
    plat_str = platform.platform()
    arch_str = platform.machine()
    sympy_ver = sp.__version__

    print("=" * 95)
    print("BẮT ĐẦU CHẠY BỘ KIỂM THỬ TỰ ĐỘNG HÀNG LOẠT V2.13 (CAD MATH STUDIO BENCHMARK HARNESS)")
    print(f"Môi trường thực thi động: SymPy {sympy_ver} | Python {py_ver} | Nền tảng: {plat_str} ({arch_str})")
    print("Kiểm tra Bất biến R1-R4 & D1-D3, Oracle Hộp phân tầng (N=3000) & 6 Toán tử đột biến thật")
    print("=" * 95)

    app = CADMathCore()
    x, y, z = sp.symbols('x y z')
    test_cases = get_test_cases(x, y, z)

    # 1. VÒNG KHỞI ĐỘNG (WARM-UP RUN TÁCH BIỆT)
    print("[1] Đang thực thi vòng khởi động (Warm-up run để nạp SymPy cache nội tại)...")
    execute_single_run(app, test_cases, is_warmup=True)

    # 2. CHẠY 5 VÒNG THỰC ĐO THỜI GIAN ĐỂ TÍNH TRUNG VỊ VÀ ĐỘ PHÂN TÁN (WITHIN & CROSS-TASK IQR)
    print("[2] Thực hiện 5 vòng đo chính thức để xác định Trung vị (Median), within-task IQR và cross-task IQR...")
    all_runs_times = []
    last_results = None
    last_passed = 0

    for r_idx in range(5):
        passed, times, results = execute_single_run(app, test_cases)
        all_runs_times.append(times)
        last_results = results
        last_passed = passed

    per_test_medians = []
    per_test_within_iqr = []
    for i in range(len(test_cases)):
        t_list = [all_runs_times[r][i] for r in range(5)]
        per_test_medians.append(statistics.median(t_list))
        q_within = statistics.quantiles(t_list, n=4)
        per_test_within_iqr.append(q_within[2] - q_within[0])

    total_medians = sum(per_test_medians)
    quantiles_all = statistics.quantiles(per_test_medians, n=4)
    cross_task_iqr = quantiles_all[2] - quantiles_all[0]
    avg_within_iqr = statistics.mean(per_test_within_iqr)

    for idx, (t_id, is_pass, _, detail) in enumerate(last_results):
        status_str = "[OK]  " if is_pass else "[FAIL]"
        med_t = per_test_medians[idx]
        w_iqr = per_test_within_iqr[idx]
        print(f"[{idx+1:02d}/{len(test_cases):02d}] {status_str} {t_id:<36} (Trung vị: {med_t:6.2f} ms | w-IQR: {w_iqr:5.2f} ms) | {detail}")

    # PHẦN 2: ORACLE KIỂM TRA TÍNH KHẢ THI NGUYÊN TRÊN THAM SỐ HÓA AFFINE (100 HỆ PHÂN TẦNG, N=3000)
    print("-" * 95)
    print("CHẠY ORACLE KIỂM TRA TÍNH KHẢ THI NGUYÊN TRÊN THAM SỐ HÓA AFFINE (100 HỆ PHÂN TẦNG, Seed = 42, Hộp N = 3000)")
    print("Cơ chế: Vét cạn trực tiếp tham số p in [1, 3000] bằng math.lcm / số học nguyên C (Không dùng công thức cận hay CRT solver)")
    random.seed(42)
    categories_needed = {
        DiophantineCategory.FINITE_BOUNDED: 0,
        DiophantineCategory.UNBOUNDED_INFINITE: 0,
        DiophantineCategory.INFEASIBLE_BOUNDS_EMPTY: 0,
        DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS: 0
    }
    dataset = []
    while any(count < 25 for count in categories_needed.values()):
        a1, b1, c1 = [random.choice([-4, -3, -2, -1, 1, 2, 3, 4]) for _ in range(3)]
        a2, b2, c2 = [random.choice([-4, -3, -2, -1, 1, 2, 3, 4]) for _ in range(3)]
        rhs1 = random.randint(-40, 40)
        rhs2 = random.randint(-40, 40)
        eqs = [a1*x + b1*y + c1*z - rhs1, a2*x + b2*y + c2*z - rhs2]
        cat, sols, n_tot, out_l = app.solve_underdetermined_or_diophantine(eqs, [x, y, z])
        if cat in categories_needed and categories_needed[cat] < 25:
            categories_needed[cat] += 1
            dataset.append(eqs)

    oracle_passed = 0
    N = 3000
    t_oracle_0 = time.perf_counter()

    for idx, eqs in enumerate(dataset):
        cat, sols, n_tot, out_l = app.solve_underdetermined_or_diophantine(eqs, [x, y, z])
        linsols = sp.linsolve(eqs, [x, y, z])
        sol_tuple = list(linsols)[0]
        free_s = sorted(list(set().union(*[it.free_symbols for it in sol_tuple])), key=lambda s: s.name)
        p = free_s[0]

        affines = []
        has_neg_slope = False
        for expr in sol_tuple:
            e_exp = sp.expand(expr)
            a_r = sp.Rational(e_exp.coeff(p))
            b_r = sp.Rational(e_exp.subs(p, 0))
            if a_r < 0: has_neg_slope = True
            D = math.lcm(a_r.q, b_r.q)
            A_p = int(a_r.p * (D // a_r.q))
            B_p = int(b_r.p * (D // b_r.q))
            affines.append((A_p, B_p, D))

        box_sols = []
        for v in range(1, N + 1):
            vals = []
            is_ok = True
            for A_p, B_p, D in affines:
                val = A_p * v + B_p
                if val <= 0 or val % D != 0:
                    is_ok = False
                    break
                vals.append(val // D)
            if is_ok:
                box_sols.append(tuple(vals))
        box_count = len(box_sols)

        if has_neg_slope:
            if box_count == 0:
                if cat in [DiophantineCategory.INFEASIBLE_BOUNDS_EMPTY, DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS] and n_tot == 0 and len(sols) == 0:
                    oracle_passed += 1
            else:
                if cat == DiophantineCategory.FINITE_BOUNDED and n_tot == box_count and sols == box_sols[:10]:
                    oracle_passed += 1
        else:
            if box_count == 0:
                if cat in [DiophantineCategory.INFEASIBLE_BOUNDS_EMPTY, DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS] and n_tot == 0 and len(sols) == 0:
                    oracle_passed += 1
            else:
                if cat == DiophantineCategory.UNBOUNDED_INFINITE and sols == box_sols[:3]:
                    oracle_passed += 1

    t_oracle = (time.perf_counter() - t_oracle_0) * 1000
    print(f"Kết quả Oracle Hộp phân tầng: {oracle_passed}/100 hệ khớp (Thời gian: {t_oracle:.2f} ms, {t_oracle/100:.2f} ms/hệ)")
    print(f"Phân bổ phân tầng 100 hệ: 25 FINITE_BOUNDED, 25 UNBOUNDED_INFINITE, 25 INFEASIBLE_BOUNDS_EMPTY, 25 INFEASIBLE_NO_INTEGER_POINTS")

    # PHẦN 3: KIỂM THỬ ĐỘT BIẾN THẬT (REAL MUTATION TESTING TRÊN 6 TOÁN TỬ ĐẠI DIỆN)
    print("-" * 95)
    print("CHẠY KIỂM THỬ ĐỘT BIẾN THẬT (REAL MUTATION TESTING TRÊN 6 TOÁN TỬ ĐẠI DIỆN)")
    orig_dioph_src = textwrap.dedent(inspect.getsource(CADMathCore.solve_underdetermined_or_diophantine))
    orig_rad_src = textwrap.dedent(inspect.getsource(CADMathCore.solve_radical_pedagogical))
    core_globals = CADMathCore.solve_underdetermined_or_diophantine.__globals__

    def build_mutant_core(target_method, target_str, repl_str):
        core_inst = CADMathCore()
        if target_method == "diophantine":
            mut_src = orig_dioph_src.replace(target_str, repl_str)
            loc_ns = {}
            exec(mut_src, core_globals, loc_ns)
            core_inst.solve_underdetermined_or_diophantine = types.MethodType(loc_ns['solve_underdetermined_or_diophantine'], core_inst)
        elif target_method == "radical":
            mut_src = orig_rad_src.replace(target_str, repl_str)
            loc_ns = {}
            exec(mut_src, core_globals, loc_ns)
            core_inst.solve_radical_pedagogical = types.MethodType(loc_ns['solve_radical_pedagogical'], core_inst)
        return core_inst

    mutants = [
        {
            "id": "M1_DIO_LO_OFF_BY_ONE",
            "name": "M1: Cận dưới floor()+0 thay vì +1 (Diophantine)",
            "method": "diophantine",
            "target": "sp.floor(-b_sym / a_sym) + 1",
            "repl": "sp.floor(-b_sym / a_sym) + 0"
        },
        {
            "id": "M2_DIO_HI_OFF_BY_ONE",
            "name": "M2: Cận trên ceiling()-0 thay vì -1 (Diophantine)",
            "method": "diophantine",
            "target": "sp.ceiling(-b_sym / a_sym) - 1",
            "repl": "sp.ceiling(-b_sym / a_sym) - 0"
        },
        {
            "id": "M3_DIO_NTOTAL_OFF_BY_ONE",
            "name": "M3: Sai số lượng n_total thiếu +1 (Diophantine)",
            "method": "diophantine",
            "target": "(hi - start_val) // m_mod + 1",
            "repl": "(hi - start_val) // m_mod"
        },
        {
            "id": "M4_DIO_GCD_BYPASS",
            "name": "M4: Bỏ qua kiểm tra gcd khả chia (Diophantine)",
            "method": "diophantine",
            "target": "(-B_val) % g_val != 0",
            "repl": "False"
        },
        {
            "id": "M5_DIO_CRT_CONFLICT_BYPASS",
            "name": "M5: Bỏ qua kiểm tra xung đột CRT sc is None",
            "method": "diophantine",
            "target": "if sc is None:",
            "repl": "if False:"
        },
        {
            "id": "M6_RAD_SIGN_BYPASS",
            "name": "M6: Bỏ qua kiểm tra dấu vế phải g(r) < 0 (Radical)",
            "method": "radical",
            "target": "if s_gx == 'neg':",
            "repl": "if False:"
        }
    ]

    mutants_killed_suite = 0

    for m in mutants:
        mut_app = build_mutant_core(m["method"], m["target"], m["repl"])
        # 1. Kiểm thử trên bộ Suite kiểm định có chủ đích
        passed_s, _, _ = execute_single_run(mut_app, test_cases, is_warmup=True)
        is_killed_by_suite = (passed_s < len(test_cases))
        if is_killed_by_suite:
            mutants_killed_suite += 1

        # 2. Kiểm thử trên 100 hệ ngẫu nhiên phân tầng
        killed_random = 0
        survived_random = 0
        if m["method"] == "diophantine":
            for eqs in dataset:
                is_killed = False
                try:
                    cat_m, sols_m, n_tot_m, out_m = mut_app.solve_underdetermined_or_diophantine(eqs, [x, y, z])
                    linsols = sp.linsolve(eqs, [x, y, z])
                    sol_tuple = list(linsols)[0]
                    free_s = sorted(list(set().union(*[it.free_symbols for it in sol_tuple])), key=lambda s: s.name)
                    p = free_s[0]

                    affines = []
                    has_neg_slope = False
                    for expr in sol_tuple:
                        e_exp = sp.expand(expr)
                        a_r = sp.Rational(e_exp.coeff(p))
                        b_r = sp.Rational(e_exp.subs(p, 0))
                        if a_r < 0: has_neg_slope = True
                        D = math.lcm(a_r.q, b_r.q)
                        A_p = int(a_r.p * (D // a_r.q))
                        B_p = int(b_r.p * (D // b_r.q))
                        affines.append((A_p, B_p, D))

                    box_sols = []
                    for v in range(1, N + 1):
                        vals = []
                        is_ok = True
                        for A_p, B_p, D in affines:
                            val = A_p * v + B_p
                            if val <= 0 or val % D != 0:
                                is_ok = False
                                break
                            vals.append(val // D)
                        if is_ok:
                            box_sols.append(tuple(vals))
                    box_count = len(box_sols)

                    if has_neg_slope:
                        if box_count == 0:
                            if cat_m not in [DiophantineCategory.INFEASIBLE_BOUNDS_EMPTY, DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS] or n_tot_m != 0 or len(sols_m) != 0:
                                is_killed = True
                        else:
                            if cat_m != DiophantineCategory.FINITE_BOUNDED or n_tot_m != box_count or sols_m != box_sols[:10]:
                                is_killed = True
                    else:
                        if box_count == 0:
                            if cat_m not in [DiophantineCategory.INFEASIBLE_BOUNDS_EMPTY, DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS] or n_tot_m != 0 or len(sols_m) != 0:
                                is_killed = True
                        else:
                            if cat_m != DiophantineCategory.UNBOUNDED_INFINITE or sols_m != box_sols[:3]:
                                is_killed = True
                except Exception:
                    is_killed = True

                if is_killed:
                    killed_random += 1
                else:
                    survived_random += 1
            rand_stat_str = f"| 100 hệ ngẫu nhiên: Bị giết {killed_random:>2}/100, Sống sót {survived_random:>2}/100"
        else:
            rand_stat_str = "| (Toán tử Radical: được kiểm thử trực tiếp bởi các ca vô tỷ trong Suite)"

        suite_kill_str = "BỊ GIẾT BỞI SUITE [PASSED]" if is_killed_by_suite else "SỐNG SÓT [FAILED]"
        print(f"  • {m['name']:<48}: {suite_kill_str} {rand_stat_str}")

    mutation_score = (mutants_killed_suite / len(mutants)) * 100
    print(f"\n==> TỔNG KẾT KIỂM THỬ ĐỘT BIẾN: Mutation Score trên Suite kiểm định = {mutants_killed_suite}/{len(mutants)} ({mutation_score:.1f}%)")

    print("=" * 95)
    rad_med = statistics.median(per_test_medians[:8])
    dioph_med = statistics.median(per_test_medians[8:])
    min_t = min(per_test_medians)
    max_t = max(per_test_medians)
    min_idx = per_test_medians.index(min_t)
    min_id = test_cases[min_idx]["id"]
    max_idx = per_test_medians.index(max_t)
    max_id = test_cases[max_idx]["id"]
    print(f"TỔNG KẾT TOÀN BỘ: {last_passed}/{len(test_cases)} bài đạt yêu cầu | Oracle Hộp phân tầng: {oracle_passed}/100 hệ khớp")
    print(f"Thời gian bộ bài (Trung vị 5 vòng): Tổng = {total_medians:.2f} ms | TB = {total_medians/len(test_cases):.2f} ms/bài")
    print(f"  • Độ phân tán: cross-task IQR = {cross_task_iqr:.2f} ms (dải độ khó) | TB within-task IQR = {avg_within_iqr:.2f} ms (độ ổn định lặp lại)")
    print(f"  • Phân hệ Radical ({len(per_test_medians[:8])} bài, Trung vị): {rad_med:.2f} ms/bài | Phân hệ Diophantine ({len(per_test_medians[8:])} bài, Trung vị): {dioph_med:.2f} ms/bài")
    print(f"  • Dải đo thực nghiệm: Min = {min_t:.2f} ms ({min_id}), Max = {max_t:.2f} ms ({max_id})")
    print("=" * 95)

if __name__ == "__main__":
    run_suite()
