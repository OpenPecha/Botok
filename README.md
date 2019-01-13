<img src=https://raw.githubusercontent.com/mikkokotila/pybo/master/pybo_logo.png width=200>

[![Build Status](https://travis-ci.org/Esukhia/pybo.svg?branch=master)](https://travis-ci.org/Esukhia/pybo)  [![Coverage Status](https://coveralls.io/repos/github/Esukhia/pybo/badge.svg?branch=master)](https://coveralls.io/github/Esukhia/pybo?branch=master)

## Overview

pybo is a word tokenizer for the Tibetan language entirely written in Python. pybo takes in chuncks of text, and returns lists of words. It provides an easy-to-use, high-performance tokenization pipeline that can be adapted either as a stand-alone solution or compliment.

## Getting Started 

    pip install pybo
    
Or if you for some reason want to install from the latest Master branch:

    pip install git+https://github.com/Esukhia/pybo.git

## Use 

#### To initiate the tokenizer together with part-of-speech capability: 

    # initialize the tokenizer
    tok = bo.BoTokenizer('POS')
    
    # read in some Tibetan text
    input_str = '༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །'
    
    # run the tokenizer
    tokens = tok.tokenize(input_str)
    
#### Now in 'tokens' you have an iterable where each token consist of several meta-data:

    # access the first token in the iterable
    tokens[0]

This will yield:

    content: "༄༅། "
    char_types: |punct|punct|punct|space|
    type: punct
    start: 0
    len: 4
    syls: None
    tag: punct
    pos: punct
    skr: "False"
    freq: 0
    
notes:
 - `start` is the starting index of the current token in the input string.
 - `syls` is a list of cleaned syllables, each syllable being represented as a list of indices.
Each index leads to a constituting character within the input string. 

#### In case you want to access all words in a list: 

    # iterate through the tokens object to get all the words in a list
    [t.content for t in tokens]

#### Or just get all the nouns that were used in the text

    # extract nouns from the tokens
    [t.content for t in tokens if t.tag == 'NOUNᛃᛃᛃ']
    
These examples highlight the basic principle of accessing attributes within each token object. 

## Acknowledgement

**pybo** is an open source library for Tibetan NLP.

We are always open to cooperation in introducing new features, tool integrations and testing solutions.

Many thanks to companies and organizations who supported the development of pybo, especially:

* [Khyentse Foundation](https://khyentsefoundation.org) for contributing USD22,000 to kickstart the project 
* The [Barom/Esukhia canon project](http://www.barom.org) for sponsoring training data curation
* [BDRC](https://tbrc.org) for contributing 2 staff for 6 months for data curation

## Maintainance

Build the source dist:

```
rm -rf dist/
python3 setup.py clean sdist
```

and upload on twine (versio >= `1.11.0`) with:

```
twine upload dist/*
```

## License

The Python code is Copyright (C) 2019 Esukhia, provided under [Apache 2](LICENSE). 

author: [Drupchen](https://github.com/drupchen)

contributors:
 * [Élie Roux](https://github.com/eroux)
 * [Thubten Rinzin](https://github.com/thubtenrigzin)
 * [Ngawang Trinley](https://github.com/ngawangtrinley)
 * [Mikko Kotila](https://github.com/mikkokotila)
 * [Tenzin](https://github.com/10zinten)
