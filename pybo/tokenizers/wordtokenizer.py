# coding: utf8
from pathlib import Path
import yaml

from .tokenize import Tokenize
from ..modifytokens.splitaffixed import split_affixed
from ..modifytokens.mergedagdra import MergeDagdra
from ..tries.trie import Trie
from ..chunks.chunks import TokChunks
from ..textunits.bosyl import BoSyl
from ..config import Config
from ..vars import TSEK, AA

part_lemmas = {}
# filename = Path(__file__).parent.parent / 'resources' / 'lemmas' / 'particles.yaml'
# with filename.open('r', encoding='utf-8-sig') as f:
#     parsed_yaml = yaml.safe_load(f.read())
#     for lemma, forms in parsed_yaml.items():
#         for form in forms:
#             part_lemmas[form] = lemma


class WordTokenizer:
    """
    Convenience class to tokenize a given string.

    """
    def __init__(self, profile='POS', modifs=None, mode='internal', ignore_chars=None):
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
        preprocessed.serve_syls_to_trie()
        tokens = self.tok.tokenize(preprocessed, debug=debug)

        if split_affixes:
            split_affixed(tokens)

        # merge pa/po/ba/bo tokens with previous ones
        MergeDagdra().merge(tokens)

        self._get_default_lemma(tokens)
        return tokens

    @staticmethod
    def _get_default_lemma(token_list):
        for t in token_list:
            # pass any token that is not a word
            if not t.text_unaffixed:
                continue

            # otherwise, check whether the aa needs to be added and if a tsek should be added
            if not t.lemma and t.pos != 'NON_WORD':
                if t.affix and not t.affix_host:
                    part = ''.join([''.join(syl) for syl in t.syls])
                    t.lemma = part_lemmas[part] + TSEK
                elif not t.affix and t.affix_host:
                    t.lemma = t.text_unaffixed + AA + TSEK if t.affixation['aa'] else t.text_unaffixed + TSEK
                else:
                    t.lemma = t.text_unaffixed if t.text_unaffixed.endswith(TSEK) else t.text_unaffixed + TSEK
