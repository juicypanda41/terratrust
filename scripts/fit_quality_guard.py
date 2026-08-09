from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import numpy as np
from PIL import Image
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.evaluate_robustness import transform  # noqa: E402
from scripts.train import SEED, discover  # noqa: E402
from src.terratrust.config import ARTIFACT_DIR  # noqa: E402
from src.terratrust.features import extract_features  # noqa: E402


def main() -> None:
    paths, labels, _ = discover(ROOT / "data" / "raw" / "EuroSAT_RGB")
    indices = np.arange(len(paths))
    _, remaining = train_test_split(indices, test_size=0.30, stratify=labels, random_state=SEED)
    validation_indices, _ = train_test_split(
        remaining, test_size=0.50, stratify=labels[remaining], random_state=SEED
    )
    subset = []
    for class_index in range(10):
        subset.extend([idx for idx in validation_indices if labels[idx] == class_index][:80])

    conditions = ["Clean", "Blur", "Low brightness", "Low contrast", "Sensor-like noise"]
    feature_rows = []
    quality_labels = []
    for condition_index, condition in enumerate(conditions):
        rng = np.random.default_rng(SEED + 100 + condition_index)
        for index in subset:
            with Image.open(paths[index]) as image:
                feature_rows.append(extract_features(transform(image, condition, rng)))
                quality_labels.append(0 if condition == "Clean" else 1)

    features = np.vstack(feature_rows)
    quality_labels = np.asarray(quality_labels)
    quality_guard = HistGradientBoostingClassifier(
        max_iter=100,
        max_leaf_nodes=15,
        learning_rate=0.08,
        l2_regularization=0.5,
        class_weight="balanced",
        random_state=SEED,
    )
    quality_guard.fit(features, quality_labels)
    clean_scores = quality_guard.predict_proba(features[quality_labels == 0])[:, 1]
    quality_threshold = float(np.quantile(clean_scores, 0.95))

    model_path = ARTIFACT_DIR / "terratrust_model.joblib"
    bundle = joblib.load(model_path)
    bundle["quality_guard"] = quality_guard
    bundle["quality_threshold"] = quality_threshold
    bundle["quality_conditions"] = conditions[1:]
    joblib.dump(bundle, model_path, compress=3)

    metrics_path = ARTIFACT_DIR / "metrics.json"
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    metrics["quality_guard"] = {
        "training_source": "validation split only",
        "clean_validation_samples": len(subset),
        "synthetically_perturbed_validation_samples": len(subset) * 4,
        "threshold": quality_threshold,
        "clean_validation_false_alert_target": 0.05,
        "conditions": conditions[1:],
        "limitation": "Detects controlled quality shifts only; it is not a general out-of-distribution guarantee.",
    }
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics["quality_guard"], indent=2))


if __name__ == "__main__":
    main()

