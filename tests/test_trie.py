from pathlib import Path

from pybo import BasicTrie, Trie, Config
from pybo import BoSyl

config = Config()


def test_createtrie():
    profile = 'empty'
    main, custom = config.get_tok_data_paths(profile)
    bt = Trie(BoSyl, profile, main, custom)

    # the lexica_bo works as expected. but the add() method should never be used directly:
    # it does not inflect entries, so the tokenizer won't work as expected.
    bt.add('གྲུབ་མཐའ་', {'POS': 'NOUN'})
    assert bt.has_word('གྲུབ་མཐའི་') == {'exists': False, 'data': {'_': {}}}
    assert bt.has_word('གྲུབ་མཐའ་') == {'exists': True, 'data': {'_': {}, 'POS': 'NOUN'}}


def test_build_trie():
    profile = 'POS'
    main, custom = config.get_tok_data_paths(profile)
    bt = Trie(BoSyl, profile, main, custom)
    bt.rebuild_trie()
    pass


def test_affixed_entries():
    bt = Trie(BoSyl, config, 'empty')
    bt.inflect_n_add('གྲུབ་མཐའ་', 'NOUN')  # adds all inflected forms
    bt.inflect_n_add('བཀྲ་ཤིས་', 'NOUN')  # only adds one entry in the lexica_bo
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





def test_building_trie():
    bt = Trie(BoSyl, config, 'pytib')
    bt.rebuild_trie()
    assert bt.has_word('བཀྲ་ཤིས་') == {'data': 'NOUNᛃᛃᛃ', 'exists': True}
    assert bt.has_word('ཤིས་') == {'data': 'VERBᛃᛃᛃ', 'exists': True}


def test_deactivate_trie_entries():
    trie = Trie(BoSyl, config, 'empty')
    trie.rebuild_trie()
    word = 'བཀྲ་ཤིས་'
    trie.add(word)
    assert trie.has_word(word)
    trie.deactivate(word)
    assert trie.has_word(word) == {'exists': False}

    trie.rebuild_trie()
    words = ['བཀྲ་ཤིས་', 'བདེ་ལེགས་']
    trie.add(words[0])
    trie.add(words[1])
    trie.deactivate_wordlist(Path(__file__).parent / 'resources/remove_vocabs/test.txt')
    assert trie.has_word(words[0]) == {'exists': False}
    assert trie.has_word(words[1]) == {'exists': False}
