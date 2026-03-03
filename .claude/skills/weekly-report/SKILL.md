---
name: weekly-report
description: "生成本周研究进展报告"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
  - Task
---
# /weekly-report

## 报告定位

**跨项目执行摘要**, 不是 changelog。回答 "本周研究整体学到了什么、下周做什么"。

信息架构层级:
```
Session logs / Git / Results    (原子数据, 每日)
         ↓
Project reports                 (单项目研究叙事, 深度)
         ↓
Weekly report                   (跨项目综合, 精简)
```

原则:
- 优先从 project report 聚合, 不重复收集细节
- 中文正文 + 英文技术术语
- 总长度 50-80 行
- 不列 commit、不列参数表 (那些在 project report 里)
- 每个项目摘要必须有 `> 详见` 引用行

## 步骤

### Step 1: 确定周期和活跃项目

**计算周期**:
- ISO 周号 + 日期范围 (周一 - 周日)

**读上周周报**:
- 扫描 `reports/weekly/` 找最新 `.md` 文件
- 提取 "下周计划" section → 用于对比实际进展

**确定活跃项目**:
- 读 CLAUDE.md 中项目注册表获取全部项目
- 判定活跃条件 (满足任一):
  - `code/{name}/` 有本周 git commits: `cd code/{name} && git log --since="{monday}" --oneline 2>/dev/null`
  - `quality_reports/session_logs/` 本周日志中提及项目名
  - `results/{name}/` 有本周新增目录
  - `reports/projects/{name}/` 有本周新报告

### Step 2: 收集项目报告 (主要数据源)

对每个活跃项目:
- 检查 `reports/projects/{name}/` 是否有本周期内的报告
- **有报告** → 读取, 提取:
  - 阶段 (从 "思考与计划" 推断)
  - 关键发现 (从 "发现" section)
  - 决策 (从 session logs 或报告中的决策点)
  - 阻塞 (从 "开放问题" 或 Issues)
  - 下一步 (从 "下一步行动项")
  - 标记: `has_project_report = true`
- **无报告** → 标记: `has_project_report = false` (Step 3 补充)

### Step 3: 补充收集 (无项目报告时)

对 `has_project_report = false` 的项目:

**Session logs**:
- grep 项目名 in `quality_reports/session_logs/` 本周文件
- 提取 Findings / Decisions / Issues sections

**Git 历史**:
```bash
cd code/{name} && git log --since="{monday}" --until="{sunday}" --format="%ai %s" 2>/dev/null
```
- 按主题归类 (不逐条列出)

**Results**:
- 扫描 `results/{name}/` 本周新增目录

对**所有**项目 (含有报告的):
- 检查 `quality_reports/plans/` 本周新建的计划 → 补充 "决策" 和 "下周计划"

### Step 4: 跨项目综合

- **Headline**: 识别全周最重要的一个事件/发现, 写一句话
- **项目摘要**: 压缩为 4 行格式 (阶段/焦点/发现/状态) + `> 详见` 引用行
- **发现与决策**: 合并去重, 只保留全局影响的 (单项目细节留在 project report)
- **阻塞**: 合并, 标注影响范围
- **下周计划**: 合并 + 优先级排序 (P0/P1/P2)
- **研究健康度**: 综合信号评估 5 个维度:
  - 实验进度: On track / Delayed / Blocked
  - 代码就绪: Ready / In progress
  - 数据管线: Healthy / Issues
  - 论文写作: Not started / Drafting / Reviewing
  - 开放问题: 计数 + 最紧急的

### Step 5: 生成报告

- 使用 `templates/weekly_report.md` 作为骨架
- 填充 Step 4 综合结果
- 对比上周 "下周计划" vs 实际完成 → 体现在项目摘要和健康度中
- 删除无活动项目的 section (不留空模板)
- 总长度控制 50-80 行

### Step 5.5: 图表生成 (按需)

如果周报需要可视化 (跨项目进度对比、指标趋势等)，使用 `/figure` skill 的工具链:
- 调用 `figures/scripts/scientific_figure_pro.py` 中的 helper 函数
- 遵循 `figures/DESIGN_THEORY.md` 的设计规范
- 图表保存到 `figures/` 目录，在报告中引用路径

### Step 6: 保存 + 摘要

**保存**:
- 确保 `reports/weekly/` 目录存在
- 保存到 `reports/weekly/YYYY-WNN.md` (NN = ISO 周号)

**输出摘要**:
向用户展示 3-4 句:
- 周期和活跃项目数
- Headline (最重要进展)
- 关键阻塞 (如有)
- 下周最高优先级行动
