# Delta Research — 金融时序可预测模式的挖掘

## 研究主题

金融时序数据中是否存在可学习的、具有样本外预测能力的模式 (因子)？三条技术路线:

```
                        时序因子挖掘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
   符号搜索 (RL)       端到端学习 (DL)      LLM 挖掘
   delta_alpha          delta_learn         delta_llm (待建)
         │                  │                  │
   搜索公式空间        原始 tick 直接学       自然语言生成
   Polish notation     Hierarchical          因子逻辑
   → 符号因子          Transformer           → 公式/代码
         │              → 预测信号              │
         └──────────────────┼──────────────────┘
                            │
                      统一评估框架
                  IC / 回测 / 去重 / 组合
                            │
                  delta_data SDK (数据源)
```

## 项目结构

```
delta_research/                    ← workflow repo (本仓库)
├── CLAUDE.md                      ← 本文件 (跨项目导航)
├── README.md                      ← workflow 使用说明
├── .claude/                       ← Claude Code workflow 配置
│
├── code/                          ← 代码项目 (各自独立 git repo)
│   ├── delta_data_sdk/            # 数据 SDK (TimescaleDB) ── git repo
│   ├── delta_alpha/               # 方法1: RL 符号公式搜索 ── git repo
│   ├── delta_learn/               # 方法2: Hierarchical Transformer ── git repo
│   └── delta_llm/                 # 方法3: LLM 因子生成 (待建)
│
├── results/                       ← 远端下载的实验结果 (本地分析)
│   ├── delta_alpha/               # delta_alpha 实验结果
│   └── delta_learn/               # delta_learn 实验结果
│
├── papers/                        # 论文草稿 (→ Overleaf)
├── slides/                        # Beamer slides
├── reports/                       # 周报/月报
├── literature/                    # 阅读笔记
├── figures/                       # 论文级图表
├── quality_reports/               # 计划/日志/审查报告
├── explorations/                  # 研究沙箱
└── templates/                     # 通用模板
```

### 代码仓库 (独立 git repo)

| 仓库 | 路径 | Remote |
|------|------|--------|
| delta_data_sdk | `code/delta_data_sdk/` | `github.com/0xLian117/delta_data_sdk` |
| delta_alpha | `code/delta_alpha/` | `github.com/0xLian117/delta_alpha` |
| delta_learn | `code/delta_learn/` | (待创建) |

每个项目独立 push/pull，本 workflow repo 不跟踪代码内容。

### 结果目录

远端实验结果下载到 `results/` 对应项目目录:
```
results/
├── delta_alpha/
│   └── {method}_{YYYYMMDD_HHMMSS}/    ← 每次实验一个子目录
│       ├── config.yaml
│       ├── history.json
│       ├── best.pt
│       └── train.log
└── delta_learn/
    └── {method}_{YYYYMMDD_HHMMSS}/
        ├── config.yaml
        ├── history.json
        ├── best.pt
        └── train.log
```

## 统一数据接口

所有项目通过 `delta_data` SDK 访问数据库，不直接使用 sqlalchemy/asyncpg:

```
┌─────────────────────────────────────────────────┐
│        delta_data SDK (pip install -e)           │
│                                                  │
│  DeltaDB ─── 只读查询 API                       │
│    ├─ query(symbol, start, end) → DataFrame  │   │
│    ├─ query_day(symbol, day) → DataFrame     │   │
│    ├─ query_underlying(underlying, s, e)     │   │
│    ├─ sql("SELECT ...") → DataFrame         │   │
│    └─ list_symbols / list_trading_days       │   │
│                                              ↓   │
│  market_snapshots (TimescaleDB hypertable)       │
│  market_trades (逐笔成交)                        │
└─────────────────────────────────────────────────┘
         ↑                    ↑
         │                    │
  delta_alpha             delta_learn
  FuturesDataLoader       FuturesStore (data/futures_store.py)
  (DeltaDB.sql →          (DeltaDB.sql → 13维tick特征)
   OHLCV bars)                ↓
         ↓                SnapshotDataset / FactorDataset
  FeatureEngineer         IndependentFeatureTransformer
  (10维 bar特征)           (13×5=65维 tick特征)
         ↓                    ↓
  AlphaEngine             Hierarchical Transformer
  (RL公式搜索)             (多horizon预测)
```

### 安装
```bash
cd delta_research
pip install -e code/delta_data_sdk/   # 所有子项目共享
```

### DSN
```python
DSN = "postgresql://deltadb:delta_data@10.246.1.175:5432/deltadb"
```

## 各项目职责

### delta_data SDK — 只读数据查询
- 路径: `code/delta_data_sdk/`
- TimescaleDB: `market_snapshots` (盘口快照), `market_trades` (逐笔成交)
- Python 包: `DeltaDB` (同步查询), `AsyncDeltaDB` (异步查询)
- 纯查询层，不含业务逻辑 (特征计算、归一化等在各项目自行实现)

### delta_alpha — 符号因子搜索 (RL)
- 路径: `code/delta_alpha/`
- Transformer + REINFORCE 自回归生成后缀公式
- 数据: `DeltaDB.sql()` → OHLCV bars → 10 维 bar 特征 → StackVM 执行
- 输出: `top_formulas.json` (符号因子, 可解释)
- 详细文档: `code/delta_alpha/CLAUDE.md`

### delta_learn — 端到端因子学习 (Hierarchical Transformer)
- 路径: `code/delta_learn/`
- 3 层架构: Patch Transformer → Sequence Transformer → Prediction
- 数据: `FuturesStore` (delta_learn/data/) → 13 维 tick 特征 × 5 变换 = 65 维
- `FuturesStore` 封装 DeltaDB 查询 + tick 特征计算
- 输出: 模型权重 + 多 horizon 预测信号
- 详细文档: `code/delta_learn/CLAUDE.md`

### delta_llm — LLM 因子生成 (待建)
- 路径: `code/delta_llm/` (待创建)
- 用 LLM 生成因子逻辑 (自然语言 → 公式)
- 与 delta_alpha 共享评估框架

## 共享约定

### 评估标准
| 指标 | 阈值 |
|------|------|
| \|IC_mean\| | > 0.015 |
| \|IR\| | > 0.3 |
| IC 一致性 | > 52% |
| Sharpe | > 0 |

### Forward Return
```
fwd_ret[t] = log(close[t+1+h] / close[t+1])   # delay=1
```
signal 在 bar t 形成, bar t+1 执行, bar t+1+h 平仓。

## 跨项目操作

在 `delta_research/` 根目录下工作时可以访问所有子项目。
各子项目有自己的 `CLAUDE.md` 提供详细上下文。
代码在 `code/` 目录下，实验结果在 `results/` 目录下。

### 远端服务器目录结构 (与本地 code/ 对齐)
```
remote:~/delta_research/
├── code/
│   ├── delta_data_sdk/    # git clone → pip install -e
│   ├── delta_alpha/       # git clone
│   └── delta_learn/       # git clone
└── outputs/               # 训练输出 (tar → 下载到本地 results/)
```

---

## Workflow — ML PhD Research Assistant

详细参考: `.claude/WORKFLOW_QUICK_REF.md`

### Skills 速查
| 命令 | 用途 |
|------|------|
| `/commit` | Git 提交工作流 |
| `/review-code [file]` | 代码审查 |
| `/experiment [hypo]` | 新实验 (含远端运行命令) |
| `/analyze-results [dir]` | 分析下载的实验结果 |
| `/compare [dirs]` | 对比实验 |
| `/data-check [target]` | 数据管道检查 |
| `/paper-draft [section]` | 论文章节草稿 |
| `/proofread [file]` | 校对 |
| `/lit-review [topic]` | 文献综述 |
| `/weekly-report` | 周报 |
| `/slides [topic]` | 组会 Beamer slides |
| `/research-idea [desc]` | 形式化研究想法 |

### 质量门控
- **代码/论文**: >= 80 分可提交, < 80 修复后重试
- **explorations/**: >= 60 分即可, 无需事先计划
- **Look-ahead bias**: 零容忍

### 执行模型 (Remote GPU)
本地 Mac 负责开发 + 写作 + 审查。训练/实验在远端 GPU 服务器运行。
1. 本地: 开发 → 验证 → 在 `code/project/` 中 `git push`
2. 远端 (用户手动): `git pull` → 运行 → tar 结果
3. 本地: 下载结果到 `results/project/` → `/analyze-results` 分析

### 日志位置
- 计划: `quality_reports/plans/`
- 会话日志: `quality_reports/session_logs/`
- 审查报告: `quality_reports/reviews/`
- 周报: `reports/weekly/`

### 论文写作流程
1. 本地起草: `/paper-draft [section]` → `papers/drafts/`
2. 校对: `/proofread [file]`
3. 复制到 Overleaf 进行最终排版
4. BibTeX 维护在 `papers/references.bib`
