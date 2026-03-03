---
name: figure
description: "生成论文级科学图表 (bar, trend, heatmap, scatter, multi-panel)"
argument-hint: "[figure description or data source]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash
  - Agent
---
# /figure

基于 [figures4papers](https://github.com/ChenLiu-1996/figures4papers) 的绘图工具链。

## 参考文件

| 文件 | 用途 |
|------|------|
| `figures/scripts/scientific_figure_pro.py` | matplotlib 封装 (style, palette, helpers) |
| `figures/DESIGN_THEORY.md` | 设计理论 (调色板、排版、导出规范) |

## 步骤

### 1. 理解需求
- 解析用户描述的图表内容
- 确定图表类型: bar / trend / heatmap / scatter / multi-panel
- 定位数据源:
  - `results/` — 实验结果 (history.json, metrics)
  - `explorations/` — 探索性分析
  - 用户提供的数据

### 2. 读取设计规范
- 读 `figures/DESIGN_THEORY.md` 获取 house style 约定
- 确认调色板语义:
  - **Blue** (`#0F4D92`, `#3775BA`): 提出的方法 / 关键方法
  - **Green** (`#8BCF8B` 等): 正向/改进
  - **Red** (`#B64342` 等): 对比基线 / ablation
  - **Neutral** (`#CFCECE`): 背景/参考
  - **Highlight** (`#FFD700`): 需要强调的点

### 3. 生成绘图脚本
- 脚本保存到 `figures/scripts/plot_<name>.py`
- **必须** 使用 `scientific_figure_pro` 模块:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from scientific_figure_pro import (
    apply_publication_style, FigureStyle, create_subplots,
    finalize_figure, make_trend, make_grouped_bar, make_heatmap,
    make_scatter, PALETTE, DEFAULT_COLORS,
)

apply_publication_style(FigureStyle(font_size=16, axes_linewidth=2.5))
# ... 绘图逻辑 ...
finalize_figure(fig, "figures/<name>", formats=["pdf", "png"], dpi=300)
```

- 遵守设计规范:
  - 去除 top/right spines (已由 `apply_publication_style` 处理)
  - Frameless legend
  - 显式设置 y-limits (留适当 headroom)
  - Dense bar panels 用 `font_size=24, axes_linewidth=3, dpi=600`
  - Compact plots 用 `font_size=15-16, axes_linewidth=2`
  - Multi-metric 比较用超宽画布 (width 3-4x height)

### 4. 执行脚本
```bash
cd /Users/lian/Desktop/delta_research && python figures/scripts/plot_<name>.py
```

### 5. 验证输出
- 确认 PDF/PNG 生成在 `figures/` 目录
- 检查文件大小合理
- 告知用户输出路径

### 6. 输出格式
- 论文图: `figures/<name>.pdf` + `figures/<name>.png`
- 探索性图: 仅 PNG 即可
- 脚本留存: `figures/scripts/plot_<name>.py` (可复现)
