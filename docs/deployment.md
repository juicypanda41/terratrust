# Sharing and Deployment

## GitHub

The repository intentionally includes code, tests, documentation, evaluated model artifacts, and a small demo sample set. The full EuroSAT archive is excluded because it is reproducibly downloadable from the official record.

Before publishing:

```powershell
git status
cd frontend
corepack pnpm install
corepack pnpm test
corepack pnpm build
cd ..
.\.venv\Scripts\python.exe -m pytest
```

## Container deployment

The included `Dockerfile` builds the React production bundle, installs the Python runtime, and serves both from port 8501.

```powershell
docker build -t terratrust .
docker run --rm -p 8501:8501 terratrust
```

Push the public repository to GitHub, connect it to a container host, and verify every destination in a signed-out browser. The service must expose port 8501 or map the platform-provided port to the Uvicorn command.

No secrets are required. The evaluated model and evidence artifacts must remain under GitHub's per-file size limit.

## Judge link check

- Open the GitHub repository while signed out.
- Open the deployed application while signed out.
- Analyze one accepted and one review-routed tile.
- Open the evidence charts and limitations.
- Confirm the README dataset, paper, ESA, and UN links.
- Confirm the 2-3 minute YouTube/Vimeo video is accessible.
