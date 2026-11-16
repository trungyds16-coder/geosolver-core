"""
Reproducible Benchmark Script for GeoSolver 2D:
1. Exhaustive 10x10 Integer Grid Sweep (157,252 triangles, 943,512 permuted evaluations)
2. 20x20 Integer Grid Evaluation (10,482,124 triangles, 116 continuous tolerance false positives)
3. Direct Symbolic Verification of all 116 near-equilateral cases in SymPy 1.14
4. Throughput Benchmark comparing GeoSolver 2D vs. SymPy 1.14 (1,000 evaluations)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import itertools
import math
import time
import sympy as sp
from geosolver_core.classifier import classify_triangle

def run_10x10_exhaustive_sweep():
    print("--- 1. Running Exhaustive 10x10 Grid Sweep ---")
    pts = [(x, y) for x in range(10) for y in range(10)]
    triples = list(itertools.combinations(pts, 3))
    t0 = time.time()
    non_collinear = 0
    equilateral_count = 0
    perm_violations = 0

    for p1, p2, p3 in triples:
        if (p2[0]-p1[0])*(p3[1]-p1[1]) - (p2[1]-p1[1])*(p3[0]-p1[0]) == 0:
            continue
        non_collinear += 1
        res = classify_triangle(p1, p2, p3)
        if res["type"] == "equilateral":
            equilateral_count += 1
        t_type = res["type"]
        for p in itertools.permutations([p1, p2, p3]):
            if classify_triangle(*p)["type"] != t_type:
                perm_violations += 1

    elapsed = time.time() - t0
    print(f"Total non-collinear triangles: {non_collinear}")
    print(f"Total permuted evaluations: {non_collinear * 6}")
    print(f"False-positive equilateral: {equilateral_count}")
    print(f"Permutation-order violations: {perm_violations}")
    print(f"Elapsed time: {elapsed:.2f}s\n")
    assert non_collinear == 157252
    assert equilateral_count == 0
    assert perm_violations == 0

def run_20x20_grid_and_sympy_verification():
    print("--- 2. Running 20x20 Grid Evaluation & SymPy Verification ---")
    pts = [(x, y) for x in range(20) for y in range(20)]
    n = len(pts)
    t0 = time.time()
    non_collinear = 0
    near_eq_triangles = []

    for i in range(n):
        p1 = pts[i]
        for j in range(i + 1, n):
            p2 = pts[j]
            dx12 = p2[0] - p1[0]
            dy12 = p2[1] - p1[1]
            d1_sq = dx12*dx12 + dy12*dy12
            for k in range(j + 1, n):
                p3 = pts[k]
                cp = dx12 * (p3[1] - p1[1]) - dy12 * (p3[0] - p1[0])
                if cp == 0:
                    continue
                non_collinear += 1
                dx23 = p3[0] - p2[0]
                dy23 = p3[1] - p2[1]
                d2_sq = dx23*dx23 + dy23*dy23
                dx31 = p1[0] - p3[0]
                dy31 = p1[1] - p3[1]
                d3_sq = dx31*dx31 + dy31*dy31

                s1 = math.sqrt(d1_sq)
                s2 = math.sqrt(d2_sq)
                s3 = math.sqrt(d3_sq)
                max_s = max(s1, s2, s3)
                min_s = min(s1, s2, s3)
                if (max_s - min_s) <= 0.006 * max_s:
                    near_eq_triangles.append((p1, p2, p3, tuple(sorted([d1_sq, d2_sq, d3_sq]))))

    elapsed = time.time() - t0
    print(f"Total non-collinear triangles: {non_collinear}")
    print(f"Near-equilateral continuous tolerance cases (tol <= 0.006): {len(near_eq_triangles)}")
    print(f"Elapsed time: {elapsed:.2f}s")
    assert non_collinear == 10482124
    assert len(near_eq_triangles) == 116

    # Verify GeoSolver 2D rejects equilateral on all 116
    geosolver_eq_count = 0
    for p1, p2, p3, _ in near_eq_triangles:
        res = classify_triangle(p1, p2, p3)
        if res["type"] == "equilateral":
            geosolver_eq_count += 1
    print(f"GeoSolver 2D false equilateral count on 116 cases: {geosolver_eq_count}")
    assert geosolver_eq_count == 0

    # Verify SymPy on all 116 cases
    print("Verifying all 116 cases with SymPy 1.14 symbolic geometry...")
    sympy_eq_count = 0
    for p1, p2, p3, _ in near_eq_triangles:
        t = sp.Triangle(sp.Point(*p1), sp.Point(*p2), sp.Point(*p3))
        if t.is_equilateral():
            sympy_eq_count += 1
    print(f"SymPy 1.14 equilateral count on 116 cases: {sympy_eq_count}")
    assert sympy_eq_count == 0
    print("SymPy 1.14 100% agreement: all 116 cases rejected as equilateral.\n")

def run_throughput_benchmark():
    print("--- 3. Running Throughput Benchmark: GeoSolver 2D vs SymPy 1.14 ---")
    p1 = (0, 0)
    p2 = (1000, 0)
    p3 = (500, 866)

    # 1000 evaluations GeoSolver 2D
    t0 = time.time()
    for _ in range(1000):
        _ = classify_triangle(p1, p2, p3)
    t_geo = (time.time() - t0) * 1000  # ms

    # 1000 evaluations SymPy
    sp1 = sp.Point(0, 0)
    sp2 = sp.Point(1000, 0)
    sp3 = sp.Point(500, 866)
    t0 = time.time()
    for _ in range(1000):
        t = sp.Triangle(sp1, sp2, sp3)
        _ = t.is_equilateral()
        _ = t.is_isosceles()
    t_sympy = (time.time() - t0) * 1000  # ms

    print(f"GeoSolver 2D (1,000 evals): {t_geo:.2f} ms ({t_geo/1000*1000:.2f} us/eval)")
    print(f"SymPy 1.14   (1,000 evals): {t_sympy:.2f} ms ({t_sympy/1000*1000:.2f} us/eval)")
    print(f"Speedup: {t_sympy / t_geo:.1f}x\n")

if __name__ == "__main__":
    print("=== GeoSolver 2D Empirical Verification Suite ===\n")
    run_10x10_exhaustive_sweep()
    run_20x20_grid_and_sympy_verification()
    run_throughput_benchmark()
    print("=== All Empirical Verifications Passed Successfully ===")
