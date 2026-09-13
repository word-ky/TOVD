# T013-OPS3 — operational incident snapshot

Engineering PASS, awaiting Lead review. Task-start HEAD is
`65b1075be239e0fb8caaf451a9769e4a48aec040`, which accepts OPS2 and assigns OPS3.
No change to the primary run, scientific protocol or monitoring cadence.

`primary_incident_snapshot.canonical_snapshot(raw)` is a deterministic pure
function. It imports and calls the accepted OPS2 `health_guard`; it contains no
storage formula or filesystem/process calls. OPS2 source matches evidence
`e380d14e5ee7b830781d38cc9efae292509ca66a` after Git line-ending normalization;
both hashes are recorded. Inputs are copied into an explicit output schema and
are not mutated. Missing/malformed evidence raises ValueError, with no snapshot
or SAFE status fabricated.

The `T013-OPS3-v1` schema contains:

- exact repository/root/run/release/freeze/dispatch/PID/tmux/OPS2-evidence bindings;
- timezone-bearing timestamp, caller's current Git HEAD and raw-source references
  for each required metadata family;
- parsed progress count/total/elapsed seconds, writer existence/state, and the
  OPS2 process/storage report (including raw marker-derived exit code);
- analysis-result existence boolean only;
- explicit scope attestation and false scientific-access, FIN1-execution and
  remediation authorization flags.

Source references and attestations document the collection; they do not replace
actual collection evidence or provide cryptographic authentication. Dispatch is
the fixed committed provenance reference; run/release/session and freeze argument
are read from operational meta.json, with resolved_release.txt agreement.
Git HEAD means the local caller's checked-out repository at collection time;
the immutable remote release is separately identified.

Raw input requires explicit empty wrapper marker list when no marker exists,
ps exit0/output for a present writer or exit1/empty output when absent, tmux
exit0/1, and the C-locale `df -B1 --output=avail` output. Invalid PID substitution,
query exit codes, progress count/free bytes, bindings and missing references are
rejected. Zombie/dead writer state is preserved as PID-existing but not alive,
so OPS2 reports process ambiguity unless completion/failure evidence resolves it.

Top-level snapshot status preserves any OPS2 return-to-Lead state. Successful
wrapper exit0 with writer/tmux gone is explicitly PRIMARY_COMPLETE_UNVERIFIED,
even though OPS2's separate top-level status may describe storage. All states,
including completion, keep scientific access/FIN1/remediation unauthorized.
Early analysis-file existence changes only the existence boolean.

`collect_primary_incident_metadata.py` is a separate one-shot collector. It
reads only operational meta.json and resolved_release.txt, runs date/ps/tmux,
filters train.log for anchored progress and wrapper-exit lines, queries df and
checks analysis-file existence. It hashes only the already-read 1,043-byte
operational meta.json. It writes nothing remotely and prints one raw JSON record.
No directory walk, prediction/cache read, analysis parse, evaluation or repair
command exists in the collector. Query errors fail instead of inventing absence.

Validation command from the repository root:

```powershell
D:/anaconda3/python.exe -m unittest discover -s research_log/t013 -p test_primary_incident_snapshot.py -v
```

Four tests / 55 fixtures PASS in 0.002s: seven required state/determinism cases
(healthy, storage risk, wrapper failure, ambiguity, completion-unverified,
early analysis existence, zombie writer), nine binding rejections, 20 missing
metadata/reference cases, and 19 malformed metadata cases. All state cases also
assert no input mutation and no scientific/FIN1/remediation authorization.
The committed 499-image health line was then replayed successfully, with the
exact source line and canonical result retained in the receipt.

After those rehearsals, exactly one live collection was executed through the
existing project SSH workflow, using the existing Python environment:

```bash
LC_ALL=C /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python /home/wenchang/asdasdsad/wjq/TOVD/research_log/t013/collect_primary_incident_metadata.py 65b1075be239e0fb8caaf451a9769e4a48aec040
```

Stdout was saved locally as `primary_incident_snapshot_live_raw.json`, then
parsed locally with `canonical_snapshot`; both raw SHA256 and canonical result
are in `primary_incident_snapshot_receipt.json`. At 2026-09-13T11:33:01+08:00:
512/1000 images, elapsed 52080.396239708s, writer721181 Rl+ and tmux alive,
no wrapper marker, analysis result absent. Free20,627,927,040 bytes;
remaining488; projected7,981,400,064; required18,167,614,669;
margin2,460,312,371; SAFE / PRIMARY_RUNNING.

The live operational meta.json SHA256 e703a63618a4be6db265f85fb9c5bd3d6704f0f150fe1f965b2e9d8ab9886575
equals the retained local original's raw bytes. Its LF-normalized SHA256 is
e9c8bd67854a9c1ee9d1a5b2f1470495cf4c616822102b226644b6fdf09dd6b0,
explaining the Git-blob representation without any file change.

No primary scientific/prediction content opened, active cache recursively
scanned/modified, frozen science/run/environment changed, or
cleanup/restart/resume/YOLO/T014 action occurred. Helpers and receipts are stored
in the project log, outside immutable release/run directories.

Stop OPS3 after delivery. The existing 15-minute health cadence continues;
this collector adds no scheduler or polling loop. An incident or
PRIMARY_COMPLETE_UNVERIFIED means preserve the raw snapshot and return to Lead.
OPS3 does not advance FIN1; the latest mailbox requires later Lead review to
advance the established CLOSE1 sequence.
