# T013-MECH1 — PASS

**Cross-vocabulary query-index verdict: PROVEN_VOCABULARY_DEPENDENT.**
This is a structural source verdict: the selected proposal/reference assigned
to slot q is a function of the vocabulary-conditioned encoder output and
token scores. It does not claim every image or vocabulary pair necessarily
produces different indices, or measure any such difference. Same-index
score/box hybrids are **prohibited** as a same-proposal causal decomposition.

Task-start HEAD65fc1208342f2fa8e3835bae20836bfcd9a64e27 includes the
concurrent Lead MECH1 update afc7c64 and the already-recorded 710-image health
point. Freeze6fec32243985ccc808123d851abf5f3dea10af99; native revision
856dde20aee659246248e20734ef9ba5214f5e44, as bound by frozen provenance.
The existing74051-byte native_source.tar.gz exactly matches frozen archive
SHA2568a0270b0ed22391b25fba9c1ddb32cd990c33a3321d26cbc0d9d3a07995fa214.
Seven traced native files exactly match both archive members and live native
tree SHA256s; three T013 files match frozen Git bytes and freeze-manifest hashes.
Copies/archive/license and raw remote hash transcript are under mech1/.
No native Git update, different release, model import or execution was used.

## Exact forward trace

Native paths below are relative to groundingdino/models/GroundingDINO/;
line numbers refer to the archived, hash-bound source copies. Full paths and
hashes are listed in mechanism_identifiability_receipt.json.

1. **Active branch.** groundingdino/config/GroundingDINO_SwinT_OGC.py sets
   num_queries900, two_stage_type='standard', embed_init_tgt=True, six encoder
   and six decoder layers, use_fusion_layer/use_text_enhancer/
   use_text_cross_attention/sub_sentence_present=True. build_groundingdino
   (groundingdino.py:379–408) and build_transformer(transformer.py:930–958)
   pass those flags through. T013 load_native (scripts/t013_native_detector.py:
   12–28) selects this exact config, CPU/eval, local BERT path and frozen weights.
   The loader was read as text, never run in MECH1.
2. **Caption to token features.** scripts/t013_text.py:47–62 constructs ordered
   lower-case class phrases separated by periods. detect_native:38–43 passes
   that caption to the model. GroundingDINO.forward:242–297 tokenizes it,
   constructs special-token masks/position IDs, calls BertModelWarper and
   projects last_hidden_state through feat_map into text_dict. BertModelWarper
   (bertwarper.py:109–160) passes embeddings/masks into the BERT encoder.
   generate_masks_with_special_tokens_and_transfer_map:224–273 builds
   per-phrase blocks and reset position IDs. Thus this audit does **not** assume
   unrestricted cross-class BERT self-attention, or claim appending distractors
   necessarily changes the initial canonical BERT embeddings.
3. **Visual features become multimodal before proposals.** set_image_tensor
   (groundingdino.py:209–212) invokes the backbone on image samples; caption
   text is not an input to this call. The features and text_dict enter
   Transformer.forward:258–279. TransformerEncoder.forward:545–595 executes
   a fusion layer, text enhancement and visual encoder layer each iteration.
   BiAttentionBlock.forward(fuse_modules.py:286–295) updates both v and l.
   BiMultiHeadAttention.forward:162–174 forms visual-query/language-key
   attention; :213–224 softmaxes over unmasked language tokens and multiplies
   language values to form a visual update. The vocabulary dependence therefore
   precedes proposal selection; final text_dict is replaced by fused memory_text.
4. **Grid proposals are not the selected query identities.**
   gen_encoder_output_proposals(utils.py:56–112) creates geometric grid/scale
   anchors from feature shapes and masks. Transformer.forward:284–301 then
   projects fused output_memory, computes enc_out_class_embed(output_memory,
   text_dict), takes max over token logits, and selects ordered top900 indices.
   ContrastiveEmbed.forward(utils.py:242–268) computes x @ encoded_text^T,
   masks padding and pads with -inf. This encoder top-k is over spatial proposals
   ranked by token scores, **not** the later global query/class top300.
5. **Reference selection/order depends on those scores.** Transformer.forward:
   296–310 computes encoder box deltas plus proposals, then gathers reference
   boxes using topk_proposals. The same indices gather output_memory at:312–315.
   With embed_init_tgt=True, :316–321 uses fixed learned tgt_embed[q] instead
   of gathered content for the decoder target. This is an important qualification:
   **target embedding identity is fixed; geometric/proposal identity is not.**
   The target at q is paired with the q-th ranked vocabulary-conditioned
   reference. Detaching that reference affects gradients, not its forward values.
6. **Decoder slots retain coupled geometry and content.** Transformer.forward:
   364–375 sends targets, gathered references, fused visual memory and text to
   the decoder. TransformerDecoder.forward:662–703 builds query positions from
   references. DeformableTransformerDecoderLayer.forward:895–925 performs
   query self-attention, text cross-attention and deformable visual cross-attention
   using these references. Iterative box updates at:715–734 produce the next
   layer's references. No cross-vocabulary proposal-ID alignment is introduced.
7. **Saved logits/boxes are final slot outputs.** GroundingDINO.forward:
   331–349 combines layer bbox deltas with layer references, computes token
   contrastive scores from layer_hs/text_dict, and returns only final pred_logits
   and pred_boxes. Intermediate encoder outputs are commented out at:351–361.
   Default unset_image_tensor at:362–364 prevents the previous forward's visual
   features being retained through this API; it does not align query slots.
8. **T013 scoring and persistence.** detect_native:44–55 computes
   sigmoid(token_logits) @ positive_map, then torch.topk(class_scores.flatten(),
   300). The positive map averages class-token probabilities with the frozen
   1e-6 denominator (t013_text.py:65–74); there is no cross-class softmax here.
   Query IDs are flat//C, labels flat%C. Boxes are converted from normalized
   cxcywh to pixel xyxy. Saved fields are boxes, class_scores, top_query_ids,
   top_labels, top_scores, token_logits and normalized_cxcywh. t013_native_run.py:
   53–68 executes each vocabulary on the same pixels and writes exactly this
   dictionary. Encoder topk_proposals, encoder memories, decoder hidden states,
   layer references and cross-vocabulary correspondences are not in this schema.

## Minimal alignment proof and its limits

For encoder location i and vocabulary V, let m_i(V) be fused visual memory and
t_j(V) fused text. The active source computes
s_i(V)=max_j <project(m_i(V)),t_j(V)>, I(V)=Top900(s(V)), and
r_q(V)=box_delta(m_{I_q(V)}(V))+grid_{I_q(V)} in unsigmoid coordinates.
Decoder input is the pair (learned_target_q, r_q(V)), plus fused memories.
There is no constraint that I_q(V1)=I_q(V2) or that r_q(V1)=r_q(V2).
The source proves a vocabulary-conditioned selection/reference path; it does
not establish actual per-image index changes or their magnitude without data.

Equal q remains a valid *array slot / learned target parameter index*, not a
proven common proposal or object. Numerically constructing boxes(V1)[q] with
scores(V2)[q] is possible but would not isolate classification vs localization
on a fixed latent proposal. Even accidental equal proposal indices would not
separate effects of fused memory, reference refinement and decoder context.

The two_stage_type='no' branch would use learned reference embeddings
(transformer.py:329–351), but it is not the frozen config. embed_init_tgt=False
would also make target content gathered/vocabulary-dependent; it is inactive.
Disabling fusion alone would not remove text-conditioned proposal scoring.
Subsentence masks constrain initial BERT/text self-attention, but do not remove
visual-language fusion or token-dependent proposal ranking. Ties/degenerate
weights may yield identical ranks for a pair; they do not supply an invariant
cross-vocabulary proposal-identity contract. No unresolved active branch is
needed for this structural verdict; exact numerical changes remain unmeasured.

## Identifiability map

These labels describe what saved outputs could support after the existing
completion/review barriers; they grant no new primary-data access now.

| Claim | Label | Supported boundary |
| --- | --- | --- |
| Final top300 distractor crowd-out | IDENTIFIABLE | CF1/CF2 isolate only this final selection competition with each saved forward held fixed; future primary execution still needs Lead authorization. |
| Vocabulary-associated class_scores/token_logits differences | OBSERVABLE-NOT-CAUSAL | Canonical columns have known class meaning; token positions require matching caption spans. Row-wise numbers are observable, but q is not a proven same proposal and no module is isolated. |
| Vocabulary-associated boxes/query geometry differences | OBSERVABLE-NOT-CAUSAL | Final box sets/slot values can differ; no claim of same-object displacement or localization-head causality follows. |
| Same-query cross-vocabulary score/box hybrid | NOT-IDENTIFIABLE-FROM-CACHE | Proposal alignment is not invariant; preregister no hybrid. |
| Attribution to initial text encoder | NOT-IDENTIFIABLE-FROM-CACHE | Initial BERT outputs absent; phrase masks prohibit assuming unrestricted initial mixing. Final text/visual effects are coupled. |
| Attribution to encoder fusion | NOT-IDENTIFIABLE-FROM-CACHE | Source shows an allowed dependence path, not its measured causal contribution; encoder states absent. |
| Attribution to proposal/query selection | NOT-IDENTIFIABLE-FROM-CACHE | Vocabulary-dependent selection is proven structurally; selected encoder IDs and preselection logits are not saved, so its outcome contribution is not isolated. |
| Attribution to decoder cross-attention | NOT-IDENTIFIABLE-FROM-CACHE | Decoder receives coupled content/references/memories; no layer interventions or states saved. |
| Attribution to classification head | NOT-IDENTIFIABLE-FROM-CACHE | Final dot-product/token scores jointly depend on hidden queries and text; score differences do not localize causality to the head. |
| Attribution to localization head | NOT-IDENTIFIABLE-FROM-CACHE | Final geometry combines selected references, repeated refinement and shared hidden states; boxes alone do not isolate the head. |

**Preregistration: no same-index score/box/token-logit hybrid.** Future causal
localization would require a separate controlled intervention/re-inference
designed and authorized after completed Grounding review. This audit neither
designs nor executes it. CF1/CF2 remain the only established counterfactual
decomposition, descriptive only; residual A_cf does not prove an upstream
module and cannot rescue a failed Grounding Gate1/Gate2.

## Static validation and operations

Exact commands included `git show 6fec32243985ccc808123d851abf5f3dea10af99:
scripts/t013_native_detector.py` (also native_run.py/text.py), `rg -n` and
bounded numbered reads of the copied source. Existing AutoDL Copy-FromAutodl
fetched only shared/t013/native_source.tar.gz. Python3.12.7 stdlib hashlib/
tarfile compared its SHA256, read the seven named members, and compared their
bytes against `sha256sum` on the same seven remote native files. No imported
model code, Torch, checkpoint or annotation. No new executable helper/tests.
Exact commands/file list and hashes are in mech1/STATIC_COMMANDS.md and receipt.

A concurrent Lead update caused the initial health-log push to be rejected;
normal fetch/merge preserved both histories. An initial bounded `ls *zip`
found no ZIP (the source is tar.gz), and two Windows rg wildcard arguments
were corrected to directory searches. No scientific/source failure resulted.

Only ordinary health point17:05:05+08:710/1000 at71953.82984643703s,
writer721181 Rl+/tmux alive,wrapper/result absent(existenceonly),free15523610624,
remaining290,projected4743045120,required14281588736,margin1242021888,
SAFE/PRIMARY_RUNNING. No extra watch, active-primary cache/scientific content,
annotations, inference, hooks/profile, checkpoint load, FIN1/replay,
counterfactual execution, run mutation, new Gate/threshold, YOLO or T014.
No cleanup/restart/resume. Stop MECH1 and await Research-Lead review.


## Exact traced source SHA256s

| Source | SHA256 |
| --- | --- |
| groundingdino/config/GroundingDINO_SwinT_OGC.py | 5d7093aaaeaafbf8eec07a1aef5bee976dff5615d54e0ca88293cd92e008a7c8 |
| groundingdino/models/GroundingDINO/groundingdino.py | f9f9fef478ad811565f34aad9f5eaeab0cd69f7379fc0ee3861c58ce4f55b29f |
| groundingdino/models/GroundingDINO/transformer.py | 7436a0daf8002cb4078bc56ab4343c7ec6d1f5dfe15b41747dc357cabad1760e |
| groundingdino/models/GroundingDINO/fuse_modules.py | a4b738a4ae3ca90cc5ae339241a9e0c24026bda96aedffb549b161bbdff96cd1 |
| groundingdino/models/GroundingDINO/bertwarper.py | 666e345c3450a6a276b37d09f2556926737e04f0c98b2526a7f6871b624ce546 |
| groundingdino/models/GroundingDINO/utils.py | 543d241b19e5592b99cbef42ce6406360bd70760da5acca14863e56f83205233 |
| groundingdino/models/GroundingDINO/transformer_vanilla.py | 540ba06a1d6c9b603ae0695e72a7a3cebae5f62c35ec5ec5e92490581f5b61f9 |
| scripts/t013_native_detector.py | b49f23f131777f08e23131ad55a94d9211c33b1c759adf86c6b52e2b95c34126 |
| scripts/t013_native_run.py | 177176fdb1c133b98770f8e6719b22e3ead0a00adbdced598e92326aec723429 |
| scripts/t013_text.py | 2c175a779304f045267e3419eda04dbc2e5c4730ae19cce23727043832102018 |
