from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = ROOT / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "terratrust_model.joblib"
METRICS_PATH = ARTIFACT_DIR / "metrics.json"
RISK_COVERAGE_PATH = ARTIFACT_DIR / "risk_coverage.csv"
CONFUSION_PATH = ARTIFACT_DIR / "confusion_matrix.csv"
ROBUSTNESS_PATH = ARTIFACT_DIR / "robustness.csv"
DEMO_DIR = ROOT / "assets" / "demo_samples"

EUROSAT_CLASSES = [
    "AnnualCrop",
    "Forest",
    "HerbaceousVegetation",
    "Highway",
    "Industrial",
    "Pasture",
    "PermanentCrop",
    "Residential",
    "River",
    "SeaLake",
]

DISPLAY_NAMES = {
    "AnnualCrop": "Annual crop",
    "Forest": "Forest",
    "HerbaceousVegetation": "Herbaceous vegetation",
    "Highway": "Highway",
    "Industrial": "Industrial",
    "Pasture": "Pasture",
    "PermanentCrop": "Permanent crop",
    "Residential": "Residential",
    "River": "River",
    "SeaLake": "Sea / lake",
}
