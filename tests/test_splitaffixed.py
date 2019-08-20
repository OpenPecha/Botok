# coding: utf8
from pybo import *


def test_split_token():
    wt = WordTokenizer("empty")
    wt.tok.trie.rebuild_trie()
    wt.tok.trie.inflect_n_modify_trie("བདེ་བ་")
    wt.tok.trie.inflect_n_add_data("བདེ་བ་\t\tNOUN")
    wt.tok.trie.inflect_n_modify_trie("གཏན་")
    wt.tok.trie.inflect_n_add_data("གཏན་\t\tNOUN")
    wt.tok.trie.inflect_n_modify_trie("གྱི་")
    wt.tok.trie.inflect_n_add_data("གྱི་\tགི\tPART")
    tokens = wt.tokenize("གཏན་གྱི་བདེ་བའི་རྒྱུ།", split_affixes=False)
    assert len(tokens) == 5
    assert tokens[2].text == "བདེ་བའི་"
    tokens = wt.tokenize("གཏན་གྱི་བདེ་བའི་རྒྱུ།")
    assert len(tokens) == 6
    assert tokens[2].text == "བདེ་བ"
    assert tokens[3].text == "འི་"
