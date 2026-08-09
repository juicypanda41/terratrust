from __future__ import annotations

import numpy as np


def apply_temperature(probabilities: np.ndarray, temperature: float) -> np.ndarray:
    """Temperature-scale probabilities without requiring model logits."""
    probs = np.clip(np.asarray(probabilities, dtype=float), 1e-12, 1.0)
    scaled = np.exp(np.log(probs) / max(float(temperature), 1e-6))
    return scaled / scaled.sum(axis=1, keepdims=True)


def negative_log_likelihood(probabilities: np.ndarray, y_true: np.ndarray) -> float:
    probs = np.clip(probabilities[np.arange(len(y_true)), y_true], 1e-12, 1.0)
    return float(-np.log(probs).mean())


def brier_score(probabilities: np.ndarray, y_true: np.ndarray) -> float:
    expected = np.zeros_like(probabilities)
    expected[np.arange(len(y_true)), y_true] = 1.0
    return float(np.mean(np.sum((probabilities - expected) ** 2, axis=1)))


def expected_calibration_error(
    probabilities: np.ndarray, y_true: np.ndarray, bins: int = 10
) -> float:
    confidence = probabilities.max(axis=1)
    correct = probabilities.argmax(axis=1) == y_true
    edges = np.linspace(0.0, 1.0, bins + 1)
    error = 0.0
    for low, high in zip(edges[:-1], edges[1:]):
        mask = (confidence > low) & (confidence <= high)
        if mask.any():
            error += mask.mean() * abs(float(correct[mask].mean()) - float(confidence[mask].mean()))
    return float(error)


def fit_temperature(probabilities: np.ndarray, y_true: np.ndarray) -> float:
    candidates = np.linspace(0.4, 3.0, 131)
    losses = [negative_log_likelihood(apply_temperature(probabilities, t), y_true) for t in candidates]
    return float(candidates[int(np.argmin(losses))])


def select_threshold(
    probabilities: np.ndarray, y_true: np.ndarray, target_accuracy: float = 0.90
) -> dict[str, float]:
    confidence = probabilities.max(axis=1)
    correct = probabilities.argmax(axis=1) == y_true
    best = {"threshold": 1.0, "coverage": 0.0, "selective_accuracy": 1.0}
    for threshold in np.linspace(0.30, 0.99, 140):
        accepted = confidence >= threshold
        if not accepted.any():
            continue
        accuracy = float(correct[accepted].mean())
        coverage = float(accepted.mean())
        if accuracy >= target_accuracy and coverage > best["coverage"]:
            best = {
                "threshold": float(threshold),
                "coverage": coverage,
                "selective_accuracy": accuracy,
            }
    return best


def risk_coverage_curve(probabilities: np.ndarray, y_true: np.ndarray) -> list[dict[str, float]]:
    confidence = probabilities.max(axis=1)
    correct = probabilities.argmax(axis=1) == y_true
    rows = []
    for threshold in np.linspace(0.30, 0.99, 70):
        accepted = confidence >= threshold
        if not accepted.any():
            continue
        accuracy = float(correct[accepted].mean())
        rows.append(
            {
                "threshold": float(threshold),
                "coverage": float(accepted.mean()),
                "review_rate": float(1.0 - accepted.mean()),
                "selective_accuracy": accuracy,
                "risk": float(1.0 - accuracy),
            }
        )
    return rows


def reliability_bins(
    probabilities: np.ndarray, y_true: np.ndarray, bins: int = 10
) -> list[dict[str, float]]:
    confidence = probabilities.max(axis=1)
    correct = probabilities.argmax(axis=1) == y_true
    edges = np.linspace(0.0, 1.0, bins + 1)
    rows = []
    for low, high in zip(edges[:-1], edges[1:]):
        mask = (confidence > low) & (confidence <= high)
        if mask.any():
            rows.append(
                {
                    "bin_low": float(low),
                    "bin_high": float(high),
                    "confidence": float(confidence[mask].mean()),
                    "accuracy": float(correct[mask].mean()),
                    "count": int(mask.sum()),
                }
            )
    return rows

