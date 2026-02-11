---
paths: ["**/literature/**"]
---
# Literature Management Protocol

## 阅读笔记格式
文件名: `literature/YYYY_Author_ShortTitle.md`

```markdown
# [Paper Title]
**Authors**: ...
**Venue**: ... (Year)
**Link**: [URL or DOI]
**BibTeX Key**: author2024short

## Core Contribution
[1-3 sentences: 这篇论文的核心贡献是什么]

## Method
[方法概述, 关键技术细节]

## Key Results
- [主要实验结果]
- [关键数字/表格]

## Relation to Our Work
[与自己研究的关系: 启发、对比、可借鉴之处]

## Notes
[其他笔记、想法、疑问]
```

## Related Work 组织
- 按主题分组, 不按时间排列
- 每组有简要综述段落
- 明确自己工作与各组的区别/联系

## BibTeX 管理
- 所有引用条目维护在 `papers/references.bib`
- Key 格式: `author2024short` (第一作者姓 + 年份 + 关键词)
- 从 Google Scholar / DBLP 获取标准 BibTeX
- 定期检查: 无重复 key, 无缺失字段

## 文献搜索策略
1. 关键词搜索 (Google Scholar, Semantic Scholar)
2. 引用追踪: 重要论文的 references + cited by
3. 作者追踪: 关键作者的最新工作
4. Venue 追踪: 目标会议最近 2-3 年的相关论文
