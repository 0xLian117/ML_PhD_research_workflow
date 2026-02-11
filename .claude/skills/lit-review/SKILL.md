---
name: lit-review
description: "文献搜索和综述"
argument-hint: "[research topic or question]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebSearch
  - Write
---
# /lit-review

## 步骤

### 1. 理解主题
- 解析用户提供的 topic/question
- 确定搜索范围: 广泛综述 vs 聚焦搜索
- 识别关键术语和同义词

### 2. 搜索文献
使用 WebSearch 多轮搜索:
- 轮次 1: 核心关键词 ("`[topic] survey [year]`")
- 轮次 2: 具体方法 ("`[method] [application] [year]`")
- 轮次 3: 补充搜索 (相关作者, venue)

每轮搜索后整理结果, 避免重复。

### 3. 检查现有笔记
- 读取 `literature/` 目录下已有的阅读笔记
- 确认哪些论文已经读过
- 标注需要新阅读的论文

### 4. 整理为结构化笔记
对新发现的重要论文, 创建笔记:
`literature/YYYY_Author_ShortTitle.md`

包含:
- 核心贡献
- 方法概述
- 关键结果
- 与自己研究的关系
- 建议的 BibTeX key

### 5. 分主题归类
将所有相关论文 (新 + 旧) 按主题分组:
```markdown
## [Subtopic 1]: [description]
- Paper A: ...
- Paper B: ...

## [Subtopic 2]: [description]
- Paper C: ...
```

### 6. 识别 Gap
- 哪些方向尚未被充分研究
- 哪些方法尚未被应用到我们的领域
- 我们工作的潜在 novelty 在哪里

### 7. 可选: 草拟 Related Work
如用户需要, 生成 Related Work 段落草稿:
- 按主题组织, 非按时间
- 包含 `\cite{key}` 占位
- 明确 positioning

### 8. 保存
- 搜索报告: `literature/search_YYYY-MM-DD_[topic].md`
- 个别论文笔记: `literature/YYYY_Author_ShortTitle.md`
- Related Work 草稿: `papers/drafts/related_work_[topic].tex` (如生成)

**注意**: WebSearch 结果需用户验证准确性。搜索引擎可能返回过时或不准确的信息。
