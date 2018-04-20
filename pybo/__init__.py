from .trie import PyBoTrie
from .stringutils import PyBoTextChunks
from .tokenizer import Tokenizer
from .syllableutils import BoSyl
from .tokenutils import BoMatcher, TokenSplit, MatchSplit


def bo_tokenizer(string, profile='POS', split_affixes=True):
    """
    Convenience function to tokenize a given string.

    :param string: to be tokenized
    :param profile: profile for building the trie. (see config.yaml)
    :param split_affixes: separates the affixed particles into seperate tokens if True
    :return: list of pybo.tokenizer.Token objects
    """
    preprocessed = PyBoTextChunks(string)
    tok = Tokenizer(PyBoTrie(BoSyl(), profile=profile))
    return tok.tokenize(preprocessed, split_affixes=split_affixes)


__all__ = ['bo_tokenizer', 'PyBoTextChunks', 'PyBoTrie', 'Tokenizer',
           'BoSyl', 'BoMatcher', 'TokenSplit', 'MatchSplit']
