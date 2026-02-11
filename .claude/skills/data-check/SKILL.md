---
name: data-check
description: "检查数据管道: 完整性、NaN、look-ahead bias、分布"
argument-hint: "[instruments or data path]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---
# /data-check

## 步骤

### 1. 确定检查范围
- 如指定品种: 检查该品种的数据
- 如指定路径: 检查该数据文件/目录
- 如未指定: 检查当前项目的数据加载代码

### 2. 数据完整性检查
```python
# 检查数据加载
df = load_data(...)
print(f"Shape: {df.shape}")
print(f"Date range: {df.index.min()} to {df.index.max()}")
print(f"Columns: {list(df.columns)}")
```

### 3. NaN 分析
```python
# 每列 NaN 比例
nan_pct = df.isna().mean()
print(nan_pct[nan_pct > 0].sort_values(ascending=False))
# 标注 > 1% 的列为 warning, > 10% 为 error
```

### 4. Look-Ahead Bias 检查
审查代码中的:
- Rolling 窗口: 是否包含当前 bar
- Target 计算: delay 是否 >= 1
- Normalization: 参数是否从 train set 计算
- 特征: 是否使用了未来信息

### 5. 分布检查
```python
# 基本统计
print(df.describe())
# 异常值
print(f"Inf count: {np.isinf(df.select_dtypes('number')).sum().sum()}")
```

### 6. Train/Val/Test 分割验证
- 检查时间边界
- 确认无重叠
- 报告各集大小

### 7. 生成报告
保存到 `quality_reports/reviews/data_check_YYYY-MM-DD.md`
