---
name: workon
description: "切入项目上下文: 加载项目文档 + git 状态 → 结构化 briefing"
argument-hint: "<project_name> (e.g. delta_learn, delta_alpha, delta_data_sdk)"
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---
# /workon [name]

切入指定项目的工作上下文。

## 参数

`$ARGUMENTS` = 项目名 (如 `delta_learn`, `delta_alpha`, `delta_data_sdk`)

## 步骤

### 1. 加载项目上下文

读取 `context/$ARGUMENTS.md`，获取项目全貌。

如果文件不存在，报错: "未找到项目上下文 context/$ARGUMENTS.md，可用项目见 context/ 目录"。

### 2. 检查 Git 状态

如果 `code/$ARGUMENTS/` 目录存在且是 git repo:

```bash
git -C code/$ARGUMENTS log --oneline -10
git -C code/$ARGUMENTS status --short
git -C code/$ARGUMENTS diff --stat
```

### 3. 检查相关实验结果

如果 `results/$ARGUMENTS/` 存在:
```bash
ls -lt results/$ARGUMENTS/ | head -5
```

### 4. 输出结构化 Briefing

格式:

```
## 🔧 已切入: {name}

**目的**: [从 context 文件提取的一句话概述]

**当前状态**:
- [从 context 文件提取的进度 checklist]

**最近提交** (code/{name}):
[git log 输出]

**工作区状态**:
[git status 输出, 或 "工作区干净"]

**未提交变更**:
[git diff --stat 输出, 或 "无"]

**最近实验** (results/{name}):
[最近几个实验目录, 或 "无"]

---
现在可以对 **{name}** 下达指令。代码路径: `code/{name}/`
```

## 注意

- 只读操作，不修改任何文件
- 如果用户后续对该项目下达指令，记住已加载的上下文
- 可以随时 `/workon` 另一个项目切换上下文
