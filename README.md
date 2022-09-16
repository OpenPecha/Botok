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

    pip3 install botok

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
>>> from botok import Text

>>> # input is a multi-line input string
>>> in_str = """ལེ གས། བཀྲ་ཤིས་མཐའི་ ༆ ཤི་བཀྲ་ཤིས་  tr 
... བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་༡༢༣ཀཀ། 
... མཐའི་རྒྱ་མཚོར་གནས་པའི་ཉས་ཆུ་འཐུང་།། །།མཁའ།"""


### STEP1: instanciating Text

>>> # A. on a string
>>> t = Text(in_str)

>>> # B. on a file
... # note all following operations can be applied to files in this way.
>>> from pathlib import Path
>>> in_file = Path.cwd() / 'test.txt'

>>> # file content:
>>> in_file.read_text()
'བཀྲ་ཤིས་བདེ་ལེགས།།\n'

>>> t = Text(in_file)
>>> t.tokenize_chunks_plaintext

>>> # checking an output file has been written:
... # BOM is added by default so that notepad in Windows doesn't scramble the line breaks
>>> out_file = Path.cwd() / 'test_pybo.txt'
>>> out_file.read_text()
'\ufeffབཀྲ་ ཤིས་ བདེ་ ལེགས །།'

### STEP2: properties will perform actions on the input string:
### note: original spaces are replaced by underscores.

>>> # OUTPUT1: chunks are meaningful groups of chars from the input string.
... # see how punctuations, numerals, non-bo and syllables are all neatly grouped.
>>> t.tokenize_chunks_plaintext
'ལེ_གས །_ བཀྲ་ ཤིས་ མཐའི་ _༆_ ཤི་ བཀྲ་ ཤིས་__ tr_\n བདེ་་ ལེ_གས །_ བཀྲ་ ཤིས་ བདེ་ ལེགས་ ༡༢༣ ཀཀ །_\n མཐའི་ རྒྱ་ མཚོར་ གནས་ པའི་ ཉས་ ཆུ་ འཐུང་ །།_།། མཁའ །'

>>> # OUTPUT2: could as well be acheived by in_str.split(' ')
>>> t.tokenize_on_spaces
'ལེ གས། བཀྲ་ཤིས་མཐའི་ ༆ ཤི་བཀྲ་ཤིས་ tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་༡༢༣ཀཀ། མཐའི་རྒྱ་མཚོར་གནས་པའི་ཉས་ཆུ་འཐུང་།། །།མཁའ།'

>>> # OUTPUT3: segments in words.
... # see how བདེ་་ལེ_གས was still recognized as a single word, even with the space and the double tsek.
... # the affixed particles are separated from the hosting word: མཐ འི་ རྒྱ་མཚོ ར་ གནས་པ འི་ ཉ ས་
>>> t.tokenize_words_raw_text
Loading Trie... (2s.)
'ལེ_གས །_ བཀྲ་ཤིས་ མཐ འི་ _༆_ ཤི་ བཀྲ་ཤིས་_ tr_ བདེ་་ལེ_གས །_ བཀྲ་ཤིས་ བདེ་ལེགས་ ༡༢༣ ཀཀ །_ མཐ འི་ རྒྱ་མཚོ ར་ གནས་པ འི་ ཉ ས་ ཆུ་ འཐུང་ །།_།། མཁའ །'
>>> t.tokenize_words_raw_lines
'ལེ_གས །_ བཀྲ་ཤིས་ མཐ འི་ _༆_ ཤི་ བཀྲ་ཤིས་__ tr_\n བདེ་་ལེ_གས །_ བཀྲ་ཤིས་ བདེ་ལེགས་ ༡༢༣ ཀཀ །_\n མཐ འི་ རྒྱ་མཚོ ར་ གནས་པ འི་ ཉ ས་ ཆུ་ འཐུང་ །།_།། མཁའ །'

>>> # OUTPUT4: segments in words, then calculates the number of occurences of each word found
... # by default, it counts in_str's substrings in the output, which is why we have བདེ་་ལེ གས	1, བདེ་ལེགས་	1
... # this behaviour can easily be modified to take into account the words that pybo recognized instead (see advanced usage)
>>> print(t.list_word_types)
འི་	3
། 	2
བཀྲ་ཤིས་	2
མཐ	2
ལེ གས	1
 ༆ 	1
ཤི་	1
བཀྲ་ཤིས་  	1
tr \n	1
བདེ་་ལེ གས	1
བདེ་ལེགས་	1
༡༢༣	1
ཀཀ	1
། \n	1
རྒྱ་མཚོ	1
ར་	1
གནས་པ	1
ཉ	1
ས་	1
ཆུ་	1
འཐུང་	1
།། །།	1
མཁའ	1
།	1
```

##### Custom dialect pack:

In order to use custom dialect pack:

- You need to prepare your dialect pack in same folder structure like [general dialect pack](https://github.com/Esukhia/botok-data/tree/master/dialect_packs/general)
- Then you need to instaintiate a config object where you will pass dialect name and path
- You can instaintiate your tokenizer object using that config object
- Your tokenizer will be using your custom dialect pack and it will be using trie pickled file in future to build the custom trie.

## Docs

No documentations.

<!-- This section must link to the docs which are in the root of the repository in /docs -->


## Owners

- [@drupchen](https://github.com/drupchen)
- [@eroux](https://github.com/eroux)
- [@ngawangtrinley](https://github.com/ngawangtrinley)
- [@10zinten](https://github.com/10zinten)
- [@kaldan007](https://github.com/kaldan007)

<!-- This section lists the owners of the repo -->


## Acknowledgements

**botok** is an open source library for Tibetan NLP.

We are always open to cooperation in introducing new features, tool integrations and testing solutions.

Many thanks to the companies and organizations who have supported botok's development, especially:

* [Khyentse Foundation](https://khyentsefoundation.org) for contributing USD22,000 to kickstart the project 
* The [Barom/Esukhia canon project](http://www.barom.org) for sponsoring training data curation
* [BDRC](https://tbrc.org) for contributing 2 staff for 6 months for data curation

## Maintainance

Build the source dist:

```
rm -rf dist/
python3 setup.py clean sdist
```

and upload on twine (version >= `1.11.0`) with:

```
twine upload dist/*
```

## License

The Python code is Copyright (C) 2019 Esukhia, provided under [Apache 2](LICENSE). 

contributors:
 * [Drupchen](https://github.com/drupchen)
 * [Élie Roux](https://github.com/eroux)
 * [Ngawang Trinley](https://github.com/ngawangtrinley)
 * [Mikko Kotila](https://github.com/mikkokotila)
 * [Thubten Rinzin](https://github.com/thubtenrigzin)

 * [Tenzin](https://github.com/10zinten)
 * Joyce Mackzenzie for reworking the logo
