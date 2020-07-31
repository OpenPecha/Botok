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