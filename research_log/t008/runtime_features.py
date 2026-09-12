"""Fixed label-free audit features. Inputs are model/X/T/Q only, never outcomes."""

import torch
from torch.func import functional_call
from .schema import PRE_FEATURES,POST_FEATURES,FEATURES,FEATURE_METADATA

EPS=1e-12


def entropy(probabilities):
    return -(probabilities*probabilities.clamp_min(EPS).log()).sum(-1).mean()


def preupdate_features(model,X,T,Q):
    """One episode with leading batch dimension1; does not call select_update."""
    memory=model.memory
    with torch.no_grad():
        before=memory(X,T,Q,enable_ttt=False)
        prob=model.logits(before.tokens,T).softmax(-1)
        top=prob.topk(2,dim=-1).values
        keys=memory.key_projection(X)
        assignments=memory.assignments(keys[0],T[0])
        atop=assignments.topk(2,dim=-1).values
        target=memory.inner_targets(keys,X,T)
    with torch.enable_grad():
        params={name:p.detach().requires_grad_(True) for name,p in memory.fast_model.named_parameters()}
        prediction=functional_call(memory.fast_model,params,(keys[0],))
        loss=memory.inner_objective(prediction,keys[0],X[0],T[0],target[0])
        gradients=torch.autograd.grad(loss,tuple(params.values()))
    with torch.no_grad():
        features={"query_entropy":entropy(prob).item(),"query_max_probability":top[...,0].mean().item(),
                  "query_probability_gap":(top[...,0]-top[...,1]).mean().item(),
                  "assignment_entropy":entropy(assignments).item(),
                  "assignment_probability_gap":(atop[...,0]-atop[...,1]).mean().item(),
                  "inner_loss_before":loss.item(),"gradient_norm":torch.sqrt(sum(g.square().sum() for g in gradients)).item()}
    return features,before


def extract_features(model,X,T,Q):
    features,before=preupdate_features(model,X,T,Q)
    with torch.no_grad():
        candidate=model(X,T,Q)
        p0=model.logits(before.tokens,T).softmax(-1)
        p1=model.logits(candidate.tokens,T).softmax(-1)
        mixture=.5*(p0+p1)
        js=.5*((p0*(p0.clamp_min(EPS).log()-mixture.clamp_min(EPS).log())).sum(-1)+
               (p1*(p1.clamp_min(EPS).log()-mixture.clamp_min(EPS).log())).sum(-1)).mean()
        w0_norm=torch.sqrt(sum(p.square().sum() for p in model.memory.fast_model.parameters())).item()
        diag=candidate.diagnostics
        features.update(chosen_eta=diag["chosen_eta"].item(),backtracking_trials=diag["backtracking_trials"].item(),
                        normalized_update=diag["fast_update_norm"].item()/(w0_norm+EPS),
                        representation_shift=(candidate.tokens-before.tokens).norm().item(),
                        relative_inner_reduction=(features["inner_loss_before"]-diag["inner_loss_after"].item())/(abs(features["inner_loss_before"])+EPS),
                        query_js=js.item(),prediction_changed_fraction=(p0.argmax(-1)!=p1.argmax(-1)).float().mean().item())
    return features,before,candidate
