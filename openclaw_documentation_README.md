<h1 align="center">
  <br>
  <a href="https://buddhistai.tools/"><img src="https://raw.githubusercontent.com/WeBuddhist/visual-assets/refs/heads/main/logo/WB-logo-purple.png" alt="OpenPecha" width="150"></a>
  <br>
</h1>

<h1 align="center">Botok</h1>

<p align="center">
  |Apache-2.0| |Python| |NLP|
</p>

🏷 བོད་ཏོག [pʰøtɔk̚] Tibetan word tokenizer in Python

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [How to get help](#how-to-get-help)
- [Terms of use](#terms-of-use)

## Features

- Tibetan word tokenization using statistical and rule-based methods
- Support for both classical and modern Tibetan
- Integration with PyBo (Python Buddhist)
- Customizable segmentation rules
-字典-based word lookup

## Prerequisites

- Python 3.8+
- pip

## Installation

```bash
# Clone the repository
git clone https://github.com/OpenPecha/Botok.git
cd Botok

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Configuration

Botok can be configured via:
- Environment variables
- YAML configuration files in `config/`
- Python API

## Usage

```python
import botok

# Create a tokenizer instance
tokenizer = botok.Tok()

# Tokenize Tibetan text
text = "བོད་ཡིག་གི་དཔེ་ཆ་"
tokens = tokenizer.tokenize(text)
print(tokens)
```

## Development

```bash
# Install dev dependencies
pip install -e .[dev]

# Run tests
pytest

# Lint
flake8 botok/
```

## Testing

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

Please read [CONTRIBUTING.md](https://github.com/OpenPecha/.github/blob/main/CONTRIBUTING.md) for details.

## How to get help
* File an issue.
* Join our [discord](https://discord.com/invite/7GFpPFSTeA).

## Terms of use
Botok is licensed under the [Apache-2.0 License](/LICENSE).