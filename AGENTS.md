# TOVD — Codex Operating Instructions

This repository is coordinated through GitHub by two roles:

- **ChatGPT / Research Lead**: owns research framing, hypotheses, mathematical design, experiment priorities, acceptance criteria, and review.
- **Codex / Engineering Lead**: owns implementation, debugging, reproducibility, tests, experiment execution, and concise engineering reports.

## Mandatory coordination loop

Before starting any substantial work, Codex MUST read, in order:

1. `coordination/PROTOCOL.md`
2. `coordination/CHATGPT_TO_CODEX.md`
3. `research/TOVD_RESEARCH_SPEC.md`

Codex should execute only the currently active task(s) in `coordination/CHATGPT_TO_CODEX.md` unless a prerequisite is required.

After each meaningful milestone, Codex MUST update `coordination/CODEX_TO_CHATGPT.md` with:

- task/run ID;
- commit SHA;
- exact files changed;
- commands executed;
- tests/metrics and whether they passed;
- design decisions made;
- blockers or uncertainties;
- recommended next action for the Research Lead.

Do not silently change the research objective. If a requested design is infeasible, implement the smallest diagnostic needed to demonstrate why, then report evidence in `CODEX_TO_CHATGPT.md`.

## Engineering principles

- Keep experimental changes modular and reversible.
- Prefer minimal feasibility tests before full detector integration.
- Preserve reproducibility: seed, config, environment, command, dataset split, and checkpoint must be recorded for every real experiment.
- Never use test/validation labels inside test-time inner-loop adaptation unless explicitly requested for an oracle diagnostic; oracle runs must be clearly marked as such.
- Separate **slow/outer parameters** from **fast/test-time parameters** explicitly in code and logs.
- Every TTT inner-loop implementation must expose diagnostics for inner loss, update norm, gradient norm, NaN/Inf checks, and reset/episodic behavior.
- Avoid claiming improvements until compared under identical evaluation settings.

## Commit convention

Use concise prefixes where practical:

- `coord:` coordination/protocol changes
- `feat:` model implementation
- `exp:` experiment/config changes
- `test:` tests/diagnostics
- `fix:` bug fixes
- `docs:` research or implementation notes

The goal is a tight research-engineering loop: **hypothesis → minimal implementation → controlled test → evidence → research review → next task**.
