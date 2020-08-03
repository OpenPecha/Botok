import io
import shutil
import zipfile
from collections import defaultdict
from pathlib import Path

import requests

# Defaults
DEFAULT_BASE_PATH = Path.home() / "Documents" / "pybo" / "dialect_packs"
DEFAULT_DIALECT_PACK = "general"


def get_dialect_pack_url(dialect_name, version=None):
    response = requests.get(
        "https://api.github.com/repos/Esukhia/botok-data/releases/latest"
    )
    if not version:
        version = response.json()["tag_name"]
    return f"https://github.com/Esukhia/botok-data/releases/download/{version}/{dialect_name}.zip"


def get_dialect_pack(dialect_name, out_dir, version=None):
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True, parents=True)
    dialect_pack_path = out_dir / dialect_name
    if dialect_pack_path.is_dir():
        return dialect_pack_path

    print(f"[INFO] Downloading {dialect_name} dialect pack ...")
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

    print(f"[INFO] Download completed!")

    return dialect_pack_path


class Config:
    """botok config for Tibetan dialect pack.

    Each dialect pack has two components:
      1. Dictionary:
         - contains all the data required to construct the Trie.
         - It should in the directory called `dictionary` inside the dialect pack directory.
      2. Adjustment:
         - Contains all the data required to adjust the text segmentation rules.
    """

    def __init__(self, dialect_name=None, base_path=None):
        """Create config for given `dialect_name` and stored in `base_path`"""
        if not dialect_name:
            dialect_name = DEFAULT_DIALECT_PACK
        if not base_path:
            base_path = DEFAULT_BASE_PATH
        dialect_pack_path = get_dialect_pack(dialect_name, base_path)
        self.reset(dialect_pack_path)

    def reset(self, dialect_pack_path=None):
        """Reset the config to default bo_general_pack."""
        if dialect_pack_path:
            self.dialect_pack_path = dialect_pack_path
        else:
            self.dialect_pack_path = get_dialect_pack(
                DEFAULT_DIALECT_PACK, DEFAULT_BASE_PATH
            )
        self.dictionary = self._get_pack_component("dictionary")
        self.adjustments = self._get_pack_component("adjustments")

    def _get_pack_component(self, pack_component_name, pack_component=None):
        """Return all the data_paths of the `pack_component.

        data_paths stored in python `dict` as per the directory
        structure of the pack component.
        """
        if not pack_component:
            pack_component = defaultdict(list)
        for path in (self.dialect_pack_path / pack_component_name).iterdir():
            if not path.is_dir():
                continue
            data_type = path.name
            pack_component[data_type].extend(list(path.rglob("*.tsv")))
        return pack_component

    @classmethod
    def from_path(cls, dialect_pack_path):
        """Creates config from ``dialect_pack_path``.

        Returns:
            :class: `Config`: An instance of a Configuration object

        Examples::

            config = Config.from_path(path_to_dialect_pack)
            assert config.dictionary == True
            assert config.adjustments == True

        """
        path = Path(dialect_pack_path)
        dialect_name = path.name
        base_path = path.parent
        return cls(dialect_name, base_path)

    @property
    def profile(self):
        """Returns profile name of the dialect_pack."""
        return self.dialect_pack_path.name

    def add_dialect_pack(self, path):
        """"Merge given dialect_pack at `path` to current dialect_pack."""
        self.dialect_pack_path = path
        self._get_pack_component("dictionary", self.dictionary)
        self._get_pack_component("adjustments", self.adjustments)
