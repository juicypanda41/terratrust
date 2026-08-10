# Metrics and Evidence Register

This register separates measured prototype results, targets, projections, and outcomes that have not yet been measured. Machine-readable results are in `artifacts/metrics.json`, `artifacts/robustness.csv`, `artifacts/risk_coverage.csv`, and `artifacts/confusion_matrix.csv`.

| Metric | Baseline or target | Current result | Sample and method | Evidence | Interpretation / limitation |
|---|---:|---:|---|---|---|
| Always-predict accuracy | Baseline | 89.4% | Held-out test, n=4,050 | `artifacts/metrics.json` | Random stratified European imagery; not a geographic holdout |
| Macro F1 | Baseline companion | 88.9% | Held-out test, n=4,050 | `artifacts/metrics.json` | Gives equal weight to ten classes |
| Accepted-case accuracy | Target ≥90.0% | 91.4% | Confidence threshold selected on validation; evaluated on held-out test | `artifacts/metrics.json` | Applies only to accepted scenes |
| Coverage | Post-benchmark planning floor ≥75.0% | 78.9% | Complete confidence-plus-quality policy on held-out test | `artifacts/metrics.json` | Not preregistered; remaining 21.1% requires human verification |
| Expected calibration error | Target <1.0% | 0.87% after calibration | Temperature selected on validation; held-out test evaluation | `artifacts/metrics.json` | Calibration is model- and distribution-specific |
| Warm CPU inference | Post-benchmark planning guardrail p95 <50 ms | Median 16.2 ms; p95 22.3 ms | 100 local warm runs, features plus classifier | `artifacts/metrics.json` | Not preregistered; deployment hardware and concurrency will differ |
| Controlled quality routing | Detect known synthetic shifts | 98.5–100% routed for four perturbations | 400 scenes per condition | `artifacts/robustness.csv` | Not evidence of general out-of-distribution detection |
| Task completion time | To be set after pilot | Not measured | Planned 5–8 participant usability study | `docs/validation-plan.md` | Must not be claimed until real participants complete the protocol |
| Conservation/forest outcome | No prototype target | Not measured | Requires a real monitoring deployment and outcome design | — | TerraTrust currently provides enabling evidence only |

## Reproduction contract

- Dataset: official EuroSAT RGB v2 archive from Zenodo.
- Split: deterministic stratified 70/15/15 with seed 42.
- Calibration and threshold selection: validation split only.
- Published results: untouched test split only.
- Regeneration: run the documented training and evaluation commands in `README.md`.
- Claims rule: a number is described as measured only when its raw artifact and method are linked above.
