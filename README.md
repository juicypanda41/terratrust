# TerraTrust

TerraTrust is a land-cover screening tool that classifies satellite scenes and sends uncertain results to human verification. It was built for the **OurPlanet.Rocks 2026 Technical Track**.

**Live app:** [terratrustshaurya.vercel.app](https://terratrustshaurya.vercel.app/)

TerraTrust is a research prototype, not a replacement for GIS analysts, field surveys, or environmental experts.

## The problem

Land-cover models can return confident-looking predictions even when an image is ambiguous, degraded, or outside the data they were tested on. A wrong automated result can be more harmful than no result at all.

TerraTrust adds a decision layer around classification. Clear reference scenes can pass automatically, while low-confidence, low-margin, or out-of-scope images are held for a person to verify.

## How it works

1. Select a held-out reference scene or upload an RGB image.
2. The model predicts one of ten land-cover classes.
3. Temperature scaling calibrates the reported confidence.
4. Confidence, prediction margin, and image-quality checks determine whether the result can be accepted.
5. Uncertain results move to the Human verification screen with the reason they were held.
6. The Validation screen shows the measurements and assumptions behind that policy.

## Product walkthrough

| Screen | Purpose |
| --- | --- |
| **Overview** | Introduces the problem, workflow, and intended use. |
| **Analyze** | Runs a reference or uploaded image through the model and explains the result. |
| **Human verification** | Collects results that should not be accepted automatically. |
| **Validation** | Shows held-out performance, calibration, risk–coverage behavior, robustness tests, and limitations. |

For a short demo, open **Analyze**, choose **Ambiguous scene**, run the analysis, and send the held result to **Human verification**.

## Measured results

The following results come from a deterministic, stratified held-out EuroSAT RGB test split containing 4,050 images:

| Metric | Measured result |
| --- | ---: |
| Overall accuracy | 89.4% |
| Macro F1 | 88.9% |
| Accepted-case accuracy | 91.4% |
| Test scenes accepted by the full policy | 78.9% |
| Test scenes sent to human verification | 21.1% |
| Expected calibration error, before scaling | 2.55% |
| Expected calibration error, after scaling | 0.87% |
| Median warm local inference time | 16.2 ms |

The quality gate routed 98.5–100% of four controlled perturbation sets to verification. These are stress-test results, not evidence of complete real-world robustness. Hardware affects the reported latency.

See [metrics evidence](docs/metrics-evidence.md), the [validation plan](docs/validation-plan.md), and the [model card](MODEL_CARD.md) for definitions and methodology.

## Technical approach

The classifier combines deterministic image statistics, spatial color pooling, channel histograms, and gradient features with histogram gradient boosting. This kept training and deployment practical on ordinary hardware while leaving time to evaluate calibration and the human-verification policy.

```text
Satellite image
      |
      v
Feature extraction --> Classifier --> Temperature scaling
                                           |
                                           v
                         Confidence + margin + quality checks
                                   /               \
                                  v                 v
                         Accepted result     Human verification
```

### Stack

- React, Vite, and Framer Motion
- FastAPI
- scikit-learn, NumPy, pandas, Pillow, and joblib
- Vitest and pytest
- Vercel

The React production bundle and API are served through one FastAPI application. Model artifacts and the small held-out demo set are packaged with the deployment.

## Run locally

### Requirements

- Python 3.11 or newer
- Node.js 22 or newer
- pnpm 10.17.1

### Setup

```powershell
git clone https://github.com/juicypanda41/terratrust.git
cd terratrust

py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

cd frontend
corepack enable
pnpm install --frozen-lockfile
pnpm build
cd ..

.\.venv\Scripts\python.exe -m uvicorn api:app --host 127.0.0.1 --port 8501
```

Open [http://localhost:8501](http://localhost:8501).

The repository already contains the evaluated model and demo assets needed to run the app. Downloading the full dataset is only required to reproduce training.

## Reproduce the model

```powershell
.\.venv\Scripts\python.exe scripts\download_data.py
.\.venv\Scripts\python.exe scripts\train.py
```

The downloader uses the official EuroSAT release and verifies the publisher-provided checksum. Training creates the model, metrics, confusion matrix, calibration results, risk–coverage curve, and held-out demo manifest under `artifacts/` and `assets/demo_samples/`.

The split is deterministic and stratified, but not geographically separated. That limitation is documented in the interface and model card.

## Test the project

```powershell
.\.venv\Scripts\python.exe -m pytest

cd frontend
pnpm test
pnpm build
```

The backend tests cover feature extraction, calibration and reliability logic, inference behavior, API health, bootstrap data, demo analysis, upload validation, and error handling. The frontend test checks evidence loading and accessible navigation.

After deployment, these routes provide quick smoke tests:

```text
GET  /api/health
GET  /api/bootstrap
POST /api/analyze/demo/Forest_1.jpg
POST /api/analyze/upload
```

## Repository structure

```text
api.py                    FastAPI routes and production frontend server
frontend/                 React interface and UI test
src/terratrust/           Features, inference, calibration, and configuration
scripts/                  Data download, training, policy, and robustness tools
tests/                    Backend test suite
artifacts/                Evaluated model and generated evidence
assets/demo_samples/      Small held-out demonstration set
docs/                     Research, validation, architecture, demo, and rubric evidence
MODEL_CARD.md             Intended use, evaluation, safeguards, and limitations
vercel.json               Production deployment configuration
```

## Deployment

The production project is connected to the `main` branch and deploys on Vercel. The repository pins the frontend package manager, declares the FastAPI entrypoint, lists the Python runtime dependencies, and bundles the model, evidence, demo images, and built interface.

No environment variables are required for the current prototype.

For deployment details and smoke-test commands, see [docs/deployment.md](docs/deployment.md).

## SDG alignment

TerraTrust supports work related to:

- **SDG Target 15.1:** conserve, restore, and sustainably use terrestrial and inland freshwater ecosystems.
- **SDG Target 15.2:** promote sustainable forest management and halt deforestation.

The prototype measures classification reliability and review workload. It does not claim measured conservation, forest restoration, or deforestation outcomes.

## Data and attribution

EuroSAT was created by Patrick Helber, Benjamin Bischke, Andreas Dengel, and Damian Borth using Copernicus Sentinel-2 imagery.

- [Official EuroSAT dataset](https://doi.org/10.5281/zenodo.7711810)
- [EuroSAT paper](https://arxiv.org/abs/1709.00029)
- [Copernicus Sentinel-2](https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2/Changing_lands)
- [United Nations Goal 15](https://sdgs.un.org/goals/goal15)

The full dataset is not committed to this repository. The included demo images are a small attributed subset of held-out evaluation data. Dependencies and external tools are recorded in the [AI and tools disclosure](docs/ai-use-log.md).

## Current limits

TerraTrust does not provide segmentation, property boundaries, acreage, temporal change detection, carbon estimates, biodiversity measurement, or globally validated predictions. Uploaded images have no verified EuroSAT provenance and therefore remain subject to human verification.

## Hackathon documentation

- [Project brief](docs/project-brief.md)
- [Judging scorecard](docs/judging-scorecard.md)
- [Metrics evidence](docs/metrics-evidence.md)
- [Validation plan](docs/validation-plan.md)
- [Architecture](docs/architecture.md)
- [Scalability plan](docs/scalability-plan.md)
- [Demo script](docs/demo-script.md)
- [Demo rehearsal record](docs/demo-rehearsal-record.md)
- [AI and tools disclosure](docs/ai-use-log.md)

## License

The project code is available under the [MIT License](LICENSE). EuroSAT and Copernicus data remain subject to their source terms.
