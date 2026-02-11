# Delta Alpha — 期货 AlphaGPT (符号因子搜索)

## 概述

基于 Transformer 的期货 Alpha **时序因子**挖掘系统。使用强化学习（Actor-Critic）自动搜索有效的交易公式。

**核心特点**:
- **多品种联合训练**: 每步所有品种独立随机窗口，中位数聚合评分，天然去噪
- **多频率因子挖掘**: 1min/3min/5min/15min 各自 h1，覆盖不同时间尺度
- Polish Notation 生成公式，Action Masking 保证语法正确
- LoRD 正则化加速训练，防止过拟合
- 真实 bid/ask 滑点模型
- Rolling robust normalization (median+MAD, 无 look-ahead)

## 技术栈

- Python 3.10+
- PyTorch 2.0+
- PostgreSQL + TimescaleDB (数据源: delta_data SDK)
- SQLAlchemy

<!-- AUTO-GENERATED:tree — /workon 自动刷新，勿手动编辑 -->
## 项目结构

```
code/delta_alpha/
├── config.py           # 全局配置 (DSN, 特征, 模型架构, 训练超参)
├── experiments.json    # 批量实验配置 (多频率挖掘)
│
├── scripts/
│   ├── train.py        # 训练入口 (CLI 驱动)
│   ├── evaluate.py     # 样本外因子评估 (IC + 回测)
│   ├── run_pipeline.py # 并行多实验管线
│   └── mine_factors.sh # 多 GPU 批量挖掘脚本
│
├── data/
│   ├── loader.py       # 从数据库加载 tick → OHLCV (via delta_data SDK)
│   └── features.py     # 10 维特征工程 (rolling median+MAD, 无 look-ahead)
│
├── model/
│   ├── alphagpt.py     # Transformer 模型 + LoRD + QKNorm
│   ├── vm.py           # StackVM 公式执行器 (EOS 感知, 向量化批量执行)
│   ├── ops.py          # 12 个算子 (11 常规 + EMAZSCORE/EOS)
│   └── engine.py       # 训练引擎 (多品种采样 + Action Masking + Actor-Critic)
│
├── backtest/
│   └── engine.py       # 期货回测 (Sortino评分, 真实滑点, per-symbol聚合)
│
├── portfolio/          # 仓位管理
├── strategy/           # 策略框架
├── execution/          # 执行层 (抽象接口)
├── dashboard/          # 监控面板
└── docs/               # 文档
```
<!-- /AUTO-GENERATED:tree -->

## 核心概念

### 训练理念

训练 = **引导式多样化搜索**，不是收敛优化。模型的价值是枚举有效公式，不是收敛到"最优"。

- 每步评估所有品种 (各自独立随机窗口)，中位数聚合 → 抗 reward hacking
- Entropy 不衰减 (constant 0.10)，维持探索多样性
- 多时间尺度通过多 interval 实现 (1min/3min/5min/15min 各自 h1)
- 因子最终用途: 作为下游时序预测模型的输入特征

### 特征 (10 维)

| 特征 | 说明 | 归一化 |
|------|------|--------|
| ret | 对数收益率 | rolling median+MAD |
| realized_vol | intra-bar 实现波动率 (SQL stddev/avg) | rolling median+MAD |
| pressure | 买卖压力 (close-open)/(high-low) | 天然 [-1,1] |
| momentum | 20-bar 累积收益率 | rolling median+MAD |
| log_volume | 对数成交量 log1p(volume) | rolling median+MAD |
| oi_change | 持仓量变化率 | rolling median+MAD |
| obi | 订单簿不平衡 | 天然 [-1,1] |
| spread | 相对买卖价差 | rolling median+MAD |
| depth | 订单簿深度 | rolling median+MAD |
| vwap_dev | VWAP偏离度 | rolling median+MAD |

### 算子 (12 个)

- 算术 (7): ADD, SUB, MUL, DIV, NEG, ABS, SIGN
- 时序 (4): DELTA5, MA20 (线性衰减), STD20 (z-score), TS_RANK20
- EOS (1): EMAZSCORE (终结算子, stack==1 且 step>=1 时可选择终止)

### 词表

23 tokens = 10 特征 + 12 算子 + 1 SOS
Token 布局: `[0-9: features | 10-20: regular ops | 21: EMAZSCORE/EOS | 22: SOS]`

## 数据依赖

通过 `delta_data` SDK 统一接口访问数据:

```python
from delta_data import FuturesStore

store = FuturesStore(DSN, 'AU')

# OHLCV + 微结构聚合
df = store.load_bars('2024-01-01', '2024-06-30', '1 minute')
# → open, high, low, close, volume, obi, spread, depth, realized_vol, ...
```

安装: `pip install -e code/delta_data_sdk/`

## 运行方式

```bash
# 虚拟数据测试
python scripts/train.py --test

# 单频率训练
python scripts/train.py \
    --symbols FUT:au FUT:cu FUT:rb FUT:ru \
    --interval "5 minutes" \
    --steps 2000 --batch-size 8192

# 多 GPU 批量挖掘 (1min/3min/5min/15min × 4 GPU)
bash scripts/mine_factors.sh

# 评估
python scripts/evaluate.py --run-dir runs/mining_*/1min/20*

# Pipeline (JSON 配置驱动)
python scripts/run_pipeline.py --config experiments.json
```

## 配置说明

`config.py` — 基础设施 + 模型架构 + 训练默认值:
- `DSN`: 数据库连接字符串
- `FEATURE_NAMES`: 10 维特征列表
- `D_MODEL`, `N_LAYERS`, `N_HEADS`, `MAX_FORMULA_LEN`: 模型架构
- `ENTROPY_COEF = 0.10` (constant, no decay)
- `TARGET_HORIZON = 1`, `TOP_K = 100`
- `FEE_RATE`, `SLIPPAGE`: 回测费用

实验参数通过 CLI 传入:
- `--symbols`, `--interval`, `--train-start/end`, `--eval-start/end`
- `--steps`, `--batch-size`, `--lr`
- `--target-horizon`, `--top-k`, `--window-bars`

## 评估标准

通过条件 (至少 1 个 horizon 满足):
- Backtest Sharpe > 0
- |IC| > 0.015, |IR| > 0.3, IC 正比例 > 52%

Multi-horizon IC 评估: [1, 6, 12, 48, 240] bars

## 当前状态

- [x] 数据加载 (按品种独立, 支持期货+加密货币)
- [x] 特征工程 (10 维, rolling robust normalization)
- [x] AlphaGPT 模型 + LoRD 正则化
- [x] StackVM 执行器 + Action Masking + 变长公式
- [x] 期货回测引擎 (Sortino评分, 真实滑点)
- [x] 多品种联合训练 (统一窗口, 中位数聚合)
- [x] 多频率挖掘管线 (1min/3min/5min/15min)
- [x] 样本外 IC 评估 + 回测验证
- [ ] 真实数据训练验证
- [ ] CTP 期货接口实现
- [ ] 公式可视化/解释
