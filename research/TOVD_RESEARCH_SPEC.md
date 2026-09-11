# TOVD Research Spec

## Working thesis

Open-vocabulary detection (OVD) is dynamically conditioned by both the current image and the current vocabulary, yet most detectors use a largely static visual-language mapping learned offline. We investigate whether current image-vocabulary context can be written into **fast semantic weights** through a differentiable test-time inner loop, yielding image- and vocabulary-conditioned representations without using test labels.

## Core motivation

For an image `I` and test vocabulary `V = {c_1,...,c_C}`, conventional OVD computes visual features and text embeddings and applies a fixed learned mapping/similarity function. But the semantic decision space can change drastically with the vocabulary: e.g. `{dog, car, person}` versus `{husky, malamute, samoyed}`. The useful visual distinctions should therefore be vocabulary-dependent.

Rather than letting context affect only activations, TOVD asks whether context should also affect a small, temporary model state:

`(image context, vocabulary context) -> inner learning -> fast weights W* -> vocabulary-conditioned detection representation`.

This is inspired by Vision Test-Time Training (ViT^3), but the scientific target is different: **open-vocabulary semantic specialization**, not merely replacing attention or compressing K/V.

## Novelty boundary

A weak version that only applies generic ViT^3 `K -> V` inside an OVD backbone is NOT the target contribution. The inner target/loss must encode OVD-specific visual-language semantics.

The intended distinction is:

- ViT^3: context -> fast weights for sequence modeling.
- TOVD: image + dynamic vocabulary -> fast semantic weights for open-vocabulary discrimination/localization.

## Initial formulation

Given visual tokens:

`X in R^{N x d}`

and text embeddings for the current vocabulary:

`T in R^{C x d}`,

construct projected keys:

`K = P_k(X)`

and a vocabulary-conditioned semantic target:

`A = softmax(K T^T / tau)`

`S = A T`.

`S_i` is therefore a text-space semantic target induced jointly by visual token `i` and the current vocabulary.

Define a small fast model `F_W : R^d -> R^d`, initialized at meta-learned `W0`.

Inner objective (first candidate):

`L_inner = 1 - mean_i cosine(F_W(K_i), S_i)`

or a stable normalized dot-product equivalent.

One-step test-time update:

`W* = W0 - eta * grad_W L_inner(F_W(K), S)`.

For object/detection queries `Q`, produce adapted semantic representations:

`Q' = F_{W*}(P_q(Q))`.

These can then feed open-vocabulary classification/alignment and/or a detector decoder.

## Slow vs fast parameters

Slow/outer parameters may include:
- visual/text projections;
- detector backbone/decoder as selected later;
- meta-initialization `W0`;
- optional learned step size `eta`.

Fast parameters:
- only the explicitly designated parameters of `F_W` during the inner loop.

The outer training objective should differentiate through the inner update when training `W0` and other upstream slow components.

## Main hypotheses

### H1 — Vocabulary conditioning changes useful representation
For fixed image tokens `X`, changing vocabulary `T` should change `S`, the fast update `W*`, and adapted query representation `Q'`.

### H2 — Fast semantic state adds capacity beyond static similarity
A learned nonlinear `F_{W*}` should represent image-vocabulary relations that cannot be reduced to one fixed global similarity transform.

### H3 — Specialization without test labels
The test-time inner loss can specialize representations to current image/vocabulary without using detection ground truth.

### H4 — Meta-learned initialization matters
A learned `W0` should require fewer/smaller inner updates and outperform random/fixed initialization under identical budgets.

### H5 — The gain should be largest when vocabulary granularity changes
Potentially strongest cases:
- coarse -> fine-grained class lists;
- semantically confusable categories;
- long-tail/unseen classes;
- large dynamic vocabularies.

## First ablations after detector integration

1. No TTT / static OVD baseline.
2. Generic visual `K -> V_visual` TTT (ViT^3-like control).
3. Proposed visual `K -> S(X,T)` semantic TTT.
4. Same semantic target but frozen `W0` / no inner update.
5. Linear vs gated-MLP vs lightweight spatial fast model.
6. 0/1/2/3 inner steps.
7. Fixed vs learned inner learning rate.
8. Image-only vs vocabulary-only vs joint image+vocabulary conditioning.
9. Full vocabulary vs filtered/top-k vocabulary.
10. Episodic reset vs continual adaptation (continual only after episodic is stable).

## Mechanism diagnostics

Measure, where practical:
- `||W* - W0||`;
- inner loss before/after update;
- gradient norm;
- cosine similarity between semantic states under different vocabularies;
- representation shift `||Q' - Q0||`;
- class-wise gains vs semantic ambiguity / vocabulary granularity;
- failure cases where vocabulary conditioning drives the state in the wrong direction.

## Baseline integration preference

Grounding DINO is the preferred first research baseline because its pipeline exposes explicit visual-language fusion, language-guided query selection and detector queries. However, the first engineering task is intentionally detector-agnostic: prove the fast semantic mechanism and differentiability in isolation before modifying a large codebase.

## Scientific success criteria

The project is scientifically promising only if results support BOTH:

1. **mechanism evidence**: dynamic vocabulary measurably changes fast state/representation in the intended way; and
2. **task evidence**: this specialization improves open-vocabulary localization/classification under controlled evaluation compared with strong static baselines and generic TTT controls.

Passing unit tests alone is engineering success, not scientific validation.
