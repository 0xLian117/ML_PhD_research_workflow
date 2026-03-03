---
marp: true
math: mathjax
theme: delta-lab
paginate: true
---

<!-- _class: lead -->
<!-- _paginate: false -->

# 项目进展

时序因子挖掘: 符号搜索 & 端到端学习

2026年3月

---

# Outline

1. **研究概览** — 整体框架与技术路线
2. **Delta Alpha** — RL 符号公式搜索 (流程已跑通)
3. **Delta Learn** — 端到端因子学习
   - 数据处理 · 模型架构 · 数据流
   - 实验设计 · 验证集结果
4. **总结与后续计划**

---

# 研究概览 | 核心问题

> 金融时序数据中是否存在可学习的、具有样本外预测能力的模式 (因子)？

<div class="columns small">
<div>

```
          时序因子挖掘
              │
   ┌──────────┼──────────┐
   │          │          │
符号搜索     端到端学习   LLM 挖掘
delta_alpha  delta_learn  (待建)
   │          │
搜索公式空间  原始tick直接学
→ 符号因子   → 预测信号
   │          │
   └──────────┼──────────┘
              │
         统一评估框架
      IC / 回测 / 去重
```

</div>
<div>

**两条已实现路线**

- **Delta Alpha**: RL + Transformer 自动搜索公式空间，输出可解释符号因子
- **Delta Learn**: Hierarchical Transformer 从 tick 数据端到端学习，输出连续预测信号

**互补性**
- 符号因子: 可解释、可组合
- 端到端信号: 表达力强、多 horizon

</div>
</div>

---

<!-- _class: lead -->
<!-- _paginate: false -->

# Part I: Delta Alpha

RL 符号公式搜索

---

# Delta Alpha | 核心思路

<div class="columns small">
<div>

**目标**: 自动搜索**可解释**的交易公式

**方法**: Transformer + REINFORCE

- 公式 = Polish notation 序列
- 模型自回归生成公式 token
- StackVM 执行公式 → 信号
- 回测计算 reward
- Policy gradient 更新

**核心理念**
训练 = **引导多样性搜索**
不是优化单一公式，而是枚举有效公式

</div>
<div>

**公式示例**

```
ret vol MUL DELTA5 EMAZSCORE
→ EMAZSCORE(DELTA5(ret × vol))
```

**搜索空间**
- 10 个输入特征 (ret, vol, pressure, ...)
- 12 个算子 (7 算术 + 4 时序 + EOS)
- 公式长度 ≤ 12 tokens
- Action Mask 保证合法 Polish notation

</div>
</div>

---

# Delta Alpha | 系统架构

<div class="columns small">
<div>

```
AlphaGPT (d=128, 2L, 4H)
  ├─ Actor → logits    ─┐
  └─ Critic → baseline  │
         │               │
    Action Mask (栈验证) │
         ▼               │
    StackVM 批量执行     │
    [B×S×T] GPU 向量化   │
         ▼               │
    回测 (Sortino)  ───→ REINFORCE
    真实滑点+手续费      更新
```

**训练循环 (每步)**
1. Transformer 生成 B=16384 条公式
2. StackVM 批量执行 → 信号 [B, S, T]
3. 多品种回测 → 中位 Sortino reward
4. Actor-Critic 更新 (REINFORCE)

</div>
<div>

**关键设计**
- **多品种联合训练**: 中位 reward 防止单品种过拟合
- **随机时间窗**: 每步不同区间 → 多行情采样
- **恒定 entropy bonus** (0.10): 维持探索

**模型细节**
- RMSNorm + SwiGLU + QKNorm
- LoRD 正则化 (低秩衰减)
- Causal mask 自回归生成

**特征**: 10 维 rolling robust normalized
- ret, realized_vol, pressure, momentum
- log_volume, oi_change, obi, spread, depth, vwap_dev

</div>
</div>

---

# Delta Alpha | 当前状态与后续定位

<div class="columns small">
<div>

**已完成**
- 端到端流程已跑通 (test mode 验证)
- 数据加载 → 特征工程 → 训练 → 评估 全链路
- 多品种联合训练 + 多频率批量挖掘脚本

**评估框架**
- 多 horizon IC + 分品种独立测试
- 因子去重 (信号相关 > 0.7 去除)
- 仍需设计

</div>
<div>

**后续定位**
- 作为 **baseline 对比** delta_learn
- 符号因子可解释性是独特优势
- 可与 delta_learn 信号**互补组合**

**待完成**
- 真实数据大规模训练 (远端 GPU)
- reward 设计

</div>
</div>

---

<!-- _class: lead -->
<!-- _paginate: false -->

# Part II: Delta Learn

端到端 Tick-Level 因子学习

---

# Delta Learn | 数据处理流水线

<div class="columns small">
<div>

**数据源**
- 中国期货 10 品种 (AU, AG, CU, AL, RB, I, RU, TA, M, P)
- 500ms 快照，~50,000 ticks/天/品种
- TimescaleDB → `delta_data` SDK

**13 维原始特征**

| 类别 | 特征 |
|---|---|
| 价格 | mid_price, vwap, micro_price |
| 收益 | 4 种 log return (mid/last/vwap/micro) |
| 订单簿 | obi, spread, bid_vol, ask_vol |
| 量/仓 | vol_diff, OpenInterest |

</div>
<div>

**4 种 Rolling 变换 → 52 维**

| 变换 | 含义 |
|---|---|
| `norm` | rolling z-score (位置) |
| `std_norm` | rolling_norm(std) (波动率状态) |
| `mean_norm` | rolling_norm(mean) (动量状态) |
| `skew_norm` | rolling_norm(skew) (分布形状) |

- 窗口: 1800 ticks (15min)
- Clip ±5，NaN → 0
- **无 look-ahead bias**: 逐 tick 滚动计算

**数据划分**
- Train: 2015–2022 / Val: 2023 / Test: 2024 H1
- ⚠ I, M, P 三品种 train 仅到 2021 (DB 缺 2022)

</div>
</div>

---

# Delta Learn | 数据流: Tick → Patch → Sequence

<div class="columns small">
<div>

**Pretrain 路径 (Stage 1)**
```
原始 tick (T=50000/天, 13D)
  ↓ 13×4 rolling transforms
变换后 (T, 52D)
  ↓ stride=180, seq_len=60
单 patch (60 ticks, 52D)
  ↓ ~267 样本/天/品种
L1 Transformer
  ↓
短 horizon 预测 (7 targets)
[2,4,6,8,10,15,30] ticks
(1s ~ 15s)
```

**全量**: ~5.3M 样本 (10品种×2000天)

</div>
<div>

**Finetune / E2E 路径 (Stage 2)**
```
变换后 (T, 52D)
  ↓ stride=1800, seq_len=3600
完整序列 (3600 ticks, 52D)
  ↓ patch 切分
(60 patches, 60 ticks, 52D)
  ↓ L1 frozen → L2 Transformer
长 horizon 预测 (6 targets)
[60,120,360,600,1200,1800] ticks
(30s ~ 15min)
```

**全量**: ~480K 样本 (10品种×2000天)

</div>
</div>

**关键约束**: 样本不跨日 · 每日前 1800 ticks 为 warmup · 无 look-ahead bias

---

# Delta Learn | 模型架构: 四种方法对比

<div class="columns small">
<div>

**Method A: Factor Model** (~295K)
```
62D 手工因子 → MLP (62→128)
→ L2 Transformer → Head → (B, 6)
```

**Method B: End-to-End** (~503K)
```
(B,60,60,52) raw ticks
→ L1 Transformer → patch emb (B,60,128)
→ L2 Transformer → Head → (B, 6)
```

**Method C: Hierarchical PT→FT** (~503K)
```
Stage 1: patch → L1 → (B,7) 短horizon
Stage 2: L1🔒 → L2(trainable) → (B,6) 长horizon
```

</div>
<div>

**Method D: Spectral** (~328K)
```
7ch STFT → log幅度谱 (60,7,61)
→ 共享 CausalConv1d → L2 → Head → (B, 6)
```

| 方法 | 输入 | 编码器 | 目的 |
|---|---|---|---|
| A | 62D 因子 | MLP | 手工 baseline |
| B | 52D tick | L1+L2 Joint | 无 pretrain |
| C | 52D tick | L1 PT+frozen | **主方法** |
| D | 7ch STFT | Conv1d | 频域探索 |

**Inductive Bias**: 30s patch (L1) → 30min sequence (L2)
**统一组件**: L2 = CausalTransformer (1L, 4H, d=128)

</div>
</div>

---

# Delta Learn | 62D 手工因子设计

<div class="columns small">
<div>

**输入**: 每个 Patch (60 ticks × 13 原始特征)
**输出**: 62 维因子向量

| 类别 | 维度 | 内容 |
|---|---|---|
| 价格统计 | 15 | mean/std/range/slope × 多价格 |
| 收益率统计 | 5 | mean, std, skew, kurt, last |
| 收益率分段 | 3 | 前半/后半/比值 |
| 波动率 | 3 | realized vol, high-low, parkinson |
| OBI 统计+动态 | 8 | mean/std/trend/变化率 |
| 价差统计 | 5 | mean/std/range/趋势 |
| 量/仓/挂单 | 14 | 成交量形态/挂单量/持仓 |
| 量价/交互/时序 | 9 | corr/autocorr/趋势强度 |

</div>
<div>

**设计思路**
- 参考传统量化高频因子库
- Patch 内统计量 → 压缩 60 ticks 为固定维度
- 53 维需 cross-sectional norm，9 维天然有界

**已知问题**
- 因子设计较为基础，未经充分筛选优化
- 62D 中部分因子可能冗余或信噪比低
- **E2E (52D tick) > 手工因子 (62D)**: IC +25%
- 因子质量改进是重要的后续方向
  - LLM 辅助因子生成 + 自动化筛选
  - 与 RL 符号搜索输出互补

</div>
</div>

---

# Delta Learn | 实验设计

<div class="columns small">
<div>

**5 个核心假设**

| ID | 假设 | 对比 |
|---|---|---|
| T1 | E2E tick > 手工因子 | B2 vs B4 |
| T2 | Pretrain 有显著价值 | B2 vs B3 |
| T3 | 模型参数扩展有边际收益 | MS1–4 |
| T4 | 数据量是关键 scaling 维度 | DS1–3 |
| T5 | 因子模型有表达力上限 | B4 vs FS1 |

**控制变量**
- B5 (Stat Baseline): patch 均值 → 去除 tick 时序信息
- S1 (Spectral): STFT 频域 → 探索替代表示

</div>
<div>

**8 组实验配置**

| ID | 方法 | 关键差异 | 参数量 |
|---|---|---|---|
| B1→B2 | PT→FT | **主方法** | 322K |
| B3 | E2E | 无 pretrain | 503K |
| B4 | Factor | 62D 手工因子 | 295K |
| B5 | Stat BL | patch 均值 | 295K |
| MS1–4 | Scaling | d=64/128/256/512 | 87K→17.4M |
| DS1–3 | Scaling | 2/5/10 品种 | 322K |
| FS1 | Factor-L | Factor ×7 | 2.3M |
| S1 | Spectral | STFT | ~500K |

**训练**: AdamW + Cosine LR, bf16, 早停 patience=15

</div>
</div>

---

# Delta Learn | Val 结果: Baseline 对比

<div class="columns small">
<div>

![w:480](../figures/baseline_val_test.png)

</div>
<div>

**关键发现**

| 对比 | ΔIC | 结论 |
|---|---|---|
| B2 vs B3 | **+23%** | Pretrain 价值显著 |
| B2 vs B4 | **+22%** | E2E tick > 手工因子 |
| B2 vs B5 | **+444%** | L1 Transformer ≫ 均值 |
| B3 vs B4 | −3.3% | 无 PT 时 E2E ≈ Factor |

- B2 全 horizon 最优，短 horizon 差距最大
- **核心结论**: B2 优势来自 **pretrain**
- Test IC 普遍高于 Val，泛化良好

</div>
</div>

---

# Delta Learn | Scaling 实验

<div class="columns small">
<div>

![w:480](../figures/model_scaling.png)

- 参数 **200×** → IC +0.07%，信号复杂度有限
- MS4 (17.4M) finetune 过拟合

</div>
<div>

![w:480](../figures/data_scaling.png)

- **全实验最强效应**: 跨品种正迁移
- 2→10 品种: Val +214%, Test +141%

</div>
</div>

---

# Delta Learn | Per-Horizon IC: Val vs Test

![w:900 center](../figures/per_horizon_val_test.png)

<div class="small">

- B2 (PT→FT) **全 horizon、Val + Test 均最优**
- IC 随 horizon 单调递减，≥10min 各方法趋近
- Test IC 普遍高于 Val (+17~22%)，泛化良好

</div>

---

# Delta Learn | Test Set 结果 (2024 H1)

<div class="columns small">
<div>

**Baseline Test IC**

| 实验 | Val IC | Test IC | Δ |
|---|---|---|---|
| **B2 (PT→FT)** | 0.067 | **0.081** | +20% |
| B3 (E2E) | 0.055 | **0.067** | +22% |
| B4 (Factor) | 0.055 | **0.064** | +17% |
| FS1 (Factor-L) | 0.057 | **0.068** | +19% |
| B5 (Stat BL) | 0.013 | 0.012 | −5% |
| S1 (Spectral) | 0.003 | **0.000** | — |

S1 (STFT 频谱): IC ≈ 0，方法完全失败

</div>
<div>

**Data Scaling Test IC**

| 数据规模 | Val IC | Test IC |
|---|---|---|
| 2 品种 | 0.021 | **0.033** |
| 5 品种 | 0.052 | **0.065** |
| 10 品种 | 0.067 | **0.081** |

**泛化确认**: 5 个假设在 test set 上全部成立
⚠ I/M/P 三品种 train 缺 2022 数据

</div>
</div>

---

<!-- _paginate: false -->

![w:820 center](../figures/summary_4panel_val_test.png)

---

# Delta Learn | 关键 Insights

<div class="columns small">
<div>


**1. Pretrain 质量决定 Finetune 上限**
- B2 v1 → v2: Test IC +14% (仅改善 pretrain)
- 相同 finetune 配置，pretrain 质量直接传导

**2. Spectral (S1) 完全失败**
- 思路: 7 通道平稳特征 → STFT (n_fft=120) → log 幅度谱 (60×7×61) → 共享 CausalConv1d → Transformer
- 类似 Whisper 音频编码，用频域替代时域输入
- Val IC = 0.003, Test IC ≈ 0 (全 horizon 随机水平)

</div>
<div>

**3. 数据扩展 >> 模型扩展**
- 模型 200× 参数: IC +0.07% (饱和)
- 数据 5× 品种: IC +141% (远未饱和)
- 跨品种正迁移是核心驱动力

**4. 因子瓶颈在输入而非模型容量**
- Factor 参数 315K→2.3M (×7): Test IC 仅 +6.1%
- 瓶颈在 62D 因子输入，非模型容量

**5. 超参调优效果有限**
- 10 组 sweep (LR/dropout/WD): IC 仅 0.042~0.050
- 同架构 10 品种 B3 = 0.067，33% gap 无法靠调参弥补
- 再次印证: **数据量 >> 超参优化**

</div>
</div>

---

<!-- _class: lead -->
<!-- _paginate: false -->

# 总结与后续计划

---

# 总结 | 当前进展

<div class="columns small">
<div>

**Delta Alpha** (符号搜索)
- 端到端流程已跑通
- Transformer + REINFORCE + StackVM
- 多品种联合训练 + 多频率挖掘
- 可作为 baseline 和互补工具
- 待: 大规模训练 + IC reward 改进

**Delta Learn** (端到端学习)
- 完整数据管线: tick → 52D → patch → sequence
- 三种模型变体 + 控制实验
- 5 个核心假设 Val + Test 双确认 ✓

</div>
<div>

**Delta Learn 核心发现 (Val + Test 双确认)**

| 结论 | Val | Test |
|---|---|---|
| Pretrain 是关键 | B2 vs B3: +23% | +21% |
| E2E > 手工因子 | B2 vs B4: +22% | +25% |
| 模型扩展饱和 | 200× → +0.07% | — |
| **数据扩展最重要** | 2→10: +214% | +141% |
| 因子表达力有上限 | 315K→2.3M: +3.6% | +6.1% |

**最佳配置**: PT→FT, 10 品种, d=128
**Val IC = 0.067, Test IC = 0.081**

</div>
</div>

---

# 后续方向 | 时序特征提取范式

<div class="columns small">
<div>

**已探索的特征提取范式**

| 范式 | 方法 | 结果 |
|---|---|---|
| 手工因子 | 62D 统计量 | IC 0.064 |
| Rolling 变换 | 13→52D 时域 | IC **0.081** |
| 频域 (STFT) | 7ch log 幅度谱 | IC ≈ 0 |
| RL 符号搜索 | Polish notation | 流程就绪 |
| **LLM 生成** | **待探索** | — |

**核心发现**: 时域 >> 频域，数据量 >> 模型容量

</div>
<div>

**下一步: LLM 驱动的因子挖掘**
- RD-Agent: LLM 自动生成因子代码 + 迭代优化
- QuantAlpha: LLM 辅助因子搜索与组合
- 与 Delta Alpha (RL) / Delta Learn (DL) 对比

**因子质量改进**
- 当前 62D 手工因子较基础，未经充分筛选
- LLM + 自动化评估 → 高质量因子库
- 更好的因子输入 → Factor Model 上限提升

**时域 + 频域融合**
- S1 单独失败，但频谱可作为辅助特征
- 52D 时域 + STFT 频域 → 多视角输入

**统一视角**: 金融时序特征提取方式的系统性对比

</div>
</div>

---

<!-- _class: lead -->

# Q & A
