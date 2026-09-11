"""Piecewise C2 meta-gradient receipts; selector switches are explicitly reported."""

from collections import defaultdict
import json
from pathlib import Path

import torch
from torch.func import functional_call
from torch.nn import functional as F

from tovd.synthetic.benchmark import training_episode
from tovd.synthetic.models import EpisodicClassifier
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig

EPSILONS=(1e-5,1e-3,.01,.1)
PARAMETER="memory.fast_model.output.weight"


def probe_episode(model, episode, seed, index, epsilons=EPSILONS):
    model.train()
    params=dict(model.named_parameters())
    device=params[PARAMETER].device
    inputs=tuple(value.to(device=device,dtype=torch.float64)[None] for value in (episode.X,episode.T,episode.Q))
    labels=episode.labels.to(device)[None]
    result=model(*inputs)
    loss=F.cross_entropy(model.logits(result.tokens,inputs[1]).flatten(0,1),labels.flatten())
    gradients=torch.autograd.grad(loss,tuple(params.values()),allow_unused=True)
    by_name=dict(zip(params,gradients))
    generator=torch.Generator().manual_seed(90000000+seed*1000+index)
    direction=torch.randn(params[PARAMETER].shape,generator=generator,dtype=torch.float64).to(device)
    direction/=direction.norm()
    analytic=(by_name[PARAMETER]*direction).sum().item()
    eta=result.diagnostics["chosen_eta"].item()
    def group_norm(prefix):
        values=[g.square().sum().item() for name,g in by_name.items() if name.startswith(prefix) and g is not None]
        return sum(values)**.5
    norms={"W0":group_norm("memory.fast_model."),"key":group_norm("memory.key_projection."),"query":group_norm("memory.query_projection.")}
    rows=[]
    for epsilon in epsilons:
        values,etas=[],[]
        for sign in (1,-1):
            shifted={**params,PARAMETER:params[PARAMETER]+sign*epsilon*direction}
            shifted_result=functional_call(model,shifted,inputs)
            values.append(F.cross_entropy(model.logits(shifted_result.tokens,inputs[1]).flatten(0,1),labels.flatten()).item())
            etas.append(shifted_result.diagnostics["chosen_eta"].item())
        numeric=(values[0]-values[1])/(2*epsilon)
        stable=all(value==eta for value in etas)
        error=abs(analytic-numeric)
        rows.append({"epsilon":epsilon,"base_eta":eta,"plus_eta":etas[0],"minus_eta":etas[1],
                     "eta_switch":not stable,"analytic_derivative":analytic,"central_difference":numeric,
                     "absolute_error":error,"stable_region_agreement":error<=1e-7+1e-4*abs(numeric) if stable else None})
    return {"seed":seed,"index":index,"regime":"easy" if index%2==0 else "hard",
            "episode_seed":10000000+seed*10000+index,"outer_loss":loss.item(),
            "outer_gradient_norms":norms,"all_gradients_finite":all(torch.isfinite(g).all().item() for g in gradients if g is not None),
            "eta_requires_grad":result.diagnostics["chosen_eta"].requires_grad,"probes":rows}


def summarize_probes(records):
    groups=defaultdict(list)
    for record in records:
        for probe in record["probes"]:
            groups[str(probe["epsilon"])].append(probe)
    distribution={key:{"count":len(rows),"switch_count":sum(row["eta_switch"] for row in rows),
                       "switch_fraction":sum(row["eta_switch"] for row in rows)/len(rows),
                       "stable_count":sum(not row["eta_switch"] for row in rows),
                       "stable_disagreements":sum(row["stable_region_agreement"] is False for row in rows),
                       "stable_max_absolute_error":max((row["absolute_error"] for row in rows if not row["eta_switch"]),default=None)}
                  for key,rows in groups.items()}
    primary=[record for record in records if any(p["epsilon"]==1e-5 and not p["eta_switch"] for p in record["probes"])]
    ready=all(record["all_gradients_finite"] and not record["eta_requires_grad"] for record in records)
    for seed in sorted({record["seed"] for record in records}):
        ready &= any(row["seed"]==seed and all(n>0 for n in row["outer_gradient_norms"].values()) for row in primary)
    ready &= all(p["stable_region_agreement"] for record in primary for p in record["probes"] if p["epsilon"]==1e-5 and not p["eta_switch"])
    return {"by_epsilon":distribution,"pretraining_gradient_requirement_passes":bool(ready)}


def run_probes(config, output, device, checkpoint_root=None, probe_count=20):
    torch.set_num_threads(1)
    world=SemanticWorld(WorldConfig(**config["world"]))
    records=[]
    for seed in config["seeds"]:
        torch.manual_seed(seed)
        model=EpisodicClassifier("P_C2_meta",**config["model"])
        if checkpoint_root is not None:
            checkpoint=torch.load(checkpoint_root/f"seed{seed}_P_C2_meta/checkpoint.pt",map_location="cpu",weights_only=True)
            model.load_state_dict(checkpoint["state_dict"])
        model=model.to(device=device,dtype=torch.float64)
        for index in range(probe_count):
            records.append(probe_episode(model,training_episode(world,seed,index),seed,index))
    result={"phase":"initial" if checkpoint_root is None else "final", "dtype":"float64","device":device,
            "parameter":PARAMETER,"epsilons":list(EPSILONS),"probe_training_episodes_per_seed":probe_count,
            "summary":summarize_probes(records),"per_seed":{str(seed):summarize_probes([row for row in records if row["seed"]==seed]) for seed in config["seeds"]},
            "records":records}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    return result
