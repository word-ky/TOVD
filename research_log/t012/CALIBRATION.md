# T012 static activation-side reduction audit

Calibration run `20260912-141907-tovd-t012-cal-a6000`. Tested implementation `8c4abff9140f1d762175472117bf6b9c3d5fcb21`; preregistration `15d3353`.
One global lambda = **0.2**, chosen from 14400 fresh base queries across all nine states. This value is shared across seeds, states and regimes.

| Lambda | Base calibration NLL | Accuracy % |
| --- | --- | --- |
| 0.0 | 0.553871328 | 79.38194 |
| 0.05 | 0.553461626 | 79.47222 |
| 0.1 | 0.553127343 | 79.47917 |
| 0.2 | 0.552682552 | 79.37500 |
| 0.5 | 0.553100711 | 79.15972 |
| 1.0 | 0.559460702 | 77.52778 |
| 2.0 | 0.592983160 | 73.87500 |

Base W0 NLL 0.553871328. Selection minimizes global base NLL; ties within1e-12 use the smallest exponent. No novel outcomes enter calibration.

Novel evaluation has not run. Commit and push the actual frozen_lambda.json and this complete calibration receipt before deploying the novel phase.
Calibration engineering validity: True. CPU/CUDA test receipts: [{'passed': 108, 'seconds': 9.36}, {'passed': 108, 'seconds': 27.36}].
