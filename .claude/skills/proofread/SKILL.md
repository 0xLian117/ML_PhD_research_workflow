---
name: proofread
description: "校对文档 (LaTeX, Markdown, 或任何文本文件)"
argument-hint: "[file path]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
---
# /proofread

## 步骤

### 1. 读取文件
- 读取指定文件
- 确定文件类型 (LaTeX / Markdown / plain text)

### 2. 运行校对
按 proofreader agent 标准检查:

**Grammar (语法)**
- 主谓一致, 冠词, 时态, 句子完整性

**Spelling (拼写)**
- 英文拼写, 技术术语, 人名/方法名

**LaTeX (格式)** — 仅 .tex 文件
- 未闭合环境/括号, 未定义 ref/cite

**Terminology (术语)**
- 术语一致性, 缩写定义

**Tone (语气)**
- 避免口语化, 避免绝对化

### 3. 生成建议报告
保存到 `quality_reports/reviews/[basename]_proofread.md`

格式:
```markdown
# Proofread: [filename]
**Issues**: N total (G grammar, S spelling, L LaTeX, T terminology, A tone)

| # | Line | Category | Original | Suggested | Reason |
|---|------|----------|----------|-----------|--------|
```

### 4. 展示给用户
- 显示 critical issues (影响理解的)
- 显示 issue 总数和分类
- 询问: "是否应用这些修改?"

### 5. 应用修改 (用户批准后)
- 对用户批准的修改, 逐一应用 Edit
- 对用户拒绝的修改, 跳过
- 更新报告标注哪些已应用
