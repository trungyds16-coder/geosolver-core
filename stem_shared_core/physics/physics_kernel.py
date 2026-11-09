# -*- coding: utf-8 -*-
"""
Module: physics_kernel.py
Đường dẫn: D:\\AI DATA\\STEM_APP\\stem_shared_core\\physics\\physics_kernel.py
Mô tả:
    Lõi tính toán Vật lý Sư phạm (Symbolic & Numerical Physics Kernel):
    1. Dao động điều hòa (Harmonic Oscillator): x(t), v(t), a(t), Wd, Wt, W.
    2. Mạch điện xoay chiều RLC nối tiếp: Z, ZL, ZC, tan(phi), phi, I, P, cos(phi), cộng hưởng.
    3. Phân tích và kiểm tra thứ nguyên tự động (Dimensional Analysis) với SymPy Units.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Optional

import sympy as sp
from sympy.physics import units as u
from sympy.physics.units.systems import SI


class PhysicsKernelError(Exception):
    """Ngoại lệ chuyên biệt cho Lõi tính toán Vật lý."""
    pass


# ==============================================================================
# 1. BỘ GIẢI DAO ĐỘNG ĐIỀU HÒA (HARMONIC OSCILLATOR)
# ==============================================================================

def solve_harmonic_oscillator(
    amplitude: float,
    omega: float,
    phi: float = 0.0,
    mass: Optional[float] = None,
    t_eval: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Xây dựng phương trình và tính toán các đại lượng đặc trưng của dao động điều hòa:
        x(t) = A * cos(omega * t + phi)
        v(t) = x'(t) = -A * omega * sin(omega * t + phi)
        a(t) = v'(t) = -A * omega^2 * cos(omega * t + phi)
    Nếu cung cấp khối lượng `mass` (kg), hàm tính thêm độ cứng k, động năng Wd(t),
    thế năng Wt(t) và cơ năng toàn phần W.

    Tham số:
        amplitude (float): Biên độ dao động A (đơn vị chuẩn: m, phải dương).
        omega (float): Tần số góc omega (rad/s, phải dương).
        phi (float): Pha ban đầu phi (rad).
        mass (float, optional): Khối lượng vật nặng m (kg, phải dương nếu truyền vào).
        t_eval (float, optional): Thời điểm t (s) cần tính giá trị tức thời.

    Trả về:
        dict: Chứa biểu thức ký hiệu x(t), v(t), a(t), chu kỳ T, tần số f, năng lượng
              và giá trị tức thời tại thời điểm t_eval.
    """
    if amplitude <= 0:
        raise PhysicsKernelError("Biên độ dao động A phải lớn hơn 0.")
    if omega <= 0:
        raise PhysicsKernelError("Tần số góc omega phải lớn hơn 0.")
    if mass is not None and mass <= 0:
        raise PhysicsKernelError("Khối lượng vật m phải lớn hơn 0.")

    t = sp.Symbol("t", real=True)
    A_sym = sp.nsimplify(amplitude, rational=True)
    w_sym = sp.nsimplify(omega, rational=False)
    phi_sym = sp.nsimplify(phi, rational=False)

    # Phương trình li độ, vận tốc, gia tốc theo biến thời gian t
    x_t = A_sym * sp.cos(w_sym * t + phi_sym)
    v_t = sp.diff(x_t, t)
    a_t = sp.diff(v_t, t)

    period_T = sp.simplify(2 * sp.pi / w_sym)
    freq_f = sp.simplify(w_sym / (2 * sp.pi))
    v_max = sp.simplify(A_sym * w_sym)
    a_max = sp.simplify(A_sym * (w_sym**2))

    energy_info: Optional[Dict[str, Any]] = None
    if mass is not None:
        m_sym = sp.nsimplify(mass, rational=True)
        k_sym = sp.simplify(m_sym * (w_sym**2))
        wt_expr = sp.simplify(sp.Rational(1, 2) * k_sym * (x_t**2))
        wd_expr = sp.simplify(sp.Rational(1, 2) * m_sym * (v_t**2))
        w_total = sp.trigsimp(wt_expr + wd_expr)

        energy_info = {
            "spring_constant_k": float(k_sym.evalf()),
            "potential_energy_expr": str(wt_expr),
            "kinetic_energy_expr": str(wd_expr),
            "total_energy_W": float(w_total.evalf()),
            "total_energy_symbolic": w_total,
        }

    instant_values: Optional[Dict[str, float]] = None
    if t_eval is not None:
        x_val = float(x_t.subs(t, t_eval).evalf())
        v_val = float(v_t.subs(t, t_eval).evalf())
        a_val = float(a_t.subs(t, t_eval).evalf())
        instant_values = {
            "t": float(t_eval),
            "x": round(x_val, 8),
            "v": round(v_val, 8),
            "a": round(a_val, 8),
        }
        if mass is not None and energy_info is not None:
            k_val = energy_info["spring_constant_k"]
            wt_val = 0.5 * k_val * (x_val**2)
            wd_val = 0.5 * mass * (v_val**2)
            instant_values["Wt"] = round(wt_val, 8)
            instant_values["Wd"] = round(wd_val, 8)
            instant_values["W"] = round(wt_val + wd_val, 8)

    return {
        "x_expr": x_t,
        "v_expr": v_t,
        "a_expr": a_t,
        "x_str": str(x_t),
        "v_str": str(v_t),
        "a_str": str(a_t),
        "period_T": float(period_T.evalf()),
        "frequency_f": float(freq_f.evalf()),
        "v_max": float(v_max.evalf()),
        "a_max": float(a_max.evalf()),
        "energy": energy_info,
        "instant_values": instant_values,
    }


# ==============================================================================
# 2. BỘ GIẢI MẠCH ĐIỆN XOAY CHIỀU RLC NỐI TIẾP
# ==============================================================================

def solve_rlc_circuit(
    R: float,
    L: float,
    C: float,
    U: float,
    omega: float,
) -> Dict[str, Any]:
    """
    Giải bài toán mạch điện xoay chiều RLC mắc nối tiếp:
    - Tính cảm kháng ZL = omega * L, dung kháng ZC = 1 / (omega * C).
    - Tính tổng trở Z = sqrt(R^2 + (ZL - ZC)^2).
    - Tính độ lệch pha phi của điện áp u so với cường độ dòng điện i:
      tan(phi) = (ZL - ZC) / R.
    - Tính cường độ dòng điện hiệu dụng I, hệ số công suất cos(phi), công suất P.
    - Kiểm tra điều kiện cộng hưởng điện (ZL == ZC) và tần số góc cộng hưởng omega_0.

    Tham số:
        R (float): Điện trở thuần (Ohm, không âm).
        L (float): Độ tự cảm của cuộn dây thuần cảm (H, dương).
        C (float): Điện dung của tụ điện (F, dương).
        U (float): Điện áp hiệu dụng hai đầu đoạn mạch (V, dương).
        omega (float): Tần số góc của dòng điện xoay chiều (rad/s, dương).

    Trả về:
        dict: Các thông số đặc trưng của mạch RLC và trạng thái cộng hưởng điện.
    """
    if R < 0:
        raise PhysicsKernelError("Điện trở R không được âm.")
    if L <= 0 or C <= 0:
        raise PhysicsKernelError("Độ tự cảm L và điện dung C phải lớn hơn 0.")
    if U <= 0 or omega <= 0:
        raise PhysicsKernelError("Điện áp hiệu dụng U và tần số góc omega phải lớn hơn 0.")

    Z_L = omega * L
    Z_C = 1.0 / (omega * C)
    Z = math.sqrt(R**2 + (Z_L - Z_C) ** 2)

    if Z == 0:
        raise PhysicsKernelError("Tổng trở Z bằng 0 (mạch ngắn mạch lý tưởng R=0 và ZL=ZC).")

    I_rms = U / Z
    phi_rad = math.atan2(Z_L - Z_C, R)
    phi_deg = math.degrees(phi_rad)
    tan_phi = (Z_L - Z_C) / R if R > 0 else math.copysign(math.inf, Z_L - Z_C)
    cos_phi = R / Z
    power_P = U * I_rms * cos_phi

    # Thông số cộng hưởng điện
    omega_resonance = 1.0 / math.sqrt(L * C)
    f_resonance = omega_resonance / (2.0 * math.pi)
    is_resonance = abs(Z_L - Z_C) <= 1e-6
    power_max_resonance = (U**2) / R if R > 0 else math.inf

    return {
        "Z_L": round(Z_L, 6),
        "Z_C": round(Z_C, 6),
        "Z": round(Z, 6),
        "I_rms": round(I_rms, 6),
        "tan_phi": round(tan_phi, 6) if not math.isinf(tan_phi) else tan_phi,
        "phi_rad": round(phi_rad, 6),
        "phi_deg": round(phi_deg, 4),
        "cos_phi": round(cos_phi, 6),
        "power_P": round(power_P, 6),
        "is_resonance": is_resonance,
        "resonance_info": {
            "omega_0": round(omega_resonance, 6),
            "f_0": round(f_resonance, 6),
            "Z_min": round(R, 6),
            "I_max": round(U / R, 6) if R > 0 else math.inf,
            "P_max": round(power_max_resonance, 6) if not math.isinf(power_max_resonance) else math.inf,
        },
    }


# ==============================================================================
# 3. KIỂM TRA THỨ NGUYÊN TỰ ĐỘNG (DIMENSIONAL ANALYSIS VỚI SYMPY UNITS)
# ==============================================================================

UNIT_SYMBOL_MAP: Dict[str, Any] = {
    "m": u.meter,
    "meter": u.meter,
    "s": u.second,
    "second": u.second,
    "kg": u.kilogram,
    "kilogram": u.kilogram,
    "A": u.ampere,
    "ampere": u.ampere,
    "K": u.kelvin,
    "mol": u.mole,
    "N": u.newton,
    "newton": u.newton,
    "J": u.joule,
    "joule": u.joule,
    "W": u.watt,
    "watt": u.watt,
    "Pa": u.pascal,
    "Hz": u.hertz,
    "V": u.volt,
    "volt": u.volt,
    "ohm": u.ohm,
    "F": u.farad,
    "farad": u.farad,
    "H": u.henry,
    "henry": u.henry,
    "C": u.coulomb,
}


def get_fundamental_dimensions(unit_expr: Any) -> Dict[str, Any]:
    """
    Trích xuất từ điển thứ nguyên cơ bản SI (length, mass, time, current, ...)
    của một biểu thức chứa đơn vị SymPy.
    """
    dim_sys = SI.get_dimension_system()
    if hasattr(SI, "_collect_factor_and_dimension"):
        dim_obj = SI._collect_factor_and_dimension(unit_expr)[1]
    elif hasattr(SI, "collect_factor_and_dimension"):
        dim_obj = SI.collect_factor_and_dimension(unit_expr)[1]
    else:
        dim_obj = SI.get_dimensional_expr(unit_expr)
    deps = dim_sys.get_dimensional_dependencies(dim_obj)
    return {str(k.name if hasattr(k, "name") else k): v for k, v in deps.items()}


def check_dimensional_consistency(lhs_unit_expr: Any, rhs_unit_expr: Any) -> Dict[str, Any]:
    """
    Kiểm tra tính đồng nhất thứ nguyên giữa vế trái (LHS) và vế phải (RHS) của
    một phương trình vật lý bằng SymPy Units.

    Tham số:
        lhs_unit_expr: Biểu thức đơn vị của vế trái (hoặc chuỗi biểu thức đơn vị).
        rhs_unit_expr: Biểu thức đơn vị của vế phải (hoặc chuỗi biểu thức đơn vị).

    Trả về:
        dict:
            - is_consistent (bool): True nếu hai vế có cùng thứ nguyên cơ bản SI.
            - lhs_dimensions (dict): Thứ nguyên cơ bản của vế trái.
            - rhs_dimensions (dict): Thứ nguyên cơ bản của vế phải.
    """
    if isinstance(lhs_unit_expr, str):
        lhs_unit_expr = sp.sympify(lhs_unit_expr, locals=UNIT_SYMBOL_MAP)
    if isinstance(rhs_unit_expr, str):
        rhs_unit_expr = sp.sympify(rhs_unit_expr, locals=UNIT_SYMBOL_MAP)

    try:
        lhs_dims = get_fundamental_dimensions(lhs_unit_expr)
        rhs_dims = get_fundamental_dimensions(rhs_unit_expr)
    except Exception as exc:
        raise PhysicsKernelError(f"Lỗi phân tích thứ nguyên: {exc}") from exc

    return {
        "is_consistent": lhs_dims == rhs_dims,
        "lhs_dimensions": lhs_dims,
        "rhs_dimensions": rhs_dims,
    }


# ==============================================================================
# KHỐI KIỂM THỬ TỰ ĐỘNG (UNIT TESTS)
# ==============================================================================

if __name__ == "__main__":
    print("=" * 72)
    print("KIỂM THỬ LÕI VẬT LÝ (physics_kernel.py)")
    print("=" * 72)

    # 1. Kiểm thử Dao động điều hòa: A = 0.1 m, omega = 10 rad/s, phi = 0, m = 0.2 kg
    ho = solve_harmonic_oscillator(amplitude=0.1, omega=10.0, phi=0.0, mass=0.2, t_eval=0.0)
    assert abs(ho["v_max"] - 1.0) <= 1e-9
    assert abs(ho["a_max"] - 10.0) <= 1e-9
    # Cơ năng W = 0.5 * m * omega^2 * A^2 = 0.5 * 0.2 * 100 * 0.01 = 0.1 J
    assert abs(ho["energy"]["total_energy_W"] - 0.1) <= 1e-9
    assert abs(ho["instant_values"]["x"] - 0.1) <= 1e-9
    assert abs(ho["instant_values"]["v"] - 0.0) <= 1e-9
    print("[PASS] 1. Bộ giải Dao động điều hòa (x, v, a, Wd, Wt, W).")

    # 2. Kiểm thử Mạch RLC nối tiếp: R = 100 Ohm, ZL = 200 Ohm, ZC = 100 Ohm, U = 100*sqrt(2) V
    omega_test = 100.0 * math.pi
    L_test = 2.0 / math.pi          # ZL = 200 Ohm
    C_test = 1e-4 / math.pi         # ZC = 100 Ohm
    U_test = 100.0 * math.sqrt(2.0) # U = 100*sqrt(2) V -> Z = 100*sqrt(2) -> I = 1 A
    rlc = solve_rlc_circuit(R=100.0, L=L_test, C=C_test, U=U_test, omega=omega_test)
    assert abs(rlc["Z_L"] - 200.0) <= 1e-5
    assert abs(rlc["Z_C"] - 100.0) <= 1e-5
    assert abs(rlc["I_rms"] - 1.0) <= 1e-5
    assert abs(rlc["phi_deg"] - 45.0) <= 1e-3
    assert abs(rlc["power_P"] - 100.0) <= 1e-4
    assert rlc["is_resonance"] is False
    print("[PASS] 2. Bộ giải Mạch điện xoay chiều RLC nối tiếp & Cộng hưởng điện.")

    # 3. Kiểm thử Thứ nguyên tự động bằng SymPy Units
    # Kiểm tra Động năng E_k = 1/2 * m * v^2 có đồng nhất với Joule hay không
    dim_energy = check_dimensional_consistency("J", "kg * (m / s)**2")
    assert dim_energy["is_consistent"] is True

    # Kiểm tra chu kỳ con lắc lò xo T = 2*pi*sqrt(m/k) với k có đơn vị N/m
    dim_period = check_dimensional_consistency("s", "sqrt(kg / (N / m))")
    assert dim_period["is_consistent"] is True

    # Phát hiện công thức sai thứ nguyên: v = a * t^2
    dim_wrong = check_dimensional_consistency("m / s", "(m / s**2) * s**2")
    assert dim_wrong["is_consistent"] is False
    print("[PASS] 3. Kiểm tra thứ nguyên tự động (Dimensional Analysis).")