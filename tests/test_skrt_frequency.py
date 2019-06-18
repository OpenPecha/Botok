from pybo import *

tok = BoTokenizer('GMD')
tok.tok.trie.rebuild_trie()


def test_frequency():
    input_str = "བཀྲ་ཤིས་བདེ་ལེགས་"
    tokens = tok.tokenize(input_str)
    assert 366 == tokens[0].freq  # TODO: should be two words, but the wordlists contain it as a whole


def test_skrt():
    input_str = "བུདྡྷཿ"
    tokens = tok.tokenize(input_str)
    assert tokens[0].skrt  # where skrt is a Bool
