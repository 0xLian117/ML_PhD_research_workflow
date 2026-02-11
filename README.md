# Delta Research — ML PhD Research Workflow

Claude Code 驱动的 ML 博士研究全生命周期工作流。覆盖代码开发、实验管理、论文写作、文献综述、项目管理的超级助手。

## 目录结构

```
delta_research/                         ← 本 repo (workflow + 研究资产)
│
├── code/                               ← 代码项目 (各自独立 git repo, 不被本 repo 跟踪)
│   ├── delta_data_sdk/                 #   数据 SDK — github.com/0xLian117/delta_data_sdk
│   ├── delta_alpha/                    #   RL 符号搜索 — github.com/0xLian117/delta_alpha
│   ├── delta_learn/                    #   Hierarchical Transformer (待创建 remote)
│   └── delta_llm/                      #   LLM 因子生成 (待建)
│
├── results/                            ← 远端下载的实验结果 (本地分析)
│   ├── delta_alpha/                    #   按 {method}_{YYYYMMDD_HHMMSS}/ 组织
│   └── delta_learn/
│
├── papers/                             ← 论文 (本地草稿 → Overleaf)
│   ├── drafts/                         #   LaTeX 草稿
│   ├── templates/                      #   Venue 模板 (ICML, NeurIPS...)
│   └── published/                      #   已发表 (只读保护)
│
├── slides/                             ← Beamer slides
│   └── templates/group_meeting.tex     #   组会模板
│
├── reports/weekly/                     ← 周报
├── literature/                         ← 阅读笔记
├── figures/                            ← 论文级图表 (Python 生成)
├── explorations/                       ← 研究沙箱 (宽松规则)
├── templates/                          ← 通用模板 (周报/实验/阅读笔记)
│
├── quality_reports/                    ← Claude 生成的质量报告
│   ├── plans/                          #   任务计划
│   ├── session_logs/                   #   研究日志
│   └── reviews/                        #   代码/论文/实验审查
│
├── .claude/                            ← Claude Code 配置
│   ├── settings.json                   #   权限 + hooks
│   ├── WORKFLOW_QUICK_REF.md           #   速查手册
│   ├── hooks/                          #   4 个自动化 hook
│   ├── rules/                          #   12 条规则 (3 always-on + 9 path-scoped)
│   ├── agents/                         #   7 个只读审查 agent
│   └── skills/                         #   12 个 slash command
│
├── CLAUDE.md                           ← 项目上下文 (Claude 自动读取)
└── README.md                           ← 本文件
```

---

## 快速开始

### 1. 环境准备

```bash
# 克隆本 workflow repo
git clone <this-repo-url> delta_research
cd delta_research

# 克隆代码项目到 code/ 目录
git clone https://github.com/0xLian117/delta_data_sdk.git code/delta_data_sdk
git clone https://github.com/0xLian117/delta_alpha.git code/delta_alpha
# delta_learn 需手动创建 remote 后克隆

# 安装共享数据 SDK
pip install -e code/delta_data_sdk/
```

### 2. 远端服务器配置 (镜像目录结构)

```bash
# 在远端 GPU 服务器上
mkdir -p ~/delta_research/code
cd ~/delta_research/code

git clone https://github.com/0xLian117/delta_data_sdk.git
git clone https://github.com/0xLian117/delta_alpha.git
# git clone <delta_learn_remote> delta_learn

pip install -e delta_data_sdk/
```

### 3. 启动 Claude Code

```bash
cd delta_research
claude
```

Claude 会自动加载 CLAUDE.md + 所有 rules，识别可用 skills。

---

## 执行模型

```
本地 Mac (Claude 可操作)                      远端 GPU (用户手动)
════════════════════════                      ══════════════════
1. 在 code/ 下开发代码
2. Claude 审查 + 本地验证
3. cd code/project && git push  ──────────→  4. cd code/project && git pull
                                              5. python train.py --config ...
                                              6. tar -czf results.tar.gz outputs/
7. 下载 → 解压到 results/project/  ←────────
8. /analyze-results results/project/run_xxx
```

**关键**: 每个 code/ 下的项目是独立 git repo，各自 push/pull。
workflow repo 只跟踪研究资产（论文、笔记、报告、计划），不跟踪代码。

---

## Skills (Slash Commands)

在 Claude Code 中输入以下命令触发对应工作流。

### 代码 & 实验

| 命令 | 用途 | 示例 |
|------|------|------|
| `/commit` | Git 提交 (自动排除大文件/密钥) | `/commit "feat: add attention layer"` |
| `/review-code [file]` | 代码审查 (8 维评分) | `/review-code code/delta_learn/models/transformer.py` |
| `/experiment [hypothesis]` | 创建实验: 假设→配置→远端命令 | `/experiment "增加 patch size 从 8 到 16 可以捕获更长周期"` |
| `/analyze-results [dir]` | 分析下载的实验结果 | `/analyze-results results/delta_learn/htf_20250211_143022` |
| `/compare [dirs]` | 对比多个实验结果 | `/compare results/delta_learn/baseline results/delta_learn/ablation` |
| `/data-check [target]` | 数据管道检查 (NaN/bias/分布) | `/data-check code/delta_learn/data/` |

### 学术写作

| 命令 | 用途 | 示例 |
|------|------|------|
| `/paper-draft [section]` | 起草论文章节 (LaTeX) | `/paper-draft method` |
| `/proofread [file]` | 校对 (语法/拼写/LaTeX/术语) | `/proofread papers/drafts/main/intro.tex` |
| `/lit-review [topic]` | 文献搜索 + 综述 | `/lit-review "transformer for time series forecasting"` |

### 报告 & 汇报

| 命令 | 用途 | 示例 |
|------|------|------|
| `/weekly-report` | 生成本周研究进展报告 | `/weekly-report` |
| `/slides [topic]` | 创建 Beamer 组会 slides | `/slides "delta_learn 实验进展"` |

### 研究

| 命令 | 用途 | 示例 |
|------|------|------|
| `/research-idea [desc]` | 将模糊想法形式化为研究计划 | `/research-idea "用 LLM 直接生成因子公式"` |

---

## Rules (自动生效规则)

### Always-on (始终生效)

| 规则 | 作用 |
|------|------|
| **plan-first** | 非琐碎任务必须先写计划再执行，计划保存到 `quality_reports/plans/` |
| **orchestrator** | 自治执行循环: CODE 模式 (实现→验证→审查) / WRITE 模式 (起草→校对→审查)，质量 >= 80 方可提交 |
| **research-journal** | 研究日志协议: 计划后、发现时、session 结束前三个触发点自动记录 |

### Path-Scoped (按文件路径自动激活)

| 规则 | 触发路径 | 核心关注 |
|------|---------|---------|
| **python-ml** | `**/*.py` | 数值安全 (nanmean/log1p/除零), 可复现 (seed), logging |
| **data-pipeline** | `**/data/**` | **Look-ahead bias 零容忍**, NaN 处理, shape 验证, train/val/test 不重叠 |
| **model-conventions** | `**/model*/**` | Config 驱动, forward shape 注释, gradient clipping, checkpoint 格式 |
| **experiment-protocol** | `**/config/**, **/scripts/**` | YAML 版本化, seed=42, 一次只改一个变量, 输出目录规范 |
| **academic-writing** | `**/*.tex, **/papers/**` | 术语一致, `\newcommand` 数学符号, 引用规范, 段落结构 |
| **figures-tables** | `**/figures/**, **/plots/**` | 300 DPI, 矢量格式, 色盲友好, >=8pt 字体, 代码生成 |
| **literature-protocol** | `**/literature/**` | 阅读笔记格式, BibTeX 管理, Related Work 组织 |
| **exploration-fast-track** | `explorations/**` | 质量阈值降低到 60, 无需计划, 毕业条件 >= 80 |
| **domain-template** | `**/backtest/**, **/evaluate*` | 量化因子评估标准 (IC/IR/Sharpe), 可替换为其他领域 |

---

## Agents (审查 Agent)

所有 agent 均为**只读**审查，生成报告到 `quality_reports/reviews/`，不直接修改文件。

| Agent | 功能 | 审查维度 |
|-------|------|---------|
| **code-reviewer** | Python/PyTorch 代码审查 | 结构、数值安全、PyTorch 正确性、可复现、内存、类型、文档、风格 (8 维) |
| **paper-reviewer** | 学术论文审查 (Reviewer 2 视角) | 结构、贡献、方法、实验、写作、rejection 预判 (6 维) |
| **proofreader** | 文本校对 | 语法、拼写、LaTeX、术语一致、学术语气 |
| **experiment-reviewer** | 实验设计审查 | 假设清晰度、受控变量、基线有效性、统计严谨、配置完整 (5 维) |
| **math-reviewer** | 数学推导/证明审查 | 逻辑正确性、符号一致、边界条件、引用、完整性 |
| **verifier** | 端到端验证 (唯一可执行代码) | Python import、config 合法、LaTeX 编译、文件验证 |
| **literature-assistant** | 文献研究辅助 | 文献搜索、笔记整理、Related Work 草拟、Gap 识别 |

---

## Hooks (自动化钩子)

| Hook | 触发时机 | 作用 |
|------|---------|------|
| **notify.sh** | 任何通知 | macOS 桌面通知 (osascript) |
| **protect-files.sh** | Edit/Write 操作前 | 拦截对受保护文件的修改 (settings.json, SDK 核心, 已发表论文) |
| **pre-compact.sh** | Context 压缩前 | 保存当前状态到 session log (防止上下文丢失) |
| **log-reminder.py** | Claude 停止响应时 | 20 次响应未更新日志则弹出提醒 |

### 受保护文件列表

| 类别 | 文件 |
|------|------|
| 配置 | `settings.json`, `settings.local.json` |
| SDK 核心 | `code/delta_data_sdk/**/api.py`, `store.py`, `schema.py` |
| SDK 包定义 | `code/delta_data_sdk/setup.py`, `pyproject.toml` |
| 已发表 | `papers/published/**` |

---

## 质量门控

| 场景 | 阈值 | 说明 |
|------|------|------|
| 代码提交 | >= 80/100 | code-reviewer 评分 |
| 论文章节 | >= 80/100 | paper-reviewer + proofreader |
| 探索性代码 | >= 60/100 | explorations/ 目录下宽松标准 |

### 因子评估标准

| 指标 | 阈值 |
|------|------|
| \|IC_mean\| | > 0.015 |
| \|IR\| | > 0.3 |
| IC 一致性 | > 52% |
| Sharpe | > 0 |

---

## 模板

| 模板 | 路径 | 用途 |
|------|------|------|
| 周报 | `templates/weekly_report.md` | `/weekly-report` 生成的报告格式 |
| 实验记录 | `templates/experiment_log.md` | `/experiment` 生成的实验文档格式 |
| 阅读笔记 | `templates/reading_note.md` | 文献阅读笔记格式 |
| 组会 slides | `slides/templates/group_meeting.tex` | Beamer 模板 (Metropolis 主题) |

---

## 典型工作流程

### 新实验

```
1. /experiment "假设描述"           → 生成 config + 实验记录 + 远端命令
2. /commit                         → 提交代码到项目 repo
3. (远端) git pull && python train.py  → 运行
4. (远端) tar 结果 → 下载到 results/
5. /analyze-results results/...     → 分析报告
6. /compare results/baseline results/new  → 对比 (可选)
```

### 写论文

```
1. /lit-review "主题"               → 文献搜索 + 笔记
2. /paper-draft intro               → 起草 Introduction
3. /proofread papers/drafts/.../intro.tex  → 校对
4. 复制到 Overleaf                   → 最终排版
```

### 周例行

```
1. /weekly-report                   → 自动汇总本周进展
2. /slides "本周进展"               → 生成组会 slides (可选)
```

---

## 不可违反的规则 (Non-Negotiables)

1. **Look-ahead bias 零容忍** — 数据管道中不允许使用未来信息
2. **每个实验必须有 seed** — 默认 42, 消融 [42, 123, 456, 789, 1024]
3. **NaN 必须检查和处理** — 每步操作后验证
4. **Test split 开发期间禁用** — 只在最终评估时使用
5. **论文数据必须可复现** — 代码生成, 非手动编辑
6. **代码和 workflow 分离** — code/ 下各项目独立 repo, workflow repo 不跟踪代码
