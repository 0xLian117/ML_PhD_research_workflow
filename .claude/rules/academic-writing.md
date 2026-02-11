---
paths: ["**/*.tex", "**/papers/**"]
---
# Academic Writing Standards

## Overleaf 工作流
- 本地 .tex 文件用于草稿和审查
- 完成后复制到 Overleaf 进行最终排版和协作
- 本地编译用于快速预览和检查

## 术语一致性
- 首次出现的术语给出定义或引用
- 之后统一使用同一术语, 不混用同义词
- 缩写: 首次 "Full Name (ABBR)", 之后用 ABBR

## 数学排版
- 用 `\newcommand` 定义常用符号, 不硬编码
- 例: `\newcommand{\loss}{\mathcal{L}}`, `\newcommand{\expect}{\mathbb{E}}`
- 行内公式用 `$...$`, 重要公式用 `\begin{equation}...\end{equation}`
- 多行推导用 `align` 环境, 对齐等号

## 引用
- `\citep{key}` — 括号引用: (Author, Year)
- `\citet{key}` — 行内引用: Author (Year)
- 在一篇论文中保持一致的引用风格
- BibTeX 条目维护在 `papers/references.bib`

## 段落结构
- 每段一个核心观点
- 段首句 (topic sentence) 概括本段要点
- 段落之间有逻辑衔接 (however, furthermore, specifically)

## 浮动体 (Figures/Tables)
- 每个 Figure/Table 必须在正文中引用 (`\ref{fig:xxx}`)
- 不允许 orphan floats (存在但未引用的图表)
- Caption 完整描述内容, 读者只看 caption 也能理解

## 论文结构
标准结构: Abstract → Introduction → Related Work → Method → Experiments → Conclusion
- Abstract: 问题 → 方法 → 结果 → 意义 (4 句话框架)
- Introduction: 背景 → 问题 → 贡献 → 结构概览
- Related Work: 按主题分组, 非按时间排列
- Method: 自顶向下, 先 overview 再细节
- Experiments: Setup → Main Results → Ablation → Analysis
- Conclusion: 总结 → 局限 → 未来工作
