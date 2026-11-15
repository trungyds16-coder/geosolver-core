# -*- coding: utf-8 -*-
"""
GeoSolver Core Test Suite - Zero GUI Dependencies
Tests pure provenance tracking and invariant classification directly on geosolver_core.
"""

from __future__ import annotations
import math
import unittest
import itertools
from geosolver_core.provenance import point_provenance_flag, snap_to_grid
from geosolver_core.classifier import classify_triangle, as_scaled_ints


class TestGeoSolverCoreDirect(unittest.TestCase):
    def test_provenance_dag_and_taint_conservation(self):
        # 1. Clean parents produce exact derived point
        pA = {"id": "A", "source": "typed", "exact": True}
        pB = {"id": "B", "source": "typed", "exact": True}
        pM = {"id": "M", "source": "midpoint", "parents": [pA, pB]}
        self.assertTrue(point_provenance_flag(pM))

        # 2. Tainted parent taints derived point (Taint Conservation Law)
        pFree = {"id": "Free", "source": "free", "exact": False}
        pM_tainted = {"id": "M2", "source": "midpoint", "parents": [pA, pFree]}
        self.assertFalse(point_provenance_flag(pM_tainted))

        # 3. Cycle safety via _visiting set
        pC1 = {"id": "C1", "source": "midpoint", "parents": []}
        pC2 = {"id": "C2", "source": "midpoint", "parents": [pC1]}
        pC1["parents"] = [pC2]
        self.assertFalse(point_provenance_flag(pC1))

    def test_item_2_1_stale_flag_after_parent_drag(self):
        """Referee Item 2.1: Stored exact flag on derived point must not wash dynamic parent taint."""
        p1 = {"source": "typed", "exact": True}
        p2 = {"source": "typed", "exact": True}
        mid = {"source": "midpoint", "parents": [p1, p2], "exact": True}
        self.assertTrue(point_provenance_flag(mid))

        # Mutate parent to dragged
        p1["source"] = "dragged"
        p1["exact"] = False
        # Must evaluate to False under Taint Conservation Law
        self.assertFalse(point_provenance_flag(mid))

    def test_item_2_2_parent_order_independence_deep_dag(self):
        """Referee Item 2.2: Order independence across parent permutations on deep subtrees (depth 110)."""
        def make_chain(length: int, base: dict) -> dict:
            curr = base
            for _ in range(length):
                curr = {"source": "midpoint", "parents": [curr]}
            return curr

        leaf = {"source": "typed", "exact": True}
        N = make_chain(60, leaf)
        top = make_chain(50, N)

        root_top_N = {"source": "midpoint", "parents": [top, N]}
        root_N_top = {"source": "midpoint", "parents": [N, top]}

        flag_top_N = point_provenance_flag(root_top_N)
        flag_N_top = point_provenance_flag(root_N_top)

        self.assertTrue(flag_top_N)
        self.assertTrue(flag_N_top)
        self.assertEqual(flag_top_N, flag_N_top, "Provenance evaluation must be strictly order-invariant across parent list order")

    def test_grid_snap_restores_exactness_and_returns_ints(self):
        """Tests snap_to_grid restores exactness and returns Python int types on integer coordinates."""
        sx, sy, src, exact = snap_to_grid(3.24, 4.76, grid_step=1.0)
        self.assertEqual((sx, sy), (3, 5))
        self.assertIsInstance(sx, int)
        self.assertIsInstance(sy, int)
        self.assertEqual(src, "grid_snap")
        self.assertTrue(exact)

    def test_shoelace_equilateral_unreachable_assertion(self):
        """Equilateral is unreachable on Z^2."""
        res = classify_triangle((0, 0), (1000, 0), (500, 866))
        self.assertEqual(res["type"], "isosceles")
        self.assertTrue(res["exact"])

    def test_permutation_invariance_all_six_orderings_headless(self):
        """Moved from GUI suite to Headless CI Suite: All 6 permutations on discrete and continuous cases."""
        cases = [
            # 1. Right at B: A(0,0), B(4,0), C(4,3)
            {
                "points": [{"name": "A", "x": 0.0, "y": 0.0},
                           {"name": "B", "x": 4.0, "y": 0.0},
                           {"name": "C", "x": 4.0, "y": 3.0}],
                "expected_type": "right",
                "apex": "B"
            },
            # 2. Isosceles at B: A(-3,0), B(0,5), C(3,0)
            {
                "points": [{"name": "A", "x": -3.0, "y": 0.0},
                           {"name": "B", "x": 0.0, "y": 5.0},
                           {"name": "C", "x": 3.0, "y": 0.0}],
                "expected_type": "isosceles",
                "apex": "B"
            },
            # 3. Right-isosceles at C: A(0,4), B(4,0), C(0,0)
            {
                "points": [{"name": "A", "x": 0.0, "y": 4.0},
                           {"name": "B", "x": 4.0, "y": 0.0},
                           {"name": "C", "x": 0.0, "y": 0.0}],
                "expected_type": "right_isosceles",
                "apex": "C"
            }
        ]
        for case in cases:
            pts = case["points"]
            results = []
            for perm in itertools.permutations(pts):
                res = classify_triangle(perm[0], perm[1], perm[2])
                results.append((res["type"], res["vertex"]))
            first_t, first_v = results[0]
            self.assertEqual(first_t, case["expected_type"])
            self.assertEqual(first_v, case["apex"])
            for t, v in results[1:]:
                self.assertEqual(t, first_t)
                self.assertEqual(v, first_v)

    def test_near_tie_permutation_invariance_headless(self):
        """Moved from GUI suite to Headless CI Suite: Claude near-tie case across all 6 permutations."""
        pA = {"name": "P", "x": 0.0, "y": 0.0, "source": "dragged", "exact": False}
        pB = {"name": "Q", "x": 1.0, "y": 0.0, "source": "dragged", "exact": False}
        pC = {"name": "R", "x": 0.51, "y": 0.86598, "source": "dragged", "exact": False}

        results = []
        for perm in itertools.permutations([pA, pB, pC]):
            res = classify_triangle(perm[0], perm[1], perm[2], points_exact=False)
            results.append((res["type"], res["vertex"]))

        first_t, first_v = results[0]
        self.assertEqual(first_t, "isosceles")
        self.assertEqual(first_v, "P")
        for t, v in results[1:]:
            self.assertEqual(t, first_t)
            self.assertEqual(v, first_v)


if __name__ == "__main__":
    unittest.main()
