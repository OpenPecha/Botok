# botok – Python Tibetan Tokenizer
[![Build Status](https://travis-ci.org/Esukhia/pybo.svg?branch=master)](https://travis-ci.org/Esukhia/botok)  [![Coverage Status](https://coveralls.io/repos/github/Esukhia/botok/badge.svg?branch=master)](https://coveralls.io/github/Esukhia/botok?branch=master) ![GitHub release](https://img.shields.io/github/release/Esukhia/botok.svg) [![CodeFactor](https://www.codefactor.io/repository/github/esukhia/botok/badge)](https://www.codefactor.io/repository/github/esukhia/botok) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)


## Overview

botok tokenizes Tibetan text into words.

### Basic usage

#### Getting started
Requires to have Python3 installed.

    pip3 install botok

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
