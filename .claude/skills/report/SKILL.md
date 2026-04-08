---
name: report
description: "研究报告: 传项目名=单项目深度报告, 不传=跨项目周报"
argument-hint: "[project_name]  — 有参数=项目报告, 无参数=周报"
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---
# /report [name?]

有参数 → 单项目进展报告。无参数 → 跨项目周报。

## 项目报告 `/report {name}`

叙事主线: Why → How → What → So what → Now what

1. **确定范围**: 读 context/{name}.md, 检查 reports/projects/{name}/ 最新报告确定起始日期
2. **收集素材**:
   - reports/plans/ — grep 项目名, 提取假设和实验设计
   - git log in code/{name} — 按主题归类 (不逐条列)
   - results/{name}/*/ — config.yaml + history.json 指标
3. **生成报告** (首次完整, 后续仅变更):
   - 动机 → 架构 → 实验 (设计+结果+分析) → 发现 (What Worked / Didn't) → 思考与计划 → 进度日志
4. **保存**: `reports/projects/{name}/YYYY-MM-DD.md`

## 周报 `/report`

跨项目执行摘要, 50-80 行。优先从项目报告聚合。

1. **活跃项目**: 读 CLAUDE.md 注册表, 判定活跃 (本周有 git commit / session log / 新结果)
2. **收集**: 有项目报告→提取摘要; 无→从 session logs + git + results 补充
3. **综合**: Headline (全周最重要发现) + 项目摘要 (每个 3-4 行) + 阻塞 + 下周计划
4. **保存**: `reports/weekly/YYYY-WNN.md`
