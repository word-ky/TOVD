"""Preregistered scalar-only ranking audit. No learned gate or feature threshold."""

import math
import statistics

from .schema import FEATURES,FEATURE_METADATA


def ranks(values):
    order=sorted(range(len(values)),key=values.__getitem__)
    result=[0.0]*len(values)
    start=0
    while start<len(order):
        end=start+1
        while end<len(order) and values[order[end]]==values[order[start]]:
            end+=1
        rank=(start+1+end)/2
        for index in order[start:end]:
            result[index]=rank
        start=end
    return result


def spearman(x,y):
    a,b=ranks(x),ranks(y)
    ma,mb=statistics.mean(a),statistics.mean(b)
    va=sum((v-ma)**2 for v in a)
    vb=sum((v-mb)**2 for v in b)
    return sum((v-ma)*(w-mb) for v,w in zip(a,b))/math.sqrt(va*vb) if va and vb else None


def auroc(scores,harm):
    positive=sum(harm)
    negative=len(harm)-positive
    if not positive or not negative:
        return None
    return (sum(rank for rank,label in zip(ranks(scores),harm) if label)-positive*(positive+1)/2)/(positive*negative)


def stats_for(rows,feature):
    x=[row[feature] for row in rows]
    y=[row["delta_nll"] for row in rows]
    return {"count":len(rows),"harm_count":sum(v>0 for v in y),"harm_gt_005_count":sum(v>.05 for v in y),
            "spearman":spearman(x,y),"auroc_harm":auroc(x,[v>0 for v in y]),
            "auroc_harm_gt_005":auroc(x,[v>.05 for v in y])}


def loso(rows,feature,threshold=0):
    """All fold orientations are trained on the other seeds, never the test seed."""
    result=[]
    seeds=sorted({row["seed"] for row in rows})
    for held in seeds:
        train=[row for row in rows if row["seed"]!=held]
        test=[row for row in rows if row["seed"]==held]
        train_auc=auroc([r[feature] for r in train],[r["delta_nll"]>threshold for r in train])
        orientation=None if train_auc is None else (1 if train_auc>=.5 else -1)
        fold={"held_seed":held,"orientation_train_seeds":[s for s in seeds if s!=held],
              "orientation_train_count":len(train),"orientation_train_auroc":train_auc,"orientation":orientation,
              "harm_threshold":threshold}
        for regime in ("overall","easy","hard"):
            subset=test if regime=="overall" else [row for row in test if row["regime"]==regime]
            fold[regime]={"count":len(subset),"harm_count":sum(r["delta_nll"]>threshold for r in subset),
                          "auroc":auroc([orientation*r[feature] for r in subset],[r["delta_nll"]>threshold for r in subset]) if orientation is not None else None}
        result.append(fold)
    return result


def fold_summary(folds,regime):
    values=[fold[regime]["auroc"] for fold in folds]
    return {"values":values,"mean":statistics.mean(values) if all(v is not None for v in values) else None,
            "min":min(values) if all(v is not None for v in values) else None}


def interpretation_gate(rows,feature,folds):
    overall=fold_summary(folds,"overall")
    easy=fold_summary(folds,"easy")
    orientations=[f["orientation"] for f in folds]
    consistent=orientations[0] is not None and len(set(orientations))==1
    sign=orientations[0] if consistent else None
    branch_aucs={}
    for branch in ("P_O0_resume","P_C2_warm"):
        for regime in ("overall","easy"):
            subset=[r for r in rows if r["branch"]==branch and (regime=="overall" or r["regime"]==regime)]
            branch_aucs[branch+"/"+regime]=auroc([sign*r[feature] for r in subset],[r["delta_nll"]>0 for r in subset]) if sign is not None else None
    g1=overall["mean"] is not None and overall["mean"]>=.70 and overall["min"]>=.65
    g2=consistent and all(v is not None and v>.5 for v in branch_aucs.values())
    g3=easy["mean"] is not None and easy["mean"]>=.65 and easy["min"]>=.60
    return {"feature":feature,"availability":FEATURE_METADATA[feature]["availability"],
            "overall_loso":overall,"easy_loso":easy,"orientations":orientations,"orientation_consistent":consistent,
            "branch_oriented_aurocs":branch_aucs,"overall_threshold_passes":g1,"direction_passes":g2,
            "easy_threshold_passes":g3,"passes":g1 and g2 and g3}


def quantile(values,p):
    ordered=sorted(values)
    position=(len(ordered)-1)*p
    lo=int(position)
    hi=min(lo+1,len(ordered)-1)
    return ordered[lo]+(ordered[hi]-ordered[lo])*(position-lo)


def distribution(values):
    return {"mean":statistics.mean(values),"median":statistics.median(values),
            "q25":quantile(values,.25),"q75":quantile(values,.75)}


def analyze(rows):
    primary=[row for row in rows if row["primary_unique"]]
    scopes={"primary/overall":primary,"full_grid/overall":rows}
    for regime in ("easy","hard"):
        scopes["primary/"+regime]=[r for r in primary if r["regime"]==regime]
        scopes["full_grid/"+regime]=[r for r in rows if r["regime"]==regime]
    for label in sorted({r["branch"] for r in rows}):
        for regime in ("overall","easy","hard"):
            scopes[f"branch/{label}/{regime}"]=[r for r in rows if r["branch"]==label and (regime=="overall" or r["regime"]==regime)]
    for seed in sorted({r["seed"] for r in rows}):
        for regime in ("overall","easy","hard"):
            scopes[f"seed/{seed}/{regime}"]=[r for r in primary if r["seed"]==seed and (regime=="overall" or r["regime"]==regime)]
        for branch in ("P_O0_resume","P_C2_warm"):
            for regime in ("overall","easy","hard"):
                scopes[f"seed_branch/{seed}/{branch}/{regime}"]=[r for r in rows if r["seed"]==seed and r["branch"]==branch and (regime=="overall" or r["regime"]==regime)]
    for state in sorted({r["state_id"] for r in rows}):
        for regime in ("easy","hard"):
            scopes[f"state/{state}/{regime}"]=[r for r in rows if r["state_id"]==state and r["regime"]==regime]
    single=[{"scope":scope,"feature":feature,**stats_for(records,feature)} for scope,records in scopes.items() for feature in FEATURES]
    folds={feature:{"primary":loso(primary,feature),"sensitivity_gt_005":loso(primary,feature,.05)} for feature in FEATURES}
    gates={feature:interpretation_gate(rows,feature,folds[feature]["primary"]) for feature in FEATURES}
    localization=[]
    for scope,records in scopes.items():
        if not(scope.startswith("primary/") or scope.startswith("branch/")):
            continue
        for group in ("harm","benefit","neutral"):
            selected=[r for r in records if (r["delta_nll"]>0 if group=="harm" else r["delta_nll"]<0 if group=="benefit" else r["delta_nll"]==0)]
            if selected:
                localization.append({"scope":scope,"outcome_group":group,"count":len(selected),
                                     "features_and_drift":{f:distribution([r[f] for r in selected]) for f in (*FEATURES,"drift_W0","drift_key","drift_query","drift_total")}})
    signs=[]
    for scope,records in scopes.items():
        if not scope.startswith("state/"):
            continue
        first=records[0]
        delta=statistics.mean(r["delta_nll"] for r in records)
        signs.append({"state_id":first["state_id"],"seed":first["seed"],"branch":first["branch"],"step":first["step"],"regime":first["regime"],
                      "count":len(records),"mean_delta_nll":delta,"sign":"harm" if delta>0 else "benefit" if delta<0 else "neutral",
                      **{metric:statistics.mean(r[metric] for r in records) for metric in ("before_accuracy","after_accuracy","before_nll","after_nll","delta_accuracy")}})
    consistency={}
    for feature in FEATURES:
        full=next(r for r in single if r["scope"]=="primary/overall" and r["feature"]==feature)
        sign=None if full["auroc_harm"] is None else (1 if full["auroc_harm"]>=.5 else -1)
        consistency[feature]={"descriptive_orientation":sign}
        for kind in ("seed/","seed_branch/","state/"):
            selected=[r for r in single if r["feature"]==feature and r["scope"].startswith(kind)]
            aucs=[r["auroc_harm"] if sign==1 else 1-r["auroc_harm"] for r in selected if r["auroc_harm"] is not None and sign is not None]
            rhos=[r["spearman"]*sign for r in selected if r["spearman"] is not None and sign is not None]
            consistency[feature][kind]={"auc_defined":len(aucs),"auc_direction_agree":sum(x>.5 for x in aucs),
                                        "rho_defined":len(rhos),"rho_direction_agree":sum(x>0 for x in rhos)}
    return {"primary_rows":len(primary),"full_grid_rows":len(rows),"single_features":single,"loso":folds,"gates":gates,
            "passing_pre_features":[f for f,g in gates.items() if g["passes"] and g["availability"]=="pre_update"],
            "passing_rollback_features":[f for f,g in gates.items() if g["passes"] and g["availability"]=="post_candidate_rollback"],
            "sign_map":signs,"localization":localization,"direction_consistency":consistency}
