# ML PhD Research Workflow

Claude Code 驱动的 ML 博士研究全生命周期工作流。覆盖代码开发、实验管理、论文写作、文献综述、项目管理。

设计为**通用模板**：clone 后按自己的研究方向定制 `CLAUDE.md` 和 `domain-template` 即可使用。

## 目录结构

```
your_research/                          ← 本 repo (workflow + 研究资产)
│
├── context/                            ← 项目上下文 (/workon 读取)
│   ├── project_a.md                    #   项目 A 完整上下文 (目的/架构/进度)
│   └── project_b.md                    #   项目 B 完整上下文
│
├── code/                               ← 代码项目 (各自独立 git repo, 不被本 repo 跟踪)
│   ├── project_a/                      #   git repo — 你的项目 A
│   ├── project_b/                      #   git repo — 你的项目 B
│   └── shared_lib/                     #   git repo — 共享依赖库 (可选)
│
├── results/                            ← 远端下载的实验结果 (本地分析)
│   ├── project_a/                      #   按 {method}_{YYYYMMDD_HHMMSS}/ 组织
│   └── project_b/
│
├── papers/                             ← 论文 (本地草稿 → Overleaf)
│   ├── drafts/                         #   LaTeX 草稿
│   ├── templates/                      #   Venue 模板 (ICML, NeurIPS, AAAI...)
│   └── published/                      #   已发表 (只读保护)
│
├── slides/                             ← Beamer slides
│   └── templates/group_meeting.tex     #   组会模板 (Metropolis 主题)
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
│   ├── hooks/ (4)                      #   自动化钩子
│   ├── rules/ (12)                     #   3 always-on + 9 path-scoped
│   ├── agents/ (7)                     #   只读审查 agent
│   └── skills/ (12)                    #   slash commands
│
├── CLAUDE.example.md                   ← 项目上下文模板 (复制为 CLAUDE.md 后定制)
└── README.md                           ← 本文件

**项目上下文**放在 `context/` 目录 (非 `code/` 下)，保持代码仓库纯净。
使用 `/workon [name]` 切入项目，自动加载 `context/{name}.md`。
```

---

## 快速开始

### 1. 克隆 & 定制

```bash
git clone https://github.com/0xLian117/ML_PhD_research_workflow.git my_research
cd my_research

# 创建项目上下文 (必须)
cp CLAUDE.example.md CLAUDE.md
# 编辑 CLAUDE.md，填入你的研究方向、项目注册表、数据接口等

# 创建 code/ 下的项目 (各自独立 repo)
mkdir -p code/
git clone <your-project-a> code/project_a
git clone <your-project-b> code/project_b

# 为每个项目创建上下文文件 (供 /workon 使用)
mkdir -p context/
# 在 context/project_a.md 中写入项目的目的、架构、文件结构、进度等
# 在 context/project_b.md 中同上

# 创建对应的 results 目录
mkdir -p results/project_a results/project_b
```

### 2. 定制领域评估标准

编辑 `.claude/rules/domain-template.md`，替换为你的领域评估指标：

| 领域 | 示例指标 |
|------|---------|
| 量化金融 | IC, IR, Sharpe |
| NLP | BLEU, ROUGE, Perplexity |
| CV | mAP, FID, SSIM |
| RL | Reward, Success Rate |

### 3. 定制受保护文件

编辑 `.claude/hooks/protect-files.sh`，添加你不希望 Claude 修改的关键文件。

### 4. 远端服务器 (如需 GPU 训练)

```bash
# 在远端 GPU 服务器上镜像 code/ 结构
mkdir -p ~/my_research/code
cd ~/my_research/code
git clone <your-project-a> project_a
git clone <your-project-b> project_b
```

### 5. 启动 Claude Code

```bash
cd my_research
claude
```

Claude 自动加载 CLAUDE.md + 所有 rules，识别可用 skills。

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

**关键**: 每个 `code/` 下的项目是独立 git repo，各自 push/pull。
workflow repo 只跟踪研究资产（论文、笔记、报告、计划），不跟踪代码和模型权重。

---

## Skills (Slash Commands)

在 Claude Code 中输入以下命令触发对应工作流。

### 代码 & 实验

| 命令 | 用途 | 示例 |
|------|------|------|
| `/workon [name]` | 切入项目上下文 (加载文档 + git 状态) | `/workon delta_learn` |
| `/commit` | Git 提交 (自动排除大文件/密钥) | `/commit "feat: add attention layer"` |
| `/review-code [file]` | 代码审查 (8 维评分) | `/review-code code/my_project/models/model.py` |
| `/experiment [hypothesis]` | 创建实验: 假设→配置→远端命令 | `/experiment "增加层数从 4 到 8 提升表现"` |
| `/analyze-results [dir]` | 分析下载的实验结果 | `/analyze-results results/my_project/run_20250211` |
| `/compare [dirs]` | 对比多个实验结果 | `/compare results/baseline results/ablation` |
| `/data-check [target]` | 数据管道检查 (NaN/bias/分布) | `/data-check code/my_project/data/` |

### 学术写作

| 命令 | 用途 | 示例 |
|------|------|------|
| `/paper-draft [section]` | 起草论文章节 (LaTeX) | `/paper-draft method` |
| `/proofread [file]` | 校对 (语法/拼写/LaTeX/术语) | `/proofread papers/drafts/main/intro.tex` |
| `/lit-review [topic]` | 文献搜索 + 综述 | `/lit-review "transformer for time series"` |

### 报告 & 汇报

| 命令 | 用途 | 示例 |
|------|------|------|
| `/weekly-report` | 生成本周研究进展报告 | `/weekly-report` |
| `/slides [topic]` | 创建 Beamer 组会 slides | `/slides "本周实验进展"` |

### 研究

| 命令 | 用途 | 示例 |
|------|------|------|
| `/research-idea [desc]` | 将模糊想法形式化为研究计划 | `/research-idea "用对比学习改进表征"` |

---

## Rules (自动生效规则)

### Always-on (始终生效, 3 条)

| 规则 | 作用 |
|------|------|
| **plan-first** | 非琐碎任务先写计划再执行, 保存到 `quality_reports/plans/` |
| **orchestrator** | 自治执行循环: CODE 模式 (实现→验证→审查) / WRITE 模式 (起草→校对→审查), 质量 >= 80 方可提交 |
| **research-journal** | 研究日志: 计划后、发现时、session 结束前三个触发点记录 |

### Path-Scoped (按路径自动激活, 9 条)

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
| **domain-template** | (可定制路径) | 领域评估标准 — 默认量化金融, 可替换为 NLP/CV/RL 等 |

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
| **protect-files.sh** | Edit/Write 前 | 拦截对受保护文件的修改 (可定制保护列表) |
| **pre-compact.sh** | Context 压缩前 | 保存当前状态到 session log (防止上下文丢失) |
| **log-reminder.py** | Claude 停止响应时 | 20 次响应未更新日志则提醒 |

---

## 质量门控

| 场景 | 阈值 | 说明 |
|------|------|------|
| 代码提交 | >= 80/100 | code-reviewer 评分 |
| 论文章节 | >= 80/100 | paper-reviewer + proofreader |
| 探索性代码 | >= 60/100 | explorations/ 目录下宽松标准 |

---

## 模板

| 模板 | 路径 | 用途 |
|------|------|------|
| 周报 | `templates/weekly_report.md` | `/weekly-report` 的输出格式 |
| 实验记录 | `templates/experiment_log.md` | `/experiment` 的实验文档格式 |
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

---

## 定制指南

| 需要定制的文件 | 说明 |
|-------------|------|
| `CLAUDE.md` | **必须** — 你的研究主题、项目注册表、数据接口、评估标准 |
| `context/*.md` | **必须** — 每个项目的完整上下文 (目的/架构/进度), 供 `/workon` 使用 |
| `.claude/rules/domain-template.md` | 领域评估指标 (默认量化金融, 替换为你的领域) |
| `.claude/hooks/protect-files.sh` | 受保护文件列表 |
| `.gitignore` | `code/` 下的项目目录名 |
| `results/` | 为你的项目创建对应子目录 |
