# AUTHOR REBUTTAL & POINT-BY-POINT RESPONSE TO REFEREE REPORT
## MANUSCRIPT: GEOSOLVER 2D (SUBMISSION TO ELSEVIER SOFTWARX)
### AUDIT ROUND 12 REBUTTAL — DATED NOVEMBER 15, 2026

We sincerely thank the Lead Peer Reviewer for this remarkably thorough, constructive, and mathematically precise referee report. Every critical observation has pinpointed a genuine vulnerability or missing contextual element in our previous submission. We have fully embraced all recommendations and systematically revised both our implementation architecture and the manuscript text.

Below is our item-by-item response detailing the exact technical resolutions implemented.

---

### ITEM 1: EXACTNESS PREDICATE & TAINT CONSERVATION CONTRADICTION
> **Referee Critique:** *Exactness predicate contradicts the Taint Conservation Law. Section 2.1 uses `(origin_exact ∨ points_exact) ∧ ¬is_tainted`, but §2.2 says any tainted vertex taints the entity. An OR here lets an entity be exact when only one input class is exact.*

**Author Response & Fix:**  
The Referee is entirely correct. The disjunction (`∨`) was an erroneous formulation from an earlier draft that supported mixed legacy annotations. In strict accordance with the Taint Conservation Law:
$$\text{exact} = \text{is\_discrete} \land \text{origin\_exact} \land (\neg \text{is\_tainted})$$
where:
$$\text{origin\_exact} = \bigwedge_{v \in V} \text{origin}(v) \quad \text{and} \quad \text{is\_tainted} = \bigvee_{v \in V} \text{tainted}(v)$$
An entity is admitted into the exact discrete regime if and only if **all** constituent vertices have verified lattice or typed origin, and **zero** constituent vertices possess a drag/taint history. The manuscript (§2.1) and code have been updated accordingly.

---

### ITEM 2: DEPTH TRUNCATION, TAINT-WASHING & DAG CYCLE PROTECTION
> **Referee Critique:** *Depth truncation can reintroduce taint-washing. `_point_flag` cuts off at `depth ≥ 8`... returning near cutoff memoized can make results traversal-order dependent. A DAG has no cycles by definition; a depth limit of 8 misclassifies legitimate deep constructions.*

**Author Response & Fix:**  
We completely concede this point. An arbitrary depth threshold ($\ge 8$) is unsound for deep geometric constructions (e.g., Euler line or 9-point circle dependencies) and creates order-dependent memoization pollution.
1. **Elimination of Arbitrary Depth Bound:** The hard cutoff `depth >= 8` has been eliminated.
2. **True Cycle Guard:** Because construction dependencies must form a strict DAG, cycles are explicitly forbidden at mutation time. When an entity declares parents, a traversal asserts `child_id not in ancestry(parents)`.
3. **Topological Order Memoization:** Taint status is propagated along the topological ordering of the DAG. Since the graph is strictly acyclic, memoization is now keyed strictly by immutable entity ID (`memo[entity_id] = is_exact`) without depth dependence, ensuring complete traversal-order invariance.

---

### ITEM 3: "EXACT" LATTICE RECOGNITION WITH FLOATS & EPSILON TOLERANCE
> **Referee Critique:** *“Exact” lattice recognition with floats. `round(x/step)*step` with `step = 0.1` yields `0.30000000000000004`... putting a tolerance back inside the “exact” regime. Store snapped coordinates as integers or Fractions.*

**Author Response & Fix:**  
This is a critical insight. Storing decimal floats inevitably introduces IEEE-754 representation noise ($0.1_{10} = 0.000110011..._2$), requiring an ad-hoc tolerance ($\epsilon = 10^{-5}$) inside what claimed to be an "exact" regime.
**Implemented Solution: Scaled-Integer Representation $(X, Y, K) \in \mathbb{Z}^3$:**
When a point is snapped to a grid of step $10^{-K}$ (e.g., step 0.1, 0.5, 1.0):
$$x = X \cdot 10^{-K}, \quad y = Y \cdot 10^{-K} \quad \text{where } X, Y, K \in \mathbb{Z}$$
- For grid step 0.1: $0.3$ is stored as $X = 3, Y = ..., K = 1$.
- All distance comparisons and collinearity checks in the discrete regime are performed **exclusively over $\mathbb{Z}$**:
  $$d_{\mathbb{Z}}^2(A, B) = (X_A - X_B)^2 + (Y_A - Y_B)^2 \in \mathbb{Z}$$
  $$\text{Cross}_{\mathbb{Z}} = (X_B - X_A)(Y_C - Y_A) - (Y_B - Y_A)(X_C - X_A) \in \mathbb{Z}$$
This completely purges floating-point epsilon checks from the discrete regime: $\text{Cross}_{\mathbb{Z}} == 0$ is an exact algebraic integer identity. Float coordinates are derived strictly at display/render time.

---

### ITEM 4: PERMUTATION INVARIANCE VS. EQUIVARIANCE & DETERMINISTIC TIE-BREAKS
> **Referee Critique:** *The permutation-invariance proof is asserted, not proved. The $\forall \sigma \in S_3$ identity needs a deterministic, label-independent tie-break... symmetric evaluation order for deviation (avoiding 1 ULP flips from atan2/acos)... and a clear distinction between invariance (type) and equivariance (apex labels).*

**Author Response & Fix:**  
We thank the Referee for distinguishing between **Invariance** and **Equivariance**:
1. **Mathematical Formulation:**
   - **Type Classification is Strictly Invariant:**  
     $$\text{Type}(\sigma(V)) = \text{Type}(V), \quad \forall \sigma \in S_3$$
   - **Apex / Vertex Assignment is Equivariant:**  
     $$\text{Apex}(\sigma(V)) = \sigma(\text{Apex}(V))$$
2. **Elimination of Trigonometric Functions (`acos`, `atan2`):**  
   All angular deviations are now evaluated via the rational Law of Cosines:
   $$\cos \theta_k = \frac{s_i + s_j - s_k}{2 \sqrt{s_i s_j}} \quad \text{where } s = d^2$$
   Differences from target angles ($\pi/2, \pi/3$) are tested via algebraic squared residuals ($(\cos \theta - \cos \theta_{\text{target}})^2$), eliminating 1-ULP trigonometric transcendental noise.
3. **Deterministic Lexicographical Tie-Breaking:**  
   When two candidate hypotheses evaluate to identical residuals within numerical machine precision ($|\chi_1^2 - \chi_2^2| < \text{EPS}$), candidate selection breaks ties via the canonical lexicographical order of the canonically sorted global vertex IDs (`(id_A, id_B, id_C)`).

---

### ITEM 5: AD-HOC DEVIATION METRIC & DIMENSIONAL INCONSISTENCY
> **Referee Critique:** *The deviation metric is ad hoc. $|l_1 - l_2|/\max$ adds a dimensionless length ratio to an angle in radians, and $\theta_{\text{target}}$ differs per candidate type... use a single normalized residual per hypothesis.*

**Author Response & Fix:**  
We have discarded the ad-hoc sum. In the revised manuscript (§2.3), candidate hypotheses $H \in \{\text{Equilateral}, \text{Right-Isosceles}, \text{Isosceles}, \text{Right}\}$ are scored via a unified, dimensionless, normalized squared residual (Chi-squared metric):
$$\chi^2(H) = \sum_{(i,j) \in \text{Edges}(H)} \left( \frac{d_{ij} - \bar{d}}{\bar{d}} \right)^2 + \sum_{k \in \text{Angles}(H)} \left( \frac{\cos \theta_k - \cos \theta_k^*}{2} \right)^2$$
Where $\bar{d}$ is the mean hypothesized edge length and $\cos \theta_k^*$ is the target cosine ($0$ for $90^\circ$, $1/2$ for $60^\circ$). Both length and angular deviations are strictly bounded in $[0, 1]$ and normalized by theoretical degrees of freedom.

---

### ITEM 6: PROOFS, OVERCLAIMING & THRESHOLD SENSITIVITY
> **Referee Critique:** *No equilateral triangle in $\mathbb{Z}^2$ is cleaner via Shoelace (Pick not needed). Saying engines "violate" theorems is wrong (say misclassify). 0.006 and $10^{-5}$ need sensitivity analysis. "Zero stack-overflow" cannot be established by 46 tests.*

**Author Response & Fix:**  
1. **Shoelace Area Proof Adopted:** Pick's theorem has been replaced with the direct, elegant Shoelace formula:
   $$\text{Area} = \frac{1}{2} |X_A(Y_B - Y_C) + X_B(Y_C - Y_A) + X_C(Y_A - Y_B)| \in \frac{1}{2}\mathbb{Z} \subset \mathbb{Q}$$
   Since an equilateral triangle with edge $a$ requires $\text{Area} = \frac{\sqrt{3}}{4}a^2$, and $a^2 = d_{\mathbb{Z}}^2 \in \mathbb{Z}$, the area is irrational ($\sqrt{3} \notin \mathbb{Q}$). An irrational number cannot equal a rational number. Q.E.D.
2. **Terminology Hardened:** All instances of "violates Pick's theorem" have been corrected to "misclassifies configurations". "Zero stack-overflow vulnerabilities" has been revised to "bounded recursive traversal on verified cycle-free DAGs".
3. **Threshold Sensitivity Analysis:** Added empirical sensitivity data for $\text{tol\_rel} \in [0.001, 0.010]$ and collinearity area ratio $\in [10^{-6}, 10^{-4}]$ on boundary degenerate slivers.

---

### ITEM 7: RELATED WORK & EXACT GEOMETRIC COMPUTATION (EGC)
> **Referee Critique:** *Related work is absent. Position against Exact Geometric Computation: Shewchuk’s adaptive-precision predicates, CGAL, and interval arithmetic. Provenance via Cheney et al. concerns database lineage; cite taint-analysis literature.*

**Author Response & Fix:**  
A dedicated *Related Work* section (§1.2) has been added to the manuscript:
- **Exact Geometric Computation (EGC):** We discuss Shewchuk's robust adaptive-precision floating-point predicates (1997) and CGAL's exact coordinate representation kernels. We explain why interactive DGS platforms cannot run pure arbitrary-precision EGC across continuous 60 FPS mouse-dragging loops without noticeable lag, thus justifying our hybrid approach: *Dynamic Taint Tracking* filters when to invoke exact integer lattice algebra vs. normalized continuous tolerance sorting.
- **Taint Analysis Literature:** We replaced the database-centric Cheney citation with classical software security and compiler taint propagation literature (Schwartz et al., *All You Ever Wanted to Know About Dynamic Taint Analysis and Forward Symbolic Execution*, IEEE S&P 2010).

---

### ITEM 8: REQUIRED SECTIONS & SOFTWARX METADATA TABLE
> **Referee Critique:** *SoftwareX structure. Required sections missing: Illustrative examples, Impact, Conclusions, and Code Metadata Table (Zenodo DOI, OSI license). Justify open-core.*

**Author Response & Fix:**  
All mandatory SoftwareX components have been fully integrated:
1. **Illustrative Examples (§3):** Two detailed walkthroughs: (a) False-positive elimination on a near-equilateral grid triangle ($AB=1000, AC=1010$), showing discrete branch integer rejection; (b) Permutation equivariance on an arbitrary triangle under all 6 cyclic permutations.
2. **Impact (§4):** Analysis of educational and CAD implications, eliminating erroneous geometric feedback in secondary education software.
3. **Conclusions (§5):** Summary of contributions and future extension to 3D solid geometry.
4. **Software Metadata Table:** Complete table containing repository link, Zenodo DOI (`10.5281/zenodo.14163920`), GNU GPLv3 license, Python language specification.
5. **Open-Core Justification:** Explicitly clarified that the scientific software described in the paper is the standalone core library `geosolver-core`, which is 100% open-source under GPLv3, independent of the commercial desktop wrapper.

---

### ITEM 9 & MINOR ITEMS: TELEMETRY, REFERENCES, AND CLEANUP
> **Referee Critique:** *8 installs is anecdotal; remove Reference 5 (DPAPI); remove quartile from title; collinearity area ratio behavior on slivers.*

**Author Response & Fix:**  
1. **Telemetry:** The 8 installs / 41 views metric is explicitly labeled as a *preliminary deployment sanity check* demonstrating executable integrity on Windows Store, not a statistical educational study.
2. **Removed DPAPI & Quartile:** The unrelated DPAPI citation and the journal quartile/indexing claims on the title page have been completely deleted.
3. **Collinearity on Slivers:** Added explicit clarification: $\frac{|\vec{u} \times \vec{v}|}{l_{\max}^2} < 10^{-5}$ represents the ratio of parallelogram area to square of maximum edge length, equivalent to the sine of the minimum altitude angle. For near-coincident points ($l_{\max} < 10^{-9}$), the engine intercepts early and classifies as `degenerate`.
