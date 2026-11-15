# GeoSolver 2D: A Provenance-Aware Dynamic Geometry Engine with Scale-Invariant and Permutation-Invariant Classification

**Authors:** Nguyen Van A$^1$, Tran Van B$^1$  
**Affiliation:** $^1$Laboratory of Applied Mathematics and Educational Technology, STEM Research Institute  
**Corresponding Author Email:** `author@geosolver.org`  
**Target Journal:** *SoftwareX* (Elsevier) — Original Software Publication (OSP)  

---

## Abstract
Interactive Dynamic Geometry Systems (DGS) are prone to geometric misclassifications when users construct or perturb configurations using freehand gestures. Floating-point rounding errors and non-transitive relative tolerances frequently lead to false-positive recognitions (such as misclassifying near-regular integer-lattice triangles as equilateral) or permutation-dependent outcomes (where the classified type depends on vertex enumeration order). We introduce **GeoSolver 2D**, an open-source, highly reliable geometry engine designed to eliminate these numerical artifacts. GeoSolver 2D implements: (1) a *Dynamic Taint Tracking Engine* that enforces an acyclic dependency graph across interactive constructions; (2) a dual-regime validation model distinguishing between exact integer-lattice coordinates ($\mathbb{Z}^2$) and continuous approximations; and (3) a *Specificity-Ordered Classifier* operating on sorted squared edge lengths $s_{(1)} \le s_{(2)} \le s_{(3)}$, which guarantees bitwise vertex-permutation invariance for type classification and equivariance for apex labeling. Evaluated across an automated verification suite of 52 regression tests, the engine demonstrates zero regression and bounded traversal on cycle-free construction graphs. The core computation engine is released as open-source software under the GNU General Public License v3 (GPLv3).

**Keywords:** Dynamic Geometry System, Taint Tracking, Permutation Invariance, Integer Lattice, Geometric Classification, Software Verification.

---

## Metadata Table

| Current code version | v3.1.0-rc5 |
| :--- | :--- |
| **Permanent code repository** | `https://github.com/geosolver-lab/geosolver-core` |
| **Legal Code License** | GNU General Public License v3 (GPLv3) |
| **Code versioning system used** | Git |
| **Software code languages** | Python 3.10+ |
| **Compilation requirements** | None (Pure Python standard library) |
| **Supported operating systems** | Windows 10/11 (tested on build 10.0.26300); cross-platform pure Python compatible |
| **Automated test suite** | Python `unittest` (52 test vectors, 100% PASS) |
| **Persistent identifier (DOI)** | `10.5281/zenodo.placeholder` (To be minted upon final GitHub tagged release) |
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

## 2. Software Architecture and Algorithmic Design

### 2.1. Dual-Regime Classification Model
GeoSolver 2D enforces an explicit mathematical partitioning between discrete integer lattice configurations and continuous approximations:
$$\text{exact} = \text{is\_discrete} \land \text{origin\_exact} \land (\neg \text{is\_tainted})$$
where:
$$\text{origin\_exact} = \bigwedge_{v \in V} \text{origin}(v) \quad \text{and} \quad \text{is\_tainted} = \bigvee_{v \in V} \text{tainted}(v)$$

1. **Discrete $\mathbb{Z}^2$ Lattice Regime:**
   - Active only when every vertex originated from integer coordinates or grid snapping and has never been perturbed by freehand dragging.
   - Coordinates are stored in a **Scaled-Integer Representation** $(X, Y, K) \in \mathbb{Z}^3$ such that $(x, y) = (X \cdot 10^{-K}, Y \cdot 10^{-K})$. Points with differing $K$ are aligned to $K_{\max} = \max(K_1, K_2, K_3)$ via $X' = X \cdot 10^{K_{\max} - K}$ prior to predicate evaluation.
   - Derived midpoints with rational coordinates remain exact on $\mathbb{Z}^2$ by scaling $K \leftarrow K + 1$. Constructed intersections of arbitrary lines can yield general rationals not representable by finite decimal scaling; in such events, coordinates naturally transition into the continuous regime.
   - All geometric predicates operate strictly over $\mathbb{Z}$ without floating-point representation drift:
     $$d_{\mathbb{Z}}^2(A, B) = (X_A - X_B)^2 + (Y_A - Y_B)^2 \in \mathbb{Z}$$
   - Triangles are classified via exact integer Pythagorean identities ($d_1^2 + d_2^2 == d_3^2$) and integer equality ($d_1^2 == d_2^2$). The equilateral branch is provably unreachable on $\mathbb{Z}^2$ via the Shoelace area theorem.
2. **Continuous Regime:**
   - Active when any vertex is tainted by freehand movement or possesses non-scaled coordinates.
   - Operates under a scale-normalized relative tolerance $\text{tol\_rel} = 0.006 \times l_{\max}$.
   - Degeneracy and collinearity are evaluated as a pre-classification stage prior to metric classification:
     $$\text{rel\_cross} = \frac{|\vec{u}_{AB} \times \vec{u}_{AC}|}{l_{\max}^2} < 10^{-5}$$
     where $l_{\max} = \max(d_{AB}, d_{BC}, d_{CA})$. For degenerate configurations where $l_{\max} < 10^{-12}$, the engine intercepts execution and returns `coincident` or `collinear`.

### 2.2. Dynamic Taint Tracking & Lattice Snapping
- **Taint Semantics:**
  Perturbing any constituent vertex freehand marks it as `tainted` (`source="dragged"`, `exact=False`), routing the entity into the continuous regime. When an ancestor mutates via mouse drag, descendant taint states are invalidated dynamically during DAG traversal. Snapping a point back onto the grid restores its exact status:
  $$X_{\text{new}} = \text{round}(x / \text{step}), \quad x_{\text{snapped}} = X_{\text{new}} \cdot \text{step}, \quad \text{source} = \text{"grid\_snap"}, \quad \text{exact} = \text{True}$$
- **Acyclic Dependency Enforcement:**
  Dependencies between points, midpoints, intersections, and projections form a strict Directed Acyclic Graph (DAG). Cycles are rejected upon construction (`child_id not in ancestry(parents)`).

### 2.3. Specificity-Ordered Classification & Canonical Invariance Proof
To prevent hypothesis suppression, candidate evaluation follows a strict **Hierarchy of Specificity**:
1. **Equilateral:** Evaluates extreme side lengths from sorted squared triple:
   $$s_{(3)} - s_{(1)} \le \text{tol\_rel} \cdot s_{(3)}$$
   Testing the extremes $s_{(3)}$ and $s_{(1)}$ avoids adjacent-pair tolerance chaining.
2. **Right-Isosceles:** Defined strictly as $\text{Right} \land \text{Isosceles}$:
   $$|s_{(1)} + s_{(2)} - s_{(3)}| \le 0.012 \cdot s_{(3)} \quad \land \quad (s_{(2)} - s_{(1)} \le \text{tol\_rel} \cdot s_{(2)} \lor s_{(3)} - s_{(2)} \le \text{tol\_rel} \cdot s_{(3)})$$
3. **Right:** Evaluates the Pythagorean residual on the extreme hypotenuse:
   $$|s_{(1)} + s_{(2)} - s_{(3)}| \le 0.012 \cdot s_{(3)}$$
4. **Isosceles:** Evaluates equal legs on adjacent sorted pairs:
   $$s_{(2)} - s_{(1)} \le \text{tol\_rel} \cdot s_{(2)} \quad \text{or} \quad s_{(3)} - s_{(2)} \le \text{tol\_rel} \cdot s_{(3)}$$
   When a triangle satisfies both Right and Isosceles independently, the conjunction promotes it deterministically to Right-Isosceles.
5. **Scalene:** Fallback when no geometric symmetry hypothesis is met.

**Theorem (Bitwise Permutation Invariance):**  
Let $\sigma \in S_3$ be any permutation of the vertex set $\{A, B, C\}$. Since the squared distance $d^2(P_i, P_j) = (x_i - x_j)^2 + (y_i - y_j)^2$ is bitwise symmetric under exchange of $P_i$ and $P_j$ (due to exact square symmetry in IEEE-754 arithmetic), the multiset of squared distances $\{\{d^2(\sigma(A), \sigma(B)), \dots\}\} \equiv \{\{d^2(A, B), \dots\}\}$ is invariant. Sorting this multiset yields a bitwise identical triple $\vec{s} = (s_{(1)}, s_{(2)}, s_{(3)})$ across all 6 permutations. Since the specificity classifier $F(\vec{s})$ operates strictly on $\vec{s}$, we have:
$$F(\sigma(A), \sigma(B), \sigma(C)) \equiv F(A, B, C), \quad \forall \sigma \in S_3$$
**Apex Equivariance:** The apex is identified by mapping the position of the unequal edge in $\vec{s}$ back to the corresponding original vertex index, ensuring $\text{Apex}(\sigma(V)) \equiv \sigma(\text{Apex}(V))$.

---

## 3. Illustrative Examples

### 3.1. Example 1: Near-Equilateral Lattice Triangle on $\mathbb{Z}^2$
Consider the integer-lattice triangle with vertices $A(0, 0)$, $B(1000, 0)$, and $C(500, 866)$.
- Pairwise squared distances:
  $$d^2(AB) = 1000^2 = 1,000,000$$
  $$d^2(AC) = 500^2 + 866^2 = 250,000 + 749,956 = 999,956$$
  $$d^2(BC) = (1000 - 500)^2 + (-866)^2 = 999,956$$
- Side length difference: $|AB - AC| = 1000 - \sqrt{999,956} \approx 1000 - 999.978 = 0.022$.  
  Relative difference: $\frac{0.022}{1000} = 0.0022\% \ll 0.6\%$.
- **Heuristic Continuous Classification:** Under standard proximity thresholds, $\Delta ABC$ is misclassified as equilateral ($AB \approx BC \approx CA$).
- **GeoSolver 2D Outcome:** All three vertices possess untainted integer provenance (`is_discrete = True`). The discrete engine tests integer equality $1,000,000 \ne 999,956$. By the Shoelace area theorem, equilateral classification is unreachable. The triangle is correctly identified as **Isosceles with apex at $C$**, reporting descriptive residual note `(near equilateral, deviation 0.002%)`.

### 3.2. Example 2: Permutation Equivariance on Isosceles Configuration
Consider vertices $A(0.0, 0.0)$, $B(10.0, 0.0)$, and $C(5.0, 7.0)$ where $AC = BC = \sqrt{74} \approx 8.6023$, and base $AB = 10.0$.
- Under all $6$ permutations ($\sigma \in S_3$), the sorted squared distance triple is identically $\vec{s} = (74, 74, 100)$.
- The specificity engine deterministically identifies the type as `isosceles` (invariance) and assigns the apex to vertex $C$ (equivariance), preserving the physical vertex identity under all orderings.

---

## 4. Empirical Verification & Sensitivity Analysis

### 4.1. Tolerance Threshold Sensitivity Analysis
To evaluate classification stability across boundary configurations, we performed a parameter sensitivity scan over relative tolerance $\text{tol\_rel} \in [0.002, 0.010]$ and collinearity ratio $\text{rel\_cross} \in [10^{-6}, 10^{-4}]$ across 1,000 perturbed triangle configurations:

| Parameter | Tested Range | Default | Stability / Boundary Impact |
| :--- | :---: | :---: | :--- |
| **`tol_rel`** (Relative Edge Tolerance) | $0.2\% - 1.0\%$ | $0.6\%$ ($0.006$) | Thresholds below $0.4\%$ reject hand-drawn isosceles triangles; thresholds above $0.8\%$ absorb near-scalene noise. $0.6\%$ provides optimal balance. |
| **`tol_pyth`** (Right Angle Tolerance) | $0.005 - 0.020$ | $0.012$ | Corresponds to angular deviation $\approx 0.7^\circ$ around $90^\circ$. |
| **`rel_cross`** (Collinearity Area Ratio) | $10^{-6} - 10^{-4}$ | $10^{-5}$ | Accurately discriminates sliver triangles ($l_{\min} / l_{\max} > 0.01$) from degenerate collinear points. |

### 4.2. Automated Regression Test Suite
The core engine was validated using Python's standard `unittest` framework:
- **`tests.test_geometry_invariants` (35 tests):** Validates lattice exactness, scale invariance ($10^{-5}$ to $10^{5}$), Ramanujan-II ellipse accuracy ($0.040\%$ max error), WCAG 2.1 AA luminance contrast [5] ($\ge 5.17:1$), and permutation invariance across all 6 orderings. Execution time: $9.319\text{s}$ (PASS).
- **`tests.test_round9_taint_validation` (11 tests):** Validates input boundary sanitation (`NaN`, `Inf` rejection) and DAG taint propagation. Execution time: $0.002\text{s}$ (PASS).
- **`tests.test_claude_round12_cases` (6 tests):** Validates exact lattice classification and apex equivariance across all $3! = 6$ permutations for Example 1, Example 2, 3-4-5 right, unit right-isosceles, scalene, and continuous near-tie configurations. Execution time: $0.001\text{s}$ (PASS).
- **Aggregate Verification Metric:** **52 / 52 Unit Tests PASS (100.0%)**.

---

## 5. Impact and Practical Applications

GeoSolver 2D addresses a critical pedagogical and software quality challenge in STEM education:
1. **Educational Integrity in Secondary School Geometry:** In dynamic geometry classrooms, students frequently encounter misleading feedback when heuristic software asserts that an imperfect drawing is an equilateral or right triangle. By enforcing lattice exactness and reporting descriptive near-type deviations, GeoSolver 2D reinforces formal deductive reasoning.
2. **CAD and Geometric Modeling Reliability:** By guaranteeing bitwise permutation invariance, the engine ensures that geometric classification and constraint inference algorithms produce identical output regardless of CAD import sequence or vertex serialization order.

---

## 6. Conclusions and Future Work

GeoSolver 2D demonstrates that combining dynamic taint tracking with specificity-ordered predicates on sorted squared edge triples resolves the tension between continuous user interaction and discrete mathematical truth. By evaluating exact integer lattice arithmetic when appropriate and falling back to canonical multiset sorting under continuous perturbations, the engine guarantees scale-invariant and permutation-invariant classification. Future work will extend this architecture to 3D spatial geometry and polyhedral cross-sections.

---

## Declaration of Generative AI in Scientific Writing
During the preparation of this manuscript, the authors used AI assistance for grammar refinement, academic phrasing, and document formatting. The authors reviewed and edited all content and take full responsibility for the factual and mathematical veracity of the publication.

---

## Conflict of Interest
The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

---

## References
1. Shewchuk, J. R. (1997). *"Adaptive Precision Floating-Point Arithmetic and Fast Robust Geometric Predicates"*. Discrete & Computational Geometry, 18(3), pp. 305–363. DOI: 10.1007/PL00009321.
2. The CGAL Project (2024). *"CGAL User and Reference Manual"*. CGAL Editorial Board, 5.6 edition.
3. Schwartz, E. J., Avgerinos, T., & Brumley, D. (2010). *"All You Ever Wanted to Know About Dynamic Taint Analysis and Forward Symbolic Execution (but Might Have Been Afraid to Ask)"*. IEEE Symposium on Security and Privacy (S&P 2010), pp. 317–331. DOI: 10.1109/SP.2010.26.
4. IEEE Computer Society (2019). *"IEEE Standard for Floating-Point Arithmetic"*. IEEE Std 754-2019, pp. 1–84. DOI: 10.1109/IEEESTD.2019.8766229.
5. World Wide Web Consortium (W3C) (2018). *"Web Content Accessibility Guidelines (WCAG) 2.1"*. W3C Recommendation.
