from .tokenize import Tokenize
from pybo.modifytokens.splitaffixed import SplitAffixed
from pybo.modifytokens.mergedagdra import MergeDagdra
from pybo.modifytokens.lemmatizetokens import LemmatizeTokens

from ..tries.trie import Trie
from ..chunks.chunks import TokChunks
from ..textunits.bosyl import BoSyl
from ..config import Config


class WordTokenizer:
    """
    Convenience class to tokenize a given string.

    """
    def __init__(self, profile, modifs=None, mode='internal', ignore_chars=None):
        """
        :param profile: profile for building the trie. (see config.yaml)
        """
        config = Config()
        main, custom = config.get_tok_data_paths(profile, modifs=modifs, mode=mode)
        self.ignore_chars = ignore_chars
        profile = mode if mode == 'custom' else profile  # trie will be named custom if mode is custom
        self.tok = Tokenize(Trie(BoSyl, profile, main_data=main, custom_data=custom))

    def tokenize(self, string, split_affixes=True, debug=False):
        """
        :param string: to be tokenized
        :param split_affixes: separates the affixed particles into seperate tokens if True
        :param debug: print debug info while parsing
        :return: list of pybo.tokenizers.Token objects
        """
        preprocessed = TokChunks(string, ignore_chars=self.ignore_chars)
        tokens = self.tok.tokenize(preprocessed, debug=debug)

        if split_affixes:
            SplitAffixed().split(tokens)

        # merge pa/po/ba/bo tokens with previous ones
        MergeDagdra().merge(tokens)

        return tokens
