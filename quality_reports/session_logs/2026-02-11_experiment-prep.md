# Session Log — 2026-02-11 — Experiment Preparation (Phase 1)

## Goal
实现实验计划 v4 的 Phase 1: 代码准备。包括 bf16 训练支持、bias_norm 删除、scaling 配置生成。

## Progress
### 14:00 — 开始实施
读取了所有关键文件: train.py, transforms.py, dataset.py, data/__init__.py, 4个config yaml, context/delta_learn.md

### 14:10 — bf16 autocast (Task #1)
- Trainer.__init__ 增加 precision 参数，计算 use_amp + amp_dtype
- train_epoch(): forward+loss 包裹 torch.autocast, backward 在 autocast 外
- validate(): forward 包裹 torch.autocast
- main(): 从 training.precision 读配置 (默认 bf16)

### 14:20 — 删除 bias_norm (Task #2)
- transforms.py: 删除 include_bias 参数, _bias(), _normalized_bias(), 相关分支
- dataset.py: 删除 include_bias 参数
- data/__init__.py: 删除 include_bias 传递
- train.py: 删除 include_bias 计算
- 4个 config yaml: 删除 include_bias: false 行, 注释 65维→52维
- n_transforms 固定为 3 + int(include_skew_norm) = 4

### 14:30 — 更新 context (Task #3)
- 特征变换描述: 5种→4种, 65维→52维
- 项目结构: 新增 config/scaling/ 和 generate_scaling_configs.py
- 新增: Scaling 实验表格 (MS1-4, DS1-3, FS1)
- 训练精度: bf16

### 14:40 — 生成 Scaling 配置 (Task #4)
- 创建 scripts/generate_scaling_configs.py
- 生成 11 个配置: MS1/3/4 × (pretrain+finetune) + DS1/2 × (pretrain+finetune) + FS1
- 参数量验证: MS1=87K, Baseline=322K, MS3=2.3M, MS4=17.4M, FS1=2.3M

### 14:50 — 本地验证 (Task #5)
- 16 个 YAML 配置全部合法
- transforms: 13维→52维, shape=(2000,52), 0% NaN
- 4种模型大小正确创建和前向传播
- train.py 语法检查通过

### 15:00 — Code Review 修复
- **CRITICAL FIX**: validate() 中 bf16 preds 需要 .float() 再转 numpy
- **HIGH FIX**: train_epoch() 添加 NaN loss guard
- 删除 generate_scaling_configs.py 中未使用的 DSN 常量

## Decisions
- bf16 autocast 包裹 forward+loss，backward 在 autocast 外 (bf16 不需要 GradScaler)
- bias_norm 彻底删除 (不是禁用)，n_transforms 固定为 3+int(include_skew_norm)
- precision 默认 bf16，通过 config training.precision 可覆盖

## Findings
- E2E 模型实际参数量 304,902 (不是 307K)，差异来自 d_patch=d_model=128 时 input_proj 为 Identity
- FS1 (factor d=256 L=4) 实际 2.3M (不是 3M)

## Issues
- [ ] MS4 (d=512) 的 batch_size=32768 可能导致 OOM，需要远端测试时观察
- [ ] 未添加 fp16 GradScaler (当前只支持 bf16, 无实际需求)
- [x] bf16→numpy 转换 bug (已修复)
- [x] NaN loss guard (已修复)

## Summary
Phase 1 完成。修改了 6 个文件，新增 2 个文件，生成 11 个 scaling 配置。代码已通过本地验证和 code review。

## Output Files
- `scripts/train.py` — 添加 bf16 autocast + NaN loss guard
- `data/transforms.py` — 删除 bias_norm
- `data/dataset.py` — 删除 include_bias
- `data/__init__.py` — 删除 include_bias
- `config/*.yaml` (×4) — 删除 include_bias, 更新注释
- `config/scaling/*.yaml` (×11) — 新增 scaling 实验配置
- `scripts/generate_scaling_configs.py` — 新增
- `context/delta_learn.md` — 更新

## Next Session
- Phase 2: 用户在远端执行 git pull + Batch 1-4 训练
- Phase 3: 下载结果 → 实现 analyze_comparison.py → 论文图表
