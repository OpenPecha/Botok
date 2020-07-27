# coding: utf-8
import io
import shutil
import zipfile
from pathlib import Path

import requests


def get_dialect_pack_url(dialect_name, version=None):
    response = requests.get(
        "https://api.github.com/repos/Esukhia/botok-data/releases/latest"
    )
    if not version:
        version = response.json()["tag_name"]
    return f"https://github.com/Esukhia/botok-data/releases/download/{version}/{dialect_name}.zip"


def download_dialect_pack(dialect_name, out_dir, version=None):
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True, parents=True)
    dialect_pack_path = out_dir / dialect_name
    if dialect_pack_path.is_dir():
        return dialect_pack_path

    # Download the dialect pack
    url = get_dialect_pack_url(dialect_name, version)
    r = requests.get(url, stream=True, timeout=50)

    # attempt 50 times to download the zip
    check = zipfile.is_zipfile(io.BytesIO(r.content))
    attempts = 0
    while not check and attempts < 50:
        r = requests.get(url, stream=True, timeout=50)
        check = zipfile.is_zipfile(io.BytesIO(r.content))
        attempts += 1

    if not check:
        raise IOError("the .zip file couldn't be downloaded.")
    else:
        # extract the zip in the current folder
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(path=str(out_dir))

    return dialect_pack_path
