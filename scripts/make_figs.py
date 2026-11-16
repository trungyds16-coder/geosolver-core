"""
Reproducible Script to Generate Figures for GeoSolver 2D Manuscript:
- Figure 2: Schematic of Example 1 (lattice triangle on Z^2)
- Figure 3: Sensitivity Analysis and Hard-Negative Stress Test (from Tables 2 & 3)
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def generate_figure_example1(output_dir: str):
    """Generates Figure 2: Example 1 schematic and classification comparison."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=300,
                                   gridspec_kw={"width_ratios": [1.1, 1.0]})
    
    # Panel (a): Triangle geometry on Z^2
    A = np.array([0, 0])
    B = np.array([1000, 0])
    C = np.array([500, 866])
    
    tri = np.array([A, B, C, A])
    ax1.plot(tri[:, 0], tri[:, 1], "k-", lw=2.5)
    ax1.plot([A[0], B[0], C[0]], [A[1], B[1], C[1]], "ko", markersize=7)
    
    ax1.text(A[0] - 20, A[1] - 60, "A(0, 0)", fontsize=11, ha="right", va="top")
    ax1.text(B[0] + 20, B[1] - 60, "B(1000, 0)", fontsize=11, ha="left", va="top")
    ax1.text(C[0], C[1] + 40, "C(500, 866)", fontsize=11, ha="center", va="bottom")
    
    # Edge labels
    ax1.text(500, -70, "$d^2(AB) = 1{,}000{,}000$", fontsize=10, ha="center", va="top")
    ax1.text(200, 470, "$d^2(AC) = 999{,}956$", fontsize=10, ha="right", va="center", rotation=60)
    ax1.text(800, 470, "$d^2(BC) = 999{,}956$", fontsize=10, ha="left", va="center", rotation=-60)
    
    ax1.set_xlim(-150, 1150)
    ax1.set_ylim(-150, 1000)
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_title("(a) Integer-lattice input", fontsize=12, pad=15)
    
    # Panel (b): Classification outcome comparison
    ax2.axis("off")
    ax2.set_title("(b) Classification outcome", fontsize=12, pad=15)
    
    text_content = (
        "Edge mismatch: 0.0022%\n"
        "(well below the 0.6% tolerance)\n\n\n"
        "Tolerance-only classifier:\n\n"
        "   Equilateral  (false positive)\n\n\n"
        "GeoSolver 2D (exact regime):\n\n"
        "   Isosceles, apex C  (exact = True)\n"
        "   since 1,000,000 \u2260 999,956; identical\n"
        "   for all 6 vertex orderings"
    )
    
    ax2.text(0.05, 0.85, "Edge mismatch: 0.0022%\n(well below the 0.6% tolerance)",
             fontsize=10.5, va="top", fontfamily="sans-serif")
    
    ax2.text(0.05, 0.58, "Tolerance-only classifier:",
             fontsize=11, fontweight="bold", va="top", fontfamily="sans-serif")
    ax2.text(0.12, 0.48, "Equilateral  (false positive)",
             fontsize=10.5, va="top", fontfamily="sans-serif")
    
    ax2.text(0.05, 0.30, "GeoSolver 2D (exact regime):",
             fontsize=11, fontweight="bold", va="top", fontfamily="sans-serif")
    ax2.text(0.12, 0.20, "Isosceles, apex C  (exact = True)\nsince 1,000,000 \u2260 999,956; identical\nfor all 6 vertex orderings",
             fontsize=10.5, va="top", fontfamily="sans-serif")
    
    plt.tight_layout()
    pdf_path = os.path.join(output_dir, "fig_example1.pdf")
    png_path = os.path.join(output_dir, "fig_example1.png")
    plt.savefig(pdf_path, bbox_inches="tight")
    plt.savefig(png_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Generated {pdf_path} and {png_path}")


def generate_figure_sensitivity(output_dir: str):
    """Generates Figure 3: Sensitivity sweep from Tables 2 and 3."""
    tol_rel = [0.002, 0.004, 0.006, 0.008, 0.010]
    
    # Data from Table 2 & scan
    overall_acc = [62.9, 77.8, 91.4, 96.8, 98.5]
    eq_recall = [15.2, 47.6, 82.0, 92.8, 97.6]
    scalene_prec = [55.7, 72.5, 85.9, 94.7, 96.5]
    
    # Data from Table 3 (Combined FP Rate)
    hard_neg_fp = [0.0, 0.0, 0.0, 0.5, 18.0]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=300)
    
    # Panel (a): Continuous prototypes
    ax1.plot(tol_rel, overall_acc, "k-o", lw=2, markersize=7, label="Overall accuracy")
    ax1.plot(tol_rel, eq_recall, color="#555555", linestyle="--", marker="s", lw=2, markersize=7, label="Equilateral recall")
    ax1.plot(tol_rel, scalene_prec, color="#888888", linestyle=":", marker="^", lw=2, markersize=7, label="Scalene precision")
    
    ax1.axvline(0.006, color="#aaaaaa", linestyle="-.", lw=1.2)
    ax1.text(0.006, 5, "default 0.006", color="#666666", fontsize=9, ha="center")
    
    ax1.set_xlabel("relative tolerance tol_rel", fontsize=11)
    ax1.set_ylabel("percentage (%)", fontsize=11)
    ax1.set_title(r"(a) Continuous prototypes (N = 1,000, $\sigma$ = 0.03)", fontsize=11)
    ax1.set_ylim(0, 105)
    ax1.set_xticks(tol_rel)
    ax1.grid(True, linestyle=":", alpha=0.5)
    ax1.legend(loc="lower right", frameon=True, fontsize=9.5)
    
    # Panel (b): Hard negatives
    ax2.plot(tol_rel, hard_neg_fp, "k-o", lw=2, markersize=7)
    for x, y in zip(tol_rel, hard_neg_fp):
        ax2.annotate(f"{y:.1f}", (x, y), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=9.5)
        
    ax2.axvline(0.006, color="#aaaaaa", linestyle="-.", lw=1.2)
    ax2.set_xlabel("relative tolerance tol_rel", fontsize=11)
    ax2.set_ylabel("false-positive rate (%)", fontsize=11)
    ax2.set_title("(b) Hard negatives (N = 200, adversarial)", fontsize=11)
    ax2.set_ylim(-1, 21)
    ax2.set_xticks(tol_rel)
    ax2.grid(True, linestyle=":", alpha=0.5)
    
    plt.tight_layout()
    pdf_path = os.path.join(output_dir, "fig_sensitivity.pdf")
    png_path = os.path.join(output_dir, "fig_sensitivity.png")
    plt.savefig(pdf_path, bbox_inches="tight")
    plt.savefig(png_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Generated {pdf_path} and {png_path}")


if __name__ == "__main__":
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "audit_reports", "ELSEVIER_SUBMISSION_PACKAGE", "antigravity_audit"))
    os.makedirs(out_dir, exist_ok=True)
    generate_figure_example1(out_dir)
    generate_figure_sensitivity(out_dir)
