import copy

import pytest

from research_log.t008.statistics import auroc,interpretation_gate,loso,ranks,spearman


def test_tied_rank_auc_and_undefined_cases():
    assert ranks([1,1,3,2])==[1.5,1.5,4,3]
    assert auroc([0,.5,.5,1],[False,True,False,True])==.875
    assert auroc([2,2,2,2],[False,True,False,True])==.5
    assert auroc([0,1],[True,True]) is None
    assert spearman([0,1,2],[2,1,0])==pytest.approx(-1)
    assert spearman([0,0,1],[0,0,1])==pytest.approx(1)
    assert spearman([1,1,1],[0,1,2]) is None


def fixture(regime_only=False):
    rows=[]
    for seed in (7,17,27):
        for branch in ("P_O0_resume","P_C2_warm"):
            for regime in ("easy","hard"):
                for i in range(10):
                    harm=i<(9 if regime=="easy" else 1)
                    rows.append({"seed":seed,"branch":branch,"regime":regime,"primary_unique":True,
                                 "query_entropy":float(regime=="easy") if regime_only else float(harm),
                                 "delta_nll":.1 if harm else -.1})
    return rows


def test_loso_orientation_excludes_test_seed_and_uses_same_sign_within_regime():
    rows=fixture()
    for row in rows:
        if row["seed"]==27:
            row["query_entropy"]=1-row["query_entropy"]
    fold=next(x for x in loso(rows,"query_entropy") if x["held_seed"]==27)
    assert fold["orientation_train_seeds"]==[7,17]
    assert fold["orientation"]==1
    assert all(fold[r]["auroc"]==0 for r in ("overall","easy","hard"))
    modified=copy.deepcopy(rows)
    for row in modified:
        if row["seed"]==27:
            row["delta_nll"]*=-1
    changed=next(x for x in loso(modified,"query_entropy") if x["held_seed"]==27)
    assert changed["orientation"]==fold["orientation"]
    assert changed["orientation_train_auroc"]==fold["orientation_train_auroc"]
    assert changed["overall"]["auroc"]==1


def test_regime_confound_fails_gate_while_within_regime_scalar_can_pass():
    rows=fixture(regime_only=True)
    result=interpretation_gate(rows,"query_entropy",loso(rows,"query_entropy"))
    assert result["overall_threshold_passes"]
    assert not result["easy_threshold_passes"]
    assert not result["passes"]
    rows=fixture()
    result=interpretation_gate(rows,"query_entropy",loso(rows,"query_entropy"))
    assert result["passes"]
    assert result["overall_loso"]["mean"]==1
    assert result["easy_loso"]["mean"]==1
