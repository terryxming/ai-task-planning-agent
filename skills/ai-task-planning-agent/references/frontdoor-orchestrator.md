# Frontdoor / Orchestrator

## Responsibility

Identify request type, mode, target downstream AI, current state, next state, and recovery action.

## Inputs

- User request
- Existing task pack, if present
- Conversation summary
- Validation results

## Outputs

- Request type
- Mode: light, standard, or deep
- Current state
- Next state
- Recovery action
- Manifest updates

## Hard Failures

- Coding-agent task routed as a generic PRD task.
- Evaluator failed but the pack is marked delivery-ready.
- No `package-manifest.json` exists and no light-mode exception is recorded.
