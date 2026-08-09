import numpy as np

from src.terratrust.reliability import (
    apply_temperature,
    expected_calibration_error,
    risk_coverage_curve,
    select_threshold,
)


def test_temperature_preserves_probability_rows():
    probabilities = np.array([[0.8, 0.2], [0.4, 0.6]])
    scaled = apply_temperature(probabilities, 1.7)
    assert np.allclose(scaled.sum(axis=1), 1.0)
    assert np.all(scaled >= 0)


def test_threshold_meets_target_when_possible():
    probabilities = np.array([[0.99, 0.01], [0.95, 0.05], [0.55, 0.45], [0.51, 0.49]])
    labels = np.array([0, 0, 1, 1])
    result = select_threshold(probabilities, labels, target_accuracy=1.0)
    assert result["selective_accuracy"] == 1.0
    assert 0 < result["coverage"] <= 0.5


def test_reliability_outputs_are_bounded():
    probabilities = np.array([[0.9, 0.1], [0.4, 0.6], [0.7, 0.3]])
    labels = np.array([0, 1, 1])
    ece = expected_calibration_error(probabilities, labels)
    rows = risk_coverage_curve(probabilities, labels)
    assert 0 <= ece <= 1
    assert rows
    assert all(0 <= row["coverage"] <= 1 for row in rows)

