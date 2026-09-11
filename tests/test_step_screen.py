import copy
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path

import pytest
import torch

from research_log.t004.oracle_objective_screen import run as historical_screen
from research_log.t005.oracle_step_screen import METHODS, interpret_rules, oracle_step_episode, run
from tovd.synthetic.benchmark import evaluate_model
from tovd.synthetic.models import EpisodicClassifier
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig


@pytest.mark.parametrize("method", list(METHODS.values()))
def test_offline_step_diagnostic_matches_runtime_and_does_not_use_labels_to_select(method):
    device=os.environ.get("TOVD_TEST_DEVICE","cpu")
    torch.manual_seed(7)
    model=EpisodicClassifier(method).to(device)
    reference=EpisodicClassifier("O1_fixed").to(device)
    original=copy.deepcopy(model.state_dict())
    ep=SemanticWorld(WorldConfig()).episode("test","easy",20070000).to(device)
    result=oracle_step_episode(model,ep,reference.memory)
    relabeled=oracle_step_episode(model,replace(ep,labels=(ep.labels+1)%4,image_ids=ep.image_ids.flip(0)),reference.memory)
    assert result["normal_output_max_error"]==0
    assert result["normal_state_max_error"]==0
    assert result["step"]==relabeled["step"]
    assert result["O1_inner_loss_after"]==relabeled["O1_inner_loss_after"]
    assert result["after"]["nll"]!=relabeled["after"]["nll"]
    assert result["nonfinite_elements"]==0 and result["all_finite"]
    for name,value in model.state_dict().items():
        torch.testing.assert_close(value,original[name],rtol=0,atol=0)


def test_research_rule_logic_including_both_worsen_and_seed_count():
    base={"after.nll":{"mean":1.},"after.accuracy":{"mean":.5},
          "after.nll_delta":{"mean":-.1},"after.accuracy_delta":{"mean":0.},
          "alignment.cosine":{"mean":0.}}
    aggregate={method:{regime:copy.deepcopy(base) for regime in ("easy","hard")} for method in METHODS}
    for method in ("C0","C1","C2"):
        aggregate[method]["hard"]["alignment.cosine"]["mean"] = .2
    aggregate["C0"]["easy"]["after.nll"]["mean"] = 2.
    aggregate["C0"]["easy"]["after.accuracy"]["mean"] = .2
    per_seed={method:{"hard":{str(seed):{"after.nll_delta":{"mean":-.1}} for seed in (7,17,27)}} for method in ("C1","C2")}
    rules=interpret_rules(aggregate,per_seed,0)
    assert rules["rule1_scale_rescue"]["passes"]
    assert rules["rule2_descent_safe"]["passes"]
    assert rules["task_useful_controllers"]==["C1","C2"]
    aggregate["C1"]["hard"]["after.nll"]["mean"]=1.1
    # Only NLL worsens: Rule 1 still passes; both worsening must fail.
    assert interpret_rules(aggregate,per_seed,0)["rule1_scale_rescue"]["passes"]
    aggregate["C1"]["hard"]["after.accuracy"]["mean"]=.4
    per_seed["C1"]["hard"]["7"]["after.nll_delta"]["mean"]=.1
    per_seed["C1"]["hard"]["17"]["after.nll_delta"]["mean"]=.1
    rules=interpret_rules(aggregate,per_seed,1)
    assert not rules["rule1_scale_rescue"]["passes"]
    assert not rules["rule2_descent_safe"]["passes"]
    assert rules["task_useful_controllers"]==["C2"]


def test_frozen_step_source_pairing_runtime_and_receipts(tmp_path):
    device=os.environ.get("TOVD_TEST_DEVICE","cpu")
    config=json.loads(Path("research_log/t002/config.json").read_text())
    config.update(eval_episodes=2,mechanism_episodes=2)
    source=tmp_path/"source"
    folder=source/"seed7_P"
    folder.mkdir(parents=True)
    (source/"config.json").write_text(json.dumps(config))
    torch.manual_seed(7)
    model=EpisodicClassifier("P",**config["model"]).to(device)
    checkpoint=folder/"checkpoint.pt"
    torch.save({"state_dict":model.state_dict(),"config":config,"revision":"unit-fixture"},checkpoint)
    original_hash=hashlib.sha256(checkpoint.read_bytes()).hexdigest()
    _,episodes=evaluate_model(model,SemanticWorld(WorldConfig(**config["world"])),config,7,device)
    (folder/"episodes.json").write_text(json.dumps(episodes))
    historical_screen(source,tmp_path/"t004",device,"unit-test",seeds=(7,),episode_limit=2)
    result=run(source,tmp_path/"t004",tmp_path/"t005",device,"unit-test",seeds=(7,),episode_limit=2)
    for check in result["historical_checks"]:
        assert max(check["errors"].values())==0 and check["episode_seed_mismatches"]==0
    assert hashlib.sha256(checkpoint.read_bytes()).hexdigest()==original_hash
    assert result["environment"]["source_checkpoints"][0]["sha256"]==original_hash
    assert sum(result["C2_eta_counts"]["seed7_easy"].values())==2
    assert len(result["timings"]["C2"]["7"]["hard"]["pass_ms_per_episode"])==3
    assert result["aggregate"]["C1"]["hard"]["step.budget_absolute_error"]["pooled"]["max"]<1e-6
    assert (tmp_path/"t005/rules.json").exists()
