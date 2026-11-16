# -*- coding: utf-8 -*-
"""
GeoSolver 2D Core - Pure Mathematical Classification Engine
License: GNU General Public License v3 (GPLv3)
"""

from __future__ import annotations
import math
from typing import Dict, Tuple, List, Optional, Any, Union
from geosolver_core.provenance import point_provenance_flag, _point_flag, snap_to_grid

def as_scaled_ints(coords: List[float], max_k: int = 4) -> Tuple[Optional[List[int]], float]:
    """
    Detect integer lattice coordinates or clean decimal inputs (e.g., 8.7, 2.9, 0.04):
    Multiplies coordinates by 10^k (k = 0..max_k). If all coordinates fall within
    alignment tolerance 1e-5 of an integer, returns the scaled integer coordinates.
    Otherwise (irrational coordinates or freehand float drift), returns (None, 1.0).

    Design and Boundary Characteristics:
    - Alignment Tolerance: 1e-5 absorbs IEEE-754 mantissa rounding around clean decimal representations.
    - Scale Limit: max_k = 4 bounds the maximum multiplier to 10^4. Fractional coordinates
      with more than 4 significant fractional digits fall cleanly into the continuous regime.
    - Epistemic Boundary: Scale invariance holds intra-regime.
      * Downward Crossing: Scaling a discrete shape below 1e-5 moves its coordinates
        across the precision threshold into the continuous regime.
      * Upward Crossing: Conversely, magnifying an untagged continuous coordinate
        with > 4 fractional digits (e.g. by 10x) can reduce its effective fractional digits
        to <= 4, causing it to cross upward into the discrete lattice regime.
        Points carrying explicit freehand provenance (`exact=False`) are quarantined
        against this upward crossing until explicitly snapped to grid.
    """
    for k in range(max_k + 1):
        s = 10 ** k
        if all(abs(v * s - round(v * s)) < 1e-5 for v in coords):
            return [round(v * s) for v in coords], float(s)
    return None, 1.0

def _finite(v: Any, label: str) -> float:
    """Validate and convert to finite float, strictly rejecting None, strings, Inf, and NaN."""
    if isinstance(v, (str, bytes)):
        raise ValueError(f"Coordinate '{label}' cannot be a string: {v!r}")
    try:
        f = float(v)
    except (TypeError, ValueError):
        raise ValueError(f"Coordinate '{label}' invalid numeric value: {v!r}")
    if not math.isfinite(f):
        raise ValueError(f"Coordinate '{label}' must be finite (rejected NaN/Inf): {f}")
    return f

def classify_triangle(
    pA: Union[Dict[str, Any], Tuple[float, float], List[float]],
    pB: Union[Dict[str, Any], Tuple[float, float], List[float]],
    pC: Union[Dict[str, Any], Tuple[float, float], List[float]],
    points_exact: Optional[bool] = None,
    tol_rel: float = 0.006
) -> Dict[str, Any]:
    """
    Pure geometric triangle classifier (Zero GUI / Tkinter dependencies).
    Guarantees bitwise type permutation invariance and apex equivariance.
    Evaluates provenance through the Directed Acyclic Graph (DAG) taint engine.
    """
    def extract_pt(p: Any, default_name: str) -> Tuple[float, float, str, Optional[bool]]:
        if p is None:
            raise ValueError(f"Point coordinate cannot be None: {p!r}")
        if isinstance(p, dict):
            if "x" not in p or "y" not in p:
                raise ValueError(f"Point dict missing 'x' or 'y': {p}")
            provenance = point_provenance_flag(p)
            return _finite(p["x"], "x"), _finite(p["y"], "y"), str(p.get("name") or default_name), provenance
        if not isinstance(p, (list, tuple)) or len(p) < 2:
            raise ValueError(f"Point must be a dict or sequence of at least 2 numbers: {p!r}")
        return _finite(p[0], "x"), _finite(p[1], "y"), default_name, None

    xA, yA, nA, exA = extract_pt(pA, "A")
    xB, yB, nB, exB = extract_pt(pB, "B")
    xC, yC, nC, exC = extract_pt(pC, "C")

    # Strict Taint Conservation Law: Any tainted vertex forces continuous regime
    pt_flags = [exA, exB, exC]
    if any(f is False for f in pt_flags) or points_exact is False:
        user_declared_exact = False
    elif points_exact is True or all(f is True for f in pt_flags):
        user_declared_exact = True
    else:
        user_declared_exact = None

    u_AB = (xB - xA, yB - yA)
    u_AC = (xC - xA, yC - yA)
    u_BC = (xC - xB, yC - yB)

    c_sq = u_AB[0]**2 + u_AB[1]**2
    b_sq = u_AC[0]**2 + u_AC[1]**2
    a_sq = u_BC[0]**2 + u_BC[1]**2

    c_len = math.sqrt(c_sq)  # AB
    b_len = math.sqrt(b_sq)  # AC
    a_len = math.sqrt(a_sq)  # BC

    cross = u_AB[0] * u_AC[1] - u_AB[1] * u_AC[0]
    scaled_coords, scale_factor = as_scaled_ints([xA, yA, xB, yB, xC, yC], max_k=4)
    is_discrete = (scaled_coords is not None) and (user_declared_exact is not False)

    if is_discrete:
        sxA, syA, sxB, syB, sxC, syC = scaled_coords
        s_uAB = (sxB - sxA, syB - syA)
        s_uAC = (sxC - sxA, syC - syA)
        s_uBC = (sxC - sxB, syC - syB)
        is_coincident = (s_uAB == (0, 0)) or (s_uAC == (0, 0)) or (s_uBC == (0, 0))
        is_collinear = (s_uAB[0] * s_uAC[1] - s_uAB[1] * s_uAC[0] == 0)
    else:
        l_max = max(a_len, b_len, c_len)
        if l_max < 1e-12:
            is_coincident = True
        else:
            is_coincident = (c_len / l_max < 1e-6) or (b_len / l_max < 1e-6) or (a_len / l_max < 1e-6)
        rel_cross = abs(cross) / (l_max * l_max) if l_max > 1e-12 else 0.0
        is_collinear = (rel_cross < 1e-5)

    if is_coincident:
        return {"is_triangle": False, "type": "coincident", "exact": False, "origin_exact": user_declared_exact, "is_discrete": is_discrete, "description": "Điểm trùng nhau", "sides": {"AB": c_len, "AC": b_len, "BC": a_len}}
    if is_collinear:
        return {"is_triangle": False, "type": "collinear", "exact": False, "origin_exact": user_declared_exact, "is_discrete": is_discrete, "description": "3 điểm thẳng hàng", "sides": {"AB": c_len, "AC": b_len, "BC": a_len}}

    l_max = max(a_len, b_len, c_len)
    l_min = min(a_len, b_len, c_len)

    # Initialize deviation metrics to exact zeros for discrete regime
    diff_AB_AC = 0.0
    diff_BA_BC = 0.0
    diff_CA_CB = 0.0

    if is_discrete:
        d2_AB = s_uAB[0]**2 + s_uAB[1]**2
        d2_AC = s_uAC[0]**2 + s_uAC[1]**2
        d2_BC = s_uBC[0]**2 + s_uBC[1]**2

        eq_AB_AC = (d2_AB == d2_AC)
        eq_BA_BC = (d2_AB == d2_BC)
        eq_CA_CB = (d2_AC == d2_BC)

        # Gauss-Shoelace area theorem: Equilateral triangle is provably unreachable on Z^2
        if eq_AB_AC and eq_BA_BC and eq_CA_CB:
            raise AssertionError("Equilateral triangle is provably impossible on Z^2 by Gauss-Shoelace area theorem")
        is_equilateral = False

        dot_A = s_uAB[0] * s_uAC[0] + s_uAB[1] * s_uAC[1]
        dot_B = -s_uAB[0] * s_uBC[0] - s_uAB[1] * s_uBC[1]
        dot_C = s_uAC[0] * s_uBC[0] + s_uAC[1] * s_uBC[1]

        perp_A = (dot_A == 0)
        perp_B = (dot_B == 0)
        perp_C = (dot_C == 0)
    else:
        max_AB_AC = max(c_len, b_len)
        max_BA_BC = max(c_len, a_len)
        max_CA_CB = max(b_len, a_len)

        eq_AB_AC = (abs(c_len - b_len) <= tol_rel * max_AB_AC) if max_AB_AC > 1e-12 else True
        eq_BA_BC = (abs(c_len - a_len) <= tol_rel * max_BA_BC) if max_BA_BC > 1e-12 else True
        eq_CA_CB = (abs(b_len - a_len) <= tol_rel * max_CA_CB) if max_CA_CB > 1e-12 else True

        diff_AB_AC = abs(c_len - b_len) / max_AB_AC if max_AB_AC > 1e-12 else 0.0
        diff_BA_BC = abs(c_len - a_len) / max_BA_BC if max_BA_BC > 1e-12 else 0.0
        diff_CA_CB = abs(b_len - a_len) / max_CA_CB if max_CA_CB > 1e-12 else 0.0

        is_equilateral = ((l_max - l_min) <= tol_rel * l_max) if l_max > 1e-12 else False

        dot_A = u_AB[0] * u_AC[0] + u_AB[1] * u_AC[1]
        dot_B = -u_AB[0] * u_BC[0] - u_AB[1] * u_BC[1]
        dot_C = u_AC[0] * u_BC[0] + u_AC[1] * u_BC[1]

        # Scale-correct perpendicularity check (|cos theta| <= 0.015 corresponds to |theta - 90| <= 0.86 deg)
        perp_A = (abs(dot_A / (c_len * b_len)) <= 0.015)
        perp_B = (abs(dot_B / (c_len * a_len)) <= 0.015)
        perp_C = (abs(dot_C / (b_len * a_len)) <= 0.015)

    # Specificity Hierarchy: Equilateral > Right-Isosceles > Isosceles > Right > Scalene
    if is_equilateral:
        desc = "Tam giác đều" if is_discrete else "Tam giác gần đều"
        return {"is_triangle": True, "type": "equilateral", "exact": is_discrete, "origin_exact": user_declared_exact, "is_discrete": is_discrete, "description": desc, "sides": {"AB": c_len, "AC": b_len, "BC": a_len}}

    opp_A = d2_BC if is_discrete else a_sq
    opp_B = d2_AC if is_discrete else b_sq
    opp_C = d2_AB if is_discrete else c_sq

    # 1. Right-Isosceles: candidate key sorted strictly by label-free (diff_leg, opposite_squared_side)
    ri_candidates = []
    if perp_A and eq_AB_AC: ri_candidates.append((diff_AB_AC, opp_A, nA))
    if perp_B and eq_BA_BC: ri_candidates.append((diff_BA_BC, opp_B, nB))
    if perp_C and eq_CA_CB: ri_candidates.append((diff_CA_CB, opp_C, nC))

    if ri_candidates:
        ri_candidates.sort(key=lambda item: (item[0], item[1]))
        best_apex = ri_candidates[0][2]
        desc = f"Tam giác vuông cân tại {best_apex}" if is_discrete else f"Tam giác gần vuông cân tại {best_apex}"
        return {"is_triangle": True, "type": "right_isosceles", "vertex": best_apex, "exact": is_discrete, "origin_exact": user_declared_exact, "is_discrete": is_discrete, "description": desc, "sides": {"AB": c_len, "AC": b_len, "BC": a_len}}

    # 2. Isosceles: candidate key sorted strictly by label-free (diff_leg, opposite_squared_side)
    iso_candidates = []
    if eq_AB_AC: iso_candidates.append((diff_AB_AC, opp_A, nA))
    if eq_BA_BC: iso_candidates.append((diff_BA_BC, opp_B, nB))
    if eq_CA_CB: iso_candidates.append((diff_CA_CB, opp_C, nC))

    if iso_candidates:
        iso_candidates.sort(key=lambda item: (item[0], item[1]))
        best_apex = iso_candidates[0][2]
        desc = f"Tam giác cân tại {best_apex}" if is_discrete else f"Tam giác gần cân tại {best_apex}"
        return {"is_triangle": True, "type": "isosceles", "vertex": best_apex, "exact": is_discrete, "origin_exact": user_declared_exact, "is_discrete": is_discrete, "description": desc, "sides": {"AB": c_len, "AC": b_len, "BC": a_len}}

    # 3. Right: candidate key sorted strictly by label-free (cosine_deviation, opposite_squared_side)
    right_candidates = []
    if perp_A: right_candidates.append((abs(dot_A / (c_len * b_len)) if not is_discrete else 0.0, opp_A, nA))
    if perp_B: right_candidates.append((abs(dot_B / (c_len * a_len)) if not is_discrete else 0.0, opp_B, nB))
    if perp_C: right_candidates.append((abs(dot_C / (b_len * a_len)) if not is_discrete else 0.0, opp_C, nC))

    if right_candidates:
        right_candidates.sort(key=lambda item: (item[0], item[1]))
        best_apex = right_candidates[0][2]
        desc = f"Tam giác vuông tại {best_apex}" if is_discrete else f"Tam giác gần vuông tại {best_apex}"
        return {"is_triangle": True, "type": "right", "vertex": best_apex, "exact": is_discrete, "origin_exact": user_declared_exact, "is_discrete": is_discrete, "description": desc, "sides": {"AB": c_len, "AC": b_len, "BC": a_len}}

    desc = "Tam giác thường"
    return {"is_triangle": True, "type": "scalene", "exact": is_discrete, "origin_exact": user_declared_exact, "is_discrete": is_discrete, "description": desc, "sides": {"AB": c_len, "AC": b_len, "BC": a_len}}
