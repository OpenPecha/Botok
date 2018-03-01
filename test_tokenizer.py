from BoTokenizer import Tokenizer


def test_token_to_string():
    tok = Tokenizer('empty')
    tok.trie.add('བཀྲ་ཤིས་', data='NOUN')
    tokens = tok.tokenize('བཀྲ་ཤིས།')
    expected = """content: "བཀྲ་ཤིས"
char types: |cons|cons|sub-cons|tsek|cons|vow|cons|
type: syl
start in input: 0
length: 7
syl chars in content(བཀྲ ཤིས): [[0, 1, 2], [4, 5, 6]]
POS: NOUN"""
    assert tokens[0].to_string == expected
    assert tokens[1].content == '།'
    assert tokens[1].chunk_markers[tokens[1].chunk_type] == 'punct'
    assert tokens[1].partOfSpeech == 'punct'


def test_non_max2():
    tok = Tokenizer('empty')
    tok.trie.add('བཀྲ་ཤིས་', data='NOUN')
    tok.trie.add('བཀྲ་ཤིས་བདེ་ལེགས།', data='EXCL')
    tokens = tok.tokenize('བཀྲ་ཤིས་བདེ་བཀྲ་')
    assert tokens[0].content == 'བཀྲ་ཤིས་'
    assert tokens[0].partOfSpeech == 'NOUN'
    assert tokens[1].content == 'བདེ་'
    assert tokens[1].partOfSpeech == 'non-word'
    assert tokens[2].content == 'བཀྲ་'
    assert tokens[2].partOfSpeech == 'non-word'


def test_non_max_end_of_string():
    tok = Tokenizer('empty')
    tok.trie.add('བཀྲ་ཤིས་')
    tok.trie.add('བཀྲ་ཤིས་བདེ་ལེགས།')
    tokens = tok.tokenize('བཀྲ་ཤིས་བདེ་')
    assert tokens[0].content == 'བཀྲ་ཤིས་'
    assert tokens[1].content == 'བདེ་'

