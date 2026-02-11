# Orchestrator — 自治执行循环

## 执行模式

根据任务涉及的文件类型自动选择模式:

### CODE 模式 (*.py, *.yaml config, scripts)
```
IMPLEMENT → VERIFY (本地检查) → REVIEW (code-reviewer) → FIX → SCORE
```

### WRITE 模式 (*.tex, *.md 论文/报告)
```
DRAFT → PROOFREAD (proofreader) → REVIEW (paper-reviewer) → REVISE → SCORE
```

### MIXED 模式
按文件类型自动分派到上述两条路径。

## VERIFY 检查项 (本地可执行范围)

| 类型 | 检查 |
|------|------|
| Python | `python -c "import module"` 通过, 语法无报错, `--test`/dry-run 模式 |
| Config | YAML 合法, 必需字段完整, 路径存在 |
| LaTeX | 编译通过 (latexmk), 无 undefined reference |
| Figures | 文件生成, 尺寸合理, 格式正确 |

**注意**: GPU 训练在远端服务器运行，本地无法直接验证训练结果。

## 远端执行工作流

Claude 辅助准备，用户手动在远端执行:

```
本地 Mac (Claude 可操作)          远端 GPU (用户手动)
─────────────────────────        ──────────────────
1. 开发 + 代码审查
2. 本地验证 (import, config)
3. git commit + push ──────────→ 4. git pull
                                  5. 运行训练/实验
                                  6. tar 结果
7. 下载结果 ←────────────────────
8. /analyze-results 分析
```

## 质量门控

| 分数 | 操作 |
|------|------|
| >= 80 | 可提交 (commit/push) |
| < 80 | 修复后重试 (最多 3 轮) |

## 评分维度

### Code Score (100 分)
- 正确性 (30): 逻辑正确, 无明显 bug
- 数值安全 (20): NaN/inf 处理, 除零保护
- 可复现 (15): seed, deterministic
- 代码质量 (15): 可读, 简洁, 结构清晰
- 文档 (10): docstring, 类型提示
- 风格 (10): 一致, PEP 8

### Writing Score (100 分)
- 内容 (30): 准确, 完整, 有深度
- 结构 (20): 逻辑清晰, 段落衔接
- 清晰度 (20): 术语准确, 表述简洁
- 格式 (15): LaTeX 正确, 引用完整
- 语言 (15): 语法正确, 学术语气
