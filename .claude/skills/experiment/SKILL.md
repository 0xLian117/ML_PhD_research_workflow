---
name: experiment
description: "设置新实验：从假设到配置到执行计划，生成远端运行命令"
argument-hint: "[hypothesis or experiment description]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash
---
# /experiment

## 步骤

### 1. 解析假设
从用户输入提取:
- **假设**: 我们相信 X 会导致 Y
- **变量**: 相对基线改了什么
- **预期**: 如果假设成立, 指标应如何变化
- **成功标准**: 具体数值门槛

如信息不完整, 向用户提问补充。

### 2. 读基线配置
- 找到最近的基线实验 config
- 显示基线的关键参数和结果 (如有)

### 3. 创建实验配置
- 复制基线 config
- 仅修改实验变量
- 保存到 `{project}/config/experiment_{YYYYMMDD}_{name}.yaml`
- 在 config 中添加注释: 假设、变量、预期

### 4. 文档化
创建实验记录:
```markdown
# Experiment: [name]
**Date**: YYYY-MM-DD
**Hypothesis**: ...
**Variable**: ...
**Baseline**: [baseline config path]
**Expected**: ...
**Success Criteria**: ...
**Config**: [new config path]
**Status**: Prepared
```
保存到 `quality_reports/plans/experiment_YYYY-MM-DD_[name].md`

### 5. 本地验证
```bash
# Config 合法性
python -c "import yaml; yaml.safe_load(open('config.yaml'))"

# Import 检查
python -c "import [project_module]"
```

### 6. 生成远端运行命令
输出用户需要在远端执行的完整命令序列:
```bash
# 远端 GPU 服务器上执行:
cd /path/to/project
git pull origin main

# 运行实验
python train.py --config config/experiment_YYYYMMDD_name.yaml

# 或 multi-GPU
torchrun --nproc_per_node=N train.py --config config/experiment_YYYYMMDD_name.yaml

# 打包结果
tar -czf results_experiment_name.tar.gz outputs/method/method_YYYYMMDD_HHMMSS/
```

### 7. 可选: 自动提交
询问用户是否 commit + push 新 config:
- 是 → git add + commit + push
- 否 → 完成, 用户手动处理
