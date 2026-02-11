---
paths: ["**/backtest/**", "**/evaluate*"]
---
# Domain Evaluation Standards — Quantitative Factor Research

此文件为领域可定制模板。当前配置为量化因子研究。
其他研究方向可替换为对应领域的评估标准 (如 NLP: BLEU/ROUGE, CV: mAP/FID 等)。

## 因子评估指标

| 指标 | 阈值 | 说明 |
|------|------|------|
| \|IC_mean\| | > 0.015 | 信息系数均值 |
| \|IR\| | > 0.3 | 信息比率 (IC_mean / IC_std) |
| IC 一致性 | > 52% | IC 同号比例 |
| Sharpe | > 0 | 风险调整收益 |

## Forward Return 定义
```
fwd_ret[t] = log(close[t+1+h] / close[t+1])   # delay=1
```
- signal 在 bar t 形成
- bar t+1 执行 (delay=1, 模拟真实延迟)
- bar t+1+h 平仓

## 回测要求
- 多品种测试: 不同期货品种交叉验证
- 时间段稳定性: 分年/季度检查 IC 稳定性
- 换手率合理: 过高换手 = 过拟合信号
- 交易成本: 考虑滑点和手续费

## 去重
- 因子间相关性 < 0.7 (Pearson)
- 新因子需与已有因子去重
- 相关因子保留 IC 更高的
