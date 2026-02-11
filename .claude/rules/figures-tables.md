---
paths: ["**/figures/**", "**/plots/**", "**/*plot*.py", "**/*figure*.py"]
---
# Figures & Tables Standards

## 输出格式
- 论文图: PDF 或 SVG (矢量格式, 缩放不失真)
- 预览/报告图: PNG, 300 DPI
- 同时保存两种格式: `fig.savefig("name.pdf"); fig.savefig("name.png", dpi=300)`

## 尺寸
- Single-column: 3.5 inches wide (约 8.9 cm)
- Double-column: 7.0 inches wide (约 17.8 cm)
- 高度按内容调整, 保持合理宽高比

## 字体
- 最小字号 >= 8pt (论文印刷后仍可读)
- 轴标签、图例、标题字号一致
- 使用 serif 字体 (与论文正文匹配) 或 matplotlib 默认

## 配色
- 色盲友好: 避免仅用红/绿区分
- 推荐调色板: `tab10`, `Set2`, 或自定义色盲安全色
- 同一论文中配色方案一致

## 可复现
- 每张图有对应的 Python 生成脚本
- 不手动编辑图片 (所有修改通过代码)
- 脚本和输出文件一起保存

## Caption
- 完整描述图表内容
- 包含关键数值 (如 "IC = 0.025")
- 说明读者应关注的要点

## matplotlib 模板
```python
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "legend.fontsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})
```
