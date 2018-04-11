from pybo import *


def test_token_to_string():
    tok = Tokenizer(PyBoTrie(BoSyl(), 'empty'))
    tok.trie.add('བཀྲ་ཤིས་', data='NOUN')
    tokens = tok.tokenize(PyBoTextChunks('བཀྲ་ཤིས།'))
    expected = """content: "བཀྲ་ཤིས"
char types: |cons|cons|sub-cons|tsek|cons|vow|cons|
type: syl
start in input: 0
length: 7
syl chars in content(བཀྲ ཤིས): [[0, 1, 2], [4, 5, 6]]
tag: NOUN
POS: NOUN"""
    assert tokens[0].__repr__() == expected
    assert tokens[1].content == '།'
    assert tokens[1].chunk_markers[tokens[1].chunk_type] == 'punct'
    assert tokens[1].tag == 'punct'


def test_non_max2():
    tok = Tokenizer(PyBoTrie(BoSyl(), 'empty'))
    tok.trie.add('བཀྲ་ཤིས་', data='NOUN')
    tok.trie.add('བཀྲ་ཤིས་བདེ་ལེགས།', data='EXCL')
    tokens = tok.tokenize(PyBoTextChunks('བཀྲ་ཤིས་བདེ་བཀྲ་'))
    assert tokens[0].content == 'བཀྲ་ཤིས་'
    assert tokens[0].tag == 'NOUN'
    assert tokens[1].content == 'བདེ་'
    assert tokens[1].tag == 'non-word'
    assert tokens[2].content == 'བཀྲ་'
    assert tokens[2].tag == 'non-word'


def test_non_max_end_of_string():
    tok = Tokenizer(PyBoTrie(BoSyl(), 'empty'))
    tok.trie.add('བཀྲ་ཤིས་')
    tok.trie.add('བཀྲ་ཤིས་བདེ་ལེགས།')
    tokens = tok.tokenize(PyBoTextChunks('བཀྲ་ཤིས་བདེ་'))
    assert tokens[0].content == 'བཀྲ་ཤིས་'
    assert tokens[1].content == 'བདེ་'


def test_split_token():
    trie = PyBoTrie(BoSyl(), 'empty')
    trie.inflect_n_add('བདེ་བ་', 'NOUN')
    trie.add('གཏན་', 'NOUN')
    trie.add('གྱི་', data='PART')
    tok = Tokenizer(trie)
    tokens = tok.tokenize(PyBoTextChunks('གཏན་གྱི་བདེ་བའི་རྒྱུ།'))
    assert len(tokens) == 5
    assert tokens[2].content == 'བདེ་བའི་'
    SplitAffixed().split(tokens)
    assert len(tokens) == 6
    assert tokens[2].content == 'བདེ་བ'
    assert tokens[3].content == 'འི་'
