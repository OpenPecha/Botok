import shutil
from pathlib import Path

from ..config import Config


def expose_data(out_path, profile=None):
    """ Copies all the trie and adjustment data to out_path
    :param out_path: must be an existing empty folder
    """
    if profile not in ["POS", "empty"]:
        raise SyntaxError('profile should be either one of ["POS", "empty"]')

    out_path = Path(out_path)
    if not out_path.is_dir() or list(out_path.glob("*")):
        raise IOError("out_path should be an empty folder")

    resources = Path(__file__).parent / "../resources"
    resources = resources.resolve()
    res_dirs = [r for r in resources.glob("*") if r.is_dir()]

    if profile:
        # export profile data
        for f in Config().config["tokenizers"]["profiles"][profile]:
            Path(out_path / Path(f).parent).mkdir(
                parents=True, exist_ok=True
            )  # create dir
            shutil.copy(resources / f, out_path / f)

        shutil.copytree(resources / "adjustment", out_path / "adjustment")

    else:
        # export all data
        for r in res_dirs:
            shutil.copytree(r, out_path / r.name)
