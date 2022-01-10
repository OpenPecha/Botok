Getting Started with Botok
==========================

Installation
------------

.. Caution::

    Pybo only support python3

Install pre-built pybo with pip:

.. code-block::

    $ pip install botok

Install from the latest Master branch of pybo with pip:

.. code-block::

    $ pip install git+https://github.com/Esukhia/botok.git

Install for developer, build pybo from source:

.. code-block::

    $ git clone https://github.com/Esukhia/botok.git
    $ cd botok
    $ python3 -m venv .env
    $ activate .env/bin/activate
    $ python setup.py clean sdist

Usage
-----

Here is the simple usage of botok to tokenize the sentence

Import the botok tokenizer called WordTokenizer:

.. code-block::

    >>> from pybo import WordTokenizer
    >>>
    >>> tokenizer = WordTokenizer()
    Building Trie... (12 s.)

Tokenize the given text:

.. code-block::

    >>> input_str = '༆ ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་༡༢༣ཀཀ།མཐའི་རྒྱ་མཚོར་གནས་པའི་ཉས་ཆུ་འཐུང་།། །།མཁའ།'
    >>> tokens = tokenizer.tokenize(input_str)
    >>> print(f'The output is a {type(tokens)}')
    The output is a <class 'list'>
    >>> print(f'The constituting elements are {type(tokens[0])}')
    The constituting elements are <class 'pybo.token.Token'>

Now in ‘tokens’ you have an iterable where each token consist of several meta-data in attributes of Token Object:

.. code-block::

    >>> tokens[0]
    content: "༆ "
    char_types: |punct|space|
    type: punct
    start: 0
    len: 2
    tag: punct
    pos: punc
    
    
Custom dialect pack:

In order to use custom dialect pack:

1. You need to prepare your dialect pack in same folder structure like [general dialect pack](https://github.com/Esukhia/botok-data/tree/master/dialect_packs/general)
2. Then you need to instaintiate a config object where you will pass dialect name and path
3. You can instaintiate your tokenizer object using that config object
4. Your tokenizer will be using your custom dialect pack and it will be using trie pickled file in future to build the custom trie.

.. code-block::

    from botok import WordTokenizer
    from botok.config import Config
    from pathlib import Path

    def get_tokens(wt, text):
        tokens = wt.tokenize(text, split_affixes=False)
        return tokens

    if __name__ == "__main__":
        config = Config(dialect_name="custom", base_path= Path.home())
        wt = WordTokenizer(config=config)
        text = "བཀྲ་ཤིས་བདེ་ལེགས་ཞུས་རྒྱུ་ཡིན་ སེམས་པ་སྐྱིད་པོ་འདུག།"
        tokens = get_tokens(wt, text)
        for token in tokens:
            print(token)
