# coding: utf8
from pybo import BasicTrie


def test_trie():
    trie = BasicTrie()

    # populate the basic lexica_bo
    words = 'hello goo good goodbye help gerald gold tea ted team to too tom stan standard money'
    for w in words.split():
        trie.add(w)

    # test word existence. has_word() is not used in pybo. it is only there for testing purposes
    assert trie.has_word('goodbye') == {'data': {'_': {}}, 'exists': True}

    # add content to data
    trie.add_data('goodbye', {'POS': 'NOUN'})
    assert trie.has_word('goodbye') == {'data': {'_': {}, 'POS': 'NOUN'}, 'exists': True}

    # only adds key/value pairs to the existing dict. does not replace the data variable
    trie.add_data('goodbye', {}, overwrite=True)
    assert trie.has_word('goodbye') == {'data': {'_': {}, 'POS': 'NOUN'}, 'exists': True}

    # by default, overwrites existing dict values
    trie.add_data('goodbye', {'POS': 'VERB', 'lang': 'en'})
    assert trie.has_word('goodbye') == {'data': {'_': {}, 'POS': 'VERB', 'lang': 'en'}, 'exists': True}

    # can be set to not overwrite
    trie.add_data('goodbye', {'POS': 'NOUN'}, overwrite=False)
    assert trie.has_word('goodbye') == {'data': {'_': {}, 'POS': 'VERB', 'lang': 'en'}, 'exists': True}

    # deactivates an entry in the lexica_bo, only modifying the Node.leaf value (bool) to be efficient
    trie.deactivate('goodbye')
    assert trie.has_word('goodbye') == {'data': {'_': {}, 'POS': 'VERB', 'lang': 'en'}, 'exists': False}

    # reactivates the entry
    trie.deactivate('goodbye', rev=True)
    assert trie.has_word('goodbye') == {'data': {'_': {}, 'POS': 'VERB', 'lang': 'en'}, 'exists': True}

    # walk() is used to externalize the walking of the lexica_bo
    node = trie.head  # getting to the root of the lexica_bo
    for char in 'goodbye':
        if char in node.children:
            node = node[char]  # one step down the lexica_bo

    assert node.label == 'e'  # last char of the word
    assert node.leaf == True  # we reached the end of a word
    assert node.data == {'_': {}, 'POS': 'VERB', 'lang': 'en'}
