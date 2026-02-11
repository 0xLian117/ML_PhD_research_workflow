---
name: weekly-report
description: "生成本周研究进展报告"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---
# /weekly-report

## 步骤

### 1. 收集本周信息

**Session 日志**:
- 读取 `quality_reports/session_logs/` 中本周 (最近 7 天) 的日志
- 提取: 目标、进展、发现、决策

**Git 历史**:
```bash
git log --since="1 week ago" --oneline --all
git diff --stat HEAD~$(git rev-list --count --since="1 week ago" HEAD)..HEAD
```

**实验结果**:
- 检查 `outputs/` 目录中最近 7 天的新文件
- 检查 `quality_reports/reviews/` 中的分析报告

**论文进展**:
- 检查 `papers/` 目录中的变更
- 检查 `literature/` 中的新笔记

### 2. 组织内容

按模板结构:
```markdown
# Weekly Report — YYYY Week NN (MM/DD - MM/DD)

## Summary
[1-2 句总结本周最重要的进展]

## Progress
### Code & Models
- [完成的代码工作]

### Experiments
- [跑的实验, 结果摘要]

### Writing
- [论文/报告进展]

### Literature
- [读的论文, 新发现]

## Key Findings
- [本周最重要的发现/洞察]

## Issues & Blockers
- [遇到的问题, 待解决]

## Next Week Plan
- [ ] [计划 1]
- [ ] [计划 2]
- [ ] [计划 3]

## Metrics
| Metric | This Week | Last Week | Trend |
|--------|-----------|-----------|-------|
| Commits | N | N | ↑↓→ |
| Experiments | N | N | |
| Papers read | N | N | |
```

### 3. 保存
- 保存到 `reports/weekly/YYYY-WNN.md`
- NN = ISO week number

### 4. 输出
向用户展示周报摘要。
