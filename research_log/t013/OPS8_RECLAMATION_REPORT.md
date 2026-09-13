# T013-OPS8 IN_PROGRESS — allowlisted reclamation complete, follow-up pending

Task-start7aa87119566b5acfb799fac9244745cfdc7fe9ce; Lead6101219 (full SHA in receipt).
OPS2 e380d14e5ee7b830781d38cc9efae292509ca66a and OPS3
6ecbc36bd66eb2e4ca6057f9a33c81863ed7eff7 reused unchanged; local source matched
accepted Git content after line-ending normalization. No helper changes/tests.

Pre20:42:13+08:840/1000 at85033.70864075999s,free11234455552,
remaining160,projected2616852480,required11730157568,margin-495702016,
STORAGE_RISK_RETURN_TO_LEAD/PRIMARY_RUNNING.

Metadata preconditions PASS before deletion. Both exact paths resolved to
same allowlisted paths and stat reported regular files: val2017.parallel.zip
815585330bytes; annotations_trainval2017.parallel.zip252907541bytes.
The frozen data_receipt.json at6fec32243985ccc808123d851abf5f3dea10af99
matches these exact sizes and archived SHA256/CRC provenance. No re-hash.
Extracted val2017/ exists; exact annotations/instances_val2017.json is regular,
19987840bytes. Frozen running-release data_receipt.json1064bytes and
image_sha256.json450003bytes exist; committed local receipts exist.
Only /proc/721181/fd links inspected: neither archive is open. Exact returned
FD targets preserved in ops8_reclamation_receipt.json. No filesystem scan.

Exact authorized deletion (successful conditional marker observed):
```bash
rm -- /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco/val2017.parallel.zip /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco/annotations_trainval2017.parallel.zip
```
Validated source-file bytes reclaimed1068492871. This is the sum of the two
validated stat sizes; it is not inferred from df changes while other writes run.
No deletion outside these two paths. This deletion is not a change to frozen
scientific inputs: extracted JPEGs/annotation JSON, receipts and source remain.

Immediate post20:43:10+08:841/1000 at85126.45402577001s,
free12291137536,remaining159,projected2600497152,required11710531175,
margin580606361,SAFE/PRIMARY_RUNNING. Both pre/post exact writer721181 Rl+
and exact tmux alive,wrapperexitabsent,analysis/results.json absent(existenceonly).
Accepted canonical_snapshot(raw) used for both; exact run/release/freeze/
dispatch, source commits, raw metadata and commands retained in receipts.

INCOMPLETE follow-up: start20:42:13+08. Existing heartbeat only; first later
scalar point around21:00+08, reserve second/final for21:27–21:42+08 to finish
45–60min window with at most two later points. An intermediate heartbeat before
that final window checks mailbox only after first later point is recorded.
No new scheduler or tighter polling. On existing risk/process/completion state,
stop immediately and return accepted OPS3 evidence to Lead. No second cleanup.

Files: research_log/t013/ops8_pre_raw.json,ops8_pre_snapshot.json,
ops8_post_raw.json,ops8_post_snapshot.json,ops8_reclamation_receipt.json,
OPS8_RECLAMATION_REPORT.md; delivery updates engineering mailbox and project
research_log/project_state.md,REMOTE.md,session_log.md. Small copies mirrored
under remote project root, never the running release.

No archive hash,du,recursive scan,broad search,nonallowlisted deletion,active
prediction/scientific content,FIN1/replay,kill/restart/resume,runner/frozen
scientific-source change,YOLO/T014,driverrepair or install. No new threshold,
forecast,depletion-rate or time-to-failure rule. Existing primary continues
unchanged; future GPU preference retained. Scientific results remain unopened.


## T013-OPS8 IN_PROGRESS — later point1/2 (2026-09-13T21:02:09+08:00)
GitHub synchronized81feb1f; project handoffs and AGENTS/protocol/mailbox/spec read, no newLead instruction. Two allowlisted ZIPs already deleted inb738711; no repeated deletion or precondition scan. Existing ordinary heartbeat collected later point1,1139s after immediatepost,1196s afterpre. Exact primary20260912-210355-tovd-native30-primary,writer721181 Rl+/tmuxalive,852/1000 at86260.61986363702s,wrapperexitabsent,analysis/results.json absent(existenceonly),free12067106816,remaining148,projected2420588544,required11494640845,margin572465971,SAFE/PRIMARY_RUNNING. Accepted unchanged OPS3 canonical_snapshot/OPS2 used; raw/snapshot storedops8_later1_*.json and appendedops8_reclamation_receipt.json. OPS8 NOT COMPLETE. Reserve second/final scalar point for21:27:13–21:42:13+08 (45–60min from20:42:13); intermediate heartbeat before21:27:13 only syncs mailbox, no extra remote point. No new scheduler/threshold/forecast/cleanup or science. No archivehash/du/scans/nonallowlisteddeletion/runmutation/FIN1/replay/kill/restart/resume/driverrepair/YOLO/T014. On established risk/process/completion state immediately stop viaOPS3 and returnLead. Otherwise final report afterwindow. FrozenCPUprimary unchanged;futureGPUpreference retained.
