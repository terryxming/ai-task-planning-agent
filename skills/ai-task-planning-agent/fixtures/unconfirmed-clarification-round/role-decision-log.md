# 角色决策日志

| Decision id | Topic | Proposal | Challenge | Evidence | Decision | Impacted artifacts | Regression risk |
|---|---|---|---|---|---|---|---|
| DEC-001 | Release gate | 交付前必须运行 deterministic evaluation。 | 只检查字段存在可能漏掉冲突。 | 契约要求 hard failure checks 和 negative cases。 | 使用 evaluator output 作为 release gate。 | `eval-plan.json`, `package-manifest.json` | 如果 evaluator 漏掉 conflict marker，可能 false pass。 |
