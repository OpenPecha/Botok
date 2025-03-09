<h1 align="center">
  <br>
  <a href="https://openpecha.org"><img src="https://avatars.githubusercontent.com/u/82142807?s=400&u=19e108a15566f3a1449bafb03b8dd706a72aebcd&v=4" alt="OpenPecha" width="150"></a>
  <br>
</h1>

<h3 align="center">Botok – Python Tibetan Tokenizer</h3>

<p align="center">
    <a href="https://github.com/OpenPecha/botok/releases"><img src="https://img.shields.io/github/release/OpenPecha/botok.svg" alt="GitHub release"></a> 
    <a href="https://botok.readthedocs.io/en/latest/?badge=latest"><img src="https://readthedocs.org/projects/botok/badge/?version=latest" alt="Documentation Status"></a> 
    <a href="https://coveralls.io/github/OpenPecha/botok?branch=master"><img src="https://coveralls.io/repos/github/OpenPecha/botok/badge.svg?branch=master" alt="Coverage Status"></a> 
    <a href="https://black.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
    <a href="https://github.com/OpenPecha/botok/blob/master/LICENSE"><img src="https://img.shields.io/github/license/OpenPecha/botok.svg" alt="License"></a>
</p>

<p align="center">
  <a href="#description">Description</a> •
  <a href="#key-features">Key Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#basic-usage">Basic Usage</a> •
  <a href="#advanced-usage">Advanced Usage</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#development">Development</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#acknowledgements">Acknowledgements</a>
</p>

<hr>

## Description

Botok is a powerful Python library for tokenizing Tibetan text. It segments text into words with high accuracy and provides optional attributes such as lemma, part-of-speech (POS) tags, and clean forms. The library supports various text formats, custom dialects, and multiple tokenization modes, making it a versatile tool for Tibetan Natural Language Processing (NLP).

## Key Features
- **Word Segmentation**: Accurate word segmentation with support for affixed particles
- **Multiple Tokenization Modes**: 
  - Word tokenization
  - Chunk tokenization (groups of meaningful characters)
  - Space-based tokenization
- **Rich Token Attributes**:
  - Lemmatization
  - POS tagging
  - Clean form generation
- **Custom Dialect Support**: Use pre-configured dialects or create your own
- **File Processing**: Process both strings and files with automatic output generation
- **Robust Handling**: Manages complex cases like double tseks and spaces within words

## Installation

### Requirements

- Python 3.6 or higher
- pip package manager

### Basic Installation

```bash
pip install botok
```

### Development Installation

```bash
git clone https://github.com/OpenPecha/botok.git
cd botok
pip install -e .
```

## Basic Usage

### Simple Word Tokenization

```python
from botok import WordTokenizer
from botok.config import Config
from pathlib import Path

# Initialize tokenizer with default configuration
config = Config(dialect_name="general", base_path=Path.home())
wt = WordTokenizer(config=config)

# Tokenize text
text = "བཀྲ་ཤིས་བདེ་ལེགས་ཞུས་རྒྱུ་ཡིན་ སེམས་པ་སྐྱིད་པོ་འདུག།"
tokens = wt.tokenize(text, split_affixes=False)

# Print each token
for token in tokens:
    print(token)
```

### File Processing

```python
from botok import Text
from pathlib import Path

# Process a file
input_file = Path("input.txt")
t = Text(input_file)
t.tokenize_chunks_plaintext  # Creates input_pybo.txt with tokenized output
```

## Advanced Usage

### Custom Dialect Configuration

```python
from botok import WordTokenizer
from botok.config import Config
from pathlib import Path

# Configure custom dialect
config = Config(
    dialect_name="custom",
    base_path=Path.home() / "my_dialects"
)

# Initialize tokenizer with custom config
wt = WordTokenizer(config=config)

# Process text with custom settings
text = "བཀྲ་ཤིས་བདེ་ལེགས།"
tokens = wt.tokenize(
    text,
    split_affixes=True,
    pos_tagging=True,
    lemmatize=True
)
```

### Different Tokenization Modes

```python
from botok import Text

text = """ལེ གས། བཀྲ་ཤིས་མཐའི་ ༆ ཤི་བཀྲ་ཤིས་"""
t = Text(text)

# 1. Word tokenization
words = t.tokenize_words_raw_text

# 2. Chunk tokenization (groups of meaningful characters)
chunks = t.tokenize_chunks_plaintext

# 3. Space-based tokenization
spaces = t.tokenize_on_spaces
```

## Documentation

For comprehensive documentation, visit:
- [ReadTheDocs](https://botok.readthedocs.io/) - Full API documentation
- [Wiki](https://github.com/OpenPecha/botok/wiki) - Guides and tutorials
- [Examples](https://github.com/OpenPecha/botok/tree/master/examples) - Code examples

## Development

### Building from Source

```bash
rm -rf dist/
python setup.py clean sdist
```

### Publishing to PyPI

#### Automated Publishing with Semantic Versioning

The repository is configured with GitHub Actions to automatically handle version bumping and publishing to PyPI when changes are pushed to the master branch. The workflow uses semantic versioning based on commit messages:

1. Use the following commit message formats:
   - `fix: your message` - For bug fixes (triggers PATCH version bump)
   - `feat: your message` - For new features (triggers MINOR version bump)
   - Add `BREAKING CHANGE: description` in the commit body for breaking changes (triggers MAJOR version bump)

   Examples:
   ```
   # This will trigger a PATCH version bump (e.g., 0.8.12 → 0.8.13)
   fix: improve test coverage to 90% and fix Python 3.12 compatibility
   
   # This will trigger a MINOR version bump (e.g., 0.8.12 → 0.9.0)
   feat: add new sentence tokenization mode for complex Tibetan sentences
   
   # This will trigger a MAJOR version bump (e.g., 0.8.12 → 1.0.0)
   feat: refactor token attributes structure
   
   BREAKING CHANGE: Token.attributes now uses a dictionary format instead of properties, requiring changes to code that accesses token attributes directly
   ```

2. When you push to the master branch, the CI workflow will:
   - Run all tests across multiple Python versions
   - Analyze commit messages to determine the next version number
   - Update version numbers in the code
   - Create a new release on GitHub
   - Publish the package to PyPI

#### Manual Publishing

For manual publishing (if needed):

```bash
twine upload dist/*
```

### Running Tests

```bash
pytest tests/
```

## Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your PR adheres to:
- [Code style guidelines](https://black.readthedocs.io/en/stable/)
- Test coverage requirements
- Documentation standards

## Project Owners

- [@drupchen](https://github.com/drupchen)
- [@eroux](https://github.com/eroux)
- [@ngawangtrinley](https://github.com/ngawangtrinley)
- [@10zinten](https://github.com/10zinten)
- [@kaldan007](https://github.com/kaldan007)

## Acknowledgements

**botok** is an open source library for Tibetan NLP. We are grateful to our sponsors and contributors:

### Sponsors

* [Khyentse Foundation](https://khyentsefoundation.org) - USD22,000 initial funding
* [Barom/Esukhia canon project](http://www.barom.org) - Training data curation
* [BDRC](https://tbrc.org) - Staff contribution for data curation

### Contributors

* [Drupchen](https://github.com/drupchen) - Core development
* [Élie Roux](https://github.com/eroux) - Architecture and development
* [Ngawang Trinley](https://github.com/ngawangtrinley) - Project management
* [Mikko Kotila](https://github.com/mikkokotila) - Development
* [Thubten Rinzin](https://github.com/thubtenrigzin) - Testing and documentation
* [Tenzin](https://github.com/10zinten) - Development
* Joyce Mackzenzie - Logo design

## License

Copyright (C) 2019-2025 OpenPecha. Licensed under [Apache 2.0](LICENSE).
