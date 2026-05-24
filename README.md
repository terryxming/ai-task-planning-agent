# AI Task Planning Agent

AI Task Planning Agent 面向 AI Agent builder，把模糊任务规划为可验证的 `Task Execution Pack`，供 Codex、Claude Code 等下游 coding agent 执行和自检。

本项目的非目标很明确：不直接执行用户业务代码，不连接生产环境，不替代 Jira 或 Linear，也不会自动修改用户已有 Skill。

## 输出

核心输出是一个 `Task Execution Pack`：

- `package-manifest.json`
- `clarification-session.json`
- `requirement-model.json`
- `task-brief.md`
- `agile-plan.md`
- `agile-plan.json`
- `execution-manifest.json`
- `tool-contract-matrix.json`
- `eval-plan.json`
- `role-decision-log.md`
- `human-review-report.md`
- `governance-report.md`
- `artifact-index.md`

机器可读 JSON 文件是事实源。Markdown 文件只是人工审阅视图。

## v0.2 新增能力

- 默认中文表达，必要技术术语保留英文。
- 使用本地 JSON Schema 子集校验器检查 manifest、tool contract 和 eval plan。
- Human waiver 必须结构化记录豁免项、原因、风险、范围、责任人和过期条件。
- Evaluator 支持 `--write-result` 写入 `evaluation-result.json`。
- 保留 `v0.1` tag 作为初始基线。

## v0.3 新增能力

- 新增独立模块 `Requirement Discovery & Modeling Engine`，位于 Clarification Engine 和 Agile Value Planner 之间。
- `requirement-model.json` 升级为 `Task Execution Pack` 必需机器事实源，不允许例外。
- 新增 `requirement-model.schema.json` 和 `validate_requirement_model.py`。
- Evaluator 会阻断缺少 requirement model、问题定义为空、目标用户为空、使用场景为空、JTBD 为空、scope out 为空、成功标准为空或需求模型仍有 blocking questions 的 pack。

## v0.4 新增能力

- 新增 `Clarification Council Loop`，强制“追问 + 挑刺”双轨：每轮五问、先挑刺再整理、用户确认后才能进入下一轮。
- Role Council 前置为横切机制，每轮角色必须发言、反驳、补充并绑定受影响字段。
- `clarification-session.json` 升级为必需机器事实源，记录追问、挑刺、角色参与、修正版理解、用户确认和阶段 brief。
- `agile-plan.json` 升级为必需机器事实源，记录 User Story、Acceptance Criteria、INVEST、Story Mapping、Story Splitting、MVP、Sprint Backlog、Increment 和 Eval cases。
- 新增 `validate_clarification_session.py`、`validate_agile_plan.py` 和 `validate_skill_entry.py`。
- 新增 SKILL.md 入口治理，防止把完整领域方法论塞回单个 `SKILL.md`。

## 快速验证

```bash
python skills/ai-task-planning-agent/scripts/validate_package_manifest.py skills/ai-task-planning-agent/fixtures/valid-task-pack
python skills/ai-task-planning-agent/scripts/validate_clarification_session.py skills/ai-task-planning-agent/fixtures/valid-task-pack
python skills/ai-task-planning-agent/scripts/validate_requirement_model.py skills/ai-task-planning-agent/fixtures/valid-task-pack
python skills/ai-task-planning-agent/scripts/validate_agile_plan.py skills/ai-task-planning-agent/fixtures/valid-task-pack
python skills/ai-task-planning-agent/scripts/validate_execution_manifest.py skills/ai-task-planning-agent/fixtures/valid-task-pack
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/valid-task-pack
python skills/ai-task-planning-agent/scripts/validate_skill_entry.py skills/ai-task-planning-agent/SKILL.md
python -m unittest discover tests
```

预期结果：valid fixture 通过，negative fixtures 按预期阻断发布。

## 最终验证

在仓库根目录运行完整测试：

```bash
python -m unittest discover tests
```

运行 fixture smoke tests：

```bash
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/valid-task-pack
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/missing-tool-contract
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/blocking-open-question
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/missing-recovery-path
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/missing-requirement-model
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/markdown-manifest-conflict
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/missing-clarification-session
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/unconfirmed-clarification-round
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/missing-critique
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/role-without-field-updates
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/missing-agile-plan
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/story-without-acceptance-criteria
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/missing-invest
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/missing-mvp
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/missing-agile-eval-cases
```

预期结果：`valid-task-pack` exit code 为 `0` 且 `release_recommendation: pass`；每个 negative fixture exit code 为 `2` 且 `release_recommendation: block`。
