"""Generate figures for project progress slides (2026-03-03).

Covers: baseline comparison, per-horizon IC, model scaling, data scaling.
Uses val + test IC from delta_learn experiments.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from scientific_figure_pro import (
    apply_publication_style,
    FigureStyle,
    create_subplots,
    finalize_figure,
    PALETTE,
)

import numpy as np
import matplotlib.pyplot as plt

# ── Data ──────────────────────────────────────────────────────────

HORIZONS = ["30s", "1m", "3m", "5m", "10m", "15m"]
HORIZONS_TICKS = [60, 120, 360, 600, 1200, 1800]

# Val IC (best epoch, per-horizon)
VAL_IC = {
    "B2 (PT→FT)":  [0.140, 0.103, 0.054, 0.044, 0.033, 0.030],
    "B3 (E2E)":    [0.112, 0.086, 0.040, 0.033, 0.028, 0.028],
    "B4 (Factor)": [0.123, 0.087, 0.035, 0.030, 0.030, 0.026],
    "B5 (Stat BL)":[0.023, 0.022, 0.005, 0.006, 0.011, 0.009],
}

# Test IC (per-horizon)
TEST_IC = {
    "B2 (PT→FT)":  [0.158, 0.111, 0.070, 0.070, 0.038, 0.036],
    "B3 (E2E)":    [0.125, 0.093, 0.066, 0.056, 0.030, 0.029],
    "B4 (Factor)": [0.128, 0.081, 0.056, 0.054, 0.031, 0.036],
    "B5 (Stat BL)":[-0.006, 0.009, 0.009, 0.002, 0.027, 0.030],
}

# Mean IC (val / test)
MEAN_VAL = {"B2 (PT→FT)": 0.067, "B3 (E2E)": 0.055, "B4 (Factor)": 0.055,
            "FS1 (Factor-L)": 0.057, "B5 (Stat BL)": 0.013}
MEAN_TEST = {"B2 (PT→FT)": 0.081, "B3 (E2E)": 0.067, "B4 (Factor)": 0.064,
             "FS1 (Factor-L)": 0.068, "B5 (Stat BL)": 0.012}

# Model scaling (pretrain IC)
MS_PARAMS = ["87K", "322K", "2.3M", "17.4M"]
MS_PARAMS_NUM = [87e3, 322e3, 2.3e6, 17.4e6]
MS_PT_IC = [0.2974, 0.2963, 0.2974, 0.2995]

# Data scaling (finetune IC, val + test)
DS_LABELS = ["2 inst.\n2 yr", "5 inst.\n4 yr", "10 inst.\n8 yr"]
DS_VAL_IC = [0.021, 0.052, 0.067]
DS_TEST_IC = [0.033, 0.065, 0.081]

# ── Colors ────────────────────────────────────────────────────────

C_B2 = PALETTE["blue_main"]       # proposed method
C_B3 = PALETTE["teal"]            # E2E alternative
C_B4 = PALETTE["red_strong"]      # factor baseline
C_FS1 = PALETTE["violet"]         # factor-L
C_B5 = PALETTE["neutral"]         # stat baseline
C_VAL = PALETTE["blue_secondary"]
C_TEST = PALETTE["green_3"]

METHOD_COLORS = {
    "B2 (PT→FT)": C_B2,
    "B3 (E2E)": C_B3,
    "B4 (Factor)": C_B4,
    "FS1 (Factor-L)": C_FS1,
    "B5 (Stat BL)": C_B5,
}

# ── Style ─────────────────────────────────────────────────────────

apply_publication_style(FigureStyle(font_size=15, axes_linewidth=2))

OUT_DIR = Path(__file__).parent.parent  # figures/


def fig1_baseline_comparison():
    """Grouped bar: Val vs Test mean IC for each method."""
    fig, axes = create_subplots(1, 1, figsize=(8, 5))
    ax = axes[0]

    methods = list(MEAN_VAL.keys())
    x = np.arange(len(methods))
    w = 0.35

    bars_val = ax.bar(x - w / 2, [MEAN_VAL[m] for m in methods], w,
                      label="Val IC", color=C_VAL, edgecolor="white", lw=0.8)
    bars_test = ax.bar(x + w / 2, [MEAN_TEST[m] for m in methods], w,
                       label="Test IC", color=C_TEST, edgecolor="white", lw=0.8)

    # Annotate
    for bars in [bars_val, bars_test]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 0.001,
                    f"{h:.3f}", ha="center", va="bottom", fontsize=10)

    ax.set_xticks(x)
    ax.set_xticklabels(methods, fontsize=12)
    ax.set_ylabel("Mean IC")
    ax.set_ylim(0, 0.105)
    ax.legend(loc="upper right")
    ax.set_title("Baseline Comparison: Val vs Test IC", loc="left", fontweight="bold")

    finalize_figure(fig, OUT_DIR / "baseline_val_test", formats=["pdf", "png"], dpi=300)


def fig2_per_horizon():
    """Line chart: per-horizon IC for baselines, val vs test side by side."""
    fig, axes = create_subplots(1, 2, figsize=(14, 5))

    x = np.arange(len(HORIZONS))
    for panel_idx, (data, title) in enumerate(
        [(VAL_IC, "Val Set (2023 H1)"), (TEST_IC, "Test Set (2023 H2)")]
    ):
        ax = axes[panel_idx]
        for method, ics in data.items():
            c = METHOD_COLORS.get(method, PALETTE["neutral"])
            lw = 3.0 if "B2" in method else 2.0
            ax.plot(x, ics, "o-", label=method, color=c, lw=lw, markersize=6)

        ax.set_xticks(x)
        ax.set_xticklabels(HORIZONS)
        ax.set_xlabel("Prediction Horizon")
        ax.set_ylabel("IC")
        ax.set_ylim(-0.02, 0.18)
        ax.set_title(title, loc="left", fontweight="bold")
        ax.legend(fontsize=10, loc="upper right")
        ax.grid(alpha=0.15, linestyle="--")

    finalize_figure(fig, OUT_DIR / "per_horizon_val_test", formats=["pdf", "png"], dpi=300)


def fig3_model_scaling():
    """Bar chart: pretrain IC vs model params (log scale x)."""
    fig, axes = create_subplots(1, 1, figsize=(7, 5))
    ax = axes[0]

    x = np.arange(len(MS_PARAMS))
    bars = ax.bar(x, MS_PT_IC, 0.6, color=C_B2, edgecolor="white", lw=0.8)

    for bar, val in zip(bars, MS_PT_IC):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.0005,
                f"{val:.4f}", ha="center", va="bottom", fontsize=11)

    ax.set_xticks(x)
    ax.set_xticklabels(MS_PARAMS)
    ax.set_xlabel("Model Parameters")
    ax.set_ylabel("Pretrain IC")
    ax.set_ylim(0.290, 0.305)
    ax.set_title("Model Scaling: 200× Params → +0.07% IC", loc="left", fontweight="bold")
    ax.grid(alpha=0.15, linestyle="--", axis="y")

    finalize_figure(fig, OUT_DIR / "model_scaling", formats=["pdf", "png"], dpi=300)


def fig4_data_scaling():
    """Grouped bar: data scaling val vs test IC."""
    fig, axes = create_subplots(1, 1, figsize=(7, 5))
    ax = axes[0]

    x = np.arange(len(DS_LABELS))
    w = 0.35

    bars_v = ax.bar(x - w / 2, DS_VAL_IC, w, label="Val IC", color=C_VAL, edgecolor="white", lw=0.8)
    bars_t = ax.bar(x + w / 2, DS_TEST_IC, w, label="Test IC", color=C_TEST, edgecolor="white", lw=0.8)

    for bars in [bars_v, bars_t]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 0.001,
                    f"{h:.3f}", ha="center", va="bottom", fontsize=11)

    ax.set_xticks(x)
    ax.set_xticklabels(DS_LABELS, fontsize=12)
    ax.set_xlabel("Data Scale")
    ax.set_ylabel("Finetune IC")
    ax.set_ylim(0, 0.10)
    ax.legend(loc="upper left")
    ax.set_title("Data Scaling: 2→10 Instruments → +141% Test IC", loc="left", fontweight="bold")

    finalize_figure(fig, OUT_DIR / "data_scaling", formats=["pdf", "png"], dpi=300)


def fig5_summary_4panel():
    """Summary 4-panel for overview slide."""
    fig, axes = create_subplots(2, 2, figsize=(14, 10))

    # Panel A: Baseline test IC bars
    ax = axes[0]
    methods = ["B2\n(PT→FT)", "B3\n(E2E)", "B4\n(Factor)", "FS1\n(Factor-L)", "B5\n(Stat)"]
    test_vals = [0.081, 0.067, 0.064, 0.068, 0.012]
    colors_a = [C_B2, C_B3, C_B4, C_FS1, C_B5]
    bars = ax.bar(np.arange(len(methods)), test_vals, 0.65, color=colors_a, edgecolor="white", lw=0.8)
    for bar, val in zip(bars, test_vals):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.001,
                f"{val:.3f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_xticks(np.arange(len(methods)))
    ax.set_xticklabels(methods, fontsize=10)
    ax.set_ylabel("Test IC")
    ax.set_ylim(0, 0.10)
    ax.set_title("A. Baseline Comparison (Test)", loc="left", fontweight="bold")
    ax.axhline(y=0.015, color="gray", linestyle="--", alpha=0.5, lw=1)
    ax.text(4.3, 0.016, "threshold", fontsize=8, color="gray")

    # Panel B: Per-horizon IC (test)
    ax = axes[1]
    x = np.arange(len(HORIZONS))
    for method, ics in TEST_IC.items():
        c = METHOD_COLORS.get(method, PALETTE["neutral"])
        lw = 3.0 if "B2" in method else 1.8
        ax.plot(x, ics, "o-", label=method, color=c, lw=lw, markersize=5)
    ax.set_xticks(x)
    ax.set_xticklabels(HORIZONS, fontsize=10)
    ax.set_ylabel("Test IC")
    ax.set_ylim(-0.02, 0.18)
    ax.set_title("B. Per-Horizon IC (Test)", loc="left", fontweight="bold")
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(alpha=0.15, linestyle="--")

    # Panel C: Model scaling
    ax = axes[2]
    bars = ax.bar(np.arange(len(MS_PARAMS)), MS_PT_IC, 0.6, color=C_B2, edgecolor="white", lw=0.8)
    for bar, val in zip(bars, MS_PT_IC):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.0003,
                f"{val:.4f}", ha="center", va="bottom", fontsize=10)
    ax.set_xticks(np.arange(len(MS_PARAMS)))
    ax.set_xticklabels(MS_PARAMS, fontsize=10)
    ax.set_xlabel("Parameters")
    ax.set_ylabel("Pretrain IC")
    ax.set_ylim(0.292, 0.304)
    ax.set_title("C. Model Scaling (Pretrain)", loc="left", fontweight="bold")
    ax.grid(alpha=0.15, linestyle="--", axis="y")

    # Panel D: Data scaling
    ax = axes[3]
    w = 0.35
    x = np.arange(len(DS_LABELS))
    ax.bar(x - w / 2, DS_VAL_IC, w, label="Val", color=C_VAL, edgecolor="white", lw=0.8)
    ax.bar(x + w / 2, DS_TEST_IC, w, label="Test", color=C_TEST, edgecolor="white", lw=0.8)
    for i, (v, t) in enumerate(zip(DS_VAL_IC, DS_TEST_IC)):
        ax.text(i - w / 2, v + 0.001, f"{v:.3f}", ha="center", va="bottom", fontsize=9)
        ax.text(i + w / 2, t + 0.001, f"{t:.3f}", ha="center", va="bottom", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(DS_LABELS, fontsize=10)
    ax.set_xlabel("Data Scale")
    ax.set_ylabel("Finetune IC")
    ax.set_ylim(0, 0.10)
    ax.legend(fontsize=10, loc="upper left")
    ax.set_title("D. Data Scaling (Val + Test)", loc="left", fontweight="bold")

    fig.tight_layout(pad=2)
    finalize_figure(fig, OUT_DIR / "summary_4panel_val_test", formats=["pdf", "png"], dpi=300)


if __name__ == "__main__":
    fig1_baseline_comparison()
    fig2_per_horizon()
    fig3_model_scaling()
    fig4_data_scaling()
    fig5_summary_4panel()
    print("All figures generated.")
