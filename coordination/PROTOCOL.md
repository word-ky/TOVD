# ChatGPT ↔ Codex Coordination Protocol

## Roles

### Research Lead — ChatGPT
Owns:
- problem definition and novelty boundary;
- mathematical formulation;
- experiment hypotheses and ablations;
- task priority and acceptance/rejection of results;
- interpretation of Codex reports and next-step instructions.

### Engineering Lead — Codex
Owns:
- repository implementation;
- tests, debugging, reproducibility and experiment execution;
- faithful implementation of the active research task;
- evidence-rich reporting back to ChatGPT.

## Shared mailbox

- `coordination/CHATGPT_TO_CODEX.md`: authoritative current instructions from Research Lead.
- `coordination/CODEX_TO_CHATGPT.md`: authoritative engineering report from Codex.
- `research/TOVD_RESEARCH_SPEC.md`: persistent research hypothesis/specification.

Codex should treat the newest task block marked `ACTIVE` as highest priority.
ChatGPT should treat only committed code/results as completed work.

## Task state machine

`PROPOSED -> ACTIVE -> IMPLEMENTED -> VERIFIED -> ACCEPTED`

Alternative terminal states:
- `REJECTED`: result disproves or invalidates the direction.
- `BLOCKED`: dependency prevents progress; report exact blocker.
- `SUPERSEDED`: replaced by a newer task/design.

Only ChatGPT/Research Lead marks a research task `ACCEPTED`, `REJECTED`, or `SUPERSEDED`.
Codex may mark implementation status and verification evidence.

## Reporting contract

For every task, Codex reports:

1. **Task ID / Run ID**
2. **Status**
3. **Commit SHA**
4. **Files changed**
5. **Implementation summary**
6. **Commands executed**
7. **Tests and exact outputs/metrics**
8. **Diagnostics** (inner loss, update norm, gradient norm, reset behavior, NaN/Inf)
9. **Deviations from spec** and why
10. **Blockers / uncertainties**
11. **Recommended next experiment**

## Research discipline

- First establish mechanism feasibility with synthetic/unit tests.
- Then integrate into a detector.
- Then run small controlled experiments.
- Only then scale training/evaluation.
- Never hide failed runs; failed hypotheses are useful evidence.
- Distinguish *engineering pass* from *scientific success*.
- Preserve baselines and identical evaluation conditions.

## Test-time-learning safeguards

For every fast-weight / inner-loop module:

- default mode is **episodic reset** per image/batch unless task explicitly requests continual adaptation;
- no ground-truth detection labels are allowed in the inner loss;
- log update magnitude `||W* - W0||`;
- log inner gradient norm;
- verify same image + different vocabulary changes the fast state when vocabulary conditioning is enabled;
- verify same image + same vocabulary + same seed is reproducible;
- verify outer gradients can flow through the inner update when training the meta-initialization;
- provide a switch to disable the TTT path for a strict baseline.

## Communication cadence

Git commits are the source of truth. Codex should update the report after meaningful milestones rather than waiting for a large batch of work. ChatGPT will review the newest commits/report when invoked or on any configured automation cadence.
