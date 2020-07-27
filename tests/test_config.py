# coding: utf8
import copy
from pathlib import Path

import pytest

from botok import Config


@pytest.fixture()
def base_path():
    return Path.home() / "Documents" / "pybo" / "dialect_packs"


def test_defaults(base_path):
    config = Config()

    # default dialect pach path
    assert config.dialect_pack_path == base_path / "bo_general"

    # Trie data should be .tsv file
    for data_type in ["words", "rules"]:
        assert data_type in config.dictionary
        for data_fn in config.dictionary[data_type]:
            assert data_fn.suffix == ".tsv"

    # Segmentation adjustment
    for data_type in ["remove", "rules", "words", "words_skrt"]:
        assert data_type in config.adjustments
        for data_fn in config.adjustments[data_type]:
            assert data_fn.suffix == ".tsv"


def test_custome_dialect_pack(base_path):
    pack_path = base_path / "bo_kangyur"
    config = Config(dialect_pack_path=pack_path)
    assert config.dialect_pack_path == pack_path


def test_reset(base_path):
    custome_pack_path = base_path / "bo_kangyur"
    default_pack_path = base_path / "bo_general"

    config = Config(dialect_pack_path=custome_pack_path)
    assert config.dialect_pack_path == custome_pack_path

    config.reset()

    assert config.dialect_pack_path == default_pack_path


def test_empty_config():
    config = Config(Path("./tests/data/empty_dialect_pack"))

    assert not config.dictionary
    assert not config.adjustments


def test_add_dialect_pack():
    config = Config()
    old_dictionary = copy.deepcopy(config.dictionary)
    old_adjustments = copy.deepcopy(config.adjustments)

    config.add_dialect_pack(Path("./tests/data/trie_dialect_pack"))

    assert config.dictionary != old_dictionary
    assert config.adjustments != old_adjustments
