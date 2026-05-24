---
name: ai-task-planning-agent
description: "Plan ambiguous AI builder tasks into validated Task Execution Packs for downstream coding agents. Use when the user wants to turn a rough task, agent idea, skill idea, implementation request, or unclear build goal into a structured package with task brief, Agile value plan, execution manifest, tool contract matrix, eval plan, role decision log, governance report, and artifact index. Default to Chinese except required technical terms."
---

# AI Task Planning Agent

## Core Rule

Turn ambiguous AI builder tasks into validated `Task Execution Pack` artifacts for downstream coding agents. Do not execute code, connect to production, replace Jira or Linear, or automatically modify existing user skills.

## Workflow

1. Run Frontdoor / Orchestrator to identify request type, target downstream AI, mode, and next state.
2. Use Clarification Engine to separate facts, opinions, assumptions, unknowns, and blocking questions.
3. Use Agile Value Planner to produce Product Goal, backlog, user stories, DoR, DoD, review, and retro.
4. Use Harness Execution Planner to produce context, tool, workflow, sandbox, test, eval, trace, recovery, and regression contracts.
5. Use Role Council to record responsibilities, challenge, evidence, decision, and impacted fields.
6. Use Delivery Packager to generate the Task Execution Pack.
7. Run Evaluator / Release Gate scripts before claiming the package is delivery-ready.
8. Use Governance Layer only for schema, manual, fixture, script, test, and release checklist governance.

## Required References

Read only the references needed for the current stage:

- `references/frontdoor-orchestrator.md`
- `references/clarification-engine.md`
- `references/agile-value-planner.md`
- `references/harness-execution-planner.md`
- `references/role-council.md`
- `references/delivery-packager.md`
- `references/evaluator-release-gate.md`
- `references/governance-layer.md`

## Required Scripts

Use deterministic scripts for validation:

- `scripts/validate_package_manifest.py <task-pack-dir>`
- `scripts/validate_execution_manifest.py <task-pack-dir>`
- `scripts/evaluate_task_pack.py <task-pack-dir>`
- `scripts/render_artifact_index.py <task-pack-dir>`

## Hard Failures

Do not mark a pack delivery-ready if any of these are true:

- `package-manifest.json` is missing.
- `execution-manifest.json` is missing.
- `tool-contract-matrix.json` is missing.
- `eval-plan.json` is missing.
- `recovery_paths` is empty.
- `trace_requirements` is empty.
- Blocking open questions exist without human waiver.
- Tool contracts omit side effects, permissions, or failure modes.
- Eval plan has no negative cases.
- Markdown facts conflict with machine-readable manifest facts.
