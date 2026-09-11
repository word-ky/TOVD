# T002 paired comparison analysis

P minus control, percentage points. Mean ± sample SD across paired seeds.

| Control | Easy Δ | Hard Δ | Hard-minus-easy Δ |
| --- | --- | --- | --- |
| P_minus_B0 | -4.542 ± 11.084 | -2.917 ± 6.676 | +1.625 ± 4.562 |
| P_minus_B1 | +2.833 ± 6.050 | +1.667 ± 3.492 | -1.167 ± 6.657 |
| P_minus_B2 | +1.958 ± 8.626 | -5.208 ± 4.043 | -7.167 ± 4.824 |
| P_minus_P_fixed | +37.000 ± 8.148 | +15.500 ± 3.599 | -21.500 ± 10.332 |

| Method | Parameters | Optimizer parameters | Eval ms/episode | Training seconds |
| --- | --- | --- | --- | --- |
| B0 | 2128 | 2128 | 0.634 ± 0.067 | 5.21 ± 0.13 |
| B1 | 2128 | 2128 | 1.290 ± 0.140 | 7.18 ± 0.16 |
| B2 | 2128 | 2128 | 7.381 ± 0.579 | 42.77 ± 2.25 |
| P | 2128 | 2128 | 7.765 ± 0.034 | 42.32 ± 2.10 |
| P_fixed | 2128 | 512 | 7.505 ± 0.490 | 44.00 ± 1.14 |

B0 includes an allocated but unused key projection (D²=256 parameters); its effective learned path has 256 fewer parameters.
B1/P/B2 have identical parameter tensors and both X/T information where applicable; B2 adaptation target excludes T.
Timing includes prototype diagnostic overhead, batch size 1, 3 warmups/10 forwards.
Independent P/seed7 checkpoint reevaluation exactly matches: True.
See analysis.json for per-seed deltas, reset/permutation/negative-control diagnostics and fixed-W0 drift.
