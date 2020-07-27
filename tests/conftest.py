from pathlib import Path

import pytest

from botok import Config, Tokenize, WordTokenizer


@pytest.fixture(scope="session")
def empty_wt():
    """Return empty word tokenizer."""
    dialect_pack_path = Path("./tests/data/empty_dialect_pack")
    config = Config(dialect_pack_path=dialect_pack_path)
    return WordTokenizer(config=config)


@pytest.fixture(scope="session")
def wt():
    """Return default word tokenizer."""
    return WordTokenizer()
