# -*- coding: utf-8 -*-
"""
Module: chemistry_kernel.py
Đường dẫn: D:\\AI DATA\\STEM_APP\\stem_shared_core\\chemistry\\chemistry_kernel.py
Mô tả:
    Lõi tính toán Hóa học Sư phạm (Symbolic & Stoichiometric Chemistry Kernel):
    1. Cân bằng phương trình hóa học tự động bằng phương pháp Không gian nghiệm Ma trận
       (Matrix Nullspace Method) với số nguyên tối giản.
    2. Tính toán nồng độ mol (CM), nồng độ phần trăm (C%) và quy đổi hai chiều.
    3. Tính số mol electron trao đổi và cân bằng bán phản ứng Oxi hóa - Khử.
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

import sympy as sp


class ChemistryKernelError(Exception):
    """Ngoại lệ chuyên biệt cho Lõi tính toán Hóa học."""
    pass


# ==============================================================================
# 1. PHÂN TÍCH CÔNG THỨC & CÂN BẰNG PHƯƠNG TRÌNH HÓA HỌC (MATRIX NULLSPACE)
# ==============================================================================

TOKEN_REGEX = re.compile(r"([A-Z][a-z]?|\(|\)|\d+)")


def parse_chemical_formula(formula: str) -> Dict[str, int]:
    """
    Phân tích chuỗi công thức hóa học (hỗ trợ ngoặc đơn/lồng nhau như Fe2(SO4)3, Ca(OH)2)
    thành từ điển đếm số nguyên tử của từng nguyên tố.

    Tham số:
        formula (str): Công thức phân tử (vd: 'Fe2(SO4)3').

    Trả về:
        dict[str, int]: Ánh xạ ký hiệu nguyên tố -> số lượng nguyên tử.
    """
    cleaned = formula.strip()
    if not cleaned:
        raise ChemistryKernelError("Công thức hóa học không được để trống.")

    tokens = TOKEN_REGEX.findall(cleaned)
    if "".join(tokens) != cleaned:
        raise ChemistryKernelError(f"Công thức hóa học chứa ký tự không hợp lệ: '{formula}'.")

    stack: List[Dict[str, int]] = [defaultdict(int)]
    i = 0
    n = len(tokens)

    while i < n:
        tok = tokens[i]
        if tok == "(":
            stack.append(defaultdict(int))
            i += 1
        elif tok == ")":
            if len(stack) < 2:
                raise ChemistryKernelError(f"Dấu ngoặc đóng dư thừa trong công thức: '{formula}'.")
            group_counts = stack.pop()
            i += 1
            multiplier = 1
            if i < n and tokens[i].isdigit():
                multiplier = int(tokens[i])
                i += 1
            for elem, cnt in group_counts.items():
                stack[-1][elem] += cnt * multiplier
        elif tok[0].isupper():
            elem = tok
            i += 1
            count = 1
            if i < n and tokens[i].isdigit():
                count = int(tokens[i])
                i += 1
            stack[-1][elem] += count
        else:
            raise ChemistryKernelError(f"Cú pháp số chỉ không hợp lệ trong '{formula}'.")

    if len(stack) != 1:
        raise ChemistryKernelError(f"Chưa đóng hết dấu ngoặc trong công thức: '{formula}'.")

    return dict(stack[0])


def balance_chemical_equation(equation_str: str) -> Dict[str, Any]:
    """
    Cân bằng phương trình hóa học tự động bằng phương pháp Matrix Nullspace:
    - Thiết lập ma trận bảo toàn nguyên tố M (số hàng = số nguyên tố, số cột = số chất).
    - Tìm vector cơ sở trong Nullspace(M) bằng SymPy.
    - Quy đồng mẫu số chung nhỏ nhất (LCM) và rút gọn ước chung lớn nhất (GCD)
      để thu được bộ hệ số nguyên dương tối giản.

    Tham số:
        equation_str (str): Chuỗi phương trình hóa học chưa cân bằng, ngăn cách bởi '->' hoặc '='
                            (vd: 'Fe + HNO3 -> Fe(NO3)3 + NO + H2O').

    Trả về:
        dict: Gồm phương trình đã cân bằng, từ điển hệ số chất phản ứng / sản phẩm
              và ma trận nguyên tố.
    """
    if "->" in equation_str:
        lhs_str, rhs_str = equation_str.split("->", 1)
    elif "=" in equation_str:
        lhs_str, rhs_str = equation_str.split("=", 1)
    else:
        raise ChemistryKernelError("Phương trình phải chứa dấu '->' hoặc '=' ngăn cách hai vế.")

    reactants = [s.strip() for s in lhs_str.split("+") if s.strip()]
    products = [s.strip() for s in rhs_str.split("+") if s.strip()]

    if not reactants or not products:
        raise ChemistryKernelError("Phương trình phải có ít nhất 1 chất tham gia và 1 sản phẩm.")

    reactant_maps = [parse_chemical_formula(r) for r in reactants]
    product_maps = [parse_chemical_formula(p) for p in products]

    lhs_elements = {e for m in reactant_maps for e in m}
    rhs_elements = {e for m in product_maps for e in m}
    if lhs_elements != rhs_elements:
        diff = lhs_elements.symmetric_difference(rhs_elements)
        raise ChemistryKernelError(
            f"Vi phạm định luật bảo toàn nguyên tố. Nguyên tố lệch giữa hai vế: {sorted(diff)}."
        )

    elements = sorted(lhs_elements)
    all_compounds = reactants + products
    num_reactants = len(reactants)

    # Xây dựng ma trận hệ số nguyên tố A * x = 0
    matrix_rows: List[List[int]] = []
    for elem in elements:
        row: List[int] = []
        for r_map in reactant_maps:
            row.append(r_map.get(elem, 0))
        for p_map in product_maps:
            row.append(-p_map.get(elem, 0))
        matrix_rows.append(row)

    stoich_matrix = sp.Matrix(matrix_rows)
    nullspace_basis = stoich_matrix.nullspace()

    if not nullspace_basis:
        raise ChemistryKernelError(f"Không thể cân bằng phương trình: '{equation_str}'.")

    # Lấy vector cơ sở đầu tiên (hoặc tổ hợp dương nếu không gian nghiệm nhiều chiều)
    vec = nullspace_basis[0]
    if any(val <= 0 for val in vec) and len(nullspace_basis) > 1:
        for comb_w in range(1, 10):
            candidate = nullspace_basis[0] + comb_w * nullspace_basis[1]
            if all(val > 0 for val in candidate):
                vec = candidate
                break

    # Chuyển đổi vector hữu tỷ sang số nguyên dương tối giản
    denominators = [sp.fraction(val)[1] for val in vec]
    lcm_val = 1
    for d in denominators:
        lcm_val = int(sp.ilcm(lcm_val, d))

    int_coeffs = [int(val * lcm_val) for val in vec]
    if all(c < 0 for c in int_coeffs):
        int_coeffs = [-c for c in int_coeffs]

    if any(c <= 0 for c in int_coeffs):
        raise ChemistryKernelError(
            f"Hệ phương trình hóa học '{equation_str}' không có nghiệm nguyên dương hợp lệ."
        )

    gcd_val = int_coeffs[0]
    for c in int_coeffs[1:]:
        gcd_val = int(sp.igcd(gcd_val, c))
    int_coeffs = [c // gcd_val for c in int_coeffs]

    reactant_coeffs = dict(zip(reactants, int_coeffs[:num_reactants]))
    product_coeffs = dict(zip(products, int_coeffs[num_reactants:]))

    def _format_side(compounds: List[str], coeffs: List[int]) -> str:
        parts = [f"{c if c > 1 else ''}{comp}" for comp, c in zip(compounds, coeffs)]
        return " + ".join(parts)

    balanced_lhs = _format_side(reactants, int_coeffs[:num_reactants])
    balanced_rhs = _format_side(products, int_coeffs[num_reactants:])

    return {
        "balanced_equation": f"{balanced_lhs} -> {balanced_rhs}",
        "coefficients": int_coeffs,
        "reactant_coefficients": reactant_coeffs,
        "product_coefficients": product_coeffs,
        "elements": elements,
        "nullspace_dimension": len(nullspace_basis),
    }


# ==============================================================================
# 2. TÍNH TOÁN NỒNG ĐỘ MOL (CM) & NỒNG ĐỘ PHẦN TRĂM (C%)
# ==============================================================================

def calculate_solution_concentrations(
    n_solute_mol: Optional[float] = None,
    v_solution_liter: Optional[float] = None,
    m_solute_gram: Optional[float] = None,
    m_solution_gram: Optional[float] = None,
    molar_mass: Optional[float] = None,
    density_g_ml: Optional[float] = None,
    c_percent: Optional[float] = None,
    c_molar: Optional[float] = None,
) -> Dict[str, Optional[float]]:
    """
    Tính toán nồng độ mol (CM = n / V), nồng độ phần trăm (C% = m_ct / m_dd * 100%)
    và quy đổi qua lại theo công thức liên hệ: CM = (10 * D * C%) / M.
    """
    if m_solute_gram is not None and molar_mass is not None and n_solute_mol is None:
        if molar_mass <= 0:
            raise ChemistryKernelError("Khối lượng mol phân tử M phải lớn hơn 0.")
        n_solute_mol = m_solute_gram / molar_mass

    if n_solute_mol is not None and molar_mass is not None and m_solute_gram is None:
        m_solute_gram = n_solute_mol * molar_mass

    if n_solute_mol is not None and v_solution_liter is not None and c_molar is None:
        if v_solution_liter <= 0:
            raise ChemistryKernelError("Thể tích dung dịch V phải lớn hơn 0.")
        c_molar = n_solute_mol / v_solution_liter

    if m_solute_gram is not None and m_solution_gram is not None and c_percent is None:
        if m_solution_gram <= 0 or m_solute_gram > m_solution_gram:
            raise ChemistryKernelError("Khối lượng dung dịch không hợp lệ.")
        c_percent = (m_solute_gram / m_solution_gram) * 100.0

    # Quy đổi hai chiều giữa CM và C% thông qua khối lượng riêng D (g/mL) và M (g/mol)
    if density_g_ml is not None and molar_mass is not None:
        if density_g_ml <= 0 or molar_mass <= 0:
            raise ChemistryKernelError("Khối lượng riêng D và khối lượng mol M phải lớn hơn 0.")
        if c_percent is not None and c_molar is None:
            c_molar = (10.0 * density_g_ml * c_percent) / molar_mass
        elif c_molar is not None and c_percent is None:
            c_percent = (c_molar * molar_mass) / (10.0 * density_g_ml)

    return {
        "n_solute_mol": round(n_solute_mol, 6) if n_solute_mol is not None else None,
        "m_solute_gram": round(m_solute_gram, 6) if m_solute_gram is not None else None,
        "C_M": round(c_molar, 6) if c_molar is not None else None,
        "C_percent": round(c_percent, 6) if c_percent is not None else None,
    }


# ==============================================================================
# 3. TÍNH SỐ MOL ELECTRON TRAO ĐỔI TRONG PHẢN ỨNG OXI HÓA - KHỬ
# ==============================================================================

def calculate_redox_electron_transfer(
    element_symbol: str,
    ox_initial: int,
    ox_final: int,
    moles_element_or_compound: float,
    atoms_per_molecule: int = 1,
) -> Dict[str, Any]:
    """
    Tính số mol electron trao đổi (nhường hoặc nhận) và xác định vai trò chất khử /
    chất oxi hóa trong phản ứng Oxi hóa - Khử.

    Tham số:
        element_symbol (str): Ký hiệu nguyên tố thay đổi số oxi hóa (vd: 'Fe', 'N', 'Mn').
        ox_initial (int): Số oxi hóa ban đầu.
        ox_final (int): Số oxi hóa sau phản ứng.
        moles_element_or_compound (float): Số mol phân tử chất tham gia / tạo thành.
        atoms_per_molecule (int): Số nguyên tử của nguyên tố đó trong 1 phân tử chất.

    Trả về:
        dict: Gồm độ biến thiên số oxi hóa, vai trò, quá trình và tổng số mol electron trao đổi.
    """
    if moles_element_or_compound < 0 or atoms_per_molecule < 1:
        raise ChemistryKernelError("Số mol và chỉ số nguyên tử phải hợp lệ.")

    delta_ox = ox_final - ox_initial
    if delta_ox == 0:
        raise ChemistryKernelError(f"Nguyên tố {element_symbol} không thay đổi số oxi hóa.")

    electrons_per_molecule = abs(delta_ox) * atoms_per_molecule
    n_electron = moles_element_or_compound * electrons_per_molecule

    if delta_ox > 0:
        role = "Chất khử (Reductant)"
        process = "Quá trình oxi hóa (Nhường electron)"
        half_eq = f"{atoms_per_molecule if atoms_per_molecule > 1 else ''}{element_symbol}({ox_initial:+d}) -> {atoms_per_molecule if atoms_per_molecule > 1 else ''}{element_symbol}({ox_final:+d}) + {electrons_per_molecule}e"
    else:
        role = "Chất oxi hóa (Oxidant)"
        process = "Quá trình khử (Nhận electron)"
        half_eq = f"{atoms_per_molecule if atoms_per_molecule > 1 else ''}{element_symbol}({ox_initial:+d}) + {electrons_per_molecule}e -> {atoms_per_molecule if atoms_per_molecule > 1 else ''}{element_symbol}({ox_final:+d})"

    return {
        "element": element_symbol,
        "ox_initial": ox_initial,
        "ox_final": ox_final,
        "electrons_per_molecule": electrons_per_molecule,
        "moles_electron_transferred": round(n_electron, 6),
        "role": role,
        "process": process,
        "half_reaction": half_eq,
    }


# ==============================================================================
# KHỐI KIỂM THỬ TỰ ĐỘNG (UNIT TESTS)
# ==============================================================================

if __name__ == "__main__":
    print("=" * 72)
    print("KIỂM THỬ LÕI HÓA HỌC (chemistry_kernel.py)")
    print("=" * 72)

    # 1. Kiểm thử cân bằng phương trình hóa học bằng Matrix Nullspace
    eq1 = balance_chemical_equation("Fe + HNO3 -> Fe(NO3)3 + NO + H2O")
    assert eq1["coefficients"] == [1, 4, 1, 1, 2]
    assert eq1["balanced_equation"] == "Fe + 4HNO3 -> Fe(NO3)3 + NO + 2H2O"

    eq2 = balance_chemical_equation("KMnO4 + HCl -> KCl + MnCl2 + Cl2 + H2O")
    assert eq2["coefficients"] == [2, 16, 2, 2, 5, 8]
    print("[PASS] 1. Cân bằng phương trình hóa học bằng Matrix Nullspace.")

    # 2. Kiểm thử tính nồng độ CM, C% và quy đổi hai chiều (H2SO4 98%, D = 1.84 g/mL, M = 98)
    conc = calculate_solution_concentrations(
        c_percent=98.0,
        density_g_ml=1.84,
        molar_mass=98.0,
    )
    assert abs(conc["C_M"] - 18.4) <= 1e-6
    print("[PASS] 2. Tính toán nồng độ mol (CM) và nồng độ phần trăm (C%).")

    # 3. Kiểm thử bảo toàn electron trong phản ứng Oxi hóa - Khử (0.15 mol Cu tác dụng HNO3 tạo NO)
    redox_cu = calculate_redox_electron_transfer("Cu", ox_initial=0, ox_final=2, moles_element_or_compound=0.15)
    assert abs(redox_cu["moles_electron_transferred"] - 0.30) <= 1e-6
    assert "Chất khử" in redox_cu["role"]
    print("[PASS] 3. Tính số mol electron trao đổi trong phản ứng Oxi hóa - Khử.")