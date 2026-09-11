# T002 implementation and fixed comparison plan

Research instruction: de51d5b (T001 ACCEPTED, T002 ACTIVE). Mode: Implement.
Reuse provenance: this repository's T001 a344037; no third-party code copied.
Baseline: Python 3.12.7 / torch 2.13.0+cpu / pytest 9.1.1; pre-edit suite recorded
in progress.md. No datasets, checkpoints, or detector integration required.

## Reuse map and increments

| Responsibility | Existing owner | Change / test |
| --- | --- | --- |
| Semantic world, episodes | absent | New synthetic generator; disjoint classes, order/remapping, hardness, paired scenes |
| P and B0 representations | FastSemanticMemory | Reuse directly; retain all T001 tests |
| B2 target | inline semantic target | Extract target method, override with X; test exact target and vocabulary independence |
| B1 activation conditioning | existing projections/MLP | Same parameters, direct vocabulary and image semantic context; test permutation/gradient |
| Fixed W0 | existing functional initialization | Exclude W0 from outer optimizer only; prove invariant while projections train |
| Training/evaluation | absent | One shared runner, same episodes for all methods; known-metric, checkpoint, mini end-to-end tests |
| Remote execution | AutoDL scripts | Existing project config, release/run and receipt fetching |

Increment order: generator -> minimal target extension and five model paths ->
training/evaluation/receipts -> full local and CUDA tests -> 3-seed comparison.
Each increment has focused pytest checks before the next edit. Revert boundaries
are its new files and its narrow patch to existing code, not repository resets.
The final comparison runs only after mini end-to-end tests pass.

## Generator and protocol chosen before headline results

Dimension 16; 12 prototype clusters, 10 classes each. Fixed world seed 20260912.
Clusters 0..7 are training; 8..11 are held out (disjoint classes and centers).
Unit semantic prototypes are normalized cluster center plus 0.35 times an
independent unit residual. Text and visual embeddings are different fixed
rotations/noisy views of those prototypes; visual observations additionally
include a small nonlinear distortion and independent observation noise.
No per-class parameters exist in any learner.

Vocabulary size 4. Easy: one class from each of four clusters. Hard: four classes
from a single cluster. Two foreground classes per training/evaluation episode;
8 query tokens sample these classes in random order. Image context: 16 noisy
foreground tokens, 8 excluded-class distractor tokens and 8 Gaussian background
tokens, shuffled together. Vocabulary order is independently shuffled; labels
are calculated from class identity after permutation. No positions encode class.

One separate paired diagnostic fixes a single-class scene and all query/image
observations, and varies only an anchor-containing easy/hard vocabulary. An
unrelated vocabulary contains none of that scene's class: report confidence,
entropy and state/output shifts, not bogus classification accuracy for absent
labels. Main episodes and diagnostic episodes use separate seeds.

Five methods: B0 static, B1 activation-only, B2 visual TTT, P semantic TTT,
P_fixed (fixed random W0 throughout outer training; projections still train).
All start with the same seeded T001 parameter tensors, dimension and hidden size.
P/B2/P_fixed use one step eta=0.05; semantic attention tau=0.2; outer normalized
similarity temperature=0.1. B2 target is raw X, with no vocabulary conditioning.
B1 reuses static output r and both projections: r + 0.5*attention(r,T)T +
0.5*mean_image(attention(P_k(X),T)T). This gives activation-only access to both
the current vocabulary and image context with no added parameters.

Headline: seeds [7,17,27], 400 outer steps, 4 episodes/step, Adam lr=0.001,
balanced easy/hard training, float32. Exactly the same 1600 training episodes
and initialization per seed across methods. No outer optimization at evaluation.
100 held-out episodes per regime per seed; final checkpoint only (no test-based
selection). Same evaluation episodes across methods; aggregate per-seed mean,
then mean/sample SD across three seeds. Fixed generator/hyperparameters will not
be tuned in response to held-out results. Record any negative comparisons.

Report accuracy, CE, cosine correct-class margin, representation shift, inner
diagnostics, parameter counts, and measured batch-1 evaluation latency with
warmup and CUDA synchronization. Timing includes the exposed T001 diagnostics;
it is approximate prototype compute, not an optimized kernel benchmark.
No new architecture sweep, thresholds, early detector integration, or real OVD
performance claims. H2/P-vs-B1 is the central comparison.
