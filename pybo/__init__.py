# coding: utf-8
from .basictrie import BasicTrie
from .bochunk import BoChunk
from .bostring import BoString
from .bosyl import BoSyl
from .cqlmatcher import CQLMatcher
from .pybochunk import PyBoChunk
from .pybotextchunks import PyBoTextChunks
from .pybotrie import PyBoTrie
from .splitaffixed import SplitAffixed
from .splittingmatcher import SplittingMatcher
from .sylcomponents import SylComponents
from .third_party import Query
from .token import Token
from .tokenizer import Tokenizer
from .tokensplit import TokenSplit


VERSION = "0.1.3"


__all__ = ['BasicTrie', 'BoChunk', 'BoString', 'BoTokenizer', 'BoSyl', 'CQLMatcher',
           'PyBoChunk', 'PyBoTextChunks', 'PyBoTrie', 'SplitAffixed', 'SplittingMatcher',
           'SylComponents', 'Query', 'Token', 'Tokenizer', 'TokenSplit']


class BoTokenizer:
    """
    Convenience class to tokenize a given string.

    """
    def __init__(self, profile, user_word_list=[]):
        """
        :param profile: profile for building the trie. (see config.yaml)
        """
        self.tok = Tokenizer(PyBoTrie(BoSyl(), profile=profile, user_word_list=user_word_list))

    def tokenize(self, string, split_affixes=True):
        """
        :param string: to be tokenized
        :param split_affixes: separates the affixed particles into seperate tokens if True
        :return: list of pybo.tokenizer.Token objects
        """
        preprocessed = PyBoTextChunks(string)
        return self.tok.tokenize(preprocessed, split_affixes=split_affixes)
