# T003 interpretation: primarily branch C, limited easy-regime A

All task gradients, token masks and exact class-text targets in this analysis
are **offline oracle diagnostics**, not deployable TTT. Six original T002 P/B2
checkpoints, three seeds and the exact original 1,200 episode/checkpoint pairs
were used. No primary outer retraining or normal model change was made.

## Decision map

**C is the strongest supported branch.** The foreground soft-target gradient
has mean task cosine 0.04650 (easy) / -0.00487 (hard), versus 0.31727 / 0.12128
for the foreground exact-text oracle. The latter improves mean task NLL and
accuracy relative to the same checkpoint's W0 in all three seeds and both
regimes. Filtering alone does not provide a comparable rescue.

**A is a secondary, easy-only effect.** P easy NLL changes by -0.00845 at eta=.01,
-0.00745 at .025, +0.03019 at .05 and +0.17293 at .10. There is overshoot in the
aggregate, but alignment is not mostly positive across the whole benchmark:
only 55% of easy and 40% of hard episodes have positive inner/task dot product.
A smaller step does not supply a consistently task-useful semantic direction.
All eta values are diagnostics on W0 meta-trained for .05, not tuned methods.

**B is not supported as the primary explanation.** Foreground-only soft targets
worsen easy mean NLL relative to the normal all-token update (0.62642 vs 0.58611)
and only slightly improve hard (1.29790 vs 1.30265). Foreground/distractor/
background gradients have high pairwise cosine (roughly .90-.93 easy and
.95-.98 hard), rather than a clearly aligned foreground opposed by harmful
background. Weighted task contributions have mixed signs and are in the receipt.
A token gate alone is therefore not supported as the main repair by this run.

**D is not supported here.** Exact-text oracle updates do help in every seed's
mean, so these results do not justify concluding that all fast updates are
intrinsically ineffective. They also do not establish that a label-free
replacement objective can achieve the oracle's gains.

## Same-checkpoint effects (three-seed means)

| P path | Easy accuracy % | Hard accuracy % | Easy NLL | Hard NLL |
| --- | --- | --- | --- | --- |
| Own W0, eta=0 | 77.5833 | 40.5417 | 0.55592 | 1.31390 |
| Normal all-token soft, eta=.05 | 74.8750 | 39.4167 | 0.58611 | 1.30265 |
| Oracle foreground-only soft | 73.6667 | 39.5417 | 0.62642 | 1.29790 |
| Oracle foreground exact-text | 85.1667 | 48.3333 | 0.36045 | 1.18409 |

Exact-text oracle NLL deltas versus own W0 by seeds 7/17/27:
- Easy: [-0.218111, -0.272769, -0.095535].
- Hard: [-0.108597, -0.126840, -0.154012].
Accuracy changes (pp): easy [+12.000, +7.750, +3.000];
hard [+3.750, +10.250, +9.375]. Only 74.67%/78.33% of episodes improve NLL:
this oracle is not a universal or mathematical performance upper bound.

Subset losses are subset means. Foreground-only updates thus change both source
selection and normalization. The recorded norms make this visible: on hard,
foreground soft/exact update norms are 0.20804/0.20217 (similar), yet their task
alignment and outcomes differ substantially. On easy the exact-text norm is
smaller (0.15445 versus 0.18921), so a magnitude effect also cannot be excluded.

## What the target statistics show

Hard foreground assignment entropy is 1.36711 nats (maximum log(4)=1.38629),
versus 1.20604 easy; top probability is 0.31071 vs 0.46690 and top1-top2 gap
0.04567 vs 0.20785. Hard foreground assignment accuracy is only 29.2708%.
The barycentric target has cosine 0.95575 with the correct text but 0.96621 with
the strongest wrong text, a negative discrimination margin of -0.01046.
Its norm is high (0.95576), so high target norm or cosine-to-correct alone is not
proof of semantic discrimination. Distractor/background assignment statistics
are similar, despite their classes being absent from the vocabulary.

This is consistent with a non-discriminative barycentric target shared by nearby
classes. It is evidence for the Research Lead's objective-redesign branch, not
proof that a particular contrastive replacement will work.

## D1 distribution caution

P easy task cosine mean is 0.01111; pooled p05/median/p95 are
[-0.22951, 0.01784, 0.23356]. Hard mean is -0.01116; pooled values are
[-0.15112, -0.01988, 0.16463]. The hard dot-product mean is nevertheless positive
because dot products weight gradient magnitudes; mean cosine and mean dot need
not share a sign. Original task NLL improves after the normal step in only
39.33% easy / 43.00% hard episodes, and 31.75% / 40.54% of queries.

B2 differs by regime: easy mean cosine -0.03489 with +0.21538 NLL change;
hard mean cosine +0.07091 with -0.02722 NLL change and 57.33% of episodes improving.
This reinforces that inner-loss descent is not itself evidence of task gain.

## Pairing and reproducibility

- Tested diagnostic code: 6780de5ae44dcc89b9f1c45ea781f33dc16ffbaf.
- Run: 20260912-030923-tovd-t003-a6000; exit 0 at 03:10:33 +08:00.
- Local 30 tests; remote CPU 30 tests / CUDA 30 tests all passed.
- Every normal eta=.05 prediction exactly matches the unchanged P/B2 model.
- All original per-episode T002 accuracy/NLL/margin errors are exactly zero.
- Six source SHA256 values match the original local T002 checkpoints.
- Weighted subset gradient reconstruction maximum error: 2.3841858e-7 (float32).
- Full source paths, hashes, environment, means/SD, pooled distributions and
  raw query/token/episode records are under the run's artifacts/t003 directory.

Recommendation to Research Lead: review C as the main next design direction,
with optional magnitude control as a secondary consideration. No T004 or
label-free gate/contrastive objective has been implemented by this task.
