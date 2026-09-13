# T013-CLOSE2: PROCESS_STATE_AMBIGUOUS_RETURN_TO_LEAD

Immediate stop on accepted OPS2 process incident at point3. CLOSE2 is not reported as PASS or primary completion. Exact primary count1000/1000 does not establish completion: exact writer721181 is absent, but exact tmux remains present and no successful wrapper exit marker exists. CLOSE1 successful completion prerequisites are not satisfied; its semantic state remains PRIMARY_RUNNING. PRIMARY_COMPLETE_UNVERIFIED is not established.

Task-start 53dcd036cbf8c72df08d9faaa57c015e4282015d; Lead instruction 0155bde95cff9831d44cfa151235623a773867a9. Run20260912-210355-tovd-native30-primary; release20260912-210306-tovd-native30-primary-freeze; freeze6fec32243985ccc808123d851abf5f3dea10af99; dispatch88668f76b22777459b5792dd28f88075f208c678. Exact tmux autodl-20260912-210355-tovd-native30-primary.

Three ordinary points over2006s (33min26s), spacings1019/987s (16min59s/16min27s); stopped early as required, no fourth point or second hour.

| Time+08 | Images | Seconds | Writer | Tmux rc | Free bytes | Remaining | Projected | Required | Margin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 00:47:10 | 984 | 99725.94160745101 | Rl+ | 0 | 184319975424 | 16 | 261685248 | 8903956890 | 175416018534 |
| 01:04:09 | 994 | 100774.95009569102 | Rl+ | 0 | 184162205696 | 6 | 98131968 | 8707692954 | 175454512742 |
| 01:20:36 | 1000 | 101363.274547162 | None | 0 | 184061218816 | 0 | 0 | 8589934592 | 175471284224 |

At all points wrapper exit marker absent/code null, analysis/results.json absent by existence-only check, storage SAFE. Points1/2 writer721181 Rl+ (ps rc0), OPS2 process PRIMARY_RUNNING. Point3 exact `ps -p 721181 -o pid=,stat=` returned no row and WRITER_RC=1; exact tmux has-session returned TMUX_RC=0. OPS2 final process/overall status PROCESS_STATE_AMBIGUOUS_RETURN_TO_LEAD. No cause inferred or process hunt performed. No scientific content or completion inferred from image count.

Accepted source commits and Git-content SHA256 verified unchanged at task start/stop:

- primary_survival_guard.py: e380d14e5ee7b830781d38cc9efae292509ca66a; 8d58f01259387c4327cee0f1ac05e4dfef1dd3fd47a4c8b0f6542820202852c6.
- primary_incident_snapshot.py: 6ecbc36bd66eb2e4ca6057f9a33c81863ed7eff7; e2573a10683d5dbdf9eb43cd9a5c9d6e13a8966df616646cbbb8f03d8dcc3e82.
- finalization_barrier.py: 0acbd4f6417d2946f2009979ec8461df351eb07b; a227933e266090e1adab5395409ddf8ab037beb43c27f92b96713586d03d6c14.

Accepted canonical_snapshot(raw) invoked at each point, reusing OPS2 unchanged. CLOSE1 state semantics applied without full finalization evaluation or fabricated completed-cache hashes. No unchanged unit suites rerun; metadata snapshots and accepted evaluator outputs are operational evidence. No connection interruptions during observations. Previously unexplained free-space increase persists; no attribution/investigation.

Artifacts under research_log/t013: close2_terminal_capture_receipt.json, close2_point1_raw.json/close2_point1_snapshot.json through close2_point3_raw.json/close2_point3_snapshot.json, CLOSE2_TERMINAL_CAPTURE_REPORT.md. Receipt contains exact commands, raw-source descriptions and immutable bindings. Point1 evidencefd6ace7, point2 evidencea8f872914e8ba81720a3241cb420f9149ac06063; final incident evidence SHA recorded in subsequent mailbox delivery. Delivery updates coordination/CODEX_TO_CHATGPT.md and research_log/project_state.md,REMOTE.md,session_log.md; necessary copies mirrored under remote project root outside running release.

No result/prediction/NPZ contents opened; no FIN1/completed-cache hashes/replay/comparison/metrics/gates/scientific/CF/MECH analysis. No cleanup/deletion/compression/movement/quota change, du/scan/find/writer hunt/cross-project inspection, kill/pause/restart/resume/duplicate writer/runner patch, newthreshold/warningband/trend/forecast, YOLO/T014, install/update/driverrepair, or frozen scientific code/config/vocabulary/IDs/seeds/gates/run mutation. Frozen CPU execution was not modified; futureGPUpreference retained.

Return to Research Lead with exact process ambiguity. No remediation or further CLOSE2 observation is authorized; existing heartbeat checks mailbox for a new instruction. No claim that the whole run failed or succeeded can be made from these fields alone.
