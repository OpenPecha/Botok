# coding: utf-8
import io
import requests
import zipfile
import shutil
from pathlib import Path


def get_data(url, out_path):
    try:
        r = requests.get(url, stream=True, timeout=50)
    except:
        # check if there are previously downloaded files and return if there are any
        for f in out_path.glob("*"):
            if f.is_dir():
                return

        #   exit botok otherwise
        exit(
            "The data required to run botok is not yet downloaded and there is no connection. "
            "Please connect first and try again."
        )

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
        tmp = Path(__file__).parent  # / "botok-data-master"
        z.extractall(
            path=tmp, members=[a for a in z.namelist() if not a.endswith(".md")]
        )

        # copy folders in destination
        tmp = tmp / "botok-data-master"
        for dir in tmp.glob("*"):
            out_dir = out_path / dir.name
            if out_dir.is_dir():
                shutil.rmtree(out_dir, ignore_errors=True)
            shutil.copytree(dir, out_dir)

        # remove tmp folder
        shutil.rmtree(tmp, ignore_errors=True)
