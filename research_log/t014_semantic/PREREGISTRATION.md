# T014-SEM-P0: clean semantic composition audit v1

Status: contract frozen before any real-cache execution. Existing T013 clean-cache
use is **EXPLORATORY / POST-HOC DEVELOPMENT**, never confirmatory primary evidence.
Task-start HEAD: 61fb9804c1166681b3aa4fe8f9925c02acc74a34.
Lead instruction: 317abd180231304986bed77384f5708d4ec75476.
Grounding primary remains GROUNDING_PRIMARY_NOT_SUPPORTED. The previous YOLO
contingency is paused/superseded. No TTT method, outcome threshold or success gate
is specified. Labels are offline evaluation anchors, never adaptation targets.

## Inputs and scope

Single in-memory object: condition='clean'; canonical_labels (canonical concept IDs);
distractor_labels={Vhard30:[IDs],Vrand30:[IDs]}; images=[{image_id,gt,detections}].
GT entries: {box:[x1,y1,x2,y2],label,iscrowd}. Detections map exactly V0,
Vhard30,Vrand30 to ordered lists of {box:[x1,y1,x2,y2],label,score}.
All boxes are positive-area continuous xyxy in the same original-image coordinate
system. Scores are finite, unchanged detector scores. Image IDs are unique.
Canonical and added labels are disjoint. Labels identify concepts across vocabulary
conditions, not vocabulary-specific array positions. The future adapter must map
indices to these fixed concept IDs. Missing required fields are errors. The helper
rejects every condition other than clean. Additional fields, including query IDs,
are ignored. The ordered detection list is the frozen selected output; no new
filtering, thresholding, top-k, NMS, score normalization or sorting is performed.

Future exploratory inputs are the same frozen 1,000 T013 clean images/pixels and
V0=COCO80, Vhard30=COCO80+the frozen30 confusable distractors,
Vrand30=COCO80+the frozen30 matched random distractors. Strings, tokenization,
checkpoint, selections and evaluator settings remain unchanged. This module has
no file loader and this package opens no primary prediction/results cache. Tests
use miniature synthetic labels/boxes only; the schema need not require80/30 counts.
A separately preregistered split/stream is required for future confirmation.

## A. Dataset descriptions

For m in {AP,AP50,AR,AR50}, Delta_m(v)=m(clean,V0)-m(clean,v).
HardMinusRandom_AP50=Delta_AP50(Vhard30)-Delta_AP50(Vrand30).
Use the existing frozen COCO evaluator semantics (including its crowd/ignore,
category, maxDet and aggregation rules) and its percentage scale unchanged;
differences are percentage points. These are descriptors, not gates.
dataset_deltas only subtracts supplied evaluator summaries; it never evaluates.
GT anchoring below is a diagnostic and does not replace COCO matching semantics.

## B. Independent GT observations

G is the set of all non-crowd GT objects, pooled across images (each object has
equal weight; no per-image averaging). Each vocabulary is observed independently.
For g and v, select detections with IoU(box_d,box_g)>=0.5. IoU uses continuous area
without +1. Representative r_v(g) maximizes (IoU,score,-selected_order).
Ties are exact numerical ties, with no tolerance. List position is selected_order.
Labels do not affect representative choice. If no candidate exists r_v(g)=null.
Record representative box, score, label, IoU, selected order, correct=(label=c_g),
and distractor membership. Crowd GTs contribute no observations or supports.
Each GT is independent: a detection can represent multiple overlapping GTs.
There is no one-to-one assignment and no cross-vocabulary query-slot matching.

Let C={g in G:r_0 exists and correct_0}; L_v={g in C:r_v exists};
B_v={g in G:r_0 and r_v both exist}. B_v deliberately includes initially incorrect
GTs; box/score stability is unconditional on correctness. Supports may differ
between hard and random; no intersection or outcome-dependent support change.

| Metric | Definition | Support |
|---|---|---|
| V0_correct_survival | count(g in C: r_v exists and correct_v)/count(C) | count(C) |
| semantic_failure_given_localized | count(g in L_v:not correct_v)/count(L_v) | count(L_v) |
| distractor_takeover_rate | count(g in L_v:distractor_v)/count(L_v) | count(L_v) |
| localization_loss_rate | count(C minus L_v)/count(C) | count(C) |
| box_stability_mean | mean IoU(box_0,box_v) over B_v | count(B_v) |
| box_stability_median | median same IoUs, midpoint for even support | count(B_v) |
| score_delta | mean(score_v-score_0) over B_v | count(B_v) |

Rates carry integer numerator and support. Means/median carry support. Empty
supports yield value=null (JSON null), never zero or omitted; numerator is0 for
empty rates. Observations remain explicit nulls when unlocalized. No pairing is
inferred from a query ID. Score delta measures score change, not calibration or AP.

## C. Oriented hard-versus-random contrasts

For semantic failure, takeover, localization loss: H-R.
For survival, box stability mean/median, and score_delta: R-H.
Thus positive consistently means worse hard-context degradation (for score_delta,
larger hard-induced score decrease), not proof of worse detection quality.
Each contrast returns its orientation and both marginal supports. If either input
value is undefined the contrast is null. No paired-support restriction, uncertainty
test, acceptance threshold or reorientation after results is allowed in v1.

## D. Optional crowd-out decomposition (not executed)

After Lead review of the basic audit, the already accepted canonical-only top-k
counterfactual may be applied to the same frozen raw outputs using its existing
selection rules: compare native selected outputs against canonical-only selection
to describe final distractor crowd-out versus residual upstream context effects.
No cross-vocabulary hybrid boxes/scores or query alignment. This decomposition is
not part of the base phenomenon gate and is not implemented/executed here.

## Validation and next action

Deterministic synthetic tests cover identical outputs, distractor takeover,
canonical misclassification, localization loss, all tie-break levels, crowd/empty
supports, oriented contrasts, query-ID changes and clean-only schema rejection.
No detector imports/GPU, real image/cache/result access, AP recomputation, runtime
infrastructure work or TTT design is authorized in this package.

Research Lead review of T014-SEM-P0 before any execution on the completed clean Grounding cache or any TTT method design
