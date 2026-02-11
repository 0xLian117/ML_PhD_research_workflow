# ML PhD Research Workflow — Quick Reference

**Model:** Contractor (你指导方向, Claude 自治执行)

## The Loop
```
你的指令
    → [PLAN] (非琐碎) → 计划 → 你批准
    → [EXECUTE] 实现 + 验证
    → [REPORT] 总结产出
    → Repeat
```

## 我问你
- 研究方向: "方法 A vs B, 哪个先做?"
- 实验范围: "跑 3 seeds 还是 5? 时间 vs 置信度"
- 写作风格: "这段更 formal 还是更 intuitive?"
- 优先级: "先完善实验还是先写 draft?"

## 我直接执行
- Bug 修复、代码格式化
- 验证 (编译、运行、检查指标)
- 日志记录、git 操作
- 生成图表 (按已定标准)

## Project Layout
```
code/          → 代码项目 (各自独立 git repo, workflow 不跟踪)
results/       → 远端下载的实验结果 (本地分析)
papers/        → 论文草稿 (→ Overleaf)
quality_reports/ → 计划/日志/审查报告
```

## Execution Model (Remote GPU)
```
本地 Mac (Claude 可操作)               远端 GPU (用户手动)
──────────────────────────            ──────────────────
1. 在 code/project/ 开发
2. 本地验证 (import, config)
3. cd code/project && git push ────→  4. cd code/project && git pull
                                       5. 运行训练/实验
                                       6. tar 结果
7. 下载到 results/project/ ←─────────
8. /analyze-results results/...
```

## Skills
| 命令 | 用途 |
|------|------|
| `/commit` | 提交代码 |
| `/review-code [file]` | 代码审查 |
| `/experiment [hypo]` | 新实验 (含远端运行命令) |
| `/analyze-results [dir]` | 分析下载的实验结果 |
| `/compare [dirs]` | 对比实验 |
| `/data-check [target]` | 数据管道检查 |
| `/paper-draft [section]` | 论文章节草稿 |
| `/proofread [file]` | 校对 |
| `/lit-review [topic]` | 文献综述 |
| `/weekly-report` | 周报 |
| `/slides [topic]` | 组会 slides |
| `/research-idea [desc]` | 形式化研究想法 |

## Quality Gates
| 分数 | 操作 |
|------|------|
| >= 80 | 可提交 |
| < 80 | 先修复 |
| explorations/ | 60 即可 |

## Non-Negotiables
- Look-ahead bias 零容忍
- 每个实验必须有 seed
- NaN 必须检查和处理
- Test split 开发期间禁用
- 论文数据必须可复现 (代码生成, 非手动)
