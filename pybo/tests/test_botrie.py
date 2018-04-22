from pybo.BoTrie import Trie, PyBoTrie
from pybo.BoSylUtils import BoSyl

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
    assert bt.has_word('བཀྲ་ཤིས་') == {'data': 'NOUN---', 'exists': True}
    assert bt.has_word('བཀྲ་ཤིསའི་') == {'exists': False}
    assert bt.has_word('གྲུབ་མཐའ་') == {'data': 'NOUN---', 'exists': True}
    assert bt.has_word('གྲུབ་མཐར་') == {'data': 'NOUN-la-1-aa', 'exists': True}
    assert bt.has_word('གྲུབ་མཐས་') == {'data': 'NOUN-gis-1-aa', 'exists': True}
    assert bt.has_word('གྲུབ་མཐའི་') == {'data': 'NOUN-gi-2-aa', 'exists': True}
    assert bt.has_word('གྲུབ་མཐའམ་') == {'data': 'NOUN-am-2-aa', 'exists': True}
    assert bt.has_word('གྲུབ་མཐའང་') == {'data': 'NOUN-ang-2-aa', 'exists': True}
    assert bt.has_word('གྲུབ་མཐའོ་') == {'data': 'NOUN-o-2-aa', 'exists': True}
    assert bt.has_word('གྲུབ་མཐའིའོ་') == {'data': 'NOUN-gi+o-4-aa', 'exists': True}


def test_trie():
    trie = Trie()
    words = 'hello goo good goodbye help gerald gold tea ted team to too tom stan standard money'
    for w in words.split():
        trie.add(w)
    assert trie.has_word('goodbye') == {'data': None, 'exists': True}


def test_building_trie():
    bt = PyBoTrie(BoSyl(), 'test')
    assert bt.has_word('བཀྲ་ཤིས་') == {'data': 'NOUN---', 'exists': True}
    assert bt.has_word('ཤིས་') == {'data': 'NOUN---', 'exists': True}


def test_deactivate_trie_entries():
    trie = PyBoTrie(BoSyl(), 'empty')
    word = 'བཀྲ་ཤིས་'
    trie.add(word)
    assert trie.has_word(word)
    trie.remove_word(word)
    assert trie.has_word(word) == {'exists': False}
