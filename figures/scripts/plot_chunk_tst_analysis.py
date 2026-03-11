#!/usr/bin/env python3
"""Generate analysis figures for chunk_tst finetune experiments.

3-panel figure:
  (a) Per-horizon IC decay (up to 1800 ticks / 15 min)
  (b) Per-instrument IC heatmap
  (c) Training convergence — val IC over epochs

Usage:
    python figures/scripts/plot_chunk_tst_analysis.py
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.scientific_figure_pro import (
    apply_publication_style, create_subplots, finalize_figure,
    PALETTE, FigureStyle,
)
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

RESULTS_DIR = Path(__file__).resolve().parents[2] / "results" / "delta_learn" / "chunk_tst"
OUT_DIR = Path(__file__).resolve().parents[2] / "figures"

# Finetune experiments only (no gap experiments)
EXPERIMENTS = {
    "chunk_finetune": ("Finetune (2-stage)", "chunk_finetune", "chunk_finetune_20260309_025023"),
    "group_chunk_nogap": ("E2E (gap=0)", "group_chunk_nogap", "group_chunk_20260306_072547"),
    "group_chunk_10d": ("E2E 10D (gap=0)", "group_chunk_10d", "group_chunk_20260309_065946"),
    "group_chunk_long": ("E2E long (2h)", "group_chunk_long", "group_chunk_20260309_081144"),
}

FINETUNE_KEYS = list(EXPERIMENTS.keys())
INSTRUMENTS = ["AU", "AG", "CU", "AL", "RB", "I", "RU", "TA", "M", "P"]

MAX_HORIZON = 1800  # ticks (= 15 min at 2 ticks/sec)


def load_all():
    """Load test_metrics.json and history.json for all experiments."""
    data = {}
    for key, (label, subdir, run) in EXPERIMENTS.items():
        run_dir = RESULTS_DIR / subdir / run
        tm = run_dir / "test_metrics.json"
        hist = run_dir / "history.json"
        if tm.exists():
            entry = {"label": label, "metrics": json.load(open(tm))}
            if hist.exists():
                entry["history"] = json.load(open(hist))
            data[key] = entry
    return data


def panel_ic_decay(ax, data):
    """(a) IC decay by horizon — finetune experiments, up to 15 min."""
    colors = {
        "chunk_finetune": PALETTE["blue_main"],
        "group_chunk_nogap": PALETTE["green_3"],
        "group_chunk_10d": PALETTE["teal"],
        "group_chunk_long": PALETTE["red_strong"],
    }
    for key in FINETUNE_KEYS:
        if key not in data:
            continue
        m = data[key]["metrics"]
        ic_h = m["ic_per_horizon"]
        horizons = sorted(
            [h for h in ic_h.keys() if int(h) <= MAX_HORIZON],
            key=lambda x: int(x),
        )
        x = [int(h) / 2 for h in horizons]  # ticks -> seconds
        y = [ic_h[h] for h in horizons]
        ax.plot(x, y, label=data[key]["label"], color=colors[key],
                lw=2.2, alpha=0.85)

    ax.axhline(y=0.015, color=PALETTE["highlight"], lw=1, ls=":", alpha=0.7)
    ax.axhline(y=0, color="gray", lw=0.6, ls="--", alpha=0.5)
    ax.set_xlabel("Forward Horizon (seconds)")
    ax.set_ylabel("IC")
    ax.set_title("(a) IC Decay by Horizon", loc="left", fontweight="bold")
    ax.legend(fontsize=8, loc="upper right")


def panel_instrument_heatmap(ax, data):
    """(b) Per-instrument IC heatmap — finetune experiments."""
    labels = []
    matrix = []
    for key in FINETUNE_KEYS:
        if key not in data:
            continue
        m = data[key]["metrics"]
        inst_ic = m.get("instrument_summary", {}).get("per_instrument_ic", {})
        if not inst_ic:
            continue
        row = [inst_ic.get(inst, float("nan")) for inst in INSTRUMENTS]
        matrix.append(row)
        labels.append(data[key]["label"])

    matrix = np.array(matrix)

    vmax = max(0.3, np.nanmax(matrix))
    vmin = min(-0.02, np.nanmin(matrix))
    norm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

    im = ax.imshow(matrix, cmap="RdYlGn", norm=norm, aspect="auto",
                   interpolation="nearest")
    ax.set_xticks(range(len(INSTRUMENTS)))
    ax.set_xticklabels(INSTRUMENTS, fontsize=9)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=9)

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            val = matrix[i, j]
            if np.isnan(val):
                continue
            color = "white" if val > 0.15 or val < -0.01 else "black"
            ax.text(j, i, f"{val:.3f}", ha="center", va="center",
                    fontsize=7, color=color)

    ax.set_title("(b) Per-Instrument IC", loc="left", fontweight="bold")
    cbar = ax.figure.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label("IC", fontsize=9)


def panel_convergence(ax, data):
    """(c) Val IC convergence curves for finetune experiments."""
    colors = {
        "chunk_finetune": PALETTE["blue_main"],
        "group_chunk_nogap": PALETTE["green_3"],
        "group_chunk_10d": PALETTE["teal"],
        "group_chunk_long": PALETTE["red_strong"],
    }
    for key in FINETUNE_KEYS:
        if key not in data or "history" not in data[key]:
            continue
        h = data[key]["history"]
        ic = h.get("val_ic_mean", [])
        if not ic:
            continue
        epochs = list(range(1, len(ic) + 1))
        ax.plot(epochs, ic, label=data[key]["label"], color=colors[key],
                lw=1.8, alpha=0.85)

    ax.axhline(y=0, color="gray", lw=0.6, ls="--", alpha=0.5)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Val IC Mean")
    ax.set_title("(c) Finetune Convergence", loc="left", fontweight="bold")
    ax.legend(fontsize=8, loc="lower right")


def figure_per_instrument_ic_decay(data):
    """2x5 small multiples: per-instrument IC decay for each experiment."""
    colors = {
        "chunk_finetune": PALETTE["blue_main"],
        "group_chunk_nogap": PALETTE["green_3"],
        "group_chunk_10d": PALETTE["teal"],
        "group_chunk_long": PALETTE["red_strong"],
    }

    fig, axes = plt.subplots(2, 5, figsize=(20, 8), sharex=True, sharey=True)
    axes = axes.flatten()

    for idx, inst in enumerate(INSTRUMENTS):
        ax = axes[idx]
        for key in FINETUNE_KEYS:
            if key not in data:
                continue
            per_inst = data[key]["metrics"].get("per_instrument", {}).get(inst, {})
            ic_h = per_inst.get("ic_per_horizon", {})
            if not ic_h:
                continue
            horizons = sorted(
                [h for h in ic_h.keys() if int(h) <= MAX_HORIZON],
                key=lambda x: int(x),
            )
            x = [int(h) / 2 for h in horizons]  # ticks -> seconds
            y = [ic_h[h] for h in horizons]
            ax.plot(x, y, label=data[key]["label"], color=colors[key],
                    lw=1.6, alpha=0.85)

        ax.axhline(y=0.015, color=PALETTE["highlight"], lw=0.8, ls=":", alpha=0.6)
        ax.axhline(y=0, color="gray", lw=0.5, ls="--", alpha=0.4)
        ax.set_title(inst, fontweight="bold", fontsize=12)

        if idx >= 5:
            ax.set_xlabel("Horizon (s)")
        if idx % 5 == 0:
            ax.set_ylabel("IC")

    # Single shared legend
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=len(FINETUNE_KEYS),
               fontsize=9, bbox_to_anchor=(0.5, 1.02))
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    return fig


def main():
    apply_publication_style(FigureStyle(font_size=13, axes_linewidth=2))
    data = load_all()

    # Figure 1: 3-panel overview
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], hspace=0.35, wspace=0.3)

    ax_a = fig.add_subplot(gs[0, :])   # top full-width
    ax_b = fig.add_subplot(gs[1, 0])   # bottom-left
    ax_c = fig.add_subplot(gs[1, 1])   # bottom-right

    panel_ic_decay(ax_a, data)
    panel_instrument_heatmap(ax_b, data)
    panel_convergence(ax_c, data)

    saved = finalize_figure(fig, OUT_DIR / "chunk_tst_analysis", formats=["pdf", "png"])
    for p in saved:
        print(f"Saved: {p}")

    # Figure 2: Per-instrument IC decay (2x5 small multiples)
    fig2 = figure_per_instrument_ic_decay(data)
    saved2 = finalize_figure(fig2, OUT_DIR / "chunk_tst_per_instrument_ic_decay",
                             formats=["pdf", "png"])
    for p in saved2:
        print(f"Saved: {p}")


if __name__ == "__main__":
    main()
