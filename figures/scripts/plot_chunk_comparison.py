#!/usr/bin/env python3
"""Generate comparison figures for chunk experiment analysis.

Produces two panels:
  (a) Bar chart: IC mean across all experiments (ranked)
  (b) IC decay curves: top experiments by horizon

Usage:
    python figures/scripts/plot_chunk_comparison.py
"""

import json
import sys
from pathlib import Path

import numpy as np

# Add project root for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.scientific_figure_pro import (
    apply_publication_style, create_subplots, finalize_figure,
    make_trend, PALETTE, DEFAULT_COLORS, FigureStyle, annotate_bars,
)
import matplotlib.pyplot as plt

RESULTS_DIR = Path(__file__).resolve().parents[2] / "results" / "delta_learn" / "chunk"
OUT_DIR = Path(__file__).resolve().parents[2] / "figures"

# Experiment definitions: (label, relative_path)
EXPERIMENTS = [
    ("m_long",        "group_chunk_m_long/group_chunk_20260305_100658"),
    ("B1_stride",     "multiscale/B1_stride_1800/group_chunk_20260305_173226"),
    ("B2_stride",     "multiscale/B2_stride_3600/group_chunk_20260305_173226"),
    ("baseline",      "group_chunk_20260305_071945"),
    ("ctx_1800",      "ablation/ctx_1800/group_chunk_20260304_220531"),
    ("A3_cs300_7200", "multiscale/A3_cs300_7200/group_chunk_20260305_032333"),
    ("ctx_7200",      "ablation/ctx_7200/group_chunk_20260304_220532"),
    ("allfu",         "group_chunk_allfu/group_chunk_20260305_052041"),
    ("A1_cs300",      "multiscale/A1_cs300_3600/group_chunk_20260305_032333"),
    ("C1_serial",     "multiscale/C1_serial/serial_ms_20260305_173225"),
    ("chunk_S",       "ablation/chunk_S/group_chunk_20260304_160753"),
    ("chunk_M",       "ablation/chunk_M/group_chunk_20260304_184834"),
    ("A2_cs600",      "multiscale/A2_cs600_3600/group_chunk_20260305_032333"),
    ("A4_cs600_7200", "multiscale/A4_cs600_7200/group_chunk_20260305_032333"),
    ("conv_S",        "ablation/conv_S/group_conv_20260304_160753"),
    ("conv_M",        "ablation/conv_M/group_conv_20260304_184833"),
]

# Top experiments for IC decay curves
TOP_EXPERIMENTS = ["m_long", "B1_stride", "baseline", "ctx_1800", "conv_S"]


def load_metrics():
    """Load test_metrics.json for all experiments."""
    data = {}
    for label, rel_path in EXPERIMENTS:
        path = RESULTS_DIR / rel_path / "test_metrics.json"
        if path.exists():
            with open(path) as f:
                data[label] = json.load(f)
    return data


def main():
    apply_publication_style(FigureStyle(font_size=13))
    metrics = load_metrics()

    fig, axes = create_subplots(1, 2, figsize=(16, 6))

    # --- Panel (a): Bar chart of IC mean ---
    ax = axes[0]
    labels = [label for label, _ in EXPERIMENTS if label in metrics]
    ic_values = [metrics[label]["ic_mean"] for label in labels]

    # Color: blue for positive, red for negative
    colors = [PALETTE["blue_main"] if v > 0 else PALETTE["red_strong"] for v in ic_values]

    bars = ax.barh(range(len(labels)), ic_values, color=colors, edgecolor="white", lw=0.5)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=11)
    ax.set_xlabel("IC Mean")
    ax.set_title("(a) Test IC Mean — All Experiments")
    ax.axvline(x=0, color="gray", lw=0.8, ls="--")
    ax.axvline(x=0.015, color=PALETTE["green_3"], lw=1.2, ls=":", label="threshold (0.015)")
    ax.invert_yaxis()
    ax.legend(fontsize=10)

    # Annotate values
    for i, (bar, val) in enumerate(zip(bars, ic_values)):
        xpos = val + 0.001 if val > 0 else val - 0.001
        ha = "left" if val > 0 else "right"
        ax.text(xpos, i, f"{val:.4f}", va="center", ha=ha, fontsize=9)

    # --- Panel (b): IC decay curves ---
    ax2 = axes[1]
    top_colors = [
        PALETTE["red_strong"],   # m_long
        PALETTE["blue_main"],    # B1_stride
        PALETTE["green_3"],      # baseline
        PALETTE["teal"],         # ctx_1800
        PALETTE["neutral"],      # conv_S
    ]

    for i, label in enumerate(TOP_EXPERIMENTS):
        if label not in metrics:
            continue
        ic_per_h = metrics[label]["ic_per_horizon"]
        horizons = sorted(ic_per_h.keys(), key=lambda x: int(x))
        x = [int(h) / 2 for h in horizons]  # Convert ticks to seconds (500ms/tick)
        y = [ic_per_h[h] for h in horizons]
        ax2.plot(x, y, label=label, color=top_colors[i], lw=2.2, alpha=0.85)

    ax2.set_xlabel("Forward Horizon (seconds)")
    ax2.set_ylabel("IC")
    ax2.set_title("(b) IC Decay by Horizon — Top Experiments")
    ax2.axhline(y=0, color="gray", lw=0.8, ls="--")
    ax2.legend(fontsize=10, loc="upper right")

    plt.tight_layout()
    saved = finalize_figure(fig, OUT_DIR / "chunk_experiment_comparison", formats=["pdf", "png"])
    for p in saved:
        print(f"Saved: {p}")


if __name__ == "__main__":
    main()
