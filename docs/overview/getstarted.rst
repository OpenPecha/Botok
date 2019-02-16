Getting Started with Pybo
+++++++++++++++++++++++++

Installation
========================

.. caution::

   Pybo only support ``python3``

* Install pre-built pybo with pip::

  $ pip install pybo


* Install from the latest Master branch of pybo with pip::

  $ pip install git+https://github.com/Esukhia/pybo.git


* Install for developer, build pybo from source::

  $ virtualenv env -p python3
  $ activate env/bin/activate
  $ git clone https://github.com/Esukhia/pybo.git
  $ cd pybo
  $ python setup.py clean sdist


Usage
========================

Here is the simple usage of pybo tokenizer to tokenize the sentence with POS
(part-of speech) annotation for each token.

Import the Pybo tokenizer called ``BoTokenizer``::

   >>> from pybo import BoTokenizer


Instanciate the tokenizer with the ‘POS’ profile::

   >>> tokenizer = BoTokenizer('POS')
   Building Trie... (12 s.)


Tokenize the given random text in Tibetan language::

   >>> input_str = '༆ ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་༡༢༣ཀཀ།མཐའི་རྒྱ་མཚོར་གནས་པའི་ཉས་ཆུ་འཐུང་།། །།མཁའ།'
   >>> tokens = tokenizer.tokenize(input_str)
   >>> print(f'The output is a {type(tokens)}')
   The output is a <class 'list'>
   >>> print(f'The constituting elements are {type(tokens[0])}')
   The constituting elements are <class 'pybo.token.Token'>


Now in ‘tokens’ you have an iterable where each token consist of several
meta-data in attributes of Token Object::

   >>> tokens[0]
   content: "༆ "
   char_types: |punct|space|
   type: punct
   start: 0
   len: 2
   tag: punct
   pos: punct


.. note::
    * ``start`` is the starting index of the current token in the input string.
    * ``syls`` is a list of cleaned syllables, each syllable being represented as
        a list of indices. Each index leads to a constituting character within
        the input string.


Print content, type and pos information of each token::

   >>> for token in tokens:
   ...     print(f'{token.content}\t{token.type}\t{token.pos}')

Output:

======== ======= ========
CONTENT  TYPE    POS
======== ======= ========
༆        punct   punct
ཤི་       syl     VERB
བཀྲ་ཤིས་   syl     NOUN
tr       non-bo  non-bo
བདེ་་ལེ གས syl     NOUN
།        punct   punct
བཀྲ་ཤིས་   syl     NOUN
བདེ་ལེགས་  syl     NOUN
༡༢༣      num     num
ཀཀ       syl     non-word
།        punct   punct
མཐ       syl     NOUN
འི་       syl     PART
རྒྱ་མཚོ     syl     NOUN
ར་       syl     PART
གནས་པ    syl     VERB
འི་       syl     PART
ཉ        syl     NOUN
ས་       syl     PART
ཆུ་       syl     NOUN
འཐུང་     syl     oov
།། །།    punct   punct
མཁའ      syl     NOUN
།        punct   punct
======== ======= ========


.. note::
   * TYPE:
      * ``syl`` : contains valid Tibetan syllables
      * ``num`` : Tibetan numerals
      * ``punct`` : Tibetan punctuation
      * ``non-bo``: non-Tibetan content
   * POS:
      * ``NOUN`` : Tibetan noun
      * ``VERB`` : Tibetan verb
      * ``PART`` : casual particle (affixed or not)
      * ``oov`` : Tibetan word for which no POS was found
      * ``non-word``: A sequence of Tibetan letters that does not appear in our
        list of words
      * ``punct`` : Tibetan punctuation
      * ``num`` : Tibetan numerals
      * ``non-bo`` : non-Tibetan characters (spaces have a special treatment)
