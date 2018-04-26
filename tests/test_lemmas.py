from pybo import *


input_str = ' མཐའི་རྒྱ་མཚོའི་གླིང་། ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་ཀཀ'
tok = BoTokenizer('POS')
tokens = tok.tokenize(input_str)


def test_lemmatize():
    lt = LemmatizeTokens()
    lt.lemmatize(tokens)
    assert tokens[1].content == 'འི་'
    assert tokens[1].lemma == 'གི'
