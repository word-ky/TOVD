import math
import os

import torch

from research_log.t005.oracle_step_screen import score_output
from research_log.t008.runtime_features import FEATURES,PRE_FEATURES,extract_features,preupdate_features
from tovd.synthetic.models import EpisodicClassifier
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig


def fixture():
    device=os.environ.get("TOVD_TEST_DEVICE","cpu")
    torch.manual_seed(7)
    model=EpisodicClassifier("O1_backtracking").to(device).eval()
    episode=SemanticWorld(WorldConfig()).episode("test","easy",20070000).to(device)
    return model,episode


def test_pre_features_do_not_form_candidate_and_match_normal_inner(monkeypatch):
    model,ep=fixture()
    X,T,Q=ep.X[None],ep.T[None],ep.Q[None]
    with torch.no_grad():
        candidate=model(X,T,Q)
    def forbidden(*args,**kwargs):
        raise AssertionError("Pre-update feature path called candidate selection")
    monkeypatch.setattr(model.memory,"select_update",forbidden)
    features,before=preupdate_features(model,X,T,Q)
    assert tuple(features)==PRE_FEATURES
    assert features["inner_loss_before"]==candidate.diagnostics["inner_loss_before"].item()
    assert features["gradient_norm"]==candidate.diagnostics["inner_gradient_norm"].item()
    p=model.logits(before.tokens,T).softmax(-1)[0]
    expected=-sum(float(v)*math.log(max(float(v),1e-12)) for row in p for v in row)/len(p)
    assert abs(features["query_entropy"]-expected)<1e-6
    assert 0<=features["query_probability_gap"]<=1


def test_oracle_labels_ids_replay_and_parameters_cannot_change_features():
    model,ep=fixture()
    X,T,Q=ep.X[None],ep.T[None],ep.Q[None]
    original={k:v.detach().clone() for k,v in model.state_dict().items()}
    features,before,candidate=extract_features(model,X,T,Q)
    with torch.no_grad():
        score1=score_output(model,ep,candidate.tokens[0])
        ep.labels=(ep.labels+1)%4
        ep.query_ids.fill_(-99)
        ep.image_ids.fill_(-42)
        score2=score_output(model,ep,candidate.tokens[0])
        normal=model(X,T,Q)
    repeated,b0,c1=extract_features(model,X,T,Q)
    assert score1["nll"]!=score2["nll"]
    assert features==repeated
    assert set(features)==set(FEATURES)
    assert all(math.isfinite(x) for x in features.values())
    assert -1e-7<=features["query_js"]<=math.log(2)+1e-7
    assert features["prediction_changed_fraction"]*8==round(features["prediction_changed_fraction"]*8)
    torch.testing.assert_close(before.tokens,b0.tokens,rtol=0,atol=0)
    for other in (normal,c1):
        torch.testing.assert_close(candidate.tokens,other.tokens,rtol=0,atol=0)
        for name,value in candidate.fast_state.items():
            torch.testing.assert_close(value,other.fast_state[name],rtol=0,atol=0)
    for name,value in model.state_dict().items():
        torch.testing.assert_close(value,original[name],rtol=0,atol=0)
