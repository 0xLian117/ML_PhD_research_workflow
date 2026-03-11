"""Rolling Walk-Forward Analysis v3 — Complete 4-Panel

A. Rolling window timeline (train/val/test) with data gap annotations
B. Pearson IC heatmap (fold × horizon)
C. Rank IC heatmap (fold × horizon)
Annotations: I/M/P missing in fold04-05, fold09 no data, fold02 outlier
"""

import sys
import json
import numpy as np
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from scientific_figure_pro import (
    apply_publication_style, FigureStyle, finalize_figure, PALETTE,
)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import Patch
import yaml

# ── Data ──────────────────────────────────────────────────────────────────

RESULTS_DIR = Path(__file__).parent.parent.parent / "results" / "delta_learn" / "rolling"

folds = []
for fold_dir in sorted(RESULTS_DIR.glob("fold*")):
    ft_dirs = list((fold_dir / "finetune").glob("finetune_*"))
    if not ft_dirs:
        continue
    ft_dir = ft_dirs[0]
    metrics_path = ft_dir / "test_metrics.json"
    config_path = ft_dir / "config.yaml"
    history_path = ft_dir / "history.json"
    if not metrics_path.exists():
        continue
    with open(metrics_path) as f:
        metrics = json.load(f)
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    with open(history_path) as f:
        hist = json.load(f)

    inst_dates = list(cfg["data"]["sources"][0]["instruments"].values())[0]
    train_start, train_end = inst_dates["train"]
    val_start, val_end = inst_dates["val"]
    test_start, test_end = inst_dates["test"]
    test_label = test_start[:4] + "H" + ("1" if test_start[5:7] <= "06" else "2")

    n_epochs = len(hist["train_loss"])
    best_epoch = hist["val_loss"].index(min(hist["val_loss"])) + 1

    # Estimate train/val samples from config + empirical rate
    # Empirical: ~9.5 test samples per instrument-day at val_stride=3600
    # train stride=1800 → ~19 samples per instrument-day
    RATE_VAL = 9.5      # samples/inst-day at val_stride=3600
    RATE_TRAIN = 19.0    # samples/inst-day at stride=1800
    DAYS_PER_YEAR = 240  # approx Chinese futures trading days

    train_start_dt = datetime.strptime(train_start, "%Y-%m-%d")
    train_end_dt = datetime.strptime(train_end, "%Y-%m-%d")
    val_start_dt = datetime.strptime(val_start, "%Y-%m-%d")
    val_end_dt = datetime.strptime(val_end, "%Y-%m-%d")

    train_years = (train_end_dt - train_start_dt).days / 365.25
    val_months = (val_end_dt - val_start_dt).days / 30.44

    # I/M/P missing in 2022 for test, but present in train (before 2022)
    n_inst_test = 7 if test_label in ("2022H1", "2022H2") else 10
    n_inst_train = 10  # all instruments have data in pre-2022 training period

    train_samples_est = int(train_years * DAYS_PER_YEAR * n_inst_train * RATE_TRAIN)
    val_days_est = int(val_months / 12 * DAYS_PER_YEAR)
    val_samples_est = int(val_days_est * n_inst_test * RATE_VAL)

    folds.append({
        "name": fold_dir.name,
        "test_label": test_label,
        "train": (train_start, train_end),
        "val": (val_start, val_end),
        "test": (test_start, test_end),
        "ic_mean": metrics["ic_mean"],
        "rank_ic_mean": metrics["rank_ic_mean"],
        "ic_per_horizon": metrics["ic_per_horizon"],
        "rank_ic_per_horizon": metrics["rank_ic_per_horizon"],
        "test_samples": metrics["test_samples"],
        "train_samples_est": train_samples_est,
        "val_samples_est": val_samples_est,
        "n_inst_test": n_inst_test,
        "n_epochs": n_epochs,
        "best_epoch": best_epoch,
    })

horizons = list(folds[0]["ic_per_horizon"].keys())
horizon_labels = []
for h in horizons:
    secs = int(h) * 0.5
    horizon_labels.append(f"{secs/60:.0f}m" if secs >= 60 else f"{secs:.0f}s")

fold_labels = [f["test_label"] for f in folds]
n_folds = len(folds)
n_horizons = len(horizons)

ic_matrix = np.array([[f["ic_per_horizon"][h] for h in horizons] for f in folds])
rank_ic_matrix = np.array([[f["rank_ic_per_horizon"][h] for h in horizons] for f in folds])

# ── Known data issues ─────────────────────────────────────────────────────

# From check_data_coverage.py output
FOLD_NOTES = {
    0: "",                                                      # fold01
    1: "Pearson IC outlier-driven (see panel B)",                # fold02
    2: "",                                                      # fold03
    3: "I/M/P no tick data in 2022 (7/10 instruments)",         # fold04
    4: "I/M/P no tick data in 2022 (7/10 instruments)",         # fold05
    5: "",                                                      # fold06
    6: "",                                                      # fold07
    7: "",                                                      # fold08
}

# ── Plot ──────────────────────────────────────────────────────────────────

apply_publication_style(FigureStyle(font_size=13, axes_linewidth=1.8))

fig = plt.figure(figsize=(20, 12.5))
gs = fig.add_gridspec(2, 2, width_ratios=[1, 1], height_ratios=[0.85, 1],
                      wspace=0.28, hspace=0.38)

ax_timeline = fig.add_subplot(gs[0, :])
ax_pearson = fig.add_subplot(gs[1, 0])
ax_rank = fig.add_subplot(gs[1, 1])

# ── Panel A: Rolling Window Timeline ─────────────────────────────────────

def to_date(s):
    return datetime.strptime(s, "%Y-%m-%d")

c_train = PALETTE["blue_secondary"]
c_val = PALETTE["green_3"]
c_test = PALETTE["red_strong"]

bar_height = 0.50
y_positions = list(range(n_folds, -1, -1))  # +1 for fold09 placeholder

# fold09 placeholder
all_fold_data = list(folds) + [{
    "name": "fold09",
    "train": ("2015-01-01", "2023-12-31"),
    "val": ("2024-01-01", "2024-06-30"),
    "test": ("2024-07-01", "2024-12-31"),
    "test_label": "2024H2",
    "test_samples": None,
}]

for i, f in enumerate(all_fold_data):
    y = y_positions[i]
    is_fold09 = (i == n_folds)

    for split, color in [("train", c_train), ("val", c_val), ("test", c_test)]:
        start = to_date(f[split][0])
        end = to_date(f[split][1])
        width = (end - start).days
        alpha = 0.30 if is_fold09 else 0.85
        ax_timeline.barh(y, width, left=mdates.date2num(start),
                         height=bar_height, color=color,
                         edgecolor="white", lw=0.8, alpha=alpha)

    test_end_num = mdates.date2num(to_date(f["test"][1]))

    if is_fold09:
        ax_timeline.text(test_end_num + 20, y,
                         "Data ends at 2024-06-14, no 2024H2 data",
                         va="center", fontsize=9.5, color="#999999", fontstyle="italic")
    else:
        # Line 1: IC values
        ic_val = f["ic_mean"]
        rank_ic_val = f["rank_ic_mean"]
        n_inst = f["n_inst_test"]

        ic_color = PALETTE["red_strong"] if (i == 1) else "#333333"
        line1 = f"IC={ic_val:.3f}  RankIC={rank_ic_val:.3f}  ({n_inst} inst)"
        ax_timeline.text(test_end_num + 20, y + 0.15, line1,
                         va="center", fontsize=9, color=ic_color,
                         fontfamily="monospace")

        # Line 2: sample counts (train / val / test)
        tr_k = f["train_samples_est"] // 1000
        va_k = f["val_samples_est"] // 1000
        te = f["test_samples"]
        line2 = f"train~{tr_k}K  val~{va_k}K  test={te:,}"
        ax_timeline.text(test_end_num + 20, y - 0.05, line2,
                         va="center", fontsize=8.5, color="#555555",
                         fontfamily="monospace")

        # Line 3: notes (data gaps, outlier, epochs, data cutoff)
        note = FOLD_NOTES.get(i, "")
        ep_text = f"{f['n_epochs']}ep (best@{f['best_epoch']})"
        if i == 7:  # fold08: data cutoff
            note = "data ends 2024-06-14 (missing ~10 trading days)"
        line3 = f"{ep_text}  {note}" if note else ep_text
        note_color = PALETTE["red_strong"] if note else "#999999"
        ax_timeline.text(test_end_num + 20, y - 0.25, line3,
                         va="center", fontsize=7.5, color=note_color)

ax_timeline.set_yticks(y_positions)
ax_timeline.set_yticklabels([f["name"] for f in all_fold_data], fontsize=11)
ax_timeline.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax_timeline.xaxis.set_major_locator(mdates.YearLocator())
ax_timeline.set_xlim(mdates.date2num(to_date("2014-09-01")),
                     mdates.date2num(to_date("2026-06-01")))

legend_elements = [
    Patch(facecolor=c_train, edgecolor="white", label="Train (expanding)"),
    Patch(facecolor=c_val, edgecolor="white", label="Validation (6 mo)"),
    Patch(facecolor=c_test, edgecolor="white", label="Test / OOS (6 mo)"),
]
ax_timeline.legend(handles=legend_elements, loc="upper left", fontsize=11,
                   ncol=3, borderaxespad=0.3)

ax_timeline.set_xlabel("Year")
ax_timeline.set_title("A. Rolling Walk-Forward: Expanding Train + Fixed Val/Test Windows",
                       loc="left", fontweight="bold", fontsize=14)
ax_timeline.grid(axis="x", alpha=0.15, linestyle="--")
for spine in ["top", "right"]:
    ax_timeline.spines[spine].set_visible(False)

# ── Helper: annotated heatmap ────────────────────────────────────────────

def draw_heatmap(ax, matrix, title, cbar_label, is_pearson=False):
    vmax = 0.15 if is_pearson else 0.13
    norm = TwoSlopeNorm(vmin=-0.02, vcenter=0.0, vmax=vmax)
    im = ax.imshow(matrix, cmap="RdBu", norm=norm, aspect="auto",
                   interpolation="nearest")

    for i in range(n_folds):
        for j in range(n_horizons):
            val = matrix[i, j]
            if val > 0.08:
                color = "white"
            elif val < -0.003:
                color = "white"
            else:
                color = "black"

            text = f"{val:.3f}" if abs(val) >= 0.001 else "0"
            weight = "bold" if (is_pearson and i == 1 and val > 0.1) else "normal"
            ax.text(j, i, text, ha="center", va="center",
                    color=color, fontsize=10, fontweight=weight)

    ax.set_xticks(np.arange(n_horizons))
    ax.set_xticklabels(horizon_labels)
    ax.set_yticks(np.arange(n_folds))

    # Y-labels with data gap annotation
    ylabels = []
    for i, label in enumerate(fold_labels):
        if i in (3, 4):
            ylabels.append(f"{label}\n-I/M/P")
        elif i == 1 and is_pearson:
            ylabels.append(f"{label}\n(outlier)")
        else:
            ylabels.append(label)
    ax.set_yticklabels(ylabels, fontsize=10)

    ax.set_xlabel("Prediction Horizon")
    ax.set_ylabel("Test Period (OOS)")

    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1.2)

    cbar = fig.colorbar(im, ax=ax, shrink=0.82, pad=0.02)
    cbar.set_label(cbar_label, fontsize=11)
    cbar.ax.tick_params(labelsize=9)

    ax.set_title(title, loc="left", fontweight="bold", fontsize=14)
    return im

# ── Panel B: Pearson IC ──────────────────────────────────────────────────

draw_heatmap(ax_pearson, ic_matrix,
             "B. OOS Pearson IC", "Pearson IC", is_pearson=True)

# ── Panel C: Rank IC ─────────────────────────────────────────────────────

draw_heatmap(ax_rank, rank_ic_matrix,
             "C. OOS Rank IC (Spearman)", "Rank IC", is_pearson=False)

# ── Bottom notes ─────────────────────────────────────────────────────────

notes = (
    "I (iron ore), M (soybean meal), P (palm oil): no tick data in 2022 (source gap: 2021-12 ~ 2023-01)\n"
    "fold02 Pearson IC=0.13 is outlier-driven; Rank IC=0.03 is normal    |    "
    "Data ends 2024-06-14; fold09 cannot be evaluated"
)
fig.text(0.5, 0.005, notes, ha="center", fontsize=9.5, color="#555555",
         fontstyle="italic", linespacing=1.5)

# ── Finalize ─────────────────────────────────────────────────────────────

finalize_figure(fig, "figures/rolling_walkforward_v3", formats=["pdf", "png"], dpi=300)
print("Done.")
