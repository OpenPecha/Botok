# coding: utf-8
# from .adjusttokens import AdjustTokens
from .basictrie import BasicTrie
from .bochunk import BoChunk
from .bostring import BoString
from .bosyl import BoSyl
from .cqlmatcher import CQLMatcher
from .mergingmatcher import MergingMatcher
from .lemmatizetoken import LemmatizeTokens
from .pybochunk import PyBoChunk
from .pybotextchunks import PyBoTextChunks
from .pybotrie import PyBoTrie
from .replacingmatcher import ReplacingMatcher
from .splitaffixed import SplitAffixed
from .splittingmatcher import SplittingMatcher
from .sylcomponents import SylComponents
from .third_party import Query, parse_cql_query, replace_token_attributes
from .token import Token
from .tokenizer import Tokenizer
from .tokenmerge import TokenMerge
from .tokensplit import TokenSplit


VERSION = "0.2.2.1"


__all__ = ['BasicTrie', 'BoChunk', 'BoString', 'BoTokenizer', 'BoSyl', 'CQLMatcher', 'MergingMatcher',
           'LemmatizeTokens', 'PyBoChunk', 'PyBoTextChunks', 'PyBoTrie', 'ReplacingMatcher', 'SplitAffixed',
           'SplittingMatcher', 'SylComponents', 'Query', 'parse_cql_query', 'replace_token_attributes', 'Token',
           'Tokenizer', 'TokenMerge', 'TokenSplit']


class BoTokenizer:
    """
    Convenience class to tokenize a given string.

    """
    def __init__(self, profile, user_word_list=[], lemmatize=True):
        """
        :param profile: profile for building the trie. (see config.yaml)
        """
        self.lemmatize = lemmatize
        self.tok = Tokenizer(PyBoTrie(BoSyl(), profile=profile, user_word_list=user_word_list))

    def tokenize(self, string, split_affixes=True, phono=False, debug=False):
        """
        :param string: to be tokenized
        :param split_affixes: separates the affixed particles into seperate tokens if True
        :return: list of pybo.tokenizer.Token objects
        """
        preprocessed = PyBoTextChunks(string)
        tokens = self.tok.tokenize(preprocessed, split_affixes=split_affixes, phono=phono, debug=debug)
        if self.lemmatize:
            LemmatizeTokens().lemmatize(tokens)
        return tokens
