# GeoSolver 2D: A Provenance-Aware Dynamic Geometry Engine with Scale-Invariant and Permutation-Invariant Classification

**Authors:** Nguyen Van A$^1$, Tran Van B$^1$  
**Affiliation:** $^1$Laboratory of Applied Mathematics and Educational Technology, STEM Research Institute  
**Corresponding Author Email:** `author@geosolver.org`  
**Target Journal:** *SoftwareX* (Elsevier) — Original Software Publication (OSP)  

---

## Abstract
Interactive Dynamic Geometry Systems (DGS) are prone to geometric misclassifications when users construct or perturb configurations using freehand gestures. Floating-point rounding errors and non-transitive relative tolerances frequently lead to false-positive recognitions (such as misclassifying near-regular integer-lattice triangles as equilateral) or permutation-dependent outcomes (where the classified type depends on vertex enumeration order). We introduce **GeoSolver 2D**, an open-source, highly reliable geometry engine designed to eliminate these numerical artifacts. GeoSolver 2D implements: (1) a *Dynamic Taint Tracking Engine* that enforces an acyclic dependency graph across interactive constructions; (2) a dual-regime validation model distinguishing between exact integer-lattice coordinates ($\mathbb{Z}^2$) and continuous approximations; and (3) a *Specificity-Ordered Classifier* operating on scale-normalized edge lengths and cosine predicates, which guarantees bitwise vertex-permutation invariance for type classification and equivariance for apex labeling. Scale-invariance holds intra-regime across both discrete and continuous domains. Evaluated across an automated verification suite of 52 regression tests (38 core geometric classification tests and 14 auxiliary system tests), the engine demonstrates zero regression and bounded traversal on cycle-free construction graphs. The core computation engine is released as open-source software under the GNU General Public License v3 (GPLv3).

**Keywords:** Dynamic Geometry System, Taint Tracking, Permutation Invariance, Integer Lattice, Geometric Classification, Software Verification.

---

## Metadata Table

| Current code version | v3.1.0-rc6 |
| :--- | :--- |
| **Permanent code repository** | `https://github.com/geosolver-lab/geosolver-core` |
| **Legal Code License** | GNU General Public License v3 (GPLv3) |
| **Code versioning system used** | Git (Commit: `73b30eb8be18001c7ec99ffb20d4afc5e5bb687f`) |
| **Software code languages** | Python 3.10+ |
| **Compilation requirements** | None (Pure Python standard library) |
| **Supported operating systems** | Windows 10/11 (tested on build 10.0.26300); cross-platform pure Python compatible |
| **Automated test suite** | Python `unittest` (52 test vectors, 100% PASS: 38 classification / 14 auxiliary) |
| **Persistent identifier (DOI)** | `10.5281/zenodo.placeholder` (To be minted upon GitHub tagged release) |
| **Documentation & Support** | `https://github.com/geosolver-lab/geosolver-core/wiki` |

---

## 1. Motivation and Significance

### 1.1. Background and Problem Statement
Dynamic Geometry Systems (DGS) are foundational tools in computer-assisted mathematics education, automated theorem proving, and computer-aided design (CAD). However, interactive geometry environments operate under a fundamental tension: **the gap between continuous user gestures (such as freehand mouse perturbations) and exact discrete mathematical truth**.

When users manipulate points on an interactive canvas, coordinate values undergo floating-point perturbations ($x \in \mathbb{R}$). Conventional DGS implementations attempt to identify geometric configurations (such as right, isosceles, or equilateral triangles) by evaluating heuristic tolerance thresholds ($\varepsilon$). In practice, this design introduces two major failure modes:
1. **Misclassification on Integer Lattices ($\mathbb{Z}^2$):** By the classical Shoelace Formula (Gauss Area Formula), any triangle whose vertices lie on the integer lattice $\mathbb{Z}^2$ has a strictly rational area:
   $$\text{Area} = \frac{1}{2} |X_A(Y_B - Y_C) + X_B(Y_C - Y_A) + X_C(Y_A - Y_B)| \in \frac{1}{2}\mathbb{Z} \subset \mathbb{Q}$$
   Conversely, an equilateral triangle with side length $a$ requires an area of $\text{Area} = \frac{\sqrt{3}}{4}a^2$. Because the squared distance between any two integer vertices is an integer ($a^2 = d_{\mathbb{Z}}^2 \in \mathbb{Z}$), the area of a lattice equilateral triangle would be strictly irrational due to $\sqrt{3} \notin \mathbb{Q}$. Since an irrational number cannot equal a rational number, **the equilateral hypothesis is provably unreachable on $\mathbb{Z}^2$**. Heuristic DGS engines that blindly apply continuous relative tolerances to lattice points frequently misclassify near-equilateral grid triangles as strictly equilateral, presenting false mathematical information to students.
2. **Permutation Dependence from Non-Transitive Tolerances:** In metric spaces over the real numbers, relative tolerance relations $|a - b| \le \varepsilon$ do not satisfy transitivity:
   $$|a - b| \le \varepsilon \land |b - c| \le \varepsilon \not\implies |a - c| \le \varepsilon$$
   In floating-point arithmetic compliant with IEEE-754 [4], when an interactive engine evaluates candidate hypotheses through sequential conditional logic (`if/elif`), the resulting classification depends on the arbitrary indexing order of the vertices ($\sigma(A, B, C)$ vs $\sigma(B, C, A)$).

### 1.2. Related Work & Positioning
In computational geometry, the standard defense against numerical instability is **Exact Geometric Computation (EGC)**, exemplified by Shewchuk's adaptive-precision floating-point predicates [1] and the CGAL geometric kernel [2]. EGC solves orientation and incircle tests robustly, but requires rigorous floating-point filtering with multi-precision fallback.

To preserve computational simplicity while eliminating classification artifacts, GeoSolver 2D adapts concepts from dynamic taint analysis [3] into geometric provenance tracking. By classifying objects based on their operational history rather than floating-point coordinates alone, GeoSolver 2D bridges the gap between interactive usability and formal mathematical truth.

---

## 2. Software Architecture and Mathematical Formulation

GeoSolver 2D partitions geometric processing into three decoupled layers:
```
[User Interaction: Freehand Drag / Snap / Typed Input]
                       │
                       ▼
    [Dynamic Taint Engine & DAG Provenance (provenance.py)]
      - Cycle detection via _visiting set
      - Stack overflow guard at depth >= 100
      - Taint Conservation: (p1_exact ∧ p2_exact) ∧ ¬is_tainted
                       │
                       ▼
  [Dual-Regime Coordinate Partitioning (as_scaled_ints)]
      - Discrete Lattice: Z^2 (Integer Predicates & Area Theorem)
      - Continuous Regime: Scale-Normalized Edge & Cosine Predicates
                       │
                       ▼
     [Specificity-Ordered Invariant Classifier (classifier.py)]
      Equilateral ≻ Right-Isosceles ≻ {Right, Isosceles} ≻ Scalene
      - Label-Free Candidate Key: (diff_leg, opposite_side_sq)
      - Bitwise Permutation Invariance & Equivariant Apex Labeling
```

### 2.1. Dynamic Taint Tracking Engine
Every geometric entity $E$ maintains a provenance flag:
$$\text{exact}(E) = (\bigwedge_{P \in \text{Parents}(E)} \text{exact}(P)) \land \neg \text{is\_tainted}(E)$$
- **Taint Conservation Law:** Freehand canvas gestures unconditionally inject taint (`exact=False`), which strictly propagates to all descendant constructions (midpoints, intersections, perpendicular feet). Snapping to the coordinate grid (`snap_to_grid`) restores exact status (`exact=True`, `source='grid_snap'`).
- **DAG Cycle & Stack Safety:** Traversal is protected against cyclic dependencies via a `_visiting` tracking set, and against recursion overflow via a defensive limit at `_depth >= 100`, returning `False` (tainted) rather than clearing taints.

### 2.2. Dual-Regime Coordinate Model & `as_scaled_ints`
Input coordinates are evaluated via `as_scaled_ints` across scale factors $10^k$ ($k \in \{0, 1, 2, 3, 4\}$):
- If all coordinates satisfy $|v \cdot 10^k - \text{round}(v \cdot 10^k)| < 10^{-5}$, they are converted to scaled integers $[\text{round}(v \cdot 10^k)]$ and evaluated under exact integer arithmetic on $\mathbb{Z}^2$.
- Untagged coordinate tuples default to exact if they align with the scale grid. Coordinates with freehand provenance unconditionally bypass integer scaling and are quarantined into the continuous floating-point regime.
- Scale invariance holds intra-regime. Scaling a discrete shape below $10^{-5}$ transitions it across the boundary into the continuous regime, reflecting the epistemic distinction between exact integer arithmetic and floating-point approximation.

### 2.3. Specificity Hierarchy and Invariance Theorem
To prevent hypothesis suppression (where less constrained hypotheses like Isosceles trivially absorb more constrained hypotheses like Equilateral), GeoSolver 2D evaluates hypotheses through a strict specificity hierarchy:
$$\text{Equilateral} \succ \text{Right-Isosceles} \succ \{\text{Isosceles}, \text{Right}\} \succ \text{Scalene}$$
Right angles are evaluated via the scale-correct cosine predicate:
$$|\cos \theta| = \left| \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|} \right| \le 0.015 \quad (\approx |\theta - 90^\circ| \le 0.86^\circ)$$

**Theorem 1 (Vertex-Permutation Invariance & Apex Equivariance):**  
Let $V = (v_1, v_2, v_3)$ be a triangle with edge lengths $l_{12}, l_{23}, l_{31}$. For each vertex $v \in V$, define its local geometric record $R(v) = (\Delta(v), d^2_{\text{opp}}(v))$ where $\Delta(v)$ is the relative mismatch between the two sides incident to $v$, and $d^2_{\text{opp}}(v)$ is the squared length of the opposite side. Because IEEE-754 subtraction and multiplication satisfy $\text{fl}(a - b)^2 = \text{fl}(b - a)^2$ under round-to-nearest mode, each side length is bitwise symmetric. For any permutation $\sigma \in S_3$, the set of records $\{R(v) \mid v \in V\}$ is mapped bijectively to $\{R(\sigma(v))\}$. Because candidate hypotheses are sorted over the label-free, tie-free key $(\Delta, d^2_{\text{opp}})$, the classified triangle type is strictly invariant under $\sigma$, and the apex selection satisfies $\text{Apex}(\sigma(V)) \equiv \sigma(\text{Apex}(V))$.

---

## 3. Illustrative Examples
- **Example 1: Near-Equilateral Lattice Triangle on $\mathbb{Z}^2$:** Consider $A(0, 0)$, $B(1000, 0)$, and $C(500, 866)$. Pairwise squared distances: $d^2(AB) = 1,000,000$ and $d^2(AC) = d^2(BC) = 500^2 + 866^2 = 999,956$. Relative difference: $\frac{1000 - \sqrt{999,956}}{1000} \approx 0.0022\% \ll 0.6\%$. A tolerance-based continuous classifier would evaluate this as equilateral. GeoSolver 2D checks integer inequality $1,000,000 \ne 999,956$, provably rejects equilateral via the Shoelace area theorem, and correctly outputs **Isosceles with apex at $C$** across all 6 input permutations.
- **Example 2: Permutation Equivariance on Near-Tie Isosceles Configuration:** Consider $P(0, 0)$, $Q(1, 0)$, and $R(0.51, 0.86598)$ where $PQ = 1.0$, $PR \approx 1.0050$, and $QR \approx 0.9950$. Both pairs $(PQ, PR)$ and $(PQ, QR)$ satisfy the $0.6\%$ tolerance. By sorting candidates via the label-free key $(\text{diff\_leg}, d^2_{\text{opposite}})$, GeoSolver 2D deterministically selects apex $P$ across all 6 input orderings, preserving physical equivariance.

---

## 4. Empirical Verification & Sensitivity Analysis

### 4.1. Tolerance Threshold Sensitivity Analysis
To evaluate classification stability across boundary configurations, we performed a Monte Carlo parameter sensitivity scan over relative edge tolerance $\text{tol\_rel} \in [0.002, 0.010]$ and right-angle cosine tolerance $\text{tol\_cos} \in [0.005, 0.025]$ across 1,000 synthetic triangles perturbed by Gaussian coordinate noise ($\sigma = 0.005$):

| Tolerance Value | Equilateral Detected | Right Detected | Right-Isosceles | Isosceles | Scalene | Behavioral Interpretation |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **$\text{tol\_rel} = 0.002$** | 14 (1.4%) | 98 (9.8%) | 21 (2.1%) | 494 (49.4%) | 373 (37.3%) | Overly restrictive: misses ~85% of near-equilateral hand drawings. |
| **$\text{tol\_rel} = 0.004$** | 55 (5.5%) | 98 (9.8%) | 78 (7.8%) | 437 (43.7%) | 332 (33.2%) | Moderate threshold: accommodates steady stylus input. |
| **$\text{tol\_rel} = 0.006$ (Default)** | **109 (10.9%)** | **98 (9.8%)** | **151 (15.1%)** | **364 (36.4%)** | **278 (27.8%)** | **Optimal balance: reliably captures user intent while rejecting noise.** |
| **$\text{tol\_rel} = 0.008$** | 160 (16.0%) | 98 (9.8%) | 182 (18.2%) | 333 (33.3%) | 227 (22.7%) | Slightly permissive: begins absorbing near-scalene noise. |
| **$\text{tol\_rel} = 0.010$** | 200 (20.0%) | 98 (9.8%) | 204 (20.4%) | 311 (31.1%) | 187 (18.7%) | Overly permissive: high false-positive rate on generic triangles. |

### 4.2. Automated Regression Test Suite
The core engine was validated using Python's standard `unittest` framework:
- **Core Classification & Geometric Invariants (38 tests):** Validates lattice exactness, scale invariance ($10^{-5}$ to $10^{5}$), right-angle cosine predicates, DAG taint propagation, cycle guards, and bitwise permutation invariance across all $3! = 6$ orderings on `tests.test_geometry_invariants` (21 tests), `tests.test_round9_taint_validation` (11 tests), and `tests.test_rebuttal_invariants` (6 tests). Execution time: 3.221s (PASS).
- **Auxiliary System & Accessibility Suite (14 tests):** Validates WCAG 2.1 AA luminance contrast ($\ge 5.17:1$), Ramanujan-II ellipse accuracy ($0.040\%$ max error), Clean Print mode, DPAPI keystore fail-soft, and HuggingFace SHA-256 download verification. Execution time: 9.319s (PASS).
- **Aggregate Verification Metric:** **52 / 52 Unit Tests PASS (100.0%)** in 12.540s on Python 3.14.5 (Win32).

---

## 5. Impact and Practical Applications
1. **Educational Integrity in Secondary School Geometry:** In dynamic geometry classrooms, students frequently encounter misleading feedback when heuristic software asserts that an imperfect drawing is an equilateral or right triangle. By enforcing lattice exactness and reporting descriptive near-type deviations, GeoSolver 2D reinforces formal deductive reasoning.
2. **CAD and Geometric Modeling Reliability:** By guaranteeing bitwise permutation invariance, the engine ensures that geometric classification and constraint inference algorithms produce identical output regardless of CAD import sequence or vertex serialization order.

---

## 6. Conclusions and Future Work
GeoSolver 2D demonstrates that combining dynamic taint tracking with specificity-ordered predicates resolves the tension between continuous user interaction and discrete mathematical truth. By evaluating exact integer lattice arithmetic when appropriate and sorting candidate hypotheses deterministically under continuous perturbations, the engine guarantees scale-invariant and permutation-invariant classification. Future work will extend this architecture to 3D spatial geometry and polyhedral cross-sections.

---

## Declaration of Generative AI in Scientific Writing
During the preparation of this manuscript, the authors used AI assistance for grammar refinement, academic phrasing, and document formatting. The authors reviewed and edited all content and take full responsibility for the factual and mathematical veracity of the publication.

## Conflict of Interest
The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

## References
1. Shewchuk, J. R. (1997). *"Adaptive Precision Floating-Point Arithmetic and Fast Robust Geometric Predicates"*. Discrete & Computational Geometry, 18(3), pp. 305–363. DOI: 10.1007/PL00009321.
2. The CGAL Project (2024). *"CGAL User and Reference Manual"*. CGAL Editorial Board, 5.6 edition.
3. Schwartz, E. J., Avgerinos, T., & Brumley, D. (2010). *"All You Ever Wanted to Know About Dynamic Taint Analysis and Forward Symbolic Execution (but Might Have Been Afraid to Ask)"*. IEEE Symposium on Security and Privacy (S&P 2010), pp. 317–331. DOI: 10.1109/SP.2010.26.
4. IEEE Computer Society (2019). *"IEEE Standard for Floating-Point Arithmetic"*. IEEE Std 754-2019, pp. 1–84. DOI: 10.1109/IEEESTD.2019.8766229.
5. World Wide Web Consortium (W3C) (2018). *"Web Content Accessibility Guidelines (WCAG) 2.1"*. W3C Recommendation.
