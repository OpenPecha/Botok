# Botok – Python Tibetan Tokenizer

[![GitHub release](https://img.shields.io/github/release/OpenPecha/botok.svg)](https://github.com/OpenPecha/botok/releases)
[![Documentation Status](https://readthedocs.org/projects/botok/badge/?version=latest)](https://botok.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/OpenPecha/botok/badge.svg?branch=master)](https://coveralls.io/github/OpenPecha/botok?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)
[![License](https://img.shields.io/github/license/OpenPecha/botok.svg)](https://github.com/OpenPecha/botok/blob/master/LICENSE)
[![Stars](https://img.shields.io/github/stars/OpenPecha/botok)](https://github.com/OpenPecha/Botok)

## Project Description

Botok is a powerful Python library for tokenizing Tibetan text. It segments text into words with high accuracy and provides optional attributes such as lemma, part-of-speech (POS) tags, and clean forms. The library supports various text formats, custom dialects, and multiple tokenization modes, making it a versatile tool for Tibetan Natural Language Processing (NLP).

## Who This Project Is For

This project is intended for developers and researchers working with Tibetan language text processing who need accurate word segmentation and tokenization.

## Project Dependencies

Before using Botok, ensure you have:

* Python 3.7+
* pip (Python package installer)

## Instructions for Installing Botok

### Install Botok

1. **Install via pip:**

   ```bash
   pip install botok
   ```

2. **Install from source:**

   ```bash
   git clone https://github.com/OpenPecha/Botok.git
   cd Botok
   pip install -e .
   ```

### Run Botok

```python
from botok import Botok

botok = Botok()
text = "བོད་ཡིག"
tokens = botok.tokenize(text)
print(tokens)
```

## Directory Structure

```
Botok/
├── .github/          # GitHub configuration
├── botok/            # Main package source code
├── docs/             # Documentation
├── tests/            # Test suite
├── requirements.txt  # Development dependencies
├── setup.py          # Package setup configuration
├── setup.cfg         # Package metadata
├── README.md         # Project documentation
├── CHANGELOG.md      # Release history
├── LICENSE           # License file
└── usage.py          # Usage examples
```

## Contributing Guidelines

Contributions are welcome! Please read the [contributing guidelines](https://github.com/OpenPecha/Botok/blob/master/README.md#contributing) for details on how to submit pull requests.

## Additional Documentation

* [Full Documentation](https://botok.readthedocs.io/)
* [API Reference](https://botok.readthedocs.io/en/latest/)

## How to Get Help

* [GitHub Issues](https://github.com/OpenPecha/Botok/issues)
* [OpenPecha Community](https://openpecha.org)

## Terms of Use

Botok is licensed under the MIT License.