---
paths: ["**/*.py", "**/model/**", "**/models/**", "**/*model*.py"]
---
# PyTorch & Python ML Standards

## 数值安全
- 使用 `np.nanmean`, `np.nanstd` 代替 `np.mean`, `np.std` (除非确认无 NaN)
- 使用 `np.log1p(x)` 代替 `np.log(1 + x)` (数值稳定)
- 除法前检查除零: `denominator = np.where(denom == 0, 1e-8, denom)`
- 每步检查 inf/nan: `assert not np.any(np.isnan(x)), f"NaN in {name}"`
- loss 出现 NaN 时 skip batch, 不要 backward

## 可复现性
- 所有随机过程必须设置 seed
- PyTorch: `torch.manual_seed(seed)`, `torch.cuda.manual_seed_all(seed)`
- NumPy: `np.random.seed(seed)` 或 `rng = np.random.default_rng(seed)`
- DataLoader: `worker_init_fn` 设置 per-worker seed
- 如需 deterministic: `torch.use_deterministic_algorithms(True)`

## 模型架构约定
- 模型由 config dict 完全定义, 不硬编码超参
- `__init__` 接收 config dict, 存为 `self.config`
- Forward 方法注明输入输出 shape: `# x: (B, T, D) → out: (B, H)`
- 中间 tensor shape 变换处加注释
- 多输出时返回 dict: `return {"pred": pred, "loss": loss}`

## 训练安全
- Gradient clipping: `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)`
- NaN loss 检测: `if torch.isnan(loss): skip batch, log warning`
- LR scheduler: 配置化, 支持 warmup

## Validation
- `@torch.no_grad()` 装饰 validation 函数
- `model.eval()` before validation, `model.train()` after
- Validation 不计算梯度, 不更新 BN running stats

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

## Logging
- 使用 `logging` 模块, 不用 `print`
- 训练循环包含数值诊断: shape, mean, std, nan count
- 例: `logger.info(f"loss={loss:.6f} grad_norm={grad_norm:.4f} nan_count={nan_count}")`

## 代码风格
- Public API 函数: 类型提示 + docstring
- 无硬编码绝对路径 (用 `Path(__file__).parent` 或 config)
- 大文件 (模型权重, 数据) 不进 git
- `if __name__ == "__main__"` 入口点
