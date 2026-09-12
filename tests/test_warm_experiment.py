import copy
import os

import torch

from scripts.train_synthetic_semantic import run as train_run
from research_log.t003.oracle_diagnostic_run import save_json
from research_log.t004.oracle_objective_screen import summarize
from research_log.t005.oracle_step_screen import oracle_step_episode
from research_log.t007.experiment import BRANCHES, digest, load_model, read_json, rules, run
from tovd.synthetic.benchmark import episode_seed
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig
from pathlib import Path


def test_preservation_and_matched_objective_comparators():
    metric={"after.nll_delta":{"mean":-.1},"after.accuracy_delta":{"mean":.01},
            "after.nll":{"mean":1.2},"after.accuracy":{"mean":.47},"alignment.cosine":{"mean":.2}}
    aggregate={b:{r:copy.deepcopy(metric) for r in ("easy","hard")} for b in BRANCHES}
    per_seed={b:{r:{str(s):copy.deepcopy(metric) for s in (7,17,27)} for r in ("easy","hard")} for b in BRANCHES}
    controls={m:{"hard":{"accuracy":{"mean":.44},"nll":{"mean":1.3}}} for m in ("B0","B1","B2")}
    historical={"C2":{"hard":copy.deepcopy(metric)},"O0":{"hard":{"alignment.cosine":{"mean":-.01}}}}
    mechanisms={b:{str(s):{"mean":{"easy_hard_state_delta":.1,"unrelated_state_delta":.1},
                          "episodes":[{"reset_state_delta":0,"reset_output_delta":0}]} for s in (7,17,27)} for b in BRANCHES}
    result=rules(aggregate,per_seed,controls,historical,{"passes":True},mechanisms)
    assert all(v["passes"] for v in result.values())
    aggregate["P_C2_warm"]["hard"]["after.accuracy"]["mean"]=.44
    aggregate["P_C2_warm"]["hard"]["after.nll"]["mean"]=1.24
    result=rules(aggregate,per_seed,controls,historical,{"passes":True},mechanisms)
    assert not result["rule3_preservation"]["passes"]
    assert not result["rule4_objective_effect"]["passes"]
    aggregate["P_C2_warm"]["hard"]["after.nll"]["mean"]=1.2
    result=rules(aggregate,per_seed,controls,historical,{"passes":True},mechanisms)
    assert result["rule4_objective_effect"]["passes"]  # Equal NLL is not worse in both.
    per_seed["P_C2_warm"]["easy"]["27"]["after.nll_delta"]["mean"]=.11
    result=rules(aggregate,per_seed,controls,historical,{"passes":True},mechanisms)
    assert not result["rule6_easy_mechanism"]["passes"]


def test_complete_warm_continuation_provenance_trajectory_and_replay(tmp_path):
    device=os.environ.get("TOVD_TEST_DEVICE","cpu")
    config=read_json(Path("research_log/t007/config.json"))
    config.update(seeds=[7],train_steps=2,batch_size=2,eval_episodes=2,mechanism_episodes=2)
    source=tmp_path/"source"
    train_run({**config,"methods":["B0","B1","B2","P"]},source,device,"unit-source")
    t006=tmp_path/"t006"
    train_run({**config,"methods":["P_C2_meta"]},t006/"trained",device,"unit-t006")
    t005=tmp_path/"t005"
    t005.mkdir()
    world=SemanticWorld(WorldConfig(**config["world"]))
    grouped={}
    for name,method,root,source_method in (("O0","O0",source,"P"),("C2","O1_backtracking",source,"P"),
                                          ("P_C2_meta","O1_backtracking",t006/"trained","P_C2_meta")):
        ckpt=torch.load(root/f"seed7_{source_method}/checkpoint.pt",map_location=device,weights_only=True)
        model=load_model(ckpt["state_dict"],method,config,device)
        fixed=load_model(ckpt["state_dict"],"O1_fixed",config,device)
        grouped[name]={}
        for regime in ("easy","hard"):
            rows=[{"episode_seed":episode_seed(7,i,"test"),"diagnostics":oracle_step_episode(model,world.episode("test",regime,episode_seed(7,i,"test")).to(device),fixed.memory)} for i in range(2)]
            grouped[name][regime]={7:rows}
            save_json((t006 if name=="P_C2_meta" else t005)/f"seed7_{name}_{regime}.json",rows)
    save_json(t005/"frozen_step_screen.json",summarize({k:v for k,v in grouped.items() if k!="P_C2_meta"}))
    hashes={f"seed7_{m}":digest((t006/"trained" if m=="P_C2_meta" else source)/f"seed7_{m}/checkpoint.pt") for m in ("B0","B1","B2","P","P_C2_meta")}
    result=run(config,source,t005,t006,hashes,tmp_path/"out",device,"unit-t007",snapshot_steps=(0,1,2))
    assert result["rules"]["rule1_validity"]["passes"]
    assert len(result["training"])==2
    assert len(result["trajectories"])==6
    assert result["environment"]["episode_offset"]==4
    zero=[row for row in result["trajectories"] if row["step"]==0]
    assert zero[0]["metrics"]["heldout"]["hard"]["after"]==zero[1]["metrics"]["heldout"]["hard"]["after"]
    assert all(row["drift"]["classifier"]==0 for row in result["trajectories"])
    for branch in BRANCHES:
        raw=read_json(tmp_path/f"out/seed7_{branch}/step2_evaluations.json")
        assert [r["episode_seed"] for r in raw["train_seen_at_final"]["easy"]]==[10070004,10070006]
        assert [r["episode_seed"] for r in raw["train_seen_at_final"]["hard"]]==[10070005,10070007]
        assert len(read_json(tmp_path/f"out/seed7_{branch}/hard_oracle.json"))==2
        checkpoint=torch.load(tmp_path/f"out/seed7_{branch}/checkpoint.pt",map_location="cpu",weights_only=True)
        assert checkpoint["source_sha256"]==hashes["seed7_P"]
        assert all(r["finite"] for r in checkpoint["training_curve"])
