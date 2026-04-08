---
name: workon
description: "切入项目上下文: 检查新鲜度 + 刷新文件树 + git 状态 briefing"
argument-hint: "<project_name> (e.g. delta_learn, delta_alpha, delta_data_sdk, futuretrade)"
allowed-tools:
  - Bash
  - Read
  - Edit
  - Glob
  - Grep
---
# /workon [name]

切入指定项目工作上下文。项目文档已通过 `code/{name}/CLAUDE.md` @import 自动加载，本 skill 负责新鲜度检查和 git 状态。

## 参数

`$ARGUMENTS` = 项目名

## 步骤

### 1. 确认项目存在

检查 `context/$ARGUMENTS.md` 是否存在。不存在则报错。

### 2. 检测 Context 新鲜度

```bash
# context 文件最后修改时间
stat -f %m context/$ARGUMENTS.md

# 最近 git commit 时间
git -C code/$ARGUMENTS log -1 --format=%ct
```

- context >= commit: 最新
- context < commit: 触发步骤 3 刷新

### 3. 自动刷新文件树 (仅当过时时)

如果 context 文件中包含 `<!-- AUTO-GENERATED:tree -->` 标记:

1. 扫描实际代码目录:
```bash
find code/$ARGUMENTS -type f \( -name "*.py" -o -name "*.yaml" -o -name "*.yml" -o -name "*.sh" \) \
  ! -path "*/__pycache__/*" ! -path "*/.git/*" ! -path "*/outputs/*" | sort
```

2. 与 context 中记录的文件树对比
3. 有差异则用 Edit 更新 `<!-- AUTO-GENERATED:tree -->` 区域
4. `touch context/$ARGUMENTS.md`

### 4. Git 状态

```bash
git -C code/$ARGUMENTS log --oneline -10
git -C code/$ARGUMENTS status --short
git -C code/$ARGUMENTS diff --stat
```

### 5. 更新 Leaf CLAUDE.md

更新 `code/$ARGUMENTS/CLAUDE.md` 的 "Current Focus" section (如用户指定了新任务)。

### 6. Briefing

```
## 已切入: {name}

**Context 状态**: 最新 / 文件树已刷新 / 部分内容可能过时

**最近提交**:
[git log]

**工作区**: [git status 或 "干净"]

---
现在可以对 {name} 下达指令。代码路径: `code/{name}/`
```
