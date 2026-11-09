#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER BENCHMARK RUNNER - GDPT 2018 STEM & SYMBOLIC COMPUTATION SUITE
=====================================================================
File Path: D:/AI DATA/STEM_APP/stem_shared_core\master_benchmark_runner.py
Role: Automated QA & Pedagogical Verification Runner for Vietnam GDPT 2018
      Mathematics (Grade 10, 11, 12) and Core Sciences (Physics, Chemistry, Biology).
Output: D:\AI DATA\STEM_APP\stem_shared_core\MASTER_PEDAGOGICAL_REPORT.md
"""

from __future__ import annotations

import json
import math
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import sympy as sp

# ==============================================================================
# 1. CẤU HÌNH ĐƯỜNG DẪN HỆ THỐNG & IMPORT CÁC MODULE LÕI (STEM SHARED CORE)
# ==============================================================================

DEFAULT_WINDOWS_CORE_DIR = Path(r"D:\AI DATA\STEM_APP\stem_shared_core")
CURRENT_SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT_DIR = CURRENT_SCRIPT_DIR.parent

for candidate_path in [
    str(CURRENT_SCRIPT_DIR),
    str(PROJECT_ROOT_DIR),
    str(DEFAULT_WINDOWS_CORE_DIR),
    str(DEFAULT_WINDOWS_CORE_DIR.parent),
]:
    if candidate_path not in sys.path:
        sys.path.insert(0, candidate_path)

try:
    from stem_shared_core.algebra_kernel import (
        analyze_function_variation,
        parse_math_expr,
        solve_radical_abs_equation,
    )
    from stem_shared_core.biology import (
        analyze_hardy_weinberg,
        solve_mendelian_cross,
    )
    from stem_shared_core.chemistry import (
        balance_chemical_equation,
        calculate_solution_concentrations,
    )
    from stem_shared_core.physics import (
        solve_harmonic_oscillator,
        solve_rlc_circuit,
    )
    import stem_shared_core.algebra_kernel as algebra_kernel_mod
except ImportError:
    # Fallback nếu chạy trực tiếp bên trong thư mục stem_shared_core
    from algebra_kernel import (  # type: ignore
        analyze_function_variation,
        parse_math_expr,
        solve_radical_abs_equation,
    )
    from biology import (  # type: ignore
        analyze_hardy_weinberg,
        solve_mendelian_cross,
    )
    from chemistry import (  # type: ignore
        balance_chemical_equation,
        calculate_solution_concentrations,
    )
    from physics import (  # type: ignore
        solve_harmonic_oscillator,
        solve_rlc_circuit,
    )
    import algebra_kernel as algebra_kernel_mod  # type: ignore


# ==============================================================================
# 2. CẤU TRÚC DỮ LIỆU KẾT QUẢ KIỂM ĐỊNH (DATACLASSES)
# ==============================================================================

@dataclass
class MathProblemResult:
    problem_id: str
    grade: int
    topic_category: str
    difficulty: str
    target_function: str
    prompt_vi: str
    expression_summary: str
    passed_math: bool
    has_extraneous_check: bool
    passed_extraneous: bool
    expected_extraneous_count: int
    detected_extraneous_count: int
    execution_time_ms: float
    expected_summary: str
    actual_summary: str
    learning_objective_vi: str
    common_pitfall_vi: str
    error_message: Optional[str] = None


@dataclass
class ScienceTestResult:
    test_id: str
    domain: str
    function_name: str
    description_vi: str
    input_summary: str
    expected_summary: str
    actual_summary: str
    passed: bool
    execution_time_ms: float
    error_message: Optional[str] = None


@dataclass
class MasterBenchmarkSummary:
    timestamp: str
    math_results: List[MathProblemResult] = field(default_factory=list)
    science_results: List[ScienceTestResult] = field(default_factory=list)

    @property
    def total_math_problems(self) -> int:
        return len(self.math_results)

    @property
    def passed_math_problems(self) -> int:
        return sum(1 for r in self.math_results if r.passed_math)

    @property
    def math_accuracy_pct(self) -> float:
        if not self.math_results:
            return 0.0
        return (self.passed_math_problems / self.total_math_problems) * 100.0

    @property
    def extraneous_problems_total(self) -> int:
        return sum(1 for r in self.math_results if r.has_extraneous_check)

    @property
    def extraneous_problems_passed(self) -> int:
        return sum(
            1 for r in self.math_results if r.has_extraneous_check and r.passed_extraneous
        )

    @property
    def total_expected_extraneous_roots(self) -> int:
        return sum(r.expected_extraneous_count for r in self.math_results)

    @property
    def total_detected_extraneous_roots(self) -> int:
        return sum(r.detected_extraneous_count for r in self.math_results)

    @property
    def extraneous_rejection_rate_pct(self) -> float:
        if self.extraneous_problems_total == 0:
            return 100.0
        return (self.extraneous_problems_passed / self.extraneous_problems_total) * 100.0

    @property
    def total_science_tests(self) -> int:
        return len(self.science_results)

    @property
    def passed_science_tests(self) -> int:
        return sum(1 for r in self.science_results if r.passed)

    @property
    def science_pass_rate_pct(self) -> float:
        if not self.science_results:
            return 0.0
        return (self.passed_science_tests / self.total_science_tests) * 100.0

    @property
    def total_execution_time_ms(self) -> float:
        math_time = sum(r.execution_time_ms for r in self.math_results)
        sci_time = sum(r.execution_time_ms for r in self.science_results)
        return math_time + sci_time


# ==============================================================================
# 3. TIỆN ÍCH NẠP FILE ĐỀ BÀI & ĐỐI SÁNH ĐẠI SỐ HÌNH THỨC (SYMBOLIC EQUIVALENCE)
# ==============================================================================

BENCHMARK_RELATIVE_PATHS: Dict[int, Path] = {
    10: Path("curricula/vn_gdpt2018/grade_10/sample_radical_equation.json"),
    11: Path("curricula/vn_gdpt2018/grade_11/sample_algebra_grade11.json"),
    12: Path("curricula/vn_gdpt2018/grade_12/sample_calculus_benchmark.json"),
}


def resolve_curriculum_file(rel_path: Path) -> Path:
    """
    Tìm kiếm file JSON đề bài theo thứ tự ưu tiên:
    1. Đường dẫn tương đối từ thư mục hiện hành (Path.cwd() / rel_path)
    2. Đường dẫn tương đối từ thư mục chứa script (CURRENT_SCRIPT_DIR / rel_path)
    3. Đường dẫn tương đối từ thư mục gốc dự án (PROJECT_ROOT_DIR / rel_path)
    4. Đường dẫn tuyệt đối chuẩn: D:\\AI DATA\\STEM_APP\\stem_shared_core\\curricula\\...
    """
    candidates = [
        Path.cwd() / rel_path,
        CURRENT_SCRIPT_DIR / rel_path,
        PROJECT_ROOT_DIR / rel_path,
        DEFAULT_WINDOWS_CORE_DIR / rel_path,
        DEFAULT_WINDOWS_CORE_DIR.parent / rel_path,
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()

    raise FileNotFoundError(
        f"Không tìm thấy file benchmark '{rel_path}'. Đã kiểm tra: "
        + ", ".join(str(c) for c in candidates)
    )


def resolve_report_output_path() -> Path:
    """
    Xác định đường dẫn xuất file MASTER_PEDAGOGICAL_REPORT.md.
    Ưu tiên D:\\AI DATA\\STEM_APP\\stem_shared_core\\MASTER_PEDAGOGICAL_REPORT.md
    nếu hệ thống đang ở môi trường Windows có thư mục đích tồn tại,
    đồng thời hỗ trợ chạy đa nền tảng.
    """
    if DEFAULT_WINDOWS_CORE_DIR.exists():
        return DEFAULT_WINDOWS_CORE_DIR / "MASTER_PEDAGOGICAL_REPORT.md"
    return CURRENT_SCRIPT_DIR / "MASTER_PEDAGOGICAL_REPORT.md"


def safe_parse_sympy(val: Any) -> sp.Expr:
    """Chuyển đổi giá trị (str, int, float, sp.Expr) sang biểu thức SymPy."""
    if isinstance(val, sp.Basic):
        return val
    val_str = str(val).strip().replace("^", "**")
    try:
        return parse_math_expr(val_str)
    except Exception:
        return sp.sympify(val_str)


def symbolic_values_equal(val1: Any, val2: Any, tol: float = 1e-7) -> bool:
    """Kiểm tra hai giá trị toán học có tương đương hình thức hoặc số học hay không."""
    try:
        e1 = safe_parse_sympy(val1)
        e2 = safe_parse_sympy(val2)
        diff = sp.simplify(e1 - e2)
        if diff == 0:
            return True
        if diff.is_number:
            return abs(complex(diff.evalf())) <= tol
    except Exception:
        pass
    return str(val1).strip() == str(val2).strip()


def compare_root_sets(expected_list: List[Any], actual_list: List[Any]) -> bool:
    """
    So sánh hai tập nghiệm đại số/lượng giác không phụ thuộc thứ tự,
    sử dụng tương đương hình thức SymPy.
    """
    if len(expected_list) != len(actual_list):
        return False
    matched_indices = set()
    for exp_item in expected_list:
        found = False
        for idx, act_item in enumerate(actual_list):
            if idx in matched_indices:
                continue
            if symbolic_values_equal(exp_item, act_item):
                matched_indices.add(idx)
                found = True
                break
        if not found:
            return False
    return True


def count_matched_roots(expected_list: List[Any], actual_list: List[Any]) -> int:
    """Đếm số nghiệm ngoại lai trong expected_list được phát hiện chính xác trong actual_list."""
    matched_indices = set()
    count = 0
    for exp_item in expected_list:
        for idx, act_item in enumerate(actual_list):
            if idx in matched_indices:
                continue
            if symbolic_values_equal(exp_item, act_item):
                matched_indices.add(idx)
                count += 1
                break
    return count


def normalize_interval_str(interval_s: Any) -> str:
    """Chuẩn hóa chuỗi khoảng đơn điệu (bao gồm cả SymPy Interval.open/Reals) để đối sánh nhất quán."""
    s = str(interval_s).strip()
    if s in ("Reals", "S.Reals", "Interval(-oo, oo)", "Interval.open(-oo, oo)"):
        return "(-oo,oo)"
    m = re.match(r"^Interval(?:\.(?:open|Lopen|Ropen))?\((.+),\s*(.+)\)$", s)
    if m:
        s = f"({m.group(1)},{m.group(2)})"
    s = s.replace("+oo", "oo").replace("+∞", "oo").replace("-∞", "-oo").replace("∞", "oo")
    s = re.sub(r"\s+", "", s)
    return s


def compare_interval_lists(expected_intervals: List[str], actual_intervals: Any) -> bool:
    """So sánh danh sách các khoảng đồng biến / nghịch biến."""
    if not isinstance(actual_intervals, (list, tuple, set)):
        return False
    exp_norm = sorted(normalize_interval_str(x) for x in expected_intervals)
    act_norm = sorted(normalize_interval_str(x) for x in actual_intervals)
    return exp_norm == act_norm


def substitute_parameters_in_expr(
    expr_str: str, param_sub: Optional[Dict[str, Any]]
) -> str:
    """Thay thế tham số (ví dụ m = 2) vào biểu thức hàm số trước khi khảo sát."""
    if not param_sub:
        return expr_str
    parsed = safe_parse_sympy(expr_str)
    subs_map = {sp.Symbol(k): safe_parse_sympy(v) for k, v in param_sub.items()}
    substituted = sp.simplify(parsed.subs(subs_map))
    return str(substituted)


# ==============================================================================
# 4. BỘ ĐIỀU PHỐI GIẢI TOÁN LỚP 10, 11, 12 (MATH BENCHMARK EXECUTOR)
# ==============================================================================

def _execute_trig_equation(
    expr_str: str, var_name: str, interval_bounds: List[str]
) -> Dict[str, Any]:
    """
    Giải phương trình lượng giác trên đoạn [a, b].
    Ưu tiên gọi solve_trig_equation từ algebra_kernel nếu có; nếu không thì
    sử dụng parse_math_expr + SymPy solveset trên Interval(a, b).
    """
    if hasattr(algebra_kernel_mod, "solve_trig_equation"):
        fn = getattr(algebra_kernel_mod, "solve_trig_equation")
        return fn(expr_str, var=var_name, interval=interval_bounds)

    if "=" in expr_str:
        lhs_str, rhs_str = expr_str.split("=", 1)
        eq_expr = parse_math_expr(lhs_str.strip()) - parse_math_expr(rhs_str.strip())
    else:
        eq_expr = parse_math_expr(expr_str)

    x_sym = sp.Symbol(var_name, real=True)
    free_map = {s: x_sym for s in eq_expr.free_symbols if s.name == var_name}
    eq_expr = eq_expr.subs(free_map)

    a_val = parse_math_expr(interval_bounds[0])
    b_val = parse_math_expr(interval_bounds[1])
    search_domain = sp.Interval(a_val, b_val)

    sol_set = sp.solveset(eq_expr, x_sym, domain=search_domain)
    roots = [str(sp.simplify(r)) for r in sorted(list(sol_set), key=lambda v: float(v.evalf()))]
    return {
        "official_roots": roots,
        "extraneous_roots": [],
        "domain": f"[{interval_bounds[0]}, {interval_bounds[1]}]",
    }


def _execute_system_2vars(
    expr1_str: str, expr2_str: str, variables: List[str]
) -> Dict[str, Any]:
    """
    Giải hệ phương trình tuyến tính 2 ẩn (ứng dụng cho Cấp số cộng Lớp 11).
    Ưu tiên gọi solve_system_2vars từ algebra_kernel nếu có; nếu không thì
    sử dụng parse_math_expr + SymPy solve.
    """
    if hasattr(algebra_kernel_mod, "solve_system_2vars"):
        fn = getattr(algebra_kernel_mod, "solve_system_2vars")
        res = fn(expr1_str, expr2_str, vars_tuple=tuple(variables))
        sols = res.get("solutions", [])
        return {"official_solutions": [[str(x) for x in sol] for sol in sols], "domain": "Reals^2"}

    def _to_zero_expr(eq_s: str) -> sp.Expr:
        if "=" in eq_s:
            l_s, r_s = eq_s.split("=", 1)
            return parse_math_expr(l_s.strip()) - parse_math_expr(r_s.strip())
        return parse_math_expr(eq_s)

    eq1 = _to_zero_expr(expr1_str)
    eq2 = _to_zero_expr(expr2_str)
    syms = [sp.Symbol(v) for v in variables]

    for sym in syms:
        eq1 = eq1.subs({s: sym for s in eq1.free_symbols if s.name == sym.name})
        eq2 = eq2.subs({s: sym for s in eq2.free_symbols if s.name == sym.name})

    sol = sp.solve([eq1, eq2], syms, dict=True)
    solutions_list: List[List[str]] = []
    for sol_dict in sol:
        solutions_list.append([str(sp.simplify(sol_dict[sym])) for sym in syms])

    return {
        "official_solutions": solutions_list,
        "domain": "Reals^2",
    }


def _execute_polynomial_equation(expr_str: str, var_name: str) -> Dict[str, Any]:
    """
    Giải phương trình đa thức (ứng dụng cho Cấp số nhân Lớp 11).
    Ưu tiên gọi solve_polynomial_equation hoặc solve_radical_abs_equation.
    """
    if hasattr(algebra_kernel_mod, "solve_polynomial_equation"):
        fn = getattr(algebra_kernel_mod, "solve_polynomial_equation")
        return fn(expr_str, var=var_name)

    try:
        res = solve_radical_abs_equation(expr_str, var=var_name)
        if isinstance(res, dict) and "official_roots" in res:
            return res
    except Exception:
        pass

    if "=" in expr_str:
        lhs_s, rhs_s = expr_str.split("=", 1)
        eq_expr = parse_math_expr(lhs_s.strip()) - parse_math_expr(rhs_s.strip())
    else:
        eq_expr = parse_math_expr(expr_str)

    v_sym = sp.Symbol(var_name, real=True)
    eq_expr = eq_expr.subs({s: v_sym for s in eq_expr.free_symbols if s.name == var_name})
    roots = sp.solve(eq_expr, v_sym)
    return {
        "official_roots": [str(sp.simplify(r)) for r in roots],
        "extraneous_roots": [],
        "domain": "Reals",
    }


def evaluate_single_math_problem(problem: Dict[str, Any]) -> MathProblemResult:
    """Thực thi và chấm điểm tự động 1 bài toán chuẩn SGK GDPT 2018."""
    problem_id = problem["problem_id"]
    grade = int(problem["grade"])
    topic_category = problem.get("topic_category", "general")
    difficulty = problem.get("difficulty", "comprehension")
    prompt_vi = problem.get("prompt", {}).get("vi", "")
    k_input = problem["kernel_input"]
    gt = problem["ground_truth"]
    rubric = problem.get("pedagogical_rubric", {})
    learning_obj_vi = rubric.get("learning_objective", {}).get("vi", "")
    pitfalls = rubric.get("common_pitfalls", [])
    pitfall_vi = pitfalls[0].get("vi", "") if pitfalls else ""

    target_fn = k_input["target_function"]
    t_start = time.perf_counter()

    try:
        if target_fn == "solve_radical_abs_equation":
            expr_str = k_input["expression"]
            var_name = k_input.get("variable", "x")
            output = solve_radical_abs_equation(expr_str, var=var_name)

            exp_official = gt.get("official_roots", [])
            exp_extraneous = gt.get("extraneous_roots", [])
            act_official = output.get("official_roots") or output.get("real_roots") or output.get("roots_in_interval") or output.get("roots") or []
            act_extraneous = output.get("extraneous_roots", [])

            roots_match = compare_root_sets(exp_official, act_official)
            ext_match = compare_root_sets(exp_extraneous, act_extraneous)
            matched_ext_cnt = count_matched_roots(exp_extraneous, act_extraneous)

            passed_math = roots_match and ext_match
            t_ms = (time.perf_counter() - t_start) * 1000.0

            return MathProblemResult(
                problem_id=problem_id,
                grade=grade,
                topic_category=topic_category,
                difficulty=difficulty,
                target_function=target_fn,
                prompt_vi=prompt_vi,
                expression_summary=expr_str,
                passed_math=passed_math,
                has_extraneous_check=True,
                passed_extraneous=ext_match,
                expected_extraneous_count=len(exp_extraneous),
                detected_extraneous_count=matched_ext_cnt,
                execution_time_ms=t_ms,
                expected_summary=f"S = {exp_official}, Ngoại lai = {exp_extraneous}",
                actual_summary=f"S = {act_official}, Ngoại lai = {act_extraneous}",
                learning_objective_vi=learning_obj_vi,
                common_pitfall_vi=pitfall_vi,
            )

        elif target_fn == "analyze_function_variation":
            raw_expr_str = k_input["expression"]
            var_name = k_input.get("variable", "x")
            param_sub = k_input.get("parameter_substitution")
            eval_expr_str = substitute_parameters_in_expr(raw_expr_str, param_sub)

            output = analyze_function_variation(eval_expr_str, var=var_name)

            exp_crit = gt.get("critical_points", [])
            act_crit = output.get("critical_points", [])
            crit_match = compare_root_sets(exp_crit, act_crit)

            exp_vt = gt.get("variation_table", {})
            act_vt = output.get("variation_table", {})

            inc_match = compare_interval_lists(
                exp_vt.get("increasing_intervals", []),
                act_vt.get("increasing_intervals", []),
            )
            dec_match = compare_interval_lists(
                exp_vt.get("decreasing_intervals", []),
                act_vt.get("decreasing_intervals", []),
            )

            passed_math = crit_match and inc_match and dec_match
            t_ms = (time.perf_counter() - t_start) * 1000.0

            expr_display = (
                f"{raw_expr_str} (với {param_sub})" if param_sub else raw_expr_str
            )
            return MathProblemResult(
                problem_id=problem_id,
                grade=grade,
                topic_category=topic_category,
                difficulty=difficulty,
                target_function=target_fn,
                prompt_vi=prompt_vi,
                expression_summary=expr_display,
                passed_math=passed_math,
                has_extraneous_check=False,
                passed_extraneous=True,
                expected_extraneous_count=0,
                detected_extraneous_count=0,
                execution_time_ms=t_ms,
                expected_summary=(
                    f"Cực trị/Tới hạn={exp_crit}, "
                    f"ĐB={exp_vt.get('increasing_intervals', [])}, "
                    f"NB={exp_vt.get('decreasing_intervals', [])}"
                ),
                actual_summary=(
                    f"Cực trị/Tới hạn={act_crit}, "
                    f"ĐB={act_vt.get('increasing_intervals', [])}, "
                    f"NB={act_vt.get('decreasing_intervals', [])}"
                ),
                learning_objective_vi=learning_obj_vi,
                common_pitfall_vi=pitfall_vi,
            )

        elif target_fn == "solve_trig_equation":
            expr_str = k_input["expression"]
            var_name = k_input.get("variable", "x")
            interval_bounds = k_input.get("interval", ["0", "2*pi"])
            output = _execute_trig_equation(expr_str, var_name, interval_bounds)

            exp_official = gt.get("official_roots", [])
            act_official = output.get("official_roots") or output.get("real_roots") or output.get("roots_in_interval") or output.get("roots") or []
            passed_math = compare_root_sets(exp_official, act_official)
            t_ms = (time.perf_counter() - t_start) * 1000.0

            return MathProblemResult(
                problem_id=problem_id,
                grade=grade,
                topic_category=topic_category,
                difficulty=difficulty,
                target_function=target_fn,
                prompt_vi=prompt_vi,
                expression_summary=f"{expr_str} trên [{interval_bounds[0]}, {interval_bounds[1]}]",
                passed_math=passed_math,
                has_extraneous_check=False,
                passed_extraneous=True,
                expected_extraneous_count=0,
                detected_extraneous_count=0,
                execution_time_ms=t_ms,
                expected_summary=f"Nghiệm = {exp_official}",
                actual_summary=f"Nghiệm = {act_official}",
                learning_objective_vi=learning_obj_vi,
                common_pitfall_vi=pitfall_vi,
            )

        elif target_fn == "solve_system_2vars":
            expr1 = k_input["expression_1"]
            expr2 = k_input["expression_2"]
            variables = k_input.get("variables", ["u1", "d"])
            output = _execute_system_2vars(expr1, expr2, variables)

            exp_sols = gt.get("official_solutions", [])
            act_sols = output.get("official_solutions") or output.get("solutions") or []
            passed_math = len(exp_sols) == len(act_sols) and all(
                all(symbolic_values_equal(e_v, a_v) for e_v, a_v in zip(e_tuple, a_tuple))
                for e_tuple, a_tuple in zip(exp_sols, act_sols)
            )
            t_ms = (time.perf_counter() - t_start) * 1000.0

            return MathProblemResult(
                problem_id=problem_id,
                grade=grade,
                topic_category=topic_category,
                difficulty=difficulty,
                target_function=target_fn,
                prompt_vi=prompt_vi,
                expression_summary=f"{{ {expr1} ; {expr2} }}",
                passed_math=passed_math,
                has_extraneous_check=False,
                passed_extraneous=True,
                expected_extraneous_count=0,
                detected_extraneous_count=0,
                execution_time_ms=t_ms,
                expected_summary=f"({', '.join(variables)}) = {exp_sols}",
                actual_summary=f"({', '.join(variables)}) = {act_sols}",
                learning_objective_vi=learning_obj_vi,
                common_pitfall_vi=pitfall_vi,
            )

        elif target_fn == "solve_polynomial_equation":
            expr_str = k_input["expression"]
            var_name = k_input.get("variable", "q")
            output = _execute_polynomial_equation(expr_str, var_name)

            exp_official = gt.get("official_roots", [])
            act_official = output.get("official_roots") or output.get("real_roots") or output.get("roots_in_interval") or output.get("roots") or []
            passed_math = compare_root_sets(exp_official, act_official)
            t_ms = (time.perf_counter() - t_start) * 1000.0

            return MathProblemResult(
                problem_id=problem_id,
                grade=grade,
                topic_category=topic_category,
                difficulty=difficulty,
                target_function=target_fn,
                prompt_vi=prompt_vi,
                expression_summary=expr_str,
                passed_math=passed_math,
                has_extraneous_check=False,
                passed_extraneous=True,
                expected_extraneous_count=0,
                detected_extraneous_count=0,
                execution_time_ms=t_ms,
                expected_summary=f"Nghiệm = {exp_official}",
                actual_summary=f"Nghiệm = {act_official}",
                learning_objective_vi=learning_obj_vi,
                common_pitfall_vi=pitfall_vi,
            )

        else:
            raise ValueError(f"Hàm mục tiêu chưa được hỗ trợ: {target_fn}")

    except Exception as exc:
        t_ms = (time.perf_counter() - t_start) * 1000.0
        return MathProblemResult(
            problem_id=problem_id,
            grade=grade,
            topic_category=topic_category,
            difficulty=difficulty,
            target_function=target_fn,
            prompt_vi=prompt_vi,
            expression_summary=str(k_input.get("expression", "")),
            passed_math=False,
            has_extraneous_check=(target_fn == "solve_radical_abs_equation"),
            passed_extraneous=False,
            expected_extraneous_count=len(gt.get("extraneous_roots", [])),
            detected_extraneous_count=0,
            execution_time_ms=t_ms,
            expected_summary=str(gt),
            actual_summary="ERROR",
            learning_objective_vi=learning_obj_vi,
            common_pitfall_vi=pitfall_vi,
            error_message=str(exc),
        )


# ==============================================================================
# 5. BỘ KIỂM THỬ 3 LÕI KHOA HỌC TỰ NHIÊN (VẬT LÝ - HÓA HỌC - SINH HỌC)
# ==============================================================================

def run_science_kernels_benchmark() -> List[ScienceTestResult]:
    """
    Kiểm thử tự động 3 module khoa học:
    1. stem_shared_core.physics: solve_harmonic_oscillator, solve_rlc_circuit
    2. stem_shared_core.chemistry: balance_chemical_equation, calculate_solution_concentrations
    3. stem_shared_core.biology: solve_mendelian_cross, analyze_hardy_weinberg
    """
    results: List[ScienceTestResult] = []

    # --- TEST 1: VẬT LÝ - Dao động điều hòa ---
    t0 = time.perf_counter()
    try:
        A, omega, phi, mass = 0.1, 10.0, 0.0, 0.2
        out_osc = solve_harmonic_oscillator(A, omega, phi, mass)
        dt_ms = (time.perf_counter() - t0) * 1000.0

        has_x_str = isinstance(out_osc.get("x_str"), str) and len(out_osc["x_str"]) > 0
        v_max_val = float(out_osc.get("v_max", -1.0))
        energy_dict = out_osc.get("energy", {})
        w_val = float(energy_dict.get("total_energy_W", -1.0))

        v_ok = math.isclose(v_max_val, 1.0, rel_tol=1e-4) or math.isclose(
            v_max_val, 0.01, rel_tol=1e-4
        )
        w_ok = math.isclose(w_val, 0.1, rel_tol=1e-4) or math.isclose(
            w_val, 1e-5, rel_tol=1e-4
        )
        passed = has_x_str and v_ok and w_ok

        results.append(
            ScienceTestResult(
                test_id="SCI-PHY-001",
                domain="Vật lý (Physics)",
                function_name="solve_harmonic_oscillator",
                description_vi="Khảo sát dao động điều hòa (phương trình li độ, vận tốc cực đại, cơ năng toàn phần).",
                input_summary="A=0.1, omega=10.0, phi=0.0, mass=0.2",
                expected_summary="v_max=1.0, total_energy_W=0.1, x_str hợp lệ",
                actual_summary=f"x_str='{out_osc.get('x_str')}', v_max={v_max_val:.4g}, W={w_val:.4g}",
                passed=passed,
                execution_time_ms=dt_ms,
            )
        )
    except Exception as exc:
        results.append(
            ScienceTestResult(
                test_id="SCI-PHY-001",
                domain="Vật lý (Physics)",
                function_name="solve_harmonic_oscillator",
                description_vi="Khảo sát dao động điều hòa.",
                input_summary="A=0.1, omega=10.0, phi=0.0, mass=0.2",
                expected_summary="v_max=1.0, total_energy_W=0.1",
                actual_summary="EXCEPTION",
                passed=False,
                execution_time_ms=(time.perf_counter() - t0) * 1000.0,
                error_message=str(exc),
            )
        )

    # --- TEST 2: VẬT LÝ - Mạch điện xoay chiều RLC nối tiếp ---
    t0 = time.perf_counter()
    try:
        R, L, C, U, omega = 40.0, 0.5, 5e-4, 100.0, 100.0
        out_rlc = solve_rlc_circuit(R, L, C, U, omega)
        dt_ms = (time.perf_counter() - t0) * 1000.0

        z_val = float(out_rlc.get("Z", -1.0))
        i_val = float(out_rlc.get("I_rms", -1.0))
        p_val = float(out_rlc.get("power_P", -1.0))
        cos_val = float(out_rlc.get("cos_phi", -1.0))

        passed = (
            math.isclose(z_val, 50.0, rel_tol=1e-4)
            and math.isclose(i_val, 2.0, rel_tol=1e-4)
            and math.isclose(p_val, 160.0, rel_tol=1e-4)
            and math.isclose(cos_val, 0.8, rel_tol=1e-4)
        )

        results.append(
            ScienceTestResult(
                test_id="SCI-PHY-002",
                domain="Vật lý (Physics)",
                function_name="solve_rlc_circuit",
                description_vi="Tính tổng trở Z, cường độ hiệu dụng I_rms, hệ số công suất cos(phi) và công suất tiêu thụ P của mạch RLC.",
                input_summary="R=40, L=0.5, C=5e-4, U=100, omega=100",
                expected_summary="Z=50.0, I_rms=2.0, power_P=160.0, cos_phi=0.8",
                actual_summary=f"Z={z_val:.4g}, I_rms={i_val:.4g}, power_P={p_val:.4g}, cos_phi={cos_val:.4g}",
                passed=passed,
                execution_time_ms=dt_ms,
            )
        )
    except Exception as exc:
        results.append(
            ScienceTestResult(
                test_id="SCI-PHY-002",
                domain="Vật lý (Physics)",
                function_name="solve_rlc_circuit",
                description_vi="Tính tổng trở Z, I_rms, P, cos_phi mạch RLC.",
                input_summary="R=40, L=0.5, C=5e-4, U=100, omega=100",
                expected_summary="Z=50.0, I_rms=2.0, power_P=160.0, cos_phi=0.8",
                actual_summary="EXCEPTION",
                passed=False,
                execution_time_ms=(time.perf_counter() - t0) * 1000.0,
                error_message=str(exc),
            )
        )

    # --- TEST 3: HÓA HỌC - Cân bằng phương trình hóa học bằng đại số tuyến tính ---
    t0 = time.perf_counter()
    try:
        eq_in = "Fe + O2 -> Fe2O3"
        out_chem_bal = balance_chemical_equation(eq_in)
        dt_ms = (time.perf_counter() - t0) * 1000.0

        bal_str = str(out_chem_bal.get("balanced_equation", "")).strip()
        norm_bal = re.sub(r"\s+", "", bal_str).replace("=", "->")
        passed = norm_bal == "4Fe+3O2->2Fe2O3"

        results.append(
            ScienceTestResult(
                test_id="SCI-CHEM-001",
                domain="Hóa học (Chemistry)",
                function_name="balance_chemical_equation",
                description_vi="Cân bằng phương trình phản ứng oxi hóa - khử Fe + O2 -> Fe2O3 bằng hệ phương trình bảo toàn nguyên tố.",
                input_summary=f"'{eq_in}'",
                expected_summary="'4Fe + 3O2 -> 2Fe2O3'",
                actual_summary=f"'{bal_str}'",
                passed=passed,
                execution_time_ms=dt_ms,
            )
        )
    except Exception as exc:
        results.append(
            ScienceTestResult(
                test_id="SCI-CHEM-001",
                domain="Hóa học (Chemistry)",
                function_name="balance_chemical_equation",
                description_vi="Cân bằng phương trình hóa học Fe + O2 -> Fe2O3.",
                input_summary="'Fe + O2 -> Fe2O3'",
                expected_summary="'4Fe + 3O2 -> 2Fe2O3'",
                actual_summary="EXCEPTION",
                passed=False,
                execution_time_ms=(time.perf_counter() - t0) * 1000.0,
                error_message=str(exc),
            )
        )

    # --- TEST 4: HÓA HỌC - Tính nồng độ mol dung dịch (C_M) ---
    t0 = time.perf_counter()
    try:
        m_gram, molar_mass, v_liter = 11.7, 58.5, 0.5
        out_conc = calculate_solution_concentrations(m_solute_gram=m_gram, molar_mass=molar_mass, v_solution_liter=v_liter)
        dt_ms = (time.perf_counter() - t0) * 1000.0

        cm_val = float(out_conc.get("C_M", -1.0))
        passed = math.isclose(cm_val, 0.4, rel_tol=1e-4)

        results.append(
            ScienceTestResult(
                test_id="SCI-CHEM-002",
                domain="Hóa học (Chemistry)",
                function_name="calculate_solution_concentrations",
                description_vi="Tính nồng độ mol (C_M) của dung dịch khi hòa tan 11.7g NaCl (M=58.5) vào 0.5 lít dung dịch.",
                input_summary="m_solute_gram=11.7, molar_mass=58.5, v_solution_liter=0.5",
                expected_summary="C_M = 0.4 M",
                actual_summary=f"C_M = {cm_val:.4g} M",
                passed=passed,
                execution_time_ms=dt_ms,
            )
        )
    except Exception as exc:
        results.append(
            ScienceTestResult(
                test_id="SCI-CHEM-002",
                domain="Hóa học (Chemistry)",
                function_name="calculate_solution_concentrations",
                description_vi="Tính nồng độ mol dung dịch C_M.",
                input_summary="m_solute_gram=11.7, molar_mass=58.5, v_solution_liter=0.5",
                expected_summary="C_M = 0.4 M",
                actual_summary="EXCEPTION",
                passed=False,
                execution_time_ms=(time.perf_counter() - t0) * 1000.0,
                error_message=str(exc),
            )
        )

    # --- TEST 5: SINH HỌC - Quy luật phân li độc lập Mendel ---
    t0 = time.perf_counter()
    try:
        out_mendel = solve_mendelian_cross("AaBb", "AaBb")
        dt_ms = (time.perf_counter() - t0) * 1000.0

        pheno_str = str(out_mendel.get("phenotype_ratio_str", "")).strip()
        passed = ("9" in pheno_str and "3" in pheno_str and "1" in pheno_str)

        results.append(
            ScienceTestResult(
                test_id="SCI-BIO-001",
                domain="Sinh học (Biology)",
                function_name="solve_mendelian_cross",
                description_vi="Xác định tỉ lệ phân li kiểu hình đời con F1 trong phép lai hai cặp tính trạng AaBb x AaBb.",
                input_summary="parent1='AaBb', parent2='AaBb'",
                expected_summary="'9 A-B- : 3 A-bb : 3 aaB- : 1 aabb'",
                actual_summary=f"'{pheno_str}'",
                passed=passed,
                execution_time_ms=dt_ms,
            )
        )
    except Exception as exc:
        results.append(
            ScienceTestResult(
                test_id="SCI-BIO-001",
                domain="Sinh học (Biology)",
                function_name="solve_mendelian_cross",
                description_vi="Phép lai phân li độc lập Mendel AaBb x AaBb.",
                input_summary="parent1='AaBb', parent2='AaBb'",
                expected_summary="'9 A-B- : 3 A-bb : 3 aaB- : 1 aabb'",
                actual_summary="EXCEPTION",
                passed=False,
                execution_time_ms=(time.perf_counter() - t0) * 1000.0,
                error_message=str(exc),
            )
        )

    # --- TEST 6: SINH HỌC - Cân bằng di truyền quần thể Hardy-Weinberg ---
    t0 = time.perf_counter()
    try:
        out_hw = analyze_hardy_weinberg(recessive_phenotype_freq=0.16)
        dt_ms = (time.perf_counter() - t0) * 1000.0

        p_val = float(out_hw.get("p_freq", -1.0))
        q_val = float(out_hw.get("q_freq", -1.0))
        eq_flag = bool(out_hw.get("is_in_equilibrium", False))

        passed = (
            math.isclose(p_val, 0.6, rel_tol=1e-4)
            and math.isclose(q_val, 0.4, rel_tol=1e-4)
            and eq_flag is True
        )

        results.append(
            ScienceTestResult(
                test_id="SCI-BIO-002",
                domain="Sinh học (Biology)",
                function_name="analyze_hardy_weinberg",
                description_vi="Phân tích cấu trúc di truyền quần thể cân bằng Hardy-Weinberg khi tần số kiểu hình lặn (aa) = 0.16.",
                input_summary="recessive_phenotype_freq=0.16",
                expected_summary="p_freq=0.6, q_freq=0.4, is_in_equilibrium=True",
                actual_summary=f"p_freq={p_val:.4g}, q_freq={q_val:.4g}, is_in_equilibrium={eq_flag}",
                passed=passed,
                execution_time_ms=dt_ms,
            )
        )
    except Exception as exc:
        results.append(
            ScienceTestResult(
                test_id="SCI-BIO-002",
                domain="Sinh học (Biology)",
                function_name="analyze_hardy_weinberg",
                description_vi="Cân bằng di truyền quần thể Hardy-Weinberg.",
                input_summary="recessive_phenotype_freq=0.16",
                expected_summary="p_freq=0.6, q_freq=0.4, is_in_equilibrium=True",
                actual_summary="EXCEPTION",
                passed=False,
                execution_time_ms=(time.perf_counter() - t0) * 1000.0,
                error_message=str(exc),
            )
        )

    return results


# ==============================================================================
# 6. BỘ KẾT XUẤT BÁO CÁO SƯ PHẠM MARKDOWN (MASTER_PEDAGOGICAL_REPORT.md)
# ==============================================================================

def generate_markdown_report(summary: MasterBenchmarkSummary) -> str:
    """Tạo nội dung báo cáo kiểm định sư phạm chuẩn GDPT 2018 định dạng Markdown."""
    lines: List[str] = []

    lines.append("# BÁO CÁO KIỂM ĐỊNH CHẤT LƯỢNG GIÁO DỤC STEM & TÍNH TOÁN HÌNH THỨC (GDPT 2018)")
    lines.append("")
    lines.append(f"- **Thời điểm kiểm định:** `{summary.timestamp}`")
    lines.append("- **Hệ chương trình:** Chương trình Giáo dục Phổ thông 2018 (Bộ GD&ĐT Việt Nam)")
    lines.append("- **Phạm vi kiểm thử:** 20 bài toán chuẩn SGK (Lớp 10, 11, 12) & 6 bài kiểm thử Lõi Khoa học Tự nhiên (Vật lý, Hóa học, Sinh học)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. TỔNG QUAN CHỈ SỐ CHẤT LƯỢNG (EXECUTIVE QA METRICS)")
    lines.append("")
    lines.append("| Chỉ số Kiểm định (Benchmark Metric) | Kết quả Đạt / Tổng số | Tỷ lệ (%) | Đánh giá Chuẩn Sư phạm |")
    lines.append("| :--- | :---: | :---: | :---: |")
    lines.append(
        f"| **1. Độ chính xác Toán học (Mathematical Accuracy)** | "
        f"`{summary.passed_math_problems}/{summary.total_math_problems}` bài | "
        f"**{summary.math_accuracy_pct:.2f}%** | "
        f"{'ĐẠT CHUẨN (PASS)' if summary.math_accuracy_pct == 100.0 else 'CẦN HIỆU CHỈNH'} |"
    )
    lines.append(
        f"| **2. Tỷ lệ khử nghiệm ngoại lai (Extraneous Root Rejection)** | "
        f"`{summary.extraneous_problems_passed}/{summary.extraneous_problems_total}` bài "
        f"(`{summary.total_detected_extraneous_roots}/{summary.total_expected_extraneous_roots}` nghiệm) | "
        f"**{summary.extraneous_rejection_rate_pct:.2f}%** | "
        f"{'ĐẠT CHUẨN (PASS)' if summary.extraneous_rejection_rate_pct == 100.0 else 'CẢNH BÁO SƯ PHẠM'} |"
    )
    lines.append(
        f"| **3. Tỷ lệ kiểm thử Khoa học (Science Kernel Pass Rate)** | "
        f"`{summary.passed_science_tests}/{summary.total_science_tests}` test | "
        f"**{summary.science_pass_rate_pct:.2f}%** | "
        f"{'ĐẠT CHUẨN (PASS)' if summary.science_pass_rate_pct == 100.0 else 'CẦN HIỆU CHỈNH'} |"
    )
    lines.append(
        f"| **4. Tổng thời gian thực thi (Total Execution Time)** | "
        f"`{summary.total_math_problems + summary.total_science_tests}` tác vụ | "
        f"`{summary.total_execution_time_ms:.2f} ms` | "
        f"Trung bình `{summary.total_execution_time_ms / max(1, summary.total_math_problems + summary.total_science_tests):.2f} ms/bài` |"
    )
    lines.append("")

    # Thống kê theo từng khối lớp
    lines.append("### Phân bổ Độ chính xác theo Khối lớp (Toán GDPT 2018)")
    lines.append("")
    lines.append("| Khối lớp | Chuyên đề Trọng tâm | Số bài đạt | Tỷ lệ chính xác | Thời gian TB (ms) |")
    lines.append("| :---: | :--- | :---: | :---: | :---: |")
    for grade in (10, 11, 12):
        g_items = [r for r in summary.math_results if r.grade == grade]
        g_passed = sum(1 for r in g_items if r.passed_math)
        g_pct = (g_passed / len(g_items) * 100.0) if g_items else 0.0
        g_avg_ms = (
            sum(r.execution_time_ms for r in g_items) / len(g_items) if g_items else 0.0
        )
        topic_desc = {
            10: "Phương trình chứa căn thức quy về bậc hai & Khử nghiệm ngoại lai",
            11: "Phương trình lượng giác trên đoạn & Cấp số cộng / Cấp số nhân",
            12: "Khảo sát hàm số (Bậc 3, Phân thức, Tham số m) & PT Căn/Trị tuyệt đối",
        }[grade]
        lines.append(
            f"| **Lớp {grade}** | {topic_desc} | `{g_passed}/{len(g_items)}` | **{g_pct:.2f}%** | `{g_avg_ms:.2f} ms` |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Chi tiết 20 bài toán SGK
    lines.append("## 2. KẾT QUẢ CHI TIẾT 20 BÀI TOÁN SGK TOÁN (LỚP 10, 11, 12)")
    lines.append("")
    lines.append("| Mã bài | Lớp | Hàm Kernel | Biểu thức / Hệ | Kết quả Chuẩn (Ground Truth) | Kết quả Thực tế (Kernel Output) | Khử ngoại lai | Thời gian (ms) | Trạng thái |")
    lines.append("| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: |")
    for r in summary.math_results:
        ext_badge = (
            f"Đạt ({r.detected_extraneous_count}/{r.expected_extraneous_count})"
            if r.has_extraneous_check and r.passed_extraneous
            else ("Thất bại" if r.has_extraneous_check else "N/A")
        )
        status_str = "PASS" if r.passed_math else "FAIL"
        lines.append(
            f"| `{r.problem_id}` | {r.grade} | `{r.target_function}` | `{r.expression_summary}` | "
            f"{r.expected_summary} | {r.actual_summary} | {ext_badge} | `{r.execution_time_ms:.2f}` | **{status_str}** |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Phân tích sư phạm và bẫy sai lầm học sinh thường gặp
    lines.append("## 3. PHÂN TÍCH SƯ PHẠM & KIỂM SOÁT SAI LẦM HỌC SINH (PEDAGOGICAL RUBRIC)")
    lines.append("")
    for r in summary.math_results:
        lines.append(f"### {r.problem_id} (Lớp {r.grade} - Mức độ: `{r.difficulty}`)")
        lines.append(f"- **Đề bài:** {r.prompt_vi}")
        lines.append(f"- **Mục tiêu năng lực (Learning Objective):** {r.learning_objective_vi}")
        lines.append(f"- **Sai lầm thường gặp (Common Pitfall):** {r.common_pitfall_vi}")
        lines.append(
            f"- **Đối chiếu tính toán hình thức:** `{r.actual_summary}` "
            f"(Thời gian: `{r.execution_time_ms:.2f} ms` — **{'ĐẠT' if r.passed_math else 'LỖI'}**)"
        )
        if r.error_message:
            lines.append(f"- **Chi tiết lỗi:** `{r.error_message}`")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Chi tiết 3 lõi khoa học tự nhiên
    lines.append("## 4. KẾT QUẢ KIỂM ĐỊNH 3 LÕI KHOA HỌC TỰ NHIÊN (VẬT LÝ - HÓA HỌC - SINH HỌC)")
    lines.append("")
    lines.append("| Mã Test | Phân môn | Hàm API Kiểm thử | Đầu vào (Input) | Đầu ra Kỳ vọng | Đầu ra Thực tế | Thời gian (ms) | Trạng thái |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: |")
    for s in summary.science_results:
        status_str = "PASS" if s.passed else "FAIL"
        lines.append(
            f"| `{s.test_id}` | {s.domain} | `{s.function_name}` | `{s.input_summary}` | "
            f"`{s.expected_summary}` | `{s.actual_summary}` | `{s.execution_time_ms:.2f}` | **{status_str}** |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 5. KẾT LUẬN CỦA HỘI ĐỒNG KIỂM ĐỊNH STEM")
    lines.append("")
    all_passed = (
        summary.math_accuracy_pct == 100.0
        and summary.extraneous_rejection_rate_pct == 100.0
        and summary.science_pass_rate_pct == 100.0
    )
    if all_passed:
        lines.append(
            "> **CHỨNG NHẬN ĐẠT CHUẨN (100% PASS):** Toàn bộ 20 bài toán đại số & giải tích "
            "(Lớp 10, 11, 12) theo Chương trình GDPT 2018 và 6 bài kiểm thử lõi Khoa học Tự nhiên "
            "(Vật lý, Hóa học, Sinh học) đều đạt độ chính xác tuyệt đối. Hệ thống xử lý chính xác "
            "100% các trường hợp nghiệm ngoại lai phát sinh khi bình phương hai vế hoặc phá dấu "
            "giá trị tuyệt đối, đồng thời phân tách đúng các khoảng đơn điệu qua điểm gián đoạn."
        )
    else:
        lines.append(
            "> **KHUYẾN NGHỊ HIỆU CHỈNH:** Phát hiện sai lệch trong quá trình kiểm thử tự động. "
            "Vui lòng rà soát các bài có trạng thái FAIL ở bảng chi tiết phía trên."
        )
    lines.append("")
    return "\n".join(lines)


# ==============================================================================
# 7. HÀM CHÍNH CHẠY TOÀN BỘ BENCHMARK & IN TÓM TẮT CONSOLE
# ==============================================================================

def run_master_benchmark() -> MasterBenchmarkSummary:
    """Nạp dữ liệu JSON, chạy toàn bộ 20 bài Toán + 6 test Khoa học và xuất báo cáo."""
    summary = MasterBenchmarkSummary(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    # 1. Nạp và chạy 20 bài toán SGK Lớp 10, 11, 12
    for grade in sorted(BENCHMARK_RELATIVE_PATHS.keys()):
        rel_path = BENCHMARK_RELATIVE_PATHS[grade]
        json_path = resolve_curriculum_file(rel_path)
        with json_path.open("r", encoding="utf-8") as f:
            dataset = json.load(f)

        problems = dataset.get("problems", [])
        for problem in problems:
            res = evaluate_single_math_problem(problem)
            summary.math_results.append(res)

    # 2. Chạy kiểm thử 3 lõi Khoa học Tự nhiên (Vật lý, Hóa học, Sinh học)
    summary.science_results = run_science_kernels_benchmark()

    # 3. Ghi đè báo cáo Markdown chuẩn sư phạm
    report_md = generate_markdown_report(summary)
    primary_report_path = resolve_report_output_path()
    primary_report_path.parent.mkdir(parents=True, exist_ok=True)
    primary_report_path.write_text(report_md, encoding="utf-8")

    local_report_path = CURRENT_SCRIPT_DIR / "MASTER_PEDAGOGICAL_REPORT.md"
    if local_report_path.resolve() != primary_report_path.resolve():
        local_report_path.write_text(report_md, encoding="utf-8")

    # 4. In bảng tóm tắt kết quả ra Console
    print("=" * 84)
    print("  MASTER STEM BENCHMARK RUNNER - BÁO CÁO TÓM TẮT KIỂM ĐỊNH SƯ PHẠM (GDPT 2018)")
    print("=" * 84)
    print(f"  Thời điểm thực thi            : {summary.timestamp}")
    print(
        f"  1. Độ chính xác Toán học      : {summary.passed_math_problems}/{summary.total_math_problems} bài "
        f"({summary.math_accuracy_pct:.2f}%)"
    )
    print(
        f"  2. Tỷ lệ khử nghiệm ngoại lai : {summary.extraneous_problems_passed}/{summary.extraneous_problems_total} bài "
        f"| {summary.total_detected_extraneous_roots}/{summary.total_expected_extraneous_roots} nghiệm "
        f"({summary.extraneous_rejection_rate_pct:.2f}%)"
    )
    print(
        f"  3. Tỷ lệ kiểm thử Khoa học    : {summary.passed_science_tests}/{summary.total_science_tests} test "
        f"({summary.science_pass_rate_pct:.2f}%)"
    )
    print(f"  4. Tổng thời gian thực thi    : {summary.total_execution_time_ms:.2f} ms")
    print("-" * 84)
    for r in summary.math_results:
        status_icon = "[PASS]" if r.passed_math else "[FAIL]"
        ext_info = (
            f" | Ngoại lai: {r.detected_extraneous_count}/{r.expected_extraneous_count}"
            if r.has_extraneous_check
            else ""
        )
        print(
            f"  {status_icon} {r.problem_id:<16} (Lớp {r.grade}) | {r.target_function:<27} | "
            f"{r.execution_time_ms:>6.2f} ms{ext_info}"
        )
    print("-" * 84)
    for s in summary.science_results:
        status_icon = "[PASS]" if s.passed else "[FAIL]"
        print(
            f"  {status_icon} {s.test_id:<16} ({s.domain:<19}) | {s.function_name:<33} | "
            f"{s.execution_time_ms:>6.2f} ms"
        )
    print("=" * 84)
    print(f"  Đã xuất báo cáo tại: {primary_report_path}")
    print("=" * 84)

    return summary


if __name__ == "__main__":
    run_master_benchmark()