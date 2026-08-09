from __future__ import annotations

import argparse
import json
import platform
import shutil
import sys
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.terratrust.config import ARTIFACT_DIR, DEMO_DIR, EUROSAT_CLASSES  # noqa: E402
from src.terratrust.features import FEATURE_VERSION, extract_batch  # noqa: E402
from src.terratrust.reliability import (  # noqa: E402
    apply_temperature,
    brier_score,
    expected_calibration_error,
    fit_temperature,
    negative_log_likelihood,
    reliability_bins,
    risk_coverage_curve,
    select_threshold,
)

SEED = 42


def discover(data_dir: Path) -> tuple[list[str], np.ndarray, list[str]]:
    classes = [name for name in EUROSAT_CLASSES if (data_dir / name).exists()]
    if len(classes) != len(EUROSAT_CLASSES):
        found = sorted(path.name for path in data_dir.iterdir() if path.is_dir()) if data_dir.exists() else []
        raise FileNotFoundError(f"Expected EuroSAT classes in {data_dir}; found {found}")
    paths: list[str] = []
    labels: list[int] = []
    for index, name in enumerate(classes):
        for path in sorted((data_dir / name).glob("*.jpg")):
            paths.append(str(path))
            labels.append(index)
    return paths, np.asarray(labels, dtype=int), classes


def save_demo_samples(paths: list[str], labels: np.ndarray, classes: list[str]) -> list[dict]:
    if DEMO_DIR.exists():
        shutil.rmtree(DEMO_DIR)
    DEMO_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for class_index, class_name in enumerate(classes):
        matches = [path for path, label in zip(paths, labels) if label == class_index][:2]
        for number, source in enumerate(matches, 1):
            destination = DEMO_DIR / f"{class_name}_{number}.jpg"
            shutil.copy2(source, destination)
            manifest.append({"file": destination.name, "label": class_name})
    (DEMO_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train and evaluate TerraTrust")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "raw" / "EuroSAT_RGB")
    parser.add_argument("--target-accuracy", type=float, default=0.90)
    parser.add_argument("--max-iter", type=int, default=120)
    parser.add_argument("--max-per-class", type=int, default=0, help="0 uses the complete dataset")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    started = time.perf_counter()
    data_dir = args.data_dir
    paths, labels, classes = discover(data_dir)

    if args.max_per_class:
        selected = []
        for class_index in range(len(classes)):
            class_indices = np.where(labels == class_index)[0][: args.max_per_class]
            selected.extend(class_indices.tolist())
        paths = [paths[i] for i in selected]
        labels = labels[selected]

    all_indices = np.arange(len(paths))
    train_indices, remaining = train_test_split(
        all_indices, test_size=0.30, stratify=labels, random_state=SEED
    )
    validation_indices, test_indices = train_test_split(
        remaining, test_size=0.50, stratify=labels[remaining], random_state=SEED
    )

    print(f"Extracting deterministic features from {len(paths):,} images...")
    features = extract_batch(paths)
    model = HistGradientBoostingClassifier(
        learning_rate=0.08,
        max_iter=args.max_iter,
        max_leaf_nodes=31,
        min_samples_leaf=20,
        l2_regularization=0.2,
        random_state=SEED,
    )
    print("Training classifier...")
    model.fit(features[train_indices], labels[train_indices])

    raw_validation = model.predict_proba(features[validation_indices])
    temperature = fit_temperature(raw_validation, labels[validation_indices])
    calibrated_validation = apply_temperature(raw_validation, temperature)
    threshold_result = select_threshold(
        calibrated_validation, labels[validation_indices], args.target_accuracy
    )

    raw_test = model.predict_proba(features[test_indices])
    calibrated_test = apply_temperature(raw_test, temperature)
    predictions = calibrated_test.argmax(axis=1)
    confidence = calibrated_test.max(axis=1)
    accepted = confidence >= threshold_result["threshold"]
    test_accuracy = float(accuracy_score(labels[test_indices], predictions))
    macro_f1 = float(f1_score(labels[test_indices], predictions, average="macro"))
    selective_accuracy = float((predictions[accepted] == labels[test_indices][accepted]).mean()) if accepted.any() else 0.0

    report = classification_report(
        labels[test_indices], predictions, target_names=classes, output_dict=True, zero_division=0
    )
    elapsed = time.perf_counter() - started
    metrics = {
        "status": "evaluated",
        "dataset": "EuroSAT RGB v2",
        "dataset_source": "https://zenodo.org/records/7711810",
        "split_method": "deterministic stratified 70/15/15; not a geographic holdout",
        "seed": SEED,
        "sample_count": len(paths),
        "train_count": len(train_indices),
        "validation_count": len(validation_indices),
        "test_count": len(test_indices),
        "feature_version": FEATURE_VERSION,
        "model": "HistGradientBoostingClassifier",
        "accuracy": test_accuracy,
        "macro_f1": macro_f1,
        "temperature": temperature,
        "threshold": threshold_result["threshold"],
        "target_selective_accuracy": args.target_accuracy,
        "coverage": float(accepted.mean()),
        "review_rate": float(1.0 - accepted.mean()),
        "selective_accuracy": selective_accuracy,
        "ece_before": expected_calibration_error(raw_test, labels[test_indices]),
        "ece_after": expected_calibration_error(calibrated_test, labels[test_indices]),
        "brier_before": brier_score(raw_test, labels[test_indices]),
        "brier_after": brier_score(calibrated_test, labels[test_indices]),
        "nll_before": negative_log_likelihood(raw_test, labels[test_indices]),
        "nll_after": negative_log_likelihood(calibrated_test, labels[test_indices]),
        "training_seconds": elapsed,
        "runtime": {"python": platform.python_version(), "platform": platform.platform()},
        "per_class": {name: report[name] for name in classes},
        "reliability_bins_before": reliability_bins(raw_test, labels[test_indices]),
        "reliability_bins_after": reliability_bins(calibrated_test, labels[test_indices]),
        "limitations": [
            "Scene classification only; no pixel-level segmentation or acreage.",
            "No temporal pairs; results do not detect land-cover change.",
            "EuroSAT is European and this random stratified split may overestimate geographic transfer.",
            "Confidence is model-specific and is not a guarantee of real-world correctness.",
        ],
    }

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    bundle = {
        "classifier": model,
        "classes": classes,
        "temperature": temperature,
        "threshold": threshold_result["threshold"],
        "feature_version": FEATURE_VERSION,
    }
    joblib.dump(bundle, ARTIFACT_DIR / "terratrust_model.joblib", compress=3)
    (ARTIFACT_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    pd.DataFrame(risk_coverage_curve(calibrated_test, labels[test_indices])).to_csv(
        ARTIFACT_DIR / "risk_coverage.csv", index=False
    )
    pd.DataFrame(
        confusion_matrix(labels[test_indices], predictions), index=classes, columns=classes
    ).to_csv(ARTIFACT_DIR / "confusion_matrix.csv")
    save_demo_samples([paths[i] for i in test_indices], labels[test_indices], classes)

    print(json.dumps({k: metrics[k] for k in ["accuracy", "macro_f1", "coverage", "review_rate", "selective_accuracy", "ece_before", "ece_after", "training_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
