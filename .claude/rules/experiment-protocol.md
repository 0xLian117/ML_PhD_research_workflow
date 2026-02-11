---
paths: ["**/config/**", "**/scripts/**"]
---
# Experiment Protocol

## 配置管理
- 所有实验参数放 YAML config, 版本化到 git
- 运行时自动保存完整 config 到 output_dir (含 resolved 的默认值)
- Config 变更必须有 commit message 说明原因

## 可复现性
- 默认 seed = 42
- 消融实验 seeds: [42, 123, 456, 789, 1024]
- 记录完整环境: Python 版本, PyTorch 版本, CUDA 版本, GPU 型号

## 输出目录结构
```
outputs/{method}/{method}_{YYYYMMDD_HHMMSS}/
├── config.yaml          # 完整配置 (运行时保存)
├── history.json         # 逐 epoch/step 指标
├── best.pt              # 最佳模型权重
├── last.pt              # 最后一个 epoch 权重
├── train.log            # 训练日志
└── figures/             # 训练过程图表 (loss 曲线等)
```

## 受控变量
- **一次只改一个变量**: 相对基线只修改一个超参/模块
- 如需改多个, 拆分为多个实验, 逐步验证
- 消融实验: 每次去掉一个组件, 验证其贡献

## 实验文档
每个实验在 config 或 README 中记录:
- **假设**: 改了什么, 为什么
- **基线**: 对照的是哪个实验
- **预期**: 期望看到什么结果
- **结论**: 实际结果和解读 (实验后填写)
