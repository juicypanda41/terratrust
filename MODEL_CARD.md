# TerraTrust Model Card

## Intended use

TerraTrust is a hackathon research prototype for triaging 64x64 RGB Sentinel-2 land-cover scenes into ten EuroSAT classes. It demonstrates calibrated confidence and human-review routing.

## Not intended for

- Final environmental, legal, safety, or land-management decisions.
- Pixel-level mapping, boundaries, acreage, object detection, carbon estimation, or biodiversity measurement.
- Deforestation or other temporal change detection.
- Claims of reliable performance outside imagery similar to EuroSAT's European scenes.

## Data

- EuroSAT RGB v2, 27,000 labeled images across ten scene classes.
- Source: https://doi.org/10.5281/zenodo.7711810
- Deterministic stratified 70/15/15 split with seed 42.
- This split is not geographic and can overestimate transfer to new regions.

## Model and features

- Histogram Gradient Boosting classifier.
- Deterministic color statistics, HSV statistics, 4x4 spatial color pooling, channel histograms, and gradient features.
- Temperature scaling fitted on validation predictions.
- Confidence threshold selected on validation data to target accepted-case accuracy.
- Separate input-quality guard trained only on clean and controlled perturbed validation imagery; its threshold targets a 5% alert rate on clean validation examples.

## Evaluation

Run `python scripts/train.py` to regenerate `artifacts/metrics.json`, `artifacts/confusion_matrix.csv`, and `artifacts/risk_coverage.csv`. The application reads only those saved artifacts for headline evidence.

The final held-out RGB test set contains 4,050 images. Overall accuracy is 89.4% and macro F1 is 88.9%. The complete confidence-plus-quality policy auto-accepts 78.9% of test images at 91.4% accepted-case accuracy and sends 21.1% to review. These are benchmark results, not deployment guarantees.

## Ethical and operational safeguards

- Uncertain cases are explicitly routed for human review.
- Limitations remain visible in the interface.
- The review workflow does not silently retrain the model.
- The quality guard recognizes only controlled shifts similar to its validation perturbations; it is not a general out-of-distribution guarantee.
- Deployment in a real region requires local validation, expert review, drift monitoring, and additional temporal/geospatial data.
