"""Render fixed T008 audit receipts without importing PyTorch or fitting policies."""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil

from .schema import FEATURES,PRE_FEATURES

TASK=Path(__file__).resolve().parent
ROOT=TASK.parents[1]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def csv_write(path,rows):
    with path.open("w",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def f(value):
    return "undefined" if value is None else f"{value:.4f}"


def save_figure(fig,name):
    fig.savefig(TASK/f"{name}.png",dpi=160)
    fig.savefig(TASK/f"{name}.svg")
    path=TASK/f"{name}.svg"
    path.write_text("\n".join(line.rstrip() for line in path.read_text(encoding="utf-8").splitlines())+"\n",encoding="utf-8")


def plots(data,rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    states=[("original_P",0),*[(b,s) for b in ("P_O0_resume","P_C2_warm") for s in (0,50,100,200,400)]]
    labels=["Original"]+[f"W{b+1} / {s}" for b in range(2) for s in (0,50,100,200,400)]
    seeds=(7,17,27)
    bound=max(abs(x["mean_delta_nll"]) for x in data["sign_map"])
    fig,axes=plt.subplots(2,1,figsize=(14,6),layout="constrained")
    for ax,regime in zip(axes,("easy","hard")):
        values=np.array([[next(x["mean_delta_nll"] for x in data["sign_map"] if x["seed"]==seed and x["branch"]==b and x["step"]==s and x["regime"]==regime)
                          for b,s in states] for seed in seeds])
        im=ax.imshow(values,cmap="RdBu_r",vmin=-bound,vmax=bound,aspect="auto")
        ax.set_xticks(range(len(labels)),labels,rotation=30,ha="right")
        ax.set_yticks(range(3),[f"Seed {s}" for s in seeds])
        ax.set_title(f"{regime.capitalize()} · mean task NLL delta (candidate minus W0)")
        for i in range(3):
            for j in range(len(states)):
                ax.text(j,i,f"{values[i,j]:+.3f}",ha="center",va="center",fontsize=8,color="white" if abs(values[i,j])>bound*.6 else "black")
    fig.colorbar(im,ax=axes,label="Negative = benefit; positive = harm",shrink=.8)
    fig.suptitle("T008 fixed checkpoint sign map · no checkpoint selection",fontsize=15)
    save_figure(fig,"sign_map")
    plt.close(fig)
    fig,axes=plt.subplots(4,4,figsize=(16,12),layout="constrained")
    for ax,feature in zip(axes.flat,FEATURES):
        for regime,color in (("easy","#c36b26"),("hard","#357eac")):
            subset=[r for r in rows if r["regime"]==regime and r["primary_unique"]]
            ax.scatter([r[feature] for r in subset],[r["delta_nll"] for r in subset],s=3,alpha=.17,color=color,
                       rasterized=True,label=regime)
        ax.axhline(0,color="#555555",linewidth=.6)
        ax.set(title=feature,xlabel="Raw scalar value",ylabel="Task NLL delta")
        ax.grid(alpha=.12)
    for ax in list(axes.flat)[len(FEATURES):]:
        ax.set_visible(False)
    handles,labels=axes[0,0].get_legend_handles_labels()
    fig.legend(handles,labels,loc="lower right",frameon=False,markerscale=4)
    fig.suptitle("T008 label-free feature geometry · 5400 unique-state episode rows\nAll 14 preregistered scalars; no fitted gate or selected feature threshold",fontsize=15)
    save_figure(fig,"feature_geometry")
    plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(13,8),sharey=True,layout="constrained")
    for ax,regime,threshold in zip(axes,("overall","easy"),(.70,.65)):
        for i,feature in enumerate(FEATURES):
            folds=data["loso"][feature]["primary"]
            for fold,color in zip(folds,("#2878b5","#d97925","#38905b")):
                if fold[regime]["auroc"] is not None:
                    ax.plot(fold[regime]["auroc"],i,"o",color=color,markersize=5)
        ax.axvline(.5,color="gray",linestyle=":")
        ax.axvline(threshold,color="black",linestyle="--",label="Mean requirement")
        ax.set(xlim=(0,1),title=f"{regime.capitalize()} · held-out-seed AUROC",xlabel="Orientation fixed from the other two seeds")
        ax.set_yticks(range(len(FEATURES)),[f"{'Pre' if x in PRE_FEATURES else 'Post'}: {x}" for x in FEATURES])
        ax.grid(alpha=.15)
    axes[0].invert_yaxis()
    from matplotlib.lines import Line2D
    axes[1].legend([Line2D([],[],marker="o",linestyle="",color=c) for c in ("#2878b5","#d97925","#38905b")],
                   ["Seed 7","Seed 17","Seed 27"],loc="upper right",frameon=False,fontsize=9)
    fig.suptitle("T008 single-scalar generalization · dots = seeds 7 / 17 / 27\nWithin-easy uses the same pooled-training orientation; no regime-specific reorientation",fontsize=14)
    save_figure(fig,"loso_auroc")
    plt.close(fig)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--run",type=Path,required=True)
    args=parser.parse_args()
    source=args.run/"artifacts/t008"
    data=read_json(source/"results.json")
    for name in ("results.json","gates.json","checks.json","schema.json","episodes.csv"):
        shutil.copyfile(source/name,TASK/name)
    with (source/"episodes.csv").open(encoding="utf-8",newline="") as handle:
        rows=list(csv.DictReader(handle))
    for row in rows:
        row["primary_unique"]=row["primary_unique"]=="True"
        for key in (*FEATURES,"delta_nll","delta_accuracy"):
            row[key]=float(row[key])
    csv_write(TASK/"single_features.csv",data["single_features"])
    csv_write(TASK/"sign_map.csv",data["sign_map"])
    gate_rows=[]
    for feature,g in data["gates"].items():
        gate_rows.append({"feature":feature,"availability":g["availability"],"overall_mean":g["overall_loso"]["mean"],
                          "overall_min":g["overall_loso"]["min"],"easy_mean":g["easy_loso"]["mean"],"easy_min":g["easy_loso"]["min"],
                          "orientations":json.dumps(g["orientations"]),**g["branch_oriented_aurocs"],
                          "overall_pass":g["overall_threshold_passes"],"direction_pass":g["direction_passes"],"easy_pass":g["easy_threshold_passes"],"passes":g["passes"]})
    csv_write(TASK/"gates.csv",gate_rows)
    fold_rows=[]
    for feature,analyses in data["loso"].items():
        for analysis,folds in analyses.items():
            for fold in folds:
                fold_rows.append({"feature":feature,"analysis":analysis,"held_seed":fold["held_seed"],"orientation":fold["orientation"],
                                  "training_seeds":json.dumps(fold["orientation_train_seeds"]),"training_count":fold["orientation_train_count"],
                                  "training_auroc":fold["orientation_train_auroc"],"harm_threshold":fold["harm_threshold"],
                                  **{regime+"_"+k:v for regime in ("overall","easy","hard") for k,v in fold[regime].items()}})
    csv_write(TASK/"loso.csv",fold_rows)
    localization=[{"scope":r["scope"],"group":r["outcome_group"],"count":r["count"],"quantity":key,**value}
                  for r in data["localization"] for key,value in r["features_and_drift"].items()]
    csv_write(TASK/"localization.csv",localization)
    consistency=[{"feature":feature,"orientation":value["descriptive_orientation"],"scope_kind":kind,**record}
                 for feature,value in data["direction_consistency"].items() for kind,record in value.items() if kind!="descriptive_orientation"]
    csv_write(TASK/"direction_consistency.csv",consistency)
    pre,post=data["passing_pre_features"],data["passing_rollback_features"]
    lines=["# T008 state-dependent adaptation observability audit","",
           f"Run `{args.run.name}`; tested `{data['environment']['revision']}`; preregistration `c163c78`.","",
           f"Validity: **{'PASS' if data['validity']['passes'] else 'FAIL'}**. Passing pre-update scalars: **{', '.join(pre) if pre else 'none'}**. Passing post-candidate scalars: **{', '.join(post) if post else 'none'}**.","",
           "A passing scalar supports only a future preregistered selective/rollback diagnosis-to-policy task; no gate, threshold, controller or detector was implemented here." if pre or post else
           "No single preregistered label-free scalar passes. Do not fit a rescue controller; current simple runtime geometry does not meet the required harm-observability standard.","",
           "33 frozen states x100 easy+100 hard episodes =6600 full rows. Primary5400 rows count the identical original/W1step0/W2step0 state only once perseed. Full-grid weighting sensitivity is also reported.",
           "Spearman/AUROC use average ties. Positive score means harm in un-oriented tables; LOSO orientation comes only from the other2 seeds and is reused within easy/hard.",
           "Three seeds, reused observations and14 planned scalar comparisons: these are diagnostic results, not independent confirmation of a deployable safety policy.","",
           "The strongest primary overall LOSO mean is post-candidate relative_inner_reduction:0.580556, folds0.638526/0.612029/0.491113. Best pre-update mean is gradient_norm:0.538529. Every feature fails the original overall.70/.65 requirement, so the negative conclusion does not depend on the extra quantification of within-easy nontriviality.",
           "Within-easy descriptive query_probability_gap AUROC is.711724 (max probability.704789), but pooled-training fold orientations are[+1,+1,-1]; its easy fold AUROCs are.738984/.689356/.278598. Do not reorient using the held-out fold or reinterpret this as a validated easy-only policy.",
           "The Delta_NLL>.05 sensitivity also remains weak: highest mean overallLOSO.559274 (relative_inner_reduction). Full-grid un-oriented correlations/AUROCs are close to the unique-state analysis; no duplicate weighting rescue is claimed.","",
           "## Scalar interpretation gate","",
           "Overall meanLOSO>=.70 and everyfold>=.65; easy mean>=.65 and everyfold>=.60; identical fold orientation and oriented W1/W2 AUROC>.5 overall/within easy.",
           "Gradient norm is pre-update but requires an inner backward pass. Every post-candidate scalar requires paying for C2 and could only support rollback.","",
           "| Feature | Availability | Overall mean / min | Easy mean / min | Fold signs | Overall | Direction | Easy | Pass |",
           "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for feature,g in data["gates"].items():
        lines.append(f"| {feature} | {'pre' if feature in PRE_FEATURES else 'post/rollback'} | {f(g['overall_loso']['mean'])} / {f(g['overall_loso']['min'])} | {f(g['easy_loso']['mean'])} / {f(g['easy_loso']['min'])} | {g['orientations']} | {g['overall_threshold_passes']} | {g['direction_passes']} | {g['easy_threshold_passes']} | **{g['passes']}** |")
    lines += ["","## Primary un-oriented single-feature relationships","",
              "Higher feature value predicts harm for AUROC>.5 and positive Spearman; inverse features can be oriented using training seeds only.","",
              "| Feature | Overall rho / AUROC | Easy rho / AUROC | Hard rho / AUROC | Full-grid AUROC |", "| --- | --- | --- | --- | --- |"]
    for feature in FEATURES:
        entries=[next(r for r in data["single_features"] if r["feature"]==feature and r["scope"]==scope)
                 for scope in ("primary/overall","primary/easy","primary/hard","full_grid/overall")]
        cells=[f"{f(r['spearman'])} / {f(r['auroc_harm'])}" for r in entries[:3]]
        lines.append(f"| {feature} | "+" | ".join(cells)+f" | {f(entries[3]['auroc_harm'])} |")
    lines += ["","## Leave-one-seed-out primary and sensitivity","",
              "Sensitivity harm=Delta_NLL>.05 has its own training-seed orientation. It never determines the primary gate.","",
              "| Feature | Harm definition | Held seed | Train sign | Overall AUC | Easy AUC | Hard AUC |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for feature,analyses in data["loso"].items():
        for name,folds in analyses.items():
            for fold in folds:
                lines.append(f"| {feature} | {name} | {fold['held_seed']} | {fold['orientation']} | {f(fold['overall']['auroc'])} | {f(fold['easy']['auroc'])} | {f(fold['hard']['auroc'])} |")
    lines += ["","## Fixed checkpoint sign map","",
              "All snapshots diagnostic; no method/checkpoint selected. Accuracy is percent.","",
              "| Branch | Seed | Step | Regime | W0 acc | C2 acc | W0 NLL | C2 NLL | Delta NLL | Sign |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in data["sign_map"]:
        lines.append(f"| {r['branch']} | {r['seed']} | {r['step']} | {r['regime']} | {100*r['before_accuracy']:.3f} | {100*r['after_accuracy']:.3f} | {r['before_nll']:.6f} | {r['after_nll']:.6f} | {r['mean_delta_nll']:+.6f} | {r['sign']} |")
    lines += ["","## Failure localization","",
              "Groups use task labels only offline. Values below are group means; full medians/quartiles and branch-stratified values in localization.csv. Drift is not a candidate predictor.","",
              "| Regime | Group | Count | Query entropy | Max probability | Assignment entropy | Normalized update | Representation shift | Relative inner reduction | Query JS | Drift W0 |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in data["localization"]:
        if r["scope"] not in ("primary/easy","primary/hard"):
            continue
        keys=("query_entropy","query_max_probability","assignment_entropy","normalized_update","representation_shift","relative_inner_reduction","query_js","drift_W0")
        lines.append(f"| {r['scope']} | {r['outcome_group']} | {r['count']} | "+" | ".join(f(r["features_and_drift"][k]["mean"]) for k in keys)+" |")
    lines += ["",
              "Easy harm is associated descriptively with more confident W0 (max probability.886158 vs.814840; entropy.342544 vs.476213). Its normalized update/representation shift are slightly larger (.023671/.477821 vs.021180/.431671).",
              "However, harmful easy episodes have smaller predictive JS (.079785 vs.090923), fewer changed top1 predictions (.191927 vs.269141), and smaller relative inner descent (.108913 vs.126109). Thus confident-W0 overspecialization is only a partial qualitative explanation; a universal confident-plus-large-predictive-change detector is not supported by these quantities or the LOSO gate.",
              "Easy W1 seeds7/17 change from beneficial initial means to harmful step400 means (+.365164/+.277746). Easy seed27 is already harmful at the original state (+.131193); W2 remains harmful at every saved step. All33 hard state/regime means remain beneficial, despite1148/2700 unique hard episodes being individually harmful.",
              "Primary harm prevalence:2235/5400 overall,1087/2700 easy,1148/2700 hard; no exactly neutral episodes. State-average benefit does not determine the sign for an individual episode."]
    lines += ["","## Validity and artifact contract","","```json",json.dumps(data["validity"],indent=2),"```","",
              "Original/T005 and all T007 trajectory metrics/episode identities replayed; schema explicitly separates14 label-free predictors from outcomes/metadata.",
              "Complete per-episode W0/C2 tokens, query probabilities, candidate diagnostics, labels/IDs and oracle-on/off checks are in original run records/. Parameters/checkpoints never train or mutate.",
              "All gate conditions were fixed before correlation outcomes. Constant correlations/single-class AUROCs are undefined, not substituted with favorable values.",
              "No p-values or independent-row confidence intervals; folds split entire seeds. A future policy would need training-only calibration and separate validation.","",
              "![Fixed sign map](sign_map.png)","","![Feature geometry](feature_geometry.png)","","![LOSO AUROC](loso_auroc.png)",""]
    (TASK/"RESULTS.md").write_text("\n".join(lines),encoding="utf-8")
    manifest=[{"path":str(p.relative_to(ROOT)).replace('\\','/'),"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
              for p in sorted(args.run.rglob("*")) if p.is_file()]
    save={"run":args.run.name,"validity":data["validity"],"raw_record_files":len(list((source/"records").glob("*.json"))),
          "raw_row_count":len(rows),"primary_row_count":sum(r["primary_unique"] for r in rows),"artifact_manifest":manifest}
    (TASK/"verification.json").write_text(json.dumps(save,indent=2)+"\n",encoding="utf-8")
    plots(data,rows)
    print(json.dumps({"validity":data["validity"],"pre":pre,"rollback":post},indent=2))


if __name__=="__main__":
    main()
