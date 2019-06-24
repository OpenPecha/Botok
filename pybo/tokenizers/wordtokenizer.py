# coding: utf8
from pathlib import Path
import yaml

from .tokenize import Tokenize
from ..modifytokens.splitaffixed import SplitAffixed
from ..modifytokens.mergedagdra import MergeDagdra
from ..tries.trie import Trie
from ..chunks.chunks import TokChunks
from ..textunits.bosyl import BoSyl
from ..config import Config
from ..vars import TSEK

part_lemmas = {}
filename = Path(__file__).parent.parent / 'resources' / 'lemmas' / 'particles.yaml'
with filename.open('r', encoding='utf-8-sig') as f:
    parsed_yaml = yaml.load(f.read(), Loader=yaml.SafeLoader)
    for lemma, forms in parsed_yaml.items():
        for form in forms:
            part_lemmas[form] = lemma


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
        # MergeDagdra().merge(tokens)

        self._get_default_lemma(tokens)
        return tokens

    @staticmethod
    def _get_default_lemma(token_list):
        for token in token_list:
            if not token.lemma:
                if token.affix:
                    part = ''.join([''.join(syl) for syl in token.syls])
                    token.lemma = part_lemmas[part] + TSEK
                else:
                    token.lemma = token.text_unaffixed