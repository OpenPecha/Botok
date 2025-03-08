.. botok documentation master file, created by
   sphinx-quickstart on Thu Jul 30 12:30:47 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Botok
===================================================================================================
State-of-the-art tokenizers for Tibetan language.

This is the documentation of our repository `botok <https://github.com/OpenPecha/botok>`_.

Features
--------------------------------

- Support various dialects
- Word segmentation with support for affixed particles
- Multiple tokenization modes (chunks, spaces, words)
- Rich token attributes (lemma, POS, clean form)
- File and string input processing
- Word frequency counting
- Handles complex cases like double tseks and spaces within words

Contents
----------------------------------

.. toctree::
    :maxdepth: 2
    :caption: Overview

    getting-started
    acknowledgement

.. toctree::
    :maxdepth: 2
    :caption: Advanced guides

    architecture
    custom-dialect-pack

.. toctree::
    :maxdepth: 2
    :caption: Package Reference

    main_classes/configuration
