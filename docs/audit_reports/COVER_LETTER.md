**Bao-Trung Nguyen**  
Independent Researcher  
Ho Chi Minh City, Vietnam  
Email: trungyds16@gmail.com  
ORCID: https://orcid.org/0009-0009-5780-3385  

November 15, 2026

**The Editors-in-Chief**  
*SoftwareX*  
Elsevier B.V.  

**Subject: Submission of Original Software Publication — "GeoSolver 2D: A Provenance-Aware Dynamic Geometry Engine with Dual-Regime and Permutation-Invariant Classification"**

Dear Editors-in-Chief,

I am pleased to submit our original software manuscript titled **"GeoSolver 2D: A Provenance-Aware Dynamic Geometry Engine with Dual-Regime and Permutation-Invariant Classification"** for consideration as an **Original Software Publication (OSP)** in *SoftwareX*.

### Motivation and Alignment with SoftwareX Scope
Interactive Dynamic Geometry Systems (DGS) are widely utilized in educational mathematics, computer-aided design (CAD), and constraint inference. However, existing interactive geometry environments face a fundamental mathematical challenge: **the tension between continuous, imperfect user gestures (such as stylus/mouse drawing) and exact discrete mathematical truth**. 

Conventional systems employ heuristic floating-point tolerance thresholds ($\varepsilon$). In practice, this design introduces two widespread failure modes:
1. **Misclassification on Integer Lattices ($\mathbb{Z}^2$):** By the Shoelace area theorem, any lattice triangle on $\mathbb{Z}^2$ has a strictly rational area, whereas an equilateral triangle has an irrational area ($\frac{\sqrt{3}}{4}a^2 \notin \mathbb{Q}$). Heuristic tolerance checks frequently misclassify near-regular lattice triangles as strictly equilateral, presenting mathematically incorrect feedback to students.
2. **Permutation Dependence:** Because metric relative tolerances are non-transitive, sequential conditional logic produces outputs that depend on arbitrary vertex enumeration order ($\sigma(A, B, C)$ vs. $\sigma(B, C, A)$).

### Software Architecture and Algorithmic Contributions
GeoSolver 2D was specifically engineered to resolve these numerical artifacts through an open-source, lightweight, and mathematically robust kernel:
- **Dynamic Taint Tracking Engine (`provenance.py`):** Enforces a strict Taint Conservation Law over an interactive Directed Acyclic Graph (DAG). Using an iterative topological post-order traversal with cycle tracking and explicit set memoization, the engine eliminates exponential re-expansions on shared-ancestor diamond structures, achieving proven and benchmarked linear $O(V+E)$ execution complexity with stack safety up to 2,000 nodes.
- **Dual-Regime Validation Model (`as_scaled_ints`):** Partitions input coordinates across scale factors $10^k$ ($k \in \{0, 1, 2, 3, 4\}$). Coordinates aligning with the discrete scale grid are evaluated via exact integer arithmetic on $\mathbb{Z}^2$, while freehand gestures are quarantined in the continuous regime until explicitly snapped to grid.
- **Specificity-Ordered Invariant Classifier (`classifier.py`):** Organizes candidate evaluation through a strict hierarchy ($\text{Equilateral} \succ \text{Right-Isosceles} \succ \{\text{Isosceles}, \text{Right}\} \succ \text{Scalene}$) and sorts candidate keys over label-free metrics. We formally prove and verify bitwise vertex-permutation invariance for triangle classification and strict equivariance for apex labeling under all $3! = 6$ vertex permutations.

### Verification, Reproducibility, and Open Science
The software has undergone thorough automated verification:
- **Comprehensive Test Suite:** 62 automated unit tests (27 headless CI tests and 35 GUI integration tests) achieve a **100% pass rate** in under 0.02 seconds for the core computational kernel.
- **Synthetic Sensitivity Benchmark:** Evaluated on a 1,000-sample canonical prototype suite perturbed by Gaussian coordinate jitter, achieving 91.4% overall classification accuracy and 100% precision on regular shapes, with 0% false positives on integer-lattice triples.
- **Zero Heavy Dependencies:** Implemented in pure Python 3.10+ standard library, requiring no external C/C++ compilation, multi-precision wrappers, or complex third-party frameworks.
- **Permanent Open-Source Archive:** The software is released under the GNU General Public License v3 (GPLv3). The complete code repository is publicly hosted on GitHub at `https://github.com/trungyds16-coder/geosolver-core` (Release tag: `v3.2.1`), and permanently archived on Zenodo with DOI: `10.5281/zenodo.24249595`.

### Author Declaration and Ethical Compliance
- This manuscript describes original software and has not been published previously, nor is it under consideration for publication elsewhere.
- All algorithms, proofs, unit tests, and empirical benchmarks were independently developed, validated, and verified by the author.
- The author has disclosed all relevant background, commercial distributions, and declarations of interest in accordance with Elsevier editorial guidelines.

Thank you very much for your time, consideration, and management of the peer-review process.

Sincerely,

**Bao-Trung Nguyen**  
Independent Researcher  
Ho Chi Minh City, Vietnam  
Email: trungyds16@gmail.com  
ORCID: https://orcid.org/0009-0009-5780-3385
