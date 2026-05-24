# Evaluator / Release Gate

## Responsibility

Block delivery when deterministic requirements fail.

## Required Checks

- Required files exist.
- Manifest schema fields exist.
- Execution manifest fields exist.
- Tool contracts include side effects, permission, failure modes, retry policy, and rollback policy.
- Eval plan includes negative cases.
- Blocking questions have waiver or block release.

## Output

Evaluation result JSON with `status`, `hard_failures`, `warnings`, and `release_recommendation`.
