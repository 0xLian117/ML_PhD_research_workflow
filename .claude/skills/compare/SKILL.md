---
name: compare
description: "对比两个或多个实验结果目录"
argument-hint: "[run_dir_1 run_dir_2 ...]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---
# /compare

## 步骤

### 1. 读取实验目录
对每个目录:
- 读 `config.yaml` — 获取完整配置
- 读 `history.json` — 获取训练历史
- 检查 `best.pt` 存在性

### 2. Config 差异分析
- 列出所有 config 参数的差异
- 高亮关键差异 (学习率, 模型大小, 数据范围等)
- 共同参数跳过

### 3. 指标对比
生成对比表:

```markdown
| Metric | Run 1 | Run 2 | Delta |
|--------|-------|-------|-------|
| Best Val Loss | 0.xxx | 0.xxx | -x.x% |
| IC Mean | 0.xxx | 0.xxx | +x.x% |
| IR | x.xx | x.xx | +x.x% |
| Best Epoch | N | N | |
| Total Epochs | N | N | |
```

### 4. 趋势分析
- Loss 收敛速度对比
- IC 稳定性对比 (std)
- 过拟合信号 (train-val gap)

### 5. 结论
- 哪个实验更好, 在哪些维度
- 差异是否显著
- 建议下一步 (接受/拒绝假设, 继续探索)

### 6. 保存报告
保存到 `quality_reports/reviews/compare_YYYY-MM-DD_[name].md`

## 示例
```
/compare outputs/delta_learn/run_20250210 outputs/delta_learn/run_20250211
/compare delta_alpha/outputs/baseline delta_alpha/outputs/ablation_no_attention
```
