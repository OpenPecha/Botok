# coding: utf-8
from .adjusttokens import AdjustTokens
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
from .config import Config


VERSION = "0.2.19"


__all__ = ['AdjustTokens', 'BasicTrie', 'BoChunk', 'BoString', 'BoTokenizer', 'BoSyl', 'Config', 'CQLMatcher',
           'MergingMatcher', 'LemmatizeTokens', 'PyBoChunk', 'PyBoTextChunks', 'PyBoTrie', 'ReplacingMatcher',
           'SplitAffixed', 'SplittingMatcher', 'SylComponents', 'Query', 'parse_cql_query', 'replace_token_attributes',
           'Token', 'Tokenizer', 'TokenMerge', 'TokenSplit']


class BoTokenizer:
    """
    Convenience class to tokenize a given string.

    """
    def __init__(self, profile, toadd_filenames=[], todel_filenames=[], lemma_folder=None, ignore_chars=[]):
        """
        :param profile: profile for building the trie. (see config.yaml)
        """
        self.config_profile = Config("config.yaml")
        self.ignore_chars = ignore_chars
        self.lt = LemmatizeTokens(lemma_folder=lemma_folder)
        self.tok = Tokenizer(PyBoTrie(BoSyl(),
                                      profile=profile,
                                      toadd_filenames=toadd_filenames,
                                      todel_filenames=todel_filenames,
                                      config=self.config_profile
                                      )
                             )

    def tokenize(self, string, split_affixes=True, lemmatize=True, phono=False, debug=False):
        """
        :param string: to be tokenized
        :param split_affixes: separates the affixed particles into seperate tokens if True
        :return: list of pybo.tokenizer.Token objects
        """
        preprocessed = PyBoTextChunks(string, ignore_chars=self.ignore_chars)
        tokens = self.tok.tokenize(preprocessed, split_affixes=split_affixes, phono=phono, debug=debug)
        if lemmatize:
            self.lt.lemmatize(tokens)
        return tokens
