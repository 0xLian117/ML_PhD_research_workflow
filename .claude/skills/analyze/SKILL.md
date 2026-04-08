---
name: analyze
description: "分析实验结果: 单 run 深度分析或多 run 对比"
argument-hint: "[dir1] [dir2...]  — 1 个=单分析, 多个=对比"
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---
# /analyze [dirs...]

1 个目录 → 单实验分析。多个目录 → 对比模式。

## 单 run 分析

1. 扫描目录: config.yaml, history.json, best.pt, train.log
2. 提取指标: best epoch, loss 趋势, IC/IR/Sharpe (如有)
3. 异常检测: NaN, loss 爆炸, 过拟合 (train-val gap), grad_norm 异常
4. 自动寻找同 method 基线对比 (同目录不同日期)
5. 结论 + 下一步建议

## 多 run 对比

1. 读取所有目录的 config.yaml + history.json
2. Config diff: 列出参数差异, 高亮关键变量 (lr, model size, data range)
3. 指标对比表 (delta 列)
4. 趋势对比: 收敛速度, IC 稳定性, 过拟合信号
5. 结论: 哪个更好, 差异是否显著

## 输出

保存到 `reports/projects/{project}/analyze_YYYY-MM-DD_[name].md`
