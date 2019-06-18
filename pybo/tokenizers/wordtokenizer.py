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
    def __init__(self, profile, toadd_filenames=None, todel_filenames=None, lemma_folder=None, ignore_chars=None):
        """
        :param profile: profile for building the trie. (see config.yaml)
        """
        self.config_profile = Config("pybo.yaml")
        self.ignore_chars = ignore_chars
        self.lt = LemmatizeTokens(lemma_folder=lemma_folder)
        self.tok = Tokenize(Trie(BoSyl(),
                                 profile=profile,
                                 toadd_filenames=toadd_filenames,
                                 todel_filenames=todel_filenames,
                                 config=self.config_profile
                                 )
                            )

    def tokenize(self, string, split_affixes=True, lemmatize=True, debug=False):
        """
        :param string: to be tokenized
        :param split_affixes: separates the affixed particles into seperate tokens if True
        :param lemmatize: adds the lemma for every token
        :param debug: print debug info while parsing
        :return: list of pybo.tokenizers.Token objects
        """
        preprocessed = TokChunks(string, ignore_chars=self.ignore_chars)
        tokens = self.tok.tokenize(preprocessed, debug=debug)

        if split_affixes:
            SplitAffixed().split(tokens)

        # merge pa/po/ba/bo tokens with previous ones
        MergeDagdra().merge(tokens)

        if lemmatize:
            self.lt.lemmatize(tokens)

        return tokens
