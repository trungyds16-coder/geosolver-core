# -*- coding: utf-8 -*-
"""
GeoSolver Core Test Suite - Zero GUI Dependencies
Tests pure provenance tracking and invariant classification directly on geosolver_core.
"""

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

        # 4. Deep stack guard (>= 100) returns False
        node = {"id": "D0", "source": "typed", "exact": True}
        for i in range(1, 105):
            node = {"id": f"D{i}", "source": "midpoint", "parents": [node]}
        self.assertFalse(point_provenance_flag(node))

    def test_grid_snap_restores_exactness(self):
        # Snapping non-integer coordinates (3.24, 4.76) with step 0.5 -> (3.0, 5.0)
        sx, sy, src, exact = snap_to_grid(3.24, 4.76, grid_step=0.5)
        self.assertEqual((sx, sy), (3.0, 5.0))
        self.assertEqual(src, "grid_snap")
        self.assertTrue(exact)

    def test_shoelace_equilateral_unreachable_assertion(self):
        # Equilateral is unreachable on Z^2
        res = classify_triangle((0, 0), (1000, 0), (500, 866))
        self.assertEqual(res["type"], "isosceles")
        self.assertTrue(res["exact"])

if __name__ == "__main__":
    unittest.main()
