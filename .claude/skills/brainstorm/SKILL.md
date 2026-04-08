---
name: brainstorm
description: "研究探索: 想法调研/形式化/文献搜索"
argument-hint: "[idea or topic]"
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - Write
  - Agent
---
# /brainstorm [idea]

三种模式, 根据输入自动判断:
- **探索** (默认): "用 foundation model 做跨市场预测" → 多源调研 + 方案评估
- **形式化**: "formalize: 用 xxx 方法做 yyy" → 研究问题 + 假设 + 评估
- **文献**: "literature: cross-market transfer learning" → 文献专项搜索 + 笔记

## 探索模式

### 1. 理解想法
提取: 核心想法, 动机, 预期目标, 约束条件。信息不足则追问。

### 2. 并行调研
用 Agent 工具并行启动 literature-assistant agents:
- **论文**: arXiv, 顶会 (NeurIPS/ICML/ICLR/KDD) 最新相关工作
- **代码**: GitHub 开源实现, 成熟度评估
- **博客**: 实践经验, 已知坑, 方法对比

### 3. 综合分析
- 支持证据 / 已有类似工作 / 潜在风险 / 值得参考的技巧

### 4. 方案建议
2-3 个方案 (保守→激进), 各含: 思路, 参考, 优劣, 工作量。推荐一个。

### 5. 保存
`explorations/brainstorm_YYYY-MM-DD_[slug].md`

## 形式化模式

1. 文献调研 (novelty check)
2. 形式化: Research Question → Hypothesis → Method → Expected Results → Success Criteria
3. 评估: Feasibility / Novelty / Impact / Effort (1-5)
4. 行动计划 + 资源需求 + 风险
5. 保存到 `reports/plans/research-idea_YYYY-MM-DD_[name].md`

## 文献模式

1. 多轮 WebSearch (关键词→引用追踪→作者追踪→venue 追踪)
2. 按主题分组, 每篇: 标题/方法/结果/与我们的关系
3. 识别 research gaps
4. 保存笔记到 `literature/YYYY_Author_ShortTitle.md`
5. 可选: 生成 Related Work 段落草稿
