# T005 frozen O1 step-control diagnosis

C2 passes the preregistered descent-safe and task-useful rules. C1 fails the full scale-rescue rule because hard NLL and accuracy both worsen versus C0 despite a large easy recovery. Recommend Research Lead review a controlled meta-training task for C2; no training starts under T005.

Run 20260912-053826-tovd-t005-a6000; tested code f2b9722ae8a1ad68e0e529488e68f88c170125de; preregistration 7b8949e.

C0 = O1_fixed; C1 = O1_norm_matched; C2 = O1_backtracking. Original O0 and C0 are immutable controls. All metrics below use the same frozen T002 P checkpoints and 600 held-out episodes per method. Task-gradient diagnostics use offline labels only; runtime step selection is label-free. No outer training, objective/temperature/generator change, detector integration or task-label step selection.

Values are mean ± sample SD across seeds 7/17/27; delta is after minus own W0. Full per-seed and pooled distributions in frozen_step_screen.json / aggregate.csv.

## Task before/after

| Method | Regime | W0 accuracy % | W* accuracy % | W0 NLL | W* NLL | ΔNLL | W0 margin | W* margin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| O0 | easy | 77.58333 ± 9.99557 | 74.87500 ± 15.65048 | 0.55592 ± 0.20889 | 0.58611 ± 0.26859 | 0.03019 ± 0.08311 | 0.20719 ± 0.01372 | 0.16221 ± 0.04289 |
| O0 | hard | 40.54167 ± 2.67317 | 39.41667 ± 1.30104 | 1.31390 ± 0.01950 | 1.30265 ± 0.01629 | -0.01126 ± 0.02148 | -0.02650 ± 0.00332 | -0.02215 ± 0.00472 |
| C0 | easy | 77.58333 ± 9.99557 | 39.45833 ± 8.36131 | 0.55592 ± 0.20889 | 3.44824 ± 0.93756 | 2.89232 ± 0.90123 | 0.20719 ± 0.01372 | -0.21379 ± 0.11627 |
| C0 | hard | 40.54167 ± 2.67317 | 41.87500 ± 4.00975 | 1.31390 ± 0.01950 | 1.31014 ± 0.04288 | -0.00377 ± 0.03431 | -0.02650 ± 0.00332 | -0.02518 ± 0.00637 |
| C1 | easy | 77.58333 ± 9.99557 | 74.45833 ± 14.79038 | 0.55592 ± 0.20889 | 0.69309 ± 0.39560 | 0.13717 ± 0.58831 | 0.20719 ± 0.01372 | 0.13271 ± 0.05125 |
| C1 | hard | 40.54167 ± 2.67317 | 39.33333 ± 3.68556 | 1.31390 ± 0.01950 | 1.33918 ± 0.06330 | 0.02527 ± 0.04810 | -0.02650 ± 0.00332 | -0.03049 ± 0.00858 |
| C2 | easy | 77.58333 ± 9.99557 | 86.70833 ± 5.10718 | 0.55592 ± 0.20889 | 0.34449 ± 0.09695 | -0.21143 ± 0.29865 | 0.20719 ± 0.01372 | 0.21315 ± 0.03103 |
| C2 | hard | 40.54167 ± 2.67317 | 46.25000 ± 4.22234 | 1.31390 ± 0.01950 | 1.23536 ± 0.02569 | -0.07854 ± 0.00647 | -0.02650 ± 0.00332 | -0.01270 ± 0.00365 |

## Direction and realized update

| Method | Regime | Raw task cosine | Raw task dot | Objective gradient norm | Raw O1 norm | Actual update norm | Realized direction cosine |
| --- | --- | --- | --- | --- | --- | --- | --- |
| O0 | easy | 0.01111 ± 0.05037 | 1.18704 ± 1.85458 | 3.58560 ± 0.47813 | 14.05324 ± 4.18088 | 0.17928 ± 0.02391 | 0.01111 ± 0.05037 |
| O0 | hard | -0.01116 ± 0.02564 | 0.17602 ± 0.87352 | 4.05984 ± 0.34706 | 3.68140 ± 0.53849 | 0.20299 ± 0.01735 | -0.01116 ± 0.02564 |
| C0 | easy | 0.41064 ± 0.27873 | 102.09002 ± 74.51081 | 14.05324 ± 4.18088 | 14.05324 ± 4.18088 | 0.70266 ± 0.20904 | 0.41064 ± 0.27873 |
| C0 | hard | 0.25091 ± 0.04571 | 10.17679 ± 3.83358 | 3.68140 ± 0.53849 | 3.68140 ± 0.53849 | 0.18407 ± 0.02692 | 0.25091 ± 0.04571 |
| C1 | easy | 0.41064 ± 0.27873 | 102.09002 ± 74.51081 | 14.05324 ± 4.18088 | 14.05324 ± 4.18088 | 0.17928 ± 0.02391 | 0.41064 ± 0.27873 |
| C1 | hard | 0.25091 ± 0.04571 | 10.17679 ± 3.83358 | 3.68140 ± 0.53849 | 3.68140 ± 0.53849 | 0.20299 ± 0.01735 | 0.25091 ± 0.04571 |
| C2 | easy | 0.41064 ± 0.27873 | 102.09002 ± 74.51081 | 14.05324 ± 4.18088 | 14.05324 ± 4.18088 | 0.09649 ± 0.01424 | 0.41064 ± 0.27873 |
| C2 | hard | 0.25091 ± 0.04571 | 10.17679 ± 3.83358 | 3.68140 ± 0.53849 | 3.68140 ± 0.53849 | 0.14723 ± 0.01960 | 0.25091 ± 0.04571 |

Raw alignment uses g0 for O0 and g1 for C0/C1/C2. C2 rejected steps still have a raw g1 diagnostic; their realized direction is zero. Effective-direction dot products are in JSON/CSV.

## Inner losses and task improvement fractions

| Method | Regime | O1 loss before | O1 loss after | Own objective after | Episodes improve % | Queries improve % |
| --- | --- | --- | --- | --- | --- | --- |
| O0 | easy | 2.25795 ± 0.39479 | 2.21680 ± 0.38503 | 0.52842 ± 0.24555 | 39.33333 ± 14.64013 | 31.75000 ± 10.51561 |
| O0 | hard | 1.65942 ± 0.02457 | 1.55895 ± 0.04893 | 0.39325 ± 0.18178 | 43.00000 ± 8.54400 | 40.54167 ± 5.49052 |
| C0 | easy | 2.25795 ± 0.39479 | 4.51553 ± 0.44051 | 4.51553 ± 0.44051 | 18.33333 ± 14.04754 | 35.54167 ± 4.00455 |
| C0 | hard | 1.65942 ± 0.02457 | 1.62074 ± 0.05002 | 1.62074 ± 0.05002 | 52.66667 ± 1.52753 | 56.41667 ± 4.84177 |
| C1 | easy | 2.25795 ± 0.39479 | 2.77622 ± 0.44718 | 2.77622 ± 0.44718 | 46.33333 ± 25.48202 | 47.33333 ± 10.31862 |
| C1 | hard | 1.65942 ± 0.02457 | 1.65492 ± 0.06633 | 1.65492 ± 0.06633 | 50.66667 ± 2.08167 | 54.83333 ± 5.11483 |
| C2 | easy | 2.25795 ± 0.39479 | 2.00317 ± 0.31130 | 2.00317 ± 0.31130 | 63.33333 ± 27.42870 | 53.66667 ± 10.33904 |
| C2 | hard | 1.65942 ± 0.02457 | 1.54000 ± 0.01302 | 1.54000 ± 0.01302 | 55.66667 ± 0.57735 | 58.62500 ± 4.76478 |

## C1 step budget

| Method | Regime | Scale | O0 actual budget | Absolute budget error | Guarded fraction |
| --- | --- | --- | --- | --- | --- |
| C1 | easy | 0.29776 ± 0.05673 | 0.17928 ± 0.02391 | 0.00000 ± 0.00000 | 0.00000 ± 0.00000 |
| C1 | hard | 1.33198 ± 0.13599 | 0.20299 ± 0.01735 | 0.00000 ± 0.00000 | 0.00000 ± 0.00000 |

- easy: scale min/p05/median/p95/max = 0.121781 / 0.154129 / 0.272309 / 0.561807 / 0.939717; max budget error 4.47034836e-08.
- hard: scale min/p05/median/p95/max = 0.511429 / 0.643512 / 1.17163 / 2.50407 / 12.2177; max budget error 5.96046448e-08.

## C2 backtracking

| Method | Regime | Chosen eta | Trials | No update fraction | Condition satisfied fraction | RHS minus after-loss |
| --- | --- | --- | --- | --- | --- | --- |
| C2 | easy | 0.00777 ± 0.00135 | 3.89667 ± 0.22053 | 0.00000 ± 0.00000 | 1.00000 ± 0.00000 | 0.25464 ± 0.08574 |
| C2 | hard | 0.03971 ± 0.00437 | 1.42000 ± 0.18193 | 0.00000 ± 0.00000 | 1.00000 ± 0.00000 | 0.11936 ± 0.01183 |

### C2 eta counts by seed/regime

| Seed/regime | Eta: count |
| --- | --- |
| seed7_easy | 0.003125: 6, 0.00625: 76, 0.0125: 14, 0.025: 4 |
| seed7_hard | 0.025: 21, 0.05: 79 |
| seed17_easy | 0.003125: 29, 0.00625: 59, 0.0125: 9, 0.025: 3 |
| seed17_hard | 0.0125: 3, 0.025: 47, 0.05: 50 |
| seed27_easy | 0.003125: 7, 0.00625: 67, 0.0125: 18, 0.025: 6, 0.05: 2 |
| seed27_hard | 0.0125: 2, 0.025: 48, 0.05: 50 |

## Runtime — normal forward only

Physical A6000 GPU 1. Three warmups and three full 100-episode timed passes per seed/regime, GPU synchronization around each pass. Oracle scoring excluded. Other project ran on GPU 0; shared host activity and the sequential measurement order limit interpretation of small timing differences.

| Method | Regime | ms/episode mean ± seed SD | Multiplier vs C0 mean ± seed SD |
| --- | --- | --- | --- |
| O0 | easy | 8.4409 ± 0.0585 | 0.8150 ± 0.0160 |
| O0 | hard | 8.4930 ± 0.0339 | 0.8212 ± 0.0097 |
| C0 | easy | 10.3593 ± 0.1956 | 1.0000 ± 0.0000 |
| C0 | hard | 10.3437 ± 0.1553 | 1.0000 ± 0.0000 |
| C1 | easy | 17.8201 ± 0.5838 | 1.7203 ± 0.0512 |
| C1 | hard | 17.7871 ± 0.6503 | 1.7196 ± 0.0576 |
| C2 | easy | 12.8387 ± 0.7134 | 1.2393 ± 0.0643 |
| C2 | hard | 11.0412 ± 0.1530 | 1.0676 ± 0.0209 |

## Per-seed paired outcomes

| Method | Regime | Seed | Task cosine | ΔNLL | ΔAccuracy pp | Post accuracy % | Post NLL | Post margin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| O0 | easy | 7 | 0.050180 | -0.026848 | 0.500000 | 72.375000 | 0.591787 | 0.183494 |
| O0 | easy | 17 | -0.045739 | 0.125554 | -11.125000 | 60.625000 | 0.851826 | 0.112840 |
| O0 | easy | 27 | 0.028889 | -0.008122 | 2.500000 | 91.625000 | 0.314730 | 0.190288 |
| O0 | hard | 7 | -0.023975 | 0.004574 | -2.750000 | 38.375000 | 1.321175 | -0.027507 |
| O0 | hard | 17 | -0.027858 | -0.002630 | -2.000000 | 40.875000 | 1.290565 | -0.020382 |
| O0 | hard | 27 | 0.018363 | -0.035711 | 1.375000 | 39.000000 | 1.296209 | -0.018572 |
| C0 | easy | 7 | 0.541031 | 1.906009 | -24.625000 | 47.250000 | 2.524645 | -0.114251 |
| C0 | easy | 17 | 0.600275 | 3.672898 | -41.125000 | 30.625000 | 4.399170 | -0.341578 |
| C0 | easy | 27 | 0.090615 | 3.098062 | -48.625000 | 40.500000 | 3.420913 | -0.185550 |
| C0 | hard | 7 | 0.238620 | -0.041234 | 4.250000 | 45.375000 | 1.275367 | -0.019305 |
| C0 | hard | 17 | 0.301508 | 0.003804 | -0.125000 | 42.750000 | 1.296998 | -0.024294 |
| C0 | hard | 27 | 0.212602 | 0.026131 | -0.125000 | 37.500000 | 1.358050 | -0.031956 |
| C1 | easy | 7 | 0.541031 | -0.237300 | 14.000000 | 85.875000 | 0.381336 | 0.180678 |
| C1 | easy | 17 | 0.600275 | -0.166449 | 8.000000 | 79.750000 | 0.559823 | 0.138735 |
| C1 | easy | 27 | 0.090615 | 0.815265 | -31.375000 | 57.750000 | 1.138116 | 0.078715 |
| C1 | hard | 7 | 0.238620 | -0.009461 | 2.375000 | 43.500000 | 1.307140 | -0.024044 |
| C1 | hard | 17 | 0.301508 | 0.005110 | -4.875000 | 38.000000 | 1.298305 | -0.027199 |
| C1 | hard | 27 | 0.212602 | 0.080170 | -1.125000 | 36.500000 | 1.412089 | -0.040238 |
| C2 | easy | 7 | 0.541031 | -0.348842 | 18.500000 | 90.375000 | 0.269794 | 0.240053 |
| C2 | easy | 17 | 0.600275 | -0.416647 | 17.125000 | 88.875000 | 0.309625 | 0.220183 |
| C2 | easy | 27 | 0.090615 | 0.131193 | -8.250000 | 80.875000 | 0.454044 | 0.179209 |
| C2 | hard | 7 | 0.238620 | -0.080198 | 7.500000 | 48.625000 | 1.236403 | -0.013386 |
| C2 | hard | 17 | 0.301508 | -0.084027 | 5.875000 | 48.750000 | 1.209167 | -0.008759 |
| C2 | hard | 27 | 0.212602 | -0.071407 | 3.750000 | 41.375000 | 1.260512 | -0.015963 |

## Fixed interpretation rules

```json
{
  "rule1_scale_rescue": {
    "easy_nll_gain": 2.7551507382964093,
    "easy_accuracy_gain_pp": 35.0,
    "hard_both_worsen": true,
    "passes": false
  },
  "rule2_descent_safe": {
    "accepted_armijo_violations": 0,
    "easy_nll_harm_vs_O0": -0.24162653772160408,
    "easy_accuracy_loss_pp_vs_O0": -11.833333333333329,
    "hard_nll_no_worse_than_C0": true,
    "passes": true
  },
  "rule3_task_useful": {
    "C1": {
      "hard_nll_delta": 0.02527312864859899,
      "hard_accuracy_delta_pp": -1.2083333333333333,
      "hard_nll_improving_seeds": 1,
      "hard_cosine_gain_vs_O0": 0.2620668119975986,
      "passes": false
    },
    "C2": {
      "hard_nll_delta": -0.07854422887166342,
      "hard_accuracy_delta_pp": 5.708333333333333,
      "hard_nll_improving_seeds": 3,
      "hard_cosine_gain_vs_O0": 0.2620668119975986,
      "passes": true
    }
  },
  "task_useful_controllers": [
    "C2"
  ],
  "next_action": "Research Lead review only; no meta-training or detector integration in T005."
}
```

## Mechanism and verification

| Method | Seed | Easy/hard vocabulary state delta mean | Unrelated vocabulary state delta mean | Reset state max | Reset output max |
| --- | --- | --- | --- | --- | --- |
| O0 | 7 | 0.152130 | 0.108616 | 0 | 0 |
| O0 | 17 | 0.205807 | 0.131754 | 0 | 0 |
| O0 | 27 | 0.159879 | 0.130022 | 0 | 0 |
| C0 | 7 | 0.680848 | 0.604259 | 0 | 0 |
| C0 | 17 | 1.078933 | 0.820368 | 0 | 0 |
| C0 | 27 | 0.650069 | 0.603940 | 0 | 0 |
| C1 | 7 | 0.241992 | 0.149528 | 0 | 0 |
| C1 | 17 | 0.316436 | 0.163274 | 0 | 0 |
| C1 | 27 | 0.285963 | 0.183557 | 0 | 0 |
| C2 | 7 | 0.162199 | 0.078074 | 0 | 0 |
| C2 | 17 | 0.222931 | 0.100974 | 0 | 0 |
| C2 | 27 | 0.162850 | 0.087641 | 0 | 0 |

Main records 2400; queries 19200; mechanism episodes 240. Normal output/state max error 0.0/0.0; nonfinite elements 0; all finite True. Source hashes and original O0/C0 metric equality checks: verification.json.

## Interpretation and limits

C2 improves hard accuracy by 5.70833 percentage points and NLL by .07854 from the same W0. Hard NLL improves for all three seeds (-.08020/-.08403/-.07141); accuracy also improves in all three (+7.5/+5.875/+3.75pp). Its raw direction is exactly the O1 direction by construction, with a hard cosine advantage .26207 over O0; accepted step control changes magnitude, not the objective.

C1 restores easy accuracy by 35pp relative to C0 and lowers NLL by 2.75515, but the full Rule 1 fails: hard NLL rises from 1.31014 to 1.33918 and accuracy falls from 41.875% to 39.33333%. Matching the O0 norm budget alone is insufficient; C1 hard mean scale is 1.33198.

C2 selects much smaller steps for easy (mean .00777) than hard (.03971). All 600 steps are accepted within the fixed sequence and meet Armijo; none falls back to W0. This supports the specific direction/step-behavior hypothesis in this frozen setting. It does not establish that a future meta-trained controller or detector will improve, or that the controller is optimal.

The aggregate easy gain is not universal: seed 27 C2 worsens from its own W0 by .13119 NLL and -8.25pp accuracy. Rule 2 is defined on aggregate means and passes unchanged; retain this failure and all paired records rather than claiming per-seed easy safety.

Engineering status VERIFIED; Research Lead acceptance is pending. If the lead continues, recommend C2 under a separately assigned fixed-budget meta-training task. No T006, detector integration, new objective or extra tuning is authorized by this result alone.

## Historical non-deployable reference

T003 exact-text foreground oracle, unchanged and not rerun: easy accuracy 85.16667%, NLL .36045; hard accuracy 48.33333%, NLL 1.18409. It uses labels/IDs and is not a deployable baseline.

## Artifacts

Full raw records and run logs: research_log/remote_runs/20260912-053826-tovd-t005-a6000/. frozen_step_screen.json contains aggregate/per-seed distributions, timings, eta counts, reset/vocabulary records and environment. Rules are evaluated without modifying their thresholds; research review is required before any subsequent task.
