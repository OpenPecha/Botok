# coding: utf8
import copy
from pathlib import Path

import pytest

from botok import Config
from botok.config import DEFAULT_BASE_PATH


@pytest.fixture(scope="module")
def base_path():
    return DEFAULT_BASE_PATH


def test_defaults(base_path):
    config = Config()

    # default dialect pach path
    assert config.dialect_pack_path == base_path / "general"
    assert config.dialect_pack_path.is_dir()

    # Trie data should be .tsv file
    for data_type in ["words", "rules"]:
        assert data_type in config.dictionary
        for data_fn in config.dictionary[data_type]:
            assert data_fn.suffix == ".tsv"

    # Segmentation adjustment
    for data_type in ["remove", "rules", "words", "words_skrt"]:
        assert data_type in config.adjustments
        for data_fn in config.adjustments[data_type]:
            if data_fn.suffix:
                assert data_fn.suffix == ".tsv"


def test_custome_dialect_pack(base_path):
    config = Config(dialect_name="kangyur")
    assert config.dialect_pack_path == base_path / "kangyur"
    assert config.dialect_pack_path.is_dir()


def test_reset(base_path):
    custome_pack_name = "kangyur"
    config = Config(dialect_name=custome_pack_name)
    assert config.dialect_pack_path == base_path / custome_pack_name

    config.reset()

    assert config.dialect_pack_path == base_path / "general"


def test_empty_config():
    config = Config.from_path("./tests/data/empty_dialect_pack")

    assert not config.dictionary
    assert not config.adjustments


def test_add_dialect_pack():
    config = Config()
    old_dictionary = copy.deepcopy(config.dictionary)
    old_adjustments = copy.deepcopy(config.adjustments)

    config.add_dialect_pack(Path("./tests/data/trie_dialect_pack"))

    assert config.dictionary != old_dictionary
    assert config.adjustments != old_adjustments
