---
name: paper-draft
description: "起草论文章节 (本地 .tex, 完成后提示复制到 Overleaf)"
argument-hint: "[section name: abstract|intro|related|method|experiments|conclusion]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - WebSearch
---
# /paper-draft

## 步骤

### 1. 理解上下文
- 读现有论文大纲/notes (`papers/` 目录)
- 读相关实验结果 (`outputs/`, `quality_reports/`)
- 读已有 sections (保持一致性)
- 确定目标 venue 和格式要求

### 2. 收集素材
根据 section 类型:
- **Abstract**: 全文概览, 关键数字
- **Intro**: 背景资料, 贡献列表
- **Related**: 搜索相关文献 (WebSearch), 读 `literature/` 笔记
- **Method**: 技术细节, 数学推导, 算法流程
- **Experiments**: 实验结果, 对比表, 图表引用
- **Conclusion**: 全文总结, 局限性

### 3. 起草 LaTeX
遵循 academic-writing 规则:
- 术语一致
- `\newcommand` 定义符号
- `\citep` / `\citet` 引用
- 段首句概括
- Figure/Table 在正文引用

### 4. 校对
运行 proofreader 检查:
- 语法
- 拼写
- LaTeX 语法
- 术语一致性
- 学术语气

### 5. 保存
- 保存到 `papers/drafts/[paper_name]/[section].tex`
- 如 paper_name 未指定, 询问用户
- 提示用户完成后复制到 Overleaf

### 6. 输出
向用户展示:
- 草稿预览 (前几段)
- 校对发现的问题数
- 需要用户确认的: 引用, 数字, claims

## Section 写作指南

### Abstract (4 句框架)
1. 问题是什么 (背景 + 挑战)
2. 我们做了什么 (方法概述)
3. 结果如何 (关键数字)
4. 意义是什么 (启示)

### Introduction
1. 大背景 (1-2 段)
2. 具体问题 + 为什么重要 (1 段)
3. 现有方法的不足 (1 段)
4. 我们的方法和贡献 (1-2 段, 含 bullet list)
5. 论文结构 (可选, 1 段)

### Method
1. Overview (全景图)
2. 各组件详细描述 (自顶向下)
3. 关键数学推导
4. 算法伪代码 (如需)
