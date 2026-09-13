# T013-OPS8 PASS — bounded reclamation and observation complete

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

Completed window20:42:13–21:35:10+08,3177s=52min57s. Four scalar snapshots:
one pre,one immediate post,and exactly two later points. Spacings57s,1139s
(18min59s),1981s(33min01s). The21:18 intermediate heartbeat was mailbox-only
to keep the two-later-point limit and reserve final observation for45–60min.
No tighter polling or extra sampler. All post-reclamation observations SAFE
and exact-bound PRIMARY_RUNNING. No test reruns; scalar evidence only.

| Point | Time+08 | Images | Free bytes | Remaining | Projected bytes | Required bytes | Margin bytes | Storage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pre | 20:42:13 | 840/1000 | 11234455552 | 160 | 2616852480 | 11730157568 | -495702016 | STORAGE_RISK_RETURN_TO_LEAD |
| Immediate post | 20:43:10 | 841/1000 | 12291137536 | 159 | 2600497152 | 11710531175 | 580606361 | SAFE |
| Later1 | 21:02:09 | 852/1000 | 12067106816 | 148 | 2420588544 | 11494640845 | 572465971 | SAFE |
| Final later2 | 21:35:10 | 871/1000 | 11730296832 | 129 | 2109837312 | 11121739367 | 608557465 | SAFE |

At every point writer721181 Rl+, exact tmux alive, wrapper marker absent,
analysis/results.json absent(existenceonly), process PRIMARY_RUNNING. Later
progress seconds86260.61986363702 and88191.77212120598. Exact same accepted
OPS3/OPS2 helpers, no new rule. The observed safe state is operational only;
it is not a guarantee about future storage or a scientific acceptance.

One earlier receipt-upload connection closed; existing legacy SCP retry
succeeded(exit0), recorded in receipt. No operational event on final snapshot.
Stop after OPS8 and await Lead review. No additional cleanup is authorized.

Files: research_log/t013/ops8_pre_raw.json,ops8_pre_snapshot.json,
ops8_post_raw.json,ops8_post_snapshot.json,ops8_reclamation_receipt.json,
OPS8_RECLAMATION_REPORT.md,ops8_later1_raw.json,ops8_later1_snapshot.json,
ops8_later2_raw.json,ops8_later2_snapshot.json; delivery updates engineering mailbox and project
research_log/project_state.md,REMOTE.md,session_log.md. Small copies mirrored
under remote project root, never the running release.

No archive hash,du,recursive scan,broad search,nonallowlisted deletion,active
prediction/scientific content,FIN1/replay,kill/restart/resume,runner/frozen
scientific-source change,YOLO/T014,driverrepair or install. No new threshold,
forecast,depletion-rate or time-to-failure rule. Existing primary continues
unchanged; future GPU preference retained. Scientific results remain unopened.
