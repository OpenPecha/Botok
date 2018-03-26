# pybo

Pybo is a python tokenizer for Tibetan built as a tokenizer plugin for spaCy and the Tibetan editor. It takes in a string of raw tibetan text and spits out a list of Token objects.

## Normalisation

Acheived by `PyBoTextChunks` from BoStringUtils (see the docstrings for more information)

## Word Segmentation

Acheived by `BoTokenizer`. See [here](https://github.com/Esukhia/pybo/blob/master/pybo/tests/test_tokenizer.py)
for usage examples (and other test files for how the different components of pybo are used within the Tokenizer)

## Pattern Matchers

Pattern matchers or simply "Matchers" are used to match patterns expressed in a syntax combining regex, token and token attributes.

As for now, [a basic matcher](https://github.com/Esukhia/pybo/blob/develop/pybo/BoTokenUtils.py#L39) has been implemented.
It should be replaced by the cql parser in `thirt-party/cql.py`.

Todo:
    - implement a splitter of Token objects (an unfinished attempt is [here](https://github.com/Esukhia/pybo/blob/master/pybo/BoTokenUtils.py#L1))
    - implement a merger of Token objects
    - implement a function/class that attempts to match the query at every index in the list of Tokens,
        if it matches, replaces the content of a given attribute.
        The relative index of the attribute should be passed as argument and the new content also.

Once that is done, BoTokenizer will be used to produce Token objects, and the tokens containing affixed particles will be split. At that moment, pytib will be completely replaced.

## Licence

The code is Copyright 2018 Esukhia, and is provided under [Apache Licence 2.0](LICENCE)
