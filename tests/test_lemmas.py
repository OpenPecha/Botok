from pybo import *
from pathlib import Path

resource_path = Path().cwd() / "resources" / "lemmas"


input_str = ' མཐའི་རྒྱ་མཚོའི་གླིང་། ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་ཀཀ'
tok = WordTokenizer('POS')
tok.tok.trie.rebuild_trie()
tokens = tok.tokenize(input_str, lemmatize=False)


def test_lemmatize():
    lt = LemmatizeTokens(lemma_folder=resource_path)
    lt.lemmatize(tokens)
    assert tokens[1].content == 'འི་'
    assert tokens[1].lemma == 'གི་'
