from pybo import BasicTrie, PyBoTrie
from pybo import BoSyl

# uses py.test


def test_pybotrie():
    bt = PyBoTrie(BoSyl(), 'empty')
    bt.add('གྲུབ་མཐའ་', 'pos-tag')
    assert bt.has_word('གྲུབ་མཐའི་') == {'exists': False}
    assert bt.has_word('གྲུབ་མཐའ་') == {'exists': True, 'data': 'pos-tag'}


def test_affixed_entries():
    bt = PyBoTrie(BoSyl(), 'empty')
    bt.inflect_n_add('གྲུབ་མཐའ་', 'NOUN')  # adds all inflected forms
    bt.inflect_n_add('བཀྲ་ཤིས་', 'NOUN')  # only adds one entry in the trie
    assert bt.has_word('བཀྲ་ཤིས་') == {'data': 'NOUNᛃᛃᛃ', 'exists': True}
    assert bt.has_word('བཀྲ་ཤིསའི་') == {'exists': False}
    assert bt.has_word('གྲུབ་མཐའ་') == {'data': 'NOUNᛃᛃᛃ', 'exists': True}
    assert bt.has_word('གྲུབ་མཐར་') == {'data': 'NOUNᛃlaᛃ1ᛃaa', 'exists': True}
    assert bt.has_word('གྲུབ་མཐས་') == {'data': 'NOUNᛃgisᛃ1ᛃaa', 'exists': True}
    assert bt.has_word('གྲུབ་མཐའི་') == {'data': 'NOUNᛃgiᛃ2ᛃaa', 'exists': True}
    assert bt.has_word('གྲུབ་མཐའམ་') == {'data': 'NOUNᛃamᛃ2ᛃaa', 'exists': True}
    assert bt.has_word('གྲུབ་མཐའང་') == {'data': 'NOUNᛃangᛃ2ᛃaa', 'exists': True}
    assert bt.has_word('གྲུབ་མཐའོ་') == {'data': 'NOUNᛃoᛃ2ᛃaa', 'exists': True}
    assert bt.has_word('གྲུབ་མཐའིའོ་') == {'data': 'NOUNᛃgi+oᛃ4ᛃaa', 'exists': True}


def test_trie():
    trie = BasicTrie()
    words = 'hello goo good goodbye help gerald gold tea ted team to too tom stan standard money'
    for w in words.split():
        trie.add(w)
    assert trie.has_word('goodbye') == {'data': None, 'exists': True}


def test_building_trie():
    bt = PyBoTrie(BoSyl(), 'test')
    assert bt.has_word('བཀྲ་ཤིས་') == {'data': 'NOUNᛃᛃᛃ', 'exists': True}
    assert bt.has_word('ཤིས་') == {'data': 'NOUNᛃᛃᛃ', 'exists': True}


def test_deactivate_trie_entries():
    trie = PyBoTrie(BoSyl(), 'empty')
    word = 'བཀྲ་ཤིས་'
    trie.add(word)
    assert trie.has_word(word)
    trie.remove_word(word)
    assert trie.has_word(word) == {'exists': False}
