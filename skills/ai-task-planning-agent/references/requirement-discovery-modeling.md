# Requirement Discovery & Modeling Engine

## 职责

把 Clarification Engine 输出的事实、假设、未知项和阻塞问题，进一步挖掘并建模成可被 Agile Value Planner 和 Harness Execution Planner 使用的需求事实源。

该模块不是继续“随便追问”，而是使用规范的需求分析、需求挖掘和需求建模方法，把模糊想法转化为 `requirement-model.json`。

## 工作流

1. 原始想法归档：保留用户原始表达，避免过早改写。
2. 触发原因挖掘：追问为什么现在想做，识别痛点、机会、重复劳动、流程失控或能力沉淀。
3. 问题定义：形成 `problem_statement`，明确当前问题及其影响。
4. 真实目标建模：用 current state -> target state 描述想要的变化。
5. 用户与场景建模：明确 target users、usage scenarios 和 jobs to be done。
6. 交付物、边界与约束定义：明确 desired outputs、scope in、scope out 和 constraints。
7. 需求结构化、优先级和验证：用 MECE、MoSCoW、SMART、5W2H、5 Why、JTBD 等方法形成 requirement groups、priorities 和 validation evidence。
8. Agile handoff：只输出可被 Agile 使用的需求模型，不直接替 Agile 拆 backlog。

## 必需输出

- `requirement-model.json`
- `requirement-discovery-report.md`，如需要人工审阅视图

## `requirement-model.json` 必填字段

- `raw_idea`
- `trigger_reasons`
- `problem_statement`
- `current_state`
- `target_state`
- `target_users`
- `usage_scenarios`
- `jobs_to_be_done`
- `desired_outputs`
- `scope_in`
- `scope_out`
- `constraints`
- `success_criteria`
- `failure_criteria`
- `requirement_groups`
- `priorities`
- `validation_evidence`
- `blocking_questions`

## 进入 Agile 前的门禁

以下任一情况存在时，不得进入 Agile Value Planner：

- 缺少 `requirement-model.json`。
- `problem_statement` 为空。
- `target_users` 为空。
- `usage_scenarios` 为空。
- `jobs_to_be_done` 为空。
- `desired_outputs` 为空。
- `scope_out` 为空。
- `success_criteria` 为空。
- `blocking_questions` 非空。

## 硬失败

- 只有功能表达，没有真实问题。
- 只有目标口号，没有 current state 和 target state。
- 不知道给谁用或在哪个场景使用。
- 没有 scope out，导致边界失控。
- 没有 validation evidence，无法判断需求真实性。
- Blocking questions 非空。v0.3 起不允许对 `requirement-model.json` 缺失或阻塞问题设置例外。
