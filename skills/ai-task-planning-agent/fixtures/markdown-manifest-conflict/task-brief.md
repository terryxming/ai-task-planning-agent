# Task Brief

## Goal

Create a Task Execution Pack for a downstream coding agent.

## Non-Goals

- Do not execute user business code.
- Do not connect to production.
- Do not replace Jira or Linear.

## Known Facts

- The agent creates Task Execution Pack artifacts for downstream coding agents.
- Machine-readable JSON files are the source of truth.
- The agent must not execute user business code.

MANIFEST_CONFLICT: Machine-readable JSON files are not the source of truth.

## Success Criteria

- Required JSON files are present.
- Blocking questions are empty or waived.
- Recovery paths and trace requirements are non-empty.
