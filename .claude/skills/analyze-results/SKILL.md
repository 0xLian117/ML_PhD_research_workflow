---
name: analyze-results
description: "分析从远端下载的实验结果"
argument-hint: "[results directory path]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---
# /analyze-results

## 步骤

### 1. 扫描结果目录
检查必要文件:
- `config.yaml` — 实验配置
- `history.json` — 训练历史
- `best.pt` / `last.pt` — 模型权重
- `train.log` — 训练日志
- `figures/` — 训练过程图表

报告缺失的文件。

### 2. 提取关键指标
从 `history.json`:
- Loss 曲线: train loss, val loss (逐 epoch)
- 最佳 epoch 和对应指标
- IC / IR / Sharpe (如有)
- 收敛情况: 最后 N epoch loss 变化

### 3. 异常检测
检查:
- NaN 值: loss 或 metric 中的 NaN 数量
- Loss 爆炸: loss 突然增大的 epoch
- 过拟合: train-val gap 持续扩大
- 早停: 是否应该更早/更晚停止
- 梯度: grad_norm 异常值 (如有记录)

### 4. 与基线对比
- 寻找相关的基线实验 (同 method, 不同日期)
- 如找到, 自动对比关键指标
- 如未找到, 跳过此步

### 5. 生成分析报告
保存到 `quality_reports/reviews/[experiment_name]_analysis.md`:

```markdown
# Analysis: [experiment name]
**Date**: YYYY-MM-DD
**Config**: [config path]
**Status**: Success / Partial / Failed

## Key Metrics
| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Best Val Loss | 0.xxx | — | — |
| IC Mean | 0.xxx | > 0.015 | ✓/✗ |
| IR | x.xx | > 0.3 | ✓/✗ |
| Sharpe | x.xx | > 0 | ✓/✗ |

## Training Curve
- Converged at epoch: N
- Final train loss: X, val loss: Y
- Train-val gap: Z (overfitting: Yes/No)

## Anomalies
- [any issues found]

## vs Baseline
| Metric | This | Baseline | Delta |
|--------|------|----------|-------|
| ... | ... | ... | ... |

## Conclusion
[接受/拒绝假设? 结果说明了什么?]

## Next Steps
1. [建议的下一步行动]
```

### 6. 用户建议
- 假设成立 → 建议巩固 (更多 seeds, 更长时间段)
- 假设不成立 → 分析原因, 建议调整方向
- 部分成立 → 建议针对性消融
