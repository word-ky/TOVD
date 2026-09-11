import os

import torch

from research_log.t006.meta_gradient_probe import probe_episode, summarize_probes
from tovd.synthetic.benchmark import training_episode
from tovd.synthetic.models import EpisodicClassifier
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig


def test_C2_meta_alias_initialization_piecewise_path_and_outer_labels():
    device=os.environ.get("TOVD_TEST_DEVICE","cpu")
    torch.manual_seed(7)
    model=EpisodicClassifier("P_C2_meta").double().to(device)
    torch.manual_seed(7)
    reference=EpisodicClassifier("O1_backtracking").double().to(device)
    torch.manual_seed(7)
    original=EpisodicClassifier("P").double().to(device)
    for name,value in model.state_dict().items():
        torch.testing.assert_close(value,original.state_dict()[name],rtol=0,atol=0)
    ep=training_episode(SemanticWorld(WorldConfig()),7,0)
    inputs=tuple(x.double().to(device)[None] for x in (ep.X,ep.T,ep.Q))
    a,b=model(*inputs),reference(*inputs)
    torch.testing.assert_close(a.tokens,b.tokens,rtol=0,atol=0)
    assert not a.diagnostics["chosen_eta"].requires_grad
    result=probe_episode(model,ep,7,0,epsilons=(1e-5,))
    assert result["all_gradients_finite"]
    assert all(value>0 for value in result["outer_gradient_norms"].values())
    assert not result["probes"][0]["eta_switch"]
    assert result["probes"][0]["stable_region_agreement"]
    # Re-labeling changes only outer supervision, not selected eta.
    labels=ep.labels.to(device)
    for target in (labels,(labels+1)%4):
        replay=model(*inputs)
        torch.nn.functional.cross_entropy(model.logits(replay.tokens,inputs[1])[0],target).backward()
        torch.testing.assert_close(replay.diagnostics["chosen_eta"],a.diagnostics["chosen_eta"],rtol=0,atol=0)


def test_real_eta_switch_probes_are_reported_without_smoothness_claim():
    device=os.environ.get("TOVD_TEST_DEVICE","cpu")
    torch.manual_seed(7)
    model=EpisodicClassifier("P_C2_meta").double().to(device)
    world=SemanticWorld(WorldConfig())
    # Explicit large-perturbation branch-coverage fixture, not the study's
    # preregistered stability sample. The initial 20 probes at .1 do not cross.
    records=[probe_episode(model,training_episode(world,7,2),7,2,epsilons=(1e-5,1.))]
    summary=summarize_probes(records)
    switched=[probe for record in records for probe in record["probes"] if probe["eta_switch"]]
    assert switched
    assert all(probe["stable_region_agreement"] is None for probe in switched)
    assert summary["by_epsilon"]["1.0"]["switch_count"]==1
