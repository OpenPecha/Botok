from BoTrie import Trie, PyBoTrie

# uses py.test


def test_pybotrie():
    bt = PyBoTrie('empty')
    bt.add('གྲུབ་མཐའ་', 'pos-tag')
    assert bt.has_word('གྲུབ་མཐའི་') == {'exists': False}
    assert bt.has_word('གྲུབ་མཐའ་') == {'exists': True, 'data': 'pos-tag'}


def test_affixed_entries():
    bt = PyBoTrie('empty')
    bt.inflect_n_add('གྲུབ་མཐའ་', 'NOUN')  # adds all inflected forms
    bt.inflect_n_add('བཀྲ་ཤིས་', 'NOUN')  # only adds one entry in the trie
    assert bt.has_word('བཀྲ་ཤིས་') == {'data': 'NOUN___', 'exists': True}
    assert bt.has_word('བཀྲ་ཤིསའི་') == {'exists': False}
    assert bt.has_word('གྲུབ་མཐའ་') == {'data': 'NOUN___', 'exists': True}
    assert bt.has_word('གྲུབ་མཐར་') == {'data': 'NOUN_la_1_aa', 'exists': True}
    assert bt.has_word('གྲུབ་མཐས་') == {'data': 'NOUN_gis_1_aa', 'exists': True}
    assert bt.has_word('གྲུབ་མཐའི་') == {'data': 'NOUN_gi_2_aa', 'exists': True}
    assert bt.has_word('གྲུབ་མཐའམ་') == {'data': 'NOUN_am_2_aa', 'exists': True}
    assert bt.has_word('གྲུབ་མཐའང་') == {'data': 'NOUN_ang_2_aa', 'exists': True}
    assert bt.has_word('གྲུབ་མཐའོ་') == {'data': 'NOUN_o_2_aa', 'exists': True}
    assert bt.has_word('གྲུབ་མཐའིའོ་') == {'data': 'NOUN_gi+o_4_aa', 'exists': True}


def test_trie():
    trie = Trie()
    words = 'hello goo good goodbye help gerald gold tea ted team to too tom stan standard money'
    for w in words.split():
        trie.add(w)
    assert trie.has_word('goodbye') == {'data': None, 'exists': True}


def test_building_trie():
    bt = PyBoTrie('test')
    assert bt.has_word('བཀྲ་ཤིས་') == {'data': 'NOUN___', 'exists': True}
    assert bt.has_word('ཤིས་') == {'data': 'NOUN___', 'exists': True}