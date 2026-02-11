# Research Journal Protocol

## 触发点

### 1. Post-Plan (计划批准后立即记录)
记录:
- 目标: 这个 session 要完成什么
- 方法: 计划采用的方法
- 关键上下文: 相关的前置工作、依赖

### 2. Incremental (实时追加)
发生以下事件时立即追加到当日日志:
- **发现**: 意外的实验结果、代码行为
- **决策**: 选择了方法 A 而非 B，以及原因
- **问题**: 遇到的障碍、待解决的疑问
- **用户纠正**: 用户更正了我的理解或方向

不要攒批，发生即记。

### 3. End-of-Session (session 结束前)
记录:
- **总结**: 本次 session 完成了什么
- **产出列表**: 新增/修改的文件
- **待办**: 未完成的任务
- **下次起点**: 下次 session 应该从哪里开始

## 日志位置和格式

路径: `quality_reports/session_logs/YYYY-MM-DD_<description>.md`

```markdown
# Session Log — YYYY-MM-DD — <description>

## Goal
[本次 session 的目标]

## Progress
### HH:MM — [事件]
[详情]

### HH:MM — [事件]
[详情]

## Decisions
- [决策及原因]

## Findings
- [发现]

## Issues
- [ ] [待解决问题]

## Summary
[总结]

## Output Files
- `path/to/file` — 描述

## Next Session
[下次应该做什么，从哪里开始]
```
