# v0.4 Clarification Council Governance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Add v0.4 governance so fuzzy user ideas must pass a structured clarification council loop, machine-readable agile planning, and explicit SKILL.md entry governance before delivery.

**Architecture:** Keep `SKILL.md` as the concise entry point and move detailed policy into `references/`. Add `clarification-session.json` and `agile-plan.json` as mandatory machine fact sources, validated by deterministic scripts and enforced by the evaluator.

**Tech Stack:** Python standard library `unittest`, local JSON schema subset validator, Markdown references, Task Execution Pack fixtures.

---

### Task 1: Write v0.4 Failing Tests

**Files:**
- Create: `tests/test_v04_clarification_council.py`
- Create: `tests/test_v04_agile_plan.py`
- Create: `tests/test_v04_skill_governance.py`

- [x] **Step 1: Add clarification council tests**

Create tests that require `validate_clarification_session.py` and `evaluate_task_pack.py` to pass valid fixtures and block missing confirmation, missing critique, and missing role field ownership.

- [x] **Step 2: Add agile plan tests**

Create tests that require `validate_agile_plan.py` and `evaluate_task_pack.py` to block missing `agile-plan.json`, missing story acceptance criteria, missing INVEST checks, missing MVP, and missing eval cases.

- [x] **Step 3: Add SKILL governance tests**

Create tests that require `validate_skill_entry.py` to ensure `SKILL.md` stays concise, defaults to Chinese, references all v0.4 manuals and scripts, and mentions hard failures for `clarification-session.json` and `agile-plan.json`.

- [x] **Step 4: Run tests and confirm RED**

Run: `python -m unittest tests.test_v04_clarification_council tests.test_v04_agile_plan tests.test_v04_skill_governance`

Expected: fail because new scripts, schemas, references, and fixtures do not exist yet.

### Task 2: Add Schemas and Validators

**Files:**
- Create: `skills/ai-task-planning-agent/schemas/clarification-session.schema.json`
- Create: `skills/ai-task-planning-agent/schemas/agile-plan.schema.json`
- Create: `skills/ai-task-planning-agent/scripts/validate_clarification_session.py`
- Create: `skills/ai-task-planning-agent/scripts/validate_agile_plan.py`
- Create: `skills/ai-task-planning-agent/scripts/validate_skill_entry.py`
- Modify: `skills/ai-task-planning-agent/scripts/validate_package_manifest.py`
- Modify: `skills/ai-task-planning-agent/scripts/evaluate_task_pack.py`

- [x] **Step 1: Implement minimal validators**

Each validator loads one JSON or Markdown file, applies the local schema validator where relevant, checks v0.4 hard failures, prints JSON, and exits `0` on pass or `2` on fail.

- [x] **Step 2: Enforce new artifacts in package manifest**

Add `clarification-session.json` and `agile-plan.json` to required artifacts and manifest registration checks.

- [x] **Step 3: Add evaluator checks**

Import and run the new clarification and agile validators inside `evaluate_task_pack.py`, and prefix failures with `clarification-session:` or `agile-plan:`.

- [x] **Step 4: Run v0.4 tests and confirm partial GREEN**

Run the three v0.4 test modules. Expected: remaining failures only from fixtures/docs not yet updated.

### Task 3: Update Fixtures

**Files:**
- Modify: all fixture `package-manifest.json` files
- Create: fixture `clarification-session.json` files
- Create: fixture `agile-plan.json` files
- Create: v0.4 negative fixture directories

- [x] **Step 1: Update valid fixture**

Add valid `clarification-session.json` and `agile-plan.json` to `valid-task-pack`, and register both in `package-manifest.json`.

- [x] **Step 2: Update existing negative fixtures**

Add valid v0.4 files to existing negative fixtures so they continue to fail for their intended original reason.

- [x] **Step 3: Add v0.4 negative fixtures**

Create fixtures for missing clarification session, unconfirmed next round, missing critique, role without fields, missing agile plan, story without AC, missing INVEST, missing MVP, missing eval cases, and overgrown SKILL governance if needed by tests.

- [x] **Step 4: Run fixture smoke**

Run evaluator against all fixtures. Expected: valid fixture returns `pass`; every negative fixture returns `block`.

### Task 4: Update Skill References and Docs

**Files:**
- Modify: `skills/ai-task-planning-agent/SKILL.md`
- Create: `skills/ai-task-planning-agent/references/clarification-council.md`
- Create: `skills/ai-task-planning-agent/references/skill-governance.md`
- Modify: `skills/ai-task-planning-agent/references/clarification-engine.md`
- Modify: `skills/ai-task-planning-agent/references/requirement-discovery-modeling.md`
- Modify: `skills/ai-task-planning-agent/references/agile-value-planner.md`
- Modify: `skills/ai-task-planning-agent/references/role-council.md`
- Modify: `skills/ai-task-planning-agent/references/evaluator-release-gate.md`
- Modify: `skills/ai-task-planning-agent/references/governance-layer.md`
- Modify: `README.md`
- Modify: `docs/architecture.md`
- Modify: `docs/release-checklist.md`
- Modify: `CHANGELOG.md`

- [x] **Step 1: Keep SKILL.md concise**

Update the workflow, required references, required scripts, and hard failures without embedding full method templates.

- [x] **Step 2: Add detailed references**

Put the five-question loop, critique loop, role participation contract, stage brief rule, and SKILL governance policy into references.

- [x] **Step 3: Update release docs**

Document v0.4 goals, non-goals, validation commands, artifact index expectations, and release checklist status.

- [x] **Step 4: Run SKILL governance validator**

Run: `python skills/ai-task-planning-agent/scripts/validate_skill_entry.py skills/ai-task-planning-agent/SKILL.md`

Expected: pass.

### Task 5: Verify, Commit, Tag, Push

**Files:**
- All changed files from Tasks 1-4.

- [x] **Step 1: Run full unit tests**

Run: `python -m unittest discover tests`

Expected: all tests pass.

- [x] **Step 2: Run all release gate commands**

Run package, clarification, requirement, agile, execution, evaluator, artifact index, and skill validators.

- [x] **Step 3: Scan for private paths in published bundle**

Run a text scan over release-facing files and ensure no local private path is present.

- [x] **Step 4: Commit and tag**

Commit message: `feat: add v0.4 clarification council governance`

Tag: `v0.4`

- [x] **Step 5: Push main and tag**

Push to `origin main` and `origin v0.4`.
