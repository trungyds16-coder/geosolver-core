# -*- coding: utf-8 -*-
"""
Module: biology_kernel.py
Đường dẫn: D:\\AI DATA\\STEM_APP\\stem_shared_core\\biology\\biology_kernel.py
Mô tả:
    Lõi tính toán Sinh học Di truyền Sư phạm (Genetics & Population Biology Kernel):
    1. Bộ giải Di truyền Men-đen (Mendelian Genetics): phép lai 1 cặp và 2 cặp tính trạng
       phân ly độc lập, tính tỷ lệ kiểu gen và kiểu hình đời F1, F2 chính xác bằng phân số.
    2. Bộ phân tích Cân bằng di truyền quần thể theo Định luật Hacđi - Vanbec
       (Hardy-Weinberg Equilibrium: p^2 + 2pq + q^2 = 1).
"""

from __future__ import annotations

import math
from collections import defaultdict
from itertools import product
from typing import Any, Dict, List, Optional, Tuple

import sympy as sp


class BiologyKernelError(Exception):
    """Ngoại lệ chuyên biệt cho Lõi tính toán Sinh học."""
    pass


# ==============================================================================
# 1. BỘ GIẢI DI TRUYỀN MEN-ĐEN (PHÉP LAI 1 CẶP & 2 CẶP TÍNH TRẠNG)
# ==============================================================================

def _parse_genotype_loci(genotype: str) -> List[str]:
    """
    Tách chuỗi kiểu gen (vd: 'Aa' hoặc 'AaBb') thành danh sách từng cặp gen (locus)
    đã chuẩn hóa thứ tự alen trội (chữ hoa) đứng trước alen lặn (chữ thường).
    """
    cleaned = genotype.strip()
    if len(cleaned) not in (2, 4):
        raise BiologyKernelError(
            f"Kiểu gen '{genotype}' không hợp lệ. Chỉ hỗ trợ phép lai 1 cặp (2 ký tự) hoặc 2 cặp (4 ký tự)."
        )

    loci: List[str] = []
    for idx in range(0, len(cleaned), 2):
        pair = cleaned[idx : idx + 2]
        if pair[0].lower() != pair[1].lower() or not pair.isalpha():
            raise BiologyKernelError(
                f"Cặp alen '{pair}' trong kiểu gen '{genotype}' không cùng một gen."
            )
        # Sắp xếp chữ hoa (trội) đứng trước chữ thường (lặn): 'aA' -> 'Aa'
        sorted_pair = "".join(sorted(pair, key=lambda ch: (0 if ch.isupper() else 1)))
        loci.append(sorted_pair)

    return loci


def get_gamete_distribution(genotype: str) -> Dict[str, sp.Rational]:
    """
    Sinh tập hợp giao tử và tần số phân số chính xác của một cơ thể theo quy luật
    phân ly độc lập của Men-đen.
    """
    loci = _parse_genotype_loci(genotype)
    allele_options = [[locus[0], locus[1]] for locus in loci]
    raw_gametes = ["".join(comb) for comb in product(*allele_options)]

    total = len(raw_gametes)
    counts: Dict[str, int] = defaultdict(int)
    for g in raw_gametes:
        counts[g] += 1

    return {g: sp.Rational(cnt, total) for g, cnt in counts.items()}


def _combine_gametes(gamete1: str, gamete2: str) -> str:
    """Tổ hợp 2 giao tử thành kiểu gen hợp tử chuẩn hóa (vd: 'aB' + 'Ab' -> 'AaBb')."""
    loci_strs: List[str] = []
    for a1, a2 in zip(gamete1, gamete2):
        pair = "".join(sorted((a1, a2), key=lambda ch: (0 if ch.isupper() else 1)))
        loci_strs.append(pair)
    return "".join(loci_strs)


def _genotype_to_phenotype_code(genotype: str) -> str:
    """
    Ánh xạ kiểu gen sang ký hiệu kiểu hình trội hoàn toàn (vd: 'AaBb' -> 'A-B-', 'aabb' -> 'aabb').
    """
    loci = _parse_genotype_loci(genotype)
    pheno_parts: List[str] = []
    for pair in loci:
        if pair[0].isupper():
            pheno_parts.append(f"{pair[0]}-")
        else:
            pheno_parts.append(pair)
    return "".join(pheno_parts)


def _format_ratio_dict(prob_map: Dict[str, sp.Rational]) -> str:
    """Chuyển từ điển xác suất phân số sang chuỗi tỷ lệ số nguyên tối giản (vd: '9 A-B- : 3 A-bb : 3 aaB- : 1 aabb')."""
    denoms = [sp.fraction(prob)[1] for prob in prob_map.values()]
    lcm_val = 1
    for d in denoms:
        lcm_val = int(sp.ilcm(lcm_val, d))

    items = [(k, int(prob * lcm_val)) for k, prob in prob_map.items()]
    gcd_val = items[0][1]
    for _, c in items[1:]:
        gcd_val = int(sp.igcd(gcd_val, c))

    items = [(k, c // gcd_val) for k, c in items]
    items.sort(key=lambda x: (-x[1], x[0]))
    return " : ".join(f"{cnt} {k}" for k, cnt in items)


def solve_mendelian_cross(parent1: str, parent2: str) -> Dict[str, Any]:
    """
    Thực hiện phép lai Men-đen giữa hai cơ thể bố mẹ `parent1` x `parent2`
    (1 cặp hoặc 2 cặp tính trạng phân ly độc lập).
    """
    loci1 = _parse_genotype_loci(parent1)
    loci2 = _parse_genotype_loci(parent2)
    if len(loci1) != len(loci2) or [l.lower() for l in loci1] != [l.lower() for l in loci2]:
        raise BiologyKernelError(
            f"Hai cơ thể đem lai ('{parent1}' và '{parent2}') không tương đồng về các cặp gen."
        )

    gametes1 = get_gamete_distribution(parent1)
    gametes2 = get_gamete_distribution(parent2)

    genotype_probs: Dict[str, sp.Rational] = defaultdict( lambda: sp.Rational(0) )
    phenotype_probs: Dict[str, sp.Rational] = defaultdict( lambda: sp.Rational(0) )

    for g1, p1 in gametes1.items():
        for g2, p2 in gametes2.items():
            zygote = _combine_gametes(g1, g2)
            prob = p1 * p2
            genotype_probs[zygote] += prob
            pheno_code = _genotype_to_phenotype_code(zygote)
            phenotype_probs[pheno_code] += prob

    return {
        "parents": f"{''.join(loci1)} x {''.join(loci2)}",
        "gametes_parent1": {k: str(v) for k, v in gametes1.items()},
        "gametes_parent2": {k: str(v) for k, v in gametes2.items()},
        "genotype_probabilities": dict(genotype_probs),
        "phenotype_probabilities": dict(phenotype_probs),
        "genotype_ratio_str": _format_ratio_dict(genotype_probs),
        "phenotype_ratio_str": _format_ratio_dict(phenotype_probs),
    }


def simulate_f1_f2_generations(parent1_p: str, parent2_p: str) -> Dict[str, Any]:
    """
    Mô phỏng phép lai qua 2 thế hệ từ P -> F1, sau đó cho F1 tự thụ phấn (hoặc giao phối
    ngẫu nhiên giữa các cá thể F1 đồng nhất) để thu được kết quả đời F2.
    """
    f1_result = solve_mendelian_cross(parent1_p, parent2_p)
    f1_genotypes = list(f1_result["genotype_probabilities"].keys())

    # Nếu F1 đồng nhất 1 kiểu gen (vd P thuần chủng AABB x aabb -> 100% AaBb), cho F1 x F1
    if len(f1_genotypes) == 1:
        f1_rep = f1_genotypes[0]
        f2_result = solve_mendelian_cross(f1_rep, f1_rep)
    else:
        # Nếu F1 phân tính, tính tần số giao tử chung của quần thể F1 rồi cho tự thụ phấn
        f2_geno_probs: Dict[str, sp.Rational] = defaultdict(lambda: sp.Rational(0))
        f2_pheno_probs: Dict[str, sp.Rational] = defaultdict(lambda: sp.Rational(0))
        for geno, g_prob in f1_result["genotype_probabilities"].items():
            self_cross = solve_mendelian_cross(geno, geno)
            for z_geno, z_prob in self_cross["genotype_probabilities"].items():
                f2_geno_probs[z_geno] += g_prob * z_prob
            for z_pheno, zp_prob in self_cross["phenotype_probabilities"].items():
                f2_pheno_probs[z_pheno] += g_prob * zp_prob
        f2_result = {
            "genotype_probabilities": dict(f2_geno_probs),
            "phenotype_probabilities": dict(f2_pheno_probs),
            "genotype_ratio_str": _format_ratio_dict(f2_geno_probs),
            "phenotype_ratio_str": _format_ratio_dict(f2_pheno_probs),
        }

    return {
        "F1": f1_result,
        "F2": f2_result,
    }


# ==============================================================================
# 2. ĐỊNH LUẬT HACĐI - VANBEC (HARDY-WEINBERG EQUILIBRIUM: p^2 + 2pq + q^2 = 1)
# ==============================================================================

def analyze_hardy_weinberg(
    p_freq: Optional[float] = None,
    q_freq: Optional[float] = None,
    recessive_phenotype_freq: Optional[float] = None,
    observed_genotypes: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """
    Phân tích cấu trúc di truyền quần thể theo Định luật Hacđi - Vanbec (p^2 + 2pq + q^2 = 1):
    - Chế độ 1: Cho trước tần số alen p (A) hoặc q (a) hoặc tần số kiểu hình lặn q^2 (aa).
    - Chế độ 2: Cho trước tỷ lệ (hoặc số lượng cá thể) 3 kiểu gen {'AA': d, 'Aa': h, 'aa': r}
      để kiểm tra quần thể đã đạt trạng thái cân bằng di truyền hay chưa.
    """
    is_currently_in_equilibrium = True

    if observed_genotypes is not None:
        raw_aa_dom = float(observed_genotypes.get("AA", 0.0))
        raw_hetero = float(observed_genotypes.get("Aa", 0.0))
        raw_aa_rec = float(observed_genotypes.get("aa", 0.0))
        total = raw_aa_dom + raw_hetero + raw_aa_rec
        if total <= 0:
            raise BiologyKernelError("Tổng số cá thể hoặc tỷ lệ kiểu gen trong quần thể phải lớn hơn 0.")

        d = raw_aa_dom / total
        h = raw_hetero / total
        r = raw_aa_rec / total

        p = d + 0.5 * h
        q = r + 0.5 * h

        # Điều kiện cân bằng Hardy-Weinberg: d * r == (h / 2)^2 và d == p^2, h == 2pq, r == q^2
        is_currently_in_equilibrium = (
            abs(d - p**2) <= 1e-6
            and abs(h - 2.0 * p * q) <= 1e-6
            and abs(r - q**2) <= 1e-6
        )
    else:
        if recessive_phenotype_freq is not None:
            if not (0.0 <= recessive_phenotype_freq <= 1.0):
                raise BiologyKernelError("Tần số kiểu hình lặn (q^2) phải nằm trong đoạn [0, 1].")
            q = math.sqrt(recessive_phenotype_freq)
            p = 1.0 - q
        elif p_freq is not None and q_freq is not None:
            if abs((p_freq + q_freq) - 1.0) > 1e-6:
                raise BiologyKernelError("Tổng tần số hai alen p + q phải bằng 1.")
            p, q = float(p_freq), float(q_freq)
        elif p_freq is not None:
            p = float(p_freq)
            q = 1.0 - p
        elif q_freq is not None:
            q = float(q_freq)
            p = 1.0 - q
        else:
            raise BiologyKernelError("Cần cung cấp p_freq, q_freq, recessive_phenotype_freq hoặc observed_genotypes.")

        if not (0.0 <= p <= 1.0 and 0.0 <= q <= 1.0):
            raise BiologyKernelError("Tần số alen p và q phải nằm trong đoạn [0, 1].")

    freq_AA = round(p**2, 6)
    freq_Aa = round(2.0 * p * q, 6)
    freq_aa = round(q**2, 6)

    return {
        "p_freq": round(p, 6),
        "q_freq": round(q, 6),
        "allele_frequencies": {
            "p_A": round(p, 6),
            "q_a": round(q, 6),
        },
        "equilibrium_genotype_frequencies": {
            "AA": freq_AA,
            "Aa": freq_Aa,
            "aa": freq_aa,
        },
        "phenotype_frequencies": {
            "dominant_A_": round(freq_AA + freq_Aa, 6),
            "recessive_aa": freq_aa,
        },
        "is_in_equilibrium": is_currently_in_equilibrium,
        "equation_str": f"{freq_AA}AA + {freq_Aa}Aa + {freq_aa}aa = 1",
    }


# ==============================================================================
# KHỐI KIỂM THỬ TỰ ĐỘNG (UNIT TESTS)
# ==============================================================================

if __name__ == "__main__":
    print("=" * 72)
    print("KIỂM THỬ LÕI SINH HỌC (biology_kernel.py)")
    print("=" * 72)

    # 1. Kiểm thử phép lai 1 cặp tính trạng và 2 cặp tính trạng Men-đen (P thuần chủng -> F1 -> F2)
    mono = simulate_f1_f2_generations("AA", "aa")
    assert mono["F1"]["genotype_ratio_str"] == "1 Aa"
    assert mono["F2"]["genotype_ratio_str"] == "2 Aa : 1 AA : 1 aa"
    assert mono["F2"]["phenotype_ratio_str"] == "3 A- : 1 aa"

    dihybrid = simulate_f1_f2_generations("AABB", "aabb")
    assert dihybrid["F1"]["genotype_ratio_str"] == "1 AaBb"
    assert dihybrid["F2"]["phenotype_ratio_str"] == "9 A-B- : 3 A-bb : 3 aaB- : 1 aabb"
    assert dihybrid["F2"]["genotype_probabilities"]["AaBb"] == sp.Rational(4, 16)
    print("[PASS] 1. Bộ giải Di truyền Men-đen (F1, F2 cho phép lai 1 cặp & 2 cặp tính trạng).")

    # 2. Kiểm thử Định luật Hacđi - Vanbec (Hardy-Weinberg)
    # Quần thể 0.36 AA : 0.48 Aa : 0.16 aa -> cân bằng với p = 0.6, q = 0.4
    hw_eq = analyze_hardy_weinberg(observed_genotypes={"AA": 0.36, "Aa": 0.48, "aa": 0.16})
    assert hw_eq["is_in_equilibrium"] is True
    assert abs(hw_eq["allele_frequencies"]["p_A"] - 0.6) <= 1e-6
    assert abs(hw_eq["allele_frequencies"]["q_a"] - 0.4) <= 1e-6

    # Quần thể chưa cân bằng: 0.4 AA : 0.4 Aa : 0.2 aa -> p = 0.6, q = 0.4 nhưng d != p^2
    hw_non_eq = analyze_hardy_weinberg(observed_genotypes={"AA": 0.40, "Aa": 0.40, "aa": 0.20})
    assert hw_non_eq["is_in_equilibrium"] is False
    assert abs(hw_non_eq["equilibrium_genotype_frequencies"]["AA"] - 0.36) <= 1e-6
    print("[PASS] 2. Bộ phân tích Cân bằng di truyền quần thể Hacđi - Vanbec.")