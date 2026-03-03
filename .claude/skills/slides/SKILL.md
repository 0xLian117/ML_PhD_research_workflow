---
name: slides
description: "创建组会/会议 Marp slides (Markdown)"
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
  - `results/` — 实验结果
  - `literature/` — 相关工作
  - `quality_reports/` — 分析报告
  - `figures/` — 已有图表 (仅 `.png`)

### 2. 确定结构
典型组会 slides 结构:
1. Title slide (lead class)
2. Outline (1 slide)
3. Motivation / Problem (1-2 slides)
4. Method (2-4 slides)
5. Experiments (2-4 slides)
6. Results & Analysis (2-3 slides)
7. Conclusion & Next Steps (1 slide)
8. Questions (lead class)

向用户确认结构。

### 3. 生成 Marp Markdown
- 模板: `slides/templates/group_meeting.md`
- 主题: `slides/themes/delta-lab.css`
- Frontmatter:
  ```yaml
  marp: true
  math: mathjax
  theme: delta-lab
  paginate: true
  ```
- 每个 slide 用 `---` 分隔
- 标题: `# 标题文字` (蓝色文字, 无背景色块)
- 每个 slide 要点 3-5 条
- 公式: `$$...$$` (MathJax)
- 图片: `![w:600](../figures/xxx.png)` (w: 控制宽度, 一般 500-700)
- 分栏: `<div class="columns"><div>左</div><div>右</div></div>`
- 缩小字体: class `small` (18px) 或 `xsmall` (16px)
- Title/结束页: `<!-- _class: lead -->` + `<!-- _paginate: false -->`

### 4. 验证
- 检查图片路径存在 (`figures/*.png`)
- 检查 slide 数量合理 (组会: 10-16 页)
- 检查无 Markdown 语法错误

### 5. 输出
- 保存到 `slides/[name].md`
- 告知用户:
  1. VS Code 打开 → Marp 插件预览
  2. `Cmd+Shift+P` → "Marp: Export Slide Deck" → PDF
  3. VS Code settings.json 需配置主题路径:
     ```json
     "markdown.marp.themes": ["./slides/themes/delta-lab.css"]
     ```
