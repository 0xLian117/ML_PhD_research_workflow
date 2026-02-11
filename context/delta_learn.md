# Delta Learn — Hierarchical Transformer 端到端因子学习

## 概述

从期货 tick 级原始数据直接学习多 horizon 收益预测。3 层 Hierarchical Transformer 架构。
数据层通过 `FuturesStore` (data/futures_store.py) 封装 DeltaDB 查询 + tick 特征计算。

<!-- AUTO-GENERATED:tree — /workon 自动刷新，勿手动编辑 -->
## 项目结构

```
code/delta_learn/
├── config/                # YAML 配置文件
│   ├── level1_pretrain.yaml
│   ├── level2_finetune.yaml
│   ├── end2end.yaml
│   └── factor.yaml
├── data/
│   ├── __init__.py              # re-exports + create_datasets 工厂函数
│   ├── futures_store.py         # FuturesStore (封装 DeltaDB → 13维tick特征)
│   ├── transforms.py            # RollingNormalizer + IndependentFeatureTransformer
│   ├── dataset.py               # SnapshotDataset (pretrain + sequence 模式, 磁盘缓存)
│   ├── factor_dataset.py        # FactorDataset (手工因子)
│   └── factor_calculator.py     # 62 维因子计算
├── models/
│   ├── module.py                # 基础模块: CausalTransformer 等
│   ├── hierarchical_pretrain.py # 3层 Hierarchical 模型
│   ├── end2end_model.py         # 端到端模型
│   └── factor_model.py          # 因子模型
└── scripts/
    └── train.py                 # 统一训练入口
```
<!-- /AUTO-GENERATED:tree -->

## 数据层

### 数据源 (FuturesStore → DeltaDB)

`data/futures_store.py` 中的 `FuturesStore` 封装 DeltaDB 查询 + tick 特征计算:
- `FuturesStore(dsn, 'AU').load_tick_features('2024-01-02')` → 13 维 tick 特征 DataFrame
- `FuturesStore(dsn, 'AU').get_trading_days()` → 可用交易日列表
- `FuturesStore(dsn, 'AU').get_day_counts(days)` → 每日快照数量
- 底层依赖: `pip install -e code/delta_data_sdk/` (DeltaDB 查询接口)

### 13 维原始特征

| 特征 | SQL 计算 |
|------|---------|
| mid_price | (bid_price_1 + ask_price_1) / 2 |
| vwap | turnover / (volume * multiplier) |
| micro_price | (bid_1 * ask_vol_1 + ask_1 * bid_vol_1) / (bid_vol + ask_vol) |
| mid_price_lr_s1 | log(mid / lag(mid)) |
| last_price_lr_s1 | log(last / lag(last)) |
| vwap_lr_s1 | log(vwap / lag(vwap)) |
| micro_price_lr_s1 | log(micro / lag(micro)) |
| vol_diff | volume - lag(volume) |
| AskVolume1 | ask_volume_1 |
| BidVolume1 | bid_volume_1 |
| obi_1 | (bid_vol - ask_vol) / (bid_vol + ask_vol) |
| spread_1 | (ask - bid) / mid |
| OpenInterest | open_interest |

### 特征变换 (5 种)

每个原始特征独立应用 5 种 rolling 变换 → 13 × 5 = 65 维:
1. **norm**: rolling z-score
2. **std_norm**: rolling_norm(rolling_std(x)) — 波动率状态
3. **mean_norm**: rolling_norm(rolling_mean(x)) — 动量状态
4. **skew_norm**: rolling_norm(rolling_skew(x)) — 偏度 (可选)
5. **bias_norm**: rolling_norm(x/rolling_mean - 1) — 偏离度 (可选)

## 模型架构

3 层 Hierarchical Transformer:

```
Tick 序列 [3600 ticks]
    │
    ▼ (patch_size=60)
60 个 Patch [60 ticks each]
    │
    ▼ Level-1: Patch Transformer
Patch Embeddings [60, d_patch]
    │
    ▼ Level-2: Sequence Transformer
Sequence Embedding [d_seq]
    │
    ▼ Prediction Head
Multi-horizon Returns [60, 120, 360, 600, 1200, 1800 ticks]
```

## 训练模式

| 模式 | 命令 | 说明 |
|------|------|------|
| pretrain | `--mode pretrain` | Level-1 单 Patch 预训练 |
| finetune | `--mode finetune` | Level-2 微调 (Level-1 冻结) |
| end2end | `--mode end2end` | Level-1 + Level-2 端到端 |
| factor | `--mode factor` | 62 维手工因子 → Linear → Level-2 |

## 品种

默认 10 个期货品种: AU, AG, CU, AL, RB, I, RU, TA, M, P
