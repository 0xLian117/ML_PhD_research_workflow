---
name: commit
description: "Git 提交工作流: 状态检查 → 排除敏感文件 → stage → 自动审查 → commit → 可选 push"
argument-hint: "[optional: commit message]"
allowed-tools:
  - Bash
  - Read
  - Glob
  - Task
---
# /commit

## 步骤

### 1. 检查状态
```bash
git status
git diff --stat
```

### 2. 排除敏感/大文件
自动排除 (不 stage):
- `*.pt`, `*.pth` (模型权重)
- `.env`, `*.key`, `*credentials*` (密钥)
- `__pycache__/`, `*.pyc`
- `outputs/` 下的大文件 (> 10MB)
- `node_modules/`, `.venv/`

如发现上述文件在变更中，警告用户并跳过。

### 3. Stage 文件
- 如用户指定了文件，stage 指定文件
- 否则 stage 所有合理的变更文件 (排除上述)
- 显示将要提交的文件列表

### 4. 自动代码审查 (Pre-commit Gate)

从 staged 文件中筛选 `*.py` 文件:
- **无 .py 文件** → 跳过审查，直接进入步骤 5
- **有 .py 文件** → 对每个 .py 文件启动 code-reviewer agent (Task tool, subagent_type=code-reviewer)
  - 多个文件可并行审查
  - 收集每个文件的分数和 issues

**审查结果处理:**
- **所有文件 >= 80 分** → 显示分数摘要，继续提交
- **任一文件 < 80 分** → 显示 critical issues 列表，**阻止提交**，提示用户修复后重试
  - 展示格式: `[文件名]: [分数]/100 — [critical issues]`
  - 提示: "修复上述问题后重新 /commit，或输入 'skip review' 强制跳过审查"

**用户输入 "skip review"** → 跳过审查门控，直接继续提交（记录在 commit message 中注明 `[review skipped]`）

### 5. 生成 Commit Message
如用户未提供 message:
- 分析变更内容
- 生成格式: `<type>: <description>`
- type: feat / fix / refactor / docs / experiment / config
- 询问用户确认

如用户提供了 message，直接使用。

### 6. 提交
```bash
git add <files>
git commit -m "<message>"
```

### 7. 可选: Push
提交后询问用户是否 push:
- 是 → `git push`
- 否 → 完成

## 注意
- 提交前显示完整 diff 摘要
- 如有未解决的 merge conflict, 报错并停止
- 不自动 push (必须用户确认)
- 审查仅针对 .py 文件，其他文件类型直接通过
