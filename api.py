from __future__ import annotations

import csv
import io
import json
from dataclasses import asdict
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError

from src.terratrust.config import (
    DEMO_DIR,
    DISPLAY_NAMES,
    METRICS_PATH,
    MODEL_PATH,
    ROBUSTNESS_PATH,
    RISK_COVERAGE_PATH,
    ROOT,
)
from src.terratrust.inference import TerraTrustModel

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
FRONTEND_DIST = ROOT / "frontend" / "dist"

app = FastAPI(
    title="TerraTrust API",
    description="Local model bridge for responsible EuroSAT land-cover screening.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@lru_cache(maxsize=1)
def get_model() -> TerraTrustModel:
    if not MODEL_PATH.exists():
        raise RuntimeError("Evaluated model artifact is missing. Run scripts/train.py first.")
    return TerraTrustModel.load(str(MODEL_PATH))


@lru_cache(maxsize=1)
def get_metrics() -> dict:
    if not METRICS_PATH.exists():
        raise RuntimeError("Evaluation metrics are missing. Run scripts/train.py first.")
    return json.loads(METRICS_PATH.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def demo_manifest() -> list[dict[str, str]]:
    path = DEMO_DIR / "manifest.json"
    if not path.exists():
        return []
    items = json.loads(path.read_text(encoding="utf-8"))
    stories = {
        "Forest_1.jpg": "Clear forest",
        "Highway_2.jpg": "Ambiguous scene",
        "Highway_1.jpg": "Difficult road scene",
    }
    priority = {"Forest_1.jpg": 0, "Highway_2.jpg": 1, "Highway_1.jpg": 2}
    ordered = sorted(items, key=lambda item: (priority.get(item["file"], 99), item["file"]))
    return [
        {
            **item,
            "display_label": DISPLAY_NAMES.get(item["label"], item["label"]),
            "story": stories.get(item["file"], "Held-out sample"),
            "image_url": f"/demo-assets/{item['file']}",
        }
        for item in ordered
    ]


def serialize_result(result) -> dict:
    payload = asdict(result)
    payload["predicted_display"] = DISPLAY_NAMES.get(result.predicted_class, result.predicted_class)
    payload["second_display"] = DISPLAY_NAMES.get(result.second_class, result.second_class)
    payload["probabilities"] = [
        {
            "class_name": name,
            "display_name": DISPLAY_NAMES.get(name, name),
            "probability": probability,
        }
        for name, probability in sorted(
            result.probabilities.items(), key=lambda item: item[1], reverse=True
        )
    ]
    return payload


@app.get("/api/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "model": "ready" if MODEL_PATH.exists() else "missing",
        "frontend": "ready" if FRONTEND_DIST.exists() else "development",
    }


@app.get("/api/bootstrap")
def bootstrap() -> dict:
    try:
        metrics = get_metrics()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    risk_coverage = read_csv(RISK_COVERAGE_PATH)
    return {
        "metrics": metrics,
        "demos": demo_manifest(),
        "robustness": read_csv(ROBUSTNESS_PATH),
        "risk_coverage": risk_coverage[::5] + risk_coverage[-1:] if risk_coverage else [],
    }


@app.post("/api/analyze/demo/{filename}")
def analyze_demo(filename: str) -> dict:
    allowed = {item["file"]: item for item in demo_manifest()}
    if filename not in allowed:
        raise HTTPException(status_code=404, detail="Demo tile was not found.")
    try:
        image = Image.open(DEMO_DIR / filename).convert("RGB")
        result = get_model().predict(image)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {**serialize_result(result), "source_label": allowed[filename]["display_label"]}


@app.post("/api/analyze/upload")
async def analyze_upload(file: UploadFile = File(...)) -> dict:
    if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(status_code=415, detail="Use a JPEG, PNG, or WebP RGB image.")
    contents = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(contents) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Image must be 10 MB or smaller.")
    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        result = get_model().predict(image)
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(status_code=422, detail="The uploaded file is not a readable image.") from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    payload = serialize_result(result)
    return {
        **payload,
        "requires_review": True,
        "scope_alert": True,
        "model_review_reason": payload["review_reason"],
        "review_reason": "Uploaded imagery has no verified EuroSAT provenance and remains outside the validated scope.",
        "source_label": None,
    }


app.mount("/demo-assets", StaticFiles(directory=DEMO_DIR), name="demo-assets")


if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="frontend-assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def frontend(full_path: str) -> FileResponse:
        candidate = (FRONTEND_DIST / full_path).resolve()
        if full_path and FRONTEND_DIST.resolve() in candidate.parents and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(FRONTEND_DIST / "index.html")
