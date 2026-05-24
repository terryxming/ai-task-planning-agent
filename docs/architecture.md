# 架构说明

AI Task Planning Agent 采用一个入口 Skill、多个 reference manuals、JSON manifests、确定性 scripts、fixtures、tests 和 release docs 的结构。

## 入口 Skill

`skills/ai-task-planning-agent/SKILL.md` 是唯一 Skill 入口。它只保留触发规则、工作流、必读 references、必跑 scripts 和硬失败条件。

## References

`references/` 存放专业模块手册，覆盖 orchestration、clarification、Agile value planning、harness execution planning、role decisions、delivery packaging、release gates 和 governance。

## 事实源

`package-manifest.json`、`execution-manifest.json`、`tool-contract-matrix.json` 和 `eval-plan.json` 是机器可读事实源。Markdown 文件只作为人工审阅视图。

## 确定性门禁

`scripts/` 负责校验 manifests、评估 task packs、渲染 artifact indexes。脚本不执行用户业务代码，也不连接生产环境。

## 回归证明

`fixtures/` 包含一个 valid pack，以及缺少 tool contract、存在 blocking open question、缺少 recovery path、Markdown/manifest 冲突等 negative packs。

## v0.2 调整

v0.2 把默认表达语言调整为中文，并把 schema 文件接入验证流程。Evaluator 可以按需写入 `evaluation-result.json`，用于审计和发布记录。
