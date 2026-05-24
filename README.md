# AI Task Planning Agent

AI Task Planning Agent helps AI Agent builders turn ambiguous tasks into validated `Task Execution Pack` artifacts for downstream coding agents such as Codex and Claude Code.

The agent does not execute code, connect to production, replace Jira or Linear, or modify existing user skills automatically.

## Output

The primary output is a `Task Execution Pack`:

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

Machine-readable JSON files are the source of truth. Markdown files are human review views.

## Quick Validation

```bash
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/valid-task-pack
python -m unittest discover tests
```

Expected result: the valid fixture passes and the negative fixtures fail for the expected reasons.

## Final Verification

Run the full test suite from the repository root:

```bash
python -m unittest discover tests
```

Run fixture smoke tests from the repository root:

```bash
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/valid-task-pack
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/missing-tool-contract
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/blocking-open-question
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/missing-recovery-path
python skills/ai-task-planning-agent/scripts/evaluate_task_pack.py skills/ai-task-planning-agent/fixtures/markdown-manifest-conflict
```

Expected result: `valid-task-pack` exits `0` with `release_recommendation: pass`; each negative fixture exits `2` with `release_recommendation: block`.
