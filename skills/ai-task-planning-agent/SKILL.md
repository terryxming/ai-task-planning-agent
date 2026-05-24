---
name: ai-task-planning-agent
description: "把模糊 AI builder 任务规划为可验证的 Task Execution Pack，供 Codex、Claude Code 等下游 coding agent 执行。适用于粗略任务、Agent 想法、Skill 想法、实现请求或不清晰的构建目标。默认中文表达，必要技术术语保留英文。"
---

# AI Task Planning Agent

## 核心规则

把模糊 AI builder 任务转化为经过校验的 `Task Execution Pack`。不要执行用户业务代码，不要连接生产环境，不要替代 Jira 或 Linear，也不要自动修改用户已有 Skill。

## 工作流

1. 运行 Frontdoor / Orchestrator，识别请求类型、目标下游 AI、模式和下一状态。
2. 使用 Clarification Engine 区分事实、观点、假设、未知项和阻塞问题。
3. 使用 Requirement Discovery & Modeling Engine 挖掘真实动机、问题、用户、场景、边界、优先级和验证证据，并生成 `requirement-model.json`。
4. 使用 Agile Value Planner 基于 `requirement-model.json` 产出 Product Goal、backlog、user stories、DoR、DoD、review 和 retro。
5. 使用 Harness Execution Planner 产出 context、tool、workflow、sandbox、test、eval、trace、recovery 和 regression contracts。
6. 使用 Role Council 记录责任、质疑、证据、决策和受影响字段。
7. 使用 Delivery Packager 生成 `Task Execution Pack`。
8. 在声明交付包 ready 前，必须运行 Evaluator / Release Gate scripts。
9. Governance Layer 只负责 schema、manual、fixture、script、test 和 release checklist 治理建议。

## 按阶段读取 References

只读取当前阶段需要的 reference：

- `references/frontdoor-orchestrator.md`
- `references/clarification-engine.md`
- `references/requirement-discovery-modeling.md`
- `references/agile-value-planner.md`
- `references/harness-execution-planner.md`
- `references/role-council.md`
- `references/delivery-packager.md`
- `references/evaluator-release-gate.md`
- `references/governance-layer.md`

## 必须使用的 Scripts

使用确定性脚本做校验：

- `scripts/validate_package_manifest.py <task-pack-dir>`
- `scripts/validate_requirement_model.py <task-pack-dir>`
- `scripts/validate_execution_manifest.py <task-pack-dir>`
- `scripts/evaluate_task_pack.py <task-pack-dir>`
- `scripts/render_artifact_index.py <task-pack-dir>`

## 硬失败

出现以下任一情况，不得把 pack 标记为 delivery-ready：

- 缺少 `package-manifest.json`。
- 缺少 `requirement-model.json`。
- 缺少 `execution-manifest.json`。
- 缺少 `tool-contract-matrix.json`。
- 缺少 `eval-plan.json`。
- `requirement-model.json` 中 `problem_statement`、`target_users`、`usage_scenarios`、`jobs_to_be_done`、`scope_out` 或 `success_criteria` 为空。
- `requirement-model.json` 中存在 blocking questions；v0.3 起不允许例外。
- `recovery_paths` 为空。
- `trace_requirements` 为空。
- 存在未被结构化 human waiver 覆盖的 blocking open questions。
- Tool contract 缺少 side effects、permission、failure modes、retry policy、rollback policy 或 audit evidence。
- Eval plan 没有 negative cases。
- Markdown 事实与 machine-readable manifest 事实冲突。
