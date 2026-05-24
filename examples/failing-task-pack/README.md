# Failing Task Pack Example

## Scenario

A pack has a complete manifest but `execution-manifest.json` contains an empty `recovery_paths` array.

## Expected Hard Failure

```bash
python ../../skills/ai-task-planning-agent/scripts/evaluate_task_pack.py ../../skills/ai-task-planning-agent/fixtures/missing-recovery-path
```

Expected result:

- exit code `2`
- `release_recommendation: block`
- hard failure mentions `recovery_paths`
