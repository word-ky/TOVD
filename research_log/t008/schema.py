"""Audit schema without tensor/plotting dependencies."""

PRE_FEATURES=("query_entropy","query_max_probability","query_probability_gap",
              "assignment_entropy","assignment_probability_gap","inner_loss_before","gradient_norm")
POST_FEATURES=("chosen_eta","backtracking_trials","normalized_update","representation_shift",
               "relative_inner_reduction","query_js","prediction_changed_fraction")
FEATURES=PRE_FEATURES+POST_FEATURES
FEATURE_METADATA={name:{"is_label_free_feature":True,"availability":"pre_update" if name in PRE_FEATURES else "post_candidate_rollback"}
                  for name in FEATURES}
FEATURE_METADATA["gradient_norm"]["compute_note"]="Requires raw inner backward pass, but no candidate step/selection."
