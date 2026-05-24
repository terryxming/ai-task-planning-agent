# Role Decision Log

| Decision id | Topic | Proposal | Challenge | Evidence | Decision | Impacted artifacts | Regression risk |
|---|---|---|---|---|---|---|---|
| DEC-001 | Release gate | Require deterministic evaluation before delivery-ready status. | Field presence alone may miss conflicts. | Contract requires hard failure checks and negative cases. | Use evaluator output as release gate. | `eval-plan.json`, `package-manifest.json` | False pass if evaluator misses conflict markers. |
