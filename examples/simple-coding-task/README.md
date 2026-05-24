# 简单 Coding Task 示例

## 粗略用户请求

“给我的 CLI 增加输入校验，并让错误配置文件给出清晰失败信息。”

## 预期 Task Execution Pack 文件

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

## 校验 Pack

```bash
python ../../skills/ai-task-planning-agent/scripts/evaluate_task_pack.py ../../skills/ai-task-planning-agent/fixtures/valid-task-pack
```

完整 pack 应返回 `release_recommendation: pass`。
