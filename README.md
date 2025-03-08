<h1 align="center">
  <br>
  <a href="https://openpecha.org"><img src="https://avatars.githubusercontent.com/u/82142807?s=400&u=19e108a15566f3a1449bafb03b8dd706a72aebcd&v=4" alt="OpenPecha" width="150"></a>
  <br>
</h1>

<h3 align="center">Botok – Python Tibetan Tokenizer</h3>

<!-- Replace the title of the repository -->

<p align="center">
    <a><img src="https://img.shields.io/github/release/Esukhia/botok.svg" alt="GitHub release"></a> 
    <a href="https://botok.readthedocs.io/en/latest/?badge=latest"><img src="https://readthedocs.org/projects/botok/badge/?version=latest" alt="Documentation Status"></a> 
    <a href="https://travis-ci.org/Esukhia/botok"><img src="https://travis-ci.org/Esukhia/botok.svg?branch=master" alt="Build Status"></a> 
    <a href="https://coveralls.io/github/Esukhia/botok?branch=master"><img src="https://coveralls.io/repos/github/Esukhia/botok/badge.svg?branch=master" alt="Coverage Status"></a> 
    <a href="https://black.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a> 
</p>

<p align="center">
  <a href="#description">Description</a> •
  <a href="#install">Install</a> •
  <a href="#example">Example</a> •
  <a href="#commentedexample">Commented Example</a> •
  <a href="#docs">Docs</a> •
  <a href="#owners">Owners</a> •
  <a href="#Acknowledgements">Acknowledgements</a> •
  <a href="#Maintainance">Maintainance</a> •
  <a href="#License">License</a>
</p>
<hr>

## Description

Botok tokenizes Tibetan text into words with optional attributes such as lemma, POS, clean form.

## Install
Requires to have Python3 installed.

## Requirements

- Python 3.6 or higher
- pip package manager

## Installation

```bash
pip install botok
```

## Quick Start

## Example

```
from botok import WordTokenizer
from botok.config import Config
from pathlib import Path

def get_tokens(wt, text):
    tokens = wt.tokenize(text, split_affixes=False)
    return tokens

if __name__ == "__main__":
    config = Config(dialect_name="general", base_path= Path.home())
    wt = WordTokenizer(config=config)
    text = "བཀྲ་ཤིས་བདེ་ལེགས་ཞུས་རྒྱུ་ཡིན་ སེམས་པ་སྐྱིད་པོ་འདུག།"
    tokens = get_tokens(wt, text)
    for token in tokens:
        print(token)
```

https://user-images.githubusercontent.com/24893704/148767959-31cc0a69-4c83-4841-8a1d-028d376e4677.mp4

## Commented Example

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

## Docs

No documentations.

<!-- This section must link to the docs which are in the root of the repository in /docs -->

## Documentation

## Owners

- [@drupchen](https://github.com/drupchen)
- [@eroux](https://github.com/eroux)
- [@ngawangtrinley](https://github.com/ngawangtrinley)
- [@10zinten](https://github.com/10zinten)
- [@kaldan007](https://github.com/kaldan007)

<!-- This section lists the owners of the repo -->

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
