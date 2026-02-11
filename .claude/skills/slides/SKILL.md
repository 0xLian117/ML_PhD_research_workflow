---
name: slides
description: "创建组会/会议 Beamer slides"
argument-hint: "[topic or paper section to present]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash
---
# /slides

## 步骤

### 1. 确定内容
- 解析用户要求的 topic
- 读取相关内容:
  - `papers/` — 论文内容
  - `outputs/` — 实验结果
  - `literature/` — 相关工作
  - `quality_reports/` — 分析报告

### 2. 确定结构
典型组会 slides 结构:
1. Title slide
2. Motivation / Problem (1-2 slides)
3. Background / Related Work (1-2 slides)
4. Method (2-4 slides)
5. Experiments (2-4 slides)
6. Results & Analysis (2-3 slides)
7. Conclusion & Next Steps (1 slide)
8. References (1 slide)

向用户确认结构。

### 3. 生成 Beamer LaTeX
- 使用 `slides/templates/group_meeting.tex` 模板
- 每个 slide 要点控制在 3-5 条
- 公式简洁, 用直觉解释
- 图表引用 (如已有)

### 4. 编译
```bash
latexmk -xelatex -output-directory=slides/ slides/[name].tex
```

### 5. 验证
- 确认 PDF 生成
- 检查页数合理 (组会: 10-20 页, 会议: 15-25 页)
- 检查无编译错误

### 6. 输出
- 保存到 `slides/[name].tex` + `slides/[name].pdf`
- 告知用户 PDF 位置
