from pybo import *
import os

resource_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources", "lemmas")


input_str = ' མཐའི་རྒྱ་མཚོའི་གླིང་། ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་ཀཀ'
tok = BoTokenizer('POS', lemmatize=False)
tok.tok.trie.rebuild_trie()
tokens = tok.tokenize(input_str)


def test_lemmatize():
    lt = LemmatizeTokens(lemma_folder=resource_path)
    lt.lemmatize(tokens)
    assert tokens[1].content == 'འི་'
    assert tokens[1].lemma == 'གི་'
