# AI Task Planning Agent

AI Task Planning Agent 面向 AI Agent builder，把模糊任务规划为可验证的 `Task Execution Pack`，供 Codex、Claude Code 等下游 coding agent 执行和自检。

本项目的非目标很明确：不直接执行用户业务代码，不连接生产环境，不替代 Jira 或 Linear，也不会自动修改用户已有 Skill。

## 输出

核心输出是一个 `Task Execution Pack`：

- `package-manifest.json`
- `requirement-model.json`
- `task-brief.md`
- `agile-plan.md`
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

## 快速验证

```bash
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/valid-task-pack
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
```

预期结果：`valid-task-pack` exit code 为 `0` 且 `release_recommendation: pass`；每个 negative fixture exit code 为 `2` 且 `release_recommendation: block`。
