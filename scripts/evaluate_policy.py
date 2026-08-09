from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.train import SEED, discover  # noqa: E402
from src.terratrust.config import ARTIFACT_DIR  # noqa: E402
from src.terratrust.features import extract_batch  # noqa: E402
from src.terratrust.reliability import apply_temperature  # noqa: E402


def main() -> None:
    paths, labels, _ = discover(ROOT / "data" / "raw" / "EuroSAT_RGB")
    indices = np.arange(len(paths))
    _, remaining = train_test_split(indices, test_size=0.30, stratify=labels, random_state=SEED)
    _, test_indices = train_test_split(
        remaining, test_size=0.50, stratify=labels[remaining], random_state=SEED
    )
    test_paths = [paths[index] for index in test_indices]
    test_labels = labels[test_indices]
    features = extract_batch(test_paths)

    bundle = joblib.load(ARTIFACT_DIR / "terratrust_model.joblib")
    probabilities = apply_temperature(
        bundle["classifier"].predict_proba(features), float(bundle["temperature"])
    )
    quality_scores = bundle["quality_guard"].predict_proba(features)[:, 1]
    quality_ok = quality_scores < float(bundle["quality_threshold"])
    confidence = probabilities.max(axis=1)
    predictions = probabilities.argmax(axis=1)
    correct = predictions == test_labels
    threshold = float(bundle["threshold"])
    confidence_only = confidence >= threshold
    accepted = confidence_only & quality_ok

    metrics_path = ARTIFACT_DIR / "metrics.json"
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    metrics["confidence_only_policy"] = {
        "coverage": metrics["coverage"],
        "review_rate": metrics["review_rate"],
        "selective_accuracy": metrics["selective_accuracy"],
    }
    metrics["coverage"] = float(accepted.mean())
    metrics["review_rate"] = float((~accepted).mean())
    metrics["selective_accuracy"] = float(correct[accepted].mean())
    metrics["quality_alert_rate_clean_test"] = float((~quality_ok).mean())
    metrics["policy"] = "accept only when calibrated confidence passes and quality guard is clear"
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    rows = []
    for candidate in np.linspace(0.30, 0.99, 70):
        candidate_accepted = (confidence >= candidate) & quality_ok
        if not candidate_accepted.any():
            continue
        accuracy = float(correct[candidate_accepted].mean())
        rows.append(
            {
                "threshold": float(candidate),
                "coverage": float(candidate_accepted.mean()),
                "review_rate": float((~candidate_accepted).mean()),
                "selective_accuracy": accuracy,
                "risk": float(1.0 - accuracy),
            }
        )
    pd.DataFrame(rows).to_csv(ARTIFACT_DIR / "risk_coverage.csv", index=False)
    print(
        json.dumps(
            {
                "test_count": len(test_indices),
                "coverage": metrics["coverage"],
                "review_rate": metrics["review_rate"],
                "selective_accuracy": metrics["selective_accuracy"],
                "quality_alert_rate_clean_test": metrics["quality_alert_rate_clean_test"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

