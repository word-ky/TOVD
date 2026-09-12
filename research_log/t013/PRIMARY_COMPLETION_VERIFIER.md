# T013-FIN1 — PASS / completion verifier prepared

**13/13 tests PASS in193.507s:** full 15,000-cell positive/repeat fixture and 23 negative fixture outcomes all behave as required. Completed engineering smoke PASS45/45 opaque files. No primary scientific acceptance is implied.

Assignment: Research Lead `e22ee9b`. This checker is independent of the frozen writer and uses only standard-library JSON, paths, file sizes and streaming SHA256. It does not import NumPy, PyTorch, a detector or a scientific evaluator. Requires **Python 3.11+** (`hashlib.file_digest`); use the already-existing project Python 3.12 environment on the server.

## Frozen contract and checks

The trust anchor is the exact `native30_freeze.json` Git-blob SHA256 `50addfb8e247333b49fb22cda14570166b294101bb435b5a1b5bf688b4b3a91e` from `6fec32243985ccc808123d851abf5f3dea10af99`. Its pinned hashes bind the selection, vocabulary, image hash manifest and native runner/detector sources. The five condition names are read as a literal AST value from the pinned `scripts/t013_detector.py`; no scientific source is executed. Source/metadata CRLF is normalized to canonical Git LF for Windows checkouts; raw prediction bytes are never normalized.

Expected primary keys are reconstructed from the exact ordered 1,000 IDs, five conditions and three vocabulary names: **15,000 unique keys**. The verifier checks:

- Exact run ID and release ID against run metadata and resolved-release receipt.
- Completed final receipt: kind `T013-NATIVE30-primary`, exact freeze commit, ordered IDs, vocabulary/selection hashes, CPU/four threads, completed/weights-unchanged/code-input-verification flags true, and both model states equal the frozen expected hash.
- Manifest and final receipt each contain the full expected key set once; paths match `raw/<condition>/<vocabulary>/<12-digit image>.npz` exactly and are unique. All record metadata must agree between manifest and final receipt, including key hashes.
- Every raw file exists, is nonempty and has the recorded SHA256, computed over opaque bytes.
- Every source-image hash matches the frozen hash manifest for that image, thereby matching across all 15 records.
- Exactly three vocabulary records per image/condition, with identical pixel hashes; 5,000 such groups for primary.
- Analysis-result path existence only. No AP/CI/gate file contents are read, and integrity PASS does not depend on their values or constitute scientific acceptance.

All required fields are supported by the frozen schema; no writer/schema changes were needed. Full source bindings are included in machine-readable test/smoke receipts.

## Synthetic tests

Run from the Windows project root:

```powershell
python research_log/t013/test_primary_completion_verifier.py
```

The test creates a full 15,000-cell fixture under a project-local temporary directory, using frozen IDs and metadata but deliberately invalid NPZ-format byte strings. Successful verification therefore does not require prediction deserialization. It compares repeated verifier results exactly and introduces an invalid analysis JSON file to show that only existence is inspected. All generated fixture bytes are reproducible from the committed test source; the temporary fixture directory is removed by that test, while test results and receipts remain in `research_log/t013`.

Negative cases cover missing cell, duplicate key, extra key, incorrect/reused path, raw tampering, missing/empty file, wrong image hash, cross-vocabulary pixel mismatch, wrong freeze commit, changed or identically wrong model state, `completed=False`, omitted final record, receipt/manifest hash disagreement, reversed ID order and all other required final receipt flags/hashes/device/thread bindings. Each must fail for its expected named check.

The execution result and individual outcomes are recorded in `primary_completion_tests.txt` and `primary_completion_test_receipt.json`.

## Existing smoke rehearsal

No local raw copy was available; the original completed remote cache was readily available and was checked in place. **PASS: 45 unique manifest/final records, 45 opaque files / 48,715,584 bytes, 15 shared-pixel groups.** State-before/state-after both equal `de1683cc0a3c35157ed5475169dae013cdaffe69f45651d6e3f5550ae96139e1`. Analysis result exists; its contents were not opened.

Explicit smoke mode pins run `20260912-205428-tovd-native30-pipeline-smoke`, release `20260912-205335-tovd-native30-pipeline`, IDs `[139,285,632]`, kind `smoke_cached_pipeline`, original freeze argument `d5dc807`, and `code_vocab_selection_images_verified=False`, exactly as emitted by the frozen smoke branch. These smoke-only facts do not relax the primary contract. Vocabulary, selection, source-image hashes, state immutability, record equality and byte hashes are still checked against the final frozen artifacts.

Exact successful remote command (via the existing AutoDL workflow SSH helper):

```bash
/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/fin1/primary_completion_verifier.py --frozen-root /home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-210306-tovd-native30-primary-freeze --cache /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-205428-tovd-native30-pipeline-smoke/artifacts/cache --smoke --output /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/fin1/primary_completion_smoke_receipt.json
```

Exit0, receipt copied back as `primary_completion_smoke_receipt.json`; no raw files copied, installs or inference. Initial invocation using system `python3` failed with `AttributeError: module 'hashlib' has no attribute 'file_digest'` at line24. The same unchanged script passed with the existing project Python3.12.12 interpreter. This was an interpreter error, not an integrity/schema discrepancy; no compatibility code or environment changes were introduced.

## Completion handoff — not executed against primary in FIN1

Continue health-only checks while the primary writer is active. After its completion, the prepared command is:

```bash
/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/fin1/primary_completion_verifier.py --frozen-root /home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-210306-tovd-native30-primary-freeze --cache /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/artifacts/cache --output /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/fin1/primary_completion_receipt.json
```

This command is a rehearsal instruction only; it has **not** been run on the active primary cache. A failure reports the named check and preserves the existing cache for Lead review; it does not restart, repair, move or delete anything. After integrity PASS and complete frozen analysis, follow the existing Lead completion/reproduction/reporting contract. Scientific interpretation remains outside FIN1.

No active primary cache or scientific artifact was opened. No frozen source, plan, vocabulary, IDs, seeds, thresholds, gates or active process was changed. No YOLO work occurred. Stop FIN1 after evidence delivery and wait for Research Lead review.

End health **2026-09-13T04:27:45+08:00**: exact primary tmux alive; writer721181 `Rl+`; **258/1000** at26526.936807298014s; available bytes **25,408,024,576**. No wrapper exit marker, no primary analysis result (path existence only). The bundle receipt `primary_completion_verifier_receipt.json` binds execution commands, tests, smoke, failures, artifact hashes and this health observation.
