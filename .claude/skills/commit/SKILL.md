---
name: commit
description: "Git 提交工作流: 状态检查 → 排除敏感文件 → stage → commit → 可选 push"
argument-hint: "[optional: commit message]"
allowed-tools:
  - Bash
  - Read
  - Glob
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

### 4. 生成 Commit Message
如用户未提供 message:
- 分析变更内容
- 生成格式: `<type>: <description>`
- type: feat / fix / refactor / docs / experiment / config
- 询问用户确认

如用户提供了 message，直接使用。

### 5. 提交
```bash
git add <files>
git commit -m "<message>"
```

### 6. 可选: Push
提交后询问用户是否 push:
- 是 → `git push`
- 否 → 完成

## 注意
- 提交前显示完整 diff 摘要
- 如有未解决的 merge conflict, 报错并停止
- 不自动 push (必须用户确认)
