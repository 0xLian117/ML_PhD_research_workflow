# [Your Research Title]

## 研究主题

[简要描述你的研究方向和目标]

## 项目结构

```
your_research/
├── CLAUDE.md              ← 本文件
├── code/                  ← 代码项目 (各自独立 git repo)
│   ├── project_a/         # 项目 A
│   └── project_b/         # 项目 B
├── results/               ← 远端实验结果
├── papers/                ← 论文草稿
└── ...                    ← (其他目录见 README.md)
```

## 数据接口

[描述你的数据来源和访问方式]

```python
# 示例
from your_data_lib import DataLoader
loader = DataLoader(config)
df = loader.load("2024-01-01", "2024-12-31")
```

## 各项目职责

### project_a — [描述]
- 路径: `code/project_a/`
- 功能: [项目 A 做什么]
- 详细文档: `code/project_a/CLAUDE.md`

### project_b — [描述]
- 路径: `code/project_b/`
- 功能: [项目 B 做什么]
- 详细文档: `code/project_b/CLAUDE.md`

## 共享约定

### 评估标准

| 指标 | 阈值 |
|------|------|
| [metric_1] | > [threshold] |
| [metric_2] | > [threshold] |

[根据你的领域定制，同时更新 .claude/rules/domain-template.md]

---

## Workflow — ML PhD Research Assistant

详细参考: `.claude/WORKFLOW_QUICK_REF.md`

### Skills 速查
| 命令 | 用途 |
|------|------|
| `/commit` | Git 提交工作流 |
| `/review-code [file]` | 代码审查 |
| `/experiment [hypo]` | 新实验 (含远端运行命令) |
| `/analyze-results [dir]` | 分析下载的实验结果 |
| `/compare [dirs]` | 对比实验 |
| `/data-check [target]` | 数据管道检查 |
| `/paper-draft [section]` | 论文章节草稿 |
| `/proofread [file]` | 校对 |
| `/lit-review [topic]` | 文献综述 |
| `/weekly-report` | 周报 |
| `/slides [topic]` | 组会 Beamer slides |
| `/research-idea [desc]` | 形式化研究想法 |

### 质量门控
- **代码/论文**: >= 80 分可提交, < 80 修复后重试
- **explorations/**: >= 60 分即可, 无需事先计划

### 执行模型 (Remote GPU)
本地 Mac 负责开发 + 写作 + 审查。训练/实验在远端 GPU 服务器运行。
1. 本地: 开发 → 验证 → 在 `code/project/` 中 `git push`
2. 远端 (用户手动): `git pull` → 运行 → tar 结果
3. 本地: 下载结果到 `results/project/` → `/analyze-results` 分析

### 日志位置
- 计划: `quality_reports/plans/`
- 会话日志: `quality_reports/session_logs/`
- 审查报告: `quality_reports/reviews/`
- 周报: `reports/weekly/`

### 论文写作流程
1. 本地起草: `/paper-draft [section]` → `papers/drafts/`
2. 校对: `/proofread [file]`
3. 复制到 Overleaf 进行最终排版
4. BibTeX 维护在 `papers/references.bib`
