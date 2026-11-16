"""
Example: Automated Geometry Grading Harness (Example 3 from SoftwareX manuscript).

Demonstrates integrating geosolver_core into an autograder or Jupyter notebook
to evaluate geometric constructions based on shape classification, permutation
invariance, and exactness verification.
"""

import os
import sys

# Ensure repository root is in sys.path when running as a standalone script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from geosolver_core import classify_triangle


def grade(pA, pB, pC, expected="isosceles"):
    """
    Grade a student's triangle construction against an expected geometric type.

    Parameters
    ----------
    pA, pB, pC : tuple of (float or int, float or int)
        The Cartesian coordinates of triangle vertices in arbitrary order.
    expected : str
        Expected geometric category ("equilateral", "isosceles", "right", "scalene").

    Returns
    -------
    score : int
        Assigned score (0 = invalid/wrong type, 5 = approximate continuous, 10 = exact discrete).
    feedback : str
        Explanatory message returned to the student.
    """
    r = classify_triangle(pA, pB, pC)
    if not r["is_triangle"]:
        return 0, "Not a valid triangle."
    if r["type"] != expected:
        return 0, f"Expected {expected}, got {r['type']}."
    if not r["exact"]:
        return 5, "Right shape, approximate coordinates."
    return 10, f"Full credit (apex: {r['vertex']})."


if __name__ == "__main__":
    # Demonstration with different student submissions:

    # 1. Exact integer-grid isosceles triangle:
    score, msg = grade((0, 0), (1000, 0), (500, 866), expected="isosceles")
    print(f"Exact isosceles: score={score}, feedback='{msg}'")
    assert score == 10

    # 2. Permutation of vertices gives identical result:
    score_perm, msg_perm = grade((500, 866), (0, 0), (1000, 0), expected="isosceles")
    assert score == score_perm
    print(f"Permuted order:  score={score_perm}, feedback='{msg_perm}'")

    # 3. Continuous approximation (perturbed non-integer coordinates):
    score_approx, msg_approx = grade(
        (0.0, 0.0), (1.0, 0.0), (0.5, 0.86602540378), expected="equilateral"
    )
    print(f"Continuous approx: score={score_approx}, feedback='{msg_approx}'")
    assert score_approx == 5  # approximate coordinates, exact=False

    # 4. Collinear degenerated points:
    score_collinear, msg_collinear = grade((0, 0), (1, 1), (2, 2), expected="isosceles")
    print(f"Degenerate: score={score_collinear}, feedback='{msg_collinear}'")
    assert score_collinear == 0

    print("\nAll autograder demonstrations executed successfully.")
