---
name: figure
description: "生成图表: 数据图 / 架构图 / 流程图 / 论文图"
argument-hint: "[description]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash
---
# /figure [description]

根据描述自动路由到最佳工具。

## 目录结构

```
figures/                        # 整个目录 gitignore
├── DESIGN_THEORY.md            # 设计规范 (唯一进 git 的文件)
├── src/                        # 源文件 (脚本/HTML/TeX)
│   ├── plot_*.py
│   ├── *.html
│   └── *.tex
└── out/                        # 生成输出
    ├── data/                   # 数据图 (matplotlib/pyecharts)
    ├── diagrams/               # 架构/流程图 (HTML→截图)
    └── paper/                  # 论文图 (TikZ→PDF)
```

## 路由

| 类型 | 工具 | src → out |
|------|------|-----------|
| 数据图 (IC曲线, loss, bar) | matplotlib / pyecharts | `src/*.py` → `out/data/*.{png,pdf,html}` |
| 架构图 / 流程图 | HTML+JS (Canvas/SVG) | `src/*.html` → `out/diagrams/*.png` |
| 论文内嵌图 | TikZ | `src/*.tex` → `out/paper/*.pdf` |

## 数据图 (matplotlib / pyecharts)

- 源: `figures/src/plot_[name].py`
- 输出: `figures/out/data/[name].png` (300dpi) + `.pdf`
- pyecharts: `figures/out/data/[name].html` (交互式)
- 遵循 `figures/DESIGN_THEORY.md` 配色规范

## 架构图 / 流程图 (HTML+JS)

- 源: `figures/src/[name].html`
- Canvas API / SVG / CSS, 可引用 web 图标库
- 预览: `open figures/src/[name].html`
- 导出: 截图到 `figures/out/diagrams/[name].png`

## 论文图 (TikZ)

- 源: `figures/src/[name].tex`
- 编译: `pdflatex -output-directory=figures/out/paper figures/src/[name].tex`
- 输出: `figures/out/paper/[name].pdf`

## 设计规范

参考 `figures/DESIGN_THEORY.md`:
- 配色: 蓝 (proposed), 绿/红 (ablation), 灰 (baseline)
- 字号: 标题 14pt, 标签 11pt, 刻度 9pt
- 导出: PDF + PNG@300dpi
