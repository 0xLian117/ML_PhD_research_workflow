---
name: workon
description: "切入项目上下文: 加载项目文档 + git 状态 + 自动刷新文件树 → 结构化 briefing"
argument-hint: "<project_name> (e.g. delta_learn, delta_alpha, delta_data_sdk)"
allowed-tools:
  - Bash
  - Read
  - Edit
  - Glob
  - Grep
---
# /workon [name]

切入指定项目的工作上下文，自动检测并刷新过时内容。

## 参数

`$ARGUMENTS` = 项目名 (如 `delta_learn`, `delta_alpha`, `delta_data_sdk`)

## 步骤

### 1. 加载项目上下文

读取 `context/$ARGUMENTS.md`，获取项目全貌。

如果文件不存在，报错: "未找到项目上下文 `context/$ARGUMENTS.md`，可用项目见 `context/` 目录"。

### 2. 检测 Context 新鲜度

如果 `code/$ARGUMENTS/` 是 git repo:

```bash
# context 文件最后修改时间
stat -f %m context/$ARGUMENTS.md

# 最近 git commit 时间
git -C code/$ARGUMENTS log -1 --format=%ct
```

比较两个时间戳:
- **context >= commit**: 上下文是最新的 ✓
- **context < commit**: 有新 commit → 触发步骤 3 刷新

### 3. 自动刷新文件树 (仅当过时时)

如果 context 文件中包含 `<!-- AUTO-GENERATED:tree -->` 标记:

1. 扫描实际代码目录，生成当前文件树:
```bash
# 列出 Python/YAML/Shell 文件 (排除 __pycache__, .git, outputs 等)
find code/$ARGUMENTS -type f \( -name "*.py" -o -name "*.yaml" -o -name "*.yml" -o -name "*.sh" -o -name "*.json" \) \
  ! -path "*/__pycache__/*" ! -path "*/.git/*" ! -path "*/outputs/*" ! -path "*/.eggs/*" \
  | sort
```

2. 与 context 中记录的文件树对比，识别:
   - **新增文件**: 在代码中有，context 中没有
   - **删除文件**: 在 context 中有，代码中已不存在

3. 如果有差异，用 Edit 工具更新 `context/$ARGUMENTS.md` 中 `<!-- AUTO-GENERATED:tree -->` 和 `<!-- /AUTO-GENERATED:tree -->` 之间的内容:
   - 保留原有注释 (# 描述)，对已存在文件不改注释
   - 新增文件标注 `# (新增)` 待用户补充描述
   - 删除已不存在的文件条目

4. 刷新后 `touch context/$ARGUMENTS.md` 更新时间戳

### 4. 手动内容过时警告

如果有新 commit 且涉及非文件树的变更 (如架构、特征、模型逻辑改动)，在 briefing 末尾提示:

```
⚠️ context 自 [N 天/N 个 commit] 前可能未更新非结构性内容。
  涉及的变更: [git log 摘要]
  如需更新概述/架构/特征等描述，请告知。
```

### 5. 检查 Git 状态

```bash
git -C code/$ARGUMENTS log --oneline -10
git -C code/$ARGUMENTS status --short
git -C code/$ARGUMENTS diff --stat
```

### 6. 检查相关实验结果

如果 `results/$ARGUMENTS/` 存在:
```bash
ls -lt results/$ARGUMENTS/ | head -5
```

### 7. 输出结构化 Briefing

```
## 🔧 已切入: {name}

**目的**: [从 context 文件提取的一句话概述]

**Context 状态**: ✅ 最新 / ⚠️ 文件树已自动刷新 / ⚠️ 部分内容可能过时

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

## Context 文件约定

### 自动刷新区域

用 HTML 注释标记的区域会被 `/workon` 自动刷新:

```markdown
<!-- AUTO-GENERATED:tree — /workon 自动刷新，勿手动编辑 -->
## 项目结构
...
<!-- /AUTO-GENERATED:tree -->
```

### 手动维护区域

其他所有 section 由用户/Claude 手动维护:
- 概述、核心概念、架构设计、特征说明
- 数据依赖、运行方式、配置说明
- 评估标准、当前状态 checklist

当对项目做了重大变更 (新增模块、改架构、改特征) 后，应手动更新 context。
可以直接告诉 Claude: "更新 context/delta_learn.md 的 XX section"。

## 注意

- 文件树刷新是自动的，其他内容更新需要指示
- 可以随时 `/workon` 另一个项目切换上下文
