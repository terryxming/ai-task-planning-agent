# 架构说明

AI Task Planning Agent 采用一个入口 Skill、多个 reference manuals、JSON manifests、确定性 scripts、fixtures、tests 和 release docs 的结构。

## 入口 Skill

`skills/ai-task-planning-agent/SKILL.md` 是唯一 Skill 入口。它只保留触发规则、工作流、必读 references、必跑 scripts 和硬失败条件。

## References

`references/` 存放专业模块手册，覆盖 orchestration、clarification、Agile value planning、harness execution planning、role decisions、delivery packaging、release gates 和 governance。

v0.3 起新增 `Requirement Discovery & Modeling Engine`。它位于 Clarification Engine 和 Agile Value Planner 之间，负责把模糊想法挖掘并建模为 `requirement-model.json`。

v0.4 起新增 `Clarification Council Loop`。它位于 Clarification Engine 和 Requirement Discovery & Modeling Engine 之间，负责把“追问、挑刺、角色参与、修正版理解、用户确认和阶段 brief”记录为 `clarification-session.json`。

v0.4 同时把 Agile Value Planner 升级为机器可验证规划层，负责把 User Story、Acceptance Criteria、INVEST、Story Mapping、Story Splitting、MVP、Sprint Backlog、Increment 和 Eval cases 记录为 `agile-plan.json`。

## 事实源

`package-manifest.json`、`clarification-session.json`、`requirement-model.json`、`agile-plan.json`、`execution-manifest.json`、`tool-contract-matrix.json` 和 `eval-plan.json` 是机器可读事实源。Markdown 文件只作为人工审阅视图。

## 确定性门禁

`scripts/` 负责校验 manifests、评估 task packs、渲染 artifact indexes。脚本不执行用户业务代码，也不连接生产环境。

## 回归证明

`fixtures/` 包含一个 valid pack，以及缺少 tool contract、存在 blocking open question、缺少 recovery path、Markdown/manifest 冲突等 negative packs。

## v0.2 调整

v0.2 把默认表达语言调整为中文，并把 schema 文件接入验证流程。Evaluator 可以按需写入 `evaluation-result.json`，用于审计和发布记录。

## v0.3 调整

v0.3 把需求挖掘与建模升级为不可跳过的正式阶段。没有 `requirement-model.json`，或需求模型缺少问题定义、目标用户、使用场景、JTBD、边界、成功标准，Evaluator 必须 block。

## v0.4 调整

v0.4 把澄清过程和敏捷拆解过程都升级为不可跳过的机器事实源。没有 `clarification-session.json` 或 `agile-plan.json`，或缺少追问、挑刺、用户确认、角色字段绑定、AC、INVEST、MVP、Increment、Eval cases，Evaluator 必须 block。

`SKILL.md` 入口治理由 `references/skill-governance.md` 和 `scripts/validate_skill_entry.py` 负责，避免入口文件变成领域知识堆。
