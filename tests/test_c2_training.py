import json
import os
from pathlib import Path

import torch

from scripts.train_synthetic_semantic import run
from tovd.synthetic.benchmark import evaluate_model, train_model
from tovd.synthetic.models import EpisodicClassifier
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig


def test_meta_training_telemetry_initialization_replay_and_checkpoint(tmp_path):
    config=json.loads(Path("research_log/t006/config.json").read_text())
    config.update(seeds=[7],train_steps=2,batch_size=2,eval_episodes=2,mechanism_episodes=2)
    device=os.environ.get("TOVD_TEST_DEVICE","cpu")
    results=run(config,tmp_path,device,"unit-fixture")
    checkpoint=torch.load(tmp_path/"seed7_P_C2_meta/checkpoint.pt",map_location=device,weights_only=True)
    torch.manual_seed(7)
    original=EpisodicClassifier("P",**config["model"])
    for name,value in original.state_dict().items():
        torch.testing.assert_close(value,checkpoint["initial_state_dict"][name].cpu(),rtol=0,atol=0)
    assert checkpoint["W0_outer_drift"]>0
    assert len(checkpoint["training_curve"])==2
    for row in checkpoint["training_curve"]:
        assert row["finite"] and row["armijo_violations"]==0
        assert len(row["selected_etas"])==2
        assert 0<=row["accuracy"]<=1
    world=SemanticWorld(WorldConfig(**config["world"]))
    replay,repeated=train_model(world,config,7,"P_C2_meta",device)
    for name,value in replay.state_dict().items():
        torch.testing.assert_close(value,checkpoint["state_dict"][name],rtol=0,atol=0)
    assert repeated["training_curve"]==checkpoint["training_curve"]
    metrics,_=evaluate_model(replay,world,config,7,device)
    assert metrics==results[0]["metrics"]
    ep=world.episode("test","hard",20070000).to(device)
    with torch.no_grad():
        static=replay.memory(ep.X[None],ep.T[None],ep.Q[None],enable_ttt=False)
        direct=replay.memory.fast_model(replay.memory.query_projection(ep.Q[None]))
    torch.testing.assert_close(static.tokens,direct,rtol=0,atol=0)
