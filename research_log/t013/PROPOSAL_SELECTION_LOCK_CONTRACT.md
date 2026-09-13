# T013-MECH2 — proposal-selection lock (synthetic preparation only)

Task-start37823006fda01a942512330251608a4d67c74344.
Freeze6fec32243985ccc808123d851abf5f3dea10af99;
native856dde20aee659246248e20734ef9ba5214f5e44.
MECH1 transformer.py SHA7436a0daf8002cb4078bc56ab4343c7ec6d1f5dfe15b41747dc357cabad1760e;
SwinT_OGC config SHA5d7093aaaeaafbf8eec07a1aef5bee976dff5615d54e0ca88293cd92e008a7c8.
Active branch: standard two-stage,900 queries,embed_init_tgt=True.
Bound source copies are under research_log/t013/mech1/groundingdino/.

## One intervention

For the same image and same visual condition, obtain ordered encoder spatial
indices I0 from an ordinary V0 forward. In Vx=Vhard30/Vrand30, compute all native
encoder quantities normally, including encoder class logits and unsigmoid
encoder coordinate predictions. At Transformer.forward(transformer.py:301),
replace only `topk_proposals = torch.topk(topk_logits,900,dim=1)[1]` with I0.
Here topk_logits is max over token logits(:290–295). Initial references remain
`gather(enc_outputs_coord_unselected_x,1,I0[...,None].repeat(1,1,4)).detach()`
at:304–307. These coordinates already contain the Vx encoder box delta plus
geometric grid proposal(:296–298). **Import indices/order only, never V0 boxes.**

Production tensors: encoder class logits[B,S,T], coordinate predictions[B,S,4],
selection scores[B,S], ordered unique int64 indices[B,900],references[B,900,4].
S is the common spatial encoder lattice for identical image/preprocessing;
I0 addresses encoder locations, not decoder query slots. Never reuse clean I0
for a corrupted input. K in toy tests is a requested small analog of fixed900;
it is not a new production hyperparameter. No implicit sort/coercion/refill.

Only imported object: ordered I0, int64, correct batch/count,unique per row,
0<=index<S. Standalone reference explicitly rejects wrong dtype/shape/range,
duplicate indices or wrong count; it accepts no V0 coordinate/score/feature
tensor. Native no-override path uses exact torch.max/topk/gather behavior,
including device-specific tie order. Cross-device bitwise identity is not claimed.

Everything else remains Vx-native: caption/token features, fused text memory,
fused visual memory, encoder class logits, encoder coordinate predictions,
learned target embeddings, decoder text/visual attention, iterative box
refinement, final token/class scoring and flattened global top300. Learned
target vectors are the same model parameters and are paired with newly gathered
Vx references; no V0 decoder state is imported. This is selection/order lock,
not V0 reference replay or a same-index cross-vocabulary hybrid.

The same topk_proposals variable also gathers init_box_proposal(:308–310) and
tgt_undetach(:313–315). These become I0-indexed **Vx-native** values too. Under
the frozen embed_init_tgt=True branch, decoder tgt comes from the unchanged
learned embeddings(:316–327), not tgt_undetach. hs_enc/ref_enc/init_box_proposal
returned at:387–398 are not used by final output generation; GroundingDINO
forward:351–361 leaves intermediate output exposure commented out. Thus the
live final-prediction path changes only selector-driven reference initialization
and its downstream consequences, not an additional imported hidden state.
If this active branch/schema ever changes, this contract does not transfer.

## Future descriptors — NOT RUN, NOT A GATE

If authorized later, AP50_lock(c,v) uses the original T013 evaluation and paired
image bootstrap on this one intervention's output. V0 keeps its ordinary/native
selection (the null lock). Preserve all images, visual-condition seeds,
vocabularies, weights, preprocessing, finaltop300, metric definitions and pairing.

- D_lock(c,v)=AP50_lock(clean,v)-AP50_lock(c,v).
- A_lock(c,v)=D_lock(c,v)-D_lock(c,V0).
- C_select(c,v)=A_orig(c,v)-A_lock(c,v).

Use paired replicate-first differences with frozen bootstrap conventions if
later executed. C_select is a descriptive causal-intervention decomposition
for selection/order and all its consequences under the preserved Vx state.
It does not isolate all upstream vocabulary influence, freeze geometry, or
assign residual A_lock to one downstream module. No new threshold or Gate.

**Do not execute if Grounding Gate1 or Gate2 fails.** A failed primary stays
failed; this is not a rescue experiment. Future execution requires completed
primary, CLOSE1 validity, completed Grounding Research-Lead review and explicit
later authorization. No inference is authorized by this preregistration.

## This package

Standalone helper/tests only under mech2/, no integration/patch to model code.
Six deterministic tests cover five required validation classes; invalid cases
are eight overrides and four requested counts. Synthetic CPU and available
CUDA tests use Torch2.4.0; CUDA is preferred for synthetic tensors per user
preference, while CPU also validates frozen execution semantics. No detector
import/checkpoint/forward, data, annotations, smoke predictions, metrics,
bootstrap execution, hooks/profiling, source/run mutation, FIN1/replay,
second intervention, new Gate, YOLO or T014. Keep ordinary scalar monitoring;
incident/completion returns to Lead via existing OPS3. Stop after evidence.
