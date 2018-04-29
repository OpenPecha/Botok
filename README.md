<img src=https://raw.githubusercontent.com/mikkokotila/pybo/master/pybo_logo.png width=200>

## Overview

pybo is a word tokenizer for the Tibetan language entirely written in Python. pybo takes in chuncks of text, and returns lists of words. It provides an easy-to-use, high-performance tokenization pipeline that can be adapted either as a stand-alone solution or compliment.

## Getting Started 

    pip install pybo
    
Or if you for some reason want to install from the latest Master branch:

    pip install git+https://github.com/Esukhia/pybo.git

## Use 

To initiate the tokenizer together with part-of-speech capability: 

    # initialize the tokenizer
    pybo = bo.BoTokenizer('POS')
    
    # read in some Tibetan text
    input_str = '༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །'
    
    # run the tokenizer
    tokens = tok.tokenize(input_str)
    
Now in 'tokens' you have an iterable where each token consist of several meta-data:

    # access the first token in the iterable
    tokens[0]

This will yield:

    content: "༄༅། "
    char types: |punct|punct|punct|space|
    type: punct
    start in input: 0
    length: 4
    syl chars in content: None
    tag: punct
    POS: punct    
    
In case you want to access all words in a list: 

    # iterate through the tokens object to get all the words in a list
    [t.content for t in tokens]
