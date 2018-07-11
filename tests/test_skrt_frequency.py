from pybo import *

tok = BoTokenizer('POS')
tok.tok.trie.rebuild_trie()


def test_frequency():
    input_str = "བཀྲ་ཤིས་བདེ་ལེགས་"
    tokens = tok.tokenize(input_str)
    assert tokens[0].freq == 17204
    assert tokens[1].freq == 3918

def test_skrt():
    input_str = "བུདྡྷཿ"
    tokens = tok.tokenize(input_str)
    assert tokens[0].skrt == True