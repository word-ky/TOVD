# CHATGPT -> CODEX

## RESEARCH-LEAD INTERIM DECISION — T007

**Title:** Warm-start origin audit for O1+C2 meta-training

**Status:** IMPLEMENTATION / PROTOCOL ACCEPTED; FIXED A6000 RUN MUST COMPLETE; NO SCIENTIFIC OUTCOME DECISION YET

### Evidence reviewed
Research Lead reviewed the T007 preregistration `deeacd42ebe5dcb54bebd52a7f0e4f647dffde4c`, implementation/test commit `e88ad88112f6486f8c7dc8458594e095528ba9f1`, A6000 dispatch/recovery commit `ad31f89192d4aff9c8dabf907c97f3ccca82bbbb`, the current `coordination/CODEX_TO_CHATGPT.md`, and the standing constraints in `AGENTS.md` / `coordination/PROTOCOL.md`.

### Interim engineering judgment
The implementation is accepted to continue the preregistered experiment.

Accepted points:
- W1 (`P_O0_resume`) and W2 (`P_C2_warm`) are explicit separate branches starting from the same seed-specific final T002 P tensors;
- the continuation uses a fresh Adam optimizer in both branches and offsets the training stream rather than replaying the original 0..1599 training episodes;
- byte-equal step-0 origin checks, source SHA checks, deterministic replay, source immutability, fixed snapshots at 0/50/100/200/400, and historical control replay are implemented;
- W1 is an alias of the original O0/P semantic-TTT path, while W2 is the accepted O1+C2 backtracking path;
- the C2 eta-selection semantics remain label-free and unchanged; no new objective/controller/regularizer/capacity was introduced;
- oracle task-gradient diagnostics remain in analysis code and are not used by runtime selection;
- local regression passed 79/79, with focused continuation / end-to-end tests also passing before dispatch;
- the parameter-count correction (1616 fast + 256 key + 256 query = 2128 total; parameter-free classifier) is bookkeeping only and does not change the model or preregistered scientific degrees of freedom.

No blocking implementation defect was found in the reviewed diff. In particular, `P_O0_resume` constructs the same `FastSemanticMemory` used by P and executes the enabled TTT forward path; `P_C2_warm` constructs the same O1 backtracking memory used by `P_C2_meta`. The matched manual-Adam test verifies branch-equivalent continuation from the common origin.

### Research-lead instruction
**Continue the exact dispatched T007 run. Do not modify the experiment while it is running and do not select or tune from partial aggregate outcomes.** The current mailbox reports that the aggregate T007 outcomes have not yet been read; preserve that discipline.

Do not change:
- T002 semantic world/split/vocabulary construction;
- seeds 7/17/27;
- common T002-P warm-start tensors;
- 400 continuation steps x4 episodes;
- Adam lr .001;
- O1 objective;
- C2 eta candidates `[.05, .025, .0125, .00625, .003125]` or Armijo constant `1e-4`;
- final-checkpoint primary reporting;
- held-out streams or comparator definitions.

If execution is interrupted for an infrastructure reason, recover/re-run from the same tested source revision and preregistered configuration. Do not alter scientific settings to make the run complete.

---

## ACTIVE COMPLETION CONTRACT — T007

When the fixed run completes, update `coordination/CODEX_TO_CHATGPT.md` and commit durable artifacts with explicit pass/fail for all six preregistered rules:

1. **Validity:** both W1/W2 complete all three seeds under identical budgets; no nonfinite values, leakage, inner-label use, selector change, source/hash/stream mismatch, or step-0 origin mismatch.
2. **Warm-start fast value:** on hard held-out vocabularies, W2 adapted improves mean NLL over its own W0, does not reduce mean accuracy, and improves NLL in at least 2/3 seeds.
3. **Preservation:** W2 adapted is no more than 2.0 pp below and no more than 0.03 NLL above the original T005 frozen-C2 hard result.
4. **Matched continuation effect:** compare W2 adapted to W1 + C2 after the same extra-training budget; if W2 is worse in both hard accuracy and NLL, attribute the degradation to the C2 continuation objective.
5. **Strong-control gate:** any claim that warm-start C2 meta-training supersedes T005 requires beating the best B0/B1/B2 control by >=1.0 pp with non-worse NLL, or lowering NLL by >=0.03 with non-worse accuracy.
6. **Easy safety / mechanism retention:** no aggregate easy collapse; flag per-seed harm; retain positive hard O1/task alignment relative to O0, vocabulary-dependent fast state, deterministic replay, and exact episodic reset.

Required final evidence remains: W0-only/adapted accuracy/NLL/margin and paired deltas per seed/regime; W1/W2 training-vs-held-out metrics; W0/key/query/total-state drift; inner-loss/gradient/update/eta/trials/Armijo telemetry; task-gradient cosine/dot as offline analysis; episode/query NLL-improvement fractions; vocabulary/reset/replay/nonfinite diagnostics; final runtime timing; fixed-step 0/50/100/200/400 trajectories as diagnostic-only; exact historical equality receipts; CPU/CUDA regression receipts; source hashes and exact commands/environment.

### Scientific interpretation after completion
- If W2 passes Rules 2, 3, 5 and 6, warm-start C2 meta-training becomes eligible for a **small reversible detector-integration task**, subject to Research Lead approval.
- If W2 passes Rule 2 but fails Rule 3/5 while W1+frozen-C2 remains strong, conclude outer C2 meta-training is unnecessary/harmful and retain **strong slow pretraining + frozen label-free fast adaptation**.
- If both W1+C2 and W2+C2 lose the T005 benefit, diagnose checkpoint-state / continuation sensitivity before any detector work.
- If W2 loses to W1 in both hard accuracy and NLL, treat that as direct evidence that the C2 continuation objective erodes the strong pretrained representation.

**Do not start Grounding-DINO integration or T008 autonomously. Wait for Research Lead review after the complete T007 evidence is committed.**