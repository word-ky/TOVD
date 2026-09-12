import hashlib
import os
from pathlib import Path

import torch

from research_log.t005.oracle_step_screen import score_output
from research_log.t007.experiment import load_model,read_json
from research_log.t008.audit import run,save_json
from research_log.t008.schema import FEATURES
from tovd.synthetic.benchmark import episode_seed
from tovd.synthetic.models import EpisodicClassifier
from tovd.synthetic.semantic_episodes import SemanticWorld,WorldConfig


def test_frozen_audit_full_flow_and_deduplicated_primary_grid(tmp_path):
    """Artificial checkpoint fixtures, no training or real feature selection."""
    torch.set_num_threads(1)
    device=os.environ.get("TOVD_TEST_DEVICE","cpu")
    config=read_json(Path("research_log/t008/config.json"))
    config["eval_episodes"]=2
    world=SemanticWorld(WorldConfig(**config["world"]))
    t005,t007=tmp_path/"t005",tmp_path/"t007"
    t005.mkdir(); t007.mkdir()
    sources=[]
    for seed in config["seeds"]:
        torch.manual_seed(seed)
        original=EpisodicClassifier("P",**config["model"]).state_dict()
        for branch,step in (("original_P",0),("P_O0_resume",0),("P_O0_resume",50),("P_C2_warm",0),("P_C2_warm",50)):
            state={k:v.clone() for k,v in original.items()}
            if step:
                state["memory.fast_model.output.weight"]+=.01 if branch=="P_C2_warm" else -.01
            state_id=f"seed{seed}_{branch}_step{step}"
            path=tmp_path/"runs/fixture"/f"{state_id}.pt"
            path.parent.mkdir(parents=True,exist_ok=True)
            torch.save({"state_dict":state},path)
            sources.append({"state_id":state_id,"seed":seed,"branch":branch,"step":step,
                            "path":"research_log/remote_runs/fixture/"+path.name,
                            "sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"primary_unique":branch=="original_P" or step!=0})
            model=load_model(state,"O1_backtracking",config,device)
            heldout={}
            for regime in ("easy","hard"):
                records=[]
                for index in range(2):
                    ep=world.episode("test",regime,episode_seed(seed,index,"test")).to(device)
                    with torch.no_grad():
                        static=model.memory(ep.X[None],ep.T[None],ep.Q[None],enable_ttt=False)
                        adapted=model(ep.X[None],ep.T[None],ep.Q[None])
                        before=score_output(model,ep,static.tokens[0])
                        after=score_output(model,ep,adapted.tokens[0])
                    records.append({"episode_seed":episode_seed(seed,index,"test"),"vocabulary_ids":ep.vocabulary_ids.tolist(),"query_ids":ep.query_ids.tolist(),
                                    "diagnostics":{"before":before,"after":after}})
                heldout[regime]=records
                if branch=="original_P":
                    save_json(t005/f"seed{seed}_C2_{regime}.json",records)
            if branch!="original_P":
                directory=t007/f"seed{seed}_{branch}"
                directory.mkdir(exist_ok=True)
                save_json(directory/f"step{step}_evaluations.json",{"heldout":heldout})
    result=run(config,sources,tmp_path/"runs",t005,t007,tmp_path/"out",device,"unit-artificial")
    assert result["validity"]["passes"]
    assert result["validity"]["normal_oracle_bitwise_equal"]
    assert result["full_grid_rows"]==60
    assert result["primary_rows"]==36
    assert len(result["sign_map"])==30
    assert set(result["gates"])==set(FEATURES)
    assert result["environment"]["training"]=="none"
    record=read_json(next((tmp_path/"out/records").glob("*.json")))[0]
    assert len(record["outputs"]["W0_tokens"])==8
    assert len(record["outputs"]["C2_tokens"][0])==16
    assert set(record["features"])==set(FEATURES)
    assert "labels" not in record["features"]
    assert record["checks"]["features_exact"]
    for source in sources:
        path=tmp_path/"runs"/Path(source["path"]).relative_to("research_log/remote_runs")
        assert hashlib.sha256(path.read_bytes()).hexdigest()==source["sha256"]
