---
name: paper-draft
description: "起草论文章节 (LaTeX, 含校对)"
argument-hint: "[section: abstract|intro|related|method|experiments|conclusion]"
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - WebSearch
---
# /paper-draft [section]

## 步骤

1. **收集素材**: 读 papers/ 现有大纲, results/ 实验数据, literature/ 笔记, 已有 sections
2. **起草 LaTeX**: 遵循 academic-writing rule (术语一致, `\newcommand`, `\citep`/`\citet`)
3. **校对**: 检查语法, 拼写, LaTeX 语法, 术语一致性, 学术语气
4. **保存**: `papers/drafts/[paper_name]/[section].tex`, 提示复制到 Overleaf

## Section 框架

- **Abstract**: 问题 → 方法 → 结果 → 意义 (4 句)
- **Intro**: 背景 → 问题 → 现有不足 → 贡献 (bullet list) → 结构
- **Related**: 按主题分组, 明确差异
- **Method**: Overview → 各组件 (自顶向下) → 数学推导 → 伪代码
- **Experiments**: Setup → Main Results → Ablation → Analysis
- **Conclusion**: 总结 → 局限 → 未来工作
