# Architecture

AI Task Planning Agent uses one entry Skill, multiple reference manuals, JSON manifests, deterministic scripts, fixtures, tests, and release docs.

## Entry Skill

`skills/ai-task-planning-agent/SKILL.md` is the only Skill entrypoint. It contains trigger rules, workflow, required references, required scripts, and hard failures.

## References

`references/` stores professional module manuals for orchestration, clarification, Agile value planning, harness execution planning, role decisions, delivery packaging, release gates, and governance.

## Source of Truth

`package-manifest.json`, `execution-manifest.json`, `tool-contract-matrix.json`, and `eval-plan.json` are machine-readable facts. Markdown files are human review views.

## Deterministic Gate

`scripts/` validates manifests, evaluates task packs, and renders artifact indexes. Scripts do not execute user business code or connect to production.

## Regression Proof

`fixtures/` contains one valid pack and negative packs for missing tool contracts, blocking open questions, missing recovery paths, and Markdown/manifest conflicts.
