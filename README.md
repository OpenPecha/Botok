# botok – Python Tibetan Tokenizer

![GitHub release](https://img.shields.io/github/release/Esukhia/botok.svg) [![Documentation Status](https://readthedocs.org/projects/botok/badge/?version=latest)](https://botok.readthedocs.io/en/latest/?badge=latest) [![Build Status](https://travis-ci.org/Esukhia/botok.svg?branch=master)](https://travis-ci.org/Esukhia/botok) [![Coverage Status](https://coveralls.io/repos/github/Esukhia/botok/badge.svg?branch=master)](https://coveralls.io/github/Esukhia/botok?branch=master) [![CodeFactor](https://www.codefactor.io/repository/github/esukhia/botok/badge)](https://www.codefactor.io/repository/github/esukhia/botok) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)

## Overview

Botok is a powerful Tibetan text tokenizer that segments Tibetan text into words with high accuracy. It handles various text formats, supports custom dialects, and provides multiple tokenization modes.

### Features

- Word segmentation with support for affixed particles
- Multiple tokenization modes (chunks, spaces, words)
- Custom dialect support
- File and string input processing
- Word frequency counting
- Handles complex cases like double tseks and spaces within words

## Requirements

- Python 3.6 or higher
- pip package manager

## Installation

```bash
pip install botok
```

## Quick Start

```python
from botok import Text

# Process a string
text = "བཀྲ་ཤིས་བདེ་ལེགས།"
t = Text(text)
tokens = t.tokenize_words_raw_text
print(tokens)

# Process a file
from pathlib import Path
file_path = Path("input.txt")
t = Text(file_path)
t.tokenize_chunks_plaintext  # Outputs to input_pybo.txt
```

## Usage Modes

### 1. Basic Tokenization
```python
from botok import Text

text = """ལེ གས། བཀྲ་ཤིས་མཐའི་ ༆ ཤི་བཀྲ་ཤིས་"""
t = Text(text)

# Get word tokens
tokens = t.tokenize_words_raw_text

# Get chunks (meaningful groups of characters)
chunks = t.tokenize_chunks_plaintext

# Split on spaces
spaces = t.tokenize_on_spaces
```

### 2. Custom Dialect Support

```python
from botok import WordTokenizer
from botok.config import Config
from pathlib import Path

# Configure custom dialect
config = Config(
    dialect_name="custom",
    base_path=Path.home()
)

# Initialize tokenizer
wt = WordTokenizer(config=config)

# Process text
text = "བཀྲ་ཤིས་བདེ་ལེགས།"
tokens = wt.tokenize(text, split_affixes=False)
```

## Documentation

For detailed documentation, visit our [ReadTheDocs page](https://botok.readthedocs.io/).

## Development

### Building from Source

```bash
rm -rf dist/
python setup.py clean sdist
```

### Publishing to PyPI

```bash
twine upload dist/*
```

## Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## Acknowledgements

**botok** is an open source library for Tibetan NLP.

Special thanks to our sponsors:

* [Khyentse Foundation](https://khyentsefoundation.org) - USD22,000 initial funding
* [Barom/Esukhia canon project](http://www.barom.org) - Training data curation
* [BDRC](https://tbrc.org) - Staff contribution for data curation

## Contributors

* [Drupchen](https://github.com/drupchen)
* [Élie Roux](https://github.com/eroux)
* [Ngawang Trinley](https://github.com/ngawangtrinley)
* [Mikko Kotila](https://github.com/mikkokotila)
* [Thubten Rinzin](https://github.com/thubtenrigzin)
* [Tenzin](https://github.com/10zinten)
* Joyce Mackzenzie - Logo design

## License

Copyright (C) 2019 Esukhia. Licensed under [Apache 2.0](LICENSE).
