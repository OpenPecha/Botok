from .trie import PyBoTrie
from .stringutils import PyBoTextChunks
from .tokenizer import Tokenizer
from .syllableutils import BoSyl
from .tokenutils import BoMatcher, TokenSplit, MatchSplit


class BoTokenizer:
    """
    Convenience class to tokenize a given string.

    """
    def __init__(self, profile):
        """
        :param profile: profile for building the trie. (see config.yaml)
        """
        self.tok = Tokenizer(PyBoTrie(BoSyl(), profile=profile))

    def tokenize(self, string, split_affixes=True):
        """
        :param string: to be tokenized
        :param split_affixes: separates the affixed particles into seperate tokens if True
        :return: list of pybo.tokenizer.Token objects
        """
        preprocessed = PyBoTextChunks(string)
        return self.tok.tokenize(preprocessed, split_affixes=split_affixes)


__all__ = ['BoTokenizer', 'PyBoTextChunks', 'PyBoTrie', 'Tokenizer',
           'BoSyl', 'BoMatcher', 'TokenSplit', 'MatchSplit']
