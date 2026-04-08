---
paths: ["**/data/**", "**/data/*.py", "**/backtest/**", "**/evaluate*"]
---
# Data Pipeline & Evaluation Standards

## Look-Ahead Bias 红线 (零容忍)
- Rolling 计算只用历史数据: `rolling(window).mean()` 不含当前 bar
- Target (forward return) 必须 delay >= 1: `fwd_ret[t] = log(close[t+1+h] / close[t+1])`
- Normalization 参数只从 train set 计算, 应用到 val/test
- 特征工程中不能使用未来信息
- **违反 look-ahead bias 是最严重的错误, 优先级高于一切**

## 数据源
- 优先使用 `delta_data` SDK API (`DeltaDB.query()`, `DeltaDB.sql()`)
- 如需 raw SQL, 必须注释说明为什么 SDK API 不够用
- 不直接使用 sqlalchemy/asyncpg 连接

## NaN 处理
- 每步操作后检查 NaN 比例
- NaN 填充策略必须文档化 (forward fill / zero / drop / interpolate)
- NaN > 1% 时记录 warning
- NaN > 10% 时记录 error 并考虑丢弃该样本/品种

## Shape 验证
- 数据加载后验证 shape: `assert df.shape[0] > 0, "Empty dataframe"`
- 特征矩阵维度检查: `assert X.shape[1] == expected_features`
- Batch 维度检查: `assert batch.shape[0] == batch_size` (最后一个 batch 除外)

## Train / Val / Test 分割
- 时序数据: 按时间分割, 不用随机分割
- 三者不重叠: 确保日期范围无交集
- Test set 开发期间禁用: 只在最终评估时使用
- 记录分割边界日期到 config

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

## 因子去重
- 因子间相关性 < 0.7 (Pearson)
- 新因子需与已有因子去重
- 相关因子保留 IC 更高的
