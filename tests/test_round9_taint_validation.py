"""Test hồi quy Round 9: taint, nhánh dung sai cho điểm vẽ tay, validate đầu vào.

Đặt vào tests/ và chạy:
python -m unittest tests.test_round9_taint_validation -v
"""
import math
import unittest

from geosolver.geosolver_desktop import classify_triangle


def P(x, y, source=None, exact=None, **kw):
    d = {"x": x, "y": y}
    if source is not None:
        d["source"] = source
    if exact is not None:
        d["exact"] = exact
    d.update(kw)
    return d


class TestInputValidation(unittest.TestCase):
    def test_nan_inf_none_rejected_in_dict(self):
        for bad in (float("nan"), float("inf"), float("-inf"), None, "abc"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    classify_triangle(P(bad, 0), P(1, 0), P(0, 1))

    def test_nan_inf_none_rejected_in_tuple(self):
        for bad in (float("nan"), float("inf"), None):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    classify_triangle((0, bad), (1, 0), (0, 1))


class TestFreehandTaint(unittest.TestCase):
    def test_free_integer_right_triangle_uses_tolerance_branch(self):
        r = classify_triangle(P(0, 0, "free"), P(3, 0, "free"), P(0, 4, "free"))
        self.assertEqual(r["type"], "right")
        self.assertFalse(r["is_discrete"])
        self.assertFalse(r["exact"])
        self.assertIs(r["origin_exact"], False)

    def test_free_near_isosceles_is_flagged_but_typed_is_not(self):
        # Hai cạnh góc vuông 1000 và 1004: lệch ~0.4% < 0.6%
        free = classify_triangle(P(0, 0, "free"), P(1000, 0, "free"), P(0, 1004, "free"))
        typed = classify_triangle(P(0, 0, "typed"), P(1000, 0, "typed"), P(0, 1004, "typed"))
        self.assertEqual(free["type"], "right_isosceles")
        self.assertIn("gần", free["description"])
        self.assertFalse(free["exact"])
        # Gõ tay thì so sánh chính xác: 1000 != 1004 nên chỉ là vuông thường
        self.assertEqual(typed["type"], "right")
        self.assertTrue(typed["exact"])

    def test_mixed_typed_and_free_is_false(self):
        r = classify_triangle(P(0, 0, "typed"), P(4, 0, "free"), P(0, 3, "typed"))
        self.assertIs(r["origin_exact"], False)
        self.assertFalse(r["exact"])

    def test_points_exact_true_cannot_override_free(self):
        r = classify_triangle(P(0, 0, "free"), P(4, 0, "typed"), P(0, 3, "typed"),
                              points_exact=True)
        self.assertIs(r["origin_exact"], False)
        self.assertFalse(r["exact"])

    def test_explicit_exact_false_beats_exact_source(self):
        r = classify_triangle(P(0, 0, "typed", exact=False), P(4, 0, "typed"), P(0, 3, "typed"))
        self.assertIs(r["origin_exact"], False)


class TestDerivedPointPropagation(unittest.TestCase):
    A = P(0, 0, "typed")
    B = P(4, 0, "typed")

    def test_midpoint_of_free_parents_is_tainted(self):
        c = P(0, 3, "midpoint", parents=[P(0, 2, "free"), P(0, 4, "typed")])
        r = classify_triangle(self.A, self.B, c)
        self.assertIs(r["origin_exact"], False)
        self.assertFalse(r["exact"])

    def test_midpoint_of_typed_parents_is_exact(self):
        c = P(0, 3, "midpoint", parents=[P(0, 2, "typed"), P(0, 4, "typed")])
        r = classify_triangle(self.A, self.B, c)
        self.assertIs(r["origin_exact"], True)
        self.assertTrue(r["exact"])

    def test_derived_without_parents_is_unknown(self):
        c = P(0, 3, "midpoint")
        r = classify_triangle(self.A, self.B, c)
        self.assertIsNone(r["origin_exact"])  # chuyển sang heuristic is_discrete


class TestMicroScaleStillOk(unittest.TestCase):
    def test_3_4_5_at_1e_minus_5(self):
        k = 1e-5
        r = classify_triangle((0, 0), (3 * k, 0), (0, 4 * k))
        self.assertTrue(r["is_triangle"])
        self.assertEqual(r["type"], "right")
        self.assertEqual(r["vertex"], "A")


if __name__ == "__main__":
    unittest.main()
