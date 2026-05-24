# CHANGELOG

## Unreleased

## v0.3.0-alpha

- 新增 Requirement Discovery & Modeling Engine，作为 Clarification Engine 和 Agile Value Planner 之间的独立必经模块。
- `requirement-model.json` 升级为 Task Execution Pack 必需机器事实源，不允许例外。
- 新增 `requirement-model.schema.json` 和 `validate_requirement_model.py`。
- Evaluator 接入 requirement model release gate。
- Fixtures、artifact index、README、Skill、architecture docs 和 tests 同步 v0.3 契约。
- 增加 `missing-requirement-model` negative fixture。
- 保持 release status 为 alpha。

## v0.2.0-alpha

- 默认中文化 README、Skill 入口、reference manuals、examples 和 release docs。
- 增加本地 JSON Schema 子集校验器，并接入 package manifest、execution manifest、tool contract matrix 和 eval plan 校验。
- 增加 structured human waiver 校验，要求记录豁免项、原因、接受风险、影响范围、责任人和过期条件。
- Evaluator 增加 `--write-result`，可写入 `evaluation-result.json`。
- 增加 v0.2 release gate 回归测试。
- 保持 release status 为 alpha。

## v0.1.0-alpha

- Initial AI Task Planning Agent repo.
- Added Codex Skill bundle.
- Added Task Execution Pack schemas.
- Added deterministic validation and evaluation scripts.
- Added positive and negative fixtures.
- Added release gate tests.
- Added release documentation and kept release status as alpha.
