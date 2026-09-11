# T003 fixed oracle-diagnostic plan

Research instruction: c068c6f / 0c3ef5f. T002 accepted as a valid negative result.
This plan precedes reading T003 aggregate results. No outer training, generator
changes, test-based selection, or detector integration. Existing T001/T002 code
and checkpoints remain unchanged. Reuse the incremental baseline workflow.

## Sources and pairing

T002 tested code b88153a; completed run 20260912-023122-tovd-t002-a6000.
Use artifacts/t002/seed{7,17,27}_{P,B2}/checkpoint.pt from that run, together
with its saved config and episode generator. SHA256 and full input paths will
be written into the diagnostic receipt. Use all original 100 test episodes
per easy/hard regime, each seed, same seed formula 20000000+seed*10000+index.
Total: 1,200 checkpoint/episode diagnoses; P's 600 episodes additionally get
D3/D4. All analyses use the saved float32 checkpoint in eval mode.

Labels, class IDs and oracle gradients live only in explicitly named
oracle_diagnostic files. Normal model/inner signatures remain X/T/Q only.
Oracle results are analysis-only and not deployable TTT methods.

## Definitions fixed before execution

D1: at W0, compute g_inner from the checkpoint's normal mean cosine inner
loss, and g_task from mean query CE of its own static W0 path. Gradients are
only over six fast-MLP parameter tensors; slow projections are detached.
Flatten in named-parameter order. Report cosine, dot, both norms,
-eta*g_inner.dot(g_task) at eta=.05, actual task NLL change, episode/query
improvement fractions, per-seed moments and pooled episode distributions.
Gradient diagnostic uses labels only to construct g_task and score predictions;
the normal inner gradient is independent of those labels.

D2: evaluate W0-eta*g_inner at eta in [0,.01,.025,.05,.10] on the same frozen
checkpoint and episode. Save accuracy/NLL/cosine margin, deltas from eta=0,
per-query NLL and its delta. No checkpoint or eta selection; all values reported.
Also compare diagnostics' eta=.05 output to the unmodified normal model.

D3 (P only): foreground = image class ID in vocabulary, distractor = nonnegative
ID outside vocabulary, background = ID -1. Compute subset-mean gradients and
weighted contributions n_subset/N to the original all-token mean gradient.
Report norms, task cosine/dot, pairwise subset cosines and projection onto the
all-token gradient. Verify weighted sum reconstructs g_inner. This avoids
confusing subset-mean magnitude with contribution to the all-token update.
Oracle updates use eta=.05 on (a) all-token soft target, (b) foreground-mean soft
target, (c) foreground-mean exact class-text target. Report each update norm;
subset-mean normalization changes magnitude as well as selection, so distinguish
direction evidence from a clean causal magnitude attribution.

D4 (P only): at W0 record per-token assignment entropy (nats), top probability,
top1-top2 gap, target norm; for foreground also correct/wrong target cosine,
their margin and whether the highest-probability assignment is correct.
Retain source-separated raw token arrays and aggregate by episode then seed.
Distractor/background top probability quantifies forced assignment, not accuracy.
Relate hardness differences to observed update norms without claiming causality
from an aggregate correlation.

Statistics: means/sample SD across the three seed means; distribution summaries
mean/SD/p05/p25/median/p75/p95 and sign/improvement fractions over all 300 paired
episodes per method/regime. Per-episode paired records are primary evidence.
No new significance/acceptance thresholds. A/B/C/D recommendation follows the
Research Lead's decision logic and may be mixed or inconclusive.

## Increments and checks

1. Reproduce current full suite before edits. Reuse unchanged FastSemanticMemory,
   EpisodicClassifier, SemanticWorld, episode_seed and outer_metrics.
2. Add analysis-only gradients/updates: test exact normal P/B2 equality, small-step
   finite difference of task loss, weighted gradient recombination, class-target
   mapping, frozen-state preservation and label-independent normal gradient.
3. Add source reader/paired runner/aggregator: one tiny source-checkpoint fixture
   across P/B2, test raw records and aggregates; no training required.
4. Full CPU and CUDA suites, then fixed A6000 diagnostic run. Source checkpoint
   files and normal implementation are never written by the diagnostic.
5. Fetch raw records and report all branches including contradictions/negative
   results. No T004 implementation without Research Lead instruction.
