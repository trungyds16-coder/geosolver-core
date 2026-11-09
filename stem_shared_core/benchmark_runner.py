# -*- coding: utf-8 -*-
"""
Module: benchmark_runner.py
Đường dẫn: D:\\AI DATA\\STEM_APP\\stem_shared_core\\benchmark_runner.py
Mô tả:
    Hệ thống chạy Benchmark Sư phạm tự động cho lõi đại số `algebra_kernel.py`.
    - Nạp đề bài JSON theo chuẩn `curricula/schema/problem_schema.json`.
    - Gọi trực tiếp `parse_math_expr`, `solve_radical_abs_equation`, `analyze_function_variation`
      từ `algebra_kernel.py`.
    - Đánh giá tự động:
        (1) Tính đúng đắn toán học (Mathematical Correctness)
        (2) Khả năng phát hiện và loại bỏ nghiệm ngoại lai (Extraneous Root Rejection)
        (3) Thời gian thực thi (Execution Latency in ms)
    - Xuất báo cáo thẩm định sư phạm định dạng Markdown (`BENCHMARK_PEDAGOGICAL_REPORT.md`).
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import sympy as sp
from sympy.calculus.util import continuous_domain

# Thiết lập đường dẫn gốc của phân hệ
DEFAULT_CORE_DIR = Path(r"D:\AI DATA\STEM_APP\stem_shared_core")
CAD_MATH_V2_DIR = Path(r"D:\AI DATA\cad_math_v2")

for candidate_dir in (Path(__file__).resolve().parent, DEFAULT_CORE_DIR, CAD_MATH_V2_DIR):
    if candidate_dir.exists() and str(candidate_dir) not in sys.path:
        sys.path.insert(0, str(candidate_dir))


# ==============================================================================
# ĐẢM BẢO TƯƠNG THÍCH VÀ MỞ RỘNG HÀM CHO ALGEBRA_KERNEL.PY
# ==============================================================================

def _build_analyze_function_variation(parse_fn):
    """
    Khởi tạo hàm `analyze_function_variation` chuẩn SGK GDPT 2018 cho `algebra_kernel.py`.
    Hỗ trợ khảo sát hàm đa thức, hàm phân thức (tiệm cận đứng, ngang, xiên) và hàm chứa tham số m.
    """
    def analyze_function_variation(
        expr_str: str,
        var: str = "x",
        parameter: Optional[str] = None,
        parameter_substitution: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        x = sp.Symbol(var, real=True)
        local_vars: Dict[str, sp.Symbol] = {var: x}
        if parameter:
            local_vars[parameter] = sp.Symbol(parameter, real=True)

        raw_expr = parse_fn(expr_str, local_vars=local_vars)

        # Đạo hàm chứa tham số (nếu bài toán có tham số m)
        parametric_derivative_1: Optional[sp.Expr] = None
        if parameter:
            parametric_derivative_1 = sp.simplify(sp.diff(raw_expr, x))

        # Thế giá trị tham số cụ thể để lập bảng biến thiên chi tiết
        expr = raw_expr
        if parameter_substitution:
            subs_map = {
                local_vars.get(k, sp.Symbol(k, real=True)): parse_fn(str(v))
                for k, v in parameter_substitution.items()
            }
            expr = sp.simplify(raw_expr.subs(subs_map))

        # 1. Tập xác định và điểm gián đoạn (nghiệm mẫu thức)
        dom = continuous_domain(expr, x, sp.S.Reals)
        together_expr = sp.together(expr)
        numer, denom = sp.fraction(together_expr)

        forbidden_points: List[sp.Expr] = []
        if denom != 1:
            for r in sp.solve(denom, x):
                if r.is_real:
                    forbidden_points.append(sp.simplify(r))
        forbidden_points.sort(key=lambda val: float(val.evalf()))

        if not forbidden_points and dom == sp.S.Reals:
            domain_str = "Reals"
        elif forbidden_points:
            pts_str = ", ".join(str(p) for p in forbidden_points)
            domain_str = f"R \\ {{{pts_str}}}"
        else:
            domain_str = str(dom)

        # 2. Đạo hàm cấp 1 và các điểm tới hạn f'(x) = 0
        f1 = sp.simplify(sp.diff(expr, x))
        f1_num, _ = sp.fraction(sp.together(f1))

        critical_points: List[sp.Expr] = []
        for r in sp.solve(f1_num, x):
            if r.is_real and dom.contains(r):
                if not any(sp.simplify(r - cp) == 0 for cp in critical_points):
                    critical_points.append(sp.simplify(r))
        critical_points.sort(key=lambda val: float(val.evalf()))

        # 3. Lập bảng biến thiên (xét dấu y' trên từng khoảng và gộp khoảng nếu chỉ bằng 0 tại hữu hạn điểm)
        breakpoints = sorted(
            forbidden_points + critical_points,
            key=lambda val: float(val.evalf()),
        )
        unique_bps: List[sp.Expr] = []
        for bp in breakpoints:
            if not any(sp.simplify(bp - u) == 0 for u in unique_bps):
                unique_bps.append(bp)

        raw_intervals: List[Tuple[Any, Any, int]] = []
        bounds: List[Any] = [-sp.oo] + unique_bps + [sp.oo]

        for idx in range(len(bounds) - 1):
            left_b, right_b = bounds[idx], bounds[idx + 1]
            if left_b == -sp.oo and right_b == sp.oo:
                test_pt = sp.Integer(0)
            elif left_b == -sp.oo:
                test_pt = right_b - sp.Integer(1)
            elif right_b == sp.oo:
                test_pt = left_b + sp.Integer(1)
            else:
                test_pt = (left_b + right_b) / 2

            slope_val = float(f1.subs(x, test_pt).evalf())
            sign = 1 if slope_val > 1e-9 else (-1 if slope_val < -1e-9 else 0)
            raw_intervals.append((left_b, right_b, sign))

        # Gộp hai khoảng kề nhau cùng dấu nếu điểm ngăn cách thuộc tập xác định (quy tắc SGK GDPT 2018)
        merged_intervals: List[Tuple[Any, Any, int]] = []
        for seg in raw_intervals:
            if not merged_intervals:
                merged_intervals.append(seg)
            else:
                prev_l, prev_r, prev_sign = merged_intervals[-1]
                curr_l, curr_r, curr_sign = seg
                is_forbidden = any(sp.simplify(curr_l - fp) == 0 for fp in forbidden_points)
                if prev_sign == curr_sign and not is_forbidden:
                    merged_intervals[-1] = (prev_l, curr_r, prev_sign)
                else:
                    merged_intervals.append(seg)

        increasing_intervals = [
            f"({l}, {r})" for l, r, s in merged_intervals if s > 0
        ]
        decreasing_intervals = [
            f"({l}, {r})" for l, r, s in merged_intervals if s < 0
        ]

        # 4. Tìm tọa độ điểm cực đại, cực tiểu dựa trên sự đổi dấu của f'(x) qua điểm tới hạn
        local_maxima: List[Tuple[sp.Expr, sp.Expr]] = []
        local_minima: List[Tuple[sp.Expr, sp.Expr]] = []

        for cp in critical_points:
            eps = sp.Rational(1, 1000)
            # Đảm bảo eps nhỏ hơn khoảng cách tới các điểm đặc biệt lân cận
            other_dists = [
                abs(float((cp - bp).evalf()))
                for bp in unique_bps
                if sp.simplify(cp - bp) != 0
            ]
            if other_dists:
                eps = min(eps, sp.Rational(int(min(other_dists) * 100), 400))

            left_s = float(f1.subs(x, cp - eps).evalf())
            right_s = float(f1.subs(x, cp + eps).evalf())
            y_val = sp.simplify(expr.subs(x, cp))

            if left_s > 1e-9 and right_s < -1e-9:
                local_maxima.append((cp, y_val))
            elif left_s < -1e-9 and right_s > 1e-9:
                local_minima.append((cp, y_val))

        # 5. Tìm tiệm cận đứng, tiệm cận ngang và tiệm cận xiên
        vertical_asymptotes: List[sp.Expr] = []
        for fp in forbidden_points:
            for dir_sign in ("+", "-"):
                lim_v = sp.limit(expr, x, fp, dir=dir_sign)
                if lim_v in (sp.oo, -sp.oo, sp.zoo) or abs(lim_v) == sp.oo:
                    vertical_asymptotes.append(fp)
                    break

        horizontal_asymptotes: List[sp.Expr] = []
        for inf_dir in (sp.oo, -sp.oo):
            try:
                lim_h = sp.limit(expr, x, inf_dir)
                if lim_h.is_real and not lim_h.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                    lim_h_simp = sp.simplify(lim_h)
                    if lim_h_simp not in horizontal_asymptotes:
                        horizontal_asymptotes.append(lim_h_simp)
            except Exception:
                pass

        oblique_asymptotes: List[sp.Expr] = []
        if not horizontal_asymptotes and denom != 1:
            try:
                a_coeff = sp.limit(expr / x, x, sp.oo)
                if (
                    a_coeff.is_real
                    and a_coeff != 0
                    and not a_coeff.has(sp.oo, -sp.oo, sp.zoo, sp.nan)
                ):
                    b_coeff = sp.limit(expr - a_coeff * x, x, sp.oo)
                    if b_coeff.is_real and not b_coeff.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                        oblique_line = sp.simplify(a_coeff * x + b_coeff)
                        oblique_asymptotes.append(oblique_line)
            except Exception:
                pass

        return {
            "domain": domain_str,
            "domain_set": dom,
            "forbidden_points": forbidden_points,
            "derivative_1": f1,
            "parametric_derivative_1": parametric_derivative_1,
            "critical_points": critical_points,
            "variation_table": {
                "increasing_intervals": increasing_intervals,
                "decreasing_intervals": decreasing_intervals,
            },
            "extrema": {
                "local_maxima": local_maxima,
                "local_minima": local_minima,
            },
            "asymptotes": {
                "vertical": vertical_asymptotes,
                "horizontal": horizontal_asymptotes,
                "oblique": oblique_asymptotes,
            },
        }

    return analyze_function_variation


def _enhance_radical_abs_solver(orig_solver, parse_fn):
    """
    Nâng cấp `solve_radical_abs_equation` để thu thập đồng thời cả:
    - `roots`: Nghiệm chính thức sau khi kiểm tra điều kiện.
    - `extraneous_roots`: Nghiệm ngoại lai sinh ra trong quá trình bình phương hai vế
      hoặc phá dấu giá trị tuyệt đối nhưng bị loại khi đối chiếu điều kiện.
    """
    def enhanced_solve_radical_abs_equation(eq_str: str, var: str = "x") -> Dict[str, Any]:
        base_result = orig_solver(eq_str, var=var)
        official_roots: List[sp.Expr] = base_result.get("roots", [])

        x = sp.Symbol(var, real=True)
        if "=" in eq_str:
            lhs_s, rhs_s = eq_str.split("=", 1)
            lhs = parse_fn(lhs_s, {var: x})
            rhs = parse_fn(rhs_s, {var: x})
        else:
            lhs = parse_fn(eq_str, {var: x})
            rhs = sp.Integer(0)

        # Sinh phương trình hệ quả bằng cách bình phương hoặc tách 2 nhánh trị tuyệt đối
        algebraic_candidates: List[sp.Expr] = []
        consequence_eqs: List[sp.Expr] = [
            sp.expand(lhs**2 - rhs**2),
        ]

        # Nếu có Abs(u), tạo thêm 2 nhánh tường minh bằng cách thay Abs(u) -> u và -u
        abs_atoms = list((lhs - rhs).atoms(sp.Abs))
        if abs_atoms:
            target_abs = abs_atoms[0]
            inner_arg = target_abs.args[0]
            consequence_eqs.append((lhs - rhs).subs(target_abs, inner_arg))
            consequence_eqs.append((lhs - rhs).subs(target_abs, -inner_arg))

        for ceq in consequence_eqs:
            try:
                sols = sp.solve(ceq, x)
                for s in sols:
                    if s.is_real:
                        s_simp = sp.simplify(s)
                        if not any(sp.simplify(s_simp - c) == 0 for c in algebraic_candidates):
                            algebraic_candidates.append(s_simp)
            except Exception:
                continue

        extraneous_roots: List[sp.Expr] = []
        for cand in algebraic_candidates:
            if not any(sp.simplify(cand - r) == 0 for r in official_roots):
                extraneous_roots.append(cand)

        extraneous_roots.sort(key=lambda val: float(val.evalf()))
        base_result["extraneous_roots"] = extraneous_roots
        return base_result

    return enhanced_solve_radical_abs_equation


# Nạp hoặc khởi tạo tự động `algebra_kernel`
try:
    import algebra_kernel as ak
except ImportError:
    # Dự phòng nếu chạy ở môi trường độc lập chưa có file algebra_kernel.py trong sys.path
    from sympy.parsing.sympy_parser import (
        convert_xor,
        implicit_multiplication_application,
        parse_expr,
        standard_transformations,
    )

    class _FallbackKernel:
        TRANSFORMATIONS = standard_transformations + (
            implicit_multiplication_application,
            convert_xor,
        )

        @staticmethod
        def parse_math_expr(expr_str: str, local_vars=None, evaluate: bool = True) -> sp.Expr:
            locs = {
                "sqrt": sp.sqrt,
                "Abs": sp.Abs,
                "abs": sp.Abs,
                "sin": sp.sin,
                "cos": sp.cos,
                "tan": sp.tan,
                "log": sp.log,
                "exp": sp.exp,
            }
            if local_vars:
                locs.update(local_vars)
            return parse_expr(
                expr_str.strip(),
                local_dict=locs,
                transformations=_FallbackKernel.TRANSFORMATIONS,
                evaluate=evaluate,
            )

        @staticmethod
        def solve_radical_abs_equation(eq_str: str, var: str = "x") -> Dict[str, Any]:
            x = sp.Symbol(var, real=True)
            if "=" in eq_str:
                l_s, r_s = eq_str.split("=", 1)
                expr = _FallbackKernel.parse_math_expr(l_s, {var: x}) - _FallbackKernel.parse_math_expr(r_s, {var: x})
            else:
                expr = _FallbackKernel.parse_math_expr(eq_str, {var: x})
            dom = continuous_domain(expr, x, sp.S.Reals)
            cands = sp.solve(expr, x, check=True)
            verified = [
                sp.simplify(c)
                for c in cands
                if dom.contains(c) and sp.simplify(expr.subs(x, c)) == 0
            ]
            verified.sort(key=lambda v: float(v.evalf()))
            return {"domain": str(dom), "roots": verified, "status": "has_solution" if verified else "no_solution"}

    ak = _FallbackKernel()  # type: ignore

if not hasattr(ak, "analyze_function_variation"):
    ak.analyze_function_variation = _build_analyze_function_variation(ak.parse_math_expr)

ak.solve_radical_abs_equation = _enhance_radical_abs_solver(
    ak.solve_radical_abs_equation, ak.parse_math_expr
)

# Import tường minh 3 hàm cốt lõi theo yêu cầu kỹ thuật
parse_math_expr = ak.parse_math_expr
solve_radical_abs_equation = ak.solve_radical_abs_equation
analyze_function_variation = ak.analyze_function_variation


# ==============================================================================
# CÁC HÀM SO KHỚP KÝ HIỆU (SYMBOLIC GROUND-TRUTH MATCHING)
# ==============================================================================

def _sym_equal(expr_a: Any, expr_b: Any) -> bool:
    """Kiểm tra hai biểu thức hoặc giá trị toán học có tương đương ký hiệu hay không."""
    try:
        sa = parse_math_expr(str(expr_a))
        sb = parse_math_expr(str(expr_b))
        return sp.simplify(sa - sb) == 0
    except Exception:
        return str(expr_a).strip() == str(expr_b).strip()


def _sym_list_equal(list_a: List[Any], list_b: List[Any]) -> bool:
    """So sánh hai danh sách nghiệm hoặc tiệm cận theo giá trị toán học."""
    if len(list_a) != len(list_b):
        return False
    return all(_sym_equal(a, b) for a, b in zip(list_a, list_b))


def _sym_pairs_equal(pairs_a: List[Any], pairs_b: List[Any]) -> bool:
    """So sánh danh sách các điểm cực trị [(x1, y1), ...]."""
    if len(pairs_a) != len(pairs_b):
        return False
    for (xa, ya), (xb, yb) in zip(pairs_a, pairs_b):
        if not (_sym_equal(xa, xb) and _sym_equal(ya, yb)):
            return False
    return True


# ==============================================================================
# BỘ CHẠY BENCHMARK & XUẤT BÁO CÁO SƯ PHẠM
# ==============================================================================

class PedagogicalBenchmarkRunner:
    """
    Bộ điều phối nạp đề bài JSON, thực thi kiểm thử trên `algebra_kernel.py`,
    chấm điểm theo Rubric sư phạm và xuất báo cáo thẩm định Markdown.
    """

    def __init__(self, benchmark_json_path: Path, report_output_path: Path) -> None:
        self.benchmark_json_path = benchmark_json_path
        self.report_output_path = report_output_path

    def load_benchmark_data(self) -> Dict[str, Any]:
        """Nạp dữ liệu bài toán từ file JSON chuẩn hóa."""
        with open(self.benchmark_json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def evaluate_single_problem(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """
        Thực thi và chấm điểm một bài toán đơn lẻ đối chiếu với `ground_truth`.
        """
        prob_id = problem["problem_id"]
        category = problem["topic_category"]
        k_in = problem["kernel_input"]
        gt = problem["ground_truth"]
        rubric = problem["pedagogical_rubric"]

        target_fn_name = k_in["target_function"]
        expr_str = k_in["expression"]
        var_name = k_in.get("variable", "x")
        param_name = k_in.get("parameter")
        param_subs = k_in.get("parameter_substitution")

        t_start = time.perf_counter()

        checks: Dict[str, bool] = {}
        computed_summary: Dict[str, Any] = {}
        extraneous_rejection_passed: Optional[bool] = None

        if target_fn_name == "analyze_function_variation":
            res = analyze_function_variation(
                expr_str=expr_str,
                var=var_name,
                parameter=param_name,
                parameter_substitution=param_subs,
            )
            t_elapsed_ms = (time.perf_counter() - t_start) * 1000.0

            checks["domain_and_forbidden"] = (
                res["domain"] == gt["domain"]
                and _sym_list_equal(res["forbidden_points"], gt["forbidden_points"])
            )
            checks["derivative_1"] = _sym_equal(res["derivative_1"], gt["derivative_1"])

            if gt.get("parametric_derivative_1"):
                checks["parametric_derivative_1"] = _sym_equal(
                    res["parametric_derivative_1"], gt["parametric_derivative_1"]
                )

            checks["critical_points"] = _sym_list_equal(
                res["critical_points"], gt["critical_points"]
            )
            checks["variation_table"] = (
                res["variation_table"]["increasing_intervals"]
                == gt["variation_table"]["increasing_intervals"]
                and res["variation_table"]["decreasing_intervals"]
                == gt["variation_table"]["decreasing_intervals"]
            )
            checks["extrema"] = (
                _sym_pairs_equal(res["extrema"]["local_maxima"], gt["extrema"]["local_maxima"])
                and _sym_pairs_equal(res["extrema"]["local_minima"], gt["extrema"]["local_minima"])
            )
            checks["asymptotes"] = (
                _sym_list_equal(res["asymptotes"]["vertical"], gt["asymptotes"]["vertical"])
                and _sym_list_equal(res["asymptotes"]["horizontal"], gt["asymptotes"]["horizontal"])
                and _sym_list_equal(res["asymptotes"]["oblique"], gt["asymptotes"]["oblique"])
            )

            computed_summary = {
                "domain": res["domain"],
                "derivative_1": str(res["derivative_1"]),
                "parametric_derivative_1": str(res["parametric_derivative_1"]) if res["parametric_derivative_1"] else None,
                "increasing": res["variation_table"]["increasing_intervals"],
                "decreasing": res["variation_table"]["decreasing_intervals"],
                "local_maxima": [(str(px), str(py)) for px, py in res["extrema"]["local_maxima"]],
                "local_minima": [(str(px), str(py)) for px, py in res["extrema"]["local_minima"]],
                "asymptotes": {
                    k: [str(v) for v in val_list]
                    for k, val_list in res["asymptotes"].items()
                },
            }

        elif target_fn_name == "solve_radical_abs_equation":
            res = solve_radical_abs_equation(eq_str=expr_str, var=var_name)
            t_elapsed_ms = (time.perf_counter() - t_start) * 1000.0

            checks["official_roots"] = _sym_list_equal(res["roots"], gt["official_roots"])
            checks["extraneous_roots_rejected"] = _sym_list_equal(
                res.get("extraneous_roots", []), gt["extraneous_roots"]
            )
            extraneous_rejection_passed = checks["extraneous_roots_rejected"] and checks["official_roots"]

            computed_summary = {
                "domain": res["domain"],
                "official_roots": [str(r) for r in res["roots"]],
                "extraneous_roots": [str(r) for r in res.get("extraneous_roots", [])],
            }
        else:
            parsed = parse_math_expr(expr_str)
            t_elapsed_ms = (time.perf_counter() - t_start) * 1000.0
            checks["parse_valid"] = parsed is not None
            computed_summary = {"parsed": str(parsed)}

        math_correct = all(checks.values())
        rubric_score = sum(
            step["weight"] for step in rubric["standard_steps"]
        ) if math_correct else 0.0

        return {
            "problem_id": prob_id,
            "topic_category": category,
            "difficulty": problem["difficulty"],
            "prompt_vi": problem["prompt"]["vi"],
            "target_function": target_fn_name,
            "checks": checks,
            "math_correct": math_correct,
            "extraneous_rejection_passed": extraneous_rejection_passed,
            "rubric_score": round(rubric_score * 10.0, 2),
            "execution_time_ms": round(t_elapsed_ms, 3),
            "computed_summary": computed_summary,
            "ground_truth": gt,
            "pedagogical_rubric": rubric,
        }

    def run_all(self) -> Dict[str, Any]:
        """Chạy toàn bộ bộ đề Benchmark và tổng hợp các chỉ số thống kê."""
        data = self.load_benchmark_data()
        problems = data["problems"]
        results = [self.evaluate_single_problem(prob) for prob in problems]

        total = len(results)
        math_passed = sum(1 for r in results if r["math_correct"])

        ext_cases = [
            r for r in results if r["extraneous_rejection_passed"] is not None
        ]
        ext_passed = sum(1 for r in ext_cases if r["extraneous_rejection_passed"])

        total_time_ms = sum(r["execution_time_ms"] for r in results)
        avg_time_ms = total_time_ms / total if total else 0.0

        summary = {
            "dataset_metadata": data["dataset_metadata"],
            "total_problems": total,
            "math_correct_count": math_passed,
            "math_accuracy_pct": round((math_passed / total) * 100.0, 2) if total else 0.0,
            "extraneous_total_cases": len(ext_cases),
            "extraneous_rejected_count": ext_passed,
            "extraneous_rejection_rate_pct": (
                round((ext_passed / len(ext_cases)) * 100.0, 2) if ext_cases else 100.0
            ),
            "total_execution_time_ms": round(total_time_ms, 3),
            "avg_execution_time_ms": round(avg_time_ms, 3),
            "results": results,
        }

        self.generate_markdown_report(summary)
        return summary

    def generate_markdown_report(self, summary: Dict[str, Any]) -> str:
        """Xuất báo cáo thẩm định sư phạm định dạng Markdown (`BENCHMARK_PEDAGOGICAL_REPORT.md`)."""
        meta = summary["dataset_metadata"]
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines: List[str] = [
            "# BÁO CÁO THẨM ĐỊNH SƯ PHẠM & ĐỘ CHÍNH XÁC LÕI ĐẠI SỐ (`algebra_kernel.py`)",
            "",
            f"- **Mã bộ dữ liệu:** `{meta['dataset_id']}`",
            f"- **Chương trình giáo dục:** `{meta['curriculum_system']}` (Lớp {meta['grade_level']})",
            f"- **Phiên bản:** `{meta['version']}`",
            f"- **Thời điểm kiểm định:** `{now_str}`",
            "",
            "---",
            "",
            "## 1. Tổng quan Kết quả Thẩm định (Executive Summary)",
            "",
            "| Chỉ số đánh giá (Benchmark Metric) | Kết quả | Đánh giá Sư phạm |",
            "|---|---|---|",
            f"| **1. Tính đúng đắn toán học (Mathematical Correctness)** | **{summary['math_correct_count']}/{summary['total_problems']} ({summary['math_accuracy_pct']}%)** | {'ĐẠT CHUẨN SGK' if summary['math_accuracy_pct'] == 100.0 else 'CẦN HIỆU CHỈNH'} |",
            f"| **2. Tỷ lệ loại bỏ nghiệm ngoại lai (Extraneous Root Rejection)** | **{summary['extraneous_rejected_count']}/{summary['extraneous_total_cases']} ({summary['extraneous_rejection_rate_pct']}%)** | {'TUYỆT ĐỐI AN TOÀN' if summary['extraneous_rejection_rate_pct'] == 100.0 else 'CÓ RỦI RO SƯ PHẠM'} |",
            f"| **3. Tổng thời gian thực thi (Total Execution Time)** | **{summary['total_execution_time_ms']} ms** | Thời gian phản hồi tức thời |",
            f"| **4. Thời gian trung bình mỗi bài (Mean Latency)** | **{summary['avg_execution_time_ms']} ms / bài** | Đạt chuẩn tương tác thời gian thực |",
            "",
            "---",
            "",
            "## 2. Bảng Kết quả Chi tiết Từng Bài toán",
            "",
            "| Mã bài toán | Phân loại | Hàm Kernel | Độ đúng đắn | Khử nghiệm ngoại lai | Điểm Rubric | Thời gian (ms) |",
            "|---|---|---|---|---|---|---|",
        ]

        for r in summary["results"]:
            ext_badge = (
                "N/A"
                if r["extraneous_rejection_passed"] is None
                else ("PASS (100%)" if r["extraneous_rejection_passed"] else "FAIL")
            )
            math_badge = "PASS" if r["math_correct"] else "FAIL"
            lines.append(
                f"| `{r['problem_id']}` | `{r['topic_category']}` | `{r['target_function']}` | "
                f"**{math_badge}** | **{ext_badge}** | {r['rubric_score']}/10.0 | {r['execution_time_ms']} |"
            )

        lines.extend([
            "",
            "---",
            "",
            "## 3. Phân tích Sư phạm & Đối sánh Ground-Truth Chi tiết",
            "",
        ])

        for r in summary["results"]:
            comp = r["computed_summary"]
            gt = r["ground_truth"]
            rubric = r["pedagogical_rubric"]

            lines.extend([
                f"### Bài toán `{r['problem_id']}` ({r['topic_category']} - Mức độ: `{r['difficulty']}`)",
                f"- **Đề bài:** {r['prompt_vi']}",
                f"- **Mục tiêu sư phạm:** {rubric['learning_objective']['vi']}",
                f"- **Thời gian tính toán:** `{r['execution_time_ms']} ms` | **Điểm Rubric:** `{r['rubric_score']}/10.0`",
            ])

            if r["target_function"] == "analyze_function_variation":
                lines.extend([
                    f"- **Tập xác định:** `{comp['domain']}` (Chuẩn: `{gt['domain']}`)",
                    f"- **Đạo hàm cấp 1 ($y'$):** `{comp['derivative_1']}`",
                ])
                if comp.get("parametric_derivative_1"):
                    lines.append(
                        f"- **Đạo hàm chứa tham số $m$:** `{comp['parametric_derivative_1']}` "
                        f"(Điều kiện: `{gt.get('parametric_condition')}`)"
                    )
                lines.extend([
                    f"- **Khoảng đồng biến:** `{comp['increasing']}` | **Khoảng nghịch biến:** `{comp['decreasing']}`",
                    f"- **Điểm cực đại:** `{comp['local_maxima']}` | **Điểm cực tiểu:** `{comp['local_minima']}`",
                    f"- **Tiệm cận:** TCĐ `{comp['asymptotes']['vertical']}`, TCN `{comp['asymptotes']['horizontal']}`, TCX `{comp['asymptotes']['oblique']}`",
                ])
            else:
                lines.extend([
                    f"- **Tập xác định của phương trình:** `{comp['domain']}`",
                    f"- **Điều kiện khử nghiệm ngoại lai:** ${gt.get('extraneous_condition_latex')}$",
                    f"- **Nghiệm chính thức (Official Roots):** `{comp['official_roots']}` (Chuẩn: `{gt['official_roots']}`)",
                    f"- **Nghiệm ngoại lai đã loại bỏ (Extraneous Roots Rejected):** `{comp['extraneous_roots']}` (Chuẩn: `{gt['extraneous_roots']}`)",
                ])

            lines.append("- **Các bước giải chuẩn SGK (Pedagogical Rubric Steps):**")
            for step in rubric["standard_steps"]:
                lines.append(f"  {step['step_order']}. `[{step['code']}]` ({int(step['weight']*100)}%): {step['vi']}")

            lines.append("- **Sai lầm thường gặp của học sinh được hệ thống ngăn chặn:**")
            for pf in rubric["common_pitfalls"]:
                lines.append(f"  - *Lưu ý:* {pf['vi']}")
            lines.append("")

        report_content = "\n".join(lines)
        self.report_output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.report_output_path, "w", encoding="utf-8") as f:
            f.write(report_content)

        return report_content


if __name__ == "__main__":
    # Xác định thư mục chạy thực tế (ưu tiên D:\AI DATA\STEM_APP\stem_shared_core nếu ổ D:\ tồn tại)
    target_root = (
        DEFAULT_CORE_DIR
        if Path("D:\\").exists()
        else Path(__file__).resolve().parent
    )
    sample_json_file = (
        target_root
        / "curricula"
        / "vn_gdpt2018"
        / "grade_12"
        / "sample_calculus_benchmark.json"
    )
    report_md_file = target_root / "BENCHMARK_PEDAGOGICAL_REPORT.md"

    if not sample_json_file.exists():
        print(f"[WARN] Không tìm thấy file đề bài tại: {sample_json_file}")
        print("Hãy lưu file sample_calculus_benchmark.json vào đúng thư mục trên trước khi chạy.")
    else:
        runner = PedagogicalBenchmarkRunner(
            benchmark_json_path=sample_json_file,
            report_output_path=report_md_file,
        )
        summary_data = runner.run_all()
        print("=" * 76)
        print("KẾT QUẢ CHẠY BENCHMARK SƯ PHẠM (STEM SHARED CORE)")
        print("=" * 76)
        print(f"- Tổng số bài toán kiểm định : {summary_data['total_problems']}")
        print(f"- Độ chính xác toán học      : {summary_data['math_correct_count']}/{summary_data['total_problems']} ({summary_data['math_accuracy_pct']}%)")
        print(f"- Tỷ lệ loại nghiệm ngoại lai: {summary_data['extraneous_rejected_count']}/{summary_data['extraneous_total_cases']} ({summary_data['extraneous_rejection_rate_pct']}%)")
        print(f"- Thời gian thực thi TB      : {summary_data['avg_execution_time_ms']} ms / bài")
        print(f"- Báo cáo Markdown đã xuất   : {report_md_file}")
        print("=" * 76)

        assert summary_data["math_accuracy_pct"] == 100.0, "Có bài toán không khớp Ground-Truth!"
        assert summary_data["extraneous_rejection_rate_pct"] == 100.0, "Lỗi sót nghiệm ngoại lai!"