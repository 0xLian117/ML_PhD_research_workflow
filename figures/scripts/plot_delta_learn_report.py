"""Generate publication-quality figures for delta_learn project report.

Produces 4 figures:
1. Baseline method comparison (bar chart)
2. Model scaling curves (pretrain + finetune)
3. Data scaling curves (pretrain + finetune)
4. Per-horizon IC comparison (line chart)
"""

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
from scientific_figure_pro import (
    apply_publication_style, create_subplots, finalize_figure,
    PALETTE, FigureStyle,
)

OUT_DIR = Path(__file__).parent.parent  # figures/

# ============================================================================
# Data — all from experiment results
# ============================================================================

# --- Baseline (long-horizon finetune IC) ---
BASELINE_METHODS = ["B2\nPT→FT", "B3\nE2E", "B4\nFactor", "B5\nStat", "FS1\nFactor-L", "S1\nSpectral"]
BASELINE_IC = [0.0669, 0.0532, 0.0550, 0.0123, 0.0565, 0.0018]
BASELINE_RANKIC = [0.0704, 0.0549, 0.0613, 0.0101, 0.0617, 0.0021]
IC_THRESHOLD = 0.015

# --- Per-horizon IC (finetune) ---
HORIZONS = [60, 120, 360, 600, 1200, 1800]
HORIZON_LABELS = ["30s", "1m", "3m", "5m", "10m", "15m"]
PER_HORIZON = {
    "B2 PT→FT":    [0.1406, 0.1028, 0.0532, 0.0426, 0.0330, 0.0292],
    "B3 E2E":      [0.1125, 0.0864, 0.0387, 0.0298, 0.0258, 0.0262],
    "B4 Factor":   [0.1226, 0.0876, 0.0354, 0.0302, 0.0292, 0.0250],
    "B5 Stat":     [0.0226, 0.0228, 0.0040, 0.0054, 0.0105, 0.0088],
}

# --- Model Scaling ---
MS_PARAMS = [87e3, 322e3, 2.3e6, 17.4e6]
MS_LABELS = ["87K\n(MS1)", "322K\n(MS2)", "2.3M\n(MS3)", "17.4M\n(MS4)"]
MS_PT_IC = [0.2974, 0.2963, 0.2974, 0.2985]
MS_FT_IC = [np.nan, 0.0669, 0.0677, 0.0678]  # MS1-ft missing

# --- Data Scaling ---
DS_SAMPLES_PT = [260e3, 1.3e6, 5.2e6]
DS_SAMPLES_FT = [23e3, 117e3, 468e3]
DS_LABELS = ["2×2yr\n(DS1)", "5×4yr\n(DS2)", "10×8yr\n(DS3)"]
DS_PT_IC = [0.2160, 0.2620, 0.2963]
DS_FT_IC = [0.0214, 0.0522, 0.0669]


def fig1_baseline_comparison():
    """Bar chart: Baseline method IC comparison."""
    apply_publication_style(FigureStyle(font_size=15, axes_linewidth=2.2))
    fig, axes = create_subplots(1, 1, figsize=(10, 5.5))
    ax = axes[0]

    x = np.arange(len(BASELINE_METHODS))
    width = 0.35

    bars_ic = ax.bar(x - width/2, BASELINE_IC, width, label="IC",
                     color=PALETTE["blue_main"], edgecolor="white", lw=0.8)
    bars_ric = ax.bar(x + width/2, BASELINE_RANKIC, width, label="Rank IC",
                      color=PALETTE["teal"], edgecolor="white", lw=0.8)

    # Threshold line
    ax.axhline(y=IC_THRESHOLD, color=PALETTE["red_strong"], linestyle="--",
               lw=1.5, alpha=0.7, label=f"|IC| threshold = {IC_THRESHOLD}")

    # Annotate IC values
    for bar, val in zip(bars_ic, BASELINE_IC):
        if val > 0.005:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                    f"{val:.4f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(BASELINE_METHODS, fontsize=11)
    ax.set_ylabel("IC / Rank IC")
    ax.set_title("Baseline Method Comparison (Val IC, Long Horizons)", loc="left", fontweight="bold")
    ax.set_ylim(0, 0.085)
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(axis="y", alpha=0.2, linestyle="--")

    finalize_figure(fig, OUT_DIR / "delta_learn_baseline_comparison", formats=["png", "pdf"], dpi=300)


def fig2_model_scaling():
    """Dual-panel: Model scaling for pretrain and finetune."""
    apply_publication_style(FigureStyle(font_size=14, axes_linewidth=2.2))
    fig, axes = create_subplots(1, 2, figsize=(13, 5))

    # Panel A: Pretrain
    ax = axes[0]
    ax.semilogx(MS_PARAMS, MS_PT_IC, "o-", color=PALETTE["blue_main"],
                lw=2.5, ms=9, mec="white", mew=1.5, zorder=3)
    for i, (p, ic) in enumerate(zip(MS_PARAMS, MS_PT_IC)):
        ax.annotate(f"{ic:.4f}", (p, ic), textcoords="offset points",
                    xytext=(0, 12), ha="center", fontsize=10, fontweight="bold")
    ax.set_xlabel("Total Parameters")
    ax.set_ylabel("Val IC (mean)")
    ax.set_title("A. Pretrain — Model Scaling", loc="left", fontweight="bold")
    ax.set_ylim(0.290, 0.305)
    ax.grid(alpha=0.2, linestyle="--")
    # Custom x ticks
    ax.set_xticks(MS_PARAMS)
    ax.set_xticklabels(["87K", "322K", "2.3M", "17.4M"], fontsize=10)

    # Panel B: Finetune
    ax = axes[1]
    ft_params = [322e3, 2.3e6, 17.4e6]
    ft_ic = [0.0669, 0.0677, 0.0678]
    ax.semilogx(ft_params, ft_ic, "s-", color=PALETTE["red_strong"],
                lw=2.5, ms=9, mec="white", mew=1.5, zorder=3)
    for i, (p, ic) in enumerate(zip(ft_params, ft_ic)):
        ax.annotate(f"{ic:.4f}", (p, ic), textcoords="offset points",
                    xytext=(0, 12), ha="center", fontsize=10, fontweight="bold")
    ax.axhline(y=IC_THRESHOLD, color=PALETTE["neutral"], linestyle="--", lw=1.2, alpha=0.6)
    ax.set_xlabel("Total Parameters")
    ax.set_ylabel("Val IC (mean)")
    ax.set_title("B. Finetune — Model Scaling", loc="left", fontweight="bold")
    ax.set_ylim(0.060, 0.075)
    ax.grid(alpha=0.2, linestyle="--")
    ax.set_xticks(ft_params)
    ax.set_xticklabels(["322K", "2.3M", "17.4M"], fontsize=10)

    fig.tight_layout(pad=2)
    finalize_figure(fig, OUT_DIR / "delta_learn_model_scaling", formats=["png", "pdf"], dpi=300)


def fig3_data_scaling():
    """Dual-panel: Data scaling for pretrain and finetune."""
    apply_publication_style(FigureStyle(font_size=14, axes_linewidth=2.2))
    fig, axes = create_subplots(1, 2, figsize=(13, 5))

    # Panel A: Pretrain
    ax = axes[0]
    ax.semilogx(DS_SAMPLES_PT, DS_PT_IC, "o-", color=PALETTE["blue_main"],
                lw=2.5, ms=9, mec="white", mew=1.5, zorder=3)
    for p, ic, lbl in zip(DS_SAMPLES_PT, DS_PT_IC, DS_LABELS):
        ax.annotate(f"{ic:.4f}", (p, ic), textcoords="offset points",
                    xytext=(0, 12), ha="center", fontsize=10, fontweight="bold")
    ax.set_xlabel("Pretrain Samples")
    ax.set_ylabel("Val IC (mean)")
    ax.set_title("A. Pretrain — Data Scaling", loc="left", fontweight="bold")
    ax.set_ylim(0.19, 0.32)
    ax.grid(alpha=0.2, linestyle="--")
    ax.set_xticks(DS_SAMPLES_PT)
    ax.set_xticklabels(["260K", "1.3M", "5.2M"], fontsize=10)

    # Panel B: Finetune
    ax = axes[1]
    ax.semilogx(DS_SAMPLES_FT, DS_FT_IC, "s-", color=PALETTE["red_strong"],
                lw=2.5, ms=9, mec="white", mew=1.5, zorder=3)
    for p, ic, lbl in zip(DS_SAMPLES_FT, DS_FT_IC, DS_LABELS):
        ax.annotate(f"{ic:.4f}", (p, ic), textcoords="offset points",
                    xytext=(0, 12), ha="center", fontsize=10, fontweight="bold")
    ax.axhline(y=IC_THRESHOLD, color=PALETTE["neutral"], linestyle="--", lw=1.2, alpha=0.6,
               label=f"|IC| = {IC_THRESHOLD}")
    ax.set_xlabel("Finetune Samples")
    ax.set_ylabel("Val IC (mean)")
    ax.set_title("B. Finetune — Data Scaling", loc="left", fontweight="bold")
    ax.set_ylim(0.0, 0.08)
    ax.grid(alpha=0.2, linestyle="--")
    ax.legend(fontsize=10)
    ax.set_xticks(DS_SAMPLES_FT)
    ax.set_xticklabels(["23K", "117K", "468K"], fontsize=10)

    fig.tight_layout(pad=2)
    finalize_figure(fig, OUT_DIR / "delta_learn_data_scaling", formats=["png", "pdf"], dpi=300)


def fig4_per_horizon_ic():
    """Line chart: Per-horizon IC for key methods."""
    apply_publication_style(FigureStyle(font_size=14, axes_linewidth=2.2))
    fig, axes = create_subplots(1, 1, figsize=(9, 5.5))
    ax = axes[0]

    colors = {
        "B2 PT→FT": PALETTE["blue_main"],
        "B3 E2E": PALETTE["teal"],
        "B4 Factor": PALETTE["violet"],
        "B5 Stat": PALETTE["neutral"],
    }
    markers = {
        "B2 PT→FT": "o",
        "B3 E2E": "s",
        "B4 Factor": "D",
        "B5 Stat": "^",
    }

    x = np.arange(len(HORIZONS))
    for method, ics in PER_HORIZON.items():
        ax.plot(x, ics, marker=markers[method], label=method,
                color=colors[method], lw=2.5, ms=8, mec="white", mew=1.2, alpha=0.9)

    ax.axhline(y=IC_THRESHOLD, color=PALETTE["red_strong"], linestyle="--",
               lw=1.2, alpha=0.5, label=f"|IC| = {IC_THRESHOLD}")

    ax.set_xticks(x)
    ax.set_xticklabels(HORIZON_LABELS, fontsize=12)
    ax.set_xlabel("Prediction Horizon")
    ax.set_ylabel("Val IC")
    ax.set_title("Per-Horizon IC Comparison (Val Set)", loc="left", fontweight="bold")
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(alpha=0.2, linestyle="--")
    ax.set_ylim(-0.01, 0.16)

    finalize_figure(fig, OUT_DIR / "delta_learn_per_horizon_ic", formats=["png", "pdf"], dpi=300)


def fig5_full_summary():
    """4-panel summary figure for the report."""
    apply_publication_style(FigureStyle(font_size=12, axes_linewidth=2.0))
    fig, axes = create_subplots(2, 2, figsize=(16, 12))

    # --- Panel A: Baseline bar ---
    ax = axes[0]
    x = np.arange(len(BASELINE_METHODS))
    width = 0.35
    ax.bar(x - width/2, BASELINE_IC, width, label="IC",
           color=PALETTE["blue_main"], edgecolor="white", lw=0.6)
    ax.bar(x + width/2, BASELINE_RANKIC, width, label="Rank IC",
           color=PALETTE["teal"], edgecolor="white", lw=0.6)
    ax.axhline(y=IC_THRESHOLD, color=PALETTE["red_strong"], linestyle="--", lw=1.2, alpha=0.6)
    for i, v in enumerate(BASELINE_IC):
        if v > 0.005:
            ax.text(i - width/2, v + 0.001, f"{v:.3f}", ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(BASELINE_METHODS, fontsize=9)
    ax.set_ylabel("IC / Rank IC")
    ax.set_title("A. Baseline Comparison", loc="left", fontweight="bold")
    ax.set_ylim(0, 0.085)
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.15, linestyle="--")

    # --- Panel B: Model scaling ---
    ax = axes[1]
    ax.semilogx(MS_PARAMS, MS_PT_IC, "o-", color=PALETTE["blue_main"],
                lw=2, ms=7, mec="white", mew=1.2, label="Pretrain IC")
    ft_params = [322e3, 2.3e6, 17.4e6]
    ft_ic = [0.0669, 0.0677, 0.0678]
    ax2 = ax.twinx()
    ax2.semilogx(ft_params, ft_ic, "s--", color=PALETTE["red_strong"],
                 lw=2, ms=7, mec="white", mew=1.2, label="Finetune IC")
    ax.set_xlabel("Parameters")
    ax.set_ylabel("Pretrain IC", color=PALETTE["blue_main"])
    ax2.set_ylabel("Finetune IC", color=PALETTE["red_strong"])
    ax.set_title("B. Model Scaling", loc="left", fontweight="bold")
    ax.set_ylim(0.28, 0.31)
    ax2.set_ylim(0.060, 0.075)
    ax.set_xticks(MS_PARAMS)
    ax.set_xticklabels(["87K", "322K", "2.3M", "17.4M"], fontsize=9)
    ax.grid(alpha=0.15, linestyle="--")
    # Combined legend
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc="lower right")
    ax2.spines["right"].set_visible(True)
    ax2.spines["top"].set_visible(False)

    # --- Panel C: Data scaling ---
    ax = axes[2]
    ax.plot([0, 1, 2], DS_PT_IC, "o-", color=PALETTE["blue_main"],
            lw=2, ms=7, mec="white", mew=1.2, label="Pretrain IC")
    ax3 = ax.twinx()
    ax3.plot([0, 1, 2], DS_FT_IC, "s--", color=PALETTE["red_strong"],
             lw=2, ms=7, mec="white", mew=1.2, label="Finetune IC")
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(DS_LABELS, fontsize=9)
    ax.set_xlabel("Data Scale")
    ax.set_ylabel("Pretrain IC", color=PALETTE["blue_main"])
    ax3.set_ylabel("Finetune IC", color=PALETTE["red_strong"])
    ax.set_title("C. Data Scaling", loc="left", fontweight="bold")
    ax.grid(alpha=0.15, linestyle="--")
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax3.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc="center right")
    ax3.spines["right"].set_visible(True)
    ax3.spines["top"].set_visible(False)

    # --- Panel D: Per-horizon IC ---
    ax = axes[3]
    colors_ph = {
        "B2 PT→FT": PALETTE["blue_main"],
        "B3 E2E": PALETTE["teal"],
        "B4 Factor": PALETTE["violet"],
        "B5 Stat": PALETTE["neutral"],
    }
    markers_ph = {"B2 PT→FT": "o", "B3 E2E": "s", "B4 Factor": "D", "B5 Stat": "^"}
    xh = np.arange(len(HORIZONS))
    for method, ics in PER_HORIZON.items():
        ax.plot(xh, ics, marker=markers_ph[method], label=method,
                color=colors_ph[method], lw=2, ms=6, mec="white", mew=1, alpha=0.9)
    ax.axhline(y=IC_THRESHOLD, color=PALETTE["red_strong"], linestyle="--", lw=1, alpha=0.4)
    ax.set_xticks(xh)
    ax.set_xticklabels(HORIZON_LABELS, fontsize=10)
    ax.set_xlabel("Prediction Horizon")
    ax.set_ylabel("Val IC")
    ax.set_title("D. Per-Horizon IC", loc="left", fontweight="bold")
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(alpha=0.15, linestyle="--")
    ax.set_ylim(-0.01, 0.16)

    fig.tight_layout(pad=2)
    finalize_figure(fig, OUT_DIR / "delta_learn_summary_4panel", formats=["png", "pdf"], dpi=300)


if __name__ == "__main__":
    print("Generating delta_learn report figures...")
    fig1_baseline_comparison()
    print("  [1/5] Baseline comparison done")
    fig2_model_scaling()
    print("  [2/5] Model scaling done")
    fig3_data_scaling()
    print("  [3/5] Data scaling done")
    fig4_per_horizon_ic()
    print("  [4/5] Per-horizon IC done")
    fig5_full_summary()
    print("  [5/5] Summary 4-panel done")
    print(f"\nAll figures saved to: {OUT_DIR}")
