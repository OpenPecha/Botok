Getting Started with Botok
==========================

Installation
------------

.. Caution::

    Botok only supports Python 3.6 or higher

Install pre-built botok with pip:

.. code-block::

    $ pip install botok

Install from the latest Master branch of botok with pip:

.. code-block::

    $ pip install git+https://github.com/OpenPecha/botok.git

Install for developers, build botok from source:

.. code-block::

    $ git clone https://github.com/OpenPecha/botok.git
    $ cd botok
    $ python -m venv .env
    $ source .env/bin/activate  # On Windows: .env\Scripts\activate
    $ pip install -e .

Usage
-----

Here is the simple usage of botok to tokenize Tibetan text:

Import the botok tokenizer called WordTokenizer:

.. code-block::

    >>> from botok import WordTokenizer
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
    The constituting elements are <class 'botok.token.Token'>

Now in 'tokens' you have an iterable where each token consists of several meta-data in attributes of Token Object:

.. code-block::

    >>> tokens[0]
    content: "༆ "
    char_types: |punct|space|
    type: punct
    start: 0
    len: 2
    tag: punct
    pos: punc
    
    
Custom dialect pack
------------------

In order to use a custom dialect pack:

1. Prepare your dialect pack in the same folder structure as the `general dialect pack <https://github.com/OpenPecha/botok-data/tree/master/dialect_packs/general>`_
2. Instantiate a config object where you pass the dialect name and path
3. Instantiate your tokenizer object using that config object
4. Your tokenizer will use your custom dialect pack and will use a trie pickled file in the future to build the custom trie

.. code-block::

    from botok import WordTokenizer
    from botok.config import Config
    from pathlib import Path

    def get_tokens(wt, text):
        tokens = wt.tokenize(text, split_affixes=False)
        return tokens

    if __name__ == "__main__":
        config = Config(dialect_name="custom", base_path=Path.home())
        wt = WordTokenizer(config=config)
        text = "བཀྲ་ཤིས་བདེ་ལེགས་ཞུས་རྒྱུ་ཡིན་ སེམས་པ་སྐྱིད་པོ་འདུག།"
        tokens = get_tokens(wt, text)
        for token in tokens:
            print(token)

Advanced Usage
-------------

For more advanced usage, including POS tagging and lemmatization, see the :doc:`advanced guides <architecture>`.
