---
marp: true
math: mathjax
theme: delta-lab
paginate: true
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Hierarchical Transformer for Tick-Level Return Prediction

Encoder 进展汇报

2026年3月

---

# Outline

1. **研究动机** — 核心问题
2. **方法** — 架构 · 数据 · 实验配置
3. **实验结果** — Baseline · Per-Horizon · Scaling
4. **结论与下一步**

---

# 研究动机 | 核心问题

> 期货 tick 级原始行情中，是否存在可学习的、具有样本外预测能力的**多 horizon 收益模式**？

<div class="columns">
<div>

**为什么端到端？**
- 避免人工因子偏差
- 多 horizon 统一建模
- 与符号搜索 (delta_alpha) 互补

</div>
<div>

**三个实验问题**
- **Q1** E2E tick > 手工因子？
- **Q2** Pretrain→FT > 直接训练？
- **Q3** Model/Data scaling 边际收益？

</div>
</div>

---

# 方法 | Hierarchical Transformer

<div class="columns">
<div>

```
┌─────────────────────────────┐
│  Tick 序列 (B, 3600, 52)    │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│  Patch 切分 (B, 60, 60, 52) │
└──────────────┬──────────────┘
               ▼                   ┌──────────────────┐
┌─────────────────────────────┐    │ Pretrain Head     │
│  L1 Patch Transformer       │───→│ → (B,7) 短horizon │
│  CausalAttn, d=128         │    │ [2..30] ticks     │
└──────────────┬──────────────┘    └──────────────────┘
     L1 frozen ▼
┌─────────────────────────────┐
│  L2 Sequence Transformer    │
│  CausalAttn, d=128         │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│  Prediction Head → (B, 6)   │
│  [60..1800] ticks           │
└─────────────────────────────┘
```

</div>
<div>

**Stage 1: Pretrain**
L1 在短 horizon (≤30 ticks / 15s) 上训练

**Stage 2: Finetune**
冻结 L1，训练 L2 + Head 在长 horizon

**Inductive Bias**
30s patch → 30min sequence
短期模式构成长期模式的基础

**参数量**: ~322K (baseline)

</div>
</div>

---

# 方法 | 数据与实验配置

<div class="columns">
<div>

**数据**
- 中国期货 10 品种，500ms 快照
- 13 特征 × 4 rolling 变换 = **52 维**
- Train 2015–22 / Val 2023 / Test 2024
- PT: ~5.2M 样本　FT: ~468K 样本

</div>
<div class="small">

**8 种实验配置** (参数量控制 ~300K)

| ID | 方法 | L1/L2 | 差异 | 组 |
|---|---|---|---|---|
| B1→B2 | **PT→FT** | T/T | 主方法 | BL |
| B3 | E2E | T/T | 无 pretrain | BL |
| B4 | Factor | —/T | 62 维因子 | BL |
| B5 | Stat BL | —/T | patch 均值 | BL |
| MS1–4 | Scaling | T/T | 87K→17.4M | MS |
| DS1–3 | Scaling | T/T | 2→10 品种 | DS |
| FS1 | Factor-L | —/T | Factor×7 | 附加 |
| S1 | Spectral | C/T | STFT | 附加 |

</div>
</div>

---

# 实验结果 | Baseline 对比

<div class="columns xsmall">
<div>

![w:480](../figures/delta_learn_baseline_comparison.png)

</div>
<div>

| 对比 | ΔIC | 结论 |
|---|---|---|
| B2 vs B3 | **+25.8%** | PT 价值显著 |
| B2 vs B4 | **+21.6%** | E2E > Factor |
| B2 vs B5 | **+444%** | L1 ≫ 均值 |
| B3 vs B4 | *−3.3%* | E2E ≈ Factor |

B2 优势来自 **pretrain** 而非结构差异 (B3≈B4)

B5 IC=0.012，patch 均值丢失 tick 信息

</div>
</div>

---

# 实验结果 | Per-Horizon IC

<div class="columns xsmall">
<div>

![w:480](../figures/delta_learn_per_horizon_ic.png)

</div>
<div>

| | **B2** | B3 | B4 | B5 |
|---|---|---|---|---|
| 30s | **.141** | .113 | .123 | .023 |
| 1m | **.103** | .086 | .088 | .023 |
| 3m | **.053** | .039 | .035 | .004 |
| 5m | **.043** | .030 | .030 | .005 |
| 10m | **.033** | .026 | .029 | .011 |
| 15m | **.029** | .026 | .025 | .009 |

- B2 全 horizon 最优，短 horizon 差距最大
- IC 单调递减，≥10m 各方法趋近

</div>
</div>

---

# 实验结果 | Model Scaling

<div class="columns xsmall">
<div>

![w:480](../figures/delta_learn_model_scaling.png)

</div>
<div>

| 参数 | PT IC | Δ |
|---|---|---|
| 87K | 0.2974 | — |
| 322K | 0.2963 | 0% |
| 2.3M | 0.2974 | 0% |
| 17.4M | 0.2985 | +0.07% |

参数 **200×** → IC 不变，信号复杂度远低于 87K

MS4 (17.4M) finetune 过拟合: IC ep7=0.068 → ep17=0.049

</div>
</div>

---

# 实验结果 | Data Scaling

<div class="columns xsmall">
<div>

![w:480](../figures/delta_learn_data_scaling.png)

</div>
<div>

| 规模 | FT IC | Δ |
|---|---|---|
| 2 品种×2yr | 0.0214 | — |
| 5 品种×4yr | 0.0522 | +144% |
| 10 品种×8yr | **0.0669** | **+213%** |

**全实验最强效应**: 跨品种正迁移，数据量是最重要的 scaling 维度

</div>
</div>

---

# 实验结果 | Factor Scaling & Spectral

<div class="columns">
<div>

## Factor Scaling (FS1)

<div class="xsmall">

| 实验 | 参数 | IC |
|---|---|---|
| B4 Factor | 315K | 0.0550 |
| FS1 Factor-L | 2.3M | 0.0565 |

×7 参数 → +2.7%，瓶颈在 62 维因子表示

对比 MS3 (同 2.3M, E2E): IC 0.068 > 0.057

</div>

</div>
<div>

## Spectral (S1)

<div class="xsmall">

| 指标 | 值 |
|---|---|
| IC | 0.0018 |
| RankIC | 0.0021 |

完全失败，IC ≈ 0

STFT 假设周期性不适用，待排查归一化

</div>

</div>
</div>

---

# 结论 | 五大结论

<div class="xsmall">

| | 论点 | 对比 | ΔIC | 结论 |
|---|---|---|---|---|
| **T1** | E2E vs Factor | B2 vs B4 | **+21.6%** | tick 信息 > 手工因子 |
| **T2** | Pretrain 价值 | B2 vs B3 | **+25.8%** | pretrain 是核心优势 |
| **T3** | Model scaling | 87K→17.4M | *+0.07%* | 信号复杂度有限 |
| **T4** | Data scaling | 2→10 品种 | **+213%** | 跨品种迁移极强 |
| **T5** | Factor ceiling | 315K→2.3M | *+2.7%* | 因子瓶颈在输入 |

**Worked**: PT→FT (IC=0.067), Data scaling +213%, L1 ≫ patch 均值
**Didn't**: Model scaling 饱和, Factor +2.7%, Spectral IC≈0

</div>

---

<!-- _paginate: false -->

![w:820](../figures/delta_learn_summary_4panel.png)

---

# 结论 | Next Steps

<div class="columns">
<div>

**P1: 补全实验**
- 补跑 MS1-ft, MS3-ft (30+ ep)
- 重跑 MS4-ft: lr=5e-5 + dropout=0.2
- 诊断 Spectral S1

**P2: 验证**
- Test set (2024) 评估
- 分品种 IC 分析

</div>
<div>

**P3: 扩展**
- Data scaling 上界 (20+ 品种)
- 论文写作: Scaling curves

**开放问题**
- MS4 过拟合 — 正则化？
- Data scaling 上界？
- Spectral 是否放弃？

</div>
</div>

---

<!-- _class: lead -->

# Questions?
