# T003 progress

## 2026-09-12 — Started from research review 0c3ef5f
- Read project-local state/logs and ordered protocol/inbox/spec; T002 accepted as a valid negative result.
- Fixed T003 plan saved before aggregate results; only existing P/B2 checkpoints and T002 held-out streams will be used.
- Existing 23-test suite reproduced before edits. Next: isolated oracle-diagnostic math and focused equality/gradient tests.

## 2026-09-12 03:04:50 +08:00 — Oracle math increment
- Baseline 23 passed in 11.12s before edits.
- Added oracle_diagnostic.py only; normal model/generator/training files unchanged.
- Five focused tests passed: P/B2 normal-output equality, frozen state, weighted token-gradient reconstruction, inner-gradient independence from diagnostic labels/IDs, and double-precision first-order finite differences.
- Next: checkpoint reader, paired raw records, distributions and summary tables.

## 2026-09-12 03:08:27 +08:00 — Runner increment
- Seven focused diagnostic tests passed, including tiny source reader/paired aggregate fixture and source hash preservation.
- Main oracle labels/IDs restricted to explicitly named analysis files; runtime code unchanged.
- D1-D4 raw records and per-seed/pooled distributions implemented. Next full regression, then A6000 fixed diagnostic.

## 2026-09-12 03:09:01 +08:00 — Full local regression
- Expanded diagnostic suite: 7 passed in 11.12s.
- Final full suite: 30 tests passed. No normal model, generator, or training file changed.
- Ready to commit analysis and run fixed D1-D4 against original checkpoints.
