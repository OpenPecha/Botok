import pytest

from botok import Config, Tokenize, WordTokenizer


@pytest.fixture(scope="session")
def empty_wt():
    """Return empty word tokenizer."""
    config = Config.from_path("./tests/data/empty_dialect_pack")
    return WordTokenizer(config=config)


@pytest.fixture(scope="session")
def wt():
    """Return default word tokenizer."""
    return WordTokenizer()
