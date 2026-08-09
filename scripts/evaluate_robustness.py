from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.train import SEED, discover  # noqa: E402
from src.terratrust.config import ARTIFACT_DIR  # noqa: E402
from src.terratrust.features import extract_features  # noqa: E402
from src.terratrust.reliability import apply_temperature  # noqa: E402


def transform(image: Image.Image, condition: str, rng: np.random.Generator) -> Image.Image:
    image = image.convert("RGB")
    if condition == "Clean":
        return image
    if condition == "Blur":
        return image.filter(ImageFilter.GaussianBlur(radius=1.5))
    if condition == "Low brightness":
        return ImageEnhance.Brightness(image).enhance(0.6)
    if condition == "Low contrast":
        return ImageEnhance.Contrast(image).enhance(0.6)
    if condition == "Sensor-like noise":
        arr = np.asarray(image, dtype=np.float32)
        noisy = np.clip(arr + rng.normal(0, 18, arr.shape), 0, 255).astype(np.uint8)
        return Image.fromarray(noisy)
    raise ValueError(condition)


def main() -> None:
    data_dir = ROOT / "data" / "raw" / "EuroSAT_RGB"
    paths, labels, _ = discover(data_dir)
    indices = np.arange(len(paths))
    _, remaining = train_test_split(indices, test_size=0.30, stratify=labels, random_state=SEED)
    _, test_indices = train_test_split(
        remaining, test_size=0.50, stratify=labels[remaining], random_state=SEED
    )

    # Fixed, class-balanced subset keeps this post-training audit quick and reproducible.
    subset = []
    for class_index in range(10):
        members = [idx for idx in test_indices if labels[idx] == class_index][:40]
        subset.extend(members)

    bundle = joblib.load(ARTIFACT_DIR / "terratrust_model.joblib")
    model = bundle["classifier"]
    temperature = float(bundle["temperature"])
    threshold = float(bundle["threshold"])
    quality_guard = bundle.get("quality_guard")
    quality_threshold = float(bundle.get("quality_threshold", 1.0))
    conditions = ["Clean", "Blur", "Low brightness", "Low contrast", "Sensor-like noise"]
    rows = []
    latency_samples = []

    for condition_index, condition in enumerate(conditions):
        rng = np.random.default_rng(SEED + condition_index)
        feature_rows = []
        for index in subset:
            with Image.open(paths[index]) as image:
                altered = transform(image, condition, rng)
                started = time.perf_counter()
                feature_rows.append(extract_features(altered))
                latency_samples.append((time.perf_counter() - started) * 1000)
        feature_matrix = np.vstack(feature_rows)
        probabilities = apply_temperature(model.predict_proba(feature_matrix), temperature)
        predictions = probabilities.argmax(axis=1)
        confidence = probabilities.max(axis=1)
        quality_scores = (
            quality_guard.predict_proba(feature_matrix)[:, 1]
            if quality_guard is not None
            else np.zeros(len(feature_matrix))
        )
        accepted = (confidence >= threshold) & (quality_scores < quality_threshold)
        subset_labels = labels[subset]
        rows.append(
            {
                "condition": condition,
                "sample_count": len(subset),
                "accuracy": float((predictions == subset_labels).mean()),
                "mean_confidence": float(confidence.mean()),
                "review_rate": float((~accepted).mean()),
                "quality_alert_rate": float((quality_scores >= quality_threshold).mean()),
                "accepted_case_accuracy": float((predictions[accepted] == subset_labels[accepted]).mean()) if accepted.any() else None,
            }
        )

    pd.DataFrame(rows).to_csv(ARTIFACT_DIR / "robustness.csv", index=False)
    metrics_path = ARTIFACT_DIR / "metrics.json"
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))

    # Warm end-to-end latency on 100 clean images, including features and model prediction.
    inference_times = []
    for index in subset[:100]:
        with Image.open(paths[index]) as image:
            started = time.perf_counter()
            feature = extract_features(image)[None, :]
            model.predict_proba(feature)
            inference_times.append((time.perf_counter() - started) * 1000)
    metrics["inference_latency_ms"] = {
        "sample_count": len(inference_times),
        "median": float(np.median(inference_times)),
        "p95": float(np.quantile(inference_times, 0.95)),
        "scope": "warm local CPU, feature extraction plus classifier; deployment hardware will differ",
    }
    metrics["robustness_audit"] = {
        "sample_count_per_condition": 400,
        "conditions": conditions,
        "purpose": "controlled stress test, not a claim of real-world distribution coverage",
    }
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(pd.DataFrame(rows).to_string(index=False))
    print(json.dumps(metrics["inference_latency_ms"], indent=2))


if __name__ == "__main__":
    main()
