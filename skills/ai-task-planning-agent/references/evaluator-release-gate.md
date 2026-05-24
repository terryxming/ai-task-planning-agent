# Evaluator / Release Gate

## 职责

当确定性要求失败时阻断交付。

## 必需检查

- 必需文件存在。
- Manifest schema 字段存在并通过 schema-driven 校验。
- Execution manifest 字段存在并通过 schema-driven 校验。
- Tool contracts 包含 side effects、permission、failure modes、retry policy、rollback policy 和 audit evidence。
- Eval plan 包含 negative cases。
- Blocking questions 必须被结构化 human waiver 覆盖，否则 block release。

## 输出

Evaluation result JSON，包含 `status`、`hard_failures`、`warnings` 和 `release_recommendation`。
