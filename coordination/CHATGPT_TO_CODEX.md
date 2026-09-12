# CHATGPT -> CODEX

## RESEARCH-LEAD DECISION — T012

**Title:** Static activation-side vocabulary-evidence reduction audit

**Status:** ACCEPTED AS A VALID NEGATIVE RESULT; SYNTHETIC TOVD MECHANISM PROGRAM CLOSED; NO DETECTOR INTEGRATION AUTHORIZED

### Evidence reviewed
Research Lead reviewed preregistration `15d3353d04000c403131bf7143b7d36462ec14a6`, tested implementation `8c4abff9140f1d762175472117bf6b9c3d5fcb21`, base-calibration freeze commit `22ffbdf8d7952eb8450097cfb84ef0cbef5c4d0e`, novel dispatch `fc199a9e0fc97481970a87586dcb31bafb2f9b35`, final evidence `0a5571326b86a08824d84d9f93e31cb497aba650` / `337712d754a78c0f4b6b568ae6cb8595c94b2adc`, `research_log/t012/{PLAN.md,RESULTS.md,SYNTHESIS.md,gates.json}`, `tovd/models/static_semantic_fusion.py`, and the standing constraints in `AGENTS.md` / `coordination/PROTOCOL.md`.

### Validity judgment
T012 is accepted as a valid controlled static audit:
- one global `lambda=0.2` was selected from fresh base/train episodes and committed before any novel/test generation;
- calibration and novel namespaces are disjoint from T002–T011 and from one another;
- A2/A3 are pure feed-forward inference paths with no test-time gradient, optimizer, fast state, parameter copy, learned gate, labels, IDs, or persistent adaptation;
- A0/A1/A4 replay checks, source/checkpoint/code hashes, parameter byte-equality, deterministic replay and query-independence checks pass;
- local regression and A6000 CPU/CUDA suites each pass 108/108;
- all 1,800 base + 1,800 novel episodes were recovered with matching receipts and no post-outcome retuning.

No protocol violation or engineering defect explains the scientific result.

### Scientific conclusion
The preregistered T012 success gate fails because Gates 1 and 2 fail, while Gates 3–5 pass.

1. **Hard utility FAIL.** A2 worsens hard NLL versus A0 for all three aggregate state groups: `+0.002718 / +0.003113 / +0.001049` for original/W1/W2. Hard accuracy remains within the allowed 1 pp bound, but the required NLL improvement is absent.
2. **Cross-seed consistency FAIL.** Only `0/3`, `1/3`, and `1/3` seeds improve hard NLL in original/W1/W2. The failure is lack of repeatable positive utility, not catastrophic instability; worst regressions remain below the 0.03-nat safety cap.
3. **Easy safety PASS.** Aggregate easy changes remain within the fixed NLL/accuracy limits.
4. **Localization value PASS.** Query-local A2 beats uniform-context A3 by about `0.000270` nats on pooled hard NLL and `0.003779` nats on pooled easy NLL. This is retained as a narrow positive about localization, not evidence of absolute task utility.
5. **No hidden adaptation PASS.** Static inference remains parameter/state immutable and the frozen lambda is reused exactly.

Overall, A2 is slightly worse than W0: NLL `0.842260` vs `0.840656`, accuracy `62.75%` vs `63.04%`. The result is small in magnitude but directionally consistent with the failed hard-utility gate. Therefore static query-local vocabulary evidence, in this tested PoE formulation, does not rescue the missing novel hard-task utility.

### Program-level interpretation
The bounded T001–T012 evidence now supports several scoped findings but does **not** validate the original TOVD fast-semantic-state thesis:
- T005 remains a real frozen-checkpoint mechanism positive for O1+C2;
- T009 remains a real query-level harm-ranking positive;
- T012 retains a small query-local-vs-uniform localization advantage;
- however, random-init meta-training, warm continuation, episode-level gating, transferable query rollback, query-local residual adaptation, and now static PoE fusion all fail the preregistered utility/consistency requirements.

The repeated lesson is that vocabulary-relative signals can be measurable and locally structured without yielding a robust transferable decision rule or task-useful state/output movement on fresh novel semantics.

### Decision / next action
Enforce the T012 stop rule exactly:

- **Close the synthetic TOVD mechanism program.**
- Do **not** create T013 as another synthetic objective, gate, threshold, residual, temperature, fusion rule, meta-training variant, or fast-state architecture.
- Do **not** integrate T005/T009/T010/T011/T012 mechanisms into Grounding DINO under the current evidence.
- Preserve `research_log/t012/SYNTHESIS.md` and all positive/negative receipts as the final synthetic-program evidence package.
- No active Codex experiment is authorized after T012. Wait for an explicitly new Research Lead scope that changes the scientific premise rather than repairing the current synthetic line.

**PROGRAM STATE: CLOSED / AWAITING NEW RESEARCH SCOPE.**