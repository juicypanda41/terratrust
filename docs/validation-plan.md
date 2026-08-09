# Validation Plan

## Technical evidence

- Regenerate all metrics from the official dataset.
- Confirm the threshold is selected on validation data only.
- Report the complete test-set size, split method, and seed.
- Inspect the confusion matrix and worst-class recall.
- Demonstrate one accepted case, one reviewed case, and one failure.
- Run the full automated test suite.

## Small usability study

Recruit 5-8 target-adjacent testers. Do not label them GIS or environmental professionals unless that is true.

Tasks:

1. Identify the model's top prediction.
2. Decide whether the system auto-accepted it or requested review.
3. Explain whether the result is a final environmental determination.
4. Complete one review-queue action.

Record consent, role/background, completion, elapsed time, errors, and one improvement suggestion. Store anonymized aggregate results only. No results exist until this study is actually run.

