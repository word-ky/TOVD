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

## 2026-09-12 03:09:53 +08:00 — A6000 diagnostic launched
- Tested analysis SHA 6780de5ae44dcc89b9f1c45ea781f33dc16ffbaf; final local regression 30 passed in 11.95s.
- Release 20260912-030919-tovd-t003; run 20260912-030923-tovd-t003-a6000.
- Original T002 source remains /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-023122-tovd-t002-a6000/artifacts/t002.
- No outer training; run starts with full CPU/CUDA tests, then six original checkpoint diagnostics. Do not launch a duplicate.

## 2026-09-12 03:16:27 +08:00 — T003 complete
- A6000 CPU 30 passed in 3.17s; CUDA 30 passed in 5.52s. Two existing protobuf deprecation warnings per suite.
- Run exited 0 at 03:10:33 +08:00; all 1200 paired episodes processed; no active session remains.
- Normal predictions and original T002 per-episode metrics match exactly; source checkpoint hashes match local originals. Weighted subset reconstruction max error 2.3841858e-7.
- Fetched all raw records (14.57 MB). D1-D4 tables and interpretation support branch C primarily, limited easy-regime A; B not primary and D unsupported.
- Full report, source pairing receipt and artifact manifest prepared; no T004 implementation or primary retraining.
