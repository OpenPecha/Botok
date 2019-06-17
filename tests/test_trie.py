from pathlib import Path

from pybo import BasicTrie, Trie, Config
from pybo import BoSyl

# uses py.test


def test_pybotrie():
    bt = Trie(BoSyl, 'empty', config=Config("pybo.yaml"))
    bt.rebuild_trie()
    bt.add('གྲུབ་མཐའ་', 'pos-tag')
    assert bt.has_word('གྲུབ་མཐའི་') == {'exists': False}
    assert bt.has_word('གྲུབ་མཐའ་') == {'exists': True, 'data': 'pos-tag'}


def test_affixed_entries():
    bt = Trie(BoSyl, 'empty', config=Config("pybo.yaml"))
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
    bt = Trie(BoSyl, 'pytib', config=Config("pybo.yaml"))
    bt.rebuild_trie()
    assert bt.has_word('བཀྲ་ཤིས་') == {'data': 'NOUNᛃᛃᛃ', 'exists': True}
    assert bt.has_word('ཤིས་') == {'data': 'VERBᛃᛃᛃ', 'exists': True}


def test_deactivate_trie_entries():
    trie = Trie(BoSyl, 'empty', config=Config("pybo.yaml"))
    trie.rebuild_trie()
    word = 'བཀྲ་ཤིས་'
    trie.add(word)
    assert trie.has_word(word)
    trie.deactivate_word(word)
    assert trie.has_word(word) == {'exists': False}

    trie.rebuild_trie()
    words = ['བཀྲ་ཤིས་', 'བདེ་ལེགས་']
    trie.add(words[0])
    trie.add(words[1])
    trie.deactivate_wordlist(Path(__file__).parent / 'resources/remove_vocabs/test.txt')
    assert trie.has_word(words[0]) == {'exists': False}
    assert trie.has_word(words[1]) == {'exists': False}
