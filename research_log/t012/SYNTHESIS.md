# TOVD synthetic-program research synthesis

The fixed T012 success criterion fails. Per the active task stop rule, engineering stops the synthetic TOVD mechanism program here and submits this synthesis for Research Lead review. No successor mechanism or detector integration is proposed or launched.

## Evidence that remains valid

- T001 established vocabulary-dependent fast state, exact episodic reset and an outer-gradient path. These are mechanism/implementation facts, not detection utility.
- T005 found a useful frozen-checkpoint O1+C2 update: hard accuracy 40.54% to 46.25%, NLL 1.31390 to 1.23536; easy accuracy 77.58% to 86.71%. This positive result is preserved with its original state/stream scope.
- T009 found query-level harm ranking: delta-entropy LOSO AUROC mean .750696, minimum .722485, with offline oracle headroom. Ranking and an oracle are not deployable decision rules.

Sources: [Research Lead review ledger](../../coordination/CHATGPT_REVIEW_LOG.md), [T005](../t005/RESULTS.md), [T009](../t009/RESULTS.md).

## Where the proposed route failed

- T002–T004 separated a well-formed semantic inner loop from downstream task alignment and led to the O1 objective used in the later frozen T005 test.
- T006 lost absolute competitiveness under random-init C2 meta-training. T007 matched warm continuation still did not establish a stable successor and retained substantial easy-state regressions.
- T008 episode-level scalar harm observability failed; T009 localized the observable ranking signal to queries, but did not itself establish selection transfer.
- T010 froze actual base-calibrated thresholds before fresh novel validation. It removed many damaging updates but discarded most useful hard corrections: original/W1/W2 hard NLL-gain retention 47.56%/-4.79%/2.44%.
- T011 changed the fast state to an independent zero-initialized query residual. Inner descent and reset remained healthy, yet all five criteria failed; pooled accuracy fell from 59.79% W0 to 29.83%. Local teacher variation did not produce the required residual-localization advantage.
- T012 removed test-time state updates altogether and froze a single base-calibrated PoE exponent 0.2. The fixed novel-stream criterion still fails; gates are {'1': False, '2': False, '3': True, '4': True, '5': True}. Overall A0/A2 NLL 0.840656/0.842260, accuracy 63.0417%/62.7500%. Exact per-group/seed evidence is in RESULTS.md and gates.json.

T012 preserves a narrow positive: local fusion beats uniform fusion under the fixed localization criterion and meets aggregate easy-safety limits. Its hard NLL nevertheless worsens relative to W0 in all three state groups, and improving hard seeds number0/3,1/3,1/3. These are small adverse shifts, not the catastrophic easy collapse seen in T011. The static audit therefore separates a relative localization benefit from the missing absolute hard-task utility.

Sources: [T006](../t006/RESULTS.md), [T007](../t007/RESULTS.md), [T008](../t008/RESULTS.md), [T010](../t010/RESULTS.md), [T011](../t011/RESULTS.md), [T012](RESULTS.md).

## What this supports, and what it does not

The tested vocabulary evidence can change representations and predict some harm, but the program did not establish the required combination of novel hard utility, cross-seed consistency and easy safety. Successful local-objective descent, nonzero state changes, or an AUROC ranking alone are insufficient to support the original task-utility thesis. Freezing slow weights and using feed-forward fusion does not itself guarantee a beneficial decision boundary.

The conclusion is bounded to the specified synthetic world, source checkpoints, adaptation/fusion formulas and preregistered streams. Several states share training history; fresh episodes do not create independent semantic worlds. These experiments do not prove that every possible OVD method or static fusion is ineffective, and they contain no detector results. In particular, T005 and T009 remain valid scoped positives.

Archive the complete positive and negative evidence, keep the executed code and frozen calibration receipts, and wait for Research Lead review. Do not turn this synthesis into a new synthetic objective, gate, controller, exponent search or fast-state architecture.
