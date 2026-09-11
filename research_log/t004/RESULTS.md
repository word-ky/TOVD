# T004 results — Phase 1 complete; Phase 2 not authorized by fixed gate

O1/O3 improve gradient direction, but fail the fixed eta=.05 easy-regression limits. O2 worsens hard alignment and actual NLL. No candidate selected; no new outer training.

These checkpoints were meta-trained for O0. This screen does not establish that O1/O3 cannot be meta-trained successfully. It does establish that none meets the preregistered eligibility rule at this fixed W0 and step size.

Run: 20260912-043224-tovd-t004-screen-a6000. Tested code: 9afe8df54c22d0a20b284d6b4b20aaab5b36ea9a. Preregistration: be0a11c.

Three seeds (7/17/27), 100 easy + 100 hard episodes each, four objectives: 2,400 paired diagnoses / 19,200 query outcomes. All three source hashes match. All O0 NLL/accuracy/margin errors versus T002 and all diagnostic/normal output errors are zero. All records finite. Mean ± sample SD across seed means; accuracy in percent.

## Actual pre/post task performance

| Objective | Regime | W0 acc % | W* acc % | W0 NLL | W* NLL | ΔNLL | W0 margin | W* margin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| O0 | easy | 77.58333 ± 9.99557 | 74.87500 ± 15.65048 | 0.55592 ± 0.20889 | 0.58611 ± 0.26859 | 0.03019 ± 0.08311 | 0.20719 ± 0.01372 | 0.16221 ± 0.04289 |
| O0 | hard | 40.54167 ± 2.67317 | 39.41667 ± 1.30104 | 1.31390 ± 0.01950 | 1.30265 ± 0.01629 | -0.01126 ± 0.02148 | -0.02650 ± 0.00332 | -0.02215 ± 0.00472 |
| O1 | easy | 77.58333 ± 9.99557 | 39.45833 ± 8.36131 | 0.55592 ± 0.20889 | 3.44824 ± 0.93756 | 2.89232 ± 0.90123 | 0.20719 ± 0.01372 | -0.21379 ± 0.11627 |
| O1 | hard | 40.54167 ± 2.67317 | 41.87500 ± 4.00975 | 1.31390 ± 0.01950 | 1.31014 ± 0.04288 | -0.00377 ± 0.03431 | -0.02650 ± 0.00332 | -0.02518 ± 0.00637 |
| O2 | easy | 77.58333 ± 9.99557 | 70.29167 ± 21.16982 | 0.55592 ± 0.20889 | 0.81032 ± 0.65544 | 0.25440 ± 0.48410 | 0.20719 ± 0.01372 | 0.16949 ± 0.11464 |
| O2 | hard | 40.54167 ± 2.67317 | 35.87500 ± 2.39466 | 1.31390 ± 0.01950 | 1.50740 ± 0.03780 | 0.19349 ± 0.03846 | -0.02650 ± 0.00332 | -0.05405 ± 0.00392 |
| O3 | easy | 77.58333 ± 9.99557 | 37.58333 ± 7.29333 | 0.55592 ± 0.20889 | 3.82356 ± 0.95831 | 3.26764 ± 0.91709 | 0.20719 ± 0.01372 | -0.25429 ± 0.11924 |
| O3 | hard | 40.54167 ± 2.67317 | 30.33333 ± 2.11517 | 1.31390 ± 0.01950 | 2.03569 ± 0.09149 | 0.72178 ± 0.08817 | -0.02650 ± 0.00332 | -0.12192 ± 0.01198 |

## Gradient direction, update size and actual improvement fractions

| Objective | Regime | Task cosine | Task dot | Gradient norm | Update norm | Episodes improve % | Queries improve % |
| --- | --- | --- | --- | --- | --- | --- | --- |
| O0 | easy | 0.01111 ± 0.05037 | 1.18704 ± 1.85458 | 3.58560 ± 0.47813 | 0.17928 ± 0.02391 | 39.33333 ± 14.64013 | 31.75000 ± 10.51561 |
| O0 | hard | -0.01116 ± 0.02564 | 0.17602 ± 0.87352 | 4.05984 ± 0.34706 | 0.20299 ± 0.01735 | 43.00000 ± 8.54400 | 40.54167 ± 5.49052 |
| O1 | easy | 0.41064 ± 0.27873 | 102.09002 ± 74.51081 | 14.05324 ± 4.18088 | 0.70266 ± 0.20904 | 18.33333 ± 14.04754 | 35.54167 ± 4.00455 |
| O1 | hard | 0.25091 ± 0.04571 | 10.17679 ± 3.83358 | 3.68140 ± 0.53849 | 0.18407 ± 0.02692 | 52.66667 ± 1.52753 | 56.41667 ± 4.84177 |
| O2 | easy | 0.13933 ± 0.30882 | 1.09673 ± 5.45784 | 1.72385 ± 0.37353 | 0.08619 ± 0.01868 | 47.00000 ± 28.16026 | 51.41667 ± 19.23552 |
| O2 | hard | -0.07873 ± 0.04429 | -1.72505 ± 0.75482 | 2.08414 ± 0.17075 | 0.10421 ± 0.00854 | 34.00000 ± 5.56776 | 42.70833 ± 1.30104 |
| O3 | easy | 0.40996 ± 0.27125 | 126.82277 ± 90.39037 | 17.63182 ± 4.74414 | 0.88159 ± 0.23721 | 15.00000 ± 13.52775 | 33.50000 ± 4.32471 |
| O3 | hard | 0.22789 ± 0.05139 | 53.58323 ± 17.54746 | 23.23736 ± 2.60149 | 1.16187 ± 0.13007 | 36.00000 ± 6.00000 | 44.87500 ± 6.24124 |

## Inner loss and query representation

| Objective | Regime | Inner before | Inner after | Representation shift | Centered query margin after |
| --- | --- | --- | --- | --- | --- |
| O0 | easy | 1.05485 ± 0.26150 | 0.52842 ± 0.24555 | 0.52833 ± 0.07369 | 0.19218 ± 0.05059 |
| O0 | hard | 1.02054 ± 0.18570 | 0.39325 ± 0.18178 | 0.60147 ± 0.05118 | -0.07599 ± 0.01591 |
| O1 | easy | 2.25795 ± 0.39479 | 4.51553 ± 0.44051 | 2.05458 ± 0.65217 | -0.25254 ± 0.13855 |
| O1 | hard | 1.65942 ± 0.02457 | 1.62074 ± 0.05002 | 0.54272 ± 0.08666 | -0.08426 ± 0.02588 |
| O2 | easy | 0.93278 ± 0.02901 | 0.78759 ± 0.03750 | 0.24542 ± 0.06374 | 0.20137 ± 0.13399 |
| O2 | hard | 0.96511 ± 0.02152 | 0.76267 ± 0.04321 | 0.30337 ± 0.02805 | -0.18371 ± 0.02077 |
| O3 | easy | 2.50297 ± 0.49562 | 5.51338 ± 0.52619 | 2.57602 ± 0.74333 | -0.30291 ± 0.14237 |
| O3 | hard | 3.30774 ± 0.14573 | 5.38075 ± 0.24542 | 3.40966 ± 0.43301 | -0.41207 ± 0.04689 |

## Foreground assignment ambiguity (offline oracle scoring)

| Objective | Regime | Assignment correct % | Entropy | Top1-top2 gap | Target correct-wrong cosine |
| --- | --- | --- | --- | --- | --- |
| O0 | easy | 59.64583 ± 34.17078 | 1.20604 ± 0.07252 | 0.20785 ± 0.07964 | 0.07198 ± 0.24735 |
| O0 | hard | 29.27083 ± 2.63119 | 1.36711 ± 0.00441 | 0.04567 ± 0.00369 | -0.01046 ± 0.00029 |
| O1 | easy | 59.64583 ± 34.17078 | 1.20604 ± 0.07252 | 0.20785 ± 0.07964 | 0.07198 ± 0.24735 |
| O1 | hard | 29.27083 ± 2.63119 | 1.36711 ± 0.00441 | 0.04567 ± 0.00369 | -0.01046 ± 0.00029 |
| O2 | easy | 59.77083 ± 33.91052 | 1.15167 ± 0.09297 | 0.24756 ± 0.09435 | 0.08536 ± 0.64148 |
| O2 | hard | 28.93750 ± 2.25607 | 1.20460 ± 0.02844 | 0.18753 ± 0.01377 | -0.54976 ± 0.07273 |
| O3 | easy | 59.77083 ± 33.91052 | 1.15167 ± 0.09297 | 0.24756 ± 0.09435 | 0.08536 ± 0.64148 |
| O3 | hard | 28.93750 ± 2.25607 | 1.20460 ± 0.02844 | 0.18753 ± 0.01377 | -0.54976 ± 0.07273 |

O0/O1 use original text geometry; O2/O3 use centered normalized text. The last column scores A*T (O0/O1) or A_rel*T_rel (O2/O3). For distribution objectives this vector is only an inspection statistic, never the loss target. Absolute margins across original/centered coordinate systems are not directly comparable. Distractor/background entropy and gaps, token distributions and seed SDs are in frozen_screen.json.

## Per-seed paired task outcomes

| Objective | Regime | Seed | Cosine | ΔNLL | ΔAccuracy pp | Post accuracy % | Post NLL | Post margin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| O0 | easy | 7 | 0.05018 | -0.02685 | 0.50000 | 72.37500 | 0.59179 | 0.18349 |
| O0 | easy | 17 | -0.04574 | 0.12555 | -11.12500 | 60.62500 | 0.85183 | 0.11284 |
| O0 | easy | 27 | 0.02889 | -0.00812 | 2.50000 | 91.62500 | 0.31473 | 0.19029 |
| O0 | hard | 7 | -0.02398 | 0.00457 | -2.75000 | 38.37500 | 1.32118 | -0.02751 |
| O0 | hard | 17 | -0.02786 | -0.00263 | -2.00000 | 40.87500 | 1.29056 | -0.02038 |
| O0 | hard | 27 | 0.01836 | -0.03571 | 1.37500 | 39.00000 | 1.29621 | -0.01857 |
| O1 | easy | 7 | 0.54103 | 1.90601 | -24.62500 | 47.25000 | 2.52464 | -0.11425 |
| O1 | easy | 17 | 0.60028 | 3.67290 | -41.12500 | 30.62500 | 4.39917 | -0.34158 |
| O1 | easy | 27 | 0.09062 | 3.09806 | -48.62500 | 40.50000 | 3.42091 | -0.18555 |
| O1 | hard | 7 | 0.23862 | -0.04123 | 4.25000 | 45.37500 | 1.27537 | -0.01930 |
| O1 | hard | 17 | 0.30151 | 0.00380 | -0.12500 | 42.75000 | 1.29700 | -0.02429 |
| O1 | hard | 27 | 0.21260 | 0.02613 | -0.12500 | 37.50000 | 1.35805 | -0.03196 |
| O2 | easy | 7 | 0.23627 | 0.00612 | 0.87500 | 72.75000 | 0.62475 | 0.21432 |
| O2 | easy | 17 | -0.20633 | 0.81227 | -23.75000 | 48.00000 | 1.53854 | 0.03920 |
| O2 | easy | 27 | 0.38805 | -0.05518 | 1.00000 | 90.12500 | 0.26767 | 0.25494 |
| O2 | hard | 7 | -0.03742 | 0.14973 | -8.00000 | 33.12500 | 1.46633 | -0.05248 |
| O2 | hard | 17 | -0.07328 | 0.22192 | -5.37500 | 37.50000 | 1.51511 | -0.05115 |
| O2 | hard | 27 | -0.12549 | 0.20883 | -0.62500 | 37.00000 | 1.54075 | -0.05851 |
| O3 | easy | 7 | 0.53710 | 2.27323 | -27.50000 | 44.37500 | 2.89187 | -0.15159 |
| O3 | easy | 17 | 0.59429 | 4.08017 | -41.87500 | 29.87500 | 4.80644 | -0.38506 |
| O3 | easy | 27 | 0.09850 | 3.44951 | -50.62500 | 38.50000 | 3.77236 | -0.22622 |
| O3 | hard | 7 | 0.24112 | 0.62168 | -9.00000 | 32.12500 | 1.93828 | -0.10882 |
| O3 | hard | 17 | 0.27138 | 0.75578 | -14.87500 | 28.00000 | 2.04898 | -0.12459 |
| O3 | hard | 27 | 0.17118 | 0.78789 | -6.75000 | 30.87500 | 2.11981 | -0.13234 |

## Preregistered selection

| Candidate | Hard NLL gain vs O0 | Hard cosine gain | Easy NLL harm | Easy accuracy loss pp | Eligible |
| --- | --- | --- | --- | --- | --- |
| O1 | -0.00749 | 0.26207 | 2.86213 | 35.41667 | False |
| O2 | -0.20475 | -0.06757 | 0.22421 | 4.58333 | False |
| O3 | -0.73304 | 0.23905 | 3.23744 | 37.29167 | False |

Rule unchanged from be0a11c: hard ΔNLL gain ≥.02 OR cosine gain ≥.05; easy NLL harm ≤.10 AND accuracy loss ≤5pp. Selected: none. Phase 2: not run.

## Historical reference (non-deployable)

T003 foreground exact-text oracle at the same P W0: easy accuracy 85.16667%, NLL .36045, task cosine .31727; hard accuracy 48.33333%, NLL 1.18409, cosine .12128. It uses ground-truth source IDs and exact text targets; retained only as a reference, not rerun. Source: research_log/remote_runs/20260912-030923-tovd-t003-a6000/artifacts/t003/alignment.json.

## Interpretation and recommendation

O1/O3 hard cosine increases are real direction changes at the same W0, not merely larger gradient norms. However local alignment does not ensure a finite eta=.05 step improves the task. O1 easy inner CE increases 2.25795→4.51553, O3 easy 2.50297→5.51338, and O3 hard 3.30774→5.38075. Together with large updates these observations are consistent with step-size/curvature mismatch; no eta sweep was performed to establish its cause.

Centering sharpens hard assignments (entropy 1.36711→1.20460, gap .04567→.18753) without improving correctness (29.27083%→28.93750%). More confident assignments are not evidence of better semantics. O2 hard task cosine becomes more negative.

Recommend stopping this fixed-objective/fixed-step branch before detector integration. Research Lead may explicitly authorize a reformulation addressing objective scale/local step behavior and teacher correctness; these are hypotheses, not implemented fixes. Do not claim all objectives are misaligned, that meta-training has failed, or that the broader fast-weight mechanism is disproved. No Phase-2 success claim is available.

## Artifacts

- frozen_screen.json: aggregate/per-seed metrics and experiment environment.
- selection.json: exact fixed gate decisions.
- verification.json: original pairing, hashes and full receipt manifest.
- research_log/remote_runs/20260912-043224-tovd-t004-screen-a6000/: complete raw records, metadata and logs.
