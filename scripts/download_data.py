from __future__ import annotations

import hashlib
import shutil
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOWNLOAD_DIR = ROOT / "data" / "downloads"
RAW_DIR = ROOT / "data" / "raw"
ZIP_PATH = DOWNLOAD_DIR / "EuroSAT_RGB.zip"
URL = "https://zenodo.org/records/7711810/files/EuroSAT_RGB.zip?download=1"
EXPECTED_MD5 = "f46e308c4d50d4bf32fedad2d3d62f3b"


def md5(path: Path) -> str:
    digest = hashlib.md5()  # nosec B324 - integrity check specified by publisher
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if not ZIP_PATH.exists() or md5(ZIP_PATH) != EXPECTED_MD5:
        print("Downloading the official EuroSAT RGB archive from Zenodo...")
        with urllib.request.urlopen(URL) as response, ZIP_PATH.open("wb") as output:
            shutil.copyfileobj(response, output)

    actual = md5(ZIP_PATH)
    if actual != EXPECTED_MD5:
        raise RuntimeError(f"Checksum mismatch: expected {EXPECTED_MD5}, got {actual}")

    target = RAW_DIR / "EuroSAT_RGB"
    if not target.exists():
        print("Extracting EuroSAT...")
        with zipfile.ZipFile(ZIP_PATH) as archive:
            archive.extractall(RAW_DIR)

    print(f"Dataset ready: {target}")


if __name__ == "__main__":
    main()
