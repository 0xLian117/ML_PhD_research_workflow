---
paths: ["**/*.py"]
---
# Python / ML Code Standards

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

## Logging
- 使用 `logging` 模块, 不用 `print`
- 训练循环包含数值诊断: shape, mean, std, nan count
- 例: `logger.info(f"loss={loss:.6f} grad_norm={grad_norm:.4f} nan_count={nan_count}")`

## 类型与文档
- Public API 函数: 类型提示 + docstring
- 类: 类级 docstring 说明用途
- 内部函数: 类型提示可选, 但复杂逻辑需注释

## 其他
- 无硬编码绝对路径 (用 `Path(__file__).parent` 或 config)
- 大文件 (模型权重, 数据) 不进 git
- `if __name__ == "__main__"` 入口点
