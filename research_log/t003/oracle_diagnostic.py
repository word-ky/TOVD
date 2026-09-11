"""ORACLE DIAGNOSTICS ONLY: labels/IDs are never used by deployable TTT.

No model parameter or checkpoint is mutated. Normal T001/T002 code is reused.
"""

import torch
from torch.func import functional_call
from torch.nn import functional as F

from tovd.synthetic.benchmark import outer_metrics

ETAS = (0.0, 0.01, 0.025, 0.05, 0.10)


def flatten(gradients):
    return torch.cat([g.reshape(-1) for g in gradients])


def gradient_relation(left, right):
    a, b = flatten(left), flatten(right)
    return {"cosine": F.cosine_similarity(a.unsqueeze(0), b.unsqueeze(0)).item(),
            "dot": torch.dot(a, b).item(), "gradient_norm": a.norm().item(),
            "task_gradient_norm": b.norm().item()}


def oracle_preupdate(model, episode):
    """At W0: independent label-free inner and oracle query-task gradients."""
    memory = model.memory
    params = {name: p.detach().clone().requires_grad_(True)
              for name, p in memory.fast_model.named_parameters()}
    keys = memory.key_projection(episode.X).detach()
    queries = memory.query_projection(episode.Q).detach()
    target = memory.inner_targets(keys.unsqueeze(0), episode.X.unsqueeze(0),
                                  episode.T.unsqueeze(0))[0].detach()
    pred = functional_call(memory.fast_model, params, (keys,))
    token_losses = 1 - F.cosine_similarity(pred, target, dim=-1)
    inner = torch.autograd.grad(token_losses.mean(), tuple(params.values()), retain_graph=True)
    query_output = functional_call(memory.fast_model, params, (queries,))
    logits = model.logits(query_output.unsqueeze(0), episode.T.unsqueeze(0))[0]
    task_loss = F.cross_entropy(logits, episode.labels)
    task = torch.autograd.grad(task_loss, tuple(params.values()))
    return {"params": params, "keys": keys, "queries": queries, "target": target,
            "token_losses": token_losses, "g_inner": inner, "g_task": task}


def oracle_evaluate_update(model, episode, context, gradients, eta):
    """Update uses supplied gradient only; labels are for offline scoring."""
    params = {name: p - eta * g for (name, p), g in zip(context["params"].items(), gradients)}
    with torch.no_grad():
        output = functional_call(model.memory.fast_model, params, (context["queries"],))
        similarities = model.similarities(output.unsqueeze(0), episode.T.unsqueeze(0))
        logits = similarities / model.classifier_temperature
        row = outer_metrics(logits, similarities, episode.labels.unsqueeze(0))
        per_query = F.cross_entropy(logits[0], episode.labels, reduction="none")
        row["query_nll"] = per_query.tolist()
        row["update_norm"] = eta * flatten(gradients).norm().item()
    return row, output


def paired_changes(after, before):
    result = {**after}
    for metric in ("accuracy", "nll", "margin"):
        result[metric + "_delta"] = after[metric] - before[metric]
    changes = [a - b for a, b in zip(after["query_nll"], before["query_nll"])]
    result["query_nll_delta"] = changes
    result["episode_nll_improves"] = float(result["nll_delta"] < 0)
    result["query_nll_improves_fraction"] = sum(value < 0 for value in changes) / len(changes)
    return result


def oracle_token_masks(episode):
    return {"foreground": torch.isin(episode.image_ids, episode.vocabulary_ids),
            "distractor": (episode.image_ids >= 0) & ~torch.isin(episode.image_ids, episode.vocabulary_ids),
            "background": episode.image_ids == -1}


def oracle_target_ambiguity(model, episode, context, masks):
    with torch.no_grad():
        assignments = torch.softmax(context["keys"] @ episode.T.T / model.memory.tau, dim=-1)
        target = assignments @ episode.T
        top = assignments.topk(2, dim=-1).values
        base = {"entropy": -(assignments * assignments.clamp_min(1e-12).log()).sum(-1),
                "top1_probability": top[:, 0], "top1_top2_gap": top[:, 0] - top[:, 1],
                "target_norm": target.norm(dim=-1)}
        result = {name: {key: tensor[mask].tolist() for key, tensor in base.items()}
                  for name, mask in masks.items()}
        fg = masks["foreground"]
        correct_index = (episode.image_ids[fg, None] == episode.vocabulary_ids[None, :]).long().argmax(-1)
        similarities = F.normalize(target[fg], dim=-1) @ F.normalize(episode.T, dim=-1).T
        correct = similarities.gather(-1, correct_index[:, None]).squeeze(-1)
        wrong = similarities.clone()
        wrong.scatter_(-1, correct_index[:, None], -torch.inf)
        strongest_wrong = wrong.max(-1).values
        result["foreground"].update({
            "target_correct_cosine": correct.tolist(),
            "target_strongest_wrong_cosine": strongest_wrong.tolist(),
            "target_cosine_margin": (correct - strongest_wrong).tolist(),
            "assignment_correct": (assignments[fg].argmax(-1) == correct_index).float().tolist(),
        })
    return result


def oracle_diagnose_episode(model, episode):
    """D1-D4 for one original T002 held-out episode (P or B2 checkpoint)."""
    model.eval()
    context = oracle_preupdate(model, episode)
    before, _ = oracle_evaluate_update(model, episode, context, context["g_inner"], 0.0)
    eta_records = {}
    outputs = {}
    for eta in ETAS:
        after, output = oracle_evaluate_update(model, episode, context, context["g_inner"], eta)
        eta_records[str(eta)] = paired_changes(after, before)
        outputs[eta] = output
    normal = model(episode.X.unsqueeze(0), episode.T.unsqueeze(0), episode.Q.unsqueeze(0))
    relation = gradient_relation(context["g_inner"], context["g_task"])
    alignment = {**relation, "predicted_task_nll_delta": -0.05 * relation["dot"],
                 "actual_task_nll_delta": eta_records["0.05"]["nll_delta"],
                 "episode_nll_improves": eta_records["0.05"]["episode_nll_improves"],
                 "query_nll_improves_fraction": eta_records["0.05"]["query_nll_improves_fraction"],
                 "positive_alignment": float(relation["dot"] > 0),
                 "normal_output_max_error": (outputs[0.05] - normal.tokens[0]).abs().max().item()}
    record = {"oracle_diagnostic": True, "alignment": alignment, "eta": eta_records,
              "inner_loss_before": context["token_losses"].mean().item()}
    if model.method == "P":
        masks = oracle_token_masks(episode)
        groups, gradients = {}, {}
        all_vector = flatten(context["g_inner"])
        for name, mask in masks.items():
            grad = torch.autograd.grad(context["token_losses"][mask].mean(),
                                       tuple(context["params"].values()), retain_graph=True)
            gradients[name] = grad
            weight = mask.float().mean().item()
            weighted_vector = weight * flatten(grad)
            groups[name] = {**gradient_relation(grad, context["g_task"]),
                            "token_count": mask.sum().item(), "token_weight": weight,
                            "weighted_gradient_norm": weighted_vector.norm().item(),
                            "weighted_task_dot": torch.dot(weighted_vector, flatten(context["g_task"])).item(),
                            "all_gradient_projection_fraction": (torch.dot(weighted_vector, all_vector) /
                                                                  all_vector.square().sum().clamp_min(1e-12)).item()}
        reconstruction = sum(groups[name]["token_weight"] * flatten(grad) for name, grad in gradients.items())
        pairwise = {a + "__" + b: gradient_relation(gradients[a], gradients[b])["cosine"]
                    for a, b in (("foreground", "distractor"), ("foreground", "background"),
                                 ("distractor", "background"))}
        fg = masks["foreground"]
        correct_index = (episode.image_ids[fg, None] == episode.vocabulary_ids[None, :]).long().argmax(-1)
        exact_target = episode.T[correct_index]
        exact_pred = functional_call(model.memory.fast_model, context["params"], (context["keys"][fg],))
        exact_loss = (1 - F.cosine_similarity(exact_pred, exact_target, dim=-1)).mean()
        exact_grad = torch.autograd.grad(exact_loss, tuple(context["params"].values()))
        groups["foreground_exact_text"] = gradient_relation(exact_grad, context["g_task"])
        variants = {"all_soft": eta_records["0.05"]}
        for name, grad in (("foreground_soft", gradients["foreground"]), ("foreground_exact_text", exact_grad)):
            after, _ = oracle_evaluate_update(model, episode, context, grad, 0.05)
            variants[name] = paired_changes(after, before)
        record["decomposition"] = {"groups": groups, "pairwise_cosines": pairwise,
                                   "weighted_reconstruction_max_error": (reconstruction - all_vector).abs().max().item()}
        record["oracle_variants"] = variants
        record["ambiguity_tokens"] = oracle_target_ambiguity(model, episode, context, masks)
    return record
