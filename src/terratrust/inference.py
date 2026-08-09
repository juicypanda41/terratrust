from __future__ import annotations

import time
from dataclasses import dataclass

import joblib
import numpy as np
from PIL import Image

from .features import extract_features
from .reliability import apply_temperature


@dataclass(frozen=True)
class ScreeningResult:
    predicted_class: str
    confidence: float
    second_class: str
    second_confidence: float
    requires_review: bool
    quality_alert: bool
    review_reason: str
    latency_ms: float
    probabilities: dict[str, float]


class TerraTrustModel:
    def __init__(self, bundle: dict):
        self.classifier = bundle["classifier"]
        self.classes = list(bundle["classes"])
        self.temperature = float(bundle["temperature"])
        self.threshold = float(bundle["threshold"])
        self.feature_version = bundle.get("feature_version", "unknown")
        self.quality_guard = bundle.get("quality_guard")
        self.quality_threshold = float(bundle.get("quality_threshold", 1.0))

    @classmethod
    def load(cls, path: str) -> "TerraTrustModel":
        return cls(joblib.load(path))

    def predict(self, image: Image.Image) -> ScreeningResult:
        started = time.perf_counter()
        features = extract_features(image)[None, :]
        raw = self.classifier.predict_proba(features)
        calibrated = apply_temperature(raw, self.temperature)[0]
        quality_score = (
            float(self.quality_guard.predict_proba(features)[0, 1])
            if self.quality_guard is not None
            else 0.0
        )
        order = np.argsort(calibrated)[::-1]
        elapsed = (time.perf_counter() - started) * 1000
        top, second = int(order[0]), int(order[1])
        confidence = float(calibrated[top])
        quality_alert = quality_score >= self.quality_threshold
        confidence_alert = confidence < self.threshold
        requires_review = quality_alert or confidence_alert
        if quality_alert:
            review_reason = "Input-quality pattern differs from clean validation imagery."
        elif confidence_alert:
            review_reason = "Confidence is below the validation-selected acceptance threshold."
        else:
            review_reason = "Confidence and input quality meet the validation-selected policy."
        return ScreeningResult(
            predicted_class=self.classes[top],
            confidence=confidence,
            second_class=self.classes[second],
            second_confidence=float(calibrated[second]),
            requires_review=requires_review,
            quality_alert=quality_alert,
            review_reason=review_reason,
            latency_ms=float(elapsed),
            probabilities={name: float(calibrated[i]) for i, name in enumerate(self.classes)},
        )
