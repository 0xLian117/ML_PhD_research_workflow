---
name: research-idea
description: "将模糊的研究想法形式化为具体的研究计划"
argument-hint: "[rough idea description]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebSearch
  - Write
---
# /research-idea

## 步骤

### 1. 解析 Rough Idea
从用户描述中提取:
- 核心直觉: 用户想探索什么
- 相关领域: 涉及哪些技术/方法
- 动机: 为什么这个方向有趣

### 2. 文献调研
WebSearch 查找:
- 是否已有人做过类似的事 (novelty check)
- 相关的最新方法和结果
- 潜在的 baseline

### 3. 形式化

```markdown
## Research Question
[清晰的研究问题, 以问号结尾]

## Hypothesis
[可证伪的假设]

## Proposed Method
[方法概述: 输入 → 处理 → 输出]

## Expected Results
[如果假设成立, 预期看到什么]

## Success Criteria
| Metric | Threshold |
|--------|-----------|
| ... | ... |
```

### 4. 评估

| 维度 | 评分 (1-5) | 说明 |
|------|-----------|------|
| **Feasibility** | X/5 | 技术可行性, 资源需求 |
| **Novelty** | X/5 | 与现有工作的差异 |
| **Impact** | X/5 | 如果成功, 影响有多大 |
| **Effort** | X/5 | 预计工作量 (1=少, 5=大) |

### 5. 行动计划
```markdown
## Next Steps
1. [ ] [第一步: 通常是详细文献调研或 pilot 实验]
2. [ ] [第二步]
3. [ ] [第三步]

## Resources Needed
- Data: ...
- Compute: ...
- Time estimate: ...

## Risks
- [风险 1 及缓解策略]
- [风险 2 及缓解策略]
```

### 6. 保存
保存到 `quality_reports/plans/research-idea_YYYY-MM-DD_[name].md`

### 7. 讨论
向用户展示:
- 形式化的研究问题
- Novelty 评估结果
- 建议的第一步
- 询问: 是否继续深入, 还是调整方向
