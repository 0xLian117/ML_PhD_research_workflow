---
name: review-code
description: "对指定文件或目录运行代码审查，自动按文件类型分派审查 agent"
argument-hint: "[file path or directory]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
---
# /review-code

## 步骤

### 1. 确定审查范围
- 如指定文件: 审查该文件
- 如指定目录: 找出其中所有 .py 文件
- 如未指定: 审查最近修改的 Python 文件 (`git diff --name-only` 中的 .py 文件)

### 2. 按文件类型分派
| 路径模式 | 审查重点 |
|----------|---------|
| `**/data/**` | data-pipeline 规则 + code-reviewer (重点: look-ahead bias) |
| `**/model*/**` | model-conventions 规则 + code-reviewer (重点: PyTorch) |
| `**/evaluate*`, `**/backtest/**` | domain-template 规则 + code-reviewer |
| 其他 .py | code-reviewer 标准审查 |

### 3. 执行审查
对每个文件:
1. 读取文件内容
2. 按对应规则检查
3. 8 维评分 (结构/数值安全/PyTorch/可复现/内存/类型/文档/风格)
4. 列出 critical issues, warnings, suggestions

### 4. 生成报告
- 单文件: `quality_reports/reviews/[basename]_code_review.md`
- 多文件: 汇总报告 `quality_reports/reviews/batch_review_YYYY-MM-DD.md`

### 5. 摘要输出
向用户展示:
- 总分
- Critical issues 数量
- 是否通过质量门控 (>= 80)
- 建议的修复优先级

## 示例
```
/review-code delta_learn/data/dataset.py
/review-code delta_alpha/
/review-code   ← 审查最近变更
```
