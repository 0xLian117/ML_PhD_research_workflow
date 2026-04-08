---
name: slides
description: "生成 Slidev (HTML) slides — 支持 web 全部素材"
argument-hint: "[topic]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Bash
---
# /slides [topic]

## 目录规范

```
slides/
├── YYYY-MM-DD_topic/        ← 每次演示一个目录
│   ├── slides.md            ← Slidev 源文件
│   └── public/              ← 引用的图片/资源
└── _archive/                ← 旧文件
```

保存到 `slides/YYYY-MM-DD_[topic]/slides.md`。

## 结构

1. Title slide (标题 + 日期 + 作者)
2. Outline / Agenda
3. Background / Motivation (1-2 slides)
4. Method / Architecture (含架构图)
5. Experiments + Results (表格, 引用图)
6. Analysis / Discussion
7. Summary + Next Steps

## 格式

```markdown
---
theme: default
title: [topic]
---

# Slide Title

content

---

# Next Slide
```

素材来源: papers/, results/, reports/, figures/。
可内嵌: ECharts 图表, HTML 组件, LaTeX 数学, 代码块。
引用图片复制到 `public/` 子目录, 用相对路径引用。

## 预览 & 导出

```bash
cd slides/YYYY-MM-DD_topic && npx slidev          # 预览
cd slides/YYYY-MM-DD_topic && npx slidev export    # PDF
```
