# T011 progress

- 2026-09-12 13:24+08: Preregistration b615642a3b23261dfaed6ebbdb61b423be7f3901. No scientific outcomes.
- Module3tests passed5.15s; runner6tests passed6.72s. Local full101passed19.16s.
- Tested implementation79e6e2baac5b92dd8b66c1a8a048a4d5013f5d5b, dispatchcd1c1aa.
- Release20260912-133111-tovd-t011; run20260912-133149-tovd-t011-a6000, started13:31:58+08 onGPU1.
- Remote fullCPU101passed9.71s; CUDA101passed25.66s before scientific stream. Existing NVML/protobufwarnings unchanged; PyTorch CUDA works.
- 13:35+08: four of nine checkpoint states completed (800episodes); run active. All model/scientific code frozen; only pure report renderer and recoverynotes added after dispatch.
- Report generator parses completed raw artifacts and original fixed gate outputs; it never imports model/Torch or executes adaptation.
- All outcomes to be retained and reported. Current task completes only after all1,800episodes, validity check, raw retrieval, report, commit/push and remote mirror.

## 2026-09-12 13:38 +08 T011 screen finished; recovery in progress
Run20260912-133149-tovd-t011-a6000 exit0 at13:37:55+08. All1800episodes/14400queries complete, validityTrue. Five scientific criteria allFAIL. OverallS0/S1/S2/S3 NLL .9079148837/.8539555307/2.4197990865/2.3612078392; accuracy59.7916667/63.1180556/29.8263889/27.3402778percent. ResidualdiversityS2 .4102165641 vsS3 .4302423724. S2accepted14397/14400, finite/nonzero/reset/vocabularychecks pass but utility fails. No repair/tuning.
Downloading34MB losslessfullrunarchive; remoteSHA2565567735c5f387ab5ffed8bbfa33280b3a80a9b4522b28d86bf8324886bc10bc9. Finalverification/report/commit pending retrieval. A read-only remote Python summary command had shell-quoting SyntaxError; cat of immutablegates/summary succeeded, scientificrun unaffected.

## 2026-09-12 13:46 +08 T011 final evidence
All27runfiles/18rawrecords recovered; archiveSHA5567735c5f387ab5ffed8bbfa33280b3a80a9b4522b28d86bf8324886bc10bc9 matches. Raw1800episodes/14400queries and aggregateNLL checked. Fullreport/tables/diagramPNG/SVG generated and plot visuallychecked. All5scientificcriteriaFAIL; engineeringvalidityTRUE,101tests eachlocal/CPU/CUDA. Stoprule enforced; no furthermethodchanges. Preparing final commit/push and mirroring projectrecovery/reports toA6000.
