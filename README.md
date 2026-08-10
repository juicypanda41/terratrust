# TerraTrust

**Satellite screening that knows when to stop.**

TerraTrust is a human-in-the-loop land-cover screening prototype built for the OurPlanet.Rocks 2026 Technical Track. It classifies clear EuroSAT scenes automatically, calibrates confidence, and sends ambiguous cases to a review queue instead of forcing a prediction.

> TerraTrust is a research and demonstration tool. It is not a replacement for GIS analysts, field surveys, or environmental experts.

## Why it matters

Sentinel-2 imagery supports land-cover and forest monitoring, but raw classification confidence can be misleading. TerraTrust makes uncertainty operational: a validation-selected threshold controls whether a result is eligible for auto-acceptance or requires human review.

## Working product

- Ten-class EuroSAT RGB scene classification.
- Temperature-scaled confidence.
- Validation-selected abstention threshold.
- Analyze-tile experience with top-two predictions.
- Human review queue.
- Risk-coverage, calibration, and confusion-matrix evidence.
- Reproducible training and held-out evaluation.
- Explicit limitations and decision safeguards.

## Evaluated results

On a deterministic held-out EuroSAT RGB test set of 4,050 images:

- **89.4%** overall accuracy and **88.9%** macro F1.
- **91.4%** accuracy on the **78.9%** of tiles accepted by the complete confidence-plus-quality policy.
- **21.1%** routed to human review.
- Expected calibration error improved from **2.55% to 0.87%**.
- Median warm local inference was **16.2 ms** across 100 images; hardware affects this result.
- A validation-trained quality gate routed **98.5%-100%** of four controlled test perturbations to review. This stress test does not establish complete real-world robustness.

## Quick start in VS Code

1. Open this folder in VS Code.
2. Create the environment:

   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Download the official EuroSAT RGB release:

   ```powershell
   .\.venv\Scripts\python.exe scripts\download_data.py
   ```

4. Reproduce training and evaluation:

   ```powershell
   .\.venv\Scripts\python.exe scripts\train.py
   ```

5. Install and build the React interface (Node.js 22+):

   ```powershell
   cd frontend
   corepack enable
   pnpm install
   pnpm test
   pnpm build
   cd ..
   ```

6. Run tests and the application:

   ```powershell
   .\.venv\Scripts\python.exe -m pytest
   .\.venv\Scripts\python.exe -m uvicorn api:app --host 127.0.0.1 --port 8501
   ```

7. Open `http://localhost:8501`. For the fastest demo, choose **Analyze**, select **Ambiguous scene**, run screening, and add the result to the review queue.

VS Code tasks and debug configurations for these commands are included under `.vscode/`.

## Evidence contract

The interface reads its headline claims from generated files under `artifacts/`:

- `metrics.json`
- `risk_coverage.csv`
- `confusion_matrix.csv`
- `terratrust_model.joblib`

Calibration and threshold selection use validation data only. Final metrics use a held-out test split. The exact split is deterministic and stratified, but not geographic; this limitation is displayed throughout the project.

## Repository map

```text
api.py                         FastAPI model bridge and production web server
frontend/                      React/Vite product interface and UI test
src/terratrust/                Features, calibration, inference, configuration
scripts/download_data.py       Official download plus checksum validation
scripts/train.py               Reproducible train/validation/test evaluation
tests/                         Fast automated tests
artifacts/                     Evaluated model and evidence outputs
assets/demo_samples/           Small held-out demo set
docs/                          Architecture, research, validation, demo, rubric
design-system/terratrust/      Persisted UI source of truth
MODEL_CARD.md                  Intended use and limitations
```

The interface uses a quiet management-tool design system: warm paper, thin rules, restrained serif headings, one field-green action color, and amber review states. The current interface avoids decorative page animation; only loading feedback moves. The production bundle is served by FastAPI, so judges need one URL.

## Model approach

The hackathon model combines deterministic image statistics, spatial color pooling, channel histograms, and gradient features with histogram gradient boosting. This approach was selected because it trains on ordinary hardware, keeps deployment lightweight, and leaves enough time to build and validate the responsible decision workflow.

See [MODEL_CARD.md](MODEL_CARD.md) and [docs/architecture.md](docs/architecture.md) for details.

## SDG alignment

TerraTrust is an enabling tool aligned to:

- **SDG Target 15.1:** conservation, restoration, and sustainable use of terrestrial and inland freshwater ecosystems.
- **SDG Target 15.2:** sustainable forest management and efforts to halt deforestation.

The current prototype measures classification reliability and potential review-workload reduction. It does not claim measured conservation or deforestation outcomes.

## Data and attribution

EuroSAT was created by Patrick Helber, Benjamin Bischke, Andreas Dengel, and Damian Borth from Copernicus Sentinel-2 imagery.

- Official dataset: https://doi.org/10.5281/zenodo.7711810
- Paper: https://arxiv.org/abs/1709.00029
- Sentinel-2 context: https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2/Changing_lands
- UN Goal 15: https://sdgs.un.org/goals/goal15

The full dataset is not stored in Git. The downloader verifies the publisher-provided checksum. Small demo images copied from held-out evaluation data retain their source attribution.

## Limits

TerraTrust does not provide segmentation, boundaries, acreage, temporal change detection, carbon estimates, biodiversity measurement, or validated global deployment. See the model card for operational safeguards.

## Hackathon materials

- [Submission-grade project brief](docs/project-brief.md)
- [Judging scorecard](docs/judging-scorecard.md)
- [AI-use disclosure](docs/ai-use-log.md)
- [Validation plan](docs/validation-plan.md)
- [2:40 demo script](docs/demo-script.md)

## License

Project code is available under the MIT License. Dataset usage remains subject to the official EuroSAT and Copernicus terms described by the source record.
