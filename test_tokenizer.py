from BoTokenizer import Tokenizer


def test_tokenizer():
    tok = Tokenizer('empty')
    tok.trie.add('བཀྲ་ཤིས་')
    tok.trie.add('བཀྲ་ཤིས་བདེ་ལེགས།')
    tokens = tok.tokenize('བཀྲ་ཤིས་བདེ་')
    assert tokens[0].content == 'བཀྲ་ཤིས་'
    assert tokens[1].content == 'བདེ་'
