# Data

TerraTrust uses **EuroSAT RGB v2**, created by Patrick Helber, Benjamin Bischke, Andreas Dengel, and Damian Borth from Copernicus Sentinel-2 imagery.

The dataset is not committed to Git. Download the official archive and verify its publisher-provided checksum with:

```powershell
python scripts/download_data.py
```

Official record and citation: https://doi.org/10.5281/zenodo.7711810

The downloader expects MD5 `f46e308c4d50d4bf32fedad2d3d62f3b`, as published for `EuroSAT_RGB.zip` by Zenodo. Sentinel data is free and open; users should also review the Copernicus Sentinel Data Terms and Conditions linked from the official record.

Only a small set of held-out CC0 demo images is copied to `assets/demo_samples/` after evaluation so the hosted application can demonstrate inference without distributing the full dataset.

