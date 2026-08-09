import numpy as np
from PIL import Image

from src.terratrust.inference import TerraTrustModel


class FakeClassifier:
    def predict_proba(self, features):
        return np.array([[0.75, 0.25]])


def test_inference_contract_and_review_routing():
    model = TerraTrustModel(
        {
            "classifier": FakeClassifier(),
            "classes": ["Forest", "River"],
            "temperature": 1.0,
            "threshold": 0.8,
            "feature_version": "test",
        }
    )
    image = Image.fromarray(np.zeros((64, 64, 3), dtype=np.uint8))
    result = model.predict(image)
    assert result.predicted_class == "Forest"
    assert result.requires_review is True
    assert result.quality_alert is False
    assert "confidence" in result.review_reason.lower()
    assert abs(sum(result.probabilities.values()) - 1.0) < 1e-8
