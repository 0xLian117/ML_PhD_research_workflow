---
name: project-report
description: "生成单个项目的研究进展报告 (导师汇报/自我回溯)"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
  - Task
---
# /project-report [name]

## 参数

- `name` — 项目名 (必须, 对应 `context/{name}.md`)

## 报告定位

**研究笔记/进展报告**, 不是 changelog。
- 叙事主线: Why → How → What → So what → Now what
- 兼顾两个读者: 导师 (汇报进展) + 未来的自己 (回溯思路)
- 中文正文 + 英文技术术语
- 维度标注: `(B, 3600, 52) → (B, 60, 60, 52)`
- 表格用于参数/结果对比

## 步骤

### Step 1: 确定项目和上下文

**读取项目上下文**:
- 读 `context/{name}.md` — 获取完整项目描述 (动机、架构、设计)

**确定报告期间**:
- 检查 `reports/projects/{name}/` 下最新的 `.md` 文件
- 如果存在上次报告:
  - period 起始 = 上次报告日期
  - 读取上次报告内容 → 用于延续发现、确定详略
  - 标记: `is_followup = true`
- 如果不存在:
  - 默认回溯 30 天
  - 标记: `is_followup = false` (首次报告，各 section 写完整)

### Step 2: 收集研究叙事素材

**计划和假设** — 从 `quality_reports/plans/` 收集:
- grep 项目名，读取 period 内的计划文件
- 提取: 假设 (Hypothesis)、预期 (Expected outcome)、实验矩阵

**Session 日志** — 从 `quality_reports/session_logs/` 收集:
- grep 项目名，读取 period 内的日志
- 提取: Findings, Decisions, Issues 各 section
- 这些是"发现"section 的主要来源

**Git 历史** — 用于进度日志:
```bash
cd code/{name} && git log --since="{start_date}" --format="%ai %s" 2>/dev/null || echo "无 git 历史"
```
- 按主题归类 (如: 数据层、模型、训练、评估)
- **不要**逐条列出 commit，而是归纳为进度事件

### Step 3: 收集实验结果

**已完成实验**:
- 扫描 `results/{name}/*/` 中 period 内新增的目录
- 读取 `config.yaml` → 提取关键配置参数差异
- 读取 `history.json` → 提取 IC, IR, loss 等指标
- 如果有 per-horizon 数据, 构建对比表

**计划中实验**:
- 从 plans 和 `code/{name}/config/*.yaml` 识别已配置但未运行的实验
- 标注"待运行"

**无结果时**: 明确标注"暂无实验结果，待远端运行"，不要跳过实验 section。

### Step 4: 确定各 section 详略

根据 `is_followup` 调整:

| Section | 首次报告 (`is_followup=false`) | 后续报告 (`is_followup=true`) |
|---------|-------------------------------|------------------------------|
| 1. 动机 | 完整阐述 | 一句话 + "详见 context/{name}.md" |
| 2. 架构 | 完整 ASCII 图 + 设计理由 | 仅描述本期变更 (无变更则引用 context) |
| 3. 实验设计 | 完整矩阵 | 仅新增实验 |
| 3. 结果 | 全部 | 仅本期新增 |
| 4. 发现 | 全部标 `[NEW]` | 新增标 `[NEW]` + 延续累积列表 |
| 5. 计划 | 完整 | 更新状态 |
| 6. 进度日志 | 全周期 | 仅本期 |

### Step 5: 生成报告

使用 `templates/project_report.md` 作为骨架，按以下原则填充:

**动机 section**:
- 首次: 从 context 文件提取核心问题和方向选择理由
- 后续: "本项目探索 [一句话]。详见 `context/{name}.md`。"

**架构 section**:
- 从 context 文件提取架构图和维度标注
- 标注 inductive bias 和设计理由
- 后续报告: 仅描述与上次的差异

**实验 section**:
- 实验设计: 阐述假设和对比逻辑 (不是只列参数)
- 结果: IC/IR 对比表，per-horizon 表
- 计划中: 带状态标注

**发现 section**:
- 分 What Worked / What Didn't Work
- 每条发现必须有: 证据 (数据) + 原因分析
- `[NEW]` 标记本期新发现
- 累积发现从上次报告延续，标注首次发现日期

**思考 section**:
- 当前对问题的理解 (基于实验证据)
- 下一步行动项 (具体可执行)
- 开放问题 (需讨论的)

**进度日志**:
- 合并 session logs 事件 + git 主题归类
- 按日期倒序
- 用 `[x]` / `[ ]` 标记完成状态

### Step 5.5: 图表生成 (按需)

如果报告中涉及实验对比、趋势展示等需要可视化的内容，使用 `/figure` skill 的工具链生成论文级图表:
- 调用 `figures/scripts/scientific_figure_pro.py` 中的 helper 函数
- 遵循 `figures/DESIGN_THEORY.md` 的设计规范
- 图表保存到 `figures/` 目录，在报告中引用路径

### Step 6: 保存 + 摘要

**保存**:
- 确保 `reports/projects/{name}/` 目录存在 (不存在则创建)
- 保存到 `reports/projects/{name}/YYYY-MM-DD.md`

**输出摘要**:
向用户展示 3-5 句摘要:
- 报告周期
- 本期关键进展
- 主要发现
- 下一步方向
- 如有开放问题需讨论，特别提示
