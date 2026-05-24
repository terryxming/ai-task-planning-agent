# Agile Plan

## Product Goal

Help AI Agent builders produce a validated execution package that downstream coding agents can follow without re-clarifying core requirements.

## Backlog

- Define the task boundary.
- Create execution contracts.
- Package artifacts.
- Run release gate evaluation.

## Definition of Ready

- Goal, non-goals, target downstream AI, and success criteria are present.

## Definition of Done

- Evaluator returns `pass` for the package.
- Negative fixtures block release.

## Review and Retro

Review evaluator output and add regression fixtures for newly discovered hard failures.
