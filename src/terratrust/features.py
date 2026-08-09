from __future__ import annotations

import numpy as np
from PIL import Image

FEATURE_VERSION = "rgb-stat-grid-hist-gradient-v1"


def _to_rgb_array(image: Image.Image | np.ndarray) -> np.ndarray:
    if isinstance(image, np.ndarray):
        arr = image
        if arr.ndim == 2:
            arr = np.repeat(arr[..., None], 3, axis=2)
        if arr.shape[-1] > 3:
            arr = arr[..., :3]
        image = Image.fromarray(arr.astype(np.uint8))
    rgb = image.convert("RGB").resize((64, 64), Image.Resampling.BILINEAR)
    return np.asarray(rgb, dtype=np.float32) / 255.0


def extract_features(image: Image.Image | np.ndarray) -> np.ndarray:
    """Create deterministic, explainable RGB features from one 64x64 tile."""
    arr = _to_rgb_array(image)
    flat = arr.reshape(-1, 3)

    channel_stats = np.concatenate(
        [
            flat.mean(axis=0),
            flat.std(axis=0),
            np.quantile(flat, [0.1, 0.25, 0.5, 0.75, 0.9], axis=0).reshape(-1),
        ]
    )

    hsv = np.asarray(
        Image.fromarray((arr * 255).astype(np.uint8)).convert("HSV"), dtype=np.float32
    ) / 255.0
    hsv_flat = hsv.reshape(-1, 3)
    hsv_stats = np.concatenate([hsv_flat.mean(axis=0), hsv_flat.std(axis=0)])

    grid_features = []
    for row in range(4):
        for col in range(4):
            patch = arr[row * 16 : (row + 1) * 16, col * 16 : (col + 1) * 16]
            grid_features.extend(patch.mean(axis=(0, 1)))

    hist_features = []
    for channel in range(3):
        hist, _ = np.histogram(arr[..., channel], bins=16, range=(0.0, 1.0), density=True)
        hist_features.extend(hist / max(hist.sum(), 1e-8))

    gray = arr.mean(axis=2)
    gx = np.diff(gray, axis=1, prepend=gray[:, :1])
    gy = np.diff(gray, axis=0, prepend=gray[:1, :])
    magnitude = np.sqrt(gx * gx + gy * gy)
    gradient_stats = [
        magnitude.mean(),
        magnitude.std(),
        *np.quantile(magnitude, [0.5, 0.75, 0.9, 0.95]),
    ]
    for row in range(4):
        for col in range(4):
            patch = magnitude[row * 16 : (row + 1) * 16, col * 16 : (col + 1) * 16]
            gradient_stats.append(patch.mean())

    return np.asarray(
        [
            *channel_stats,
            *hsv_stats,
            *grid_features,
            *hist_features,
            *gradient_stats,
        ],
        dtype=np.float32,
    )


def extract_batch(paths: list[str]) -> np.ndarray:
    features = []
    for path in paths:
        with Image.open(path) as image:
            features.append(extract_features(image))
    return np.vstack(features)

