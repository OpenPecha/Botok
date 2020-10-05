Custom Dialect Pack
===================

Why Custom Dialect Pack
-----------------------

- For domain specific tokenization
- Improving tokenization accuracy


Example
-------

To use a custom dialect pack for tokenization, all we have to do is to create a `botok.Config` object with path to the custom dialect pack and use this config for creating word tokenizer.

First, create config for the custom dialect pack.

.. code::

    >>> from botok import Config
    >>> config = Config.from_path('custom/dialect/pack/path')

Then, create word tokenizer with that same config.

.. code::

    >>> from botok import WordTokenizer
    >>> wt = WordTokenizer(config=config)
    >>> wt.tokenize("མཐའི་བཀྲ་ཤིས། ཀཀ abc མཐའི་རྒྱ་མཚོ་")
