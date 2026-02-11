# Plan-First Protocol

## Rule
非琐碎任务必须先计划再执行。琐碎任务 = 单文件小改动、格式化、简单 bug fix。

## Workflow
1. 收到非琐碎任务 → 进入 plan mode
2. 写计划到 `quality_reports/plans/YYYY-MM-DD_<slug>.md`
3. 用户批准 → 执行
4. 未批准 → 修改计划 → 重新提交

## Plan Templates

### 实验类计划必须包含
- **假设 (Hypothesis)**: 我们相信 X 会导致 Y
- **变量 (What changes)**: 相对基线改了什么
- **预期 (Expected outcome)**: 如果假设成立，指标应该如何变化
- **成功标准 (Metrics + thresholds)**: 具体数值门槛

### 论文类计划必须包含
- **目标读者 (Venue/audience)**: 投稿 venue 和审稿人画像
- **核心贡献 (Contributions list)**: 3-5 个 bullet points
- **大纲 (Section outline)**: 各 section 要点

### 代码类计划必须包含
- **目标**: 要实现什么
- **影响范围**: 哪些文件/模块会改动
- **验证方法**: 如何确认改动正确

## Session Recovery
新 session 或 context compact 后的恢复顺序:
1. 读 CLAUDE.md (项目上下文)
2. 读最近的 plan (`quality_reports/plans/` 最新文件)
3. `git log -10` + `git diff` (最近变更)
4. 复述当前任务和进度，向用户确认
