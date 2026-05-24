# Simple Coding Task Example

## Rough User Request

"Add input validation to my CLI and make sure bad config files fail clearly."

## Expected Task Execution Pack Files

- `package-manifest.json`
- `task-brief.md`
- `agile-plan.md`
- `execution-manifest.json`
- `tool-contract-matrix.json`
- `eval-plan.json`
- `role-decision-log.md`
- `human-review-report.md`
- `governance-report.md`
- `artifact-index.md`

## Validate the Pack

```bash
python ../../skills/ai-task-planning-agent/scripts/evaluate_task_pack.py ../../skills/ai-task-planning-agent/fixtures/valid-task-pack
```

The evaluator should return `release_recommendation: pass` for a complete pack.
