# T013 real-OVD research reset

## Program boundary
The T001–T012 synthetic fast-semantic-state program is closed. Its evidence remains archived in `research_log/t012/SYNTHESIS.md`. T013 is not a continuation of that mechanism family.

## New empirical premise
Open-vocabulary detection exposes two distinct test-time shifts:

1. **Vocabulary composition shift**: user-provided class lists may be broad, irrelevant or semantically confusable.
2. **Visual/domain shift**: corruptions, adverse weather and appearance changes can degrade localization and open-vocabulary recognition.

Recent work has established each side separately: test-time vocabulary adaptation refines user vocabularies; ViTPrompt, FACTOR and PISA address open-vocabulary detection under image/domain shifts using training-free or source-free adaptation strategies.

T013 asks a narrower benchmark question before any method is proposed:

> Do semantically confusable test vocabularies amplify corruption-induced failure in a frozen real detector beyond the sum of the vocabulary-only and corruption-only effects?

If yes, later work can study a detector-native coupled-shift mechanism. If no, the vocabulary-conditioned robustness premise is rejected under the tested detector rather than rescued with another synthetic mechanism.

## Why Grounding DINO first
Grounding DINO directly conditions detection on free-form textual class prompts and is widely used as a language-driven/open-vocabulary detector. It provides a concrete real detector in which vocabulary composition can alter the same detection pipeline that must also handle corrupted visual inputs.

T013 intentionally uses only one frozen detector and a fixed COCO subset. Cross-detector generalization is deferred until the interaction itself is established.

## Key statistic
For corruption `c` and vocabulary `v`:

`D(c,v) = AP50(clean,v) - AP50(c,v)`

and

`A(c,v) = D(c,v) - D(c,V0)`.

`A(c,v) > 0` means that changing the vocabulary makes the detector more vulnerable to the same visual corruption. The critical comparison is confusable `Vhard` versus equal-size unrelated `Vrand`.

## Non-goals
T013 does not implement an adaptation method. It does not use fast weights, test-time gradients, prompt tuning, caption-based vocabulary pruning, learned gates, or any T001–T012 mechanism. It is a falsifiable real-detector interaction audit only.

## Related-work anchors
- Test-time Vocabulary Adaptation for Language-driven Object Detection, ICIP 2025 / arXiv:2506.00333.
- ViTPrompt: Training-Free Prompt Refinement with Visual Tokens for Open-Vocabulary Detection, CVPR 2026.
- FACTOR: Counterfactual Training-Free Test-Time Adaptation for Open-Vocabulary Object Detection, arXiv:2605.03294.
- PISA: A Pseudo-Individual Source-Domain Feature Adaptation Framework for Test-Time Open-Vocabulary Object Detection, arXiv:2608.14142.

These references motivate the separation between vocabulary-side and image-shift-side adaptation. T013 does not claim from literature search alone that coupled-shift analysis is entirely absent.