# GeoSolver 2D: A Provenance-Aware Dynamic Geometry Engine with Dual-Regime and Permutation-Invariant Classification

**Author:** Bao-Trung Nguyen$^1$  
**Affiliation:** $^1$Independent Researcher, Ho Chi Minh City, Vietnam  
**Corresponding Author Email:** `trungyds16@gmail.com`  
**Target Journal:** *SoftwareX* (Elsevier) — Original Software Publication (OSP)  

---

## Abstract
Interactive Dynamic Geometry Systems (DGS) are prone to geometric misclassifications when users construct or perturb configurations using freehand gestures. Floating-point rounding errors and non-transitive relative tolerances frequently lead to false-positive recognitions (such as misclassifying near-regular integer-lattice triangles as equilateral) or permutation-dependent outcomes (where the classified type depends on vertex enumeration order). We introduce **GeoSolver 2D**, an open-source geometry engine designed to remove these numerical artifacts in triangle classification. GeoSolver 2D implements: (1) a *Dynamic Taint Tracking Engine* that enforces an acyclic dependency graph across interactive constructions using an iterative topological traversal with explicit stack safety and strictly linear $O(V+E)$ complexity; (2) a dual-regime validation model distinguishing between exact integer-lattice coordinates ($\mathbb{Z}^2$) and continuous approximations; and (3) a *Specificity-Ordered Classifier* operating on scale-normalized edge lengths and cosine predicates, which guarantees bitwise vertex-permutation invariance for type classification and equivariance for apex labeling. Scale-invariance holds unconditionally within the continuous regime, with explicit provenance tagging preventing artificial scale-induced transitions. Evaluated across an automated verification suite of 62 regression tests (27 headless core library tests and 35 desktop integration tests) and an empirical benchmark suite achieving 91.4% accuracy on canonical prototypes, the engine demonstrates bitwise permutation invariance, strict apex equivariance, and bounded linear $O(V+E)$ traversal on cycle-free construction graphs. The core computation engine is released as open-source software under the GNU General Public License v3 (GPLv3).

**Keywords:** Dynamic Geometry System, Taint Tracking, Permutation Invariance, Integer Lattice, Geometric Classification, Software Verification.

---

## Metadata Table

| Current code version | v3.2.1 |
| :--- | :--- |
| **Permanent code repository** | `https://github.com/trungyds16-coder/geosolver-core` |
| **Legal Code License** | GNU General Public License v3 (GPLv3) |
| **Code versioning system used** | Git (Release tag: `v3.2.1`) |
| **Software code languages** | Python 3.10+ |
| **Compilation requirements** | None (Pure Python standard library) |
| **Supported operating systems** | Windows 10/11, Linux (Ubuntu 22.04+), macOS; CI tested via GitHub Actions |
| **Automated test suite** | Python `unittest` (27 headless CI tests, 35 GUI integration tests, 100% PASS) |
| **Persistent identifier (DOI)** | `10.5281/zenodo.14889201` |
| **Documentation & Support** | `https://github.com/trungyds16-coder/geosolver-core` |

---

## 1. Motivation and Significance

### 1.1. Background and Problem Statement
Dynamic Geometry Systems (DGS) are foundational tools in computer-assisted mathematics education, automated theorem proving, and computer-aided design (CAD). However, interactive geometry environments operate under a fundamental tension: **the gap between continuous user gestures (such as freehand mouse perturbations) and exact discrete mathematical truth**.

When users manipulate points on an interactive canvas, coordinate values undergo floating-point perturbations ($x \in \mathbb{R}$). Conventional DGS implementations attempt to identify geometric configurations (such as right, isosceles, or equilateral triangles) by evaluating heuristic tolerance thresholds ($\varepsilon$). In practice, this design introduces two major failure modes:
1. **Misclassification on Integer Lattices ($\mathbb{Z}^2$):** By the classical Shoelace Formula (Gauss Area Formula), any triangle whose vertices lie on the integer lattice $\mathbb{Z}^2$ has a strictly rational area:
   $$\text{Area} = \frac{1}{2} |X_A(Y_B - Y_C) + X_B(Y_C - Y_A) + X_C(Y_A - Y_B)| \in \frac{1}{2}\mathbb{Z} \subset \mathbb{Q}$$
   Conversely, an equilateral triangle with side length $a$ requires an area of $\text{Area} = \frac{\sqrt{3}}{4}a^2$. Because the squared distance between any two integer vertices is an integer ($a^2 = d_{\mathbb{Z}}^2 \in \mathbb{Z}$), the area of a lattice equilateral triangle would be strictly irrational due to $\sqrt{3} \notin \mathbb{Q}$. Since an irrational number cannot equal a rational number, **the equilateral hypothesis is provably unreachable on $\mathbb{Z}^2$**. Heuristic DGS engines that blindly apply continuous relative tolerances to lattice points can misclassify near-equilateral grid triangles as strictly equilateral, which may give students incorrect mathematical feedback.
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
      - Stack overflow guard at depth >= 100 (non-memoizing cutoff)
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
- **Taint Conservation Law:** Freehand canvas gestures unconditionally inject taint (`exact=False`), which strictly propagates to all descendant constructions (midpoints, intersections, perpendicular feet). Snapping to the coordinate grid (`snap_to_grid`) restores exact integer status (`exact=True`, `source='grid_snap'`). Stored flags on derived entities are never trusted over dynamic parent state.
- **DAG Cycle Safety & Stack Safety:** Traversal is protected against cyclic dependencies via an active `_visiting` tracking set. Traversal is evaluated iteratively via an explicit stack (topological post-order DFS), eliminating recursion depth limits and guaranteeing strict traversal-order invariance across subtrees.

### 2.2. Dual-Regime Coordinate Model & `as_scaled_ints`
Input coordinates are evaluated via `as_scaled_ints` across scale factors $10^k$ ($k \in \{0, 1, 2, 3, 4\}$):
- If all coordinates satisfy $|v \cdot 10^k - \text{round}(v \cdot 10^k)| < 10^{-5}$, they are converted to scaled integers $[\text{round}(v \cdot 10^k)]$ and evaluated under exact integer arithmetic on $\mathbb{Z}^2$.
- Untagged coordinate tuples default to exact if they align with the scale grid. Coordinates with freehand provenance unconditionally bypass integer scaling and are quarantined into the continuous floating-point regime until explicitly snapped to grid.
- **Dual-Regime Scale Transitions:** For untagged inputs, uniform coordinate scaling can transition shapes across regime boundaries: $P(0,0), Q(1,0), R(0.51, 0.86598)$ has 5 decimal places and evaluates in the continuous regime as isosceles (`exact=False`). Magnified by $\times 10$, $R'(5.1, 8.6598)$ has 4 decimal places, which aligns with the $k=4$ discrete scale grid and is evaluated over $\mathbb{Z}^2$ as a distinct scalene configuration (`exact=True`). In contrast, when vertices carry freehand provenance tags (`exact=False`), the Taint Conservation Law quarantines them into the continuous regime until explicitly snapped to grid, preserving classification invariance across arbitrary magnifications.

### 2.3. Specificity Hierarchy and Invariance Theorem
To prevent hypothesis suppression (where less constrained hypotheses like Isosceles trivially absorb more constrained hypotheses like Equilateral), GeoSolver 2D evaluates hypotheses through a strict specificity hierarchy:
$$\text{Equilateral} \succ \text{Right-Isosceles} \succ \{\text{Isosceles}, \text{Right}\} \succ \text{Scalene}$$
Right angles are evaluated via the scale-correct cosine predicate:
$$|\cos \theta| = \left| \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|} \right| \le 0.015 \quad (\approx |\theta - 90^\circ| \le 0.86^\circ)$$

**Theorem 1 (Vertex-Permutation Invariance & Apex Equivariance):**  
Let $V = (v_1, v_2, v_3)$ be a triangle with edge lengths $l_{12}, l_{23}, l_{31}$. For each vertex $v \in V$, define its local geometric record $R(v) = (\Delta(v), d^2_{\text{opp}}(v))$ where $\Delta(v)$ is the relative mismatch between the two sides incident to $v$, and $d^2_{\text{opp}}(v)$ is the squared length of the opposite side. Because IEEE-754 subtraction and multiplication satisfy $\text{fl}(a - b)^2 = \text{fl}(b - a)^2$ under round-to-nearest mode, each side length is bitwise symmetric. For any permutation $\sigma \in S_3$, the set of records $\{R(v) \mid v \in V\}$ is mapped bijectively to $\{R(\sigma(v))\}$. Because candidate hypotheses are sorted over the label-free key $(\Delta, d^2_{\text{opp}})$, the classified triangle type is strictly invariant under $\sigma$, and the apex selection satisfies $\text{Apex}(\sigma(V)) \equiv \sigma(\text{Apex}(V))$. In the discrete regime, two apex candidates can tie on opposite squared length $d^2_{\text{opp}}$ if and only if all three sides are equal ($a^2 = b^2 = c^2$); because equilateral configurations are unreachable on $\mathbb{Z}^2$ (Shoelace area formula), candidate keys are strictly unique. In the continuous regime, two non-winning candidates can tie on the candidate key if and only if their opposite sides are bitwise equal; however, the winning apex candidate is strictly unique because the third vertex then has leg mismatch $\Delta = 0$ and strictly wins the candidate sort. Equilateral configurations are resolved at the highest specificity level without apex labeling.

---

## 3. Illustrative Examples
- **Example 1: Near-Equilateral Lattice Triangle on $\mathbb{Z}^2$:** Consider $A(0, 0)$, $B(1000, 0)$, and $C(500, 866)$. Pairwise squared distances: $d^2(AB) = 1,000,000$ and $d^2(AC) = d^2(BC) = 500^2 + 866^2 = 999,956$. Relative difference: $\frac{1000 - \sqrt{999,956}}{1000} \approx 0.0022\% \ll 0.6\%$. A tolerance-based continuous classifier would evaluate this as equilateral. GeoSolver 2D checks integer inequality $1,000,000 \ne 999,956$, provably rejects equilateral via the Shoelace area theorem, and correctly outputs **Isosceles with apex at $C$** across all 6 input permutations.
- **Example 2: Permutation Equivariance on Near-Tie Isosceles Configuration:** Consider $P(0, 0)$, $Q(1, 0)$, and $R(0.51, 0.86598)$ where $PQ = 1.0$, $PR \approx 1.0050$, and $QR \approx 0.9950$. Both pairs $(PQ, PR)$ and $(PQ, QR)$ satisfy the $0.6\%$ tolerance. By sorting candidates via the label-free key $(\text{diff\_leg}, d^2_{\text{opposite}})$, GeoSolver 2D deterministically selects apex $P$ across all 6 input orderings, preserving physical equivariance.

---

## 4. Empirical Verification & Sensitivity Analysis

### 4.1. Canonical Benchmark, Parameter Sensitivity & Stress Tests
To evaluate tolerance sensitivity against input perturbations, we generated a reproducible benchmark dataset of 1,000 synthetic triangles (250 each of ground-truth Equilateral, Isosceles, Right, and Scalene prototypes) using `scripts/sensitivity_benchmark.py` (`seed = 42`) perturbed by Gaussian coordinate jitter ($\sigma = 0.03$, 0.3% of nominal edge length 10.0). Table 1 measures the tolerance-versus-noise performance on these continuous prototypes:

| Triangle Class | Ground Truth | True Positive (TP) | Recall (%) | Precision (%) | F1-Score (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Equilateral** | 250 | 205 | 82.0% | 100.0% | 90.1% |
| **Isosceles** | 250 | 212 | 84.8% | 82.5% | 83.6% |
| **Right** | 250 | 247 | 98.8% | 100.0% | 99.4% |
| **Scalene** | 250 | 250 | 100.0% | 85.9% | 92.4% |
| **Overall Dataset** | **1,000** | **914** | **91.4%** | **91.4%** | **91.4%** |

*Empirical sensitivity scan across relative edge tolerance $\text{tol\_rel} \in [0.002, 0.010]$:*
- $\text{tol\_rel} = 0.002$: Overall = 62.9%, Equilateral Recall = 15.2%, Precision = 100.0%, Scalene Precision = 55.7% (overly restrictive; rejects valid hand-drawn regular shapes).
- $\text{tol\_rel} = 0.004$: Overall = 77.8%, Equilateral Recall = 47.6%, Precision = 100.0%, Scalene Precision = 72.5%.
- $\text{tol\_rel} = 0.006$ (Default): Overall = 91.4%, Equilateral Recall = 82.0%, Precision = 100.0%, Scalene Precision = 85.9% (practical operational balance for interactive stylus/freehand drawing).
- $\text{tol\_rel} = 0.008$: Overall = 96.8%, Equilateral Recall = 92.8%, Precision = 100.0%, Scalene Precision = 94.7%.
- $\text{tol\_rel} = 0.010$: Overall = 98.5%, Equilateral Recall = 97.6%, Precision = 100.0%, Scalene Precision = 96.5%.

*Hard Negatives Stress Test (Near-Boundary Asymmetric Triangles):*  
To evaluate robustness against near-boundary false positives across distinct geometric families, we evaluated 200 near-boundary scalene triangles (100 near-isosceles with side mismatch drawn from $0.8\%–1.5\%$, and 100 near-right with angles in $[88.0^\circ, 88.8^\circ]$ where $|\cos \theta| \in [0.021, 0.035]$):

| $\text{tol\_rel}$ | Near-Iso FP ($N=100$) | Near-Right FP ($N=100$) | Total Scalene TN ($N=200$) | Total FP ($N=200$) | Combined FP Rate (%) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 0.002 | 0/100 | 0/100 | 200/200 | 0/200 | 0.0% |
| 0.004 | 0/100 | 0/100 | 200/200 | 0/200 | 0.0% |
| 0.006 (Default) | 0/100 | 0/100 | 200/200 | 0/200 | 0.0% |
| 0.008 | 1/100 | 0/100 | 199/200 | 1/200 | 0.5% |
| 0.010 | 36/100 | 0/100 | 164/200 | 36/200 | 18.0% |

This empirical behavior directly reflects the underlying geometric design: false positives in the near-isosceles family only begin to emerge as $\text{tol\_rel}$ enters and exceeds the $0.8\%–1.5\%$ perturbation band (1/100 at 0.008, 36/100 at 0.010), while the 100 near-right scalene configurations produce 0/100 false positives across all tolerance levels because the orthogonal classifier employs a decoupled fixed angular bound ($|\cos \theta| \le 0.015$, corresponding to $[89.14^\circ, 90.86^\circ]$).

*Empirical Invariance & Dual-Regime Comparative Baselines:*
1. **Permutation Equivariance vs. Naive Classifier:** Across 200 near-tie configurations under all $3! = 6$ permutations, a naive positional `if/elif` classifier exhibited **100.0% apex-variant outcomes** (200/200), whereas GeoSolver 2D achieved **0.0% variance** (0/200), strictly preserving apex equivariance.
2. **Lattice Exactness on $\mathbb{Z}^2$:** On integer lattice triples (including near-equilateral configurations such as $(0,0), (1000,0), (500,866)$), a standard continuous tolerance classifier suffered a **75.0% false-positive rate** (3/4) by incorrectly asserting equilateral geometry. GeoSolver 2D's discrete regime correctly proved non-existence of equilateral triangles on $\mathbb{Z}^2$ with **0.0% false positives** (0/4).
3. **Decimal Lattice Sweep ($k \in \{1, 2, 3, 4\}$):** Across 496 non-collinear candidate pairs evaluated on decimal-scaled lattices where float squared lengths drift at $10^{-16}$, GeoSolver 2D's discrete integer kernel achieved **100.0% exact recognition** (496/496: 490 isosceles + 6 right-isosceles, all exact: True with apex at $A$).

### 4.2. Automated Regression Test Suite
The codebase was verified using Python's standard `unittest` framework:
- **Headless Core Library Suite (27 tests):** Pure Python standard library, zero GUI dependencies. Automatically executed on GitHub Actions CI across Ubuntu, Windows, and macOS on Python 3.10–3.13. Covers discrete integer arithmetic on decimal lattices, Shoelace area assertions, intra-regime scale invariance, apex equivariance under all 6 permutations, adversarial near-tie test vectors, DAG taint conservation, cycle safety, deep DAG order-independence, stack safety up to 2,000 nodes, 25-level diamond ladder traversal with strict $O(V+E)$ complexity (verified via deterministic visit counter: 52 evaluated nodes), and integer return types on grid snapping. Execution time: **0.019s** (PASS).
- **Desktop GUI Canvas Integration Suite (35 tests):** Covers Tkinter canvas event handling, mouse drag snapping, undo/redo instance rebinding, and WCAG 2.1 AA luminance contrast. Execution time: **10.826s** (PASS).
- **Aggregate Local Verification Metric:** **62 / 62 Unit Tests PASS (100.0%)**. The isolated execution of the two suites sums to 10.845s (0.019s headless core CI suite + 10.826s desktop integration suite). When evaluated via a single unified discovery pass (`python -m unittest discover tests`), the run completed in **17.060s**, where the remaining ~6.2s reflects test discovery, test runner process startup, and module import overhead.
- **Cross-Platform Verification:** Automated CI pipeline (`.github/workflows/ci.yml`) executes across `ubuntu-latest`, `windows-latest`, and `macos-latest` on Python 3.10 through 3.13.

---

## 5. Impact and Practical Applications

GeoSolver 2D addresses a specific, well-defined gap: interactive geometry tools that classify freehand or lattice-based triangles using tolerance heuristics can return results that depend on vertex order or that contradict exact arithmetic. By making classification permutation-invariant and by evaluating integer-lattice inputs exactly, the engine is designed to give consistent, mathematically defensible feedback in two settings:

1. **Educational Geometry Software:** Tolerance-based recognition can label an imperfect drawing as equilateral or right-angled. GeoSolver 2D is intended to reduce such misleading feedback by separating exact lattice inputs from freehand inputs and by reporting near-type deviations descriptively. Its effect on learning has not yet been evaluated.
2. **Geometric Modelling Pipelines:** Because the classifier is invariant to vertex ordering, its output does not depend on import or serialization order, which simplifies testing and reproducibility in tools that infer constraints from point sets.
3. **Current Use and Limitations:** The educational edition has been distributed through the Microsoft Store. No classroom study has been conducted; this release focuses on the correctness and reproducibility of the core engine. Evaluating the effect on students’ reasoning, and usability with teachers, is planned future work. The core library is a dependency-free Python package under GPLv3, so it can be reused and extended independently of the desktop application.

---

## 6. Conclusions and Future Work
GeoSolver 2D demonstrates that combining dynamic taint tracking with specificity-ordered predicates addresses the tension between continuous user interaction and discrete mathematical truth. By evaluating exact integer lattice arithmetic when appropriate and sorting candidate hypotheses deterministically under continuous perturbations, the engine guarantees intra-regime scale invariance and permutation-invariant classification. The present work validates the classification engine through unit tests and synthetic benchmarks; classroom evaluation remains future work. Future developments will also explore extending this architecture to 3D spatial geometry and polyhedral cross-sections.

---

## Declaration of Generative AI in Scientific Writing
During the preparation and development of this work, the author utilized generative AI assistants (Claude by Anthropic and Gemini by Google) for code refactoring, test generation, mathematical invariant verification, grammar refinement, and editorial structuring. The iterative review rounds conducted with AI models served as rigorous internal design audits and red-teaming exercises; they do not substitute for formal journal peer review. The author independently verified, executed, and validated all algorithms, mathematical proofs, test suites, and empirical benchmarks, and takes full responsibility for the factual and mathematical veracity of this publication.

## Conflict of Interest
The author develops and distributes educational dynamic geometry software, including packaged distributions of GeoSolver on the Microsoft Store. The core mathematical algorithms, classification engine, and provenance tracking system described in this paper are released as free and open-source software under the GNU General Public License v3 (GPLv3) without commercial restrictions.

## Author Biography
**Bao-Trung Nguyen** received his degree in Pharmacy from the University of Medicine and Pharmacy at Ho Chi Minh City in 2021. With over five years of professional experience in pharmaceutical research and development (R&D), his current research interests include computational geometry, scientific software engineering, dynamic geometry systems, and robust arithmetic algorithms. He currently conducts scientific research as an independent researcher in Ho Chi Minh City, Vietnam.

## References
1. Shewchuk, J. R. (1997). *"Adaptive Precision Floating-Point Arithmetic and Fast Robust Geometric Predicates"*. Discrete & Computational Geometry, 18(3), pp. 305–363. DOI: 10.1007/PL00009321.
2. The CGAL Project (2024). *"CGAL User and Reference Manual"*. CGAL Editorial Board, 5.6 edition.
3. Schwartz, E. J., Avgerinos, T., & Brumley, D. (2010). *"All You Ever Wanted to Know About Dynamic Taint Analysis and Forward Symbolic Execution (but Might Have Been Afraid to Ask)"*. IEEE Symposium on Security and Privacy (S&P 2010), pp. 317–331. DOI: 10.1109/SP.2010.26.
4. IEEE Computer Society (2019). *"IEEE Standard for Floating-Point Arithmetic"*. IEEE Std 754-2019, pp. 1–84. DOI: 10.1109/IEEESTD.2019.8766229.
5. World Wide Web Consortium (W3C) (2018). *"Web Content Accessibility Guidelines (WCAG) 2.1"*. W3C Recommendation.
