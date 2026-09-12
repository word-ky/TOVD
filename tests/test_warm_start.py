import json
import os
from pathlib import Path

import pytest
import torch
from torch.nn import functional as F

from tovd.synthetic.benchmark import train_model, training_episode
from tovd.synthetic.models import EpisodicClassifier
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig, stack_episodes


@pytest.mark.parametrize("branch,alias", [("P_O0_resume","P"),("P_C2_warm","P_C2_meta")])
def test_common_origin_fresh_adam_continuation_and_snapshots(branch, alias, tmp_path):
    device=os.environ.get("TOVD_TEST_DEVICE","cpu")
    config=json.loads(Path("research_log/t007/config.json").read_text(encoding="utf-8-sig"))
    config.update(train_steps=2,batch_size=2)
    world=SemanticWorld(WorldConfig(**config["world"]))
    _,source=train_model(world,config,7,"P",device)
    source_state={k:v.clone() for k,v in source["state_dict"].items()}
    snapshots={}
    def snapshot(step, model):
        snapshots[step]={k:v.detach().clone() for k,v in model.state_dict().items()}
    actual,checkpoint=train_model(world,config,7,branch,device,initial_state_dict=source_state,
                                  episode_offset=4,snapshot_steps=(0,1,2),snapshot_callback=snapshot)
    manual=EpisodicClassifier(alias,**config["model"]).to(device)
    manual.load_state_dict(source_state)
    optimizer=torch.optim.Adam(manual.outer_parameters(),lr=config["outer_lr"])
    assert not optimizer.state
    for step in range(2):
        X,T,Q,labels=stack_episodes([training_episode(world,7,4+step*2+j) for j in range(2)],device)
        manual.zero_grad(set_to_none=True)
        result=manual(X,T,Q)
        if step==0:
            origin=EpisodicClassifier(branch,**config["model"]).to(device)
            origin.load_state_dict(snapshots[0])
            origin_result=origin(X,T,Q)
            torch.testing.assert_close(result.tokens,origin_result.tokens,rtol=0,atol=0)
        loss=F.cross_entropy(manual.logits(result.tokens,T).flatten(0,1),labels.flatten())
        loss.backward()
        optimizer.step()
        for name,value in manual.state_dict().items():
            torch.testing.assert_close(value,snapshots[step+1][name],rtol=0,atol=0)
    for name,value in source_state.items():
        torch.testing.assert_close(value,source["state_dict"][name],rtol=0,atol=0)
        torch.testing.assert_close(value,snapshots[0][name],rtol=0,atol=0)
        torch.testing.assert_close(value.cpu(),checkpoint["initial_state_dict"][name],rtol=0,atol=0)
    replay,_=train_model(world,config,7,branch,device,initial_state_dict=source_state,episode_offset=4)
    torch.save(checkpoint,tmp_path/"checkpoint.pt")
    loaded=torch.load(tmp_path/"checkpoint.pt",map_location=device,weights_only=True)
    assert loaded["continuation"]["episode_offset"]==4
    for name,value in actual.state_dict().items():
        torch.testing.assert_close(value,replay.state_dict()[name],rtol=0,atol=0)
        torch.testing.assert_close(value,loaded["state_dict"][name],rtol=0,atol=0)
    assert checkpoint["W0_outer_drift"]>0
    assert all(row["finite"] and row["armijo_violations"]==0 for row in checkpoint["training_curve"])
