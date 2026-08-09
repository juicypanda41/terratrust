# Sharing and Deployment

## GitHub

The repository intentionally includes code, tests, documentation, evaluated model artifacts, and a small demo sample set. The full EuroSAT archive is excluded because it is reproducibly downloadable from the official record.

Before publishing:

```powershell
git status
python -m pytest
```

## Streamlit Community Cloud

1. Push the public repository to GitHub.
2. Sign in to https://share.streamlit.io/ with GitHub.
3. Choose the repository and `main` branch.
4. Set the entry point to `app.py`.
5. Deploy and verify every tab in a private/incognito browser window.

No secrets are required. The evaluated model and evidence artifacts must remain under GitHub's per-file size limit.

## Judge link check

- Open the GitHub repository while signed out.
- Open the deployed application while signed out.
- Analyze one accepted and one review-routed tile.
- Open the evidence charts and limitations.
- Confirm the README dataset, paper, ESA, and UN links.
- Confirm the 2-3 minute YouTube/Vimeo video is accessible.

