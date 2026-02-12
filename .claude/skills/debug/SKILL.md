---
name: debug
description: "结构化 ML 实验调试: 症状分类 → 信息收集 → 诊断检查 → 报告生成"
argument-hint: "[症状描述 或 日志路径]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Bash
  - Task
---
# /debug

对 ML 实验失败进行结构化排查，生成诊断报告。

## 步骤

### 1. 症状分类

从用户描述或日志中自动识别失败类型:

| 类型 | 关键词 |
|------|--------|
| `loss_nan` | NaN, Inf, nan loss, inf loss |
| `grad_explode` | gradient explosion, grad norm spike, 梯度爆炸 |
| `grad_vanish` | gradient vanishing, grad ≈ 0, 梯度消失 |
| `ic_zero` | IC ≈ 0, no predictive power, 无预测能力 |
| `no_converge` | loss not decreasing, 不收敛, plateau |
| `oom` | OOM, CUDA out of memory, 显存不足 |
| `other` | 无法匹配上述 → 询问用户补充 |

如提供了日志路径，先读取日志内容辅助分类。

### 2. 信息收集

根据症状类型，自动定位并读取相关文件:

| 文件类型 | 路径模式 | 何时读取 |
|----------|----------|----------|
| 训练日志 | `train.log`, `*.log` | 所有症状 |
| 配置文件 | `config.yaml`, `*.yaml` | 所有症状 |
| 数据管道 | `data/`, `dataset*` | `loss_nan`, `ic_zero`, `no_converge` |
| 模型代码 | `model*/`, `network*` | `grad_explode`, `grad_vanish`, `loss_nan` |
| Loss 函数 | 含 `loss`, `criterion` 的文件 | `loss_nan`, `no_converge` |
| 训练循环 | 含 `train`, `trainer` 的文件 | 所有症状 |

使用 Glob + Grep 定位文件，用 Read 读取关键段落。如用户指定了项目 (如 delta_learn)，在 `code/{project}/` 下搜索。

### 3. 诊断检查表

按症状类型执行对应检查:

#### loss_nan
- [ ] 除零保护: 是否有 `/ (x + eps)` 或 `torch.clamp`
- [ ] log 输入范围: `torch.log` 的参数是否保证 > 0
- [ ] 学习率: lr 是否过大 (> 1e-3 对 Transformer 通常偏大)
- [ ] 数据 NaN 比例: 输入数据中 NaN/Inf 占比
- [ ] gradient clipping: 是否启用, clip value 是否合理
- [ ] 权重初始化: 是否使用了合理的 init (Xavier/Kaiming)

#### grad_explode
- [ ] grad_norm 趋势: 日志中 grad_norm 是否持续增长
- [ ] learning rate schedule: warmup 是否合理
- [ ] weight initialization: 方差是否正确
- [ ] 残差连接: 深层网络是否有 skip connection
- [ ] layer norm / batch norm: 归一化层是否正确放置

#### grad_vanish
- [ ] 激活函数: 是否使用了 sigmoid/tanh (深层易消失)
- [ ] 残差连接: 是否缺失
- [ ] 初始化: 方差是否过小
- [ ] 网络深度: 层数是否过深

#### ic_zero
- [ ] forward return 计算: 公式是否正确 `log(close[t+1+h] / close[t+1])`
- [ ] look-ahead bias: 是否有未来数据泄露
- [ ] 数据泄露: train/val split 是否有重叠
- [ ] 特征是否全为常数: std ≈ 0 的特征占比
- [ ] 标签分布: 是否极度不平衡
- [ ] 模型输出: 是否坍缩到常数 (所有预测相同)

#### no_converge
- [ ] 学习率: 是否过大或过小
- [ ] batch size: 是否过大 (梯度噪声不足) 或过小 (不稳定)
- [ ] 数据 shuffle: 是否开启了 shuffle
- [ ] label 分布: 方差是否过小
- [ ] 模型容量: 是否欠拟合 (模型太小)
- [ ] 优化器: AdamW 参数是否合理 (betas, weight_decay)

#### oom
- [ ] batch size: 当前值和推荐范围
- [ ] sequence length: 是否过长 (attention O(n^2))
- [ ] 不必要的 tensor 保留: 是否有 `.detach()` 缺失
- [ ] gradient checkpointing: 是否启用
- [ ] 混合精度: 是否使用 fp16/bf16
- [ ] 模型参数量: 估算显存占用

### 4. 生成诊断报告

保存到 `quality_reports/reviews/debug_YYYY-MM-DD_[symptom].md`:

```markdown
# Debug Report — YYYY-MM-DD — [症状类型]

## 症状描述
[用户描述 + 日志证据]

## 根因分析 (按可能性排序)

### 1. [最可能原因] — 置信度: 高/中/低
**证据**: [在代码/日志中发现的证据]
**验证方法**: [如何确认这是根因]
**修复方案**: [具体代码修改建议]

### 2. [次可能原因] — 置信度: 高/中/低
...

## 检查清单结果
| 检查项 | 状态 | 备注 |
|--------|------|------|
| ... | PASS/FAIL/SKIP | ... |

## 建议修复顺序
1. [优先修复项]
2. [次优先]
3. ...

## 预防建议
- [避免此类问题再发生的建议]
```

### 5. 可选: 本地验证

对怀疑的代码段做局部检查:
- `python -c "import ..."` 确认无语法错误
- 数据采样检查 (NaN 比例、分布)
- config 字段一致性检查
- 用 code-reviewer agent 审查可疑文件 (Task tool, subagent_type=code-reviewer)

## 注意
- 不要猜测，基于代码和日志中的证据诊断
- 优先检查最常见的原因 (数据问题 > 超参数 > 代码 bug)
- 如果信息不足，明确告知用户需要哪些额外信息
- 报告应可操作: 每个可能原因都给出具体的验证步骤和修复方案
