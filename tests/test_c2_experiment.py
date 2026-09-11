import copy
import json
import os
from pathlib import Path

import torch

from scripts.train_synthetic_semantic import run as train_run
from research_log.t004.oracle_objective_screen import summarize
from research_log.t005.oracle_step_screen import oracle_step_episode
from research_log.t006.experiment import interpretation_rules, run
from tovd.synthetic.benchmark import episode_seed
from tovd.synthetic.models import EpisodicClassifier
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig


def test_rule_comparators_fast_value_and_seed_robustness_flags():
    metric={"after.nll_delta":{"mean":-.1},"after.accuracy_delta":{"mean":.01},
            "after.nll":{"mean":1.25},"after.accuracy":{"mean":.46},"alignment.cosine":{"mean":.2}}
    aggregate={"P_C2_meta":{"easy":copy.deepcopy(metric),"hard":copy.deepcopy(metric)}}
    per_seed={"P_C2_meta":{regime:{str(seed):copy.deepcopy(metric) for seed in (7,17,27)} for regime in ("easy","hard")}}
    controls={m:{"hard":{"accuracy":{"mean":acc},"nll":{"mean":nll}}} for m,acc,nll in (("B0",.42,1.2),("B1",.38,1.4),("B2",.44,1.3))}
    mechanisms={str(seed):{"mean":{"easy_hard_state_delta":.1,"unrelated_state_delta":.1},"episodes":[{"reset_state_delta":0,"reset_output_delta":0}]} for seed in (7,17,27)}
    result=interpretation_rules(aggregate,per_seed,controls,-.01,{"passes":True},mechanisms)
    assert result["rule3_control_value"]["accuracy_branch"]["control"]=="B2"
    assert result["rule3_control_value"]["nll_branch"]["control"]=="B0"
    assert result["rule3_control_value"]["accuracy_branch"]["passes"]
    assert not result["rule3_control_value"]["nll_branch"]["passes"]
    per_seed["P_C2_meta"]["easy"]["27"]["after.nll_delta"]["mean"] = .2
    result=interpretation_rules(aggregate,per_seed,controls,-.01,{"passes":True},mechanisms)
    assert result["rule4_easy_safety"]["passes"]
    assert "27" in result["rule4_easy_safety"]["seed_robustness_flags"]
    assert result["recommendation"].startswith("Address stability")


def test_complete_meta_experiment_reuses_controls_and_initial_state(tmp_path):
    device=os.environ.get("TOVD_TEST_DEVICE","cpu")
    config=json.loads(Path("research_log/t006/config.json").read_text())
    config.update(seeds=[7],train_steps=2,batch_size=2,eval_episodes=2,mechanism_episodes=2)
    source_config={**config,"methods":["B0","B1","B2","P"]}
    source=tmp_path/"source"
    train_run(source_config,source,device,"unit-control-fixture")
    checkpoint=torch.load(source/"seed7_P/checkpoint.pt",map_location=device,weights_only=True)
    world=SemanticWorld(WorldConfig(**config["world"]))
    o1=EpisodicClassifier("O1_fixed",**config["model"]).to(device)
    grouped={}
    for name,method in (("O0","O0"),("C2","O1_backtracking")):
        model=EpisodicClassifier(method,**config["model"]).to(device)
        model.load_state_dict(checkpoint["state_dict"])
        grouped[name]={regime:{7:[{"diagnostics":oracle_step_episode(model,world.episode("test",regime,episode_seed(7,index,"test")).to(device),o1.memory)} for index in range(2)]} for regime in ("easy","hard")}
    historical=tmp_path/"t005"
    historical.mkdir()
    (historical/"frozen_step_screen.json").write_text(json.dumps(summarize(grouped)))
    result=run(config,source,historical,tmp_path/"t006",device,"unit-fixture",probe_count=2)
    validity=result["rules"]["rule1_validity"]
    assert validity["passes"]
    assert validity["control_max_metric_error"]==0
    assert validity["normal_state_max_error"]==0
    assert validity["training_runner_eval_max_error"]==0
    assert validity["initial_tensor_max_error"]==0
    assert len(result["source_checkpoints"])==4
    assert len(result["training"]["7"]["curve"])==2
    assert result["environment"]["config"]["methods"]==["P_C2_meta"]
    assert (tmp_path/"t006/meta_gradient_final.json").exists()
