# -*- coding: utf-8 -*-
"""
GeoSolver 2D Core - Formal Rebuttal & Invariant Verification Suite
Validates bitwise type invariance and apex equivariance across discrete and continuous regimes.
"""

import unittest
import itertools
from geosolver_core.classifier import classify_triangle

class TestRebuttalInvariants(unittest.TestCase):
    def test_example_1_lattice_isosceles_named_equivariance(self):
        # Example 1: A(0,0), B(1000,0), C(500,866)
        # AC^2 = BC^2 = 999,956, AB^2 = 1,000,000 -> apex C
        pA = {"x": 0.0, "y": 0.0, "name": "A", "exact": True}
        pB = {"x": 1000.0, "y": 0.0, "name": "B", "exact": True}
        pC = {"x": 500.0, "y": 866.0, "name": "C", "exact": True}
        for p1, p2, p3 in itertools.permutations([pA, pB, pC]):
            res = classify_triangle(p1, p2, p3)
            self.assertEqual(res["type"], "isosceles")
            self.assertEqual(res["vertex"], "C")
            self.assertTrue(res["exact"])

    def test_example_2_lattice_isosceles_named_equivariance(self):
        # Example 2: A(0,0), B(10,0), C(5,7)
        # AC^2 = BC^2 = 74, AB^2 = 100 -> apex C
        pA = {"x": 0.0, "y": 0.0, "name": "A", "exact": True}
        pB = {"x": 10.0, "y": 0.0, "name": "B", "exact": True}
        pC = {"x": 5.0, "y": 7.0, "name": "C", "exact": True}
        for p1, p2, p3 in itertools.permutations([pA, pB, pC]):
            res = classify_triangle(p1, p2, p3)
            self.assertEqual(res["type"], "isosceles")
            self.assertEqual(res["vertex"], "C")
            self.assertTrue(res["exact"])

    def test_3_4_5_right_triangle_named_equivariance(self):
        # A(0,0), B(4,0), C(0,3) -> right angle at A
        pA = {"x": 0.0, "y": 0.0, "name": "A", "exact": True}
        pB = {"x": 4.0, "y": 0.0, "name": "B", "exact": True}
        pC = {"x": 0.0, "y": 3.0, "name": "C", "exact": True}
        for p1, p2, p3 in itertools.permutations([pA, pB, pC]):
            res = classify_triangle(p1, p2, p3)
            self.assertEqual(res["type"], "right")
            self.assertEqual(res["vertex"], "A")
            self.assertTrue(res["exact"])

    def test_unit_right_isosceles_named_equivariance(self):
        # A(0,0), B(1,0), C(0,1) -> right-isosceles at A
        pA = {"x": 0.0, "y": 0.0, "name": "A", "exact": True}
        pB = {"x": 1.0, "y": 0.0, "name": "B", "exact": True}
        pC = {"x": 0.0, "y": 1.0, "name": "C", "exact": True}
        for p1, p2, p3 in itertools.permutations([pA, pB, pC]):
            res = classify_triangle(p1, p2, p3)
            self.assertEqual(res["type"], "right_isosceles")
            self.assertEqual(res["vertex"], "A")
            self.assertTrue(res["exact"])

    def test_lattice_scalene_permutation_invariance(self):
        # (0,0), (10,30), (29,13)
        for p1, p2, p3 in itertools.permutations([(0,0), (10,30), (29,13)]):
            res = classify_triangle(p1, p2, p3)
            self.assertEqual(res["type"], "scalene")
            self.assertTrue(res["exact"])

    def test_near_tie_equivariance_continuous(self):
        # Continuous non-transitive near-tie case:
        # P=(0,0), Q=(1,0), R=(0.51, 0.86598)
        P = {"x": 0.0, "y": 0.0, "name": "P"}
        Q = {"x": 1.0, "y": 0.0, "name": "Q"}
        R = {"x": 0.51, "y": 0.86598, "name": "R"}
        for p1, p2, p3 in itertools.permutations([P, Q, R]):
            res = classify_triangle(p1, p2, p3)
            self.assertEqual(res["type"], "isosceles")
            self.assertEqual(res["vertex"], "P")
            self.assertFalse(res["exact"])

if __name__ == "__main__":
    unittest.main()
