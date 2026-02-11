---
paths: ["**/model/**", "**/models/**", "**/*model*.py"]
---
# PyTorch Model Conventions

## 配置驱动
- 模型由 config dict 完全定义, 不硬编码超参
- Config 示例: `{"d_model": 128, "n_heads": 4, "n_layers": 3, "dropout": 0.1}`
- `__init__` 接收 config dict, 存为 `self.config`

## Forward 方法
- 注明输入输出 shape: `# x: (B, T, D) → out: (B, H)`
- 中间 tensor shape 变换处加注释
- 返回 dict (多输出时): `return {"pred": pred, "loss": loss, "aux": aux}`

## 训练安全
- Gradient clipping: `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)`
- NaN loss 检测: `if torch.isnan(loss): skip batch, log warning`
- LR scheduler: 配置化, 支持 warmup

## Validation
- `@torch.no_grad()` 装饰 validation 函数
- `model.eval()` before validation, `model.train()` after
- Validation 不计算梯度, 不更新 BN running stats (除非特殊需要)

## Checkpoint
每次保存包含:
- `best.pt` — 最佳验证指标的权重
- `last.pt` — 最新 epoch 权重
- `config.yaml` — 完整模型 + 训练配置
- `history.json` — 逐 epoch loss/metric 记录

格式:
```python
torch.save({
    "epoch": epoch,
    "model_state_dict": model.state_dict(),
    "optimizer_state_dict": optimizer.state_dict(),
    "config": config,
    "best_metric": best_metric,
}, path)
```
