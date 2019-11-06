import shutil
from pathlib import Path


def expose_data(out_path):
    """ Copies all the trie and adjustment data to out_path
    :param out_path: must be an existing empty folder
    """
    out_path = Path(out_path)
    if not out_path.is_dir() or list(out_path.glob("*")):
        raise IOError("out_path should be an empty folder")

    resources = Path(__file__).parent / "../resources"
    resources = resources.resolve()
    res_dirs = [r for r in resources.glob("*") if r.is_dir()]

    for r in res_dirs:
        shutil.copytree(r, out_path / r.name)
