from pybo import *


def test_token_to_string():
    tok = Tokenizer(PyBoTrie(BoSyl(), 'empty', config=Config("pybo.yaml")))
    tok.trie.rebuild_trie()
    tok.trie.add('བཀྲ་ཤིས་', data='NOUN', freq=17500)
    tokens = tok.tokenize(PyBoTextChunks('བཀྲ་ཤིས།'), phono=True)
    expected = """content: "བཀྲ་ཤིས"
cleaned_content: "བཀྲ་ཤིས་"
unaffixed_word: "བཀྲ་ཤིས་"
char_types: |cons|cons|sub-cons|tsek|cons|vow|cons|
type: syl
start: 0
len: 7
syls (བཀྲ ཤིས): [[0, 1, 2], [4, 5, 6]]
tag: NOUN
pos: NOUN
freq: 17500
"""
    assert tokens[0].__repr__() == expected
    assert tokens[1].content == '།'
    assert tokens[1].chunk_markers[tokens[1].chunk_type] == 'punct'
    assert tokens[1].tag == 'punct'


def test_non_max2():
    tok = Tokenizer(PyBoTrie(BoSyl(), 'empty', config=Config("pybo.yaml")))
    tok.trie.rebuild_trie()
    tok.trie.add('བཀྲ་ཤིས་', data='NOUN')
    tok.trie.add('བཀྲ་ཤིས་བདེ་ལེགས།', data='EXCL')
    tokens = tok.tokenize(PyBoTextChunks('བཀྲ་ཤིས་བདེ་བཀྲ་'))
    assert tokens[0].content == 'བཀྲ་ཤིས་'
    assert tokens[0].tag == 'NOUN'
    assert tokens[1].content == 'བདེ་'
    assert tokens[1].tag == 'non-word'
    assert tokens[2].content == 'བཀྲ་'
    assert tokens[2].tag == 'oov'


def test_non_max_end_of_string():
    tok = Tokenizer(PyBoTrie(BoSyl(), 'empty', config=Config("pybo.yaml")))
    tok.trie.rebuild_trie()
    tok.trie.add('བཀྲ་ཤིས་')
    tok.trie.add('བཀྲ་ཤིས་བདེ་ལེགས།')
    tokens = tok.tokenize(PyBoTextChunks('བཀྲ་ཤིས་བདེ་'))
    assert tokens[0].content == 'བཀྲ་ཤིས་'
    assert tokens[1].content == 'བདེ་'


def test_split_token():
    tok = BoTokenizer('empty')
    tok.tok.trie.rebuild_trie()
    tok.tok.trie.inflect_n_add('བདེ་བ་', 'NOUN', ins='data')
    tok.tok.trie.add('གཏན་', 'NOUN')
    tok.tok.trie.add('གྱི་', data='PART')
    tokens = tok.tokenize('གཏན་གྱི་བདེ་བའི་རྒྱུ།', split_affixes=False)
    assert len(tokens) == 5
    assert tokens[2].content == 'བདེ་བའི་'
    tokens = tok.tokenize('གཏན་གྱི་བདེ་བའི་རྒྱུ།')
    assert len(tokens) == 6
    assert tokens[2].content == 'བདེ་བ'
    assert tokens[3].content == 'འི་'


def test_bug1():
    tok = BoTokenizer('POS')
    string = 'བ་ཀུ་'
    tokens = tok.tokenize(string, debug=True)
    assert tokens


def test_bug2():
    tok = BoTokenizer('GMD')
    string = 'བྲ་གྲྀ་'
    tokens = tok.tokenize(string, debug=True)
    assert tokens
