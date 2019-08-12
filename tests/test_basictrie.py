# coding: utf8
from pybo import BasicTrie


def test_trie():
    trie = BasicTrie()

    # populate the basic trie
    words = 'hello goo good goodbye help gerald gold tea ted team to too tom stan standard money'
    for w in words.split():
        trie.add(w)

    # test word existence. has_word() is not used in pybo. it is only there for testing purposes
    assert trie.has_word('goodbye') == {'data': {'_': {}}, 'exists': True}

    # add content to data
    trie.add_data('goodbye', {'pos': 'NOUN'})
    assert trie.has_word('goodbye') == {'exists': True, 'data': {'_': {}, 'meanings': [{'pos': 'NOUN'}]}}

    # adding an empty dict to show it does not replace existing content but updates it
    trie.add_data('goodbye', {})
    assert trie.has_word('goodbye') == {'exists': True, 'data': {'_': {}, 'meanings': [{'pos': 'NOUN'}]}}

    # by default, overwrites existing dict values
    trie.add_data('goodbye', {'pos': 'VERB', 'lemma': 'goodbye'})
    assert trie.has_word('goodbye') == {'exists': True, 'data': {'_': {}, 'meanings': [{'pos': 'NOUN'}, {'pos': 'VERB', 'lemma': 'goodbye'}]}}

    # deactivates an entry, only modifying the Node.leaf value (bool) instead of removing it from the trie.
    trie.deactivate('goodbye')
    assert trie.has_word('goodbye') == {'exists': False, 'data': {'_': {}, 'meanings': [{'pos': 'NOUN'}, {'pos': 'VERB', 'lemma': 'goodbye'}]}}

    # reactivates the entry
    trie.deactivate('goodbye', rev=True)
    assert trie.has_word('goodbye') == {'exists': True, 'data': {'_': {}, 'meanings': [{'pos': 'NOUN'}, {'pos': 'VERB', 'lemma': 'goodbye'}]}}

    # walk() is used to externalize the walking of the trie
    current_node = None  # setting an empty variable for the current node
    for char in 'goodbye':
        current_node = trie.walk(char, current_node)

    assert current_node.label == 'e'  # last char of the word
    assert current_node.leaf is True  # we reached the end of a word
    assert current_node.data == {'_': {}, 'meanings': [{'pos': 'NOUN'}, {'pos': 'VERB', 'lemma': 'goodbye'}]}
