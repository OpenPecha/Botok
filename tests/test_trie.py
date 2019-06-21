from pathlib import Path

from pybo import BasicTrie, Trie, Config
from pybo import BoSyl

config = Config()


def test_createtrie():
    profile = 'empty'
    main, custom = config.get_tok_data_paths(profile)
    bt = Trie(BoSyl, profile, main, custom)

    # the trie works as expected. but the add() method should never be used directly:
    # it does not inflect entries, so the tokenizer won't work as expected.
    bt.add('གྲུབ་མཐའ་', {'POS': 'NOUN'})
    assert bt.has_word('གྲུབ་མཐའི་') == {'exists': False, 'data': {'_': {}}}

    # use inflect_n_modify_trie() instead, to add entries
    bt.inflect_n_modify_trie('གྲུབ་མཐའ་')

    assert bt.has_word('གྲུབ་མཐའི་') == {'exists': True,
                                    'data': {'_': {},
                                             'affixation': {'len': 2, 'type': 'gi', 'aa': True}}}

    bt.inflect_n_modify_trie('ཀ་ར་', skrt=True)
    assert bt.has_word('ཀ་རར་') == {'exists': True,
                                  'data': {'_': {},
                                           'affixation': {'len': 1, 'type': 'la', 'aa': False},
                                           'skrt': True}}  # arrives here because skrt was True

    bt.inflect_n_add_data('གྲུབ་མཐའ་\t532', 'freq')  # 'freq' is hard-coded in Trie, just as 'lemma' and 'pos' are
    assert bt.has_word('གྲུབ་མཐའི་') == {'exists': True,
                                    'data': {'_': {},
                                             'affixation': {'len': 2, 'type': 'gi', 'aa': True},
                                             'freq': 532}}  # freq is an int

    # just like add() was not meant to be used directly, deactivate() is not
    bt.deactivate('ཀ་ར་')
    assert bt.has_word('ཀ་རར་')['exists'] is True
