# T012 preregistration: static activation-side reduction audit

2026-09-12, Research Lead d2738a7 / bb4d451. T011 accepted as a valid negative; the fast-semantic-state program is terminated. This task tests a static prediction-distribution fusion. No T012 calibration or novel outcomes have been generated/read.

## Sources, data and phases

Use the same nine checkpoint files and exact SHA256 values listed in sources.json: original T002 P, T007 W1/W2 step400 for seeds7/17/27. All local hashes verified. Freeze existing world, generator, model and classification temperature; config.json records the complete constants. No outer training/checkpoint selection.

Calibration: fresh base/train semantics, 100 easy +100 hard episodes per checkpoint, 1,800 episodes /14,400 queries. Episode seed=4,000,000,000 +seed*100,000 +(10,000 if hard else0)+index, index0..99.

Novel evaluation: fresh test semantics, same counts (1,800/14,400), namespace5,000,000,000 with the same offsets. Each phase has600 unique scene seeds paired across three states. Both namespaces are disjoint from T002–T011 and each other; all explicit IDs in sources.json. Novel generation/scoring starts only after the actual selected lambda and full calibration receipt are committed and pushed. Unit/integration fixtures use random models rather than scientific source checkpoints.

## Formula and one global lambda selection

Reuse the pure T011 local_teacher function without changing it: normalized k=P_k(X), q=P_q(Q), t=T (F.normalize eps1e-12); pi=softmax(k@t.T/0.2); a=softmax(q@k.T/0.2); pi_bar=a@pi. Uniform pi_bar uses a=1/N. W0 tokens are z0=F_W0(P_q(Q)); p0=softmax(existing classifier logits(z0,T)).

Static fused log probabilities are log_softmax(log(p0+1e-12)+lambda*log(pi_bar+1e-12)). This implements the requested probability-level product of experts literally, including epsilon for lambda0; no hidden identity shortcut or logit blending. Float32 model/evidence/fusion follows the established computation. Stable log probabilities supply offline NLL.

Fix lambda grid [0,0.05,0.1,0.2,0.5,1,2]. Select ONCE by minimum mean base-calibration query NLL over ALL seeds/states/easy+hard equally weighted. Absolute NLL ties within1e-12 choose the smallest lambda. No accuracy constraint, LOSO, state/regime-specific value, validation feedback or retuning. Lambda0 is a legitimate null selection. Commit selected value, all candidate base scores, source/code hashes and receipts before any novel evaluation.

To distinguish literal strict improvements from numerical roundoff, evaluate the strict NLL-improvement comparisons in Gates1/2/4 with a preregistered 1e-6-nat numerical tolerance (gain must exceed1e-6); all stated safety thresholds .03/.02/.01 and 1pp remain unchanged. This addresses scoring discrepancies up to1.1027e-6 already measured in T011 and prevents an epsilon/normalization-only effect at lambda0 from being interpreted as utility. Report signed deltas regardless of this convention.

## Controls and inference boundary

- A0: exact W0 prediction on each source state.
- A1: existing B1 activation formula, using EpisodicClassifier('B1') loaded with the SAME frozen source tensors. Technically meaningful because its projections/MLP state keys/shapes exactly match. Replay its existing code unmodified. This is a matched-state B1 formula control, not the separately trained historical B1 checkpoint/score.
- A2: query-local static product of experts with the frozen global lambda.
- A3: uniform-context product of experts with the SAME lambda.
- A4: unchanged global O1+C2 solely as the specifically required historical diagnostic, never a successor candidate.

A0/A1/A2/A3 run under torch.inference_mode. A2/A3 allocate no parameter copies, residual variables, optimizer or persistent/test-time state; they use only forward tensors and a fixed scalar. Static runtime signatures contain no labels/IDs. The explicitly required A4 is run separately under the existing no_grad/inner-enable-grad C2 path; its inner gradient is confined to that historical reference and cannot enter A2/A3. The task's no-adaptation prohibition is applied to the proposed static inference path, preserving its explicit A4 control requirement.

Calibration only requires A0/evidence plus A2's fixed grid; no C2 call is needed in calibration. All five controls are evaluated on identical novel scenes. Labels enter only after feed-forward outputs and diagnostics are complete. Calibration labels are used solely in offline selection of the global constant; novel labels are evaluation only.

## Diagnostics and fixed gates

Retain per-query p0, local/uniform teacher, image-token teacher, attention, all control probabilities/log probabilities, offline NLL/accuracy, attention entropy/effective token count, teacher/query diversity, A2-vs-A3 probability difference/KL and class changes. Record global lambda, all phase/state/episode IDs, source/code hashes, exact A0/A1/A4 replay and model tensor byte equality; finite checks. Verify no autograd.grad/backward can be invoked on A2/A3, no model tensor .grad is produced, deterministic replay, query independence and label/ID independence in unit tests. Retain full per-state/seed/regime tables and source records.

All five criteria must hold:

1. Hard utility: in EACH original/W1/W2 group A2 hard NLL improves over A0 (gain>1e-6), and accuracy>=A0-0.01.
2. Cross-seed: in EACH group at least2/3 seeds improve hard NLL (gain>1e-6); no seed NLL regression>.03.
3. Easy safety: in EACH aggregate easy group A2 NLL<=A0+.02 AND accuracy>=A0-.01.
4. Localization: pooled hard A2 NLL<A3 by>1e-6; pooled easy A2 NLL<=A3+.01.
5. No hidden adaptation: all slow/model tensors byte-identical, no labels/IDs/novel outcomes or learned runtime gate in A2/A3; no runtime gradient/optimizer/state in the static path; actual calibration lambda frozen before novel generation and reused exactly.

Numerical validity and complete source/replay checks are reported separately. All criteria fixed before outcomes. If all pass, stop and recommend a separate static/activation-side detector integration DESIGN for Research Lead review, without integrating now. If any fails, stop the synthetic TOVD mechanism program entirely and provide a synthesis of the existing evidence; do not invent another synthetic mechanism. This is not a TTT rescue.

## Baseline reuse and bounded implementation

Baseline d2738a7: `python -m pytest -q tests/test_query_local_residual.py tests/test_step_control.py` =>17passed9.02s. Reuse checkpoint loader, SemanticWorld, exact B1/C2 paths, pure local_teacher and existing JSON/CSV helpers. No external donor code or framework introduced.

Increment1: new modular static evidence/PoE functions and tests for formula, forward-only operation, query isolation, reset, no parameter mutation and exact W0/B1 behavior. Run focused tests before increment2.

Increment2: task-local two-phase runner, lambda calibration, fixed gate summary; random-checkpoint end-to-end and gate/label-boundary tests. Full local regression before deploy.

Increment3: commit exact tested implementation/hash manifest; A6000 GPU1 runs fullCPU and CUDA regressions BEFORE base calibration. Fetch and commit actual lambda and complete calibration receipt. Deploy unchanged tested core plus frozen lambda, then run novel phase. Archive and hash all receipts, generate report/synthesis if negative, update engineering mailbox and stop for review.
