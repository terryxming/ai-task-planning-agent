# Failing Task Pack 示例

## 场景

某个 pack 的 manifest 看似完整，但 `execution-manifest.json` 中 `recovery_paths` 是空数组。

## 预期硬失败

```bash
python ../../skills/ai-task-planning-agent/scripts/evaluate_task_pack.py ../../skills/ai-task-planning-agent/fixtures/missing-recovery-path
```

预期结果：

- exit code 为 `2`
- `release_recommendation: block`
- hard failure 提到 `recovery_paths`
