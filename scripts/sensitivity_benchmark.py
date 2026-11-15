# -*- coding: utf-8 -*-
"""
GeoSolver 2D Core - Comprehensive Sensitivity & Invariance Benchmark
Evaluates:
  1. Standard Sensitivity Sweep: Precision, Recall, F1 across 1,000 labeled triangles under Gaussian jitter.
  2. Hard Negatives Stress Test: Trade-off curve with near-boundary asymmetric configurations.
  3. Permutation Invariance Baseline: Comparison with naive positional if/elif classifier.
  4. Dual-Regime Lattice Exactness: Continuous tolerance vs. discrete integer arithmetic on Z^2.
  5. Decimal Lattice Sweep: Invariant exact classification across k in {1, 2, 3, 4}.

Reproducibility Seed: 42
"""

from __future__ import annotations
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
import random
import itertools
import argparse
from typing import Dict, List, Tuple, Any
from geosolver_core.classifier import classify_triangle


def generate_standard_dataset(seed: int = 42, N_per_class: int = 250, jitter_sigma: float = 0.03) -> List[Tuple[Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]], str]]:
    random.seed(seed)
    dataset: List[Tuple[Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]], str]] = []

    # 1. Equilateral (target: equilateral, side=10)
    for _ in range(N_per_class):
        pA = (0.0, 0.0)
        pB = (10.0 + random.gauss(0, jitter_sigma), 0.0)
        pC = (5.0 + random.gauss(0, jitter_sigma), 5.0 * math.sqrt(3) + random.gauss(0, jitter_sigma))
        dataset.append(((pA, pB, pC), 'equilateral'))

    # 2. Isosceles (target: isosceles, base=12, height=8, legs=10)
    for _ in range(N_per_class):
        pA = (0.0, 0.0)
        pB = (12.0 + random.gauss(0, jitter_sigma), 0.0)
        pC = (6.0 + random.gauss(0, jitter_sigma), 8.0 + random.gauss(0, jitter_sigma))
        dataset.append(((pA, pB, pC), 'isosceles'))

    # 3. Right (target: right, legs 6 and 8, hypotenuse 10)
    for _ in range(N_per_class):
        pA = (0.0, 0.0)
        pB = (8.0 + random.gauss(0, jitter_sigma), 0.0)
        pC = (0.0 + random.gauss(0, jitter_sigma), 6.0 + random.gauss(0, jitter_sigma))
        dataset.append(((pA, pB, pC), 'right'))

    # 4. Scalene (target: scalene, generic asymmetric vertices)
    for _ in range(N_per_class):
        pA = (0.0, 0.0)
        pB = (11.0 + random.gauss(0, jitter_sigma), 0.0)
        pC = (3.0 + random.gauss(0, jitter_sigma), 7.0 + random.gauss(0, jitter_sigma))
        dataset.append(((pA, pB, pC), 'scalene'))

    return dataset


def evaluate_dataset(dataset: List[Tuple[Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]], str]], tol_rel: float = 0.006) -> Dict[str, Any]:
    N_per_class = len(dataset) // 4
    tp = {'equilateral': 0, 'isosceles': 0, 'right': 0, 'scalene': 0}
    total_pred = {'equilateral': 0, 'isosceles': 0, 'right': 0, 'scalene': 0, 'right_isosceles': 0}

    for pts, target in dataset:
        res = classify_triangle(pts[0], pts[1], pts[2], points_exact=False, tol_rel=tol_rel)
        pred = res['type']
        total_pred[pred] = total_pred.get(pred, 0) + 1
        if pred == target:
            tp[target] += 1

    metrics = {}
    for cls in tp:
        precision = tp[cls] / total_pred[cls] if total_pred.get(cls, 0) > 0 else 0.0
        recall = tp[cls] / N_per_class
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        metrics[cls] = {'precision': precision, 'recall': recall, 'f1': f1, 'tp': tp[cls]}

    overall_acc = sum(tp.values()) / len(dataset)
    return {'per_class': metrics, 'overall_accuracy': overall_acc, 'tp_sum': sum(tp.values())}


def run_sensitivity_sweep(dataset: List[Tuple[Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]], str]]) -> None:
    tolerances = [0.002, 0.004, 0.006, 0.008, 0.010]
    print("\n=== Standard Dataset Sensitivity Sweep ===")
    print("tol_rel | Overall | Eq Rec | Eq Prec | Iso Rec | Iso Prec | Right Rec | Scalene Prec")
    print("--------|---------|--------|---------|---------|----------|-----------|-------------")
    for tol in tolerances:
        res = evaluate_dataset(dataset, tol_rel=tol)
        m = res['per_class']
        print(f"{tol:7.3f} | {res['overall_accuracy']*100:6.1f}% | {m['equilateral']['recall']*100:5.1f}% | {m['equilateral']['precision']*100:6.1f}% | {m['isosceles']['recall']*100:6.1f}% | {m['isosceles']['precision']*100:7.1f}% | {m['right']['recall']*100:8.1f}% | {m['scalene']['precision']*100:11.1f}%")


def run_hard_negatives_benchmark(seed: int = 42) -> None:
    """
    Evaluates 200 near-boundary hard negative scalene triangles across two decoupled families:
      - 100 near-isosceles scalene configurations with 0.8% - 1.5% side length mismatch.
        False positives begin emerging as tol_rel reaches and exceeds the lower bound of the
        mismatch band (1/100 at 0.008; 36/100 at 0.010).
      - 100 near-right scalene configurations with angles in [88.0 deg, 88.8 deg]
        (|cos theta| in [0.021, 0.035]). Yields 0/100 FP across all tol_rel values because
        the right-angle predicate employs a decoupled fixed angular bound |cos| <= 0.015 (~89.14 deg).
    """
    random.seed(seed)
    near_iso = []
    # 100 near-isosceles scalene
    for _ in range(100):
        mismatch = random.uniform(0.008, 0.015)
        base = 12.0
        leg1 = 10.0
        leg2 = 10.0 * (1.0 + mismatch)
        xC = (base**2 + leg1**2 - leg2**2) / (2.0 * base)
        yC = math.sqrt(max(0.1, leg1**2 - xC**2))
        near_iso.append(((0.0, 0.0), (base, 0.0), (xC, yC)))

    # 100 near-right scalene
    near_right = []
    for _ in range(100):
        deg = random.uniform(88.0, 88.8)
        rad = math.radians(deg)
        near_right.append(((0.0, 0.0), (8.0, 0.0), (6.0 * math.cos(rad), 6.0 * math.sin(rad))))

    print("\n=== Hard Negatives Stress Test (Near-Boundary Scalene) ===")
    print("tol_rel | Near-Iso FP (N=100) | Near-Right FP (N=100) | Total TN (N=200) | Total FP (N=200) | Combined FP (%)")
    print("--------|---------------------|-----------------------|------------------|------------------|----------------")
    for tol in [0.002, 0.004, 0.006, 0.008, 0.010]:
        fp_iso = 0
        for pts in near_iso:
            res = classify_triangle(pts[0], pts[1], pts[2], points_exact=False, tol_rel=tol)
            if res['type'] != 'scalene':
                fp_iso += 1

        fp_right = 0
        for pts in near_right:
            res = classify_triangle(pts[0], pts[1], pts[2], points_exact=False, tol_rel=tol)
            if res['type'] != 'scalene':
                fp_right += 1

        total_fp = fp_iso + fp_right
        total_tn = 200 - total_fp
        print(f"{tol:7.3f} | {fp_iso:16d}/100 | {fp_right:18d}/100 | {total_tn:13d}/200 | {total_fp:13d}/200 | {total_fp/200*100:13.1f}%")


def naive_classify_triangle(pA: Tuple[float, float], pB: Tuple[float, float], pC: Tuple[float, float], tol: float = 0.006) -> Tuple[str, Optional[int]]:
    """Naive positional if/elif classifier without label-free tie-breaking."""
    dAB = math.hypot(pB[0] - pA[0], pB[1] - pA[1])
    dBC = math.hypot(pC[0] - pB[0], pC[1] - pB[1])
    dCA = math.hypot(pA[0] - pC[0], pA[1] - pC[1])
    sides = [dAB, dBC, dCA]
    m = max(sides)
    if (m - min(sides)) <= tol * m:
        return 'equilateral', None
    # Positional first-match checks
    if abs(dAB - dCA) <= tol * max(dAB, dCA):
        return 'isosceles', 0  # Apex at first vertex A
    if abs(dAB - dBC) <= tol * max(dAB, dBC):
        return 'isosceles', 1  # Apex at second vertex B
    if abs(dBC - dCA) <= tol * max(dBC, dCA):
        return 'isosceles', 2  # Apex at third vertex C
    # Right angle check
    dotA = (pB[0]-pA[0])*(pC[0]-pA[0]) + (pB[1]-pA[1])*(pC[1]-pA[1])
    dotB = (pA[0]-pB[0])*(pC[0]-pB[0]) + (pA[1]-pB[1])*(pC[1]-pB[1])
    dotC = (pA[0]-pC[0])*(pB[0]-pC[0]) + (pA[1]-pC[1])*(pB[1]-pC[1])
    if abs(dotA) / (dAB * dCA) <= tol: return 'right', 0
    if abs(dotB) / (dAB * dBC) <= tol: return 'right', 1
    if abs(dotC) / (dBC * dCA) <= tol: return 'right', 2
    return 'scalene', None


def run_permutation_baseline(n_triangles: int = 200, seed: int = 42) -> None:
    random.seed(seed)
    naive_variants = 0
    geosolver_variants = 0

    for _ in range(n_triangles):
        d = random.uniform(5.0, 10.0)
        pA = (random.uniform(-5, 5), random.uniform(-5, 5))
        pB = (pA[0] + d, pA[1])
        pC = (pA[0] + d * 0.51, pA[1] + d * 0.86598)
        pts = [pA, pB, pC]
        names = {pA: 'A', pB: 'B', pC: 'C'}

        naive_apex_set = set()
        geo_apex_set = set()

        for perm in itertools.permutations(pts):
            _, n_apex_idx = naive_classify_triangle(perm[0], perm[1], perm[2])
            n_apex_name = names[perm[n_apex_idx]] if n_apex_idx is not None else None
            naive_apex_set.add(n_apex_name)

            dict_perm = [{'x': p[0], 'y': p[1], 'name': names[p]} for p in perm]
            g = classify_triangle(dict_perm[0], dict_perm[1], dict_perm[2], points_exact=False)
            geo_apex_set.add(g.get('vertex'))

        if len(naive_apex_set) > 1:
            naive_variants += 1
        if len(geo_apex_set) > 1:
            geosolver_variants += 1

    print("\n=== Permutation Invariance & Equivariance Comparison ===")
    print(f"Sample size: {n_triangles} near-tie configurations under all 6 permutations")
    print(f"  - Naive Positional Classifier: {naive_variants}/{n_triangles} ({naive_variants/n_triangles*100:.1f}%) apex-variant outcomes")
    print(f"  - GeoSolver 2D Invariant Kernel: {geosolver_variants}/{n_triangles} ({geosolver_variants/n_triangles*100:.1f}%) apex-variant outcomes")


def run_lattice_exactness_benchmark() -> None:
    print("\n=== Dual-Regime Lattice Exactness Benchmark ===")
    lattice_cases = [
        ((0, 0), (1000, 0), (500, 866)),   # Paper Example 1 (866^2 = 749956, AC^2 = BC^2 = 999956)
        ((0, 0), (100, 0), (50, 87)),      # Scaled near-equilateral
        ((0, 0), (10, 0), (5, 9)),         # Integer isosceles
        ((0, 0), (10000, 0), (5000, 8660)) # Higher-scale near-equilateral
    ]
    naive_fp = 0
    geosolver_fp = 0

    for pts in lattice_cases:
        n_type, _ = naive_classify_triangle(pts[0], pts[1], pts[2], tol=0.006)
        if n_type == 'equilateral':
            naive_fp += 1

        g = classify_triangle(pts[0], pts[1], pts[2], points_exact=True)
        if g['type'] == 'equilateral':
            geosolver_fp += 1

    print(f"Test cases on integer lattice Z^2: {len(lattice_cases)}")
    print(f"  - Continuous Tolerance Classifier: {naive_fp}/{len(lattice_cases)} ({naive_fp/len(lattice_cases)*100:.1f}%) false-positive equilateral")
    print(f"  - GeoSolver Discrete Lattice Regime: {geosolver_fp}/{len(lattice_cases)} ({geosolver_fp/len(lattice_cases)*100:.1f}%) false-positive equilateral")


def run_decimal_lattice_sweep(n_samples: int = 500, seed: int = 42) -> None:
    """Tests 500 non-collinear decimal lattice isosceles pairs across k in {1, 2, 3, 4}."""
    random.seed(seed)
    valid_count = 0
    exact_match_count = 0

    for _ in range(n_samples):
        k = random.randint(1, 4)
        scale = 10**k
        sxB = random.randint(-50, 50)
        syB = random.randint(-50, 50)
        d2 = sxB**2 + syB**2
        found_pair = None
        for dx in range(-abs(sxB), abs(sxB) + 1):
            rem = d2 - dx**2
            if rem >= 0:
                dy = int(round(rem**0.5))
                if dy**2 == rem and (dx != sxB or dy != syB) and (dx * syB != dy * sxB):
                    found_pair = (dx, dy)
                    break
        if found_pair:
            sxC, syC = found_pair
            pA = (0.0, 0.0)
            pB = (sxB / scale, syB / scale)
            pC = (sxC / scale, syC / scale)
            res = classify_triangle(pA, pB, pC)
            if res.get('is_triangle'):
                valid_count += 1
                if res['type'] in ('isosceles', 'right_isosceles') and res['vertex'] == 'A' and res['exact'] is True:
                    exact_match_count += 1

    print("\n=== Decimal Lattice Invariant Sweep (k in {1, 2, 3, 4}) ===")
    print(f"Non-collinear candidate pairs evaluated: {valid_count}")
    print(f"  - GeoSolver Discrete Regime Matches: {exact_match_count}/{valid_count} ({exact_match_count/valid_count*100:.1f}%) exact isosceles")


def main() -> None:
    parser = argparse.ArgumentParser(description="GeoSolver 2D Scientific Benchmark Suite")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    parser.add_argument("--tol-rel", type=float, default=0.006, help="Relative edge tolerance (default: 0.006)")
    parser.add_argument("--sweep", action="store_true", help="Run tolerance sweep across [0.002, 0.010]")
    parser.add_argument("--hard-negatives", action="store_true", help="Run hard negatives stress test")
    parser.add_argument("--baseline", action="store_true", help="Run permutation & lattice baseline comparisons")
    parser.add_argument("--decimal-lattice", action="store_true", help="Run decimal lattice sweep across k in 1..4")
    parser.add_argument("--all", action="store_true", help="Run all benchmarks and comparisons")
    args = parser.parse_args()

    dataset = generate_standard_dataset(seed=args.seed)
    
    # 1. Main classification report
    res = evaluate_dataset(dataset, tol_rel=args.tol_rel)
    print(f"=== GeoSolver 2D Benchmark (tol_rel = {args.tol_rel:.3f}, Seed = {args.seed}) ===")
    print("Triangle Class | Ground Truth | True Positive (TP) | Recall (%) | Precision (%) | F1-Score (%)")
    print("---------------|:------------:|:------------------:|:----------:|:-------------:|:------------:")
    for c, m in res['per_class'].items():
        print(f"{c.capitalize():14s} | {250:12d} | {m['tp']:18d} | {m['recall']*100:9.1f}% | {m['precision']*100:12.1f}% | {m['f1']*100:11.1f}%")
    print(f"Overall Dataset| {len(dataset):12d} | {res['tp_sum']:18d} | {res['overall_accuracy']*100:9.1f}% | {res['overall_accuracy']*100:12.1f}% | {res['overall_accuracy']*100:11.1f}%")

    if args.sweep or args.all:
        run_sensitivity_sweep(dataset)

    if args.hard_negatives or args.all:
        run_hard_negatives_benchmark(seed=args.seed)

    if args.baseline or args.all:
        run_permutation_baseline(n_triangles=200, seed=args.seed)
        run_lattice_exactness_benchmark()

    if args.decimal_lattice or args.all:
        run_decimal_lattice_sweep(n_samples=500, seed=args.seed)


if __name__ == '__main__':
    main()
