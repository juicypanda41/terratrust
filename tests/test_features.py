import numpy as np
from PIL import Image

from src.terratrust.features import extract_features


def test_features_are_deterministic_and_finite():
    image = Image.fromarray(np.full((64, 64, 3), [30, 140, 80], dtype=np.uint8))
    first = extract_features(image)
    second = extract_features(image)
    assert first.ndim == 1
    assert first.shape == second.shape
    assert first.size > 100
    assert np.all(np.isfinite(first))
    assert np.allclose(first, second)


def test_rgba_and_grayscale_are_supported():
    gray = Image.fromarray(np.full((32, 32), 120, dtype=np.uint8))
    rgba = Image.fromarray(np.full((32, 32, 4), 200, dtype=np.uint8))
    assert extract_features(gray).shape == extract_features(rgba).shape
