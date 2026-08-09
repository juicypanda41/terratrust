from fastapi.testclient import TestClient

from api import app
from src.terratrust.config import DEMO_DIR


client = TestClient(app)


def test_health_reports_model_ready():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["model"] == "ready"


def test_bootstrap_exposes_evaluated_evidence():
    response = client.get("/api/bootstrap")
    assert response.status_code == 200
    payload = response.json()
    assert payload["metrics"]["status"] == "evaluated"
    assert payload["metrics"]["test_count"] == 4050
    assert len(payload["demos"]) == 20


def test_demo_analysis_returns_auditable_decision():
    response = client.post("/api/analyze/demo/Forest_1.jpg")
    assert response.status_code == 200
    payload = response.json()
    assert 0 <= payload["confidence"] <= 1
    assert isinstance(payload["requires_review"], bool)
    assert len(payload["probabilities"]) == 10
    assert payload["review_reason"]


def test_unknown_demo_is_rejected():
    response = client.post("/api/analyze/demo/not-a-real-tile.jpg")
    assert response.status_code == 404


def test_upload_without_verified_provenance_is_always_reviewed():
    image = (DEMO_DIR / "Forest_1.jpg").read_bytes()
    response = client.post(
        "/api/analyze/upload",
        files={"file": ("forest.jpg", image, "image/jpeg")},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["requires_review"] is True
    assert payload["scope_alert"] is True
    assert "outside the validated scope" in payload["review_reason"]
